from __future__ import annotations

import re
from pathlib import Path

ROOT_PATH_RE = re.compile(r"`((?:docs|specs|runtime|tools|tests)/[^`]+)`")


def _literal_repo_paths(markdown: str) -> list[str]:
    return [match.strip() for match in ROOT_PATH_RE.findall(markdown)]


def validate_root_surface(root: Path) -> list[str]:
    errors: list[str] = []
    readme_path = root / "README.md"
    current_path = root / "CURRENT.md"

    if not readme_path.is_file():
        errors.append("README.md is missing")
        return errors
    if not current_path.is_file():
        errors.append("CURRENT.md is missing")
        return errors

    readme = readme_path.read_text(encoding="utf-8")
    current = current_path.read_text(encoding="utf-8")

    if not current.startswith("# God Brain — Current State\n"):
        errors.append("CURRENT.md must identify God Brain, not an inherited project, as the current-state subject")

    inherited_title = "# HC Brain — Current State"
    if inherited_title in current:
        errors.append("CURRENT.md contains the inherited HC current-state title")

    required_boundaries = (
        "CHECKPOINT != CURRENT_TRUTH",
        "REVIEWED_OLD_HEAD != REVIEWED_NEW_HEAD",
        "INHERITED_IMPLEMENTATION != GOD_BRAIN_QUALIFICATION",
        "REVIEW_PASS != MERGE_OR_DEPLOY_AUTHORITY",
    )
    for boundary in required_boundaries:
        if boundary not in current:
            errors.append(f"CURRENT.md missing currentness boundary: {boundary}")

    for source_name, document in (("README.md", readme), ("CURRENT.md", current)):
        for rel in _literal_repo_paths(document):
            candidate = root / rel.rstrip("/")
            if not candidate.exists():
                errors.append(f"{source_name} references repository path missing from this tree: {rel}")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_root_surface(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("God Brain root surface: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
