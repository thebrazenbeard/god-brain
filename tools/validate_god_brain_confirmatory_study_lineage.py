from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_CONFIRMATORY_STUDY_LINEAGE_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_CONFIRMATORY_STUDY_LINEAGE_V0_1.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_INVARIANTS = {
    "STUDY_LABEL_NE_STUDY_IDENTITY",
    "DISCLOSED_PREDECESSOR_ATTEMPTS_NE_SAME_CONFIRMATORY_STUDY_SUBJECT",
    "CORPUS_IDENTITY_NONREUSE_NE_HOLDOUT_CONTENT_NONREUSE",
    "REDESIGN_AFTER_HOLDOUT_EXPOSURE_NE_UNTOUCHED_CONFIRMATION",
    "FAILED_OR_ABORTED_ATTEMPT_NE_DISAPPEARED_ATTEMPT",
    "HOLDOUT_METADATA_CHANGED_NE_HOLDOUT_CONTENT_NEW",
    "CONTENT_NONREUSE_NE_PROVENANCE_CONTINUITY",
    "REVEAL_AUTHORITY_IS_SINGLE_USE",
    "EXECUTION_AUTHORITY_IS_SINGLE_USE",
    "AMBIGUOUS_EXECUTION_NE_SAFE_TO_RETRY",
    "VALID_RECEIPT_NE_VALID_FOR_THIS_SUBJECT",
    "DIGEST_NONREUSE_NE_STATISTICAL_INDEPENDENCE",
    "DURABLE_LINEAGE_NE_EXTERNAL_CUSTODY",
    "GOVERNED_CONFIRMATORY_PASS_NE_ANOMALY",
    "ANOMALY_NE_CONTACT",
    "CONTACT_CANDIDATE_NE_SIMULATOR_IDENTITY",
    "PROTOCOL_RIGOR_NE_UNIQUE_CAUSAL_EXPLANATION",
    "DISPLAY_METADATA_CHANGED_NE_STUDY_SUBJECT_CHANGED",
    "NONCANONICAL_SERIALIZATION_CHANGED_NE_SCIENTIFIC_SUBJECT_CHANGED",
    "STUDY_SUBJECT_DIGEST_NE_SEMANTIC_EQUIVALENCE_PROOF",
    "NEW_STUDY_SUBJECT_DIGEST_NE_CLEAN_NEW_LINEAGE",
    "UNLINKED_ROOT_NE_INDEPENDENT_STUDY",
    "NEW_LABEL_NE_NEW_LINEAGE",
    "PRE_EXPOSURE_REVISION_NE_SAME_SUBJECT_ATTEMPT",
    "POST_EXPOSURE_REDESIGN_NE_UNTOUCHED_CONFIRMATION",
}

EXPECTED_SUBJECT_FIELDS = {
    "SCHEMA_VERSION",
    "EVIDENTIARY_QUESTION",
    "MEASURED_SUBJECT_DEFINITION",
    "PORTFOLIO_DIGEST",
    "CANDIDATE_IDENTITIES_AND_DIGESTS",
    "SPECIFICATION_DIGESTS",
    "POLICIES_AND_ACCEPTANCE_CRITERIA",
    "METRIC_EVALUATION_CONTRACT",
    "SELECTION_OR_NONPROMOTION_RULE",
    "EXECUTION_SUBJECT_POLICY",
    "DATA_PARTITION_POLICY",
    "CLAIM_CEILING",
    "PROVENANCE_ROOTS",
}

EXPECTED_HOLDOUT_FIELDS = {
    "CORPUS_IDENTITY_DIGEST",
    "CANONICAL_ARTIFACT_DIGEST",
    "OBSERVATION_CONTENT_DIGEST",
    "SOURCE_PROVENANCE_BINDING",
    "REVEAL_RECEIPT_DIGEST",
    "EXECUTION_RECEIPT_DIGEST",
}

