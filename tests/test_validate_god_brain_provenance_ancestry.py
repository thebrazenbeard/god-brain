from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_provenance_ancestry import (
    DOC_PATH,
    FIXTURE_PATH,
    SPEC_PATH,
    validate_provenance_ancestry,
)


class GodBrainProvenanceAncestryTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_provenance_ancestry(root), [])

    def _write_subject(self, target: Path, spec: dict, fixture: dict, doc: str) -> None:
        for relative in (SPEC_PATH, FIXTURE_PATH, DOC_PATH):
            (target / relative).parent.mkdir(parents=True, exist_ok=True)
        (target / SPEC_PATH).write_text(json.dumps(spec), encoding="utf-8")
        (target / FIXTURE_PATH).write_text(json.dumps(fixture), encoding="utf-8")
        (target / DOC_PATH).write_text(doc, encoding="utf-8")

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
