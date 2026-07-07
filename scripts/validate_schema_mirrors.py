from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

try:
    from _validation import ROOT, fail, has_true_authorization, read_text, unexpected_data_files
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import ROOT, fail, has_true_authorization, read_text, unexpected_data_files


MANIFEST_PATH = "schemas/doctrine_genealogy/schema_mirror_manifest.yaml"
SCHEMA_DIR = "schemas/doctrine_genealogy"

EXPECTED_MIRRORS = {
    "schemas/doctrine_genealogy/date_block.v1.schema.json": (
        "87b04f72a5241638e40f7b8e9a2334155dd1e0e4153de2ce635563922e4916b0",
        "json_schema",
    ),
    "schemas/doctrine_genealogy/doctrine_provenance.v1.schema.json": (
        "c3893e3efb4f02ee62b7a93d2f0698260337d46d9f56fb4e118fb7db1c30bb63",
        "json_schema",
    ),
    "schemas/doctrine_genealogy/doctrine_node.v1.schema.json": (
        "b3efad1c14c1cc583ae1828e943b751dfb9673875c0e39223a607763ef9323d7",
        "json_schema",
    ),
    "schemas/doctrine_genealogy/genealogy_edge.v1.schema.json": (
        "a5305b8718b032583b86859bba65d33e8094d2851a79945d12ace37ba9c4e7e1",
        "json_schema",
    ),
    "schemas/doctrine_genealogy/evidence_packet.v1.schema.json": (
        "70cdf5a9da37c20b5aab65dff46447bb2f53453e92a9a6a04dd95098d19d4b78",
        "json_schema",
    ),
    "schemas/doctrine_genealogy/gate_trigger_registry.v1.yaml": (
        "4cfc16da3ca8f721e1318c32a427a91b70c81e78185aea755422f9e42fc59dbd",
        "gate_trigger_registry",
    ),
}

ALLOWED_SCHEMA_DIR_FILES = {
    "README.md",
    "schema_mirror_manifest.yaml",
    *{Path(path).name for path in EXPECTED_MIRRORS},
}

REQUIRED_MANIFEST_TOKENS = {
    "object_type: doctrine_genealogy_schema_mirror_manifest",
    "trust_zone: active_scaffold",
    "lifecycle_status: active",
    "selected_lane: DR-OPTION-A",
    "issue: https://github.com/lowelltwong-alt/logos-doctrine-genealogy/issues/4",
    "decision_comment: https://github.com/lowelltwong-alt/logos-doctrine-genealogy/issues/4#issuecomment-4899887684",
    "source_commit: b456a28a4bdc15e4222638e1d89a1f5097c07116",
    "local_schema_mirrors_are_source_of_truth: false",
    "authorizes_doctrine_lineage_records: false",
    "authorizes_source_imports: false",
    "authorizes_source_rows: false",
    "authorizes_reviewed_lineage_promotion: false",
    "authorizes_graph_retrieval_vector_truth: false",
    "authorizes_scripture_or_chunk_output: false",
    "authorizes_new_vocabularies: false",
    "authorizes_runtime_adapters: false",
    "authorizes_theology_authority: false",
}

REQUIRED_GATE_TRIGGER_TOKENS = {
    "object_type: doctrine_genealogy_gate_trigger_registry",
    "orthodox_original_language_pressure_dossier_queue",
    "textual_variant_source_tradition_dossier_queue",
    "preferred_reading_selection",
    "source_tradition_preference",
    "gate_completion_by_ai_parse",
    "scripture_policy_fork",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_block_for(text: str, path: str) -> str:
    pattern = re.compile(rf"  - path: {re.escape(path)}\n(?P<body>(?:    .+\n?)*)")
    match = pattern.search(text)
    if not match:
        return ""
    return match.group(0)


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifest = root / MANIFEST_PATH
    if not manifest.exists():
        return [f"missing {MANIFEST_PATH}"]

    manifest_text = read_text(root, MANIFEST_PATH)
    for token in sorted(REQUIRED_MANIFEST_TOKENS):
        if token not in manifest_text:
            errors.append(f"schema mirror manifest missing required token: {token}")

    for field in has_true_authorization(manifest_text):
        errors.append(f"schema mirror manifest sets authority field true: {field}")

    for rel, (expected_hash, expected_kind) in EXPECTED_MIRRORS.items():
        path = root / rel
        if not path.exists():
            errors.append(f"missing mirrored schema file: {rel}")
            continue

        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            errors.append(f"schema mirror hash mismatch: {rel} expected {expected_hash} got {actual_hash}")

        block = manifest_block_for(manifest_text, rel)
        if not block:
            errors.append(f"schema mirror manifest missing block for {rel}")
        else:
            for token in [
                f"source_path: {rel}",
                f"sha256: {expected_hash}",
                f"file_kind: {expected_kind}",
            ]:
                if token not in block:
                    errors.append(f"schema mirror manifest block for {rel} missing {token}")

        if expected_kind == "json_schema":
            try:
                parsed = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON schema syntax in {rel}: {exc}")
            else:
                if parsed.get("$comment") != "draft, non-authorizing, owner decisions D1-D10 apply":
                    errors.append(f"schema mirror missing non-authorizing comment: {rel}")
                if parsed.get("x-governance", {}).get("object_type") != "doctrine_genealogy_schema":
                    errors.append(f"schema mirror missing doctrine_genealogy_schema object_type: {rel}")

    gate_text = read_text(root, "schemas/doctrine_genealogy/gate_trigger_registry.v1.yaml")
    for token in sorted(REQUIRED_GATE_TRIGGER_TOKENS):
        if token not in gate_text:
            errors.append(f"gate trigger registry mirror missing required token: {token}")

    schema_dir = root / SCHEMA_DIR
    actual_names = {path.name for path in schema_dir.iterdir() if path.is_file()}
    for name in sorted(actual_names - ALLOWED_SCHEMA_DIR_FILES):
        errors.append(f"unexpected schema mirror file: {SCHEMA_DIR}/{name}")

    for rel in unexpected_data_files(root):
        errors.append(f"schema mirror lane introduced forbidden data file: {rel}")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Schema mirror validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
