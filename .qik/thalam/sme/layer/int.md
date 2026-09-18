<!-- @needs sme_layer_int skill file — intent layer craft-expert, prd_unit_imp__thalam__sme_layer_int, prd_unit_imp, [prd_unit_des__thalam__sme_layer_int], proposed -->

# sme_layer_int — Intent Layer Craft-Expert (conviction-and-purpose register)

**Load trigger:** layer-expert branch resolves the target layer to `int` — invoked only on explicit request, independent of enabler and scope.
**Reference:** ISO/IEC/IEEE 15288 Mission Analysis

---

## Authoring guidance

**Dos**
- State the pain or stake in present-tense indicative: "The project cannot trace a change request to the affected code without manual search."
- Name the value delivered to a named actor or to the system goal.
- Use active voice; be concrete about the domain, vague about the solution.
- One purpose per node.

**Don'ts**
- No `shall`/`should`/`may` (RFC 2119 keywords signal a requirement, not an intent — reclassify the node).
- No mechanism, tool, or architecture name.
- No how — the intent states *why*, the `req` and `arc` layers state *what* and *how*.

---

## Review checklist

Apply each indicator when critique reviews an `int` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

| # | Indicator | Type |
|---|-----------|------|
| L-I-1 | No RFC 2119 keyword (`shall`/`should`/`may`) present | pass/fail |
| L-I-2 | Names no mechanism, tool, or architecture | pass/fail |
| L-I-3 | States the pain/stake in present-tense indicative | 0–3 |
| L-I-4 | Names the value delivered to a named actor or system goal | 0–3 |
| L-I-5 | Single purpose (not a bundle of concerns) | 0–3 |
