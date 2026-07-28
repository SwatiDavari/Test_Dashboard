Signal Router Component FMEA
==============================

Confirmed S-CORE work product: FMEA verifies the component
architecture (as part of the SW Safety Concept). Detections,
preventions, mitigations linked to Software Component Requirements or
Assumptions of Use.

.. cmp_req:: Signal router component requirement
   :id: CMP_SIGNALROUTER_001
   :status: draft
   :derives_from: ARC_COM_001

   The signal-router component shall forward validated OTA payload
   signals from the update-server-interface to the bootloader-interface
   without modification.

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
