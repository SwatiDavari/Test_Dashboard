<!-- @needs sme_layer_des skill file — design layer craft-expert, prd_unit_imp__thalam__sme_layer_des, prd_unit_imp, [prd_unit_des__thalam__sme_layer_des], proposed -->

# sme_layer_des — Design Layer Craft-Expert (technical realization register)

**Load trigger:** layer-expert branch resolves the target layer to `des` — scope is always `unit` at this layer, for any enabler.
**Content:** unit-level technical realization, enabler-calibrated, never the implementation itself.

---

## Authoring guidance

**Dos**
- State the realization choice in technical terms: data layout, algorithm steps, state transitions, error paths, performance contracts.
- Fulfil the parent `arc` node via `:fulfils:` link; also fulfil a `comp_req` directly when no `arc` layer exists.
- Calibrate prescriptiveness by enabler: a `tst_unit_des` may be detailed enough to approach an executable test specification; a `prd_unit_des` stays a decision record.
- Scope is always `unit` at this layer — no other scope is valid.

**Don'ts**
- No implementation code (the design is not the source file; `unit_imp` is).
- No architectural decisions (component selection, protocol choice) — those are `arc`.
- No requirement language (`shall`) — the design decides, it does not mandate.
- No rationale inflation: one concrete design decision per node, not a survey of every option considered.

---

## Review checklist

Apply each indicator when critique reviews a `des` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

| # | Indicator | Type |
|---|-----------|------|
| L-D-1 | States realization in concrete technical terms (data layout/algorithm/state/error path) | pass/fail |
| L-D-2 | Fulfils parent `arc` (or `comp_req` when no `arc` layer exists) via link | pass/fail |
| L-D-3 | Scope is `unit` | pass/fail |
| L-D-4 | No implementation code, no `shall`-language | pass/fail |
| L-D-5 | Implementable/testable without further questions | 0–3 |
