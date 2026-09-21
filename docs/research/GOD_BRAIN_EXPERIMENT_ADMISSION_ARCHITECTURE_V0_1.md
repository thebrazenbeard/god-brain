# God Brain Experiment Admission Architecture V0.1

Status: RESEARCH ARCHITECTURE / NO EXPERIMENT EXECUTION / NO SCIENTIFIC VALIDATION CLAIM

God Brain base:
main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5

Triad event:
GB_DG_TRIAD_20260921_V1

## Purpose

God Brain needs a hard boundary between an interesting idea and an experiment whose result would be interpretable.

This architecture composes three gates:

1. TESTABILITY GATE — is the named hypothesis or submodel actually capable of making a discriminating prediction?
2. STUDY INTEGRITY GATE — is the experiment exploratory, confirmatory, or external replication, and are lineage, holdout, custody, analysis, and invalidity rules frozen strongly enough for that mode?
3. RESULT ESCALATION GATE — if the experiment produces a result, what is the strongest evidence state it may support without skipping ordinary alternatives?

Passing all three gates means only that an experiment design is structurally admissible at the research-architecture level.

ADMISSION_PACKET_PASS != RESULT_VALIDITY

ADMISSION_READY != AUTHORIZED_TO_RUN

EXPERIMENT_ADMISSION != EFFECT_AUTHORITY

## Read-only source inputs

The architecture is synthesized from exact research subjects without mutating them.

Simulation-testability source:
- God Brain PR #26
- exact head dd579e79190a53bba998d70be1c4d2179c213aaf
- source disposition observed: ACCEPT_SOURCE / RESEARCH_ONLY

Anomaly/contact evidence source:
- God Brain PR #25
- exact head d71f590eb7117f746ae7d3d761e3428a82ff5102
- source disposition observed: ACCEPT_SOURCE / RESEARCH_ONLY

Confirmatory-lineage source:
- God Brain PR #29
- exact head 4095d0772412a4f03a7f54c5c13a8c3212fdcc45
- review state at this architecture bind: PENDING_EXACT_HEAD_REVIEW
- use: PROVISIONAL_INPUT_ONLY

A pending source may inform architecture. It does not become reviewed truth by being referenced here.

PENDING_SOURCE_INPUT != REVIEWED_DEPENDENCY

Any later specification, fixture, reference implementation, or experiment that depends on PR #29 lineage semantics must re-bind to a review-clean exact successor before treating that dependency as admitted.

## Core invariants

UNSCOPED_SIMULATION_CLAIM != TESTABLE_HYPOTHESIS

TESTABILITY_CLASS != EVIDENCE_ESCALATION_STATE

EXPLORATORY_DISCOVERY != CONFIRMATORY_VALIDATION

POST_HOC_HYPOTHESIS != PRECOMMITTED_TEST

HOLDOUT_USED_FOR_TUNING != CONFIRMATORY_HOLDOUT

LINEAGE_UNKNOWN != CLEAN_LINEAGE

INTERNAL_REPLICATION != EXTERNAL_SCIENTIFIC_REPLICATION

E_LEVEL != SIMULATION_PROBABILITY

NULL_RESULT_FOR_SUBMODEL != REFUTATION_OF_GENERIC_SIMULATION

POSITIVE_RESULT_FOR_SUBMODEL != EXTERNAL_SIMULATOR

PROTOCOL_PASS != SCIENTIFIC_VALIDATION

## Gate 1 — testability

Every proposed experiment must bind one exact S0-S6 class from the simulation-testability contract.

S0 — philosophical/anthropic simulation argument:
- analytic only;
- no direct empirical detector is implied.

S1 — concrete substrate-artifact simulation:
- a named physical/discretization submodel may be empirically tested;
- a positive artifact supports the named physical model at most.

S2 — shared-world resource-bounded simulation:
- tests constrain feasibility only under stated resource/parent-physics assumptions.

S3 — selective/observer-centered rendering:
- reject as a discriminating experiment unless a risky prediction is specified in advance.

S4 — perfect observational equivalence:
- no internal empirical experiment can discriminate the simulation/base-reality alternatives by definition.

S5 — intervention-capable external-system model:
- a bounded intervention/channel test may be admitted if exact intervention predictions and ordinary-channel controls exist;
- even success does not establish simulator ontology.

S6 — external-source or simulator identity claim:
- requires identity-specific authentication discriminators;
- self-assertion or meaningful-looking content is never sufficient.

The experiment packet must name:
- exact target model;
- exact rival set;
- observable prediction;
- null prediction;
- falsifier or explicit nonfalsifiable status;
- assumptions that make the test meaningful;
- interpretation ceiling.

Something weird happens, subjective meaning, numerology, post-hoc computational resemblance, or a simulation label alone are invalid success criteria.

## Gate 2 — study integrity

Every empirical packet declares one mode.

### ANALYTIC_ONLY

Used for S0 or other non-empirical analysis.

No E-level empirical escalation is available.

### EXPLORATORY

