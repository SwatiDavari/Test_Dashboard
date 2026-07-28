COM Module Requirements & Architecture
=========================================

Per S-CORE convention, module-level documentation merges requirements
and architecture into a single work product (rather than keeping
architecture as a separate folder at feature level).

.. mod_req:: COM module requirement — signal routing
   :id: MOD_COM_001
   :status: approved
   :derives_from: FEAT_OTA_001

   The communication module shall route OTA payload signals between
   the update server interface and the bootloader interface.

.. arch:: COM module architecture — signal routing block
   :id: ARC_COM_001
   :status: approved
   :derives_from: ARC_OTA_001
   :satisfies: MOD_COM_001

   Decomposition of the product-level OTA architecture element
   (``ARC_OTA_001``) into this module's internal block structure:
   update-server-interface -> signal-router -> bootloader-interface.
