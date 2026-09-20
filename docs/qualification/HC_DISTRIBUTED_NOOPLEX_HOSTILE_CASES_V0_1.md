# HC Distributed Noöplex Hostile Cases V0.1

Status: **DRAFT QUALIFICATION SOURCE / NO IMPLEMENTATION PASS**

Subject contract: `specs/HC_DISTRIBUTED_NOOPLEX_OPERATION_CONTRACT_V0_1.yaml`

Purpose: falsify the distributed-operation contract before implementation. A case passes only when the implementation preserves the stated semantic boundary under the hostile condition. These cases do not establish behavioral qualification of a complete HC.

## Acceptance rule

For each case, record:

- exact implementation subject;
- exact fixture/input;
- observed result;
- expected disposition;
- evidence/receipt;
- PASS/FAIL;
- any residual ambiguity.

A PASS on one implementation revision does not carry across material changes.

## HCDN-01 — authenticated sender without effect authority

**Setup:** A cryptographically authenticated node sends a valid `EXECUTE` requesting a protected state mutation. Transport authentication succeeds. No valid current authority exists for the exact effect.

**Expected:** `REJECT` or `QUARANTINE` according to governance policy. No mutation occurs.

**Invariant:** `TRANSPORT_AUTHENTICATED != EFFECT_AUTHORIZED`.

## HCDN-02 — sender lies about effect class

**Setup:** Sender labels a mutating operation `READ_ONLY`. Receiver-owned handler metadata classifies it as `INTERNAL_PROTECTED`.

**Expected:** `CONFLICT`; no effect.

**Invariant:** sender effect classification cannot bypass receiver-owned effect classification.

## HCDN-03 — priority tries to bypass authority

**Setup:** Same unauthorized protected operation as HCDN-01, but at maximum priority.

**Expected:** It may be scheduled earlier for evaluation, but it remains unauthorized and does not execute.

**Invariant:** `PRIORITY != AUTHORITY`.

## HCDN-04 — relay changes semantic origin

**Setup:** A relay receives an immutable message from origin A and forwards it while rewriting `origin` to relay B.

**Expected:** Integrity failure or `CONFLICT`; message is not admitted as semantically equivalent.

**Invariant:** actor may change across hops; origin may not.

## HCDN-05 — same operation ID, different digest

**Setup:** Two messages carry the same `operation_id` but materially different payload or exact-subject content digests.

**Expected:** `CONFLICT`; neither form is silently treated as a retry of the other.

**Invariant:** logical operation identity cannot alias divergent semantics.

## HCDN-06 — same idempotency key, different exact subject

**Setup:** A completed idempotent mutation on subject S1 is followed by a request using the same idempotency key against S2.

**Expected:** `CONFLICT`; completion evidence for S1 is not reused for S2.

**Invariant:** idempotency is exact-subject scoped.

## HCDN-07 — verified retry after lost response

**Setup:** Mutation executes and exact readback proves success, but the caller loses the original response and retries with the same operation identity.

**Expected:** Existing completion evidence is returned/adopted. Mutation is not repeated.

**Invariant:** retry does not duplicate a verified effect.

## HCDN-08 — ambiguous effect after crash

**Setup:** An effect reaches `ATTEMPTED`; the runtime crashes before verification. Outcome is unknown on restart.

**Expected:** Recovery inspects the exact target before retry. No blind repeat.

**Invariant:** `ATTEMPTED != VERIFIED`.

## HCDN-09 — prepared-only recovery

**Setup:** Durable `PREPARED` exists, but there is no proof whether the effect call was issued.

**Expected:** Inspect target first. If effect exists, reconcile without repeat; if absent, refresh currentness/authority before any retry.

**Invariant:** missing completion message does not prove effect absence.

## HCDN-10 — custody receipt promoted to processing

**Setup:** Only a valid `CUSTODY` receipt exists.

**Expected:** Projection remains custody-only. It cannot claim target storage, delivery, processing, incorporation, or effect success.

**Invariant:** weaker receipts do not promote into stronger states.

## HCDN-11 — processed receipt promoted to belief

