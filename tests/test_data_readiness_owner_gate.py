from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_data_readiness_owner_gate as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_data_readiness_owner_gate_pass() -> None:
    assert validator.validate(ROOT) == []


def test_data_readiness_owner_gate_fails_without_lane_option(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    issue_template = repo / validator.ISSUE_TEMPLATE_PATH
    text = issue_template.read_text(encoding="utf-8")
    issue_template.write_text(text.replace("DR-OPTION-D - Evidence-product harness only", "DR-OPTION-D"), encoding="utf-8")
    errors = validator.validate(repo)
    assert any("DR-OPTION-D - Evidence-product harness only" in error for error in errors)
