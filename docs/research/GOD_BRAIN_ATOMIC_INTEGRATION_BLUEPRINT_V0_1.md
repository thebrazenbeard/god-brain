# God Brain Atomic Integration Blueprint V0.1

Status: **RESEARCH PLAN / NO CANONICAL PROMOTION**

Date: 2026-09-20

Repository: `thebrazenbeard/god-brain`

Observed canonical base:
- `main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

This document records a dependency and assembly plan only. All mutable PR/review/Bus state named below must be fresh-read before execution.

## Objective

Prepare a single coherent God Brain repository-level integration candidate after the relevant independent reviews return, instead of promoting partially compatible layers in an order that temporarily creates broken pointers, ambiguous authority, or conflicting currentness.

The integration problem now spans distinct surfaces:

1. reviewed God Brain foundation/currentness;
2. repository/HC-lineage rebinding;
3. God Brain governance;
4. ChatGPT Project interface/bootstrap;
5. project-file semantic ownership;
6. Project-instruction source/install separation;
7. future machine current pointer;
8. cross-file conformance.

These should converge deliberately.

## Current observed inputs

### Foundation bundle — PR #6

Observed:
- base: `c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`
- head: `c8aff4109e53930a15eed54ab2f00b746ec8b09c`
- prior classification: `MAIN_READY / MERGE_AUTHORITY_NOT_GRANTED`

Role in eventual integration:
- God Brain README;
- God Brain CURRENT;
- portfolio source-universe / transfer-gap / registry;
- reviewed Noöplex contract/hostile material included in that bundle.

Do not infer that this old review automatically covers a later composite head.

### Repository/governance rebinding proposal — PR #8

Observed:
- base: `c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`
- head: `930392a8edebebf089f98a5e65311bbfe2b12c6a`
- proposal file blob: `f8cc859f6d37a745453d9a6c092a09f31b287562`

Role:
- defines how `docs/REPOSITORY_MAP.md` must stop speaking as though God Brain is merely HC;
- preserves `WARDEN.md` as predecessor governance rather than silently rewriting it;
- recommends a separate God Brain governance contract.

### Governance contract — PR #10

Observed:
- base: `930392a8edebebf089f98a5e65311bbfe2b12c6a`
- head: `8c2bbce1e00d0cf79dc716d958a82b61e2824ed4`
- status at this observation: independent review pending.

Role:
- future candidate source for God Brain constitutional governance.

### ChatGPT Project interface — PR #11

Observed:
- base: `c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`
- head: `d80dcec08137d5fd1a8b5cafa62fb60d956e7ce2`
- status at this observation: independent review pending.

Role:
- root repo interface manifest;
- bootstrap;
- epistemic contract;
- routing/delegation contract;
- recovery/continuation contract;
- compact Project instruction source;
- interface conformance CI.

The exact PR #11 Project-file pack is currently installed as Project files and Patrick reports the Project instruction setting installed. That installation does not make PR #11 canonical.

`PROJECT_INSTALLATION != MAIN_PROMOTION`

### Project file architecture — PR #12

Observed:
- head: `215eb2ccd1ee8834377dcf98d862a54eaf4e5edb`
- status at this observation: independent review requested.

Role:
- semantic ownership/truth ceilings for README, CURRENT, root interface, governance, machine current pointer, checkpoints, review evidence, research files, and live operational state.

### Project instruction sync — PR #13

Observed:
- head: `25bbb837d22b5986582345a8d03094b231f93b62`
- status at this observation: independent review requested.

Role:
- source/install/current-chat distinction;
- installation receipts;
- deterministic text normalization;
- evidence ceiling for Project-setting verification.

## Core dependency DAG

```text
main@c0f6af7
   |
   +--> PR #6 foundation -------------------------------+
   |                                                    |
   +--> PR #8 rebinding proposal --> PR #10 governance |
   |                                                    |
   +--> PR #11 Project interface -----------------------+--> COMPOSITE ASSEMBLY
   |                                                    |
   +--> PR #12 file architecture -----------------------+
   |                                                    |
   +--> PR #13 instruction sync ------------------------+
                                                        |
                                                        v
                                            REPOSITORY MAP REBINDING
                                                        |
                                                        v
                                            MACHINE CURRENT POINTER
                                                        |
                                                        v
                                           CROSS-FILE CONFORMANCE
                                                        |
                                                        v
                                         FRESH EXACT-HEAD REVIEW
                                                        |
                                                        v
                                      PATRICK PROMOTION AUTHORITY ONLY
