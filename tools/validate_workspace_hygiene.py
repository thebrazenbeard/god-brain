"""Read-only, source-only checks against editor auto-execution and fake font assets.

Designed to run from a *trusted* checkout against an untrusted candidate directory.
Never import, execute, or fetch from candidate source. This is not a malware scanner.
"""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


SFNT_HEADERS = (b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1")
MAX_JSON_BYTES = 1024 * 1024
MAX_FONT_TABLES = 256
MAX_COLLECTION_FONTS = 256
COMMON_FONT_TABLES = frozenset({b"OS/2", b"cmap", b"head", b"hhea",
                                b"hmtx", b"maxp", b"name", b"post"})


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


def _sfnt_directory_is_bounded(fp, file_size: int, header_offset: int) -> bool:
    """Bounded SFNT table-directory check; not a full font-format verifier."""
    if header_offset < 0 or header_offset + 12 > file_size:
        return False
    fp.seek(header_offset)
    header = fp.read(12)
    if len(header) != 12 or header[:4] not in SFNT_HEADERS:
        return False
    table_count = struct.unpack_from(">H", header, 4)[0]
    if not (1 <= table_count <= MAX_FONT_TABLES):
        return False
    if header_offset + 12 + table_count * 16 > file_size:
        return False
    directory = fp.read(table_count * 16)
    if len(directory) != table_count * 16:
        return False
    tags = set()
    table_lengths = {}
    for index in range(table_count):
        tag, _, offset, length = struct.unpack_from(">4sIII", directory, index * 16)
        if tag in tags or any(c < 32 or c > 126 for c in tag):
            return False
        tags.add(tag)
        table_lengths[tag] = length
        if offset % 4 != 0 or offset > file_size or length > file_size - offset:
            return False
    if header[:4] in (b"\x00\x01\x00\x00", b"OTTO"):
        if any(table_lengths.get(tag, 0) == 0 for tag in COMMON_FONT_TABLES):
            return False
        if header[:4] == b"OTTO":
            if not (table_lengths.get(b"CFF ", 0) or table_lengths.get(b"CFF2", 0)):
                return False
        elif not (table_lengths.get(b"glyf", 0) and table_lengths.get(b"loca", 0)):
            return False
    return True


def _font_directory_is_bounded(path: Path) -> bool:
    """Inspect bytes as inert data, reading only bounded headers/directories."""
    with path.open("rb") as fp:
        fp.seek(0, 2)
        file_size = fp.tell()
        fp.seek(0)
        magic = fp.read(4)
        if magic == b"ttcf":
            fp.seek(0)
            header = fp.read(12)
            if len(header) != 12:
                return False
            _, version, count = struct.unpack(">4sII", header)
            if version not in (0x00010000, 0x00020000):
                return False
            if not (1 <= count <= MAX_COLLECTION_FONTS):
                return False
            if 12 + 4 * count > file_size:
                return False
            offsets = fp.read(4 * count)
            if len(offsets) != 4 * count:
                return False
            positions = struct.unpack(f">{count}I", offsets)
            # A TTC table's offsets refer to the start of the TTC file.
            return all(_sfnt_directory_is_bounded(fp, file_size, pos)
                       for pos in positions)
        return _sfnt_directory_is_bounded(fp, file_size, 0)


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
            name = path.relative_to(root).as_posix()
            if path.is_symlink():
                errors.append(f"{name}: unsafe public symlink")
                continue
            if path.suffix.lower() != ".ttf":
                continue
            if not path.is_file():
                errors.append(f"{name}: invalid font entry")
                continue
            try:
                valid_directory = _font_directory_is_bounded(path)
            except (OSError, ValueError, struct.error):
                errors.append(f"{name}: unreadable font")
                continue
            if not valid_directory:
                errors.append(f"{name}: font table directory invalid (no payload evaluated)")
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
