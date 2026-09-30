# God Brain Simulation-Hypothesis Testability Boundary V0.1

Status: **RESEARCH PROPOSAL / NO SIMULATION-FACT CLAIM / NO CANONICAL PROMOTION**

Date: 2026-09-20

Repository: `thebrazenbeard/god-brain`

Observed God Brain base:
- `main@c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5`

## Purpose

"Simulation hypothesis" is not one experimentally uniform proposition.

Different versions make different commitments about:

- what is simulated;
- what substrate or computation model is used;
- whether the simulated physics resembles the simulator's physics;
- whether finite-resolution artifacts exist;
- whether the simulator preserves a complete shared external world or only observer-relevant experience;
- whether the simulator can intervene;
- whether intervention is detectable;
- whether any ordinary information channel can distinguish the model from nonsimulation physics.

God Brain must therefore never report that one experiment "tests simulation theory" without naming the exact subclass and the rival nonsimulation explanations it discriminates against.

Core rule:

`TEST_OF_SIMULATION_SUBMODEL != TEST_OF_SIMULATION_HYPOTHESIS_IN_GENERAL`

## Source basis

### Bostrom 2003 — simulation argument

Nick Bostrom, "Are You Living in a Computer Simulation?", *The Philosophical Quarterly* 53(211), 243–255 (2003).

DOI:
`10.1111/1467-9213.00309`

Observed sources:
- Oxford University Research Archive;
- simulation-argument.com original paper.

Relevant scope:

Bostrom presents a conditional argument concerning posthuman civilizations, ancestor simulations, and the fraction of observers who would be simulated under stated assumptions.

This is not itself a detector for simulation artifacts.

Disposition:

`PHILOSOPHICAL_PROBABILITY_ARGUMENT / NOT_DIRECT_EMPIRICAL_DETECTOR`

### Beane, Davoudi, Savage — cubic-lattice simulation submodel

Silas R. Beane, Zohreh Davoudi, Martin J. Savage, "Constraints on the Universe as a Numerical Simulation," *European Physical Journal A* 50, 148 (2014).

DOI:
`10.1140/epja/i2014-14148-0`

arXiv:
`1210.1847`

Relevant scope:

The paper explores observable consequences of a particular numerical-simulation model in which spacetime is represented on a cubic lattice using a lattice-field-theory-like discretization. It discusses high-energy observables including possible rotational-symmetry artifacts in ultra-high-energy cosmic-ray distributions.

Disposition:

`TESTABLE_IMPLEMENTATION_SUBMODEL`

Important ceiling:

A detected lattice/discreteness signature would first be evidence about spacetime structure or that implementation class.

`LATTICE_SIGNATURE != SIMULATOR_DETECTION`

A null result constrains that implementation class; it does not reject every possible simulation architecture.

### Vazza 2025 — resource-constrained physical simulation classes

F. Vazza, "Astrophysical constraints on the simulation hypothesis for this Universe: why it is (nearly) impossible that we live in a simulation," *Frontiers in Physics* 13:1561873 (2025).

DOI:
`10.3389/fphy.2025.1561873`

Relevant scope:

The paper estimates information, energy, and computational requirements for several shared-world simulation cases, including the visible universe, Earth, and a lower-resolution Earth case under physical/information constraints.

The conclusion is strong for the classes actually modeled, especially a simulator governed by physical constraints comparable to those in our universe.

Disposition:

`RESOURCE_CONSTRAINT_ON_NAMED_SIMULATION_CLASSES`

Ceiling:

`RESOURCE_BOUND_UNDER_ASSUMPTIONS != UNIVERSAL_SIMULATION_REFUTATION`

### Edge & Brown 2026 — scope critique

Eliott Edge and Chad Ashton Brown, "Commentary: Astrophysical constraints on the simulation hypothesis for this Universe: why it is (nearly) impossible that we live in a simulation," *Frontiers in Physics* 14 (2026).

