from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SPEC_PATH = "specs/GOD_BRAIN_PROJECT_FILE_ARCHITECTURE_V0_1.yaml"
DOC_PATH = "docs/research/GOD_BRAIN_PROJECT_FILE_ARCHITECTURE_V0_1.md"

REQUIRED_STRATA = {
    "ROOT_DISCOVERY_MANIFEST",
    "CONSTITUTIONAL_CONTRACTS",
    "MACHINE_CURRENT_POINTER",
    "HUMAN_CANONICAL_CURRENTNESS",
    "MUTABLE_OPERATIONAL_STATE",
    "REVIEW_EVIDENCE",
    "CONTINUATION_CHECKPOINTS",
    "RESEARCH_AND_PROPOSALS",
}

REQUIRED_FORBIDDEN_CURRENT_POINTER_FIELDS = {
    "open_pull_requests",
    "active_reviews",
    "delegated_subjects",
    "provider_health",
    "runtime_health",
    "current_chat",
    "current_commit_sha",
}

REQUIRED_CLAIM_CEILING = {
    "NO_CANONICAL_PROMOTION",
    "NO_GOVERNANCE_ADOPTION",
    "NO_RUNTIME_OR_PROVIDER_CURRENTNESS_CLAIM",
}


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be an object")
    return value


def validate_project_file_architecture(root: Path) -> list[str]:
    errors: list[str] = []
    spec_path = root / SPEC_PATH
    doc_path = root / DOC_PATH

    if not spec_path.is_file():
        errors.append(f"missing {SPEC_PATH}")
        return errors
    if not doc_path.is_file():
        errors.append(f"missing {DOC_PATH}")

    try:
        spec = _load_object(spec_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"{SPEC_PATH} must be JSON-compatible YAML: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_PROJECT_FILE_ARCHITECTURE_V0_1":
        errors.append("unexpected schema_version")
    if spec.get("status") != "RESEARCH_PROPOSAL_MACHINE_CONTRACT":
        errors.append("status must remain research-only")

    claim_ceiling = set(spec.get("claim_ceiling", []))
    missing_claims = REQUIRED_CLAIM_CEILING - claim_ceiling
    if missing_claims:
        errors.append(f"claim_ceiling missing: {sorted(missing_claims)}")

    strata = spec.get("strata")
    if not isinstance(strata, list):
        errors.append("strata must be a list")
        strata = []

    ids = {item.get("id") for item in strata if isinstance(item, dict)}
    missing_strata = REQUIRED_STRATA - ids
    if missing_strata:
        errors.append(f"missing strata: {sorted(missing_strata)}")

    pointer_entries = [
        item for item in strata
        if isinstance(item, dict) and item.get("id") == "MACHINE_CURRENT_POINTER"
    ]
    if len(pointer_entries) != 1:
        errors.append("exactly one MACHINE_CURRENT_POINTER stratum is required")
    else:
        forbidden = set(pointer_entries[0].get("forbidden", []))
        required = {
            "open_pr_state",
            "current_review_assignments",
            "bus_assignment_state",
            "provider_health",
            "runtime_reachability",
            "self_commit_sha",
        }
        if not required.issubset(forbidden):
            errors.append("machine current pointer stratum does not forbid all volatile state classes")

    future = spec.get("future_current_pointer_contract")
    if not isinstance(future, dict):
        errors.append("future_current_pointer_contract must be an object")
    else:
        forbidden_fields = set(future.get("forbidden_fields", []))
        missing = REQUIRED_FORBIDDEN_CURRENT_POINTER_FIELDS - forbidden_fields
        if missing:
            errors.append(f"future current pointer missing forbidden fields: {sorted(missing)}")
        if future.get("proposed_path") != "architecture/current/GOD_BRAIN_CURRENT.json":
            errors.append("future current pointer path drifted")
        truth_ceiling = future.get("required_truth_ceiling", "")
        if "must be freshly read" not in truth_ceiling:
            errors.append("future current pointer truth ceiling must require fresh mutable-state reads")

    if doc_path.is_file():
        doc = doc_path.read_text(encoding="utf-8")
        required_markers = (
            "CURRENT_MD = CANONICAL_INTERPRETATION_OF_MAIN",
            "CURRENT_POINTER != CURRENT_GIT_OBSERVATION",
            "CHECKPOINT = RECOVERY_ACCELERATOR",
            "PR-description currentness",
            "Research proposal path dependency",
        )
        for marker in required_markers:
            if marker not in doc:
                errors.append(f"{DOC_PATH} missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_project_file_architecture(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain project file architecture research contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
