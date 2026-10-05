from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs/research/GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_V0_1.json"
DOC = ROOT / "docs/research/GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_V0_1.md"
FIXTURES = ROOT / "specs/research/fixtures/GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_HOSTILE_CASES_V0_1.json"

class CoordinationCoreOverlayContractTest(unittest.TestCase):
    def test_contract_artifacts_exist_and_bind_core_overlay_separation(self) -> None:
        self.assertTrue(SPEC.is_file(), "coordination core/private-overlay spec is missing")
        self.assertTrue(DOC.is_file(), "coordination core/private-overlay research doc is missing")
        self.assertTrue(FIXTURES.is_file(), "coordination core/private-overlay hostile fixtures are missing")

        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        self.assertEqual(spec["schema_version"], "GOD_BRAIN_COORDINATION_CORE_PRIVATE_OVERLAY_V0_1")
        self.assertEqual(spec["parent_source_universe_head"], "f56f52b3606839147a12e68375612336fb9bbfdd")

        donors = {d["repository"]: d["exact_head"] for d in spec["donor_sources"]}
        self.assertEqual(donors["thebrazenbeard/ccb-core"], "0b542a78ebf5827a518e0731a63f17a7ac8a2727")
        self.assertEqual(donors["thebrazenbeard/chat-communication-bus"], "e0bcb5eb18630693de55a1af2066411c7af079bb")

        invariants = set(spec["invariants"])
        self.assertIn("REUSABLE_CODE_AUTHORITY_NE_PRIVATE_DEPLOYMENT_STATE", invariants)
        self.assertIn("PRIVATE_DISCOVERY_NE_CANONICAL_GENERIC_FIX", invariants)
        self.assertIn("SOURCE_PIN_NE_DEPLOYMENT_AUTHORITY", invariants)
        self.assertIn("PRIVATE_HISTORY_NE_REUSABLE_IMPLEMENTATION", invariants)

        self.assertEqual(
            spec["pipeline"],
            [
                "DISCOVER_GENERIC_OR_PRIVATE_FIX",
                "CLASSIFY_CORE_VS_OVERLAY",
                "SANITIZE_PRIVATE_MATERIAL",
                "REPRODUCE_IN_PUBLIC_CORE",
                "ADD_DETERMINISTIC_REGRESSION",
                "QUALIFY_EXACT_CORE_CUT",
                "PIN_OVERLAY_TO_QUALIFIED_CORE",
                "RECONCILE_PRIVATE_STATE_SEPARATELY",
            ],
        )

if __name__ == "__main__":
    unittest.main()