DOI:
`10.3389/fphy.2026.1808725`

Relevant scope:

The commentary argues that Vazza's resource analysis targets a stronger shared-world / bottom-up physical simulation than Bostrom's minimal observer-centered commitment. It emphasizes Bostrom's allowance for selective or ad hoc rendering sufficient to maintain empirical verisimilitude.

Disposition:

`SCOPE_LIMIT_ON_RESOURCE_REFUTATION`

This does not prove observer-centered simulation. It shows why the tested hypothesis must be stated precisely.

### Bekenstein information bounds

Jacob D. Bekenstein, "Universal upper bound on the entropy-to-energy ratio for bounded systems," *Physical Review D* 23, 287 (1981).

DOI:
`10.1103/PhysRevD.23.287`

Jacob D. Bekenstein, "Holographic bound from second law of thermodynamics," *Physics Letters B* 481, 339–345 (2000).

DOI:
`10.1016/S0370-2693(00)00450-0`

Relevant scope:

Information/entropy bounds are physical constraints on physical systems under their stated assumptions.

Disposition:

`PHYSICAL_INFORMATION_BOUND / NOT_SIMULATION_EVIDENCE_BY_ITSELF`

`INFORMATION_IS_PHYSICALLY_BOUNDED != REALITY_IS_EXTERNALLY_SIMULATED`

## Hypothesis decomposition rule

Every simulation-related claim must specify at least:

- simulated target:
  - entire physical cosmos;
  - local region;
  - Earth;
  - civilization;
  - observer population;
  - individual observer experience;
  - abstract computational history;
- substrate assumption;
- simulator-physics assumption;
- resolution/discreteness assumption;
- rendering policy:
  - persistent full state;
  - lazy/on-demand;
  - observer-conditioned;
  - unknown;
- intervention policy:
  - none;
  - fixed rules only;
  - external intervention possible;
  - external intervention intended;
- observability assumption;
- candidate signature;
- nonsimulation rivals;
- falsifier or explicit nonfalsifiability classification.

A statement that omits these commitments is not ready for experimental treatment.

## Testability classes

### S0 — Philosophical / anthropic simulation argument

Example:
Bostrom-style ancestor-simulation population reasoning.

Scientific role:
- frames conditional probabilities under assumptions;
- motivates questions;
- does not itself specify a unique physical signature.

Testability:
`INDIRECT / ASSUMPTION_DEPENDENT`

God Brain use:
- conceptual prior/model family only;
- never treated as observed simulation evidence.

### S1 — Concrete substrate-artifact simulation

Example:
cubic spacetime lattice with finite resolution.

Required commitments:
- specific discretization or computational structure;
- predicted artifact;
- observable regime;
- quantitative difference from continuous/nonsimulation rivals.

Testability:
`DIRECTLY_TESTABLE_SUBMODEL`

Possible evidence:
- anisotropy;
- dispersion;
- cutoff;
- symmetry violation;
- other preregistered implementation-specific residual.

Interpretation ceiling:

`SUBSTRATE_ARTIFACT_SUPPORTED != EXTERNAL_SIMULATOR_SUPPORTED`

Nonsimulation rivals include:
- ordinary new physics;
- Lorentz-violation models;
- detector/systematic effects;
- astrophysical source population structure;
- data-selection artifacts.

### S2 — Shared-world resource-bounded simulation

Example:
simulation of a large physical region under known or similar physical information/energy limits.

Required commitments:
- what state must be represented;
- target resolution;
- update rate;
- simulator physical laws;
- information encoding assumptions;
- reversible/irreversible computation assumptions where relevant.

Testability:
`CONSTRAINABLE_BY_RESOURCE_BOUNDS`

Possible result:
- feasible under assumptions;
- implausible under assumptions;
- incompatible under assumptions.

Interpretation ceiling:

