<!-- @needs sme_layer_req skill file — requirement layer craft-expert, prd_unit_imp__thalam__sme_layer_req, prd_unit_imp, [prd_unit_des__thalam__sme_layer_req], proposed -->

# sme_layer_req — Requirement Layer Craft-Expert (RFC 2119 mandate register)

**Load trigger:** layer-expert branch resolves the target layer to `req`, for any enabler and scope.
**References:** ISO/IEC/IEEE 29148 atomicity rule; ISO/IEC Directives Part 2 §7.1 modal verbs

---

## Authoring guidance

**Dos**
- Exactly one `shall` or `shall not` per node (atomicity rule — one observable obligation, testable independently).
- State *what* is required, not *how* it is realized.
- Make the pass/fail criterion derivable from the statement alone.
- Use `shall` for binding obligations; `should` for recommendations; `may` for permissions — never `will`, `must`, or imperative mood.

**Don'ts**
- No implementation detail (algorithm, data structure, library name) — those belong at `arc` or `des`.
- No multiple obligations in one node (`X shall do A, and X shall do B` → two nodes).
- No rationale or motivation (belongs in the parent `int`).
- No re-statement of the parent `int`'s text (`refines` is the link; text redundancy is noise).

---

## Review checklist

Apply each indicator when critique reviews a `req` node. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

| # | Indicator | Type |
|---|-----------|------|
| L-R-1 | Exactly one `shall`/`shall not` — no compound obligation | pass/fail |
| L-R-2 | Uses `shall`/`should`/`may` correctly — never `will`/`must`/imperative | pass/fail |
| L-R-3 | No implementation detail (algorithm, library, data structure) | pass/fail |
| L-R-4 | No restatement of the parent `int`'s text | pass/fail |
| L-R-5 | Pass/fail criterion derivable from the statement alone | 0–3 |
