from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_data_readiness_packet as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_data_readiness_packet_pass() -> None:
    assert validator.validate(ROOT) == []


def test_data_readiness_packet_fails_when_non_authorization_removed(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    packet = repo / validator.PACKET_PATH
    text = packet.read_text(encoding="utf-8")
    packet.write_text(text.replace("source imports or source rows", "source handling"), encoding="utf-8")
    errors = validator.validate(repo)
    assert any("source imports or source rows" in error for error in errors)
