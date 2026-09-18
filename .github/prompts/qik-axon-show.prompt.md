---
description: 'Retrieve a single need by ID with full metadata. Use when you need the complete record of a specific requirement, design, or implementation artefact.'
---

<!-- @needs axon show procedure (Copilot), prd_unit_imp__axon__show_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__show_procedure_copilot], released -->

# qik axon show — show a single need

Use `mcp_qik-mcp_axon_show` or CLI:

```bash
qik axon show <NEED_ID>
```

Returns the full need record: title, type, status, tags, links (outgoing + incoming),
source file path and line number, and `lifeline` (the version the need was at when
it last entered each status it has ever reached, if any — e.g.
`draft@0.3.0, released@0.6.0`).

Prefer this over reading `needs.json` directly — the output is stable and formatted.
