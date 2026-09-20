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

RECEIPT_DIR = "state/project-interface/instruction-installation"

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

    receipt_dir = root / RECEIPT_DIR
    if receipt_dir.is_dir():
        for receipt_path in sorted(receipt_dir.glob("*.json")):
            try:
                observed = _load_object(receipt_path)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                errors.append(f"{receipt_path.relative_to(root)} invalid receipt JSON: {exc}")
                continue

            if observed.get("schema_version") != "GOD_BRAIN_PROJECT_INSTRUCTION_INSTALLATION_RECEIPT_V0_1":
                errors.append(f"{receipt_path.relative_to(root)} unexpected receipt schema_version")
            if observed.get("repository") != "thebrazenbeard/god-brain":
                errors.append(f"{receipt_path.relative_to(root)} repository drifted")
            if observed.get("source_path") != "architecture/chatgpt/PROJECT_INSTRUCTIONS.md":
                errors.append(f"{receipt_path.relative_to(root)} source_path drifted")
            if observed.get("sync_state") not in REQUIRED_SYNC_STATES:
                errors.append(f"{receipt_path.relative_to(root)} invalid sync_state")

            limitations = observed.get("limitations")
            if not isinstance(limitations, list) or not limitations:
                errors.append(f"{receipt_path.relative_to(root)} limitations must be a nonempty list")

            ceilings = set(observed.get("claim_ceiling", []))
            if "INSTALLATION_RECEIPT_NE_PROOF_CURRENT_CHAT_CONSUMED_TEXT" not in ceilings:
                errors.append(f"{receipt_path.relative_to(root)} missing chat-consumption claim ceiling")
            if "NO_CANONICAL_PROMOTION" not in ceilings:
                errors.append(f"{receipt_path.relative_to(root)} missing canonical-promotion claim ceiling")

            methods = observed.get("verification_method")
            setting_method = methods.get("project_instruction_setting") if isinstance(methods, dict) else None
            if setting_method == "USER_REPORT_ONLY_NO_INDEPENDENT_SETTING_BYTE_READBACK":
                if observed.get("sync_state") == "INSTALLED_EXACT_SOURCE_VERIFIED":
                    errors.append(
                        f"{receipt_path.relative_to(root)} cannot claim exact installed source from user-report-only setting evidence"
                    )

            project_files = observed.get("project_file_verification")
            if isinstance(project_files, dict) and project_files.get("result") == "EXACT_PACK_MATCH":
                files = project_files.get("files")
                if not isinstance(files, dict) or len(files) < 6:
                    errors.append(f"{receipt_path.relative_to(root)} exact pack match lacks file digest evidence")

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
