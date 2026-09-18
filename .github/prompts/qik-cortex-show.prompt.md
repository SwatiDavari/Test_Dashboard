---
description: 'Show the recorded reason and details behind a specific cortex rule. Use when you want to understand why a rule exists or what incident it was derived from.'
---

<!-- @needs cortex show procedure (Copilot), prd_unit_imp__cortex__show_procedure_copilot, prd_unit_imp, [prd_unit_des__cortex__show_procedure_copilot], released -->

# qik cortex show — explain a rule

```bash
qik cortex show <rule-id>
```

Returns the full rule record: kind, severity, scope, pattern/check-prompt,
and the `why` field explaining the incident or rationale behind the rule.

Use `mcp_qik-mcp_cortex_show` with the rule id for the same result via MCP.
