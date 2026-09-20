from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


REQUIRED_FILES = {
    "architecture/chatgpt/BOOTSTRAP.md": (
        "A ChatGPT conversation is an execution terminal",
        "Fresh-read",
        "Chat Communication Bus",
        "CHECKPOINT != CURRENT_TRUTH",
        "REVIEWED_OLD_HEAD != REVIEWED_NEW_HEAD",
        "Do not stop after orientation",
    ),
    "architecture/chatgpt/EPISTEMIC_CONTRACT.md": (
        "SIMULATION_HYPOTHESIS != SIMULATION_FACT",
        "ANOMALY != CONTACT",
        "AI_OUTPUT != EXTERNAL_MESSAGE",
        "UNEXPLAINED != SUPERNATURAL",
        "SELF_MODEL != CONSCIOUSNESS",
        "COMPLEX_BEHAVIOR != PERSONHOOD",
        "COPIED_LINEAGE != INDEPENDENT_CORROBORATION",
    ),
    "architecture/chatgpt/PROJECT_INSTRUCTIONS.md": (
        "You are Patrick's primary God Brain Coordinator.",
        "CHATGPT_REPO_INTERFACE.yaml",
        "God Brain is not Hyperconnectome Brain renamed.",
        "bounded implementation explicitly delegated to BT2",
        "Without Patrick's explicit authorization for the exact effect",
        "do not stop at orientation",
    ),
    "architecture/chatgpt/RECOVERY_AND_CONTINUATION.md": (
        "A continuation artifact exists to reduce reconstruction cost.",
        "starting snapshot, not current truth",
        "CHAT_CONTINUATION != PROJECT_MEMORY",
        "CHECKPOINT != CANON",
    ),
}

MANIFEST_PATH = "CHATGPT_REPO_INTERFACE.yaml"
ROUTING_PATH = "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml"
DELEGATED_IMPLEMENTATION_TOKEN = "bounded_implementation_explicitly_delegated_to_bt2"


def _load_yaml_mapping(path: Path, relative: str, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing required project-interface file: {relative}")
        return None
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"{relative} is not valid readable YAML: {exc.__class__.__name__}")
        return None
    if type(value) is not dict:
        errors.append(f"{relative} must contain one YAML mapping")
        return None
    return value


def _expect_equal(
    value: Any,
    expected: Any,
    *,
    relative: str,
    field: str,
    errors: list[str],
) -> None:
    if value != expected:
        errors.append(f"{relative} field {field} mismatch: expected {expected!r}")


def _expect_list_contains(
    value: Any,
    required: str,
    *,
    relative: str,
    field: str,
    errors: list[str],
) -> None:
    if type(value) is not list or required not in value:
        errors.append(f"{relative} field {field} must contain {required}")


def _get(mapping: dict[str, Any], *path: str) -> Any:
    current: Any = mapping
    for key in path:
        if type(current) is not dict or key not in current:
            return None
        current = current[key]
    return current


