#!/usr/bin/env python3
"""cortex `subcommand-traceable` py-rule: every clap subcommand carries a marker.

The deterministic half of subcommand traceability. `qik axon check` validates the
declared graph top-down, so a CLI subcommand implemented with *no* impl marker
produces no impl need and stays invisible to it — the bottom-up blind spot. This
rule closes it at the source: it requires every variant of a clap `Subcommand`
enum to be preceded by a sphinx-codelinks impl marker naming an `IMPL_` id and the
`DSN_` it realizes. Once the marker exists, codelinks
emits the impl need and the ordinary `axon check` chain (REQ -> DSN -> IMPL) takes
over — so this rule only has to guarantee the marker is there.

Protocol
--------
stdin    : full UTF-8 content of the file being checked
stdout   : JSON array of {"line": <1-based int>, "message": <str>}

Algorithm
---------
* A `#[derive(...)]` naming `Subcommand` marks the next `enum` as a clap command
  set; its direct variants are the subcommands.
* Each such variant must have, directly above it (skipping `#[...]` attributes,
  `///`/`//!` doc comments and ordinary `//` comments), a codelinks impl marker
  (an `IMPL_` need). A variant without one is flagged.
"""

import json
import re
import sys

# A derive attribute that brings in clap's `Subcommand` (so the enum is a command set).
DERIVE_SUBCOMMAND = re.compile(r"#\[derive\([^)]*\bSubcommand\b")
# `enum Name {` — optionally `pub` / `pub(crate)`.
ENUM_OPEN = re.compile(r"^(pub(\([^)]*\))?\s+)?enum\s+\w+")
# A variant declaration: an upper-case-led identifier at the enum's body depth.
VARIANT = re.compile(r"^[A-Z]\w*")


def has_marker(lines: list, index: int) -> bool:
    """Whether a codelinks impl marker sits directly above the item at *index*.

    Attributes, doc comments and ordinary comments are skipped while scanning
    upward; a blank or code line ends the search. Only the codelinks impl marker
    counts as satisfying the rule.
    """
    j = index
    while j > 0:
        j -= 1
        t = lines[j].strip()
        if t.startswith("#[") or t.startswith("#!["):
            continue  # attribute
        if t.startswith("//"):
            if "@" in t and "unit_imp__" in t:
                return True  # the codelinks impl marker
            continue  # doc or ordinary comment — keep scanning
        return False  # code or blank line — no marker adjacent
    return False


# @needs Subcommand marker enforcement, prd_unit_imp__cortex__rule_subcommand, prd_unit_imp, [prd_unit_des__cortex__rule_subcommand], released
def main() -> None:
    lines = sys.stdin.read().splitlines()

    violations = []
    depth = 0
    pending_subcommand = False  # a Subcommand derive seen, awaiting its `enum`
    enum_body_depth = None  # brace depth at which the current command enum's variants live

    for i, raw in enumerate(lines):
        trimmed = raw.strip()

        if DERIVE_SUBCOMMAND.search(trimmed):
            pending_subcommand = True

        # A variant of the active command enum: upper-case-led at body depth.
        if (
            enum_body_depth is not None
            and depth == enum_body_depth
            and VARIANT.match(trimmed)
            and not has_marker(lines, i)
        ):
            violations.append(
                {
                    "line": i + 1,
                    "message": "clap subcommand variant lacks an imp marker "
                    "(// @<title>, unit_imp__<cluster>__<id>, unit_imp, [unit_des__<cluster>__<id>])",
                }
            )

        opens = raw.count("{")
        closes = raw.count("}")

        if pending_subcommand and ENUM_OPEN.match(trimmed) and opens > 0:
            enum_body_depth = depth + 1  # variants live one level inside the enum
            pending_subcommand = False

        depth += opens - closes

        # The command enum has closed; stop treating lines as its variants.
        if enum_body_depth is not None and depth < enum_body_depth:
            enum_body_depth = None

    print(json.dumps(violations))


if __name__ == "__main__":
    main()
