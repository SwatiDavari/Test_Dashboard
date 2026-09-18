---
description: 'Walk the upstream provenance cone of a need — where does this artifact come from? Use to understand what requirements, architecture decisions, or intentions back a given design or implementation.'
---

<!-- @needs axon trace procedure (Copilot), prd_unit_imp__axon__trace_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__trace_procedure_copilot], released -->

# qik axon trace — upstream provenance

Use `mcp_qik-mcp_axon_trace` or CLI:

```bash
qik axon trace <NEED_ID>
```

Walks upward from `<NEED_ID>` through all `links:` to the top of the hierarchy
(intent → requirement → architecture → design → impl → test).

Returns the full upstream chain with distance from the start node.
Use this to answer: "what requirement covers this code?" or "is this design backed
by an approved requirement?".

**Topology**: by default, only link kinds whose declared topology
is `default = true` are walked — a `relates_to`-style kinship link (topology
`peer`) is excluded unless you pass `--topology peer` or name it explicitly
in `--via`. See `.qik/axon/classify.toml [[topology]]`.

For the full blast radius (both directions), use `/qik-axon-blast`.
