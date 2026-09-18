<!-- @needs sme_structure skill file — real-tree folder-placement guards shared by every thalam persona, prd_unit_imp__thalam__sme_structure, prd_unit_imp, [prd_unit_des__thalam__sme_structure], proposed -->

# sme_structure — Real-Tree Folder-Placement expert, shared by every thalam persona

**Lives at `.qik/thalam/sme/guardrails/structure.md`, a sibling of
`integrity.md`, `presentation.md` and `placement.md`** — same
platform-neutral home and same "read once, never restated per persona"
discipline (see `integrity.md`'s own header for why that home). Split from
all three deliberately: this file's concern is **where source, build, test,
and documentation content physically lives in the repository** — `prod/`,
`tests/`, `docs/`, `build/`, `dist/` and how each is sub-divided — distinct
from `integrity.md`'s graph-correctness question (enabler classification,
marker hygiene), `presentation.md`'s Information Architecture question (how
the graph's content is organized for a reader), and `placement.md`'s
needs/-internal file-placement question (which concrete file under
`needs/` itself a node's content belongs in). All four concerns used to
risk collapsing into one another; each is kept its own file so no guard set
overloads another with an unrelated responsibility.

**Load trigger:** any real-tree (non-`needs/`) folder-placement question —
scaffolding a new project's canonical root folders, or auditing whether an
authored or generated artifact sits in the right real-tree location.
**References:** ISO/IEC/IEEE 15288 §6.4.8 Integration and §6.4.10
Transition (the manufacturing and delivery system).

**Two tiers, read in order.** Part I states the general schemata — the
vocabulary and grammar any qik-bootstrapped project uses, regardless of
which enablers or Assemblies it happens to populate. Part II states how a
specific enabler folder (`prod/`, `tests/`, `build/`, `docs/`, and,
speculatively, `saf/`/`sec/`) derives its own internal shape *from* Part
I's general rules — a derivation, never a competing rule of its own.

---

## Foundational concept: System-of-Interest → System / Assembly / Element (concise — full derivation lives in `placement.md`)

`placement.md`'s own foundational-concept section derives this in full,
including its ISO/IEC/IEEE 15288 grounding; restated here only to the depth
this file's own real-tree guards need, since every one of them is built on
it. ISO/IEC/IEEE 15288 separates a project's **system-of-interest** — the
system whose life cycle is under consideration, the thing actually built and
delivered — from the **enabling systems** that support that life cycle
without themselves being the delivered thing (a build tool, a test rig). A
project decomposes its own system-of-interest, at the top, into
**Assemblies**: project-declared groupings defined by exactly one criterion,
build-independence (each with its own build entry point and its own build
output, never requiring the rest of the corpus to build alongside it) — the
one decomposition level directly beneath the system-of-interest itself, no
level between the two. Each Assembly's own top-level structural component is
called an **Element** — the first level of structural decomposition directly
beneath that Assembly; finer components beneath an Element remain
components of it, never themselves promoted to Element or Assembly status.
**System** names the system-of-interest viewed at the top, before any
Assembly-level decomposition — a project's own mission, concept model, and
general realization paradigms, none of it scoped to one Assembly.

This is exactly what every real-tree guard below is built on: an
enabler-folder workspace (`prod/`, `docs/`, `tests/`, `build/`) holds zero or
more Assembly-named subfolders as peers — never itself an Assembly — and
each Assembly-named subfolder is where that one Assembly's own real-tree
content lives, however many Elements its own internal module structure
happens to nest.

---

## Foundational concept: Ecosystem — the language/toolchain a piece of source content is written in and built by

Unlike System/Assembly/Element (defined once, in full, in `placement.md`),
**Ecosystem** is a concept this file itself introduces, because it is
structure-*forming* for the real tree in a way it is not for the needs
graph: the `<enabler>/<assembly>/<ecosystem>/...` leaf grammar throughout
this file is built directly on it.

An **ecosystem** is the language, toolchain, or development environment one
piece of source content is written in and built by — a Rust crate built by
Cargo, an mdBook site built by mdBook, an npm/TypeScript package built by
npm/tsc, for instance — together with that ecosystem's own, pre-existing
convention for how its own content is internally laid out (Cargo's own
`src/`, mdBook's own `src/`+`book/`, npm/tsc's own `src/`+`out/`). Every
real-tree leaf beneath an Assembly names, first, which ecosystem the content
beneath it belongs to; that ecosystem's own convention takes over from
there, never re-decided by this model (the guard on the leaf grammar,
below, states this in full).

One Assembly may span more than one ecosystem at once — one already built,
another decided but not yet built — which is recorded explicitly, per the
guard further below, never left to be inferred from which folders currently
exist on disk.

---

## This file's own formula, and how it differs from `placement.md`'s and `presentation.md`'s

`structure.md`, `placement.md`, and `presentation.md` all reason over the
same building blocks (System, Assembly, Element, Ecosystem, Enabler, Scope,
Layer) — none invents a vocabulary the other two do not share. What
distinguishes them is that each composes those same blocks into a different
ordered path, for a different purpose:

- **This file (`structure.md`), real-tree source location:**
  `<enabler>/<assembly>/<ecosystem>/...` — Enabler-first, because the
  repository root is enabler-typed by definition (the guard above).
- **`placement.md`, needs-tree file location:**
  `<assembly>/<element>/<enabler>/<scope>/<layer>/...` — Assembly/Element
  first instead, so one module team's whole artifact graph sits under one
  subtree root it owns without interference.
- **`presentation.md`, reader-facing navigation:** its own main menu orders
  `System`, then one slot per enabler-with-content, then `Distribution`;
  its own per-enabler sidebar orders `<enabler>/<assembly>/` then a
  three-tier split (`glob`-scope tier, `Features` tier, Element tier)
  within the active Assembly.

Same seven building blocks, three different orderings for three different
purposes — not three unrelated concept sets that merely happen to share
some words.

---

## Enabler, Scope, and Layer are separate, needs-graph axes — not defined here

The real-tree concern folders this file discusses (`prod/`, `tests/`,
`docs/`, `build/`) correspond, by project convention, to the same
**Enabler** axis the needs graph itself uses — which enabling system's
artifact something is (`prd`/`tst`/`bld`/`doc`/`saf`/`sec` — *whose* work).
**Scope** (the decomposition grain within one Element: `glob`/`feat`/`comp`/
`unit`) and **Layer** (the abstraction level from intention to code:
`int`/`req`/`arc`/`des`) have no real-tree counterpart this file governs at
all. All three axes are each fully defined in their own dedicated files —
`.qik/thalam/sme/enabler/*.md`, `.qik/thalam/sme/scope/*.md`,
`.qik/thalam/sme/layer/*.md` — read those for the full definition; only this
one-line reminder of what each axis means lives here.

---

## Part I — General schemata

### Guard: enabler-first, not assembly-first, at the repository root

**Dos**
- Keep the repository root enabler-typed: `prod/`, `tests/`, `docs/`,
  `build/` stay top-level siblings.
- Nest an Assembly segment *inside* each enabler folder, never the reverse.

**Don'ts**
- No top-level `assemblies/` wrapper folder mirroring a needs-tree's own
  `assemblies/<assembly>/<element>/...` shape.
- No enabler folder relocated beneath a top-level Assembly-named folder.

**Why.** An assembly-first top level would need one single, universal
Assembly partition to double as the literal top-level folder set. But
Assembly *identity* is global — one shared namespace across the whole
project — while Assembly *presence* varies per workspace: two different
enabler folders hold genuinely different **subsets** of that one shared
namespace, not two independently-named vocabularies that happen never to
collide. A single top-level `assemblies/` folder would still force every
workspace's own present-subset to collapse into one literal top-level
listing, which does not correctly represent "presence varies, identity does
not" any better than the enabler-first shape does. Enabler-first is the
shape that can actually carry an Assembly concept whose presence is
enabler-relative.

| Check | Type |
|---|---|
| Root stays enabler-typed (`prod/`, `docs/`, `tests/`, `build/` as top-level siblings) | pass/fail |
| No top-level `assemblies/` segment introduced at the repository root | pass/fail |

---

### Guard: an enabler-folder is a workspace, never itself an Assembly

Assembly is a flat, non-nesting boundary: an Assembly never contains
another Assembly, the same way a compilation-unit boundary in a language
ecosystem cannot contain another instance of itself while its own internal
module structure nests arbitrarily deep. A concern folder that holds
several sibling Assemblies is exactly such a container — a **workspace** —
and it groups Assemblies as peers; it is never itself a further Assembly on
top of them.

**Dos**
- Name a concern folder (`prod/`, `docs/`, ...) as a workspace holding zero
  or more Assembly-named subfolders.

**Don'ts**
- Do not carry Assembly-level identity on the workspace folder itself in
  addition to the Assemblies nested beneath it — even where that folder's
  own name would read naturally as a candidate Assembly name.

| Check | Type |
|---|---|
| A concern folder is never itself named/treated as an Assembly | pass/fail |

---

### Guard: Assembly identity is global, one shared namespace; Assembly presence is what varies per workspace

If an Assembly named in one workspace and one named in another workspace
ever happen to share a name, they are the same Assembly, never two
unrelated things that merely collided. A project declares exactly one,
ever-growing set of Assembly names — one shared namespace, never a
separate, locally-scoped partition invented anew by each workspace. What
varies from one workspace to the next is only which of those globally-named
Assemblies happen to have content there at all — a workspace simply omits
an Assembly it holds nothing for, the same way any container omits a
member it does not have.

**The model is N Assemblies × M workspaces, not M independent Assembly
vocabularies.**

| Check | Type |
|---|---|
| A workspace's Assembly list is read as its own present subset of one shared vocabulary, never as a separate vocabulary of its own | pass/fail |
| No second, differently-scoped Assembly name is invented for a workspace merely because that workspace has never held an Assembly of that name before, without first checking the project's one global list | pass/fail |

---

### Guard: the `<concern>/<assembly>/<ecosystem>/...` leaf grammar — no invented `src`/`source` segment

The real-tree leaf shape beneath a source-bearing concern folder is the
Assembly segment, directly followed by the **ecosystem** segment — the
language, toolchain, or development environment the content is written in
and built by — with no further, invented `src`/`source` segment between
them.

**Why no `src` segment — dissolved, not decided.** A concern folder is
already, by definition, where content of one kind lives; Assembly and
ecosystem between them already say everything this model needs to say
about *whose* content it is and *in what ecosystem* it is written. Whatever
internal layout a source-bearing subtree needs beneath the ecosystem
segment — its own convention for where compiled sources sit versus where
build output lands — belongs entirely to that ecosystem's own,
pre-existing convention (Cargo's own `src/`, mdBook's own `src/`+`book/`,
npm/tsc's own `src/`+`out/`), never re-decided by this model.

| Check | Type |
|---|---|
| Leaf grammar reads `<concern>/<assembly>/<ecosystem>/...`, no inserted `src`/`source` segment | pass/fail |
| Internal layout beneath the ecosystem segment follows that ecosystem's own tooling convention, not a project-invented one | pass/fail |

---

### Guard: record an Assembly's own ecosystem composition as its own decision, not an inference

Which ecosystem(s) an Assembly's real-tree source spans is a project
decision, stated once, at the point the project's own Assembly/Element
structure is recorded — not something a later reader should have to infer
from which folders currently exist on disk. An Assembly may span more than
one ecosystem at once (one already built, another decided but not yet
built); which is which is recorded explicitly, never left implicit in the
current folder listing.

| Check | Type |
|---|---|
| Each Assembly's own ecosystem composition is recorded explicitly at the project's own Assembly/Element structure node, not inferred from disk | pass/fail |

---

### Guard: Profile, Target, and Pipeline — three orthogonal build-vocabulary axes

Beyond Assembly and ecosystem, three further universal terms name a
build's own configuration, output, and execution axes:

- **Profile** — a cross-cutting build *configuration/stage* axis (e.g.
  dev / pre-release / release), orthogonal to what is being built.
  Parameterizes execution (compiler flags, signing, the output root
  beneath `dist/`) without itself belonging to any one Assembly.
- **Target** — a named build *goal/output* produced within one Assembly's
  own build corner. One Assembly's corner may host more than one Target
  side by side (e.g. a binary Target and a documentation Target from the
  same corner) — Assembly-hood never limits a corner to exactly one.
- **Pipeline** — the *ordered sequence of steps* that realizes one Target
  for one Assembly under one Profile.

**How they compose.** Profile parameterizes execution; Assembly is the
structural, build-independent unit; each Assembly's own build corner can
host multiple Targets; each Target is realized by exactly one Pipeline. The
fully general build-output shape this composition implies is
`dist/<profile>/<assembly>/<target>/...` — a project where every Assembly
happens to have exactly one Target is the degenerate case where the
`<target>` segment is invisible.

**Don'ts**
- Do not name an Assembly itself as "the Target" — a Target is what one
  Assembly's own build corner *produces*, never the Assembly itself.
- Do not let a Pipeline span more than one Assembly, Target, or Profile at
  once.

| Check | Type |
|---|---|
| Profile, Target, and Pipeline are kept as three distinct, orthogonal axes, none collapsed into another | pass/fail |
| No Assembly is itself named "the Target" | pass/fail |
| No Pipeline spans more than one Assembly, Target, or Profile | pass/fail |

---

### Guard: the marker-tier policy — `.folder` obligation scales down with depth, `shall` → `should` → `may`

A folder-descriptor's obligation is not uniform across the
enabler/Assembly/ecosystem nesting — it scales down as a folder gets more
specific:

1. **Top-level enabler folders** (`prod/`, `docs/`, `build/`, `tests/`,
   `dist/`) **shall** carry their own `.folder` marker.
2. **Assembly-level folders** (one level beneath an enabler folder)
   **should** carry one — a recommendation, not a hard obligation.
3. **Ecosystem-level folders and below** (two levels beneath an enabler
   folder, or deeper) **may** carry one — the weakest tier, left to the
   author's own judgment.

This tiering never relaxes tier one's `shall`, and it never retroactively
obligates a marker at tiers two or three where none exists today — it
states, for content newly placed at each depth, how strongly a marker is
called for there, not a mandate to backfill every folder that currently
lacks one.

| Check | Type |
|---|---|
| Every top-level enabler folder carries a `.folder` marker | pass/fail |
| A missing tier-two or tier-three marker is only flagged where a concrete reason favors adding one, never filled purely for symmetry | pass/fail |

---

## Part II — Per-enabler internal structuring

**What this tier is licensed to state.** Each subsection below derives one
enabler folder's own internal partition from Part I's general rules — it
does not introduce a competing rule of its own. Where a derivation reflects
a genuinely common pattern for that kind of enabling system, it is stated
as general, teachable pattern knowledge — never as any one project's
concrete instance of it.

### `prod/` — a workspace of code-producing Assemblies

`prod/` derives its shape directly from Part I's leaf grammar: one
Assembly-named folder per code-producing Assembly the project declares,
each carrying its own ecosystem sub-folder(s) beneath it —
`<assembly>/<ecosystem>/...`, no further segment. Which Assemblies are
present in `prod/` at all is itself a project decision, not a universal
list.

### `tests/` — mirrors whichever partition it is testing

A `tests/` folder that holds cross-Assembly test content derives the same
grammar the folder it tests uses, because test content can equally target
any source-bearing partition: `tests/<enabler>/<assembly>/<ecosystem>/...`,
where `<enabler>` names which workspace (`prod/`, `docs/`, ...) the test
content is exercising. *Whether* a project populates `tests/` this way at
all, versus co-locating test code inside each ecosystem's own in-source
test location (the more common case for a language ecosystem that already
has one, e.g. Cargo's own `tests/` inside a crate), is a per-project choice
this general shape leaves open, not something this derivation mandates.

### `build/` — flat, one corner per Assembly, plus a shared-content exemption

**The general derivation:** exactly like `prod/`, `build/` is flat —
`build/<assembly>/`, not one segment deeper — and each Assembly's own build
corner may itself be sub-divided by ecosystem
(`build/<assembly>/<ecosystem>/...`, the build corner's own ecosystem,
independent of the Assembly's own source ecosystem). One Assembly's corner
is exactly where Part I's Target vocabulary attaches: a corner may host
more than one Target, each realized by its own Pipeline.

**Made explicit: `build/`'s entire difference from `prod/` is two additions
on top of one identical base.** The `<assembly>/<ecosystem>/...` derivation
itself is the same derivation `prod/` uses, unchanged; `build/` adds exactly
two things `prod/` has no need for — the Target/Pipeline attachment point
just stated, and the shared-content exemption stated next — and nothing
else about the two folders' internal grammar differs.

**A shared-content exemption is a deliberate, general part of this shape,
not a peculiarity of any one project.** A build workspace's own
cross-Assembly shared content — build recipes, shared assets, tooling
every Assembly's Pipeline draws on — is not itself an Assembly (it is not
independently build-independent in the sense the Assembly criterion asks),
so it never carries an ecosystem segment governed by this grammar; its own
internal names stay whatever pragmatic labels the project chooses. This is
a general pattern any build workspace needs.

### `docs/` — a workspace of documentation Assemblies

**General pattern, teachable independent of any one project:** a
documentation enabling system commonly decomposes into a handful of
recognizable deliverable kinds — a **user manual** (task- and
reference-oriented, organized by feature area), a **tutorial** (a guided,
sequential walkthrough for a newcomer), **release notes** (per-version,
chronological, often generated rather than hand-authored), and a
**getting-started guide** (a short, standalone on-ramp, sometimes its own
deliverable and sometimes a first chapter of the manual). This split is
ordinary documentation-genre knowledge — the same shape a great many
software projects' own docs independently converge on.

**What stays project-specific:** *whether* each of those kinds actually
earns its own independent Assembly-level build (able to be built and
shipped as its own artifact, for instance) — as opposed to staying a
chapter inside a larger deliverable — is a per-project judgment call, not
mandated by the general pattern above. Some projects will genuinely have
only one documentation deliverable, and a single combined source-plus-
build-output pair remains an acceptable degenerate case of the same
pattern for exactly that reason.

### `saf/` and `sec/` — the same grammar would apply, if and when a real-tree folder exists

**Genuinely speculative, flagged as such rather than asserted either way:**
a project's `saf_`/`sec_` enabler content can live entirely inside its
needs-graph as analysis nodes *about* the product (safety/security
analyses), with no real-tree deliverable of their own to place under a
concern folder. Whether a qik-bootstrapped project ever needs a real-tree
`saf/` or `sec/` workspace of its own — holding, say, a
fault-tree-analysis tool's own project files, or a threat-model tool's own
— is open. **If** such a folder is ever introduced, nothing about the
general derivations above changes: it would be a workspace exactly like
`prod/`, `tests/`, `build/`, and `docs/`, holding whichever Assemblies carry
`saf_`/`sec_`-relevant real-tree content, partitioned by the same
`<assembly>/<ecosystem>/...` grammar. This subsection states that
conditional derivation, not a decision that such a folder should exist.

---

## Non-Assembly top-level folders

A small set of top-level folders may exist that were never meant to carry
an Assembly segment, or any part of the `<enabler>/<assembly>/<ecosystem>`
grammar above at all — they are not `prod/`, `tests/`, `docs/`, or
`build/`, not an enabler-concern folder in the first place. A project may
hold convenience/staging folders that sit outside the enabler/Assembly/
ecosystem grammar entirely — a top-level wrapper-script collection, a
raw-input staging area, a scaffold-template store, or similar — and that
absence from the grammar is by design, not an unmigrated gap. Each such
folder is a genuinely different kind of thing from an enabler-concern
folder, and reading its absence from the concern grammar as something a
pending migration will eventually correct is exactly the mistake this
section exists to head off.

| Check | Type |
|---|---|
| A non-Assembly convenience/staging folder is never assigned an Assembly-shaped subtree (`<something>/<ecosystem>/...`) | pass/fail |
| Its absence from the `<enabler>/<assembly>/<ecosystem>` grammar is read as by-design, not as a gap a pending real-tree migration will close | pass/fail |
