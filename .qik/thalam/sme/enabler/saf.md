# ISO 26262 skill file — `saf_` authoring guidance + conformance checklist

<!-- @needs saf_ SME enabler skill file, prd_unit_imp__thalam__sme_enabler_saf, prd_unit_imp, [prd_unit_des__thalam__sme_enabler_saf], released -->

Loaded by `qik-thalam-author` (Step 2, authoring guidance) and `qik-thalam-critique`
(Step 3, review checklist) when the target's enabler prefix is `saf_`.

**Reference:** ISO 26262:2018 (Edition 2), Road vehicles — Functional safety
- Part 3: Concept phase — ISO catalog 68385 — §6 HARA, §7 Safety goals
- Part 4: Product development: system level — ISO catalog 68386 — §7 Functional safety requirements
- Part 6: Product development: software level — ISO catalog 68388 — §7 Software safety requirements
- Part 8: Supporting processes — ISO catalog 68390 — §6 Requirements for requirements

**Note:** ISO 26262:2018 is under revision (ISO/DIS 26262-x in development); 2018 edition remains current.

---

**Content gate — verify before applying anything below.** This file
applies only when the target node's content genuinely *is* functional-
safety analysis — hazards, safety goals, functional safety requirements —
not merely attached to a `saf_` parent. The product behavior that
satisfies these is `prd_`. Ask: stripped of its id, would this node's
actual content read as safety analysis, or as some other enabler's work
instead (the enabler-vs-topic guard). If it reads as something
else, do not force-fit it here — reject it and report the mismatch back as
a design error, the same way `qik-thalam-author`'s and
`qik-thalam-critique`'s own hard-prohibition sections do.

## Authoring guidance

### saf_feat_req — Safety Goal (ISO 26262 Part 3 §6–7, HARA)

A safety goal is the top-level functional safety requirement derived from the Hazard Analysis and Risk Assessment (HARA). It must:
- Name the **hazardous event** (Item malfunction × operating situation)
- Carry an **ASIL assignment** (ASIL A/B/C/D or QM — derived from S×E×C in HARA)
- State the **safe state** the system must reach or maintain
- Use **shall-form** — a declarative obligation, not a description

**Form:** "The system shall [prevent/detect/reach safe state] [hazardous condition] to avoid [mishap] (ASIL [X])."

**NOT a safety goal:** Technical solutions (ECU names, software modules) — these belong at `saf_comp_req` or `saf_comp_arc`. A safety goal operates at the item level, not the component level.

**ASIL scope:** If ASIL decomposition is used (Part 9), the decomposed ASILs belong on `saf_comp_req` nodes, not on the safety goal itself.

**Note on AoU shape:** A `saf_feat_req` body is either a shall-clause (ordinary safety requirement) or a declarative assumption sentence (Assumption of Use, per `sys_req__concept__aou_body_shape`). Never mix both shapes in one node.

---

### saf_comp_req — Technical Safety Requirement / FSR (ISO 26262 Part 4 §7)

A technical safety requirement or functional safety requirement (FSR) allocates a safety goal to a system element. It must:
- **Name the system element** responsible
- **State the ASIL** allocated to that element (original or decomposed)
- **Be verifiable** — carry an acceptance criterion
- **Trace via `:refines:`** to the parent safety goal (`saf_feat_req`)
- Use **shall-form**

**Form:** "The [system element] shall [behavior/function] [condition] to satisfy [parent safety goal] (ASIL [X])."

---

### saf_comp_arc — Safety Concept / Safety Architecture (ISO 26262 Part 4 §8)

The safety concept describes how safety goals are allocated to architectural elements:
- Names the architectural elements and their **safety roles**
- Specifies **ASIL decomposition** if used (Part 9) — show allocation of partial ASILs to independent sub-elements
- Notes **diagnostic coverage** requirements for hardware elements (Part 5)
- States **safe state** and **fault tolerant time interval** per element
- Traces via `:fulfils:` to the parent safety requirement

---

- `sys_req__concept__saf_enablers` — `saf_` scopes/layers (glob/feat/comp
  req+arc, plus bare `saf_comp`; no `int`, no `unit`).
- `sys_req__concept__aou_body_shape` — an Assumption of Use is a `saf_*_req`
  body-shape convention (a declarative sentence, never a `shall`-clause), not
  a separate type.
