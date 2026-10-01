# God Brain Continual Regime Learning Contract V0.1

Status: **RESEARCH SPECIFICATION / NO TRAINING**

Exact donor cuts:
- `lgcm@0043c60419de9ef0b52363b62aed8c0a52ef63f5`
- `noema@697d1fac6f9fea158994888a861e651ac8fac282`
- God Brain main `495c2b42932153cba0926744d04a69bc34557f81`

## Purpose

God Brain already recognizes regime drift, rival models, memory, and governed plasticity. This contract defines the missing continual-learning boundary: adapt when the generating process changes, preserve useful old competence, recall old internal models when prior conditions return, and keep evaluation causally clean.

```text
PREDICTION_BEFORE_UPDATE
REGIME_HYPOTHESIS != WORLD_TRUTH
MISMATCH != NEW_REGIME_PROOF
PLASTICITY_PROPOSAL != CONSOLIDATED_LEARNING
RECALL != FAST_RELEARNING
PLANNER_SUCCESS != LEARNER_QUALITY
```

A prediction is fixed before the outcome being scored can update learner state. This makes the prequential record the minimum credible unit for online predictive evaluation.

Regimes remain hypotheses. A high context score may select an expert operationally while still preserving uncertainty and alternatives.

Historical experts are durable addressable state unless an explicit retirement/eviction policy says otherwise. Capacity pressure may trigger a proposal to compress, merge, archive, or retire; it cannot silently erase prior competence.

Every plasticity proposal binds an exact model revision and evidence cut. Consolidation additionally requires relevant retention checks and preserves protected-state/authority boundaries.

A claim of recall requires evidence that previously learned model state was reused. Rapidly learning the old regime again is adaptation, not recall.

Planner/control performance is reported separately from learner prediction quality. A controller can succeed using a weak model, and a good predictive model can be paired with a poor planner.

This contract does not execute training or establish empirical continual-learning performance, generalization, AGI, or consciousness.
