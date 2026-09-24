# DesktopCommander Workstation Mechanism Admission — 2026-09-24

Status: **research candidate / architectural admission only**.

## Decision

Admit the open-source repository:

`wonderwhy-er/DesktopCommanderMCP@550a0b3e31da18b7cf25e87ed840e3d953b6da42`

as an **ADAPT_WITH_PROVENANCE** source for workstation-control mechanisms.

The source is MIT licensed at the inspected exact head.

This admission applies to its local workstation agent, process/session manager, process tools, local history, and remote-device regression patterns.

It does **not** admit the proprietary hosted Remote Desktop Commander service or relay.

## Architectural use

The source is useful because it demonstrates the mature workstation behavior that Patrick expects from a build machine connection:

- persistent interactive process sessions;
- stdin to a live process;
- readback from active and completed processes;
- line/tail pagination;
- bounded process output;
- active-session enumeration;
- OS process observation and termination;
- recent local tool history;
- reconnect/readiness behavior.

Those mechanisms may be adapted into:

- `thebrazenbeard/WorkBridgeMCP` for workstation APIs;
- `thebrazenbeard/vera-mesh` for transport, identity, reconnect, and readiness composition.

The intended architecture is:

`ChatGPT -> VeraMesh -> WorkBridge -> workstation`

rather than copying the proprietary RDC hosted relay.

## Why adaptation is preferable to direct cloning

WorkBridge already imposes a stronger authority model than the inspected DesktopCommander command surface.

Current WorkBridge design supports:

- an explicit process enable/disable gate;
- named executable grants;
- exact executable SHA-256 binding;
- bounded working roots;
- bounded runtime and output;
- bounded arguments;
- reduced child environment;
- loopback/private endpoint constraints.

Those controls should remain authoritative.

The target therefore is:

`DesktopCommander session semantics + WorkBridge authority model + VeraMesh transport/readiness`

not “rebuild Desktop Commander exactly.”

## Provenance boundary

Copied or adapted mechanisms retain exact upstream provenance.

The upstream implementation is a source lineage, not independent evidence that the resulting WorkBridge implementation is correct.

`COPIED_LINEAGE != INDEPENDENT_CORROBORATION`

WorkBridge implementation claims require their own tests and exact-head review.

## Explicitly admitted source family

The exact source blobs admitted for study are recorded in:

`specs/DESKTOPCOMMANDER_WORKSTATION_SOURCE_ADMISSION_V0_1.yaml`

They include the terminal manager, improved process tools, process handlers, tool history, remote-device state/channel implementation, and process/readiness regression tests.

## Explicit exclusions

The following are outside this admission:

- proprietary Remote Desktop Commander hosted relay/service behavior;
- hosted account, usage, billing, telemetry, feedback, or onboarding systems;
- proprietary backend database coupling;
- an unrestricted shell-string execution interface;
- security/config mutation through the same general-purpose workstation tool surface;
- authority rules where an empty allowed-directory list becomes full-disk access.

## Known upstream failure modes

The upstream regression suite is especially valuable because it documents what **not** to inherit.

### Output flooding

The reference records a historical failure where unbounded terminal output eventually caused an `Invalid string length` exception and killed the shared MCP server.

Admission consequence:

- bound output retention;
- make eviction explicit;
- protect against a single giant no-newline stream;
- preserve the newest readable tail;
- one process must not destabilize unrelated chats.

### Long synchronous waits

The reference records cases where a long-running process keeps one MCP call pending until the client-level timeout.

Admission consequence:

- starting a persistent process must return a session handle promptly;
- interacting with it must use a bounded synchronous wait;
- continued work happens through output-read calls.

### False readiness

The reference regression tests document cases where a remote channel is online while the local executor is dead, or vice versa.

Admission consequence:

A composed workstation is “ready” only when the relevant route and executor are both usable.

VeraMesh should own this composed readiness predicate.

### Recovery races

The reference documents failure modes involving:

- restart on every routed call;
- no autonomous recovery after a failed restart;
- stale online writes overtaking offline state;
- an in-flight startup completing after shutdown.

These are hostile cases, not mechanisms to reproduce.

### Transport-specific auth clock behavior

The reference contains hosted-service-specific clock-skew/session workarounds.

Those are not admitted into WorkBridge. VeraMesh owns transport authentication and route readiness.

## Current downstream binding

WorkBridge Draft PR #10:

`573eee38c7a5ce314fcacdb2c7b7d9bbf3dcd8f3`

defines the current RDC-class parity contract and acceptance fixture against WorkBridge PR #8.

The implementation subject remains delegated to BT2 under the live Bus ownership rules.

## Claim ceiling

`EXTERNAL_WORKSTATION_MECHANISM_SOURCE_ADMISSION_ONLY`

This document establishes a bounded architectural source admission. It does not merge code, enable workstation process authority, install runtime components, or establish RDC parity by itself.
