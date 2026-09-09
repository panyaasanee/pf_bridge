# STANDING A4 ADDENDUM — empty CBuffAttr preserves the action token

**ADDRESSEE:** Chief / LANE-B combat runtime owner  
**DATE:** 2026-09-09 15:07 +07:00  
**STATUS:** STATIC COMPOSITION PASS for the fresh/current hostile actor path  
**LANE:** fixed Binary + read-only current producer; no client/server run

## Result

The 14:49 A4 result left `0x0064D580` as a possible action-token modifier.
The object at `CActor+0x248` is the typed `CBuffAttr` already pinned by the
attribute census and the 10:07 Standing B1 result.  This pass composes that
existing identity into the A4 callback and re-derives the decisive bytes.

1. The common actor constructor calls factory `0x0043F2B0` and stores its
   result at `CActor+0x248` (`0x004433BC..0x004433D5`).
2. That factory calls the `CBuffAttr` constructor `0x0064A160`; its subobject
   constructor `0x0064DE70` sets the three record-list heads at subobject
   `+0x08`, `+0x14`, and `+0x20` to null.  Relative to `CBuffAttr`, these are
   the three buckets at `+0x30`, `+0x3C`, and `+0x48` already pinned by the
   container census.
3. `0x0064D580` first rejects an empty input string.  For a nonempty token it
   tests those three heads in order at `0x0064D5C3..0x0064D5EA`.  If all are
   null, `0x0064D5EC..0x0064D5F1` jumps to the return path at `0x0064D6B3`
   before uppercase conversion, lookup, or assignment.
4. The current `field_mobs.hostile_actor_entry` producer gives
   `make_remote_actor_entry` exactly two attributes: `NPC_ATTR_ID` and
   `MOVEMENT_ATTR_ID`.  It does not seed a CBuffAttr record in the actor-entry
   body.

Therefore a freshly created Tornado Eagle on this current producer path, with
no separate `CBuffVital` applied before the action, preserves all six A4
tokens byte-for-name through `0x0064D580`.  Together with the 14:56 prefix
addendum, the static known keys are the exact M011 descriptor keys:

```text
.\Data\GC\A\M011_F_SENTRY_000.kf
.\Data\GC\A\M011_F_FLEX_000.kf
.\Data\GC\A\M011_F_ATTACK_000.kf
.\Data\GC\A\M011_F_ATTACK_001.kf
.\Data\GC\A\M011_F_ATTACK_002.kf
.\Data\GC\A\M011_F_ATTACK_003.kf
```

## Search-before-disassembly result

- `external/` already contained the exact `CBuffAttr` class and bucket rows;
  these were hash-checked and used as prior identity/role evidence.
- `notes_to_chief/` already contained the 10:07 Standing B1 CBuffVital result;
  this pass does not repeat its codec or stat-effect work.
- No prior result connected the empty-bucket return in `0x0064D580` to the A4
  animation callback, so the composition above is the new result.

## Fixed-image provenance

Image `GameClient.local.bin`: 14,759,424 bytes; SHA-256
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
before and after.

| role | VA span | file span | SHA-256 |
|---|---|---|---|
| common actor constructor and `+0x248` store | `0x00443160..0x00443450` | `0x00042560..0x00042850` | `7591b36cf736dc1e12a1373126bd8438446eed5b1618b514d4ab7295c643fd49` |
| CBuffAttr factory path | `0x0043F2B0..0x0043F3C4` | `0x0003E6B0..0x0003E7C4` | `4bc1d2b9aef3fa69cec5a7669c3516668632d0646af2e7a26493caefd41a5687` |
| CBuffAttr constructor | `0x0064A160..0x0064A1BA` | `0x00249560..0x002495BA` | `67b6b7dbbaf3d73aec3859cd20d4d2ab45e98f9efa91ea2b33065d4e19c134ea` |
| empty CBuffAttr subobject constructor | `0x0064DE70..0x0064DF35` | `0x0024D270..0x0024D335` | `3fe6e11ffc51c2f1d80595e200059430987bd10e85edac9600bfca44a77fde68` |
| action-token modifier | `0x0064D580..0x0064D6BA` | `0x0024C980..0x0024CABA` | `a914ce974770dfd6b1d4e10dcae2be7a609c51d5df19e9dd83009a86b89c3e59` |
| CBuffAttr wire codec | `0x0064A430..0x0064A58A` | `0x00249830..0x0024998A` | `738d40cfef5b7ec3f4d74c3f148bd688b7ec6e3c6a8aa90cda67da702dac1e42` |

Current read-only producer:
`src/pirateforce_foundation/field_mobs.py`, SHA-256
`c518827e738159291a14e357c0daa83dd3592c2add7186df12c25ff5a378a3dc`.

## Evidence grade and nonclaims

- **A:** CBuffAttr construction, three null bucket heads, the modifier's
  all-empty early-return branch, and the six unchanged-token known answers.
- **Exact current-source fact:** the hostile actor-entry producer lists only
  NPCAttr and MovementAttr.  This is not a runtime observation that the entry
  was sent or accepted.
- A later separate CBuffVital can populate one or more buckets and make the
  modifier enter its replacement lookup.  This pass does not claim the
  modifier is universally or permanently a no-op.
- This pass does not claim that no plugin/scenario can send CBuffVital, that a
  live actor's buckets stayed empty, that the action map returned a record,
  that any clip rendered, or that selector 3220 caused damage.
- It does not assign gameplay semantics to individual buff-record fields or
  claim that every possible nonempty bucket changes every token.

## Verification

- verifier: `pf_bridge/staged/standing_a4_buff_modifier_verify.py`
- verifier SHA-256: `47749436ef479c97a69083204e5fb42116101660c4ed7490046d87ed7ba1afab`
- log: `pf_bridge/staged/standing_a4_buff_modifier_verify.log`
- log SHA-256: `d68d7663be3b63b6f2ec4d28d02cde985d29cda4619e2eb8e3d279192e20b699`
- result: `PASS spans=6 calls=3 hostile_attrs=2 known_noops=6 traps=4; fresh empty CBuffAttr preserves all A4 tokens; later CBuffVital remains a live-state precondition`

The stdlib-only verifier re-runs the A4 asset/callback/prefix dependency
guards, checks six image spans and three call edges, parses the current
producer with `ast`, checks six known no-op tokens, and rejects each nonempty
bucket plus an added-attribute mutation.

## BUILD_PROPOSED

Run the first selector-3220 attended test on a newly published Tornado Eagle
without sending CBuffVital before the action.  Record the three CBuff bucket
heads once at the callback boundary as a guard, then prioritize final path,
map return, visible clip, number, resident/HUD HP decrease, and the second
cycle.  Stop if any bucket is nonempty, the map lookup is null, or the live
preset differs from `M011_000_000_SP3`. | LANE-B / attended-test owner |
fresh actor + three zero heads + exact final key + nonnull map result + visible
clip/damage correlation
