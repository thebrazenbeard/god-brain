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

    def test_unknown_ordinary_is_nonfalsifiable_coverage_sentinel(self) -> None:
        errors = _mutated(lambda s: s["coverage_sentinel"].__setitem__("cannot_be_falsified", False))
        self.assertTrue(any("coverage sentinel" in e for e in errors))

    def test_unknown_ordinary_is_not_a_testable_rival_family(self) -> None:
        errors = _mutated(lambda s: s["minimum_testable_rival_families"].append("UNKNOWN_ORDINARY_MECHANISM"))
        self.assertTrue(any("minimum testable rival" in e for e in errors))

    def test_revision_lineage_cannot_disappear(self) -> None:
        errors = _mutated(lambda s: s["hypothesis_identity_rules"].remove("NEW_ID_DOES_NOT_ERASE_PARENT_ID"))
        self.assertTrue(any("identity rules" in e for e in errors))

    def test_earliest_exposure_is_required_on_hypothesis(self) -> None:
        errors = _mutated(lambda s: s["hypothesis_required_fields"].remove("EARLIEST_TARGET_EVIDENCE_EXPOSURE"))
        self.assertTrue(any("hypothesis fields" in e for e in errors))

    def test_evidence_independence_ledger_is_required(self) -> None:
        errors = _mutated(lambda s: s["comparison_required_fields"].remove("EVIDENCE_INDEPENDENCE_LEDGER"))
        self.assertTrue(any("comparison fields" in e for e in errors))

    def test_unknown_independence_cannot_be_support(self) -> None:
        errors = _mutated(lambda s: s["decision_guards"].remove("INDEPENDENCE_UNKNOWN_NE_INDEPENDENT_SUPPORT"))
        self.assertTrue(any("decision guards" in e for e in errors))

    def test_unresolved_confounder_blocks_favored_disposition(self) -> None:
        errors = _mutated(lambda s: s["decision_guards"].remove("MATERIAL_CONFOUNDER_UNRESOLVED_BLOCKS_FAVORED_DISPOSITION"))
        self.assertTrue(any("decision guards" in e for e in errors))

    def test_optional_stopping_guard_is_required(self) -> None:
        errors = _mutated(lambda s: s["stopping_rule_guards"].remove("STOPPING_RULE_CANNOT_DEPEND_ON_FAVORED_HYPOTHESIS_WINNING"))
        self.assertTrue(any("stopping-rule guards" in e for e in errors))

    def test_post_evidence_hypothesis_requires_fresh_confirmatory_test(self) -> None:
        errors = _mutated(lambda s: s["new_hypothesis_guards"].remove("POST_EVIDENCE_HYPOTHESIS_REQUIRES_FRESH_TEST_FOR_CONFIRMATORY_USE"))
        self.assertTrue(any("new-hypothesis guards" in e for e in errors))

    def test_simulation_probability_ceiling_is_required(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_SIMULATION_PROBABILITY_ASSIGNMENT"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_stage_cannot_jump(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("research_stage", "EXTERNAL_SCIENTIFIC_VALIDATION"))
        self.assertTrue(any("research stage" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
