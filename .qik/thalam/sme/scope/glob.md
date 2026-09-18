<!-- @needs sme_scope_glob skill file — global scope judgement expert, prd_unit_imp__thalam__sme_scope_glob, prd_unit_imp, [prd_unit_des__thalam__sme_scope_glob], proposed -->

# sme_scope_glob — Global Scope Judgement Expert (feature-decomposition grain)

**Load trigger:** scope-expert branch 3 resolves the target point's scope to `glob` — every `sys_` point, since `sys_` carries no scope qualifier and is always global, plus the `glob` points of `prd_`/`tst_`/`bld_`/`doc_` on the `int`/`req`/`arc` layers (`des`/`imp` are always `unit` scope).

---

## Authoring guidance

At `glob` scope the judgement is **feature-decomposition**: which parts realize the mission. This is the widest grain in the model, and its characteristic failure is not vagueness but *premature descent* — a global element that starts naming components has stopped answering "which features does this system have" and started answering "how is one of them built".

A `glob_arc` is judged against two obligations:

- It relates its constituent **`feat`-level** elements to each other via a structural diagram — which features compose the system or the module, and how they stand to one another. Not components. Not units.
- It shows system-level flows via a sequence or MSC diagram wherever a flow crosses feature boundaries or reaches an external actor. A flow entirely inside one feature belongs to that feature's own `feat_arc`, not here.

For a `sys_arc`, the constituents are the mission-level intents and the enabling systems, not features of one module — the same grain rule applied one level up, since `sys_` is the mission level.

Two asymmetries worth naming, because they are the ones authors get wrong:

- **A `glob` element may legitimately have no sibling.** A module with one feature still has a global scope; the structural diagram then relates that one feature to the module boundary and to whatever is external. An author who deletes the diagram because "there is only one box" has removed the boundary statement, which was the point.
- **Completeness at `glob` is exhaustiveness, not depth.** The global element's obligation is that every feature the system has appears — a missing feature is a defect, an undetailed one is not. Depth is the `feat` expert's concern.

Where `glob` meets the enabler axis: the enabling systems (`prd_`/`tst_`/`doc_`/`bld_`/`saf_`/`sec_`) each carry their own global point, and each answers the same question for its own concern. A `tst_glob_arc` relates test features, not product features. Do not let a global element of one enabler enumerate another's.

---

## Review checklist

Apply alongside `sme_layer_arc`'s checklist when critique reviews a `glob_arc` or `sys_arc` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

| # | Indicator | Type |
|---|-----------|------|
| S-G-1 | Structural diagram relates the point's constituent `feat`-level elements (for `sys_`: mission-level intents and enabling systems) — not `comp`- or `unit`-level ones | pass/fail |
| S-G-2 | Sequence/MSC diagram present wherever a flow crosses feature boundaries or reaches an external actor | pass/fail |
| S-G-3 | No premature descent: the body names no component- or unit-level artifact as a constituent | pass/fail |
| S-G-4 | Exhaustive at its own grain: every feature the system has appears, or its absence is explicitly deferred in the text | pass/fail |
| S-G-5 | Enabler-pure: the element enumerates only its own enabling system's features | pass/fail |
| S-G-6 | Feature breakdown is appropriate for global scope — neither one undifferentiated block nor a component list wearing feature names | 0–3 |
