---
description: 'Merge one change request into another, closing the source while preserving its audit trail. Use when two CRs cover overlapping territory and one should absorb the other.'
---

<!-- @needs nexus merge procedure (Copilot), prd_unit_imp__nexus__merge_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__merge_procedure_copilot], proposed -->

# qik nexus merge — absorb a CR into another

Use `mcp_qik-mcp_nexus_merge` or CLI:

```bash
qik nexus merge <FROM_ID> <INTO_ID>
```

The source (`<FROM_ID>`) is moved to the `merged` terminal stage and its
`merged_into` field records the target id. The target is **not changed**.
Neither entry is deleted — the audit trail is fully preserved.

`Released` and already-`merged` entries cannot be the source.

After merging, `qik nexus list merged` shows all absorbed entries.
