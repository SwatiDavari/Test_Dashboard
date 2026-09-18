<!-- @needs sme_layer_arc skill file — architecture layer craft-expert, prd_unit_imp__thalam__sme_layer_arc, prd_unit_imp, [prd_unit_des__thalam__sme_layer_arc], proposed -->

# sme_layer_arc — Architecture Layer Craft-Expert (elements + viewpoints register)

**Load trigger:** layer-expert branch resolves the target layer to `arc`, for any enabler and scope. Composes alongside the scope-expert (`sme_scope_glob`/`_feat`/`_comp`/`_unit`), which judges *which grain of child* an arc element must relate — this register only judges *that* an arc element carries the right viewpoints and states a decision, not which grain.
**References:** ISO/IEC/IEEE 42010 (elements, relationships, viewpoints); ISO/IEC/IEEE 15288 §6.4.4 and 12207 §6.4.4 (Architecture Definition — both delegate description technique to 42010); the project's own content-shape mandate is `sys_req__concept__arc_content_shape`.
**Content:** an element list, plus up to three viewpoints — structural (always present), behavioral, and physical/geometric (both conditional, "where applicable") — plus, where a real decision was made (technology, protocol, pattern), the decision context, selected option, and rejected alternatives.

---

## Authoring guidance

**Dos**
- List the elements within the architecture's scope. Each element is separately obligated by its own requirement elsewhere in the graph — name it and place it in context here, don't restate its obligation.
- Include a structural diagram (component, class, or block) — the diagram IS the architecture, not an illustration of it. Always present, not conditional.
- Include a behavioral diagram (any of UML's Interaction-diagram family — sequence, communication, timing, interaction-overview — or an activity diagram for algorithmic flow) whenever the elements have a non-trivial interaction to show. Conditional, but on equal footing with the structural diagram when it applies — not a should-level extra.
- Include a physical/geometric diagram (UML deployment diagram, or an equivalent SysML-style physical/block diagram) whenever the elements have a real spatial or hardware allocation to show (which board, ECU, enclosure, or deployment target). Conditional — most software-only elements have nothing to show here; hardware-adjacent or deployment-relevant elements do.
- Keep every diagram congruent with the prose: when the element's body names N distinct mechanisms or sub-components, the structural diagram shows N corresponding nodes, or the gap is explicitly deferred in the arc's own text.
- Where a real technology or design choice was made, state it explicitly and document the rejected alternatives with the reason for rejection (traceability for future change analysis) — this is secondary content, in service of the elements and their viewpoints, not the node's primary subject.
- Fulfil every parent `req` node explicitly via `:fulfils:`. Fulfilling several requirement nodes at once is the expected, common case — the architecture layer exists to give structurally-coupled requirements one shared place — not a bundling defect. The test for bundling is whether the fulfilled requirements share genuine structural coupling (the same elements and relationships), not how many `:fulfils:` links the node carries.
- Count mechanisms: when the element's body names N distinct realized mechanisms or artifacts (e.g. "a glossary document, cross-referenced by every other document" names two — the document and the cross-reference scheme), each named mechanism either has its own downstream `unit_des` or is explicitly deferred in the element's own text. The `arc-must-have-downstream-des` mechanized rule only requires *at least one* downstream `unit_des`, so an element naming several mechanisms with only one designed passes mechanized checking while remaining genuinely incomplete.

**Don'ts**
- No shall-clauses (the arc is a decision, not an obligation — obligations live at `req`).
- No implementation code or pseudocode.
- No vague "good design" assertions without rationale.
- No structural scope creep: one arc element covers one component's structure, not the whole module.
- No bundling requirements that lack genuine structural coupling under one architecture merely for authoring convenience.

---

## Review checklist

Apply each indicator when critique reviews an `arc` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective. Apply alongside the matching `sme_scope_*` checklist, which judges which grain of child the diagrams must relate.

| # | Indicator | Type |
|---|-----------|------|
| L-C-1 | Element list present, each element traceable to its own separate obligation | pass/fail |
| L-C-2 | Structural diagram present (component/class/block) — always required | pass/fail |
| L-C-3 | Behavioral diagram present whenever elements have a non-trivial interaction to show | pass/fail |
| L-C-4 | Physical/geometric diagram present whenever elements have a real spatial/hardware allocation to show | pass/fail |
| L-C-5 | Diagram-prose congruence: diagram node count matches N mechanisms/sub-components named in prose, or the gap is explicitly deferred in the text | pass/fail |
| L-C-6 | Count mechanisms: each named mechanism has its own downstream `unit_des`, or is explicitly deferred in the text | pass/fail |
| L-C-7 | Fulfils every parent `req` node via `:fulfils:`; multiple targets only flagged if they lack genuine structural coupling | pass/fail |
| L-C-8 | No shall-clauses; no implementation code | pass/fail |
| L-C-9 | Rejected alternatives documented with rationale, where a real decision was made | 0–3 |
