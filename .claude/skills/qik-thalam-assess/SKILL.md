# qik thalam assess — needs critique procedure

<!-- @needs Claude Code procedure surface for the 3-lens assessment workflow, prd_unit_imp__thalam__critique_procedure_claude, prd_unit_imp, [prd_unit_des__thalam__authoring_procedure_claude], released -->
<!-- @needs thalam assess skill (Claude), prd_unit_imp__thalam__assess_skill_claude, prd_unit_imp, [prd_unit_des__thalam__assess_skill_claude], released -->

Executed by the **qik-thalam-critique** persona (independent reviewer).

## When to invoke

At a status-advance gate (proposed → approved, or further). When nexus requires
a critique pass at step 14a of the CR orchestration. When the user requests
explicit review.

## Procedure

### Step 1 — Ground (independent context)

This skill MUST be invoked as a genuinely fresh context, never a continuation
of the authoring session. Load the need IDs to assess and read each one via
`axon_show(<id>)`.

### Step 2 — Load the enabler, scope, and layer checklists

Critique must be grounded in the same standard that governed authoring — the
same three orthogonal families, not the enabler alone.

For each assessed need's enabler, load the corresponding SME file:

| Enabler | File |
|---------|------|
| `prd_` | `.qik/thalam/sme/enabler/prd.md` |
| `tst_` | `.qik/thalam/sme/enabler/tst.md` |
| `doc_` | `.qik/thalam/sme/enabler/doc.md` |
| `sys_` | `.qik/thalam/sme/enabler/sys.md` |
| `bld_` | `.qik/thalam/sme/enabler/bld.md` |
| `saf_` | `.qik/thalam/sme/enabler/saf.md` |
| `sec_` | `.qik/thalam/sme/enabler/sec.md` |

For each assessed need's layer, load the corresponding layer-expert file
(skip for `imp`):

| Layer | File |
|-------|------|
| `int` | `.qik/thalam/sme/layer/int.md` |
| `req` | `.qik/thalam/sme/layer/req.md` |
| `arc` | `.qik/thalam/sme/layer/arc.md` |
| `des` | `.qik/thalam/sme/layer/des.md` |

For each assessed need's scope, load the corresponding scope-expert file:

| Scope | File |
|-------|------|
| `glob` | `.qik/thalam/sme/scope/glob.md` |
| `feat` | `.qik/thalam/sme/scope/feat.md` |
| `comp` | `.qik/thalam/sme/scope/comp.md` |
| `unit` | `.qik/thalam/sme/scope/unit.md` |

Also read `.qik/thalam/sme/guardrails/integrity.md` and apply its guards — the
enabler-tracks-whose-work check and the never-reproduce-a-
codelinks-marker prohibition — regardless of which enabler/layer/scope
files above were loaded for this need.

Apply every indicator from all loaded files' `## Review checklist` sections,
in addition to the three lenses below. Skip a file only if it does not yet
exist — never invent indicators from memory.

### Step 3 — Apply three lenses

For each need, evaluate:

1. **Can fail** — is there a realistic scenario where this node's content is
   wrong, contradictory, or untestable?
2. **Inconsistent** — does this node conflict with any other node in its
   blast radius?
3. **Incomplete** — is the body substantive? Does it say anything, or just
   restate the title?

### Step 4 — Classify findings

- **Hard violations** — must be resolved before advancing to `approved`.
  Return: `{id, axis, finding, fix_suggestion}`
- **Advisory violations** — document as follow-up; do not block.

### Step 5 — Report

Return findings to the caller (nexus or human). Do NOT modify any needs files.
This is a read-only skill.
