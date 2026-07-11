from __future__ import annotations

from pathlib import Path

try:
    from _validation import (
        REQUIRED_FALSE_AUTHORIZATIONS,
        ROOT,
        fail,
        has_true_authorization,
        read_text,
        unexpected_data_files,
    )
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import (
        REQUIRED_FALSE_AUTHORIZATIONS,
        ROOT,
        fail,
        has_true_authorization,
        read_text,
        unexpected_data_files,
    )


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    authority_path = root / "governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md"
    mirror_path = root / "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml"
    if not authority_path.exists():
        return ["missing governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md"]

    authority_text = read_text(root, "governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md")
    for field in sorted(REQUIRED_FALSE_AUTHORIZATIONS):
        if f"{field}: false" not in authority_text:
            errors.append(f"authority rules missing false assertion: {field}: false")

    for rel in [
        "governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md",
        "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml",
    ]:
        if (root / rel).exists():
            for field in has_true_authorization(read_text(root, rel)):
                errors.append(f"authority leakage: {rel} sets {field}: true")

    if mirror_path.exists():
        mirror_text = read_text(root, "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml")
        for token in [
            "authorizes_child_repo_override: false",
            "authorizes_doctrine_lineage_records: false",
            "authorizes_source_imports: false",
            "authorizes_reviewed_lineage_promotion: false",
            "authorizes_graph_retrieval_vector_truth: false",
            "authorizes_scripture_or_chunk_output: false",
            "authorizes_new_vocabularies: false",
            "authorizes_runtime_adapters: false",
        ]:
            if token not in mirror_text:
                errors.append(f"mirror missing no-authority token: {token}")

    for rel in unexpected_data_files(root):
        errors.append(f"data file creates scaffold authority risk: {rel}")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("No authority leakage validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