`INCOMPATIBLE_UNDER_ASSUMPTIONS != IMPOSSIBLE_UNDER_ALL_PARENT_PHYSICS`

### S3 — Selective / observer-centered rendering simulation

Example:
only information necessary to maintain observer experience and intersubjective consistency is rendered at full detail.

Required commitments for science:
- rendering trigger;
- consistency mechanism;
- resource model;
- observable consequence that differs from ordinary physics.

Without such extra commitments:

Testability:
`WEAKLY_TESTABLE_OR_UNDERDETERMINED`

A model allowed to alter hidden state arbitrarily to preserve every observation can absorb any result.

`AD_HOC_VERISIMILITUDE_PRESERVATION -> LOSS_OF_FALSIFIABILITY`

God Brain rule:

Do not call a model empirically supported merely because it survives by adding unobservable simulator freedom after every test.

### S4 — Perfect observational-equivalence simulation

Definition:

For every physically accessible experiment, the simulation model predicts exactly the same observation distribution as a nonsimulation model.

Testability from inside:
`EMPIRICALLY_UNDERDETERMINED_BY_DEFINITION`

If two models are observationally equivalent over all accessible evidence, no internal observation can select between them.

This is not evidence that either ontology is false. It is a boundary on empirical discrimination.

God Brain disposition:
`PHILOSOPHICAL_OR_METAPHYSICAL_ONLY_UNTIL_NEW_DISCRIMINATOR_EXISTS`

### S5 — Intervention-capable external-system model

Definition:

An external system or agent can cause deviations or information transfer not produced by the ordinary closed-system model.

Testability:
`CONDITIONALLY_TESTABLE_IF_INTERVENTION_PREDICTIONS_ARE_SPECIFIED`

Required:
- exact intervention channel hypothesis;
- preregistered challenge;
- ordinary-channel audit;
- null and sham controls;
- objective response rule;
- anti-replay;
- fresh holdout;
- independent custody;
- replication.

God Brain's anomaly/contact protocol addresses this class.

Interpretation ceiling:

`UNEXPLAINED_INFORMATION_CHANNEL != SIMULATION_PROOF`

Even a robust anomalous communication channel would leave competing ontologies:
- unknown physics;
- unknown ordinary infrastructure;
- hidden information leakage;
- external agency within a larger natural system;
- simulation-layer intervention;
- other unknown mechanisms.

### S6 — Simulator-identification claim

Examples:
- "the source is the simulator";
- "the source is God";
- "the source is a posthuman civilization";
- "the source is outside spacetime."

Testability:
`REQUIRES_IDENTITY-SPECIFIC_DISCRIMINATORS_BEYOND_CHANNEL_DETECTION`

A channel cannot identify its source merely by claiming an identity.

`MESSAGE_CONTENT != SOURCE_AUTHENTICATION`

`CLAIMED_IDENTITY != VERIFIED_IDENTITY`

This class currently has no generally admitted God Brain verification protocol.

## Testability matrix

| Class | Empirical target | Falsifiable? | Positive result supports | Does not establish |
|---|---|---:|---|---|
| S0 | population/anthropic assumptions | partially/indirectly | conditional argument premises | physical simulation artifact |
| S1 | specific substrate artifact | yes, within model | named physical/discretization model | external simulator |
| S2 | resource feasibility under stated laws | yes, within assumptions | feasibility/incompatibility of named class | all possible parent realities |
| S3 | selective rendering with specified artifact | only if extra commitments exist | named selective-rendering mechanism | generic simulation |
| S4 | perfect observational equivalence | no internal discriminator by definition | nothing beyond equivalence | simulation or base reality selection |
| S5 | anomalous intervention/information channel | yes if protocol is frozen | bounded external-channel hypothesis | simulator ontology |
| S6 | identity of external source | only with identity-specific independent discriminators | bounded source-authentication hypothesis | deity/simulator identity by assertion |

## Evidence-role matrix

