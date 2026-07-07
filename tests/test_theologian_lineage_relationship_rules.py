from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_theologian_lineage_relationship_rules as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_theologian_lineage_relationship_rules_pass() -> None:
    assert validator.validate(ROOT) == []


def test_theologian_lineage_relationship_rules_fail_on_forbidden_approved_verb(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    mirror = repo / "registry/controlled_values_mirror.yaml"
    text = mirror.read_text(encoding="utf-8")
    mirror.write_text(text.replace("  - verb: tensions_with", "  - verb: tensions_with\n  - verb: influences"), encoding="utf-8")
    errors = validator.validate(repo)
    assert any("influences" in error for error in errors)

