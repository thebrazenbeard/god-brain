from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_DRIFTGUARD_SOURCE_ADMISSION_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_DRIFTGUARD_SOURCE_ADMISSION_V0_1.json"

SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_INVARIANTS = {
    "SOURCE_PRESENCE_NE_ARCHITECTURAL_ADMISSION",
    "ADAPT_WITH_PROVENANCE_NE_RUNTIME_COUPLING",
    "REVIEWED_SOURCE_MECHANISM_NE_GOD_BRAIN_CANON",
    "DRIFTGUARD_BEHAVIORAL_DRIFT_NE_GOD_BRAIN_ONTOLOGICAL_ANOMALY",
    "DETECTOR_ALARM_NE_CONTACT",
    "EFFECT_VERIFICATION_NE_CAUSAL_EXPLANATION",
    "SAME_HOLDOUT_COMPARISON_NE_PRODUCTION_SELECTION_AUTHORITY",
    "INDIVIDUALLY_VALID_READS_NE_ATOMIC_CURRENTNESS_DECISION",
    "DURABLE_EFFECT_FENCE_NE_PROTECTED_EFFECT_AUTHORITY",
    "DISPATCH_UNCERTAIN_NE_EFFECT_OCCURRED",
    "GENERIC_RECEIPT_NE_PROVIDER_TRUTH",
    "VERIFIED_PROVIDER_EFFECT_NE_BEHAVIORAL_RECOVERY",
}

EXPECTED_SOURCES = {
    "DRIFTGUARD_R10_DETECTOR_COMPARISON": {
        "source_pr": 30,
        "exact_head": "a5328ff50c10fc2fab846fccbe8317bf9508d505",
        "path": "docs/R10_DETECTOR_COMPARISON_V1.md",
        "blob": "a18715d88e31102ab0a0e8d3f4625c19c31b1f39",
        "review_disposition": "PASS_WITH_CLAIM_CEILING",
        "workflow_run": 35546027652,
        "admission": "ADAPT_WITH_PROVENANCE",
        "mechanism_field": "admitted_mechanisms",
        "mechanisms": {
            "FROZEN_CANDIDATE_PER_ALGORITHM",
            "SHARED_METRIC_SEMANTICS",
            "INCUMBENT_PARITY_ORACLE",
            "OVERLAP_AWARE_ERROR_ACCOUNTING",
            "NO_SAME_HOLDOUT_PROMOTION",
            "DESCRIPTIVE_PARETO_WITHOUT_PROMOTION",
            "PARAMETER_PROVENANCE_WITH_EXPLICIT_LIMITS",
        },
    },
    "DRIFTGUARD_PR28_CURRENTNESS_RACE": {
        "source_pr": 28,
        "exact_head": "5b0baea9538de1a254c731e2b1770c0b58677724",
        "review_disposition": "CHANGES_REQUIRED",
        "admission": "HISTORICAL_ONLY",
        "mechanism_field": "admitted_mechanisms",
        "mechanisms": {"NONATOMIC_COMPOSITE_CURRENTNESS_IS_BLOCKER_EVIDENCE"},
    },
    "DRIFTGUARD_PR31_ATOMIC_CURRENTNESS": {
        "source_pr": 31,
        "exact_head": "9df4800d81ab2e937ffa97263b8095305a845661",
        "path": "docs/EXTERNAL_BOUNDARY_V1.md",
        "blob": "c2933806a44da5f0327d11d898197a894ae963d2",
        "review_disposition": "NO_EXACT_HEAD_REVIEW_OBSERVED",
        "admission": "RESEARCH_ONLY_PENDING_EXACT_HEAD_REVIEW",
        "mechanism_field": "candidate_mechanisms",
        "mechanisms": {
            "SINGLE_TRANSACTION_CURRENTNESS_SNAPSHOT",
            "FACTORY_GATED_CURRENTNESS_READBACK",
        },
    },
    "DRIFTGUARD_PR32_EFFECT_AUTHORIZATION_CAS_DESIGN": {
        "source_pr": 32,
        "exact_head": "549456473cdef342c50641e3495c2ad66102872f",
        "path": "docs/EFFECT_AUTHORIZATION_CAS_V1.md",
        "blob": "205a5af5ef9f24dbfbb201b21d7be44c5456e3d4",
        "review_disposition": "NO_EXACT_HEAD_REVIEW_OBSERVED",
        "admission": "RESEARCH_ONLY_DESIGN",
        "mechanism_field": "candidate_mechanisms",
        "mechanisms": {
            "DURABLE_SINGLE_USE_EFFECT_RESERVATION",
            "LOCAL_INVALIDATION_FENCE",
            "DISPATCH_UNCERTAIN_BEFORE_NETWORK_IO",
            "PROVIDER_RECONCILIATION_BEFORE_RETRY",
            "EXACT_FINALIZATION_CAS",
        },
    },
}

