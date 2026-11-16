# Windows dialogue task diagnostics (read-only)

The God Brain dialogue room is an **optional, private** local service. A passing source test does not prove that the installed service is healthy or that public ingress is authorized.

The tool at tools/dialogue_task_diagnostics.ps1 is a bounded read-only diagnostic for the Windows Task Scheduler instance and loopback TCP listener. It **does not** start, stop, install or modify a task or service; change port forwarding; read the dialogue database; perform any external HTTP request; inspect submissions; or expose the task's arguments, account, executable path, or credentials.

From a trusted local PowerShell terminal in the repository root:

    powershell.exe -NoProfile -NonInteractive -File .\tools\dialogue_task_diagnostics.ps1 -TaskName GodBrainDialogue -LoopbackPort 18765

The tool emits a single JSON object using schema GOD_BRAIN_TASK_DIAGNOSTIC_V1. The task is scoped by exact TaskName and TaskPath (default: root task folder). Each query has a separate status; an unavailable or ambiguous task query or failed listener query produces OBSERVATION_INCOMPLETE, not a false absence.

Listener bindings are classified as ABSENT, LOOPBACK_ONLY, WILDCARD_OR_NON_LOOPBACK, MIXED or UNKNOWN. A wildcard or non-loopback listener is an exposure risk, not proof of HTTP health. Even LOOPBACK_ONLY is not proof that HTTP health, Tailscale Funnel, moderation, privacy, backup/recovery, or public release gates have passed. A scheduler LastRunTime without trustworthy UTC provenance is labeled last_run_local with its DateTime kind; it is not silently converted to authoritative UTC. The cause stays UNKNOWN: Windows Task Scheduler's last-result code is evidence of an outcome, not a traceback.

TASK_CONFIGURED_TO_STOP_ON_BATTERY and TASK_CONFIGURED_NOT_TO_START_ON_BATTERY are configuration risks for a laptop expected to operate continuously. They do **not** prove that a past stop occurred on battery power. TASK_SCHEDULER_OPERATIONAL_HISTORY_DISABLED means historical task transitions cannot be reconstructed from that disabled log. Future logging or changing task power conditions is a separate host configuration change requiring explicit operator authority.

If the listener is absent, preserve the report and check existing Windows evidence and authorized, private application crash logs. A safe additional *isolated* reproduction uses a disposable SQLite database and distinct, confirmed-unused loopback port; it must never reuse the production database, modify the installed checkout, or bind to the production port. Do not repair an outage by blindly altering the scheduled task, restarting shared services, replacing local edits, changing Tailscale Funnel, or approving public ingress.

Tests: python -m unittest -v tests.test_dialogue_task_diagnostics. On Windows, this exercises a deliberately nonexistent task and injected denied, duplicate, and wildcard-provider cases. On other platforms, PowerShell integration cases are skipped. A real task report must be checked separately on the authorized host. A lexical mutation check supplements source review; it does not formally prove immutability.

**Release distinction:** production task reliability, public ingress readiness, a successful synthetic test, and a source-level security review are separate evidence classes. Public operation remains gated by exact-effect authority and qualified security/privacy, recovery, and rollback evidence.