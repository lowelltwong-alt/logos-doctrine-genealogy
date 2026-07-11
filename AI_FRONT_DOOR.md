---
object_type: ai_front_door
trust_zone: active_scaffold
lifecycle_status: active
provenance_note: "Created 2026-07-06 by Codex as the required first front door for the scaffold-only doctrine-genealogy repo."
reason_for_inclusion: "Route agents through authority, source-trust, profile-scope, and validation controls before any data work."
---

# AI Front Door

This repo is scaffold-only until a later governed PR authorizes data.

## Mandatory Read Order

1. [AGENTS.md](AGENTS.md)
2. [AI_TABLE_OF_CONTENTS.md](AI_TABLE_OF_CONTENTS.md)
3. [governance/UPSTREAM_GOVERNANCE_CONTRACT.md](governance/UPSTREAM_GOVERNANCE_CONTRACT.md)
4. [governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md](governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md)
5. [governance/SOURCE_TRUST_RULES.md](governance/SOURCE_TRUST_RULES.md)
6. [governance/PROFILE_SCOPE_RULES.md](governance/PROFILE_SCOPE_RULES.md)
7. [governance/THEOLOGIAN_LINEAGE_RELATIONSHIP_RULES.md](governance/THEOLOGIAN_LINEAGE_RELATIONSHIP_RULES.md)

## Authority Boundary

Authority level: `interpretive_historical_profile_scoped`.

This repo may later describe doctrine development, scoped reception, and
historical relationships. It must not become canonical Scripture authority,
final theology authority, graph truth, retrieval truth, vector truth, or a
source-import owner without separate governance approval.

## Current Allowed Work

- Improve scaffold documentation.
- Improve local validators.
- Improve registry mirrors only when they mirror already-approved governance
  values.
- Maintain the non-runtime LLOS v1 adapter and its empty lesson-index bootstrap
  as metadata-only mirrors of the approved upstream standard.
- Prepare review packets for future owner decisions.
- Prepare data-readiness decision packets that remain non-authorizing.

## Current Forbidden Work

- doctrine-lineage records;
- source imports or source rows;
- reviewed-lineage promotion;
- graph/retrieval/vector truth;
- Scripture or chunk output;
- runtime adapters or runtime behavior; the LLOS v1 adapter is metadata-only
  and does not authorize a runtime adapter;
- new relationship verbs, profiles, enum values, authority rungs, or evidence
  utility flags;
- theological classification inferred by AI.

## Validation

Run:

```powershell
python scripts\run_validation_suite.py
python -m pytest -q
git diff --check
```

For LLOS work, also read
[governance/llos_v1_adapter.yaml](governance/llos_v1_adapter.yaml) and
[governance/llos_v1_lesson_index.yaml](governance/llos_v1_lesson_index.yaml).
Logos-local tooling may write its own outbox and pull DAD central candidates.
DAD may read approved outboxes and write its own central records under
`DAD_DATA_ROOT`, but it must not push an inbox or write any Doctrine file.

If a validator blocks the task, do not weaken it locally. Route the question to
`logos-governance-architecture`.

