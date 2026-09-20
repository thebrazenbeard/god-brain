# God Brain Project File Architecture V0.1

Status: **RESEARCH PROPOSAL / NO CANONICAL PROMOTION**

Date: 2026-09-20

Repository: `thebrazenbeard/god-brain`

Base inspected:
- `main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

Current God Brain interface candidate deliberately not modified by this proposal:
- Draft PR #11
- exact head `d80dcec08137d5fd1a8b5cafa62fb60d956e7ce2`

Current God Brain governance candidate deliberately not modified by this proposal:
- Draft PR #10
- exact head `8c2bbce1e00d0cf79dc716d958a82b61e2824ed4`

## Purpose

God Brain needs more than good files. It needs a rule for what each class of file is allowed to mean.

Without that rule, repository state tends to collapse into competing pseudo-authorities:

- a README starts carrying current operational status;
- `CURRENT.md` starts carrying volatile PR/review state;
- a continuation checkpoint starts behaving like memory;
- Project instructions grow into a second repository;
- a PR description becomes an accidental currentness database;
- a machine pointer starts claiming provider/runtime truth it cannot verify.

The target is a stratified file architecture in which every durable artifact has a bounded semantic job and an explicit truth ceiling.

## Source mechanisms inspected

These are source mechanisms, not mandatory runtime dependencies.

### ON_THEO ChatGPT repo interface

Source:
- repo: `thebrazenbeard/on-theo`
- ref: `architecture/chatgpt-project-interface-v1-20260920`
- file: `CHATGPT_REPO_INTERFACE.yaml`
- blob: `708aaf78bad59e5c6e015c19567e7b3f7e251cc4`

Useful mechanism:
- small root manifest;
- durable references to evidence/routing/provenance contracts;
- explicit currentness rule;
- protected-effect boundary.

Transfer disposition:
`ADAPT_WITH_PROVENANCE`

Do not copy ON_THEO's domain-specific authority/evidence taxonomy into God Brain.

### Vera current pointer

Source:
- repo: `thebrazenbeard/vera`
- main observed: `b7b8dcd1440a3b7147bec2cc35972f083e20f44a`
- file: `architecture/identity/WORKFLOW_CONTINUITY_CURRENT.json`
- blob: `aad696077e22bd05d19fb9e05acbc326a5f32908`

Useful mechanism:
- one small machine-readable pointer resolves the current source contract;
- the pointer explicitly states a truth ceiling;
- source routing currentness is kept separate from proof of live ChatGPT Project/runtime consumption.

Transfer disposition:
`ADAPT_WITH_PROVENANCE`

Key transferable rule:

`CURRENT_POINTER != LIVE_RUNTIME_PROOF`

### Radar canonical-current and recovery split

Source:
- repo: `thebrazenbeard/chat-communication-bus`
- main observed: `aeab0f04fc9b4bd7c2945c9a53011c53fac809b4`
- `architecture/contracts/RADAR_CURRENT.json` blob `e416e89ee5b8f2cde19659729936e122cf9ed23b`
- `docs/operator/RECOVERY.md` blob `c56e2df50597a2ee559c75860d328657837e6f5f`
- `docs/protocol/RECOVERY_CHECKPOINT_NAMESPACE_V1.md` blob `37fba6a9be1651285799a7b91e28c01175954b4b`

Useful mechanisms:
- canonical source/current pointer separated from recovery procedure;
- provider state is explicitly noncanonical;
- recovery does not guess unavailable state;
- checkpoints use their own namespace and do not consume ordinary message identity;
- a checkpoint is continuity metadata, not ordinary coordination or authority.

Transfer disposition:
`ADAPT_WITH_PROVENANCE`

## Proposed God Brain file strata

### Stratum 0 — root discovery manifest

Target:
`CHATGPT_REPO_INTERFACE.yaml`

Job:
- identify repository/project/primary coordinator;
- identify canonical branch and Bus;
- point to durable contracts;
- encode minimal stable invariants;
- tell a fresh execution surface how to reconstruct.

Allowed claims:
- stable project identity;
- canonical source locations;
- protected-effect classes;
- bootstrap paths;
- role split;
- freshness requirement.

Forbidden claims:
- current open PR list;
- current delegated subject list;
- latest review verdicts;
- live provider/runtime status;
- latest continuation checkpoint;
- transient next task.

Truth ceiling:

`ROOT_MANIFEST = DISCOVERY_AND_BOOTSTRAP_CONTRACT`

`ROOT_MANIFEST != OPERATIONAL_STATE_DATABASE`

### Stratum 1 — constitutional contracts

Targets include future canonical forms of:
- God Brain governance;
- epistemic/scientific policy;
- routing/delegation/collision policy;
- privacy/provenance policy;
- protected-effect rules.

Job:
define stable rules that should survive individual chats and ordinary frontier movement.

These files should change less frequently than currentness pointers.

Truth ceiling:

`CONSTITUTIONAL_RULE != CURRENT_OPERATIONAL_FACT`

A governance contract can say how reviews must work; it cannot say a particular PR is still reviewed without fresh exact-head evidence.

### Stratum 2 — machine-readable canonical current pointer

Proposed future path:
`architecture/current/GOD_BRAIN_CURRENT.json`

This should be added only after the project-interface/governance semantics are independently reviewed and a bounded implementation candidate is prepared.

Job:
resolve the currently canonical God Brain source contracts on `main`.

Candidate fields:

```json
{
  "schema": "GOD_BRAIN_CURRENT_POINTER_V1",
  "repository": "thebrazenbeard/god-brain",
  "canonical_branch": "main",
  "project_interface_path": "CHATGPT_REPO_INTERFACE.yaml",
  "governance_path": "docs/governance/GOD_BRAIN_GOVERNANCE_V1.md",
  "epistemic_contract_path": "architecture/chatgpt/EPISTEMIC_CONTRACT.md",
  "routing_contract_path": "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml",
  "human_currentness_path": "CURRENT.md",
  "truth_ceiling": "Resolves canonical source contracts only; mutable PR/review/delegation/provider/runtime state must be freshly read."
}
```

The pointer should not embed its own unknowable current commit SHA.

It should not list open PRs, active reviews, Bus assignments, or provider health.

Those are mutable external observations.

`CURRENT_POINTER != CURRENT_GIT_OBSERVATION`

`CURRENT_POINTER != REVIEW_RECEIPT`

`CURRENT_POINTER != DEPLOYMENT_READBACK`

### Stratum 3 — human canonical currentness

Target:
`CURRENT.md`

Job:
provide a human-readable interpretation of what the current canonical repository means.

The reviewed foundation-bundle candidate already moves in the right direction by stating that repository PR/review/merge status is mutable external Git state and should not be encoded as durable currentness.

Recommended long-term content:
- current project identity;
- current canonical architectural layers;
- current source-lineage classification;
- canonical research/architecture contracts;
- known durable claim ceilings;
- durable next-stage methodology, where promotion-stable.

Avoid:
- pending PR numbers as “current state”;
- temporary reviewer assignments;
- mutable branch heads except as historical evidence;
- “waiting on reviewer X”;
- live provider health;
- current chat frontier.

A useful rule:

`CURRENT_MD = CANONICAL_INTERPRETATION_OF_MAIN`

not:

`CURRENT_MD = TODAY'S_WORK_QUEUE`

