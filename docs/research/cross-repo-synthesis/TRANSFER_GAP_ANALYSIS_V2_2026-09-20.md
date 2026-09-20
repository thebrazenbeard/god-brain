# God Brain Portfolio Transfer-Gap Analysis V2 — 2026-09-20

Status: **RESEARCH / PROPOSED TRANSFERS / NO ARCHITECTURE PROMOTION**

## Post-draft review status

A first `HC_DISTRIBUTED_NOOPLEX_OPERATION_CONTRACT_V0_1` draft and 40-case hostile set were authored on `vera/portfolio-source-universe-v2-20260920` at exact head `17dc50e3e729f867e0222a565a26513b7f60f378`. Four independently reviewed exact contract blob `02efbfb981a190ebc8558e2510db860d24dd06a1` and hostile-set blob `aa699b82028eb2c601c88350fd151d96626fdc5c` and returned `CHANGES_REQUIRED_IMPLEMENTATION_BLOCKED`.

Blocking findings: missing cancellation target-operation identity; missing stream/sequence semantics; incomplete immutable-field classification; insufficient restart/recovery fencing; orphan `TARGET_DELIVERED`; under-specified receipt identity/binding; PREPARED-only recovery absent from the normative contract; and completed-retry handling ordered too early relative to current trust/authority/prohibition/currentness gates.

Therefore the originally reviewed distributed contract is **not main-ready**. Hephaestus returned a bounded repair at exact head `0e152584479734c00f9ae6ef73c8b5507b7c1caa`, contract blob `f6b3cd71620f9dad0c43c4a9b1e25a4327e12c8d`, hostile-set blob `9cdb0eb827e0a67b865bbe9230485753882c6188`. Reported author validation is YAML PASS, blocker consistency 8/8 PASS, repository tests 174/174 PASS, and diff check PASS. Four has now independently rereviewed that exact repaired subject and returned **CHANGES_REQUIRED**. Seven original blockers are materially closed. Remaining blocker `REREVIEW-F1`: PREPARED-only recovery must normatively distinguish exact intended effect already present -> reconcile without repeat, target absent -> refresh gates before retry, and divergent target -> conflict/stop; hostile coverage must explicitly falsify divergence. The subject remains **not implementation-ready and not main-ready**. Current gate: `HEPHAESTUS_R2_REPAIR -> FOUR_EXACT_SUBJECT_REREVIEW`.

Companion source universe: `docs/research/cross-repo-synthesis/SOURCE_UNIVERSE_V2_2026-09-20.md`.

Baseline capability state is taken from the current inspected HC implementation ledger and `CURRENT.md`. The executable surface includes a hardened reference kernel and a bounded cognitive core, but major domains remain unimplemented or only partially implemented. This analysis identifies where the wider repository portfolio may help close those gaps.

## Baseline claim discipline

The baseline explicitly separates:

`ARCHITECTURALLY_REQUIRED + SPECIFIED != IMPLEMENTED`

`REFERENCE_IMPLEMENTED != DEMONSTRATED_INTEGRATED`

`DEMONSTRATED_INTEGRATED != BEHAVIORALLY_QUALIFIED`

This document preserves those boundaries. A useful source mechanism is not an implementation result.

## Gap matrix

