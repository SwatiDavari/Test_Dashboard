---
description: 'List needs filtered by classify-dimension expressions. Use to inventory what exists in the traceability graph, optionally narrowed by layer, scope, component, status, etc.'
---

<!-- @needs axon list procedure (Copilot), prd_unit_imp__axon__list_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__list_procedure_copilot], released -->

# qik axon list — inventory of needs

Use `mcp_qik-mcp_axon_list` or CLI:

```bash
qik axon list                                      # all needs (colored on TTY)
qik axon list --no-color                           # parse-safe output
qik axon list --select layer=req                   # requirements only
qik axon list --select layer=des                   # designs only
qik axon list --select layer=imp                   # implementations only
qik axon list --select component=axon              # axon cluster only
qik axon list --select status=proposed             # proposed needs only
qik axon list --select status=proposed,approved    # proposed OR approved
qik axon list --select status=released>0.2.0       # released at a version > 0.2.0 (lifeline filter)
qik axon list --select status=released>0.2.0 --select status=released<0.5.0   # released in (0.2.0, 0.5.0) — range via AND
qik axon list --select layer=req --select component=nexus   # ANDed
```

**Supported axes for `--select`:**

| Axis | Values |
|------|--------|
| `layer` | `int`, `req`, `arc`, `des`, `imp`, `tst`, `doc` |
| `scope` | `glob`, `feat`, `comp`, `unit` |
| `enabling_system` | `prd`, `sys`, `tst`, `doc` |
| `component` | cluster name (e.g. `axon`, `nexus`, `cortex`) |
| `tag` | need-specific tag |
| `status` | `draft`, `proposed`, `approved`, `released`, `deprecated`, `retired` |

`status` additionally accepts `<name><op><version>` (op one of `> >= < <= =`,
version `X.Y.Z`), e.g. `status=released>0.2.0` — this filters on the need's
`lifeline` (the version it was at when it *entered* that status), not its
current status. A need with no lifeline entry for that status never matches.
Combine two such filters via two `--select status=...` flags for a version
range (AND, same as any other repeated `--select`).

Multiple `--select` flags are ANDed. A need with no status set never matches a status filter.
Results are independent of links — this shows what *exists*, not what is connected.
