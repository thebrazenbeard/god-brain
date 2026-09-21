from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_THREE_LANE_REASONING_PROTOCOL_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_THREE_LANE_REASONING_PROTOCOL_V0_1.json"

EXPECTED_TOP_LEVEL_KEYS = {
    "schema_version",
    "status",
    "repository",
    "base_head",
    "event_id",
    "lanes",
    "lane_roles",
    "first_pass_exposure_classes",
    "subject_packet_required_fields",
    "first_pass_required_fields",
    "workflow_states",
    "reconciliation_dispositions",
    "reconciliation_factors",
    "invariants",
    "required_hostile_cases",
    "research_stage",
    "claim_ceiling",
}

EXPECTED_LANES = {
    "GOD_BRAIN_COORDINATOR",
    "GOD_BRAIN_REZON_REASONER",
    "GOD_BRAIN_NULL_ENGINE",
}
EXPECTED_EXPOSURE = {
    "BLIND_AS_PRACTICAL",
    "PARTIALLY_EXPOSED",
    "FULLY_EXPOSED_TO_OTHER_LANE_CONCLUSIONS",
    "EXPOSURE_UNKNOWN",
}
EXPECTED_SUBJECT_PACKET_FIELDS = {
    "EVENT_ID",
    "REPOSITORY_AND_EXACT_HEAD_WHEN_APPLICABLE",
    "RELEVANT_PATHS_OR_BLOBS_WHEN_APPLICABLE",
    "LITERAL_PROPOSITION_OR_ARCHITECTURE_SUBJECT",
    "ADMITTED_EVIDENCE_SET",
    "CLAIM_CEILING",
    "PROTECTED_EFFECT_BOUNDARY",
    "REQUIRED_LANES",
    "LANE_EXPOSURE_DISCLOSURE",
}

EXPECTED_FIRST_PASS_FIELDS = {
    "EXACT_SUBJECT_BINDING",
    "CONCLUSION_OR_DISPOSITION",
    "COMPETING_HYPOTHESES_OR_INTERPRETATIONS",
    "STRONGEST_SUPPORTING_EVIDENCE",
    "STRONGEST_OPPOSING_EVIDENCE",
    "ASSUMPTIONS",
    "FALSIFIERS",
    "UNRESOLVED_DEPENDENCIES",
    "RECOMMENDED_DISCRIMINATING_TEST",
    "EXPOSURE_DISCLOSURE",
    "CLAIM_CEILING",
}

EXPECTED_RECONCILIATION_FACTORS = {
    "EXACT_SUBJECT_MATCH",
    "SOURCE_QUALITY",
    "SOURCE_INDEPENDENCE",
    "LOGICAL_VALIDITY",
    "CAUSAL_ADEQUACY",
    "ASSUMPTION_LOAD",
    "FALSIFIABILITY",
    "CONTRADICTION_SEVERITY",
    "PROVENANCE_CURRENTNESS",
    "EXPOSURE_CORRELATION",
    "PREDICTIVE_DISCRIMINATION",
}

