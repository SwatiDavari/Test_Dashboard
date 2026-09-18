---
description: 'Compute a SHA-1 of the needs sources and store it in .qik/fingerprint.toml. Use after building the needs index to record a stable checksum.'
---

<!-- @needs axon stamp procedure (Copilot), prd_unit_imp__axon__stamp_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__stamp_procedure_copilot], released -->

# qik axon stamp — record needs fingerprint

Use `mcp_qik-mcp_axon_stamp` or CLI:

```bash
qik axon stamp
```

Computes the SHA-1 of the needs source files and writes the hash to
`.qik/fingerprint.toml`. Commit this file alongside any needs changes
so `mcp_qik-mcp_axon_verify` can detect drift later.
