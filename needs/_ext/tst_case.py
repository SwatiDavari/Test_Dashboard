"""Sphinx extension: tst_unit_des internal-structure directives (cr-000246).

Six directives valid ONLY inside a tst_unit_des need body:
  objective   — :kind: observation|verdict, first arg = name
  narrative   — ISO/IEC/IEEE 29119-3 "Test Case Narrative"
  context     — :environment: and :scenario: reference options
  entry_conditions
  exit_conditions
  procedure   — optional; body rendered as a literal block

None of these produce sphinx-needs nodes.  The enclosing tst_unit_des is the
sole graph-visible artefact.  A doctree-read handler validates nesting,
enforces one tst_unit_des per file, and stores a structured TcData object
on env.tst_case_data (keyed by need id) for downstream tooling.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from docutils import nodes
from docutils.parsers.rst import directives as rst_directives
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger

if TYPE_CHECKING:
    from sphinx.application import Sphinx

logger = getLogger(__name__)


# ---------------------------------------------------------------------------
# Docutils node classes (invisible to sphinx-needs)
# ---------------------------------------------------------------------------

class TcBlockNode(nodes.General, nodes.Element):
    """Marker base class for all TC structure nodes."""


class TcObjectiveNode(TcBlockNode):
    pass


class TcNarrativeNode(TcBlockNode):
    pass


class TcContextNode(TcBlockNode):
    pass


class TcEntryConditionsNode(TcBlockNode):
    pass


class TcExitConditionsNode(TcBlockNode):
    pass


class TcProcedureNode(TcBlockNode):
    pass


# ---------------------------------------------------------------------------
# Structured TC data model
# ---------------------------------------------------------------------------

@dataclass
class TcObjective:
    name: str
    kind: str  # "observation" | "verdict"
    text: str


@dataclass
class TcData:
    need_id: str
    docname: str
    objectives: list[TcObjective] = field(default_factory=list)
    narrative: str | None = None
    context_environment: str | None = None
    context_scenario: str | None = None
    entry_conditions: str | None = None
    exit_conditions: str | None = None
    procedure: str | None = None


# ---------------------------------------------------------------------------
# Directive helpers
# ---------------------------------------------------------------------------

def _kind_choice(argument: str) -> str:
    return rst_directives.choice(argument, ("observation", "verdict"))


# ---------------------------------------------------------------------------
# Directives
# ---------------------------------------------------------------------------

class ObjectiveDirective(SphinxDirective):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {"kind": _kind_choice}
    has_content = True

    def run(self) -> list[nodes.Node]:
        name = self.arguments[0]
        kind = self.options.get("kind", "observation")
        node = TcObjectiveNode("", tc_name=name, tc_kind=kind)
        node += nodes.paragraph(
            "", "", nodes.strong("", f"Objective — {name}  [{kind}]")
        )
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class NarrativeDirective(SphinxDirective):
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self) -> list[nodes.Node]:
        node = TcNarrativeNode("")
        node += nodes.paragraph("", "", nodes.strong("", "Narrative"))
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class ContextDirective(SphinxDirective):
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        "environment": rst_directives.unchanged,
        "scenario": rst_directives.unchanged,
    }
    has_content = False

    def run(self) -> list[nodes.Node]:
        env_ref = self.options.get("environment", "")
        scenario_ref = self.options.get("scenario", "")
        node = TcContextNode("", tc_environment=env_ref, tc_scenario=scenario_ref)
        dl = nodes.definition_list()
        for label, val in (("Environment", env_ref), ("Scenario", scenario_ref)):
            if val:
                dl += nodes.definition_list_item(
                    "",
                    nodes.term("", label),
                    nodes.definition("", nodes.paragraph("", val)),
                )
        if dl.children:
            node += nodes.paragraph("", "", nodes.strong("", "Context"))
            node += dl
        return [node]


class EntryConditionsDirective(SphinxDirective):
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self) -> list[nodes.Node]:
        node = TcEntryConditionsNode("")
        node += nodes.paragraph("", "", nodes.strong("", "Entry Conditions"))
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class ExitConditionsDirective(SphinxDirective):
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self) -> list[nodes.Node]:
        node = TcExitConditionsNode("")
        node += nodes.paragraph("", "", nodes.strong("", "Exit Conditions"))
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class ProcedureDirective(SphinxDirective):
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self) -> list[nodes.Node]:
        node = TcProcedureNode("")
        node += nodes.paragraph("", "", nodes.strong("", "Procedure"))
        lit = nodes.literal_block("", "\n".join(self.content))
        lit["language"] = "text"
        node += lit
        return [node]


# ---------------------------------------------------------------------------
# Event handler: validate nesting, enforce one-per-file, collect data
# ---------------------------------------------------------------------------

def _process_tc_doctree(app: Sphinx, doctree: nodes.document) -> None:
    try:
        from sphinx_needs.nodes import Need as NeedNode
    except ImportError:
        return

    docname: str = app.env.docname
    env = app.env

    if not hasattr(env, "tst_case_data"):
        env.tst_case_data: dict[str, TcData] = {}

    # Collect structured data from every tst_unit_des in this document.
    tst_nodes = [
        n for n in doctree.traverse(NeedNode)
        if (n.get("ids") or [""])[0].startswith("tst_unit_des__")
    ]
    for need_node in tst_nodes:
        need_id: str = need_node["ids"][0]
        tc = TcData(need_id=need_id, docname=docname)
        for child in need_node.traverse():
            if isinstance(child, TcObjectiveNode):
                tc.objectives.append(TcObjective(
                    name=child["tc_name"],
                    kind=child["tc_kind"],
                    text=child.astext(),
                ))
            elif isinstance(child, TcNarrativeNode):
                tc.narrative = child.astext()
            elif isinstance(child, TcContextNode):
                tc.context_environment = child.get("tc_environment") or None
                tc.context_scenario = child.get("tc_scenario") or None
            elif isinstance(child, TcEntryConditionsNode):
                tc.entry_conditions = child.astext()
            elif isinstance(child, TcExitConditionsNode):
                tc.exit_conditions = child.astext()
            elif isinstance(child, TcProcedureNode):
                tc.procedure = child.astext()
        env.tst_case_data[need_id] = tc

    # Validate: every TcBlockNode must be a descendant of a tst_unit_des NeedNode.
    for node in doctree.traverse(TcBlockNode):
        parent = node.parent
        in_tst = False
        while parent is not None:
            if isinstance(parent, NeedNode):
                ids = parent.get("ids") or []
                if ids and ids[0].startswith("tst_unit_des__"):
                    in_tst = True
                break
            parent = parent.parent
        if not in_tst:
            logger.warning(
                f"'{type(node).__name__}' is only valid inside a tst_unit_des need body.",
                location=node,
                type="tst_case",
                subtype="invalid_nesting",
            )

    # Enforce one tst_unit_des per file.
    if len(tst_nodes) > 1:
        logger.warning(
            f"Only one tst_unit_des per file; found {len(tst_nodes)} in '{docname}'.",
            location=tst_nodes[1],
            type="tst_case",
            subtype="one_per_file",
        )


# ---------------------------------------------------------------------------
# HTML visitor helpers
# ---------------------------------------------------------------------------

_CSS_CLASSES = {
    TcObjectiveNode: "tc-objective",
    TcNarrativeNode: "tc-narrative",
    TcContextNode: "tc-context",
    TcEntryConditionsNode: "tc-entry-conditions",
    TcExitConditionsNode: "tc-exit-conditions",
    TcProcedureNode: "tc-procedure",
}


def _make_html_visitors(css_class: str):
    def visit(self, node):
        self.body.append(
            self.starttag(node, "div", CLASS=f"tc-block {css_class}")
        )

    def depart(self, node):
        self.body.append("</div>\n")

    return visit, depart


def _skip_visit(self, node):
    raise nodes.SkipNode


# ---------------------------------------------------------------------------
# Extension entry point
# ---------------------------------------------------------------------------

def setup(app: Sphinx) -> dict:
    for node_cls, css in _CSS_CLASSES.items():
        visit_html, depart_html = _make_html_visitors(css)
        app.add_node(
            node_cls,
            html=(visit_html, depart_html),
            latex=(_skip_visit, None),
            text=(_skip_visit, None),
            texinfo=(_skip_visit, None),
        )

    app.add_directive("objective", ObjectiveDirective)
    app.add_directive("narrative", NarrativeDirective)
    app.add_directive("context", ContextDirective)
    app.add_directive("entry_conditions", EntryConditionsDirective)
    app.add_directive("exit_conditions", ExitConditionsDirective)
    app.add_directive("procedure", ProcedureDirective)

    app.connect("doctree-read", _process_tc_doctree)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
