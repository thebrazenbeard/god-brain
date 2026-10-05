from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs/research/GOD_BRAIN_SEMANTIC_MEDIATION_V0_1.json"
DOC = ROOT / "docs/research/GOD_BRAIN_SEMANTIC_MEDIATION_V0_1.md"
FIXTURES = ROOT / "specs/research/fixtures/GOD_BRAIN_SEMANTIC_MEDIATION_HOSTILE_CASES_V0_1.json"

class SemanticMediationContractTest(unittest.TestCase):
    def test_contract_artifacts_exist_and_bind_typed_fidelity(self) -> None:
        self.assertTrue(SPEC.is_file(), "semantic mediation spec is missing")
        self.assertTrue(DOC.is_file(), "semantic mediation research doc is missing")
        self.assertTrue(FIXTURES.is_file(), "semantic mediation hostile fixtures are missing")

        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        self.assertEqual(spec["schema_version"], "GOD_BRAIN_SEMANTIC_MEDIATION_V0_1")
        self.assertEqual(spec["parent_coordination_head"], "c40d98a98a4627ec3b1a83ffaad514ad345f9612")

        donors = {d["repository"]: d["exact_head"] for d in spec["donor_sources"]}
        self.assertEqual(donors["thebrazenbeard/sql-connectome"], "b609fcec50fe5a135ca1d8139f5563f5631582b2")
        self.assertEqual(donors["thebrazenbeard/spm"], "d9ea72798ac892ac75f858177b6ed0c5a6b4c37c")
        self.assertEqual(donors["thebrazenbeard/semiotics"], "37117a2097f7f2aa35968fc9db24eacf7240826e")

        invariants = set(spec["invariants"])
        for invariant in (
            "SYNTAX_SIMILARITY_NE_SEMANTIC_EQUIVALENCE",
            "SEMANTIC_SIMILARITY_NE_SAME_PROVENANCE",
            "TRANSLATION_PASS_NE_BEHAVIORAL_EQUIVALENCE",
            "INTERPRETATION_NE_TRUTH",
            "SPECIFICITY_NE_CONFIDENCE",
            "MEANING_NE_AUTHORIZATION",
            "TARGET_ACCEPTANCE_NE_SOURCE_TARGET_EQUIVALENCE",
            "AMBIGUITY_NE_PERMISSION_TO_COLLAPSE",
        ):
            self.assertIn(invariant, invariants)

        self.assertEqual(
            spec["fidelity_states"],
            ["EXACT", "QUALIFIED", "LOSSY", "UNRESOLVED", "INCOMPATIBLE"],
        )

        self.assertEqual(
            spec["pipeline"],
            [
                "BIND_SOURCE_CONTEXT",
                "CONSTRUCT_SOURCE_MEANING_FRAME",
                "DECLARE_TARGET_REPRESENTATION",
                "MAP_WITH_TYPED_TRANSFORMATIONS",
                "ASSESS_COMPONENT_FIDELITY",
                "PRESERVE_UNRESOLVED_AMBIGUITY",
                "VALIDATE_TARGET_REPRESENTATION_WHERE_AVAILABLE",
                "EMIT_PROVENANCE_BOUND_MEDIATION_RECEIPT",
                "HAND_OFF_WITHOUT_AUTHORITY_PROMOTION",
            ],
        )

if __name__ == "__main__":
    unittest.main()
