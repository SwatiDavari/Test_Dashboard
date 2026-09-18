<!-- @needs sme_enabler_sys skill file — ISO/IEC/IEEE 15288 systems-engineering expert, prd_unit_imp__thalam__sme_enabler_sys, prd_unit_imp, [prd_unit_des__thalam__sme_enabler_sys], proposed -->

# sme_sys — ISO/IEC/IEEE 15288 Systems-Engineering Expert

**Load trigger:** enabler prefix `sys_`  
**References:** ISO/IEC/IEEE 15288:2023 (System and Software Engineering — System Life Cycle Processes), ASPICE SYS.1–5 (https://www.automotivespice.com/), Eclipse S-CORE

`sys_`'s scope is always `glob` — the id schema omits the segment because no other scope applies to `sys_`. A `sys_` node never has a `feat` or `comp` scope qualifier.

---

**Content gate — verify before applying anything below.** This file
applies only when the target node's content genuinely *is* systems-
engineering intent/requirement/architecture content establishing the
enabling-system model itself — not merely attached to a `sys_` parent, and
never any one enabler's own product, verification, or delivery content
wearing a `sys_` id. Ask: stripped of its id, would this node's actual
content read as this? If it would read as some other enabler's work
instead (the enabler-vs-topic guard), do not force-fit it here — reject
it and report the mismatch back as a design error, the same way
`qik-thalam-author`'s and `qik-thalam-critique`'s own hard-prohibition
sections do.

## Authoring guidance

### sys_int — Mission Analysis (ISO 15288 §6.4.1)

A `sys_int` states a **mission purpose**: why this system-of-interest exists, what unacceptable situation it resolves, and for whom. It must not contain solution vocabulary or implementation choices.

**Shall contain:**
- The stakeholder class whose need drives the system ("operators of…", "the development team…")
- The operational context or environment
- The unacceptable situation or constraint being resolved
- The intended outcome (in terms of capability or mission, not technical solution)

**Shall not contain:**
- References to specific technologies, frameworks, or tools
- How the system works (that belongs at `arc` or `des`)
- Normative shall-clauses (that belongs at `req`)

**Form (ISO 15288 §6.4.1 Mission Analysis):**
> "[Context] currently [problem/constraint]. The system-of-interest shall enable [stakeholder] to [outcome], within [boundary]."

**Scope:** `sys_` admits only `glob` scope. A `sys_int` applies to the whole system-of-interest, not to a feature or component.

---

### sys_req — System Requirements Definition (ISO 15288 §6.4.4, ASPICE SYS.2)

A `sys_req` states a **verifiable, traceable obligation** on the system-of-interest. It must be derivable from at least one `sys_int` or stakeholder need.

**Quality criteria (ISO 15288 §6.4.4 + ISO/IEC/IEEE 29148):**
- **Unambiguous:** one and only one interpretation
- **Verifiable:** an acceptance criterion can be derived
- **Necessary:** traces to a stakeholder need or a `sys_int`
- **Complete:** no TBD, TBR, or deferred content
- **Consistent:** no contradiction with siblings

**Form:** "The system shall [action] [condition/constraint]." — shall-form only; no "should", "may", or passive constructions.

**ASPICE SYS.2 compliance:** each `sys_req` carries:
- A rationale (why this requirement exists)
- A source traceability (which `sys_int` or stakeholder need it derives from)
- A priority or stability indicator where applicable

---

### sys_arc — System Architecture Definition (ISO 15288 §6.4.5, ASPICE SYS.3)

A `sys_arc` element states **what system element takes on which responsibility** and **how elements interface**. It allocates functions from requirements to architectural elements.

**Shall contain:**
- Which architectural element is described (name and role)
- Which `sys_req`(s) it satisfies (via `:fulfils:` or `:implements:`)
- The element's interfaces (inputs and outputs, named concretely)
- The operational mode or condition if applicable

**ASPICE SYS.3 compliance:**
- All `sys_req` must be allocated to at least one `sys_arc` element
- All interfaces between elements must be specified
- If `saf_` co-exists: ASIL allocation per element must be noted
- If `sec_` co-exists: cybersecurity trust boundary placement must be noted

**Eclipse S-CORE decomposition:** `sys_arc` at `glob` scope describes the top-level system; sub-systems are authored as `prd_feat_arc` or `prd_comp_arc` nodes at feature/component scope in the relevant enabling system.

---

## Review checklist

Apply each indicator when critique reviews a `sys_` node. Emit **pass/fail** for mechanizable indicators, **0–3 score + justification** for subjective ones.

### For sys_int

| # | Indicator | Type |
|---|-----------|------|
| S-I-1 | Names at least one stakeholder class | pass/fail |
| S-I-2 | States the operational context | pass/fail |
| S-I-3 | States the unacceptable situation or constraint | pass/fail |
| S-I-4 | Uses no solution/technology vocabulary | pass/fail |
| S-I-5 | Contains no shall-clauses | pass/fail |
| S-I-6 | Scope is `glob` (id schema: no scope segment for `sys_`) | pass/fail |
| S-I-7 | Clarity of purpose statement | 0–3 |
| S-I-8 | Completeness of stakeholder context | 0–3 |

### For sys_req

| # | Indicator | Type |
|---|-----------|------|
| S-R-1 | Uses "shall" (not "should", "may", passive voice) | pass/fail |
| S-R-2 | Traceable to a `sys_int` via `:refines:` | pass/fail |
| S-R-3 | No TBD/TBR/placeholder content | pass/fail |
| S-R-4 | Single-condition (not a compound shall) | pass/fail |
| S-R-5 | Verifiable — an acceptance criterion is derivable | 0–3 |
| S-R-6 | Unambiguous — only one interpretation | 0–3 |
| S-R-7 | Consistent with sibling `sys_req` nodes | 0–3 |

### For sys_arc

| # | Indicator | Type |
|---|-----------|------|
| S-A-1 | Names the architectural element | pass/fail |
| S-A-2 | Carries `:fulfils:` or `:implements:` link to `sys_req` | pass/fail |
| S-A-3 | All `sys_req` in scope allocated to at least one element | pass/fail |
| S-A-4 | All interfaces between elements are named | pass/fail |
| S-A-5 | ASIL allocation present if `saf_` nodes co-exist | pass/fail |
| S-A-6 | Rationale for decomposition stated | 0–3 |
| S-A-7 | Granularity appropriate for `glob` scope | 0–3 |
