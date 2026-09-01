ถึง: LANE-A / chief — ผล RE-197 (static bridge)

# RE-197 RESULT — DONE / PASS: 51-byte PC is empty GetWorldInfo + TargetPos, not a button discriminator

- Ticket START: `2026-09-02T03:27:00+07:00`
- Result time: `2026-09-02T03:33+07:00`
- Queue SHA-256 at start: `2443e5d19563b7c8933238f6821f7b65f419a8073e13a9adb857524a5fb413ce`
- Static/read-only only: no game/server boot, no `LOCK_GAME`, no canonical DB, no source/queue/external/gamedata edit.

## Mandatory searches

- ค้นใน `pf_bridge\external\` แล้ว: เจอ `GetWorldInfoVital` ใน `PF_FIELD_VALIDATION.tsv` (W observed 15; R observed 1), `PF_PROTOCOL_REGISTRY.tsv`, และ `PF_SERIALIZER_FIELDS.tsv`; scope = 2,683 files / 930,201,065 bytes, terms `GetWorldInfoVital`, `gt192_20260901_184254`, `WORLDINFO_RECORD_SKELETON`, `#1398`, `51 bytes`. ของใน external ช่วยยืนยัน identity/static schema แต่คำตอบชี้ขาดมาจาก raw capture ด้านล่าง.
- ค้นใน `pf_bridge\gamedata\` แล้ว: ไม่เจอ identifier/capture/address ข้างต้นใน 1,109 files / 15,319,585 bytes. ผลลบจำกัดเฉพาะ extracted gamedata tree.

## Job 1 — structure of `[G< #1398]`: CLOSED

Raw input:

`GameClient\capture_gt192_20260901_184254\capture_v141\GAME_20260901_184516_220559_53370.txt`

- File size 6,293,505; SHA-256 `326ae19764e4fe4742d9eb9591c15638def5ad9733a16b42276692a5eae436d1`.
- Evidence lines 62933-62944; decompressed-PC evidence lines 62939-62942.
- Exact 51-byte PC SHA-256 `15af2ddd31a6ebacc55ed8b8813cbc04b023c600ed202e5cdb5bda3b30f24484`.

Decoded using tag boundaries and the named ID crosswalk (`PF_VITAL_NAMES.json` SHA-256 `781d745f6d32e4cb32661c7da96ea76ecb331d0d78ea7fbc95b1412f8bdd98cc`):

1. Outer `GSCN_RunTimeProtocolReq (0x6E6F)`, version 0, mask `0x02`, `vital_count=2`.
2. Vital 1: `GetWorldInfoVital (0x3D4B)`, version 0, payload exactly `0B 00` — the known 2-byte **empty form**, not the 248-byte full payload.
3. Vital 2: `TargetPosVital (0x2A90)`, version 0, 24-byte payload `f32 x/y/z/heading` (four `0x2A`-tagged fields) then `u8 moving/mask` (two `0x0B`-tagged fields). Its values in #1398 decode to approximately `(19350.82, -7809.948, 490.0, 1.851113, moving=1, mask=0)`.

The TargetPos identity/schema is not inferred from equal numeric IDs: it is pinned independently by `PF_VITAL_NAMES.json` and `PF_MOVE_AUTHORITY001_TARGETPOS_PRODUCER_STATIC_20260818.md` SHA-256 `78777e44137f14910d365b8f0bfd4ad53b1fab0714894c7d9dc953d6e0740caa`.

Therefore “51-byte GetWorldInfoVital” is an imprecise label for a **two-vital bundle**. It is not a shortened instance of the 268-byte full form by itself.

## Job 2 — can it distinguish UI-A versus UI-B?: CLOSED / NO

- Full forms `#1396` and `#1401` (capture lines 62901-62919 and 62972-62990) are each 268 bytes, byte-identical, SHA-256 `25759397ed0de2c4353c29139483e0736f8329a8b66aaa1fdd55191da8b6147c`.
- `#1398` contains no `LogoutVital (0x1B40)` and no logout subcode. The UI-A subcode `3` already arrived one frame earlier in `#1397`; the 51-byte bundle carries only empty-worldinfo framing plus position/movement state.
- The exact same 51-byte structural bundle occurs outside this UI-A/UI-B sequence, with only TargetPos values/flags changing:
  - `capture_adhocprobe_20260827_212411\capture_v141\GAME_20260827_212521_090231_56722.txt`, file SHA-256 `c4453ea74efb511836d6dd0d25d166bf11369952c7642d5f0cae7db6261a9594`, lines 57197-57207, PC SHA-256 `4681dbac38c6b165abdb68182cf7556c7020411b712461e2764966a0a0159f6c`.
  - `capture_gt172_20260901_011757\capture_v141\GAME_20260901_014410_588285_61976.txt`, file SHA-256 `e1f4c6a9004cba6b38c058bfe9bfa3c50c08b8ffe7900bacaa8ffac4cd0a7581`, lines 801-811 and 1002-1012, PC SHA-256 `e1a0729412c6ffcb48bb879d94d6ac25fced3542250e2091083b132fa817d683` / `add471d7141f90a9a3743844c8407710915897a55a782e72c41b5cd228b54d32`.

This repeated generic shape is positive evidence that #1398 is ordinary empty-GetWorldInfo bundled with a movement report, not a button-specific code path. It cannot serve as a reliable pre-click classifier.

## Job 3 — UI-B byte differential: CLOSED / BOUNDED NEGATIVE

The one owner-operated GT-192 session has no `#1398`-equivalent GetWorldInfo+TargetPos bundle immediately after UI-B `#1402`; subsequent `#1403/#1404` are `COnLandVital + TargetPosVital`, not GetWorldInfo. No second owner-operated UI-B capture with a paired 51-byte candidate was found in the searched capture paths.

That n=1 absence is **not** promoted into a UI-B semantic claim. A clean A/B frequency claim would require repeated captures under matched movement state. This does not affect the structural answer above: the 51-byte PC itself has no button field/subcode and occurs in unrelated sessions.

## Relation to current source

`logout_hypothesis.py` SHA-256 `17d5e9280fd86cf6abc8780a0668998bbacd625574ea4dd9005b186c3b709b70` already defines `WORLDINFO_EMPTY_RECORD = 0B00` and documents that this empty form fires mid-gameplay without logout correlation. The full-form recognizer requires the 248-byte payload (two 123-byte records plus `0B00`) and is structurally distinct from #1398.

## Input/output integrity

- `PF_FIELD_VALIDATION.tsv` SHA-256 `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`.
- `PF_SERIALIZER_FIELDS.tsv` SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`.
- Source request note (consumed) SHA-256 `9be5dd99bdf414135875886b254b33f3828e0518684db29fbf2d33cd219e571c`.
- Queue, capture inputs, external tables, and server source were rehashed after analysis and remained unchanged. Only this result letter and runner bookkeeping are written.

## Nonclaims

- This is wire/capture evidence only; no client-observable behavior was tested in this RE round.
- It does not explain why the client bundles empty GetWorldInfo with TargetPos or prove original-server semantics.
- It does not validate or falsify whether `HYP-PF-040` changes the screen; `production_allowed` remains `False`.
- It does not infer a UI-B rule from one missing equivalent frame.
- It does not claim the TargetPos coordinates themselves have logout meaning.

## BUILD_IMPACT

`BUILD_IMPACT: do not use #1398 as the UI-A/UI-B discriminator or as a dialog-open trigger. Treat it as the known empty GetWorldInfo form bundled with TargetPos noise. Keep the 268-byte full-form classifier separate; for actual button choice, the proven discriminator remains LogoutVital's own subcode (3 vs 1) or a future independently captured pre-click signal. No source patch was made by the RE runner.`
