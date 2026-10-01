from __future__ import annotations
import argparse,json,re
from pathlib import Path
from typing import Any
DOC="docs/research/GOD_BRAIN_DURABLE_WORK_AND_CORRECTIVE_LEARNING_V0_1.md"
SPEC="specs/research/GOD_BRAIN_DURABLE_WORK_AND_CORRECTIVE_LEARNING_V0_1.json"
FIX="specs/research/fixtures/GOD_BRAIN_DURABLE_WORK_CORRECTIVE_LEARNING_HOSTILE_CASES_V0_1.json"
SHA40=re.compile(r"^[0-9a-f]{40}$")
DONORS={
"thebrazenbeard/pre-active":"4558923a5ddbb2672449addc424a21de9c62e7ec",
"thebrazenbeard/project-runner":"ee17ce504018aff2eb26c9a71e16e4832ebee6bf",
"thebrazenbeard/wip":"3b93b64c09f5ed704b21a9db28cb918df181947e",
"thebrazenbeard/fuckup":"a87dea38a58c4cff75bc7d123d87f63a5e110895",
"thebrazenbeard/RepairTracker":"cd7c6f27d27a03130d6e793d69634005a130dc3a",
"thebrazenbeard/bugops":"1d35bcbd16da24c7635a004845de1390de850b4e",
"thebrazenbeard/roots":"1bc3af6aec0bebe383f60f56ad3070e83f0f40b5",
"thebrazenbeard/god-brain":"495c2b42932153cba0926744d04a69bc34557f81"}
WORK_RULES={"DURABLE_WORK_MUST_BIND_EXACT_SUBJECT_AND_AUTHORITY_CEILING","CLAIM_OR_RECLAIM_MUST_ADVANCE_MONOTONIC_FENCING_TOKEN","STALE_FENCE_MUST_FAIL_CLOSED","CHECKPOINT_MUST_SEPARATE_OBSERVED_INFERRED_COMPLETED_UNFINISHED","MUTABLE_EXTERNAL_STATE_MUST_BE_FRESH_READ_BEFORE_RESUME_WHEN_MATERIAL","CONSEQUENTIAL_EFFECT_MUST_RECORD_PREPARED_BEFORE_DISPATCH","AMBIGUOUS_EFFECT_MUST_ENTER_OUTCOME_UNKNOWN_BEFORE_ANY_RETRY","OUTCOME_UNKNOWN_REQUIRES_TARGET_READBACK_OR_PROVIDER_RECONCILIATION","RETRY_AFTER_RECONCILIATION_MUST_USE_EXACT_STORED_REQUEST_OR_EXPLICIT_NEW_WORK","TERMINAL_WORK_CANNOT_BE_ROLLED_BACK_TO_ACTIVE_STATE","COMPLETION_REQUIRES_EXACT_SUBJECT_VERIFICATION_EVIDENCE"}
CORR_RULES={"INCIDENT_EVIDENCE_MUST_REMAIN_DISTINCT_FROM_HYPOTHESIS","ROOT_CAUSE_REQUIRES_DISCRIMINATING_EVIDENCE_BEYOND_REPRODUCTION","CORRECTION_MUST_SUPERSEDE_WITHOUT_DELETING_PRIOR_HISTORY","REPAIR_EFFECT_MUST_BE_VERIFIED_SEPARATELY_FROM_SOURCE_CHANGE","REGRESSION_FIXTURE_MUST_DISTINGUISH_FAILURE_FROM_CORRECTED_BEHAVIOR","CLOSURE_CLAIM_MUST_BIND_ACCEPTANCE_CRITERIA_AND_VERIFICATION_REFS","RECURRENCE_CLAIM_MUST_BIND_SUBJECT_AND_OBSERVATION_WINDOW","PREVENTION_MUST_USE_EVIDENCE_CEILING_NOT_ABSOLUTE_NEVER_AGAIN_LANGUAGE","OPTIONAL_EXTERNAL_PROVIDER_CANNOT_BECOME_REPAIR_AUTHORITY_BY_PRESENCE","PROMOTION_REQUIRES_FRESH_CURRENTNESS_AND_REQUIRED_INDEPENDENT_REVIEW"}
CASES={f"DW-{i:02d}" for i in range(1,13)}
OBJECTS={"WorkUnit","Lease","Checkpoint","EffectJournal","RepairCase","CorrectionRecord","RecurrenceWindow"}
def load(p:Path)->dict[str,Any]:
 v=json.loads(p.read_text(encoding="utf-8"))
 if not isinstance(v,dict):raise ValueError("root must be object")
 return v
def exact(e,v,x,label):
 if not isinstance(v,list):e.append(f"{label} must be list");return
 if len(v)!=len(set(v)):e.append(f"{label} must be unique")
 if set(v)!=x:e.append(f"{label} must be exact closed set")