| Current HC gap | Current state | Strongest portfolio sources | Proposed V2 action | Ceiling |
|---|---|---|---|---|
| Distributed multi-process Noöplex execution | Specified; no full distributed runtime | `vera-mesh`, `intranel`, `chat-communication-bus`, `project-runner`, `wip` | Define HC-native node/operation/custody contract and fault semantics without requiring those repos at runtime | RESEARCH_TRANSFER_CANDIDATE |
| Specialized accelerator / model-graph runtime | Specified; no complete runtime | `mosaic`, `vera-os`, existing HC model-graph work | Run residency/continuity experiments; define specialist-state handoff and provenance contract | RESEARCH_TRANSFER_CANDIDATE |
| Fault tolerance / repair / partition behavior | Specified; no full distributed-organ implementation | `wip`, `project-runner`, `vera-mesh`, `project-achilles`, `bugops` | Transfer write-ahead effects, fencing, staged receipts, degraded-state semantics and localized fail-closed behavior | RESEARCH_TRANSFER_CANDIDATE |
| Resource / power / thermal control | Specified; no full runtime | HC engineering docs, `project-runner` budget model, `mosaic` residency budget, ABIL operational patterns | Generalize resource budgets and scheduling; do not confuse software budgets with physical power/thermal control | PARTIAL_METHOD_TRANSFER |
| Learned relational / causal model discovery | Partial world-model implementation; richer relational reasoning incomplete | `noema`, `world-zero`, `semanticatlas`, existing HC research | Add rival causal models, mechanism admission, ablation and relation-level coverage tests | RESEARCH_TRANSFER_CANDIDATE |
| Richer multimodal perception / adaptable I/O | Narrow capability admission only; optics/speech absent | `unvtrslr`, `skeletonkey`, `abil`, `spm` | Extend observation/grounding contracts before choosing perception models | RESEARCH_TRANSFER_CANDIDATE |
| Large-scale associative memory indexing / bounded replay | Deep-memory reference slice exists; large-scale replay/index incomplete | `deepmemorystorage`, `temporal`, `roots`, `semanticatlas` | Design ancestry-aware associative index and replay scheduler preserving contradiction/currentness | RESEARCH_TRANSFER_CANDIDATE |
| Richer allostasis and body calibration | Bounded homeostasis/body-schema slice exists | `abil`, `skeletonkey`, `selfimage` mechanism-only, HC somatics | Extend calibration/adaptation with evidence-bound sensor admission and morphology-neutral learning | RESEARCH_TRANSFER_CANDIDATE |
| Kinesis / embodiment | Only narrow effect-control invariants; no complete action system | `abil`, `skeletonkey`, `project-achilles`, HC body/action architecture | Build action gateway contracts from shadow/read-only through bounded actuation | RESEARCH_TRANSFER_CANDIDATE |
| Multi-party social learning and language integration | Bounded empathy/pragmatics slice; no broad language-generation integration | `empathy`, `personification`, `spm`, `unvtrslr`, `semanticatlas` | Extend scoped social models and semantic/pragmatic state without importing named relationships/personas | RESEARCH_TRANSFER_CANDIDATE |
| Psychological / learned behavior | Architecturally specified; not reference implemented | `noema`, prior conditioning review, `driftguard` as monitoring concept | Build learned-tendency acquisition/extinction/generalization runtime plus drift observability | RESEARCH_TRANSFER_CANDIDATE |
| Sexuality / embodied affect | Architecturally specified; not reference implemented | `sexuality` mechanism source; `orgasm` only as tightly scrubbed case study | Keep desire/arousal/attraction/consent/authority distinct; do not import named or intimate payloads | PRIVACY_BOUND_RESEARCH |
| Chronology | Partial timestamp/restart semantics only | `temporal`, `roots`, deep memory lineage | Implement event chronology with source ancestry, uncertainty and no semantic promotion | RESEARCH_TRANSFER_CANDIDATE |
| Behavioral qualification | No HC-wide behavioral qualification | `bugops`, `vera_model_training`, `driftguard`, `voss`, `masamune`, `hephaestus`, `world-zero` methodology | Build exact-subject qualification harness, drift checks, adversarial cases and regression closure | METHOD_TRANSFER_CANDIDATE |

## Proposed new transfer records

These are proposed continuations after the existing T01-T22 record set. They are **not admitted transfers yet**.

### T23 — distributed operation identity and custody

Sources:
- `vera-mesh`
- `intranel`
- `chat-communication-bus`

Targets:
- Noöplex Fabric
- routing
- integration-arbitration
- resolver
- distributed runtime

Candidate mechanism:
- distinguish semantic origin, current actor/relay, processing target and reply route;
- stable packet/message identity versus logical operation identity;
- exact-subject binding;
- transport/authentication distinct from action authority;
- staged custody/delivery/processed receipts;
- replay/idempotency conflict handling;
- observable sequence gaps and degradation.

