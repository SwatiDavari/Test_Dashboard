---
description: 'Amend the headline, what, why, or change nature of an existing entry. Use to correct or refine a CR in place.'
---

<!-- @needs nexus update procedure (Copilot), prd_unit_imp__nexus__update_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__update_procedure_copilot], proposed -->

# qik nexus update — amend an entry

Use `mcp_qik-mcp_nexus_update` or CLI:

```bash
qik nexus update <CR_ID> \
  [--headline "<new headline>"] \
  [--what "<revised what>"] \
  [--why "<revised why>"] \
  [--change <breaking|feature|fix>]
```

At least one field must be supplied. The entry id and stage are never changed
by `update` — use `promote`/`demote` for stage transitions.