```

The arrows encode dependency, not automatic promotion.

## Why an atomic candidate is safer

Sequentially merging these layers can create known bad intermediate states.

Examples:

### Interface before governance

The root interface could point users toward a governance discovery model while inherited repository navigation still presents `WARDEN.md` as current repository authority.

### Governance before repository-map rebinding

A new God Brain governance contract could coexist with a top-level repository map that still names Noah/Warden as current integration authority, producing two apparent authority surfaces.

### Machine current pointer before target coexistence

A machine pointer cannot safely reference canonical governance/interface/currentness paths that do not yet coexist on the same candidate tree.

### CURRENT before repository-map rebinding

A correct God Brain `CURRENT.md` alongside an HC-current `docs/REPOSITORY_MAP.md` leaves the repository with contradictory entrypoints.

### Project installation before canonical promotion

This is already an intentionally tolerated temporary state because the installed pack is explicitly candidate-bound and review-pending. It must not be mistaken for canonical repository convergence.

## Proposed composite content

The eventual integration candidate should be constructed from fresh `main`, not by merging historical branches wholesale.

Candidate content should include only reviewed/admitted files.

### Layer A — foundation

Admit from the then-current reviewed foundation subject:
- `README.md`
- `CURRENT.md`
- God Brain cross-repo synthesis artifacts;
- source registry;
- any bounded reviewed architecture/specification files whose admission remains current.

### Layer B — repository identity rebinding

Create a God Brain-specific `docs/REPOSITORY_MAP.md` that:

- names God Brain as the repository;
- preserves HC architecture as inherited substrate;
- classifies HC qualification as predecessor evidence unless freshly rebound;
- classifies `WARDEN.md` as predecessor governance;
- removes predecessor-currentness language such as active Warden integration from God Brain present tense;
- distinguishes God Brain project-level architecture from HC substrate architecture;
- points to canonical God Brain governance only when that governance file is in the same candidate.

Do not rewrite `WARDEN.md` in the first integration pass.

### Layer C — God Brain governance

Promote a reviewed successor of the PR #10 governance contract to a canonical path such as:

`docs/governance/GOD_BRAIN_GOVERNANCE_V1.md`

Only after review findings are reconciled.

The canonical governance file must not retain research-only status language.

### Layer D — ChatGPT Project interface

Admit the reviewed Project-interface files from PR #11 or reviewed successors:

- `CHATGPT_REPO_INTERFACE.yaml`
- `architecture/chatgpt/BOOTSTRAP.md`
- `architecture/chatgpt/EPISTEMIC_CONTRACT.md`
- `architecture/chatgpt/ROUTING_AND_DELEGATION.yaml`
- `architecture/chatgpt/RECOVERY_AND_CONTINUATION.md`
- `architecture/chatgpt/PROJECT_INSTRUCTIONS.md`
- validator/tests/workflow as appropriate.

Before composite review, update candidate-only status fields to the correct canonical-candidate semantics without claiming already-merged state.

Any such status edit creates a new exact head and requires fresh review.

### Layer E — machine current pointer

Only after Layers A-D coexist, add:

`architecture/current/GOD_BRAIN_CURRENT.json`

It should resolve canonical source paths only.

It must not encode:
- open PRs;
- active reviewers;
- delegated subjects;
- Bus work queue;
- provider health;
- current chat;
- its own current commit SHA.

Truth ceiling:

`CURRENT_POINTER = CANONICAL_SOURCE_RESOLUTION_ONLY`

### Layer F — instruction installation state

Do **not** move installation receipts into canonical currentness.

If an installation receipt is admitted at all, preserve it as historical/observational state under a bounded state namespace.

The current observed receipt on PR #13 is research-state evidence, not proof of canonical source installation.

After canonical source promotion, a separate exact authorized Project-setting installation/verification cycle may be required.

`OLD_CANDIDATE_INSTALLATION != CANONICAL_SOURCE_INSTALLATION`

## Cross-file conformance requirements

The composite candidate must mechanically reject at least these contradictions.

### Identity

- README says God Brain.
- CURRENT says God Brain.
- repository map says God Brain.
- root interface says God Brain.
- HC files may continue saying HC within HC scope.

Reject:

`ROOT_GOD_BRAIN + REPOSITORY_MAP_HC_AS_WHOLE_REPO`

### Governance

- God Brain governance is the current project governance path.
- `WARDEN.md` is predecessor governance.
- no top-level file may grant present God Brain canonical effect authority to predecessor roles by implication.

Reject:

`GOD_BRAIN_GOVERNANCE + WARDEN_AS_CURRENT_GOD_BRAIN_AUTHORITY`

### Currentness

- `CURRENT.md` interprets canonical source.
- machine current pointer resolves canonical paths.
- mutable workflow state is externally fresh-read.

Reject open PR lists/review assignments/provider health from machine current pointer.

### Project interface

Every root-interface path must exist on the candidate tree.

No canonical interface path may point only to an unmerged research branch.

### Epistemic discipline

At minimum preserve:

`SIMULATION_HYPOTHESIS != SIMULATION_FACT`

`ANOMALY != CONTACT`

`AI_OUTPUT != EXTERNAL_MESSAGE`

`UNEXPLAINED != SUPERNATURAL`

`SELF_MODEL != CONSCIOUSNESS`

`COMPLEX_BEHAVIOR != PERSONHOOD`

### Review/currentness discipline

`HEAD_MOVEMENT -> PRIOR_REVIEW_HISTORICAL_ONLY`

No composite candidate inherits component PASS labels as a substitute for composite review.

## Required review-return reconciliation

For each pending review (#10, #11, #12, #13):

1. fresh-read exact source head;
2. verify returned review is bound to that head;
3. classify findings:
   - blocking semantic defect;
   - bounded repair;
   - nonblocking note;
   - provenance/currentness note;
4. do not edit the reviewed source branch unless the subject is returned from delegation;
5. if repairs are required, create or use the delegate-approved successor subject;
6. obtain fresh review on repaired exact head;
7. only admit review-clean content into composite assembly.

For Noöplex PR #9, keep its fixture semantics isolated from this repository-level integration blueprint unless its result materially changes foundation contents.

## Composite branch construction rule

When all required inputs are review-clean:

1. fresh-read `main`;
2. create one new bounded integration branch from that exact main head;
3. copy/adapt only the intended files from reviewed inputs;
4. do not merge source branches wholesale;
5. record source head/blob provenance for every admitted file;
6. make necessary cross-file status/path edits on the composite branch;
7. add repository-map rebinding;
8. add machine current pointer;
9. add cross-file conformance;
10. run all existing and new tests;
11. request independent exact-head composite review.

This composite review is a new evidence event.

`COMPONENT_REVIEW_PASS != COMPOSITE_REVIEW_PASS`

## Promotion gate

The composite may be classified `MAIN_READY` only if:

- all intended files are provenance-bound;
- no unresolved review blockers remain;
- cross-file conformance passes;
- ordinary repository tests pass;
- exact composite head receives independent review;
- no known pointer refers to absent paths;
- no top-level authority/currentness contradiction remains;
- protected-effect authority is unchanged.

Even then:

`MAIN_READY != MERGE_AUTHORITY`

Patrick must explicitly authorize the exact canonical promotion effect.

## Project-file reinstall consequence

If the canonical composite changes any of the installed Project-interface source bytes, the currently installed PR #11 pack becomes historical candidate installation evidence.

After canonical promotion, the Project-file/instruction surface should be regenerated from canonical source and reinstalled/reverified as a separate effect.

`CANONICAL_SOURCE_MOVEMENT -> PRIOR_INSTALLATION_NOT_CURRENTLY_VERIFIED`

## Explicit non-actions

This blueprint does not:

- merge any PR;
- modify `main`;
- modify delegated PR #9, #10, #11, #12, or #13 subjects;
- rewrite `WARDEN.md`;
- create the canonical governance file;
- create the canonical machine current pointer;
- change ChatGPT Project settings;
- claim any pending review has passed;
- claim the currently installed candidate pack is canonical.

## Next execution gate

While reviews are pending, safe work is limited to:

- improving this integration plan;
- building non-mutating conformance design/fixtures against synthetic candidate layouts;
- auditing other inherited root surfaces for God Brain/HC referent conflicts;
- preparing provenance manifests.

Once all required review returns are available:

`RECONCILE -> ASSEMBLE FRESH COMPOSITE -> TEST -> INDEPENDENT REVIEW -> CLASSIFY`