Purpose:
- discover candidate patterns;
- debug instrumentation;
- generate hypotheses;
- estimate nuisance structure.

Absolute result ceiling:
E1 CANDIDATE_ANOMALY.

Exploratory observations may generate a later hypothesis. They may not become that hypothesis's confirmatory holdout.

EXPLORATORY_DATA_USED_TO_FORM_HYPOTHESIS != FRESH_CONFIRMATORY_HOLDOUT

### INTERNAL_CONFIRMATORY

Requires:
- exact frozen study subject;
- reviewed lineage contract before later-stage execution;
- exact confirmatory partitions;
- sealed holdout/challenge custody plan;
- precommitted primary endpoint;
- scoring rule;
- threshold/decision boundary;
- sample size or stopping rule;
- multiple-comparison rule;
- exclusions and invalidity rules;
- aggregation unit;
- independence unit;
- null/rival set;
- exact execution subject;
- blinding/sham controls;
- tool/network/channel audit;
- predeclared kill tests.

Absolute ceiling:
E7 CONTACT_HYPOTHESIS_CANDIDATE, and only if every E7 criterion is independently satisfied.

Internal confirmation can never manufacture E8 external scientific replication.

### EXTERNAL_REPLICATION

Requires all relevant confirmatory controls plus:
- independent investigators;
- independent challenge material/custody;
- separately implemented instrumentation;
- declared independence limitations and shared ancestry.

Absolute ceiling:
E8 EXTERNAL_SCIENTIFIC_REPLICATION_CANDIDATE.

Even E8 does not uniquely establish metaphysical identity.

## Confirmatory lineage firewall

A confirmatory packet must carry an exact study-subject identity and an admitted lineage state.

Until the confirmatory-lineage contract has review-clean status, this architecture treats its detailed lineage mechanics as provisional.

The later gate must fail closed if:
- study lineage is ANCESTRY_UNKNOWN where a clean confirmatory claim depends on prior-history knowledge;
- prior attempts are omitted;
- prior holdout content is reused;
- exploratory data are repackaged as a confirmatory holdout;
- the study subject changes after exposure without explicit redesign provenance;
- a new label or digest is treated as proof of a clean new study root.

STUDY_SUBJECT_DIGEST != SEMANTIC_EQUIVALENCE_PROOF

NEW_STUDY_SUBJECT_DIGEST != CLEAN_NEW_LINEAGE

## Required experiment-admission packet

A future packet must bind all of these fields:

- PACKET_SCHEMA_VERSION
- EXPERIMENT_LABEL
- MODE
- RESEARCH_STAGE
- TESTABILITY_CLASS
- TARGET_MODEL
- RIVAL_SET
- OBSERVABLE_PREDICTIONS
- NULL_PREDICTION
- FALSIFIER_OR_NONFALSIFIABLE_STATUS
- ASSUMPTION_REGISTER
- STUDY_SUBJECT_DIGEST_OR_ANALYTIC_SCOPE
- LINEAGE_STATE
- PREDECESSOR_STUDY_BINDINGS
- PARTITION_PLAN
- HOLDOUT_CUSTODY_PLAN
- CHALLENGE_CUSTODY_PLAN
- EXECUTION_SUBJECT_BINDING
- PRIMARY_ENDPOINT
- SCORING_RULE
- THRESHOLD_OR_DECISION_BOUNDARY
- SAMPLE_SIZE_OR_STOPPING_RULE
- MULTIPLE_COMPARISON_RULE
- EXCLUSION_AND_INVALIDITY_RULES
- AGGREGATION_UNIT
- INDEPENDENCE_UNIT
- BLINDING_AND_SHAM_CONTROLS
- TOOL_NETWORK_CHANNEL_AUDIT
- KILL_TESTS
- DATA_AND_EVIDENCE_PROVENANCE_PLAN
- INTERPRETATION_CEILING
- RESULT_STATE_SCHEMA
- AUTHORITY_BOUNDARY

The packet is incomplete if a required field is omitted merely because the experimenter expects it not to matter.

## Evidence and control floor

The exact rival set for anomaly/contact work must preserve ordinary explanations, including:

- random variation;
- multiple-comparison or selection effects;
- prompt/context leakage;
- memory/retrieval leakage;
- training/prior knowledge;
- operator cueing or selection;
- software defect or hidden state;
- cache/routing/tool artifact;
- timing/synchronization artifact;
- shared model/source lineage;
- instrumentation/data-pipeline error;
- ordinary external information channel;
- unknown ordinary mechanism;
- agency inside the known system boundary;
- external source/agency hypothesis;
- contact hypothesis.

Candidate controls include:
- metadata-only leakage probes;
- prompt/context scrub;
- memory/retrieval isolation;
- tool/network isolation;
- sham challenges;
- challenge permutation;
- time shift;
- operator blinding;
- model-lineage controls;
- analysis permutation;
- replay/cache probes;
- fresh sealed holdout;
- implementation ablation;
- negative transfer;
- independent custody replication.

