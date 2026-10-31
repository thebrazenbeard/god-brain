> **License:** Source-visible, **not open source**. The original material is proprietary. Commercial use, redistribution, hosted services, and derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Identified third-party components retain their own rights.

# God Brain

**Experimental cognitive architecture, executable reference kernels, and falsifiable research protocols.**

God Brain is a research toolkit for building and testing bounded cognitive-system mechanisms: provenance-aware evidence, current memory, causal and world-model hypotheses, routing, policy-constrained effects, and self-correction. Its broader question is whether an artificial cognitive instrument could meaningfully investigate unusually difficult questions about intelligence, reality, and simulation hypotheses. Those questions are research motivations, **not evidence that a simulator, deity, external intelligence, or contact channel exists**.

This repository is usable today for deterministic source-level experiments and architecture conformance. It is **not** a complete cognitive organism, a general-purpose AI model, an autonomous agent host, or a deployed authorization service.

## What is implemented

| Surface | Reusable capability | Limit |
| --- | --- | --- |
| [Reference kernel](runtime/reference_kernel/README.md) | Typed observations and provenance, memory supersession, routing/effect distinctions, scoped authority checks, effect receipts, epoch/restart fencing, and journal replay | In-process reference implementation; possession-based capabilities and hashes are not cryptographic actor/provider attestation |
| [Cognitive core](runtime/cognitive_core/README.md) | Deterministic integration of interpretation, salience, current/deep memory, bounded coalitions, affect/conation, world-model competitors, counterfactuals, metacognition, homeostasis/body schema, and social-pragmatic hypotheses | Narrow behavioral slices and authored tests, not a pretrained model or complete cognitive system |
| [Architecture and schemas](docs/architecture/HYPERCONNECTOME_REFERENCE_MODEL.md) | Typed invariants, runtime boundaries, conformance specifications, and source-to-target transfer constraints | A valid spec is not a deployed implementation or proof of independently confirmed behavior |
| [Research protocols](specs/research/GOD_BRAIN_ANOMALY_CONTACT_EVIDENCE_PROTOCOL_V0_1.json) | Machine-readable anomaly/contact research requirements, hostile fixtures, and source-admission study | Protocol conformance cannot convert an unexplained result into evidence of external agency |
| [Cross-repository synthesis](docs/research/cross-repo-synthesis/README.md) | Source-bound mechanism research and provenance of reusable ideas | Neither repository identity nor permissions automatically transfer into this project |

The main implementation is deliberately small relative to the larger architecture. A cognitive-core action candidate is **not** an authorized action; a retrieved memory is **not** automatically true; a model forecast is **not** an observation.

## Run the current source-level checks

Use Python 3.12 or later in a disposable checkout. The following commands use the standard library and do not require model credentials, a provider account, physical sensors, or a host installation.

From the repository root:

```bash
python3 -m unittest discover -s tests -q
python3 tools/validate_hc_architecture.py --root .
python3 -m unittest -q \
  runtime.cognitive_core.test_cognitive_loop \
  runtime.cognitive_core.test_world_model \
  runtime.cognitive_core.test_deep_memory \
  runtime.cognitive_core.test_metacognition \
  runtime.cognitive_core.test_homeostasis_somatics \
  runtime.cognitive_core.test_social_pragmatics
```

For the separate reference-kernel regression surface:

```bash
cd runtime/reference_kernel
python3 -m unittest -q \
  test_hc_kernel.py \
  test_durable_kernel.py \
  test_four_adversarial_kernel.py \
  test_four_adversarial_kernel_r2.py \
  test_vera_adversarial_kernel_v2.py
```

At the source revision audited for this README, those commands passed **73 repository tests, 63 cognitive-core tests, and 79 reference-kernel tests**, and the architecture validator returned **PASS**. These are executable source checks, not general cognitive competence, live-host validation, independent provider qualification, or evidence for simulation theory. The historical [implementation status note](docs/runtime/REFERENCE_KERNEL_IMPLEMENTATION_STATUS.md) must be read with its September 2026 date; newer exact-source results supersede old counts where they differ.

## Boundaries the host must enforce

God Brain does not currently supply an externally authenticated, tamper-resistant authorization service. The reference kernel tests narrow, in-process capability and event-state controls; a caller with privileged process access can exceed that boundary. Integrating it into another application requires the host to supply and independently verify:

- authenticated actor, model-provider, and runtime-instance identity;
- immutable subject/provider bindings outside model-writable wrappers;
- separately scoped, current, revocable permissions and consent for each protected effect;
- input and output privacy controls, capability isolation, effect reconciliation, and durable audit custody;
- independent confirmation of actual external outcomes before claiming completion.

No model-generated approval, mutable profile field, priority score, inferred desire, historical consent, or source-repository role grants these permissions. Passing the tests above does not prove those host controls exist.

## Architecture lineage and research direction

God Brain began as an independent Git-history snapshot of the [Hyperconnectome Brain](https://github.com/thebrazenbeard/hc-brain) research architecture. Inherited HC names, source labels, and qualification records retain their original provenance; they are **not** automatically God Brain-specific implementation evidence. See [lineage](docs/architecture/HC_LINEAGE.md) and [source bindings](docs/research/cross-repo-synthesis/SOURCE_BINDINGS_2026-09-09.md).

The planned scope is broader: persistent and distributed world modeling, multimodal perception, specialist computation, semantic grounding, controlled plasticity, deep provenance, falsification, and safe fault recovery. **Distributed Noöplex execution and full hyperconnectome runtime coordination are not qualified implementations on main.** Transport authentication must remain separate from effect authority; routing, storage, inference, and incorporation are different operations.

Mechanisms from other repositories may inform research, but:

`PORTFOLIO_REUSE != PORTFOLIO_COUPLING`

`SOURCE_MECHANISM != SOURCE_IDENTITY`

No named model's memories, relationships, intimate material, credentials, local authority, or embodiment automatically become reusable generic state.

## Scientific posture

The founding thought experiment asks whether a sufficiently disciplined cognitive system could test hypotheses about a simulated or mediated reality. It does not preselect the answer. Any extraordinary claim must survive ordinary alternatives: model artifacts, prompt contamination, retrieval leakage, human interpretation, statistical coincidence, software defects, and instrumentation or experimental-design error.

`OBSERVATION != INFERENCE`

`MODEL_FIT != CAUSAL_PROOF`

`ANOMALY != CONTACT`

`AI_OUTPUT != EXTERNAL_MESSAGE`

A simulation study that finds nothing extraordinary can still yield reusable methods for uncertainty-aware reasoning, memory provenance, bounded planning, and experimental falsification. No file in this repository grants deployment, credential, training, installation, or protected-effect authority.