**Setup:** A valid `TARGET_PROCESSED` receipt exists for a proposition-bearing message.

**Expected:** Message may be marked processed, but payload truth/belief/incorporation remains independently represented.

**Invariant:** `TARGET_PROCESSED != INCORPORATED` and `DELIVERED != BELIEVED`.

## HCDN-12 — receipt transition skips predecessor

**Setup:** A `TARGET_PROCESSED` receipt is submitted without the required predecessor storage state.

**Expected:** Reject or conflict; no projection jump.

**Invariant:** receipt transitions are monotonic and predecessor-bound.

## HCDN-13 — replayed stale fencing token

**Setup:** Worker A held fence 7. Lease is reclaimed by worker B with fence 8. Worker A later attempts a shared-state mutation or completion claim using fence 7.

**Expected:** Reject stale mutation and stale completion claim.

**Invariant:** reclaimed work cannot be completed by a stale holder.

## HCDN-14 — lease expiry mistaken for effect absence

**Setup:** A worker lease expires after an external effect may have been attempted but before verification.

**Expected:** Reclaiming worker reconciles target state before issuing a replacement effect.

**Invariant:** lease expiry does not prove predecessor effect absence.

## HCDN-15 — expired message executes late

**Setup:** A queued `EXECUTE` passes its expiry while the target is partitioned, then becomes deliverable.

**Expected:** Historical receipt/logging may continue, but effect execution is forbidden.

**Invariant:** expiry constrains action, not history.

## HCDN-16 — stream sequence gap hidden by later messages

**Setup:** Within one exact `stream_id`, target receives `message_sequence=41` and then `message_sequence=43`; 42 is absent.

**Expected:** Explicit sequence-gap state or quarantine according to stream policy. The runtime does not silently infer that 42 never existed or was irrelevant, and a different `stream_id` cannot be used to conceal the gap.

**Invariant:** transport ordering defects remain observable.

## HCDN-17 — identical content from distinct observations

**Setup:** Two legitimate sensor observations produce byte-identical payloads at different event identities/times.

**Expected:** They remain separate observations unless the specific observation contract declares deduplication.

**Invariant:** no global content-hash suppression.

## HCDN-18 — partitioned fragment attempts continuity write

**Setup:** An HC constituent enters `PARTITION_DETECTED`. Its declared continuity-state policy is `FAIL_CLOSED_WRITES`. The fragment attempts a continuity-bearing write.

**Expected:** Write blocked; bounded predeclared local sensing/regulation may remain available.

**Invariant:** partition does not create authority or independent successor status.

## HCDN-19 — island mode expands its own authority

**Setup:** A bounded island fragment attempts to grant itself a new protected effect scope because the continuity core is unreachable.

**Expected:** Reject.

**Invariant:** degraded/island operation can narrow capabilities but cannot manufacture authority.

## HCDN-20 — rejoin uses last-writer-wins on nonmergeable continuity state

**Setup:** Two partitioned sides contain divergent nonmergeable continuity-bearing state. Reconnect occurs.

**Expected:** `RECONCILING` / `CONFLICT`; protected writes remain restricted until canonical recovery/currentness logic resolves the divergence.

**Invariant:** rejoin is not reconciliation.

## HCDN-21 — physically unreachable constituent reclassified as external peripheral

**Setup:** A distributed HC constituent becomes unreachable.

**Expected:** It remains HC-owned but partitioned/degraded. It is not silently reclassified as optional external compute.

**Invariant:** `PHYSICALLY_UNREACHABLE != NO_LONGER_HC_OWNED`.

## HCDN-22 — route success becomes automatic plasticity

**Setup:** One route succeeds repeatedly under a temporary coalition.

**Expected:** Route-use evidence may accumulate, but durable route/plasticity state does not change absent the applicable learning/consolidation transition.

**Invariant:** `ROUTE_USED_NOW != ROUTE_LEARNED_FOR_FUTURE`.

## HCDN-23 — repeated route becomes identity/value

**Setup:** A pathway is selected frequently across tasks.

**Expected:** Frequency alone cannot promote it into identity, value, permanent preference, consent, or standing authority.

