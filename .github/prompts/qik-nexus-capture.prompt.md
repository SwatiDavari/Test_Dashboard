---
description: 'Capture a new change request at a stage (idea / backlog / pi). Use when recording a new CR, feature request, bug, or idea.'
---

<!-- @needs nexus capture procedure (Copilot), prd_unit_imp__nexus__capture_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__capture_procedure_copilot], proposed -->

# qik nexus capture — record a new CR

Use `mcp_qik-mcp_nexus_capture` or CLI:

```bash
qik nexus capture \
  --stage <idea|backlog|pi> \
  --headline "<one-line summary>" \
  --what "<what this entry is>" \
  --why "<why it matters>" \
  [--change <breaking|feature|fix>]
```

## Guidelines

- **headline**: concise, action-oriented (≤ 80 chars)
- **what**: describe the scope precisely — what will change, what new capability
- **why**: the motivation — what problem it solves, what it enables
- **change**: semver nature of the change (`breaking`, `feature`, `fix`)
- **stage**: start at `idea` for rough thoughts, `backlog` for shaped work,
  `pi` for committed sprint items

After capture, verify with `mcp_qik-mcp_nexus_show` on the returned id.
