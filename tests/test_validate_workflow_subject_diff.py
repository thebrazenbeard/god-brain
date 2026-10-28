"""Offline first-branch push regressions for the exact-subject diff guard."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "tools" / "validate_workflow_subject_diff.py"
ZERO = "0" * 40


def git(directory: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(directory), *args],
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()


class WorkflowSubjectDiffTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.source.mkdir()
        git(self.source, "init", "-b", "main")
        git(self.source, "config", "user.name", "Fixture")
        git(self.source, "config", "user.email", "fixture@example.invalid")
        (self.source / "base.py").write_text("baseline = True\n", encoding="utf-8")
        git(self.source, "add", "base.py")
        git(self.source, "commit", "-m", "base")
        self.main_sha = git(self.source, "rev-parse", "HEAD")

    def checkout_subject(self, content: str, *, orphan: bool = False) -> str:
        if orphan:
            git(self.source, "checkout", "--orphan", "feature")
        else:
            git(self.source, "checkout", "-b", "feature")
        (self.source / "feature.py").write_text(content, encoding="utf-8")
        git(self.source, "add", "-A")
        git(self.source, "commit", "-m", "feature")
        self.head_sha = git(self.source, "rev-parse", "HEAD")
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", "feature",
             self.source.as_uri(), str(self.root / "repo")],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(git(self.root / "repo", "rev-parse", "--is-shallow-repository"), "true")
        return self.head_sha

    def run_guard(self, *, before: str = ZERO, head: str | None = None):
        env = dict(os.environ, HEAD_SHA=head or self.head_sha,
                   BASE_SHA=before, DEFAULT_BRANCH="main")
        return subprocess.run([sys.executable, str(GUARD)], cwd=self.root,
                              env=env, capture_output=True, text=True)

    def test_first_default_branch_push_never_self_diffs(self):
        # `before=000...` can also describe the initial creation of `main`.
        # There is no meaningful existing branch tip, and fetching `main`
        # returns the *same* commit as HEAD. That must not yield a green diff.
        self.head_sha = self.main_sha
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", "main",
             self.source.as_uri(), str(self.root / "repo")],
            capture_output=True, text=True, check=True,
        )
        result = self.run_guard()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no distinct default-branch baseline", result.stderr)

    def test_empty_new_feature_branch_is_conservatively_refused(self):
        # The same self-diff would occur on a new feature branch with no
        # commits yet. Refusal is intentional; it asserts no false evidence.
        git(self.source, "checkout", "-b", "feature")
        self.head_sha = self.main_sha
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", "feature",
             self.source.as_uri(), str(self.root / "repo")],
            capture_output=True, text=True, check=True,
        )
        result = self.run_guard()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no distinct default-branch baseline", result.stderr)

    def test_new_branch_clean_diff_uses_merge_base_and_passes(self):
        self.checkout_subject("feature = 1\n")
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["mode"], "new_branch_merge_base")
        self.assertEqual(parsed["baseline_sha"], self.main_sha)
        self.assertEqual(parsed["observed_default_sha"], self.main_sha)
        self.assertEqual(parsed["status"], "PASS")

    def test_new_branch_whitespace_error_still_refused(self):
        self.checkout_subject("feature = 1 \n")
        result = self.run_guard()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REFUSED", result.stderr)
        self.assertIn("trailing whitespace", result.stderr)

    def test_regular_push_keeps_exact_before_sha(self):
        self.checkout_subject("feature = 1\n")
        result = self.run_guard(before=self.main_sha)
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["mode"], "event_before_sha")
        self.assertEqual(parsed["baseline_sha"], self.main_sha)

    def test_regular_push_whitespace_error_still_refused(self):
        self.checkout_subject("feature = 1 \n")
        result = self.run_guard(before=self.main_sha)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("trailing whitespace", result.stderr)

    def test_first_branch_with_unrelated_history_refused(self):
        self.checkout_subject("independent = True\n", orphan=True)
        result = self.run_guard()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("merge-base", result.stderr)

    def test_subject_mismatch_refused(self):
        self.checkout_subject("feature = 1\n")
        result = self.run_guard(head="f" * 40)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checked-out HEAD differs", result.stderr)

    def test_invalid_before_sha_refused(self):
        self.checkout_subject("feature = 1\n")
        result = self.run_guard(before="main")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("full lowercase Git SHAs", result.stderr)

    def test_all_four_workflows_use_checked_guard(self):
        workflows = ["repository-hygiene.yml", "anomaly-contact-protocol-research.yml",
                     "driftguard-source-admission-research.yml",
                     "inherited-hc-provenance-notices.yml"]
        for filename in workflows:
            with self.subTest(filename=filename):
                content = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
                self.assertIn("DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}", content)
                self.assertIn("run: python3 repo/tools/validate_workflow_subject_diff.py", content)
                self.assertNotIn('git -C repo fetch --no-tags --depth=1 origin "${BASE_SHA}"', content)


if __name__ == "__main__":
    unittest.main()
