from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SPEC_PATH = "specs/research/GOD_BRAIN_PROJECT_FILE_ARCHITECTURE_V0_1.yaml"
DOC_PATH = "docs/research/GOD_BRAIN_PROJECT_FILE_ARCHITECTURE_V0_1.md"

REQUIRED_CLAIM_CEILING = {
    "NO_CANONICAL_PROMOTION",
    "NO_GOVERNANCE_ADOPTION",
    "NO_RUNTIME_OR_PROVIDER_CURRENTNESS_CLAIM",
}

REQUIRED_STRATUM_GUARDS: dict[str, dict[str, Any]] = {
    "ROOT_DISCOVERY_MANIFEST": {
        "owns": {
            "project_identity",
            "bootstrap_routing",
            "stable_authority_boundaries",
            "freshness_requirement",
        },
        "forbidden": {
            "open_pr_list",
            "delegated_subject_list",
            "latest_review_verdicts",
            "live_provider_status",
            "latest_checkpoint",
        },
        "truth_ceiling": "DISCOVERY_AND_BOOTSTRAP_CONTRACT",
    },
    "CONSTITUTIONAL_CONTRACTS": {
        "owns": {
            "governance",
            "epistemic_policy",
            "routing_and_collision_policy",
            "privacy_and_provenance_policy",
        },
        "forbidden": {"volatile_operational_currentness"},
        "truth_ceiling": "STABLE_RULES_NOT_LIVE_OPERATIONAL_FACTS",
    },
    "MACHINE_CURRENT_POINTER": {
        "owns": {"canonical_source_contract_paths"},
        "forbidden": {
            "open_pr_state",
            "current_review_assignments",
            "bus_assignment_state",
            "provider_health",
            "runtime_reachability",
            "self_commit_sha",
        },
        "truth_ceiling": "RESOLVES_CANONICAL_SOURCE_CONTRACTS_ONLY",
    },
    "HUMAN_CANONICAL_CURRENTNESS": {
        "owns": {
            "human_interpretation_of_canonical_main",
            "durable_claim_ceilings",
            "canonical_layer_summary",
        },
        "forbidden": {
            "todays_work_queue",
            "waiting_on_reviewer",
            "volatile_pr_status",
            "live_provider_health",
        },
        "truth_ceiling": "CANONICAL_INTERPRETATION_OF_MAIN",
    },
    "MUTABLE_OPERATIONAL_STATE": {
        "sources": {
            "github_pr_branch_head_state",
            "review_surfaces",
            "chat_communication_bus",
            "ci_status",
            "provider_runtime_readback",
        },
        "rule": "FRESH_READ",
        "truth_ceiling": "OBSERVED_MUTABLE_STATE_ONLY",
    },
    "REVIEW_EVIDENCE": {
        "required_binding": {
            "repository",
            "exact_head",
            "base_when_applicable",
            "paths_blobs_or_semantic_subject",
            "reviewer_identity",
            "reviewer_role",
            "disposition",
            "limitations",
        },
        "forbidden": {
            "self_certification",
            "automatic_successor_head_inheritance",
        },
        "truth_ceiling": "EXACT_SUBJECT_REVIEW_EVIDENCE",
    },
    "CONTINUATION_CHECKPOINTS": {
        "owns": {
            "recovery_snapshot",
            "last_observed_frontier_pointers",
        },
        "forbidden": {
            "canonical_currentness",
            "worker_identity_authority",
            "review_carry_forward",
            "merge_authority",
            "live_provider_proof",
        },
        "truth_ceiling": "RECOVERY_ACCELERATOR_ONLY",
    },
    "RESEARCH_AND_PROPOSALS": {
        "owns": {
            "candidate_mechanisms",
            "unadopted_designs",
            "research_results_with_provenance",
        },
        "forbidden": {"implicit_adoption"},
        "truth_ceiling": "RESEARCH_ONLY_UNLESS_SEPARATELY_PROMOTED",
    },
}

REQUIRED_CURRENT_POINTER_FIELDS = {
    "schema",
    "repository",
    "canonical_branch",
    "project_interface_path",
    "governance_path",
    "epistemic_contract_path",
    "routing_contract_path",
    "human_currentness_path",
    "truth_ceiling",
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


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be an object")
    return value


def _require_members(
    entry: dict[str, Any],
    field: str,
    required: set[str],
    *,
    label: str,
    errors: list[str],
) -> None:
    value = entry.get(field)
    if not isinstance(value, list):
        errors.append(f"{label}.{field} must be a list")
        return
    missing = required - set(value)
    if missing:
        errors.append(f"{label}.{field} missing: {sorted(missing)}")


def _validate_stratum(
    entry: dict[str, Any],
    stratum_id: str,
    required: dict[str, Any],
    errors: list[str],
) -> None:
    label = f"stratum {stratum_id}"
    for field, expected in required.items():
        if isinstance(expected, set):
            _require_members(entry, field, expected, label=label, errors=errors)
        elif entry.get(field) != expected:
            errors.append(
                f"{label}.{field} mismatch: expected {expected!r}"
            )


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

    valid_entries = [item for item in strata if isinstance(item, dict)]
    ids = [item.get("id") for item in valid_entries]
    expected_ids = set(REQUIRED_STRATUM_GUARDS)
    if len(valid_entries) != len(strata):
        errors.append("every stratum must be an object")
    if len(ids) != len(set(ids)):
        errors.append("stratum ids must be unique")
    missing_strata = expected_ids - set(ids)
    unknown_strata = set(ids) - expected_ids
    if missing_strata:
        errors.append(f"missing strata: {sorted(missing_strata)}")
    if unknown_strata:
        errors.append(f"unknown strata: {sorted(unknown_strata)}")
    if len(strata) != len(expected_ids):
        errors.append(
            f"expected exactly {len(expected_ids)} declared strata; observed {len(strata)}"
        )

    entries_by_id = {
        item["id"]: item
        for item in valid_entries
        if item.get("id") in expected_ids
    }
    for stratum_id, required in REQUIRED_STRATUM_GUARDS.items():
        entry = entries_by_id.get(stratum_id)
        if entry is not None:
            _validate_stratum(entry, stratum_id, required, errors)

    future = spec.get("future_current_pointer_contract")
    if not isinstance(future, dict):
        errors.append("future_current_pointer_contract must be an object")
    else:
        if future.get("schema") != "GOD_BRAIN_CURRENT_POINTER_V1":
            errors.append("future current pointer schema drifted")
        if future.get("proposed_path") != "architecture/current/GOD_BRAIN_CURRENT.json":
            errors.append("future current pointer path drifted")
        _require_members(
            future,
            "required_fields",
            REQUIRED_CURRENT_POINTER_FIELDS,
            label="future_current_pointer_contract",
            errors=errors,
        )
        _require_members(
            future,
            "forbidden_fields",
            REQUIRED_FORBIDDEN_CURRENT_POINTER_FIELDS,
            label="future_current_pointer_contract",
            errors=errors,
        )
        truth_ceiling = future.get("required_truth_ceiling", "")
        if (
            truth_ceiling
            != "Resolves canonical source contracts only; mutable PR/review/delegation/provider/runtime state must be freshly read."
        ):
            errors.append(
                "future current pointer truth ceiling must preserve the exact fresh-read boundary"
            )

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