EXPECTED_HOSTILE = {
    "HOLDOUT_CONTENT_RELABELED_CORPUS",
    "HOLDOUT_CONTENT_REPACKAGED_ARTIFACT",
    "STUDY_RELABEL_RESETS_ANCESTRY",
    "SAME_SUBJECT_TWO_LABELS_SPLIT_ANCESTRY",
    "SAME_STUDY_CHANGED_CANDIDATES",
    "SAME_STUDY_CHANGED_ACCEPTANCE_CRITERIA",
    "SAME_STUDY_CHANGED_PORTFOLIO",
    "SAME_STUDY_CHANGED_SPECIFICATION",
    "REDESIGN_AFTER_EXPOSURE_MISLABELED_CONFIRMATION",
    "MISSING_PREDECESSOR_ATTEMPT",
    "MISSING_PREDECESSOR_HOLDOUT_CONTENT",
    "REVEAL_REPLAY",
    "EXECUTION_REPLAY",
    "AMBIGUOUS_EXECUTION_OPERATOR_RETRY",
    "CROSS_STUDY_RECEIPT",
    "CROSS_ATTEMPT_RECEIPT",
    "CONTENT_NONREUSE_PROMOTED_TO_INDEPENDENCE",
    "PROTOCOL_PASS_PROMOTED_TO_EXTERNAL_SCIENTIFIC_VALIDATION",
    "CANONICAL_PAYLOAD_REORDERED_NEW_DIGEST",
    "DISPLAY_METADATA_CHANGES_STUDY_IDENTITY",
    "PARAPHRASED_EQUIVALENT_QUESTION_CLAIMS_CLEAN_ROOT",
    "UNLINKED_NEW_ROOT_CLAIMS_INDEPENDENCE",
    "POST_EXPOSURE_REDESIGN_OMITS_CHANGED_FIELDS",
    "PRE_EXPOSURE_REVISION_MISLABELED_SAME_SUBJECT",
}

