---
object_type: repository_governance_contract
trust_zone: active_scaffold
lifecycle_status: active
provenance_note: "Created 2026-07-06 by Codex from the governed scaffold blueprint after owner acceptance of Issue #83."
reason_for_inclusion: "Keep local AI-assisted work bound to the upstream governance contract before any doctrine-lineage data exists."
---

# AGENTS.md

## Project Intent

This repository is a governed doctrine-lineage and profile-comparison plane for
the Logos project family.

Optimize for provenance, scope clarity, source-trust discipline, and human
review gates. Do not optimize for early data volume.

## Live-Main Startup

Before new AI-assisted work:

```powershell
git status
git branch --show-current
git fetch origin --prune --tags
git checkout main
git pull --ff-only origin main
git status
git log --oneline --decorate -n 8
```

If there is uncommitted work, divergence, a non-fast-forward condition, or an
untracked-file risk, stop and report before editing.

## Non-Negotiable Rules

- `logos-governance-architecture` is the source of truth for repo authority,
  relationship contracts, controlled vocabulary, and governance dependency-map
  requirements.
- This repo may mirror governance values for validation, but it must not
  redefine, expand, or weaken them.
- Do not add doctrine-lineage data records before validators and source/profile
  gates explicitly permit them.
- Do not import source text, commentary corpora, or source rows in scaffold
  work.
- Do not create Scripture output, chunk output, graph truth, retrieval truth, or
  vector truth.
- Do not infer theology from AI output, semantic similarity, embeddings, graph
  rank, generated confidence, issue text, comments, or PR bodies.
- Preserve disputed doctrine scope instead of collapsing it into universal
  truth.
- If a needed value is missing, route the decision to
  `logos-governance-architecture`; do not mint it locally.

## Required Metadata

Meaningful Markdown or YAML additions should identify:

- `object_type`
- `trust_zone`
- `lifecycle_status`
- `provenance_note`
- `reason_for_inclusion`

## Definition Of Done

Before finishing:

- run `python scripts\run_validation_suite.py`;
- run `python -m pytest -q`;
- run `git diff --check`;
- confirm no data records or source imports were added unless separately
  authorized;
- leave the worktree clean.

