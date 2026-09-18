#!/usr/bin/env python3
"""cortex `rust__use-import-discipline` py-rule — deterministic enforcement.

Protocol
--------
stdin    : full UTF-8 content of the file being checked
stdout   : JSON array of {"line": <1-based int>, "message": <str>}

Rules
-----
1. Sibling workspace crates must be imported via their prelude only:
   `use <crate>::prelude::*` — any deeper path into a sibling crate is a
   violation (e.g. `use qed_core::factory::ConfigConcept`).
2. The current crate's items must use `crate::` — not via a re-exported
   prelude wildcard of the same crate.
3. `pub use` that re-exports foreign (non-`crate::`) symbols is only allowed
   inside a `pub mod prelude` block; anywhere else it is a violation.
4. Import groups must be separated by blank lines so rustfmt sorts within
   groups only and never reorders across group boundaries.
   Groups (in order): std, external crates, workspace crates (::prelude),
   crate:: items. A missing blank line between two consecutive `use` lines
   from different groups is flagged.

Items inside `//` comments and `#[...]` attributes are ignored.

The list of known workspace-crate prefixes is passed as argv[1..] as
`crate_prefixes` (e.g. `qed_core qed_com qed_exec qed_oper`).  When no
prefixes are given the script infers them from `use` statements that match
the pattern `<word>_<word>::prelude` — a heuristic sufficient for the seed
ruleset.

# @needs Import-discipline py-rule, prd_unit_imp__cortex__rule_import_discipline, prd_unit_imp, [prd_unit_des__cortex__rule_import_discipline], released
"""

import json
import re
import sys

