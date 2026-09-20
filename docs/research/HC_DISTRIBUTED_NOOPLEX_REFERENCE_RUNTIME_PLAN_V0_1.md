# Distributed Noöplex V0.1 — Reference Runtime Plan

Status: **PLANNING ONLY / NO IMPLEMENTATION CLAIM / NO MAIN PROMOTION**

Date: 2026-09-20

Target repository: `thebrazenbeard/god-brain`

## Exact reviewed source subject

This plan is bound to the independently reviewed R2 specification subject:

- source branch: `hephaestus/nooplex-v0-1-review-repairs-20260920`
- exact head: `bdac4346bed77949cf29a009179402d4d02796c7`
- contract: `specs/HC_DISTRIBUTED_NOOPLEX_OPERATION_CONTRACT_V0_1.yaml`
- contract blob: `f9f906f89b18ba95b8057978d087327567b1d489`
- hostile set: `docs/qualification/HC_DISTRIBUTED_NOOPLEX_HOSTILE_CASES_V0_1.md`
- hostile blob: `74dfcf09d89a6c4a78ce9835d982041a07cba9ff`
- Four exact-subject disposition: `INDEPENDENT_REVIEW_PASS`
- Four durable review Bus blob: `136e50ccd7f3e2da3c230c617e17b009011e67e8`

This exact subject remains a specification/hostile-set research subject. It is not runtime implementation, behavioral qualification, or merge authority.

## Gate sequence

The hostile-set contract defines the next sequence:

1. independent semantic review;
2. freeze the reviewed exact subject;
3. create machine-readable fixtures/vectors for deterministic HCDN cases;
4. implement the smallest reference runtime slice.

Step 1 is complete for the exact R2 subject above.

This plan covers Steps 2–4 without performing them.

## Step 2 — freeze the reviewed qualification subject

Create a machine-readable qualification-subject manifest that binds, at minimum:

- contract path and Git blob;
- hostile-set path and Git blob;
- exact reviewed source head;
- review disposition and durable review locator;
- declared source-binding blobs already present in the contract;
- HCDN case range and count;
- claim ceiling;
- implementation status;
- behavioral qualification status;
- supersession rule.

Required invariant:

`QUALIFICATION_SUBJECT_MOVEMENT => NEW_REVIEW_SUBJECT`

The freeze artifact must not be placed in a way that makes Four's existing exact-head review appear to attest a later changed head. It should describe the reviewed immutable blobs rather than retroactively extending the prior review receipt to new source.

## Step 3 — machine-readable HCDN vectors

Create a versioned fixture surface such as:

`fixtures/nooplex/v0_1/`

with one canonical case registry plus individual input/expected-output vectors where useful.

Recommended registry fields:

- `case_id`;
- `contract_clause_refs`;
- `fixture_kind`;
- `initial_state`;
- `input_envelopes`;
- `authority_state`;
- `currentness_state`;
- `target_readback`;
- `expected_routing_state`;
- `expected_incorporation_state`;
- `expected_effect_state`;
- `expected_receipt_chain`;
- `expected_error_or_conflict`;
- `must_not_occur`;
- `deterministic`;
- `notes`.

The fixture surface should preserve:

`FIXTURE_EXPECTATION != IMPLEMENTATION_RESULT`

and

`HOSTILE_CASE_PASS != BEHAVIORAL_QUALIFICATION`

### First deterministic fixture tranche

Start with cases whose result is contract-local and does not require a distributed physical environment:

- HCDN-01 authenticated sender without effect authority;
- HCDN-02 sender effect-class lie;
- HCDN-03 priority bypass attempt;
- HCDN-04 relay origin mutation;
- HCDN-05 operation-ID / digest conflict;
- HCDN-06 idempotency-key / exact-subject conflict;
- HCDN-07 verified retry;
- HCDN-08 ambiguous effect recovery;
- HCDN-09 PREPARED-only present/absent/divergent target outcomes;
- HCDN-10..12 receipt-strength progression;
- HCDN-13 stale fencing token;
- HCDN-14 lease expiry versus effect absence;
- HCDN-15 expired effect attempt;
- HCDN-16 stream sequence gap;
- HCDN-17 identical content / distinct observations;
- HCDN-22 route success versus plasticity;
- HCDN-23 repeated route versus identity/value;
- HCDN-26 observation versus permission;
- HCDN-27 hypothesis versus fact;
- HCDN-28 relay receipt versus target effect;
- HCDN-29 completed irreversible cancellation;
- HCDN-30 cancellation target-operation identity;
- HCDN-31 exact-subject substitution;
- HCDN-32 stale authority evidence;
- HCDN-34 transport substitution;
- HCDN-38 routing score versus epistemic confidence;
- HCDN-39 immutable semantic relay fields;
- HCDN-40 unknown prohibition clearance;
- HCDN-41 expiry/content-digest relay mutation;
- HCDN-42 stale recovery epoch;
- HCDN-43 receipt substitution;
- HCDN-44 completed duplicate after authority revocation.

Partition, health, privacy, and external-source-outage cases may still have deterministic model-level vectors, but they should remain separate from any later physical-distribution qualification.

