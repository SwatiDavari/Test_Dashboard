OTA Feature FMEA
==================

Confirmed S-CORE work product: FMEA verifies the feature architecture
(as part of the SW Safety Concept). Detections, preventions,
mitigations linked to Software Feature Requirements or Feature
Assumptions of Use.

.. ssr:: OTA software safety requirement — firmware verification
   :id: SSR_OTA_001
   :status: approved
   :satisfies: TSR_OTA_001

   The OTA update mechanism shall verify firmware signature before
   flashing.

FMEA table (placeholder)
----------------------------

.. list-table::
   :header-rows: 1

   * - Failure Mode
     - Effect
     - Detection
     - Prevention/Mitigation
     - Linked Requirement
   * - Corrupted firmware image received
     - Vehicle bricked / unsafe behavior on boot
     - CRC + signature check on receipt
     - Reject and retry from server
     - SSR_OTA_001
