---
description: 'Set an entry aside in the dropped side-state (non-destructive). Use when a CR is no longer pursued but should be preserved for audit trail.'
---

<!-- @needs nexus drop procedure (Copilot), prd_unit_imp__nexus__drop_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__drop_procedure_copilot], proposed -->

# qik nexus drop — set aside an entry

Use `mcp_qik-mcp_nexus_drop` or CLI:

```bash
qik nexus drop <CR_ID> --reason "<why it was dropped>"
```

Moves the entry to the `dropped` side-state. It is NOT deleted — history is
preserved. Use `mcp_qik-mcp_nexus_restore` to bring it back.

**Always provide `--reason`.** Dropped entries are audit artifacts — they record
*why* a CR was decided against. A drop without a reason is an invisible decision:
future readers cannot tell whether it was a deliberate choice or a forgotten
half-decision. The `--reason` flag was introduced in v0.4.0 (mid-PI-4); older
dropped entries without a reason pre-date this feature.

To permanently remove a specific dropped entry, use `mcp_qik-mcp_nexus_delete`.
