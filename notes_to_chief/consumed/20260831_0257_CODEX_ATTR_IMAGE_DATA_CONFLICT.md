# CODEX ATTR IMAGE/DATA CONFLICT - 2026-08-31 02:57 +07:00

Read-only static re-derivation found a source-layer conflict that must remain explicit.

- IMAGE has an optional MOBS-runtime `f_SCALE` query at VA 0x004A2FC3; the runtime slot is initialized to 0.0 at VA 0x004A2020.
- Current original DATA table MOBS in `GameClient/Data/B_CONSTDATA_TH.pc_` has 54 columns and does not contain `f_SCALE`, `n_STRIDE_WALK`, `n_STRIDE_RUN`, `n_FACTION`, or `n_ENEMY`.
- `n_FACTION` is nevertheless resolved by a separate exact path: MOBS `n_AI_WANDER` selects an AI_WANDER row; DATA AI_WANDER has `n_FACTION`; IMAGE stores that value in the MOBS runtime object at +0xF8 and then copies it to BasicAttr +0x68. It must not be described as a direct MOBS DATA column.
- The actual unresolved cross-source mismatch here is `f_SCALE`: IMAGE probes it as an optional MOBS value, while current DATA MOBS has no such column, so the runtime slot remains its 0.0 constructor default on this DATA set. The meaning of 0.0 is not inferred.
- IMAGE and DATA facts remain separate rows and are not merged into one source claim.

No client/server/runtime/test/Git/lease action was performed. No proprietary raw bytes or decoded row values are included.
