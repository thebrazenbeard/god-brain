"""Read-only Windows dialogue task diagnostics contract."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "dialogue_task_diagnostics.ps1"


class TaskDiagnosticTests(unittest.TestCase):
    def test_source_is_present_and_has_no_task_mutation_verbs(self):
        self.assertTrue(SCRIPT.is_file(), "Read-only diagnostic script must be versioned")
        source = SCRIPT.read_text(encoding="utf-8").lower()
        for forbidden in (
            "start-scheduledtask", "stop-scheduledtask", "set-scheduledtask",
            "register-scheduledtask", "unregister-scheduledtask",
            "stop-process", "start-process", "set-service", "start-service",
        ):
            self.assertNotIn(forbidden, source)

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell is required for this integration test")
    def test_missing_task_reports_unknown_cause_without_sensitive_fields(self):
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive",
             "-ExecutionPolicy", "Bypass", "-File", str(SCRIPT),
             "-TaskName", "GodBrainDiagnosticKnownMissingTask20261116",
             "-LoopbackPort", "18768"],
            capture_output=True, text=True, timeout=25, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema"], "GOD_BRAIN_TASK_DIAGNOSTIC_V1")
        self.assertIs(report["task"]["exists"], False)
        self.assertEqual(report["summary"], "TASK_NOT_FOUND")
        self.assertEqual(report["cause"], "UNKNOWN")
        self.assertIn("task_scheduler_history_enabled", report)
        self.assertIn("port_listener_present", report)
        for secret_key in ("arguments", "username", "password", "database_path",
                           "task_command_line", "task_executable_full_path"):
            self.assertNotIn(secret_key, result.stdout.lower())



    def _run_fixture(self, definitions):
        path = str(SCRIPT).replace("'", "''")
        script = definitions + "\n& '" + path + "' -TaskName FakeTask -TaskPath '\\' -LoopbackPort 18768"
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True, text=True, timeout=20, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_denied_queries_do_not_masquerade_as_absence(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 throw [System.UnauthorizedAccessException]::new('denied') }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 throw [System.UnauthorizedAccessException]::new('denied') }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 throw [System.UnauthorizedAccessException]::new('denied') }
""")
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertEqual(report["task_query_status"], "ACCESS_DENIED")
        self.assertEqual(report["listener_query_status"], "ACCESS_DENIED")
        self.assertIsNone(report["task"]["exists"])
        self.assertIsNone(report["port_listener_present"])
        self.assertEqual(report["cause"], "UNKNOWN")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_nonloopback_listener_is_not_reported_as_loopback(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='0.0.0.0'}
 [pscustomobject]@{LocalPort=10003;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_query_status"], "OK")
        self.assertEqual(report["listener_query_status"], "OK")
        self.assertEqual(report["listener_binding"], "WILDCARD_OR_NON_LOOPBACK")
        self.assertIs(report["port_listener_present"], True)
        self.assertEqual(report["summary"], "LISTENER_PRESENT_NON_LOOPBACK_NOT_HEALTH_PROOF")
        self.assertIn("last_run_local", report["task"])
        self.assertNotIn("last_run_utc", report["task"])

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_duplicate_task_results_fail_closed(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=$null}
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=$null} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$false} }
""")
        self.assertEqual(report["task_query_status"], "AMBIGUOUS")
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertIsNone(report["task"]["exists"])



    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_generic_object_not_found_is_not_verified_task_absence(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 $err = [System.Management.Automation.ErrorRecord]::new(
  [System.Exception]::new('provider failure'), 'OtherObjectNotFound',
  [System.Management.Automation.ErrorCategory]::ObjectNotFound, $null)
 $PSCmdlet.ThrowTerminatingError($err) }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_query_status"], "ERROR")
        self.assertIsNone(report["task"]["exists"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_single_task_with_missing_settings_is_not_validated(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=$null} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_query_status"], "INCOMPLETE")
        self.assertIs(report["task"]["exists"], True)
        self.assertIsNone(report["task"]["stop_if_going_on_batteries"])
        self.assertIsNone(report["task"]["restart_attempts_configured"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_equivalent_ipv6_loopback_and_port_scoped_query(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 if ($LocalPort -ne 18768) { throw 'Unscoped port lookup' }
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='0:0:0:0:0:0:0:1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["listener_query_status"], "OK")
        self.assertEqual(report["listener_binding"], "LOOPBACK_ONLY")
        self.assertEqual(report["summary"], "LISTENER_PRESENT_NOT_A_HEALTH_OR_PUBLIC_READINESS_PROOF")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_history_access_denial_is_explicit(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 throw [System.UnauthorizedAccessException]::new('denied') }
""")
        self.assertEqual(report["history_query_status"], "ACCESS_DENIED")
        self.assertIsNone(report["task_scheduler_history_enabled"])
        self.assertEqual(report["cause"], "UNKNOWN")


    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_invalid_ip_is_unknown_not_a_verified_exposure(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='not-an-ip'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["listener_binding"], "UNKNOWN")
        self.assertIs(report["port_listener_present"], True)
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertIn("LISTENER_BINDING_UNRESOLVED", report["risks"])

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_mixed_loopback_and_wildcard_are_exposure_risk(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'}
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='::'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["listener_binding"], "MIXED")
        self.assertEqual(report["summary"], "LISTENER_PRESENT_NON_LOOPBACK_NOT_HEALTH_PROOF")
        self.assertIn("LISTENER_MAY_BE_EXPOSED_BEYOND_LOOPBACK", report["risks"])


    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_null_settings_values_are_unknown_not_false(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$null;DisallowStartIfOnBatteries=$null;RestartCount=$null}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_query_status"], "INCOMPLETE")
        self.assertIsNone(report["task"]["stop_if_going_on_batteries"])
        self.assertIsNone(report["task"]["disallow_start_on_batteries"])
        self.assertIsNone(report["task"]["restart_attempts_configured"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_empty_task_state_is_not_validated(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_query_status"], "INCOMPLETE")
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_task_info_permission_failure_is_explicit(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 throw [System.UnauthorizedAccessException]::new('denied') }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_info_status"], "ACCESS_DENIED")
        self.assertIsNone(report["task"]["last_result_hex"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_history_denial_marks_summary_incomplete(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 throw [System.UnauthorizedAccessException]::new('denied') }
""")
        self.assertEqual(report["history_query_status"], "ACCESS_DENIED")
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell 5.1 required")
    def test_real_absent_port_reports_absent_not_provider_error(self):
        port = 18769
        probe = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
             f"Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue"],
            capture_output=True, text=True, timeout=12, check=False)
        if probe.stdout.strip():
            self.skipTest(f"port {port} currently occupied")
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy",
             "Bypass", "-File", str(SCRIPT),
             "-TaskName", "GodBrainDiagnosticKnownMissingTask20261116",
             "-LoopbackPort", str(port)],
            capture_output=True, text=True, timeout=25, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["listener_query_status"], "OK")
        self.assertEqual(report["listener_binding"], "ABSENT")
        self.assertIs(report["port_listener_present"], False)



    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_null_last_run_timestamp_does_not_report_info_ok(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=$null} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_info_status"], "INCOMPLETE")
        self.assertIsNone(report["task"]["last_result_hex"])
        self.assertIsNone(report["task"]["last_run_local"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_malformed_last_run_cannot_leave_partial_result(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime='not-a-timestamp'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_info_status"], "INCOMPLETE")
        self.assertIsNone(report["task"]["last_result_hex"])
        self.assertIsNone(report["task"]["last_run_local"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_history_nonboolean_false_string_not_coerced_to_true(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled='False'} }
""")
        self.assertEqual(report["history_query_status"], "INCOMPLETE")
        self.assertIsNone(report["task_scheduler_history_enabled"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")



    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_empty_success_task_query_is_not_verified_absence(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath) }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_query_status"], "INCOMPLETE")
        self.assertIsNone(report["task"]["exists"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertIn("TASK_QUERY_EMPTY_UNVERIFIED", report["risks"])

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_wrong_task_identity_fails_closed(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='OtherTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["task_query_status"], "INCOMPLETE")
        self.assertIsNone(report["task"]["exists"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertIn("TASK_IDENTITY_UNVERIFIED", report["risks"])

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_empty_success_tcp_query_is_not_verified_absence(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort) }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["listener_query_status"], "INCOMPLETE")
        self.assertIsNone(report["port_listener_present"])
        self.assertEqual(report["listener_binding"], "UNKNOWN")
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertIn("LISTENER_QUERY_EMPTY_UNVERIFIED", report["risks"])

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_nonlistening_tcp_row_is_not_listener(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18768;State='Established';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["listener_query_status"], "INCOMPLETE")
        self.assertIsNone(report["port_listener_present"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertIn("LISTENER_ROW_UNVERIFIED", report["risks"])

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),
                         "Windows PowerShell fixture")
    def test_wrong_port_tcp_row_is_not_listener(self):
        report = self._run_fixture("""
function Get-ScheduledTask { [CmdletBinding()]param($TaskName,$TaskPath)
 [pscustomobject]@{TaskName='FakeTask';TaskPath='\\';State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State,$LocalPort)
 [pscustomobject]@{LocalPort=18888;State='Listen';LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$true} }
""")
        self.assertEqual(report["listener_query_status"], "INCOMPLETE")
        self.assertIsNone(report["port_listener_present"])
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")


if __name__ == "__main__":
    unittest.main()