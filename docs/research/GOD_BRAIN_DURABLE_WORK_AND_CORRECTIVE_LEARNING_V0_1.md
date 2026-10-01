# God Brain Durable Work and Corrective Learning V0.1

Status: **RESEARCH SPECIFICATION / NO RUNTIME**

This contract absorbs reusable mechanisms from exact current cuts of Pre-Active, Project Runner, WIP, F.U.C.K.U.P., RepairTracker, BugOps, and Roots without creating runtime dependencies on those repositories.

## Core separations

```text
WORK INTENT != EXECUTION AUTHORITY
CHECKPOINT != CURRENT EXTERNAL STATE
PREPARED != ATTEMPTED
ATTEMPTED != EFFECT OCCURRED
EFFECT OCCURRED != VERIFIED EFFECT
OUTCOME UNKNOWN != SAFE TO RETRY
INCIDENT != ROOT CAUSE
REPRODUCTION != ROOT CAUSE
SOURCE CHANGE != DEPLOYED REPAIR
CORRECTION != HISTORY ERASURE
TEST PASS != GLOBAL CORRECTNESS
```

Long-running work receives a durable exact-subject identity, capability/authority ceiling, generation, and lease with monotonic fencing token. Recovery can reconstruct the work from checkpoints, but material mutable external state must be refreshed before resuming.

Consequential effects use a write-ahead journal. The durable transition is:

```text
PREPARED -> ATTEMPTED -> OBSERVED_APPLIED / OBSERVED_NOT_APPLIED / OUTCOME_UNKNOWN -> RECONCILED
```

If a response or worker dies after dispatch and effect status is uncertain, the next worker reconciles the target before retrying. A retry uses the exact stored request unless explicitly opened as new work.

Checkpoints keep observed, inferred, completed, unfinished, next action, and do-not-repeat material separate.

Corrective learning is versioned. A bad assumption/behavior may be superseded by a qualified correction or guardrail, but the original evidence remains historical provenance. Repairs are graphs: evidence -> hypotheses -> discriminating root-cause evidence -> mitigation/fix -> effect -> verification -> monitoring.

A regression fixture must distinguish the failure from the corrected behavior. Lack of recurrence is evidence only for its subject and observation window; it is not proof that the failure class can never happen again.

Optional external systems can strengthen execution, recovery, provenance, review, or repair, but presence never grants authority.

This specification does not start a daemon, run background work, perform effects, merge/deploy, or establish permanent prevention.
