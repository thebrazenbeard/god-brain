from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DOC_PATH = "docs/research/GOD_BRAIN_PROVENANCE_ANCESTRY_CONTRACT_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_PROVENANCE_ANCESTRY_CONTRACT_V0_1.json"
FIXTURE_PATH = "specs/research/fixtures/GOD_BRAIN_PROVENANCE_ANCESTRY_HOSTILE_CASES_V0_1.json"

REQUIRED_INVARIANTS = {
    "SOURCE_COUNT_NE_INDEPENDENT_CORROBORATION",
    "SAME_ROOT_DESCENDANTS_NE_INDEPENDENT_EVIDENCE",
    "TEMPORAL_ORDER_NE_CAUSAL_DERIVATION",
    "DERIVED_FROM_NE_EQUIVALENT_TO",
    "RETRIEVED_NE_INCORPORATED",
    "HISTORICAL_EVIDENCE_NE_CURRENT_AUTHORITY",
    "SEMANTIC_SIMILARITY_NE_PROVENANCE_EQUIVALENCE",
    "PRIVACY_PROJECTION_NE_RAW_SOURCE",
    "PROVENANCE_NE_TRUTH",
    "DISTINCT_INSTANCE_NE_INDEPENDENT_EVIDENCE",
    "REVIEW_OF_PARENT_HEAD_NE_REVIEW_OF_CHILD_HEAD",
    "PROVENANCE_POINTER_NE_PAYLOAD_TRANSFER",
    "PROVENANCE_DAG_NE_ALL_RELATIONS_GRAPH",
}

EXPECTED_ARTIFACT_CLASSES = [
    "SOURCE_INSTANCE",
    "EVIDENCE_SPAN",
    "PROJECTION",
    "DERIVED_ARTIFACT",
    "INTERPRETATION",
    "PROPOSITION",
    "MEMORY_RECORD",
    "REVIEW_RECORD",
]

EXPECTED_INDEPENDENCE_STATES = [
    "INDEPENDENT_WITHIN_DECLARED_SCOPE",
    "PARTIALLY_SHARED_ANCESTRY",
    "SHARED_ROOT_ANCESTRY",
    "COMMON_GENERATION_CHANNEL",
    "ANCESTRY_UNKNOWN",
    "NOT_APPLICABLE",
]

EXPECTED_PROVENANCE_EDGE_TYPES = {
    "EXTRACTED_FROM",
    "DERIVED_FROM",
    "SUMMARIZED_FROM",
    "TRANSLATED_FROM",
    "NORMALIZED_FROM",
    "REDACTED_FROM",
    "COPIED_FROM",
    "GENERATED_USING",
    "AGGREGATED_FROM",
    "RETRIEVED_FROM",
    "REPLAYED_FROM",
}

EXPECTED_LIFECYCLE_EDGE_TYPES = {
    "REFINES", "SUPERSEDES", "RETRACTS", "EVOLVED_FROM"
}
EXPECTED_EPISTEMIC_EDGE_TYPES = {"SUPPORTS", "CONTRADICTS"}
EXPECTED_IDENTITY_EDGE_TYPES = {
    "EQUIVALENT_TO", "DISTINCT_FROM", "RELATED_NOT_EQUIVALENT"
}
EXPECTED_TEMPORAL_EDGE_TYPES = {"PRECEDES", "FOLLOWS"}

EXPECTED_INDEPENDENCE_RULES = {
    "DIFFERENT_ARTIFACT_IDS_DO_NOT_IMPLY_INDEPENDENCE",
    "DIFFERENT_REPOSITORY_PATHS_DO_NOT_IMPLY_INDEPENDENCE",
    "DIFFERENT_CHATS_DO_NOT_IMPLY_INDEPENDENCE",
    "DIFFERENT_AGENTS_DO_NOT_IMPLY_INDEPENDENCE",
    "DIFFERENT_MODELS_DO_NOT_IMPLY_INDEPENDENCE_WITHOUT_RELEVANT_ANCESTRY_ANALYSIS",
    "DIFFERENT_TIMESTAMPS_DO_NOT_IMPLY_INDEPENDENCE",
    "PROJECTION_AND_SOURCE_ARE_NOT_INDEPENDENT",
    "CORRECTION_AND_CORRECTED_SOURCE_ARE_NOT_INDEPENDENT_SUPPORT",
    "COPIED_DOWNSTREAM_CITATION_IS_NOT_SECOND_SOURCE",
    "INDEPENDENCE_IS_CLAIM_RELATIVE",
}

