---
description: 'Suppress a graph rule without deleting it. Use when a rule must be bypassed in a specific context with a recorded reason.'
---

<!-- @needs axon ignore procedure (Copilot), prd_unit_imp__axon__ignore_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__ignore_procedure_copilot], released -->

# qik axon ignore — suppress a graph rule

Use `mcp_qik-mcp_axon_ignore` or CLI:

```bash
qik axon ignore <rule-id> --reason "<why this is exempt>"
```

Sets the rule's severity to `off` in `.qik/axon/rules.toml`.
Use `mcp_qik-mcp_axon_forget` on the override to re-enable it.
