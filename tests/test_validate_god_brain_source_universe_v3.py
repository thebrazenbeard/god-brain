from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_source_universe_v3 import (
    GAP_DOC,
    SOURCE_DOC,
    SOURCE_SPEC,
    TOOL_DOC,
    TOOL_SPEC,
    validate_source_universe_v3,
)

ROOT = Path(__file__).resolve().parents[1]

def _load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def _mutated(source_mutator=None, tool_mutator=None) -> list[str]:
    source = copy.deepcopy(_load(SOURCE_SPEC))
    tools = copy.deepcopy(_load(TOOL_SPEC))
    if source_mutator:
        source_mutator(source)
    if tool_mutator:
        tool_mutator(tools)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for relative in (SOURCE_SPEC, TOOL_SPEC, SOURCE_DOC, TOOL_DOC, GAP_DOC):
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
        (root / SOURCE_SPEC).write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
        (root / TOOL_SPEC).write_text(json.dumps(tools, indent=2) + "\n", encoding="utf-8")
        for relative in (SOURCE_DOC, TOOL_DOC, GAP_DOC):
            (root / relative).write_text((ROOT / relative).read_text(encoding="utf-8"), encoding="utf-8")
        return validate_source_universe_v3(root)

class SourceUniverseV3Tests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate_source_universe_v3(ROOT), [])

    def test_repo_count_cannot_silently_follow_stale_user_heading(self) -> None:
        errors = _mutated(lambda spec: spec.__setitem__("live_repository_count", 76))
        self.assertTrue(any("census" in error for error in errors))

    def test_unclassified_source_is_rejected(self) -> None:
        def mutate(spec):
            spec["sources"][0]["class"] = "UNCLASSIFIED"
        errors = _mutated(mutate)
        self.assertTrue(any("unclassified" in error for error in errors))

    def test_runtime_dependency_admission_ceiling_cannot_be_removed(self) -> None:
        def mutate(spec):
            spec["claim_ceiling"].remove("NO_RUNTIME_DEPENDENCY_ADMISSION")
        errors = _mutated(mutate)
        self.assertTrue(any("runtime dependency" in error for error in errors))

    def test_transfer_cannot_reference_unknown_repo(self) -> None:
        def mutate(spec):
            spec["transfer_candidates"][0]["sources"].append("not-a-repo")
        errors = _mutated(mutate)
        self.assertTrue(any("unknown source" in error for error in errors))

    def test_exact_head_must_be_40_hex(self) -> None:
        def mutate(spec):
            next(x for x in spec["sources"] if x["id"] == "ingest")["evidence_cut"]["exact_head"] = "bad"
        errors = _mutated(mutate)
        self.assertTrue(any("exact_head" in error for error in errors))

    def test_tool_namespace_cannot_become_runtime_dependency(self) -> None:
        def mutate(spec):
            next(x for x in spec["namespaces"] if x["name"] == "GitHub")["runtime_dependency"] = True
        errors = _mutated(tool_mutator=mutate)
        self.assertTrue(any("runtime_dependency" in error for error in errors))

    def test_tool_authority_invariant_cannot_be_removed(self) -> None:
        def mutate(spec):
            spec["invariants"].remove("TOOL_AVAILABILITY_NE_AUTHORITY")
        errors = _mutated(tool_mutator=mutate)
        self.assertTrue(any("tool invariants" in error for error in errors))

    def test_cricket_overlay_must_remain_review_not_authority(self) -> None:
        def mutate(spec):
            spec["installed_skill_overlays"] = []
        errors = _mutated(tool_mutator=mutate)
        self.assertTrue(any("Cricket" in error for error in errors))

    def test_private_payload_transfer_ceiling_cannot_be_removed(self) -> None:
        def mutate(spec):
            spec["claim_ceiling"].remove("NO_PRIVATE_PAYLOAD_TRANSFER")
        errors = _mutated(mutate)
        self.assertTrue(any("private payload" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
