from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DOC_PATH = "docs/research/GOD_BRAIN_ADVERSARIAL_REVIEW_LAYER_V0_1.md"
SPEC_PATH = "specs/research/GOD_BRAIN_ADVERSARIAL_REVIEW_LAYER_V0_1.json"
FIXTURE_PATH = "specs/research/fixtures/GOD_BRAIN_ADVERSARIAL_REVIEW_HOSTILE_CASES_V0_1.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_INVARIANTS = {
    "REVIEW_NE_TRUTH","SELF_REVIEW_NE_INDEPENDENT_REVIEW","DISAGREEMENT_NE_ERROR",
    "CRITIQUE_NE_AUTHORITY","BLOCKER_FINDING_NE_EFFECT_AUTHORITY","POLICY_LITERALISM_NE_INTENDED_OUTCOME",
    "RIVAL_HYPOTHESIS_NE_FALSE_EQUIVALENCE","MODEL_CONFIDENCE_NE_EVIDENCE",
    "PASS_NE_CANONICAL_PROMOTION","PASS_NE_MERGE_AUTHORITY","PASS_NE_DEPLOYMENT_AUTHORITY",
    "HEAD_MOVEMENT_STALES_EXACT_SUBJECT_REVIEW","COPIED_FINDING_NE_INDEPENDENT_CORROBORATION",
    "REVIEWER_PERSONA_NE_REVIEWER_INDEPENDENCE",
}
EXPECTED_LANES = {"constraint_loophole","candidate_integrity","forensic_falsification","regression_root_cause"}
EXPECTED_RULES = {
    "EVERY_FINDING_MUST_BIND_EXACT_SUBJECT",
    "EVERY_MATERIAL_FINDING_MUST_CITE_EVIDENCE_OR_REPRODUCTION",
    "BLOCKER_MUST_NAME_EXISTING_INVARIANT_OR_VERIFIABLE_FAILURE",
    "LOOPHOLE_FINDING_MUST_INCLUDE_LITERAL_PATH_AND_PROTECTED_INTENT",
    "CANDIDATE_REVIEW_MUST_PRESERVE_LITERAL_USER_PROPOSITION",
    "FORENSIC_REVIEW_MUST_KEEP_LIVE_RIVALS_WHEN_EVIDENCE_DOES_NOT_DISCRIMINATE",
    "ROOT_CAUSE_MUST_DISTINGUISH_REPRODUCTION_FROM_CAUSAL_EXPLANATION",
    "REVIEW_PASS_MUST_NOT_GRANT_PROMOTION_OR_EFFECT_AUTHORITY",
    "EXACT_HEAD_CHANGE_MAKES_PRIOR_VERDICT_HISTORICAL_ONLY",
    "INTERNAL_HOSTILE_REVIEW_MUST_NOT_BE_RELABELED_INDEPENDENT",
    "COPIED_OR_SHARED_FINDINGS_MUST_SHARE_INDEPENDENCE_FAMILY",
}
EXPECTED_CASES = {f"AR-{i:02d}" for i in range(1,13)}
EXPECTED_DONORS = {
    "thebrazenbeard/freerowcochkar":"9ea4eaefe5229ca90d7ae6099dbf30d9e13b64b2",
    "thebrazenbeard/cricket":"c2342648c72aa9faefd9c5441c654ad8239afe33",
    "thebrazenbeard/voss":"36a623d3a158e5aef521d42e378bafacd67d3de5",
    "thebrazenbeard/masamune":"25653790d59080cda0b6d6e57b8a4cd64d1ee2b5",
    "thebrazenbeard/god-brain":"495c2b42932153cba0926744d04a69bc34557f81",
}

def _load(path: Path) -> dict[str, Any]:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict): raise ValueError("root must be object")
    return value

def _exact(errors:list[str],value:Any,expected:set[str],label:str)->None:
    if not isinstance(value,list):
        errors.append(f"{label} must be list"); return
    if len(value)!=len(set(value)): errors.append(f"{label} must be unique")
    if set(value)!=expected: errors.append(f"{label} must be exact closed set")

