# qik cortex learn — rule recording procedure

<!-- @needs cortex learn procedure (Claude Code), prd_unit_imp__cortex__learn_procedure_claude, prd_unit_imp, [prd_unit_des__cortex__learn_procedure_claude], released -->

Executed by the **qik-cortex** persona (Quality Guardian).

## When to invoke

After a violation is discovered that reveals a missing rule — a recurring
pattern not yet captured in the rule set. Do NOT defer: record immediately.

## Prerequisite: the rule must already be formulated

Before calling `cortex_learn`, the Quality Guardian must have already applied
the formulation criteria (see persona). This skill records a rule that is
already valid — it does not help formulate one.

## Procedure

### Step 1 — Choose the kind

| Condition type | Kind to use |
|---|---|
| Regex pattern must NOT appear | `forbid-regex` |
| File must contain a pattern | `require-regex` |
| Complex structural check | `py-rule` |
| Semantic, inherently binary question | `llm` |

Default to `forbid-regex`. Only use `llm` when a regex genuinely cannot express
the condition.

### Step 2 — Choose the glob

Be as narrow as possible. `**/*.rs` is narrower than `**`. A narrow glob reduces
false positives and makes the rule faster to evaluate.

### Step 3 — Record the rule

```bash
qik cortex learn <id> \
  --kind <kind> \
  --severity <error|warning> \
  --include-glob "<glob>" \
  --pattern "<regex>"      # for forbid-regex / require-regex
  --why "<one sentence: incident that triggered this rule>"
```

For LLM rules, use `--check-prompt` instead of `--pattern`. The check prompt
must produce a binary `PASS` or `FAIL + location + reason` — nothing in between.

### Step 4 — Verify

```bash
qik cortex check --kind algo --no-color
```

Zero new errors on the current working tree.
