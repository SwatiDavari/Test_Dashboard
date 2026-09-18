---
description: >-
  Author a new sphinx-needs node (requirement, architecture, design, or
  implementation) using the qik-thalam-author agent. Provide the CR or intent
  context and the target enabler+scope+layer. The authored node is returned
  with its id, file path, and status.
---

<!-- @needs thalam authoring procedure (Copilot), prd_unit_imp__thalam__authoring_procedure_copilot, prd_unit_imp, [prd_unit_des__thalam__authoring_procedure_copilot], released -->

# qik thalam write

Invoke **qik-thalam-author** to draft one sphinx-needs node.

## Required context

Provide at minimum:

- **Parent need id** (intent, requirement, or architecture element being realized)
- **Target layer**: `int` / `req` / `arc` / `des` / `imp`
- **Enabler**: `prd_` / `tst_` / `doc_` / `sys_` / `bld_` / `saf_` / `sec_`
- **Scope**: `glob` / `feat` / `comp` / `unit`
- **Cluster** (owning module, e.g. `axon`, `nexus`, `thalam`)
- **What** the node should express (one-sentence intent)

## thalam-author will

1. Classify one structural tag (`glob`/`feat`/`comp`/`unit`), one layer tag
   (`int`/`req`/`arc`/`des`/`imp`), and one enabler tag (`sys_`/`prd_`/`tst_`/
   `doc_`/`bld_`/`saf_`/`sec_`). **Verify the enabler against the content
   before loading anything** — read
   `.qik/thalam/sme/guardrails/integrity.md` and check its
   enabler-tracks-whose-work guard first; do not re-derive this check from
   memory, and do not load a mismatched enabler's SME file and rationalize
   the wrong choice forward.

   Load the SME knowledge file for the resolved **enabler**:

   | Enabler | File |
   |---------|------|
   | `sys_` | `.qik/thalam/sme/enabler/sys.md` |
   | `prd_` | `.qik/thalam/sme/enabler/prd.md` |
   | `tst_` | `.qik/thalam/sme/enabler/tst.md` |
   | `doc_` | `.qik/thalam/sme/enabler/doc.md` |
   | `saf_` | `.qik/thalam/sme/enabler/saf.md` |
   | `sec_` | `.qik/thalam/sme/enabler/sec.md` |
   | `bld_` | `.qik/thalam/sme/enabler/bld.md` |

   Load the SME knowledge file for the resolved **layer** (skip for `imp` —
   no layer-expert exists at that layer):

   | Layer | File |
   |-------|------|
   | `int` | `.qik/thalam/sme/layer/int.md` |
   | `req` | `.qik/thalam/sme/layer/req.md` |
   | `arc` | `.qik/thalam/sme/layer/arc.md` |
   | `des` | `.qik/thalam/sme/layer/des.md` |

   Load the SME knowledge file for the resolved **scope**, following the
   three-branch selection procedure (`sys_` → always `glob`; `des`/`imp`
   layer → always `unit`; otherwise judge `glob`/`feat`/`comp` from the
   content's actual grain):

   | Scope | File |
   |-------|------|
   | `glob` | `.qik/thalam/sme/scope/glob.md` |
   | `feat` | `.qik/thalam/sme/scope/feat.md` |
   | `comp` | `.qik/thalam/sme/scope/comp.md` |
   | `unit` | `.qik/thalam/sme/scope/unit.md` |

   Apply all three families' `## Authoring guidance` sections together — they
   compose into one coherent output, not three paragraphs stapled together.
2. Draft the node at `status: proposed`
3. Apply the three lenses to its own draft, and rewrite until all three pass
4. Return the id, file path, and directive block

## The three lenses — mandatory at authoring time

These are the same lenses `qik-thalam-critique` applies. They are not a review
instrument critique owns; they are the quality standard, and the author is held
to it first.

- **Can it fail?** What would have to happen for this artifact to be wrong? A
  node nothing could falsify states nothing.
- **Is it inconsistent?** Does it contradict its own parent, a sibling, or
  itself? Check the parent's actual text, not a memory of it.
- **Is it incomplete?** Does it concretely answer *how* the linked requirement
  or architecture is realized, or only assert that a mechanism exists?

Carrying a known lens failure into the graph, to be found by critique later, is
a defect the author introduced — not a review finding.

## After authoring

Run `qik axon check` to confirm the new node is linked and the graph is coherent.

If the node is new to its cluster, insert its entry into that cluster's
`index.md` toctree at its correct sorted position — enabler, then scope, then
layer — never appended at the end, and confirm the toctree carries no
duplicate entry. See `.qik/thalam/sme/guardrails/presentation.md`'s
navigation-ordering guard for the fixed order.
