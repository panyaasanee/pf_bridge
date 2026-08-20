Raw lane findings from round 83 (DAMAGE-MODEL-001), 2026-08-19.
Investigation scratch, NOT evidence. Kept because /tmp is ephemeral.

WARNING - these contain errors that the verifier caught and corrected.
The authoritative artifact is:
  reports/PF_DAMAGE_MODEL001_CLIENT_HIT_RESULT_EXPECTATION_20260819.md
  tools/pf_damage_hit_result_static.py   (235/235 guards)
Known errors in these raw docs:
 - LANE B: called element+0x18 the damage number. It is a yaw angle.
 - LANE B: attributed 0x751xxx sites to CHitResult. They are CMissileHitResult.
 - LANE C: "whole-.text sweep, 393,711 instructions" actually covered ~15% of
   .text - capstone linear disasm halts at the first undecodable byte (0x521C0C).
   Its blanket "no arithmetic store to attr+0x44 anywhere" is therefore UNPROVEN
   and was not pinned. A resumed sweep decodes 2,893,637 instructions and finds
   20 arithmetic stores at those displacements (none in the damage path).
