from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_mirror_freshness as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def seed_source_repo(child_repo: Path) -> Path:
    source_root = child_repo.parent / "logos-governance-architecture"
    for rel in validator.EXPECTED_MIRRORS:
        source = child_repo / rel
        target = source_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return source_root


def test_mirror_freshness_passes() -> None:
    assert validator.validate(ROOT) == []


def test_mirror_freshness_can_require_local_source(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    errors = validator.validate(repo, require_local_source=True)
    assert any("local source repo missing" in error for error in errors)


def test_mirror_freshness_fails_on_upstream_hash_drift(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    seed_source_repo(repo)
    source = repo.parent / "logos-governance-architecture/schemas/doctrine_genealogy/date_block.v1.schema.json"
    source.write_text(source.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    errors = validator.validate(repo)

    assert any("upstream source hash drift" in error for error in errors)


def test_mirror_freshness_fails_when_required_token_is_missing(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    manifest = repo / validator.MANIFEST_PATH
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace("  staleness_budget_days: 14\n", ""),
        encoding="utf-8",
    )

    errors = validator.validate(repo)

    assert any("staleness_budget_days" in error for error in errors)
