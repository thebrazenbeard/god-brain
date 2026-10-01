from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_intake_evidence_admission import (
    DOC_PATH,
    FIXTURE_PATH,
    SPEC_PATH,
    validate_intake_evidence_admission,
)

ROOT = Path(__file__).resolve().parents[1]

def _load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def _mutated(spec_mutator=None, fixture_mutator=None) -> list[str]:
    spec = copy.deepcopy(_load(SPEC_PATH))
    fixtures = copy.deepcopy(_load(FIXTURE_PATH))
    if spec_mutator:
        spec_mutator(spec)
    if fixture_mutator:
        fixture_mutator(fixtures)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for relative in (DOC_PATH, SPEC_PATH, FIXTURE_PATH):
            (root / relative).parent.mkdir(parents=True, exist_ok=True)
        (root / DOC_PATH).write_text((ROOT / DOC_PATH).read_text(encoding="utf-8"), encoding="utf-8")
        (root / SPEC_PATH).write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        (root / FIXTURE_PATH).write_text(json.dumps(fixtures, indent=2) + "\n", encoding="utf-8")
        return validate_intake_evidence_admission(root)

class IntakeEvidenceAdmissionTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate_intake_evidence_admission(ROOT), [])

    def test_model_output_cannot_be_promoted_to_verified(self) -> None:
        errors = _mutated(lambda spec: spec["admission_rules"].remove("MODEL_OR_TOOL_OUTPUT_MUST_NOT_SELF_PROMOTE_TO_VERIFIED_FACT"))
        self.assertTrue(any("admission_rules" in error for error in errors))

    def test_currentness_cannot_move_inside_intake(self) -> None:
        errors = _mutated(lambda spec: spec["admission_rules"].remove("CURRENTNESS_IS_DOWNSTREAM_OF_EVIDENCE_ADMISSION"))
        self.assertTrue(any("admission_rules" in error for error in errors))

    def test_effect_authority_ceiling_cannot_be_removed(self) -> None:
        errors = _mutated(lambda spec: spec["claim_ceiling"].remove("NO_EFFECT_AUTHORITY"))
        self.assertTrue(any("claim_ceiling" in error for error in errors))

    def test_private_payload_ceiling_cannot_be_removed(self) -> None:
        errors = _mutated(lambda spec: spec["claim_ceiling"].remove("NO_PRIVATE_PAYLOAD_TRANSFER"))
        self.assertTrue(any("claim_ceiling" in error for error in errors))

    def test_exact_donor_head_cannot_drift(self) -> None:
        def mutate(spec):
            next(x for x in spec["donor_sources"] if x["repository"] == "thebrazenbeard/ingest")["exact_head"] = "f" * 40
        errors = _mutated(mutate)
        self.assertTrue(any("exact donor head" in error for error in errors))

    def test_normalization_must_keep_raw_parent(self) -> None:
        def mutate(spec):
            spec["objects"]["NormalizationRecord"]["required"].remove("parent_raw_sha256")
        errors = _mutated(mutate)
        self.assertTrue(any("parent_raw_sha256" in error for error in errors))

    def test_interpretation_must_keep_provenance(self) -> None:
        def mutate(spec):
            spec["objects"]["InterpretationCandidate"]["required"].remove("provenance_class")
        errors = _mutated(mutate)
        self.assertTrue(any("provenance_class" in error for error in errors))

    def test_admission_must_keep_independence_family(self) -> None:
        def mutate(spec):
            spec["objects"]["EvidenceAdmissionDecision"]["required"].remove("independence_family")
        errors = _mutated(mutate)
        self.assertTrue(any("independence_family" in error for error in errors))

    def test_semantic_similarity_invariant_cannot_be_removed(self) -> None:
        errors = _mutated(lambda spec: spec["invariants"].remove("SEMANTIC_SIMILARITY_NE_SAME_PROVENANCE"))
        self.assertTrue(any("invariants" in error for error in errors))

    def test_user_statement_cannot_become_independent_verification(self) -> None:
        errors = _mutated(lambda spec: spec["invariants"].remove("USER_STATED_NE_INDEPENDENTLY_VERIFIED"))
        self.assertTrue(any("invariants" in error for error in errors))

    def test_hostile_case_cannot_be_removed(self) -> None:
        def mutate(fixtures):
            fixtures["cases"] = [x for x in fixtures["cases"] if x["id"] != "IE-08"]
        errors = _mutated(fixture_mutator=mutate)
        self.assertTrue(any("IE-01..IE-12" in error for error in errors))

    def test_hostile_case_guard_must_reference_contract(self) -> None:
        def mutate(fixtures):
            fixtures["cases"][0]["guards"] = ["INVENTED_GUARD"]
        errors = _mutated(fixture_mutator=mutate)
        self.assertTrue(any("unknown guard" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
