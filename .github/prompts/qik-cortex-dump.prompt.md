---
description: 'Emit the qik cortex rules for priming an agent. Use when you need to load the current rule set before a review or quality gate pass.'
---

<!-- @needs cortex dump procedure (Copilot), prd_unit_imp__cortex__dump_procedure_copilot, prd_unit_imp, [prd_unit_des__cortex__dump_procedure_copilot], released -->

# qik cortex dump — emit rule set

Use `mcp_qik-mcp_cortex_dump` or CLI:

```bash
qik cortex dump --kind all        # all rules (algo + llm)
qik cortex dump --kind algo       # algorithmic rules only
qik cortex dump --kind llm        # semantic/LLM rules only
```

The output primes the agent with the active rules for the current path.
Rules are hierarchical — project-root rules can be overridden per crate/sub-path.
