---
description: 'Close the current PI increment — stage complete items, forward incomplete items to the next increment. Use at the end of a PI to do the PI bookkeeping.'
---

<!-- @needs nexus close procedure (Copilot), prd_unit_imp__nexus__close_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__close_procedure_copilot], proposed -->

# qik nexus close — close PI increment

Use `mcp_qik-mcp_nexus_close` or CLI:

```bash
qik nexus close
```

**What it does:**
1. Bumps the PI counter.
2. Any `pi+complete` entries that were not individually promoted are staged.
3. All incomplete (`open`, `wip`, `validate`) PI entries are forwarded to the
   next increment.

**Primary staging path**: promote items individually via `qik nexus promote` as
work completes — do not wait for `close`. Use `close` only for PI bookkeeping
(counter bump + carryover forwarding).

## End-of-PI checklist

1. Verify all completed items are promoted: `qik nexus list pi --progress complete`
2. Review what will be forwarded: `qik nexus list pi` (items at open/wip/validate)
3. Run `qik nexus close`.
4. Confirm the new PI number with `qik nexus pi`.
