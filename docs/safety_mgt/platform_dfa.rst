Platform DFA (Dependent Failure Analysis)
=============================================

Confirmed S-CORE work product: analyses dependencies between features,
referencing all platform feature static architecture diagrams and
highlighting potential shared use of features/components with
different ASIL.

.. hazard:: OTA update corruption hazard
   :id: HAZ_OTA_001
   :status: approved

   Corrupted or malicious firmware installed via OTA update.

.. safety_goal:: Prevent unsafe firmware installation
   :id: SG_OTA_001
   :status: approved
   :derives_from: HAZ_OTA_001

   The vehicle shall never install firmware that has not been
   verified as authentic and complete.

.. fsr:: Functional safety requirement — firmware verification
   :id: FSR_OTA_001
   :status: approved
   :derives_from: SG_OTA_001

   The system shall verify firmware integrity and authenticity
   before any flashing operation begins.

.. tsr:: Technical safety requirement — signature check
   :id: TSR_OTA_001
   :status: approved
   :derives_from: FSR_OTA_001

   The bootloader shall perform a cryptographic signature check
   prior to firmware activation.

Platform DFA notes
--------------------

(placeholder — dependency analysis across OTA / COM / other platform
features sharing the signal-routing infrastructure would be captured
here as prose + a needflow diagram, once feature/component-level DFAs
below are populated)
