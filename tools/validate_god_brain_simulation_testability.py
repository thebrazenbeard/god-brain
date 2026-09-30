from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DOC_PATH = "docs/research/GOD_BRAIN_SIMULATION_TESTABILITY_BOUNDARY_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_SIMULATION_TESTABILITY_BOUNDARY_V0_1.json"
FIXTURE_PATH = "specs/research/fixtures/GOD_BRAIN_SIMULATION_TESTABILITY_HOSTILE_CASES_V0_1.json"

EXPECTED_CLASSES = ["S0","S1","S2","S3","S4","S5","S6"]

REQUIRED_CLAIM_CEILING = {
    "NO_SIMULATION_FACT_CLAIM",
    "NO_NONSIMULATION_FACT_CLAIM",
    "NO_SIMULATION_PROBABILITY_ASSIGNMENT",
    "NO_CURRENT_ARTIFACT_CLAIM",
    "NO_CANONICAL_PROMOTION",
}

REQUIRED_INVARIANTS = {
    "TEST_OF_SIMULATION_SUBMODEL_NE_TEST_OF_SIMULATION_HYPOTHESIS_IN_GENERAL",
    "LATTICE_SIGNATURE_NE_SIMULATOR_DETECTION",
    "RESOURCE_BOUND_UNDER_ASSUMPTIONS_NE_UNIVERSAL_SIMULATION_REFUTATION",
    "INFORMATION_IS_PHYSICALLY_BOUNDED_NE_REALITY_IS_EXTERNALLY_SIMULATED",
    "SUBSTRATE_ARTIFACT_SUPPORTED_NE_EXTERNAL_SIMULATOR_SUPPORTED",
    "UNEXPLAINED_INFORMATION_CHANNEL_NE_SIMULATION_PROOF",
    "MESSAGE_CONTENT_NE_SOURCE_AUTHENTICATION",
    "CLAIMED_IDENTITY_NE_VERIFIED_IDENTITY",
    "COMPUTABLE_DESCRIPTION_NE_EXTERNAL_COMPUTATION",
    "DISCRETENESS_NE_SIMULATION",
    "OUR_PHYSICS_LIMIT_NE_NECESSARILY_PARENT_PHYSICS_LIMIT",
    "TESTABILITY_CLASSIFICATION_NE_ANOMALY_ESCALATION",
}

