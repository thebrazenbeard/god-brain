# God Brain Generic Coordination Core / Private Overlay Contract V0.1

Status: **RESEARCH SPECIFICATION / NO RUNTIME MIGRATION**

Transfer candidate: **T36 — GENERIC_COORDINATION_CORE_PRIVATE_OVERLAY_SPLIT**

Parent source universe: `f56f52b3606839147a12e68375612336fb9bbfdd`

Fresh donor cuts:

- `thebrazenbeard/ccb-core@0b542a78ebf5827a518e0731a63f17a7ac8a2727`
- `thebrazenbeard/chat-communication-bus@e0bcb5eb18630693de55a1af2066411c7af079bb`

## Purpose

God Brain needs durable coordination, routing, review requests, and exact-subject handoffs without conflating reusable coordination software with the private deployment state carried by the live Chat Communication Bus.

The donor split is explicit:

- **CCB Base / `ccb-core`** owns reusable, public-safe implementation mechanisms.
- **`chat-communication-bus`** remains the private coordination hub and deployment/branch overlay: writer lanes, topology, identities, receipts, messages, checkpoints, deployment coordinates, and private operational history.

God Brain consumes the distinction as an architecture rule. It does **not** make either repository a mandatory in-process cognitive dependency.

## Hard separations

```text
REUSABLE CODE AUTHORITY != PRIVATE DEPLOYMENT STATE
PUBLIC CORE != PRIVATE OVERLAY
PRIVATE DISCOVERY != CANONICAL GENERIC FIX
SOURCE PIN != DEPLOYMENT AUTHORITY
PRIVATE HISTORY != REUSABLE IMPLEMENTATION
PRIVATE TOPOLOGY != GENERIC ROUTING AUTHORITY
CORE QUALIFICATION != OVERLAY ACTIVATION
COORDINATION STATE != GOD BRAIN CANONICAL REPOSITORY STATE
```

A Bus message may coordinate work, preserve review evidence, or carry a delegation. It does not replace `god-brain/main` as canonical project state.

## Change flow

The only admitted generic-fix path is:

```text
discover generic/private fix
  -> classify core vs overlay
  -> sanitize private material
  -> reproduce in public core
  -> add deterministic regression
  -> qualify exact core cut
  -> pin overlay to qualified core
  -> reconcile private state separately
```

A fix discovered in the private repository is evidence of a candidate mechanism, not generic implementation authority.

## Public-core requirements

A reusable coordination mechanism must be reproducible without:

- private writer-lane history;
- named identity/persona payloads;
- private topology;
- credentials or provider secrets;
- deployment-specific receipts;
- operator-specific authority records.

If those are required to reproduce the mechanism, the candidate is not yet public/generic.

## Private-overlay requirements

The private overlay may bind a qualified `ccb-core` revision and add private state. It may not silently maintain a divergent second copy of generic runtime logic.

Private overlay state can remain canonical **within its deployment scope** without becoming reusable-code authority.

## Currentness

Every source pin is exact-cut evidence only. If `ccb-core` moves, prior qualification does not silently transfer. If the private overlay moves, its deployment/currentness claims must also be refreshed independently.

```text
REVIEWED_OLD_CORE_HEAD != REVIEWED_NEW_CORE_HEAD
CORE_SOURCE_CURRENTNESS != PRIVATE_DEPLOYMENT_CURRENTNESS
```

## Authority

A source pin or qualification receipt does not authorize:

- merge;
- deployment;
- route activation;
- topology changes;
- provider/credential/permission changes;
- private-history publication.

```text
SOURCE PIN != DEPLOYMENT AUTHORITY
QUALIFICATION != EFFECT AUTHORITY
```

## God Brain use

God Brain may adapt generic coordination mechanisms from `ccb-core` with provenance. The live `chat-communication-bus` remains the project coordination hub for work-bearing non-PR coordination under the ChatGPT project contract.

That relationship is service/coordination usage, not ontology:

```text
COORDINATION SERVICE != SEAT OF COGNITION
BUS MESSAGE != SCIENTIFIC EVIDENCE BY DEFAULT
```

## Claim ceiling

This contract is specification/fixture work. It does not migrate Bus code, publish private Bus material, activate routes, install runtime components, change provider state, or establish any simulation/contact claim.
