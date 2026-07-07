from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_profile_scope_rules as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_profile_scope_rules_pass() -> None:
    assert validator.validate(ROOT) == []


def test_profile_scope_rules_fail_on_unknown_profile(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    profile_file = repo / "registry/profile_scopes.yaml"
    text = profile_file.read_text(encoding="utf-8")
    profile_file.write_text(text.replace("value: reformed", "value: invented_profile"), encoding="utf-8")
    errors = validator.validate(repo)
    assert any("invented_profile" in error for error in errors)

