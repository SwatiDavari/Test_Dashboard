---
description: 'Report how far a need\'s downward cone reaches — open / impl / test / rc coverage status. Use to check whether a requirement has been implemented and tested.'
---

<!-- @needs axon coverage procedure (Copilot), prd_unit_imp__axon__coverage_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__coverage_procedure_copilot], released -->

# qik axon coverage — downward coverage report

Use `mcp_qik-mcp_axon_coverage` or CLI:

```bash
qik axon coverage <NEED_ID>
```

Reports the coverage level of `<NEED_ID>`'s downstream cone:
- `open` — no implementation artefact linked
- `impl` — implementation exists but no test
- `test` — test artefact linked
- `rc` — all downstream artefacts at `released` status

Use this to quickly assess whether a requirement is "done" end-to-end before
closing a PI or cutting a release.
