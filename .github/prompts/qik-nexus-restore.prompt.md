---
description: 'Bring a dropped entry back into the spine at a specified stage. Use to revive a previously dropped CR.'
---

<!-- @needs nexus restore procedure (Copilot), prd_unit_imp__nexus__restore_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__restore_procedure_copilot], proposed -->

# qik nexus restore — revive a dropped entry

Use `mcp_qik-mcp_nexus_restore` or CLI:

```bash
qik nexus restore <CR_ID> --stage <idea|backlog|pi>
```

Moves the entry from `dropped` back to the specified stage. The entry resumes its
normal lifecycle from there.