EXPECTED_DETECTOR_RULES = {
    "DEFINE_EVIDENCE_SUBJECT_BEFORE_DETECTOR",
    "ONE_FROZEN_CANDIDATE_PER_ALGORITHM_ON_CONFIRMATORY_HOLDOUT",
    "SEPARATE_DESIGN_CALIBRATION_CONFIRMATORY",
    "PRESERVE_PROVENANCE_AND_SHARED_ROOT_ACCOUNTING",
    "ONE_EXACT_METRIC_CONTRACT_ACROSS_CANDIDATES",
    "REPORT_OVERLAP_AWARE_ERRORS",
    "NO_SELECTION_FROM_SAME_HOLDOUT_USED_FOR_COMPARISON",
    "NEW_UNTOUCHED_SELECTION_OR_QUALIFICATION_SUBJECT_REQUIRED",
    "DETECTOR_QUALIFICATION_BELOW_EXTERNAL_SCIENTIFIC_VALIDATION",
}

EXPECTED_EFFECT_RULES = {
    "EXACT_CURRENTNESS_READMISSION",
    "LOCAL_DURABLE_RESERVATION_AND_FENCE",
    "PERSIST_UNCERTAINTY_BEFORE_EXTERNAL_IO",
    "PROVIDER_SPECIFIC_IDEMPOTENCY_AND_READBACK",
    "RECONCILE_BEFORE_RETRY",
    "EXACT_FINALIZATION_CAS",
    "EFFECT_VERIFICATION_SEPARATE_FROM_CAUSAL_INTERPRETATION",
}

