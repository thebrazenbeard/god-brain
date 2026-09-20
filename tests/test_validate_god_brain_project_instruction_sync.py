from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_project_instruction_sync import (
    DOC_PATH,
    SPEC_PATH,
    validate_project_instruction_sync,
)


class GodBrainProjectInstructionSyncTests(unittest.TestCase):
    def test_repository_research_contract_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_project_instruction_sync(root), [])

    def test_source_file_alone_cannot_prove_installation(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["bootstrap_rule"]["source_file_alone_proves_installation"] = True
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_project_instruction_sync(target)
            self.assertTrue(any("must not prove installation" in error for error in errors))

    def test_installation_must_remain_protected_effect(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["effect_boundary"]["project_instruction_install_or_replace"] = "AUTOMATIC"
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_project_instruction_sync(target)
            self.assertTrue(any("protected external configuration effect" in error for error in errors))

    def test_receipt_cannot_claim_chat_consumption(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["receipt"]["required_claim_ceiling"] = []
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_project_instruction_sync(target)
            self.assertTrue(any("chat consumption" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
