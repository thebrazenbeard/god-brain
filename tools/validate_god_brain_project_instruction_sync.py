from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SPEC_PATH = "specs/research/GOD_BRAIN_PROJECT_INSTRUCTION_SYNC_V0_1.yaml"
DOC_PATH = "docs/research/GOD_BRAIN_PROJECT_INSTRUCTION_SYNC_V0_1.md"

REQUIRED_SYNC_STATES = {
    "SOURCE_DRAFT",
    "SOURCE_CANONICAL_NOT_VERIFIED_INSTALLED",
    "INSTALLATION_REPORTED_UNVERIFIED",
    "INSTALLED_EXACT_SOURCE_VERIFIED",
    "INSTALLATION_DRIFT",
    "INSTALLATION_UNKNOWN",
}

REQUIRED_CLAIM_CEILING = {
    "NO_PROJECT_SETTING_MUTATION",
    "NO_INSTALLATION_CLAIM",
    "NO_CURRENT_CHAT_CONSUMPTION_CLAIM",
}

REQUIRED_RECEIPT_FIELDS = {
    "schema_version",
    "repository",
    "canonical_source_commit",
    "source_path",
    "source_git_blob",
    "normalized_source_sha256",
    "target_project_label",
    "action_type",
    "installer_identity",
    "observed_at",
    "verification_method",
    "comparison_result",
    "limitations",
    "claim_ceiling",
}


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} root must be an object")
    return value


def validate_project_instruction_sync(root: Path) -> list[str]:
    errors: list[str] = []
    spec_path = root / SPEC_PATH
    doc_path = root / DOC_PATH

    if not spec_path.is_file():
        return [f"missing {SPEC_PATH}"]
    if not doc_path.is_file():
        errors.append(f"missing {DOC_PATH}")

    try:
        spec = _load_object(spec_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"{SPEC_PATH} must be JSON-compatible YAML: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_PROJECT_INSTRUCTION_SYNC_V0_1":
        errors.append("unexpected schema_version")
    if spec.get("status") != "RESEARCH_PROPOSAL_MACHINE_CONTRACT":
        errors.append("status must remain research-only")

    missing_claims = REQUIRED_CLAIM_CEILING - set(spec.get("claim_ceiling", []))
    if missing_claims:
        errors.append(f"claim_ceiling missing: {sorted(missing_claims)}")

    missing_states = REQUIRED_SYNC_STATES - set(spec.get("sync_states", []))
    if missing_states:
        errors.append(f"sync_states missing: {sorted(missing_states)}")

    normalization = spec.get("normalization")
    if not isinstance(normalization, dict):
        errors.append("normalization must be an object")
    else:
        expected = {
            "encoding": "UTF-8",
            "line_endings": "LF",
            "preserve_other_characters": True,
            "final_newline": "EXACTLY_ONE_LF",
            "digest": "SHA-256",
        }
        for key, value in expected.items():
            if normalization.get(key) != value:
                errors.append(f"normalization.{key} drifted")

    receipt = spec.get("receipt")
    if not isinstance(receipt, dict):
        errors.append("receipt must be an object")
    else:
        missing_fields = REQUIRED_RECEIPT_FIELDS - set(receipt.get("required_fields", []))
        if missing_fields:
            errors.append(f"receipt required_fields missing: {sorted(missing_fields)}")
        forbidden = set(receipt.get("forbidden_fields", []))
        for sensitive in ("credential", "token", "secret"):
            if sensitive not in forbidden:
                errors.append(f"receipt must forbid {sensitive}")
        required_ceiling = set(receipt.get("required_claim_ceiling", []))
        marker = "INSTALLATION_RECEIPT_NE_PROOF_CURRENT_CHAT_CONSUMED_TEXT"
        if marker not in required_ceiling:
            errors.append("receipt claim ceiling must separate installation from chat consumption")

    effect = spec.get("effect_boundary")
    if not isinstance(effect, dict):
        errors.append("effect_boundary must be an object")
    else:
        if effect.get("project_instruction_install_or_replace") != "PROTECTED_EXTERNAL_CONFIGURATION_EFFECT":
            errors.append("Project instruction installation must remain a protected external configuration effect")
        if effect.get("required_authority") != "PATRICK_EXPLICIT_EXACT_EFFECT":
            errors.append("Project instruction installation authority drifted")

    bootstrap = spec.get("bootstrap_rule")
    if not isinstance(bootstrap, dict):
        errors.append("bootstrap_rule must be an object")
    else:
        if bootstrap.get("source_file_alone_proves_installation") is not False:
            errors.append("source file alone must not prove installation")
        if bootstrap.get("unknown_must_remain_unknown") is not True:
            errors.append("unknown installation state must remain unknown")
        required_classes = {"MATCH", "DRIFT", "UNKNOWN"}
        if not required_classes.issubset(set(bootstrap.get("required_classification_when_checked", []))):
            errors.append("bootstrap installation classification is incomplete")

    if doc_path.is_file():
        doc = doc_path.read_text(encoding="utf-8")
        for marker in (
            "SOURCE_INSTRUCTIONS != INSTALLED_PROJECT_INSTRUCTIONS",
            "INSTALLED_PROJECT_INSTRUCTIONS != CURRENT_CHAT_CONSUMPTION_PROOF",
            "SOURCE_PROMOTION != PROJECT_INSTALLATION",
            "GIT_BLOB_SHA != NORMALIZED_TEXT_SHA256",
            "SETTING_MATCH_AT_T1 != CHAT_CONSUMPTION_AT_T2",
        ):
            if marker not in doc:
                errors.append(f"{DOC_PATH} missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_project_instruction_sync(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain Project instruction sync research contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
