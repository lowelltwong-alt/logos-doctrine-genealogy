from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_no_authority_leakage as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_no_authority_leakage_pass() -> None:
    assert validator.validate(ROOT) == []


def test_no_authority_leakage_fails_on_true_authorization(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    authority = repo / "governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md"
    text = authority.read_text(encoding="utf-8")
    authority.write_text(text.replace("authorizes_theology_authority: false", "authorizes_theology_authority: true"), encoding="utf-8")
    errors = validator.validate(repo)
    assert any("authorizes_theology_authority" in error for error in errors)

