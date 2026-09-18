<!-- @needs sme_enabler_tst skill file — ISO/IEC/IEEE 29119-3:2021 test documentation expert, prd_unit_imp__thalam__sme_enabler_tst, prd_unit_imp, [prd_unit_des__thalam__sme_enabler_tst], proposed -->

# ISO/IEC/IEEE 29119 skill file — `tst_` authoring guidance + conformance checklist

Loaded by `qik-thalam-author` (Step 2, authoring guidance) and `qik-thalam-critique`
(Step 3, review checklist) when the target's enabler prefix is `tst_`.

**References:**
- ISO/IEC/IEEE 29119-1:2022 (Edition 2) — General concepts — ISO catalog 81291 — https://www.iso.org/standard/81291.html
- ISO/IEC/IEEE 29119-2:2021 — Test processes
- ISO/IEC/IEEE 29119-3:2021 — Test documentation
- ASPICE 4.0 SWE.4 (Software Unit Verification), SWE.5 (Software Integration and Integration Test), SWE.6 (Software Qualification Test) — https://www.automotivespice.com/

---

## Authoring guidance

### tst_glob_req — Test Policy (ISO 29119-1:2022 §4, 29119-2:2021 §6.3)

The test policy is the organizational mandate for testing. It must:
- State that testing is **required** for the project/product
- Name the **test levels** to be performed (unit, integration, system, acceptance)
- Define the **test approach** (risk-based, requirements-based, coverage-based)
- State the **overall exit criteria** for the test campaign

**Root node:** Every `tst_` chain must ultimately trace to the project's own designated test-policy root — a `tst_glob_req` node at the `realization` aspect that states the test policy (illustratively shaped like `tst_glob_req__realization__<test-policy-tag>`, where the tag segment is the project's own free-form choice, not a fixed schema token) — or to the project's own mission-level intent node (a `sys_int`, e.g. `sys_int__mission__<mission-tag>`). Whichever node a given project designates, it is the normative anchor for the whole `tst_` enabling system.

---

### tst_feat_req — Test Plan (ISO 29119-2:2021 §7.2, 29119-3:2021 §9)

A test plan specifies the scope and approach for testing a feature. It must:
- **Scope** — which feature or capability is being tested
- **Test approach** — techniques to be applied (equivalence partitioning, boundary value analysis, statement coverage, etc.)
- **Entry/exit criteria** — conditions that must hold before/after this test level
- **Resource requirements** — test environment, tools, dependencies
- **Traceability** — validates the parent `prd_feat_req` it covers (via `:validates:`)

---

### tst_comp_req — Test Design Specification (ISO 29119-3:2021 §10.2)

A test design specification derives test conditions from requirements. It must:
- **Test conditions** — specific conditions to be covered
- **Technique** — test design technique applied (e.g. boundary value, state transition)
- **Coverage criterion** — what counts as sufficient coverage of the requirement
- **Traceability** — verifies the parent `prd_comp_req` via `:verifies:`

---

### tst_unit_des — Test Case Specification (ISO 29119-3:2021 §10.3)

A test case fully specifies **one executable test**. It must contain all four mandatory directive blocks:

```
:::{objective}
One sentence: "Verify that <specific condition from prd_unit_des> holds when <precondition>."
:::

:::{entry_conditions}
System state required before the test begins:
- Software version X.Y.Z installed
- Configuration: <specific settings>
- Test data: <specific input files or values>
:::

:::{narrative}
Numbered procedure steps — one action per step:
1. <Action>
2. <Action>
3. Observe <output/behavior>
:::

:::{exit_conditions}
Expected results — specific and measurable:
- <Output value> equals <expected value>
- System state: <expected final state>
- Exit criterion: pass if <criterion>, fail if <criterion>
:::
```

**Critical quality checks:**
- **Objective** must reference the specific clause of the `prd_unit_des` it verifies — not "verify unit X works"
- **Entry conditions** must be reproducible — not "system running normally"
- **Procedure steps** must be deterministic — same steps, same environment → same result, every time
- **Exit conditions** must be measurable — not "output is correct" but "output equals '42'"
- **Traceability:** carries `:verifies:` link to the `prd_unit_des` or `prd_comp_req` under test

---

## Process-as-product authoring guidance (when the standard IS the subject matter)

**When this applies:** the project's system-of-interest is itself a process
governed by ISO/IEC/IEEE 29119 — e.g. modeling an organization's own test
process (its stages, workflows, roles, templates) as the deliverable — not
verifying some *other* `prd_` deliverable. All content described here is
authored as `prd_` throughout: the process definition is this project's
*product*. `tst_` stays reserved for verifying *this* project's own
deliverable (the process definition itself), a distinct, meta-level
concern — see the enabler-vs-topic guard in `qik-thalam-tutor`'s embedded
concept model (the full teaching-voice treatment) and its terse,
load-bearing restatement in `qik-thalam-author`'s and `qik-thalam-critique`'s
own hard-prohibition sections: the enabler prefix tracks whose work an
artifact is, never the topic it discusses.

