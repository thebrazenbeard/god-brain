from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_project_file_architecture import (
    DOC_PATH,
    SPEC_PATH,
    validate_project_file_architecture,
)


ROOT = Path(__file__).resolve().parents[1]


def load_spec() -> dict:
    return json.loads((ROOT / SPEC_PATH).read_text(encoding="utf-8"))


def validate_mutation(mutator) -> list[str]:
    spec = load_spec()
    mutator(spec)
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        (target / SPEC_PATH).parent.mkdir(parents=True)
        (target / DOC_PATH).parent.mkdir(parents=True)
        (target / SPEC_PATH).write_text(
            json.dumps(spec, indent=2) + "\n",
            encoding="utf-8",
        )
        (target / DOC_PATH).write_text(
            (ROOT / DOC_PATH).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        return validate_project_file_architecture(target)


def stratum(spec: dict, stratum_id: str) -> dict:
    return next(item for item in spec["strata"] if item["id"] == stratum_id)


class GodBrainProjectFileArchitectureTests(unittest.TestCase):
    def test_repository_research_contract_validates(self) -> None:
        self.assertEqual(validate_project_file_architecture(ROOT), [])

    def test_current_pointer_cannot_admit_live_pr_state(self) -> None:
        errors = validate_mutation(
            lambda spec: spec["future_current_pointer_contract"][
                "forbidden_fields"
            ].remove("open_pull_requests")
        )
        self.assertTrue(any("open_pull_requests" in error for error in errors))

    def test_future_current_pointer_required_field_cannot_be_dropped(self) -> None:
        errors = validate_mutation(
            lambda spec: spec["future_current_pointer_contract"][
                "required_fields"
            ].remove("governance_path")
        )
        self.assertTrue(any("governance_path" in error for error in errors))

    def test_research_claim_ceiling_cannot_be_dropped(self) -> None:
        errors = validate_mutation(
            lambda spec: spec["claim_ceiling"].remove("NO_CANONICAL_PROMOTION")
        )
        self.assertTrue(
            any("NO_CANONICAL_PROMOTION" in error for error in errors)
        )

    def test_root_manifest_forbidden_live_state_guard_cannot_be_dropped(self) -> None:
        def mutate(spec: dict) -> None:
            stratum(spec, "ROOT_DISCOVERY_MANIFEST")["forbidden"].remove(
                "live_provider_status"
            )

        errors = validate_mutation(mutate)
        self.assertTrue(
            any("ROOT_DISCOVERY_MANIFEST.forbidden" in error for error in errors)
        )
        self.assertTrue(any("live_provider_status" in error for error in errors))

    def test_review_evidence_required_binding_cannot_be_dropped(self) -> None:
        def mutate(spec: dict) -> None:
            stratum(spec, "REVIEW_EVIDENCE")["required_binding"].remove(
                "reviewer_identity"
            )

        errors = validate_mutation(mutate)
        self.assertTrue(
            any("REVIEW_EVIDENCE.required_binding" in error for error in errors)
        )
        self.assertTrue(any("reviewer_identity" in error for error in errors))

    def test_review_evidence_self_certification_guard_cannot_be_dropped(self) -> None:
        def mutate(spec: dict) -> None:
            stratum(spec, "REVIEW_EVIDENCE")["forbidden"].remove(
                "self_certification"
            )

        errors = validate_mutation(mutate)
        self.assertTrue(
            any("REVIEW_EVIDENCE.forbidden" in error for error in errors)
        )
        self.assertTrue(any("self_certification" in error for error in errors))

    def test_checkpoint_authority_guard_cannot_be_dropped(self) -> None:
        def mutate(spec: dict) -> None:
            stratum(spec, "CONTINUATION_CHECKPOINTS")["forbidden"].remove(
                "merge_authority"
            )

        errors = validate_mutation(mutate)
        self.assertTrue(
            any("CONTINUATION_CHECKPOINTS.forbidden" in error for error in errors)
        )
        self.assertTrue(any("merge_authority" in error for error in errors))

    def test_mutable_operational_state_must_remain_fresh_read(self) -> None:
        def mutate(spec: dict) -> None:
            stratum(spec, "MUTABLE_OPERATIONAL_STATE")["rule"] = "CACHED_OK"

        errors = validate_mutation(mutate)
        self.assertTrue(
            any("MUTABLE_OPERATIONAL_STATE.rule mismatch" in error for error in errors)
        )

    def test_duplicate_stratum_id_is_rejected(self) -> None:
        def mutate(spec: dict) -> None:
            spec["strata"][-1]["id"] = "ROOT_DISCOVERY_MANIFEST"

        errors = validate_mutation(mutate)
        self.assertTrue(any("stratum ids must be unique" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
