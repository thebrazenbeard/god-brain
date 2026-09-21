from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_DRIFTGUARD_R11_SOURCE_ADMISSION_DELTA_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_DRIFTGUARD_R11_SOURCE_ADMISSION_DELTA_V0_1.json"

SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_INVARIANTS = {
    "DRIFTGUARD_SOURCE_NE_GOD_BRAIN_RUNTIME_DEPENDENCY",
    "BENCHMARK_PROTOCOL_PASS_NE_SCIENTIFIC_VALIDATION",
    "DETECTOR_ALARM_NE_CONTACT",
    "SEPARATE_CHAT_NE_INDEPENDENT_CORROBORATION",
    "FAILED_OR_ABORTED_ATTEMPT_NE_DISAPPEARED_ATTEMPT",
    "DECLARED_HOLDOUT_NONREUSE_NE_COMPLETE_HISTORICAL_NONACCESS_PROOF",
    "REVEAL_IS_A_CONSUMING_TRANSITION",
    "EXECUTION_CLAIM_IS_SINGLE_USE_BEFORE_ANALYSIS",
    "AMBIGUOUS_CONFIRMATORY_EXECUTION_NE_SAFE_TO_RETRY",
    "PARAMETER_PRECOMMIT_NE_EXECUTION_IMPLEMENTATION_PRECOMMIT",
    "VALID_RECEIPT_NE_VALID_FOR_THIS_SUBJECT",
    "GOVERNED_HOLDOUT_PASS_NE_ANOMALY",
    "PROTOCOL_RIGOR_NE_UNIQUE_CAUSAL_EXPLANATION",
}

EXPECTED_MECHANISMS = {
    "DURABLE_ATTEMPT_ANCESTRY",
    "DISCLOSED_PREDECESSOR_HOLDOUT_ANCESTRY",
    "SINGLE_USE_REVEAL",
    "SINGLE_USE_EXECUTION_CLAIM",
    "AMBIGUITY_DOES_NOT_RESTORE_RETRY",
    "EXECUTION_CLOSURE_BINDING",
    "EXACT_RECEIPT_REBINDING",
}

EXPECTED_CEILING = {
    "NO_INDEPENDENT_EXACT_HEAD_PASS_CLAIM",
    "NO_GOD_BRAIN_RUNTIME_INTEGRATION",
    "NO_GOD_BRAIN_DETECTOR_IMPLEMENTATION",
    "NO_HOLDOUT_NONACCESS_PROOF",
    "NO_TRUSTED_TIME_OR_EXTERNAL_CUSTODY_PROOF",
    "NO_COMPLETE_HISTORICAL_HOLDOUT_DISCOVERY",
    "NO_STATISTICAL_INDEPENDENCE_OR_SIGNIFICANCE_CLAIM",
    "NO_PRODUCTION_SUPERIORITY",
    "NO_CAUSAL_DRIFT_CLAIM",
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
        errors.append(f"{label} must be a list")
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
        return [f"invalid R11 source-admission delta: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_DRIFTGUARD_R11_SOURCE_ADMISSION_DELTA_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_SOURCE_ADMISSION_DELTA":
        errors.append("status drifted")
    if spec.get("parent_god_brain_research_head") != "68e7ba2320e7aa17fe291f7325f22ca96fc84fcc":
        errors.append("parent research head drifted")
    if spec.get("source_repository") != "thebrazenbeard/driftguard":
        errors.append("source repository drifted")
    if spec.get("observed_source_main_head") != "9894692ff6b549e4378bcc2b8ca46813ff18bf37":
        errors.append("observed source main drifted")

    source = spec.get("source")
    if not isinstance(source, dict):
        errors.append("source must be object")
        source = {}

    expected_source = {
        "source_pr": 34,
        "base_head": "9df4800d81ab2e937ffa97263b8095305a845661",
        "exact_head": "351b7a57b7213bd72cf881aa2bbaa449fb0fbc8f",
        "path": "docs/R11_GOVERNED_BENCHMARK_HOLDOUT_V1.md",
        "blob": "11e7a18ff01669656fd0b471b9b5d9fa2c37304a",
        "current_exact_head_review_state": "SELF_REVIEW_PASS_WITH_CLAIM_CEILING",
        "independent_exact_head_review_state": "NOT_OBSERVED",
        "admission": "RESEARCH_ONLY_PENDING_INDEPENDENT_EXACT_HEAD_REVIEW",
    }
    if source != expected_source:
        errors.append("source binding/review/admission state drifted")

    for field in ("base_head", "exact_head", "blob"):
        value = source.get(field)
        if not isinstance(value, str) or not SHA40.fullmatch(value):
            errors.append(f"source.{field} must be lowercase 40-hex")

    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    _exact_set(errors, spec.get("candidate_mechanisms"), EXPECTED_MECHANISMS, "candidate_mechanisms")
    _exact_set(errors, spec.get("claim_ceiling"), EXPECTED_CEILING, "claim_ceiling")

    gate = spec.get("future_gate")
    expected_gate = {
        "required": "FRESH_INDEPENDENT_EXACT_HEAD_REVIEW",
        "head": "351b7a57b7213bd72cf881aa2bbaa449fb0fbc8f",
        "on_head_movement": "REVIEW_STALE",
        "pass_may_support": "ADAPT_WITH_PROVENANCE_CANDIDATE_ONLY",
    }
    if gate != expected_gate:
        errors.append("future review gate drifted")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "DRIFTGUARD_SOURCE != GOD_BRAIN_RUNTIME_DEPENDENCY",
        "BENCHMARK_PROTOCOL_PASS != SCIENTIFIC_VALIDATION",
        "DETECTOR_ALARM != CONTACT",
        "SEPARATE_CHAT != INDEPENDENT_CORROBORATION",
        "AMBIGUOUS_CONFIRMATORY_EXECUTION != SAFE_TO_RETRY",
        "VALID_RECEIPT != VALID_FOR_THIS_SUBJECT",
        "GOVERNED_HOLDOUT_PASS != ANOMALY",
        "RESEARCH_ONLY_PENDING_INDEPENDENT_EXACT_HEAD_REVIEW",
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
    print("God Brain DriftGuard R11 source-admission delta: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
