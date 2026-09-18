<!-- @needs sme_enabler_prd skill file — ISO/IEC/IEEE 29148:2018 + ASPICE SWE requirements engineering expert, prd_unit_imp__thalam__sme_enabler_prd, prd_unit_imp, [prd_unit_des__thalam__sme_enabler_prd], proposed -->

# sme_prd — ISO/IEC/IEEE 29148:2018 + ASPICE SWE Requirements Engineering Expert

**Load trigger:** enabler prefix `prd_`  
**References:** ISO/IEC/IEEE 29148:2018 (ISO catalog 72089, https://www.iso.org/standard/72089.html), ASPICE 4.0 SWE.1–SWE.3 (https://www.automotivespice.com/)

**Note:** ISO/IEC/IEEE 29148:2018 is confirmed current (reviewed 2024). A revised edition (ISO/IEC/IEEE DIS 29148, catalog 94091) is under development but not yet published. Use the 2018 edition.

---

**Content gate — verify before applying anything below.** This file
applies only when the target node's content genuinely *is* the product's
own delivered requirement, architecture, design, or implementation — what
is actually built and shipped — not merely attached to a `prd_` parent.
Verification evidence for that product (a test suite, test vectors, test
cases) is `tst_`, `:verifies:`-linked back here, never authored under this
enabler with an `:implements:` link, however closely it sits next to the
feature it verifies. Ask: stripped of its id, would this node's actual
content read as product delivery, or as verification of it (the
enabler-vs-topic guard). If it reads as verification, do not
force-fit it here — reject it and report the mismatch back as a design
error, the same way `qik-thalam-author`'s and `qik-thalam-critique`'s own
hard-prohibition sections do.

## Authoring guidance

### prd_feat_req — Feature Requirement (ISO 29148 §5.2.5, ASPICE SWE.1)

A feature requirement states a **single, verifiable, traceable obligation** on the system's feature-level behavior. It derives from a feature intent (`prd_feat_int`) or directly from a `sys_req`.

**8 quality characteristics (ISO 29148 §5.2.5):**
1. **Necessary** — traces to a stated need or higher-level requirement
2. **Appropriate** — suitable abstraction for the feature level
3. **Unambiguous** — only one interpretation possible
4. **Complete** — no TBD, TBR, or placeholder content
5. **Singular** — one condition, one obligation
6. **Feasible** — achievable within known engineering constraints
7. **Verifiable** — an acceptance criterion can be derived from it
8. **Correct** — accurately describes a real system behavior

**Form:** "The system shall [action] [condition/constraint]." — shall-form only; no "should", "may", or passive voice within the shall clause.

**ASPICE SWE.1 compliance:** Carry a unique ID, a rationale (why this requirement exists), and a source traceability (`:refines:` link to parent).

**Not allowed:** No `int`-layer vocabulary (goal/purpose/problem statements belong at `prd_feat_int`). No design decisions (those belong at `prd_comp_arc` or `prd_unit_des`).

---

### prd_comp_req — Component Requirement (ISO 29148 §5.2.5, ASPICE SWE.1)

Inherits all 8 quality characteristics from feat_req, and additionally:
- **Names the component** responsible for satisfying this requirement
- **Traces via `:refines:`** to the parent `prd_feat_req` it decomposes

Component requirements are more specific than feature requirements: they constrain a particular subsystem's behavior, interface, or resource budget, not the overall feature.

---

### prd_comp_arc — Software Architecture (ISO 29148 §5.2.7, ASPICE SWE.2)

A component architecture element specifies **how** a component is structured to satisfy its requirements:
- Names the architectural elements (modules, services, interfaces)
- Allocates requirements from `prd_comp_req` to elements via `:fulfils:`
- Specifies interfaces: input/output signals, data types, protocols
- States the rationale for the decomposition decision
- Notes testability considerations (how will a unit test verify this?)

**ASPICE SWE.2:** Every `prd_comp_req` must be traceable to at least one `prd_comp_arc` element.

---

### prd_unit_des — Unit Design (ASPICE SWE.3)

A unit design specifies **how** a unit is realized in code:
- Names the algorithm, data structure, or interface concretely (not "a mechanism exists")
- Names the programming language / API / class used
- States the error handling strategy for this unit
- States testability: which inputs cause which outputs (enables unit test cases)

**ASPICE SWE.3 completeness criterion:** A reviewer reading only this node and its parent arc should be able to implement the unit without asking questions.

**Not a unit design:** "Unit X will handle Y" — that is architecture. "Unit X uses a ring buffer of size N where N is dynamically sized" — that is design.

---

## Review checklist

Apply each indicator when critique reviews a `prd_` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

### For prd_feat_req / prd_comp_req

| # | Indicator | Type |
|---|-----------|------|
| P-R-1 | Uses "shall" (not "should", "may", passive voice) | pass/fail |
| P-R-2 | Traceable via `:refines:` to parent | pass/fail |
| P-R-3 | No TBD/TBR/placeholder content | pass/fail |
| P-R-4 | Single condition (not a compound "shall A and B") | pass/fail |
| P-R-5 | Verifiable — acceptance criterion derivable | 0–3 |
| P-R-6 | Unambiguous — one interpretation only | 0–3 |
| P-R-7 | Consistent with sibling requirements | 0–3 |
| P-R-8 | Feasible within known engineering constraints | 0–3 |

### For prd_comp_arc

| # | Indicator | Type |
|---|-----------|------|
| P-A-1 | Carries `:fulfils:` link to `prd_comp_req` | pass/fail |
| P-A-2 | Names all interfaces (inputs/outputs) — **n/a** if the element has no interface of its own to name (see note below) | pass/fail/n/a |
| P-A-3 | All prd_comp_req in scope allocated to at least one element | pass/fail |
| P-A-4 | Rationale for decomposition stated | 0–3 |
| P-A-5 | Granularity appropriate for component scope | 0–3 |

**P-A-2 applicability note:** interface/I-O language only applies to a
`prd_comp_arc` that specifies a component boundary (signals, data types,
protocols crossing that boundary). A `prd_comp_arc` that is a structural or
documentation-purpose overview — decomposition rationale, module
organization, a site/navigation structure — legitimately has no interface
of its own to specify. Applying P-A-2 there produces a false positive that
trains authors to either invent interface language that doesn't belong or
silently ignore the indicator. Mark P-A-2 **n/a** for such nodes rather
than fail; do not skip it silently — an explicit n/a still shows the
indicator was considered.

### For prd_unit_des

| # | Indicator | Type |
|---|-----------|------|
| P-D-1 | Carries `:fulfils:` and `:implements:` links | pass/fail |
| P-D-2 | Names algorithm/data structure/interface concretely | pass/fail |
| P-D-3 | No "a mechanism exists" — specificity required | pass/fail |
| P-D-4 | Implementable without further questions | 0–3 |
| P-D-5 | Testable — inputs/outputs stated specifically enough for unit test | 0–3 |
