from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_INTEGRATION_READINESS_V0_2.md"
SPEC_PATH = "specs/research/GOD_BRAIN_INTEGRATION_READINESS_V0_2.json"

EXPECTED_INVARIANTS = {
    "READINESS_SNAPSHOT_NE_CURRENT_TRUTH",
    "REVIEWED_COMPONENT_NE_REVIEWED_COMPOSITE",
    "MAIN_READY_NE_MERGE_AUTHORITY",
    "SOURCE_ACCEPTANCE_NE_CANONICAL_ADOPTION",
    "NOOPLEX_FIXTURE_REVIEW_NE_GOD_BRAIN_ROOT_REBINDING_GATE",
    "SCIENCE_RESEARCH_SOURCE_ACCEPTANCE_NE_CORE_REPOSITORY_REBINDING_DEPENDENCY",
}

EXPECTED_ROOTS = {
    "README": ("GOD_BRAIN", "fbcaaec73b6d80f71849115533adbfb7c9098663"),
    "CURRENT": ("HC_PREDECESSOR_CURRENTNESS_STALE_FOR_GOD_BRAIN", "f5ff3f9ffe8e55e5cf1fe122afee7978ae1ed113"),
    "REPOSITORY_MAP": ("HC_PREDECESSOR_MAP_STALE_FOR_GOD_BRAIN", "642d191ec62ab1ee959069bc5e32f2c47c632caa"),
    "WARDEN": ("HC_PREDECESSOR_GOVERNANCE_SOURCE", "4018be2085d1a97957f73c9ad0ab430f5794d0a5"),
}

EXPECTED_TRACK_A = [
    ("A0_FOUNDATION_PR6", 6, "c8aff4109e53930a15eed54ab2f00b746ec8b09c", "ATOMIC_INTEGRATION_REVIEW_PASS_MAIN_READY_NO_MERGE_AUTHORITY"),
    ("A1_PROJECT_INTERFACE_PR18", 18, "d0a16b876895397c214c96e5f6630f83c58967e5", "REVIEW_PENDING_BLOCKER_CANDIDATE"),
    ("A2_PROJECT_FILE_PR22", 22, "09d00ae20879ca76560d2eba525105e0856b7076", "SUCCESSOR_REPAIR_PENDING_FRESH_REVIEW"),
    ("A3_GOVERNANCE_PR23", 23, "1f0a7516d58638d427bdd2dce24ed54d71aa5e5a", "REVIEWED_RESEARCH_SOURCE_CANDIDATE"),
    ("A4_INSTRUCTION_SYNC_PR24", 24, "fd2ca21740509ee501a3b09eb430559cc12e9031", "CHANGES_REQUIRED_NEEDS_POINTER_BINDING_SUCCESSOR"),
    ("A5_ROOT_REBINDING", None, None, "NOT_YET_AUTHORED_ON_CURRENT_REVIEWED_COMPOSITE"),
]

EXPECTED_TRACK_B = [
    ("B1_ANOMALY_CONTACT_PR25", 25, "d71f590eb7117f746ae7d3d761e3428a82ff5102", "REVIEWED_RESEARCH_SOURCE_CANDIDATE"),
    ("B2_SIMULATION_TESTABILITY_PR26", 26, "dd579e79190a53bba998d70be1c4d2179c213aaf", "REVIEWED_RESEARCH_SOURCE_CANDIDATE"),
    ("B3_PROVENANCE_PR27", 27, "14bc622b91e35683ffea8550ee06472926ce9812", "REVIEWED_RESEARCH_SOURCE_CANDIDATE_POINTERS_VERIFIED_AT_T1"),
]

EXPECTED_TRACK_C = [
    ("C1_HCDN_ALLOF_PR16", 16, "864a8adab84a89af03972b97a1d9554eabf941c3", "REVIEW_PENDING_BLOCKER_CANDIDATE_NOT_CORE_CONVERGENCE_BLOCKING"),
]