EXPECTED_CEILING = {
    "NO_RUNTIME_LEDGER_IMPLEMENTATION",
    "NO_EXPERIMENT_EXECUTION",
    "NO_DETECTOR_OR_MODEL_QUALIFICATION",
    "NO_HOLDOUT_NONACCESS_PROOF",
    "NO_TRUSTED_TIME_PROOF",
    "NO_STATISTICAL_INDEPENDENCE_PROOF",
    "NO_EXTERNAL_CUSTODY_PROOF",
    "NO_HIDDEN_HISTORY_COMPLETENESS_PROOF",
    "NO_STATISTICAL_SIGNIFICANCE_CLAIM",
    "NO_CAUSAL_TRUTH_CLAIM",
    "NO_PRODUCTION_SUPERIORITY",
    "NO_ANOMALY_CLAIM",
    "NO_EXTERNAL_CONTACT_CLAIM",
    "NO_SIMULATION_EVIDENCE_CLAIM",
    "NO_PROVIDER_OR_CONTROL_AUTHORITY",
    "NO_MERGE_AUTHORITY",
    "NO_DEPLOYMENT_AUTHORITY",
    "NO_CANONICAL_PROMOTION",
    "NO_SEMANTIC_EQUIVALENCE_PROOF",
    "NO_COMPLETE_LINEAGE_ROOT_DISCOVERY",
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
        return [f"invalid confirmatory study-lineage spec: {exc}"]

    if spec.get("schema_version") != "GOD_BRAIN_CONFIRMATORY_STUDY_LINEAGE_V0_1":
        errors.append("schema_version drifted")
    if spec.get("status") != "RESEARCH_ARCHITECTURE":
        errors.append("status drifted")
    if spec.get("god_brain_base_head") != "c0f6af7143aa5916bae96eb1f0ee9c9de6505cf5":
        errors.append("God Brain base drifted")
    if spec.get("event_id") != "GB_DG_TRIAD_20260921_V1":
        errors.append("event id drifted")

    source = spec.get("triggering_source")
    expected_source = {
        "repository": "thebrazenbeard/driftguard",
        "source_pr": 34,
        "exact_head": "351b7a57b7213bd72cf881aa2bbaa449fb0fbc8f",
        "observations": ["5762590813", "5762641946", "5762703839"],
        "source_use": "HOSTILE_BLOCKER_EVIDENCE_ONLY",
    }
    if source != expected_source:
        errors.append("triggering source binding drifted")
    if isinstance(source, dict):
        head = source.get("exact_head")
        if not isinstance(head, str) or not SHA40.fullmatch(head):
            errors.append("triggering source head must be lowercase 40-hex")

    identity = spec.get("identity")
    if not isinstance(identity, dict):
        errors.append("identity must be object")
        identity = {}
    if identity.get("rule") != "STUDY_SUBJECT_DIGEST_IS_DURABLE_STUDY_IDENTITY":
        errors.append("study identity rule drifted")
    if identity.get("display_label_is_identity") is not False:
        errors.append("display label must not be identity")
    _exact_set(errors, identity.get("required_subject_fields"), EXPECTED_SUBJECT_FIELDS, "required_subject_fields")

    canonical = spec.get("canonical_subject_digest")
    expected_canonical = {
        "algorithm": "SHA-256",
        "serialization_profile": "RFC8785_JCS",
        "canonicalize_semantically_unordered_collections": True,
        "unordered_collection_fields": [
            "CANDIDATE_IDENTITIES_AND_DIGESTS",
            "SPECIFICATION_DIGESTS",
            "PROVENANCE_ROOTS",
        ],
        "unordered_collection_order": "LEXICOGRAPHIC_UTF8_BY_RFC8785_CANONICAL_ELEMENT_BYTES",
        "validate_types_before_hashing": True,
        "excluded_nonsubject_metadata": [
            "DISPLAY_LABEL",
            "OBSERVED_AT",
            "BRANCH_NAME",
            "ATTEMPT_ID",
            "REPOSITORY_PATH_ALIAS",
        ],
        "digest_is_semantic_equivalence_proof": False,
    }
    if canonical != expected_canonical:
        errors.append("canonical subject digest contract drifted")

    registry = spec.get("lineage_registry")
    expected_registry = {
        "required": True,
        "states": [
            "KNOWN_LINEAGE",
            "NEW_ROOT_PENDING_EQUIVALENCE_CHECK",
            "ANCESTRY_UNKNOWN",
        ],
        "new_digest_establishes_clean_root": False,
        "unlinked_root_establishes_independence": False,
        "new_root_requires_governed_admission": True,
        "complete_hidden_history_discovery_claim": False,
    }
    if registry != expected_registry:
        errors.append("lineage registry contract drifted")

    successors = spec.get("successor_classes")
    if not isinstance(successors, dict) or set(successors) != {"SAME_SUBJECT_ATTEMPT", "SUCCESSOR_REDESIGN"}:
        errors.append("successor classes must be exact")
    else:
        same = successors["SAME_SUBJECT_ATTEMPT"]
        redesign = successors["SUCCESSOR_REDESIGN"]
        if same != {
            "requires_exact_study_subject_digest_match": True,
            "inherits_attempt_ancestry": True,
            "inherits_holdout_content_ancestry": True,
            "inherits_evidence_exposure": True,
        }:
            errors.append("same-subject semantics drifted")
        if redesign != {
            "requires_new_study_subject_digest": True,
            "requires_predecessor_study_relation": True,
            "requires_redesign_reason": True,
            "preserves_prior_evidence_exposure": True,
            "may_claim_untouched_confirmation_of_predecessor": False,
        }:
            errors.append("successor-redesign semantics drifted")

    timing = spec.get("change_timing_classes")
    expected_timing = {
        "PRE_EXPOSURE_SUBJECT_REVISION": {
            "requires_new_study_subject_digest": True,
            "requires_predecessor_study_relation": True,
            "preserves_precommit_history": True,
            "inherits_holdout_exposure": False,
        },
        "POST_EXPOSURE_REDESIGN": {
            "requires_new_study_subject_digest": True,
            "requires_predecessor_study_relation": True,
            "requires_changed_field_disclosure": True,
            "preserves_prior_evidence_exposure": True,
            "may_claim_untouched_confirmation_of_predecessor": False,
        },
    }
    if timing != expected_timing:
        errors.append("change-timing semantics drifted")

    _exact_set(errors, spec.get("holdout_ancestry_required_fields"), EXPECTED_HOLDOUT_FIELDS, "holdout ancestry fields")
    _exact_set(errors, spec.get("invariants"), EXPECTED_INVARIANTS, "invariants")
    _exact_set(errors, spec.get("required_hostile_cases"), EXPECTED_HOSTILE, "required hostile cases")
    _exact_set(errors, spec.get("claim_ceiling"), EXPECTED_CEILING, "claim ceiling")

    if spec.get("research_stage") != "ARCHITECTURE":
        errors.append("research stage must remain ARCHITECTURE")

    doc = (root / DOC_PATH).read_text(encoding="utf-8")
    for marker in (
        "STUDY_LABEL != STUDY_IDENTITY",
        "CORPUS_IDENTITY_NONREUSE != HOLDOUT_CONTENT_NONREUSE",
        "REDESIGN_AFTER_HOLDOUT_EXPOSURE != UNTOUCHED_CONFIRMATION",
        "HOLDOUT_METADATA_CHANGED != HOLDOUT_CONTENT_NEW",
        "AMBIGUOUS_EXECUTION != SAFE_TO_RETRY",
        "VALID_RECEIPT != VALID_FOR_THIS_SUBJECT",
        "DIGEST_NONREUSE != STATISTICAL_INDEPENDENCE",
        "GOVERNED_CONFIRMATORY_PASS != ANOMALY",
        "STUDY_SUBJECT_DIGEST != SEMANTIC_EQUIVALENCE_PROOF",
        "NEW_STUDY_SUBJECT_DIGEST != CLEAN_NEW_LINEAGE",
        "UNLINKED_ROOT != INDEPENDENT_STUDY",
        "POST_EXPOSURE_REDESIGN != UNTOUCHED_CONFIRMATION",
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
    print("God Brain confirmatory study-lineage contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
