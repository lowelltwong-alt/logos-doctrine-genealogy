from __future__ import annotations

from pathlib import Path

try:
    from _validation import REQUIRED_LOCAL_PATHS, ROOT, fail, missing_paths, read_text
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import REQUIRED_LOCAL_PATHS, ROOT, fail, missing_paths, read_text


REQUIRED_MIRROR_TOKENS = {
    "source_of_truth_repo: logos-governance-architecture",
    "registration_issue: https://github.com/lowelltwong-alt/logos-governance-architecture/issues/83",
    "owner_acceptance_comment: https://github.com/lowelltwong-alt/logos-governance-architecture/issues/83#issuecomment-4896715109",
    "owner_decision_record: FABLE-D1-D10-2026-07-06",
    "authority_level: interpretive_historical_profile_scoped",
    "replaces_upstream_governance: false",
    "authorizes_child_repo_override: false",
    "authorizes_doctrine_lineage_records: false",
    "authorizes_source_imports: false",
    "authorizes_reviewed_lineage_promotion: false",
    "authorizes_graph_retrieval_vector_truth: false",
    "authorizes_scripture_or_chunk_output: false",
    "authorizes_new_vocabularies: false",
}

REQUIRED_UPSTREAM_PATH_TOKENS = {
    "governance/LOGOS_REPO_REGISTRY.yaml",
    "governance/REPOSITORY_LINK_CONTRACTS.md",
    "governance/ADDING_NEW_LOGOS_REPOS.md",
    "docs/roadmap/fable-kernels/OWNER-DECISIONS-AND-PILOTS.md",
    "docs/roadmap/fable-kernels/COMPLETION_AUDIT.md",
    "incoming/research/doctrine-genealogy-registration/scaffold_blueprint.md",
}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    mirror_path = root / "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml"
    if not mirror_path.exists():
        return ["missing governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml"]

    mirror_text = read_text(root, "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml")
    for token in sorted(REQUIRED_MIRROR_TOKENS | REQUIRED_UPSTREAM_PATH_TOKENS):
        if token not in mirror_text:
            errors.append(f"mirror missing required token: {token}")

    for path in missing_paths(root, REQUIRED_LOCAL_PATHS):
        errors.append(f"required local scaffold path missing: {path}")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Governance dependency map mirror validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
