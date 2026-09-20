from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_atomic_integration_blueprint import (
    DOC_PATH,
    FIXTURE_PATH,
    SPEC_PATH,
    validate_atomic_integration_blueprint,
)


class GodBrainAtomicIntegrationBlueprintTests(unittest.TestCase):
    def test_repository_blueprint_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_atomic_integration_blueprint(root), [])

    def test_pending_component_cannot_be_treated_as_review_clean(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["inputs"]["project_interface"]["role"] = "REVIEW_CLEAN_INPUT"
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_atomic_integration_blueprint(target)
            self.assertTrue(any("project_interface" in error and "PENDING_REVIEW_INPUT" in error for error in errors))

    def test_machine_current_pointer_cannot_admit_live_review_state(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["composite_conformance"]["machine_current_pointer_forbidden_fields"].remove("active_reviews")
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_atomic_integration_blueprint(target)
            self.assertTrue(any("active_reviews" in error for error in errors))

    def test_candidate_project_pack_cannot_be_marked_canonical(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["project_installation_rule"]["candidate_pack_is_canonical"] = True
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_atomic_integration_blueprint(target)
            self.assertTrue(any("candidate Project pack" in error for error in errors))

    def test_current_must_remain_mandatory_rebinding_target(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            mutated = json.loads(json.dumps(spec))
            mutated["root_surface_audit"]["surfaces"]["CURRENT.md"]["disposition"] = "GOD_BRAIN_CORRECT"
            (target / SPEC_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_atomic_integration_blueprint(target)
            self.assertTrue(any("CURRENT.md" in error and "disposition drifted" in error for error in errors))

    def test_composite_fixture_sequence_is_closed(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / SPEC_PATH).parent.mkdir(parents=True)
            (target / DOC_PATH).parent.mkdir(parents=True)
            (target / FIXTURE_PATH).parent.mkdir(parents=True)
            (target / SPEC_PATH).write_text(json.dumps(spec), encoding="utf-8")
            (target / DOC_PATH).write_text(
                (root / DOC_PATH).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            mutated = json.loads(json.dumps(fixture))
            mutated["cases"].pop()
            (target / FIXTURE_PATH).write_text(json.dumps(mutated), encoding="utf-8")
            errors = validate_atomic_integration_blueprint(target)
            self.assertTrue(any("GB-COMP-001..016" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
