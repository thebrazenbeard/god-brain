from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_three_lane_reasoning_protocol import DOC_PATH, SPEC_PATH, validate

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

class ThreeLaneProtocolTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_unknown_top_level_authority_claim_is_rejected(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("merge_authority", True))
        self.assertTrue(any("top-level machine contract keys" in e for e in errors))

    def test_unknown_top_level_independence_claim_is_rejected(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("lane_independence_proven", True))
        self.assertTrue(any("top-level machine contract keys" in e for e in errors))

    def test_lane_set_is_closed(self) -> None:
        errors = _mutated(lambda s: s["lanes"].append("FOURTH_VOTER"))
        self.assertTrue(any("lanes" in e for e in errors))

    def test_subject_packet_cannot_drop_exact_head_binding(self) -> None:
        errors = _mutated(
            lambda s: s["subject_packet_required_fields"].remove(
                "REPOSITORY_AND_EXACT_HEAD_WHEN_APPLICABLE"
            )
        )
        self.assertTrue(any("subject packet required fields" in e for e in errors))

    def test_first_pass_cannot_drop_exposure_disclosure(self) -> None:
        errors = _mutated(
            lambda s: s["first_pass_required_fields"].remove("EXPOSURE_DISCLOSURE")
        )
        self.assertTrue(any("first pass required fields" in e for e in errors))

    def test_reconciliation_cannot_drop_contradiction_severity(self) -> None:
        errors = _mutated(
            lambda s: s["reconciliation_factors"].remove("CONTRADICTION_SEVERITY")
        )
        self.assertTrue(any("reconciliation factors" in e for e in errors))

    def test_blind_does_not_mean_independent(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("BLIND_AS_PRACTICAL_NE_INDEPENDENT_EVIDENCE"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_hard_blocker_cannot_be_outvoted(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("HARD_EVIDENCE_BLOCKER_NE_OUTVOTABLE"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_shared_source_not_tripled(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("SAME_SOURCE_USED_BY_THREE_LANES_NE_THREE_SOURCES"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_missing_lane_not_agreement(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("MISSING_LANE_NE_IMPLIED_AGREEMENT"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_external_validation_ceiling_is_required(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_EXTERNAL_CORROBORATION_CLAIM"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_cross_exam_hostile_case_is_required(self) -> None:
        errors = _mutated(lambda s: s["required_hostile_cases"].remove("CROSS_EXAM_AGREEMENT_MISLABELED_BLIND"))
        self.assertTrue(any("hostile" in e for e in errors))

    def test_moved_head_case_is_required(self) -> None:
        errors = _mutated(lambda s: s["required_hostile_cases"].remove("MOVED_HEAD_RESULT_REMAINS_CURRENT"))
        self.assertTrue(any("hostile" in e for e in errors))

    def test_stage_cannot_jump(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("research_stage", "EXTERNAL_SCIENTIFIC_VALIDATION"))
        self.assertTrue(any("research stage" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
