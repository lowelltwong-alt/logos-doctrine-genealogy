---
object_type: repository_readme
trust_zone: active_scaffold
lifecycle_status: active
provenance_note: "Created 2026-07-06 by Codex after owner acceptance of logos-governance-architecture Issue #83 for scaffold-only repo creation."
reason_for_inclusion: "State the repo role, authority boundary, non-authorizations, and validation commands before any doctrine-lineage data exists."
---

# Logos Doctrine Genealogy

`logos-doctrine-genealogy` is the doctrine lineage and profile-comparison plane
for the Logos project family.

Current status: scaffold-only, data-free.

Authority level: `interpretive_historical_profile_scoped`.

This repo may later hold governed doctrine-lineage, tradition/profile scoped
claims, theologian-to-theologian development records, and human judgment gates.
It is not ready for those records yet. The initial scaffold establishes front
doors, mirrors, source-trust rules, profile-scope rules, relationship-verb
controls, and fail-closed validators before data can exist.

## Non-Authorizations

This scaffold does not authorize:

- doctrine-lineage records;
- source imports or source rows;
- reviewed-lineage promotion;
- graph truth, retrieval truth, or vector truth;
- Scripture text or chunk output;
- new relationship verbs, profiles, enum values, authority rungs, or evidence
  utility flags;
- theology authority.

## Required Entry Points

Read these before editing:

- [AGENTS.md](AGENTS.md)
- [AI_FRONT_DOOR.md](AI_FRONT_DOOR.md)
- [AI_TABLE_OF_CONTENTS.md](AI_TABLE_OF_CONTENTS.md)
- [governance/UPSTREAM_GOVERNANCE_CONTRACT.md](governance/UPSTREAM_GOVERNANCE_CONTRACT.md)
- [governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md](governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md)

## Validation

```powershell
python scripts\validate_governance_dependency_map_mirror.py
python scripts\validate_source_trust_rules.py
python scripts\validate_profile_scope_rules.py
python scripts\validate_theologian_lineage_relationship_rules.py
python scripts\validate_no_authority_leakage.py
python scripts\run_validation_suite.py
python -m pytest -q
git diff --check
```

The validators are intentionally conservative. If they block useful work, route
the decision back through `logos-governance-architecture` instead of weakening
this repo locally.

