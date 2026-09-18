---
description: 'Move a need\'s lifecycle status one step back. Use to roll back an incorrect advance.'
---

<!-- @needs axon retreat procedure (Copilot), prd_unit_imp__axon__retreat_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__retreat_procedure_copilot], released -->

# qik axon retreat — retreat need status

Use `mcp_qik-mcp_axon_retreat` or CLI:

```bash
qik axon retreat <NEED_ID>
```

Mutates the authored source `.md` — never `needs.json`.

Status regression: `retired → deprecated → released → approved → proposed`

After running, rebuild the needs index so the change is visible in `needs.json`.
