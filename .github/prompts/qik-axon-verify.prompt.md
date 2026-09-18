---
description: 'Compare current needs checksum against the stored stamp. Use to detect whether the needs sources have drifted since the last stamp.'
---

<!-- @needs axon verify procedure (Copilot), prd_unit_imp__axon__verify_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__verify_procedure_copilot], released -->

# qik axon verify — check needs fingerprint

Use `mcp_qik-mcp_axon_verify` or CLI:

```bash
qik axon verify
```

Computes the current SHA-1 of needs sources and compares it against the hash
stored in `.qik/fingerprint.toml`. Returns `identity` (match) or `change`
(mismatch with stored/current hashes).

If the check shows `change`: edit the needs source, rebuild, and run `mcp_qik-mcp_axon_stamp`.