EXPECTED_CURRENTNESS_STATES = {
    "CURRENT", "HISTORICAL", "SUPERSEDED", "RETRACTED", "UNRESOLVED", "UNKNOWN"
}
EXPECTED_REQUIRED_ARTIFACT_FIELDS = {
    "artifact_id", "artifact_class", "created_at", "currentness", "privacy_class",
    "parents", "root_family_ids", "independence_state", "provenance_ceiling",
}
EXPECTED_PARENT_EDGE_FIELDS = {"artifact_id", "edge_type"}
EXPECTED_QUERY_CONTRACTS = {
    "WHY_DO_WE_BELIEVE_THIS",
    "WHERE_DID_THIS_COME_FROM",
    "ARE_THESE_RESULTS_INDEPENDENT",
    "WHAT_CHANGED",
    "IS_THIS_CURRENT",
}
EXPECTED_NEXT_GATE = {
    "INDEPENDENT_REVIEW",
    "MACHINE_SCHEMA",
    "HOSTILE_ANCESTRY_FIXTURES",
    "REFERENCE_GRAPH_EVALUATOR",
    "CROSS_REPO_TRANSFER_RECEIPT_INTEGRATION",
}

REQUIRED_INVALID_STATES = {
    "SELF_PARENT_EDGE",
    "UNKNOWN_PROVENANCE_EDGE_TYPE",
    "DUPLICATE_PARENT_EDGE",
    "PROVENANCE_CYCLE",
    "INDEPENDENT_STATE_WITH_SHARED_MATERIAL_ROOT",
    "PRIVACY_PROJECTION_CLAIMS_RAW_SOURCE_IDENTITY",
    "EXACT_EVIDENCE_SPAN_WITHOUT_SOURCE_VERSION_REPRESENTATION_BINDING",
    "DERIVED_ARTIFACT_WITHOUT_TRANSFORM_IDENTITY",
    "REVIEW_VERDICT_BOUND_TO_DIFFERENT_HEAD",
    "SUPERSESSION_DELETES_PREDECESSOR_HISTORY",
    "CHRONOLOGY_USED_AS_CAUSAL_PROOF",
    "UNKNOWN_ANCESTRY_PROMOTED_TO_INDEPENDENT",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root must be object")
    return value


def validate_provenance_ancestry(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in (DOC_PATH, SPEC_PATH, FIXTURE_PATH):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        spec = _load(root / SPEC_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"{SPEC_PATH} invalid JSON: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_PROVENANCE_ANCESTRY_CONTRACT_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_PROPOSAL_MACHINE_CONTRACT":
        errors.append("status must remain research proposal")

    ceilings = set(spec.get("claim_ceiling", []))
    for item in (
        "NO_CANONICAL_PROMOTION",
        "NO_RUNTIME_IMPLEMENTATION_CLAIM",
        "NO_COMPLETE_LINEAGE_CAPTURE_CLAIM",
        "NO_INDEPENDENCE_PROOF_FROM_UNKNOWN_ANCESTRY",
        "NO_PRIVATE_PAYLOAD_TRANSFER",
    ):
        if item not in ceilings:
            errors.append(f"claim ceiling missing {item}")

    missing = REQUIRED_INVARIANTS - set(spec.get("invariants", []))
    if missing:
        errors.append(f"invariants missing: {sorted(missing)}")

    sources = spec.get("source_provenance")
    if not isinstance(sources, list) or len(sources) != 4:
        errors.append("source provenance must bind exactly four source repositories")
    else:
        expected = [
            "thebrazenbeard/roots",
            "thebrazenbeard/semanticatlas",
            "thebrazenbeard/temporal",
            "thebrazenbeard/deepmemorystorage",
        ]
        actual = [source.get("repository") for source in sources if isinstance(source, dict)]
        if actual != expected:
            errors.append("source provenance repository order/set drifted")
        for source in sources:
            if not isinstance(source, dict):
                errors.append("source provenance entry must be object")
                continue
            artifacts = source.get("artifacts")
            if not isinstance(artifacts, list) or not artifacts:
                errors.append(f"{source.get('repository')} lacks exact artifact provenance")
                continue
            for artifact in artifacts:
                if not isinstance(artifact, list) or len(artifact) != 2:
                    errors.append(f"{source.get('repository')} artifact binding malformed")
                    continue
                if not isinstance(artifact[1], str) or len(artifact[1]) != 40:
                    errors.append(f"{source.get('repository')} artifact blob invalid")

    if spec.get("artifact_classes") != EXPECTED_ARTIFACT_CLASSES:
        errors.append("artifact class set/order drifted")

    if spec.get("independence_states") != EXPECTED_INDEPENDENCE_STATES:
        errors.append("independence state set/order drifted")

    exact_set_surfaces = (
        ("provenance_edge_types", EXPECTED_PROVENANCE_EDGE_TYPES),
        ("lifecycle_edge_types", EXPECTED_LIFECYCLE_EDGE_TYPES),
        ("epistemic_edge_types", EXPECTED_EPISTEMIC_EDGE_TYPES),
        ("identity_edge_types", EXPECTED_IDENTITY_EDGE_TYPES),
        ("temporal_edge_types", EXPECTED_TEMPORAL_EDGE_TYPES),
        ("independence_rules", EXPECTED_INDEPENDENCE_RULES),
        ("currentness_states", EXPECTED_CURRENTNESS_STATES),
        ("required_artifact_fields", EXPECTED_REQUIRED_ARTIFACT_FIELDS),
        ("parent_edge_required_fields", EXPECTED_PARENT_EDGE_FIELDS),
        ("query_contracts", EXPECTED_QUERY_CONTRACTS),
        ("next_gate", EXPECTED_NEXT_GATE),
    )
    for field, expected in exact_set_surfaces:
        value = spec.get(field)
        if not isinstance(value, list):
            errors.append(f"{field} must be a list")
            continue
        if len(value) != len(set(value)):
            errors.append(f"{field} contains duplicate values")
        if set(value) != expected:
            missing = sorted(expected - set(value))
            extra = sorted(set(value) - expected)
            errors.append(f"{field} drifted: missing={missing}, extra={extra}")

    ancestry = spec.get("ancestry_rules")
    if not isinstance(ancestry, dict):
        errors.append("ancestry_rules must be object")
    else:
        if ancestry.get("provenance_edges_form_dag") is not True:
            errors.append("provenance ancestry must remain a DAG")
        if ancestry.get("semantic_or_lifecycle_edges_do_not_implicitly_enter_provenance_dag") is not True:
            errors.append("semantic/lifecycle edges must remain outside provenance DAG by default")
        if ancestry.get("unknown_root_state") != "ANCESTRY_UNKNOWN":
            errors.append("unknown ancestry state drifted")
        if ancestry.get("unknown_ancestry_does_not_imply_independence") is not True:
            errors.append("unknown ancestry must not imply independence")

    invalid = set(spec.get("invalid_states", []))
    missing = REQUIRED_INVALID_STATES - invalid
    if missing:
        errors.append(f"invalid ancestry states missing: {sorted(missing)}")

    privacy = spec.get("privacy_rules")
    if not isinstance(privacy, dict):
        errors.append("privacy_rules must be object")
    else:
        if privacy.get("provenance_without_payload_transfer_allowed") is not True:
            errors.append("privacy-preserving provenance must be allowed")
        if privacy.get("privacy_projection_must_retain_lineage") is not True:
            errors.append("privacy projection must retain lineage")
        if privacy.get("digest_match_does_not_grant_publication_authority") is not True:
            errors.append("digest match must not grant publication authority")

    try:
        fixture = _load(root / FIXTURE_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{FIXTURE_PATH} invalid JSON: {exc}")
        fixture = {}

    if fixture.get("schema_version") != "GOD_BRAIN_PROVENANCE_ANCESTRY_HOSTILE_CASES_V0_1":
        errors.append("fixture schema_version drifted")
    if fixture.get("status") != "RESEARCH_FIXTURES":
        errors.append("fixtures must remain research-only")

    cases = fixture.get("cases")
    if not isinstance(cases, list):
        errors.append("fixture cases must be list")
        cases = []

    expected_ids = [f"GB-PA-{i:03d}" for i in range(1, 25)]
    actual_ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if actual_ids != expected_ids:
        errors.append("fixture IDs must be contiguous GB-PA-001..024")

    valid_states = set(EXPECTED_INDEPENDENCE_STATES) | {"INVALID"}
    for case in cases:
        if not isinstance(case, dict):
            errors.append("fixture case must be object")
            continue
        if case.get("independence_state") not in valid_states:
            errors.append(f"{case.get('id')} invalid independence_state")
        for field in ("title", "setup", "expected", "reason"):
            if not isinstance(case.get(field), str) or not case.get(field):
                errors.append(f"{case.get('id')} missing {field}")

    by_id = {case.get("id"): case for case in cases if isinstance(case, dict)}
    pinned = {
        "GB-PA-001": ("SHARED_ROOT_ANCESTRY", "ONE_SOURCE_LINEAGE"),
        "GB-PA-005": ("COMMON_GENERATION_CHANNEL", "NOT_INDEPENDENT_BY_AGENT_COUNT"),
        "GB-PA-006": ("ANCESTRY_UNKNOWN", "DO_NOT_GRANT_FULL_INDEPENDENCE"),
        "GB-PA-007": ("INDEPENDENT_WITHIN_DECLARED_SCOPE", "INDEPENDENCE_MAY_BE_CLAIMED_WITH_SCOPE"),
        "GB-PA-010": ("INVALID", "FRESH_REVIEW_REQUIRED"),
        "GB-PA-016": ("INVALID", "REJECT"),
        "GB-PA-023": ("NOT_APPLICABLE", "VALID_PRIVACY_PRESERVING_PROVENANCE"),
        "GB-PA-024": ("INVALID", "FRESH_READ_REQUIRED"),
    }
    for case_id, (state, expected) in pinned.items():
        case = by_id.get(case_id, {})
        if case.get("independence_state") != state or case.get("expected") != expected:
            errors.append(f"{case_id} expectation drifted")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "SOURCE_COUNT != INDEPENDENT_CORROBORATION",
        "SAME_ROOT_DESCENDANTS != INDEPENDENT_EVIDENCE",
        "TEMPORAL_ORDER != CAUSAL_DERIVATION",
        "SEMANTIC_SIMILARITY != PROVENANCE_EQUIVALENCE",
        "PRIVACY_PROJECTION != RAW_SOURCE",
        "DISTINCT_INSTANCE != INDEPENDENT_EVIDENCE",
        "REVIEW_OF_PARENT_HEAD != REVIEW_OF_CHILD_HEAD",
        "PROVENANCE_POINTER != PAYLOAD_TRANSFER",
        "PROVENANCE_DAG != ALL_RELATIONS_GRAPH",
        "COMPLETE_LINEAGE_CAPTURE != INDEPENDENCE_PROOF_WHEN_HIDDEN_ANCESTRY_EXISTS",
    ):
        if marker not in doc:
            errors.append(f"{DOC_PATH} missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_provenance_ancestry(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain provenance ancestry contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
