---
object_type: ai_table_of_contents
trust_zone: active_scaffold
lifecycle_status: active
provenance_note: "Created 2026-07-06 by Codex to make the scaffold guardrails findable for future AI agents and reviewers."
reason_for_inclusion: "Agents need tags and read-when guidance for authority, source-trust, scope, validators, and empty data boundaries."
---

# AI Table Of Contents

## Start Here

- [README.md](README.md) - tags: `overview`, `authority-boundary`, `scaffold-only`; read when orienting to the repo role.
- [AGENTS.md](AGENTS.md) - tags: `agent-rules`, `startup`, `non-authorizations`; read before AI-assisted edits.
- [AI_FRONT_DOOR.md](AI_FRONT_DOOR.md) - tags: `front-door`, `routing`, `validation`; read before choosing a task lane.

## Governance

- [governance/UPSTREAM_GOVERNANCE_CONTRACT.md](governance/UPSTREAM_GOVERNANCE_CONTRACT.md) - tags: `upstream-governance`, `authority-direction`, `issue-83`; read when checking whether this repo may own a task.
- [governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md](governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md) - tags: `non-authorizations`, `authority`, `stop-rules`; read before any implementation proposal.
- [governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml](governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml) - tags: `governance-mirror`, `dependency-map`, `validators`; read when changing front doors, registry mirrors, or validators.
- [governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR_CONTROL.md](governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR_CONTROL.md) - tags: `mirror-control`, `fail-closed`, `upstream`; read when updating mirror coverage.
- [governance/SOURCE_TRUST_RULES.md](governance/SOURCE_TRUST_RULES.md) - tags: `source-trust`, `licensing`, `source-imports`; read before any source-intake idea.
- [governance/PROFILE_SCOPE_RULES.md](governance/PROFILE_SCOPE_RULES.md) - tags: `profile-scope`, `tradition-scope`, `anti-collapse`; read before scoped doctrine work.
- [governance/THEOLOGIAN_LINEAGE_RELATIONSHIP_RULES.md](governance/THEOLOGIAN_LINEAGE_RELATIONSHIP_RULES.md) - tags: `relationship-verbs`, `lineage`, `anti-guessing`; read before edge or relationship work.

## Registry Mirrors

- [registry/README.md](registry/README.md) - tags: `registry`, `mirrors`, `governance-owned-values`.
- [registry/controlled_values_mirror.yaml](registry/controlled_values_mirror.yaml) - tags: `controlled-values`, `verbs`, `profiles`, `authority-rungs`.
- [registry/profile_scopes.yaml](registry/profile_scopes.yaml) - tags: `profile-scopes`, `tradition-scope`.
- [registry/source_trust_tiers.yaml](registry/source_trust_tiers.yaml) - tags: `source-trust`, `authority-rungs`, `no-source-rows`.

## Data And Schemas

- [data/README.md](data/README.md) - tags: `empty-data`, `no-records`; read before adding anything under `data/`.
- [schemas/README.md](schemas/README.md) - tags: `schema-mirror`, `governance-owned`; read before schema work.
- [schemas/doctrine_genealogy/README.md](schemas/doctrine_genealogy/README.md) - tags: `doctrine-genealogy-schema`, `non-authorizing`.

## Roadmap And Review

- [docs/roadmap/data-readiness-decision-packet.md](docs/roadmap/data-readiness-decision-packet.md) - tags: `data-readiness`, `owner-gate`, `non-authorizing`, `source-intake`, `schema-mirror`, `evidence-harness`; read before proposing source intake, schema mirroring, first doctrine-slice work, examples, or data.
- [docs/roadmap/data-readiness-lane-implementation-runbook.md](docs/roadmap/data-readiness-lane-implementation-runbook.md) - tags: `data-readiness`, `implementation-runbook`, `preflight`, `owner-gate`, `non-authorizing`; read after an owner selects one DR-OPTION lane and before any lane implementation PR.
- [docs/roadmap/data-readiness-owner-decision-template.md](docs/roadmap/data-readiness-owner-decision-template.md) - tags: `owner-decision`, `data-readiness`, `lane-selection`, `audit`, `non-authorizing`; read when recording or checking an owner lane selection.
- [.github/ISSUE_TEMPLATE/data_readiness_lane_selection.yml](.github/ISSUE_TEMPLATE/data_readiness_lane_selection.yml) - tags: `github-issue`, `owner-decision`, `data-readiness`, `lane-selection`; use to open the formal owner decision issue.
- [docs/roadmap/first-task-and-readiness.md](docs/roadmap/first-task-and-readiness.md) - tags: `first-task`, `readiness`, `why-this-repo-exists`.
- [docs/governance/promotion-gates.md](docs/governance/promotion-gates.md) - tags: `promotion`, `reviewed-lineage`, `owner-gate`.

## Validators

- [scripts/run_validation_suite.py](scripts/run_validation_suite.py) - tags: `validation-suite`, `scaffold`.
- [scripts/validate_governance_dependency_map_mirror.py](scripts/validate_governance_dependency_map_mirror.py) - tags: `governance-mirror`.
- [scripts/validate_source_trust_rules.py](scripts/validate_source_trust_rules.py) - tags: `source-trust`.
- [scripts/validate_profile_scope_rules.py](scripts/validate_profile_scope_rules.py) - tags: `profile-scope`.
- [scripts/validate_theologian_lineage_relationship_rules.py](scripts/validate_theologian_lineage_relationship_rules.py) - tags: `relationship-verbs`.
- [scripts/validate_no_authority_leakage.py](scripts/validate_no_authority_leakage.py) - tags: `authority-leakage`, `non-authorizations`.
- [scripts/validate_data_readiness_packet.py](scripts/validate_data_readiness_packet.py) - tags: `data-readiness`, `roadmap`, `owner-gate`, `non-authorizing`.
- [scripts/validate_data_readiness_owner_gate.py](scripts/validate_data_readiness_owner_gate.py) - tags: `owner-decision`, `data-readiness`, `issue-template`, `lane-selection`, `non-authorizing`.
- [scripts/validate_data_readiness_runbook.py](scripts/validate_data_readiness_runbook.py) - tags: `data-readiness`, `implementation-runbook`, `preflight`, `non-authorizing`.

