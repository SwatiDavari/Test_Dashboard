OTA Requirements
=================

.. feat_req:: OTA feature requirement — signed update delivery
   :id: FEAT_OTA_002
   :status: approved
   :derives_from: PROD_OTA_001

   The OTA feature shall deliver signed firmware packages end to end
   from the update server to the target ECU.

.. note::
   Architecture for this requirement is detailed at module level —
   see ``modules/com/requirements/index`` (``ARC_COM_001``), which
   derives from the product-level ``ARC_OTA_001`` in
   ``product-x/architecture/index``.
