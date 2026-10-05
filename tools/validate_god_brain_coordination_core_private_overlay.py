from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_V0_1.json"
FIXTURE_PATH = "specs/research/fixtures/GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_HOSTILE_CASES_V0_1.json"

SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_DONORS = {
    "thebrazenbeard/ccb-core": "0b542a78ebf5827a518e0731a63f17a7ac8a2727",
    "thebrazenbeard/chat-communication-bus": "e0bcb5eb18630693de55a1af2066411c7af079bb",
}

EXPECTED_INVARIANTS = {
    "REUSABLE_CODE_AUTHORITY_NE_PRIVATE_DEPLOYMENT_STATE",
    "PUBLIC_CORE_NE_PRIVATE_OVERLAY",
    "PRIVATE_DISCOVERY_NE_CANONICAL_GENERIC_FIX",
    "SOURCE_PIN_NE_DEPLOYMENT_AUTHORITY",
    "PRIVATE_HISTORY_NE_REUSABLE_IMPLEMENTATION",
    "PRIVATE_TOPOLOGY_NE_GENERIC_ROUTING_AUTHORITY",
    "PRIVATE_IDENTITY_STATE_NE_PORTABLE_MECHANISM",
    "GENERIC_FIX_REQUIRES_SANITIZED_CORE_REPRODUCTION",
    "CORE_QUALIFICATION_NE_OVERLAY_ACTIVATION",
    "OVERLAY_PIN_NE_CORE_MUTATION_AUTHORITY",
    "PRIVATE_OVERLAY_NE_INDEPENDENT_IMPLEMENTATION_AUTHORITY",
    "COORDINATION_STATE_NE_GOD_BRAIN_CANONICAL_REPOSITORY_STATE",
}

EXPECTED_PIPELINE = [
    "DISCOVER_GENERIC_OR_PRIVATE_FIX",
    "CLASSIFY_CORE_VS_OVERLAY",
    "SANITIZE_PRIVATE_MATERIAL",
    "REPRODUCE_IN_PUBLIC_CORE",
    "ADD_DETERMINISTIC_REGRESSION",
    "QUALIFY_EXACT_CORE_CUT",
    "PIN_OVERLAY_TO_QUALIFIED_CORE",
    "RECONCILE_PRIVATE_STATE_SEPARATELY",
]

EXPECTED_RULES = {
    "GENERIC_MECHANISM_MUST_LIVE_IN_CORE_AFTER_QUALIFICATION",
    "PRIVATE_DISCOVERY_MUST_SANITIZE_BEFORE_CORE_REPRODUCTION",
    "CORE_FIX_MUST_HAVE_DETERMINISTIC_REGRESSION",
    "OVERLAY_MAY_REFERENCE_CORE_ONLY_BY_EXACT_QUALIFIED_PIN",
    "OVERLAY_MUST_NOT_MAINTAIN_DIVERGENT_GENERIC_RUNTIME_COPY",
    "PRIVATE_STATE_MUST_REMAIN_OVERLAY_SCOPED",
    "PIN_MUST_NOT_GRANT_DEPLOYMENT_PROVIDER_OR_PRIVATE_TOPOLOGY_AUTHORITY",
    "CORE_HEAD_MOVEMENT_STALES_PRIOR_PIN_QUALIFICATION",
    "PRIVATE_HISTORY_MUST_NOT_BE_REQUIRED_TO_REPRODUCE_PUBLIC_MECHANISM",
    "BUS_COORDINATION_HUB_STATUS_MUST_NOT_REPLACE_GOD_BRAIN_GITHUB_CANON",
}

EXPECTED_OBJECTS = {"CoreMechanismBinding", "PrivateOverlayBinding", "GenericFixCandidate", "ConsumptionPin"}
EXPECTED_CASES = {f"CO-{i:02d}" for i in range(1, 11)}

def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be object")
    return value

