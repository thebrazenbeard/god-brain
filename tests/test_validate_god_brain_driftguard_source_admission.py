from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_driftguard_source_admission import (
    DOC_PATH,
    SPEC_PATH,
    validate_driftguard_source_admission,
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
        return validate_driftguard_source_admission(root)


class DriftGuardSourceAdmissionTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate_driftguard_source_admission(ROOT), [])

    def test_pr31_cannot_be_silently_admitted(self) -> None:
        def mutate(spec):
            next(x for x in spec["sources"] if x["id"] == "DRIFTGUARD_PR31_ATOMIC_CURRENTNESS")[
                "admission"
            ] = "ADAPT_WITH_PROVENANCE"
        errors = _mutated(mutate)
        self.assertTrue(any("PR31" in error or "admission" in error for error in errors))

    def test_pr32_cannot_be_promoted_from_design(self) -> None:
        def mutate(spec):
            next(x for x in spec["sources"] if x["id"] == "DRIFTGUARD_PR32_EFFECT_AUTHORIZATION_CAS_DESIGN")[
                "admission"
            ] = "ADAPT_WITH_PROVENANCE"
        errors = _mutated(mutate)
        self.assertTrue(any("PR32" in error or "admission" in error for error in errors))

    def test_failed_pr28_cannot_be_relabelled_pass(self) -> None:
        def mutate(spec):
            next(x for x in spec["sources"] if x["id"] == "DRIFTGUARD_PR28_CURRENTNESS_RACE")[
                "review_disposition"
            ] = "PASS"
        errors = _mutated(mutate)
        self.assertTrue(any("PR28" in error or "review_disposition" in error for error in errors))

    def test_r10_cannot_gain_runtime_coupling(self) -> None:
        def mutate(spec):
            next(x for x in spec["sources"] if x["id"] == "DRIFTGUARD_R10_DETECTOR_COMPARISON")[
                "admission"
            ] = "ADMIT_UNCHANGED_RUNTIME_DEPENDENCY"
        errors = _mutated(mutate)
        self.assertTrue(any("R10" in error or "admission" in error for error in errors))

    def test_detector_alarm_contact_guard_is_closed(self) -> None:
        errors = _mutated(lambda spec: spec["invariants"].remove("DETECTOR_ALARM_NE_CONTACT"))
        self.assertTrue(any("invariants" in error for error in errors))

    def test_same_holdout_promotion_guard_is_closed(self) -> None:
        errors = _mutated(
            lambda spec: spec["invariants"].remove(
                "SAME_HOLDOUT_COMPARISON_NE_PRODUCTION_SELECTION_AUTHORITY"
            )
        )
        self.assertTrue(any("invariants" in error for error in errors))

    def test_claim_ceiling_cannot_gain_simulation_evidence(self) -> None:
        errors = _mutated(lambda spec: spec["claim_ceiling"].append("SIMULATION_EVIDENCE_VERIFIED"))
        self.assertTrue(any("claim ceiling" in error for error in errors))

    def test_source_head_must_remain_exact(self) -> None:
        def mutate(spec):
            next(x for x in spec["sources"] if x["id"] == "DRIFTGUARD_R10_DETECTOR_COMPARISON")[
                "exact_head"
            ] = "f" * 40
        errors = _mutated(mutate)
        self.assertTrue(any("exact_head" in error for error in errors))

    def test_source_fields_are_closed(self) -> None:
        def mutate(spec):
            spec["sources"][0]["runtime_dependency"] = True
        errors = _mutated(mutate)
        self.assertTrue(any("fields must be exact" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
