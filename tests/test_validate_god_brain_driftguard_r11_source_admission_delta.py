from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_driftguard_r11_source_admission_delta import (
    DOC_PATH,
    SPEC_PATH,
    validate,
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
        (root / SPEC_PATH).write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        return validate(root)


class DriftGuardR11SourceAdmissionDeltaTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_self_review_cannot_be_promoted_to_independent(self) -> None:
        def mutate(spec):
            spec["source"]["independent_exact_head_review_state"] = "PASS"
        errors = _mutated(mutate)
        self.assertTrue(any("source binding" in error for error in errors))

    def test_corrected_hostile_blocker_cannot_be_erased(self) -> None:
        def mutate(spec):
            spec["source"]["hostile_exact_head_review_state"] = "PASS"
        errors = _mutated(mutate)
        self.assertTrue(any("source binding" in error for error in errors))

    def test_failed_source_cannot_revert_to_pending_admission(self) -> None:
        def mutate(spec):
            spec["source"]["admission"] = "RESEARCH_ONLY_PENDING_INDEPENDENT_EXACT_HEAD_REVIEW"
        errors = _mutated(mutate)
        self.assertTrue(any("source binding" in error for error in errors))

    def test_hostile_review_cannot_be_relabelled_independent(self) -> None:
        def mutate(spec):
            spec["source"]["hostile_review_independence"] = "INDEPENDENT_CORROBORATION"
        errors = _mutated(mutate)
        self.assertTrue(any("source binding" in error for error in errors))

    def test_current_head_cannot_move_silently(self) -> None:
        def mutate(spec):
            spec["source"]["exact_head"] = "f" * 40
        errors = _mutated(mutate)
        self.assertTrue(any("source binding" in error or "exact_head" in error for error in errors))

    def test_admission_cannot_skip_review_gate(self) -> None:
        def mutate(spec):
            spec["source"]["admission"] = "ADAPT_WITH_PROVENANCE"
        errors = _mutated(mutate)
        self.assertTrue(any("source binding" in error for error in errors))

    def test_retry_ambiguity_guard_is_closed(self) -> None:
        errors = _mutated(
            lambda spec: spec["invariants"].remove(
                "AMBIGUOUS_CONFIRMATORY_EXECUTION_NE_SAFE_TO_RETRY"
            )
        )
        self.assertTrue(any("invariants" in error for error in errors))

    def test_separate_chat_independence_guard_is_closed(self) -> None:
        errors = _mutated(
            lambda spec: spec["invariants"].remove(
                "SEPARATE_CHAT_NE_INDEPENDENT_CORROBORATION"
            )
        )
        self.assertTrue(any("invariants" in error for error in errors))

    def test_simulation_claim_cannot_enter_ceiling(self) -> None:
        errors = _mutated(
            lambda spec: spec["claim_ceiling"].append("SIMULATION_CONFIRMED")
        )
        self.assertTrue(any("claim_ceiling" in error for error in errors))

    def test_future_gate_must_bind_exact_head(self) -> None:
        def mutate(spec):
            spec["future_gate"]["failed_head"] = "0" * 40
        errors = _mutated(mutate)
        self.assertTrue(any("future review gate" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
