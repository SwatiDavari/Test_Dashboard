---
description: 'Attach an external tracker reference to a CR. Use to link a GitHub issue, Jira ticket, or other tracker item to a nexus entry.'
---

<!-- @needs nexus ref procedure (Copilot), prd_unit_imp__nexus__ref_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__ref_procedure_copilot], proposed -->

# qik nexus ref — attach external reference

Use `mcp_qik-mcp_nexus_ref` or CLI:

```bash
qik nexus ref <CR_ID> --what github --locator "HartmannNico/qorix-ik#42"
qik nexus ref <CR_ID> --what jira   --locator "QORIX-42"
```

Multi-valued: repeated calls append references, not overwrite.
References appear in `qik nexus show` output.
