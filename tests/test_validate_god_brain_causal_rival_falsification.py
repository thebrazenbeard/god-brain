from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_causal_rival_falsification import DOC_PATH, SPEC_PATH, validate

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

class CausalRivalFalsificationTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_unknown_top_level_unique_cause_claim_is_rejected(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("unique_cause_proven", True))
        self.assertTrue(any("top-level machine contract keys" in e for e in errors))

    def test_unknown_ordinary_mechanism_is_required(self) -> None:
        errors = _mutated(lambda s: s["minimum_rival_families"].remove("UNKNOWN_ORDINARY_MECHANISM"))
        self.assertTrue(any("minimum rival" in e for e in errors))

    def test_one_failed_rival_guard_is_required(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("ONE_FAILED_RIVAL_NE_FAVORED_HYPOTHESIS_CONFIRMED"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_favored_within_set_is_not_unique_cause(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("FAVORED_WITHIN_DECLARED_RIVAL_SET_NE_UNIQUE_CAUSE"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_post_hoc_state_cannot_disappear(self) -> None:
        errors = _mutated(lambda s: s["precommitment_states"].remove("CREATED_AFTER_TARGET_EVIDENCE"))
        self.assertTrue(any("precommitment" in e for e in errors))

    def test_missing_confounder_hostile_case_is_required(self) -> None:
        errors = _mutated(lambda s: s["required_hostile_cases"].remove("MISSING_CONFOUNDER_TREATED_ABSENT"))
        self.assertTrue(any("hostile" in e for e in errors))

    def test_simulation_probability_ceiling_is_required(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_SIMULATION_PROBABILITY_ASSIGNMENT"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_contact_ceiling_is_required(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_EXTERNAL_CONTACT_CLAIM"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_stage_cannot_jump(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("research_stage", "EXTERNAL_SCIENTIFIC_VALIDATION"))
        self.assertTrue(any("research stage" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
