# Copilot Instructions — Qorix quality gate (qik)

This repository is governed by the **Qorix Intelligence Kit** (`qik`). The
project rules are not optional style preferences — they are enforced by the
`qik` MCP server and the `qik` binary (`qik cortex …`). Treat them as hard
constraints.

<!-- @needs copilot-instructions dispatch trigger — standard agent routes to qik-nexus on CR mention, prd_unit_imp__nexus__agent_dispatch_trigger, prd_unit_imp, [prd_unit_des__nexus__agent_dispatch_trigger], released -->
<!-- @needs copilot-instructions dispatch trigger — standard agent routes to qik-thalam-author on needs authoring, prd_unit_imp__thalam__author_dispatch_trigger, prd_unit_imp, [prd_unit_des__thalam__author_dispatch_trigger], released -->
## Automatic agent dispatch (mandatory, no exceptions)

The standard agent must not handle CR lifecycle or sphinx-needs authoring inline.
Dispatch is mandatory in exactly these two cases:

- **CR lifecycle** — whenever the user mentions a CR ID (`cr-NNNNNN`) or says
  `work`/`bearbeite`/`fix` + CR ID → **always dispatch to `qik-nexus` subagent
  first**. Never execute lifecycle steps (`nexus_advance`, `nexus_promote`,
  `axon_blast`, `cortex_check`, etc.) inline.
- **Needs authoring** — whenever a sphinx-needs directive needs to be authored or
  modified (`:::{type}`, `:id:`, `:status:`, any needs node content) → **always
  dispatch to `qik-thalam-author` subagent**. Never write needs directives inline.

## Deterministic tools before exploration (qik-first)

Whatever `qik` can decide, let `qik` decide. Do not spend reasoning tokens — or
`find` / `grep` / whole-file reads — re-deriving a fact a qik command returns
deterministically. On a feature, architecture, or traceability task, reach for
the qik command **first**, then read only the locations it points you at:

- **Traceability** — "what does this affect", "where does this come from", "is
  the graph coherent", "what are the requirements/design for X" → `qik axon`
  (`axon_list`, `axon_check`, `axon_trace`, `axon_impact`, `axon_blast`).
  Do **not** hand-walk the `needs/` corpus to reconstruct the trace graph.
- **Rules / quality** — "is this allowed", "why this convention", code review →
  `qik cortex` (`cortex_check`, `cortex_dump`, `cortex_list`, `cortex_show`).

Manual exploration is the **fallback** for what no qik command covers — never
the reflex. Starting a change: `axon_list`/`axon_impact` first to see the
affected slice, then read those coordinates.

## MCP tools (preferred when available)

The `qik` MCP server is registered. Use these tools directly:

| Tool | Purpose |
|------|---------|
| `cortex_check` | Deterministic algo check. Run first. Returns a JSON `Report`. |
| `cortex_dump` | Full rule set for priming. `kind="llm"` for semantic rules. |
| `cortex_learn` | Record a new rule from an incident, immediately. |
| `cortex_ignore` | Suspend a rule in a specific scope with a recorded reason. |
| `cortex_forget` | Remove a learned rule that was wrong or superseded. |

All nexus lifecycle operations are also available via MCP (`nexus_list`,
`nexus_advance`, `nexus_close`, `nexus_link`, etc.) — prefer these over
shelling out to `qik nexus …`.

## Git commit → nexus staging (automatic lifecycle)

After every `git commit`, call `nexus_close` **if** any PI items have
`progress = complete`. This stages them automatically so the lifecycle stays
in sync with the code:

```
1. git commit completes
2. call nexus_list(stage="pi") — check for complete items
3. if any exist → call nexus_close()
4. report: N items staged, M forwarded to next PI
```

Do NOT skip this step. A complete item that is not staged after its commit
is a lifecycle gap — the nexus store and the git history will be out of sync.

## Workflow (run in order, every code review)

1. **Algo check** — call `cortex_check(kind="algo")`. Parse the JSON report.
   Every `"severity": "error"` is a hard blocker. Fix the code, not the rule.
   Re-run until clean.

2. **Semantic check** — call `cortex_dump(kind="llm")`. Apply each rule's
   `check_prompt` to the changed code. Report `FAIL + location + reason`
   for violations; `PASS` otherwise.

3. **Learn** — when the audit reveals a recurring pattern not yet in the
   rules, call `cortex_learn(...)` immediately. Do not defer.

## CLI fallback (when MCP unavailable)

```bash
qik cortex dump --kind all              # prime with current rules
qik cortex check --kind algo --mcp      # algo check → JSON report
qik cortex dump --kind llm --mcp        # semantic rules for manual review
qik cortex learn <id> --kind <k> ...    # record rule from incident
```

## PI progress tracking (nexus)

At the start of any work session in a project, check which PI items need
attention before writing any code:

```bash
qik nexus list pi          # see all PI items and their completion state
```

**Always advance progress** as work happens — never leave items stale:

| When | Command |
|------|---------|
| Starting an item | `qik nexus advance <id> wip` |
| Implementation done, needs review | `qik nexus advance <id> validate` |
| Finishing an item | `qik nexus advance <id> complete` |
| Correcting an entry | `qik nexus update <id> --what "…" --why "…"` |

An item is `open` (not started), `wip` (in progress), `validate` (done, awaiting review), or `complete` (done, awaiting staging).

**Staging** means moving a completed PI item from `pi` to `staged` — the
holding area from which items are released as a version. A `staged` item is
fully done and frozen; it waits only for `nexus_release` to stamp it with a
version number.

Staging path: `nexus_promote <id>` — moves one item one step up the spine
(idea→backlog→pi→staged). Stage a CR as soon as its work is committed.

`nexus_close` is for **PI bookkeeping only**: it bumps the PI counter and
forwards all incomplete pi entries to the next increment. As a side-effect it
also stages any items still sitting at `complete` — but that is just cleanup,
not the primary path. Do not use `nexus_close` to stage items; promote them
individually instead.

**At every `git commit`**: stage all `pi+complete` items via `nexus_promote
<id>`, use their headlines to build the commit message, then commit. The nexus
store (`.qik/nexus/entries.toml`) must be included in the commit.

Do NOT end a session without pulling the progress of every item you touched.

## Traceability (axon)

When you change code, design, or requirements, check what else is affected
before declaring the change done. The same `qik` MCP server exposes the
traceability graph (built by sphinx-needs into `needs.json`):

| Tool | Purpose |
|------|---------|
| `axon_trace` | Upstream provenance of a need — "where does this come from". |
| `axon_impact` | Downstream effect of a need — "what does changing it touch". |
| `axon_blast` | The blast radius: `trace` (up) + `impact` (down) combined from one start point — two independent one-directional walks, merged, never switching direction at an intermediate node. Each entry carries `direction`/`distance` from the start (e.g. `[up, 1]`, `[down, 3]`). |
| `axon_check` | Traceability integrity (orphans, dangling links) as a `Report`. |

CLI fallback: `qik axon impact <ID>`, `qik axon trace <ID>`, `qik axon check`.

After a change, call `axon_impact` (or `axon_blast`) on the affected need,
read the listed artifacts at their locations, and update the ones that drift —
**never silently**; propose the edits.

## Rules of engagement

- Violations are facts — state them directly.
- Fix the code, never weaken a rule.
- No stubs, no `todo!()`, no placeholder implementations.
- When a recurring pattern is found, record it with `cortex_learn` — do not
  just apologize and move on.
- Bypassing a rule in a specific scope requires `cortex_ignore` with a recorded
  reason. Never silently skip a rule.
