from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_project_file_architecture import (
    DOC_PATH,
    SPEC_PATH,
    validate_project_file_architecture,
)


class GodBrainProjectFileArchitectureTests(unittest.TestCase):
    def test_repository_research_contract_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_project_file_architecture(root), [])

    def test_current_pointer_cannot_admit_live_pr_state(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / "docs/research").mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            future = mutated["future_current_pointer_contract"]
            future["forbidden_fields"].remove("open_pull_requests")
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_project_file_architecture(target)
            self.assertTrue(any("open_pull_requests" in error for error in errors))

    def test_research_claim_ceiling_cannot_be_dropped(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / "docs/research").mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["claim_ceiling"].remove("NO_CANONICAL_PROMOTION")
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_project_file_architecture(target)
            self.assertTrue(any("NO_CANONICAL_PROMOTION" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
