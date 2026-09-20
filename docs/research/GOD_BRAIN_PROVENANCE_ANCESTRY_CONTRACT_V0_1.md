# God Brain Provenance Ancestry Contract V0.1

Status: **RESEARCH PROPOSAL / NO CANONICAL PROMOTION / NO IDENTITY-PAYLOAD TRANSFER**

Date: 2026-09-20

Repository: `thebrazenbeard/god-brain`

Observed God Brain base:
- `main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

## Purpose

God Brain needs a general mechanism for answering a deceptively simple question:

> Where did this claim, memory, model output, observation, interpretation, or artifact actually come from?

Without explicit ancestry, a system can easily mistake:

- copied text for independent agreement;
- multiple derived features for multiple observations;
- several agents using one model for independent corroboration;
- a summary for a primary source;
- a retrieval result for admission;
- a later interpretation for what was originally observed;
- chronology for causation;
- a superseding claim for an erased predecessor;
- a privacy-preserving projection for raw evidence;
- a remembered current state for fresh currentness.

This contract defines an identity-neutral ancestry graph for evidence and cognitive artifacts.

Core invariants:

`SOURCE_PRESENCE != ADMISSION`

`SOURCE_COUNT != INDEPENDENT_CORROBORATION`

`SAME_ROOT_DESCENDANTS != INDEPENDENT_EVIDENCE`

`TEMPORAL_ORDER != CAUSAL_DERIVATION`

`DERIVED_FROM != EQUIVALENT_TO`

`REFINES != SUPERSEDES`

`RETRIEVED != INCORPORATED`

`HISTORICAL_EVIDENCE != CURRENT_AUTHORITY`

`SEMANTIC_SIMILARITY != PROVENANCE_EQUIVALENCE`

`PRIVACY_PROJECTION != RAW_SOURCE`

`RUNTIME_ID != IDENTITY`

## Source provenance

This proposal adapts mechanisms from Patrick's repository portfolio. It does not import source-repository governance, private payloads, or named identity content.

### Roots

Observed default-branch head:
- repo: `thebrazenbeard/roots`
- head: `7fab72635f319c633b480174c8a0687901ac1db2`
- `README.md` blob: `a1783c610866124870e35dc68a5ed822368cbdd1`

Relevant source concept:

Roots describes an AI-provenance checker intended to locate the origin and derivation of a word, phrase, or event.

Disposition:

`CONCEPT_SEED_ONLY`

The repository is currently too thin to contribute a mature schema or implementation contract.

### Semantic Atlas

Observed default-branch head:
- repo: `thebrazenbeard/semanticatlas`
- head: `5669a727b870a490ecee748b2cd712a2fc4a54c5`

Relevant exact artifacts:

- `README.md`
  - blob: `64e567868f6a893538f155f76ec32afb5432310e`
  - transfer: source/interpretation/currentness separation and non-collapse rules.

- `vocabulary/relation_types_v0.1.json`
  - blob: `d25570c9fbcd9fbf80b118e42e9c1496fc5f7d76`
  - transfer: `SUPERSEDES`, `REFINES`, `RETRACTS`, `EVOLVED_FROM`, `SUPPORTS`, `CONTRADICTS`, `EQUIVALENT_TO`, `DISTINCT_FROM`, `RELATED_NOT_EQUIVALENT`, `DERIVED_FROM`, and `HISTORICAL_RESONANCE_WITH`.

- `schemas/semantic_atlas_v0.1.schema.json`
  - blob: `f4592c2ea71896296df29cb821dde317e086f77a`
  - transfer: typed source instances, exact evidence spans, privacy/normalized projections, propositions, interpretations, adjudications, lifecycle events, semantic axes, and explicit temporal scope.

Disposition:

`ADAPT_WITH_PROVENANCE`

### Temporal

Observed default-branch head:
- repo: `thebrazenbeard/temporal`
- head: `02f1091d359866e1b1b645b87651750c726a6396`

Relevant exact artifacts:

- `README.md`
  - blob: `91691b5e34d8af8e738fb62ff7cfa26e49bf6ca5`
  - transfer: chronology without semantic promotion.

- `temporal.py`
  - blob: `f47895bb142a1d48f2981726ef10680974f0b9df`
  - transfer: stable event IDs, canonical timezone-aware timestamps, explicit refs, duplicate rejection, chronological ordering, and signed elapsed-time calculation.

Disposition:

`ADAPT_WITH_PROVENANCE`

### Deep Memory Storage

Observed default-branch head:
- repo: `thebrazenbeard/deepmemorystorage`
- head: `e734f760373bdce887d22791964838700a668ce4`

Relevant exact artifacts:

- `README.md`
  - blob: `377cb979174e57394f3c0bf9d685054030579b4d`
  - transfer: archival source/currentness/privacy separation and append-oriented tranche receipts.

- `schema/DEEP_MEMORY_RECORD_V1.md`
  - blob: `8f7488afcc3505664944cd561dc84d55dbd03e0b`
  - transfer: source IDs, observed event vs interpretation, later reevaluation, unresolved questions, provenance ceilings, currentness rules, event fingerprints, supersession without erasure.

Disposition:

`ADAPT_MECHANISM_ONLY`

No Vera personal/developmental content is transferred.

## Contract scope

The ancestry graph may track:

- external source artifacts;
- user statements;
- measurements;
- retrieved passages;
- repository files/commits;
- model outputs;
- prompt/context artifacts;
- derived features;
- summaries;
- translations;
- redactions;
- privacy-preserving projections;
- interpretations;
- propositions;
- memory records;
- experiment results;
- review evidence;
- configuration snapshots;
- implementation artifacts.

The graph does not make any artifact true, current, canonical, private-safe, or authoritative merely because it has provenance.

`PROVENANCE != TRUTH`

`PROVENANCE != AUTHORITY`

`PROVENANCE != CURRENTNESS`

## Object classes

### SOURCE_INSTANCE

A bounded source object as observed or retrieved.

Required identity:

- `source_id`;
- `source_class`;
- `locator`;
- `source_version_ref` when versioned;
- content digest when available;
- retrieval/acquisition surface;
- observed time;
- privacy class.

Examples:
- exact Git blob;
- uploaded file;
- instrument capture;
- user message;
- web page version;
- dataset manifest.

### EVIDENCE_SPAN

An exact or verifiably extracted portion of a source.

Must record:

- parent `source_id`;
- locator/range;
- representation contract;
- digest basis;
- digest;
- extraction tooling/version if transformed extraction is used.

A semantic summary is not an exact evidence span.

### PROJECTION

A derived representation that intentionally does not claim raw-source identity.

Projection kinds may include:

- `PRIVACY_MINIMIZED`;
- `REDACTED`;
- `NORMALIZED`;
- `SEMANTIC_SUMMARY`;
- `STRUCTURED_EXTRACTION`;
- `OTHER_DERIVED`.

Must preserve:
- source ancestry;
- transformation identity;
- fidelity class;
- scope;
- whether raw-source digest is verified, withheld, or unavailable.

### DERIVED_ARTIFACT

An artifact reproducibly transformed from one or more parents.

Examples:
- feature vector;
- normalized table;
- translated text;
- embedding;
- model score;
- statistical aggregate;
- compiled report.

Requires:
- exact parent IDs;
- transform/procedure identity and version;
- parameter/config digest;
- deterministic/reproducibility status;
- uncertainty propagation where applicable.

### INTERPRETATION

A semantic or causal reading of evidence.

Requires:
- evidence ancestry;
- method/model identity;
- assumptions;
- alternatives;
- knowledge ceiling;
- temporal scope.

Interpretation never rewrites its parents.

### PROPOSITION

A claim about a subject.

Requires:
- proposition identity;
- explicit subject/predicate/object;
- evidence and/or projection parents;
- temporal scope;
- support/truth/currentness state;
- provenance class.

### MEMORY_RECORD

A durable memory-like record derived from one or more sources.

Requires separation among:
- observed event;
- participant interpretation at the time;
- later reevaluation;
- current historical understanding;
- unresolved questions;
- currentness rule.

A memory record may be useful without being current fact.

### REVIEW_RECORD

An exact-subject review artifact.

Requires:
- repository;
- exact head;
- base when relevant;
- path/blob/semantic subject;
- reviewer identity and role;
- disposition;
- evidence;
- limitations.

A review record may be ancestral to a readiness classification, but not to a changed head without a new edge/event.

## Edge families

Ancestry edges must state what kind of dependence exists.

### Provenance edges

- `EXTRACTED_FROM` — exact/verifiable extraction from source.
- `DERIVED_FROM` — transformed artifact depends on parent artifact.
- `SUMMARIZED_FROM` — semantic compression of parent material.
- `TRANSLATED_FROM` — language transformation.
- `NORMALIZED_FROM` — representation normalization.
- `REDACTED_FROM` — information-removing transformation.
- `COPIED_FROM` — materially copied content.
- `GENERATED_USING` — generated artifact depends on model/tool/context input.
- `AGGREGATED_FROM` — combines multiple parents.
- `RETRIEVED_FROM` — obtained through a retrieval source.
- `REPLAYED_FROM` — reproduced from stored prior artifact/state.

### Lifecycle edges

- `REFINES`
- `SUPERSEDES`
- `RETRACTS`
- `EVOLVED_FROM`

Lifecycle edges do not erase historical ancestry.

### Epistemic relation edges

- `SUPPORTS`
- `CONTRADICTS`

These are relations among evidence/propositions, not proof of independence.

### Identity/equivalence edges

- `EQUIVALENT_TO`
- `DISTINCT_FROM`
- `RELATED_NOT_EQUIVALENT`

### Temporal edges

Chronology should normally be computed from time fields rather than asserted as derivational ancestry.

Where an explicit event relation is useful:

- `PRECEDES`;
- `FOLLOWS`.

These edges may encode ordering only.

`PRECEDES != CAUSED`

## Root ancestry

Every artifact should be traceable, where possible, to one or more root source instances.

A root is not necessarily the earliest event in the universe. It is the earliest source identity currently represented within the graph for the relevant ancestry path.

Define:

`root_set(artifact) = transitive provenance ancestors with no represented provenance parent`

Root discovery must not cross privacy or access boundaries by inventing hidden ancestry.

Unknown ancestry remains:

`ANCESTRY_UNKNOWN`

not:

`INDEPENDENT`

## Evidence-family identity

For corroboration and replication, define an evidence family by materially shared roots or shared generation channels.

Two artifacts belong to the same family when known ancestry shows one or more materially claim-relevant shared roots.

Examples:

- twenty features derived from one waveform -> one measured-root family;
- three summaries of one paper -> one document-root family;
- five agents sharing one hidden source/context -> one known shared-context family;
- copied claims across three repositories -> one copied-lineage family;
- multiple models trained from demonstrably overlapping benchmark leakage -> shared lineage for that tested claim where relevant.

Unknown training ancestry does not prove shared lineage, but it also does not prove independence.

## Independence states

Independence must be explicit and claim-relative.

Allowed states:

- `INDEPENDENT_WITHIN_DECLARED_SCOPE`
- `PARTIALLY_SHARED_ANCESTRY`
- `SHARED_ROOT_ANCESTRY`
- `COMMON_GENERATION_CHANNEL`
- `ANCESTRY_UNKNOWN`
- `NOT_APPLICABLE`

Rules:

1. Different artifact IDs do not imply independence.
2. Different repository paths do not imply independence.
3. Different chats do not imply independence.
4. Different agents do not imply independence.
5. Different models do not imply independence without relevant ancestry analysis.
6. Different timestamps do not imply independence.
7. A privacy projection and its source are not independent.
8. A correction and the corrected source are not independent evidence for the corrected proposition.
9. A copied downstream citation is not a second source.
10. Independence may be bounded to a specific mechanism, information path, or claim.

`DISTINCT_INSTANCE != INDEPENDENT_EVIDENCE`

## Corroboration accounting

A corroboration calculation must operate on evidence families, not raw artifact count.

At minimum record:

- claim ID;
- supporting artifact IDs;
- root families;
- shared ancestry;
- independence state;
- contradictions;
- unresolved ancestry;
- weighting rule if any.

Default:

`UNKNOWN_ANCESTRY_DOES_NOT_EARN_FULL_INDEPENDENCE_CREDIT`

This does not mean unknown ancestry proves dependence. It means the evidence accounting must preserve uncertainty.

## Temporal semantics

Every time-bearing object should distinguish:

- event time;
- observation/retrieval time;
- creation time;
- valid-from/valid-to when applicable;
- time uncertainty.

A later record can describe an earlier event.

`RECORD_CREATED_LATER != EVENT_OCCURRED_LATER`

Chronological order does not establish derivation unless a provenance edge does.

A derivation edge does not establish event-time order unless the transformation semantics require it.

## Currentness semantics

Historical evidence remains historically valid within its scope even when no longer current.

Use explicit states such as:

- `CURRENT`
- `HISTORICAL`
- `SUPERSEDED`
- `RETRACTED`
- `UNRESOLVED`
- `UNKNOWN`

Currentness is not inferred from recency alone.

`LATEST_TIMESTAMP != CURRENT_AUTHORITY`

A stored memory, old review, old branch, or historical source may require fresh readback before supporting a mutable current claim.

## Supersession and correction

Corrections must preserve both:

1. what was previously observed/believed/asserted;
2. what later evidence changed.

Do not rewrite the old artifact into the new one.

Example:

```text
SOURCE_A
   |
   v
