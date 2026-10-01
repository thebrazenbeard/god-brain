from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SOURCE_SPEC = "specs/research/GOD_BRAIN_SOURCE_UNIVERSE_V3.json"
TOOL_SPEC = "specs/research/GOD_BRAIN_TOOL_CAPABILITY_REGISTRY_V1.json"
SOURCE_DOC = "docs/research/cross-repo-synthesis/SOURCE_UNIVERSE_V3_2026-10-01.md"
TOOL_DOC = "docs/architecture/EXTERNAL_TOOL_AND_PLUGIN_FABRIC_V1.md"
GAP_DOC = "docs/research/cross-repo-synthesis/TRANSFER_GAP_ANALYSIS_V3_2026-10-01.md"

SHA40 = re.compile(r"^[0-9a-f]{40}$")

REQUIRED_SOURCE_INVARIANTS = {
    "SOURCE_PRESENCE_NE_ARCHITECTURAL_ADMISSION",
    "PORTFOLIO_REUSE_NE_RUNTIME_COUPLING",
    "SHARED_MECHANISM_NE_MANDATORY_SHARED_SERVICE",
    "COPIED_LINEAGE_NE_INDEPENDENT_CORROBORATION",
    "PRIVATE_PAYLOAD_NE_PORTABLE_SOURCE",
    "REPOSITORY_LOCAL_AUTHORITY_NE_GOD_BRAIN_AUTHORITY",
    "OBSERVED_HEAD_NE_FUTURE_CURRENTNESS",
    "CASE_STUDY_NE_ARCHITECTURE_PROOF",
    "REVIEW_METHOD_NE_INDEPENDENT_REVIEW",
    "TOOL_AVAILABILITY_NE_COGNITIVE_SUBSYSTEM",
}

REQUIRED_TOOL_INVARIANTS = {
    "TOOL_AVAILABILITY_NE_ARCHITECTURAL_ADMISSION",
    "TOOL_AVAILABILITY_NE_AUTHORITY",
    "CONNECTED_ACCOUNT_NE_PERMISSION",
    "TOOL_OUTPUT_NE_VERIFICATION",
    "PLUGIN_INSTALLATION_NE_ALWAYS_ON_EXECUTION",
    "EXTERNAL_SERVICE_NE_SEAT_OF_COGNITION",
    "RESEARCH_CONNECTOR_NE_PRIMARY_SOURCE_AUTHORITY",
    "WORKSTATION_ACCESS_NE_EFFECT_AUTHORITY",
    "DEPLOYMENT_CAPABILITY_NE_DEPLOYMENT_AUTHORITY",
    "PRIVATE_TOOL_DATA_NE_PORTABLE_TRAINING_DATA",
}

REQUIRED_TRANSFER_IDS = {f"T{i}" for i in range(30, 41)}

