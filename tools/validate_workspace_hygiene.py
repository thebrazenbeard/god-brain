"""Read-only, source-only checks against editor auto-execution and fake font assets.

Designed to run from a *trusted* checkout against an untrusted candidate directory.
Never import, execute, or fetch from candidate source. This is not a malware scanner.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


SFNT_HEADERS = (b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1", b"ttcf")
MAX_JSON_BYTES = 1024 * 1024


def _json(path: Path, errors: list[str], root: Path):
    name = path.relative_to(root).as_posix()
    if path.is_symlink() or path.parent.is_symlink() or not path.is_file():
        errors.append(f"{name}: missing file or unsafe symlink")
        return None
    try:
        if path.stat().st_size > MAX_JSON_BYTES:
            raise ValueError("over maximum JSON size")
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"{name}: invalid JSON ({type(exc).__name__})")
        return None


def _dict_nodes(data):
    if isinstance(data, dict):
        yield data
        for value in data.values():
            yield from _dict_nodes(value)
    elif isinstance(data, list):
        for item in data:
            yield from _dict_nodes(item)


def validate_workspace(root: Path) -> list[str]:
    root = Path(root).resolve()
    errors: list[str] = []
    settings_path = root / ".vscode" / "settings.json"
    settings = _json(settings_path, errors, root)
    if not isinstance(settings, dict) or settings.get("task.allowAutomaticTasks") != "off":
        errors.append(".vscode/settings.json: task.allowAutomaticTasks must be off")

    config_paths = [root / ".vscode" / "tasks.json", *sorted(root.glob("*.code-workspace"))]
    for path in config_paths:
        if path.name == "tasks.json" and not path.exists() and not path.is_symlink():
            continue
        config = _json(path, errors, root)
        if config is None:
            continue
        for node in _dict_nodes(config):
            if node.get("runOn") == "folderOpen":
                errors.append(f"{path.relative_to(root).as_posix()}: folderOpen task forbidden")
            if (path.suffix == ".code-workspace" and "task.allowAutomaticTasks" in node
                    and node["task.allowAutomaticTasks"] != "off"):
                errors.append(f"{path.name}: auto task override forbidden")

    public = root / "public"
    if public.is_symlink():
        errors.append("public: unsafe symlink")
    elif public.is_dir():
        for path in sorted(public.rglob("*")):
            if path.suffix.lower() != ".ttf":
                continue
            name = path.relative_to(root).as_posix()
            if path.is_symlink() or not path.is_file():
                errors.append(f"{name}: invalid font entry")
                continue
            try:
                with path.open("rb") as fp:
                    magic = fp.read(4)
            except OSError:
                errors.append(f"{name}: unreadable font")
                continue
            if magic not in SFNT_HEADERS:
                errors.append(f"{name}: font header not recognized (no payload evaluated)")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    errors = validate_workspace(args.root)
    for error in errors:
        print("REFUSED:", error)
    if errors:
        return 1
    print("Workspace source-only hygiene: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