EXPECTED_WORKFLOW = {
    "SUBJECT_BOUND",
    "FIRST_PASS_OPEN",
    "FIRST_PASS_FROZEN",
    "CROSS_EXAMINATION",
    "RECONCILIATION",
    "RESULT_OR_DISCRIMINATOR",
}
EXPECTED_DISPOSITIONS = {
    "CONVERGENT_INTERNAL_REASONING",
    "CONVERGENT_WITH_MATERIAL_SHARED_LINEAGE",
    "MATERIAL_DISAGREEMENT",
    "BLOCKED_BY_EVIDENCE_GAP",
    "BLOCKED_BY_CURRENTNESS_OR_PROVENANCE",
    "DISCRIMINATING_TEST_REQUIRED",
    "SUBJECT_INVALIDATED_OR_MOVED",
}
EXPECTED_INVARIANTS = {
    "SEPARATE_CHAT_NE_INDEPENDENT_CORROBORATION",
    "DIFFERENT_REASONING_HANDLER_NE_INDEPENDENT_EVIDENCE",
    "INTERNAL_AGREEMENT_NE_EXTERNAL_VALIDATION",
    "REZON_RESULT_NE_GOD_BRAIN_CONCLUSION",
    "NULL_FAILURE_TO_REFUTE_NE_PROOF",
    "NULL_REFUTATION_ATTEMPT_NE_AUTOMATIC_REJECTION",
    "SAME_TOPIC_NE_SAME_REVIEW_SUBJECT",
    "BLIND_AS_PRACTICAL_NE_INDEPENDENT_EVIDENCE",
    "REVISED_AFTER_CROSS_EXAMINATION_NE_ORIGINAL_FIRST_PASS",
    "CROSS_EXAMINATION_AFTER_FREEZE_NE_BLIND_FIRST_PASS",
    "CLAIM_QUALITY_GT_VOTE_COUNT",
    "HARD_EVIDENCE_BLOCKER_NE_OUTVOTABLE",
    "SAME_SOURCE_USED_BY_THREE_LANES_NE_THREE_SOURCES",
    "MULTIPLE_OUTPUTS_FROM_SHARED_ROOT_NE_INDEPENDENT_CORROBORATION",
    "CONVERGENT_INTERNAL_REASONING_NE_EXTERNAL_CORROBORATION",
    "UNRESOLVED_DISAGREEMENT_NE_FAILURE",
    "PROPOSED_TEST_NE_AUTHORIZED_EXPERIMENT",
    "MISSING_LANE_NE_IMPLIED_AGREEMENT",
    "REVIEWED_OLD_HEAD_NE_REVIEWED_NEW_HEAD",
    "THREE_INTERNAL_LANES_NE_EXTERNAL_REPLICATION",
}
EXPECTED_HOSTILE = {
    "TWO_PASS_ONE_EXACT_BLOCKER",
    "THREE_LANES_ONE_SOURCE_COUNTED_THREE_TIMES",
    "NULL_READS_REZON_BEFORE_FREEZE_LABELED_BLIND",
    "REZON_POST_CROSS_EXAM_REVISION_LABELED_ORIGINAL",
    "HEAD_MOVES_AFTER_ONE_LANE_REVIEW",
    "SAME_TOPIC_DIFFERENT_BLOB_TREATED_SAME_SUBJECT",
    "MISSING_LANE_TREATED_AS_AGREEMENT",
    "COPIED_FIXTURE_THREE_MATCHING_OUTPUTS_CLAIMED_INDEPENDENT",
    "SHARED_BLOCKER_SUMMARY_NOT_DISCLOSED",
    "DIFFERENT_MODEL_INVOCATION_COUNTED_INDEPENDENT_BY_DEFAULT",
    "COORDINATOR_PREFERENCE_OVERRIDES_STRONGER_EVIDENCE",
    "SPECULATIVE_OBJECTION_VETOES_VERIFIED_EVIDENCE",
    "SHARED_SOURCE_CONVERGENCE_PROMOTED_EXTERNAL_VALIDATION",
    "CROSS_EXAM_AGREEMENT_MISLABELED_BLIND",
    "EXACT_BLOCKER_AVERAGED_AWAY_BY_CONFIDENCE",
    "PROPOSED_TEST_TREATED_AS_RUN_AUTHORITY",
    "UNRESOLVED_DISAGREEMENT_OMITTED",
    "MOVED_HEAD_RESULT_REMAINS_CURRENT",
    "THREE_LANE_CONSENSUS_PROMOTED_ANOMALY_TO_CONTACT",
    "INTERNAL_PROTOCOL_PASS_PROMOTED_SCIENTIFIC_QUALIFICATION",
}
EXPECTED_CEILING = {
    "NO_STATISTICAL_LANE_INDEPENDENCE_CLAIM",
    "NO_DEFAULT_EPISTEMIC_LANE_INDEPENDENCE_CLAIM",
    "NO_EVIDENCE_SOURCE_INDEPENDENCE_PROOF",
    "NO_REVIEWER_INDEPENDENCE_PROOF",
    "NO_EXTERNAL_CORROBORATION_CLAIM",
    "NO_SCIENTIFIC_VALIDATION_CLAIM",
    "NO_DETECTOR_OR_MODEL_QUALIFICATION",
    "NO_ANOMALY_CLAIM",
    "NO_EXTERNAL_CONTACT_CLAIM",
    "NO_SIMULATION_EVIDENCE_CLAIM",
    "NO_EXPERIMENT_EXECUTION_AUTHORITY",
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
        return [f"invalid three-lane protocol: {exc}"]

    if set(spec) != EXPECTED_TOP_LEVEL_KEYS:
        errors.append("top-level machine contract keys must be exact closed set")

    if spec.get("schema_version") != "GOD_BRAIN_THREE_LANE_REASONING_PROTOCOL_V0_1":
        errors.append("schema version drifted")
    if spec.get("status") != "RESEARCH_ARCHITECTURE":
        errors.append("status drifted")
    if spec.get("repository") != "thebrazenbeard/god-brain":
        errors.append("repository drifted")
    if spec.get("base_head") != "c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5":
        errors.append("base head drifted")
    if spec.get("event_id") != "GB_THREE_LANE_20260921_V1":
        errors.append("event id drifted")

    _exact_set(errors, spec.get("lanes"), EXPECTED_LANES, "lanes")
    _exact_set(errors, spec.get("subject_packet_required_fields"), EXPECTED_SUBJECT_PACKET_FIELDS, "subject packet required fields")
    _exact_set(errors, spec.get("first_pass_required_fields"), EXPECTED_FIRST_PASS_FIELDS, "first pass required fields")
    _exact_set(errors, spec.get("reconciliation_factors"), EXPECTED_RECONCILIATION_FACTORS, "reconciliation factors")
    _exact_set(errors, spec.get("first_pass_exposure_classes"), EXPECTED_EXPOSURE, "first pass exposure classes")
    _exact_set(errors, spec.get("workflow_states"), EXPECTED_WORKFLOW, "workflow states")
    _exact_set(errors, spec.get("reconciliation_dispositions"), EXPECTED_DISPOSITIONS, "reconciliation dispositions")
    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    _exact_set(errors, spec.get("required_hostile_cases"), EXPECTED_HOSTILE, "hostile cases")
    _exact_set(errors, spec.get("claim_ceiling"), EXPECTED_CEILING, "claim ceiling")

    expected_roles = {
        "GOD_BRAIN_COORDINATOR": "SUBJECT_BINDING_AND_EPISTEMIC_RECONCILIATION",
        "GOD_BRAIN_REZON_REASONER": "HETEROGENEOUS_MULTI_VIEW_REASONING",
        "GOD_BRAIN_NULL_ENGINE": "CAUSAL_FALSIFICATION_AND_RIVAL_EXPLANATIONS",
    }
    if spec.get("lane_roles") != expected_roles:
        errors.append("lane roles drifted")

    if spec.get("research_stage") != "ARCHITECTURE":
        errors.append("research stage must remain ARCHITECTURE")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "SEPARATE_CHAT != INDEPENDENT_CORROBORATION",
        "DIFFERENT_REASONING_HANDLER != INDEPENDENT_EVIDENCE",
        "INTERNAL_AGREEMENT != EXTERNAL_VALIDATION",
        "CLAIM_QUALITY > VOTE_COUNT",
        "HARD_EVIDENCE_BLOCKER != OUTVOTABLE",
        "CROSS_EXAMINATION_AFTER_FREEZE != BLIND_FIRST_PASS",
        "MISSING_LANE != IMPLIED_AGREEMENT",
        "THREE_INTERNAL_LANES != EXTERNAL_REPLICATION",
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
    print("God Brain three-lane reasoning protocol: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
