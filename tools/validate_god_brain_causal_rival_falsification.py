from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_CAUSAL_RIVAL_FALSIFICATION_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_CAUSAL_RIVAL_FALSIFICATION_V0_1.json"

EXPECTED_TOP_LEVEL_KEYS = {
    "schema_version",
    "status",
    "repository",
    "base_head",
    "event_id",
    "minimum_rival_families",
    "hypothesis_required_fields",
    "precommitment_states",
    "comparison_required_fields",
    "rival_states",
    "output_dispositions",
    "invariants",
    "required_hostile_cases",
    "research_stage",
    "claim_ceiling",
}

EXPECTED_RIVALS = {
    "RANDOM_VARIATION_OR_MULTIPLE_COMPARISON",
    "MEASUREMENT_OR_INSTRUMENTATION",
    "SOFTWARE_PIPELINE_OR_TOOLING",
    "MODEL_BEHAVIOR_OR_PRIOR_KNOWLEDGE",
    "PROMPT_CONTEXT_MEMORY_RETRIEVAL_LEAKAGE",
    "HUMAN_OPERATOR_CUEING_OR_SELECTION",
    "SHARED_SOURCE_OR_COMMON_CAUSE",
    "TIMING_SYNCHRONIZATION_CACHE_OR_ROUTING",
    "ORDINARY_EXTERNAL_INFORMATION_CHANNEL",
    "KNOWN_SYSTEM_AGENCY",
    "UNKNOWN_ORDINARY_MECHANISM",
    "EXTERNAL_SOURCE_OR_INTERVENTION_HYPOTHESIS",
}

EXPECTED_PRECOMMITMENT = {
    "PRECOMMITTED_BEFORE_TARGET_EVIDENCE",
    "REVISED_BEFORE_TARGET_EVIDENCE",
    "CREATED_AFTER_TARGET_EVIDENCE",
    "REVISED_AFTER_TARGET_EVIDENCE",
    "TIMING_UNKNOWN",
}

EXPECTED_RIVAL_STATES = {
    "UNTESTED",
    "COMPATIBLE_WITH_CURRENT_EVIDENCE",
    "DISFAVORED_BY_DISCRIMINATING_EVIDENCE",
    "FALSIFIED_WITHIN_DECLARED_SCOPE",
    "INVALID_OR_UNTESTABLE_AS_STATED",
    "EVIDENCE_INSUFFICIENT",
    "SUBJECT_MOVED_OR_REDEFINED",
}

EXPECTED_DISPOSITIONS = {
    "NO_DISCRIMINATION",
    "RIVAL_SET_INCOMPLETE",
    "MATERIAL_CONFOUNDER_UNRESOLVED",
    "ONE_OR_MORE_RIVALS_DISFAVORED",
    "FAVORED_WITHIN_DECLARED_RIVAL_SET",
    "MODEL_DISCRIMINATING_RESULT_CANDIDATE",
    "SUBJECT_INVALIDATED_OR_MOVED",
}

EXPECTED_INVARIANTS = {
    "OBSERVATION_NE_CAUSE",
    "CORRELATION_NE_CAUSATION",
    "FAILURE_TO_FALSIFY_NE_CONFIRMATION",
    "ONE_FAILED_RIVAL_NE_FAVORED_HYPOTHESIS_CONFIRMED",
    "BETTER_FIT_NE_UNIQUE_CAUSAL_EXPLANATION",
    "FAVORED_WITHIN_DECLARED_RIVAL_SET_NE_UNIQUE_CAUSE",
    "FALSIFIED_SUBMODEL_NE_FALSIFIED_ONTOLOGY",
    "UNMEASURED_CONFOUNDER_NE_ABSENT_CONFOUNDER",
    "UNTESTED_ORDINARY_MECHANISM_NE_DISPROVEN_ORDINARY_MECHANISM",
    "POST_HOC_EXPLANATION_NE_PRECOMMITTED_PREDICTION",
    "MODEL_SELECTION_NE_CAUSAL_DISCOVERY",
    "UNKNOWN_ORDINARY_MECHANISM_NE_EXTRAORDINARY_MECHANISM",
    "DECLARED_RIVAL_SET_NE_EXHAUSTIVE_CAUSAL_SPACE",
    "HYPOTHESIS_LABEL_NE_HYPOTHESIS_IDENTITY",
    "POST_EVIDENCE_FIT_NE_PRIOR_PREDICTIVE_SUCCESS",
    "COMPATIBLE_WITH_H_NE_CAUSED_BY_H",
    "RIVAL_ELIMINATION_NE_PROBABILITY_TRANSFER_TO_FAVORITE",
    "UNRESOLVED_CONFOUNDER_NE_CONTROLLED_CONFOUNDER",
    "DIFFERENT_STORIES_SAME_PREDICTION_NE_DISCRIMINATING_TEST",
    "ASSOCIATED_COMPONENT_NE_NECESSARY_CAUSE",
    "KNOWN_RIVALS_EXHAUSTED_NE_ORDINARY_CAUSAL_SPACE_EXHAUSTED",
    "EXPLANATION_GENERATION_NE_CONFIRMATORY_VALIDATION",
    "ANOMALY_NE_CONTACT",
    "CONTACT_CANDIDATE_NE_SIMULATOR_IDENTITY",
}

