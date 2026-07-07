from __future__ import annotations

from pathlib import Path

try:
    from _validation import ROOT, fail, has_true_authorization, read_text
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import ROOT, fail, has_true_authorization, read_text


RUNBOOK_PATH = "docs/roadmap/data-readiness-lane-implementation-runbook.md"

REQUIRED_RUNBOOK_TOKENS = {
    "object_type: data_readiness_lane_implementation_runbook",
    "trust_zone: active_scaffold",
    "lifecycle_status: active",
    "issue #4",
    "It does not select a lane. It does not authorize data work.",
    "Confirm the owner selected exactly one",
    "data_free_until_later_authorization: true",
    "DR-OPTION-A",
    "DR-OPTION-B",
    "DR-OPTION-C",
    "DR-OPTION-D",
    "Do not expand schemas locally, add records, or mint vocabulary.",
    "Do not import sources, add source rows, or rank sources as doctrine authority.",
    "Do not create lineage records, influence claims, reviewed lineage, or theological authority.",
    "Do not let fixtures become historical or doctrinal records.",
    "python scripts\\validate_data_readiness_runbook.py",
    "This runbook does not authorize:",
    "doctrine-lineage records",
    "source imports or source rows",
    "reviewed-lineage promotion",
    "graph/retrieval/vector truth",
    "Scripture or chunk output",
    "theology authority",
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
    path = root / RUNBOOK_PATH
    if not path.exists():
        return [f"missing {RUNBOOK_PATH}"]

    text = read_text(root, RUNBOOK_PATH)
    for token in sorted(REQUIRED_RUNBOOK_TOKENS):
        if token not in text:
            errors.append(f"data-readiness runbook missing required token: {token}")

    for token in sorted(FORBIDDEN_PROMOTION_TOKENS):
        if token in text:
            errors.append(f"data-readiness runbook contains unauthorized promotion phrase: {token}")

    for field in has_true_authorization(text):
        errors.append(f"data-readiness runbook sets authority field true: {field}")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Data-readiness runbook validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
