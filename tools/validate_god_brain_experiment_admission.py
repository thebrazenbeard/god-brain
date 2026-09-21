from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_EXPERIMENT_ADMISSION_ARCHITECTURE_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_EXPERIMENT_ADMISSION_ARCHITECTURE_V0_1.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_INVARIANTS = {
    "ADMISSION_PACKET_PASS_NE_RESULT_VALIDITY",
    "ADMISSION_READY_NE_AUTHORIZED_TO_RUN",
    "EXPERIMENT_ADMISSION_NE_EFFECT_AUTHORITY",
    "UNSCOPED_SIMULATION_CLAIM_NE_TESTABLE_HYPOTHESIS",
    "TESTABILITY_CLASS_NE_EVIDENCE_ESCALATION_STATE",
    "EXPLORATORY_DISCOVERY_NE_CONFIRMATORY_VALIDATION",
    "POST_HOC_HYPOTHESIS_NE_PRECOMMITTED_TEST",
    "HOLDOUT_USED_FOR_TUNING_NE_CONFIRMATORY_HOLDOUT",
    "LINEAGE_UNKNOWN_NE_CLEAN_LINEAGE",
    "INTERNAL_REPLICATION_NE_EXTERNAL_SCIENTIFIC_REPLICATION",
    "E_LEVEL_NE_SIMULATION_PROBABILITY",
    "NULL_RESULT_FOR_SUBMODEL_NE_REFUTATION_OF_GENERIC_SIMULATION",
    "POSITIVE_RESULT_FOR_SUBMODEL_NE_EXTERNAL_SIMULATOR",
    "PROTOCOL_PASS_NE_SCIENTIFIC_VALIDATION",
    "PENDING_SOURCE_INPUT_NE_REVIEWED_DEPENDENCY",
    "INVALID_EXPERIMENT_NE_FALSE_HYPOTHESIS",
}

EXPECTED_PACKET_FIELDS = {
    "PACKET_SCHEMA_VERSION",
    "EXPERIMENT_LABEL",
    "MODE",
    "RESEARCH_STAGE",
    "TESTABILITY_CLASS",
    "TARGET_MODEL",
    "RIVAL_SET",
    "OBSERVABLE_PREDICTIONS",
    "NULL_PREDICTION",
    "FALSIFIER_OR_NONFALSIFIABLE_STATUS",
    "ASSUMPTION_REGISTER",
    "STUDY_SUBJECT_DIGEST_OR_ANALYTIC_SCOPE",
    "LINEAGE_STATE",
    "PREDECESSOR_STUDY_BINDINGS",
    "PARTITION_PLAN",
    "HOLDOUT_CUSTODY_PLAN",
    "CHALLENGE_CUSTODY_PLAN",
    "EXECUTION_SUBJECT_BINDING",
    "PRIMARY_ENDPOINT",
    "SCORING_RULE",
    "THRESHOLD_OR_DECISION_BOUNDARY",
    "SAMPLE_SIZE_OR_STOPPING_RULE",
    "MULTIPLE_COMPARISON_RULE",
    "EXCLUSION_AND_INVALIDITY_RULES",
    "AGGREGATION_UNIT",
    "INDEPENDENCE_UNIT",
    "BLINDING_AND_SHAM_CONTROLS",
    "TOOL_NETWORK_CHANNEL_AUDIT",
    "KILL_TESTS",
    "DATA_AND_EVIDENCE_PROVENANCE_PLAN",
    "INTERPRETATION_CEILING",
    "RESULT_STATE_SCHEMA",
    "AUTHORITY_BOUNDARY",
}

EXPECTED_FREEZE = {
    "EXACT_SYSTEM_SUBJECT",
    "PRIMARY_ENDPOINT",
    "SCORING_RULE",
    "THRESHOLD_OR_DECISION_BOUNDARY",
    "SAMPLE_SIZE_OR_STOPPING_RULE",
    "MULTIPLE_COMPARISON_RULE",
    "EXCLUSION_AND_INVALIDITY_RULES",
    "AGGREGATION_UNIT",
    "INDEPENDENCE_UNIT",
    "NULL_AND_RIVAL_SET",
    "HOLDOUT_PARTITION",
}

