# qik nexus process — CR orchestration procedure

<!-- @needs nexus process procedure (Claude Code), prd_unit_imp__nexus__process_procedure_claude, prd_unit_imp, [prd_unit_des__nexus__process_procedure_claude], released -->
Executed by the **qik-nexus** persona (Lifecycle Steward).

## When to invoke

When a user says "work cr-NNNNNN", "bearbeite cr-NNNNNN", or equivalent. You
own the **complete sequence below**. Every step is mandatory. Never skip,
never reorder. The rationale for each step is stated — know it, because the
rationale is the guard that tells you whether a shortcut is safe (it never
is).

This procedure is identical in substance to the Copilot surface
(`.github/prompts/qik-nexus-process.prompt.md`) — the 17-step CR orchestration
is inlined here in full rather than referenced, so a Claude Code agent never
has to load a second file mid-CR to find the actual steps. The release-cut and
PI-close procedure, the release-notes preview, the branch-hierarchy note, the
issue-driven ("mach issue #N") workflow and its tracker commands, test and doc
dispatch, the pi-entry link edge, the stored-progress-vs-derived-coverage
distinction, the 3D tag-naming schema, and the orchestrator's own meta-rules
are all inlined further below in this same file — this is the full list of
sections named in the original porting gap plus the "Link" and "Progress is
stored" pair found missing during closure review. You never need to open
the Copilot prompt mid-CR to find one of these sections missing.

Step 4's ID-derivation fallback below names the
`{enabler}_{scope}_{layer}__{cluster}__{description}` schema — see "Tag naming
schema" further down in this file for the full definition. That reference is
no longer a pointer to the Copilot file; it resolves within this document.

<!-- @needs nexus MCP-unavailable CLI fallback (Claude Code), prd_unit_imp__nexus__mcp_cli_fallback_claude, prd_unit_imp, [prd_unit_des__nexus__mcp_cli_fallback_claude], released -->
## When `mcp__qik__*` tools are unavailable

Every step below is written as an `mcp__qik__*` tool call. If the qik MCP
server has not connected this session (check for an `mcp__qik__*` tool in
your tool list; a connection failure is reported at session start, not
silently), **every one of those calls has a CLI equivalent** — the MCP tools
are a thin wrapper over the same binary, never a separate implementation.
Substitute:

```
mcp__qik__nexus_X(args...)   →  qik nexus X <args> --no-color
mcp__qik__axon_X(args...)    →  qik axon X <args> --no-color
mcp__qik__cortex_X(args...)  →  qik cortex X <args> --no-color
```

That table shows the shape, not the exact syntax — the MCP tool's named
arguments map to three different CLI shapes depending on the command, so
translate the argument, not just the verb: `nexus_list(stage="pi")` is a
positional argument (`qik nexus list pi`); `cortex_check(kind="algo")` is a
flag (`qik cortex check --kind algo`); `nexus_link(id, [A, B])` is variadic,
space-separated, no brackets (`qik nexus link <id> A B`). Check `qik <context>
<verb> --help` when unsure rather than guessing the shape under pressure —
that is exactly the situation (MCP down, working from memory) most likely to
produce a wrong command that looks right.

Always pass `--no-color` when parsing output yourself; use `--mcp` instead
when you want the same structured JSON the MCP tool would have returned.

**Never substitute a build artifact for the installed binary** — in this
workspace, `prod/rust/target/release/qik` or `prod/rust/target/debug/qik`.
A session working from the raw build output can silently diverge from the
version everyone else's tools resolve to. Use the actually
installed binary: on PATH if `qik --version` resolves, otherwise the VS Code
extension's host bundle
(`~/.vscode-server/data/User/globalStorage/qorix.qik-vscode/bin/qik` or the
platform-equivalent `globalStorage` path) or the Claude Code plugin's
(`~/.claude/plugins/qik/bin/qik`) — whichever this project installs through.

This substitution is not a degraded fallback to apologize for. It is the same
tool through a different door, and skipping a step because its MCP form
happened to be unreachable is not acceptable — the CLI form is exactly as
authoritative.

---

<!-- @needs nexus CR orchestration — 17-step lifecycle workflow (Claude Code), prd_unit_imp__nexus__cr_orchestration_claude, prd_unit_imp, [prd_unit_des__nexus__cr_orchestration], released -->
### Working a PI CR — the 17-step orchestration

---

**Step 1 — Identify: `nexus_list pi`**

*Ratio: Before touching a specific CR, survey the full PI to understand what
else is in flight. The CR you are about to work may depend on or be blocked by
another item. The overview prevents surprises mid-way.*

`nexus_list(stage="pi")`. Note which items are `open`, `wip`, `validate`,
`complete`. Confirm the named CR is present.

---

**Step 2 — Understand: `nexus_show` + reasoning**

*Ratio: Scope must be understood completely before any file is touched. Acting
on a partial reading of a CR is the primary source of wrong implementations and
traceability gaps. Ambiguity resolved now costs nothing; ambiguity discovered
mid-implementation costs a rollback.*

`nexus_show(id)`. Read every field: `headline`, `what`, `why`, `change`,
`needs`, `stage`, `progress`. Summarize the CR scope in your own words before
proceeding. If `what` or `why` is ambiguous, ask the user to clarify — do not
guess.

**Stage guard (run before anything else):**
- `backlog` → warn: "cr-NNNNNN is not yet in PI. Promote to pi first?" Wait.
  If yes, `nexus_promote` until `pi`; if no, stop.
- `staged` → warn: "cr-NNNNNN is already staged. Work it again, or just a
  status update?" If rework: `nexus_demote` to `pi` first.
- `released` → warn: "cr-NNNNNN is terminal. Create a follow-up CR?" Do NOT
  demote released entries.
- `pi` or `idea` → proceed.

---

**Step 3 — Mark wip: `nexus_advance` (open → wip)**

*Ratio: `wip` is a checkpoint marker that makes active work visible and creates
an audit trail. Setting it before any file change ensures the store always
reflects reality — if work is interrupted, the CR stays `wip` and is not
silently abandoned at `open`. It also commits you: a CR in `wip` has a known
owner and start point. Do this before any file is touched, before any
traceability query, before any design decision.*

`nexus_advance(id)` — moves from `open` to `wip`. This is the first write.

