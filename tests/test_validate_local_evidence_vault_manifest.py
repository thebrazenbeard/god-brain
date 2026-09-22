import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_local_evidence_vault_manifest import validate_manifest


def base_manifest():
    return {
        "schema": "god-brain.local-evidence-vault-manifest.v0.1",
        "project": "unvtrslr",
        "repository": "thebrazenbeard/unvtrslr",
        "canonical_branch": "main",
        "canonical_authority": "GITHUB_MAIN",
        "source_head": "7" * 40,
        "executed_head": "8" * 40,
        "evidence_id": "example-run",
        "vault_role": "NON_CANONICAL_DURABLE_EVIDENCE_REPLICA",
        "objects": [{
            "relative_path": "predictions/result.jsonl",
            "sha256": hashlib.sha256(b"ok").hexdigest(),
            "bytes": 2,
            "sensitivity": "PUBLIC",
        }],
    }


class LocalEvidenceVaultManifestTests(unittest.TestCase):
    def test_valid_metadata_only_manifest(self):
        validate_manifest(base_manifest())

    def test_private_endpoint_field_is_rejected(self):
        manifest = base_manifest()
        manifest["host"] = "private.example"
        with self.assertRaisesRegex(ValueError, "forbidden"):
            validate_manifest(manifest)

    def test_canonical_authority_cannot_move_to_vault(self):
        manifest = base_manifest()
        manifest["canonical_authority"] = "LOCAL_NAS"
        with self.assertRaisesRegex(ValueError, "GITHUB_MAIN"):
            validate_manifest(manifest)

    def test_parent_traversal_is_rejected(self):
        manifest = base_manifest()
        manifest["objects"][0]["relative_path"] = "../escape"
        with self.assertRaisesRegex(ValueError, "unsafe"):
            validate_manifest(manifest)

    def test_root_verifies_real_bytes(self):
        manifest = base_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "predictions" / "result.jsonl"
            path.parent.mkdir()
            path.write_bytes(b"ok")
            validate_manifest(manifest, root)

    def test_root_detects_hash_mismatch(self):
        manifest = base_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "predictions" / "result.jsonl"
            path.parent.mkdir()
            path.write_bytes(b"no")
            with self.assertRaisesRegex(ValueError, "sha256 mismatch|size mismatch"):
                validate_manifest(manifest, root)


if __name__ == "__main__":
    unittest.main()