### Stratum 4 — mutable operational state

Sources:
- GitHub PR/branch/head state;
- review surfaces;
- Chat Communication Bus;
- CI status;
- provider/runtime readback where applicable.

Job:
answer questions such as:
- what is open now?
- which exact head is under review?
- what is delegated?
- which blocker is unresolved?
- what CI is passing on the current head?
- what is actually deployed or reachable?

This stratum should generally be read live rather than copied into canonical narrative files.

`MUTABLE_OPERATIONAL_STATE -> FRESH_READ`

### Stratum 5 — review evidence

Review evidence should remain bound to:
- repository;
- exact head;
- base where applicable;
- exact files/blobs/subject;
- reviewer;
- role/independence state;
- disposition;
- limitations.

Review evidence should not live inside the reviewed subject in a way that makes the subject self-certifying.

A canonical artifact may point to external review evidence after promotion, but the review result remains historically exact-subject bound.

`REVIEW_RECEIPT != SUBJECT_SELF_ATTESTATION`

### Stratum 6 — continuation/checkpoint state

Target namespace:
`state/continuation/`

Job:
accelerate reconstruction of a replacement execution surface.

A continuation is allowed to record the last observed frontier and pointers to durable evidence.

It must never become:
- canonical currentness;
- worker identity;
- merge authority;
- review carry-forward;
- live provider proof.

