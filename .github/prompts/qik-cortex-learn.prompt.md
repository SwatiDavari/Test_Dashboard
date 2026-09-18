---
description: >-
  Record a new cortex rule after a violation reveals a missing pattern.
  Use when the Quality Guardian has already formulated a valid rule and
  needs to execute the recording procedure.
---

<!-- @needs cortex learn procedure (Copilot), prd_unit_imp__cortex__learn_procedure_copilot, prd_unit_imp, [prd_unit_des__cortex__learn_procedure_copilot], released -->

# qik cortex learn — rule recording procedure

Executed by the **qik-cortex** Quality Guardian persona.

## Prerequisite

The rule must already be **formulated** — the `@qik-cortex` agent applies the
formulation criteria (unambiguous, surgical, binary). This prompt records a rule
that is already valid.

## Step 1 — Choose the kind

| Condition type | Kind |
|---|---|
| Regex must NOT appear in file | `forbid-regex` |
| File must contain a pattern | `require-regex` |
| Complex structural check | `py-rule` |
| Semantic, inherently binary question | `llm` |

Default to `forbid-regex`. Use `llm` only when a regex genuinely cannot express
the condition — and only if the check prompt yields a binary `PASS`/`FAIL`.

## Step 2 — Choose the glob

Be as narrow as possible. `prod/qik/rust/**/*.rs` beats `**/*.rs` beats `**`.

## Step 3 — Record

```bash
qik cortex learn <id> \
  --kind <kind> \
  --severity <error|warning> \
  --include-glob "<glob>" \
  --pattern "<regex>"       # for forbid-regex / require-regex
  --why "<one sentence: the incident that triggered this rule>"
```

For `llm` rules replace `--pattern` with
`--check-prompt "<binary question yielding PASS or FAIL + location>"`.

## Step 4 — Verify

```bash
qik cortex check --kind algo --no-color
```

Zero new errors on the current working tree. If algo check fails, the rule
pattern matched something it should not — tighten the glob or regex.