EXPECTED_HOSTILE = {
    "ONE_FAILED_ORDINARY_RIVAL_PROVES_CONTACT",
    "FAVORED_FIT_RELABELLED_UNIQUE_CAUSE",
    "POST_HOC_RELABELLED_PRECOMMITTED",
    "MISSING_CONFOUNDER_TREATED_ABSENT",
    "KNOWN_RIVALS_TREATED_EXHAUSTIVE",
    "CORRELATED_OBSERVATIONS_COUNTED_INDEPENDENT",
    "SUCCESSFUL_TRIAL_SELECTION",
    "SHARED_MODEL_SOURCE_LINEAGE_COUNTED_INDEPENDENT",
    "SOFTWARE_ARTIFACT_OMITTED",
    "ORDINARY_EXTERNAL_CHANNEL_UNAUDITED",
    "UNKNOWN_ORDINARY_MECHANISM_REMOVED",
    "UNCHANGED_LABEL_CHANGED_CAUSAL_ASSUMPTIONS",
    "NEW_ID_HIDES_POST_EVIDENCE_REVISION",
    "COMPATIBILITY_RELABELLED_CAUSAL_IDENTIFICATION",
    "IDENTICAL_PREDICTIONS_RELABELLED_DISCRIMINATING",
    "NEGATIVE_CONTROL_FAILURE_IGNORED",
    "ABLATION_NON_EFFECT_COMPONENT_CALLED_NECESSARY",
    "FALSIFIED_SUBMODEL_RELABELLED_GENERIC_SIMULATION_REFUTATION",
    "RIVAL_COUNT_PROMOTES_ANOMALY_TO_CONTACT",
    "INTERNAL_CAUSAL_PASS_PROMOTED_EXTERNAL_VALIDATION",
}

EXPECTED_CEILING = {
    "NO_CAUSAL_DISCOVERY_PROOF",
    "NO_EXHAUSTIVE_RIVAL_SET_PROOF",
    "NO_HIDDEN_CONFOUNDER_ABSENCE_PROOF",
    "NO_SIMULATION_PROBABILITY_ASSIGNMENT",
    "NO_ANOMALY_CLAIM",
    "NO_AGENCY_CLAIM",
    "NO_EXTERNAL_CONTACT_CLAIM",
    "NO_SIMULATOR_IDENTITY_CLAIM",
    "NO_DEITY_IDENTITY_CLAIM",
    "NO_EXPERIMENT_EXECUTION_AUTHORITY",
    "NO_DETECTOR_OR_MODEL_QUALIFICATION",
    "NO_EXTERNAL_SCIENTIFIC_VALIDATION_CLAIM",
    "NO_PROVIDER_OR_CONTROL_AUTHORITY",
    "NO_MERGE_AUTHORITY",
    "NO_DEPLOYMENT_AUTHORITY",
    "NO_CANONICAL_PROMOTION",
}