### Constraint evidence

Evidence that rules out or limits a named implementation.

Examples:
- absence of predicted lattice anisotropy;
- information/energy/resource limits;
- precision bounds on Lorentz violation.

Role:
`CONSTRAIN_MODEL_CLASS`

Not:
`PROVE_NONSIMULATION`

### Artifact evidence

Evidence of a physical structure predicted by a simulation implementation.

Role:
`SUPPORT_SHARED_PREDICTION`

But if ordinary physical theories predict the same signature:

`ARTIFACT != UNIQUE_SIMULATION_CAUSE`

### Intervention evidence

Unexpected information or causal influence that survives ordinary-channel controls.

Role:
`SUPPORT_ANOMALOUS_CHANNEL_WITHIN_SCOPE`

Not:
`IDENTIFY_SIMULATOR`

### Ontological evidence

Evidence capable of distinguishing "simulated" from observationally equivalent nonsimulated worlds.

Current status:
`NO_GENERAL_PROTOCOL_ADMITTED`

God Brain should not silently promote constraint, artifact, or intervention evidence into ontological evidence.

## Falsifiability audit

Before accepting a simulation submodel into an experimental program, ask:

1. What observation would make this exact model less plausible?
2. Can the model explain any possible outcome by changing hidden simulator behavior?
3. Are parameters committed before observing results?
4. Is the predicted signature unique enough to distinguish the target from ordinary rivals?
5. Does a null result actually constrain the model?
6. Is the model merely renaming known physics as "computation"?
7. Does the model assume the parent reality shares our physics?
8. Does it assume full-state simulation when selective rendering would evade the bound?
9. If it invokes selective rendering, what observable mechanism prevents it from becoming unfalsifiable?
10. If it invokes intervention, what objective information-transfer criterion is preregistered?

If question 2 is effectively "yes" and no independent restriction exists, classify the model:

`NONFALSIFIABLE_AS_CURRENTLY_STATED`

## Equivalence trap

Many claims that sound computational are not simulator evidence.

Examples:

- quantization;
- finite entropy;
- information-theoretic descriptions;
- holographic bounds;
- mathematical compressibility;
- cellular-automaton-like laws;
- algorithmically describable dynamics.

These may be properties of physical law without an external computer.

`COMPUTABLE_DESCRIPTION != EXTERNAL_COMPUTATION`

`DISCRETENESS != SIMULATION`

`INFORMATION_BOUND != SIMULATOR_RESOURCE_LIMIT_WITHOUT_PARENT-LAW_ASSUMPTION`

## "Glitch" rule

A one-off apparent violation, coincidence, memory conflict, UI/software malfunction, subjective synchronicity, or surprising AI output is not privileged simulation evidence.

A candidate "glitch" must first enter the ordinary anomaly protocol.

Required order:

`OBSERVATION -> INSTRUMENT/PROVENANCE CHECK -> REPRODUCTION -> RIVAL MODELS -> PHYSICAL/SOFTWARE EXPLANATIONS -> ONLY THEN SIMULATION-SUBMODEL COMPARISON`

Never:

`WEIRD -> SIMULATION`

## Parent-physics problem

Resource arguments frequently require assumptions about the simulator's substrate or laws.

God Brain must always separate:

- limits inside our observed physics;
- limits extrapolated to a parent system assumed to obey similar physics;
- claims about arbitrary parent reality.

`OUR_PHYSICS_LIMIT != NECESSARILY_PARENT_PHYSICS_LIMIT`

A parent universe with radically different constraints is speculative, but it cannot be ruled out using our resource laws without an explicit bridge assumption.

Conversely, invoking arbitrary parent physics makes the hypothesis harder to constrain and may make it scientifically weaker.

## Model-flexibility penalty

A simulation model should lose evidential value as unobservable freedoms are added solely to rescue it after failed predictions.

