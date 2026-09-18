---
description: 'Show a single lifecycle entry in full — headline, what, why, stage, progress, needs, version. Use to inspect a specific CR.'
---

<!-- @needs nexus show procedure (Copilot), prd_unit_imp__nexus__show_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__show_procedure_copilot], proposed -->

# qik nexus show — show one entry

Use `mcp_qik-mcp_nexus_show` or CLI:

```bash
qik nexus show <CR_ID>        # e.g. qik nexus show cr-000107 [#qik-cortex allow(no-internal-cr-mentions-in-agent-surfaces): id-format example]
```

Returns the full record: id, headline, what, why, stage, progress,
change nature, linked needs, and any external refs.
