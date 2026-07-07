---
object_type: governance_dependency_map_mirror_control
trust_zone: active_scaffold
lifecycle_status: active
provenance_note: "Created 2026-07-06 by Codex to explain the local mirror validator and update triggers."
reason_for_inclusion: "Prevent child-repo governance mirrors from becoming stale or replacing the upstream governance map."
---

# Governance Dependency Map Mirror Control

The mirror at
[GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml](GOVERNANCE_DEPENDENCY_MAP_MIRROR.yaml)
is a child-repo control surface. It is not the upstream source of truth.

Update the mirror when local governance, registry, validator, front-door, or
TOC files change.

Run:

```powershell
python scripts\validate_governance_dependency_map_mirror.py
```

If the local mirror conflicts with `logos-governance-architecture`, stop and
route the issue upstream.

