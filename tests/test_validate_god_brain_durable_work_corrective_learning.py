import copy,json,tempfile,unittest
from pathlib import Path
from tools.validate_god_brain_durable_work_corrective_learning import DOC,FIX,SPEC,validate
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def mutated(sm=None,fm=None):
 s=copy.deepcopy(load(SPEC));f=copy.deepcopy(load(FIX))
 if sm:sm(s)
 if fm:fm(f)
 with tempfile.TemporaryDirectory() as t:
  r=Path(t)
  for p in (DOC,SPEC,FIX):(r/p).parent.mkdir(parents=True,exist_ok=True)
  (r/DOC).write_text((ROOT/DOC).read_text(),encoding="utf-8");(r/SPEC).write_text(json.dumps(s),encoding="utf-8");(r/FIX).write_text(json.dumps(f),encoding="utf-8")
  return validate(r)
class Tests(unittest.TestCase):
 def test_valid(self):self.assertEqual(validate(ROOT),[])
 def test_unknown_effect_requires_reconciliation(self):
  e=mutated(lambda s:s["work_rules"].remove("OUTCOME_UNKNOWN_REQUIRES_TARGET_READBACK_OR_PROVIDER_RECONCILIATION"));self.assertTrue(any("work_rules" in x for x in e))
 def test_stale_fence(self):
  e=mutated(lambda s:s["work_rules"].remove("STALE_FENCE_MUST_FAIL_CLOSED"));self.assertTrue(any("work_rules" in x for x in e))
 def test_checkpoint_fact_inference(self):
  e=mutated(lambda s:s["work_rules"].remove("CHECKPOINT_MUST_SEPARATE_OBSERVED_INFERRED_COMPLETED_UNFINISHED"));self.assertTrue(any("work_rules" in x for x in e))
 def test_root_cause_not_reproduction(self):
  e=mutated(lambda s:s["correction_rules"].remove("ROOT_CAUSE_REQUIRES_DISCRIMINATING_EVIDENCE_BEYOND_REPRODUCTION"));self.assertTrue(any("correction_rules" in x for x in e))
 def test_correction_keeps_history(self):
  e=mutated(lambda s:s["correction_rules"].remove("CORRECTION_MUST_SUPERSEDE_WITHOUT_DELETING_PRIOR_HISTORY"));self.assertTrue(any("correction_rules" in x for x in e))
 def test_source_change_not_effect(self):
  e=mutated(lambda s:s["correction_rules"].remove("REPAIR_EFFECT_MUST_BE_VERIFIED_SEPARATELY_FROM_SOURCE_CHANGE"));self.assertTrue(any("correction_rules" in x for x in e))
 def test_no_permanent_prevention_claim(self):
  e=mutated(lambda s:s["claim_ceiling"].remove("NO_PERMANENT_PREVENTION_CLAIM"));self.assertTrue(any("NO_PERMANENT_PREVENTION_CLAIM" in x for x in e))
 def test_no_daemon_install(self):
  e=mutated(lambda s:s["claim_ceiling"].remove("NO_DAEMON_INSTALLATION"));self.assertTrue(any("NO_DAEMON_INSTALLATION" in x for x in e))
 def test_donor_head(self):
  def m(s):next(x for x in s["donor_sources"] if x["repository"]=="thebrazenbeard/pre-active")["exact_head"]="f"*40
  e=mutated(m);self.assertTrue(any("exact head drifted" in x for x in e))
 def test_fixture_removed(self):
  e=mutated(fm=lambda f:f.__setitem__("cases",f["cases"][:-1]));self.assertTrue(any("DW-01..DW-12" in x for x in e))
 def test_promotion_requires_review_currentness(self):
  e=mutated(lambda s:s["correction_rules"].remove("PROMOTION_REQUIRES_FRESH_CURRENTNESS_AND_REQUIRED_INDEPENDENT_REVIEW"));self.assertTrue(any("correction_rules" in x for x in e))
if __name__=="__main__":unittest.main()
