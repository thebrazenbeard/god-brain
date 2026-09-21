from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_integration_readiness_v0_2 import (
    DOC_PATH,
    SPEC_PATH,
    validate_integration_readiness,
)

ROOT = Path(__file__).resolve().parents[1]


def _load() -> dict:
    return json.loads((ROOT / SPEC_PATH).read_text(encoding="utf-8"))


def _mutated(mutator) -> list[str]:
    spec = copy.deepcopy(_load())
    mutator(spec)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for relative in (DOC_PATH, SPEC_PATH):
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
        (root / DOC_PATH).write_text(
            (ROOT / DOC_PATH).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (root / SPEC_PATH).write_text(
            json.dumps(spec, indent=2) + "\n",
            encoding="utf-8",
        )
        return validate_integration_readiness(root)


class GodBrainIntegrationReadinessTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate_integration_readiness(ROOT), [])

    def test_snapshot_cannot_become_currentness_authority(self) -> None:
        errors = _mutated(lambda spec: spec.update({"snapshot_is_currentness_authority": True}))
        self.assertTrue(any("currentness authority" in error for error in errors))

    def test_nooplex_track_cannot_become_core_blocker(self) -> None:
        def mutate(spec):
            spec["classification"]["track_c"] = "CORE_CONVERGENCE_BLOCKER"
        errors = _mutated(mutate)
        self.assertTrue(any("classification" in error for error in errors))

    def test_pr24_red_cannot_be_promoted_without_successor(self) -> None:
        def mutate(spec):
            next(x for x in spec["tracks"]["A_CORE_REPOSITORY_CONVERGENCE"] if x["id"] == "A4_INSTRUCTION_SYNC_PR24")[
                "state"
            ] = "REVIEWED_RESEARCH_SOURCE_CANDIDATE"
        errors = _mutated(mutate)
        self.assertTrue(any("A4_INSTRUCTION_SYNC_PR24" in error for error in errors))

    def test_pr22_cannot_be_silently_marked_reviewed(self) -> None:
        def mutate(spec):
            next(x for x in spec["tracks"]["A_CORE_REPOSITORY_CONVERGENCE"] if x["id"] == "A2_PROJECT_FILE_PR22")[
                "state"
            ] = "REVIEWED"
        errors = _mutated(mutate)
        self.assertTrue(any("A2_PROJECT_FILE_PR22" in error for error in errors))

    def test_pr6_pass_cannot_become_merge_authority(self) -> None:
        def mutate(spec):
            next(x for x in spec["tracks"]["A_CORE_REPOSITORY_CONVERGENCE"] if x["id"] == "A0_FOUNDATION_PR6")[
                "state"
            ] = "ATOMIC_INTEGRATION_REVIEW_PASS_AND_MERGE_AUTHORITY"
        errors = _mutated(mutate)
        self.assertTrue(any("A0_FOUNDATION_PR6" in error for error in errors))

    def test_patrick_merge_gate_cannot_be_deleted(self) -> None:
        errors = _mutated(
            lambda spec: spec["core_composite_prerequisites"].remove(
                "PATRICK_EXACT_MERGE_AUTHORIZATION"
            )
        )
        self.assertTrue(any("prerequisites" in error for error in errors))

    def test_merge_all_source_branches_cannot_be_allowed(self) -> None:
        errors = _mutated(
            lambda spec: spec.update(
                {"composite_assembly_rule": "MERGE_ALL_SOURCE_BRANCHES"}
            )
        )
        self.assertTrue(any("assembly rule" in error for error in errors))

    def test_root_warden_cannot_become_god_brain_authority(self) -> None:
        errors = _mutated(
            lambda spec: spec["root_surfaces"]["WARDEN"].update(
                {"classification": "GOD_BRAIN_CURRENT_AUTHORITY"}
            )
        )
        self.assertTrue(any("WARDEN" in error for error in errors))

    def test_science_track_cannot_become_core_dependency_by_mutation(self) -> None:
        errors = _mutated(
            lambda spec: spec["invariants"].remove(
                "SCIENCE_RESEARCH_SOURCE_ACCEPTANCE_NE_CORE_REPOSITORY_REBINDING_DEPENDENCY"
            )
        )
        self.assertTrue(any("invariants" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
