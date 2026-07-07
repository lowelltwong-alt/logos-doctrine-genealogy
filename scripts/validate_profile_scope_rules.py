from __future__ import annotations

from pathlib import Path

try:
    from _validation import EXPECTED_PROFILES, ROOT, extract_value_entries, fail, read_text
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import EXPECTED_PROFILES, ROOT, extract_value_entries, fail, read_text


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    profile_path = root / "registry/profile_scopes.yaml"
    rules_path = root / "governance/PROFILE_SCOPE_RULES.md"
    if not profile_path.exists():
        return ["missing registry/profile_scopes.yaml"]
    if not rules_path.exists():
        errors.append("missing governance/PROFILE_SCOPE_RULES.md")

    profiles = extract_value_entries(read_text(root, "registry/profile_scopes.yaml"))
    missing = EXPECTED_PROFILES - profiles
    extra = profiles - EXPECTED_PROFILES
    for value in sorted(missing):
        errors.append(f"profile scope missing from mirror: {value}")
    for value in sorted(extra):
        errors.append(f"profile scope not approved by governance mirror: {value}")

    text = read_text(root, "registry/profile_scopes.yaml")
    if "local_profile_authority: false" not in text:
        errors.append("profile scope mirror must set local_profile_authority: false")
    if "profile_scope_required_for_contested_claims: true" not in text:
        errors.append("profile scope mirror must require scope for contested claims")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Profile scope validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
