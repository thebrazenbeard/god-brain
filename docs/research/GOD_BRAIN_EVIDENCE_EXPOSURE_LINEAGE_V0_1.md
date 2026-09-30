# God Brain Evidence Exposure and Contamination Lineage V0.1

Status: **RESEARCH ARCHITECTURE / NO CUSTODY OR INDEPENDENCE PROOF**

God Brain base:
`main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

Triad event:
`GB_DG_TRIAD_20260921_V1`

## Purpose

Confirmatory research can be compromised even when study identity, attempt ancestry, and holdout digests are perfect.

The missing question is:

> who or what has already been exposed to evidence from this subject, directly or indirectly, and what later work therefore cannot honestly be called untouched?

This contract defines a conservative evidence-exposure lineage model for future God Brain research.

It complements, but does not modify or canonically depend on, the confirmatory study-lineage architecture under review in PR #29.

## Core boundary

`NO_RECORDED_EXPOSURE != PROOF_OF_NONACCESS`

A local ledger can prove only what was durably recorded under its own evidence boundary. It cannot prove that a human, model, process, administrator, external system, or hidden copy never accessed the evidence elsewhere.

Therefore this architecture never emits a state named `PROVEN_UNEXPOSED`.

The allowed exposure-status vocabulary is:

- `NO_RECORDED_EXPOSURE`
- `KNOWN_DIRECT_EXPOSURE`
- `KNOWN_DERIVED_EXPOSURE`
- `EXPOSURE_UNKNOWN`

`NO_RECORDED_EXPOSURE` means exactly that: no qualifying exposure is recorded in the governed lineage available to the decision.

It is not a custody guarantee.

## Evidence subjects

Exposure must bind an exact evidence subject.

Candidate evidence classes include:

- raw HOLDOUT observations;
- labels/ground truth;
- aggregate metrics;
- per-example metrics;
- detector/model outputs;
- comparison results;
- ranking or selection outcomes;
- anomaly flags;
- reviewer findings;
- failure traces;
- derived summaries;
- transformed or redacted artifacts;
- prompts/context carrying any of the above.

An exposure to a result can contaminate later design even when the raw HOLDOUT was never seen.

`RESULT_EXPOSURE != RAW_DATA_EXPOSURE`

but also:

`RESULT_EXPOSURE_CAN_CONTAMINATE_FUTURE_DESIGN`

## Exposure event

A future `EvidenceExposureEvent` should bind at minimum:

- exact study-subject digest or lineage-family subject;
- exact evidence-artifact digest when available;
- exposure class;
- recipient identity class;
- recipient identity/reference;
- execution/context identity where meaningful;
- source event or source artifact lineage;
- channel/provenance reference;
- observed ordering evidence;
- scope of exposed information;
- whether exposure is direct or derived;
- recorder/evidence provenance;
- explicit claim ceiling.

Observed wall-clock time may be recorded, but:

`RECORDED_TIMESTAMP != TRUSTED_TIME`

## Recipient identity

Exposure can attach to:

- a human;
- a named reviewer role occupied by a human;
- a model invocation;
- a persistent model/agent identity;
- a chat/session/context;
- a worker/process;
- a tool/runtime;
- a dataset-generation process;
- a repository artifact or document.

Identity must be scoped to the claim.

A new execution surface does not automatically create a clean recipient.

`NEW_CHAT != CLEAN_REVIEWER`

`NEW_PROCESS != UNEXPOSED_PROCESS`

`NEW_ROLE != INFORMATION_INDEPENDENCE`

If a new surface receives copied context, summaries, results, prompts, memory, files, or derived artifacts from an exposed source, exposure lineage follows that information.

## Direct exposure

A direct exposure occurs when a recipient receives the governed evidence artifact or an exact representation sufficient to reveal its protected information.

Examples:

- reading HOLDOUT observations;
- receiving ground-truth labels;
- opening a report containing final confirmatory metrics;
- viewing a per-family failure table;
- receiving the exact final detector comparison result.

Direct exposure is durable history for future confirmatory claims.

## Derived exposure

A derived artifact inherits exposure when it carries information learned from an exposed evidence subject.

Examples:

- a summary of HOLDOUT failures;
- an instruction saying which detector won;
- a repaired prompt based on observed HOLDOUT errors;
- a hand-written list of troublesome cases;
- a model-generated critique that was itself produced with HOLDOUT results in context;
- a code change chosen because of a confirmatory failure.

`DERIVATION_CAN_PROPAGATE_EXPOSURE_WITHOUT_COPYING_RAW_DATA`

A hash mismatch with the original artifact does not make the derivative clean.

`NEW_ARTIFACT_DIGEST != NEW_INFORMATION_LINEAGE`

## Exposure propagation

The default rule is conservative:

If artifact B is materially derived from artifact A for the scientific decision under review, and A carries relevant exposure lineage, B inherits that relevant lineage unless a separately governed transformation contract establishes a narrower information scope.

The system should not assume that paraphrasing, summarization, compression, redaction, reformatting, or model regeneration removes exposure.

`TRANSFORMATION != DECONTAMINATION`

A future sanitization/declassification mechanism would need its own bounded claim and hostile tests.

## Design contamination

Exposure does not make subsequent work worthless.

It changes the evidence class.

If a researcher, model, or process has seen confirmatory evidence and then modifies:

- candidate selection;
- thresholds;
- prompts;
- policies;
- scoring;
- preprocessing;
- benchmark composition;
- stopping criteria;
- analysis code;
- interpretation rules;

the resulting work is post-exposure/adaptive with respect to that evidence lineage.

`POST_EXPOSURE_DESIGN != UNTOUCHED_CONFIRMATORY_DESIGN`

It may be excellent exploratory engineering. It simply needs a new untouched qualification subject before a fresh confirmatory claim.

## Reviewer exposure and independence

Reviewer independence is about information lineage, not labels.

`SEPARATE_CHAT != INDEPENDENT_CORROBORATION`

`DIFFERENT_MODEL_INVOCATION != INDEPENDENT_CORROBORATION`

`ROLE_SEPARATION != INFORMATION_INDEPENDENCE`

A reviewer exposed to:

- the prior verdict;
- known blocker descriptions;
- expected failure cases;
- repair rationale;
- hidden HOLDOUT outcomes;

must disclose that exposure if the review is later used as evidence of independence.

A hostile rereview can still be valuable without being independent.

## Shared-root exposure

Two outputs may look independent while sharing one exposed root.

Examples:

- two chats seeded with the same HOLDOUT failure summary;
- two reviewers reading the same prior hostile review;
- two generated test suites derived from one revealed benchmark result;
- a model and a human both reading one postmortem.

`MULTIPLE_OUTPUTS_FROM_ONE_EXPOSED_ROOT != INDEPENDENT_EVIDENCE`

Exposure lineage should preserve shared roots whenever known.

## Unknown exposure

When available evidence cannot determine whether a relevant recipient or artifact was exposed, use:

`EXPOSURE_UNKNOWN`

Do not silently convert unknown into clean.

`UNKNOWN_EXPOSURE != NO_EXPOSURE`

Unknown exposure does not necessarily invalidate the work. It prevents a stronger untouched/nonaccess claim.

## No recorded exposure

`NO_RECORDED_EXPOSURE` is the strongest local negative statement this architecture permits.

It means:

> within the governed exposure records available to this decision, no qualifying exposure event is recorded for the bound recipient/evidence scope.

It does not mean:

- nobody accessed the data;
- no copy exists;
- the recipient has no memory of equivalent evidence;
- a model was never trained on equivalent material;
- external systems have complete audit logs;
- trusted custody exists.

## Model-specific boundary

For models and agents, exact context exposure can be governed when the context and provenance are available.

Training-data or latent-memory non-exposure generally cannot be established from this local contract.

`NO_CONTEXT_EXPOSURE != NO_MODEL_PRIOR_KNOWLEDGE`

If prior-model knowledge matters materially to the scientific claim, it must be addressed by a separate experimental design rather than assumed away.

## Exposure-aware successor rule

A redesigned study or candidate derived after exposure must inherit an exposure relationship to the predecessor evidence.

A new subject digest, branch, chat, prompt, code path, or model invocation cannot erase that relationship.

`NEW_SUBJECT != CLEAN_SUBJECT_IF_DERIVED_FROM_EXPOSED_EVIDENCE`

A future confirmatory qualification may be clean only relative to a new evidence subject under a separately governed custody/nonaccess design.

## Decision rule

For claims requiring untouched evidence:

- `KNOWN_DIRECT_EXPOSURE` => untouched claim rejected;
- `KNOWN_DERIVED_EXPOSURE` => untouched claim rejected;
- `EXPOSURE_UNKNOWN` => untouched claim unsupported;
- `NO_RECORDED_EXPOSURE` => locally compatible with untouched status, but insufficient by itself to prove it.

Therefore:

`NO_RECORDED_EXPOSURE + LOCAL_LINEAGE != PROOF_OF_UNTOUCHED_EVIDENCE`

External custody, access-control, provenance, or equivalent evidence would still be needed for a stronger claim.

## Relationship to study lineage

Study lineage answers:

> is this the same exact study subject, a revision, or a redesigned successor, and what attempt/HOLDOUT ancestry must follow it?

Exposure lineage answers:

> what evidence has been seen, by whom or what, and how did that information propagate into later work?

Both are needed.

`STUDY_LINEAGE != EXPOSURE_LINEAGE`

`EXPOSURE_LINEAGE != STUDY_LINEAGE`

## God Brain epistemic boundary

For anomaly/contact/simulation research:

`CLEANER_EXPOSURE_GOVERNANCE != ANOMALY`

`ANOMALY != CONTACT`

`CONTACT_CANDIDATE != SIMULATOR_IDENTITY`

`EXPOSURE_LEDGER_PASS != EXTERNAL_SCIENTIFIC_VALIDATION`

This architecture reduces one route to self-deception. It does not provide positive evidence for extraordinary hypotheses.

## Required hostile cases before implementation

A future fixture/reference implementation should at minimum address:

1. raw HOLDOUT copied under a new filename;
2. HOLDOUT summarized without raw rows;
3. detector winner communicated without scores;
4. failure cases paraphrased into a new prompt;
5. post-HOLDOUT code repair represented as pre-HOLDOUT design;
6. new chat seeded with exposed summary;
7. new process seeded with exposed artifact;
8. new reviewer role occupied by an already exposed person;
9. two reviews derived from one prior verdict;
10. transformed/redacted artifact falsely treated as decontaminated;
11. new study digest derived from exposed predecessor evidence and falsely treated as clean;
12. missing exposure record falsely promoted to proof of nonaccess;
13. unknown exposure silently converted to no exposure;
14. wall-clock timestamp treated as trusted ordering;
15. raw-data nonexposure falsely used to ignore result exposure;
16. exact-context nonexposure falsely promoted to no model prior knowledge;
17. copied generated test cases treated as independent corroboration;
18. reviewer blocker knowledge omitted from independence disclosure;
19. lineage break caused by changing recipient label;
20. local exposure-ledger pass promoted to external scientific validation.

## Research-stage placement

This artifact is architecture only.

`RESEARCH_PROPOSAL -> ARCHITECTURE -> SPECIFICATION -> FIXTURE -> REFERENCE_IMPLEMENTATION -> PRODUCTION_IMPLEMENTATION -> DEPLOYMENT -> BEHAVIORAL_QUALIFICATION -> EXTERNAL_SCIENTIFIC_VALIDATION`

## Claim ceiling

This artifact does not:

- implement an exposure ledger;
- prove complete logging;
- prove non-access;
- prove trusted time;
- prove external custody;
- prove reviewer independence;
- prove training-data absence;
- prove statistical independence;
- prove hidden-history completeness;
- qualify a detector/model;
- validate an anomaly;
- establish external contact;
- establish simulation theory;
- authorize merge;
- authorize deployment;
- authorize provider/control effects;
- canonically promote this architecture.
