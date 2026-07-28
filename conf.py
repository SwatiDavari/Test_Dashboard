# Configuration file for Sphinx + Sphinx-Needs
# Product: product-x
# Standards in scope: ASPICE, ISO 26262, ISO/SAE 21434

project = "product-x"
author = "Engineering"
extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
]

# ---------------------------------------------------------------------------
# Sphinx-Needs: need types (one entry per ID prefix in the unified ID scheme)
# ---------------------------------------------------------------------------
needs_types = [
    # --- Product enabler ---
    dict(directive="sys_req",     title="System Requirement",      prefix="SYS_",  color="#3A00F5", style="node"),
    dict(directive="prod_req",    title="Product Requirement",     prefix="PROD_", color="#4B00FF", style="node"),
    dict(directive="feat_req",    title="Feature Requirement",     prefix="FEAT_", color="#4FE0C4", style="node"),
    dict(directive="mod_req",     title="Module Requirement",      prefix="MOD_",  color="#66E8AA", style="node"),
    dict(directive="cmp_req",     title="Component Requirement",   prefix="CMP_",  color="#72E27A", style="node"),
    dict(directive="arch",        title="Architecture Element",    prefix="ARC_",  color="#8FEA6B", style="node"),
    dict(directive="design",      title="Design Element",          prefix="DES_",  color="#A7F04A", style="node"),

    # --- Test enabler ---
    dict(directive="utc",         title="Unit Test Case",          prefix="UTC_",  color="#C4FF32", style="node"),
    dict(directive="itc",         title="Integration Test Case",   prefix="ITC_",  color="#C4FF32", style="node"),
    dict(directive="stc",         title="System Test Case",        prefix="STC_",  color="#C4FF32", style="node"),

    # --- Safety enabler (ISO 26262) ---
    dict(directive="hazard",      title="Hazard",                  prefix="HAZ_",  color="#FF4D6D", style="node"),
    dict(directive="safety_goal", title="Safety Goal",             prefix="SG_",   color="#FF4D6D", style="node"),
    dict(directive="fsr",         title="Functional Safety Req",   prefix="FSR_",  color="#FF4D6D", style="node"),
    dict(directive="tsr",         title="Technical Safety Req",    prefix="TSR_",  color="#FF4D6D", style="node"),
    dict(directive="ssr",         title="Software Safety Req",     prefix="SSR_",  color="#FF4D6D", style="node"),

    # --- Security enabler (ISO/SAE 21434) ---
    dict(directive="threat",      title="Threat Scenario",         prefix="THR_",  color="#FF9E4D", style="node"),
    dict(directive="cyber_goal",  title="Cybersecurity Goal",      prefix="CG_",   color="#FF9E4D", style="node"),
    dict(directive="cyber_req",   title="Cybersecurity Req",       prefix="CR_",   color="#FF9E4D", style="node"),

    # --- Documentation enabler ---
    dict(directive="doc_ref",     title="Documentation Reference", prefix="DOC_",  color="#9D9DB8", style="node"),
]

# Link types connecting the enablers (used for traceability matrices / gates)
needs_links = [
    dict(option="derives_from", incoming="derived by",   outgoing="derives from"),
    dict(option="verifies",     incoming="verified by",  outgoing="verifies"),
    dict(option="mitigates",    incoming="mitigated by", outgoing="mitigates"),   # cyber_req -> threat
    dict(option="satisfies",    incoming="satisfied by", outgoing="satisfies"),   # ssr->tsr->fsr->safety_goal
]

# IDs are required to be explicitly authored (not auto-generated) so that
# ASPICE/ISO 26262/21434 audits can trace a stable ID across revisions.
needs_id_required = True
needs_id_regex = r"^[A-Z]+_[A-Za-z0-9_]+$"

# Statuses used across all need types (tailor per-project as needed)
needs_fields = {
    "status": {
        "schema": {
            "enum": ["draft", "review", "approved", "obsolete"]
        }
    }
}

# Traceability gate: fail build on orphan needs (no incoming/outgoing links)
needs_report_dead_links = True

html_theme = "sphinx_rtd_theme"
master_doc = "index"
