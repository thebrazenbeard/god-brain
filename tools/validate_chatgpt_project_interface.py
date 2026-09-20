from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_FILES = {
    "CHATGPT_REPO_INTERFACE.yaml": (
        "schema_version: god-brain.chatgpt-repo-interface.v1",
        "canonical_branch: main",
        "coordination_hub: thebrazenbeard/chat-communication-bus",
        "evidence_class: HYPOTHESIS",
        "chat_conversation: REPLACEABLE_EXECUTION_SURFACE",
        "rule: FRESH_READ_MUTABLE_STATE",
        "protected_effect_authority: PATRICK_EXPLICIT_EXACT_EFFECT",
        "DELEGATED_SUBJECT_IS_BT2_OWNED_UNTIL_RETURN_OR_EXPLICIT_CANCELLATION",
    ),
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
    "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml": (
        "god_brain_coordinator:",
        "bt2_coordinator:",
        "DELEGATED_SUBJECT_IS_DELEGATE_OWNED_UNTIL_RETURN_OR_EXPLICIT_CANCELLATION",
        "exact_subject_binding_required: true",
        "repository: thebrazenbeard/chat-communication-bus",
        "require_patrick_exact_authorization: true",
    ),
    "architecture/chatgpt/PROJECT_INSTRUCTIONS.md": (
        "You are Patrick's primary God Brain Coordinator.",
        "CHATGPT_REPO_INTERFACE.yaml",
        "God Brain is not Hyperconnectome Brain renamed.",
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


def validate_project_interface(root: Path) -> list[str]:
    errors: list[str] = []
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

    manifest = root / "CHATGPT_REPO_INTERFACE.yaml"
    if manifest.is_file():
        text = manifest.read_text(encoding="utf-8")
        referenced_paths = (
            "architecture/chatgpt/BOOTSTRAP.md",
            "architecture/chatgpt/EPISTEMIC_CONTRACT.md",
            "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml",
            "architecture/chatgpt/RECOVERY_AND_CONTINUATION.md",
            "architecture/chatgpt/PROJECT_INSTRUCTIONS.md",
        )
        for relative in referenced_paths:
            if relative not in text:
                errors.append(f"manifest does not reference: {relative}")
            if not (root / relative).is_file():
                errors.append(f"manifest reference does not exist: {relative}")

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
