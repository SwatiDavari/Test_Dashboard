---
description: 'Display the stored needs stamp — algorithm, hash, updated timestamp. Pure read, no computation. Use to quickly check when the fingerprint was last updated.'
---

<!-- @needs axon fingerprint procedure (Copilot), prd_unit_imp__axon__fingerprint_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__fingerprint_procedure_copilot], released -->

# qik axon fingerprint — show stored stamp

Use `mcp_qik-mcp_axon_fingerprint` or CLI:

```bash
qik axon fingerprint
```

Reads `.qik/fingerprint.toml` and returns the stored algorithm, hash, and
last-updated timestamp. No computation, no write.

To recompute and store a new stamp, use `mcp_qik-mcp_axon_stamp`.