USE_RE = re.compile(r"^\s*(?P<pub>pub\s+)?use\s+(?P<path>\S+)\s*;")
COMMENT_RE = re.compile(r"^\s*//")
ATTR_RE = re.compile(r"^\s*#\[")
MOD_PRELUDE_OPEN = re.compile(r"pub\s+mod\s+prelude\s*\{")
MOD_DECL_RE = re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?mod\s+(\w+)\s*[;{]")

# Detect net-opening `fn` block: matches any `fn name` before the opening `{`.
# Covers: fn, async fn, unsafe fn, unsafe async fn, extern "C" fn, etc.
# Does NOT match `mod`, `impl`, closures (no `fn` keyword) — intentional.
FN_OPEN_RE = re.compile(
    r"\b(?:async\s+|unsafe\s+|unsafe\s+async\s+|extern\s+\"[^\"]*\"\s+)?fn\s+\w"
)

# Detect net-opening `mod` block (excludes `mod name;` declarations since
# those have no `{`; the pattern requires `{`).
MOD_BLOCK_OPEN_RE = re.compile(r"\bmod\s+\w+\s*\{")


def count_real_braces(line: str) -> tuple[int, int]:
    """Count Rust structural `{` and `}` characters in *line*.

    Skips:
    * `//` line comments (including `///` doc comments)
    * double-quoted string literals `"..."` (with escape handling)
    * single-quoted char literals `'.'` and byte literals `b'.'`
    * raw string literals `r#"..."#` / `r"..."` (up to 6 `#` delimiters)

    Returns (opens, closes).
    """
    opens = closes = 0
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        # Line comment — rest of line is not code.
        if c == "/" and i + 1 < n and line[i + 1] == "/":
            break
        # Raw string literal: r"..." or r#"..."# or r##"..."##  (up to 6 hashes)
        if c == "r" and i + 1 < n:
            hashes = 0
            j = i + 1
            while j < n and line[j] == "#" and hashes < 6:
                hashes += 1
                j += 1
            if j < n and line[j] == '"':
                # Inside raw string — skip until closing `"` + same number of `#`.
                j += 1  # skip opening "
                close_seq = '"' + "#" * hashes
                end = line.find(close_seq, j)
                if end != -1:
                    i = end + len(close_seq)
                else:
                    i = n  # not closed on this line (multi-line raw string)
                continue
        # Byte literal prefix `b` — handled by the `'` branch below (b'x').
        # Regular double-quoted string.
        if c == '"':
            i += 1
            while i < n:
                if line[i] == "\\" :
                    i += 2
                    continue
                if line[i] == '"':
                    i += 1
                    break
                i += 1
            continue
        # Char or byte literal: 'x', '\n', b'x', b'\n'.
        # Preceded by optional `b`.
        if c == "'" or (c == "b" and i + 1 < n and line[i + 1] == "'"):
            if c == "b":
                i += 1  # skip 'b'
            i += 1  # skip opening '
            if i < n and line[i] == "\\":
                i += 2  # skip escaped char
            elif i < n:
                i += 1  # skip the char itself
            if i < n and line[i] == "'":
                i += 1  # skip closing '
            continue
        if c == "{":
            opens += 1
        elif c == "}":
            closes += 1
        i += 1
    return opens, closes

# Import group classification (lower number = earlier in file)
def import_group(first_seg: str, sibling_prefixes: set[str]) -> int:
    """Assign a group number to a `use` statement's leading segment.

    0 = std
    1 = external crates (third-party dependencies)
    2 = workspace/local crates (always imported via their prelude)
    3 = own crate internal modules (crate::, self::, super::)
    """
    if first_seg == "std":
        return 0
    if first_seg == "crate" or first_seg == "self" or first_seg == "super":
        return 3
    if first_seg in sibling_prefixes:
        return 2
    return 1  # external


def collect_sibling_prefixes(lines: list[str]) -> set[str]:
    """Infer sibling-crate prefixes from prelude imports in the file."""
    prefixes: set[str] = set()
    for line in lines:
        m = re.search(r"use\s+((?:\w+_)+\w+)::prelude", line)
        if m:
            prefixes.add(m.group(1))
    return prefixes


def collect_local_modules(lines: list[str]) -> set[str]:
    """Collect declared sub-module names (mod foo; / pub mod foo;)."""
    mods: set[str] = set()
    for line in lines:
        m = MOD_DECL_RE.match(line)
        if m:
            mods.add(m.group(1))
    return mods


_GROUP_NAMES = ["std", "external deps", "workspace crates (prelude)", "own crate (crate::)"]


def is_at_module_level(
    brace_depth: int,
    mod_open_depths: list[int],
    fn_open_depths: list[int],
) -> bool:
    """Return True when the current brace position is at a module's top level.

    A `use` is module-level when it can legally appear alongside other module
    items.  Three cases:

    * depth 0          — the file's root scope.
    * depth == mod[-1]+1 and no open fn inside that mod — immediately inside
      a `mod { }` block and not yet inside any inner function.
    * Any other depth  — inside a function body, closure, impl block, etc.:
      NOT module-level.
    """
    if fn_open_depths:
        return False  # inside a function (or nested fn) — never module-level
    if brace_depth == 0:
        return True
    if mod_open_depths and brace_depth == mod_open_depths[-1] + 1:
        return True
    return False


def check(lines: list[str], sibling_prefixes: set[str]) -> list[dict]:
    findings: list[dict] = []
    in_prelude_mod = 0  # brace depth inside `pub mod prelude {`
    local_mods = collect_local_modules(lines)

    brace_depth = 0
    # Brace depths at which fn blocks were opened (net-positive open).
    fn_open_depths: list[int] = []
    # Brace depths at which mod blocks were opened (net-positive open).
    mod_open_depths: list[int] = []
    # Brace depths at which #[cfg(test)] mod blocks were opened.
    # Inside these scopes, function-local `use` statements are allowed
    # (test snippets are short and FQN or local imports are idiomatic).
    test_mod_open_depths: list[int] = []
    # Set when the preceding attribute line was `#[cfg(test)]`; consumed
    # when the next `mod { }` is detected.
    cfg_test_pending: bool = False

    # Per-module ordering state stack.  Each entry is a mutable list
    # [max_group_ever, prev_use_lineno, prev_group] so we can update in-place.
    # A fresh entry is pushed when entering a `mod { }` block and popped on exit.
    ordering_ctx: list[list] = [[-1, None, None]]

    for lineno, raw in enumerate(lines, start=1):
        stripped = raw.rstrip()

        # ── Brace accounting ──────────────────────────────────────────────────
        opens, closes = count_real_braces(raw)
        depth_before = brace_depth

        # Track #[cfg(test)] attribute lines (no braces, just a flag).
        if stripped == "#[cfg(test)]":
            cfg_test_pending = True
        elif stripped and not stripped.startswith("#[") and not stripped.startswith("//"):
            # Any non-attribute, non-comment line that is not a mod opener
            # clears the pending flag (attribute applies to the very next item).
            if not MOD_BLOCK_OPEN_RE.search(stripped):
                cfg_test_pending = False

        # Detect fn / mod block openings on this line BEFORE updating depth.
        # Only track when there is a net opening (single-line `fn foo() {}` is
        # complete and cannot contain a use statement anyway).
        if opens > closes:
            if FN_OPEN_RE.search(stripped):
                fn_open_depths.append(depth_before)
            elif MOD_BLOCK_OPEN_RE.search(stripped):
                mod_open_depths.append(depth_before)
                if cfg_test_pending:
                    test_mod_open_depths.append(depth_before)
                cfg_test_pending = False
                # Push a fresh ordering context for the new module scope.
                ordering_ctx.append([-1, None, None])

        brace_depth += opens - closes

        # Pop fn/mod scopes that are now fully closed.
        while fn_open_depths and brace_depth <= fn_open_depths[-1]:
            fn_open_depths.pop()
        while mod_open_depths and brace_depth <= mod_open_depths[-1]:
            mod_open_depths.pop()
            if len(ordering_ctx) > 1:
                ordering_ctx.pop()
        while test_mod_open_depths and brace_depth <= test_mod_open_depths[-1]:
            test_mod_open_depths.pop()

        inside_test_scope = bool(
            test_mod_open_depths and depth_before > test_mod_open_depths[-1]
        )

        # Current ordering context (mutable list [max_group, prev_lineno, prev_group])
        ctx = ordering_ctx[-1]

        # ── pub mod prelude tracking (for Rule 3) ─────────────────────────────
        if MOD_PRELUDE_OPEN.search(stripped):
            in_prelude_mod += 1
        elif in_prelude_mod > 0:
            in_prelude_mod = max(0, in_prelude_mod + opens - closes)

        at_module = is_at_module_level(depth_before, mod_open_depths, fn_open_depths)

        # ── Blank line resets group-tracking state within current module ──────
        if not stripped:
            if at_module:
                ctx[1] = None
                ctx[2] = None
            continue

        if COMMENT_RE.match(stripped) or ATTR_RE.match(stripped):
            continue

        m = USE_RE.match(stripped)
        if not m:
            if at_module:
                ctx[1] = None
                ctx[2] = None
            continue

        is_pub = bool(m.group("pub"))
        path = m.group("path").rstrip(";").strip()
        first_seg = path.split("::")[0]

        # Skip pub use from local sub-modules (not foreign)
        is_local_mod = first_seg in local_mods

        # ── Rule 6: non-module-level `use` (function-local / closure-local) ──
        # Exception: inside a #[cfg(test)] mod scope, local imports are allowed
        # (test snippets are short; FQN and function-local use are idiomatic).
        if not at_module and not inside_test_scope:
            findings.append({
                "line": lineno,
                "message": (
                    f"`use {path}` is not at module level (inside a function body, "
                    f"closure, or non-mod block) — move it to the module's import "
                    f"block at the top of the file."
                ),
            })
            continue

        # ── Rule 3: pub use outside pub mod prelude ───────────────────────────
        if is_pub and in_prelude_mod == 0 and first_seg != "crate" and not is_local_mod:
            findings.append({
                "line": lineno,
                "message": (
                    f"`pub use {path}` re-exports a foreign symbol outside a "
                    "`pub mod prelude` block — move it inside `pub mod prelude {{ … }}`."
                ),
            })
            continue

        # ── Rule 1: sibling crate must be imported via prelude ────────────────
        if first_seg in sibling_prefixes:
            segs = path.split("::")
            if len(segs) < 2 or segs[1] != "prelude":
                findings.append({
                    "line": lineno,
                    "message": (
                        f"Deep import `{path}` from sibling crate `{first_seg}` — "
                        f"use `{first_seg}::prelude::*` instead."
                    ),
                })

        cur_group = import_group(first_seg, sibling_prefixes)
        max_group_ever, prev_use_lineno, prev_group = ctx[0], ctx[1], ctx[2]

        # Rules 4 and 5 only apply at module level.  Function-local imports
        # inside test scopes (which are exempt from Rule 6) must not pollute
        # the module's ordering context.
        if at_module:
            # ── Rule 4: blank line required between different import groups ──
            if (
                prev_use_lineno is not None
                and prev_group is not None
                and cur_group != prev_group
                and lineno == prev_use_lineno + 1
            ):
                findings.append({
                    "line": lineno,
                    "message": (
                        f"Missing blank line before import group change "
                        f"(group {prev_group} → {cur_group}): add a blank line "
                        f"between import blocks so rustfmt sorts within groups only."
                    ),
                })

            # ── Rule 5: import groups must be in ascending order ──────────────
            if cur_group < max_group_ever:
                findings.append({
                    "line": lineno,
                    "message": (
                        f"`use {path}` is import group {cur_group} "
                        f"({_GROUP_NAMES[cur_group]}) but appears after group "
                        f"{max_group_ever} ({_GROUP_NAMES[max_group_ever]}) — "
                        f"move it up to the correct block "
                        f"(std → external deps → workspace (prelude) → own crate (crate::))."
                    ),
                })
            else:
                ctx[0] = cur_group

            ctx[1] = lineno
            ctx[2] = cur_group

    return findings


def main() -> None:
    content = sys.stdin.read()
    lines = content.splitlines()

    explicit_prefixes = set(sys.argv[1:]) if len(sys.argv) > 1 else set()
    sibling_prefixes = explicit_prefixes or collect_sibling_prefixes(lines)

    findings = check(lines, sibling_prefixes)
    print(json.dumps(findings))


if __name__ == "__main__":
    main()

