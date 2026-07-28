Traceability Overview
=======================

This page renders live traceability tables/graphs from every ``need``
defined across the repo (requirements, architecture, safety, security,
tests). Regenerate via ``sphinx-build`` — nothing here is hand-maintained.

All requirements
-----------------

.. needtable::
   :columns: id, title, status, tags

Unlinked (orphan) needs — traceability gate check
----------------------------------------------------

.. needtable::
   :filter: len(links) == 0 and len(links_back) == 0
   :columns: id, title, type

Safety chain: Hazard → Safety Goal → FSR → TSR → SSR
--------------------------------------------------------

.. needflow::
   :types: hazard, safety_goal, fsr, tsr, ssr
   :link_types: derives_from

Security chain: Threat → Cyber Goal → Cyber Requirement
-------------------------------------------------------------

.. needflow::
   :types: threat, cyber_goal, cyber_req
   :link_types: derives_from, mitigates