def validate_adversarial_review(root: Path)->list[str]:
    errors:list[str]=[]
    for rel in (DOC_PATH,SPEC_PATH,FIXTURE_PATH):
        if not (root/rel).is_file(): errors.append(f"missing {rel}")
    if errors:return errors
    try:
        spec=_load(root/SPEC_PATH); fixtures=_load(root/FIXTURE_PATH)
    except (OSError,UnicodeError,json.JSONDecodeError,ValueError) as exc:
        return [f"invalid adversarial-review contract: {exc}"]

    if spec.get("schema_version")!="GOD_BRAIN_ADVERSARIAL_REVIEW_LAYER_V0_1": errors.append("schema_version drifted")
    if spec.get("status")!="RESEARCH_SPECIFICATION_NO_RUNTIME": errors.append("status must remain no-runtime research")
    if spec.get("parent_intake_head")!="41ca6320cb162bab0463ab06f57d6dce1e95256a": errors.append("parent intake head drifted")
    _exact(errors,spec.get("invariants"),EXPECTED_INVARIANTS,"invariants")
    _exact(errors,spec.get("review_rules"),EXPECTED_RULES,"review_rules")

    donors=spec.get("donor_sources")
    if not isinstance(donors,list): errors.append("donor_sources must be list"); donors=[]
    seen=set()
    for d in donors:
        if not isinstance(d,dict): errors.append("donor must be object"); continue
        repo=d.get("repository"); seen.add(repo)
        if repo not in EXPECTED_DONORS: errors.append(f"unexpected donor {repo!r}"); continue
        if d.get("ref")!="main": errors.append(f"{repo}: ref must be main")
        if d.get("exact_head")!=EXPECTED_DONORS[repo]: errors.append(f"{repo}: exact_head drifted")
        if not isinstance(d.get("exact_head"),str) or not SHA40.fullmatch(d["exact_head"]): errors.append(f"{repo}: invalid exact_head")
    if seen!=set(EXPECTED_DONORS): errors.append("donor source set drifted")

    lanes=spec.get("lanes")
    if not isinstance(lanes,dict) or set(lanes)!=EXPECTED_LANES: errors.append("review lanes must be exact closed set")
    else:
        for name,lane in lanes.items():
            if not isinstance(lane,dict): errors.append(f"{name}: lane must be object"); continue
            if not lane.get("role") or not lane.get("source") or not lane.get("output"): errors.append(f"{name}: lane fields missing")
            if not str(lane.get("authority","")).startswith("ADVISORY"): errors.append(f"{name}: lane authority must remain advisory")

    provenance=spec.get("reviewer_provenance")
    classification=spec.get("independence_classification")
    if not isinstance(provenance,list) or not isinstance(classification,dict) or set(provenance)!=set(classification):
        errors.append("reviewer provenance/classification mismatch")
    else:
        for value in ("AUTHOR_SELF","SAME_MODEL_SELF"):
            if classification.get(value)!="NOT_INDEPENDENT": errors.append(f"{value} must remain NOT_INDEPENDENT")
        if classification.get("SEPARATE_MODEL_SAME_OPERATOR_CONTEXT")!="INDEPENDENCE_UNESTABLISHED":
            errors.append("separate model same context must remain independence-unestablished")

    required_subject=set(spec.get("review_subject_required",[]))
    for field in ("repository","base_exact_head","exact_head","paths_or_artifact_ids","claim_scope","review_request_id"):
        if field not in required_subject: errors.append(f"review subject must require {field}")
    required_finding=set(spec.get("finding_required",[]))
    for field in ("finding_id","lane","severity","proposition","evidence_refs","rival_or_failure_path","recommendation","claim_ceiling"):
        if field not in required_finding: errors.append(f"finding must require {field}")

    ceiling=set(spec.get("claim_ceiling",[]))
    for guard in ("NO_MERGE_AUTHORITY","NO_DEPLOYMENT_AUTHORITY","NO_INDEPENDENCE_CLAIM_FROM_SELF_REVIEW","NO_SCIENTIFIC_VALIDATION"):
        if guard not in ceiling: errors.append(f"claim ceiling missing {guard}")

    if fixtures.get("schema_version")!="GOD_BRAIN_ADVERSARIAL_REVIEW_HOSTILE_CASES_V0_1": errors.append("fixture schema drifted")
    cases=fixtures.get("cases")
    if not isinstance(cases,list): errors.append("cases must be list"); cases=[]
    ids=[x.get("id") for x in cases if isinstance(x,dict)]
    if set(ids)!=EXPECTED_CASES or len(ids)!=12: errors.append("hostile cases must be exactly AR-01..AR-12")
    for case in cases:
        if not isinstance(case,dict): continue
        if case.get("lane") not in EXPECTED_LANES: errors.append(f"{case.get('id')}: unknown lane")
        guards=case.get("guards")
        if not isinstance(guards,list) or not guards: errors.append(f"{case.get('id')}: guards missing"); continue
        for guard in guards:
            if guard not in EXPECTED_RULES: errors.append(f"{case.get('id')}: unknown guard {guard}")

    doc=(root/DOC_PATH).read_text(encoding="utf-8")
    for marker in ("REVIEW != TRUTH","SELF_REVIEW != INDEPENDENT_REVIEW","DISAGREEMENT != ERROR","CRITIQUE != AUTHORITY","PASS != MERGE_AUTHORITY","PASS != DEPLOYMENT_AUTHORITY","BEST_AMONG_DECLARED_RIVALS != UNIQUE_CAUSAL_EXPLANATION"):
        if marker not in doc: errors.append(f"doc missing marker: {marker}")
    return errors

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--root",default="."); args=parser.parse_args()
    errors=validate_adversarial_review(Path(args.root).resolve())
    if errors:
        for error in errors: print(f"FAIL: {error}")
        return 1
    print("God Brain adversarial review layer V0.1: PASS"); return 0

if __name__=="__main__": raise SystemExit(main())