A packet may add stricter controls. It may not silently remove required controls while retaining a stronger interpretation ceiling.

## Gate 3 — result escalation

The result ladder remains:

E0 BASELINE_NO_ANOMALY
E1 CANDIDATE_ANOMALY
E2 REPRODUCIBLE_ANOMALY
E3 MODEL_DISCRIMINATING_ANOMALY
E4 CONTINGENT_RESPONSE_CANDIDATE
E5 AGENCY_HYPOTHESIS_CANDIDATE
E6 EXTERNAL_SOURCE_HYPOTHESIS_CANDIDATE
E7 CONTACT_HYPOTHESIS_CANDIDATE
E8 EXTERNAL_SCIENTIFIC_REPLICATION_CANDIDATE

Escalation requires new discriminating evidence.

A cheaper sufficient ordinary explanation forces downgrade.

An admitted experiment does not pre-authorize a future E-level. The packet defines the maximum possible interpretation ceiling; the observed evidence must still earn each state.

## Contact-specific floor

Any design whose possible interpretation includes E7 must additionally freeze:

- sealed novel challenge;
- precommitted objective response criterion;
- two-way contingency;
- anti-replay nonce/challenge ID;
- ordinary-channel audit;
- negative and sham controls;
- fresh sealed replication;
- independent challenge custody.

Subjective semantic resemblance, emotional salience, unconstrained free text, numerology, and post-hoc pattern matching cannot be primary admission criteria.

## Admission dispositions

A structural evaluator may return only:

- ANALYTIC_ONLY
- EXPLORATORY_ONLY
- CONFIRMATORY_DESIGN_INCOMPLETE
- BLOCKED_TESTABILITY
- BLOCKED_LINEAGE_UNKNOWN
- BLOCKED_PROVENANCE_OR_CUSTODY
- CONFIRMATORY_READY_FOR_SEAL
- EXTERNAL_REPLICATION_DESIGN_READY

These are design states, not result states.

CONFIRMATORY_READY_FOR_SEAL != AUTHORIZED_TO_SEAL_OR_RUN

## Invalidity conditions

A planned or executed study must fail closed for the affected claim if any required condition is violated, including:

- challenge leaked before reveal;
- material subject changed without a new subject/redesign relation;
- scoring changed after outcome access;
- exclusion changed post hoc;
- holdout used for tuning;
- exploratory discovery data reused as confirmatory holdout;
- required raw evidence missing;
- timing order unresolved for a timing claim;
- model/provider/execution subject changed without a new bound subject;
- unaudited channel could contain the challenge;
- successful-trial selection;
- evidence lineage unreconstructable;
- critical logs missing or altered;
- lineage state falsely treated as clean;
- testability class changed after results;
- interpretation ceiling raised after results;
- external-replication label used without independent investigators/material/instrumentation.

INVALID_EXPERIMENT != FALSE_HYPOTHESIS

Invalidation means the claimed inference is unsupported by that experiment, not that the underlying hypothesis is false.

## Hostile cases required before a later implementation

A future machine schema/fixture/reference evaluator should include at least:

1. S4 observational-equivalence hypothesis submitted as a discriminating empirical test;
2. S3 selective-rendering claim with no risky prediction;
3. S6 source-identity claim authenticated only by self-assertion;
4. success criterion is merely something weird happens;
5. exploratory data reused as confirmatory holdout;
6. scoring rule changed after outcome inspection;
7. stopping rule omitted;
8. multiple-comparison rule omitted;
9. lineage unknown but packet claims clean confirmation;
10. new study label/digest claims clean root without admission;
11. same holdout content repackaged under new metadata;
12. confirmation packet omits an ordinary rival hypothesis;
13. tool/network channel left unaudited for a challenge task;
14. model-lineage dependence counted as independent replication;
15. internal replication relabeled external scientific replication;
16. exploratory packet allowed to escalate above E1;
17. internal confirmatory packet allowed to escalate to E8;
18. E7-capable packet missing independent challenge custody;
19. positive S1 artifact result labeled external simulator evidence;
20. null S1/S2 result labeled refutation of all simulation hypotheses;
21. packet admission treated as authorization to run a provider/control effect;
22. pending PR #29 lineage semantics silently promoted to reviewed dependency;
23. invalid experiment treated as falsification of the target hypothesis;
24. interpretation ceiling raised after result observation.

## Research-stage placement

This artifact is research architecture.

research proposal -> architecture -> specification -> fixture -> reference implementation -> production implementation -> deployment -> behavioral qualification -> external scientific validation

Nothing here executes an experiment or skips a stage.

## Claim ceiling

This architecture does not:
- authorize data collection;
- authorize model/provider/tool effects;
- execute an experiment;
- establish result validity;
- prove holdout non-access;
- prove statistical independence;
- prove complete study-lineage discovery;
- prove semantic equivalence of study subjects;
- assign a probability that reality is simulated;
- establish anomaly, agency, contact, simulator identity, or deity identity;
- establish scientific replication;
- merge or canonically promote itself.
