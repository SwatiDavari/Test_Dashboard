---
description: 'Suspend a cortex rule in a specific scope without deleting it. Use when a rule must be bypassed with a recorded reason — never silently skip a rule.'
---

<!-- @needs cortex ignore procedure (Copilot), prd_unit_imp__cortex__ignore_procedure_copilot, prd_unit_imp, [prd_unit_des__cortex__ignore_procedure_copilot], released -->

# qik cortex ignore — suspend a rule

Suppresses a rule in a specific scope. The rule is NOT deleted — it is overridden
with `severity = off` and a mandatory recorded reason.

**Bypassing a rule without `ignore` (with recorded reason) is not allowed.**

Use `mcp_qik-mcp_cortex_ignore` or CLI:

```bash
qik cortex ignore <rule-id> --scope '<glob>' --reason "<why this scope is exempt>"
```

The override is stored in `.qik/cortex/` and visible in `qik cortex list`.
To re-enable: use `mcp_qik-mcp_cortex_forget` on the override, or edit the scope file.
