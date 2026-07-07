from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_schema_mirrors as validator


ROOT = Path(__file__).resolve().parents[1]


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_schema_mirrors_pass() -> None:
    assert validator.validate(ROOT) == []


def test_schema_mirrors_fail_on_hash_drift(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    schema = repo / "schemas/doctrine_genealogy/date_block.v1.schema.json"
    schema.write_text(schema.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    errors = validator.validate(repo)
    assert any("date_block.v1.schema.json" in error and "hash mismatch" in error for error in errors)


def test_schema_mirrors_fail_on_forbidden_data_file(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    forbidden = repo / "data/doctrine_records.jsonl"
    forbidden.write_text("", encoding="utf-8")
    errors = validator.validate(repo)
    assert any("forbidden data file" in error for error in errors)
