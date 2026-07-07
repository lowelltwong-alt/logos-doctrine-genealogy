from __future__ import annotations

import importlib
import time


CHECKS = [
    ("governance_dependency_map_mirror", "validate_governance_dependency_map_mirror"),
    ("source_trust_rules", "validate_source_trust_rules"),
    ("profile_scope_rules", "validate_profile_scope_rules"),
    ("theologian_lineage_relationship_rules", "validate_theologian_lineage_relationship_rules"),
    ("no_authority_leakage", "validate_no_authority_leakage"),
    ("data_readiness_packet", "validate_data_readiness_packet"),
    ("data_readiness_owner_gate", "validate_data_readiness_owner_gate"),
    ("data_readiness_runbook", "validate_data_readiness_runbook"),
    ("schema_mirrors", "validate_schema_mirrors"),
    ("mirror_freshness", "validate_mirror_freshness"),
]


def main() -> int:
    failures: list[tuple[str, list[str]]] = []
    for name, module_name in CHECKS:
        start = time.perf_counter()
        module = importlib.import_module(module_name)
        errors = module.validate()
        elapsed = time.perf_counter() - start
        if errors:
            print(f"[FAIL] {name} ({elapsed:.3f}s)")
            for error in errors:
                print(f"  - {error}")
            failures.append((name, errors))
        else:
            print(f"[PASS] {name} ({elapsed:.3f}s)")

    if failures:
        print(f"Validation suite failed ({len(failures)} check(s)).")
        return 1

    print(f"Validation suite passed ({len(CHECKS)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