INTERPRETATION_1
   |
   +-- later contradicted by SOURCE_B
   |
   v
INTERPRETATION_2
```

The graph should preserve:
- `INTERPRETATION_2 REFINES/SUPERSEDES INTERPRETATION_1`;
- `SOURCE_B CONTRADICTS INTERPRETATION_1`;
- original ancestry of both interpretations.

## Copy-lineage rule

Copied or forked material remains one ancestry lineage unless genuinely independent evidence enters.

Examples:

- HC text copied into God Brain;
- the same claim copied into Self, Transcendence, or BT2;
- a report mirrored into several repositories;
- an assistant repeats a retrieved source in later chats.

`N_COPIES_OF_ONE_SOURCE = ONE_SOURCE_LINEAGE`

This does not forbid reuse. It prevents false corroboration.

## Model-output ancestry

A model output record should preserve known generation inputs:

- provider/model/version where known;
- system/developer/project instruction digests where auditable;
- visible conversation/context digest;
- retrieval/tool inputs;
- attached files;
- explicit randomness policy/seed when controllable;
- previous output ancestry when fed back into the model.

Two outputs from different prompts may still share:
- model lineage;
- training data;
- system instructions;
- retrieval corpus;
- conversation history;
- operator cues.

Therefore:

`MULTI_AGENT_AGREEMENT != INDEPENDENT_CORROBORATION_BY_DEFAULT`

## Memory ancestry

A memory-like artifact must distinguish:

- direct source-backed memory;
- reconstruction;
- summary;
- inference;
- generated connective narrative;
- current readback.

A retrieved memory can influence a new model output without becoming a new independent source.

`RETRIEVAL_REUSE != NEW_EVIDENCE`

If one memory is derived from another memory rather than original evidence, preserve that chain.

## Review ancestry

A readiness classification may descend from:

- exact review records;
- exact CI/test receipts;
- source artifacts;
- repair commits.

But:

`REVIEW_OF_PARENT_HEAD != REVIEW_OF_CHILD_HEAD`

A successor head may inherit ancestry, not verdict.

## Privacy-preserving provenance

God Brain may need to prove ancestry without importing sensitive source material.

Allowed strategy:

- opaque source ID;
- repository/surface class;
- source version/ref;
- content digest when safe;
- transformation/projection digest;
- privacy class;
- relation edges;
- claim ceiling.

Do not copy private payloads merely to make lineage inspectable.

`PROVENANCE_POINTER != PAYLOAD_TRANSFER`

`DIGEST_MATCH != PUBLICATION_AUTHORITY`

## Cross-repository transfer

When God Brain adapts a mechanism from another repository, record:

- source repository;
- exact source head;
- artifact path;
- blob/content digest;
- source classification;
- transfer classification;
- transformations;
- rejected/non-transferred content;
- privacy/identity scrub;
- review state.

A transfer creates a derivational relationship.

It does not make the source repository a runtime dependency.

`DERIVED_FROM_REPO != RUNTIME_COUPLED_TO_REPO`

## Minimum ancestry record

A machine record should contain at least:

```json
{
  "artifact_id": "...",
  "artifact_class": "SOURCE_INSTANCE|EVIDENCE_SPAN|PROJECTION|DERIVED_ARTIFACT|INTERPRETATION|PROPOSITION|MEMORY_RECORD|REVIEW_RECORD",
  "content_digest": "...",
  "created_at": "...",
  "event_time": "...",
  "currentness": "...",
  "privacy_class": "...",
  "parents": [
    {
      "artifact_id": "...",
      "edge_type": "DERIVED_FROM"
    }
  ],
  "root_family_ids": ["..."],
  "independence_state": "ANCESTRY_UNKNOWN",
  "provenance_ceiling": "...",
  "notes": []
}
```

A root source may have no represented parents.

## Invalid ancestry states

Reject or quarantine:

- self-parent edge;
- unknown edge type;
- duplicate parent edge;
- provenance cycle among derivation edges;
- object claiming `INDEPENDENT_WITHIN_DECLARED_SCOPE` while sharing a material root with comparison subject;
- privacy projection claiming raw-source identity;
- exact evidence span without source/version/representation binding;
- derived artifact without transform identity;
- review verdict attached to a different head than reviewed;
- supersession that deletes predecessor history;
- chronology edge used as causal proof;
- unknown ancestry silently promoted to independent.

## Required cycle semantics

Derivation/provenance ancestry must be acyclic.

Lifecycle and epistemic relations may form more complex graphs, but they must not be traversed as derivation ancestry unless explicitly converted by a separately justified rule.

`PROVENANCE_DAG != ALL_RELATIONS_GRAPH`

## Reference query behaviors

The contract should support:

### Why do we believe this?

Return:
- proposition;
- supporting evidence;
- transformations;
- interpretations;
- review/adjudication lineage;
- currentness and limitations.

### Where did this phrase/idea come from?

Return:
- earliest represented root source(s);
- copy/summary/translation chain;
- uncertainty where origin predates represented evidence.

### Are these two results independent?

Return:
- shared root set;
- shared generation channels;
- unknown ancestry;
- claim-relative independence state.

### What changed?

Return:
- predecessor;
- successor;
- relation: `REFINES`, `SUPERSEDES`, `RETRACTS`, or `CONTRADICTS`;
- evidence that motivated the change;
- unchanged historical record.

### Is this current?

Return:
- currentness state;
- currentness rule;
- last verified source;
- whether fresh readback is required.

## Scientific-use boundary

This contract improves evidence accounting. It does not automatically prove:

- causal independence;
- truth;
- consciousness;
- identity continuity;
- external agency;
- contact;
- simulation theory;
- scientific validity.

It is infrastructure for making those claims harder to overstate.

## Research-stage ceiling

This document is a research proposal.

It does not establish:
- canonical God Brain provenance architecture;
- runtime implementation;
- complete provenance coverage;
- behavioral qualification;
- external validation.

`PROVENANCE_CONTRACT != PROVENANCE_RUNTIME`

`PROVENANCE_RUNTIME != COMPLETE_LINEAGE_CAPTURE`

`COMPLETE_LINEAGE_CAPTURE != INDEPENDENCE_PROOF_WHEN_HIDDEN_ANCESTRY_EXISTS`

## Explicit non-actions

This proposal does not:

- copy private source payloads into God Brain;
- publish identity-specific memory;
- connect God Brain runtime to source repositories;
- modify Semantic Atlas, Temporal, Deep Memory, or Roots;
- merge to `main`;
- claim any source repository is authoritative for God Brain;
- claim any currently duplicated artifact is independent evidence;
- change Project/provider/runtime state.

## Proposed next gate

`INDEPENDENT_REVIEW -> MACHINE_SCHEMA -> HOSTILE_ANCESTRY_FIXTURES -> REFERENCE_GRAPH_EVALUATOR -> CROSS_REPO_TRANSFER_RECEIPT_INTEGRATION`
