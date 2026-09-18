# ISO/SAE 21434 skill file — `sec_` authoring guidance + conformance checklist

<!-- @needs sec_ SME enabler skill file, prd_unit_imp__thalam__sme_enabler_sec, prd_unit_imp, [prd_unit_des__thalam__sme_enabler_sec], released -->

Loaded by `qik-thalam-author` (Step 2, authoring guidance) and `qik-thalam-critique`
(Step 3, review checklist) when the target's enabler prefix is `sec_`.

**Reference:** ISO/SAE 21434:2021 (Edition 1), Road vehicles — Cybersecurity engineering
- ISO catalog 70918 — https://www.iso.org/standard/70918.html
- §10: Concept — Threat Analysis and Risk Assessment (TARA)
- §11: Product development — cybersecurity requirements
- §14: Verification — cybersecurity testing

**Note:** ISO/SAE 21434:2021 is currently under systematic review (90.20); 2021 edition remains current.

---

**Content gate — verify before applying anything below.** This file
applies only when the target node's content genuinely *is* cybersecurity
engineering — threat analysis, security goals, security requirements — not
merely attached to a `sec_` parent. The product behavior that satisfies
these is `prd_`. Ask: stripped of its id, would this node's actual content
read as security analysis, or as some other enabler's work instead (the
enabler-vs-topic guard). If it reads as something else, do not
force-fit it here — reject it and report the mismatch back as a design
error, the same way `qik-thalam-author`'s and `qik-thalam-critique`'s own
hard-prohibition sections do.

## Authoring guidance

### sec_feat_req — Cybersecurity Goal (ISO/SAE 21434 §10)

A cybersecurity goal expresses a high-level security objective derived from TARA. It must:
- **Reference the asset** and the threat scenario it addresses
- **State the cybersecurity property** affected: Confidentiality, Integrity, Availability, or Authenticity (CIAA)
- **Carry a CAL assignment** (Cybersecurity Assurance Level 1–4, derived from impact × attack feasibility in TARA)
- Use **shall-form**

**Form:** "The system shall protect [asset] against [threat scenario] to maintain [CIAA property] (CAL [N])."

**NOT a cybersecurity goal:** Technical control measures (encryption algorithms, access control lists) — these belong at `sec_comp_req`. A cybersecurity goal operates at the item level, specifying what to protect, not how.

---

### sec_comp_req — Cybersecurity Requirement / Control Measure (ISO/SAE 21434 §11)

A cybersecurity requirement specifies the control measure applied to a system element. It must:
- **Name the control measure** (cryptographic protection, access control, secure boot, message authentication code, intrusion detection, etc.)
- **Name the system element** applying it
- **State the CAL** allocated to that element
- **Be verifiable** — carry an acceptance criterion
- **Trace via `:refines:`** to the parent cybersecurity goal (`sec_feat_req`)

---

### sec_comp_arc — Cybersecurity Concept (ISO/SAE 21434 §10.5)

The cybersecurity concept allocates cybersecurity goals to architectural elements:
- **Names trust boundaries** and communication channels
- **Specifies control measures** per element and interface
- **States CAL allocation** per element
- Notes **key management** and **secure channel** requirements where applicable
- Traces via `:fulfils:` to the parent cybersecurity requirement

---
that already carries the equivalent meaning here (see SC-CS-01 below).

- `sys_req__concept__sec_enablers` — `sec_` scopes/layers (glob/feat/comp
  req+arc, plus bare `sec_comp`; no `int`, no `unit`, no AoU shape).
- `sys_arc__concept__saf_sec_relation_shapes` — `mitigates` (req → arc),
  `violates` (arc → prd_/sys_ arc); `covers` never applies to `sec_`.
- `.qik/axon/rules.toml` rules `sec_glob_req-must-refine`,
  `sec_feat_req-must-refine`, `sec_comp_req-must-refine`,
  `sec_glob_arc-must-fulfil`, `sec_feat_arc-must-fulfil`,
  `sec_comp_arc-must-fulfil`, `sec_arc-must-have-incoming-mitigates`,
  `need-id-naming`, `need-id-type-match`.

This checklist does not check `violates`: that relation shape is sketched in
`sys_arc__concept__saf_sec_relation_shapes` but has no `needs_links`/rule
entry yet (deferred wiring) — auditing it here would enforce structure the
graph itself does not yet apply.

## Indicators

| ID | Name | Type | Pass rule |
|---|---|---|---|
| SC-CS-01 | cs_rm01_risk_management | mechanized, arc-layer only | The `sec_*_arc` carries at least one incoming `mitigates` link from a same-scope `sec_*_req`, satisfying `sec_arc-must-have-incoming-mitigates` — the identified risk (this analysis element) has an identified management action (the mitigating requirement). Record `result: null` for req-layer nodes and bare `sec_comp` — the risk-management pairing is checked from the arc side, mirroring how the analogous rule is `reverse`-oriented in `.qik/axon/rules.toml`. |
| SC-CS-02 | cs_traceability | mechanized | req-layer: carries a `refines` link satisfying its scope's rule (`sec_glob_req-must-refine` / `sec_feat_req-must-refine` / `sec_comp_req-must-refine`). arc-layer: carries a `fulfils` link satisfying its scope's rule (`sec_glob_arc-must-fulfil` / `sec_feat_arc-must-fulfil` / `sec_comp_arc-must-fulfil`). |
| SC-CS-03 | cs_unique_id | mechanized | `id` matches the `sec_` alternative of the `need-id-naming` rule's `id_pattern`: `^sec_(glob_(req\|arc)\|feat_(req\|arc)\|comp_(req\|arc)\|comp)__[a-z][a-z0-9_]+__[a-z0-9_]+$`. `need_type` matches the id's leading segment, per `need-id-type-match`. |
| SC-CS-04 | cs_threat_analysis_adequacy | subjective, 0–3 | 3 = the node's content describes a concrete cyber-threat scenario — attack vector, affected asset, and impact all named; 0 = no threat context stated at all, only a generic assertion. |
| SC-CS-05 | cs_risk_treatment_rationale | subjective, 0–3 | 3 = the mitigating `sec_*_req` (or the arc's own content, when read together with it) states the chosen risk treatment — accept/mitigate/avoid/transfer — with explicit justification; 0 = no treatment rationale present, only the bare `mitigates` link. |

## Emitting a finding

One finding per indicator, in the same shape for both mechanized and
subjective rows: the indicator `ID`/`name`, a `pass`/`fail` (mechanized) or
`0`–`3` score (subjective), and a one-line justification citing the concrete
field, link, or rule id the judgement rests on. Use `null` (not a score) only
where this table says an indicator does not apply to the target's layer.