EXPECTED_TESTABILITY_FIELDS = {
    "EXACT_CLASS_S0_TO_S6",
    "EXPLICIT_TARGET_MODEL",
    "EXACT_RIVAL_SET",
    "SOURCE_AND_EVIDENCE_PROVENANCE",
    "OBSERVABLE_PREDICTION",
    "NULL_PREDICTION",
    "FALSIFIER_OR_EXPLICIT_NONFALSIFIABLE_STATUS",
    "PARENT_PHYSICS_ASSUMPTIONS",
    "RENDERING_ASSUMPTIONS",
    "INDEPENDENCE_AND_CUSTODY_PLAN",
    "STATISTICAL_PLAN",
    "INTERPRETATION_CEILING",
    "NON_OVERCLAIMING_RESULT_STATES",
}

EXPECTED_REJECT_CRITERIA = {
    "SOMETHING_WEIRD_HAPPENS",
    "SUBJECTIVE_MEANING",
    "POST_HOC_COMPUTATIONAL_RESEMBLANCE",
    "SIMULATION_BY_LABEL_ONLY",
}

EXPECTED_RIVALS = {
    "H0_RANDOM_VARIATION",
    "H1_MULTIPLE_COMPARISON_SELECTION",
    "H2_PROMPT_OR_CONTEXT_LEAKAGE",
    "H3_MEMORY_OR_RETRIEVAL_LEAKAGE",
    "H4_TRAINING_OR_PRIOR_KNOWLEDGE",
    "H5_OPERATOR_CUEING_OR_SELECTION",
    "H6_SOFTWARE_DEFECT_OR_HIDDEN_STATE",
    "H7_PROVIDER_CACHE_ROUTING_OR_TOOL_ARTIFACT",
    "H8_TIMING_OR_SYNCHRONIZATION_ARTIFACT",
    "H9_SHARED_SOURCE_OR_MODEL_LINEAGE",
    "H10_INSTRUMENTATION_OR_DATA_PIPELINE_ERROR",
    "H11_ORDINARY_EXTERNAL_INFORMATION_CHANNEL",
    "H12_UNKNOWN_ORDINARY_MECHANISM",
    "H13_AGENCY_WITHIN_KNOWN_SYSTEM_BOUNDARY",
    "H14_EXTERNAL_SOURCE_OR_AGENCY_HYPOTHESIS",
    "H15_CONTACT_HYPOTHESIS",
}

EXPECTED_KILL_TESTS = {
    "METADATA_ONLY_LEAKAGE",
    "PROMPT_CONTEXT_SCRUB",
    "MEMORY_RETRIEVAL_ISOLATION",
    "TOOL_NETWORK_ISOLATION",
    "SHAM_CHALLENGE",
    "CHALLENGE_PERMUTATION",
    "TIME_SHIFT",
    "OPERATOR_BLIND",
    "MODEL_LINEAGE_CONTROL",
    "ANALYSIS_PERMUTATION",
    "REPLAY_CACHE_PROBE",
    "FRESH_SEALED_HOLDOUT",
    "IMPLEMENTATION_ABLATION",
    "NEGATIVE_TRANSFER",
    "INDEPENDENT_CUSTODY_REPLICATION",
}

EXPECTED_E7_MINIMUM = {
    "SEALED_NOVEL_CHALLENGE",
    "PRECOMMITTED_OBJECTIVE_RESPONSE_CRITERION",
    "TWO_WAY_CONTINGENCY",
    "ANTI_REPLAY_NONCE_OR_CHALLENGE_ID",
    "ORDINARY_CHANNEL_AUDIT",
    "NEGATIVE_AND_SHAM_CONTROLS",
    "FRESH_SEALED_REPLICATION",
    "INDEPENDENT_CHALLENGE_CUSTODY",
}

EXPECTED_INVALIDITY = {
    "CHALLENGE_LEAKED_PRE_REVEAL",
    "MATERIAL_SUBJECT_CHANGED_WITHOUT_NEW_SUBJECT_RELATION",
    "SCORING_CHANGED_POST_OUTCOME",
    "EXCLUSION_CHANGED_POST_HOC",
    "HOLDOUT_USED_FOR_TUNING",
    "EXPLORATORY_DATA_REUSED_AS_CONFIRMATORY_HOLDOUT",
    "REQUIRED_RAW_EVIDENCE_MISSING",
    "TIMING_ORDER_UNRESOLVED_FOR_TIMING_CLAIM",
    "EXECUTION_SUBJECT_CHANGED_WITHOUT_NEW_BINDING",
    "UNAUDITED_CHANNEL_COULD_CONTAIN_CHALLENGE",
    "SUCCESSFUL_TRIAL_SELECTION",
    "EVIDENCE_LINEAGE_UNRECONSTRUCTABLE",
    "CRITICAL_LOGS_MISSING_OR_ALTERED",
    "LINEAGE_UNKNOWN_PROMOTED_TO_CLEAN",
    "TESTABILITY_CLASS_CHANGED_POST_RESULT",
    "INTERPRETATION_CEILING_RAISED_POST_RESULT",
    "EXTERNAL_REPLICATION_WITHOUT_REQUIRED_INDEPENDENCE",
}

