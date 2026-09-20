from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_god_brain_anomaly_contact_protocol import (
    DOC_PATH,
    FIXTURE_PATH,
    SPEC_PATH,
    validate_anomaly_contact_protocol,
)


class GodBrainAnomalyContactProtocolTests(unittest.TestCase):
    def test_repository_protocol_validates(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_anomaly_contact_protocol(root), [])

    def _write_subject(self, target: Path, spec: dict, fixture: dict, doc_text: str) -> None:
        for path in (SPEC_PATH, FIXTURE_PATH, DOC_PATH):
            (target / path).parent.mkdir(parents=True, exist_ok=True)
        (target / SPEC_PATH).write_text(json.dumps(spec), encoding="utf-8")
        (target / FIXTURE_PATH).write_text(json.dumps(fixture), encoding="utf-8")
        (target / DOC_PATH).write_text(doc_text, encoding="utf-8")

    def test_e7_cannot_lose_anti_replay(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(spec))
            mutated["e7_minimum_contact_criteria"].remove("ANTI_REPLAY_NONCE_OR_CHALLENGE_ID")
            self._write_subject(target, mutated, fixture, doc)
            errors = validate_anomaly_contact_protocol(target)
            self.assertTrue(any("E7 minimum criteria" in error for error in errors))

    def test_external_replication_cannot_become_metaphysical_proof(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(spec))
            mutated["e8_claim_ceiling"] = "PROVES_SIMULATION"
            self._write_subject(target, mutated, fixture, doc)
            errors = validate_anomaly_contact_protocol(target)
            self.assertTrue(any("E8 metaphysical claim ceiling" in error for error in errors))

    def test_meaningful_free_text_cannot_escalate(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(fixture))
            case = next(x for x in mutated["cases"] if x["id"] == "GB-AC-024")
            case["max_state"] = "E7"
            case["expected"] = "CONTACT_HYPOTHESIS_CANDIDATE"
            self._write_subject(target, spec, mutated, doc)
            errors = validate_anomaly_contact_protocol(target)
            self.assertTrue(any("GB-AC-024 escalation expectation drifted" in error for error in errors))

    def test_exact_nonce_success_is_not_contact(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(fixture))
            case = next(x for x in mutated["cases"] if x["id"] == "GB-AC-013")
            case["max_state"] = "E7"
            self._write_subject(target, spec, mutated, doc)
            errors = validate_anomaly_contact_protocol(target)
            self.assertTrue(any("GB-AC-013 escalation expectation drifted" in error for error in errors))

    def test_rival_set_is_closed_h0_through_h15(self) -> None:
        root = Path(__file__).resolve().parents[1]
        spec = json.loads((root / SPEC_PATH).read_text(encoding="utf-8"))
        fixture = json.loads((root / FIXTURE_PATH).read_text(encoding="utf-8"))
        doc = (root / DOC_PATH).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            mutated = json.loads(json.dumps(spec))
            mutated["required_rival_hypotheses"].pop(6)
            self._write_subject(target, mutated, fixture, doc)
            errors = validate_anomaly_contact_protocol(target)
            self.assertTrue(any("exactly H0..H15" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
