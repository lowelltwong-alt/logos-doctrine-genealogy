from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_DATA_FILES = {"README.md", ".gitkeep"}

EXPECTED_PROFILES = {
    "reformed",
    "arminian_wesleyan",
    "baptist",
    "anglican",
    "lutheran",
    "presbyterian",
    "methodist",
    "pentecostal_charismatic",
    "patristic_creedal",
    "roman_catholic",
    "eastern_orthodox",
    "oriental_orthodox",
    "church_of_the_east",
    "pre_division_patristic",
}

EXPECTED_RELATIONSHIP_VERBS = {
    "derives_from",
    "depends_on",
    "clarifies",
    "modifies",
    "systematizes",
    "reads_back_into",
    "interprets_passage",
    "cites_source",
    "receives",
    "rejects",
    "counters",
    "partially_aligns_with",
    "tensions_with",
}

FORBIDDEN_RELATIONSHIP_VERBS = {
    "related_to",
    "influences",
    "condemns",
    "is_condemned_by",
}

REQUIRED_FALSE_AUTHORIZATIONS = {
    "authorizes_doctrine_lineage_records",
    "authorizes_source_imports",
    "authorizes_source_rows",
    "authorizes_reviewed_lineage_promotion",
    "authorizes_graph_retrieval_vector_truth",
    "authorizes_scripture_or_chunk_output",
    "authorizes_new_relationship_verbs",
    "authorizes_new_profiles",
    "authorizes_new_enum_values",
    "authorizes_theology_authority",
}

REQUIRED_LOCAL_PATHS = {
    "README.md",
    "AGENTS.md",
    "AI_FRONT_DOOR.md",
    "AI_TABLE_OF_CONTENTS.md",
    "governance/UPSTREAM_GOVERNANCE_CONTRACT.md",
    "governance/AUTHORITY_AND_NON_AUTHORIZATION_RULES.md",
    "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml",
    "governance/GOVERNANCE_DEPENDENCY_MAP_MIRROR_CONTROL.md",
    "governance/SOURCE_TRUST_RULES.md",
    "governance/PROFILE_SCOPE_RULES.md",
    "governance/THEOLOGIAN_LINEAGE_RELATIONSHIP_RULES.md",
    "registry/controlled_values_mirror.yaml",
    "registry/profile_scopes.yaml",
    "registry/source_trust_tiers.yaml",
    ".github/ISSUE_TEMPLATE/data_readiness_lane_selection.yml",
    "docs/roadmap/data-readiness-decision-packet.md",
    "docs/roadmap/data-readiness-lane-implementation-runbook.md",
    "docs/roadmap/data-readiness-owner-decision-template.md",
    "docs/roadmap/first-task-and-readiness.md",
    "schemas/README.md",
    "schemas/doctrine_genealogy/README.md",
    "data/README.md",
    "data/.gitkeep",
    "scripts/run_validation_suite.py",
    "scripts/validate_governance_dependency_map_mirror.py",
    "scripts/validate_source_trust_rules.py",
    "scripts/validate_profile_scope_rules.py",
    "scripts/validate_theologian_lineage_relationship_rules.py",
    "scripts/validate_no_authority_leakage.py",
    "scripts/validate_data_readiness_packet.py",
    "scripts/validate_data_readiness_owner_gate.py",
    "scripts/validate_data_readiness_runbook.py",
}


def read_text(root: Path, relative_path: str) -> str:
    return (root / relative_path).read_text(encoding="utf-8")


def missing_paths(root: Path, paths: set[str]) -> list[str]:
    return sorted(path for path in paths if not (root / path).exists())


def data_files(root: Path) -> list[Path]:
    data_root = root / "data"
    if not data_root.exists():
        return []
    return [path for path in data_root.rglob("*") if path.is_file()]


def unexpected_data_files(root: Path) -> list[str]:
    unexpected: list[str] = []
    for path in data_files(root):
        if path.parent != root / "data" or path.name not in ALLOWED_DATA_FILES:
            unexpected.append(path.relative_to(root).as_posix())
    return sorted(unexpected)


def extract_value_entries(text: str) -> set[str]:
    return set(re.findall(r"^\s+- value:\s*([A-Za-z0-9_]+)\s*$", text, re.MULTILINE))


def extract_verb_entries(text: str) -> set[str]:
    return set(re.findall(r"^\s+- verb:\s*([A-Za-z0-9_]+)\s*$", text, re.MULTILINE))


def has_true_authorization(text: str) -> list[str]:
    return sorted(
        set(re.findall(r"\b(authorizes_[A-Za-z0-9_]+)\s*:\s*true\b", text))
    )


def fail(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    return 0

