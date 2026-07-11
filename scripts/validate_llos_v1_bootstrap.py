from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

try:
    from _validation import ROOT, fail
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import ROOT, fail


ADAPTER_PATH = "governance/llos_v1_adapter.yaml"
LESSON_INDEX_PATH = "governance/llos_v1_lesson_index.yaml"

REQUIRED_METADATA = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_runtime_adapters",
    "authorizes_source_authority",
    "authorizes_data_authority",
    "authorizes_theology_authority",
    "authorizes_source_imports",
    "authorizes_source_rows",
    "authorizes_data_records",
    "authorizes_doctrine_lineage_records",
    "authorizes_reviewed_lineage_promotion",
    "authorizes_graph_retrieval_vector_truth",
    "authorizes_lesson_admission",
    "authorizes_lesson_application",
}

REQUIRED_DAD_FALSE = {
    "may_write_doctrine_files",
    "may_mutate_llos_adapter",
    "may_mutate_llos_lesson_index",
    "authority_transfers",
}


def load_governed_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    documents = list(yaml.safe_load_all(text))
    if not documents or any(not isinstance(document, dict) for document in documents):
        raise ValueError(f"{path}: expected governed YAML mappings")

    data: dict[str, Any] = {}
    for document in documents:
        data.update(document)
    return data


def _validate_authority(data: dict[str, Any], label: str, errors: list[str]) -> None:
    authority = data.get("authority")
    if not isinstance(authority, dict):
        errors.append(f"{label} missing authority mapping")
        return

    for key in sorted(REQUIRED_AUTHORITY_FALSE):
        if authority.get(key) is not False:
            errors.append(f"{label} authority.{key} must be false")

    for key, value in authority.items():
        if key.startswith("authorizes_") and value is not False:
            errors.append(f"{label} authority.{key} must be false")


def _validate_dad_bridge(data: dict[str, Any], label: str, errors: list[str]) -> None:
    bridge = data.get("dad_bridge")
    if not isinstance(bridge, dict):
        errors.append(f"{label} missing dad_bridge mapping")
        return

    if bridge.get("may_read_approved_metadata") is not True:
        errors.append(f"{label} dad_bridge.may_read_approved_metadata must be true")
    for key in sorted(REQUIRED_DAD_FALSE):
        if bridge.get(key) is not False:
            errors.append(f"{label} dad_bridge.{key} must be false")
    for key in (
        "requires_new_explicit_approval_for_every_doctrine_write",
        "approval_must_be_fresh_and_explicit",
    ):
        if bridge.get(key) is not True:
            errors.append(f"{label} dad_bridge.{key} must be true")


def _validate_asymmetric_communication(data: dict[str, Any], errors: list[str]) -> None:
    bridge = data.get("dad_bridge")
    if not isinstance(bridge, dict):
        return
    if bridge.get("may_read_approved_logos_outbox") is not True:
        errors.append("adapter dad_bridge.may_read_approved_logos_outbox must be true")
    if bridge.get("may_write_central_dad_records") is not True:
        errors.append("adapter dad_bridge.may_write_central_dad_records must be true")
    if bridge.get("central_write_root") != "DAD_DATA_ROOT":
        errors.append("adapter DAD central writes must remain under DAD_DATA_ROOT")
    if bridge.get("may_push_or_write_logos_inbox") is not False:
        errors.append("adapter dad_bridge.may_push_or_write_logos_inbox must be false")

    local_tooling = data.get("logos_local_tooling")
    if not isinstance(local_tooling, dict):
        errors.append("adapter missing logos_local_tooling mapping")
        return
    if local_tooling.get("may_write_local_outbox") is not True:
        errors.append("adapter Logos-local tooling must be able to write its own outbox")
    if local_tooling.get("may_read_or_pull_dad_central_candidates") is not True:
        errors.append("adapter Logos-local tooling must be able to pull DAD central candidates")
    if local_tooling.get("may_receive_dad_file_push") is not False:
        errors.append("adapter must reject DAD file pushes into Logos")


