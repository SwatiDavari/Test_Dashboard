---
description: 'List the effective cortex rules for a path. Use when you want to see which rules apply in a specific directory or crate.'
---

<!-- @needs cortex list procedure (Copilot), prd_unit_imp__cortex__list_procedure_copilot, prd_unit_imp, [prd_unit_des__cortex__list_procedure_copilot], released -->

# qik cortex list — show effective rules

Use `mcp_qik-mcp_cortex_list` or CLI:

```bash
qik cortex list                   # all rules at project root
qik cortex list --path rust/qed-core/src
```

Shows the rules that apply at the given path, including inherited overrides.
Use this to audit which rules are active before modifying code.