`CHECKPOINT = RECOVERY_ACCELERATOR`

`CHECKPOINT != MEMORY_AUTHORITY`

`CHECKPOINT != CANON`

### Stratum 7 — research and proposals

Targets:
`docs/research/**`
and other explicitly research-scoped surfaces.

Job:
explore candidate mechanisms without pretending they are adopted architecture.

A research proposal may describe:
- future file paths;
- future governance;
- future runtime;
- future experiments;
- future provider integration.

Existence does not imply adoption.

`RESEARCH_PROPOSAL != CANONICAL_CONTRACT`

### Stratum 8 — specification / fixture / implementation / qualification

These must remain distinct even when colocated in one repository:

- architecture/specification;
- deterministic fixture;
- reference implementation;
- production implementation;
- deployment evidence;
- behavioral qualification;
- external scientific validation.

No file naming convention should erase those stage boundaries.

## Proposed ownership matrix

### `README.md`

Owns:
- project identity;
- mission;
- high-level scope;
- navigation.

Must not own:
- current work queue;
- review status;
- provider health;
- exact deployment state.

### `CHATGPT_REPO_INTERFACE.yaml`

Owns:
- fresh-chat discovery;
- bootstrap routing;
- stable role/currentness/authority boundaries.

Must not own:
- transient operational state.

### `CURRENT.md`

Owns:
- human-readable canonical interpretation of `main`.

Must not own:
- volatile external workflow state.

### `architecture/current/GOD_BRAIN_CURRENT.json`

Future proposed owner of:
- machine-readable canonical source pointers.

Must not own:
- live operational truth.

### `docs/governance/GOD_BRAIN_GOVERNANCE_V1.md`

Future proposed owner of:
- adopted God Brain governance.

Must not rewrite:
- `WARDEN.md` predecessor history.

### `WARDEN.md`

Owns:
- HC predecessor governance provenance.

Must not be interpreted as:
- current God Brain authority unless a later canonical God Brain artifact explicitly and narrowly adopts a provision.

### `state/continuation/**`

Owns:
- recovery snapshots.

Must not own:
- canon or live currentness.

### Bus / PR / CI

Own:
- current coordination/review/automation evidence within their actual scope.

Must not own:
- God Brain architecture by mere presence.

## Anti-patterns to prohibit

1. **Self-updating CURRENT file loop**

A file cannot reliably contain its own current commit SHA without another successor commit changing that fact.

Prefer external Git observation or a pointer whose truth ceiling does not pretend self-reference is solved.

2. **PR-description currentness**

PR descriptions are useful subject declarations, not canonical state databases.

3. **Checkpoint promotion by convenience**

A continuation is not authoritative merely because it is the easiest reconstruction source.

4. **Instruction duplication**

Do not copy the same detailed rules into:
- Project instructions;
- bootstrap docs;
- governance;
- README;
- CURRENT;
- continuation templates.

Choose one owner and reference it.

5. **Provider projection as canon**

Provider/runtime state may be operational evidence, but Git canonical source and deployment/runtime truth are distinct.

6. **Research proposal path dependency**

A canonical bootstrap file should not require a path that exists only on an unmerged research branch.

7. **Review status embedded as durable architecture**

Review status changes when heads move. Keep exact review evidence externally bound.

## Proposed promotion discipline

When these strata are eventually implemented canonically:

1. independently review the project-interface contract;
2. independently review the God Brain governance contract;
3. reconcile the repository-map rebinding against those reviewed semantics;
4. create one bounded implementation candidate from fresh then-current `main`;
5. add the machine current pointer only when its target canonical paths actually coexist in that candidate;
6. validate all pointers mechanically;
7. verify `README.md`, `CURRENT.md`, repository map, governance, and root interface do not duplicate or contradict ownership;
8. obtain fresh exact-head independent review;
9. require Patrick's explicit authorization before canonical promotion.

If sequential promotion would temporarily leave broken pointers or ambiguous authority, prefer one atomic reviewed bundle.

## Recommended next project-file frontier

After PR #10 and PR #11 reviews return:

`RECONCILE_REVIEW_FINDINGS -> REPOSITORY_MAP_REBINDING_IMPLEMENTATION -> MACHINE_CURRENT_POINTER -> CROSS_FILE_CONFORMANCE -> ATOMIC_INTEGRATION_REVIEW`

This proposal itself performs none of those canonical effects.
