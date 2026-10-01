from __future__ import annotations

import argparse, json, re
from pathlib import Path
from typing import Any

DOC="docs/research/GOD_BRAIN_CONTINUAL_REGIME_LEARNING_V0_1.md"
SPEC="specs/research/GOD_BRAIN_CONTINUAL_REGIME_LEARNING_V0_1.json"
FIX="specs/research/fixtures/GOD_BRAIN_CONTINUAL_REGIME_LEARNING_HOSTILE_CASES_V0_1.json"
SHA40=re.compile(r"^[0-9a-f]{40}$")
DONORS={
 "thebrazenbeard/lgcm":"0043c60419de9ef0b52363b62aed8c0a52ef63f5",
 "thebrazenbeard/noema":"697d1fac6f9fea158994888a861e651ac8fac282",
 "thebrazenbeard/god-brain":"495c2b42932153cba0926744d04a69bc34557f81",
}
INVARIANTS={
 "PREDICTION_MUST_PRECEDE_OUTCOME_UPDATE","REGIME_HYPOTHESIS_NE_WORLD_TRUTH","CONTEXT_SCORE_NE_IDENTITY",
 "MISMATCH_NE_NEW_REGIME_PROOF","HISTORICAL_COMPETENCE_NE_CURRENT_COMPETENCE","RECALL_NE_RELEARNING_PROOF",
 "PERSISTENCE_NE_GENERALIZATION","PLASTICITY_PROPOSAL_NE_CONSOLIDATED_LEARNING","SHARED_MODEL_UPDATE_NE_SILENT_EXPERT_REWRITE",
 "CAPACITY_PRESSURE_NE_SILENT_EVICTION","OLD_REGIME_RETURN_NE_MODEL_FAILURE","PLANNER_SUCCESS_NE_LEARNER_QUALITY",
 "LABEL_FREE_CONTEXT_INFERENCE_NE_CAUSAL_IDENTIFICATION","TRAINING_EXECUTION_NE_ARCHITECTURE_QUALIFICATION",
}
RULES={
 "CURRENT_OUTCOME_MUST_NOT_LEAK_INTO_ITS_OWN_PREDICTION","REGIME_SELECTION_MUST_PRESERVE_UNCERTAINTY_AND_ALTERNATIVES",
 "NEW_EXPERT_SPAWN_REQUIRES_PERSISTENT_MISMATCH_EVIDENCE","DORMANT_EXPERT_MUST_REMAIN_ADDRESSABLE_UNLESS_EXPLICITLY_RETIRED",
 "EVICTION_OR_COMPRESSION_REQUIRES_EXPLICIT_POLICY_AND_PROVENANCE","PLASTICITY_MUST_BIND_EXACT_EVIDENCE_CUT_AND_MODEL_REVISION",
 "CONSOLIDATION_REQUIRES_RETENTION_CHECK_ON_RELEVANT_PRIOR_REGIMES","RECALL_CLAIM_REQUIRES_PRIOR_MODEL_REUSE_NOT_ONLY_FAST_RELEARNING",
 "RECOVERY_METRIC_MUST_BE_SEPARATE_FROM_NEW_REGIME_ADAPTATION_METRIC","PLANNER_RESULTS_MUST_BE_REPORTED_SEPARATELY_FROM_PREDICTIVE_LEARNER_RESULTS",
 "CONTEXT_LABELS_IF_AVAILABLE_ARE_EVALUATION_EVIDENCE_NOT_REQUIRED_RUNTIME_INPUT","NO_PLASTICITY_PATH_MAY_BYPASS_AUTHORITY_OR_PROTECTED_STATE_GOVERNANCE",
}
CASES={f"CL-{i:02d}" for i in range(1,11)}
OBJECTS={"PrequentialEvent","RegimeHypothesis","ContextExpert","PlasticityProposal","CompetenceSnapshot"}

def load(p:Path)->dict[str,Any]:
 v=json.loads(p.read_text(encoding="utf-8"))
 if not isinstance(v,dict): raise ValueError("root must be object")
 return v

def exact(errors,value,expected,label):
 if not isinstance(value,list): errors.append(f"{label} must be list"); return
 if len(value)!=len(set(value)): errors.append(f"{label} must be unique")
 if set(value)!=expected: errors.append(f"{label} must be exact closed set")

