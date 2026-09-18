---
description: 'Show current and next version (read-only preview). Use before releasing to verify the version that will be stamped.'
---

<!-- @needs nexus version procedure (Copilot), prd_unit_imp__nexus__version_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__version_procedure_copilot], proposed -->

# qik nexus version — preview version

Use `mcp_qik-mcp_nexus_version` or CLI:

```bash
qik nexus version             # show current + next version
qik nexus version --level minor  # preview a specific bump level
```

Read-only. To actually bump, use `mcp_qik-mcp_nexus_bump`. To release, use `mcp_qik-mcp_nexus_release`.
