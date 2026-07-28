Signal Router Component FMEA
==============================

Confirmed S-CORE work product: FMEA verifies the component
architecture (as part of the SW Safety Concept). Detections,
preventions, mitigations linked to Software Component Requirements or
Assumptions of Use.

See :need:`CMP_SIGNALROUTER_001` (defined in
``requirements/index.rst``) for the component requirement this FMEA
verifies.

FMEA table (placeholder)
----------------------------

.. list-table::
   :header-rows: 1

   * - Failure Mode
     - Effect
     - Detection
     - Prevention/Mitigation
     - Linked Requirement
   * - Signal dropped mid-route
     - Incomplete firmware image assembled
     - Sequence number gap check
     - Retransmission request
     - CMP_SIGNALROUTER_001
