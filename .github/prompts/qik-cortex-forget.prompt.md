---
description: 'Remove a learned or local cortex rule. Use when a rule was recorded incorrectly or has been superseded by a better formulation.'
---

<!-- @needs cortex forget procedure (Copilot), prd_unit_imp__cortex__forget_procedure_copilot, prd_unit_imp, [prd_unit_des__cortex__forget_procedure_copilot], released -->

# qik cortex forget — remove a rule

Deletes a rule that was added via `cortex learn` or exists only in `.qik/cortex/`.
Rules from the kit's built-in set cannot be deleted with `forget` — use `ignore` to
suppress them.

Use `mcp_qik-mcp_cortex_forget` or CLI:

```bash
qik cortex forget <rule-id>
```

Confirm with `mcp_qik-mcp_cortex_list` that the rule no longer appears.
