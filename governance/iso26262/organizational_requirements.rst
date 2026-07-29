ISO 26262 Part 2 — Organizational Safety Requirements
==========================================================

These requirements apply at the **organization level** — independent
of any single product or project — per ISO 26262 Part 2 (Management
of Functional Safety). They are prerequisites that must exist before
any product-level safety work (HARA, safety goals, FSR/TSR/SSR) can
be considered valid.

Safety Culture
------------------

.. org_req:: Safety culture policy
   :id: ORG_SAFETY_CULTURE_001
   :status: draft
   :derives_from: ISO26262_2_5_4_2_1

   The organization shall establish and maintain a safety culture in
   which functional safety is recognized as an organizational value,
   and personnel are encouraged to report safety concerns without
   fear of blame.

Safety Management System
-----------------------------

.. org_req:: Safety management system definition
   :id: ORG_SMS_001
   :status: draft

   The organization shall define and maintain a safety management
   system describing roles, responsibilities, and processes for
   achieving functional safety across all projects.

.. org_req:: Project-independent tailoring rules
   :id: ORG_SMS_002
   :status: draft
   :derives_from: ORG_SMS_001

   The organization shall define rules for tailoring the safety
   lifecycle to a specific project, based on ASIL, project scope,
   and reuse of existing safety elements.

Competence Management
--------------------------

.. org_req:: Safety competence and training
   :id: ORG_COMPETENCE_001
   :status: draft
   :derives_from: ORG_SMS_001

   The organization shall ensure personnel performing safety-related
   activities have the necessary qualification, training, and
   experience, and shall maintain records of this competence.

Quality Management System Interface
----------------------------------------

.. org_req:: Quality management system alignment
   :id: ORG_QMS_001
   :status: draft
   :derives_from: ORG_SMS_001

   The organization's quality management system shall support the
   achievement of functional safety objectives (e.g., via ASPICE
   process assessments feeding into safety confirmation measures).

Confirmation Measures
--------------------------

.. org_req:: Confirmation measures — audit, assessment, confirmation review
   :id: ORG_CONFIRMATION_001
   :status: draft
   :derives_from: ORG_SMS_001

   The organization shall define and perform, independent of the
   project, functional safety audits, safety assessments, and
   confirmation reviews as required by the project's ASIL.

Field Monitoring
--------------------

.. org_req:: Field monitoring process
   :id: ORG_FIELD_MONITORING_001
   :status: draft
   :derives_from: ORG_SMS_001

   The organization shall establish a process to monitor field data
   for safety-related issues after release, and feed findings back
   into the safety lifecycle (including potential HARA/FMEA/DFA
   updates at platform or product level).
