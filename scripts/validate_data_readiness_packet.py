from __future__ import annotations

from pathlib import Path

try:
    from _validation import ROOT, fail, has_true_authorization, read_text
except ModuleNotFoundError:  # pragma: no cover - exercised by pytest package import
    from scripts._validation import ROOT, fail, has_true_authorization, read_text


PACKET_PATH = "docs/roadmap/data-readiness-decision-packet.md"

REQUIRED_TOKENS = {
    "object_type: data_readiness_decision_packet",
    "trust_zone: active_scaffold",
    "lifecycle_status: proposed",
    "This packet does not authorize:",
    "doctrine-lineage records",
    "source imports or source rows",
    "reviewed-lineage promotion",
    "graph/retrieval/vector truth",
    "Scripture or chunk output",
    "new relationship verbs, profiles, enum values, authority rungs",
    "theology authority",
    "Owner Decision Required",
    "DR-OPTION-A",
    "DR-OPTION-B",
    "DR-OPTION-C",
    "DR-OPTION-D",
    "python scripts\\validate_data_readiness_packet.py",
    "python scripts\\validate_data_readiness_owner_gate.py",
    "data-readiness-owner-decision-template.md",
    "data_readiness_lane_selection.yml",
}

FORBIDDEN_PROMOTION_TOKENS = {
    "reviewed-lineage promotion is authorized",
    "doctrine-lineage records are authorized",
    "source imports are authorized",
    "graph truth is authorized",
    "retrieval truth is authorized",
    "vector truth is authorized",
    "theology authority is authorized",
}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    packet = root / PACKET_PATH
    if not packet.exists():
        return [f"missing {PACKET_PATH}"]

    text = read_text(root, PACKET_PATH)
    for token in sorted(REQUIRED_TOKENS):
        if token not in text:
            errors.append(f"data-readiness packet missing required token: {token}")

    for token in sorted(FORBIDDEN_PROMOTION_TOKENS):
        if token in text:
            errors.append(f"data-readiness packet contains unauthorized promotion phrase: {token}")

    for field in has_true_authorization(text):
        errors.append(f"data-readiness packet sets authority field true: {field}")

    return errors


def main() -> int:
    errors = validate()
    if not errors:
        print("Data-readiness decision packet validation passed.")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