EXPECTED_CLAIM_CEILING = {
    "NO_GOD_BRAIN_RUNTIME_INTEGRATION",
    "NO_GOD_BRAIN_DETECTOR_IMPLEMENTATION",
    "NO_GOD_BRAIN_PROVIDER_EFFECT_PATH",
    "NO_SIMULATION_EVIDENCE_CLAIM",
    "NO_EXTERNAL_CONTACT_CLAIM",
    "NO_CAUSAL_ATTRIBUTION",
    "NO_PRODUCTION_READINESS",
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


def validate_driftguard_source_admission(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (DOC_PATH, SPEC_PATH):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        spec = _load(root / SPEC_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid source-admission spec: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_DRIFTGUARD_SOURCE_ADMISSION_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_SOURCE_ADMISSION_ASSESSMENT":
        errors.append("status must remain research source admission assessment")
    if spec.get("god_brain_base_head") != "c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5":
        errors.append("God Brain base head binding drifted")
    if spec.get("source_repository") != "thebrazenbeard/driftguard":
        errors.append("source repository drifted")
    if spec.get("observed_source_main_head") != "9894692ff6b549e4378bcc2b8ca46813ff18bf37":
        errors.append("observed DriftGuard main head binding drifted")

    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    _exact_set(
        errors,
        spec.get("god_brain_future_detector_rules"),
        EXPECTED_DETECTOR_RULES,
        "future detector rules",
    )
    _exact_set(
        errors,
        spec.get("god_brain_future_effect_rules"),
        EXPECTED_EFFECT_RULES,
        "future effect rules",
    )
    _exact_set(errors, spec.get("claim_ceiling"), EXPECTED_CLAIM_CEILING, "claim ceiling")

    sources = spec.get("sources")
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []
    ids = [item.get("id") for item in sources if isinstance(item, dict)]
    if ids != list(EXPECTED_SOURCES):
        errors.append("source order/identity drifted")

    for item in sources:
        if not isinstance(item, dict):
            errors.append("source entry must be object")
            continue
        source_id = item.get("id")
        expected = EXPECTED_SOURCES.get(source_id)
        if expected is None:
            errors.append(f"unknown source id: {source_id!r}")
            continue

        for field in ("source_pr", "exact_head", "review_disposition", "admission"):
            if item.get(field) != expected[field]:
                errors.append(f"{source_id}.{field} drifted")

        head = item.get("exact_head")
        if not isinstance(head, str) or not SHA40.fullmatch(head):
            errors.append(f"{source_id}.exact_head must be lowercase 40-hex")

        for optional in ("path", "blob", "workflow_run"):
            if optional in expected and item.get(optional) != expected[optional]:
                errors.append(f"{source_id}.{optional} drifted")

        blob = item.get("blob")
        if blob is not None and (not isinstance(blob, str) or not SHA40.fullmatch(blob)):
            errors.append(f"{source_id}.blob must be lowercase 40-hex")

        mechanism_field = expected["mechanism_field"]
        _exact_set(
            errors,
            item.get(mechanism_field),
            expected["mechanisms"],
            f"{source_id}.{mechanism_field}",
        )

        allowed_fields = {
            "id",
            "source_pr",
            "exact_head",
            "review_disposition",
            "admission",
            mechanism_field,
        }
        if "path" in expected:
            allowed_fields.add("path")
        if "blob" in expected:
            allowed_fields.add("blob")
        if "workflow_run" in expected:
            allowed_fields.add("workflow_run")
        if set(item) != allowed_fields:
            errors.append(f"{source_id} fields must be exact")

    by_id = {item.get("id"): item for item in sources if isinstance(item, dict)}
    if by_id.get("DRIFTGUARD_PR31_ATOMIC_CURRENTNESS", {}).get("admission") != "RESEARCH_ONLY_PENDING_EXACT_HEAD_REVIEW":
        errors.append("PR31 must remain pending exact-head review")
    if by_id.get("DRIFTGUARD_PR32_EFFECT_AUTHORIZATION_CAS_DESIGN", {}).get("admission") != "RESEARCH_ONLY_DESIGN":
        errors.append("PR32 must remain design-only")
    if by_id.get("DRIFTGUARD_PR28_CURRENTNESS_RACE", {}).get("review_disposition") != "CHANGES_REQUIRED":
        errors.append("PR28 blocker evidence cannot be promoted to pass")
    if by_id.get("DRIFTGUARD_R10_DETECTOR_COMPARISON", {}).get("admission") != "ADAPT_WITH_PROVENANCE":
        errors.append("R10 source disposition drifted")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "SOURCE_PRESENCE != ARCHITECTURAL_ADMISSION",
        "ADAPT_WITH_PROVENANCE != RUNTIME_COUPLING",
        "DRIFTGUARD_BEHAVIORAL_DRIFT != GOD_BRAIN_ONTOLOGICAL_ANOMALY",
        "DETECTOR_ALARM != CONTACT",
        "SAME_HOLDOUT_COMPARISON != PRODUCTION_SELECTION_AUTHORITY",
        "DURABLE_EFFECT_FENCE != PROTECTED_EFFECT_AUTHORITY",
        "GENERIC_RECEIPT != PROVIDER_TRUTH",
    ):
        if marker not in doc:
            errors.append(f"research doc missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_driftguard_source_admission(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain DriftGuard source admission: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
