---
description: 'Run the deterministic algorithmic rules against the workspace. Use for a quick pass on just the algo rules, without the full semantic check.'
---

<!-- @needs cortex check procedure (Copilot), prd_unit_imp__cortex__check_procedure_copilot, prd_unit_imp, [prd_unit_des__cortex__check_procedure_copilot], released -->

# qik cortex check — algorithmic rule check

Use `mcp_qik-mcp_cortex_check` with `kind="algo"` (or CLI: `qik cortex check --kind algo`):

```bash
qik cortex check --kind algo
qik cortex check --kind all       # algo + semantic annotations
```

Returns a JSON `Report`. Every statement with `"severity": "error"` is blocking.
Report `warning` statements but they do not block.

For the **full quality gate** (prime rules + algo check + semantic check + learn),
use `/qik-cortex`.
