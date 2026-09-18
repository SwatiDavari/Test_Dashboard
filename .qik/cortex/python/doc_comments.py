#!/usr/bin/env python3
"""Cortex py-rule: require a `///` doc comment on every Rust item.

Protocol
--------
stdin    : full UTF-8 content of the file being checked
stdout   : JSON array of {"line": <1-based int>, "message": <str>}

Args (argv[1..])
----------------
--pub-only  Check only `pub` items (used by the error-severity rule).
            Without this flag, only non-pub fn/struct/enum/trait items are
            checked (used by the warning-severity rule).

Algorithm
---------
* --pub-only mode (rust__doc-comments-pub, error):
    Flag every `pub` item that lacks a preceding `///` doc comment.
    Skip items inside `impl` bodies (trait impls inherit docs from the trait).
    Skip bare `pub mod foo;` (docs live in the module file as `//!`).

* default mode (rust__doc-comments-private, warning):
    Flag every non-pub fn/struct/enum/trait item at module level (outside any
    impl block) that lacks a preceding `///` doc comment.

In both modes, `#[...]` attribute lines and ordinary `//` line comments
between the doc comment and the item are transparent: they do not detach a
preceding `///` from what it documents.
"""

import json
import re
import sys

PUB_ONLY = "--pub-only" in sys.argv

# Keywords checked for public items (full set incl. type aliases, constants …).
PUB_ITEM_KEYWORDS = frozenset(
    ["fn", "struct", "enum", "trait", "mod", "type", "union", "const", "static"]
)

# Keywords checked for private items (the four user-visible declaration kinds).
PRIVATE_ITEM_KEYWORDS = frozenset(["fn", "struct", "enum", "trait"])

# Matches bare `pub mod foo;` / `pub(crate) mod foo;` — docs live in the
# module file as `//!`, so we skip them.
EXCLUDE_RE = re.compile(r'^pub(\([^)]*\))?\s+mod\s+\w+\s*;')


def is_pub_item(trimmed: str) -> bool:
    """Return True when the trimmed line opens a public item declaration."""
    if not trimmed.startswith("pub"):
        return False
    rest = trimmed[3:]
    if not rest:
        return False
    if rest[0] == " ":
        rest = rest.lstrip(" ")
    elif rest[0] == "(":
        close = rest.find(")")
        if close == -1:
            return False
        rest = rest[close + 1 :].lstrip(" ")
    else:
        return False  # e.g. `pubfoo`

    for token in rest.split():
        if token in ("async", "unsafe", "extern", "default"):
            continue
        return token.rstrip("!") in PUB_ITEM_KEYWORDS
    return False


def is_private_item(trimmed: str) -> bool:
    """Return True when the trimmed line opens a non-public fn/struct/enum/trait declaration."""
    if trimmed.startswith("pub"):
        return False
    # Skip attributes, comments, macro invocations, and impl blocks.
    if not trimmed or trimmed[0] in ("#", "/", "!"):
        return False
    tokens = trimmed.split()
    if not tokens:
        return False
    token = tokens[0]
    # Transparent qualifiers: async fn, unsafe fn, extern fn.
    if token in ("async", "unsafe", "extern", "default") and len(tokens) > 1:
        token = tokens[1]
    return token.rstrip("!") in PRIVATE_ITEM_KEYWORDS


def has_test_attr(lines: list, index: int) -> bool:
    """Return True when the item at *index* is decorated with `#[test]`.

    Scans upward through attribute and comment lines — the same traversal as
    `has_preceding_doc`.  Returns True as soon as it sees a `#[test]` line,
    False as soon as it hits a non-attribute line.
    """
    j = index
    while j > 0:
        j -= 1
        t = lines[j].lstrip()
        if t == "#[test]" or t.startswith("#[test]"):
            return True
        if t.startswith("#[") or t.startswith("#!["):
            continue  # other attribute — keep scanning
        if t.startswith("//"):
            continue  # line comment — not a detacher
        return False  # code or blank line — no test attr adjacent
    return False


def has_preceding_doc(lines: list, index: int) -> bool:
    """Return True when the item at *index* is preceded by a doc comment.

    Scanning upward, attribute lines (`#[...]`) and ordinary line comments
    (`//…`, e.g. a codelinks impl marker or a note explaining
    an `#[allow]`) are skipped: neither detaches a `///` from what it documents,
    because a real code or blank line always separates two items and stops the
    scan first. Only a `///`/`//!`/block doc comment counts as documentation.
    """
    j = index
    while j > 0:
        j -= 1
        t = lines[j].lstrip()
        if (
            t.startswith("///")
            or t.startswith("//!")
            or t.startswith("/**")
            or t.startswith("*")
            or t.endswith("*/")
        ):
            return True  # doc comment (line or block) — item is documented
        if t.startswith("#[") or t.startswith("#!["):
            continue  # attribute — keep scanning upward
        if t.startswith("//"):
            continue  # ordinary line comment (incl. codelinks markers) — not a detacher
        return False  # real code or blank line — no doc adjacent
    return False


def main() -> None:
    content = sys.stdin.read()
    lines = content.splitlines()

    violations = []
    depth = 0
    impl_depths: list[int] = []

    for i, raw in enumerate(lines):
        trimmed = raw.lstrip()
        inside_impl = bool(impl_depths)

        if PUB_ONLY:
            excluded = bool(EXCLUDE_RE.match(trimmed))
            if (
                not inside_impl
                and not excluded
                and is_pub_item(trimmed)
                and not has_preceding_doc(lines, i)
                and not has_test_attr(lines, i)
            ):
                violations.append(
                    {"line": i + 1, "message": "public item lacks a `///` doc comment"}
                )
        else:
            if (
                not inside_impl
                and is_private_item(trimmed)
                and not has_preceding_doc(lines, i)
                and not has_test_attr(lines, i)
            ):
                violations.append(
                    {"line": i + 1, "message": "non-public item lacks a `///` doc comment"}
                )

        opens_impl = (
            trimmed.startswith("impl ")
            or trimmed.startswith("impl<")
            or trimmed.startswith("unsafe impl")
        )
        opens = raw.count("{")
        closes = raw.count("}")

        if opens_impl and opens > 0:
            impl_depths.append(depth)  # record depth BEFORE update (mirrors Rust)

        depth += opens - closes

        # Pop impl scopes that have been fully closed.
        while impl_depths and depth <= impl_depths[-1]:
            impl_depths.pop()

    print(json.dumps(violations))


if __name__ == "__main__":
    main()
