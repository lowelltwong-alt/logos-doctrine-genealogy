---
object_type: doctrine_genealogy_schema_mirror_readme
trust_zone: active_scaffold
lifecycle_status: active
provenance_note: "Created 2026-07-06 by Codex to point to governance-owned doctrine-genealogy schema standards. Updated 2026-07-07 after owner authorized DR-OPTION-A to mirror already-approved governance schema standards locally."
reason_for_inclusion: "Keep future schema work tied to the upstream Fable kernel standards and non-authorizations while allowing local validation against data-free schema mirrors."
---

# Doctrine-Genealogy Schema Mirrors

This directory contains data-free local mirrors of the approved upstream schema
standards from:

`logos-governance-architecture/schemas/doctrine_genealogy/`

The local mirrors are locked by
[schema_mirror_manifest.yaml](schema_mirror_manifest.yaml) and
`scripts/validate_schema_mirrors.py`.

## Mirrored Files

- `date_block.v1.schema.json`
- `doctrine_provenance.v1.schema.json`
- `doctrine_node.v1.schema.json`
- `genealogy_edge.v1.schema.json`
- `evidence_packet.v1.schema.json`
- `gate_trigger_registry.v1.yaml`

## Authority Boundary

These files mirror governance-owned standards. They are not the local source of
truth and may not expand schema authority, mint vocabulary, authorize doctrine
records, authorize source imports, promote reviewed lineage, create
graph/retrieval/vector truth, change Scripture/chunk output, create runtime
adapters, or create theology authority.