def _validate_metadata(data: dict[str, Any], label: str, errors: list[str]) -> None:
    for key in sorted(REQUIRED_METADATA):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{label} missing non-empty metadata field: {key}")
    if data.get("trust_zone") != "active_scaffold":
        errors.append(f"{label} trust_zone must be active_scaffold")
    if data.get("lifecycle_status") != "active":
        errors.append(f"{label} lifecycle_status must be active")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    adapter_path = root / ADAPTER_PATH
    index_path = root / LESSON_INDEX_PATH
    if not adapter_path.exists():
        return [f"missing {ADAPTER_PATH}"]
    if not index_path.exists():
        return [f"missing {LESSON_INDEX_PATH}"]

    try:
        adapter = load_governed_yaml(adapter_path)
        index = load_governed_yaml(index_path)
    except (OSError, ValueError, yaml.YAMLError) as error:
        return [str(error)]

    _validate_metadata(adapter, "adapter", errors)
    _validate_metadata(index, "lesson index", errors)
    if adapter.get("object_type") != "llos_v1_adapter":
        errors.append("adapter object_type must be llos_v1_adapter")
    if adapter.get("schema_version") != "logos.llos.adapter.v1":
        errors.append("adapter schema_version must be logos.llos.adapter.v1")
    if adapter.get("adapter_id") != "logos_doctrine_genealogy_llos_v1":
        errors.append("adapter_id must identify the Doctrine LLOS v1 adapter")
    if adapter.get("local_repository") != "logos-doctrine-genealogy":
        errors.append("adapter local_repository must be logos-doctrine-genealogy")

    standard = adapter.get("upstream_standard")
    if not isinstance(standard, dict):
        errors.append("adapter missing upstream_standard mapping")
    elif standard != {
        "repository": "logos-governance-architecture",
        "path": "governance/LOGOS_LEARNING_LOOP_OPERATING_STANDARD.yaml",
        "schema_version": "logos.llos.standard.v1",
        "standard_id": "LLOS-v1",
        "surface_version": "1.0.0",
    }:
        errors.append("adapter upstream_standard must exactly mirror the approved LLOS v1 reference")

    route = adapter.get("route")
    if not isinstance(route, dict) or route.get("id") != "doctrine":
        errors.append("adapter route.id must be doctrine")
    else:
        if route.get("registry_ref") != "logos-governance-architecture:governance/registry/LLOS_ROUTE_REGISTRY.yaml":
            errors.append("adapter route must reference the approved LLOS route registry")
        if route.get("category_allowlist") != [
            "doctrine_scaffold",
            "profile_scope",
            "lineage_validation",
            "source_trust",
        ]:
            errors.append("adapter route category allowlist must match the approved doctrine route")
    _validate_authority(adapter, "adapter", errors)
    _validate_dad_bridge(adapter, "adapter", errors)
    _validate_asymmetric_communication(adapter, errors)

    _validate_authority(index, "lesson index", errors)
    _validate_dad_bridge(index, "lesson index", errors)
    if index.get("object_type") != "llos_v1_lesson_index":
        errors.append("lesson index object_type must be llos_v1_lesson_index")
    if index.get("schema_version") != "logos.llos.lesson_index.v1":
        errors.append("lesson index schema_version must be logos.llos.lesson_index.v1")
    if index.get("index_id") != "logos_doctrine_genealogy_llos_v1":
        errors.append("lesson index must identify the Doctrine LLOS v1 index")
    if index.get("adapter_ref") != ADAPTER_PATH:
        errors.append("lesson index adapter_ref must point to the local adapter")
    if index.get("local_repository") != "logos-doctrine-genealogy":
        errors.append("lesson index local_repository must be logos-doctrine-genealogy")
    if index.get("route") != "doctrine":
        errors.append("lesson index route must be doctrine")
    if index.get("state") != "empty_bootstrap":
        errors.append("lesson index state must be empty_bootstrap")

    admission = index.get("admission")
    if admission != {
        "standard_ref": "logos-governance-architecture:governance/LOGOS_LEARNING_LOOP_OPERATING_STANDARD.yaml",
        "human_review_required": True,
        "records_present": False,
    }:
        errors.append("lesson index admission must preserve the approved empty-bootstrap gate")
    if index.get("lessons") != []:
        errors.append("lesson index must remain empty; lesson admission requires a future explicit approval")
    if index.get("lesson_graph") != []:
        errors.append("lesson index graph must remain empty; graph authority is not authorized")

    suite_path = root / "scripts/run_validation_suite.py"
    if not suite_path.exists() or '"llos_v1_bootstrap", "validate_llos_v1_bootstrap"' not in suite_path.read_text(encoding="utf-8"):
        errors.append("validation suite must run validate_llos_v1_bootstrap")

    for rel in ("AI_FRONT_DOOR.md", "AI_TABLE_OF_CONTENTS.md", "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml"):
        path = root / rel
        if not path.exists() or ADAPTER_PATH not in path.read_text(encoding="utf-8"):
            errors.append(f"{rel} must reference {ADAPTER_PATH}")
    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("LLOS v1 Doctrine bootstrap validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
