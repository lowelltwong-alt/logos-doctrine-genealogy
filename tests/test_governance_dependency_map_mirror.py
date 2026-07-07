from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_governance_dependency_map_mirror as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_governance_dependency_map_mirror_passes() -> None:
    assert validator.validate(ROOT) == []


def test_governance_dependency_map_mirror_fails_when_required_path_missing(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    (repo / "AI_FRONT_DOOR.md").unlink()
    errors = validator.validate(repo)
    assert any("AI_FRONT_DOOR.md" in error for error in errors)

