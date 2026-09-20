from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SPEC_PATH = "specs/research/GOD_BRAIN_ATOMIC_INTEGRATION_BLUEPRINT_V0_1.yaml"
DOC_PATH = "docs/research/GOD_BRAIN_ATOMIC_INTEGRATION_BLUEPRINT_V0_1.md"
FIXTURE_PATH = "specs/research/fixtures/GOD_BRAIN_COMPOSITE_CONFORMANCE_CASES_V0_1.json"
PROVENANCE_PATH = "specs/research/GOD_BRAIN_COMPOSITE_PROVENANCE_MANIFEST_V0_1.json"

REQUIRED_INPUTS = {
    "foundation",
    "rebinding_proposal",
    "governance",
    "project_interface",
    "project_file_architecture",
    "instruction_sync",
}

REQUIRED_CLAIM_CEILING = {
    "NO_CANONICAL_PROMOTION",
    "NO_MERGE_AUTHORITY",
    "NO_PENDING_REVIEW_PASS_CLAIM",
    "NO_PROJECT_SETTING_MUTATION",
}

REQUIRED_FORBIDDEN_CURRENT_FIELDS = {
    "open_pull_requests",
    "active_reviews",
    "delegated_subjects",
    "bus_work_queue",
    "provider_health",
    "runtime_health",
    "current_chat",
    "current_commit_sha",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root must be object")
    return value


def validate_atomic_integration_blueprint(root: Path) -> list[str]:
    errors: list[str] = []
    spec_path = root / SPEC_PATH
    doc_path = root / DOC_PATH

    if not spec_path.is_file():
        return [f"missing {SPEC_PATH}"]
    if not doc_path.is_file():
        errors.append(f"missing {DOC_PATH}")

    try:
        spec = _load(spec_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"{SPEC_PATH} invalid JSON-compatible YAML: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_ATOMIC_INTEGRATION_BLUEPRINT_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_PLAN_MACHINE_CONTRACT":
        errors.append("status must remain research-plan only")

    missing_claims = REQUIRED_CLAIM_CEILING - set(spec.get("claim_ceiling", []))
    if missing_claims:
        errors.append(f"claim ceiling missing: {sorted(missing_claims)}")

    inputs = spec.get("inputs")
    if not isinstance(inputs, dict):
        errors.append("inputs must be object")
        inputs = {}
    missing_inputs = REQUIRED_INPUTS - set(inputs)
    if missing_inputs:
        errors.append(f"inputs missing: {sorted(missing_inputs)}")

    for name in ("governance", "project_interface", "project_file_architecture", "instruction_sync"):
        item = inputs.get(name)
        if not isinstance(item, dict):
            continue
        if item.get("role") != "PENDING_REVIEW_INPUT":
            errors.append(f"{name} must remain PENDING_REVIEW_INPUT until reconciled")
        if item.get("required_before_assembly") != "REVIEW_CLEAN_SUCCESSOR":
            errors.append(f"{name} must require a review-clean successor before assembly")

    if spec.get("component_review_rule") != "COMPONENT_REVIEW_PASS_NE_COMPOSITE_REVIEW_PASS":
        errors.append("component/composite review separation drifted")

    if spec.get("head_movement_rule") != "HEAD_MOVEMENT_MAKES_PRIOR_REVIEW_HISTORICAL_ONLY":
        errors.append("head movement rule drifted")

    paths = spec.get("candidate_paths")
    if not isinstance(paths, dict):
        errors.append("candidate_paths must be object")
    else:
        required_paths = {
            "root_interface",
            "human_currentness",
            "repository_map",
            "god_brain_governance",
            "machine_current_pointer",
            "epistemic_contract",
            "routing_contract",
            "recovery_contract",
            "project_instruction_source",
        }
        missing = required_paths - set(paths)
        if missing:
            errors.append(f"candidate paths missing: {sorted(missing)}")

    preserve = set(spec.get("preserve_unchanged_first_pass", []))
    if "WARDEN.md" not in preserve:
        errors.append("WARDEN.md must remain unchanged in the first integration pass")

    conformance = spec.get("composite_conformance")
    if not isinstance(conformance, dict):
        errors.append("composite_conformance must be object")
    else:
        if conformance.get("repository_map_must_not_present_hc_as_whole_repository") is not True:
            errors.append("repository map HC-whole-repository prohibition missing")
        if conformance.get("warden_classification") != "HC_PREDECESSOR_GOVERNANCE_SOURCE":
            errors.append("WARDEN classification drifted")
        if conformance.get("all_root_interface_paths_must_exist") is not True:
            errors.append("root interface path existence rule missing")
        forbidden = set(conformance.get("machine_current_pointer_forbidden_fields", []))
        missing = REQUIRED_FORBIDDEN_CURRENT_FIELDS - forbidden
        if missing:
            errors.append(f"machine current pointer forbidden fields missing: {sorted(missing)}")
        if conformance.get("protected_effect_authority") != "PATRICK_EXPLICIT_EXACT_EFFECT":
            errors.append("protected effect authority drifted")

    root_audit = spec.get("root_surface_audit")
    if not isinstance(root_audit, dict):
        errors.append("root_surface_audit must be object")
    else:
        surfaces = root_audit.get("surfaces")
        if not isinstance(surfaces, dict):
            errors.append("root_surface_audit.surfaces must be object")
            surfaces = {}
        required_surface_dispositions = {
            "README.md": "GOD_BRAIN_CORRECT",
            "CURRENT.md": "MANDATORY_REBINDING_TARGET",
            "docs/REPOSITORY_MAP.md": "MANDATORY_REBINDING_TARGET",
            "WARDEN.md": "PRESERVE_AS_HC_PREDECESSOR_GOVERNANCE_SOURCE",
        }
        for path, disposition in required_surface_dispositions.items():
            item = surfaces.get(path)
            if not isinstance(item, dict):
                errors.append(f"root surface missing: {path}")
                continue
            if item.get("disposition") != disposition:
                errors.append(f"root surface disposition drifted: {path}")
        current = surfaces.get("CURRENT.md")
        if isinstance(current, dict) and current.get("forbidden_final_referent") != "HC_BRAIN_AS_PROJECT_CURRENTNESS":
            errors.append("CURRENT.md must forbid inherited HC project-currentness referent")
        repo_map = surfaces.get("docs/REPOSITORY_MAP.md")
        if isinstance(repo_map, dict) and repo_map.get("forbidden_final_referent") != "HC_AS_WHOLE_REPOSITORY_WITH_WARDEN_CURRENT_AUTHORITY":
            errors.append("repository map must forbid HC whole-repository/Warden-current referent")
        warden = surfaces.get("WARDEN.md")
        if isinstance(warden, dict) and warden.get("must_remain_unchanged_first_pass") is not True:
            errors.append("WARDEN.md must remain unchanged in first pass")
        convergence = set(root_audit.get("required_final_convergence", []))
        required_convergence = {
            "README_EQ_GOD_BRAIN",
            "CURRENT_EQ_GOD_BRAIN",
            "REPOSITORY_MAP_EQ_GOD_BRAIN_WITH_HC_SUBSTRATE",
            "WARDEN_EQ_HC_PREDECESSOR_GOVERNANCE_SOURCE",
        }
        if not required_convergence.issubset(convergence):
            errors.append("root surface final convergence requirements incomplete")

    installation = spec.get("project_installation_rule")
    if not isinstance(installation, dict):
        errors.append("project_installation_rule must be object")
    else:
        if installation.get("candidate_pack_is_canonical") is not False:
            errors.append("candidate Project pack must not be canonical")
        if installation.get("canonical_source_movement_invalidates_current_verification") is not True:
            errors.append("canonical source movement must invalidate prior Project installation verification")

    assembly = spec.get("assembly_method")
    if not isinstance(assembly, dict):
        errors.append("assembly_method must be object")
    else:
        if assembly.get("branch_from_fresh_main") is not True:
            errors.append("composite must branch from fresh main")
        if assembly.get("merge_source_branches_wholesale") is not False:
            errors.append("whole source branch merges must remain prohibited")
        if assembly.get("file_level_provenance_required") is not True:
            errors.append("file-level provenance must be required")
        if assembly.get("composite_status_edits_require_fresh_review") is not True:
            errors.append("composite status edits must require fresh review")

    fixture_path = root / FIXTURE_PATH
    if not fixture_path.is_file():
        errors.append(f"missing {FIXTURE_PATH}")
    else:
        try:
            fixture = _load(fixture_path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{FIXTURE_PATH} invalid JSON: {exc}")
            fixture = {}
        if fixture.get("schema_version") != "GOD_BRAIN_COMPOSITE_CONFORMANCE_CASES_V0_1":
            errors.append("composite fixture schema_version drifted")
        if fixture.get("status") != "RESEARCH_FIXTURES":
            errors.append("composite fixtures must remain research fixtures")
        cases = fixture.get("cases")
        if not isinstance(cases, list):
            errors.append("composite fixture cases must be list")
            cases = []
        expected_ids = [f"GB-COMP-{i:03d}" for i in range(1, 17)]
        actual_ids = [case.get("id") for case in cases if isinstance(case, dict)]
        if actual_ids != expected_ids:
            errors.append("composite fixture IDs must be contiguous GB-COMP-001..016")
        dispositions = [case.get("expected") for case in cases if isinstance(case, dict)]
        if dispositions.count("REJECT") != 12 or dispositions.count("ACCEPT") != 4:
            errors.append("composite fixtures must contain 12 REJECT and 4 ACCEPT cases")
        for case in cases:
            if not isinstance(case, dict):
                errors.append("composite fixture case must be object")
                continue
            if case.get("expected") not in {"REJECT", "ACCEPT"}:
                errors.append(f"{case.get('id')} has invalid expected disposition")
            if not case.get("reason"):
                errors.append(f"{case.get('id')} missing reason")

    provenance_path = root / PROVENANCE_PATH
    if not provenance_path.is_file():
        errors.append(f"missing {PROVENANCE_PATH}")
    else:
        try:
            provenance = _load(provenance_path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{PROVENANCE_PATH} invalid JSON: {exc}")
            provenance = {}
        if provenance.get("schema_version") != "GOD_BRAIN_COMPOSITE_PROVENANCE_MANIFEST_V0_1":
            errors.append("composite provenance schema_version drifted")
        if provenance.get("status") != "RESEARCH_PROVENANCE_PLAN":
            errors.append("composite provenance must remain research-plan state")
        sources = provenance.get("sources")
        if not isinstance(sources, list):
            errors.append("composite provenance sources must be list")
            sources = []
        observed_prs = [source.get("pr") for source in sources if isinstance(source, dict)]
        if observed_prs != [6, 8, 10, 11, 12, 13]:
            errors.append("composite provenance source PR order/set drifted")
        expected_counts = {6: 7, 8: 1, 10: 1, 11: 9, 12: 5, 13: 6}
        for source in sources:
            if not isinstance(source, dict):
                errors.append("composite provenance source must be object")
                continue
            pr = source.get("pr")
            entries = source.get("entries")
            if not isinstance(entries, list):
                errors.append(f"PR {pr} provenance entries must be list")
                continue
            if pr in expected_counts and len(entries) != expected_counts[pr]:
                errors.append(f"PR {pr} provenance entry count drifted")
            for entry in entries:
                if not isinstance(entry, list) or len(entry) != 3:
                    errors.append(f"PR {pr} provenance entry must be [path, blob, disposition]")
                    continue
                path, blob, disposition = entry
                if not isinstance(path, str) or not path:
                    errors.append(f"PR {pr} provenance path invalid")
                if not isinstance(blob, str) or len(blob) != 40:
                    errors.append(f"PR {pr} provenance blob invalid for {path}")
                if not isinstance(disposition, str) or not disposition:
                    errors.append(f"PR {pr} provenance disposition missing for {path}")
        transformed = provenance.get("transformed_targets")
        if not isinstance(transformed, list) or len(transformed) != 3:
            errors.append("composite provenance must define exactly three transformed targets")
        invariants = set(provenance.get("assembly_invariants", []))
        required_invariants = {
            "FRESH_READ_EVERY_SOURCE_HEAD_BEFORE_COPY",
            "NO_SOURCE_BRANCH_WHOLESALE_MERGE",
            "EXACT_FILE_BLOB_PROVENANCE_REQUIRED",
            "TRANSFORMED_FILE_NE_SOURCE_REVIEWED_BLOB",
            "ALL_TRANSFORMATIONS_REQUIRE_COMPOSITE_REVIEW",
            "PENDING_REVIEW_INPUT_NE_ADMISSIBLE_UNTIL_REVIEW_CLEAN",
        }
        if not required_invariants.issubset(invariants):
            errors.append("composite provenance assembly invariants incomplete")

    if doc_path.is_file():
        doc = doc_path.read_text(encoding="utf-8")
        for marker in (
            "PROJECT_INSTALLATION != MAIN_PROMOTION",
            "COMPONENT_REVIEW_PASS != COMPOSITE_REVIEW_PASS",
            "MAIN_READY != MERGE_AUTHORITY",
            "CANONICAL_SOURCE_MOVEMENT -> PRIOR_INSTALLATION_NOT_CURRENTLY_VERIFIED",
            "OLD_CANDIDATE_INSTALLATION != CANONICAL_SOURCE_INSTALLATION",
            "MAIN_CURRENT_HC_REFERENT != GOD_BRAIN_CURRENTNESS",
            "WARDEN_TEXT_PRESERVED != WARDEN_AUTHORITY_IMPORTED",
        ):
            if marker not in doc:
                errors.append(f"{DOC_PATH} missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_atomic_integration_blueprint(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain atomic integration blueprint: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
