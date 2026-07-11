from __future__ import annotations

import json
import shutil
from pathlib import Path

from scripts import validate_llos_v1_bootstrap as validator


ROOT = Path(__file__).resolve().parents[1]


def test_dad_repo_write_policy_is_fail_closed_without_standing_approval() -> None:
    policy = json.loads((ROOT / ".digital-asset/dad-write-policy.json").read_text(encoding="utf-8"))
    assert policy["dad_write_allowed"] is False
    assert policy["approved_explicit_approval_ids"] == []
    assert policy["logos_local_outbox_write_allowed"] is True
    assert policy["logos_local_dad_central_read_allowed"] is True
    assert policy["dad_push_or_inbox_write_allowed"] is False
    assert policy["rollout_approval_is_standing_write_permission"] is False


def copy_repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", ".pytest_cache", "__pycache__"),
    )
    return target


def test_llos_v1_bootstrap_passes() -> None:
    assert validator.validate(ROOT) == []


def test_llos_v1_bootstrap_rejects_populated_lessons(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    index = repo / validator.LESSON_INDEX_PATH
    index.write_text(
        index.read_text(encoding="utf-8").replace("lessons: []", "lessons:\n  - lesson_id: llos:doctrine:test"),
        encoding="utf-8",
    )

    errors = validator.validate(repo)

    assert any("lesson index must remain empty" in error for error in errors)


def test_llos_v1_bootstrap_rejects_dad_doctrine_write(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    adapter = repo / validator.ADAPTER_PATH
    adapter.write_text(
        adapter.read_text(encoding="utf-8").replace("may_write_doctrine_files: false", "may_write_doctrine_files: true"),
        encoding="utf-8",
    )

    errors = validator.validate(repo)

    assert any("may_write_doctrine_files" in error for error in errors)


def test_llos_v1_bootstrap_rejects_runtime_adapter_authority(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    adapter = repo / validator.ADAPTER_PATH
    adapter.write_text(
        adapter.read_text(encoding="utf-8").replace("authorizes_runtime_adapters: false", "authorizes_runtime_adapters: true"),
        encoding="utf-8",
    )

    errors = validator.validate(repo)

    assert any("authorizes_runtime_adapters" in error for error in errors)


def test_llos_v1_bootstrap_rejects_source_data_and_theology_authority(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    index = repo / validator.LESSON_INDEX_PATH
    index.write_text(
        index.read_text(encoding="utf-8").replace("authorizes_data_authority: false", "authorizes_data_authority: true"),
        encoding="utf-8",
    )

    errors = validator.validate(repo)

    assert any("authorizes_data_authority" in error for error in errors)


def test_llos_v1_bootstrap_requires_fresh_explicit_dad_approval(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    index = repo / validator.LESSON_INDEX_PATH
    index.write_text(
        index.read_text(encoding="utf-8").replace(
            "approval_must_be_fresh_and_explicit: true",
            "approval_must_be_fresh_and_explicit: false",
        ),
        encoding="utf-8",
    )

    errors = validator.validate(repo)

    assert any("approval_must_be_fresh_and_explicit" in error for error in errors)


def test_llos_v1_bootstrap_keeps_two_way_communication_asymmetric(tmp_path: Path) -> None:
    repo = copy_repo(tmp_path)
    adapter = repo / validator.ADAPTER_PATH
    adapter.write_text(
        adapter.read_text(encoding="utf-8").replace(
            "may_push_or_write_logos_inbox: false",
            "may_push_or_write_logos_inbox: true",
        ),
        encoding="utf-8",
    )

    errors = validator.validate(repo)

    assert any("may_push_or_write_logos_inbox" in error for error in errors)
