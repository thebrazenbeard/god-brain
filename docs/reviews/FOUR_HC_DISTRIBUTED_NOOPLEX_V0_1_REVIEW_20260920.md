# Four — Independent Review: HC Distributed Noöplex V0.1

Status: **CHANGES_REQUIRED / IMPLEMENTATION_BLOCKED**

Review date: 2026-09-20

Reviewer identity: `Four`

Execution context: coordinator-controlled temporary BT2 role context reconstructed from durable Four state. This review is independent from the subject authorship path in the sense that Four did not author the reviewed contract/hostile blobs. It is not represented as a separate model/runtime instance.

## Exact reviewed subject

Repository: `thebrazenbeard/god-brain`

Source branch observed for review:
`vera/portfolio-source-universe-v2-20260920`

Exact branch head at review cut:
`17dc50e3e729f867e0222a565a26513b7f60f378`

Reviewed contract:
- path: `specs/HC_DISTRIBUTED_NOOPLEX_OPERATION_CONTRACT_V0_1.yaml`
- Git blob: `02efbfb981a190ebc8558e2510db860d24dd06a1`

Reviewed hostile set:
- path: `docs/qualification/HC_DISTRIBUTED_NOOPLEX_HOSTILE_CASES_V0_1.md`
- Git blob: `aa699b82028eb2c601c88350fd151d96626fdc5c`

The review is exact-subject-bound. It does not transfer to changed blobs.

## Source-binding integrity

All source bindings declared by the reviewed contract were read back at the exact declared Git blobs:

- HC typed routing: `7a812ecf44e7a18ee3492c3506e2305889cdacd2`
- HC runtime model: `17593d4e3601590d8af9a9dd72692c55cb128fc9`
- HC fault/partition contract: `e861d3ab13a4dadfa51c46deb77b03387243a68e`
- VeraMesh architecture: `a0cde52adef19611cbef9f0841a24062790c6441`
- VeraMesh authorization matrix: `c82c5c1c4c9de1fe249ea0b3c6a02346f3c869d5`
- VeraMesh receipt schema: `d2601d17c3013f6a176e012b91b41600fca6380e`
- Intranel semantics: `768ee95d715aef5e34a2e246c912eb4f612183f4`
- Project Runner design: `2199332540c2243da2c5ad1aa49fb4aaffafa643`
- WIP effect protocol: `1db3bda8f10d0d6b9eb473a3e7675d47dacfe96a`
- WIP recovery protocol: `43fa5b9b381e71d7b12b6c4405e22371501c2b68`
- WIP checkpoint protocol: `f6d5619d2c9b3ddda07ba6907ab5fefc3432eaa5`

Canonical HC governance/currentness/recovery contracts were also checked for contradictions, including:
- Authority/Consent/Effect Governance `ac435a6368ce081b3681b753638b016f83c410e4`
- Current-State Selection `3cab8681be77639deb759ac28bbe3d7dbd160c41`
- Conflict/Reconciliation `f1d491a3b0c1136a08420c8f116c6324edfdcebb`
- Noöplex Fabric `16e88b2146f72f4cbe3e6e367c69f82bde032f48`
- Bootstrap/Recovery/Safe Degradation `0caa1036adbe32fad8b74890fec2697e373a2539`
- HC Bootstrap Recovery V1 `21a9747db7da9d0dc48156360e074e1b7a4b5e65`

Source-binding result: **PASS**.

## Blocking findings

### F1 — CANCEL has no explicit target-operation field

The contract makes `CANCEL` a distinct operation kind and HCDN-30 requires the cancellation request to have its own `operation_id` instead of aliasing the target operation.

However, the envelope defines no `target_operation_id` or equivalent conditional field.

This contradicts the bound Intranel semantics, which explicitly require a distinct cancellation `operation_id` plus `target_operation_id`.

Required repair:
- define `target_operation_id`;
- require it for `CANCEL`;
- bind it into immutable semantic content and idempotency/operation digest semantics;
- preserve HCDN-29/30 against that explicit field.

### F2 — Sequence-gap qualification is not representable by the envelope

HCDN-16 requires detection of a missing sequence element such as 41, 43 with 42 absent.

The contract defines sequence-gap behavior but the message envelope has no normative `stream_id`, `message_sequence`, sequence scope, or rule saying when sequence is required.

The bound VeraMesh receipt schema explicitly binds `stream_id` and `message_sequence`.

Required repair:
- define stream identity and message sequence semantics;
- define when sequencing is required;
- define sequence domain/scope and reset/epoch semantics;
- bind receipt/projection behavior to the same sequence identity.

### F3 — Required semantic fields have incomplete mutability classification

The envelope requires `content_digest`, `created_at`, `expiry`, and `priority`, but none appears in either the mutable-hop field set or immutable-semantic field set.

