from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_experiment_admission import DOC_PATH, SPEC_PATH, validate

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
        (root / DOC_PATH).write_text(
            (ROOT / DOC_PATH).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (root / SPEC_PATH).write_text(
            json.dumps(spec, indent=2) + "\n",
            encoding="utf-8",
        )
        return validate(root)


class ExperimentAdmissionArchitectureTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_pending_lineage_source_cannot_be_silently_promoted(self) -> None:
        def mutate(spec):
            spec["source_inputs"][2]["review_state"] = "ACCEPT_SOURCE_RESEARCH_ONLY"
        self.assertTrue(any("source input" in e for e in _mutated(mutate)))

    def test_s4_cannot_become_discriminating_experiment(self) -> None:
        def mutate(spec):
            spec["testability_gate"]["class_dispositions"]["S4"] = "NAMED_SUBMODEL_EMPIRICAL_TEST"
        self.assertTrue(any("testability class dispositions" in e for e in _mutated(mutate)))

    def test_exploratory_ceiling_cannot_exceed_e1(self) -> None:
        def mutate(spec):
            spec["modes"]["EXPLORATORY"]["absolute_escalation_ceiling"] = "E3"
        self.assertTrue(any("exploratory ceiling" in e for e in _mutated(mutate)))

    def test_exploratory_data_cannot_become_confirmatory_holdout(self) -> None:
        def mutate(spec):
            spec["modes"]["EXPLORATORY"]["discovery_data_may_be_confirmatory_holdout"] = True
        self.assertTrue(any("exploratory data" in e for e in _mutated(mutate)))

    def test_internal_confirmation_cannot_claim_e8(self) -> None:
        def mutate(spec):
            spec["modes"]["INTERNAL_CONFIRMATORY"]["absolute_escalation_ceiling"] = "E8"
        self.assertTrue(any("internal confirmatory ceiling" in e for e in _mutated(mutate)))

    def test_external_replication_requires_independent_instrumentation(self) -> None:
        def mutate(spec):
            spec["modes"]["EXTERNAL_REPLICATION"]["requires_separately_implemented_instrumentation"] = False
        self.assertTrue(any("external replication missing" in e for e in _mutated(mutate)))

    def test_lineage_unknown_guard_cannot_be_removed(self) -> None:
        def mutate(spec):
            spec["lineage_gate"]["clean_confirmation_disallowed_when_lineage_unknown"] = False
        self.assertTrue(any("lineage gate" in e for e in _mutated(mutate)))

    def test_new_digest_cannot_prove_clean_root(self) -> None:
        def mutate(spec):
            spec["lineage_gate"]["new_label_or_digest_proves_clean_root"] = True
        self.assertTrue(any("lineage gate" in e for e in _mutated(mutate)))

    def test_packet_cannot_drop_multiple_comparison_rule(self) -> None:
        errors = _mutated(lambda s: s["required_packet_fields"].remove("MULTIPLE_COMPARISON_RULE"))
        self.assertTrue(any("required packet fields" in e for e in errors))

    def test_required_rival_floor_cannot_drop_training_prior_knowledge(self) -> None:
        errors = _mutated(
            lambda s: s["required_rival_hypotheses"].remove("H4_TRAINING_OR_PRIOR_KNOWLEDGE")
        )
        self.assertTrue(any("required rival hypotheses" in e for e in errors))

    def test_e7_minimum_cannot_drop_independent_challenge_custody(self) -> None:
        errors = _mutated(
            lambda s: s["escalation_gate"]["e7_minimum"].remove("INDEPENDENT_CHALLENGE_CUSTODY")
        )
        self.assertTrue(any("E7 minimum controls" in e for e in errors))

    def test_invalidity_floor_cannot_drop_unaudited_channel(self) -> None:
        errors = _mutated(
            lambda s: s["invalidity_conditions"].remove("UNAUDITED_CHANNEL_COULD_CONTAIN_CHALLENGE")
        )
        self.assertTrue(any("invalidity conditions" in e for e in errors))

    def test_testability_floor_cannot_drop_independence_custody_plan(self) -> None:
        errors = _mutated(
            lambda s: s["testability_gate"]["required_fields"].remove("INDEPENDENCE_AND_CUSTODY_PLAN")
        )
        self.assertTrue(any("testability required fields" in e for e in errors))

    def test_internal_confirmation_requires_fresh_holdout(self) -> None:
        errors = _mutated(
            lambda s: s["modes"]["INTERNAL_CONFIRMATORY"].__setitem__("requires_fresh_holdout", False)
        )
        self.assertTrue(any("internal confirmatory requirements" in e for e in errors))

    def test_admission_cannot_be_run_authority(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("ADMISSION_READY_NE_AUTHORIZED_TO_RUN"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_claim_ceiling_cannot_drop_simulation_probability_guard(self) -> None:
        errors = _mutated(lambda s: s["claim_ceiling"].remove("NO_SIMULATION_PROBABILITY_ASSIGNMENT"))
        self.assertTrue(any("claim ceiling" in e for e in errors))

    def test_invalid_experiment_guard_is_required(self) -> None:
        errors = _mutated(lambda s: s["invariants"].remove("INVALID_EXPERIMENT_NE_FALSE_HYPOTHESIS"))
        self.assertTrue(any("invariants" in e for e in errors))

    def test_source_head_is_exact(self) -> None:
        def mutate(spec):
            spec["source_inputs"][0]["exact_head"] = "f" * 40
        self.assertTrue(any("source input" in e for e in _mutated(mutate)))


if __name__ == "__main__":
    unittest.main()
