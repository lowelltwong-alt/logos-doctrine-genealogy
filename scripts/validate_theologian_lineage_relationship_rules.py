from __future__ import annotations

from pathlib import Path

try:
    from _validation import (
        EXPECTED_RELATIONSHIP_VERBS,
        FORBIDDEN_RELATIONSHIP_VERBS,
        ROOT,
        extract_verb_entries,
        fail,
        read_text,
    )
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import (
        EXPECTED_RELATIONSHIP_VERBS,
        FORBIDDEN_RELATIONSHIP_VERBS,
        ROOT,
        extract_verb_entries,
        fail,
        read_text,
    )


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    mirror_path = root / "registry/controlled_values_mirror.yaml"
    rules_path = root / "governance/THEOLOGIAN_LINEAGE_RELATIONSHIP_RULES.md"
    if not mirror_path.exists():
        return ["missing registry/controlled_values_mirror.yaml"]
    if not rules_path.exists():
        errors.append("missing governance/THEOLOGIAN_LINEAGE_RELATIONSHIP_RULES.md")

    text = read_text(root, "registry/controlled_values_mirror.yaml")
    verbs = extract_verb_entries(text)
    missing = EXPECTED_RELATIONSHIP_VERBS - verbs
    extra = verbs - EXPECTED_RELATIONSHIP_VERBS
    for value in sorted(missing):
        errors.append(f"relationship verb missing from mirror: {value}")
    for value in sorted(extra):
        errors.append(f"relationship verb not approved for doctrine genealogy: {value}")

    for value in sorted(FORBIDDEN_RELATIONSHIP_VERBS):
        if f"  - {value}" not in text:
            errors.append(f"forbidden relationship verb not listed as forbidden: {value}")
        if f"- verb: {value}" in text:
            errors.append(f"forbidden relationship verb appears as approved: {value}")

    if "local_vocabulary_authority: false" not in text:
        errors.append("controlled value mirror must set local_vocabulary_authority: false")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Theologian lineage relationship validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
