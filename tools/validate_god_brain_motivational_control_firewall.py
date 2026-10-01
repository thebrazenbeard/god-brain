from __future__ import annotations
import argparse,json,re
from pathlib import Path
from typing import Any
DOC="docs/research/GOD_BRAIN_MOTIVATIONAL_CONTROL_FIREWALL_V0_1.md"
SPEC="specs/research/GOD_BRAIN_MOTIVATIONAL_CONTROL_FIREWALL_V0_1.json"
FIX="specs/research/fixtures/GOD_BRAIN_MOTIVATIONAL_CONTROL_HOSTILE_CASES_V0_1.json"
SHA40=re.compile(r"^[0-9a-f]{40}$")
DONORS={"thebrazenbeard/meso-crct":"060d0feeb9dc9eb23801082bd8f1c4a7cb06184d","thebrazenbeard/god-brain":"495c2b42932153cba0926744d04a69bc34557f81"}
INVARIANTS={"WANTING_NE_LIKING","ATTENTION_NE_DESIRE","SEMANTIC_RELEVANCE_NE_PLEASURE","REWARD_NE_TRUTH","SALIENCE_NE_AUTHORITY","HAZARD_NE_SUFFERING","PREDICTION_ERROR_NE_REWARD","HOMEOSTATIC_DEFICIT_NE_COMMAND","MEMORY_STRENGTH_NE_CURRENT_ACTIVATION","TARGET_PRIORITY_NE_ACTION_DIRECTION","ACTION_TENDENCY_NE_INTENT","INTENT_PROPOSAL_NE_AUTHORIZATION","AUTHORIZATION_NE_EXECUTION","REPEATED_CUE_NE_NEW_LEARNING_EVENT","AFFECTIVE_STATE_NE_EPISTEMIC_CONFIDENCE","NO_SINGLE_GLOBAL_UTILITY_SCALAR"}
CHANNELS={"PERCEPTUAL_SALIENCE","SEMANTIC_RELEVANCE","MOTIVATIONAL_SALIENCE","INCENTIVE_SALIENCE","EPISTEMIC_VALUE","ATTENTIONAL_PRIORITY","HEDONIC_VALENCE","PREDICTION_ERROR","SATIATION","HOMEOSTATIC_DEFICIT","HAZARD","AVOIDANCE","ASSOCIATION_STRENGTH"}
RULES={"CHANNELS_MUST_REMAIN_TYPED_THROUGH_SELECTION","NO_CHANNEL_MAY_SELF_AUTHORIZE_PROTECTED_EFFECT","REWARD_OR_PLEASURE_MUST_NOT_PROMOTE_TRUTH_CONFIDENCE","HAZARD_AND_AVOIDANCE_MUST_REMAIN_AVAILABLE_WITHOUT_LARGE_NEGATIVE_HEDONICS","LEARNING_REQUIRES_DISTINCT_EVENT_IDENTITY","CUE_RECALL_MUST_NOT_RECOUNT_ONE_EVENT_AS_NEW_LEARNING","QUARANTINED_OR_REVIEW_STALE_ASSOCIATION_MUST_NOT_DRIVE_RECALL","SAME_EVENT_CONFLICTING_TENDENCIES_MUST_NOT_BE_SUMMED_INTO_FALSE_CERTAINTY","SELECTION_POLICY_MUST_PRESERVE_PROTECTION_AND_AUTHORITY_CONSTRAINTS","INTENT_MUST_PASS_SEPARATE_AUTHORIZATION_AND_EXECUTION_GATES","AFFECTIVE_OR_MOTIVATIONAL_CHANNELS_MUST_NOT_WRITE_EPISTEMIC_STATUS","SEMANTIC_RELEVANCE_REQUIRES_SEMANTIC_PROVENANCE_NOT_SELF_ASSERTED_IMPORTANCE"}
OBJECTS={"AppraisalVector","HomeostaticNeed","AssociationTrace","SelectionRecord","ActionTendency","IntentProposal"}
CASES={f"MC-{i:02d}" for i in range(1,13)}
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
 if s.get("schema_version")!="GOD_BRAIN_MOTIVATIONAL_CONTROL_FIREWALL_V0_1":e.append("schema drifted")
 if s.get("status")!="RESEARCH_SPECIFICATION_NO_RUNTIME":e.append("status must remain no-runtime research")
 if s.get("parent_continual_head")!="91835664dd48acb4d0fa6bc94200bdbc7fe550f9":e.append("parent continual head drifted")
 exact(e,s.get("invariants"),INVARIANTS,"invariants");exact(e,s.get("channels"),CHANNELS,"channels");exact(e,s.get("rules"),RULES,"rules")
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
 required_by={
  "AppraisalVector":{"channel_values","channel_evidence","provenance_ref"},
  "HomeostaticNeed":{"deficit","satiation","evidence_refs"},
  "AssociationTrace":{"cue_identity","outcome_identity","learning_event_refs","review_state"},
  "SelectionRecord":{"typed_basis","conflicts","policy_revision","evidence_cut"},
  "ActionTendency":{"direction","basis_refs","hazard_relation"},
  "IntentProposal":{"proposed_action","risk_refs","authority_required","status"},
 }
 for name,fields in required_by.items():
  required=set(objs.get(name,{}).get("required",[]))
  for field in fields:
   if field not in required:e.append(f"{name} must require {field}")
 ceiling=set(s.get("claim_ceiling",[]))
 for x in ("NO_RUNTIME_IMPLEMENTATION","NO_SYNTHETIC_FEELING_CLAIM","NO_BIOLOGICAL_EQUIVALENCE_CLAIM","NO_PROTECTED_EFFECT_AUTHORITY","NO_CONSCIOUSNESS_CLAIM","NO_MERGE_OR_DEPLOYMENT_AUTHORITY"):
  if x not in ceiling:e.append(f"claim ceiling missing {x}")
 if f.get("schema_version")!="GOD_BRAIN_MOTIVATIONAL_CONTROL_HOSTILE_CASES_V0_1":e.append("fixture schema drifted")
 cases=f.get("cases",[]);ids=[x.get("id") for x in cases if isinstance(x,dict)]
 if set(ids)!=CASES or len(ids)!=12:e.append("fixtures must be exactly MC-01..MC-12")
 for c in cases:
  if c.get("guard") not in RULES:e.append(f"{c.get('id')}: unknown guard")
 doc=(root/DOC).read_text(encoding="utf-8")
 for marker in ("wanting != liking","attention != desire","semantic relevance != pleasure","reward != truth","salience != authority","hazard != suffering","homeostatic deficit != command","action tendency != intent","intent proposal != authorization","authorization != execution"):
  if marker not in doc:e.append(f"doc missing marker: {marker}")
 return e
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--root",default=".");a=p.parse_args();errors=validate(Path(a.root).resolve())
 if errors:
  for x in errors:print("FAIL:",x)
  return 1
 print("God Brain motivational control firewall V0.1: PASS");return 0
if __name__=="__main__":raise SystemExit(main())
