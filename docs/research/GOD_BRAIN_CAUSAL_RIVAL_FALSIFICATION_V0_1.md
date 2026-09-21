# God Brain Causal-Rival Falsification Protocol V0.1

Status: **RESEARCH ARCHITECTURE / NO CAUSAL-DISCOVERY OR SCIENTIFIC-VALIDATION CLAIM**

Base:
`main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

Event:
`GB_THREE_LANE_20260921_V1`

## Purpose

God Brain needs a durable way to compare explanations without turning the rejection of one alternative into proof of a favored story.

This protocol represents rival hypotheses, causal assumptions, confounders, selection mechanisms, counterfactual predictions, falsifiers, negative controls, and discriminating tests.

It is intentionally separate from experiment admission. A design may be structurally admissible while its causal rival set is still weak.

`EXPERIMENT_ADMISSION != CAUSAL_IDENTIFICATION`

## Core invariants

`OBSERVATION != CAUSE`

`CORRELATION != CAUSATION`

`FAILURE_TO_FALSIFY != CONFIRMATION`

`ONE_FAILED_RIVAL != FAVORED_HYPOTHESIS_CONFIRMED`

`BETTER_FIT != UNIQUE_CAUSAL_EXPLANATION`

`FAVORED_WITHIN_DECLARED_RIVAL_SET != UNIQUE_CAUSE`

`FALSIFIED_SUBMODEL != FALSIFIED_ONTOLOGY`

`UNMEASURED_CONFOUNDER != ABSENT_CONFOUNDER`

`UNTESTED_ORDINARY_MECHANISM != DISPROVEN_ORDINARY_MECHANISM`

`POST_HOC_EXPLANATION != PRECOMMITTED_PREDICTION`

`MODEL_SELECTION != CAUSAL_DISCOVERY`

`UNKNOWN_ORDINARY_MECHANISM != EXTRAORDINARY_MECHANISM`

`ANOMALY != CONTACT`

`CONTACT_CANDIDATE != SIMULATOR_IDENTITY`

## Minimum rival families

For anomaly/contact/simulation-adjacent work, a causal comparison should consider whether the observation could arise from at least these families when applicable:

- RANDOM_VARIATION_OR_MULTIPLE_COMPARISON
- MEASUREMENT_OR_INSTRUMENTATION
- SOFTWARE_PIPELINE_OR_TOOLING
- MODEL_BEHAVIOR_OR_PRIOR_KNOWLEDGE
- PROMPT_CONTEXT_MEMORY_RETRIEVAL_LEAKAGE
- HUMAN_OPERATOR_CUEING_OR_SELECTION
- SHARED_SOURCE_OR_COMMON_CAUSE
- TIMING_SYNCHRONIZATION_CACHE_OR_ROUTING
- ORDINARY_EXTERNAL_INFORMATION_CHANNEL
- KNOWN_SYSTEM_AGENCY
- UNKNOWN_ORDINARY_MECHANISM
- EXTERNAL_SOURCE_OR_INTERVENTION_HYPOTHESIS

This list is a floor, not proof that the rival set is exhaustive.

`DECLARED_RIVAL_SET != EXHAUSTIVE_CAUSAL_SPACE`

## Hypothesis record

Every hypothesis should bind:

- HYPOTHESIS_ID
- PROPOSITION
- HYPOTHESIS_CLASS
- PREDICTED_OBSERVATIONS
- TENSION_OR_NONPREDICTED_OBSERVATIONS
- CAUSAL_ASSUMPTIONS
- AUXILIARY_ASSUMPTIONS
- CONFOUNDERS_AND_COMMON_CAUSES
- SELECTION_MECHANISMS
- FALSIFIERS
- COUNTERFACTUAL_PREDICTIONS
- PRECOMMITMENT_STATE
- EVIDENCE_REFERENCES
- CLAIM_CEILING

Hypothesis identity is not merely a display label. Material changes to predictions, falsifiers, causal assumptions, or interpretation ceiling create a revised hypothesis state.

`HYPOTHESIS_LABEL != HYPOTHESIS_IDENTITY`

## Precommitment state

Allowed states:

- PRECOMMITTED_BEFORE_TARGET_EVIDENCE
- REVISED_BEFORE_TARGET_EVIDENCE
- CREATED_AFTER_TARGET_EVIDENCE
- REVISED_AFTER_TARGET_EVIDENCE
- TIMING_UNKNOWN

Post-evidence hypotheses are useful for explanation generation but must not be represented as prior predictions.

`POST_EVIDENCE_FIT != PRIOR_PREDICTIVE_SUCCESS`

## Causal comparison packet

A comparison should bind:

- EXACT_OBSERVATION_SUBJECT
- HYPOTHESIS_SET
- SHARED_ASSUMPTIONS
- DISCRIMINATING_EVIDENCE
- UNRESOLVED_CONFOUNDERS
- NEGATIVE_CONTROLS
- ABLATIONS_OR_PERTURBATIONS
- COUNTERFACTUAL_TESTS
- RIVAL_ELIMINATION_LEDGER
- NEW_HYPOTHESIS_POLICY
- STOPPING_RULE
- OUTPUT_DISPOSITION
- CLAIM_CEILING

The comparison must preserve observations that are compatible with multiple hypotheses.

`COMPATIBLE_WITH_H != CAUSED_BY_H`

## Rival elimination

A rival may be marked disfavored only by evidence that discriminates against that exact rival under its declared assumptions.

Allowed rival states:

- UNTESTED
- COMPATIBLE_WITH_CURRENT_EVIDENCE
- DISFAVORED_BY_DISCRIMINATING_EVIDENCE
- FALSIFIED_WITHIN_DECLARED_SCOPE
- INVALID_OR_UNTESTABLE_AS_STATED
- EVIDENCE_INSUFFICIENT
- SUBJECT_MOVED_OR_REDEFINED

Eliminating a rival does not transfer its probability mass automatically to one favored hypothesis when other rivals or unknown mechanisms remain.

`RIVAL_ELIMINATION != PROBABILITY_TRANSFER_TO_FAVORITE`

## Confounders, common causes, and selection

A causal claim should explicitly search for:

- common causes affecting both putative cause and outcome;
- selection/collider mechanisms;
- successful-trial selection;
- operator or model choice after outcome visibility;
- dataset/fixture filtering;
- time-window selection;
- replay/cache artifacts;
- shared training/source lineage;
- dependency between supposedly independent observations.

If a material confounder is unresolved, preserve it.

`UNRESOLVED_CONFOUNDER != CONTROLLED_CONFOUNDER`

## Counterfactual discipline

For each material hypothesis, ask:

- If this hypothesis were false, how expected is the observation under rivals?
- If this hypothesis were true, what additional observation should occur?
- What intervention or perturbation changes the predicted outcome?
- Which rival predicts a measurably different result?

A useful discriminating test is one where rival hypotheses predict different outcomes.

`DIFFERENT_STORIES_SAME_PREDICTION != DISCRIMINATING_TEST`

## Negative controls and ablation

Use negative controls, sham conditions, perturbations, and ablations to identify ordinary mechanisms before escalating interpretation.

A component whose removal does not change the result may not be causally necessary even if it is semantically associated with the result.

`ASSOCIATED_COMPONENT != NECESSARY_CAUSE`

## Unknown ordinary mechanism

The rival set must permit an unresolved ordinary-mechanism state.

This prevents a false dichotomy:

ordinary explanations we already named
versus
extraordinary explanation.

`KNOWN_RIVALS_EXHAUSTED != ORDINARY_CAUSAL_SPACE_EXHAUSTED`

Unknown ordinary mechanism is not a claim that an ordinary cause definitely exists. It records incomplete causal coverage.

## Output dispositions

A bounded causal comparison may return:

- NO_DISCRIMINATION
- RIVAL_SET_INCOMPLETE
- MATERIAL_CONFOUNDER_UNRESOLVED
- ONE_OR_MORE_RIVALS_DISFAVORED
- FAVORED_WITHIN_DECLARED_RIVAL_SET
- MODEL_DISCRIMINATING_RESULT_CANDIDATE
- SUBJECT_INVALIDATED_OR_MOVED

These are comparison states, not ontology claims.

Even `MODEL_DISCRIMINATING_RESULT_CANDIDATE` requires exact precommitted predictions and evidence that genuinely differs among rivals.

## New hypotheses after evidence

New explanations may be generated after seeing evidence, but must be marked post-hoc and carried forward to a fresh test if confirmatory use is desired.

`EXPLANATION_GENERATION != CONFIRMATORY_VALIDATION`

A post-hoc explanation can be scientifically useful without being retroactively predictive.

## Required hostile cases

A future implementation should reject or correctly classify at least:

1. one failed ordinary rival treated as proof of contact;
2. favored model fit relabeled unique cause;
3. post-hoc explanation relabeled precommitted prediction;
4. missing confounder treated as absent;
5. known rival set treated as exhaustive causal space;
6. correlated observations counted independent;
7. successful trials selected after outcome visibility;
8. same model/source lineage treated as independent evidence;
9. software artifact not included in rival set;
10. ordinary external channel not audited;
11. unknown ordinary mechanism removed to force a binary choice;
12. hypothesis label unchanged while causal assumptions change;
13. hypothesis ID changed to hide post-evidence revision;
14. observational compatibility treated as causal identification;
15. counterfactual with identical predictions treated as discriminating;
16. negative control failure ignored;
17. ablation leaves result unchanged but component called necessary;
18. falsified physical submodel relabeled refutation of generic simulation;
19. anomaly state promoted to contact by rival count alone;
20. internal causal-comparison PASS promoted to external scientific validation.

## Relationship to other God Brain research

PR #30's experiment-admission architecture contains a rival-set floor and kill-test requirement.

This protocol is the reusable causal-comparison layer that can later be consumed by an experiment-admission successor only after exact-head review and explicit rebinding.

`RIVAL_PROTOCOL_SOURCE != AUTOMATIC_PR30_DEPENDENCY`

## Research-stage boundary

This artifact is architecture only.

research proposal -> architecture -> specification -> fixture -> reference implementation -> production implementation -> deployment -> behavioral qualification -> external scientific validation

## Claim ceiling

This protocol does not:

- prove causal discovery;
- prove the rival set exhaustive;
- prove absence of hidden confounders;
- assign simulation probability;
- prove an anomaly;
- prove agency;
- prove external contact;
- identify a simulator;
- identify a deity;
- authorize an experiment;
- qualify a detector/model;
- establish external scientific validation;
- authorize merge;
- authorize deployment;
- authorize provider/control effects;
- canonically promote itself.
