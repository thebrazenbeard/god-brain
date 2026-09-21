from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_evidence_exposure_lineage import DOC_PATH, SPEC_PATH, validate

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
        (root / DOC_PATH).write_text((ROOT / DOC_PATH).read_text(encoding="utf-8"), encoding="utf-8")
        (root / SPEC_PATH).write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        return validate(root)

class EvidenceExposureLineageTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_proven_unexposed_stays_forbidden(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("forbidden_statuses", []))
        self.assertTrue(any("PROVEN_UNEXPOSED" in e for e in errors))

    def test_no_recorded_exposure_cannot_become_proof(self) -> None:
        errors = _mutated(lambda s: s["untouched_decision"].__setitem__("NO_RECORDED_EXPOSURE", "PROVEN_UNTOUCHED"))
        self.assertTrue(any("untouched decision" in e for e in errors))

    def test_unknown_exposure_cannot_be_clean(self) -> None:
        errors = _mutated(lambda s: s["untouched_decision"].__setitem__("EXPOSURE_UNKNOWN", "LOCALLY_CLEAN"))
        self.assertTrue(any("untouched decision" in e for e in errors))

    def test_hash_change_does_not_clear_exposure(self) -> None:
        errors = _mutated(lambda s: s["propagation"].__setitem__("hash_change_clears_exposure", True))
        self.assertTrue(any("propagation" in e for e in errors))

    def test_summary_does_not_clear_exposure(self) -> None:
        errors = _mutated(lambda s: s["propagation"].__setitem__("summary_clears_exposure", True))
        self.assertTrue(any("propagation" in e for e in errors))

    def test_new_chat_guard_is_required(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("NEW_CHAT_NE_CLEAN_REVIEWER"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_result_exposure_guard_is_required(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("RESULT_EXPOSURE_CAN_CONTAMINATE_FUTURE_DESIGN"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_model_prior_knowledge_ceiling_is_required(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_TRAINING_DATA_ABSENCE_PROOF"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_independence_ceiling_is_required(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_REVIEWER_INDEPENDENCE_PROOF"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_copied_generated_tests_hostile_case_is_required(self) -> None:
        errors = _mutated(lambda s: s["required_hostile_cases"].remove("COPIED_GENERATED_TESTS_PROMOTED_TO_INDEPENDENCE"))
        self.assertTrue(any("hostile" in e for e in errors))

    def test_stage_cannot_jump_to_validation(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("research_stage", "EXTERNAL_SCIENTIFIC_VALIDATION"))
        self.assertTrue(any("research stage" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