def validate(root:Path)->list[str]:
 e=[]
 for p in (DOC,SPEC,FIX):
  if not (root/p).is_file(): e.append(f"missing {p}")
 if e:return e
 try:s=load(root/SPEC);f=load(root/FIX)
 except Exception as exc:return [f"invalid contract: {exc}"]
 if s.get("schema_version")!="GOD_BRAIN_CONTINUAL_REGIME_LEARNING_V0_1":e.append("schema drifted")
 if s.get("status")!="RESEARCH_SPECIFICATION_NO_TRAINING":e.append("status must remain no-training research")
 if s.get("parent_review_head")!="0d2faba7862e3e368a93a8c275f7aa06b46e0fc4":e.append("parent head drifted")
 exact(e,s.get("invariants"),INVARIANTS,"invariants")
 exact(e,s.get("rules"),RULES,"rules")
 donors=s.get("donor_sources",[])
 if not isinstance(donors,list):e.append("donors must be list");donors=[]
 seen=set()
 for d in donors:
  if not isinstance(d,dict):e.append("donor must be object");continue
  r=d.get("repository");seen.add(r)
  if r not in DONORS:e.append(f"unexpected donor {r}");continue
  if d.get("ref")!="main":e.append(f"{r}: ref must be main")
  if d.get("exact_head")!=DONORS[r]:e.append(f"{r}: exact head drifted")
  if not SHA40.fullmatch(str(d.get("exact_head",""))):e.append(f"{r}: invalid exact head")
 if seen!=set(DONORS):e.append("donor set drifted")
 objs=s.get("objects")
 if not isinstance(objs,dict) or set(objs)!=OBJECTS:e.append("object families drifted");objs={}
 for n,o in objs.items():
  if not isinstance(o,dict) or not isinstance(o.get("required"),list) or not o.get("required"):e.append(f"{n}: invalid definition")
 for name,fields in {
  "PrequentialEvent":{"prediction","prediction_state_digest","outcome_after","error"},
  "RegimeHypothesis":{"evidence_refs","uncertainty","state"},
  "ContextExpert":{"parameter_revision","training_cut","capacity_state"},
  "PlasticityProposal":{"target_model","evidence_cut","retention_risk","reversibility","status"},
  "CompetenceSnapshot":{"evaluation_cut","prequential","retention_comparison","recovery_comparison"},
 }.items():
  required=set(objs.get(name,{}).get("required",[]))
  for field in fields:
   if field not in required:e.append(f"{name} must require {field}")
 ceiling=set(s.get("claim_ceiling",[]))
 for x in ("NO_TRAINING_EXECUTION","NO_MODEL_WEIGHT_UPDATE","NO_AGI_CLAIM","NO_GENERALIZATION_CLAIM","NO_CONSCIOUSNESS_CLAIM","NO_MERGE_OR_DEPLOYMENT_AUTHORITY"):
  if x not in ceiling:e.append(f"claim ceiling missing {x}")
 if f.get("schema_version")!="GOD_BRAIN_CONTINUAL_REGIME_LEARNING_HOSTILE_CASES_V0_1":e.append("fixture schema drifted")
 cases=f.get("cases",[])
 ids=[x.get("id") for x in cases if isinstance(x,dict)]
 if set(ids)!=CASES or len(ids)!=10:e.append("fixtures must be exactly CL-01..CL-10")
 for c in cases:
  if c.get("guard") not in RULES:e.append(f"{c.get('id')}: unknown guard")
 doc=(root/DOC).read_text(encoding="utf-8")
 for marker in ("PREDICTION_BEFORE_UPDATE","REGIME_HYPOTHESIS != WORLD_TRUTH","MISMATCH != NEW_REGIME_PROOF","PLASTICITY_PROPOSAL != CONSOLIDATED_LEARNING","RECALL != FAST_RELEARNING","PLANNER_SUCCESS != LEARNER_QUALITY"):
  if marker not in doc:e.append(f"doc missing marker: {marker}")
 return e

def main()->int:
 p=argparse.ArgumentParser();p.add_argument("--root",default=".");a=p.parse_args();errors=validate(Path(a.root).resolve())
 if errors:
  for x in errors:print("FAIL:",x)
  return 1
 print("God Brain continual regime learning V0.1: PASS");return 0
if __name__=="__main__":raise SystemExit(main())
