#!/usr/bin/env python3
"""Check whitespace against a source-bound workflow subject and its baseline.

On branch creation GitHub emits an all-zero ``before`` SHA, which is not a
Git object. In that case a full-history merge-base against the observed
default-branch tip is the narrowest available baseline. An unrelated history
or unavailable ref is a hard failure, never an implicit green result.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys


ZERO_SHA = "0" * 40
_SHA = re.compile(r"[0-9a-f]{40}\Z")
_BRANCH = re.compile(r"[A-Za-z0-9._/-]+\Z")


class SubjectDiffError(Exception):
    pass


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        diagnostic = (result.stderr or result.stdout).strip().splitlines()
        reason = diagnostic[0][:240] if diagnostic else "Git command failed"
        raise SubjectDiffError(f"git {args[0]} failed ({result.returncode}): {reason}")
    return result.stdout.strip()


def validate(repo: Path, head: str, before: str, default_branch: str) -> dict[str, str]:
    if not _SHA.fullmatch(head) or not _SHA.fullmatch(before):
        raise SubjectDiffError("head and before must be full lowercase Git SHAs")
    if (not _BRANCH.fullmatch(default_branch) or default_branch.startswith("-")
            or ".." in default_branch or "//" in default_branch):
        raise SubjectDiffError("invalid default branch name")

    actual_head = _git(repo, "rev-parse", "HEAD")
    if actual_head != head:
        raise SubjectDiffError("checked-out HEAD differs from the event subject")

    if before == ZERO_SHA:
        # A first-branch push has no preceding branch tip. Compare the entire
        # branch delta from its common ancestor with the observed default ref.
        # Never compare against the empty tree: it would reinterpret thousands
        # of already-existing hard Markdown breaks as newly introduced errors.
        if _git(repo, "rev-parse", "--is-shallow-repository") == "true":
            _git(repo, "fetch", "--no-tags", "--unshallow", "origin")
        _git(repo, "fetch", "--no-tags", "origin", f"refs/heads/{default_branch}")
        observed_default = _git(repo, "rev-parse", "FETCH_HEAD")
        if observed_default == head:
            # On the first push that creates the default branch, this would
            # silently compare HEAD to itself and miss every new line. A new
            # branch pointing at the unchanged default tip is also refused:
            # absent an event-supplied predecessor we cannot distinguish it
            # from a newly established root/default source boundary.
            raise SubjectDiffError("all-zero before has no distinct default-branch baseline")
        baseline = _git(repo, "merge-base", head, observed_default)
        mode = "new_branch_merge_base"
    else:
        _git(repo, "fetch", "--no-tags", "--depth=1", "origin", before)
        baseline = before
        observed_default = ""
        mode = "event_before_sha"

    # Git itself defines the whitespace errors and exit status. A nonzero
    # return cannot be reinterpreted as clean by callers.
    _git(repo, "diff", "--check", f"{baseline}..{head}")
    return {"mode": mode, "head_sha": head, "baseline_sha": baseline,
            "observed_default_sha": observed_default, "status": "PASS"}


def main() -> int:
    try:
        result = validate(Path("repo"), os.environ.get("HEAD_SHA", ""),
                          os.environ.get("BASE_SHA", ""),
                          os.environ.get("DEFAULT_BRANCH", ""))
    except SubjectDiffError as exc:
        print(f"workflow subject diff REFUSED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
