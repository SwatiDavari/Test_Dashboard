<!-- @needs sme_enabler_bld skill file — delivery engineering expert, prd_unit_imp__thalam__sme_enabler_bld, prd_unit_imp, [prd_unit_des__thalam__sme_enabler_bld], proposed -->

# sme_bld — Delivery Engineering Expert

**Load trigger:** enabler prefix `bld_`  
**References:** Bazel (https://bazel.build), CMake (https://cmake.org), GNU Make (https://www.gnu.org/software/make/), Reproducible Builds (https://reproducible-builds.org), SLSA supply-chain integrity framework (https://slsa.dev)

**Note:** No single ISO standard governs build/delivery engineering as a standalone process. This skill grounds its knowledge in build-tooling engineering practice (Bazel/CMake/Make), supply-chain integrity frameworks (SLSA), and CI/CD practice. ASPICE SUP.8 (https://www.automotivespice.com/, Configuration Management — baselining, build reproducibility) is the closest formal-process analog; ASPICE SWE.4 (Software Unit Verification), SWE.5 (Software Integration and Integration Test), and SWE.6 (Software Qualification Test) belong to `tst_`, not `bld_`.

---

**Content gate — verify before applying anything below.** This file
applies only when the target node's content genuinely *is* delivery/
manufacturing engineering — how the product is assembled, packaged, and
shipped — not merely attached to a `bld_` parent. The product's own
behavior is `prd_`; verification of the build is `tst_`. Ask: stripped of
its id, would this node's actual content read as delivery engineering, or
as some other enabler's work instead (the enabler-vs-topic guard)? If
it reads as something else, do not force-fit it here —
reject it and report the mismatch back as a design error, the same way
`qik-thalam-author`'s and `qik-thalam-critique`'s own hard-prohibition
sections do.

## Authoring guidance

### bld_feat_req / bld_glob_req — Build/Delivery Requirements

A build requirement states what the delivery system shall produce or accomplish.

**Shall contain:**
- **Platform targets** (Linux x86_64, macOS arm64, Windows x86_64, etc.)
- **Artifact types** (binary, VSIX extension, ZIP archive, Docker image, package index entry)
- **Distribution channels** (GitHub release, package registry, direct download URL)
- **Quality gate level** (which tests must pass before distribution)
- **Reproducibility** — same input → same artifact (content-addressable, version-stamped)

Form: "The build system shall produce a [artifact type] for [platform target] that [verification criterion]."

**Traceability:** Traces via `:refines:` to a `sys_req` or `prd_feat_req` that drives the delivery requirement.

---

### bld_comp_arc — Build Pipeline Architecture

A build pipeline architecture element describes the **topology of the delivery pipeline** — the stages and their contracts:

**Pipeline stages and their artifacts:**
```
source → compile/lint → test → package → distribute
```

Each stage must specify:
- **Name** of the stage (compile, unit-test, integration-test, package, publish)
- **Input** artifact contract (what it consumes)
- **Output** artifact contract (what it produces — name, type, path)
- **Tools** used (e.g. cargo, npm, docker, or a project-specific build script)
- **Success criterion** (exit code 0, non-empty output dir, test pass rate)
- **Entry script or command** (the concrete shell command or script path)

**Pipeline-stage practice:** Each stage typically maps to a build-system target or CI/CD job (compile, unit-test invocation, package, publish) — common practice in Bazel/CMake-based and CI/CD pipelines. Which test level runs at which stage is `tst_`'s content, not a `bld_`-owned ASPICE alignment claim.

**Links:** `:fulfils: bld_comp_req__<module>__<tag>` for each requirement the pipeline stage satisfies.

---

### bld_unit_des — Script/Job/Folder Specification

A build unit design specifies a **single script, CI job, or folder** concretely:

**For a build script:**
- **Input files:** what files/directories the script reads
- **Commands:** the exact shell invocation(s) (not "runs the build" but e.g. `<build-tool> build --target <target> --profile release`)
- **Environment variables:** required env vars and their expected format
- **Output directory:** exact path where artifacts land
- **Success criterion:** non-empty output dir + exit code 0 + artifact naming pattern

**For a folder:**
- **Role:** what this folder contains and why it exists
- **Naming convention:** what files live here
- **Owner:** which build stage produces or consumes it

**Idempotency:** Running the script twice with the same inputs shall produce the same output. State this as a requirement in the design.

**Links:** `:fulfils: bld_comp_arc__<module>__<tag>` + `:implements: bld_comp_req__<module>__<tag>`

---

### bld_unit_imp — Folder Descriptor / @needs Marker

A build implementation is a `@needs` marker comment in a `.folder` descriptor file at the folder root. The pattern:

```
# @needs <description>, bld_unit_imp__<module>__<tag>, bld_unit_imp, [bld_unit_des__<module>__<tag>], proposed
```

This makes the folder traceable in the graph without adding a Markdown file to the build output. The marker implements the `bld_unit_des` that specifies the folder's role.

---

## Review checklist

### For bld_feat_req / bld_glob_req

| # | Indicator | Type |
|---|-----------|------|
| B-R-1 | Platform target or artifact type named | pass/fail |
| B-R-2 | Distribution channel or quality gate named | pass/fail |
| B-R-3 | Uses "shall" form | pass/fail |
| B-R-4 | Traceable via `:refines:` to parent | pass/fail |
| B-R-5 | Verifiable — success criterion derivable | 0–3 |

### For bld_comp_arc

| # | Indicator | Type |
|---|-----------|------|
| B-A-1 | All pipeline stages named | pass/fail |
| B-A-2 | Input/output contracts specified per stage | pass/fail |
| B-A-3 | Entry script or command named | pass/fail |
| B-A-4 | Carries `:fulfils:` link to bld_comp_req | pass/fail |
| B-A-5 | Success criterion stated per stage | 0–3 |

### For bld_unit_des

| # | Indicator | Type |
|---|-----------|------|
| B-D-1 | Output directory named exactly | pass/fail |
| B-D-2 | Commands/scripts named concretely (not "runs the build") | pass/fail |
| B-D-3 | Idempotency stated (same input → same output) | pass/fail |
| B-D-4 | Carries `:fulfils:` and `:implements:` links | pass/fail |
| B-D-5 | Sufficient for CI/CD engineer to configure without further questions | 0–3 |

### For bld_unit_imp

| # | Indicator | Type |
|---|-----------|------|
| B-I-1 | @needs marker present in .folder or source file | pass/fail |
| B-I-2 | Marker implements the correct bld_unit_des | pass/fail |
| B-I-3 | Location consistent with bld_unit_des path commitment | pass/fail |
