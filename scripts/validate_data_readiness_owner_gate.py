from __future__ import annotations

from pathlib import Path

try:
    from _validation import ROOT, fail, has_true_authorization, read_text
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import ROOT, fail, has_true_authorization, read_text


DECISION_TEMPLATE_PATH = "docs/roadmap/data-readiness-owner-decision-template.md"
ISSUE_TEMPLATE_PATH = ".github/ISSUE_TEMPLATE/data_readiness_lane_selection.yml"

REQUIRED_DECISION_TEMPLATE_TOKENS = {
    "object_type: data_readiness_owner_decision_template",
    "trust_zone: active_scaffold",
    "lifecycle_status: active",
    "owner_decision_id:",
    "selected_lane: DR-OPTION-A | DR-OPTION-B | DR-OPTION-C | DR-OPTION-D",
    "allowed_files:",
    "forbidden_files:",
    "validators_required:",
    "data_free_until_later_authorization: true",
    "requires_upstream_governance_if_new_values_needed: true",
    "does_not_authorize:",
    "doctrine_lineage_records: true",
    "source_imports_or_source_rows: true",
    "reviewed_lineage_promotion: true",
    "graph_retrieval_vector_truth: true",
    "scripture_or_chunk_output: true",
    "new_relationship_verbs_profiles_enums_rungs_or_flags: true",
    "theology_authority: true",
    "python scripts\\validate_data_readiness_owner_gate.py",
}

REQUIRED_ISSUE_TEMPLATE_TOKENS = {
    "name: Data Readiness Lane Selection",
    "owner-decision",
    "data-readiness",
    "DR-OPTION-A - Governance schema mirror only",
    "DR-OPTION-B - Source-intake docket only",
    "DR-OPTION-C - First doctrine-slice review packet only",
    "DR-OPTION-D - Evidence-product harness only",
    "Allowed files",
    "Forbidden files and surfaces",
    "Non-authorizations",
    "This does not authorize doctrine-lineage records.",
    "This does not authorize source imports or source rows.",
    "This does not authorize reviewed-lineage promotion.",
    "This does not authorize graph/retrieval/vector truth.",
    "This does not authorize Scripture or chunk output.",
    "This does not authorize theology authority or Codex inference of doctrine.",
    "python scripts\\validate_data_readiness_owner_gate.py",
    "logos-governance-architecture",
}

FORBIDDEN_PROMOTION_TOKENS = {
    "doctrine-lineage records are authorized",
    "source imports are authorized",
    "source rows are authorized",
    "reviewed-lineage promotion is authorized",
    "graph truth is authorized",
    "retrieval truth is authorized",
    "vector truth is authorized",
    "theology authority is authorized",
}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for rel in [DECISION_TEMPLATE_PATH, ISSUE_TEMPLATE_PATH]:
        if not (root / rel).exists():
            errors.append(f"missing {rel}")

    if errors:
        return errors

    decision_text = read_text(root, DECISION_TEMPLATE_PATH)
    issue_text = read_text(root, ISSUE_TEMPLATE_PATH)

    for token in sorted(REQUIRED_DECISION_TEMPLATE_TOKENS):
        if token not in decision_text:
            errors.append(f"owner decision template missing required token: {token}")

    for token in sorted(REQUIRED_ISSUE_TEMPLATE_TOKENS):
        if token not in issue_text:
            errors.append(f"owner decision issue template missing required token: {token}")

    combined_text = f"{decision_text}\n{issue_text}"
    for token in sorted(FORBIDDEN_PROMOTION_TOKENS):
        if token in combined_text:
            errors.append(f"owner decision gate contains unauthorized promotion phrase: {token}")

    for field in has_true_authorization(combined_text):
        errors.append(f"owner decision gate sets authority field true: {field}")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Data-readiness owner gate validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