REQUIRED_ADMISSION = {
    "EXACT_CLASS_S0_TO_S6",
    "EXPLICIT_TARGET_MODEL",
    "EXACT_RIVAL_SET",
    "SOURCE_AND_EVIDENCE_PROVENANCE",
    "OBSERVABLE_PREDICTION",
    "NULL_PREDICTION",
    "FALSIFIER_OR_EXPLICIT_NONFALSIFIABLE_STATUS",
    "PARENT_PHYSICS_ASSUMPTIONS",
    "RENDERING_ASSUMPTIONS",
    "INDEPENDENCE_AND_CUSTODY_PLAN",
    "STATISTICAL_PLAN",
    "INTERPRETATION_CEILING",
    "NON_OVERCLAIMING_RESULT_STATES",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root must be object")
    return value


def validate_simulation_testability(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (DOC_PATH, SPEC_PATH, FIXTURE_PATH):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        spec = _load(root / SPEC_PATH)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"{SPEC_PATH} invalid JSON: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_SIMULATION_TESTABILITY_BOUNDARY_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_PROPOSAL_MACHINE_CONTRACT":
        errors.append("status must remain research proposal")

    ceilings = set(spec.get("claim_ceiling", []))
    missing_ceilings = REQUIRED_CLAIM_CEILING - ceilings
    if missing_ceilings:
        errors.append(f"claim ceiling missing: {sorted(missing_ceilings)}")

    missing = REQUIRED_INVARIANTS - set(spec.get("invariants", []))
    if missing:
        errors.append(f"invariants missing: {sorted(missing)}")

    sources = spec.get("sources")
    if not isinstance(sources, list) or len(sources) != 6:
        errors.append("sources must bind exactly six declared literature inputs")
    else:
        ids = [x.get("id") for x in sources if isinstance(x, dict)]
        if ids != [
            "BOSTROM_2003","BEANE_DAVOUDI_SAVAGE_2014","VAZZA_2025",
            "EDGE_BROWN_2026","BEKENSTEIN_1981","BEKENSTEIN_2000"
        ]:
            errors.append("literature source identity/order drifted")
        for source in sources:
            if not isinstance(source, dict) or not source.get("doi"):
                errors.append("each literature source requires DOI provenance")

    classes = spec.get("classes")
    if not isinstance(classes, list):
        errors.append("classes must be list")
        classes = []
    ids = [x.get("id") for x in classes if isinstance(x, dict)]
    if ids != EXPECTED_CLASSES:
        errors.append("testability classes must be exactly S0..S6")
    class_map = {x.get("id"):x for x in classes if isinstance(x, dict)}
    if class_map.get("S4",{}).get("testability") != "EMPIRICALLY_UNDERDETERMINED_BY_DEFINITION":
        errors.append("S4 observational-equivalence boundary drifted")
    if class_map.get("S5",{}).get("positive_support_ceiling") != "BOUNDED_EXTERNAL_CHANNEL_HYPOTHESIS":
        errors.append("S5 may support only bounded external-channel hypothesis")
    if "IDENTITY_BY_SELF_ASSERTION" not in set(class_map.get("S6",{}).get("cannot_establish", [])):
        errors.append("S6 must reject identity by self-assertion")

    missing = REQUIRED_ADMISSION - set(spec.get("experiment_admission_required", []))
    if missing:
        errors.append(f"experiment admission fields missing: {sorted(missing)}")

    reject = set(spec.get("reject_if_success_criterion", []))
    if "SOMETHING_WEIRD_HAPPENS" not in reject or "SUBJECTIVE_MEANING" not in reject:
        errors.append("unscoped weirdness/subjective meaning must be rejected as success criteria")

    try:
        fixture = _load(root / FIXTURE_PATH)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{FIXTURE_PATH} invalid JSON: {exc}")
        fixture = {}

    if fixture.get("schema_version") != "GOD_BRAIN_SIMULATION_TESTABILITY_HOSTILE_CASES_V0_1":
        errors.append("fixture schema_version drifted")
    if fixture.get("status") != "RESEARCH_FIXTURES":
        errors.append("fixtures must remain research-only")
    cases = fixture.get("cases")
    if not isinstance(cases, list):
        errors.append("fixture cases must be list")
        cases = []
    expected_ids=[f"GB-ST-{i:03d}" for i in range(1,21)]
    actual_ids=[x.get("id") for x in cases if isinstance(x,dict)]
    if actual_ids != expected_ids:
        errors.append("fixture IDs must be contiguous GB-ST-001..020")
    by_id={x.get("id"):x for x in cases if isinstance(x,dict)}
    pinned={
        "GB-ST-003":("S1","REJECT_OVERCLAIM"),
        "GB-ST-006":("S2","REJECT_OVERCLAIM"),
        "GB-ST-009":("S4","PERFECT_OBSERVATIONAL_EQUIVALENCE_SIMULATION"),
        "GB-ST-011":("S5","INTERVENTION_CAPABLE_EXTERNAL_SYSTEM_MODEL"),
        "GB-ST-013":("S6","SIMULATOR_OR_EXTERNAL_SOURCE_IDENTITY_CLAIM"),
        "GB-ST-015":("UNSCOPED","REJECT_UNSCOPED_SIMULATION_CLAIM"),
        "GB-ST-020":("S1","ADMIT_EXPERIMENT_PACKET"),
    }
    for case_id,(classification,expected) in pinned.items():
        case=by_id.get(case_id,{})
        if case.get("classification") != classification or case.get("expected") != expected:
            errors.append(f"{case_id} classification expectation drifted")

    doc=(root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "TEST_OF_SIMULATION_SUBMODEL != TEST_OF_SIMULATION_HYPOTHESIS_IN_GENERAL",
        "LATTICE_SIGNATURE != SIMULATOR_DETECTION",
        "AD_HOC_VERISIMILITUDE_PRESERVATION -> LOSS_OF_FALSIFIABILITY",
        "COMPUTABLE_DESCRIPTION != EXTERNAL_COMPUTATION",
        "WEIRD -> SIMULATION",
        "OUR_PHYSICS_LIMIT != NECESSARILY_PARENT_PHYSICS_LIMIT",
        "TESTABILITY_CLASSIFICATION != ANOMALY_ESCALATION",
    ):
        if marker not in doc:
            errors.append(f"{DOC_PATH} missing marker: {marker}")

    return errors


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args=parser.parse_args()
    errors=validate_simulation_testability(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain simulation testability boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
