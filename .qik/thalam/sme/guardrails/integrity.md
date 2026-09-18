<!-- @needs sme_guardrails skill file — graph-integrity guards shared by every thalam persona, prd_unit_imp__thalam__sme_guardrails, prd_unit_imp, [prd_unit_des__thalam__sme_guardrails], released -->

# sme_guardrails (integrity) — cross-cutting graph-integrity knowledge shared by every thalam persona

**Lives at `.qik/thalam/sme/guardrails/integrity.md` — deliberately neither under `.claude/`
nor under `.github/`.** Every other thalam procedure/persona file is
platform-specific by design (a Claude Code `SKILL.md`/`.md` agent file, a
GitHub Copilot `.prompt.md`/`.agent.md` file — different formats, different
runtimes, one per platform). The knowledge in *this* file is not: it is the
same fact regardless of which platform's persona is asking, so it lives once,
in qik's own neutral namespace, and both platforms' persona files `Read` it
by the same absolute-from-repo-root path rather than each carrying a private
copy. Platform parity guarantees `.claude/` and `.github/` are
always scaffolded together as one mandatory bundle — never one without the
other — so a cross-directory reference from either platform into `.qik/`
never dangles.

**Scope: integrity, not presentation.** This file checks whether the graph
itself is correct — enabler classification, marker hygiene. How content is
*organized for a reader* (top-level menu, per-Assembly/Element sidebar
ordering) is a distinct concern, checked by the sibling
`.qik/thalam/sme/guardrails/presentation.md` — an Information Architecture
persona, not this one. The two used to share one file; they were split so
neither guard set overloads the other with an unrelated responsibility.

Loaded by `qik-thalam-tutor` (when teaching the concept model), `qik-thalam-author`
(Step 2, before finalizing an enabler tag), `qik-thalam-critique` (applying the
three lenses), and every `sme_enabler_*.md` file (content-gate check) alike —
on both platforms. This file is the single source for guards that cut across
all of them — no persona file or SME file restates one in full; each
references this file by name.

---

## Guard: enabler tracks whose work, never the topic discussed

The enabler prefix (`sys_`/`prd_`/`tst_`/`doc_`/`bld_`/`saf_`/`sec_`) answers
*whose work an artifact is* — never *what topic the content happens to
discuss*. This single confusion recurs in three distinct directions; check
all three, not just the one direction that comes to mind first.

**Direction 1 — a product *about* another enabler's topic still stays its
own enabler.** A project whose own deliverable is a test tool, a test
process, or test documentation still classifies that deliverable under
`prd_` (or whichever enabler its delivery actually is) — the word "test"
appearing in the subject matter is never itself a reason to reach for
`tst_`. `tst_` is reserved for verifying *this* project's own deliverable,
whatever that deliverable is. The confusion is easiest to make precisely
when a project's own delivered subject matter already legitimately talks
about testing — e.g. a project whose system-of-interest is itself a test
tool or a test process — since the topic word is present in the content
for a reason that has nothing to do with who is doing the verifying.

**Direction 2 — genuine verification content filed under the deliverable's
own enabler instead of `tst_`.** A node whose content is fundamentally a
test suite, test vectors, or verification evidence for a
`prd_`/`bld_`/`doc_`/etc. deliverable is `tst_`, `:verifies:`/`:validates:`-
linked back to that deliverable — never authored under the deliverable's
own enabler with an `:implements:` link, no matter which requirement or
cluster it attaches to. This is not direction 1 (no topic-word confusion)
and not direction 3 below (no fabrication) — it is the plain case: real
verification content, filed under the wrong enabler, with no confusion or
fabrication involved, just an unchecked default. A typical instance: an
integration-test suite for a component's own CLI or API, authored under
that component's own enabler with an `:implements:` link, when its actual
content — test cases, fixtures, pass/fail criteria — makes it `tst_` with
a `:verifies:` link instead.

**Direction 3 — a fabricated `tst_` wrapper manufactured to give a mandate
node something to point at.** A subtler recurrence: every node stays
correctly typed (`tst_` is never misfiled as `prd_` or vice versa), but a
`tst_feat_req`/`tst_comp_req`/`tst_comp_arc`/`tst_unit_des` chain gets
manufactured that restates an existing `prd_` requirement's shall clause
under borrowed ISO/IEC/IEEE 29119-3 test-technique vocabulary
(specification-based technique, coverage criteria, entry/exit criteria) —
not to verify anything genuinely falsifiable, but solely to give the
project's fixed `tst_glob_req` mandate nodes a downstream link. Symptom: a
`tst_comp_req`'s body is near-verbatim the same shall as its sibling
`prd_comp_req`. If the project's deliverable is non-executable
(documentation, a process definition, a template), checking that an
authored work product satisfies its own requirement is a quality-assurance
concern (ASPICE SUP.1, https://www.automotivespice.com/), not a `tst_`
matter — route it to the house's quality-assurance process instead. A
mandate node with nothing genuinely executable to verify does not stay a
standing, never-closing warning either: declare it explicitly
not-applicable in the mandate node's own body, and exempt it from
`req-must-have-downstream-arc`/`-proposed` via a project-**local**
`except_from_id` in that project's own `.qik/axon/rules.toml` (never in
qik's shared template — this is a per-project determination, not a
house-wide one).

**How to check, regardless of which persona is checking:** ask, stripped of
its id, would this node's actual content — what it says, not what it is
attached to or which requirement it implements — independently read as
this enabler's own kind of work? If it would read as a different enabler's
work instead, that is one of the three directions above, not a reason to
force-fit the content into the enabler it happened to be filed under.

---

## Guard: never reproduce a codelinks marker

A fully-formed sphinx-codelinks one-line marker — the comma-separated
payload carrying title, id, type, `[links]`, status behind the `@needs `
start sequence — must never be reproduced anywhere as an example or
illustration, in any node body, prompt, or output. Naming the bare token to
describe the syntax is fine; reproducing an instance that carries a real id
is forbidden.

**Why it is severe.** sphinx-codelinks scans every configured `src_dir` for
that start sequence and mints an `*_unit_imp` need from every match. A
marker written as an example, sitting in a scanned tree, mints a phantom
node under an id that already belongs to a real source marker — a
duplicate manufactured out of documentation. Whether the tree written into
happens to be scanned today is not the test: one `src_dir` or
`comment_type` edit in `needs/conf.py` arms every reproduced marker in the
corpus at once — report it as latent even where nothing currently scans
that path.

Where a node's subject *is* the marker convention itself, state the shape
with placeholder segments and no real id, or describe it in prose.