def _closed(errors: list[str], value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be list")
        return
    if len(value) != len(set(value)):
        errors.append(f"{label} contains duplicates")
    if set(value) != expected:
        errors.append(f"{label} must be exact closed set")

def validate(root: Path) -> list[str]:
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
        return [f"invalid T36 contract: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_SPECIFICATION_NO_RUNTIME":
        errors.append("status must remain research specification / no runtime")
    if spec.get("parent_source_universe_head") != "f56f52b3606839147a12e68375612336fb9bbfdd":
        errors.append("parent source-universe binding drifted")

    donors = spec.get("donor_sources")
    if not isinstance(donors, list) or len(donors) != 2:
        errors.append("donor_sources must contain exact two-source cut")
        donors = []
    seen: set[str] = set()
    for donor in donors:
        if not isinstance(donor, dict):
            errors.append("donor must be object")
            continue
        repository = donor.get("repository")
        seen.add(repository)
        if repository not in EXPECTED_DONORS:
            errors.append(f"unexpected donor {repository!r}")
            continue
        if donor.get("ref") != "main":
            errors.append(f"{repository}: ref must be main")
        if donor.get("exact_head") != EXPECTED_DONORS[repository]:
            errors.append(f"{repository}: exact head drifted")
        if not isinstance(donor.get("exact_head"), str) or not SHA40.fullmatch(donor["exact_head"]):
            errors.append(f"{repository}: exact head must be lowercase 40-hex")
    if seen != set(EXPECTED_DONORS):
        errors.append("donor set drifted")

    _closed(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    if spec.get("pipeline") != EXPECTED_PIPELINE:
        errors.append("pipeline order/identity drifted")
    _closed(errors, spec.get("admission_rules"), EXPECTED_RULES, "admission_rules")

    objects = spec.get("objects")
    if not isinstance(objects, dict) or set(objects) != EXPECTED_OBJECTS:
        errors.append("object families must be exact closed set")
        objects = {}
    required_fields = {
        "CoreMechanismBinding": {"repository","ref","exact_head","role","public_safe_scope","qualification_refs"},
        "PrivateOverlayBinding": {"repository","ref","exact_head","role","private_state_classes","core_pin","privacy_scope"},
        "GenericFixCandidate": {"candidate_id","discovery_source","provenance_refs","sanitization_state","reproduction_state","regression_state","core_candidate_ref","disposition"},
        "ConsumptionPin": {"overlay_repository","core_repository","exact_core_head","qualification_ref","private_inputs","authority_flags"},
    }
    for name, required in required_fields.items():
        definition = objects.get(name, {})
        actual = definition.get("required") if isinstance(definition, dict) else None
        if not isinstance(actual, list) or not required.issubset(set(actual)):
            errors.append(f"{name}: required fields drifted")

    if fixtures.get("schema_version") != "GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_HOSTILE_CASES_V0_1":
        errors.append("fixture schema_version drifted")
    cases = fixtures.get("cases")
    if not isinstance(cases, list):
        errors.append("fixture cases must be list")
        cases = []
    ids=[case.get("id") for case in cases if isinstance(case, dict)]
    if set(ids) != EXPECTED_CASES or len(ids) != 10 or len(ids) != len(set(ids)):
        errors.append("hostile cases must be exactly CO-01..CO-10")
    for case in cases:
        if not isinstance(case, dict):
            errors.append("fixture case must be object")
            continue
        guards=case.get("guards")
        if not isinstance(guards, list) or not guards:
            errors.append(f"{case.get('id')}: guards missing")
            continue
        for guard in guards:
            if guard not in EXPECTED_INVARIANTS and guard not in EXPECTED_RULES:
                errors.append(f"{case.get('id')}: unknown guard {guard}")
        if not isinstance(case.get("expected"), str) or not case["expected"]:
            errors.append(f"{case.get('id')}: expected missing")

    doc=(root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "REUSABLE CODE AUTHORITY != PRIVATE DEPLOYMENT STATE",
        "PUBLIC CORE != PRIVATE OVERLAY",
        "PRIVATE DISCOVERY != CANONICAL GENERIC FIX",
        "SOURCE PIN != DEPLOYMENT AUTHORITY",
        "PRIVATE HISTORY != REUSABLE IMPLEMENTATION",
        "CORE QUALIFICATION != OVERLAY ACTIVATION",
        "COORDINATION STATE != GOD BRAIN CANONICAL REPOSITORY STATE",
        "COORDINATION SERVICE != SEAT OF COGNITION",
    ):
        if marker not in doc:
            errors.append(f"research doc missing marker: {marker}")

    return errors

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args=parser.parse_args()
    errors=validate(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain coordination core/private overlay V0.1: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
