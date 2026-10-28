from __future__ import annotations

import argparse
import re
from pathlib import Path

# YAML permits whitespace before the mapping colon, quoted mapping keys,
# and flow mappings ("{name: x, uses: owner/action@ref}").  All three are
# valid `uses` keys and must receive the same immutable-ref check.
# This is a deliberately bounded line scanner, not a full YAML parser.
USES_RE = re.compile(r"(?:^|[{,])\s*-?\s*(?:uses|'uses'|\"uses\")\s*:\s*([^\s#,}]+)")
COMMIT_REF_RE = re.compile(r"^[0-9a-fA-F]{40}$")
DOCKER_DIGEST_RE = re.compile(r"^docker://.+@sha256:[0-9a-fA-F]{64}$")


def validate_workflow_supply_chain(root: Path) -> list[str]:
    errors: list[str] = []
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        return [".github/workflows is missing"]

    for path in sorted([*workflows.glob("*.yml"), *workflows.glob("*.yaml")]):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for match in USES_RE.finditer(line):
                target = match.group(1)
                if target.startswith("./"):
                    continue
                if target.startswith("docker://"):
                    if not DOCKER_DIGEST_RE.fullmatch(target):
                        errors.append(f"{path.relative_to(root)}:{lineno}: docker action must use sha256 digest: {target}")
                    continue
                if "@" not in target:
                    errors.append(f"{path.relative_to(root)}:{lineno}: external action missing immutable ref: {target}")
                    continue
                action, ref = target.rsplit("@", 1)
                if not action or not COMMIT_REF_RE.fullmatch(ref):
                    errors.append(f"{path.relative_to(root)}:{lineno}: external action ref must be full 40-hex commit SHA: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_workflow_supply_chain(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("GitHub workflow supply-chain policy: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