Evidence inspected:
- `vera-mesh/docs/ARCHITECTURE.md` blob `a0cde52adef19611cbef9f0841a24062790c6441`;
- `intranel/spec/INTRANEL_1.md` blob `768ee95d715aef5e34a2e246c912eb4f612183f4`.

Transformation:
replace Vera/project/operator identities with HC subsystem/node identities; keep action authority and cognition internal to HC governance.

Excluded:
device-specific Vera identity, Tailscale, Android key storage, GitHub/Bus lane names, human-project authority.

Claim ceiling:
`DISTRIBUTED_RUNTIME_PROTOCOL_PATTERN`.

### T24 — crash-safe effect lifecycle and stale-worker exclusion

Sources:
- `project-runner`
- `wip`
- `bugops`

Targets:
- resolver
- fault tolerance
- runtime state custody
- action/effect pipeline

Candidate mechanism:
- dependency/currentness invalidation;
- immutable inputs and isolated writers where possible;
- persistent work/effect generations;
- leases and monotonic fencing;
- write-ahead `PREPARED -> ATTEMPTED -> VERIFIED|FAILED|AMBIGUOUS`;
- readback before retry after ambiguous failure;
- regression/closure evidence separate from acknowledgement.

Evidence inspected:
- `project-runner/docs/superpowers/specs/2026-09-17-project-runner-design.md` blob `2199332540c2243da2c5ad1aa49fb4aaffafa643`;
- `project-runner@main` tree `bc05812b560b4fcde3a362e72fba04c626cafac8`;
- `wip@main` tree `12a7c23dbe0482fd7bfe63659e54526778efef1e`;
- `bugops@main` tree `39eb19bcf7669466c22703fbae7cc226bd44f714`.

Transformation:
convert project/work execution semantics into generic HC internal effect and recovery semantics. Do not import human worker authority or GitHub-specific operations.

Claim ceiling:
`FAULT_RECOVERY_AND_EFFECT_INTEGRITY_PATTERN`.

### T25 — specialist residency and continuity across compute swaps

Sources:
- `mosaic`
- `vera-os`
- existing HC accelerator/model-graph architecture

Targets:
- specialized accelerators
- Noöplex model graph
- working-state handoff
- resource control

Candidate mechanism:
- logical whole distinct from resident parameter set;
- persistent core and separately loadable specialists;
- explicit provenance for specialist-produced state;
- structured/current working-state handoff across unload/reload;
- empirical VRAM residency accounting including weights, KV cache, activations and framework overhead;
- compare textual, structured and learned/latent handoff channels.

Evidence inspected:
- `mosaic/docs/ARCHITECTURE_V0.md` blob `061527dd5d6f7cbe4c08eeb92a43213f84b399f2`;
- Mosaic orientation recorded foundation head `f13a1740a6c3e0040af35a47582babd9a44e20ee`, but requires a fresh head check before exact transfer.

Transformation:
remove Vera/model-size identity assumptions and treat Mosaic as an experimental source, not an HC template.

Claim ceiling:
`MODEL_RESIDENCY_AND_HANDOFF_HYPOTHESIS`.

### T26 — mechanism admission, ablation and causal topology coverage

Sources:
- `world-zero`
- `noema`
- HC causal/world-model architecture

Targets:
- cognition
- learning/plasticity
- world model
- qualification

Candidate mechanism:
- rival causal structures rather than one privileged model;
- explicit mechanism admission gates;
- kill tests;
- ablation expectations;
- holdout isolation;
- declared-topology to executable-code coverage;
- frozen confirmatory metrics and exact run receipts.

Transformation:
use World Zero's scientific method, not its economic/ecological domain model.

Claim ceiling:
`CAUSAL_MODEL_EVALUATION_METHOD`.

### T27 — ancestry-aware cognitive provenance

Sources:
- `roots`
- `semanticatlas`
- `temporal`
- deep memory

Targets:
- cognition
- semantics
- current/deep memory
- resolver

Candidate mechanism:
record not merely a current proposition but its derivation chain: observations, transformations, prior hypotheses, corrections, supersession and unresolved alternatives.

