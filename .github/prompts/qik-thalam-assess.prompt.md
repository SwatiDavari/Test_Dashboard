---
description: >-
  Assess (critique) one or more authored sphinx-needs nodes using the
  qik-thalam-critique agent. Provide the need ids to assess. thalam-critique
  applies the three lenses (can fail / inconsistent / incomplete) plus
  enabler-specific checklists and returns hard and advisory findings.
---

<!-- @needs qik-thalam-assess command-verb prompt, prd_unit_imp__thalam__assess_procedure_copilot, prd_unit_imp, [prd_unit_des__thalam__assess_procedure_copilot], released -->

# qik thalam assess

Invoke **qik-thalam-critique** to independently review one or more authored
sphinx-needs nodes.

## Required input

- **Need ids** to assess (one or more `prd_`/`tst_`/`doc_`/… ids)
- **Assessment scope**: which lenses to apply (default: all three)

## thalam-critique will

1. Load the standard checklist for each assessed node's enabler
2. Apply three lenses: *can fail*, *inconsistent*, *incomplete*
3. Return findings in two classes:
   - **Hard violations** — must be resolved before `status: approved`
   - **Advisory violations** — document as follow-up or commit note

## After assessment

Hard violations must be addressed before advancing the CR to `validate`. Fix
the node content by running the `qik-thalam-write` procedure, which re-authors
the affected node through the `qik-thalam-author` persona — thalam has no CLI
surface, so there is no `qik thalam …` command to invoke. Then re-run
`qik axon check`.