## Step 4 — smallest reference runtime slice

The first runtime slice should implement only the semantics needed to execute the deterministic vectors. It should not attempt a complete distributed HC runtime.

Recommended components:

### 1. Envelope validator

Responsibilities:

- required and conditional field validation;
- immutable semantic-field classification;
- origin / actor / target / reply separation;
- `message_id` versus `operation_id`;
- cancellation `target_operation_id`;
- `stream_id` / `message_sequence`;
- `recovery_epoch`;
- expiry;
- content digest verification.

### 2. Receiver admission gate

Responsibilities:

- receiver-side effect classification;
- exact-subject validation;
- current trust/authority/prohibition checks;
- expiry/recovery-epoch checks;
- protected duplicate admission ordering.

The gate should consume injected authority/currentness state rather than invent a new God Brain authority system.

### 3. Routing / incorporation state machine

Keep distinct:

- custody;
- target storage;
- target processing;
- semantic incorporation.

Do not create a hidden `TARGET_DELIVERED` promotion.

### 4. Receipt engine

Responsibilities:

- exact receipt binding;
- monotonic receipt progression;
- no cross-message / cross-operation substitution;
- no promotion from processing to belief or effect truth.

### 5. Operation / idempotency store

Minimum semantics:

- one logical operation across retries;
- same operation + same digest -> replay existing disposition;
- same operation + changed digest -> conflict;
- same idempotency key + changed exact subject -> conflict;
- completed duplicate does not bypass refreshed current authority/currentness gates.

Persistence should be behind an interface. A test adapter may be in-memory; a durable adapter may be added later. Do not make a provider part of the cognitive contract.

### 6. Effect lifecycle engine

Implement:

`PREPARED -> ATTEMPTED -> VERIFIED | FAILED | AMBIGUOUS -> RECONCILED`

Required PREPARED-only inspection outcomes:

- intended effect observed -> `RECONCILE_WITHOUT_REPEAT`;
- target absent -> refresh gates before retry;
- divergent target -> `CONFLICT_STOP_NO_OVERWRITE_OR_BLIND_RETRY`.

Effects themselves should be represented by a deterministic test target/interface in the first slice, not real external mutation.

### 7. Sequence-gap tracker

Responsibilities:

- scope by stream and epoch;
- detect missing/reordered positions;
- do not equate transport order with event time;
- do not execute expired material work merely because it arrived later.

### 8. Fencing / restart model

Responsibilities:

- monotonic fence handling;
- stale fence rejection;
- recovery-epoch invalidation;
- revalidation of queued/in-flight material work after restart.

### 9. Partition-policy evaluator

The first slice needs policy evaluation, not a real distributed consensus system.

Represent declared policies such as:

- fail-closed protected writes;
- designated continuity core;
- quorum/consensus required;
- lease/epoch;
- mergeable-state-only island operation.

A fragment must not self-promote authority or successor identity.

## Explicitly out of scope for the first slice

- real network transport;
- Tailscale;
- GitHub as runtime transport;
- Chat Communication Bus as required runtime transport;
- consensus implementation;
- production database/provider integration;
- physical HC partition hardware;
- behavioral qualification;
- identity-specific memory;
- embodiment control;
- consciousness/personhood claims;
- deployment;
- merge or canonical promotion.

## Test architecture

The reference runtime should expose a deterministic harness that can load a vector and return:

- validation disposition;
- routing state;
- incorporation state;
- receipt state;
- effect lifecycle state;
- authority/currentness checks performed;
- target inspection result;
- conflict/error code;
- durable/replay decision;
- emitted audit events.

A conformance runner should fail closed if:

- any deterministic HCDN vector fails;
- any expected forbidden transition occurs;
- an unknown field/state is silently accepted where the contract requires rejection/quarantine/conflict;
- the tested implementation subject cannot be identified exactly.

## Recommended implementation order

1. freeze manifest;
2. fixture schema + HCDN-01..16 vectors;
3. envelope + admission + operation identity;
4. receipt + routing state machines;
5. effect lifecycle + idempotency;
6. HCDN-17..32 vectors;
7. sequence/recovery/fencing;
8. partition-policy evaluator;
9. HCDN-33..44 model-level vectors;
10. one exact-subject conformance run;
11. independent review of implementation and vectors;
12. only then consider wider distributed runtime work.

## Claim ceiling for the future reference slice

Even a full HCDN-01..44 PASS would establish only:

`DISTRIBUTED_NOOPLEX_V0_1_REFERENCE_CONFORMANCE_PASS`

It would not establish:

- complete HC implementation;
- production distributed operation;
- behavioral qualification;
- safe embodiment;
- AGI;
- consciousness;
- personhood;
- God-contact or simulation evidence.

## Current frontier

This plan is ready for review as a planning artifact only.

Do not start runtime implementation from this document until:

- the exact reviewed specification subject remains current for the intended implementation;
- the freeze/fixture design is accepted;
- any required main-integration/currentness prerequisites are reconciled;
- a bounded implementation assignment is explicitly opened.