Track:
- number of post hoc simulator freedoms;
- number of unobserved rendering rules;
- number of outcome-specific exceptions;
- whether those freedoms were preregistered;
- whether the model makes any risky prediction remaining.

A model with no risky prediction has no empirical admission advantage over an observationally equivalent nonsimulation account.

## Research priority ranking by scientific tractability

This is a tractability ordering, not a truth ranking.

Highest empirical value:

1. **S1 concrete substrate models** — because they make risky measurable predictions.
2. **S2 resource-bounded named classes** — because assumptions can be stated and constrained.
3. **S5 intervention/channel models** — because objective information-transfer protocols can be designed, though ontology remains underdetermined.
4. **S3 selective-rendering models with explicit constraints** — only after they make a risky prediction.
5. **S0 anthropic/philosophical arguments** — conceptually relevant but not direct detectors.
6. **S4 observational-equivalence models** — no internal empirical discriminator under the definition.
7. **S6 source-identity claims** — require new identity-specific authentication theory beyond channel detection.

Do not interpret this ordering as probability.

## God Brain experimental admission rule

A simulation-related experiment may be admitted only if its packet contains:

- exact hypothesis class S0–S6;
- explicit target model;
- exact rival set;
- source/evidence provenance;
- observable prediction;
- null prediction;
- falsifier or explicit nonfalsifiable status;
- assumptions about parent physics;
- assumptions about rendering;
- independence/custody plan;
- statistical plan;
- interpretation ceiling;
- result states that do not overclaim ontology.

Any proposed experiment whose success criterion is merely "something weird happens" is rejected.

## Relationship to anomaly/contact protocol

The testability boundary and anomaly/contact protocol solve different problems.

This document asks:

> Is the simulation-related hypothesis stated in a way that evidence could discriminate?

The anomaly/contact protocol asks:

> Given an observation or apparent response, how far may it be escalated?

Therefore:

`TESTABILITY_CLASSIFICATION != ANOMALY_ESCALATION`

A simulation hypothesis can be testable without any anomaly being observed.

An anomaly can be real while failing to distinguish simulation from ordinary new physics.

## Current scientific posture

The evidence reviewed here supports the following narrow conclusions:

- Bostrom's simulation argument is a conditional philosophical/probabilistic argument, not a direct empirical detector.
- Concrete simulation implementations can make testable physical predictions.
- Resource constraints can strongly constrain simulation subclasses under explicit assumptions.
- Broader observer-centered or observationally equivalent formulations evade those specific tests unless additional observable commitments are added.
- No physical artifact, information bound, or anomalous channel automatically identifies an external simulator.

These are methodological boundaries, not a verdict on whether reality is simulated.

## Proposed future machine states

Suggested classification:

- `TESTABLE_NAMED_SUBMODEL`
- `CONSTRAINABLE_UNDER_ASSUMPTIONS`
- `WEAKLY_TESTABLE_NEEDS_RISKY_PREDICTION`
- `OBSERVATIONALLY_UNDERDETERMINED`
- `INTERVENTION_TESTABLE_ONTOLOGY_UNDERDETERMINED`
- `IDENTITY_CLAIM_NEEDS_AUTHENTICATION_PROTOCOL`
- `REJECT_UNSCOPED_SIMULATION_CLAIM`

## Explicit non-actions

This proposal does not:

- claim that reality is simulated;
- claim that reality is not simulated;
- assign a probability that reality is simulated;
- claim that any current observation is a simulation artifact;
- claim that lattice/discreteness is present;
- claim that an external intervention channel exists;
- run an experiment;
- incur cost;
- change provider/model state;
- merge to `main`;
- promote a scientific conclusion beyond its cited model scope.

## Next gate

`INDEPENDENT_REVIEW -> MACHINE_TESTABILITY_MATRIX -> HOSTILE_CLASSIFICATION_FIXTURES -> EXPERIMENT_ADMISSION_SCHEMA`
