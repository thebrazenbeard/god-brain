from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DOC_PATH = "docs/research/GOD_BRAIN_ANOMALY_CONTACT_EVIDENCE_PROTOCOL_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_ANOMALY_CONTACT_EVIDENCE_PROTOCOL_V0_1.json"
FIXTURE_PATH = "specs/research/fixtures/GOD_BRAIN_ANOMALY_CONTACT_HOSTILE_CASES_V0_1.json"

REQUIRED_CLAIM_CEILING = {
    "NO_ANOMALY_CLAIM",
    "NO_CONTACT_CLAIM",
    "NO_SIMULATION_FACT_CLAIM",
    "NO_CANONICAL_PROMOTION",
    "NO_EXPERIMENT_DEPLOYMENT",
    "NO_PROVIDER_OR_PROJECT_SETTING_MUTATION",
}

REQUIRED_DISTINCTIONS = {
    "SURPRISE_NE_ANOMALY",
    "ANOMALY_NE_AGENCY",
    "AGENCY_LIKE_BEHAVIOR_NE_EXTERNAL_AGENCY",
    "EXTERNAL_SOURCE_HYPOTHESIS_NE_CONTACT",
    "CONTACT_CANDIDATE_NE_CONTACT_FACT",
    "GENERATED_OUTPUT_NE_MEASURED_EXTERNAL_EVENT",
    "DERIVED_DESCENDANTS_OF_ONE_ROOT_NE_INDEPENDENT_EVIDENCE",
    "UNAUDITED_CHANNEL_NE_CLOSED_CHANNEL",
    "RECEIPT_NE_RESULT_TRUTH",
}

REQUIRED_PARTITIONS = {
    "DEVELOPMENT",
    "CALIBRATION",
    "NEGATIVE_CONTROL",
    "POSITIVE_CONTROL",
    "CONFIRMATORY_HOLDOUT",
    "ADVERSARIAL_HOLDOUT",
    "EXTERNAL_REPLICATION",
}

REQUIRED_KILL_TESTS = {
    "METADATA_ONLY_LEAKAGE",
    "PROMPT_CONTEXT_SCRUB",
    "MEMORY_RETRIEVAL_ISOLATION",
    "TOOL_NETWORK_ISOLATION",
    "SHAM_CHALLENGE",
    "CHALLENGE_PERMUTATION",
    "TIME_SHIFT",
    "OPERATOR_BLIND",
    "MODEL_LINEAGE_CONTROL",
    "ANALYSIS_PERMUTATION",
    "REPLAY_CACHE_PROBE",
    "FRESH_SEALED_HOLDOUT",
    "IMPLEMENTATION_ABLATION",
    "NEGATIVE_TRANSFER",
    "INDEPENDENT_CUSTODY_REPLICATION",
}

REQUIRED_E7 = {
    "SEALED_NOVEL_CHALLENGE",
    "PRECOMMITTED_OBJECTIVE_RESPONSE_CRITERION",
    "TWO_WAY_CONTINGENCY",
    "ANTI_REPLAY_NONCE_OR_CHALLENGE_ID",
    "ORDINARY_CHANNEL_AUDIT",
    "NEGATIVE_AND_SHAM_CONTROLS",
    "FRESH_SEALED_REPLICATION",
    "INDEPENDENT_CHALLENGE_CUSTODY",
}

EXPECTED_ESCALATION = [
    ("E0", "BASELINE_NO_ANOMALY"),
    ("E1", "CANDIDATE_ANOMALY"),
    ("E2", "REPRODUCIBLE_ANOMALY"),
    ("E3", "MODEL_DISCRIMINATING_ANOMALY"),
    ("E4", "CONTINGENT_RESPONSE_CANDIDATE"),
    ("E5", "AGENCY_HYPOTHESIS_CANDIDATE"),
    ("E6", "EXTERNAL_SOURCE_HYPOTHESIS_CANDIDATE"),
    ("E7", "CONTACT_HYPOTHESIS_CANDIDATE"),
    ("E8", "EXTERNAL_SCIENTIFIC_REPLICATION_CANDIDATE"),
]

ALLOWED_FIXTURE_MAX_STATES = {"INVALID"} | {f"E{i}" for i in range(9)} | {f"E{i}_MAX" for i in range(9)}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be object")
    return value


