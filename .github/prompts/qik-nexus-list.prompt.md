---
description: 'List lifecycle entries, optionally filtered by stage or progress. Use to get an overview of all CRs or to check PI status.'
---

<!-- @needs nexus list procedure (Copilot), prd_unit_imp__nexus__list_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__list_procedure_copilot], proposed -->

# qik nexus list — list entries

Use `mcp_qik-mcp_nexus_list` or CLI:

```bash
qik nexus list               # all entries
qik nexus list pi            # PI items (committed work)
qik nexus list pi --progress wip      # in-progress PI items
qik nexus list backlog       # shaped, not yet committed
qik nexus list staged        # done, awaiting release
qik nexus list released      # shipped
qik nexus list released --version 0.5.0          # one release's entries
qik nexus list released --type bug --version 0.5.0  # errata for one release
```

Progress states (PI only): `open`, `wip`, `validate`, `complete`.

`--version` filters to entries released as exactly that semver (only
`released` entries carry a version). Combine with `--type` to build errata
(bug-only) or full changelog (unfiltered) views — see the qik-nexus agent's
"Release notes preview" workflow for how this feeds a drafted preview.
