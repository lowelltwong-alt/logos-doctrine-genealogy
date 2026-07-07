from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_data_readiness_runbook as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_data_readiness_runbook_pass() -> None:
    assert validator.validate(ROOT) == []


def test_data_readiness_runbook_fails_without_issue_gate(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    runbook = repo / validator.RUNBOOK_PATH
    text = runbook.read_text(encoding="utf-8")
    runbook.write_text(text.replace("issue #4", "the issue"), encoding="utf-8")
    errors = validator.validate(repo)
    assert any("issue #4" in error for error in errors)
