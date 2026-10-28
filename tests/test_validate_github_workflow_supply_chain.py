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

    def test_floating_tag_with_valid_yaml_spacing_is_rejected(self) -> None:
        tmp, root = self._root("steps:\n  - uses : actions/checkout@v4\n")
        try:
            errors = validate_workflow_supply_chain(root)
            self.assertTrue(any("40-hex" in error for error in errors))
        finally:
            tmp.cleanup()

    def test_floating_tag_with_quoted_yaml_key_is_rejected(self) -> None:
        for quote in ("'", '"'):
            with self.subTest(quote=quote):
                tmp, root = self._root(f"steps:\n  - {quote}uses{quote}: actions/checkout@v4\n")
                try:
                    errors = validate_workflow_supply_chain(root)
                    self.assertTrue(any("40-hex" in error for error in errors))
                finally:
                    tmp.cleanup()

    def test_floating_tag_in_valid_yaml_flow_mapping_is_rejected(self) -> None:
        cases = (
            "steps:\n  - {uses: actions/checkout@v4}\n",
            "steps:\n  - {name: checkout, uses: actions/checkout@v4}\n",
            'steps:\n  - {name: checkout, "uses" : actions/checkout@v4}\n',
        )
        for workflow in cases:
            with self.subTest(workflow=workflow):
                tmp, root = self._root(workflow)
                try:
                    errors = validate_workflow_supply_chain(root)
                    self.assertTrue(any("40-hex" in error for error in errors))
                finally:
                    tmp.cleanup()

    def test_full_sha_in_yaml_flow_mapping_is_allowed(self) -> None:
        tmp, root = self._root(
            "steps:\n"
            "  - {name: checkout, uses: owner/action@0123456789abcdef0123456789abcdef01234567}\n"
        )
        try:
            self.assertEqual(validate_workflow_supply_chain(root), [])
        finally:
            tmp.cleanup()

    def test_checks_every_action_key_in_one_flow_mapping_line(self) -> None:
        tmp, root = self._root(
            "steps:\n"
            "  - {uses: owner/action@0123456789abcdef0123456789abcdef01234567, uses: actions/checkout@v4}\n"
        )
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