def _load(root: Path, relative: str) -> dict[str, Any]:
    value = json.loads((root / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative} root must be object")
    return value

def _closed_unique_list(errors: list[str], value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be list")
        return
    if len(value) != len(set(value)):
        errors.append(f"{label} must be unique")
    if set(value) != expected:
        errors.append(f"{label} must be exact closed set")

def validate_source_universe_v3(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in (SOURCE_SPEC, TOOL_SPEC, SOURCE_DOC, TOOL_DOC, GAP_DOC):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        source = _load(root, SOURCE_SPEC)
        tools = _load(root, TOOL_SPEC)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid V3 contract: {exc}"]

    if source.get("schema_version") != "GOD_BRAIN_SOURCE_UNIVERSE_V3":
        errors.append("source schema_version drifted")
    if source.get("status") != "RESEARCH_INTAKE_NO_PROMOTION":
        errors.append("source status must remain research-only")
    if source.get("god_brain_main_head") != "495c2b42932153cba0926744d04a69bc34557f81":
        errors.append("God Brain assessment base drifted")
    if source.get("live_repository_count") != 78:
        errors.append("live repository census must remain 78 for this assessment")
    if source.get("user_inventory_claimed_count") != 76 or source.get("user_inventory_named_rows") != 66:
        errors.append("user inventory discrepancy binding drifted")
    _closed_unique_list(errors, source.get("invariants"), REQUIRED_SOURCE_INVARIANTS, "source invariants")

    sources = source.get("sources")
    if not isinstance(sources, list):
        errors.append("sources must be list")
        sources = []
    if len(sources) != 78:
        errors.append("sources must contain exactly 78 entries")
    ids = [x.get("id") for x in sources if isinstance(x, dict)]
    if len(ids) != len(set(ids)):
        errors.append("source ids must be unique")

    source_ids = set(ids)
    for item in sources:
        if not isinstance(item, dict):
            errors.append("source entry must be object")
            continue
        sid = item.get("id")
        repo = item.get("repository")
        if repo != f"thebrazenbeard/{sid}":
            errors.append(f"{sid}: repository binding drifted")
        if item.get("class") in (None, "UNCLASSIFIED"):
            errors.append(f"{sid}: source class missing/unclassified")
        if not item.get("disposition"):
            errors.append(f"{sid}: disposition missing")
        if item.get("visibility") not in {"public", "private"}:
            errors.append(f"{sid}: visibility invalid")
        cut = item.get("evidence_cut")
        if not isinstance(cut, dict) or cut.get("ref") != "main":
            errors.append(f"{sid}: evidence_cut must bind main")
            continue
        head = cut.get("exact_head")
        if head is not None and (not isinstance(head, str) or not SHA40.fullmatch(head)):
            errors.append(f"{sid}: exact_head must be lowercase 40-hex")
        if cut.get("binding") not in {
            "EXACT_HEAD_OBSERVED_2026_10_01",
            "REFRESH_REQUIRED_BEFORE_TRANSFER",
        }:
            errors.append(f"{sid}: evidence binding invalid")

    transfers = source.get("transfer_candidates")
    if not isinstance(transfers, list):
        errors.append("transfer_candidates must be list")
        transfers = []
    transfer_ids = {x.get("id") for x in transfers if isinstance(x, dict)}
    if transfer_ids != REQUIRED_TRANSFER_IDS:
        errors.append("transfer candidate ids must be exactly T30..T40")
    for item in transfers:
        if not isinstance(item, dict):
            continue
        for sid in item.get("sources", []):
            if sid not in source_ids:
                errors.append(f"{item.get('id')}: unknown source {sid}")

    if "NO_RUNTIME_DEPENDENCY_ADMISSION" not in set(source.get("claim_ceiling", [])):
        errors.append("source claim ceiling must prohibit runtime dependency admission")
    if "NO_PRIVATE_PAYLOAD_TRANSFER" not in set(source.get("claim_ceiling", [])):
        errors.append("source claim ceiling must prohibit private payload transfer")

    if tools.get("schema_version") != "GOD_BRAIN_TOOL_CAPABILITY_REGISTRY_V1":
        errors.append("tool schema_version drifted")
    if tools.get("live_namespace_count") != 39:
        errors.append("live tool namespace census must remain 39 for this assessment")
    if tools.get("user_inventory_claimed_count") != 38 or tools.get("user_inventory_named_rows") != 35:
        errors.append("user tool inventory discrepancy binding drifted")
    _closed_unique_list(errors, tools.get("invariants"), REQUIRED_TOOL_INVARIANTS, "tool invariants")

    namespaces = tools.get("namespaces")
    if not isinstance(namespaces, list):
        errors.append("namespaces must be list")
        namespaces = []
    if len(namespaces) != 39:
        errors.append("namespaces must contain exactly 39 entries")
    names = [x.get("name") for x in namespaces if isinstance(x, dict)]
    if len(names) != len(set(names)):
        errors.append("tool namespace names must be unique")
    for item in namespaces:
        if not isinstance(item, dict):
            errors.append("tool namespace entry must be object")
            continue
        if item.get("class") in (None, "UNCLASSIFIED"):
            errors.append(f"{item.get('name')}: tool class missing/unclassified")
        if item.get("runtime_dependency") is not False:
            errors.append(f"{item.get('name')}: runtime_dependency must remain false")
        if not item.get("disposition"):
            errors.append(f"{item.get('name')}: disposition missing")

    overlays = tools.get("installed_skill_overlays")
    if not isinstance(overlays, list) or not any(x.get("name") == "cricket-conscience" for x in overlays if isinstance(x, dict)):
        errors.append("Cricket skill overlay binding missing")

    source_doc = (root / SOURCE_DOC).read_text(encoding="utf-8")
    tool_doc = (root / TOOL_DOC).read_text(encoding="utf-8")
    gap_doc = (root / GAP_DOC).read_text(encoding="utf-8")
    for marker in (
        "HUMAN_INVENTORY != LIVE_PROVIDER_CENSUS",
        "SOURCE_PRESENCE != ARCHITECTURAL_ADMISSION",
        "PORTFOLIO_REUSE != PORTFOLIO_COUPLING",
        "COPIED_LINEAGE != INDEPENDENT_CORROBORATION",
    ):
        if marker not in source_doc:
            errors.append(f"source doc missing marker: {marker}")
    for marker in (
        "TOOL_AVAILABILITY != ARCHITECTURAL_ADMISSION",
        "TOOL_AVAILABILITY != AUTHORITY",
        "CONNECTED_ACCOUNT != PERMISSION",
        "EXTERNAL_SERVICE != SEAT_OF_COGNITION",
        "CRICKET_REVIEW != INDEPENDENT_REVIEW",
    ):
        if marker not in tool_doc:
            errors.append(f"tool doc missing marker: {marker}")
    if "GOD_BRAIN_INTAKE_AND_EVIDENCE_ADMISSION_CONTRACT_V0_1" not in gap_doc:
        errors.append("gap analysis missing recommended next bounded subject")

    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate_source_universe_v3(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("God Brain Source Universe V3 + Tool Fabric V1: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
