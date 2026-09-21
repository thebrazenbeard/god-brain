# God Brain Confirmatory Study-Lineage Contract V0.1

Status: **RESEARCH ARCHITECTURE / NO RUNTIME OR SCIENTIFIC VALIDATION CLAIM**

God Brain base:
`main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

Triad event:
`GB_DG_TRIAD_20260921_V1`

## Purpose

A confirmatory experiment is not defined merely by a human-readable study name, one precommit, or one holdout file.

For God Brain, confirmatory evidence must preserve a durable lineage binding:

- what exact scientific question was frozen;
- which candidate/model/detector family was frozen;
- which decision criteria were frozen;
- which holdout observations have already been exposed;
- which attempts already occurred;
- whether a later attempt is genuinely the same study or a redesigned successor;
- whether reveal and execution authority has already been consumed;
- whether an ambiguous execution is unresolved.

This contract is motivated by hostile findings against a current DriftGuard research subject, but it is a God Brain architecture proposal, not a DriftGuard patch or runtime dependency.

## Triggering evidence

Read-only source observations from `thebrazenbeard/driftguard` PR #34 exact head
`351b7a57b7213bd72cf881aa2bbaa449fb0fbc8f`:

- source comment `5762590813`: cross-attempt HOLDOUT trajectory-content reuse can survive corpus metadata relabeling;
- source comment `5762641946`: caller-selected free-form `study_id` can reset ancestry by relabeling the study;
- source comment `5762703839`: attempts inside one `study_id` need not preserve one frozen semantic study subject.

These are source-level blocker observations, not independent scientific evidence.

## Core distinction

`STUDY_LABEL != STUDY_IDENTITY`

`DISCLOSED_PREDECESSOR_ATTEMPTS != SAME_CONFIRMATORY_STUDY_SUBJECT`

`CORPUS_IDENTITY_NONREUSE != HOLDOUT_CONTENT_NONREUSE`

`REDESIGN_AFTER_HOLDOUT_EXPOSURE != UNTOUCHED_CONFIRMATION`

A durable study identity must be derived from a frozen semantic subject, not supplied as a free-form namespace.

## Exact identity versus semantic equivalence

The exact subject digest must be computed from one canonical subject payload. At minimum, the contract must specify:

- SHA-256 or an explicitly versioned successor digest;
- canonical deterministic serialization (for example RFC 8785 JCS or an equivalently pinned canonical JSON profile);
- canonical ordering for semantically unordered collections;
- exact type/domain validation before hashing;
- exclusion of display labels, timestamps, branch names, attempt IDs, and path aliases that do not change the scientific subject.

`DISPLAY_METADATA_CHANGED != STUDY_SUBJECT_CHANGED`

`NONCANONICAL_SERIALIZATION_CHANGED != SCIENTIFIC_SUBJECT_CHANGED`

The digest identifies one exact canonicalized subject. It is **not** a semantic-equivalence oracle.

`STUDY_SUBJECT_DIGEST != SEMANTIC_EQUIVALENCE_PROOF`

A paraphrased evidentiary question or differently encoded but scientifically equivalent subject can still produce a different digest if the governed semantic representation changes. Therefore a new digest does not by itself establish a clean new lineage.

`NEW_STUDY_SUBJECT_DIGEST != CLEAN_NEW_LINEAGE`

## Lineage-family registry and new-root admission

God Brain needs a durable lineage-family registry above individual study-subject digests.

The registry's purpose is not to prove semantic equivalence automatically. Its purpose is to prevent a new digest from being silently treated as ancestry-free merely because exact-digest equality failed.

A new subject enters one of these states:

- `KNOWN_LINEAGE` — linked to an admitted predecessor/root family;
- `NEW_ROOT_PENDING_EQUIVALENCE_CHECK` — proposed as a genuinely new study root but not yet cleared against relevant prior work;
- `ANCESTRY_UNKNOWN` — available evidence cannot determine whether relevant predecessor lineage exists.

Only an explicitly governed new-root admission may establish a new lineage root. A label change, a new digest, a new branch, a new chat, or a new operator cannot do so by itself.

`UNLINKED_ROOT != INDEPENDENT_STUDY`

`NEW_LABEL != NEW_LINEAGE`

The registry cannot prove that all hidden historical studies have been discovered. That remains a claim-ceiling limit.

## Study subject manifest

A future `ConfirmatoryStudySubject` should bind at minimum:

- immutable study-subject schema version;
- scientific/evidentiary question identifier;
- evidence target / measured subject definition;
- benchmark or experiment portfolio digest;
- candidate/model/detector identities and digests;
- detector/model specification digests where applicable;
- family policies and acceptance criteria;
- metric/evaluation contract;
- selection/non-promotion rule;
- execution-subject policy;
- data-partition policy;
- claim ceiling;
- provenance roots required by the question.

Its canonical digest, computed under the pinned canonicalization profile, is the exact durable study-subject identity.

`STUDY_SUBJECT_DIGEST = EXACT_CANONICAL_STUDY_SUBJECT_IDENTITY`

It does not prove semantic uniqueness across every possible re-expression of the same scientific question.

A human label may describe the study, but cannot create a new clean lineage.

## Attempt lineage

Every confirmatory attempt belongs to exactly one study-subject digest.

An attempt ledger must preserve all attempts, including:

- completed;
- invalidated;
- aborted before execution;
- unresolved/ambiguous execution.

A later same-subject attempt must reference every relevant predecessor attempt receipt required by the protocol.

`FAILED_OR_ABORTED_ATTEMPT != DISAPPEARED_ATTEMPT`

Attempts cannot be erased merely because they were inconvenient.

## Holdout ancestry

Holdout provenance and holdout content are distinct evidence dimensions.

A durable attempt receipt should bind, as applicable:

- corpus identity/version digest;
- canonical artifact digest;
- exact role-independent observation/trajectory-content digest;
- source/provenance binding;
- reveal receipt digest;
- execution receipt digest.

A same-subject successor attempt must reject exact prior HOLDOUT content reuse even if corpus ID, version, filename, packaging, or artifact identity changes.

`HOLDOUT_METADATA_CHANGED != HOLDOUT_CONTENT_NEW`

Retaining both provenance identity and content identity matters:

`CONTENT_NONREUSE != PROVENANCE_CONTINUITY`

This rule still does not detect transformed near-duplicates, common upstream generation, leakage, or prior human/model access.

## Same-subject attempt versus redesigned successor

Two successor classes must be explicit. Subject changes must also record whether they occurred before or after confirmatory evidence exposure.

### PRE_EXPOSURE_SUBJECT_REVISION

If frozen subject material changes before any HOLDOUT reveal or confirmatory execution, the replacement still receives a new study-subject digest and a predecessor relation. It preserves precommit history, but it need not inherit nonexistent HOLDOUT exposure.

`PRE_EXPOSURE_REVISION != SAME_SUBJECT_ATTEMPT`

### POST_EXPOSURE_REDESIGN

If frozen subject material changes after HOLDOUT reveal or confirmatory execution, the successor must preserve the exact exposure lineage and explicitly identify the changed subject fields.

`POST_EXPOSURE_REDESIGN != UNTOUCHED_CONFIRMATION`

Two successor classes must be explicit at the attempt/study relationship level.

### SAME_SUBJECT_ATTEMPT

Permitted only when the exact `study_subject_digest` is unchanged.

It inherits:
- attempt ancestry;
- holdout-content ancestry;
- applicable holdout/corpus/artifact provenance;
- prior reveal/execution exposure.

### SUCCESSOR_REDESIGN

Required when the scientific question, candidates, criteria, policies, metric contract, execution subject, or other frozen study-subject material changes after evidence exposure.

A redesigned successor must:

- receive a new study-subject digest;
- reference predecessor study-subject digest(s);
- record why redesign occurred;
- preserve prior evidence exposure as provenance;
- never present itself as untouched confirmation of the predecessor.

Adaptive research is legitimate.

What is forbidden is adaptive redesign being mislabeled as one unchanged confirmatory study.

## Reveal and execution consumption

A confirmatory HOLDOUT reveal is a consuming transition.

`SEALED -> REVEALED`

A governed confirmatory execution is a consuming transition before analysis.

`REVEALED -> EXECUTING`

The exact transition mechanism may vary by implementation. The invariant does not:

`REVEAL_AUTHORITY_IS_SINGLE_USE`

`EXECUTION_AUTHORITY_IS_SINGLE_USE`

A replayed receipt, process restart, or concurrent observer must not manufacture another valid reveal/run authority.

## Ambiguous execution

Once execution authority is consumed, uncertainty does not restore retry authority.

`AMBIGUOUS_EXECUTION != SAFE_TO_RETRY`

If completion/finalization is ambiguous, the attempt remains unresolved until a separately typed reconciliation boundary establishes what happened.

A free-form operator reason, timeout, process restart, or “probably failed” judgment is not sufficient.

## Receipt admission

A structurally valid receipt is not automatically valid for the current transition.

`VALID_RECEIPT != VALID_FOR_THIS_SUBJECT`

Receipt admission should re-bind at least:

- study-subject digest;
- attempt identity;
- precommit digest;
- holdout subject/content;
- execution subject;
- predecessor lineage required by the transition.

## Independence and contamination ceiling

This contract does not prove:

- prior holdout non-access;
- trusted time;
- independent sampling;
- absence of common upstream generation;
- absence of transformed or near-duplicate leakage;
- absence of hidden historical experiments;
- absence of parallel unanchored ledgers;
- external custody;
- automatic semantic-equivalence detection across differently expressed study subjects;
- completeness of lineage-root discovery;
- statistical significance;
- causal truth;
- production superiority.

Those require separate evidence.

`DIGEST_NONREUSE != STATISTICAL_INDEPENDENCE`

`DURABLE_LINEAGE != EXTERNAL_CUSTODY`

## God Brain scientific boundary

For anomaly/contact/simulation research:

`GOVERNED_CONFIRMATORY_PASS != ANOMALY`

`ANOMALY != CONTACT`

`CONTACT_CANDIDATE != SIMULATOR_IDENTITY`

`PROTOCOL_RIGOR != UNIQUE_CAUSAL_EXPLANATION`

Study-lineage governance can reduce experimental self-deception. It does not convert an unusual result into metaphysical evidence.

## Required hostile cases before implementation

A future fixture/reference implementation should at minimum reject or distinguish:

1. same HOLDOUT observations under a new corpus ID/version;
2. same HOLDOUT observations under a new artifact name/digest wrapper;
3. same underlying study relabeled with a new free-form display name;
4. same study-subject digest under two labels starting separate ancestry;
5. same `study_id` with changed candidates;
6. same `study_id` with changed acceptance criteria;
7. same `study_id` with changed benchmark portfolio;
8. same `study_id` with changed detector/model specification;
9. redesign after HOLDOUT exposure represented as unchanged confirmation;
10. missing predecessor attempt ancestry;
11. missing predecessor holdout-content ancestry;
12. reveal replay;
13. execution replay;
14. ambiguous execution followed by operator-abort retry;
15. receipt from another study subject;
16. receipt from another attempt;
17. exact-content nonreuse falsely promoted to statistical independence;
18. current protocol state falsely promoted to external scientific validation;
19. canonical subject payload reordered but incorrectly treated as a new study;
20. display label/timestamp/path alias change incorrectly changes study identity;
21. semantically equivalent question paraphrased into a new digest and treated as ancestry-free;
22. unlinked new subject digest asserted to be an independent new root without governed admission;
23. post-exposure redesign omits changed-field disclosure or predecessor linkage;
24. pre-exposure subject revision is silently represented as the same exact subject.

## Research-stage placement

This artifact is an architecture contract.

`RESEARCH_PROPOSAL -> ARCHITECTURE -> SPECIFICATION -> FIXTURE -> REFERENCE_IMPLEMENTATION -> PRODUCTION_IMPLEMENTATION -> DEPLOYMENT -> BEHAVIORAL_QUALIFICATION -> EXTERNAL_SCIENTIFIC_VALIDATION`

Nothing here skips that ladder.

## Claim ceiling

This artifact does not:

- implement a runtime ledger;
- execute a scientific experiment;
- qualify a detector/model;
- prove holdout independence or non-access;
- validate an anomaly;
- establish external agency;
- establish simulation theory;
- authorize provider/control effects;
- authorize merge;
- authorize deployment;
- canonically promote this architecture.