At minimum:
- `content_digest` must be immutable because it is the integrity identity over immutable material content and HCDN-39 depends on its stability;
- `created_at` and `expiry` must not be silently relay-rewritten because HCDN-15 and recovery/currentness semantics depend on them;
- `priority` needs an explicit rule: either immutable or changed only through a separate governed reprioritization event.

Required repair:
- make mutability exhaustive for every envelope field;
- add hostile coverage for relay alteration of expiry/content digest and any permitted reprioritization mechanism.

### F4 — Restart/recovery epoch fencing is too narrow

The contract only requires `continuity_epoch` when an operation touches a continuity-bearing state family.

Canonical HC bootstrap/recovery semantics are broader: pre-restart queued or in-flight **material work** must be revalidated against a restart/recovery epoch or equivalent causal-currentness identity before resumption, and pre-restart authority does not automatically remain valid.

A non-continuity protected effect can therefore be stale after restart even when its exact subject has not changed.

Required repair:
- add a recovery/execution epoch or broaden the existing epoch field so all material `EXECUTE`/`CANCEL` operations crossing restart boundaries are fenced;
- require current authority/currentness revalidation after epoch change;
- add a hostile case for serialized pre-restart material work replay after recovery epoch change.

### F5 — `TARGET_DELIVERED` is an orphan routing state

The routing state machine contains both `TARGET_STORED` and `TARGET_DELIVERED`.

The receipt model defines:
`CUSTODY -> TARGET_STORAGE -> TARGET_PROCESSED`
with no `TARGET_DELIVERED` receipt/proof rule and no declared relationship between stored and delivered.

The bound VeraMesh receipt schema similarly has relay custody, recipient storage, and recipient processed—no independent delivered transition in the normative receipt chain.

Required repair:
- either remove `TARGET_DELIVERED` as a distinct normative state;
- or define its exact proof, transition order, signer/observer, and relationship to storage and processing.

### F6 — Receipt identity/binding is under-specified

The contract correctly says a receipt is an append-only proposition and weaker receipts cannot promote to stronger states, but it does not define the minimum fields that bind a receipt to one immutable message/operation subject.

The bound VeraMesh receipt schema binds receipt identity, message identity, envelope digest, stream identity, sequence, sender/recipient, signer, timestamp, and transition.

Without equivalent abstract requirements, a conforming implementation could satisfy the named receipt types while leaving cross-message receipt substitution ambiguous.

Required repair:
- define minimum receipt identity/binding semantics independent of any transport;
- include exact message/operation binding, immutable-content digest binding, issuer/signer/provenance, time, and transition/predecessor binding;
- add a hostile case for replaying a valid receipt against a different message/operation.

### F7 — PREPARED-only crash recovery is tested but not normatively specified

HCDN-09 requires target inspection before retry when only `PREPARED` exists.

The bound WIP effect/recovery protocols make this explicit because absence of `ATTEMPTED` does not prove the call was never issued.

The contract's normative `effect_lifecycle` currently specifies inspect-before-retry for unresolved `ATTEMPTED` state but does not state the equivalent `PREPARED` rule.

Required repair:
- move the PREPARED-only inspect-before-retry rule into the normative contract, not only the hostile suite.

### F8 — Duplicate completion evidence can become an authority/currentness shortcut

The contract says a completed retry returns existing completion evidence.

The bound Intranel semantics add an important condition: for mutating operations, duplicate recognition occurs only after the **current** message passes the receiver trust/authority/currentness boundary. Duplicate handling must not become an unauthenticated operation-existence oracle or a way to reuse stale authorization.

Required repair:
- explicitly order protected duplicate/retry handling after current authentication, authority, prohibition, exact-subject, expiry, and relevant recovery-epoch checks;
- state what bounded response is allowed when those current checks fail;
- add hostile coverage for an otherwise identical completed operation retried after authority revocation or recovery-epoch change.

## Non-blocking observations

The following major separations are aligned with the checked source universe:
- routing != authority;
- delivery/processing != semantic incorporation;
- priority != authority/truth;
- capability advertisement != health/permission;
- exact subject cannot be convenience-upgraded;
- external source/tooling repos are not mandatory runtime cognition;
- partition does not manufacture successor identity or authority;
- stale fencing token cannot commit/claim completion;
- lease expiry does not prove effect absence;
- fallback restoration != repair;
- repair verification != full requalification;
- route success != durable plasticity;
- rejoin != reconciliation;
- unresolved hard-prohibition clearance fails closed.

## Verdict

`REVIEW_PASS = FALSE`

`DISPOSITION = CHANGES_REQUIRED_BEFORE_IMPLEMENTATION`

No implementation should begin against contract blob
`02efbfb981a190ebc8558e2510db860d24dd06a1`
or hostile-set blob
`aa699b82028eb2c601c88350fd151d96626fdc5c`.

After repair, Four must review the new exact contract and hostile-set blobs. No finding in this review authorizes merge, deployment, provider mutation, training, installation, or another protected effect.
