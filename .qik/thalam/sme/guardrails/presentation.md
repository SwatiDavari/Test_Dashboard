<!-- @needs sme_presentation skill file — Information Architecture / navigation guards shared by every thalam persona, prd_unit_imp__thalam__sme_presentation, prd_unit_imp, [prd_unit_des__thalam__sme_presentation], proposed -->

# sme_presentation — Information Architecture expert, shared by every thalam persona

**Lives at `.qik/thalam/sme/guardrails/presentation.md`, a sibling of
`integrity.md`** — same platform-neutral home and same "read once, never
restated per persona" discipline (see `integrity.md`'s own header for why
that home). Split from `integrity.md` deliberately: this file's concern is
whether the graph's content is *organized so a reader can find it*
(navigation, menus, hierarchy) — an Information Architecture question,
distinct from `integrity.md`'s graph-correctness question (enabler
classification, marker hygiene). Folding both into one file would overload
it with two unrelated responsibilities.

**The persona this file carries:** an **Information Architect** — the
professional role you would actually hire for this concern (Rosenfeld &
Morville, *Information Architecture for the Web and Beyond*, is the field's
standard reference; ISO 9241-210 Human-centred design for interactive
systems is the normative grounding), the same way `sme_enabler_prd` carries
an ISO/IEC/IEEE 29148 requirements-engineering expert. Organizing content
into a findable, navigable hierarchy — not visual design, not graphic UI —
is this persona's craft.

Loaded by `qik-thalam-author` (when authoring or reordering a toctree, or a
project's own hand-written navbar/sidebar template) and `qik-thalam-critique`
(auditing a toctree or rendered menu/sidebar) alike — on both platforms.
This file is the single source for these five guards; no persona file
restates any in full.

---

## Foundational concept: System-of-Interest → System / Assembly / Element (concise — full derivation lives in `placement.md`)

`placement.md`'s own foundational-concept section derives this in full,
including its ISO/IEC/IEEE 15288 grounding; restated here only to the depth
this file's own navigation guards need, since every one of them below
organizes content by Assembly and, within it, Element. ISO/IEC/IEEE 15288
separates a project's **system-of-interest** — the system whose life cycle
is under consideration, the thing actually built and delivered — from the
**enabling systems** that support that life cycle without themselves being
the delivered thing. A project decomposes its own system-of-interest, at
the top, into **Assemblies**: project-declared groupings defined by exactly
one criterion, build-independence (each with its own build entry point and
output) — the one decomposition level directly beneath the system-of-interest
itself. Each Assembly's own top-level structural component is an
**Element** — the first level of structural decomposition directly beneath
that Assembly; finer components remain components of their owning Element,
never themselves promoted to Element or Assembly status. **System** names
the system-of-interest viewed at the top, before any Assembly-level
decomposition — a project's own mission, concept model, and general
realization paradigms, none of it scoped to one Assembly; this is exactly
what the main-menu guard's fixed `System { Mission, Concept, Realization }`
slot names below, and exactly why every other guard in this file organizes
content by Assembly and, within it, Element, never by any finer or coarser
grouping.

**Enabler, Scope, and Layer are three further, separate axes this file's
own guards lean on without redefining.** **Enabler**
(`sys`/`prd`/`tst`/`bld`/`doc`/`saf`/`sec`) names *whose* work an artifact
is — the main-menu and navigation-ordering guards below both sort by it.
**Scope** (`glob`/`feat`/`comp`/`unit`) names the decomposition grain within
one Element — the navigation-ordering guard's own three tiers (`glob`-scope
tier, `Features` tier, Element tier) are a direct reading of this axis.
**Layer** (`int`/`req`/`arc`/`des`) names the abstraction level from
intention to code — the `Intention`/`Requirement`/`Architecture`/`Design`
groupings throughout this file are it. Each axis is fully defined in its own
dedicated files — `.qik/thalam/sme/enabler/*.md`, `.qik/thalam/sme/scope/*.md`,
`.qik/thalam/sme/layer/*.md` — not restated here.

---

## This file's own formula, and how it differs from `structure.md`'s and `placement.md`'s

`presentation.md`, `structure.md`, and `placement.md` all reason over the
same building blocks (System, Assembly, Element, Ecosystem, Enabler, Scope,
Layer) — none invents a vocabulary the other two do not share. What
distinguishes them is that each composes those same blocks into a different
ordered path, for a different purpose:

