import copy,json,tempfile,unittest
from pathlib import Path
from tools.validate_god_brain_motivational_control_firewall import DOC,FIX,SPEC,validate
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
  (r/SPEC).write_text(json.dumps(s),encoding="utf-8");(r/FIX).write_text(json.dumps(f),encoding="utf-8")
  return validate(r)
class Tests(unittest.TestCase):
 def test_valid(self):self.assertEqual(validate(ROOT),[])
 def test_reward_truth_firewall(self):
  e=mutated(lambda s:s["rules"].remove("REWARD_OR_PLEASURE_MUST_NOT_PROMOTE_TRUTH_CONFIDENCE"));self.assertTrue(any("rules" in x for x in e))
 def test_salience_authority_firewall(self):
  e=mutated(lambda s:s["rules"].remove("NO_CHANNEL_MAY_SELF_AUTHORIZE_PROTECTED_EFFECT"));self.assertTrue(any("rules" in x for x in e))
 def test_typed_channels(self):
  e=mutated(lambda s:s["rules"].remove("CHANNELS_MUST_REMAIN_TYPED_THROUGH_SELECTION"));self.assertTrue(any("rules" in x for x in e))
 def test_event_identity_learning(self):
  e=mutated(lambda s:s["rules"].remove("LEARNING_REQUIRES_DISTINCT_EVENT_IDENTITY"));self.assertTrue(any("rules" in x for x in e))
 def test_quarantine_recall(self):
  e=mutated(lambda s:s["rules"].remove("QUARANTINED_OR_REVIEW_STALE_ASSOCIATION_MUST_NOT_DRIVE_RECALL"));self.assertTrue(any("rules" in x for x in e))
 def test_intent_authorization_execution(self):
  e=mutated(lambda s:s["rules"].remove("INTENT_MUST_PASS_SEPARATE_AUTHORIZATION_AND_EXECUTION_GATES"));self.assertTrue(any("rules" in x for x in e))
 def test_affect_epistemic_firewall(self):
  e=mutated(lambda s:s["rules"].remove("AFFECTIVE_OR_MOTIVATIONAL_CHANNELS_MUST_NOT_WRITE_EPISTEMIC_STATUS"));self.assertTrue(any("rules" in x for x in e))
 def test_biological_claim_ceiling(self):
  e=mutated(lambda s:s["claim_ceiling"].remove("NO_BIOLOGICAL_EQUIVALENCE_CLAIM"));self.assertTrue(any("NO_BIOLOGICAL_EQUIVALENCE_CLAIM" in x for x in e))
 def test_fixture_removed(self):
  e=mutated(fm=lambda f:f.__setitem__("cases",f["cases"][:-1]));self.assertTrue(any("MC-01..MC-12" in x for x in e))
 def test_donor_head(self):
  def m(s):next(x for x in s["donor_sources"] if x["repository"]=="thebrazenbeard/meso-crct")["exact_head"]="f"*40
  e=mutated(m);self.assertTrue(any("exact head drifted" in x for x in e))
if __name__=="__main__":unittest.main()
