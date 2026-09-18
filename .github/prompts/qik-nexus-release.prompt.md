---
description: 'Ship all staged items under the current version — moves staged entries to released and stamps the version. Use when cutting a release.'
---

<!-- @needs nexus release procedure (Copilot), prd_unit_imp__nexus__release_procedure_copilot, prd_unit_imp, [prd_unit_des__nexus__release_procedure_copilot], proposed -->

# qik nexus release — ship a release

Use `mcp_qik-mcp_nexus_release` or CLI:

```bash
qik nexus release
```

Moves all `staged` entries to `released` and stamps them with the current version
(from the bump config). The version is derived from the `change` nature of staged
entries unless you have set it explicitly with `qik nexus bump`.

## Pre-release checklist

1. Confirm staged items are correct: `qik nexus list staged`
2. Optional: preview release notes from the staged set (see the qik-nexus
   agent's "Release notes preview" workflow) before shipping.
3. Check the version that will be used: `qik nexus version`
4. Bump version if needed: `qik nexus bump <major|minor|patch>`
5. Run `qik nexus release`.
6. Commit `.qik/nexus/entries.toml` with a release commit message.
