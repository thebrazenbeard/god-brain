#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

SCHEMA = "god-brain.local-evidence-vault-manifest.v0.1"
AUTHORITY = "GITHUB_MAIN"
VAULT_ROLE = "NON_CANONICAL_DURABLE_EVIDENCE_REPLICA"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_KEYS = {
    "private_ip", "ip", "host", "hostname", "username", "password",
    "token", "access_token", "private_key", "local_share_path",
    "local_mount_path", "endpoint", "credentials",
}


def fail(message: str) -> None:
    raise ValueError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def walk_keys(value, prefix=""):
    if isinstance(value, dict):
        for key, child in value.items():
            yield prefix + str(key)
            yield from walk_keys(child, prefix + str(key) + ".")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_keys(child, prefix + f"[{index}].")


def validate_manifest(obj: dict, root: Path | None = None) -> None:
    if obj.get("schema") != SCHEMA:
        fail("unsupported manifest schema")
    required = {
        "project", "repository", "canonical_branch", "canonical_authority",
        "source_head", "executed_head", "evidence_id", "vault_role", "objects",
    }
    missing = sorted(required - set(obj))
    if missing:
        fail(f"missing required fields: {missing}")
    if obj["canonical_authority"] != AUTHORITY:
        fail("canonical_authority must remain GITHUB_MAIN")
    if obj["vault_role"] != VAULT_ROLE:
        fail("vault_role must remain non-canonical")
    if obj["canonical_branch"] != "main":
        fail("canonical_branch must be main")
    if "/" not in str(obj["repository"]):
        fail("repository must be owner/name")
    if not SHA40.fullmatch(str(obj["source_head"])):
        fail("source_head must be a 40-character Git SHA")
    if not SHA40.fullmatch(str(obj["executed_head"])):
        fail("executed_head must be a 40-character Git SHA")
    if not str(obj["project"]) or not str(obj["evidence_id"]):
        fail("project and evidence_id must be nonempty")

    forbidden = sorted({
        key.split(".")[-1]
        for key in walk_keys(obj)
        if key.split(".")[-1] in FORBIDDEN_KEYS
    })
    if forbidden:
        fail(f"public manifest contains forbidden local/private fields: {forbidden}")

    objects = obj["objects"]
    if not isinstance(objects, list) or not objects:
        fail("objects must be a nonempty list")

    seen = set()
    for index, item in enumerate(objects):
        if not isinstance(item, dict):
            fail(f"objects[{index}] must be an object")
        for key in ("relative_path", "sha256", "bytes", "sensitivity"):
            if key not in item:
                fail(f"objects[{index}] missing {key}")
        path_text = str(item["relative_path"])
        path = PurePosixPath(path_text)
        if path.is_absolute() or ".." in path.parts or path_text in ("", "."):
            fail(f"objects[{index}] relative_path is unsafe")
        if path_text in seen:
            fail(f"duplicate object path: {path_text}")
        seen.add(path_text)
        if not SHA256.fullmatch(str(item["sha256"])):
            fail(f"objects[{index}] sha256 is invalid")
        size = item["bytes"]
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            fail(f"objects[{index}] bytes must be a nonnegative integer")
        if item["sensitivity"] not in {"PUBLIC", "PRIVATE", "RESTRICTED"}:
            fail(f"objects[{index}] sensitivity is invalid")

        if root is not None:
            candidate = root.joinpath(*path.parts)
            if not candidate.is_file():
                fail(f"missing vaulted object: {path_text}")
            if candidate.stat().st_size != size:
                fail(f"size mismatch for {path_text}")
            if sha256_file(candidate) != item["sha256"]:
                fail(f"sha256 mismatch for {path_text}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--root")
    args = parser.parse_args()
    manifest_path = Path(args.manifest)
    obj = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest(obj, Path(args.root) if args.root else None)
    print("LOCAL_EVIDENCE_VAULT_MANIFEST_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
