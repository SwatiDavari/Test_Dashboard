---
description: 'List all graph rules in the axon rule set. Use to audit what traceability constraints are currently active.'
---

<!-- @needs axon rules procedure (Copilot), prd_unit_imp__axon__rules_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__rules_procedure_copilot], released -->

# qik axon rules — list graph rules

Use `mcp_qik-mcp_axon_rules` or CLI:

```bash
qik axon rules
```

Shows all rules from `.qik/axon/rules.toml`, including id, from_type, to_type,
link name, severity, and any suppression status.
