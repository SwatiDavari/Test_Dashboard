"""Sphinx configuration for this project's qik traceability needs (`/needs`).

Authoring is MyST Markdown; sphinx-needs holds the artifact graph; the `needs`
builder emits ``needs.json`` — the single bridge format consumed by ``qik axon``.
Scaffolded by ``qik init``; adjust the project name and enable code-links (see the
bottom of this file) to point at your sources.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE / "_ext"))

project = "My Project"
author = "Project Team"
html_title = project

extensions = [
    "myst_parser",
    "sphinx_needs",
    "tst_case",
]

# Human-facing HTML theme (the `needs` builder that emits needs.json ignores
# this). `qorix` inherits pydata_sphinx_theme for a persistent top navbar, a
# contextual left sidebar (only the active branch's children, collapsible)
# and a scrollspy "on this page" right sidebar. Edit qorix.css's `:root`
# block to rebrand the palette; edit `logo`/`html_title` for your project name.
html_theme = "qorix"
html_theme_path = ["_themes"]
html_theme_options = {
    "logo": {"text": project},
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    "header_links_before_dropdown": 6,
    "navigation_depth": 4,
    "collapse_navigation": True,
    "secondary_sidebar_items": ["page-toc"],
    "show_toc_level": 2,
}
html_context = {"default_mode": "dark"}

# MyST: allow colon-fenced directives (used for need objects).
myst_enable_extensions = ["colon_fence"]

# --- Need types: canonical qik 3D schema (enabler × scope × layer) -----------
# ID format: {type}__{cluster}__{tag}  ---  all lowercase, double-underscore
# enabler: sys_  prd_  tst_  doc_  saf_  sec_  bld_
# scope:   glob  feat  comp  unit  (sys_ has no scope qualifier)
# layer:   int   req   arc   des   imp   (not all combinations exist)
needs_types = [
    # sys_: mission level -- no scope qualifier
    {"directive": "sys_int",       "title": "System Intention",              "prefix": "sys_int__",       "color": "#F5D76E", "style": "node"},
    {"directive": "sys_req",       "title": "System Requirement",            "prefix": "sys_req__",       "color": "#F0C040", "style": "node"},
    {"directive": "sys_arc",       "title": "System Architecture",           "prefix": "sys_arc__",       "color": "#E8A020", "style": "node"},
    # prd_: product / system-of-interest
    {"directive": "prd_glob_int",  "title": "Product Global Intention",      "prefix": "prd_glob_int__",  "color": "#BFD8D2", "style": "node"},
    {"directive": "prd_glob_req",  "title": "Product Global Requirement",    "prefix": "prd_glob_req__",  "color": "#7FB3C8", "style": "node"},
    {"directive": "prd_glob_arc",  "title": "Product Global Architecture",   "prefix": "prd_glob_arc__",  "color": "#FEDCD2", "style": "node"},
    {"directive": "prd_feat_int",  "title": "Product Feature Intention",     "prefix": "prd_feat_int__",  "color": "#A8C8BC", "style": "node"},
    {"directive": "prd_feat_req",  "title": "Product Feature Requirement",   "prefix": "prd_feat_req__",  "color": "#6AA0B8", "style": "node"},
    {"directive": "prd_feat_arc",  "title": "Product Feature Architecture",  "prefix": "prd_feat_arc__",  "color": "#F8C0A0", "style": "node"},
    {"directive": "prd_comp",      "title": "Product Component",             "prefix": "prd_comp__",      "color": "#D8E8C5", "style": "node"},
    {"directive": "prd_comp_req",  "title": "Product Component Requirement", "prefix": "prd_comp_req__",  "color": "#55909C", "style": "node"},
    {"directive": "prd_comp_arc",  "title": "Product Component Architecture","prefix": "prd_comp_arc__",  "color": "#F0A880", "style": "node"},
    {"directive": "prd_unit_des",  "title": "Product Unit Design",           "prefix": "prd_unit_des__",  "color": "#DF744A", "style": "node"},
    {"directive": "prd_unit_imp",  "title": "Product Unit Implementation",   "prefix": "prd_unit_imp__",  "color": "#DCB239", "style": "node"},
    # tst_: test enabling system
    {"directive": "tst_glob_req",  "title": "Test Global Requirement",       "prefix": "tst_glob_req__",  "color": "#D8B8E8", "style": "node"},
    {"directive": "tst_feat_req",  "title": "Test Feature Requirement",      "prefix": "tst_feat_req__",  "color": "#C4A0D0", "style": "node"},
    {"directive": "tst_comp_req",  "title": "Test Component Requirement",    "prefix": "tst_comp_req__",  "color": "#B090C4", "style": "node"},
    {"directive": "tst_unit_des",  "title": "Test Unit Design",              "prefix": "tst_unit_des__",  "color": "#8860A0", "style": "node"},
    {"directive": "tst_unit_imp",  "title": "Test Unit Implementation",      "prefix": "tst_unit_imp__",  "color": "#744890", "style": "node"},
    # doc_: documentation enabling system
    {"directive": "doc_feat_req",  "title": "Doc Feature Requirement",       "prefix": "doc_feat_req__",  "color": "#9CBCF0", "style": "node"},
    {"directive": "doc_unit_des",  "title": "Doc Unit Design",               "prefix": "doc_unit_des__",  "color": "#5078C8", "style": "node"},
    {"directive": "doc_unit_imp",  "title": "Doc Unit Implementation",       "prefix": "doc_unit_imp__",  "color": "#3C6CBC", "style": "node"},
]

# IDs follow <type>__<cluster>__<description>: lowercase, double-underscore separators.
needs_id_regex = r"^[a-z][a-z0-9_]*__[a-z][a-z0-9_]*__[a-z][a-z0-9_]+$"

# --- Link semantics (S-CORE-aligned, cr-000312) --------------------------------
# Structural links use active-verb inverses (generalizes/comprises/owns).
# Traceability and V&V links keep established passive inverses. Kept in sync
# with .qik/axon/rules.toml, which this scaffold ships verbatim from qik's own
# live rule store (see cr-000374) -- every link name a shipped rule can
# reference must be declared here too, or an authored need using it is an
# unrecognized Sphinx field.
needs_links = {
    "refines":     {"incoming": "generalizes",        "outgoing": "refines"},
    "satisfies":   {"incoming": "is satisfied by",    "outgoing": "satisfies"},
    "fulfils":     {"incoming": "is fulfilled by",    "outgoing": "fulfils"},
    "implements":  {"incoming": "is implemented by",  "outgoing": "implements"},
    "validates":   {"incoming": "is validated by",    "outgoing": "validates"},
    "verifies":    {"incoming": "is verified by",     "outgoing": "verifies"},
    "mitigates":   {"incoming": "is mitigated by",    "outgoing": "mitigates"},
    "violates":    {"incoming": "is violated by",     "outgoing": "violates"},
    "covers":      {"incoming": "is covered by",      "outgoing": "covers"},
    "documents":   {"incoming": "is documented by",   "outgoing": "documents"},
    "belongs_to":  {"incoming": "owns",               "outgoing": "belongs to"},
    "decomposes":  {"incoming": "comprises",          "outgoing": "decomposes"},
}

# Emit needs.json (the bridge format) alongside the build.
needs_build_json = True
needs_json_remove_defaults = True
needs_flow_engine = "graphviz"

source_suffix = {".md": "markdown"}
exclude_patterns = ["_build"]

# --- Optional: link code to design via sphinx-codelinks -----------------------
# Add "sphinx_codelinks" to `extensions` above, then uncomment and point
# `src_dir` at your sources. A one-line marker
# `// @<title>, <id>, <type>, [<links>]` in a source file is discovered and
# turned into an impl/test need in the same needs.json, recording its file+line
# so `qik axon` can answer with link + range.
#
# from pathlib import Path
# from sphinx_codelinks.config import generate_project_configs
#
# src_trace_set_local_url = True
# src_trace_projects = {
#     "project": {
#         "source_discover": {
#             "src_dir": str((Path(__file__).parent / ".." / "src").resolve()),
#             "comment_type": "rust",  # or "c", "cpp", "python", ...
#         },
#         "analyse": {
#             "get_oneline_needs": True,
#             "get_need_id_refs": False,
#             "oneline_comment_style": {
#                 "needs_fields": [
#                     {"name": "title"},
#                     {"name": "id"},
#                     {"name": "type", "default": "imp"},
#                     {"name": "implements", "type": "list[str]", "default": []},
#                 ],
#             },
#         },
#     },
# }
# generate_project_configs(src_trace_projects)

# --- Checksum stamp (Build-time) -----------------------------------------------
# Delegate checksum logic to `qik axon stamp`. Sphinx only supplies the trigger
# (build-finished event); all stamp/manifest logic lives in the qik binary.
# Keeps .qik/fingerprint.toml's [needs] checksum current on every build without
# a separate manual step (cr-000375).

import shutil
import subprocess


def _axon_stamp(app, exception):
    if exception is not None:
        return
    if app.builder.name != "needs":
        return

    workspace_root = _HERE.parent

    if shutil.which("qik") is None:
        print("[axon] qik not found, skipping stamp")
        return

    result = subprocess.run(
        ["qik", "axon", "stamp"],
        cwd=workspace_root,
        capture_output=True,
        text=True,
        check=False,
    )
    checksum = result.stdout.strip()
    print(f"[axon] stamped needs checksum: {checksum}")


# --- Logo subtitle (cr-000380) ------------------------------------------------
# The navbar subtitle (a generated `::after` CSS fragment in qorix.css --
# pydata's `logo.text` only gives one <p>) reads this CSS variable instead of
# a hardcoded brand string, so this project's own name always shows, never
# qik's.


def _inject_logo_subtitle(app, pagename, templatename, context, doctree):
    subtitle = app.config.project.replace('"', '\\"')
    context["metatags"] = context.get("metatags", "") + (
        '\n<style>:root { --qorix-logo-subtitle: "%s"; }</style>' % subtitle
    )


def setup(app):
    """Register Sphinx event handlers."""
    app.connect("html-page-context", _inject_logo_subtitle)
    app.connect("build-finished", _axon_stamp)
