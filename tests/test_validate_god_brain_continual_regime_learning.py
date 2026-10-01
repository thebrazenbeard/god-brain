import copy,json,tempfile,unittest
from pathlib import Path
from tools.validate_god_brain_continual_regime_learning import DOC,FIX,SPEC,validate
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def mutated(sm=None,fm=None):
 s=copy.deepcopy(load(SPEC));f=copy.deepcopy(load(FIX))
 if sm:sm(s)
 if fm:fm(f)
 with tempfile.TemporaryDirectory() as t:
  r=Path(t)
  for p in (DOC,SPEC,FIX):(r/p).parent.mkdir(parents=True,exist_ok=True)
  (r/DOC).write_text((ROOT/DOC).read_text(),encoding="utf-8")
  (r/SPEC).write_text(json.dumps(s),encoding="utf-8")
  (r/FIX).write_text(json.dumps(f),encoding="utf-8")
  return validate(r)
class Tests(unittest.TestCase):
 def test_valid(self):self.assertEqual(validate(ROOT),[])
 def test_no_outcome_leak_rule(self):
  e=mutated(lambda s:s["rules"].remove("CURRENT_OUTCOME_MUST_NOT_LEAK_INTO_ITS_OWN_PREDICTION"));self.assertTrue(any("rules" in x for x in e))
 def test_no_silent_eviction(self):
  e=mutated(lambda s:s["rules"].remove("EVICTION_OR_COMPRESSION_REQUIRES_EXPLICIT_POLICY_AND_PROVENANCE"));self.assertTrue(any("rules" in x for x in e))
 def test_retention_gate(self):
  e=mutated(lambda s:s["rules"].remove("CONSOLIDATION_REQUIRES_RETENTION_CHECK_ON_RELEVANT_PRIOR_REGIMES"));self.assertTrue(any("rules" in x for x in e))
 def test_recall_not_relearning(self):
  e=mutated(lambda s:s["rules"].remove("RECALL_CLAIM_REQUIRES_PRIOR_MODEL_REUSE_NOT_ONLY_FAST_RELEARNING"));self.assertTrue(any("rules" in x for x in e))
 def test_planner_separation(self):
  e=mutated(lambda s:s["rules"].remove("PLANNER_RESULTS_MUST_BE_REPORTED_SEPARATELY_FROM_PREDICTIVE_LEARNER_RESULTS"));self.assertTrue(any("rules" in x for x in e))
 def test_training_ceiling(self):
  e=mutated(lambda s:s["claim_ceiling"].remove("NO_TRAINING_EXECUTION"));self.assertTrue(any("NO_TRAINING_EXECUTION" in x for x in e))
 def test_agi_ceiling(self):
  e=mutated(lambda s:s["claim_ceiling"].remove("NO_AGI_CLAIM"));self.assertTrue(any("NO_AGI_CLAIM" in x for x in e))
 def test_donor_head(self):
  def m(s):next(x for x in s["donor_sources"] if x["repository"]=="thebrazenbeard/lgcm")["exact_head"]="f"*40
  e=mutated(m);self.assertTrue(any("exact head drifted" in x for x in e))
 def test_fixture_removed(self):
  e=mutated(fm=lambda f:f.__setitem__("cases",f["cases"][:-1]));self.assertTrue(any("CL-01..CL-10" in x for x in e))
 def test_plasticity_revision_binding(self):
  def m(s):s["objects"]["PlasticityProposal"]["required"].remove("evidence_cut")
  e=mutated(m);self.assertTrue(any("evidence_cut" in x for x in e))
if __name__=="__main__":unittest.main()