EXPECTED_DISPOSITIONS = {
    "ANALYTIC_ONLY",
    "EXPLORATORY_ONLY",
    "CONFIRMATORY_DESIGN_INCOMPLETE",
    "BLOCKED_TESTABILITY",
    "BLOCKED_LINEAGE_UNKNOWN",
    "BLOCKED_PROVENANCE_OR_CUSTODY",
    "CONFIRMATORY_READY_FOR_SEAL",
    "EXTERNAL_REPLICATION_DESIGN_READY",
}

EXPECTED_HOSTILE = {
    "S4_SUBMITTED_AS_DISCRIMINATING_EMPIRICAL_TEST",
    "S3_WITHOUT_RISKY_PREDICTION",
    "S6_SELF_ASSERTION_ONLY_AUTHENTICATION",
    "WEIRDNESS_AS_SUCCESS_CRITERION",
    "EXPLORATORY_DATA_REUSED_AS_CONFIRMATORY_HOLDOUT",
    "POST_OUTCOME_SCORING_CHANGE",
    "MISSING_STOPPING_RULE",
    "MISSING_MULTIPLE_COMPARISON_RULE",
    "LINEAGE_UNKNOWN_CLAIMS_CLEAN_CONFIRMATION",
    "NEW_LABEL_OR_DIGEST_CLAIMS_CLEAN_ROOT",
    "HOLDOUT_CONTENT_REPACKAGED",
    "ORDINARY_RIVAL_OMITTED",
    "UNAUDITED_TOOL_NETWORK_CHANNEL",
    "SHARED_MODEL_LINEAGE_COUNTED_INDEPENDENT",
    "INTERNAL_REPLICATION_RELABELLED_EXTERNAL",
    "EXPLORATORY_ESCALATES_ABOVE_E1",
    "INTERNAL_CONFIRMATORY_ESCALATES_TO_E8",
    "E7_WITHOUT_INDEPENDENT_CUSTODY",
    "POSITIVE_S1_RELABELLED_EXTERNAL_SIMULATOR",
    "NULL_SUBMODEL_RESULT_RELABELLED_GENERIC_REFUTATION",
    "ADMISSION_PASS_RELABELLED_RUN_AUTHORITY",
    "PENDING_LINEAGE_SOURCE_PROMOTED_TO_REVIEWED",
    "INVALID_EXPERIMENT_RELABELLED_FALSE_HYPOTHESIS",
    "POST_RESULT_INTERPRETATION_CEILING_RAISED",
}