EXPECTED_HYP_FIELDS = {
    "HYPOTHESIS_ID",
    "PROPOSITION",
    "HYPOTHESIS_CLASS",
    "PREDICTED_OBSERVATIONS",
    "TENSION_OR_NONPREDICTED_OBSERVATIONS",
    "CAUSAL_ASSUMPTIONS",
    "AUXILIARY_ASSUMPTIONS",
    "CONFOUNDERS_AND_COMMON_CAUSES",
    "SELECTION_MECHANISMS",
    "FALSIFIERS",
    "COUNTERFACTUAL_PREDICTIONS",
    "PRECOMMITMENT_STATE",
    "EVIDENCE_REFERENCES",
    "CLAIM_CEILING",
}

EXPECTED_COMPARISON_FIELDS = {
    "EXACT_OBSERVATION_SUBJECT",
    "HYPOTHESIS_SET",
    "SHARED_ASSUMPTIONS",
    "DISCRIMINATING_EVIDENCE",
    "UNRESOLVED_CONFOUNDERS",
    "NEGATIVE_CONTROLS",
    "ABLATIONS_OR_PERTURBATIONS",
    "COUNTERFACTUAL_TESTS",
    "RIVAL_ELIMINATION_LEDGER",
    "NEW_HYPOTHESIS_POLICY",
    "STOPPING_RULE",
    "OUTPUT_DISPOSITION",
    "CLAIM_CEILING",
}

def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root must be object")
    return value

def _exact_set(errors: list[str], value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be list")
        return
    if len(value) != len(set(value)):
        errors.append(f"{label} must not contain duplicates")
    if set(value) != expected:
        errors.append(f"{label} must be exact closed set")

def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (DOC_PATH, SPEC_PATH):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        spec = _load(root / SPEC_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid causal-rival spec: {exc}"]

    if set(spec) != EXPECTED_TOP_LEVEL_KEYS:
        errors.append("top-level machine contract keys must be exact closed set")
    if spec.get("schema_version") != "GOD_BRAIN_CAUSAL_RIVAL_FALSIFICATION_V0_1":
        errors.append("schema version drifted")
    if spec.get("status") != "RESEARCH_ARCHITECTURE":
        errors.append("status drifted")
    if spec.get("repository") != "thebrazenbeard/god-brain":
        errors.append("repository drifted")
    if spec.get("base_head") != "c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5":
        errors.append("base head drifted")
    if spec.get("event_id") != "GB_THREE_LANE_20260921_V1":
        errors.append("event id drifted")

    _exact_set(errors, spec.get("minimum_rival_families"), EXPECTED_RIVALS, "minimum rival families")
    _exact_set(errors, spec.get("hypothesis_required_fields"), EXPECTED_HYP_FIELDS, "hypothesis fields")
    _exact_set(errors, spec.get("precommitment_states"), EXPECTED_PRECOMMITMENT, "precommitment states")
    _exact_set(errors, spec.get("comparison_required_fields"), EXPECTED_COMPARISON_FIELDS, "comparison fields")
    _exact_set(errors, spec.get("rival_states"), EXPECTED_RIVAL_STATES, "rival states")
    _exact_set(errors, spec.get("output_dispositions"), EXPECTED_DISPOSITIONS, "output dispositions")
    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    _exact_set(errors, spec.get("required_hostile_cases"), EXPECTED_HOSTILE, "hostile cases")
    _exact_set(errors, spec.get("claim_ceiling"), EXPECTED_CEILING, "claim ceiling")

    if spec.get("research_stage") != "ARCHITECTURE":
        errors.append("research stage must remain ARCHITECTURE")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "OBSERVATION != CAUSE",
        "FAILURE_TO_FALSIFY != CONFIRMATION",
        "ONE_FAILED_RIVAL != FAVORED_HYPOTHESIS_CONFIRMED",
        "BETTER_FIT != UNIQUE_CAUSAL_EXPLANATION",
        "FAVORED_WITHIN_DECLARED_RIVAL_SET != UNIQUE_CAUSE",
        "FALSIFIED_SUBMODEL != FALSIFIED_ONTOLOGY",
        "POST_HOC_EXPLANATION != PRECOMMITTED_PREDICTION",
        "KNOWN_RIVALS_EXHAUSTED != ORDINARY_CAUSAL_SPACE_EXHAUSTED",
        "ANOMALY != CONTACT",
        "CONTACT_CANDIDATE != SIMULATOR_IDENTITY",
    ):
        if marker not in doc:
            errors.append(f"research doc missing marker: {marker}")

    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain causal-rival falsification protocol: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