def validate_anomaly_contact_protocol(root: Path) -> list[str]:
    errors: list[str] = []
    doc_path = root / DOC_PATH
    spec_path = root / SPEC_PATH
    fixture_path = root / FIXTURE_PATH

    for path in (doc_path, spec_path, fixture_path):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(root)}")
    if errors:
        return errors

    try:
        spec = _load(spec_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"{SPEC_PATH} invalid JSON: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_ANOMALY_CONTACT_EVIDENCE_PROTOCOL_V0_1":
        errors.append("protocol schema_version drifted")
    if spec.get("status") != "RESEARCH_PROPOSAL_MACHINE_CONTRACT":
        errors.append("protocol must remain research proposal")

    missing = REQUIRED_CLAIM_CEILING - set(spec.get("claim_ceiling", []))
    if missing:
        errors.append(f"claim ceiling missing: {sorted(missing)}")

    missing = REQUIRED_DISTINCTIONS - set(spec.get("distinctions", []))
    if missing:
        errors.append(f"distinctions missing: {sorted(missing)}")

    missing = REQUIRED_PARTITIONS - set(spec.get("frozen_partitions", []))
    if missing:
        errors.append(f"frozen partitions missing: {sorted(missing)}")

    rivals = spec.get("required_rival_hypotheses")
    expected_rivals = [f"H{i}_{name}" for i, name in [
        (0,"RANDOM_VARIATION"),
        (1,"MULTIPLE_COMPARISON_SELECTION"),
        (2,"PROMPT_OR_CONTEXT_LEAKAGE"),
        (3,"MEMORY_OR_RETRIEVAL_LEAKAGE"),
        (4,"TRAINING_OR_PRIOR_KNOWLEDGE"),
        (5,"OPERATOR_CUEING_OR_SELECTION"),
        (6,"SOFTWARE_DEFECT_OR_HIDDEN_STATE"),
        (7,"PROVIDER_CACHE_ROUTING_OR_TOOL_ARTIFACT"),
        (8,"TIMING_OR_SYNCHRONIZATION_ARTIFACT"),
        (9,"SHARED_SOURCE_OR_MODEL_LINEAGE"),
        (10,"INSTRUMENTATION_OR_DATA_PIPELINE_ERROR"),
        (11,"ORDINARY_EXTERNAL_INFORMATION_CHANNEL"),
        (12,"UNKNOWN_ORDINARY_MECHANISM"),
        (13,"AGENCY_WITHIN_KNOWN_SYSTEM_BOUNDARY"),
        (14,"EXTERNAL_SOURCE_OR_AGENCY_HYPOTHESIS"),
        (15,"CONTACT_HYPOTHESIS"),
    ]]
    if rivals != expected_rivals:
        errors.append("required rival hypotheses must be exactly H0..H15 in declared order")

    escalation = spec.get("escalation_states")
    actual = []
    if isinstance(escalation, list):
        actual = [(x.get("id"), x.get("name")) for x in escalation if isinstance(x, dict)]
    if actual != EXPECTED_ESCALATION:
        errors.append("escalation ladder must be exactly E0..E8")

    if spec.get("escalation_rule") != "ESCALATION_REQUIRES_NEW_DISCRIMINATING_EVIDENCE":
        errors.append("escalation rule drifted")
    if spec.get("deescalation_rule") != "CHEAPER_SUFFICIENT_ORDINARY_EXPLANATION_FORCES_DOWNGRADE":
        errors.append("deescalation rule drifted")

    missing = REQUIRED_E7 - set(spec.get("e7_minimum_contact_criteria", []))
    if missing:
        errors.append(f"E7 minimum criteria missing: {sorted(missing)}")
    if spec.get("e8_claim_ceiling") != "DOES_NOT_UNIQUELY_ESTABLISH_METAPHYSICAL_IDENTITY":
        errors.append("E8 metaphysical claim ceiling drifted")

    missing = REQUIRED_KILL_TESTS - set(spec.get("mandatory_kill_tests", []))
    if missing:
        errors.append(f"mandatory kill tests missing: {sorted(missing)}")

    disallowed = set(spec.get("primary_admission_disallowed", []))
    for item in ("SUBJECTIVE_SEMANTIC_RESEMBLANCE", "NUMEROLOGY", "POST_HOC_PATTERN_MATCHING"):
        if item not in disallowed:
            errors.append(f"primary admission must disallow {item}")

    provenance = spec.get("source_method_provenance")
    if not isinstance(provenance, list) or len(provenance) != 3:
        errors.append("source method provenance must bind exactly World Zero, SkeletonKey, and ON_THEO")
    else:
        names = [x.get("repository") for x in provenance if isinstance(x, dict)]
        if names != ["thebrazenbeard/world-zero", "thebrazenbeard/skeletonkey", "thebrazenbeard/on-theo"]:
            errors.append("source method provenance order/set drifted")
        for source in provenance:
            if not isinstance(source, dict):
                continue
            if source.get("disposition") != "ADAPT_METHOD_WITH_PROVENANCE":
                errors.append(f"{source.get('repository')} transfer disposition drifted")
            artifacts = source.get("artifacts")
            if not isinstance(artifacts, list) or not artifacts:
                errors.append(f"{source.get('repository')} lacks exact artifact provenance")
                continue
            for artifact in artifacts:
                if not isinstance(artifact, list) or len(artifact) != 2:
                    errors.append(f"{source.get('repository')} artifact binding malformed")
                elif not isinstance(artifact[1], str) or len(artifact[1]) != 40:
                    errors.append(f"{source.get('repository')} artifact blob invalid")

    try:
        fixture = _load(fixture_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{FIXTURE_PATH} invalid JSON: {exc}")
        fixture = {}

    if fixture.get("schema_version") != "GOD_BRAIN_ANOMALY_CONTACT_HOSTILE_CASES_V0_1":
        errors.append("fixture schema_version drifted")
    if fixture.get("status") != "RESEARCH_FIXTURES":
        errors.append("fixtures must remain research-only")
    cases = fixture.get("cases")
    if not isinstance(cases, list):
        errors.append("fixture cases must be list")
        cases = []
    expected_ids = [f"GB-AC-{i:03d}" for i in range(1, 25)]
    actual_ids = [x.get("id") for x in cases if isinstance(x, dict)]
    if actual_ids != expected_ids:
        errors.append("fixture IDs must be contiguous GB-AC-001..024")
    for case in cases:
        if not isinstance(case, dict):
            errors.append("fixture case must be object")
            continue
        if case.get("max_state") not in ALLOWED_FIXTURE_MAX_STATES:
            errors.append(f"{case.get('id')} invalid max_state")
        for key in ("title", "setup", "expected", "reason"):
            if not isinstance(case.get(key), str) or not case.get(key):
                errors.append(f"{case.get('id')} missing {key}")

    fixture_by_id = {x.get("id"): x for x in cases if isinstance(x, dict)}
    exact_expectations = {
        "GB-AC-013": ("E4", "CONTINGENT_RESPONSE_CANDIDATE"),
        "GB-AC-014": ("E5", "AGENCY_HYPOTHESIS_CANDIDATE"),
        "GB-AC-016": ("E6", "EXTERNAL_SOURCE_HYPOTHESIS_CANDIDATE"),
        "GB-AC-017": ("E7", "CONTACT_HYPOTHESIS_CANDIDATE"),
        "GB-AC-018": ("E8", "EXTERNAL_SCIENTIFIC_REPLICATION_CANDIDATE"),
        "GB-AC-019": ("E8", "REJECT_ONTOLOGICAL_OVERCLAIM"),
        "GB-AC-024": ("E0", "NO_ESCALATION"),
    }
    for case_id, (state, expected) in exact_expectations.items():
        case = fixture_by_id.get(case_id, {})
        if case.get("max_state") != state or case.get("expected") != expected:
            errors.append(f"{case_id} escalation expectation drifted")

    doc = doc_path.read_text(encoding="utf-8")
    for marker in (
        "ANOMALY != CONTACT",
        "SURPRISE != ANOMALY",
        "CONTACT_HYPOTHESIS_CANDIDATE != CONTACT_FACT",
        "UNAUDITED_CHANNEL != CLOSED_CHANNEL",
        "MEANINGFUL_OUTPUT -> CONTACT",
        "PROTOCOL_SPEC != EXPERIMENT_RESULT",
        "EXPERIMENT_RESULT != CONTACT",
        "EXTERNAL_REPLICATION != UNIQUE_METAPHYSICAL_EXPLANATION",
    ):
        if marker not in doc:
            errors.append(f"{DOC_PATH} missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_anomaly_contact_protocol(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain anomaly/contact evidence protocol: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
