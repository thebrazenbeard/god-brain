from __future__ import annotations
import copy,json,tempfile,unittest
from pathlib import Path
from tools.validate_god_brain_adversarial_review import DOC_PATH,FIXTURE_PATH,SPEC_PATH,validate_adversarial_review
ROOT=Path(__file__).resolve().parents[1]
def _load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def _mutated(spec_mutator=None,fixture_mutator=None):
    spec=copy.deepcopy(_load(SPEC_PATH)); fixtures=copy.deepcopy(_load(FIXTURE_PATH))
    if spec_mutator: spec_mutator(spec)
    if fixture_mutator: fixture_mutator(fixtures)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for p in (DOC_PATH,SPEC_PATH,FIXTURE_PATH):(root/p).parent.mkdir(parents=True,exist_ok=True)
        (root/DOC_PATH).write_text((ROOT/DOC_PATH).read_text(encoding="utf-8"),encoding="utf-8")
        (root/SPEC_PATH).write_text(json.dumps(spec,indent=2)+"\n",encoding="utf-8")
        (root/FIXTURE_PATH).write_text(json.dumps(fixtures,indent=2)+"\n",encoding="utf-8")
        return validate_adversarial_review(root)
class AdversarialReviewTests(unittest.TestCase):
    def test_repository_subject_validates(self): self.assertEqual(validate_adversarial_review(ROOT),[])
    def test_self_review_cannot_become_independent(self):
        e=_mutated(lambda s:s["independence_classification"].__setitem__("SAME_MODEL_SELF","INDEPENDENT"))
        self.assertTrue(any("NOT_INDEPENDENT" in x for x in e))
    def test_separate_model_same_context_is_not_automatic_independence(self):
        e=_mutated(lambda s:s["independence_classification"].__setitem__("SEPARATE_MODEL_SAME_OPERATOR_CONTEXT","INDEPENDENT_IF_SUBJECT_AND_INFLUENCE_BOUND"))
        self.assertTrue(any("independence-unestablished" in x for x in e))
    def test_pass_cannot_gain_merge_authority(self):
        e=_mutated(lambda s:s["claim_ceiling"].remove("NO_MERGE_AUTHORITY"))
        self.assertTrue(any("NO_MERGE_AUTHORITY" in x for x in e))
    def test_review_lane_cannot_gain_execution_authority(self):
        e=_mutated(lambda s:s["lanes"]["candidate_integrity"].__setitem__("authority","EXECUTE"))
        self.assertTrue(any("advisory" in x for x in e))
    def test_head_staleness_rule_cannot_be_removed(self):
        e=_mutated(lambda s:s["review_rules"].remove("EXACT_HEAD_CHANGE_MAKES_PRIOR_VERDICT_HISTORICAL_ONLY"))
        self.assertTrue(any("review_rules" in x for x in e))
    def test_literal_path_guard_cannot_be_removed(self):
        e=_mutated(lambda s:s["review_rules"].remove("LOOPHOLE_FINDING_MUST_INCLUDE_LITERAL_PATH_AND_PROTECTED_INTENT"))
        self.assertTrue(any("review_rules" in x for x in e))
    def test_rival_hypothesis_guard_cannot_be_removed(self):
        e=_mutated(lambda s:s["review_rules"].remove("FORENSIC_REVIEW_MUST_KEEP_LIVE_RIVALS_WHEN_EVIDENCE_DOES_NOT_DISCRIMINATE"))
        self.assertTrue(any("review_rules" in x for x in e))
    def test_reproduction_root_cause_guard_cannot_be_removed(self):
        e=_mutated(lambda s:s["review_rules"].remove("ROOT_CAUSE_MUST_DISTINGUISH_REPRODUCTION_FROM_CAUSAL_EXPLANATION"))
        self.assertTrue(any("review_rules" in x for x in e))
    def test_hostile_case_cannot_be_removed(self):
        e=_mutated(fixture_mutator=lambda f:f.__setitem__("cases",[x for x in f["cases"] if x["id"]!="AR-03"]))
        self.assertTrue(any("AR-01..AR-12" in x for x in e))
    def test_unknown_hostile_guard_rejected(self):
        def mutate(f): f["cases"][0]["guards"]=["FAKE_GUARD"]
        e=_mutated(fixture_mutator=mutate); self.assertTrue(any("unknown guard" in x for x in e))
    def test_exact_donor_head_cannot_drift(self):
        def mutate(s): next(x for x in s["donor_sources"] if x["repository"]=="thebrazenbeard/cricket")["exact_head"]="f"*40
        e=_mutated(mutate); self.assertTrue(any("exact_head drifted" in x for x in e))
if __name__=="__main__": unittest.main()
