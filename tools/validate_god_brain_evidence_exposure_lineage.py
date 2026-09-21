from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_EVIDENCE_EXPOSURE_LINEAGE_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_EVIDENCE_EXPOSURE_LINEAGE_V0_1.json"

EXPECTED_STATUSES = {
    "NO_RECORDED_EXPOSURE",
    "KNOWN_DIRECT_EXPOSURE",
    "KNOWN_DERIVED_EXPOSURE",
    "EXPOSURE_UNKNOWN",
}
EXPECTED_RECIPIENTS = {
    "HUMAN",
    "HUMAN_ROLE",
    "MODEL_INVOCATION",
    "PERSISTENT_MODEL_OR_AGENT",
    "CHAT_OR_SESSION_CONTEXT",
    "WORKER_OR_PROCESS",
    "TOOL_OR_RUNTIME",
    "DATA_GENERATION_PROCESS",
    "REPOSITORY_ARTIFACT_OR_DOCUMENT",
}
EXPECTED_CLASSES = {
    "RAW_HOLDOUT_OBSERVATIONS",
    "GROUND_TRUTH_LABELS",
    "AGGREGATE_METRICS",
    "PER_EXAMPLE_METRICS",
    "MODEL_OR_DETECTOR_OUTPUTS",
    "COMPARISON_RESULTS",
    "RANKING_OR_SELECTION_OUTCOMES",
    "ANOMALY_FLAGS",
    "REVIEWER_FINDINGS",
    "FAILURE_TRACES",
    "DERIVED_SUMMARIES",
    "TRANSFORMED_OR_REDACTED_ARTIFACTS",
    "PROMPT_OR_CONTEXT_DERIVATIVE",
}
EXPECTED_EVENT_FIELDS = {
    "STUDY_OR_LINEAGE_SUBJECT",
    "EVIDENCE_ARTIFACT_SUBJECT",
    "EXPOSURE_CLASS",
    "RECIPIENT_IDENTITY_CLASS",
    "RECIPIENT_IDENTITY_REFERENCE",
    "EXECUTION_OR_CONTEXT_IDENTITY",
    "SOURCE_LINEAGE",
    "CHANNEL_OR_PROVENANCE_REFERENCE",
    "OBSERVED_ORDERING_EVIDENCE",
    "INFORMATION_SCOPE",
    "DIRECT_OR_DERIVED",
    "RECORDER_EVIDENCE_PROVENANCE",
    "CLAIM_CEILING",
}
EXPECTED_INVARIANTS = {
    "NO_RECORDED_EXPOSURE_NE_PROOF_OF_NONACCESS",
    "RESULT_EXPOSURE_NE_RAW_DATA_EXPOSURE",
    "RESULT_EXPOSURE_CAN_CONTAMINATE_FUTURE_DESIGN",
    "RECORDED_TIMESTAMP_NE_TRUSTED_TIME",
    "NEW_CHAT_NE_CLEAN_REVIEWER",
    "NEW_PROCESS_NE_UNEXPOSED_PROCESS",
    "NEW_ROLE_NE_INFORMATION_INDEPENDENCE",
    "DERIVATION_CAN_PROPAGATE_EXPOSURE_WITHOUT_COPYING_RAW_DATA",
    "NEW_ARTIFACT_DIGEST_NE_NEW_INFORMATION_LINEAGE",
    "TRANSFORMATION_NE_DECONTAMINATION",
    "POST_EXPOSURE_DESIGN_NE_UNTOUCHED_CONFIRMATORY_DESIGN",
    "SEPARATE_CHAT_NE_INDEPENDENT_CORROBORATION",
    "DIFFERENT_MODEL_INVOCATION_NE_INDEPENDENT_CORROBORATION",
    "ROLE_SEPARATION_NE_INFORMATION_INDEPENDENCE",
    "MULTIPLE_OUTPUTS_FROM_ONE_EXPOSED_ROOT_NE_INDEPENDENT_EVIDENCE",
    "UNKNOWN_EXPOSURE_NE_NO_EXPOSURE",
    "NO_CONTEXT_EXPOSURE_NE_NO_MODEL_PRIOR_KNOWLEDGE",
    "NEW_SUBJECT_NE_CLEAN_SUBJECT_IF_DERIVED_FROM_EXPOSED_EVIDENCE",
    "NO_RECORDED_EXPOSURE_PLUS_LOCAL_LINEAGE_NE_PROOF_OF_UNTOUCHED_EVIDENCE",
    "STUDY_LINEAGE_NE_EXPOSURE_LINEAGE",
    "EXPOSURE_LINEAGE_NE_STUDY_LINEAGE",
    "CLEANER_EXPOSURE_GOVERNANCE_NE_ANOMALY",
    "ANOMALY_NE_CONTACT",
    "CONTACT_CANDIDATE_NE_SIMULATOR_IDENTITY",
    "EXPOSURE_LEDGER_PASS_NE_EXTERNAL_SCIENTIFIC_VALIDATION",
}
EXPECTED_HOSTILE = {
    "RAW_HOLDOUT_RENAMED",
    "HOLDOUT_SUMMARY_WITHOUT_RAW_ROWS",
    "WINNER_ONLY_DISCLOSURE",
    "FAILURE_CASES_PARAPHRASED_INTO_PROMPT",
    "POST_HOLDOUT_REPAIR_MISLABELED_PRE_HOLDOUT",
    "NEW_CHAT_SEEDED_WITH_EXPOSED_SUMMARY",
    "NEW_PROCESS_SEEDED_WITH_EXPOSED_ARTIFACT",
    "NEW_ROLE_SAME_EXPOSED_HUMAN",
    "TWO_REVIEWS_ONE_PRIOR_VERDICT",
    "TRANSFORMED_ARTIFACT_FALSE_DECONTAMINATION",
    "NEW_STUDY_DERIVED_FROM_EXPOSED_PREDECESSOR_FALSE_CLEAN",
    "MISSING_RECORD_PROMOTED_TO_NONACCESS_PROOF",
    "UNKNOWN_EXPOSURE_PROMOTED_TO_NO_EXPOSURE",
    "TIMESTAMP_PROMOTED_TO_TRUSTED_ORDERING",
    "RAW_NONEXPOSURE_IGNORES_RESULT_EXPOSURE",
    "NO_CONTEXT_EXPOSURE_PROMOTED_TO_NO_PRIOR_MODEL_KNOWLEDGE",
    "COPIED_GENERATED_TESTS_PROMOTED_TO_INDEPENDENCE",
    "REVIEWER_BLOCKER_KNOWLEDGE_OMITTED",
    "RECIPIENT_RELABEL_BREAKS_LINEAGE",
    "LOCAL_LEDGER_PASS_PROMOTED_TO_EXTERNAL_VALIDATION",
}
EXPECTED_CEILING = {
    "NO_EXPOSURE_LEDGER_IMPLEMENTATION",
    "NO_COMPLETE_LOGGING_PROOF",
    "NO_NONACCESS_PROOF",
    "NO_TRUSTED_TIME_PROOF",
    "NO_EXTERNAL_CUSTODY_PROOF",
    "NO_REVIEWER_INDEPENDENCE_PROOF",
    "NO_TRAINING_DATA_ABSENCE_PROOF",
    "NO_STATISTICAL_INDEPENDENCE_PROOF",
    "NO_HIDDEN_HISTORY_COMPLETENESS_PROOF",
    "NO_DETECTOR_OR_MODEL_QUALIFICATION",
    "NO_ANOMALY_CLAIM",
    "NO_EXTERNAL_CONTACT_CLAIM",
    "NO_SIMULATION_EVIDENCE_CLAIM",
    "NO_PROVIDER_OR_CONTROL_AUTHORITY",
    "NO_MERGE_AUTHORITY",
    "NO_DEPLOYMENT_AUTHORITY",
    "NO_CANONICAL_PROMOTION",
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
        return [f"invalid exposure-lineage spec: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_EVIDENCE_EXPOSURE_LINEAGE_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_ARCHITECTURE":
        errors.append("status drifted")
    if spec.get("god_brain_base_head") != "c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5":
        errors.append("God Brain base drifted")
    if spec.get("event_id") != "GB_DG_TRIAD_20260921_V1":
        errors.append("event id drifted")

    _exact_set(errors, spec.get("exposure_statuses"), EXPECTED_STATUSES, "exposure statuses")
    _exact_set(errors, spec.get("recipient_identity_classes"), EXPECTED_RECIPIENTS, "recipient identity classes")
    _exact_set(errors, spec.get("evidence_exposure_classes"), EXPECTED_CLASSES, "evidence exposure classes")
    _exact_set(errors, spec.get("exposure_event_required_fields"), EXPECTED_EVENT_FIELDS, "exposure event fields")
    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    _exact_set(errors, spec.get("required_hostile_cases"), EXPECTED_HOSTILE, "required hostile cases")
    _exact_set(errors, spec.get("claim_ceiling"), EXPECTED_CEILING, "claim ceiling")

    if spec.get("forbidden_statuses") != ["PROVEN_UNEXPOSED"]:
        errors.append("PROVEN_UNEXPOSED must remain forbidden")

    expected_decision = {
        "KNOWN_DIRECT_EXPOSURE": "REJECT_UNTOUCHED_CLAIM",
        "KNOWN_DERIVED_EXPOSURE": "REJECT_UNTOUCHED_CLAIM",
        "EXPOSURE_UNKNOWN": "UNTOUCHED_CLAIM_UNSUPPORTED",
        "NO_RECORDED_EXPOSURE": "LOCALLY_COMPATIBLE_BUT_INSUFFICIENT",
    }
    if spec.get("untouched_decision") != expected_decision:
        errors.append("untouched decision semantics drifted")

    expected_propagation = {
        "derived_artifacts_inherit_relevant_exposure_by_default": True,
        "hash_change_clears_exposure": False,
        "format_change_clears_exposure": False,
        "summary_clears_exposure": False,
        "redaction_clears_exposure_automatically": False,
        "separate_sanitization_contract_required_for_narrower_scope": True,
    }
    if spec.get("propagation") != expected_propagation:
        errors.append("exposure propagation semantics drifted")

    if spec.get("research_stage") != "ARCHITECTURE":
        errors.append("research stage must remain ARCHITECTURE")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "NO_RECORDED_EXPOSURE != PROOF_OF_NONACCESS",
        "NEW_CHAT != CLEAN_REVIEWER",
        "NEW_ARTIFACT_DIGEST != NEW_INFORMATION_LINEAGE",
        "TRANSFORMATION != DECONTAMINATION",
        "POST_EXPOSURE_DESIGN != UNTOUCHED_CONFIRMATORY_DESIGN",
        "SEPARATE_CHAT != INDEPENDENT_CORROBORATION",
        "UNKNOWN_EXPOSURE != NO_EXPOSURE",
        "NO_CONTEXT_EXPOSURE != NO_MODEL_PRIOR_KNOWLEDGE",
        "STUDY_LINEAGE != EXPOSURE_LINEAGE",
        "EXPOSURE_LEDGER_PASS != EXTERNAL_SCIENTIFIC_VALIDATION",
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
    print("God Brain evidence exposure lineage: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
