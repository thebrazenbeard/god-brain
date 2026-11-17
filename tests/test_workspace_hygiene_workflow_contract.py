"""Ensure the automatic-task gate does not execute untrusted PR code."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "workspace-autotask-hygiene.yml"


class WorkspaceWorkflowContractTests(unittest.TestCase):
    def test_trusted_base_validator_runs_against_candidate_only_as_data(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("pull_request_target:", source)
        self.assertIn("ref: ${{ github.event.pull_request.base.sha || github.sha }}", source)
        self.assertIn("ref: ${{ github.event.pull_request.head.sha || github.sha }}", source)
        self.assertIn("python3 guard/tools/validate_workspace_hygiene.py --root candidate", source)
        self.assertEqual(source.count("persist-credentials: false"), 2)
        self.assertNotIn("python3 candidate/", source)


if __name__ == "__main__":
    unittest.main()
