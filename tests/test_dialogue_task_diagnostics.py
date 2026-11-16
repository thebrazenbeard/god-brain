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
function Get-NetTCPConnection { [CmdletBinding()]param($State)
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
 [pscustomobject]@{State='Ready';Settings=[pscustomobject]@{
 StopIfGoingOnBatteries=$false;DisallowStartIfOnBatteries=$false;RestartCount=0}} }
function Get-ScheduledTaskInfo { [CmdletBinding()]param($InputObject)
 [pscustomobject]@{LastTaskResult=0;LastRunTime=[datetime]'2026-11-16 02:45:17'} }
function Get-NetTCPConnection { [CmdletBinding()]param($State)
 [pscustomobject]@{LocalPort=18768;LocalAddress='0.0.0.0'}
 [pscustomobject]@{LocalPort=10003;LocalAddress='127.0.0.1'} }
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
 [pscustomobject]@{State='Ready';Settings=$null}
 [pscustomobject]@{State='Ready';Settings=$null} }
function Get-NetTCPConnection { [CmdletBinding()]param($State)
 [pscustomobject]@{LocalPort=18768;LocalAddress='127.0.0.1'} }
function Get-WinEvent { [CmdletBinding()]param($ListLog)
 [pscustomobject]@{IsEnabled=$false} }
""")
        self.assertEqual(report["task_query_status"], "AMBIGUOUS")
        self.assertEqual(report["summary"], "OBSERVATION_INCOMPLETE")
        self.assertIsNone(report["task"]["exists"])


if __name__ == "__main__":
    unittest.main()