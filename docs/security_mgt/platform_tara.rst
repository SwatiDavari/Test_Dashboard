Platform TARA (Threat Analysis and Risk Assessment)
========================================================

.. note::
   Placement inferred by structural symmetry with the confirmed
   ``docs/safety_mgt/`` pattern — not independently verified against
   S-CORE's Security Analysis Work Products page in this session.

.. threat:: Unsigned firmware injection
   :id: THR_OTA_001
   :status: approved

   An attacker delivers unsigned or modified firmware through the
   OTA update channel.

.. cyber_goal:: Ensure firmware authenticity
   :id: CG_OTA_001
   :status: approved
   :derives_from: THR_OTA_001

   The system shall only accept firmware from an authenticated,
   trusted source.
