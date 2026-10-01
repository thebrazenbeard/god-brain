from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_INTAKE_AND_EVIDENCE_ADMISSION_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_INTAKE_AND_EVIDENCE_ADMISSION_V0_1.json"
FIXTURE_PATH = "specs/research/fixtures/GOD_BRAIN_INTAKE_EVIDENCE_HOSTILE_CASES_V0_1.json"

SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_INVARIANTS = {
    "ACQUIRED_NE_TRUSTED",
    "RAW_NE_NORMALIZED",
    "NORMALIZED_NE_INTERPRETED",
    "INTERPRETED_NE_VERIFIED",
    "RETRIEVED_NE_ADMITTED",
    "STORED_NE_CURRENT",
    "CURRENT_NE_TRUE",
    "SOURCE_LABEL_NE_SEMANTIC_IDENTITY",
    "SEMANTIC_SIMILARITY_NE_SAME_PROVENANCE",
    "MULTIPLE_DERIVATIVES_NE_INDEPENDENT_EVIDENCE",
    "USER_STATED_NE_INDEPENDENTLY_VERIFIED",
    "TOOL_OUTPUT_NE_AUTHORITY",
    "INGESTION_NE_MEMORY_ADMISSION",
    "MEMORY_ADMISSION_NE_CURRENTNESS_PROMOTION",
    "CURRENTNESS_PROMOTION_NE_ACTION_AUTHORITY",
}

EXPECTED_PIPELINE = [
    "ACQUIRE_RAW",
    "VERIFY_RAW_IDENTITY",
    "OPTIONAL_NORMALIZE",
    "BUILD_INTERPRETATION_CANDIDATES",
    "CLASSIFY_PROVENANCE_AND_INDEPENDENCE",
    "APPLY_PRIVACY_AND_SCOPE",
    "ADMIT_OR_QUARANTINE_EVIDENCE",
    "HAND_OFF_TO_CURRENTNESS_RESOLUTION",
]

EXPECTED_RULES = {
    "MUTABLE_SOURCE_REQUIRES_EXACT_REVISION_OR_LIMITED_CLAIM_CEILING",
    "RAW_BYTES_OR_PROVIDER_VERIFIABLE_OBJECT_IDENTITY_REQUIRED_FOR_EXACT_ARTIFACT_CLAIM",
    "NORMALIZATION_MUST_BIND_PARENT_AND_TRANSFORMATION",
    "INTERPRETATION_MUST_BIND_SOURCE_CONTEXT_AND_PROVENANCE",
    "PRIVATE_SCOPE_MUST_NOT_BROADEN_DURING_ADMISSION",
    "SHARED_ANCESTRY_MUST_SHARE_INDEPENDENCE_FAMILY",
    "CONFLICTING_UNSUPERSEDED_EVIDENCE_MUST_NOT_AUTO_RESOLVE_BY_RECENCY",
    "MODEL_OR_TOOL_OUTPUT_MUST_NOT_SELF_PROMOTE_TO_VERIFIED_FACT",
    "ADMISSION_MUST_NOT_GRANT_EFFECT_AUTHORITY",
    "CURRENTNESS_IS_DOWNSTREAM_OF_EVIDENCE_ADMISSION",
}

EXPECTED_CEILING = {
    "NO_RUNTIME_IMPLEMENTATION",
    "NO_MEMORY_MIGRATION",
    "NO_PROVIDER_COUPLING",
    "NO_PRIVATE_PAYLOAD_TRANSFER",
    "NO_CURRENTNESS_PROMOTION",
    "NO_EFFECT_AUTHORITY",
    "NO_SCIENTIFIC_VALIDATION",
    "NO_SIMULATION_EVIDENCE_CLAIM",
    "NO_EXTERNAL_CONTACT_CLAIM",
}

EXPECTED_DONORS = {
    "thebrazenbeard/ingest": "27764c9fb97c84d178a3f66e0da2d669df645ed6",
    "thebrazenbeard/semiotics": "37117a2097f7f2aa35968fc9db24eacf7240826e",
    "thebrazenbeard/semanticatlas": "895677a64af5d29b580306ca52ecc0e0607a9ccc",
    "thebrazenbeard/god-brain": "495c2b42932153cba0926744d04a69bc34557f81",
}

EXPECTED_OBJECTS = {
    "AcquisitionRecord",
    "NormalizationRecord",
    "InterpretationCandidate",
    "EvidenceAdmissionDecision",
}

EXPECTED_CASES = {f"IE-{i:02d}" for i in range(1, 13)}

def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be object")
    return value

