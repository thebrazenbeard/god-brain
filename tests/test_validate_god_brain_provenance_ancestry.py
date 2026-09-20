from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_provenance_ancestry import (
    DOC_PATH,
    FIXTURE_PATH,
    POINTER_RECEIPT_PATH,
    SPEC_PATH,
    validate_provenance_ancestry,
)


class GodBrainProvenanceAncestryTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_provenance_ancestry(root), [])

    def _write_subject(self, target: Path, spec: dict, fixture: dict, doc: str) -> None:
        root = Path(__file__).resolve().parents[1]
        for relative in (SPEC_PATH, FIXTURE_PATH, DOC_PATH, POINTER_RECEIPT_PATH):
            (target / relative).parent.mkdir(parents=True, exist_ok=True)
        (target / SPEC_PATH).write_text(json.dumps(spec), encoding="utf-8")
        (target / FIXTURE_PATH).write_text(json.dumps(fixture), encoding="utf-8")
        (target / DOC_PATH).write_text(doc, encoding="utf-8")
        (target / POINTER_RECEIPT_PATH).write_text(
            (root / POINTER_RECEIPT_PATH).read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    def test_unknown_ancestry_cannot_default_to_independent(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(spec))
            mutated["ancestry_rules"]["unknown_ancestry_does_not_imply_independence"] = False
            self._write_subject(target, mutated, fixture, doc)
            errors = validate_provenance_ancestry(target)
            self.assertTrue(any("unknown ancestry must not imply independence" in error for error in errors))

    def test_different_agents_cannot_be_counted_as_independent_by_default(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(fixture))
            case = next(x for x in mutated["cases"] if x["id"] == "GB-PA-005")
            case["independence_state"] = "INDEPENDENT_WITHIN_DECLARED_SCOPE"
            self._write_subject(target, spec, mutated, doc)
            errors = validate_provenance_ancestry(target)
            self.assertTrue(any("GB-PA-005 expectation drifted" in error for error in errors))

    def test_old_review_cannot_apply_to_changed_head(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(fixture))
            case = next(x for x in mutated["cases"] if x["id"] == "GB-PA-010")
            case["independence_state"] = "NOT_APPLICABLE"
            case["expected"] = "REVIEW_STILL_VALID"
            self._write_subject(target, spec, mutated, doc)
            errors = validate_provenance_ancestry(target)
            self.assertTrue(any("GB-PA-010 expectation drifted" in error for error in errors))

    def test_privacy_projection_must_retain_lineage(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(spec))
            mutated["privacy_rules"]["privacy_projection_must_retain_lineage"] = False
            self._write_subject(target, mutated, fixture, doc)
            errors = validate_provenance_ancestry(target)
            self.assertTrue(any("privacy projection must retain lineage" in error for error in errors))

    def _mutated_contract_errors(self, mutator) -> list[str]:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(spec))
            mutator(mutated)
            self._write_subject(target, mutated, fixture, doc)
            return validate_provenance_ancestry(target)

    def test_declared_invariant_set_is_exact(self) -> None:
        errors = self._mutated_contract_errors(
            lambda spec: spec["invariants"].remove("SOURCE_PRESENCE_NE_ADMISSION")
        )
        self.assertTrue(any("invariants drifted" in error for error in errors))

    def test_nonhex_blob_pointer_fails_closed(self) -> None:
        def mutate(spec: dict) -> None:
            spec["source_provenance"][0]["artifacts"][0][1] = "z" * 40

        errors = self._mutated_contract_errors(mutate)
        self.assertTrue(any("artifact blob must be lowercase 40-hex" in error for error in errors))

    def test_fake_valid_shape_head_fails_receipt_binding(self) -> None:
        def mutate(spec: dict) -> None:
            spec["source_provenance"][0]["observed_head"] = "0" * 40

        errors = self._mutated_contract_errors(mutate)
        self.assertTrue(any("do not exactly match verification receipt" in error for error in errors))

    def test_nonexistent_path_fails_receipt_binding(self) -> None:
        def mutate(spec: dict) -> None:
            spec["source_provenance"][1]["artifacts"][0][0] = "does/not/exist.md"

        errors = self._mutated_contract_errors(mutate)
        self.assertTrue(any("do not exactly match verification receipt" in error for error in errors))

    def test_correct_blob_rebound_to_wrong_head_fails_receipt_binding(self) -> None:
        def mutate(spec: dict) -> None:
            spec["source_provenance"][2]["observed_head"] = spec["source_provenance"][0]["observed_head"]

        errors = self._mutated_contract_errors(mutate)
        self.assertTrue(any("do not exactly match verification receipt" in error for error in errors))

    def test_provenance_edge_vocabulary_cannot_silently_weaken(self) -> None:
        errors = self._mutated_contract_errors(
            lambda spec: spec["provenance_edge_types"].remove("COPIED_FROM")
        )
        self.assertTrue(any("provenance_edge_types drifted" in error for error in errors))

    def test_required_artifact_identity_field_cannot_be_deleted(self) -> None:
        errors = self._mutated_contract_errors(
            lambda spec: spec["required_artifact_fields"].remove("artifact_id")
        )
        self.assertTrue(any("required_artifact_fields drifted" in error for error in errors))

    def test_independence_rule_cannot_be_deleted(self) -> None:
        errors = self._mutated_contract_errors(
            lambda spec: spec["independence_rules"].remove("INDEPENDENCE_IS_CLAIM_RELATIVE")
        )
        self.assertTrue(any("independence_rules drifted" in error for error in errors))

    def test_currentness_and_query_surfaces_are_machine_bound(self) -> None:
        def mutate(spec: dict) -> None:
            spec["currentness_states"].remove("UNKNOWN")
            spec["query_contracts"].remove("IS_THIS_CURRENT")

        errors = self._mutated_contract_errors(mutate)
        self.assertTrue(any("currentness_states drifted" in error for error in errors))
        self.assertTrue(any("query_contracts drifted" in error for error in errors))

    def test_provenance_must_remain_dag(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(spec))
            mutated["ancestry_rules"]["provenance_edges_form_dag"] = False
            self._write_subject(target, mutated, fixture, doc)
            errors = validate_provenance_ancestry(target)
            self.assertTrue(any("must remain a DAG" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
