<!-- @needs sme_enabler_doc skill file — ISO/IEC/IEEE 26511:2018 + ISO/IEC 26514 documentation expert, prd_unit_imp__thalam__sme_enabler_doc, prd_unit_imp, [prd_unit_des__thalam__sme_enabler_doc], proposed -->

# sme_doc — ISO/IEC/IEEE 26511:2018 + ISO/IEC 26514 Documentation Expert

**Load trigger:** enabler prefix `doc_`  
**References:** ISO/IEC/IEEE 26511:2018 (managing information for users), ISO/IEC 26514 (design and development of user documentation)

The `doc_` enabler governs the documentation enabling system. `sys_arc__concept__doc_enabler` maps each `doc_` scope×layer point: outer `glob`/`feat` points (26511 — what documentation shall contain and how it is managed) and inner `comp`/`unit` points (26514 — how documentation is structured and what each unit carries).

**Scope note:** `doc_` has no `int` layer. The layer spine for doc_ is req → arc → des → imp only.

---

**Content gate — verify before applying anything below.** This file
applies only when the target node's content genuinely *is* documentation
content — what a reader-facing deliverable presents and how — not merely
attached to a `doc_` parent. The product behavior being documented is
`prd_`; verification of the documentation itself is `tst_`. Ask: stripped
of its id, would this node's actual content read as documentation, or as
some other enabler's work instead (the enabler-vs-topic guard)? If it
reads as something else, do not force-fit it here — reject it and
report the mismatch back as a design error, the same way
`qik-thalam-author`'s and `qik-thalam-critique`'s own hard-prohibition
sections do.

## Authoring guidance

### doc_glob_req / doc_feat_req — Documentation Requirements (ISO/IEC/IEEE 26511:2018)

A documentation requirement states what the documentation product shall accomplish for its users.

**ISO 26511 §6 (Documentation plan requirements):** Each documentation requirement shall:
- **Name the target audience** (developer, end user, operator, administrator)
- **Name the information product type** (user guide, reference manual, API documentation, tutorial, release notes)
- **Name the delivery format** (HTML, PDF, mdBook, embedded help)
- **State the purpose** — which user task or information need the document supports
- **Carry a rationale** tracing to the system capability it documents

Form: "The documentation shall provide [audience] with [information type] covering [capability], in [format]."

**ASPICE SUP.7 (Documentation, https://www.automotivespice.com/):** Documentation requirements shall be managed, reviewed, and versioned alongside the system they document.

---

### doc_comp_arc — Documentation Architecture (ISO/IEC 26514:2022)

A documentation architecture element specifies how documentation content is structured:
- **Topic type** (concept/procedure/reference) — must be declared and consistent within a unit
- **Information architecture** — chapter hierarchy, navigation, cross-references
- **Naming the committed location** (the exact file path or module in the project's own documentation source tree, whatever generator or convention it uses)
- **Rationale** — why this structure serves the target audience

**ISO 26514 §9 (Structuring information):** Concept topics explain what; procedure topics instruct how (numbered steps, one action per step); reference topics list facts. Never mix topic types within a single unit.

---

### doc_unit_des — Documentation Unit Design (ISO/IEC 26514:2022 §10)

A documentation unit design specifies what a single documentation unit shall contain:
- **Topic type declared** (concept/procedure/reference) and consistent with the arc
- **Committed location** — the exact file path or module where the prose will live
- **Content specification** — what information items the unit must cover
- **Audience and task** — who reads this and what task it supports

**Not a design:** "Chapter X will explain Y" — that is architecture. "Chapter X shall explain Y by listing the three configuration parameters (name, type, default) in a reference table" — that is design.

### doc_unit_imp — Documentation Prose (codelinks-scanned marker, never hand-authored)

`doc_unit_imp` is OUTPUT, not a need — like every `_imp` need in this project, it is never a hand-authored directive block under `needs/`, with no exception for `doc_`. The real prose lives inside the project's own documentation source tree — at whatever path and using whatever doc-generator convention that project has adopted (e.g. a project's own `docs/` tree, whatever generator it uses) — with a `<!-- @needs title, id, type, [links] -->` HTML-comment marker inline in that same page; sphinx-codelinks scans that marker to produce the graph node. `sme_doc` never writes into `needs/` for this layer. When generating prose:
1. Read the `doc_unit_des` node to determine topic type, committed location, and content specification
2. Apply the correct topic-type structure:
   - **Concept:** declarative sentences, no imperative voice, explains what something is
   - **Procedure:** numbered steps, one action per step, present tense imperative ("Click", "Enter", "Run")
   - **Reference:** structured tables, consistent entry format, minimal prose
3. Write the prose directly into the documentation source file at the committed location (as named by the `doc_unit_des` node), with the `<!-- @needs ... -->` marker inline in that same file
4. Never author a `doc_unit_imp` directive block in a `needs/*.md` file under any circumstance — not as a placeholder, not "temporarily," not even when the committed location is unclear (ask instead of hand-authoring)
5. Never choose a new location — location is a design-level decision

---

## Review checklist

### For doc_feat_req / doc_comp_req

| # | Indicator | Type |
|---|-----------|------|
| D-R-1 | Target audience explicitly named | pass/fail |
| D-R-2 | Information product type named | pass/fail |
| D-R-3 | Delivery format named | pass/fail |
| D-R-4 | Purpose / user task stated | pass/fail |
| D-R-5 | Traceable via `:refines:` to parent | pass/fail |
| D-R-6 | Completeness — covers scope of audience needs | 0–3 |

### For doc_comp_arc

| # | Indicator | Type |
|---|-----------|------|
| D-A-1 | Topic type declared | pass/fail |
| D-A-2 | Location committed (file path named) | pass/fail |
| D-A-3 | Topic type consistent within the arc | pass/fail |
| D-A-4 | Navigation/cross-reference structure stated | 0–3 |

### For doc_unit_des

| # | Indicator | Type |
|---|-----------|------|
| D-D-1 | Topic type declared and consistent with arc | pass/fail |
| D-D-2 | Committed location stated (file:line or module) | pass/fail |
| D-D-3 | Content specification present (not just "cover Y") | pass/fail |
| D-D-4 | Sufficient for prose generation without further questions | 0–3 |
| D-D-5 | Audience-appropriate scope | 0–3 |

### For doc_unit_imp

| # | Indicator | Type |
|---|-----------|------|
| D-I-1 | Topic type consistent with des (no mixing) | pass/fail |
| D-I-2 | Real `<!-- @needs -->` marker in the documentation source file committed by des — never a `needs/*.md` directive block | pass/fail |
| D-I-3 | Procedures: numbered steps, one action each | pass/fail |
| D-I-4 | Concepts: declarative, no imperative | pass/fail |
| D-I-5 | Comprehensibility for target audience | 0–3 |
