<!-- @needs sme_scope_unit skill file — unit scope judgement expert, prd_unit_imp__thalam__sme_scope_unit, prd_unit_imp, [prd_unit_des__thalam__sme_scope_unit], proposed -->

# sme_scope_unit — Unit Scope Judgement Expert (realization-choice grain)

**Load trigger:** scope-expert branch 3 resolves the target point's scope to `unit`. This is every `des` and `imp` point without exception — those two layers are always unit scope — and it is the only scope at which a concrete artifact is named.

---

## Authoring guidance

At `unit` scope the judgement is **realization choice**: which concrete artifact realizes the thing, and where it lives. Every scope above this one relates children to each other; this one has no children to relate. That inversion is what makes unit scope distinctive, and it drives every check below.

A `unit_des` is judged against three obligations:

- **One artifact.** It names exactly one realizable thing — one file, one function, one script, one document, one folder descriptor — with its concrete path. A `unit_des` naming two artifacts is over-scoped: it is a `comp_arc` that lost its diagram. Split it.
- **A location, committed.** The path is stated, not implied. "the scanner configuration" is not a location; `needs/conf.py`'s `src_trace_projects` entry is. A `unit_des` that commits to no location cannot be drifted against, and drift detection is what the layer exists for.
- **The mechanism, not the obligation.** It says *how* the thing works. Obligations live at `req`, decisions at `arc`. A `unit_des` restating its parent's shall has described nothing.

**Diagrams are conditional here, unlike at every scope above.** A unit has no constituent children, so there is nothing for a structural diagram to relate, and demanding one produces a box with the file name in it. Require a diagram only where the unit's *internal* control or data flow is itself non-trivial — a multi-branch algorithm, a state machine, an ordered protocol exchange. A single function with a linear body needs prose, not a picture. This is the one place where `sme_layer_arc`'s "the diagram IS the architecture" mandate does not reach, because `arc` and `unit` never coincide.

Two failures specific to this grain:

- **The plural body.** "This design covers the three scanner entries" — three artifacts, one node, no way for any of them to be drifted against individually. The `des`-to-`imp` marker relation is one-to-one for a reason.
- **The floating unit.** A `unit_des` whose `:implements:` names no `comp_req`, only a `:fulfils:` to an arc. The arc path is the architectural side-branch; the direct implements link is the traceability chain, and axon enforces it at every status from draft upward.

For `imp` points the artifact is not authored but *scanned* — a codelinks marker in a real source file mints it. The judgement at unit scope there is whether the marker sits in the file the corresponding `unit_des` committed to. A marker in a different file than its design named is drift, not a variant.

---

## Marker syntax reference

At `imp` points the artifact is scanned, not authored, so judging one means
knowing what a marker looks like in that file's language and where the file is
allowed to live. This table is the current per-language reference; each row's
normative source is the matching `prd_comp_req__main__code_traceability_*`
requirement, and none of them is restated here.

| Language | Extensions | Comment lead-in | Terminator |
|---|---|---|---|
| Bash and compatible shells | `.sh`, `.bash`, `.zsh`, `.ksh` | `#` | end of line |
| C | `.c`, `.h` | `//` | end of line |
| C++ | `.cpp`, `.hpp`, `.cc`, `.hh` | `//` | end of line |
| Markdown / MyST | `.md` | `<!--` | `-->` |
| Python | `.py` | `#` | end of line |
| Rust | `.rs` | `//` | end of line |
| TOML | `.toml` | `#` | end of line |
| TypeScript | `.ts`, `.tsx` | `//` | end of line |

Markdown is the only row that closes its comment rather than ending at the
newline: `needs/conf.py` sets an explicit end sequence for it, because
tree-sitter-markdown's `html_block` node includes the delimiters. TypeScript
carries a second trap — the scanner selects the TSX grammar for `.tsx` only,
and a `.ts` file parsed as TSX silently drops markers after a legacy
angle-bracket type assertion, so the scan comes back clean rather than failing.

**Directories.** A folder carries no code and so no marker of its own. It is
anchored by a git-tracked `.folder` dotfile using the `#` comment character,
carrying exactly one marker and no executable logic.

**Not a marker.** `[#qik-<cluster> <command>]` is an inline directive to the
crawler, not a traceability marker. It is listed here precisely because it is
the construct most often mistaken for one; it mints nothing and links nothing.

**Placement.** Knowing the syntax is half the judgement. A marker-bearing file
must also sit where the canonical folder layout permits — that is what turns
indicator S-U-5 from a syntax check into a placement check. A correctly formed
marker in a file the layout does not admit is still a finding.

> **This file is itself a scan target.** `needs/conf.py` scans `.claude/agents/`
> recursively with markdown comment handling and no include filter, so this
> checklist is read by the scanner like any source file. The table above gives
> lead-ins and extensions only, never a filled-in payload with a real id — a
> complete example written here would mint a phantom need rather than
> illustrate one. Keep it that way when you extend the table.

## Review checklist

Apply alongside `sme_layer_des`'s checklist when critique reviews a `unit_des` node, and alongside the enabler expert for the concern the artifact belongs to. Emit **pass/fail** for mechanizable, **0–3 score + justification** for subjective.

| # | Indicator | Type |
|---|-----------|------|
| S-U-1 | Names exactly one realizable artifact — not two, not a family | pass/fail |
| S-U-2 | States that artifact's concrete path, not a description of it | pass/fail |
| S-U-3 | Carries a direct `:implements:` to a `comp_req`, not only a `:fulfils:` to an arc | pass/fail |
| S-U-4 | Diagram present if and only if the unit's internal flow is non-trivial — no box-per-filename diagrams | pass/fail |
| S-U-5 | For an `imp` point: the scanned marker sits in the file its `unit_des` committed to | pass/fail |
| S-U-6 | States the mechanism rather than restating the parent's obligation | 0–3 |
| S-U-7 | Granularity is appropriate for unit scope — the artifact is small enough to be drifted against as one thing | 0–3 |