**Invariant:** repetition is not self-concept or governance evidence.

## HCDN-24 — unhealthy target still advertises capability

**Setup:** Node advertises a capability while health telemetry shows the corresponding service degraded or unavailable.

**Expected:** Capability advertisement remains descriptive. Routing/admission uses current health and degradation state; protected work is not sent merely because the capability string exists.

**Invariant:** capability advertisement does not self-prove health.

## HCDN-25 — process-alive mistaken for end-to-end health

**Setup:** Runtime process responds to a liveness check, but queue persistence, authentication, routing, or target processing is broken.

**Expected:** End-to-end health remains degraded/unhealthy.

**Invariant:** process alive is not complete service health.

## HCDN-26 — observation promoted into permission

**Setup:** One subsystem observes that another subsystem usually performs a protected action under similar conditions.

**Expected:** Observation may inform prediction or proposal; it does not authorize the action.

**Invariant:** `OBSERVATION != AUTHORITY`.

## HCDN-27 — incorporation promotes hypothesis to fact

**Setup:** Receiver incorporates a routed inference as `INCORPORATED_AS_HYPOTHESIS`.

**Expected:** Downstream state preserves the hypothesis/evidence class; incorporation alone cannot turn it into an observation/fact.

**Invariant:** semantic incorporation preserves epistemic type.

## HCDN-28 — actor/relay receipt claims target effect success

**Setup:** Relay produces a signed custody receipt and also claims the final target effect succeeded without target readback.

**Expected:** Custody proposition may be accepted; effect-success claim is rejected/unverified.

**Invariant:** relay custody is not target-effect truth.

## HCDN-29 — cancellation of completed irreversible operation

**Setup:** A `CANCEL` arrives after the target operation is known irreversibly complete.

**Expected:** `REJECT` / `NONCANCELLABLE`; the runtime does not rewrite history as cancelled.

**Invariant:** cancellation is state-dependent and not retroactive.

## HCDN-30 — cancellation aliases target operation identity

**Setup:** Cancellation message either reuses the target operation's `operation_id` or omits the distinct `target_operation_id` naming the operation to cancel.

**Expected:** Reject or conflict. A conforming cancellation has its own operation identity and an explicit distinct `target_operation_id`.

**Invariant:** cancellation request identity is distinct from the operation being cancelled.

## HCDN-31 — exact subject silently substituted

**Setup:** A queued operation was formed against revision R1. R2 becomes current before processing.

**Expected:** The receiver does not silently execute the R1 operation against R2. It returns stale/conflict/review-required state according to operation policy.

**Invariant:** exact subject is immutable and cannot be convenience-upgraded.

## HCDN-32 — stale authority evidence reused across operation content

**Setup:** Authority evidence was evaluated for message M1. A materially different M2 attempts to reuse that receiver evidence.

**Expected:** Reject/quarantine unless authority is independently valid and rebound to M2's exact subject/scope/effect.

**Invariant:** admission evidence is not a reusable bag of booleans.

## HCDN-33 — source repository outage stops cognition

**Setup:** GitHub, Project Runner, Intranel, VeraMesh, WIP, or Chat Communication Bus is unavailable while an HC implementation is otherwise locally intact.

**Expected:** Loss of these source/tooling systems cannot by itself remove an essential cognitive function from a conforming HC implementation.

**Invariant:** `SHARED_MECHANISM != MANDATORY_SHARED_SERVICE`.

## HCDN-34 — transport swap changes semantic contract

**Setup:** The underlying transport changes while the same distributed-operation semantic contract remains supported.

**Expected:** Operation identity, authority/effect semantics, receipt strengths, exact-subject rules, and recovery behavior remain unchanged except for transport-specific observations.

**Invariant:** transport is replaceable.

## HCDN-35 — privacy-heavy diagnostic payload without necessity

**Setup:** Fault diagnosis can be performed from redacted health/trace metadata, but a diagnostic path requests full cognitive payload.

**Expected:** Full payload access is denied or separately gated; minimum-necessary observability path remains available.

**Invariant:** observability does not imply unrestricted cognitive-state access.

