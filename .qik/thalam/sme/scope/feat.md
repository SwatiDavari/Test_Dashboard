<!-- @needs sme_scope_feat skill file — feature scope judgement expert, prd_unit_imp__thalam__sme_scope_feat, prd_unit_imp, [prd_unit_des__thalam__sme_scope_feat], proposed -->

# sme_scope_feat — Feature Scope Judgement Expert (behavior-fulfilment grain)

**Load trigger:** scope-expert branch 3 resolves the target point's scope to `feat` (only on `int`/`req`/`arc` layers of `prd_`/`tst_`/`bld_`/`doc_` — `des`/`imp` are always `unit` scope, `sys_` is always `glob`).

---

## Authoring guidance

At `feat` scope, an architecture element (`feat_arc`) is judged at the behavior-fulfilment grain — concretely, against two obligations:

- It must relate its constituent `comp`-level elements to each other via a component or structural diagram (composition, dependency — what the feature is made of).
- It must show the significant cross-component flows via a sequence or MSC diagram, wherever such flows exist.

This is distinct from the layer-expert's generic "arc needs a diagram" mandate (`sme_layer_arc`), which does not know which grain of child element is being related — the layer-expert judges *that* a diagram exists and is congruent with the prose; this scope-expert judges *which* children the diagram must relate.

**Feat scope is where a cross-cluster lateral link belongs.** Read
`.qik/axon/classify.toml`'s declared `[[link]]`/`[[topology]]` `hint` text
to judge, semantically, which declared link kind (if any) reads as a
lateral / symmetric / see-also relation — never a fixed name, a project is
free to call it anything — and likewise read the same file's own cluster
axis rather than assuming fixed cluster names. When two different
clusters' capabilities genuinely correspond (both expose the same kind of
operation through their own component-level realizations), state that
correspondence once here, between the two feat-level nodes — not once per
component pair underneath, which is exactly what `sme_scope_comp`'s own
check exists to catch and redirect up here.

---

## Review checklist

Apply alongside `sme_layer_arc`'s checklist when critique reviews a `feat_arc` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

| # | Indicator | Type |
|---|-----------|------|
| S-F-1 | Structural diagram relates the feat's constituent `comp`-level elements to each other | pass/fail |
| S-F-2 | Sequence/MSC diagram present wherever significant cross-component flows exist | pass/fail |
| S-F-3 | Granularity of the component breakdown is appropriate for feature scope (not over- or under-decomposed) | 0–3 |
