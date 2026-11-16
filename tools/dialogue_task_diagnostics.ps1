# Read-only Windows task/listener evidence. Nothing is installed, stopped or changed.
[CmdletBinding()]
param(
    [ValidatePattern('^[A-Za-z0-9_.-]{1,80}$')]
    [string]$TaskName = 'GodBrainDialogue',
    [ValidatePattern('^\\(?:[A-Za-z0-9_. -]+\\)*$')]
    [string]$TaskPath = '\',
    [ValidateRange(1,65535)]
    [int]$LoopbackPort = 18765
)

$ErrorActionPreference = 'Stop'
function Get-FailureCategory {
    param($Record)
    $exception = $Record.Exception
    if ($exception -is [System.Management.Automation.CommandNotFoundException]) {
        return 'ERROR'
    }
    if ($exception -is [System.UnauthorizedAccessException] -or
        $exception.InnerException -is [System.UnauthorizedAccessException] -or
        $Record.CategoryInfo.Category -eq [System.Management.Automation.ErrorCategory]::PermissionDenied) {
        return 'ACCESS_DENIED'
    }
    if ($Record.CategoryInfo.Category -eq [System.Management.Automation.ErrorCategory]::ObjectNotFound) {
        return 'NOT_FOUND'
    }
    return 'ERROR'
}

$report = [ordered]@{
    schema = 'GOD_BRAIN_TASK_DIAGNOSTIC_V1'
    observed_utc = (Get-Date).ToUniversalTime().ToString('o')
    summary = 'OBSERVATION_INCOMPLETE'
    cause = 'UNKNOWN'
    task_query_status = 'ERROR'
    listener_query_status = 'ERROR'
    task = [ordered]@{
        exists = $null
        state = $null
        last_result_hex = $null
        last_run_local = $null
        last_run_time_kind = $null
        stop_if_going_on_batteries = $null
        disallow_start_on_batteries = $null
        restart_attempts_configured = $null
    }
    task_scheduler_history_enabled = $null
    port_listener_present = $null
    listener_binding = 'UNKNOWN'
    loopback_port = $LoopbackPort
    risks = @()
}
$risks = [System.Collections.Generic.List[string]]::new()

try {
    $tasks = @(Get-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath -ErrorAction Stop)
    if ($tasks.Count -eq 0) {
        $report.task_query_status = 'NOT_FOUND'
        $report.task.exists = $false
    } elseif ($tasks.Count -gt 1) {
        $report.task_query_status = 'AMBIGUOUS'
    } else {
        $report.task_query_status = 'OK'
        $report.task.exists = $true
        $task = $tasks[0]
        $report.task.state = [string]$task.State
        $report.task.stop_if_going_on_batteries =
            [bool]$task.Settings.StopIfGoingOnBatteries
        $report.task.disallow_start_on_batteries =
            [bool]$task.Settings.DisallowStartIfOnBatteries
        $report.task.restart_attempts_configured = [int]$task.Settings.RestartCount
        if ($report.task.stop_if_going_on_batteries) {
            $risks.Add('TASK_CONFIGURED_TO_STOP_ON_BATTERY')
        }
        if ($report.task.disallow_start_on_batteries) {
            $risks.Add('TASK_CONFIGURED_NOT_TO_START_ON_BATTERY')
        }
        try {
            $info = Get-ScheduledTaskInfo -InputObject $task -ErrorAction Stop
            $report.task.last_result_hex = ('0x{0:X8}' -f [uint32]$info.LastTaskResult)
            if ($null -ne $info.LastRunTime -and $info.LastRunTime.Year -ge 2000) {
                # Scheduler may return an unspecified DateTime, not a UTC instant.
                $report.task.last_run_local = $info.LastRunTime.ToString('yyyy-MM-ddTHH:mm:ss')
                $report.task.last_run_time_kind = [string]$info.LastRunTime.Kind
            }
        } catch {
            $risks.Add('TASK_LAST_RUN_INFO_UNAVAILABLE')
        }
    }
} catch {
    $report.task_query_status = Get-FailureCategory $_
    if ($report.task_query_status -eq 'NOT_FOUND') {
        $report.task.exists = $false
    } else {
        $risks.Add('TASK_QUERY_UNAVAILABLE')
    }
}

try {
    $operational = Get-WinEvent -ListLog 'Microsoft-Windows-TaskScheduler/Operational' -ErrorAction Stop
    $report.task_scheduler_history_enabled = [bool]$operational.IsEnabled
    if (-not $operational.IsEnabled) {
        $risks.Add('TASK_SCHEDULER_OPERATIONAL_HISTORY_DISABLED')
    }
} catch {
    $risks.Add('TASK_SCHEDULER_HISTORY_STATUS_UNAVAILABLE')
}

try {
    # Query all listening connections so absence of this port is not treated
    # as a provider ObjectNotFound error. Never emit socket addresses or PIDs.
    $listeners = @(Get-NetTCPConnection -State Listen -ErrorAction Stop |
                   Where-Object { $_.LocalPort -eq $LoopbackPort })
    $report.listener_query_status = 'OK'
    $report.port_listener_present = ($listeners.Count -gt 0)
    if ($listeners.Count -eq 0) {
        $report.listener_binding = 'ABSENT'
    } else {
        $loopbackCount = 0
        $nonLoopbackCount = 0
        foreach ($listener in $listeners) {
            $address = [string]$listener.LocalAddress
            if ($address -eq '::1' -or $address -match '^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$') {
                $loopbackCount++
            } else {
                $nonLoopbackCount++
            }
        }
        if ($loopbackCount -gt 0 -and $nonLoopbackCount -gt 0) {
            $report.listener_binding = 'MIXED'
        } elseif ($nonLoopbackCount -gt 0) {
            $report.listener_binding = 'WILDCARD_OR_NON_LOOPBACK'
        } else {
            $report.listener_binding = 'LOOPBACK_ONLY'
        }
    }
} catch {
    $report.listener_query_status = Get-FailureCategory $_
    $risks.Add('LISTENER_QUERY_UNAVAILABLE')
}

if ($report.task_query_status -notin @('OK', 'NOT_FOUND') -or
    $report.listener_query_status -ne 'OK') {
    $report.summary = 'OBSERVATION_INCOMPLETE'
} elseif ($report.listener_binding -in @('MIXED', 'WILDCARD_OR_NON_LOOPBACK')) {
    $report.summary = 'LISTENER_PRESENT_NON_LOOPBACK_NOT_HEALTH_PROOF'
    $risks.Add('LISTENER_MAY_BE_EXPOSED_BEYOND_LOOPBACK')
} elseif ($report.task_query_status -eq 'NOT_FOUND') {
    $report.summary = 'TASK_NOT_FOUND'
} elseif ($report.listener_binding -eq 'LOOPBACK_ONLY') {
    $report.summary = 'LISTENER_PRESENT_NOT_A_HEALTH_OR_PUBLIC_READINESS_PROOF'
} else {
    $report.summary = 'LOOPBACK_LISTENER_ABSENT'
    $risks.Add('CAUSE_OF_PROCESS_EXIT_UNDETERMINED')
}
$report.risks = $risks.ToArray()
# The allowlisted report deliberately omits command lines, executable paths,
# task account, database, bearer links, visitor data and external HTTP calls.
$report | ConvertTo-Json -Compress -Depth 6