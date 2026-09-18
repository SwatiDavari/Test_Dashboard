<!-- @needs sme_scope_comp skill file — component scope judgement expert, prd_unit_imp__thalam__sme_scope_comp, prd_unit_imp, [prd_unit_des__thalam__sme_scope_comp], proposed -->

# sme_scope_comp — Component Scope Judgement Expert (structural-decomposition grain)

**Load trigger:** scope-expert branch 3 resolves the target point's scope to `comp` (only on `int`/`req`/`arc` layers of `prd_`/`tst_`/`bld_`/`doc_` — `des`/`imp` are always `unit` scope, `sys_` is always `glob`).

---

## Authoring guidance

At `comp` scope, an architecture element (`comp_arc`) is judged at the structural-decomposition grain — concretely, against two obligations:

- It must relate its constituent `unit`-level elements to each other via a structural diagram (what units compose the component).
- It must show comp-level flows — unit-to-unit interactions, or interactions with external actors or interfaces — via a sequence or MSC diagram, wherever such flows exist.

This is distinct from the layer-expert's generic "arc needs a diagram" mandate (`sme_layer_arc`), which does not know which grain of child element is being related — the layer-expert judges *that* a diagram exists and is congruent with the prose; this scope-expert judges *which* children the diagram must relate.

A `comp_arc` whose body narrates multiple named sub-components as prose without a matching structural diagram (or without those sub-components existing as separate downstream `unit_des` nodes) is under-decomposed at this scope — apply `sme_layer_arc`'s diagram-prose congruence check together with this scope-expert's structural-diagram-relates-units obligation to catch it.

**Lateral links stay inside the cluster at this scope.** The project's
`.qik/axon/classify.toml` declares its own link vocabulary and an optional
topology per link kind; read the `hint` text of each
declared `[[link]]`/`[[topology]]` entry to judge, semantically, which
declared kind (if any) reads as a lateral / symmetric / see-also relation
between otherwise-unrelated derivation chains — this is a judgement call
from the hint's own wording, never a fixed name to grep for, since a
project is free to call it anything. `classify.toml` separately declares
the project's cluster axis (its component/cluster grouping) the same way.
A node being authored or reviewed at `comp` scope should carry a lateral
link only to another need in the *same* cluster. A comp-scope lateral link
reaching into a different cluster is a smell, not a violation to silently
accept: the correspondence it expresses almost always already holds one
scope up, between the two clusters' matching capabilities, and restating
it per component pair multiplies combinatorially as both clusters grow.
Recommend moving it to feat scope (see `sme_scope_feat`) rather than
leaving it here.

---

## Review checklist

Apply alongside `sme_layer_arc`'s checklist when critique reviews a `comp_arc` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

| # | Indicator | Type |
|---|-----------|------|
| S-C-1 | Structural diagram relates the comp's constituent `unit`-level elements to each other | pass/fail |
| S-C-2 | Sequence/MSC diagram present wherever unit-to-unit or external-interface flows exist | pass/fail |
| S-C-3 | Granularity of the unit breakdown is appropriate for component scope (not over- or under-decomposed) | 0–3 |
| S-C-4 | Any classify.toml-declared lateral link (judged from its own `hint`, not a fixed name) present on this node targets a need in the same cluster — a cross-cluster instance is flagged with a recommendation to state it once at feat scope instead | pass/fail |
