from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

try:
    from _validation import ROOT, fail, read_text
    from validate_schema_mirrors import EXPECTED_MIRRORS, MANIFEST_PATH
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import ROOT, fail, read_text
    from scripts.validate_schema_mirrors import EXPECTED_MIRRORS, MANIFEST_PATH


REQUIRED_FRESHNESS_TOKENS = {
    "mirror_freshness:",
    "freshness_standard_ref: logos-governance-architecture:governance/MIRROR_FRESHNESS_STANDARD.yaml",
    "freshness_standard_commit: ad338b5c2dc2c8d979843707aaaabb834cf64785",
    "verified_against_source_commit_at: \"2026-07-07T00:00:00Z\"",
    "staleness_budget_days: 14",
    "local_source_repo_unavailable_policy: report_when_unavailable",
    "missing_or_drifted_mirrored_file_policy: fail_closed_when_source_repo_available",
}

SOURCE_ROOT_CANDIDATES = [
    "../logos-governance-architecture",
]


def normalized_text_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_int(text: str, key: str) -> int | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(\d+)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return int(match.group(1))


def find_local_source_root(root: Path) -> Path | None:
    for candidate in SOURCE_ROOT_CANDIDATES:
        path = (root / candidate).resolve()
        if path.exists() and path.is_dir():
            return path
    return None


def validate(root: Path = ROOT, *, require_local_source: bool = False) -> list[str]:
    errors: list[str] = []
    manifest = root / MANIFEST_PATH
    if not manifest.exists():
        return [f"missing {MANIFEST_PATH}"]

    manifest_text = read_text(root, MANIFEST_PATH)
    for token in sorted(REQUIRED_FRESHNESS_TOKENS):
        if token not in manifest_text:
            errors.append(f"schema mirror manifest missing freshness token: {token}")

    staleness_budget_days = extract_int(manifest_text, "staleness_budget_days")
    if staleness_budget_days is None:
        errors.append("schema mirror manifest missing numeric staleness_budget_days")
    elif staleness_budget_days < 1 or staleness_budget_days > 14:
        errors.append("schema mirror manifest staleness_budget_days must be between 1 and 14")

    source_root = find_local_source_root(root)
    if source_root is None:
        if require_local_source:
            errors.append("local source repo missing for freshness validation")
        return errors

    for rel, (expected_hash, _expected_kind) in EXPECTED_MIRRORS.items():
        source = source_root / rel
        if not source.exists():
            errors.append(f"missing upstream source mirror target: logos-governance-architecture:{rel}")
            continue
        actual_hash = normalized_text_sha256(source)
        if actual_hash != expected_hash:
            errors.append(
                f"upstream source hash drift: {rel} expected {expected_hash} got {actual_hash}"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    require_local_source = bool(argv and "--require-local-source" in argv)
    errors = validate(require_local_source=require_local_source)
    if not errors:
        print("Mirror freshness validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
