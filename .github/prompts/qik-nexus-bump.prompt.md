---
description: 'Raise a module version level. Use to manually set the semver bump level before cutting a release.'
---

<!-- @needs nexus bump procedure (Copilot), prd_unit_imp__nexus__bump_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__bump_procedure_copilot], proposed -->

# qik nexus bump — raise version level

Use `mcp_qik-mcp_nexus_bump` or CLI:

```bash
qik nexus bump <major|minor|patch> --target <name>
```

Raises the version of the named target from `.qik/nexus/config.toml`.
If staged entries already declare a `change` nature, the level is auto-derived
by `mcp_qik-mcp_nexus_release` — use `bump` to override.

Check the result with `mcp_qik-mcp_nexus_version`.
