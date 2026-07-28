OTA Feature
============

.. feat_req:: OTA feature requirement
   :id: FEAT_OTA_001
   :status: approved
   :tags: ota
   :derives_from: PROD_OTA_001

   The OTA feature shall deliver signed firmware packages to the target ECU.

.. toctree::
   :maxdepth: 1

   requirements/index
   design/index
   docs/safety_mgt/feature_fmea
   docs/safety_mgt/feature_dfa
   docs/security_mgt/feature_tara
   modules/com/index
   tests/index

.. note::
   Detailed architecture for this feature is not a separate folder —
   following S-CORE convention, architecture is documented together
   with requirements at the module/component level (see
   ``modules/com/requirements/index``), and only referenced/summarized
   here at feature level.
