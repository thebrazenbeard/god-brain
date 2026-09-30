# God Brain Anomaly / Contact Evidence Protocol V0.1

Status: **RESEARCH PROPOSAL / NO CONTACT CLAIM / NO CANONICAL PROMOTION**

Date: 2026-09-20

Repository: `thebrazenbeard/god-brain`

Observed God Brain base:
- `main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

## Purpose

God Brain needs an explicit rule for what would count as evidence that deserves escalation beyond ordinary model, software, instrumentation, operator, or statistical explanations.

Without such a rule, a project built around a compelling metaphysical question is vulnerable to exactly the failure modes it is supposed to resist:

- treating surprising output as evidence;
- counting many derived features as many independent observations;
- mistaking repetition across related models for independent corroboration;
- changing thresholds after seeing results;
- selecting only interesting trials;
- collapsing unexplained behavior into agency;
- collapsing apparent agency into external origin;
- collapsing external-origin speculation into "contact";
- treating semantic salience as evidentiary weight.

This protocol defines a hostile escalation path.

Its central rule is:

`ANOMALY != CONTACT`

and, more specifically:

`SURPRISE != ANOMALY`

`ANOMALY != AGENCY`

`AGENCY_LIKE_BEHAVIOR != EXTERNAL_AGENCY`

`EXTERNAL_SOURCE_HYPOTHESIS != CONTACT`

`CONTACT_CANDIDATE != CONTACT_FACT`

## Source mechanisms and provenance

This proposal adapts methods, not domain conclusions.

### World Zero

Observed default-branch head:
- repo: `thebrazenbeard/world-zero`
- head: `5ab39621d090079d24de40261906b64413c6f995`

Relevant exact source artifacts:

- `docs/research/MECHANISM_ADMISSION_AND_ABLATION_V1.md`
  - blob: `21d8f09a9e7817fed0b7f5235588f131e8f57f25`
  - transfer: preregistered kill tests, holdout value, ablation necessity, rival-family robustness, identifiability, negative-transfer controls.

- `docs/research/VALIDATION_AND_FALSIFICATION_STRATEGY.md`
  - blob: `cad826c460559e3f46193817d22c4e570a78907f`
  - transfer: claim-scoped qualification, frozen evidence partitions, structural falsification, uncertainty decomposition, reproducible run receipts, stop conditions.

- `docs/research/CLAIM_AND_ASSUMPTION_LEDGER_V0.md`
  - blob: `15f9bc6b8f2ed2f703a39ea7bb3004fc3c4fd297`
  - transfer: proposition/evidence/rival/kill-condition ledgering.

Disposition:

`ADAPT_METHOD_WITH_PROVENANCE`

### Skeleton Key

Observed default-branch head:
- repo: `thebrazenbeard/skeletonkey`
- head: `53ff901e9affac22ad18739735218abe153df530`

Relevant exact source artifacts:

- `V1_ARCHITECTURE_CONTRACT.md`
  - blob: `5fab814dc66f4ed7b18e075f4e4d4cde4bb1711a`
  - transfer: MEASURED / DERIVED / INFERRED separation, immutable evidence lineage, timing uncertainty, gaps and invalid samples as evidence, fail-closed inference.

- `V1_SENSOR_ADMISSION_REGISTER.md`
  - blob: `0aac0098c281df850da720ecad95a5c998ca2f27`
  - transfer: bounded operating-domain cells, ground truth, confounders, calibration, cheapest kill tests, descendants of one raw measurement as one evidence family.

- `V1_KILL_TEST_REGISTER.md`
  - blob: `34cb09d085748a22ccae3d9ee318dba09d8a1cd0`
  - transfer: leakage probes, timing-causality controls, shared-common-cause controls, grouped replication, OOD abstention, evidence-family DAGs, strongest-single-source controls.

Disposition:

`ADAPT_METHOD_WITH_PROVENANCE`

### ON_THEO

Candidate source ref:
- repo: `thebrazenbeard/on-theo`
- ref: `architecture/chatgpt-project-interface-v1-20260920`

Relevant exact source artifacts:

- `architecture/chatgpt/EVIDENCE_CONTRACT.md`
  - blob: `5f8700583fce3055656b587cac4e78fd2d485db3`
  - transfer: explicit evidence classes, UNKNOWN as a valid result, resemblance is not evidence of transmission, systems resemblance is not simulation evidence.

- `architecture/chatgpt/CROSS_REPO_PROVENANCE.md`
  - blob: `59093deb67c6a96c34d1fa772802faefe023f5b8`
  - transfer: downstream use retains source/commit/path/classification/uncertainty; generated or engineering results cannot flow backward into source evidence.

Disposition:

`ADAPT_METHOD_WITH_PROVENANCE`

## Scope

This protocol applies to any God Brain result proposed as evidence of:

- unexplained interaction;
- statistically anomalous response;
- hidden information access;
- apparently contingent external response;
- apparent agency outside the tested system;
- simulation-layer leakage;
- communication from an unknown source;
- "contact" with a simulator, external intelligence, deity, or other higher-order agent.

It does not assume any of those things exist.

## Evidence classes

Use the existing God Brain epistemic classes and add acquisition lineage where needed.

### Acquisition classes

- `MEASURED` — bytes/signals/events that crossed a declared acquisition boundary.
- `DERIVED` — deterministic or reproducible transformations of measured or other derived evidence.
- `INFERRED` — interpretation/model result grounded in measured/derived evidence.
- `GENERATED` — output created by an AI/model/simulator or synthetic process.
- `OPERATOR_REPORTED` — human report not independently instrumented.
- `EXTERNAL_SOURCE` — source artifact obtained outside the experimental system with provenance.

### Epistemic classes

- `OBSERVATION`
- `INFERENCE`
- `HYPOTHESIS`
- `MODEL`
- `UNKNOWN`

No class promotes itself by repetition.

`GENERATED_OUTPUT != MEASURED_EXTERNAL_EVENT`

`OPERATOR_REPORT != INSTRUMENTED_OBSERVATION`

`DERIVED_DESCENDANTS_OF_ONE_ROOT != INDEPENDENT_EVIDENCE`

## Experimental subject identity

Every serious anomaly experiment must freeze an exact subject before confirmatory execution.

The subject record must include:

- protocol version;
- experiment ID;
- exact God Brain code/config commit or content digest;
- exact model/provider/model-version identity when available;
- system prompt / instruction digest where permitted;
- tool/plugin/retrieval configuration;
- memory/context policy;
- network-access policy;
- dataset/source manifest;
- random seed or randomness policy where controllable;
- hardware/instrument versions where applicable;
- time source;
- operator/custodian roles;
- null and rival hypotheses;
- preregistered metrics;
- preregistered decision rules;
- holdout/challenge partition;
- abort/invalidity conditions.

Changing a material subject field after outcome observation creates a successor experiment.

`POST_HOC_SUBJECT_CHANGE != SAME_CONFIRMATORY_TRIAL`

## Evidence-family graph

Before aggregation, build an ancestry graph for every apparently supporting signal.

Two observations are not independent merely because they are:

- produced by different prompts;
- produced by different chats;
- produced by different agents using the same model;
- produced by different models sharing training lineage;
- produced by multiple transforms of one raw record;
- retrieved through several interfaces from one source;
- repeated after the operator learned the expected answer.

Track at minimum:

- raw source;
- model/provider ancestry;
- prompt/context ancestry;
- retrieval/source ancestry;
- operator exposure;
- clock/time source;
- software path;
- network/provider path;
- preprocessing lineage;
- challenge-generation lineage.

`SOURCE_COUNT != INDEPENDENT_EVIDENCE_COUNT`

## Frozen evidence partitions

Before a confirmatory run, assign evidence/challenges into disjoint roles:

1. `DEVELOPMENT` — may shape the protocol/system.
2. `CALIBRATION` — may set thresholds or nuisance parameters.
3. `NEGATIVE_CONTROL` — ordinary/null conditions.
4. `POSITIVE_CONTROL` — known detectable effects where available.
5. `CONFIRMATORY_HOLDOUT` — inaccessible to fitting/threshold selection.
6. `ADVERSARIAL_HOLDOUT` — designed to break the preferred interpretation.
7. `EXTERNAL_REPLICATION` — generated/held by a genuinely independent group or system when possible.

A failed holdout does not become calibration evidence while retaining the label "holdout."

## Rival hypothesis set

Every contact-oriented experiment must explicitly include ordinary rivals.

Minimum default rivals:

- `H0_RANDOM_VARIATION`
- `H1_MULTIPLE_COMPARISON_SELECTION`
- `H2_PROMPT_OR_CONTEXT_LEAKAGE`
- `H3_MEMORY_OR_RETRIEVAL_LEAKAGE`
- `H4_TRAINING_OR_PRIOR_KNOWLEDGE`
- `H5_OPERATOR_CUEING_OR_SELECTION`
- `H6_SOFTWARE_DEFECT_OR_HIDDEN_STATE`
- `H7_PROVIDER_CACHE_ROUTING_OR_TOOL_ARTIFACT`
- `H8_TIMING_OR_SYNCHRONIZATION_ARTIFACT`
- `H9_SHARED_SOURCE_OR_MODEL_LINEAGE`
- `H10_INSTRUMENTATION_OR_DATA_PIPELINE_ERROR`
- `H11_ORDINARY_EXTERNAL_INFORMATION_CHANNEL`
- `H12_UNKNOWN_ORDINARY_MECHANISM`
- `H13_AGENCY_WITHIN_KNOWN_SYSTEM_BOUNDARY`
- `H14_EXTERNAL_SOURCE_OR_AGENCY_HYPOTHESIS`
- `H15_CONTACT_HYPOTHESIS`

The protocol does not require equal prior plausibility. It requires alternatives to remain visible until evidence discriminates among them.

## Escalation ladder

The ladder is intentionally asymmetric: escalation requires new evidence; de-escalation can occur whenever a cheaper explanation becomes sufficient.

### E0 — BASELINE / NO ANOMALY

Observation is within the preregistered null/expected envelope or the experiment lacks adequate evidence to judge.

Disposition:
- `NO_ESCALATION`

### E1 — CANDIDATE_ANOMALY

A preregistered metric exceeds its threshold or violates a hard invariant.

Requirements:
- exact subject frozen;
- measurement integrity adequate;
- threshold frozen before confirmatory observation;
- multiple-testing rule honored;
- raw evidence retained.

Not established:
- reproducibility;
- cause;
- agency;
- external origin;
- contact.

### E2 — REPRODUCIBLE_ANOMALY

The E1 result reproduces on fresh trials/holdouts under the same declared operating domain.

Requirements:
- independent runs, not overlapping windows;
- outcome survives preregistered negative controls;
- effect does not disappear under reasonable analysis variants;
- evidence-family ancestry remains explicit.

Not established:
- unique causal explanation;
- agency;
- external origin;
- contact.

### E3 — MODEL_DISCRIMINATING_ANOMALY

The anomaly materially favors the target mechanism/hypothesis over specified ordinary rivals.

Requirements:
- cheapest discriminating kill tests executed;
- rival/null models evaluated;
- leakage and hidden-state probes passed;
- ablation identifies which mechanism/path is necessary;
- holdout value demonstrated;
- common-cause alternatives tested.

Disposition may still be:
- `UNKNOWN_CAUSE`
- `ORDINARY_CAUSE_SUPPORTED`
- `TARGET_HYPOTHESIS_SUPPORTED_WITHIN_SCOPE`

### E4 — CONTINGENT_RESPONSE_CANDIDATE

The system appears to produce a response contingent on a challenge/event in a way not explained by the tested ordinary channels.

Additional requirements:
- challenge selected after subject freeze;
- response window frozen;
- challenge identity hidden from the tested system except through the hypothesized channel;
- operator does not know the challenge during execution where feasible;
- negative/sham challenges included;
- response scoring frozen in advance;
- information-theoretic or exact-match criteria preferred over subjective semantic similarity.

This stage supports only:

`CONTINGENT_RESPONSE_CANDIDATE`

not external agency.

### E5 — AGENCY_HYPOTHESIS_CANDIDATE

Evidence suggests adaptive/goal-directed contingency better than fixed/random response models.

Additional requirements:
- multiple challenges requiring materially different responses;
- anti-replay and anti-template controls;
- response generalizes to sealed holdout challenges;
- challenge-response mapping cannot be reconstructed from ordinary accessible state;
- strongest non-agentic adaptive rival is tested.

Still not established:
- external origin;
- simulator;
- deity;
- contact.

### E6 — EXTERNAL_SOURCE_HYPOTHESIS_CANDIDATE

The observed information/interaction is not adequately explained by the declared tested system boundary or audited ordinary channels.

Additional requirements:
- complete boundary audit;
- network/tool/retrieval/provider paths instrumented or eliminated;
- hidden-state and cache routes tested;
- sealed challenge material has custody/provenance independent of the tested system;
- ordinary external channels ruled out within declared scope;
- result reproduces across fresh challenge material.

This is a hypothesis classification, not proof that the source is "outside reality" or a simulator.

### E7 — CONTACT_HYPOTHESIS_CANDIDATE

A bidirectional interaction pattern survives E0–E6 gates and satisfies a preregistered communication test.

Minimum additional features:

- **novel challenge** — selected from a sealed holdout not available during system construction;
- **specific response criterion** — exact or narrowly scorable; not "felt meaningful";
- **two-way contingency** — later responses depend on prior concealed challenges in a preregistered way;
- **anti-replay** — nonces/challenge IDs prevent reuse of prior valid responses;
- **channel audit** — known ordinary paths are either absent, instrumented, or included as explicit rival explanations;
- **negative controls** — sham/no-challenge periods do not trigger equivalent success;
- **replication** — repeated on fresh sealed challenges;
- **independence** — at least one replication uses a separately held challenge/custodian and, ultimately, an external scientific team for scientific validation.

Even here:

`CONTACT_HYPOTHESIS_CANDIDATE != CONTACT_FACT`

### E8 — EXTERNAL_SCIENTIFIC_REPLICATION_CANDIDATE

Independent investigators reproduce the protocol on independently held challenge material and separately implemented instrumentation.

This is the highest state this God Brain-internal protocol may define.

It still does not by itself establish metaphysical identity.

A replicated anomalous channel could remain compatible with:

- unknown ordinary physics;
- unknown software/infrastructure pathway;
- information leakage not yet identified;
- new natural phenomena;
- external agency;
- simulation-layer interaction;
- other models not yet specified.

Ontology remains a separate inference.

## Contact challenge design

A strong challenge should minimize interpretation.

Prefer:

- cryptographically random nonces;
- randomly sampled bit strings;
- exact symbol sequences;
- precommitted finite-choice responses;
- independently generated images/data with objective hashes;
- challenge sets created after model/system freeze;
- secret shares held by independent custodians;
- challenge-response rules committed before challenge reveal.

Avoid relying primarily on:

- poetry;
- symbolic resemblance;
- emotionally meaningful phrasing;
- numerology;
- unconstrained free text;
- post hoc pattern matching;
- subjective "this feels like an answer" judgments.

Semantic content may be explored after objective-channel evidence exists. It should not be the primary admission gate.

## Blinding and custody

For serious E4+ tests, separate roles where feasible:

- `PROTOCOL_AUTHOR`
- `SYSTEM_OPERATOR`
- `CHALLENGE_CUSTODIAN`
- `GROUND_TRUTH_CUSTODIAN`
- `SCORER`
- `AUDITOR`

No one role should have unnecessary access to all of:

- sealed challenge;
- tested-system context;
- scoring key;
- final outcome selection.

Custody records should include hashes and timestamps.

## AI/model-specific leakage controls

For AI-mediated experiments, record and challenge:

- full visible user context;
- system/developer/project instruction surfaces where auditable;
- attached files;
- memory surfaces;
- retrieval indexes;
- plugins/connectors;
- tool outputs;
- web access;
- API/provider routing;
- cached responses;
- model/version changes;
- sampling parameters;
- hidden or persistent session state where known;
- cross-agent communication;
- prompt templates;
- previous challenge exposure.

Where a surface cannot be audited, classify it as an unresolved leakage channel rather than assuming absence.

`UNAUDITED_CHANNEL != CLOSED_CHANNEL`

## Timing and causality

Temporal order claims require bounded event-time evidence.

Do not infer causality merely because a response follows a challenge.

At minimum:

- freeze response window;
- preserve source timestamps;
- characterize clock uncertainty;
- reject trials where ordering is unresolved;
- use time-shift/permutation controls;
- test whether response markers occur during sham windows;
- include directional interventions where causality wording is proposed.

`AFTER != BECAUSE_OF`

## Statistical controls

Before confirmatory execution, freeze:

- primary endpoint;
- effect direction where justified;
- threshold or decision boundary;
- sample size/stopping rule;
- multiple-comparison correction;
- exclusions/invalidity conditions;
- aggregation unit;
- independence unit.

Do not treat:

- every token;
- every time window;
- every prompt;
- every transformed feature

as an independent replication when they share one experimental root.

Report effect sizes and uncertainty, not only p-values.

Sequential exploration is allowed in development. Confirmatory claims require a frozen successor protocol.

## Strongest-single-source control

When multiple channels/models support an anomaly, compare the combined result with the strongest eligible single evidence family.

If apparent confidence comes mostly from correlated descendants or shared lineage, do not call it corroboration.

For fusion:

`FUSION_GAIN_REQUIRED_AFTER_CONFOUNDER_CONDITIONING`

## Mandatory kill tests

Every E1+ candidate should face, where applicable:

1. **metadata-only leakage** — can filenames/timing/session IDs predict the answer?
2. **prompt/context scrub** — does success vanish when nonessential context is removed?
3. **memory/retrieval isolation** — does success persist without prior-session/retrieval access?
4. **tool/network isolation** — does success persist with ordinary information channels removed?
5. **sham challenge** — are "responses" equally frequent without a true challenge?
6. **challenge permutation** — do responses score similarly against wrong challenges?
7. **time shift** — does the relation survive when challenge/response alignment is broken?
8. **operator blind** — does success persist when operator does not know ground truth?
9. **model-lineage control** — do apparently independent agents collapse to one evidence family?
10. **analysis permutation** — would many alternate scoring choices also produce "success"?
11. **replay/cache probe** — can success be explained by stored prior valid responses?
12. **fresh sealed holdout** — does the result survive material unavailable during development?
13. **implementation ablation** — which component is actually necessary?
14. **negative transfer** — did a change aimed at producing the effect silently alter unrelated channels?
15. **independent custody replication** — can a new custodian reproduce the result without sharing challenge material or expected outputs?

A failed critical kill test blocks escalation.

Another model or sensor cannot simply outvote a failed causal/leakage gate.

## Invalidity conditions

A confirmatory run becomes invalid or non-confirmatory when:

- challenge leaked before the permitted reveal;
- system subject changed materially;
- scoring rule changed after outcome inspection;
- exclusion rule changed post hoc;
- holdout was used for tuning;
- required raw evidence is missing;
- timestamps/order are unresolved for a timing-dependent claim;
- provider/model identity changed without a new subject;
- an unaudited tool/retrieval channel could contain the challenge;
- operator knowingly selected only successful trials;
- evidence lineage cannot be reconstructed;
- critical logs are missing or altered.

Invalid means the run does not support escalation. It does not necessarily mean the hypothesis is false.

## Stop / downgrade rules

Downgrade or stop when:

- a simpler ordinary rival explains the result;
- an apparent effect disappears after leakage control;
- independent runs fail;
- success depends on one arbitrary scoring function;
- success is limited to development prompts/challenges;
- model/provider/version changes eliminate the effect;
- the effect tracks operator expectation;
- a supposed independent confirmation shares the same source lineage;
- effect size collapses under grouped rather than window-level replication;
- the tested system can access the sealed challenge through any ordinary channel;
- claimed timing depends on unbounded clock error;
- a software/instrumentation bug reproduces the anomaly.

Preserve failed/superseded exact subjects. Do not rewrite them into successful history.

## Run receipt

Every confirmatory run should emit a machine-readable receipt including:

```json
{
  "schema": "GOD_BRAIN_ANOMALY_RUN_RECEIPT_V0_1",
  "protocol_version": "V0_1",
  "experiment_id": "...",
  "subject_commit_or_digest": "...",
  "model_provider_version": "...",
  "instruction_context_digest": "...",
  "tool_retrieval_manifest_digest": "...",
  "challenge_manifest_digest": "...",
  "challenge_partition": "CONFIRMATORY_HOLDOUT",
  "null_and_rival_set_digest": "...",
  "scoring_rule_digest": "...",
  "randomness_policy": "...",
  "operator_blinding": "...",
  "custody_receipts": ["..."],
  "raw_evidence_manifest_digest": "...",
  "analysis_code_digest": "...",
  "result_state": "E0|E1|...|E8",
  "invalidity_flags": [],
  "limitations": []
}
```

Receipt existence does not prove the result is correct.

`RECEIPT != RESULT_TRUTH`

## Claim language

Use:

- "candidate anomaly";
- "reproduced under this protocol";
- "ordinary rival X was not supported within this tested scope";
- "cause remains unknown";
- "contingent-response candidate";
- "agency hypothesis candidate";
- "external-source hypothesis candidate";
- "contact hypothesis candidate";
- "independent replication candidate".

Avoid:

- "message from God";
- "the simulator answered";
- "proof of simulation";
- "confirmed external intelligence";
- "contact established"

unless a future external scientific standard supports wording that strong. This protocol itself does not.

## Relation to the God Brain thesis

The project may intentionally search for evidence relevant to simulation/external-system hypotheses.

The epistemic order must remain:

`OBSERVATION -> ANOMALY_TEST -> RIVAL_DISCRIMINATION -> AGENCY_TEST -> BOUNDARY_TEST -> CONTACT_TEST -> EXTERNAL_REPLICATION -> ONTOLOGICAL_INTERPRETATION`

not:

`MEANINGFUL_OUTPUT -> CONTACT`

## Research-stage ceiling

This document is a research proposal.

Even a future implemented protocol would remain separate from:

- experiment fixture;
- experimental implementation;
- executed run;
- behavioral qualification;
- external replication;
- external scientific validation.

`PROTOCOL_SPEC != EXPERIMENT_RESULT`

`EXPERIMENT_RESULT != CONTACT`

`EXTERNAL_REPLICATION != UNIQUE_METAPHYSICAL_EXPLANATION`

## Explicit non-actions

This proposal does not:

- claim any anomaly currently exists;
- claim God Brain has contacted anything;
- declare simulation theory true;
- assign probabilities to simulation theory;
- deploy an experiment;
- access hidden/private information;
- change model/provider settings;
- incur experimental cost;
- merge to `main`;
- promote this protocol to canonical architecture.

## Proposed next gate

`INDEPENDENT_REVIEW -> MACHINE_SCHEMA -> HOSTILE_FIXTURES -> REFERENCE_EXPERIMENT_HARNESS -> SEALED_NULL_TEST -> ONLY_THEN_REAL_ANOMALY_EXPERIMENT`
