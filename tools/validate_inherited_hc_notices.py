from __future__ import annotations

from pathlib import Path

NOTICE = "God Brain provenance notice:"
REQUIRED = (
    "inherited Hyperconnectome Brain source-lineage material",
    "do **not** govern God Brain",
    "`CURRENT.md`",
    "`README.md`",
    "preserved as lineage evidence",
)
SUBJECTS = ("WARDEN.md", "docs/REPOSITORY_MAP.md")


def validate_inherited_hc_notices(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in SUBJECTS:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing inherited subject: {relative}")
            continue
        prefix = "\n".join(path.read_text(encoding="utf-8").splitlines()[:14])
        if NOTICE not in prefix:
            errors.append(f"{relative} missing God Brain provenance notice near file start")
        for marker in REQUIRED:
            if marker not in prefix:
                errors.append(f"{relative} provenance notice missing marker: {marker}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_inherited_hc_notices(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Inherited HC authority notices: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
