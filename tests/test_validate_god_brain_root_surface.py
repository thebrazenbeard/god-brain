from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_root_surface import validate_root_surface


class GodBrainRootSurfaceTests(unittest.TestCase):
    def test_repository_root_surface_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_root_surface(root), [])

    def test_inherited_hc_current_title_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# God Brain\n", encoding="utf-8")
            (root / "CURRENT.md").write_text("# HC Brain — Current State\n", encoding="utf-8")
            errors = validate_root_surface(root)
            self.assertTrue(any("God Brain" in error or "inherited HC" in error for error in errors))

    def test_missing_literal_repo_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# God Brain\n\n- `docs/missing.md`\n", encoding="utf-8")
            (root / "CURRENT.md").write_text(
                "# God Brain — Current State\n"
                "CHECKPOINT != CURRENT_TRUTH\n"
                "REVIEWED_OLD_HEAD != REVIEWED_NEW_HEAD\n"
                "INHERITED_IMPLEMENTATION != GOD_BRAIN_QUALIFICATION\n"
                "REVIEW_PASS != MERGE_OR_DEPLOY_AUTHORITY\n",
                encoding="utf-8",
            )
            errors = validate_root_surface(root)
            self.assertTrue(any("docs/missing.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
