# qik cortex check — full quality-gate procedure


<!-- @needs cortex check procedure (Claude Code), prd_unit_imp__cortex__check_procedure_claude, prd_unit_imp, [prd_unit_des__cortex__check_procedure_claude], released -->
Executed by the **qik-cortex** persona (Quality Guardian).

## When to invoke

Before every commit. After any change to Rust/Python files. On code review.
Whenever a rule violation is discovered (record it immediately).

## Procedure

### Step 1 — Prime (load active rules)

```bash
qik cortex dump --kind all --no-color
```

Read every rule's `check_prompt` — needed for the semantic step.

### Step 2 — Algorithmic check

```bash
qik cortex check --kind algo --no-color
```

Parse the JSON `Report`. Each `"severity": "error"` is **blocking** — fix the
code, not the rule. Re-run until clean. Warnings do not block.

### Step 3 — Semantic check

```bash
qik cortex dump --kind llm --no-color
```

Apply each rule's `check_prompt` to the changed files (`git diff --staged`).
Answer per rule:
- `PASS` — rule satisfied
- `FAIL + file:line + reason` — rule violated (error-severity FAIL is blocking)

### Step 4 — Report

Summarize: errors found/fixed, warnings, pass count. If all clear, say so plainly.

### Step 5 — Learn (if applicable)

When a real violation reveals a missing rule, record it immediately:

```bash
qik cortex learn --id <id> --kind <kind> --severity <error|warning> \
  --scope '<glob>' --why "<incident>" [--pattern '...' | --check-prompt '...']
```

Or use `cortex_learn(...)` via MCP.