- **This file (`presentation.md`), reader-facing navigation:** two
  distinct orderings, stated in full by the two guards immediately below —
  a main-menu formula, `System, <enabler-with-content>..., Distribution`,
  and, one level down, a per-enabler sidebar formula,
  `<enabler>/<assembly>/{glob-scope tier, Features tier, Element tier}`.
- **`structure.md`, real-tree source location:**
  `<enabler>/<assembly>/<ecosystem>/...` — Enabler-first, like this file's
  own sidebar formula, but composed for a build toolchain's own leaf
  grammar rather than for a reader's own findability.
- **`placement.md`, needs-tree file location:**
  `<assembly>/<element>/<enabler>/<scope>/<layer>/...` — Assembly/Element
  first instead, so one module team's whole artifact graph sits under one
  subtree root it owns without interference.

Same seven building blocks, three different orderings for three different
purposes — not three unrelated concept sets that merely happen to share
some words.

---

## Guard: top-level main menu — System, one slot per enabler-with-content, Distribution

Distinct from the guard below: this one governs the **outermost** menu — the
navbar/landing-page entry points a reader meets *before* choosing an enabler
and descending into the enabler → Assembly → tier structure the next guard
orders.

1. **`System { Mission, Concept, Realization }`** — one fixed slot, same
   content in every project.
2. **`<Enabler> { <assembly>... }`** — one slot per Element-bearing enabler
   spelled out in full (Product, Safety, Security, Test, Documentation,
   Build), listing only the Assemblies that actually carry content for that
   enabler. **A slot is omitted entirely — not rendered empty — when no
   Assembly has content for it**; add the slot the day the enabler gets its
   first need, don't pre-render it empty in anticipation.
3. **`Distribution { <profile>... }`** — one slot listing delivery/packaging
   profiles, never Product's Assembly list, even where a profile and an
   Assembly happen to name the same target: one is a build-independence
   grouping, the other a delivery/packaging concern, and the two axes stay
   distinct even when their names coincide.

**Fixed order**: `System`, then `Product, Safety, Security, Test,
Documentation, Build` (skipping any enabler with no content), then
`Distribution` last.

