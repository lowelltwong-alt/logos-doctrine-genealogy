---
object_type: theologian_lineage_relationship_rules
trust_zone: active_scaffold
lifecycle_status: active
provenance_note: "Created 2026-07-06 by Codex from governance-owned relationship registry D4."
reason_for_inclusion: "Keep doctrine-lineage relationships precise, sourced, scoped, and non-inferred."
---

# Theologian Lineage Relationship Rules

Approved doctrine-genealogy relationship verbs are mirrored in
[../registry/controlled_values_mirror.yaml](../registry/controlled_values_mirror.yaml).

Rules:

- Use only governance-approved verbs.
- `related_to` and `influences` are forbidden for doctrine-genealogy asserted
  edges.
- `condemns` and `is_condemned_by` are not hand-authored edges. Condemnation
  must be represented by a scoped assessment object in a future authorized data
  model.
- Gate fields such as `requires_original_language_review` and
  `requires_textual_critical_review` are not relationship verbs.
- Semantic similarity, embeddings, co-occurrence, graph rank, and generated
  confidence may create review candidates only.
- A future real relationship must carry source basis, authority owner, scope,
  method, review status, date discipline, and provenance.

