from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_chatgpt_project_interface import REQUIRED_FILES, validate_project_interface


class ChatGPTProjectInterfaceTests(unittest.TestCase):
    def test_repository_interface_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_project_interface(root), [])

    def test_missing_required_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            errors = validate_project_interface(root)
            self.assertTrue(any("missing required project-interface file" in error for error in errors))

    def test_missing_required_guard_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative, markers in REQUIRED_FILES.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(markers) + "\n", encoding="utf-8")

            manifest = root / "CHATGPT_REPO_INTERFACE.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "evidence_class: HYPOTHESIS", "evidence_class: FACT", 1
                ),
                encoding="utf-8",
            )
            errors = validate_project_interface(root)
            self.assertTrue(any("evidence_class: HYPOTHESIS" in error for error in errors))

    def test_instruction_source_stays_compact(self) -> None:
        root = Path(__file__).resolve().parents[1]
        path = root / "architecture/chatgpt/PROJECT_INSTRUCTIONS.md"
        self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 80)


if __name__ == "__main__":
    unittest.main()
