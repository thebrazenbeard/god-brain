from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

DOC_PATH="docs/research/GOD_BRAIN_SEMANTIC_MEDIATION_V0_1.md"
SPEC_PATH="specs/research/GOD_BRAIN_SEMANTIC_MEDIATION_V0_1.json"
FIXTURE_PATH="specs/research/fixtures/GOD_BRAIN_SEMANTIC_MEDIATION_HOSTILE_CASES_V0_1.json"
SHA40=re.compile(r"^[0-9a-f]{40}$")
EXPECTED_DONORS={
 "thebrazenbeard/sql-connectome":"b609fcec50fe5a135ca1d8139f5563f5631582b2",
 "thebrazenbeard/spm":"d9ea72798ac892ac75f858177b6ed0c5a6b4c37c",
 "thebrazenbeard/semiotics":"37117a2097f7f2aa35968fc9db24eacf7240826e",
}
EXPECTED_FIDELITY=["EXACT","QUALIFIED","LOSSY","UNRESOLVED","INCOMPATIBLE"]
EXPECTED_PIPELINE=[
 "BIND_SOURCE_CONTEXT","CONSTRUCT_SOURCE_MEANING_FRAME","DECLARE_TARGET_REPRESENTATION",
 "MAP_WITH_TYPED_TRANSFORMATIONS","ASSESS_COMPONENT_FIDELITY","PRESERVE_UNRESOLVED_AMBIGUITY",
 "VALIDATE_TARGET_REPRESENTATION_WHERE_AVAILABLE","EMIT_PROVENANCE_BOUND_MEDIATION_RECEIPT",
 "HAND_OFF_WITHOUT_AUTHORITY_PROMOTION",
]
EXPECTED_OBJECTS={"MeaningFrame","MediationMapping","FidelityAssessment","MediationReceipt"}
EXPECTED_CASES={f"SM-{i:02d}" for i in range(1,11)}
REQUIRED_INVARIANTS={
 "SYNTAX_SIMILARITY_NE_SEMANTIC_EQUIVALENCE","SEMANTIC_SIMILARITY_NE_SAME_PROVENANCE",
 "TRANSLATION_PASS_NE_BEHAVIORAL_EQUIVALENCE","INTERPRETATION_NE_TRUTH","SPECIFICITY_NE_CONFIDENCE",
 "MEANING_NE_AUTHORIZATION","TARGET_ACCEPTANCE_NE_SOURCE_TARGET_EQUIVALENCE",
 "AMBIGUITY_NE_PERMISSION_TO_COLLAPSE","UNDERSTANDING_COMMAND_NE_AUTHORITY_TO_EXECUTE",
 "CORRECTION_NE_HISTORY_DELETION","PROPOSITION_FORCE_MUST_NOT_SILENTLY_STRENGTHEN",
 "SOURCE_CONTEXT_MUST_REMAIN_BOUND","SEMANTIC_LOSS_MUST_BE_MONOTONIC",
 "TARGET_VALIDATION_NE_EXECUTION","RELATION_METADATA_NE_INFERRED_TRANSITIVITY",
}

def load(path:Path)->dict[str,Any]:
    obj=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj,dict): raise ValueError(f"{path} root must be object")
    return obj