Draw from this module **instead of**, not in addition to, the "Authoring
guidance" section above, whenever the target enabler's subject matter is
the standard itself. The section above assumes `tst_` is always on the
verifying side (test policy → plan → design → case, verifying some `prd_`
elsewhere); this section is the inverse direction it has zero guidance for.

The full ISO/IEC/IEEE 29119 vocabulary a process-as-product authoring pass
must draw from — every element below, not just whatever three-way split an
unaided pass happens to arrive at:

| ISO 29119 concept | Process group | `prd_` node shape | Citation |
|--------------------|----------------|--------------------|----------|
| Test objectives | Organizational (29119-2 §6.2) | `prd_feat_int` — why testing exists for this organization, what outcomes it must achieve | 29119-2 §6.2 |
| Test strategy | Organizational (29119-2 §6.3) | `prd_feat_req` — approach and techniques, **and** resource/capacity and scheduling concerns, not technique alone | 29119-2 §6.3 |
| Test plan | Test management (29119-2 §7.2) | `prd_comp_req` / `prd_comp_arc` — scope, entry/exit criteria, schedule, roles | 29119-2 §7.2, 29119-3 §9 |
| Test design | Dynamic (29119-3 §10.2) | `prd_comp_arc` / `prd_unit_des` — technique, coverage criterion, the template a designer fills in | 29119-3 §10.2 |
| Test execution | Dynamic (29119-2 §7.4, 29119-3 §10.4) | `prd_unit_des` / `prd_unit_imp` — the run procedure and its record | 29119-2 §7.4 |
| Incident reporting | Dynamic (29119-3 §11) | `prd_unit_des` — the incident/defect record template and workflow | 29119-3 §11 |
| Test completion | Test management (29119-2 §7.5) | `prd_comp_req` / `prd_comp_arc` — exit criteria, completion report, **and** the closure workflow and owning role, not the exit criteria alone | 29119-2 §7.5 |
| Test monitoring and control | Test management (29119-2, Test Monitoring and Control) | `prd_comp_req` / `prd_comp_arc` — progress-tracking criteria against the plan, and the corrective-action workflow when progress deviates | 29119-2 (Part-level only — § not verified against a licensed copy, per this house's citation-honesty policy) |
| Test environment set-up and maintenance | Dynamic (29119-2, Test Environment Set-Up and Maintenance) | `prd_comp_req` / `prd_comp_arc` — readiness criteria the environment must meet, and the provisioning/maintenance workflow that keeps it fit for purpose across a campaign | 29119-2 (Part-level only — § not verified against a licensed copy, per this house's citation-honesty policy) |

Two rows above (monitoring and control; environment set-up) were added
after this table's original seven — added once the corpus grew to a full
nine-stage build-out and a real authoring pass had no row to check
against for either. Their citation is deliberately held at Part-level
only, unlike the original seven's specific §s, which predate this house's
citation-honesty policy and have not been retroactively re-verified
either — do not treat the original seven's specific §s as more trustworthy
than these two's Part-level citation; neither has been checked against a
licensed copy.

**Coupled-shall citation rule:** a single "shall" clause spanning two
standard parts — e.g. "name a role" is a 29119-2 process-ownership concern,
"provide a template" is a 29119-3 documentation concern — must cite **both**
parts in its rationale, or explicitly name which part is deliberately not
addressed and why. Citing only one part when the shall genuinely spans two
is a standards-fidelity gap, not a style nit: confirmed independently by
two reviewers (`qik-thalam-critique` and `pharaoh:sphinx-needs-expert`)
during dogfooding as a real ISO 29119 Part mis-citation.

**Who draws from this module:** `qik-thalam-author` (drafting),
`qik-thalam-tutor` (when self-substituting for author per the nested-dispatch
relay fork), and `qik-thalam-critique` (reviewing) — all three,
whenever the target enabler's subject matter is the standard itself, not
just whichever persona happens to be authoring.

---

## Review checklist

Apply one indicator at a time; emit one finding per indicator.
Do not apply indicators marked n/a for the target's point type.



### SC-29119-01 — Campaign mandate (mechanized, pass/fail)

**Check:** Does the project's own designated `tst_glob_req` test-policy root
node exist in the project's needs graph? Use
`axon_list(select=["enabling_system=tst", "scope=glob", "layer=req"])` to
enumerate `tst_glob_req` candidates, then identify the project's own root
among them (the one nothing above it in the `tst_` chain refines further, or
the one the project's own convention designates — e.g. an id shaped like
`tst_glob_req__realization__<test-policy-tag>`, illustrative only).

**Pass:** At least one such root node exists and is at status `approved` or
`released`.
**Fail:** The node is absent or `draft`/`proposed` only.
**Rationale (ISO 29119-3 §8.2):** A test policy establishes the mandate for
the whole campaign. Without a root node stating that testing is required, the
`tst_` row has no normative anchor.

---

### SC-29119-02 — Chain completeness (mechanized, pass/fail)

**Check:** For the target artifact, does the upward chain reach the project's
own designated test-policy root (the `tst_glob_req` identified at SC-29119-01)
without gaps? Use `axon_trace` on the target id.

Walk the `refines`/`fulfils`/`implements` chain upward. Verify:
- A `tst_unit_des` reaches a `tst_comp_arc` via `fulfils` and a `tst_comp_req`
  via `implements`.
- A `tst_comp_req` reaches a `tst_feat_req` or mission-level need via
  `refines`.
- A `tst_feat_req` reaches a `tst_glob_req` or mission-level need via
  `refines`.

**Pass:** Chain is unbroken and terminates at the project's own test-policy
root node (a `tst_glob_req`) or at the project's own mission-level intent
node (a `sys_int`) or another approved mission-level need.
**Fail:** Any link in the chain is missing or points to a node with no
further upward trace.

---

### SC-29119-03 — Verification link (mechanized, pass/fail)

**Applies to:** `tst_comp_req`, `tst_unit_des`

**Check:** Does the artifact carry a `verifies` link to a `prd_comp_req`,
`prd_unit_des`, or mission-level need?

**Pass:** Link present and the target resolves to an existing node.
**Fail:** `verifies` link absent or target dangling.
**Rationale (ISO 29119-3 §10.2, ISO 15288 §6.4.6):** Verification establishes
that a specified requirement is met. Without the `verifies` link, no evidence
claim is possible.

---

### SC-29119-04 — Validation link (mechanized, pass/fail)

**Applies to:** `tst_feat_req`

**Check:** Does the artifact carry a `validates` link to a `prd_feat_req` or
mission-level need?

**Pass:** Link present and the target resolves.
**Fail:** `validates` link absent or target dangling.
**Rationale (ISO 29119-3 §9.2, ISO 15288 §6.4.9):** Validation at feature
scope must name one stakeholder-visible behavior as its target.

---

### SC-29119-05 — Link-type exclusion (mechanized, pass/fail)

**Check:** Does the artifact carry any forbidden link type for its point?

| Point | Forbidden link types |
|-------|---------------------|
| `tst_glob_req`, `tst_glob_arc` | `verifies`, `validates` |
| `tst_feat_req` | `verifies` (only `validates` permitted) |
| `tst_feat_arc` | `verifies`, `refines` |
| `tst_comp_arc` | `validates`, `refines` |
| `tst_unit_imp` | `fulfils`, `refines`, `validates` |

**Pass:** No forbidden link present.
**Fail:** Any forbidden link found; cite the specific link type and target.

---

### SC-29119-06 — Body structure completeness (mechanized, pass/fail)

**Applies to:** `tst_unit_des` only

**Check:** Does the `tst_unit_des` body contain all four required directive
blocks from the `tst_case` Sphinx extension?

Required blocks (per `sys_req__concept__tst_unit_des_body_structure`):
`objective`, `entry_conditions`, `narrative`, `exit_conditions`

Use `Read` on the source file at the location returned by `axon_show`.

**Pass:** All four block types present and non-empty.
**Fail:** Any required block absent or empty; cite the missing block names.

---

### SC-29119-07 — Implementation coverage (subjective, 0–3)

**Applies to:** `tst_unit_des`

**Check:** Does a `tst_unit_imp` node exist that implements this `tst_unit_des`?

**Scoring:**
- 3 — `tst_unit_imp` exists, is scanned from a real CI artifact, and carries
  no `status: draft`.
- 2 — `tst_unit_imp` exists but is `proposed` (placeholder authored, not yet
  scanned from a real artifact).
- 1 — `tst_unit_imp` absent; `tst_unit_des` is design-only.
- 0 — `tst_unit_des` is `released` with no `tst_unit_imp`: a released
  specification with no evidence of implementation.

**Rationale (ISO 29119-3 §10.4, ISO 15288 §6.4.6.3):** Verification requires
executable evidence. A design without a corresponding implementation artifact
cannot produce that evidence.

---

## Output format

For each indicator that applies, emit:

```
SC-29119-XX | <pass|fail|N/3> | <one-line justification> | [file:line]
```

For non-applicable indicators (wrong point type), record:

```
SC-29119-XX | n/a | Not applicable to <point_type>
```

Aggregate at the end: overall pass/fail and list of failed indicator ids.