def _exact_unique(errors: list[str], value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return
    if len(value) != len(set(value)):
        errors.append(f"{label} must not contain duplicates")
    if set(value) != expected:
        errors.append(f"{label} must be exact closed set")

def validate_intake_evidence_admission(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (DOC_PATH, SPEC_PATH, FIXTURE_PATH):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        spec = _load(root / SPEC_PATH)
        fixtures = _load(root / FIXTURE_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid intake/evidence contract: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_INTAKE_AND_EVIDENCE_ADMISSION_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_SPECIFICATION_NO_RUNTIME":
        errors.append("status must remain research specification / no runtime")
    if spec.get("parent_source_universe_head") != "f56f52b3606839147a12e68375612336fb9bbfdd":
        errors.append("parent source-universe binding drifted")

    _exact_unique(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    if spec.get("pipeline") != EXPECTED_PIPELINE:
        errors.append("pipeline order/identity drifted")
    _exact_unique(errors, spec.get("admission_rules"), EXPECTED_RULES, "admission_rules")
    _exact_unique(errors, spec.get("claim_ceiling"), EXPECTED_CEILING, "claim_ceiling")

    donors = spec.get("donor_sources")
    if not isinstance(donors, list):
        errors.append("donor_sources must be a list")
        donors = []
    if len(donors) != len(EXPECTED_DONORS):
        errors.append("donor_sources must contain exact four-source cut")
    seen_donors: set[str] = set()
    for donor in donors:
        if not isinstance(donor, dict):
            errors.append("donor source must be object")
            continue
        repository = donor.get("repository")
        if repository in seen_donors:
            errors.append("donor repositories must be unique")
        seen_donors.add(repository)
        expected_head = EXPECTED_DONORS.get(repository)
        if expected_head is None:
            errors.append(f"unexpected donor repository: {repository!r}")
            continue
        if donor.get("ref") != "main":
            errors.append(f"{repository}: donor ref must be main")
        if donor.get("exact_head") != expected_head:
            errors.append(f"{repository}: exact donor head drifted")
        if not isinstance(donor.get("exact_head"), str) or not SHA40.fullmatch(donor["exact_head"]):
            errors.append(f"{repository}: exact donor head must be lowercase 40-hex")
        if not isinstance(donor.get("role"), str) or not donor["role"]:
            errors.append(f"{repository}: donor role missing")
    if seen_donors != set(EXPECTED_DONORS):
        errors.append("donor source set drifted")

    objects = spec.get("objects")
    if not isinstance(objects, dict) or set(objects) != EXPECTED_OBJECTS:
        errors.append("object families must be exact closed set")
        objects = {}
    for name, definition in objects.items():
        if not isinstance(definition, dict):
            errors.append(f"{name}: object definition must be object")
            continue
        required = definition.get("required")
        if not isinstance(required, list) or not required or len(required) != len(set(required)):
            errors.append(f"{name}: required fields must be non-empty unique list")
        if not isinstance(definition.get("purpose"), str) or not definition["purpose"]:
            errors.append(f"{name}: purpose missing")

    acquisition = objects.get("AcquisitionRecord", {})
    for required in ("raw_sha256", "privacy_scope", "source_revision_binding", "transport_evidence"):
        if required not in acquisition.get("required", []):
            errors.append(f"AcquisitionRecord must require {required}")

    normalization = objects.get("NormalizationRecord", {})
    for required in ("parent_raw_sha256", "transformations", "fidelity"):
        if required not in normalization.get("required", []):
            errors.append(f"NormalizationRecord must require {required}")

    interpretation = objects.get("InterpretationCandidate", {})
    for required in ("source_context", "provenance_class", "uncertainty", "lifecycle"):
        if required not in interpretation.get("required", []):
            errors.append(f"InterpretationCandidate must require {required}")

    decision = objects.get("EvidenceAdmissionDecision", {})
    for required in ("evidence_class", "claim_ceiling", "independence_family", "currentness_scope", "privacy_scope", "disposition"):
        if required not in decision.get("required", []):
            errors.append(f"EvidenceAdmissionDecision must require {required}")

    if fixtures.get("schema_version") != "GOD_BRAIN_INTAKE_EVIDENCE_HOSTILE_CASES_V0_1":
        errors.append("fixture schema_version drifted")
    cases = fixtures.get("cases")
    if not isinstance(cases, list):
        errors.append("fixture cases must be list")
        cases = []
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if set(ids) != EXPECTED_CASES or len(ids) != 12:
        errors.append("hostile fixture ids must be exactly IE-01..IE-12")
    if len(ids) != len(set(ids)):
        errors.append("hostile fixture ids must be unique")
    for case in cases:
        if not isinstance(case, dict):
            errors.append("hostile fixture case must be object")
            continue
        guards = case.get("guards")
        if not isinstance(guards, list) or not guards:
            errors.append(f"{case.get('id')}: hostile fixture needs guards")
            continue
        for guard in guards:
            if guard not in EXPECTED_INVARIANTS and guard not in EXPECTED_RULES:
                errors.append(f"{case.get('id')}: unknown guard {guard}")
        if not isinstance(case.get("expected"), str) or not case["expected"]:
            errors.append(f"{case.get('id')}: expected result missing")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "ACQUIRED != TRUSTED",
        "RAW != NORMALIZED",
        "NORMALIZED != INTERPRETED",
        "INTERPRETED != VERIFIED",
        "RETRIEVED != ADMITTED",
        "STORED != CURRENT",
        "CURRENT != TRUE",
        "SIMILAR != SAME_PROVENANCE",
        "TOOL_OUTPUT != AUTHORITY",
        "EVIDENCE != AUTHORITY",
        "CAPABILITY != PERMISSION",
        "CURRENTNESS != AUTHORIZATION",
    ):
        if marker not in doc:
            errors.append(f"research doc missing marker: {marker}")

    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_intake_evidence_admission(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain intake/evidence admission V0.1: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
