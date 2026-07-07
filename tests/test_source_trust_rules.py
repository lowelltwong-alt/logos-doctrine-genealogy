from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_source_trust_rules as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_source_trust_rules_pass() -> None:
    assert validator.validate(ROOT) == []


def test_source_trust_rules_fail_on_data_record(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    (repo / "data/source_rows.jsonl").write_text("{}", encoding="utf-8")
    errors = validator.validate(repo)
    assert any("source_rows.jsonl" in error for error in errors)

