from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_inherited_hc_notices import validate_inherited_hc_notices


class InheritedHcNoticeTests(unittest.TestCase):
    def test_repository_notices_validate(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_inherited_hc_notices(root), [])

    def test_missing_notice_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "WARDEN.md").write_text("# Noëtarch — Warden of the Hyperconnectome\n", encoding="utf-8")
            (root / "docs" / "REPOSITORY_MAP.md").write_text("# Hyperconnectome Brain Repository Map\n", encoding="utf-8")
            errors = validate_inherited_hc_notices(root)
            self.assertTrue(any("missing God Brain provenance notice" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