def validate(root:Path)->list[str]:
    errors=[]
    for p in (DOC_PATH,SPEC_PATH,FIXTURE_PATH):
        if not (root/p).is_file(): errors.append(f"missing {p}")
    if errors:return errors
    try:
        spec=load(root/SPEC_PATH); fixtures=load(root/FIXTURE_PATH)
    except (OSError,UnicodeError,json.JSONDecodeError,ValueError) as exc:
        return [f"invalid T37 contract: {exc}"]
    if spec.get("schema_version")!="GOD_BRAIN_SEMANTIC_MEDIATION_V0_1": errors.append("schema_version drifted")
    if spec.get("status")!="RESEARCH_SPECIFICATION_NO_RUNTIME": errors.append("status must remain no-runtime research")
    if spec.get("parent_coordination_head")!="c40d98a98a4627ec3b1a83ffaad514ad345f9612": errors.append("parent coordination binding drifted")
    donors=spec.get("donor_sources")
    if not isinstance(donors,list) or len(donors)!=3: errors.append("donor_sources must be exact three-source cut"); donors=[]
    seen=set()
    for d in donors:
        if not isinstance(d,dict): errors.append("donor must be object"); continue
        repo=d.get("repository"); seen.add(repo)
        if repo not in EXPECTED_DONORS: errors.append(f"unexpected donor {repo!r}"); continue
        if d.get("ref")!="main": errors.append(f"{repo}: ref must be main")
        if d.get("exact_head")!=EXPECTED_DONORS[repo]: errors.append(f"{repo}: exact head drifted")
        if not isinstance(d.get("exact_head"),str) or not SHA40.fullmatch(d["exact_head"]): errors.append(f"{repo}: invalid exact head")
    if seen!=set(EXPECTED_DONORS): errors.append("donor set drifted")
    inv=spec.get("invariants")
    if not isinstance(inv,list) or set(inv)!=REQUIRED_INVARIANTS or len(inv)!=len(set(inv)): errors.append("invariants must be exact closed set")
    if spec.get("fidelity_states")!=EXPECTED_FIDELITY: errors.append("fidelity states/order drifted")
    if spec.get("pipeline")!=EXPECTED_PIPELINE: errors.append("pipeline order/identity drifted")
    objs=spec.get("objects")
    if not isinstance(objs,dict) or set(objs)!=EXPECTED_OBJECTS: errors.append("object families drifted")
    cases=fixtures.get("cases")
    if fixtures.get("schema_version")!="GOD_BRAIN_SEMANTIC_MEDIATION_HOSTILE_CASES_V0_1": errors.append("fixture schema drifted")
    if not isinstance(cases,list): errors.append("fixture cases must be list"); cases=[]
    ids=[x.get("id") for x in cases if isinstance(x,dict)]
    if set(ids)!=EXPECTED_CASES or len(ids)!=10 or len(ids)!=len(set(ids)): errors.append("hostile cases must be exactly SM-01..SM-10")
    rule_set=set(spec.get("rules",[]))
    for case in cases:
        if not isinstance(case,dict): errors.append("fixture case must be object"); continue
        guards=case.get("guards")
        if not isinstance(guards,list) or not guards: errors.append(f"{case.get('id')}: guards missing"); continue
        for g in guards:
            if g not in REQUIRED_INVARIANTS and g not in rule_set: errors.append(f"{case.get('id')}: unknown guard {g}")
        if not isinstance(case.get("expected"),str) or not case["expected"]: errors.append(f"{case.get('id')}: expected missing")
    doc=(root/DOC_PATH).read_text(encoding="utf-8")
    for marker in (
      "SYNTAX SIMILARITY != SEMANTIC EQUIVALENCE","SEMANTIC SIMILARITY != SAME PROVENANCE",
      "TRANSLATION PASS != BEHAVIORAL EQUIVALENCE","INTERPRETATION != TRUTH",
      "SPECIFICITY != CONFIDENCE","MEANING != AUTHORIZATION",
      "TARGET ACCEPTANCE != SOURCE/TARGET EQUIVALENCE","AMBIGUITY != PERMISSION TO COLLAPSE",
      "UNDERSTAND COMMAND != AUTHORITY TO EXECUTE","SEMANTIC RECEIPT != AUTHORIZATION RECEIPT"
    ):
        if marker not in doc: errors.append(f"research doc missing marker: {marker}")
    return errors

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--root",default="."); args=p.parse_args()
    errors=validate(Path(args.root).resolve())
    if errors:
        for e in errors: print(f"FAIL: {e}")
        return 1
    print("God Brain semantic mediation V0.1: PASS"); return 0

if __name__=="__main__": raise SystemExit(main())