def _validate_manifest(manifest: dict[str, Any], root: Path, errors: list[str]) -> None:
    relative = MANIFEST_PATH
    checks = (
        (("schema_version",), "god-brain.chatgpt-repo-interface.v1"),
        (("canonical_branch",), "main"),
        (("coordination_hub",), "thebrazenbeard/chat-communication-bus"),
        (("thesis", "evidence_class"), "HYPOTHESIS"),
        (("canonical_state", "chat_conversation"), "REPLACEABLE_EXECUTION_SURFACE"),
        (("freshness", "rule"), "FRESH_READ_MUTABLE_STATE"),
        (("authority", "protected_effect_authority"), "PATRICK_EXPLICIT_EXACT_EFFECT"),
        (
            ("collision_control", "invariant"),
            "DELEGATED_SUBJECT_IS_BT2_OWNED_UNTIL_RETURN_OR_EXPLICIT_CANCELLATION",
        ),
    )
    for field_path, expected in checks:
        _expect_equal(
            _get(manifest, *field_path),
            expected,
            relative=relative,
            field=".".join(field_path),
            errors=errors,
        )

    bt2 = _get(manifest, "coordinator_division", "bt2")
    _expect_list_contains(
        bt2,
        DELEGATED_IMPLEMENTATION_TOKEN,
        relative=relative,
        field="coordinator_division.bt2",
        errors=errors,
    )
    if type(bt2) is list and "bounded_implementation" in bt2:
        errors.append(
            f"{relative} field coordinator_division.bt2 contains unqualified bounded_implementation"
        )

    bootstrap = _get(manifest, "bootstrap")
    expected_refs = {
        "procedure": "architecture/chatgpt/BOOTSTRAP.md",
        "epistemic_contract": "architecture/chatgpt/EPISTEMIC_CONTRACT.md",
        "routing_and_delegation": ROUTING_PATH,
        "recovery_contract": "architecture/chatgpt/RECOVERY_AND_CONTINUATION.md",
        "project_instruction_source": "architecture/chatgpt/PROJECT_INSTRUCTIONS.md",
    }
    if type(bootstrap) is not dict:
        errors.append(f"{relative} field bootstrap must be a mapping")
    else:
        for key, expected in expected_refs.items():
            _expect_equal(
                bootstrap.get(key),
                expected,
                relative=relative,
                field=f"bootstrap.{key}",
                errors=errors,
            )
            if not (root / expected).is_file():
                errors.append(f"manifest reference does not exist: {expected}")


def _validate_routing(routing: dict[str, Any], errors: list[str]) -> None:
    relative = ROUTING_PATH
    checks = (
        (("schema_version",), "god-brain.routing-and-delegation.v1"),
        (
            ("delegation", "ownership_rule"),
            "DELEGATED_SUBJECT_IS_DELEGATE_OWNED_UNTIL_RETURN_OR_EXPLICIT_CANCELLATION",
        ),
        (("review", "exact_subject_binding_required"), True),
        (("bus", "repository"), "thebrazenbeard/chat-communication-bus"),
        (("protected_effects", "require_patrick_exact_authorization"), True),
    )
    for field_path, expected in checks:
        _expect_equal(
            _get(routing, *field_path),
            expected,
            relative=relative,
            field=".".join(field_path),
            errors=errors,
        )

    owns = _get(routing, "roles", "bt2_coordinator", "owns")
    _expect_list_contains(
        owns,
        DELEGATED_IMPLEMENTATION_TOKEN,
        relative=relative,
        field="roles.bt2_coordinator.owns",
        errors=errors,
    )
    if type(owns) is list and "bounded_implementation" in owns:
        errors.append(
            f"{relative} field roles.bt2_coordinator.owns contains unqualified bounded_implementation"
        )

    required_binding = _get(routing, "delegation", "required_binding")
    for item in (
        "repository",
        "starting_ref_or_exact_head",
        "exact_files_or_semantic_subject",
        "task",
        "allowed_effects",
        "prohibited_effects",
        "required_evidence",
        "return_format",
    ):
        _expect_list_contains(
            required_binding,
            item,
            relative=relative,
            field="delegation.required_binding",
            errors=errors,
        )


def validate_project_interface(root: Path) -> list[str]:
    errors: list[str] = []

    manifest = _load_yaml_mapping(root / MANIFEST_PATH, MANIFEST_PATH, errors)
    routing = _load_yaml_mapping(root / ROUTING_PATH, ROUTING_PATH, errors)
    if manifest is not None:
        _validate_manifest(manifest, root, errors)
    if routing is not None:
        _validate_routing(routing, errors)

    for relative, markers in REQUIRED_FILES.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required project-interface file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative} missing required marker: {marker}")

    instruction_path = root / "architecture/chatgpt/PROJECT_INSTRUCTIONS.md"
    if instruction_path.is_file():
        line_count = len(instruction_path.read_text(encoding="utf-8").splitlines())
        if line_count > 80:
            errors.append(
                "architecture/chatgpt/PROJECT_INSTRUCTIONS.md exceeds 80 lines; "
                "move detailed operating rules into referenced contracts"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    errors = validate_project_interface(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("God Brain ChatGPT project interface: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
