---
description: 'Move a need\'s lifecycle status one step forward. Use to advance a requirement or design artefact from proposed → approved → released → deprecated → retired.'
---

<!-- @needs axon advance procedure (Copilot), prd_unit_imp__axon__advance_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__advance_procedure_copilot], released -->

# qik axon advance — advance need status

Use `mcp_qik-mcp_axon_advance` or CLI:

```bash
qik axon advance <NEED_ID>
```

Mutates the authored source `.md` — never `needs.json`.

Status progression: `proposed → approved → released → deprecated → retired`

After running, rebuild the needs index (`scripts/needs-build.sh`)
so the change is visible in `needs.json`.

## Pre-advance gate (mandatory before advancing to `released`)

Before advancing **any** need to `released`, run `axon_check` with `--assume`
to simulate the post-advance state:

```python
axon_check(assume={"<NEED_ID>": "released"}, deny_warnings=True)
```

If the check **passes** → proceed with `axon_advance`.

If the check **reports errors** → stop and choose:

1. **Fix the gap first** — invoke **qik-thalam-author** to author the missing
   arc, imp, or link that the error names, then re-run the assume check before
   advancing.
2. **Do not advance** — the need is not structurally ready for `released`. Keep
   it at `approved` and create a follow-up CR.

Never advance to `released` past a failing assume check. The pre-commit hook
enforces the same rules, so a skipped gate guarantees a blocked commit.

### Batch advance

When advancing many needs in one wave, build the full `assume` dict first:

```python
assume = {nid: "released" for nid in needs_to_advance}
axon_check(assume=assume, deny_warnings=True)
```

If **any** errors appear, resolve each one before advancing the batch — or
split the batch and advance only the structurally complete subset.