EXPECTED_PREREQUISITES = {
    "PR18_REVIEW_CLEAN_SUCCESSOR",
    "PR22_FRESH_EXACT_HEAD_REVIEW",
    "PR24_POINTER_BINDING_SUCCESSOR_REVIEW_CLEAN",
    "PR23_HEAD_UNCHANGED_AND_SOURCE_ACCEPTED",
    "PR6_HEAD_UNCHANGED_AND_ATOMIC_REVIEW_PASS",
    "FRESH_READ_MAIN",
    "AUTHOR_ROOT_REPOSITORY_MAP_REBINDING",
    "CLASSIFY_UNCHANGED_WARDEN_AS_HC_PREDECESSOR_GOVERNANCE",
    "MACHINE_CURRENT_POINTER_ONLY_AFTER_REFERENCED_CANONICAL_FILES_COEXIST",
    "FRESH_EXACT_COMPOSITE_REVIEW",
    "PATRICK_EXACT_MERGE_AUTHORIZATION",
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


def _validate_track(
    errors: list[str],
    actual: Any,
    expected: list[tuple[str, int | None, str | None, str]],
    label: str,
) -> None:
    if not isinstance(actual, list):
        errors.append(f"{label} must be list")
        return
    if len(actual) != len(expected):
        errors.append(f"{label} length drifted")
        return

    for item, (expected_id, expected_pr, expected_head, expected_state) in zip(actual, expected):
        if not isinstance(item, dict):
            errors.append(f"{label} entry must be object")
            continue
        allowed = {"id", "state"}
        if expected_pr is not None:
            allowed.add("pr")
        if expected_head is not None:
            allowed.add("head")
        if set(item) != allowed:
            errors.append(f"{label}.{expected_id} fields must be exact")
        if item.get("id") != expected_id:
            errors.append(f"{label} identity/order drifted")
        if expected_pr is not None and item.get("pr") != expected_pr:
            errors.append(f"{expected_id}.pr drifted")
        if expected_head is not None and item.get("head") != expected_head:
            errors.append(f"{expected_id}.head drifted")
        if item.get("state") != expected_state:
            errors.append(f"{expected_id}.state drifted")


def validate_integration_readiness(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (DOC_PATH, SPEC_PATH):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        spec = _load(root / SPEC_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid readiness spec: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_INTEGRATION_READINESS_V0_2":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_CURRENTNESS_SNAPSHOT":
        errors.append("status drifted")
    if spec.get("observed_main_head") != "c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5":
        errors.append("observed main head drifted")
    if spec.get("snapshot_is_currentness_authority") is not False:
        errors.append("snapshot must not become currentness authority")

    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")

    roots = spec.get("root_surfaces")
    if not isinstance(roots, dict) or set(roots) != set(EXPECTED_ROOTS):
        errors.append("root surface set drifted")
    else:
        for key, (classification, blob) in EXPECTED_ROOTS.items():
            entry = roots.get(key)
            if not isinstance(entry, dict) or set(entry) != {"classification", "blob"}:
                errors.append(f"root surface {key} fields drifted")
                continue
            if entry.get("classification") != classification:
                errors.append(f"root surface {key} classification drifted")
            if entry.get("blob") != blob:
                errors.append(f"root surface {key} blob drifted")

    tracks = spec.get("tracks")
    if not isinstance(tracks, dict):
        errors.append("tracks must be object")
        tracks = {}
    if set(tracks) != {
        "A_CORE_REPOSITORY_CONVERGENCE",
        "B_SCIENCE_RESEARCH",
        "C_NOOPLEX_EXECUTION",
    }:
        errors.append("track set drifted")

    _validate_track(errors, tracks.get("A_CORE_REPOSITORY_CONVERGENCE"), EXPECTED_TRACK_A, "track A")
    _validate_track(errors, tracks.get("B_SCIENCE_RESEARCH"), EXPECTED_TRACK_B, "track B")
    _validate_track(errors, tracks.get("C_NOOPLEX_EXECUTION"), EXPECTED_TRACK_C, "track C")

    _exact_set(
        errors,
        spec.get("core_composite_prerequisites"),
        EXPECTED_PREREQUISITES,
        "core composite prerequisites",
    )

    if spec.get("composite_assembly_rule") != "FRESH_MAIN_PLUS_REVIEWED_FILE_LEVEL_INPUTS_PLUS_NEW_REBINDING_DELTA":
        errors.append("composite assembly rule drifted")
    if spec.get("prohibited_assembly_rule") != "MERGE_ALL_SOURCE_BRANCHES":
        errors.append("prohibited assembly rule drifted")

    expected_classification = {
        "track_a": "REPAIR_AND_REVIEW_REQUIRED_BEFORE_FRESH_COMPOSITE",
        "track_b": "MULTIPLE_REVIEWED_RESEARCH_SOURCE_CANDIDATES_AVAILABLE",
        "track_c": "REVIEW_PENDING_NOT_CORE_CONVERGENCE_BLOCKING",
        "canonical_main": "NOT_YET_GOD_BRAIN_COHERENT_ACROSS_ROOT_CURRENTNESS_SURFACES",
        "protected_effects": "NO_MERGE_OR_CANONICAL_PROMOTION_AUTHORIZED",
    }
    if spec.get("classification") != expected_classification:
        errors.append("readiness classification drifted")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "READINESS_SNAPSHOT != CURRENT_TRUTH",
        "REVIEWED_COMPONENT != REVIEWED_COMPOSITE",
        "MAIN_READY != MERGE_AUTHORITY",
        "NOOPLEX_FIXTURE_REVIEW != GOD_BRAIN_ROOT_REBINDING_GATE",
        "FRESH_MAIN + REVIEWED_FILE_LEVEL_INPUTS + NEW_REBINDING_DELTA",
        "PATRICK_EXACT_MERGE_AUTHORIZATION",
    ):
        if marker not in doc:
            errors.append(f"readiness doc missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_integration_readiness(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain integration readiness V0.2: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
