---
description: 'Remove a graph rule from the axon rule set. Use when a rule was recorded incorrectly or is no longer applicable.'
---

<!-- @needs axon forget procedure (Copilot), prd_unit_imp__axon__forget_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__forget_procedure_copilot], released -->

# qik axon forget — remove a graph rule

Use `mcp_qik-mcp_axon_forget` or CLI:

```bash
qik axon forget <rule-id>
```

Removes the rule from `.qik/axon/rules.toml`.
Confirm with `mcp_qik-mcp_axon_rules` that it no longer appears.
