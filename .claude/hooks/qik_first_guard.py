#!/usr/bin/env python3
"""Claude Code PreToolUse hook: gate manual sweeps over needs/ or .qik/, and
gate a `git commit` with no explicit pathspec.

Scaffolded by `qik init`/`qik upgrade` (rust/qik-main/src/scaffold.rs embeds
this file verbatim) into a target repository's `.claude/hooks/`, with the
`.claude/settings.json` PreToolUse wiring handled alongside it in
rust/qik-main/src/lifecycle.rs. Catches two recurring failure modes:

1. An agent reconstructing the needs graph, rules, or lifecycle state by hand
   (Grep/Glob/find/grep/rg) instead of querying qik's own tools
   (mcp__qik__axon_*, mcp__qik__cortex_*, mcp__qik__nexus_*) or delegating to
   the qik-axon/qik-cortex/qik-nexus subagent. Read is intentionally NOT
   gated: reading one specific need's or rule's exact prose to edit it is
   legitimate; only the exploratory sweep pattern is blocked.
2. `git commit` with no trailing `-- <paths>` pathspec: in a shared working
   tree (multiple concurrent sessions touching the same checkout), a bare
   `git commit -m "..."` commits the ENTIRE index, not just the files this
   session just `git add`ed -- silently riding along with whatever another
   session staged in the meantime. `git add <file>` alone does not create
   this risk; only `commit` without a pathspec does.
"""
import json
import os
import re
import sys

MSG = (
    "Blocked: this looks like a manual sweep over needs/ or .qik/. Use qik "
    "instead: mcp__qik__axon_* for the needs graph (list/trace/impact/analyze/"
    "check/coverage), mcp__qik__cortex_* for rules (list/why/check), "
    "mcp__qik__nexus_* for lifecycle (list/get/engage) -- or delegate to the "
    "qik-axon / qik-cortex / qik-nexus subagent. If qik genuinely has no "
    "answer and you need one specific file's exact prose (e.g. to edit it), "
    "use Read on that single file, not Grep/Glob/find/grep/rg."
)

COMMIT_MSG = (
    "Blocked: `git commit` with no trailing `-- <paths>` pathspec. In a "
    "shared working tree, this commits the entire index, not just the files "
    "this session staged -- another session's concurrently staged changes "
    "would ride along, misattributed. Add an explicit pathspec, e.g. "
    "`git commit -m \"...\" -- path/to/file`."
)

# Matches a `needs` or `.qik` path *segment*: the token must start right after
# a `/` (or at the very start of the string) and end at a non-identifier
# character or end-of-string -- so it catches "needs/", "/needs -type f", or
# "needs.json", but not "my-needs-list" or the bare English word inside a
# sentence like "grep -rn 'needs to be fixed'".
_PATH_SEGMENT = re.compile(r"(?:^|/)(?:needs|\.qik)(?:$|[^a-z0-9_])")

_FIND_GREP_VERB = re.compile(r"(^|[|;&]|\s)(find|grep|rg)(\s|$)")

# qik's own commands always pass — they operate on .qik/ by design and are
# themselves the remediation tools. Blocking `qik cortex ignore` (or any
# compound like `qik cortex learn && grep .qik/…`) on global check state is
# the catch-22 this guard exists to prevent, not to cause.
_QIK_COMMAND = re.compile(r"^\s*(\S+[/\\])?qik(\s|$)")

# Splits a compound shell command into per-command segments on the chain
# operators (&&, ||, ;, |). Not a real shell parser (does not respect quotes),
# same crude-regex tradeoff as the grep/find guard above -- but unlike that
# guard, a git commit message routinely contains ; or | as prose punctuation
# (and this project's own commit convention pipes the message through a
# `$(cat <<'EOF' ... EOF)` heredoc), so raw commands must have their quoted/
# heredoc regions blanked out first or a punctuation mark inside the message
# text would be misread as a chain operator, splitting `git commit` off from
# its own trailing pathspec.
_CHAIN_SPLIT = re.compile(r"&&|\|\||;|\|")

_HEREDOC_BODY = re.compile(r"<<-?\s*(['\"]?)(\w+)\1.*?\n\2\b", re.DOTALL)
_SINGLE_QUOTED = re.compile(r"'[^']*'")
_DOUBLE_QUOTED = re.compile(r'"(?:[^"\\]|\\.)*"')

_GIT_COMMIT_START = re.compile(r"^\s*(\S+[/\\])?git\s+commit(\s|$)")

# A `--` pathspec separator followed by at least one argument. Requires
# whitespace after `--` so flags like `--amend` don't false-positive as
# "has a pathspec".
_HAS_PATHSPEC = re.compile(r"--\s+\S")


def matches_needs_or_qik(s: str) -> bool:
    return bool(_PATH_SEGMENT.search(s.lower()))


def is_qik_invocation(command: str) -> bool:
    """True if the command's leading word is the `qik` binary (any path prefix)."""
    return bool(_QIK_COMMAND.match(command))


def _blank_quoted_regions(command: str) -> str:
    """Blank out heredoc bodies and quoted strings so their punctuation can't
    be mistaken for shell chain operators or a `--` pathspec marker."""
    command = _HEREDOC_BODY.sub(" ", command)
    command = _SINGLE_QUOTED.sub(" ", command)
    command = _DOUBLE_QUOTED.sub(" ", command)
    return command


def has_unpathspec_git_commit(command: str) -> bool:
    """True if any chained segment is a `git commit` with no `-- <paths>`."""
    scrubbed = _blank_quoted_regions(command)
    for segment in _CHAIN_SPLIT.split(scrubbed):
        if _GIT_COMMIT_START.match(segment) and not _HAS_PATHSPEC.search(segment):
            return True
    return False


def deny(reason: str = MSG) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    if tool_name in ("Grep", "Glob"):
        path = tool_input.get("path") or os.getcwd()
        pattern = tool_input.get("pattern") or tool_input.get("glob") or ""
        if matches_needs_or_qik(path) or matches_needs_or_qik(pattern):
            deny()
    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        if is_qik_invocation(command):
            sys.exit(0)
        if _FIND_GREP_VERB.search(command.lower()) and matches_needs_or_qik(command):
            deny()
        if has_unpathspec_git_commit(command):
            deny(COMMIT_MSG)

    sys.exit(0)


if __name__ == "__main__":
    main()
