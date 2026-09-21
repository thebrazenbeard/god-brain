from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_confirmatory_study_lineage import DOC_PATH, SPEC_PATH, validate

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


class ConfirmatoryStudyLineageTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_display_label_cannot_be_identity(self) -> None:
        errors = _mutated(lambda s: s["identity"].__setitem__("display_label_is_identity", True))
        self.assertTrue(any("display label" in e for e in errors))

    def test_same_subject_must_inherit_holdout_content_ancestry(self) -> None:
        errors = _mutated(lambda s: s["successor_classes"]["SAME_SUBJECT_ATTEMPT"].__setitem__("inherits_holdout_content_ancestry", False))
        self.assertTrue(any("same-subject" in e for e in errors))

    def test_redesign_cannot_claim_untouched_confirmation(self) -> None:
        errors = _mutated(lambda s: s["successor_classes"]["SUCCESSOR_REDESIGN"].__setitem__("may_claim_untouched_confirmation_of_predecessor", True))
        self.assertTrue(any("successor-redesign" in e for e in errors))

    def test_observation_content_digest_is_required(self) -> None:
        errors = _mutated(lambda s: s["holdout_ancestry_required_fields"].remove("OBSERVATION_CONTENT_DIGEST"))
        self.assertTrue(any("holdout ancestry" in e for e in errors))

    def test_study_relabel_hostile_case_is_required(self) -> None:
        errors = _mutated(lambda s: s["required_hostile_cases"].remove("STUDY_RELABEL_RESETS_ANCESTRY"))
        self.assertTrue(any("hostile" in e for e in errors))

    def test_ambiguous_retry_guard_is_required(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("AMBIGUOUS_EXECUTION_NE_SAFE_TO_RETRY"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_independence_cannot_be_promoted(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_STATISTICAL_INDEPENDENCE_PROOF"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_new_digest_cannot_establish_clean_root(self) -> None:
        errors = _mutated(lambda s: s["lineage_registry"].__setitem__("new_digest_establishes_clean_root", True))
        self.assertTrue(any("lineage registry" in e for e in errors))

    def test_digest_cannot_claim_semantic_equivalence(self) -> None:
        errors = _mutated(lambda s: s["canonical_subject_digest"].__setitem__("digest_is_semantic_equivalence_proof", True))
        self.assertTrue(any("canonical subject digest" in e for e in errors))

    def test_post_exposure_redesign_requires_changed_fields(self) -> None:
        errors = _mutated(lambda s: s["change_timing_classes"]["POST_EXPOSURE_REDESIGN"].__setitem__("requires_changed_field_disclosure", False))
        self.assertTrue(any("change-timing" in e for e in errors))

    def test_unlinked_root_cannot_claim_independence(self) -> None:
        errors = _mutated(lambda s: s["lineage_registry"].__setitem__("unlinked_root_establishes_independence", True))
        self.assertTrue(any("lineage registry" in e for e in errors))

    def test_stage_cannot_jump_to_validation(self) -> None:
        errors = _mutated(lambda s: s.__setitem__("research_stage", "EXTERNAL_SCIENTIFIC_VALIDATION"))
        self.assertTrue(any("research stage" in e for e in errors))

    def test_triggering_source_head_is_exact(self) -> None:
        errors = _mutated(lambda s: s["triggering_source"].__setitem__("exact_head", "f" * 40))
        self.assertTrue(any("source binding" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