**Why this order differs from the next guard's `prd, tst, bld, doc, saf,
sec` — know this, don't flag it as a contradiction to reconcile.** The two
guards serve two different readers at two different depths. This guard's
order is a first-contact orientation narrative: `Product` (the
system-of-interest) first, then `Safety`/`Security` (analyses *about* that
product), then `Test` (validates the product and its safety/security
posture), then `Documentation` (describes the validated product), then
`Build` (manufactures/packages it last, right before `Distribution` ships
it). The next guard's order answers a narrower question — how to sort one
already-chosen enabler's own Assembly/Element content — and is free to keep
its own production-pipeline rationale unchanged. `qik-thalam-critique`: a
main-menu structure that borrows the *other* guard's enabler order (or vice
versa) is not itself a defect — check each structure against its own guard,
not against the other one's order.

---

## Guard: navigation ordering — enabler → Assembly → {glob-by-layer, Features-flat, Element-by-type}

Every `needs/**/index.md` (or equivalent, e.g. `*-index.md`) toctree — the
source-of-truth for navigation, not just its rendered form — follows this
fixed order. An Assembly/Element structural level, once a project has one,
adds a fourth axis navigation has to place beyond a flatter
`enabler → scope → layer` sort; the order below is the one that places it:

1. **Enabler**, outermost, closed order `prd, tst, bld, doc, saf, sec`
   (`sys_` excluded — mission-area content is not Element-bearing, it is
   navigated separately via its own three-aspect, layer-only structure).
   Navigation-specific pipeline reasoning: `prd_`/`saf_`/`sec_`/`doc_` are
   facets of the product, `tst_` validates them, `bld_` packages everything
   and always sorts last — deliberately distinct from whatever general
   classification order a project's own concept documentation uses for
   these same enablers elsewhere.
2. Within one enabler, **Assembly**, in the project's own declared order.
   An Assembly with nothing for the current enabler does not appear at all
   — no empty heading.
3. Within one Assembly, **exactly three tiers, always in this order, never
   flattened into one lexicographic scope sort**:
   - **`glob`-scope tier**: every `glob`-scope need of that enabler, grouped
     by layer only — `Intention`s, `Requirement`s, `Architecture` — never
     grouped by Element, since `glob`-scope content states a property of
     the Assembly as a whole. A layer with no `glob`-scope content for this
     enabler is omitted, the same content-gate applied everywhere in this
     ordering.
   - **`Features` tier**: every `feat`-scope need of that enabler, a single
     flat list mixed across every Element, not further split by Element and
     not further split by layer either — `feat` stays element-agnostic for
     a different reason than `glob` does: it states one user-facing
     capability's own behavior, not the Assembly's own governance.
   - **Element tier**: every `comp`+`unit` need, grouped by Element (the
     Assembly's own declared order), and within one Element by type —
     `Component` (the scope-object anchor), `Requirement`s, `Architecture`,
     with `Design` nested inside the `Component` grouping it belongs to
     rather than standing as a fourth flat peer — except where the Element
     carries no `Component` anchor at all, in which case `Design` stays its
     own sibling category alongside `Requirement`s and `Architecture`, since
     there is no `Component` grouping to nest it into. An Element with
     nothing for the current enabler is skipped.
4. `imp` is never an entry at any tier — scanned, not navigated.

**Why three tiers replaced the flat `glob, feat, comp, unit` scope sort —
know this, don't just apply it.** A strict lexicographic scope order,
applied uniformly, forces a choice that loses something either way: sort
`glob`/`feat` first as one long undifferentiated block before any Element
appears, and a reader loses the "which Element does this belong to"
context exactly where `comp`/`unit` content would have supplied it; sort
per-Element instead, and the Assembly's own aggregate, whole-picture story
(what does this Assembly commit to, overall) gets buried piecemeal inside
each Element's own section, never visible as one thing. Collapsing
`comp`+`unit` into one Element-resolved "detail" tier keeps that half of
the fix; splitting `glob` and `feat` from one another, rather than merging
them into one shared "big picture" tier, is the further refinement this
guard adopted after first trying the merged form: `glob`-scope content
states a property of the Assembly as a whole (platform-level policy,
whole-product architecture) — genuinely about no single Element or
Feature — while `feat`-scope content states one user-facing capability's
own behavior, a different kind of claim entirely, about what one Feature
does rather than what the whole Assembly's platform commits to. Merging
both under one shared `Intention`/`Requirement`/`Architecture` heading, as
first tried, conflated those two questions under one label. Three tiers
give a reader three altitudes on purpose: the Assembly's whole-platform
commitments (`glob`-scope tier), one Feature's own behavior (`Features`
tier), then one Element's own detail (Element tier) — matching how a
reader actually approaches an unfamiliar Assembly, not an artifact of the
file layout. `qik-thalam-critique`: this is the fact to check a navigation
structure against — a toctree that instead sorts strictly by scope
regardless of Element, that scatters `glob`-scope content across
per-Element sections, or that re-merges `glob` and `feat` under one shared
heading, is the defect this guard exists to catch, not a stylistic
variant.

**No duplicate entries.** The same target file or caption shall not appear
twice in one toctree — check this whenever finalizing or reviewing an
`index.md`.

**Where this bites in practice.** A toctree accretes entries in whatever
order nodes were authored, not in coordinate order — every
`qik-thalam-author` finalization that adds a new node shall insert it at
its correct position in the three-tier structure above, not append it at
the end. `qik-thalam-critique` shall flag a toctree found out of order,
missing the three-tier split, or carrying a duplicate as a structural
defect on the same file, the same way a misplaced source file is flagged.
`qik-thalam-tutor` shall teach this three-tier ordering when introducing a
new project to its own `index.md` convention, so a project starts with the
current convention rather than needing a later cleanup pass.

---

## Guard: System-aspect sidebar isolation — quick-access row, then that aspect's own two tiers only

Distinct from both guards above: this one governs the `System` slot's own
sub-navigation once a reader has picked one mission-area aspect (Mission,
Concept, Realization).

1. **A flat, cross-aspect quick-access row** — `Mission | Concept |
   Realization` — with the active one visually distinguished (not merely
   marked in the DOM; a reader must be able to *see* which aspect they are
   in at a glance).
2. **Below it, the active aspect's own two tiers only, never a sibling
   aspect's content**: tier one is layer (`Intention`, `Requirement`,
   `Architecture`, `Design` — content-gated, a layer with nothing for this
   aspect is omitted); tier two is that layer's own needs (or the files
   grouping them), filtered to ids whose segment 2 names *this* aspect.

**Why isolation, not the generic "show the whole branch, collapse
siblings" pattern a site-navigation renderer defaults to.** Mission, Concept
and Realization are not nested levels of one tree — they are three
independent, equally-weighted aspects. A renderer's stock behavior (active
branch expanded, siblings shown collapsed alongside it) reintroduces exactly
the failure mode this guard forbids: showing System as a whole instead of
the one aspect a reader chose. `qik-thalam-critique`: a System-aspect page
whose sidebar lists the other two aspects' own titles anywhere below the
quick-access row — even collapsed, even without their children shown — is
the defect this guard exists to catch. The mechanical tell: each aspect's
own index page must be an independent top-level toctree root — the moment
two aspects share one toctree parent block, the stock-renderer
sibling-bleed reappears.

**Genuinely separate documents, not `##` headings, make the second tier
real.** The same lesson the enabler/Assembly/Element sidebar guard above
already states: an aspect's `Intention`/`Requirement`/`Architecture`/
`Design` groupings must each be their own file that the aspect's own index
page toctrees into — a single file with `##` headings and inline toctree
blocks renders as one flat list in the sidebar, not a real second tier.

