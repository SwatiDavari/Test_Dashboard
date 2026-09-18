---
description: 'Add a structural graph rule to the axon rule set. Use when a traceability check reveals a missing constraint that should be enforced across the project.'
---

<!-- @needs axon learn procedure (Copilot), prd_unit_imp__axon__learn_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__learn_procedure_copilot], released -->

# qik axon learn — add a graph rule

Use `mcp_qik-mcp_axon_learn` or CLI:

```bash
qik axon learn \
  --id <rule-id> \
  --kind <require-link|forbid-link|require-format|forbid-regex-in-body|require-regex-in-body> \
  --from-type <need-type> \
  --to-type <need-type> \
  --link <link-name> \
  [--severity error|warning]
```

Adds a rule to `.qik/axon/rules.toml`. Use `mcp_qik-mcp_axon_rules` to see
existing rules before adding a new one.

**Topology**: a `forbid-link` rule with `--link` omitted is a
*wildcard* — it checks every link kind whose declared topology
(`.qik/axon/classify.toml [[topology]]`) is `default = true` (unchanged from
before this axis existed). Pass `--topology <name>[,...]` to narrow a
wildcard rule to specific topology values instead. `--topology` is rejected
together with `--link` — a rule naming one link explicitly already matches
only that link, regardless of its topology.
