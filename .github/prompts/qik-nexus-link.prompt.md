---
description: 'Record the needs a PI item gives rise to — handoff into the traceability graph. Use after implementation to link a CR to its needs artefacts.'
---

<!-- @needs nexus link procedure (Copilot), prd_unit_imp__nexus__link_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__link_procedure_copilot], proposed -->

# qik nexus link — link CR to needs

Use `mcp_qik-mcp_nexus_link` or CLI:

```bash
qik nexus link <CR_ID> <NEED_ID> [<NEED_ID> ...]
```

Records which sphinx-needs artefacts (requirements, designs, tests) this PI entry
produced. Multi-valued: repeated calls append rather than overwrite.

**Required before advancing to `complete`** — an unlinked PI item cannot be
advanced to complete without `--force`.

Example:

```bash
qik nexus link cr-000188 sys_int__concept__main sys_req__concept__cluster_names  # [#qik-cortex allow(no-internal-cr-mentions-in-agent-surfaces): id-format example]
```
