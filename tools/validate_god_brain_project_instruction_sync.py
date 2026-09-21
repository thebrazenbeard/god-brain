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
SOURCE_POINTER_RECEIPT_PATH = (
    "state/project-interface/source-provenance/"
    "GOD_BRAIN_PROJECT_INSTRUCTION_SOURCE_POINTER_RECEIPT_V0_1.json"
)

REQUIRED_RECEIPT_FIELDS = {
    "schema_version",
    "repository",
    "source_status",
    "canonical_source_commit",
    "candidate_source_head",
    "source_pr",
    "source_verification_receipt",
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


def _is_sha40(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(ch in "0123456789abcdef" for ch in value)
    )


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

        source_rules = receipt.get("source_identity_rules")
        if not isinstance(source_rules, dict):
            errors.append("receipt source_identity_rules must be an object")
        else:
            if source_rules.get("source_status_values") != ["CANONICAL", "CANDIDATE_NONCANONICAL"]:
                errors.append("receipt source_status_values drifted")
            expected_rules = {
                "CANONICAL": {
                    "canonical_source_commit": "REQUIRED_40_HEX",
                    "candidate_source_head": "MUST_BE_NULL",
                    "source_pr": "MUST_BE_NULL",
                },
                "CANDIDATE_NONCANONICAL": {
                    "canonical_source_commit": "MUST_BE_NULL",
                    "candidate_source_head": "REQUIRED_40_HEX",
                    "source_pr": "REQUIRED_POSITIVE_INTEGER",
                },
            }
            for status, expected_rule in expected_rules.items():
                if source_rules.get(status) != expected_rule:
                    errors.append(f"receipt source identity rule drifted for {status}")

        pointer_contract = receipt.get("source_verification_receipt_contract")
        if not isinstance(pointer_contract, dict):
            errors.append("receipt source_verification_receipt_contract must be an object")
        else:
            if pointer_contract.get("candidate_source_receipt") != "REQUIRED":
                errors.append("candidate source verification receipt must remain required")
            if pointer_contract.get("required_schema") != "GOD_BRAIN_PROJECT_INSTRUCTION_SOURCE_POINTER_RECEIPT_V0_1":
                errors.append("source verification receipt schema drifted")
            if pointer_contract.get("required_status") != "EXACT_GIT_POINTER_VERIFIED":
                errors.append("source verification receipt status drifted")
            if pointer_contract.get("exact_tuple_fields") != [
                "repository",
                "source_pr",
                "candidate_source_head",
                "source_path",
                "source_git_blob",
            ]:
                errors.append("source verification tuple contract drifted")
            required_pointer_ceiling = {
                "POINTER_VERIFIED_AT_T1",
                "NO_CURRENTNESS_CLAIM",
                "NO_CANONICAL_PROMOTION",
                "NO_INSTALLATION_PROOF",
                "NO_PROJECT_SETTING_EFFECT",
            }
            if set(pointer_contract.get("receipt_claim_ceiling", [])) != required_pointer_ceiling:
                errors.append("source verification receipt claim ceiling drifted")

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

    pointer_path = root / SOURCE_POINTER_RECEIPT_PATH
    pointer_receipt: dict[str, Any] = {}
    if pointer_path.is_file():
        try:
            pointer_receipt = _load_object(pointer_path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{SOURCE_POINTER_RECEIPT_PATH} invalid pointer receipt: {exc}")
    else:
        errors.append(f"missing {SOURCE_POINTER_RECEIPT_PATH}")

    if pointer_receipt:
        if pointer_receipt.get("schema_version") != "GOD_BRAIN_PROJECT_INSTRUCTION_SOURCE_POINTER_RECEIPT_V0_1":
            errors.append("source pointer receipt schema_version drifted")
        if pointer_receipt.get("status") != "EXACT_GIT_POINTER_VERIFIED":
            errors.append("source pointer receipt status drifted")
        if pointer_receipt.get("verification_surface") != "GITHUB_EXACT_PR_HEAD_FILE_READBACK":
            errors.append("source pointer verification surface drifted")
        if pointer_receipt.get("repository") != "thebrazenbeard/god-brain":
            errors.append("source pointer repository drifted")
        if not _is_sha40(pointer_receipt.get("source_head")):
            errors.append("source pointer head must be lowercase 40-hex")
        if not _is_sha40(pointer_receipt.get("source_git_blob")):
            errors.append("source pointer git blob must be lowercase 40-hex")
        if pointer_receipt.get("source_path") != "architecture/chatgpt/PROJECT_INSTRUCTIONS.md":
            errors.append("source pointer path drifted")
        source_pr = pointer_receipt.get("source_pr")
        if isinstance(source_pr, bool) or not isinstance(source_pr, int) or source_pr <= 0:
            errors.append("source pointer PR must be a positive integer")
        required_pointer_ceiling = {
            "POINTER_VERIFIED_AT_T1",
            "NO_CURRENTNESS_CLAIM",
            "NO_CANONICAL_PROMOTION",
            "NO_INSTALLATION_PROOF",
            "NO_PROJECT_SETTING_EFFECT",
        }
        if set(pointer_receipt.get("claim_ceiling", [])) != required_pointer_ceiling:
            errors.append("source pointer claim ceiling drifted")

    receipt_dir = root / RECEIPT_DIR
    if receipt_dir.is_dir():
        for receipt_path in sorted(receipt_dir.glob("*.json")):
            try:
                observed = _load_object(receipt_path)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                errors.append(f"{receipt_path.relative_to(root)} invalid receipt JSON: {exc}")
                continue

            relative = receipt_path.relative_to(root)
            missing_observed = REQUIRED_RECEIPT_FIELDS - set(observed)
            if missing_observed:
                errors.append(f"{relative} missing required receipt fields: {sorted(missing_observed)}")

            if observed.get("schema_version") != "GOD_BRAIN_PROJECT_INSTRUCTION_INSTALLATION_RECEIPT_V0_1":
                errors.append(f"{relative} unexpected receipt schema_version")
            if observed.get("repository") != "thebrazenbeard/god-brain":
                errors.append(f"{relative} repository drifted")

            source_status = observed.get("source_status")
            canonical_source_commit = observed.get("canonical_source_commit")
            candidate_source_head = observed.get("candidate_source_head")
            source_pr = observed.get("source_pr")
            if source_status == "CANONICAL":
                if not _is_sha40(canonical_source_commit):
                    errors.append(f"{relative} canonical source requires 40-hex canonical_source_commit")
                if candidate_source_head is not None or source_pr is not None:
                    errors.append(f"{relative} canonical source cannot also claim candidate source identity")
            elif source_status == "CANDIDATE_NONCANONICAL":
                if canonical_source_commit is not None:
                    errors.append(f"{relative} candidate source cannot claim canonical_source_commit")
                if not _is_sha40(candidate_source_head):
                    errors.append(f"{relative} candidate source requires 40-hex candidate_source_head")
                if isinstance(source_pr, bool) or not isinstance(source_pr, int) or source_pr <= 0:
                    errors.append(f"{relative} candidate source requires positive integer source_pr")
                if observed.get("source_verification_receipt") != SOURCE_POINTER_RECEIPT_PATH:
                    errors.append(f"{relative} candidate source verification receipt path drifted")
                if pointer_receipt:
                    observed_tuple = (
                        observed.get("repository"),
                        source_pr,
                        candidate_source_head,
                        observed.get("source_path"),
                        observed.get("source_git_blob"),
                    )
                    verified_tuple = (
                        pointer_receipt.get("repository"),
                        pointer_receipt.get("source_pr"),
                        pointer_receipt.get("source_head"),
                        pointer_receipt.get("source_path"),
                        pointer_receipt.get("source_git_blob"),
                    )
                    if observed_tuple != verified_tuple:
                        errors.append(f"{relative} candidate source tuple does not match verification receipt")
            else:
                errors.append(f"{relative} invalid source_status")
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