---

## Guard: Assembly sidebar isolation — quick-access row, then that enabler's active Assembly's own three tiers only

Distinct from all three guards above: this one governs an Element-bearing
enabler's own sub-navigation once a reader has picked one Assembly from
that enabler's `<Enabler> { <assembly>... }` slot — the Assembly-level
counterpart to the System-aspect sidebar guard immediately above, one level
down the menu.

1. **A flat, cross-Assembly quick-access row** — the enabler's own
   content-gated Assembly list (only the Assemblies that actually carry
   content for the active enabler; the rest omitted) — with the active
   Assembly visually distinguished (not merely marked in the DOM; a reader
   must be able to *see* which Assembly they are in at a glance).
2. **Below it, the active Assembly's own three tiers only, never a sibling
   Assembly's content**: tier one is the navigation-ordering guard's
   `glob`-scope tier (`Intention`, `Requirement`, `Architecture`,
   content-gated, no Element grouping); tier two is that guard's `Features`
   tier (every `feat`-scope need, a single flat list mixed across
   Elements); tier three is that guard's Element tier (`Component`,
   `Requirement`s, `Architecture`, per Element, with `Design` nested inside
   the `Component` grouping it belongs to rather than sitting beside it as
   a fourth peer entry — except where the Element carries no `Component`
   anchor at all, in which case `Design` stays its own sibling category, per
   the navigation-ordering guard's own conditional above).

**Why isolation, not the generic "show the whole branch, collapse
siblings" pattern a site-navigation renderer defaults to.** An Assembly is
not a nested level of another Assembly — Assemblies are independent,
equally-weighted groupings within one enabler. A renderer's stock behavior
(active branch expanded, siblings shown collapsed alongside it) shows
"the whole enabler" rather than the one Assembly a reader chose — the same
argument the System-aspect guard above makes for Mission/Concept/
Realization, generalized here to every enabler's own Assembly set.
`qik-thalam-critique`: an enabler page whose sidebar lists another
Assembly's own titles anywhere below the quick-access row — even
collapsed, even without their children shown — is the defect this guard
exists to catch.

A further, nested Element-level quick-access row — a switcher one level
below the Assembly quick-access row, letting a reader jump directly between
Elements within the active Assembly — is a legitimate future refinement of
this guard's own tier-two description, not something every implementation
must already have; its absence is not itself a defect this guard flags.

---

## Guard: Distribution — deliberately unstructured

Distinct from all four guards above, and deliberately the odd one out: this
section states what does *not* apply to Distribution's own sub-navigation,
not a structure to check every project's Distribution content against.
Distribution is one of the top-level menu segments the Main-Menu guard
above already names — the `Distribution { <profile>... }` slot.

**No required quick-access row, no required tier structure — unlike
Product/Test/Build/Documentation.** A delivery/packaging profile is not an
Element-bearing enabler, so nothing in the enabler → Assembly → tier model
the two guards above govern applies to it. A flat page listing a profile's
own content directly — no per-profile switcher, no split into
`glob`-scope/`Features`/Element tiers — is a legitimate shape for this
segment, not a gap to remediate by force-fitting the Assembly-sidebar-
isolation guard's own tier structure onto a fundamentally different kind of
content.

**A project's own Distribution content may still grow its own internal
navigation later.** If and when it does, that project's own design pass —
not this guard — decides its shape; inventing a shape here, ahead of any
real content that would need it, is not this guard's job.

**`qik-thalam-critique`: do not flag this absence as a defect.** The
Assembly-sidebar-isolation and navigation-ordering guards above govern
Product/Test/Build/Documentation — the Element-bearing enablers whose
content is organized enabler → Assembly → tier. Distribution is not one of
those: it is a delivery/packaging concern, structurally outside the
enabler → Assembly → tier model those two guards govern. A Distribution
page missing Element-quick-access or tier isolation is not a violation of
either guard — neither guard's scope reaches this segment at all.
