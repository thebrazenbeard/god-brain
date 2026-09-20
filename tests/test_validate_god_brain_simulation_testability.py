from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_simulation_testability import (
    DOC_PATH,
    FIXTURE_PATH,
    SPEC_PATH,
    validate_simulation_testability,
)


class GodBrainSimulationTestabilityTests(unittest.TestCase):
    def test_repository_subject_validates(self) -> None:
        root=Path(__file__).resolve().parents[1]
        self.assertEqual(validate_simulation_testability(root), [])

    def _write(self,target:Path,spec:dict,fixture:dict,doc:str)->None:
        for path in (SPEC_PATH,FIXTURE_PATH,DOC_PATH):
            (target/path).parent.mkdir(parents=True,exist_ok=True)
        (target/SPEC_PATH).write_text(json.dumps(spec),encoding="utf-8")
        (target/FIXTURE_PATH).write_text(json.dumps(fixture),encoding="utf-8")
        (target/DOC_PATH).write_text(doc,encoding="utf-8")

    def test_lattice_signature_cannot_become_simulator_detection(self) -> None:
        root=Path(__file__).resolve().parents[1]
        spec=json.loads((root/SPEC_PATH).read_text(encoding="utf-8"))
        fixture=json.loads((root/FIXTURE_PATH).read_text(encoding="utf-8"))
        doc=(root/DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            mutated=json.loads(json.dumps(spec))
            mutated["invariants"].remove("LATTICE_SIGNATURE_NE_SIMULATOR_DETECTION")
            self._write(target,mutated,fixture,doc)
            errors=validate_simulation_testability(target)
            self.assertTrue(any("LATTICE_SIGNATURE" in error for error in errors))

    def test_s4_must_remain_empirically_underdetermined(self) -> None:
        root=Path(__file__).resolve().parents[1]
        spec=json.loads((root/SPEC_PATH).read_text(encoding="utf-8"))
        fixture=json.loads((root/FIXTURE_PATH).read_text(encoding="utf-8"))
        doc=(root/DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            mutated=json.loads(json.dumps(spec))
            next(x for x in mutated["classes"] if x["id"]=="S4")["testability"]="DIRECTLY_TESTABLE"
            self._write(target,mutated,fixture,doc)
            errors=validate_simulation_testability(target)
            self.assertTrue(any("S4 observational-equivalence" in error for error in errors))

    def test_external_channel_cannot_become_simulation_proof(self) -> None:
        root=Path(__file__).resolve().parents[1]
        spec=json.loads((root/SPEC_PATH).read_text(encoding="utf-8"))
        fixture=json.loads((root/FIXTURE_PATH).read_text(encoding="utf-8"))
        doc=(root/DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            mutated=json.loads(json.dumps(spec))
            next(x for x in mutated["classes"] if x["id"]=="S5")["positive_support_ceiling"]="SIMULATION_PROOF"
            self._write(target,mutated,fixture,doc)
            errors=validate_simulation_testability(target)
            self.assertTrue(any("S5 may support only" in error for error in errors))

    def test_weirdness_cannot_be_experiment_success_criterion(self) -> None:
        root=Path(__file__).resolve().parents[1]
        spec=json.loads((root/SPEC_PATH).read_text(encoding="utf-8"))
        fixture=json.loads((root/FIXTURE_PATH).read_text(encoding="utf-8"))
        doc=(root/DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            mutated=json.loads(json.dumps(spec))
            mutated["reject_if_success_criterion"].remove("SOMETHING_WEIRD_HAPPENS")
            self._write(target,mutated,fixture,doc)
            errors=validate_simulation_testability(target)
            self.assertTrue(any("weirdness" in error for error in errors))

    def test_resource_bound_cannot_rule_out_arbitrary_parent_physics(self) -> None:
        root=Path(__file__).resolve().parents[1]
        spec=json.loads((root/SPEC_PATH).read_text(encoding="utf-8"))
        fixture=json.loads((root/FIXTURE_PATH).read_text(encoding="utf-8"))
        doc=(root/DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)
            mutated=json.loads(json.dumps(fixture))
            case=next(x for x in mutated["cases"] if x["id"]=="GB-ST-006")
            case["expected"]="UNIVERSAL_SIMULATION_REFUTATION"
            self._write(target,spec,mutated,doc)
            errors=validate_simulation_testability(target)
            self.assertTrue(any("GB-ST-006 classification expectation drifted" in error for error in errors))


if __name__=="__main__":
    unittest.main()