Current blocker:
`roots` is presently only a one-file concept repository. The stronger architecture must be built from existing provenance systems rather than inferred from the name.

Claim ceiling:
`PROVENANCE_ANCESTRY_RESEARCH_DIRECTION`.

### T28 — behavioral drift observability and qualification lifecycle

Sources:
- `driftguard`
- `bugops`
- `vera_model_training`
- reviewer/debugger repositories
- World Zero evaluation method

Targets:
- metacognition
- qualification
- protected update/requalification
- developmental capability health

Candidate mechanism:
- exact-subject behavioral baselines;
- scheduled/triggered regression observations;
- distinguish drift observation from authority to overwrite state;
- fault report -> root cause -> corrective control -> regression evidence -> bounded closure;
- proxy/training readiness distinct from target-runtime qualification.

Hard prohibition:
a stored behavioral save-state must not automatically become current identity, memory, desire, consent, or control authority.

Current blocker:
`driftguard` is currently only a one-line concept README.

Claim ceiling:
`BEHAVIORAL_CONFORMANCE_METHOD`.

### T29 — anti-monoculture and replaceable infrastructure

Source:
- `discovery`

Targets:
- whole-system architecture
- Noöplex infrastructure boundaries
- external service boundaries

Candidate mechanism:
shared protocols may be standardized while implementations remain replaceable and failure domains remain independent.

Required invariant:

`SHARED_MECHANISM != MANDATORY_SHARED_SERVICE`

`PORTFOLIO_REUSE != PORTFOLIO_COUPLING`

This prevents God Brain from becoming a brittle wrapper around Project Runner, Lantern, Intranel, Bus/Radar, VeraMesh, or any other external repository.

Claim ceiling:
`ARCHITECTURAL_CONSTRAINT`.

## Priority implementation/research sequence

This is dependency order, not a claim that later items are less important.

1. **Distributed runtime contract (T23)** — because Noöplex multi-process execution is already an explicit HC gap and several mature protocol sources now exist.
2. **Crash/fault/effect integrity (T24)** — distributed execution without stale-worker, retry and ambiguous-effect controls would create an unsafe runtime.
3. **Specialist residency experiments (T25)** — test whether distributed/specialist compute can preserve coherent state before making stronger modular-agent claims.
4. **Causal-model evaluation hardening (T26)** — strengthen how learned relations and world models earn admission.
5. **Ancestry-aware provenance (T27)** — improve explanation, correction propagation and memory derivation.
6. **Behavioral qualification/drift lifecycle (T28)** — build a conformance layer that can test the resulting runtime without turning saved behavior into authority.
7. **Carry anti-monoculture constraint (T29) across every implementation.**

## Concrete next engineering subject

The strongest bounded next subject is:

`HC_DISTRIBUTED_NOOPLEX_OPERATION_CONTRACT_V0_1`

It should be an HC-native specification, not a wrapper around any external repo. It should minimally define:

- node/subsystem identity;
- message/event identity;
- logical operation identity;
- causal parentage;
- exact subject;
- origin/actor/target separation;
- routing versus incorporation;
- sender-declared versus receiver-classified effect type;
- authority/consent/effect boundaries;
- idempotency;
- sequence/gap semantics;
- staged custody/delivery/processing receipts;
- timeout/expiry/cancellation;
- partition/degraded behavior;
- replay/recovery;
- duplicate/conflict semantics;
- state ownership and persistence;
- conformance vectors.

The starting source trio should be `vera-mesh` + `intranel` + the existing HC routing/runtime architecture, with `project-runner` and `wip` supplying failure/recovery constraints.

## Non-actions

This pass does not authorize or perform:

- merge to `main`;
- deployment;
- provider or credential changes;
- identity/memory migration;
- installation;
- external service coupling;
- private payload transfer;
- model training;
- behavioral qualification claims.

The next frontier after this document is a second bounded repair of `REREVIEW-F1`, followed by fresh exact-subject Four rereview before implementation or main integration of the Noöplex contract.
