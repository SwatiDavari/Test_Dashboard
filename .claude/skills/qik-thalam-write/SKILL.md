# qik thalam write — needs authoring procedure


<!-- @needs thalam authoring procedure (Claude Code), prd_unit_imp__thalam__authoring_procedure_claude, prd_unit_imp, [prd_unit_des__thalam__authoring_procedure_claude], released -->
Executed by the **qik-thalam-author** persona (Content Expert).

## When to invoke

When a CR or intent needs new graph content drafted. When nexus hands off
authoring. When drift repair requires new content rather than a relink.

## Procedure

### Step 1 — Ground yourself

Call `axon_show(<parent_id>)` on the intent/requirement/CR you are realizing.
Call `axon_list` on the target layer to see what's already authored.
Never grep `needs/` by hand.

### Step 2 — Classify

Pick exactly one structural tag (`glob`/`feat`/`comp`/`unit`), one process/layer
tag (`int`/`req`/`arc`/`des`/`imp`), and one enabler tag (`sys_`/`prd_`/`tst_`/
`doc_`/`bld_`/`saf_`/`sec_`).

**Verify the enabler against the content before doing anything else with
it.** Read `.qik/thalam/sme/guardrails/integrity.md` and check its enabler-tracks-
whose-work guard before loading any enabler's SME file — do not
re-derive this check from memory. If the content and the chosen enabler
don't match, stop and re-classify; do not load the mismatched enabler's SME
file and rationalize the wrong choice forward.

**Load the SME skill file** for the resolved enabler before drafting:

| Enabler | File |
|---------|------|
| `sys_` | `.qik/thalam/sme/enabler/sys.md` |
| `prd_` | `.qik/thalam/sme/enabler/prd.md` |
| `tst_` | `.qik/thalam/sme/enabler/tst.md` |
| `doc_` | `.qik/thalam/sme/enabler/doc.md` |
| `saf_` | `.qik/thalam/sme/enabler/saf.md` |
| `sec_` | `.qik/thalam/sme/enabler/sec.md` |
| `bld_` | `.qik/thalam/sme/enabler/bld.md` |

Apply its `## Authoring guidance` section throughout drafting.

**Load the layer-expert skill file** for the resolved layer (skip for `imp` —
no layer-expert exists at that layer):

| Layer | File |
|-------|------|
| `int` | `.qik/thalam/sme/layer/int.md` |
| `req` | `.qik/thalam/sme/layer/req.md` |
| `arc` | `.qik/thalam/sme/layer/arc.md` |
| `des` | `.qik/thalam/sme/layer/des.md` |

**Load the scope-expert skill file** for the resolved scope, following the
three-branch selection procedure (`sys_` → always `glob`; `des`/`imp` layer →
always `unit`; otherwise judge `glob`/`feat`/`comp` from the content's actual
grain):

| Scope | File |
|-------|------|
| `glob` | `.qik/thalam/sme/scope/glob.md` |
| `feat` | `.qik/thalam/sme/scope/feat.md` |
| `comp` | `.qik/thalam/sme/scope/comp.md` |
| `unit` | `.qik/thalam/sme/scope/unit.md` |

Apply all three families' `## Authoring guidance` together — they compose
into one coherent output, not three paragraphs stapled together.

### Step 3 — Draft

Positive phrasing, indicative present tense, active voice. A title is not a
body. A `req` title is a headline, not the requirement. An `int` body states the
conviction — never narrates the node's own graph position. An `arc` node always
carries an element list plus a structural diagram (mermaid, component/class/
block) — the diagram IS the architecture, not an illustration of it — and a
behavioral and/or physical diagram wherever the elements have real interaction
or spatial/hardware allocation to show. `sme_layer_arc` (loaded in Step 2)
carries the full shape; `sys_req__concept__arc_content_shape` states the
underlying content-shape mandate.

### Step 4 — Apply the three lenses to your own draft

Mandatory, before anything is written. These are the same three lenses
`qik-thalam-critique` will apply — not a review instrument it owns, but the
quality standard itself. You hold the draft to it at authoring time; critique
holds it to the same standard later, independently. That is what lets the
review be independent without inventing a different bar.

- **Can it fail?** What would have to happen for this artifact to be wrong? A
  node nothing could falsify states nothing.
- **Is it inconsistent?** Does it contradict its own parent, a sibling, or
  itself? Check the parent's actual text, not your memory of it.
- **Is it incomplete?** Does it concretely answer *how* the linked
  requirement or architecture is realized, or only assert that a mechanism
  exists? A title-only node is incomplete however well the title is worded.

Rewrite until all three pass. Carrying a known lens failure into the graph and
leaving it for critique to find is a defect you authored, not a review finding.

### Step 5 — Write

Path: `needs/<module>/<layer>/<scope>/<name>.md`
ID: `<enabler>_<scope>_<layer>__<module>__<name>`
Status: `proposed` by default, `approved` only when explicitly reviewed.

### Step 6 — Verify and report

```bash
qik axon check
```

Zero errors required. Check toctree for new `des/unit/` files. Every new entry
in a cluster's `index.md` toctree shall be inserted at its correct sorted
position (enabler, then scope, then layer — see
`.qik/thalam/sme/guardrails/presentation.md`'s navigation-ordering guard), never
appended at the end; the same toctree shall carry no duplicate entry. Run
lifecycle gate.
Report new IDs, file paths, and statuses. Hand back to nexus or the user.
