from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_github_workflow_supply_chain import validate_workflow_supply_chain


class WorkflowSupplyChainTests(unittest.TestCase):
    def _root(self, text: str) -> tuple[tempfile.TemporaryDirectory, Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        workflows = root / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "test.yml").write_text(text, encoding="utf-8")
        return tmp, root

    def test_repository_workflows_are_immutable_ref_clean(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_workflow_supply_chain(root), [])

    def test_floating_major_tag_is_rejected(self) -> None:
        tmp, root = self._root("steps:\n  - uses: actions/checkout@v4\n")
        try:
            errors = validate_workflow_supply_chain(root)
            self.assertTrue(any("40-hex" in error for error in errors))
        finally:
            tmp.cleanup()

    def test_full_commit_sha_is_allowed(self) -> None:
        tmp, root = self._root("steps:\n  - uses: owner/action@0123456789abcdef0123456789abcdef01234567\n")
        try:
            self.assertEqual(validate_workflow_supply_chain(root), [])
        finally:
            tmp.cleanup()

    def test_local_action_is_allowed(self) -> None:
        tmp, root = self._root("steps:\n  - uses: ./.github/actions/local\n")
        try:
            self.assertEqual(validate_workflow_supply_chain(root), [])
        finally:
            tmp.cleanup()

    def test_mutable_docker_tag_is_rejected(self) -> None:
        tmp, root = self._root("steps:\n  - uses: docker://python:3.11\n")
        try:
            errors = validate_workflow_supply_chain(root)
            self.assertTrue(any("sha256" in error for error in errors))
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
