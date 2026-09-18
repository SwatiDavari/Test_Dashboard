---
description: 'Move a PI-stage entry\'s progress one step forward. Use to track work as it progresses through open → wip → validate → complete.'
---

<!-- @needs nexus advance procedure (Copilot), prd_unit_imp__nexus__advance_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__advance_procedure_copilot], proposed -->

# qik nexus advance — advance PI progress

Use `mcp_qik-mcp_nexus_advance` or CLI:

```bash
qik nexus advance <CR_ID>
```

Progress progression: `open → wip → validate → complete`

| When | Target state |
|------|-------------|
| Starting work | `wip` |
| Implementation done, awaiting review | `validate` |
| Reviewed and accepted | `complete` |

**Note**: Advancing to `complete` requires linked needs (use `qik nexus link`)
unless `--force` is passed.

After `complete`, promote the entry to `staged` via `qik nexus promote`.