def validate(root:Path)->list[str]:
 e=[]
 for p in (DOC,SPEC,FIX):
  if not (root/p).is_file():e.append(f"missing {p}")
 if e:return e
 try:s=load(root/SPEC);f=load(root/FIX)
 except Exception as exc:return [f"invalid contract: {exc}"]
 if s.get("schema_version")!="GOD_BRAIN_DURABLE_WORK_AND_CORRECTIVE_LEARNING_V0_1":e.append("schema drifted")
 if s.get("status")!="RESEARCH_SPECIFICATION_NO_RUNTIME":e.append("status must remain no-runtime research")
 if s.get("parent_motivational_head")!="c86578c53a9f07907ae01e595ea760e35021d9c7":e.append("parent motivational head drifted")
 exact(e,s.get("work_rules"),WORK_RULES,"work_rules");exact(e,s.get("correction_rules"),CORR_RULES,"correction_rules")
 donors=s.get("donor_sources",[]);seen=set()
 for d in donors:
  if not isinstance(d,dict):e.append("donor must be object");continue
  r=d.get("repository");seen.add(r)
  if r not in DONORS:e.append(f"unexpected donor {r}");continue
  if d.get("exact_head")!=DONORS[r]:e.append(f"{r}: exact head drifted")
  if not SHA40.fullmatch(str(d.get("exact_head",""))):e.append(f"{r}: invalid exact head")
 if seen!=set(DONORS):e.append("donor set drifted")
 objs=s.get("objects")
 if not isinstance(objs,dict) or set(objs)!=OBJECTS:e.append("objects drifted");objs={}
 needed={
  "WorkUnit":{"subject","authority_ceiling","generation","status"},
  "Lease":{"fencing_token","expires_at","generation"},
  "Checkpoint":{"observed","inferred","completed","unfinished","do_not_repeat","external_currentness_refs"},
  "EffectJournal":{"request_digest","authority_ref","state","readback_ref","reconciliation_ref"},
  "RepairCase":{"evidence_refs","hypotheses","root_cause_state","verification_refs","monitoring_state"},
  "CorrectionRecord":{"supersedes_refs","replacement_or_guardrail","evidence_refs","qualification_scope","status"},
  "RecurrenceWindow":{"subject_scope","start_cut","end_cut","observations","recurrences","claim_ceiling"}}
 for n,fields in needed.items():
  req=set(objs.get(n,{}).get("required",[]))
  for field in fields:
   if field not in req:e.append(f"{n} must require {field}")
 ceiling=set(s.get("claim_ceiling",[]))
 for x in ("NO_DAEMON_INSTALLATION","NO_BACKGROUND_EXECUTION_CLAIM","NO_RUNTIME_COUPLING","NO_EXTERNAL_EFFECT_AUTHORITY","NO_AUTONOMOUS_MERGE_OR_DEPLOYMENT","NO_PERMANENT_PREVENTION_CLAIM"):
  if x not in ceiling:e.append(f"claim ceiling missing {x}")
 if f.get("schema_version")!="GOD_BRAIN_DURABLE_WORK_CORRECTIVE_LEARNING_HOSTILE_CASES_V0_1":e.append("fixture schema drifted")
 cases=f.get("cases",[]);ids=[x.get("id") for x in cases if isinstance(x,dict)]
 if set(ids)!=CASES or len(ids)!=12:e.append("fixtures must be exactly DW-01..DW-12")
 all_rules=WORK_RULES|CORR_RULES
 for c in cases:
  if c.get("guard") not in all_rules:e.append(f"{c.get('id')}: unknown guard")
 doc=(root/DOC).read_text(encoding="utf-8")
 for marker in ("WORK INTENT != EXECUTION AUTHORITY","CHECKPOINT != CURRENT EXTERNAL STATE","PREPARED != ATTEMPTED","ATTEMPTED != EFFECT OCCURRED","EFFECT OCCURRED != VERIFIED EFFECT","OUTCOME UNKNOWN != SAFE TO RETRY","INCIDENT != ROOT CAUSE","REPRODUCTION != ROOT CAUSE","SOURCE CHANGE != DEPLOYED REPAIR","CORRECTION != HISTORY ERASURE","TEST PASS != GLOBAL CORRECTNESS"):
  if marker not in doc:e.append(f"doc missing marker: {marker}")
 return e
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--root",default=".");a=p.parse_args();errs=validate(Path(a.root).resolve())
 if errs:
  for x in errs:print("FAIL:",x)
  return 1
 print("God Brain durable work and corrective learning V0.1: PASS");return 0
if __name__=="__main__":raise SystemExit(main())