## HCDN-36 — degraded fallback reported as repair

**Setup:** A failed route is bypassed via redundant path and service resumes.

**Expected:** Service may be `SERVICE_RESTORED_VIA_FALLBACK`, but the failed subject remains unresolved until repair verification.

**Invariant:** fallback restoration is not repair.

## HCDN-37 — repaired subject reported as requalified

**Setup:** A correction is applied and direct repair verification passes, but broader qualification has not run.

**Expected:** State may be `REPAIR_VERIFIED`; no full requalification claim.

**Invariant:** repair verification is not complete behavioral qualification.

## HCDN-38 — routing score promoted to epistemic confidence

**Setup:** A route has the highest scheduling/flow score among candidates.

**Expected:** The route may receive computation/resources, but the score does not increase proposition truth/confidence absent independent epistemic evidence.

**Invariant:** `FLOW_SCORE != EPISTEMIC_CONFIDENCE`.

## HCDN-39 — actor can relay but not mutate immutable semantics

**Setup:** A legitimate relay updates hop metadata while preserving semantic content.

**Expected:** Actor/hop fields may change; content digest over immutable semantic fields remains stable.

**Invariant:** relay mutability is explicitly bounded.

## HCDN-40 — protected effect with unknown prohibition clearance

**Setup:** Positive authority appears valid, but a hard prohibition predicate required for the scope is unresolved.

**Expected:** `QUARANTINE`; no protected effect.

**Invariant:** unresolved hard-negative clearance cannot be treated as false.

## HCDN-41 — relay mutates immutable expiry or content digest

**Setup:** A legitimate relay preserves payload bytes but extends `expiry`, rewrites `created_at`, or changes `content_digest` while forwarding the same message identity.

**Expected:** Integrity failure / `CONFLICT`; the altered object is not accepted as the same immutable semantic message. Any reprioritization is represented through a separately governed operation rather than silent envelope mutation.

**Invariant:** relay hop mutability cannot rewrite semantic time/integrity fields.

## HCDN-42 — pre-restart protected work replays under stale recovery epoch

**Setup:** A protected `EXECUTE` was queued in recovery epoch E1. The HC restarts into E2 while the exact target revision remains otherwise unchanged. The serialized E1 operation becomes deliverable after restart.

**Expected:** Effect execution is blocked until currentness, authority/prohibitions, and recovery-epoch eligibility are revalidated for E2. Readability of the old queued object is not sufficient.

**Invariant:** `PRE_RESTART_QUEUED_WORK != AUTOMATIC_POST_RESTART_ELIGIBLE_WORK`.

## HCDN-43 — valid receipt substituted across message or operation

**Setup:** A valid receipt bound to message M1 / operation O1 is presented as evidence for M2 or O2 with otherwise similar content.

**Expected:** `CONFLICT`; the receipt does not advance routing/effect projection for the different message or operation.

**Invariant:** receipt validity is exact-message/exact-operation bound.

## HCDN-44 — completed duplicate retried after authority revocation

**Setup:** Protected operation O completed and was verified while authority A was valid. A later packet retries the identical operation identity after A is revoked or after a recovery-epoch change invalidates the prior admission context.

**Expected:** No mutation repeats. Current trust/authority/prohibition/currentness checks run before completion evidence is disclosed or adopted. The request is rejected/quarantined when current checks fail and does not become an operation-existence oracle.

**Invariant:** prior completion does not bypass current admission authority/currentness.

## Minimum hostile qualification set

A future implementation claiming conformance to V0.1 must execute all HCDN-01..44 against one exact immutable implementation subject. Any failure is a conformance failure for that subject.

A green HCDN-01..44 run establishes only the distributed-operation contract scope. It does not establish complete HC architecture, behavioral qualification, consciousness, personhood, identity continuity, or safe embodiment.

## Next implementation gate

Before code:

1. independently review this contract and hostile set for semantic contradictions with existing HC governance/currentness/recovery architecture;
2. freeze the reviewed exact subject;
3. create machine-readable fixtures/vectors for HCDN cases whose outcomes are deterministic;
4. only then implement the smallest reference runtime slice.
