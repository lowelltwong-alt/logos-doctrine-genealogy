from __future__ import annotations

from pathlib import Path

try:
    from _validation import ROOT, fail, read_text, unexpected_data_files
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import ROOT, fail, read_text, unexpected_data_files


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    required_files = [
        "governance/SOURCE_TRUST_RULES.md",
        "registry/source_trust_tiers.yaml",
        "data/README.md",
        "data/.gitkeep",
    ]
    for rel in required_files:
        if not (root / rel).exists():
            errors.append(f"missing source-trust scaffold file: {rel}")

    if (root / "registry/source_trust_tiers.yaml").exists():
        text = read_text(root, "registry/source_trust_tiers.yaml")
        for token in ["source_rows_authorized: false", "source_imports_authorized: false"]:
            if token not in text:
                errors.append(f"source trust tiers missing {token}")

    for rel in unexpected_data_files(root):
        errors.append(f"data file is not authorized in scaffold: {rel}")

    for forbidden_dir in ["sources", "source_rows", "imports", "corpus", "corpora"]:
        if (root / forbidden_dir).exists():
            errors.append(f"source/import directory is not authorized: {forbidden_dir}")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Source trust validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