EXPECTED_CEILING = {
    "NO_DATA_COLLECTION_AUTHORITY",
    "NO_EXPERIMENT_EXECUTION_AUTHORITY",
    "NO_PROVIDER_TOOL_OR_PROJECT_EFFECT_AUTHORITY",
    "NO_RESULT_VALIDITY_CLAIM",
    "NO_HOLDOUT_NONACCESS_PROOF",
    "NO_STATISTICAL_INDEPENDENCE_PROOF",
    "NO_COMPLETE_STUDY_LINEAGE_DISCOVERY",
    "NO_SEMANTIC_EQUIVALENCE_PROOF",
    "NO_SIMULATION_PROBABILITY_ASSIGNMENT",
    "NO_ANOMALY_CLAIM",
    "NO_AGENCY_CLAIM",
    "NO_EXTERNAL_CONTACT_CLAIM",
    "NO_SIMULATOR_IDENTITY_CLAIM",
    "NO_DEITY_IDENTITY_CLAIM",
    "NO_EXTERNAL_SCIENTIFIC_VALIDATION_CLAIM",
    "NO_MERGE_AUTHORITY",
    "NO_DEPLOYMENT_AUTHORITY",
    "NO_CANONICAL_PROMOTION",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root must be object")
    return value


def _exact_set(errors: list[str], value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be list")
        return
    if len(value) != len(set(value)):
        errors.append(f"{label} must not contain duplicates")
    if set(value) != expected:
        errors.append(f"{label} must be exact closed set")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (DOC_PATH, SPEC_PATH):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        spec = _load(root / SPEC_PATH)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid experiment-admission architecture: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_EXPERIMENT_ADMISSION_ARCHITECTURE_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_ARCHITECTURE":
        errors.append("status must remain RESEARCH_ARCHITECTURE")
    if spec.get("repository") != "thebrazenbeard/god-brain":
        errors.append("repository drifted")
    if spec.get("event_id") != "GB_DG_TRIAD_20260921_V1":
        errors.append("event id drifted")
    if spec.get("base_head") != "c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5":
        errors.append("base head drifted")

    expected_sources = [
        {
            "source_pr": 26,
            "exact_head": "dd579e79190a53bba998d70be1c4d2179c213aaf",
            "path": "specs/research/GOD_BRAIN_SIMULATION_TESTABILITY_BOUNDARY_V0_1.json",
            "review_state": "ACCEPT_SOURCE_RESEARCH_ONLY",
        },
        {
            "source_pr": 25,
            "exact_head": "d71f590eb7117f746ae7d3d761e3428a82ff5102",
            "path": "specs/research/GOD_BRAIN_ANOMALY_CONTACT_EVIDENCE_PROTOCOL_V0_1.json",
            "review_state": "ACCEPT_SOURCE_RESEARCH_ONLY",
        },
        {
            "source_pr": 29,
            "exact_head": "4095d0772412a4f03a7f54c5c13a8c3212fdcc45",
            "path": "specs/research/GOD_BRAIN_CONFIRMATORY_STUDY_LINEAGE_V0_1.json",
            "review_state": "PENDING_EXACT_HEAD_REVIEW_PROVISIONAL_INPUT",
        },
    ]
    if spec.get("source_inputs") != expected_sources:
        errors.append("source input bindings drifted")
    else:
        for item in spec["source_inputs"]:
            if not SHA40.fullmatch(item["exact_head"]):
                errors.append("source exact head must be lowercase 40-hex")

    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    _exact_set(errors, spec.get("required_packet_fields"), EXPECTED_PACKET_FIELDS, "required packet fields")
    _exact_set(errors, spec.get("confirmatory_freeze_required"), EXPECTED_FREEZE, "confirmatory freeze")
    _exact_set(errors, spec.get("admission_dispositions"), EXPECTED_DISPOSITIONS, "admission dispositions")
    _exact_set(errors, spec.get("required_hostile_cases"), EXPECTED_HOSTILE, "required hostile cases")
    _exact_set(errors, spec.get("claim_ceiling"), EXPECTED_CEILING, "claim ceiling")

    gate = spec.get("testability_gate")
    if not isinstance(gate, dict):
        errors.append("testability_gate must be object")
        gate = {}
    if gate.get("classes") != ["S0", "S1", "S2", "S3", "S4", "S5", "S6"]:
        errors.append("testability classes drifted")
    expected_dispositions = {
        "S0": "ANALYTIC_ONLY_NO_DIRECT_EMPIRICAL_DETECTOR",
        "S1": "NAMED_SUBMODEL_EMPIRICAL_TEST",
        "S2": "ASSUMPTION_BOUND_CONSTRAINT_TEST",
        "S3": "REJECT_UNLESS_RISKY_PREDICTION",
        "S4": "NO_INTERNAL_DISCRIMINATING_EXPERIMENT",
        "S5": "BOUNDED_INTERVENTION_TEST_ONTOLOGY_UNDERDETERMINED",
        "S6": "IDENTITY_AUTHENTICATION_PROTOCOL_REQUIRED",
    }
    if gate.get("class_dispositions") != expected_dispositions:
        errors.append("testability class dispositions drifted")
    _exact_set(errors, gate.get("required_fields"), EXPECTED_TESTABILITY_FIELDS, "testability required fields")
    _exact_set(errors, gate.get("reject_if_success_criterion"), EXPECTED_REJECT_CRITERIA, "rejected success criteria")

    modes = spec.get("modes")
    if not isinstance(modes, dict):
        errors.append("modes must be object")
        modes = {}
    if set(modes) != {"ANALYTIC_ONLY", "EXPLORATORY", "INTERNAL_CONFIRMATORY", "EXTERNAL_REPLICATION"}:
        errors.append("mode set drifted")
    if isinstance(modes.get("EXPLORATORY"), dict):
        if modes["EXPLORATORY"].get("absolute_escalation_ceiling") != "E1":
            errors.append("exploratory ceiling must remain E1")
        if modes["EXPLORATORY"].get("discovery_data_may_be_confirmatory_holdout") is not False:
            errors.append("exploratory data cannot become confirmatory holdout")
    if isinstance(modes.get("INTERNAL_CONFIRMATORY"), dict):
        expected_internal = {
            "requires_confirmatory_lineage": True,
            "requires_fresh_holdout": True,
            "absolute_escalation_ceiling": "E7",
        }
        if modes["INTERNAL_CONFIRMATORY"] != expected_internal:
            errors.append("internal confirmatory requirements drifted")
    if isinstance(modes.get("EXTERNAL_REPLICATION"), dict):
        if modes["EXTERNAL_REPLICATION"].get("absolute_escalation_ceiling") != "E8":
            errors.append("external replication ceiling must remain E8")
        for key in ("requires_independent_investigators", "requires_independent_challenge_material", "requires_separately_implemented_instrumentation"):
            if modes["EXTERNAL_REPLICATION"].get(key) is not True:
                errors.append(f"external replication missing {key}")

    lineage = spec.get("lineage_gate")
    expected_lineage = {
        "provisional_source_pr": 29,
        "provisional_source_head": "4095d0772412a4f03a7f54c5c13a8c3212fdcc45",
        "later_stage_requires_review_clean_successor": True,
        "clean_confirmation_disallowed_when_lineage_unknown": True,
        "exploratory_data_may_be_reused_as_confirmatory_holdout": False,
        "new_label_or_digest_proves_clean_root": False,
        "study_subject_digest_proves_semantic_equivalence": False,
    }
    if lineage != expected_lineage:
        errors.append("lineage gate drifted")

    _exact_set(errors, spec.get("required_rival_hypotheses"), EXPECTED_RIVALS, "required rival hypotheses")
    _exact_set(errors, spec.get("mandatory_kill_tests"), EXPECTED_KILL_TESTS, "mandatory kill tests")
    _exact_set(errors, spec.get("invalidity_conditions"), EXPECTED_INVALIDITY, "invalidity conditions")

    escalation = spec.get("escalation_gate")
    if not isinstance(escalation, dict):
        errors.append("escalation gate must be object")
        escalation = {}
    expected_states = [
        "E0_BASELINE_NO_ANOMALY",
        "E1_CANDIDATE_ANOMALY",
        "E2_REPRODUCIBLE_ANOMALY",
        "E3_MODEL_DISCRIMINATING_ANOMALY",
        "E4_CONTINGENT_RESPONSE_CANDIDATE",
        "E5_AGENCY_HYPOTHESIS_CANDIDATE",
        "E6_EXTERNAL_SOURCE_HYPOTHESIS_CANDIDATE",
        "E7_CONTACT_HYPOTHESIS_CANDIDATE",
        "E8_EXTERNAL_SCIENTIFIC_REPLICATION_CANDIDATE",
    ]
    if escalation.get("states") != expected_states:
        errors.append("escalation states drifted")
    if escalation.get("escalation_rule") != "ESCALATION_REQUIRES_NEW_DISCRIMINATING_EVIDENCE":
        errors.append("escalation rule drifted")
    if escalation.get("deescalation_rule") != "CHEAPER_SUFFICIENT_ORDINARY_EXPLANATION_FORCES_DOWNGRADE":
        errors.append("deescalation rule drifted")
    _exact_set(errors, escalation.get("e7_minimum"), EXPECTED_E7_MINIMUM, "E7 minimum controls")
    if escalation.get("e8_requirement") != "INDEPENDENT_INVESTIGATORS_INDEPENDENT_CHALLENGE_MATERIAL_SEPARATELY_IMPLEMENTED_INSTRUMENTATION":
        errors.append("E8 requirement drifted")
    if escalation.get("e8_claim_ceiling") != "DOES_NOT_UNIQUELY_ESTABLISH_METAPHYSICAL_IDENTITY":
        errors.append("E8 claim ceiling drifted")

    if spec.get("research_stage") != "ARCHITECTURE":
        errors.append("research stage must remain ARCHITECTURE")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "ADMISSION_PACKET_PASS != RESULT_VALIDITY",
        "ADMISSION_READY != AUTHORIZED_TO_RUN",
        "EXPLORATORY_DISCOVERY != CONFIRMATORY_VALIDATION",
        "LINEAGE_UNKNOWN != CLEAN_LINEAGE",
        "E_LEVEL != SIMULATION_PROBABILITY",
        "NULL_RESULT_FOR_SUBMODEL != REFUTATION_OF_GENERIC_SIMULATION",
        "POSITIVE_RESULT_FOR_SUBMODEL != EXTERNAL_SIMULATOR",
        "PENDING_SOURCE_INPUT != REVIEWED_DEPENDENCY",
        "INVALID_EXPERIMENT != FALSE_HYPOTHESIS",
    ):
        if marker not in doc:
            errors.append(f"research doc missing marker: {marker}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain experiment-admission architecture: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