- `sys_arc__concept__saf_sec_relation_shapes` — `mitigates` (req → arc),
  `violates` (arc → prd_/sys_ arc), `covers` (req → AoU-shaped req).
- `.qik/axon/rules.toml` rules `saf_glob_req-must-refine`,
  `saf_feat_req-must-refine`, `saf_comp_req-must-refine`,
  `saf_glob_arc-must-fulfil`, `saf_feat_arc-must-fulfil`,
  `saf_comp_arc-must-fulfil`, `saf_arc-must-have-incoming-mitigates`,
  `need-id-naming`, `need-id-type-match`.

This checklist does not check `violates`/`covers`: those two relation shapes
are sketched in `sys_arc__concept__saf_sec_relation_shapes` but have no
`needs_links`/rule entry yet (deferred wiring) — auditing them here would
enforce structure the graph itself does not yet apply.

## Indicators

| ID | Name | Type | Pass rule |
|---|---|---|---|
| SC-ISO-01 | schema_completeness | mechanized | `id`, `need_type`, `layer`, `scope`, `title`, `status`, and non-empty `content` are all present. For req-layer content: the body is either a single `shall`/`shall not` sentence (ordinary requirement) or a single declarative assumption sentence (AoU-shaped requirement, per `sys_req__concept__aou_body_shape`) — never neither shape. |
| SC-ISO-02 | unique_identification | mechanized | `id` matches the `saf_` alternative of the `need-id-naming` rule's `id_pattern`: `^saf_(glob_(req\|arc)\|feat_(req\|arc)\|comp_(req\|arc)\|comp)__[a-z][a-z0-9_]+__[a-z0-9_]+$`. `need_type` matches the id's leading segment, per `need-id-type-match`. |
| SC-ISO-03 | verifiability | mechanized, req-layer only | The shall-clause or AoU sentence states a condition checkable against the linked architecture (or, for an AoU, against a real operating context) — not a bare, unquantified qualifier ("adequate", "sufficient", "as appropriate", "robust", "efficient") standing in as the entire criterion. Record `result: null` for arc-layer nodes and bare `saf_comp` — architecture is decision-record prose, not itself a testable shall statement. |
| SC-ISO-04 | traceability_upward | mechanized | req-layer: carries a `refines` link satisfying its scope's rule (`saf_glob_req-must-refine` / `saf_feat_req-must-refine` / `saf_comp_req-must-refine`). arc-layer: carries a `fulfils` link satisfying its scope's rule (`saf_glob_arc-must-fulfil` / `saf_feat_arc-must-fulfil` / `saf_comp_arc-must-fulfil`) **and** at least one incoming `mitigates` link from a same-scope `saf_*_req`, satisfying `saf_arc-must-have-incoming-mitigates`. Cite the `fulfils` half and the `mitigates` half as separate findings if only one holds. |
| SC-ISO-05 | atomicity | mechanized, req-layer only | Content contains exactly one `shall`/`shall not` sentence (ordinary requirement) or exactly one declarative sentence with zero `shall` (AoU-shaped requirement) — never both shapes mixed in one node, never a second bundled mandate. Record `result: null` for arc-layer nodes and bare `saf_comp`. |
| SC-ISO-06 | unambiguity | subjective, 0–3 | 3 = the mandate/decision admits exactly one reading; 0 = the text equally supports multiple materially different readings. |
| SC-ISO-07 | comprehensibility | subjective, 0–3 | 3 = a reviewer holding only this node and its linked parent(s) — no drafting-session context — can state what is mandated/decided; 0 = the node is unintelligible without outside context. |
| SC-ISO-08 | feasibility | subjective, 0–3 | 3 = clearly realizable against the linked parent architecture (or, for an AoU-shaped req, against the assumption's real operating context); 0 = infeasible or self-contradictory. |

## Emitting a finding

One finding per indicator, in the same shape for both mechanized and
subjective rows: the indicator `ID`/`name`, a `pass`/`fail` (mechanized) or
`0`–`3` score (subjective), and a one-line justification citing the concrete
field, link, or rule id the judgement rests on. Use `null` (not a score) only
where this table says an indicator does not apply to the target's layer.