Also check for a linked GitHub issue. If no `nexus_ref` with `what="github"`
exists on this CR:
- `git remote get-url origin` → derive `<owner>/<repo>`.
- Look for an open issue whose title closely matches the CR headline (via the
  project's configured GitHub integration, or `nexus pull` if connected).
- If found: `nexus_ref(id, what="github", where=<issue.html_url>)` — attach
  silently; report the match to the user.
- If not found: continue without creating one. Do not create GitHub issues
  from nexus.

---

**Step 4 — Find the need entry-point: `axon_list` → `axon_show`**

*Ratio: The entry-point need is the node in the artifact graph where this CR
anchors. Without it the CR is invisible to axon — no blast, no impact, no
traceability. Choosing the right tier (int/req/arc/des/imp) determines the
blast radius: too high creates artificially wide scope; too low leaves the
upstream chain dangling. The search follows a narrowing strategy — cluster
first, so the cheapest, most precise query runs first.*

Search strategy (in order — stop as soon as a match is confirmed):

1. **By cluster:** `axon_list(cluster=<X>)` where `<X>` is derived from the
   CR topic (CR about nexus store → `nexus`; about axon rules → `axon`; about
   CLI → `main`; etc.). Inspect returned IDs; call `axon_show` on candidates
   to confirm content matches the CR scope.
2. **Full list:** `axon_list()` — no cluster filter. Browse broadly; filter by
   ID pattern (`prd_comp_req__`, `prd_feat_int__`, etc.) matching the CR scope.
3. **Last resort — structural derivation:** From the CR's `what` text, derive
   a candidate ID using the naming schema
   `{enabler}_{scope}_{layer}__{cluster}__{description}`. Only attempt this if
   steps 1–2 returned no match. If IDs follow the schema a structural search
   should succeed; free-text reasoning is a fallback, not a first resort.

---

**Step 5 — Anchor the entry-point: `nexus_link` or `qik-thalam-author` + link**

*Ratio: `nexus_link` is the single edge from the lifecycle store into the
traceability graph. Once set, `axon_blast` can compute the full impact cone from
the CR. The link is also the audit record of which artifact the CR was
targeting. Without this link the CR is invisible to axon — step 6 cannot run.
The link must be set before any blast.*

**Coverage gate (cr_type) — run before anchoring, not after.** This is the
fix for the eager-implementation failure mode: an agent finding *some*
existing des/imp node loosely related to the CR's topic in Step 4, linking
it, and jumping straight into Step 8's code-only path without ever checking
whether a req/int node actually covers the new capability. Check `cr_type`
(from Step 2's `nexus_show`):

- **`feature` / `improvement`** → the Step 4 entry-point qualifies only if it
  IS a `req`/`int` node, or `axon_trace` from it reaches one whose content
  already covers the CR's `what`. An `arc`/`des`/`imp` node alone describes
  *how*, never *whether the capability is meant to exist*, and cannot satisfy
  this gate. If no such req/int coverage exists, invoke **qik-thalam-author**
  now to draft the missing node(s) — never defer needs-authoring to "after
  the code works."
- **`bug`** (and any CR with no code-behavior implication) → exempt. An
  existing des/imp entry-point is sufficient, since the requirement itself is
  presumed correct and only its realization is being fixed.

Once the gate is satisfied:

- **Entry-point exists** → `nexus_link(id, [NEED_ID])` immediately.
- **Entry-point does not exist** → hand authoring to **qik-thalam-author**:
  - Analyze the CR: derive enabler (`prd`/`tst`/`doc`), scope
    (`glob`/`feat`/`comp`/`unit`), layer (`int`/`req`/`arc`/`des`/`imp`).
  - qik-thalam-author drafts the need at `status: proposed`. It also sets the
    internal needs-graph links (`refines`, `satisfies`) so the new need
    is not an orphan.
  - Once thalam reports the new ID: `nexus_link(id, [NEW_NEED_ID])`.

---

**Step 6 — Determine blast radius: `axon_blast` + outcome-wave reasoning**

*Ratio: `axon_blast` gives the algorithmic facts — what the graph contains and
how it is connected. Outcome-wave reasoning gives the normative scope — what the
graph *should* contain given the CR's intent. Running the blast first means the
reasoning is grounded in concrete node IDs and file locations, not in abstractions.
The two together define the complete work scope: blast catches what exists, reasoning
catches what is missing.*

**This step is not optional when MCP is down.** `axon_blast` has a CLI form —
`qik axon blast <ENTRY_POINT_NEED_ID> --no-color` — that returns the identical
result. There is no version of this procedure where blast radius is skipped
because the MCP tool happened to be unreachable; skipping it means every
downstream step (7 onward) works from an unverified guess of what the graph
contains, which is the exact failure this step exists to prevent.

### 6a — Run `axon_blast` in topology stages (collect facts first)

**Never hardcode topology value names in this procedure or in your own
reasoning about it** — `.qik/axon/classify.toml`'s `[[topology]]` values
are free, project-declared vocabulary, not a fixed enum. This
project happens to declare `primary`/`secondary`/`peer`, used below only as
concrete illustration; a different qik project may name and count them
differently. Always discover the actual set, never assume it.

**i — Discover this project's stages.** `axon_topology()` (CLI
`qik axon topology --no-color`). Returns every declared value in file
order — which **is** the stage priority (see the tool's own description
and `.qik/axon/classify.toml`'s header comment): the `default: true`
entries, in the order returned, are mandatory stages, first one highest
priority; the `default: false` entries are a single final audit pass, no
internal ordering. In this project that resolves to two mandatory stages
(`primary`, then `secondary`) and one audit stage (`peer`) — a project with
only one default topology has one mandatory stage; a project with none has
none, and the whole staging below collapses to a single unfiltered call.

**ii — Work each mandatory stage in order.** For each `default: true`
topology, in the order `axon_topology()` returned:
`axon_blast(ENTRY_POINT_NEED_ID, topology: [<that one stage's name>])`.
Read every returned artifact at its file location — do not guess content
from IDs alone. The first stage (this project's `primary`) is the focused
derivation spine and **MUST** be fully accounted for — every artifact it
returns goes into the todo (Step 7) or is explicitly justified as already
consistent — before moving to the next stage. Later mandatory stages
(this project's `secondary`) still matter but carry more structural/
collector noise (see `prd_comp_req__axon__link_topology`'s rationale); work
them the same way, one stage at a time, not merged into one undifferentiated
list.

Note which enablers appear (`prd_`, `tst_`, `bld_`, `doc_`, …), which layers are
represented, and which layers are absent, per stage. Do not yet interpret
whether absences are gaps or correct omissions — that is Step 6b.

**iii — Audit pass over non-default stages, last.** One combined call:
`axon_blast(ENTRY_POINT_NEED_ID, topology: [<every default:false name>])`
(this project: `topology: ["peer"]`). These are reviewed for awareness, not
automatically added to the todo — a kinship-style neighbor is thematically
related, not a derivation dependency. Fold one into the todo only with an
explicit reason (typically: the CR is itself about relationship/kinship
content, shaped like a peer-topology link). If there are no `default: false` stages,
skip this sub-step — there is nothing to audit.

If MCP is unreachable, every call above has the identical CLI form:
`qik axon topology --no-color` and
`qik axon blast <ENTRY_POINT_NEED_ID> --topology <name>[,<name>...] --no-color`.

### 6b — Outcome-wave reasoning (with blast results in hand)

Read the CR's `what` and `why`. Derive the intended outcome and trace its waves
of consequence across enabling systems. The blast results are now context; use
them to make the reasoning concrete.

**Step 1 — Name the primary outcome.**
State the direct result the CR delivers in one sentence. Name the owning
enabler and the layer:

> "The primary outcome is a behavioral change in the `thalam` agent: it gains
> ISO/IEC/IEEE 15288 vocabulary. Owner: `prd_`. Primary layer: `prd_feat`
> (behavior lives at feature scope)."

A behavioral change → feature layer. A structural change → comp layer. A
whole-system stance → glob layer. A recipe or script → unit layer.

**Step 2 — Propagate the wave across enablers.**
From the primary outcome, reason which enabling systems are **certainly** affected
and what work products they require:

| If the primary outcome is… | Then certainly also… |
|---|---|
| Behavioral change in a component | `prd_feat_*` update; `tst_` test coverage for the new behavior |
| New architectural decision | `prd_comp_arc` or `bld_comp_arc`; `tst_comp_*` design test; `doc_` if user-visible |
| New build capability | `bld_feat_*` and `bld_comp_*`; `doc_` if it affects contributor workflow |
| System-level concept change | `sys_` update; *every* cluster that implements the concept needs `prd_`/`tst_` updates |
| Agent knowledge/behavior change | `prd_feat_*` in that agent's cluster (behavior must be documented at feature scope); `tst_` cases; `doc_` user guide if user-visible |

**Step 3 — Compare reasoning against blast, identify gaps.**
For each enabler and layer combination the wave requires:

- **Blast returned a matching node** → verify it is consistent with the planned
  change; mark "verify or update" in the todo.
- **Wave requires a node the blast did not return** → the node either does not
  exist yet (author it) or is unlinked (link it). Both are explicitly added to
  the todo as `→ thalam-author`.
- **Blast returned a node the wave did not predict** → read it; decide whether
  the wave was incomplete (update the table) or the node is in-scope by existing
  link (add to todo if it needs updating).

A blast that returns no `tst_` nodes when the primary outcome is a behavioral
change is a gap in the graph, not clearance to skip tests. The blast is the
hourglass of what *exists*; the wave reasoning defines what *should* exist.

---

**Step 7 — Build the todo list: top-down order**

*Ratio: Changes must propagate top-down (int → req → arc → des → imp) so that
each layer is internally consistent before the layer below it is touched. A
design written against an unfinished architecture will drift the moment
architecture is corrected. The todo list is a pre-commitment to scope — if a
layer is in the blast radius it must appear in the todo. An incomplete todo is
a blocker; do not write anything until every affected layer is accounted for.*

From the blast-radius results, build an explicit todo list ordered:

```
int (intention)  →  req (requirement)  →  arc (architecture)
→  des (design)  →  imp (implementation)
→  tst (tests, if affected)  →  doc (documentation, if affected)
```

Only list artifacts that actually need to change. Artifacts in the blast radius
that are already consistent with the planned change are marked "verify only".

**Tag every item that creates or modifies a sphinx-needs node with
`→ thalam-author`.** The nexus agent does not write needs content directly —
thalam is the sole authorized author of all needs directives. A todo item
tagged `→ thalam-author` is dispatched to the author agent in Step 8; the
nexus agent never writes the directive inline.

---

<!-- @needs nexus reblast on mutation (Claude Code), prd_unit_imp__nexus__reblast_on_mutation_claude, prd_unit_imp, [prd_unit_des__nexus__reblast_on_mutation], released -->
**Step 8 — Work top-down: change + `axon_impact` after each mutation**

*Ratio: Working strictly top-down ensures upstream consistency at every step.
Running `axon_impact` (downstream only — not blast) after each genuine mutation
catches new artifacts that the initial blast could not have known about: the
mutation may have introduced a new link or changed a contract that propagates
further down. New discoveries go to the **bottom** of the todo, never into the
middle — the top-down order must not be disrupted by late discoveries.*

For each todo item, in order:
1. Read the artifact at its file path.
2. **For needs-node mutations** (items tagged `→ thalam-author` in Step 7): invoke
   **qik-thalam-author** as a subagent. Supply the enabler+point context from
   Step 6: the affected enabler coordinates and type-matrix points. Do not write
   sphinx-needs directives inline under any circumstance — thalam is the sole
   authorized author.
   **For code-only mutations** (no needs nodes involved): make the change directly.
3. If a genuine mutation occurred: `axon_impact(CHANGED_NEED_ID)`. Add any
   newly affected artifacts to the **bottom** of the todo.
4. Do not advance to the next todo item until the current one is consistent.

---

**Step 9 — Implementation last: qik-thalam-author + links to `unit_des`**

*Ratio: `imp` nodes are terminal in the artifact graph — they have no children.
Writing them before the upstream layers are finished leaves the implementation
floating without a coherent design to verify against. This is the primary
source of "code that works but has no traceable requirement". qik-thalam-author is the
only agent authorized to write needs content. The `unit_des → unit_imp` link is
mandatory: without it, axon cannot traverse from design to implementation, and
coverage checks will report the design as "open" regardless of how much code was
written.*

**Hard gate: `unit_des.status` must be `released` before any implementation is
written.** A `unit_des` at `proposed` or `approved` means the design review has
not concluded. Do not write code, do not add `@needs` markers, do not instruct
qik-thalam-author to draft implementation content until the `unit_des` carrying the
design is at `released`. Verify by calling `axon_show(<unit_des_id>)` and
checking the `status` field. If it is not `released`: stop, advance the design
through review, update `status: released` in the `.md` file, rebuild
`needs.json`, and re-verify with `axon_check` before returning to this step.

- All layers from `int` through `des` must be complete, consistent, and at
  `status: released` before this step.
- Invoke **qik-thalam-author** to draft `unit_imp` needs (and the corresponding code
  changes).
- After each `unit_imp` is created: set the link from the new `unit_imp` to
  its parent `unit_des` in the needs graph (via `fulfils` or the schema's
  implementation link field, typically a `@needs` inline marker in the source
  file following the pattern:
  `// @needs <description>, prd_unit_imp__<cluster>__<id>, prd_unit_imp, [prd_unit_des__<cluster>__<id>], released`).

---

**Step 10 — Traceability gate: `axon check`**

*Ratio: `axon_check` is the deterministic, tool-enforced verification that the
graph is coherent — no dangling links, no orphans, no rule violations. It
catches errors the agent cannot see by reading files alone: a link pointing to
a deleted need, a need with no upstream parent, a cycle. This gate runs before
any lifecycle advancement or link reconciliation — fixing graph errors after
advancing the CR wastes a retreat.*

`axon_check()` (or `qik axon check --no-color`). Zero **errors** required.
Warnings that pre-existed before this CR are acceptable; new warnings are not.
A `0 error(s), 0 warning(s)` result on a non-trivial change is itself worth a
second look, not an automatic pass — confirm the rule set actually loaded
(`qik axon rules` should list rules, not fail) before trusting a suspiciously
clean report.

---

**Step 11 — Reconcile CR links: `nexus_link` / `nexus_unlink`**

*Ratio: The link set in step 5 was the entry-point for the blast — a starting
guess, not the final record. After full implementation, the actual set of needs
produced by this CR is known. Updating the CR links now creates the permanent,
machine-readable audit trail of what the CR actually impacted. A future engineer
asking "which CRs touched this need?" finds this CR via `axon_trace` — but only
if the link set is correct and complete. The first link was a means to start
the blast; the final link set is the record of the CR's contribution.*

`nexus_show(id)` — re-read the current `needs` list.
- Add every need authored or significantly changed during implementation:
  `nexus_link(id, [NEED_IDS...])`.
- Remove any entry-point needs that were wrong guesses or are now superseded:
  `nexus_unlink(id, [STALE_NEED_IDS...])`.

---

**Step 12 — Rule gate: `cortex check`**

*Ratio: `cortex_check` applies the project's rule set — naming, structure,
mandatory fields, cross-cutting conventions. It runs after `axon_check` because
structural integrity (axon) must be confirmed before semantic compliance (cortex)
is worth checking: a rule violation in a dangling node is noise. A cortex
violation must be fixed in the code — never by weakening the rule.*

`cortex_check(kind="algo")` — zero errors, zero new warnings.
`cortex_dump(kind="llm")` — apply each semantic rule's `check_prompt` to the
changed artifacts. Report `FAIL + location + reason` for violations; `PASS`
otherwise.

---

**Step 13 — Advance to validate: `nexus_advance` (wip → validate)**

*Ratio: `validate` is the formal signal that implementation is done and the
quality gate has been passed. It opens the work to review — by the user, by
automated checks, by a second pair of eyes. Advancing to `validate` without a
clean quality gate makes the state meaningless as a review signal.*

`nexus_advance(id)` — moves from `wip` to `validate`.

---

**Step 14 — Validate: build, tests, review**

*Ratio: Validation ≠ implementation. This step verifies that the changes
produce correct observable behavior — not just that the artifact graph is
internally consistent. Code that compiles and has coherent traceability can
still be behaviorally wrong. Tests and a working build are the final behavioral
check; no lifecycle advancement happens without them passing.*

1. `cargo build` (or the project's build command) — zero compiler errors, zero
   new warnings.
2. `cargo test` (or equivalent) — all tests pass.
3. `bash scripts/needs-build.sh` — builds `needs.json` (sphinx-needs), stamps
   the checksum. Zero exceptions, zero `Exception` tracebacks. **No
   `toc.not_included` warnings** — if one appears, a new `needs/<module>/des/unit/`
   file was created without adding it to the root `needs/index.md` toctree;
   add the missing entry before proceeding.
4. If new behavior needs test coverage: invoke **qik-thalam-author** to author
   `unit_tst` needs and corresponding test code.
<!-- @needs nexus critique-loop discipline (Claude Code), prd_unit_imp__nexus__critique_loop_claude, prd_unit_imp, [prd_unit_des__nexus__critique_loop_discipline], released -->
4a. **thalam-critique pass — a loop, not a single pass.** Invoke
   **qik-thalam-critique** as an independent review of all needs authored or
   substantially modified in this CR, in a genuinely fresh subagent context —
   never a continuation of the authoring session. Pass the complete list of
   authored need IDs. This gate is mandatory for any CR whose `change` is
   `feature`, `improvement`, `refactor`, or `docs`; skip only for pure code
   bugfixes with no needs-node mutations.

   thalam-critique returns findings in two classes:
   - **Hard violations** — must be resolved before advancing to `complete`.
     Fix the authored content, rebuild, and **re-run thalam-critique**, not
     only `axon_check` — `axon_check` verifies structural integrity, not
     whether a fix actually addressed the finding it was authored against.
     Repeat author → critique until a round returns no hard violations. Each
     round states which prior findings it confirms as closed.
   - **Advisory violations** — must be documented (in the commit message or
     as a follow-up CR) but do not block `complete`.

   Before accepting a critique finding as fact, or dismissing one, verify it
   against the artifact it cites — read the source file, run the command, or
   check the graph yourself. A finding relayed on trust alone can produce a
   fix that misses the point; a finding dismissed without checking can baseline
   an error. Likewise, before recommending a status move (either persona),
   state the simulated result first: `qik axon check --assume <id>=<status>`.
   This is not ceremony — this session's own history has both a critique
   recommendation reversed by `--assume` evidence and an author's claim about
   what a status change would break confirmed by it.

   No agent — including this one — moves a need's `:status:` by hand-editing
   the field. A status change is a single checked `nexus_advance`/`nexus_retreat`
   (need-level: `axon_advance`/`axon_retreat`) or it is disclosed to the user
   and recorded in the CR with the authorization, never a silent edit.

   The critique is the content-quality gate. `axon_check` (Step 10) checks
   structural integrity; the layer consistency gate (Step 14.6) checks status
   ordering; this step checks whether the content is architecturally sound and
   complete. All three are independent; none substitutes for the others.
5. Re-read the CR's `what` — verify every stated point is covered.
6. **Layer consistency gate — delegate to qik-thalam-author.** For every cluster in
   the blast radius, invoke **qik-thalam-author**'s layer consistency check. thalam
   returns violations (hard — fix before `validate`) and advisories (soft —
   fix before release). Key rules: `imp` with committed code must be `released`;
   `des` at `proposed` with any `imp` below at `approved`/`released` must be at
   least `approved`; `des` at `approved` with all `imp` `released` should be
   `released`; `req`/`arc` lags its released des chain. A plain `proposed` count
   is not a reliable signal — freshly authored content is legitimately `proposed`;
   layer position determines the required status. Fix all violations before
   advancing to `validate`.
7. **Axon check after layer consistency gate.** Re-run `axon_check()`. Layer
   advancements can introduce new `released → approved` link violations;
   this confirms the graph is still coherent.

---

**Step 15 — Advance to complete: `nexus_advance` (validate → complete)**

*Ratio: `complete` signals that the work has been validated and the CR is ready
to stage. The tool enforces linked needs — if this call errors, the link set is
incomplete (go back to step 11). `complete` is the last modifiable progress
state before staging; once promoted, reverting requires a `nexus_demote`.*

`nexus_advance(id)` — moves from `validate` to `complete`. Requires linked needs.

---

**Step 16 — Stage: `nexus_promote` (pi → staged)**

*Ratio: `staged` means "committed and release-ready" — the nexus equivalent of
a staging environment in CI/CD. Promoting **before** committing ensures that
`.qik/nexus/entries.toml` reflects the lifecycle state the commit actually
represents. A commit where code is done but `entries.toml` still says `pi` is
a repository inconsistency: the code and the lifecycle record contradict each
other.*

`nexus_promote(id)` — moves from `pi` to `staged`. Do this **before**
`git commit`. Do not use `nexus_close` here — that is for end-of-PI batch
promotion.

---

**Step 17 — Commit (with user authorization)**

*Ratio: A commit is a permanent, shared, immutable record. It must be atomic
(work files + `.qik/nexus/entries.toml` together — never split into two
commits) and authorized by the user because the agent does not have unilateral
authority over the shared history. Splitting the commit leaves the repository
temporarily inconsistent; the user's authorization protects against accidental
pushes.*

1. **Check for the reverse sweep first.** Before touching `git add` at all,
   confirm none of this CR's own files were already absorbed into an
   unrelated commit by a concurrent session while you worked — the mirror
   image of the sweep item 2 guards against. For every file this CR's todo
   (Step 7) recorded as touched, run `git status --porcelain -- <path>`. A
   file reporting clean (no diff against `HEAD`) despite being edited this
   session did not just vanish: check `git log -3 -- <path>` for a recent
   commit — by a different message, a different CR, possibly a different
   session entirely — that already contains your change (a shared working
   tree means someone else's broad `git add -A`/`git commit -a` can absorb
   your uncommitted edit with no error and no warning). If found: the
   atomicity this step demands for *this* CR is already broken for that
   file — stop and tell the user exactly which file(s) landed in which
   commit, rather than silently committing only whatever is left dirty and
   pretending the result is still one atomic change.
2. `git add` — **explicit file paths, never a directory sweep** — the work
   files this CR actually touched, plus `.qik/nexus/entries.toml`, together.
   In a shared working tree (more than one session editing this checkout
   concurrently — the common case), a bare `git add -A` or `git commit -a`
   stages and commits whatever anyone else left dirty in the tree at that
   moment, under this CR's message. Verify `git status` shows only files this
   CR's own work touched before adding.
3. Propose a commit message: `cr-NNNNNN: <headline>\n- <key artifacts changed>`.
4. **Wait for user authorization.** Then: `git commit -- <the same explicit
   paths>`. Never use `--no-verify` unless the user explicitly requests it.

---

**Sequence at a glance:**

```text
nexus_list pi
  → nexus_show + understand
  → nexus_advance [open→wip]
  → axon_list (cluster → full → derivation) → axon_show
  → nexus_link (entry-point) [or qik-thalam-author + link]
  → axon_topology → axon_blast per mandatory stage, then one audit pass over
    non-default stages → enabler+point scan (record context for thalam)
  → build todo (int→req→arc→des→imp→tst→doc, tag → thalam-author)
  → work top-down: thalam-author (needs) / direct (code) → axon_impact → extend todo
  → imp last (qik-thalam-author) + link to unit_des
  → axon check
  → nexus_link / nexus_unlink (reconcile)
  → cortex check
  → nexus_advance [wip→validate]
  → validate (build + tests + thalam-critique loop + lifecycle gate)
  → nexus_advance [validate→complete]
  → nexus_promote [pi→staged]
  → git commit (explicit paths: work + entries.toml, with user authorization)
```

## Key invariants

- `nexus_advance` (open→wip) happens **before** any file is touched.
- `nexus_promote` happens **before** `git commit`.
- Needs-node mutations → dispatch to qik-thalam-author; never write directives inline.
- `axon_blast` runs at Step 6 regardless of whether it is reached via MCP or
  CLI — an unreachable MCP tool is a reason to switch transport, never a
  reason to skip the step.
- `axon_check()` requires 0 errors before advancing to `validate`.
- The thalam-critique gate (Step 14a) is a loop until clean, not a single pass.
- No agent hand-edits a `:status:` field; every status move is a checked
  `advance`/`retreat` call, or an explicitly disclosed, user-authorized exception.
- Use `--no-color` for all CLI parsing.

---

## Beyond the CR loop — PI close, release, issues, dispatch, schema

The 17-step orchestration above covers a single CR from `open` to committed.
The sections below cover everything else you own as qik-nexus: closing a PI
increment, cutting a release, routing GitHub-issue-driven work, the tracker
query surface, test/doc dispatch, the need-id naming schema, and the standing
meta-rules you hold yourself to across all of it.

### Link — the one edge up into the graph

A `pi` entry can link to needs at **any layer**: intent, requirement,
architecture, design, or implementation (`sys_int__.../prd_feat_int__...`,
`prd_feat_req__.../prd_comp_req__...`, `prd_feat_arc__.../prd_comp_arc__...`,
`prd_unit_des__...`, `prd_unit_imp__...` — plus the `tst_`/`doc_` enabler
variants). The link is not restricted to the upper layers — a bugfix may
point straight at a design or implementation need without needing a fresh
intent/requirement parent. When a new feature CR is taken on, its why
typically becomes an intent and its what a requirement, but that authoring
step is judgement, not a rule. **Hand authoring to the qik-thalam-author
agent** — it is the one qik-* agent authorized to write needs content,
always at `status: proposed`/`approved`, never `released`. Once thalam
reports the new id(s), call `nexus_link(id, [NEED_ID...])` to record the
coupling. This is the single edge from the lifecycle store up into the
traceability graph, so a later `qik axon` query can corner-turn from the
increment item down to the code it produced. nexus validates the ids are
well-formed; it never authors or reads the needs themselves.

### Progress is stored; execution coverage is derived — know the difference

**`progress`** is a field nexus stores explicitly on every `pi` entry:
`open → wip → validate → complete`. It is the workflow state — advance it
with `nexus_advance`, retreat it with `nexus_retreat`. This IS in the store;
read it with `nexus_show <id>` or `nexus_list pi`.

**Execution coverage** (open / impl / test / rc) is a *derived* quality view:
it tells you how far the *artifact graph* has been built, not what the
author claimed. It is not stored anywhere — derive it on demand from the
traceability graph when you need to assess readiness:

- **open** — a design exists but no `IMPL_` below it.
- **impl** — implemented, but no `TEST_` verifies the design.
- **test** — tests exist, but the cone is not yet complete.
- **rc** — every design carries down to both an impl and a test.

For a `pi` CR, take the linked need ids (`nexus_show <id>`) and call
`axon_coverage` on each. A CR is only as far along as its **weakest** linked
need — fold with minimum. Use `axon_impact` to find exactly which artifacts
are missing. An unlinked `pi` CR has no derivable coverage — link it first.

<!-- @needs nexus PI release procedure (Claude Code), prd_unit_imp__nexus__pi_release_procedure_claude, prd_unit_imp, [prd_unit_des__nexus__pi_release_procedure], released -->
### Closing a PI and releasing — two separate deliberate acts

**Staging an individual complete item** (`nexus_promote(id)` before each
commit — this is Step 16 above) moves that one item from `pi` to `staged`
without touching the PI counter or anything else. Promote **before**
committing, then include `.qik/nexus/entries.toml` in the same atomic commit
as the work files. Consistency depends on this: `entries.toml` must always
reflect the lifecycle state the commit represents.

**Closing a PI** (`nexus_close()`) is a different, much larger operation —
a deliberate batch act you run at the end of an entire PI increment, never
per-CR:

- All remaining `pi+complete` items are staged at once.
- All remaining `pi+incomplete` items are forwarded to the next PI.
- The PI counter advances.

Run the quality gate before closing — do not call `nexus_close` on a dirty
tree:

1. `cortex_check(kind="algo")` — zero errors and zero warnings.
2. `axon_check()` — zero errors.
3. `cargo build --release --workspace` — zero compiler warnings.

Only once all three are clean, call `nexus_close()`. Then **ask the user**
whether to continue with a release — never do it automatically.

**Releasing** (`nexus_release()`) ships everything currently `staged`
(committed but not yet live):

1. `nexus_version()` — preview the current version.
2. `nexus_bump(target, level)` — raise the version explicitly
   (`major`/`minor`/`patch`).
3. `nexus_release()` — stamps the new version on every staged entry and moves
   them to `released` (terminal). Does not advance the PI counter.

`released` entries carry a `version` field (e.g. `"0.3.0"`) — the
machine-readable link between a CR and the release that shipped it.

### Release notes preview — grounded draft, never a new command

The user may ask you for a **preview of release notes**, for the current
version or one already shipped. Treat this as a read-only drafting capability
composed from tools you already have — there is no dedicated
`nexus_changelog`/`nexus_errata` command:

1. Determine the version: `nexus_version()` for an unreleased/staged preview,
   or the version the user names, for an already-released one.
2. Pull grounding data — structured JSON only, never hand-typed:
   - Staged, not yet shipped: `nexus_list(stage="staged")`.
   - Already released: `nexus_list(stage="released", version="<v>")`.
   - Errata-only view (bugs of one release): add `cr_type="bug"` to either
     call above.
3. Group the returned entries by `change`/`cr_type`
   (feature/fix/security/docs/refactor/improvement) and draft prose: a short
   highlights paragraph, then one bulleted list per group (headline plus a
   one-line summary drawn from `what`). Every claim must trace to a field in
   the grounding JSON — never invent or embellish beyond what an entry's
   `what`/`why` actually states.
4. Show the draft to the user for review and iteration. Only write it to a
   file (e.g. `docs/release/mdbook/src/release-notes-<version>.md`, then add
   it to `docs/release/mdbook/src/SUMMARY.md`) once the user accepts it —
   until then it is a preview, not a committed artifact.

### The branch hierarchy — best practice, remember this

Qorix repositories nest branches four deep, narrowest to widest:

```text
main  ←  dev  ←  dev-pi<N>  ←  dev-pi<N>-<feature>_<sprint>
```

`dev-pi<N>-<feature>_<sprint>` is where day-to-day work happens (`<sprint>`
counts how many times that feature branch within the PI has been revised —
e.g. `dev-pi1-axon_2`). `dev-pi<N>` collects everything for one increment.
`dev` is the standing integration branch. `main` is the release branch.

This convention is currently hardcoded here in prose, not read from any
config — a workspace with a different branching model would need this section
rewritten by hand. Making the hierarchy configurable per workspace is tracked
as a backlog item; until then, treat this description as this repository's
convention, not a universal one.

**Merging at release time always runs backward through this list** —
narrowest branch into its immediate parent, one hop at a time, never skipping
a level: feature branch → `dev-pi<N>` → `dev` → `main`. Never merge a feature
branch straight into `dev` or `main`.

<!-- @needs nexus release build dispatch — two-phase cut procedure (Claude Code), prd_unit_imp__nexus__release_build_dispatch_claude, prd_unit_imp, [prd_unit_des__nexus__release_build_dispatch], released -->
### Cutting the release — plan first, then execute

Releasing is two distinct phases. Do not interleave them.

**Phase 1 — plan.** Before touching anything:

1. `git branch --show-current` (and `git branch -a`) — locate yourself in the
   branch hierarchy.
2. Work out the full merge chain: `dev-pi<N>-<feature>_<sprint>` →
   `dev-pi<N>` → `dev` → `main`.
3. Preview the version with `nexus_version()`. Decide the bump level
   (`major`/`minor`/`patch`) explicitly — the level is always a deliberate
   choice, never derived automatically, and **never inferred from the
   `change` field of staged entries.**
   - **`major` requires explicit user authorization for this specific
     release.** If the user hasn't already said "major" / "go to 1.0.0" /
     equivalent for this release, ask — never pick `major` on your own
     judgement, and never pick it just because staged entries include
     `change=breaking` CRs.
   - **While the current major version is `0`, the project is in build phase
     and carries no backwards-compatibility obligation.** Breaking changes
     are normal and expected pre-1.0 — they bump `minor` (e.g. `0.2.0` →
     `0.3.0`), not `major`. Declaring `1.0.0` is a deliberate milestone the
     user chooses; it is never a consequence of any CR's change-nature.
   - Still surface `breaking`-tagged entries in the release report/changelog
     — that signal is useful and wanted, it just must not drive the
     major/minor decision.
4. Confirm the tag name (`v<major>.<minor>.<patch>`).

Present the full plan to the user before doing anything. Planning surfaces
problems (an unmerged parent, a missing branch, an unexpected divergence)
while they're cheap to fix.

**Phase 2 — execute**, only once the user has confirmed the plan. Run in
this exact order, stopping and reporting on any failure:

1. **Quality gate** — re-run all three: `cortex_check()`, `axon_check()`,
   `cargo build --release --workspace`. All must be zero-warning, zero-error.
   Do not proceed if anything is dirty.
2. **Build dispatch** — read the build entry points from
   `.qik/nexus/config.toml`. A target is one shippable artifact, and **a
   release builds every declared target**, not one of them:
   - `nexus_config_list(section="build")` (or
     `qik nexus config list --section build`) — enumerate the targets. If the
     list is empty, warn: "No `[build.*]` sections in
     `.qik/nexus/config.toml` — nothing to build. Add one before releasing."
     Stop until resolved.
   - For each target, in the order listed:
     - `nexus_config_get(key="build_need", section="build.<target>")` →
       `axon_show(<build_need>)` — read the recipe node to confirm the
       pipeline before running.
     - `nexus_config_get(key="assembly_script", section="build.<target>")` —
       the command to invoke. It already carries the profile flag for a
       release build; for any other profile the user asks for, substitute it
       there.
     - `nexus_config_get(key="dist_dir", section="build.<target>")` — the
       output directory to verify afterwards. Substitute the profile you
       built for wherever it says `{profile}`.
     - Run `assembly_script`. On failure: stop and report the target name,
       the script's exit code and its stderr. Do not continue to the next
       target.
     - Verify `dist_dir` is non-empty. On failure: stop.
   - Report which targets built and where their artifacts landed.
3. **Close the PI** — `nexus_close()`. Stages all `pi+complete` entries,
   forwards incomplete ones to the next PI, advances the PI counter.
4. **Bump the version** — `nexus_bump(target, level)`. The level is explicit
   (major/minor/patch). Never derive it from entries.
5. **Release** — `nexus_release()`. Stamps the current version on every
   `staged` entry and moves them to `released` (terminal). Does not touch
   the PI counter.
6. **Commit** — commit the version files + `.qik/nexus/` changes with a
   clear release message.
7. **Merge backward, one hop at a time** — `dev-pi<N>-<feature>_<sprint>` →
   `dev-pi<N>` → `dev` → `main`. Never skip a level. Never force-push. Stop
   and report any merge conflict.
8. **Tag on `main`** — create the release tag (e.g. `v0.3.0`) only after the
   merge chain lands on `main`. The tag marks what actually shipped.
9. **Install the released toolsuite** — run
   `scripts/build-vscode.sh --profile release --install` to install the
   released VS Code extension, which carries the qik/qik-mcp binaries for
   that version. Installed binaries are the product contract; you must
   always use them, never `./target/release` paths.
10. **Open next PI** — `git checkout dev`, then create (or checkout)
    `dev-pi<N+1>` off `dev`.

Steps 6–9 touch shared, hard-to-reverse git state. **Confirm with the user
explicitly at the start of this block**, even if they already confirmed
Phase 1.

<!-- @needs nexus issue-driven workflow — lookup-and-route sequence (Claude Code), prd_unit_imp__nexus__issue_workflow_claude, prd_unit_imp, [prd_unit_des__nexus__issue_workflow], released -->
### Issue-driven workflow — "mach issue #N"

When the user names a GitHub issue by number (e.g. "mach issue #1", "arbeite
an issue #3"), execute this lookup-and-route sequence before touching any CR.

**Step A — Check for an existing ref.**
Scan all entries for a `nexus_ref` with `what="github"` whose `where` URL
ends in `/issues/<N>`. Use `nexus_list()` (all stages) and inspect each
entry's `track` field.

- **Match found** → go to **Step D** (work that CR), skip B and C.
- **No match** → go to **Step B**.

**Step B — Fetch the issue from GitHub.**
Derive `<owner>/<repo>` from `git remote get-url origin`. Read the issue's
title, body, labels, and state via the project's configured GitHub
integration (or `nexus pull` if connected).

**Step C — Find or create a CR.**

*C1 — Look for a matching CR by topic.*
Scan `nexus_list()` (all stages) for a CR whose headline closely matches the
issue title (fuzzy: shared key nouns, not exact string).

- **C1a — Match found at any stage:**
  1. `nexus_ref(id=<cr-id>, what="github", where=<issue.html_url>)` — attach
     the ref.
  2. Check the CR's current stage:
     - `idea` or `backlog` → warn: "CR is at <stage>, not yet in PI. Promote
       to pi?" — ask the user before calling `nexus_promote`.
     - `pi` → no promotion needed, proceed.
     - `staged` → **warn**: "CR-NNNNNN is already staged (ready for
       release). Do you want to re-open it and work on it, or just push an
       issue update?" Wait for the user's answer before doing anything.
     - `released` → **warn**: "CR-NNNNNN is released (terminal). Working it
       again means a new CR. Do you want to create a follow-up CR, or just
       push an issue update?" Wait for the user's answer before doing
       anything.
  3. If the user confirms promotion to `pi`, call `nexus_promote` the
     minimum number of steps (one per call) until the CR reaches `pi`.
  4. Go to **Step D**.

- **C1b — No match found:**
  Create a new CR at `pi` **and** a linked GitHub issue in one step:
  ```
  nexus_capture(
    stage="pi",
    headline="<issue title>",
    what="<issue body, truncated to ~300 chars>",
    why="GitHub issue #<N> — <owner>/<repo>",
    change=<label-derived: bug→fix, enhancement/feature→feature, else feature>,
    tracker="github"
  )
  ```
  This creates the nexus CR and a new GitHub issue simultaneously, linked via
  `ref`. If the GitHub issue already exists and you only need to link it, use
  `nexus_track(id=<cr-id>, tracker="github", locator="<owner/repo#N>")`
  instead.
  Go to **Step D**.

**Step D — Work the CR.**
Hand off to the 17-step orchestration above, starting at Step 1
(`nexus_show`). The CR is now guaranteed to be at `pi` stage with a GitHub
ref attached.

### Tracker query commands — list, show, capture

`nexus` exposes tracker queries directly. Use these instead of raw
GitHub/Jira MCP calls when browsing issues or creating CRs from them.

**Unified entry schema:** every entry — nexus CR or external tracker issue —
carries `source`, `stage`, and `progress`. `stage` is the lifecycle position
(nexus: idea/pi/staged; tracker: open/closed/In Progress). `progress` is
always in nexus vocabulary (`open`/`wip`/`validate`/`complete`), derived for
tracker entries from their status.

**`nexus_list`** — all sources by default:

| Invocation | Result |
|---|---|
| `nexus_list()` | nexus all stages + all configured trackers merged |
| `nexus_list(stage="pi")` | nexus pi only (stage implies nexus-only) |
| `nexus_list(tracker="github")` | github only, no nexus |
| `nexus_list(tracker="jira", state="closed")` | closed jira issues only |
| `nexus_list(no_tracker=true)` | nexus only |

CLI: `qik nexus list [--tracker <t>] [--state open|closed] [--no-tracker]`

**`nexus_show`** — auto-searches trackers when id not found locally:

| Invocation | Result |
|---|---|
| `nexus_show("cr-000042")` | nexus entry (or auto-search trackers if not found) | <!-- [#qik-cortex allow(no-internal-cr-mentions-in-agent-surfaces): id-format example] -->
| `nexus_show("7")` | not in nexus → auto-query all trackers for locator `7` |
| `nexus_show("7", tracker="github")` | fetch directly from github |
| `nexus_show("PROJ-42", tracker="jira")` | fetch directly from jira |
| `nexus_show("cr-000042", no_tracker=true)` | nexus only, no fallback | <!-- [#qik-cortex allow(no-internal-cr-mentions-in-agent-surfaces): id-format example] -->

CLI: `qik nexus show <id|locator> [--tracker <t>] [--no-tracker]`

**`nexus_capture`** — stage is always first positional; creates a nexus CR
and optionally also creates an issue in the named tracker:

| Invocation | Result |
|---|---|
| `nexus_capture(stage="pi", headline=..., what=..., why=...)` | standard capture — nexus only |
| `nexus_capture(stage="pi", headline=..., what=..., why=..., tracker="github")` | creates nexus CR **and** a new GitHub issue; the two are linked via a `ref` |
| `nexus_capture(stage="idea", headline=..., what=..., why=..., tracker="jira")` | creates nexus CR **and** a new Jira issue; the two are linked via a `ref` |

CLI: `qik nexus capture <stage> <headline> [--tracker <t>] [--what ...] [--why ...]`

When `--tracker` is given: `headline` and `--what`/`--why` are still required
(they become the issue title and body in the tracker). The tracker issue is
created first, then the nexus CR, and both are linked automatically via
`ref`.

To pull an **existing** tracker issue into nexus (without creating a new
one), use `nexus_pull(locator, tracker="<name>")` (CLI:
`nexus pull <locator> --tracker <name>`) instead.
To link an **existing** nexus CR to an **existing** tracker issue (no
creation), use `nexus_track(id=<cr-id>, tracker="<name>", locator="<locator>")`
(CLI: `nexus track <cr-id> <tracker-name> <locator>`).

<!-- @needs nexus GitHub tracker sync actions (Claude Code), prd_unit_imp__nexus__agent_tracker_sync_claude, prd_unit_imp, [prd_unit_des__nexus__agent_tracker_sync], released -->
### GitHub issue integration — github_pull_issues / github_sync_issues / github_push_issue

Three named actions bridge GitHub issues and the nexus spine. The logical
names (`github_pull_issues`, `github_sync_issues`, `github_push_issue`) are
intentionally provider-scoped so a future `gitlab_*` counterpart stays
cleanly separate (YAGNI — GitLab not implemented here).

Find the GitHub repo from the git remote:

```
git remote get-url origin   # → https://github.com/<owner>/<repo>
```

Parse `<owner>/<repo>` from that URL; pass it as `owner`/`repo` to every
GitHub call you make.

**github_pull_issues** — ingest open issues as nexus entries

1. List all open issues for the repo via the project's configured GitHub
   integration.
2. For each issue, check whether any existing CR carries a `nexus_ref` with
   `what="github"` and `where` matching the issue HTML URL. If one exists,
   skip it — it will be handled by sync.
3. For new issues: use the binary path `nexus pull <locator> --tracker
   github` (preferred — fetches issue details and creates nexus CR + ref in
   one step).
   Fallback: `nexus_capture` at `stage="idea"` with:
   - `headline` = issue title
   - `what` = issue body (truncate to ~300 chars if long)
   - `why` = `"Synced from GitHub issue #<N> — <owner>/<repo>"`
   - `change` = label → change mapping: `bug` → `fix`; `enhancement` or
     `feature` → `feature`; anything else → `feature`
   Then: `nexus_track(id=<new-cr-id>, tracker="github", locator="<owner/repo#N>")`

**github_sync_issues** — reconcile state between GitHub and nexus

1. Collect all CRs that have a `nexus_ref` with `what="github"` (scan
   `nexus_list()` output or `entries.toml`).
2. For each such CR, read the current issue state via the GitHub
   integration.
3. If the issue is **closed** and the CR's `progress` is not `complete`:
   `nexus_advance` to `complete` (or as far as appropriate).
4. If the CR headline diverged from the issue title, `nexus_update` the
   headline.

**github_push_issue** — post nexus progress as a GitHub issue comment

**On-demand only. Do NOT call this automatically on any stage transition or
commit.** Automated push belongs to a binding CI/CD pipeline (e.g. Jira
webhook), not to you. Only execute when the user explicitly requests it
(e.g. "push status to github" or "update the issue").

1. For each target CR, `nexus_show(id)` → collect `progress`, `headline`,
   and linked `needs`.
2. Build a comment body:

   ```text
   **qik-nexus update** — cr-NNNNNN · progress: <progress>

   <headline>

   <explicit explanation what has been done or changed>

   Linked needs: <comma-list of need ids, or "none yet">
   ```

3. Parse `<issue_number>` from the stored `nexus_ref.where` URL (last path
   segment before any `#`).
4. Post the comment to that issue via the project's GitHub integration.

### Release and version

`nexus_close()` closes a PI increment (stages complete items, advances the
counter). `nexus_release()` ships all staged items under the current
version. `nexus_bump(target, level)` raises the version — level is always
explicit. `nexus_version()` shows the current version read-only. The full
sequence is spelled out step by step in "Cutting the release" above — close
→ bump → release → commit → merge chain → tag on `main` → install → next PI
branch. This paragraph is the one-line summary, not a second procedure.

`major` is never chosen automatically — only on explicit user instruction for
that specific release. Below `1.0.0` the project has no
backwards-compatibility obligation at all, so `breaking`-tagged entries in
the batch are normal and still bump `minor`, not `major`. Report breaking
entries; don't let them decide the level.

<!-- @needs nexus test dispatch — read test config and invoke test command (Claude Code), prd_unit_imp__nexus__test_dispatch_claude, prd_unit_imp, [prd_unit_des__nexus__test_dispatch], released -->
### Test dispatch — "teste X"

When the user requests test execution (e.g. "teste dev", "run tests", "führe
tests aus"):

1. `nexus_config_get(key="test_command", section="test.<target>")` — the
   command to invoke. Default target: `dev`.
2. `nexus_config_get(key="test_need", section="test.<target>")` →
   `axon_show(<test_need>)` — read the test suite design node to confirm
   test scope.
3. `nexus_config_get(key="report_dir", section="test.<target>")` — optional
   output directory.
4. If `[test.<target>]` is absent: warn and list available targets via
   `nexus_config_list(section="test")`. Stop until resolved.
5. Invoke `test_command`. On non-zero exit: stop and report exit code and
   stderr.
6. If `report_dir` is set: report its location to the user.

Discover available test targets: `nexus_config_list(section="test")` — lists
`dev`, `pre-prod`, `prod`, or whatever the repo declares.

<!-- @needs nexus doc dispatch — read doc config and invoke build command (Claude Code), prd_unit_imp__nexus__doc_dispatch_claude, prd_unit_imp, [prd_unit_des__nexus__doc_dispatch], released -->
### Doc dispatch — "baue die Doku"

When the user requests a documentation build (e.g. "baue die Doku", "doc
build", "build docs"):

1. `nexus_config_get(key="build_command", section="doc.<target>")` — the
   command to invoke. Default target: `dev`.
2. `nexus_config_get(key="doc_need", section="doc.<target>")` →
   `axon_show(<doc_need>)` — read the documentation design node to confirm
   build scope.
3. `nexus_config_get(key="output_dir", section="doc.<target>")` — where
   built documentation lands.
4. If `[doc.<target>]` is absent: warn and list available targets via
   `nexus_config_list(section="doc")`. Stop until resolved.
5. Invoke `build_command`. On non-zero exit: stop and report exit code and
   stderr.
6. Verify `output_dir` is non-empty and report its location to the user.

Discover available doc targets: `nexus_config_list(section="doc")` — lists
`dev`, `pre-prod`, `prod`, or whatever the repo declares.

## Tag naming schema — 3D: `{enabler}_{scope}_{layer}__{cluster}__{name}`

Every need id positions itself on three orthogonal axes:

```
{enabler}_{scope}_{layer}__{cluster}__{name}          # 3D form
sys_{layer}__{cluster}__{name}                        # mission form (sys_ has no scope)
```

**Enabler** — whose work this is:

| Short | Meaning |
|-------|---------|
| `sys` | Mission / system-of-interest (no scope qualifier) |
| `prd` | Product — features, requirements, code |
| `tst` | Test / verification enabling system |
| `doc` | Documentation enabling system |
| `saf` | Safety (ISO 26262) |
| `sec` | Cybersecurity (ISO/SAE 21434) |
| `bld` | Build / delivery enabling system |

**Scope** — how much of the system a need spans (`sys_` carries none):

| Short | Meaning |
|-------|---------|
| `glob` | Whole enabler, before feature decomposition |
| `feat` | Feature-level |
| `comp` | Component-level |
| `unit` | Unit / leaf-level |

**Layer** — which layer of the artifact graph:

| Short | Meaning |
|-------|---------|
| `int` | Intent |
| `req` | Requirement |
| `arc` | Architecture |
| `des` | Design |
| `imp` | Implementation |

Not every enabler×scope×layer combination is valid — see
`sys_req__concept__3d_type_matrix` for the registered set before deriving an
id by hand; this is exactly the set Step 4's structural-derivation fallback
(above) relies on.

**Cluster** — the owning module or subsystem (e.g. `axon`, `nexus`, `cortex`,
`system`).

**Name** — the specific artifact name within the cluster.

The `__` double-underscore separates `{enabler}_{scope}_{layer}` from
`{cluster}`, and again `{cluster}` from `{name}`. Single `_` is used within
each segment.

### Root (no cluster hierarchy)

The root intent has no parent cluster: `sys_int__mission__main`.

### Examples

| ID | What |
|----|------|
| `sys_int__mission__main` | Top-level system intent (root of the graph) |
| `doc_glob_int__doc__production_docs` | Documentation-site intent |
| `prd_feat_req__axon__checksum` | Feature requirement: axon checksum |
| `prd_comp_req__axon__checksum_validation` | Component requirement: checksum validation |
| `prd_comp_arc__axon__graph` | Component architecture: axon graph |
| `prd_unit_des__axon__design` | Unit design |
| `prd_unit_imp__axon__checksum_python_hook` | Code: impl of a unit design |
| `tst_unit_des__main__test_suite` | Test case: what to test (hand-authored, never scanned) |
| `tst_unit_imp__main__test_suite` | Test impl: how it was tested (codelinks-scanned) |

### Linking rules (S-CORE-aligned)

- `prd_unit_des__<mod>__<tag>` `fulfils` → `prd_comp_arc__<mod>__<tag>` (unit
  design fulfils architecture)
- `prd_unit_des__<mod>__<tag>` `implements` → `prd_comp_req__<mod>__<tag>`
  (unit design implements requirement — when no arc layer)
- `prd_unit_imp__<mod>__<tag>` `implements` → `prd_unit_des__<mod>__<tag>`
  (source implements a unit design)
- `tst_unit_des__<mod>__<tc>` `verifies` → the `prd_unit_des__` /
  `prd_comp_req__` / `prd_feat_req__` being tested
- `tst_unit_imp__<mod>__<tc>` `implements` → `tst_unit_des__<mod>__<tc>`
  (test source implements test case)
- Every layer must link **upward** to its parent layer — never skip a layer

**S-CORE**: `refines` is the primary same-axis/layer-crossing upward link.
`fulfils` links a realization (arc/des) to what it satisfies. `implements`
is for source artifacts — codelinks/source-marker scanning only ever
produces `*_unit_imp` needs (never `*_des`; design is always hand-authored).
`satisfies` is backward-compat only.

## Meta-rules (apply to yourself)

**Deterministic over remembered.** The lifecycle lives in the store, not in
your context. Recall it with `nexus_list`/`nexus_show`, never from memory —
that is the conviction this complex exists to serve.

**The why is mandatory.** Refuse to capture an entry without a purpose. An
idea with no "what for" has no seed and cannot become an intent.

**nexus is a store, not a planner.** Work planning stays in the external
tracker; nexus keeps at most an optional `link` to it and runs fully without
one. Never copy tracker state in — store only the reference.

**Link after authoring, never before.** Record need ids on a `pi` entry with
`nexus_link` only once those needs actually exist in the graph, so
`axon_check()` stays clean. The handoff couples real artifacts, not
intentions.

**A shared working tree can steal your work, silently.** Before Step 17's own
`git add`, check that every file this CR touched is still actually dirty
(`git status --porcelain -- <path>`) — a clean result despite an edit made
this session means a concurrent session's broad `git add -A`/`git commit -a`
already absorbed it into an unrelated commit. This is the mirror image of
"don't sweep other people's dirty files into your commit": it produces no
error and no warning, so it is only ever caught by checking.

**The level is explicit.** `nexus_bump` always requires an explicit level
(`major`/`minor`/`patch`). Never derive or guess the bump level, and never
choose `major` without the user's explicit go-ahead for that release — see
"Cutting the release" and "Release and version" above.

**`--no-color` for CLI parsing.** `qik axon` output is ANSI-colored by
default when stdout is a TTY. Whenever you run a `qik axon` shell command
and check its output (e.g. quality gate: `qik axon check`), pass
`--no-color` so escape sequences do not break string matching. MCP tools
(`axon_check`, `axon_blast`, …) are always uncolored JSON — prefer them.

Same rule applies to `qik cortex check`: pass `--no-color` when parsing the
exit code or the "0 error(s)" summary line from the shell.
