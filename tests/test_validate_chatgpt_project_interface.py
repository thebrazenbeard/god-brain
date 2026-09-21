from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tools.validate_chatgpt_project_interface import (
    DELEGATED_IMPLEMENTATION_TOKEN,
    validate_project_interface,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
INTERFACE_FILES = (
    "CHATGPT_REPO_INTERFACE.yaml",
    "architecture/chatgpt/BOOTSTRAP.md",
    "architecture/chatgpt/EPISTEMIC_CONTRACT.md",
    "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml",
    "architecture/chatgpt/PROJECT_INSTRUCTIONS.md",
    "architecture/chatgpt/RECOVERY_AND_CONTINUATION.md",
)


def copy_interface_subject(target: Path) -> None:
    for relative in INTERFACE_FILES:
        source = REPO_ROOT / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


class ChatGPTProjectInterfaceTests(unittest.TestCase):
    def test_repository_interface_validates(self) -> None:
        self.assertEqual(validate_project_interface(REPO_ROOT), [])

    def test_missing_required_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate_project_interface(Path(tmp))
            self.assertTrue(
                any("missing required project-interface file" in error for error in errors)
            )

    def test_manifest_semantic_guard_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            manifest = root / "CHATGPT_REPO_INTERFACE.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "evidence_class: HYPOTHESIS",
                    "evidence_class: FACT",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any("thesis.evidence_class mismatch" in error for error in errors)
            )

    def test_malformed_manifest_yaml_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            manifest = root / "CHATGPT_REPO_INTERFACE.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8") + "\nmalformed: [\n",
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any(
                    "CHATGPT_REPO_INTERFACE.yaml is not valid readable YAML" in error
                    for error in errors
                )
            )

    def test_malformed_routing_yaml_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            routing = root / "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml"
            routing.write_text(
                routing.read_text(encoding="utf-8") + "\nmalformed: [\n",
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any(
                    "ROUTING_AND_DELEGATION.yaml is not valid readable YAML" in error
                    for error in errors
                )
            )

    def test_manifest_unqualified_bt2_implementation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            manifest = root / "CHATGPT_REPO_INTERFACE.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    DELEGATED_IMPLEMENTATION_TOKEN,
                    "bounded_implementation",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any("unqualified bounded_implementation" in error for error in errors)
            )

    def test_routing_unqualified_bt2_implementation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            routing = root / "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml"
            routing.write_text(
                routing.read_text(encoding="utf-8").replace(
                    DELEGATED_IMPLEMENTATION_TOKEN,
                    "bounded_implementation",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any("unqualified bounded_implementation" in error for error in errors)
            )

    def test_manifest_bt2_extra_merge_authority_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            manifest = root / "CHATGPT_REPO_INTERFACE.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "    - engineering_coordination\n",
                    "    - engineering_coordination\n    - merge_authority\n",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any(
                    "coordinator_division.bt2 unexpected" in error
                    and "merge_authority" in error
                    for error in errors
                )
            )

    def test_routing_bt2_extra_merge_authority_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            routing = root / "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml"
            routing.write_text(
                routing.read_text(encoding="utf-8").replace(
                    "      - engineering_coordination\n",
                    "      - engineering_coordination\n      - merge_authority\n",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any(
                    "roles.bt2_coordinator.owns unexpected" in error
                    and "merge_authority" in error
                    for error in errors
                )
            )

    def test_review_non_grant_cannot_drop_merge_authority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            routing = root / "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml"
            routing.write_text(
                routing.read_text(encoding="utf-8").replace(
                    "    - merge_authority\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any("review.pass_does_not_grant missing" in error for error in errors)
            )

    def test_protected_effect_class_cannot_drop_merge_main_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_interface_subject(root)
            routing = root / "architecture/chatgpt/ROUTING_AND_DELEGATION.yaml"
            routing.write_text(
                routing.read_text(encoding="utf-8").replace(
                    "    - merge_or_direct_main_mutation\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(
                any("protected_effects.classes missing" in error for error in errors)
            )

    def test_instruction_source_stays_compact(self) -> None:
        path = REPO_ROOT / "architecture/chatgpt/PROJECT_INSTRUCTIONS.md"
        self.assertLessEqual(
            len(path.read_text(encoding="utf-8").splitlines()),
            80,
        )


if __name__ == "__main__":
    unittest.main()
