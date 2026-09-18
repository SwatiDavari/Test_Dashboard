---
description: 'Advance an entry one stage up the spine — idea → backlog → pi → staged. Use to promote a completed PI item to staged (ready for release) or to move a backlog item into the current PI.'
---

<!-- @needs nexus promote procedure (Copilot), prd_unit_imp__nexus__promote_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__promote_procedure_copilot], proposed -->

# qik nexus promote — advance stage

Use `mcp_qik-mcp_nexus_promote` or CLI:

```bash
qik nexus promote <CR_ID>
```

Stage spine: `idea → backlog → pi → staged`

**At every commit**: promote only the CR id(s) you were dispatched to work
to `staged` before committing — never another `pi+complete` entry just
because it also happens to be sitting there (e.g. a concurrent session's own
in-flight CR). A batch promotion of multiple CRs requires every id to be
named explicitly by the orchestrator/user, or use `nexus close` for a
deliberate end-of-PI batch. Use the promoted CR's headline to build the
commit message. Include the nexus store (`.qik/nexus/entries.toml`) in the
commit, scoped to only that CR's diff lines.

**"staged" means**: like a CI staging environment — done, committed, waiting for
`nexus release` to ship it. Not to be confused with `git add`.
