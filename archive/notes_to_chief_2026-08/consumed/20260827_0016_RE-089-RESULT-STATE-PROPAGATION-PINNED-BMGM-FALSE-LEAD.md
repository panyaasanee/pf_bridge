[ถึง: chief cloud · COO · LANE-GM | จาก: RE runner local · 2026-08-27T00:16+07:00]

# RE-089 RESULT — DONE/BOUNDED-NEGATIVE · STATE PROPAGATION PINNED · `bm_gm.tga` FALSE LEAD

- ใบ: `RE-089 GM-STATE-VISUAL-001 [STATIC-ON-BRIDGE]`
- วิธี: static/read-only เท่านั้น · ImageBase ของ VA ทุกจุดด้านล่าง = `0x00400000`
- verdict หนึ่งบรรทัด: handler พินได้ว่า wire `+0x14/+0x15` ถูก normalize ด้วยเงื่อนไข **เท่ากับ 1 เท่านั้น** แล้วเก็บเป็น `GMModule_Client+0x18/+0x19`; u32 `+0x18` ถูกก๊อปตรงไป `GMModule_Client+0x1C`. แต่ static ไม่ให้ semantic label ว่า byte ไหนคือ `is_gm` หรือ u32 คือ level และไม่พบ direct render/visibility crosswalk. เบาะแส `bm_gm.tga` ในใบถูกหักล้าง: มันคือ glyph `0x29` = **green minus** ใน `FxNumberCache`, ไม่ใช่ไอคอน Game Master.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** registry row ของ `GM_UpdateGMStateVital` (vtable `0x00F4631C`, serializer `0x00729720`, handler `0x00729F00`), serializer rows 6 แถว (`W/R × 3 fields`) และ validation W/R เป็น `NOT_OBSERVED`/0 frame. ชุดส่งมอบตอบ wire layout/span ได้ครบ แต่ **ไม่ตอบ semantic หรือ UI consumer**; รอบนี้จึงเปลี่ยนเป็น verify SHA → re-derive state flow → ใช้แบบ bounded.
- **ค้น gamedata แล้ว: ไม่เจอ** vital name/id/VA, `GMModule_Client`, `GMState`, `bm_gm.tga`, GM level/state/icon crosswalk ในดัชนี/ตาราง/Lua/scene ทั้ง tree. พบ lexical hit `GAMEMASTER/gamemaster` เพียงสองแถวใน `TEXTDATA_TH__DIRTYWORD.tsv`/`DIRTYTITLE.tsv`; เป็น blacklist text คนละ namespace จึงไม่ join และไม่ใช้เป็นหลักฐาน semantic.

## T0 — handler และ field-to-state mapping

### wire layout ที่ verify ซ้ำ

- serializer `[0x00729720,0x00729785)` SHA-256 `03b186737b43884c61c7e82dc9805f7ee161cce3ae3436f2c5d0a5db8033c661` ตรงอิมเมจจริง:
  1. tag `0x0B`, 1 byte, object `+0x14`
  2. tag `0x0B`, 1 byte, object `+0x15`
  3. tag `0x14`, 4 bytes, object `+0x18`
- handler `[0x00729F00,0x00729F5D)` SHA `89b9c320510c7aa61fe92a2bf41c8b761661db2cf8ccd467ca098ca554689e46`; recursive CFG `93/93`, gap/error `0/0`.
- `0x00729F13` ขอ `GMModule_Client` ด้วย type token `0x00F462D4`; หลัง type checks แล้ว `0x00729F53` ส่ง vital เข้า state sink `0x00727AB0`.

### assignment จริงใน `0x00727AB0`

branch ของ `GM_UpdateGMStateVital` `[0x00727AB0,0x00727B39)` SHA `a9b6ab0fbd5fdec56b463ce65834f2667c483340488a3fbc3e56bfddcd80a088`; bounded recursive CFG ครบ `137/137`, gap/error `0/0`:

| wire/object field | exact use | destination |
|---|---|---|
| byte `+0x14` | `cmp [msg+0x14],1; sete` @ `0x00727B09-0x00727B0D` | `GMModule_Client+0x18` @ `0x00727B10` |
| byte `+0x15` | `cmp [msg+0x15],1; sete` @ `0x00727B13-0x00727B17` | `GMModule_Client+0x19` @ `0x00727B1A` |
| u32 `+0x18` | load unchanged @ `0x00727B1D` | `GMModule_Client+0x1C` @ `0x00727B20` |

ข้อสำคัญ: byte input ค่า `2..255` กลายเป็น `0`; code ไม่ได้ใช้ generic nonzero truth. Branch นี้เขียน state แล้ว return success โดยไม่มี call ไป renderer/widget/texture loader.

## T1 — state consumer ที่พินได้ และเหตุผลที่ `bm_gm.tga` ใช้ไม่ได้

### state-export adapter เพียงจุดที่พินได้

`GMModule_Client` vtable slot ที่ `0x00F4624C` ชี้ `0x00726D30`. ฟังก์ชัน `[0x00726D30,0x00726D62)` SHA `bba473c432f5bedf3f6f2d281c4450e304601faa44e7999b29b1b31898159e48`; recursive CFG `50/50`, gap/error `0/0`. มันตอบเฉพาะ argument/record ที่ `+0x10 == 0x25`:

- module `+0x19` → argument byte `+0x14`
- module `+0x1C` → argument dword `+0x18`
- `bool(module+0x18)` → argument qword `+0x20/+0x24`

นี่พิสูจน์ **state projection** ออกจาก module แต่ type-`0x25` argument ยังไม่มี semantic crosswalk ไป widget/render call; จึงห้ามเรียก destination ทั้งสามว่า icon/prefix/permission/level จาก offset อย่างเดียว. Byte-level census พบ `0x00726D30` ไม่มี direct `E8` caller และมี absolute pointer จุดเดียวที่ vtable; virtual callers จึงเป็นเพดาน static ที่ยังเปิด.

### `bm_gm.tga` คือ green-minus glyph

- ASCII path `0x00F859A4` = `.\Data\CP\bmmsg\bm_gm.tga`; image-wide dword-xref มีจุดเดียว `0x00A7E123` ใน `FxNumberCache` loader.
- loader ชุดเดียวกันจับคู่ชื่อ/รหัสต่อเนื่อง:
  - `bm_gp.tga` → glyph `0x28` @ `0x00A7E01E` (green plus)
  - `bm_gm.tga` → glyph `0x29` @ `0x00A7E17F` (green minus)
  - `bm_bp.tga` → glyph `0x2A` @ `0x00A7E2F8` (blue plus)
  - `bm_bm.tga` → glyph `0x2B` @ `0x00A7E490` (blue minus)
- ช่วง cache builder `[0x00A7DF8D,0x00A7E45D)` SHA `a33fa6cbb9e5a9471fcfdb1096fb9ec2dff081c0941def95ebf64c6b31cd7763`; ตรงกับ independent damage audit `drafts/DAMAGE_MODEL001_lanes_20260819/LANE_C_CLIENT_COMPUTATION.md` SHA `f88b56405ce226b818bde19d09a3c164e2e9c950b17bf424cb5d103e67b06b78`.
- ดังนั้น `gm` ใน filename นี้คือ **green minus**, ไม่ใช่ `Game Master`; ไม่มี direct crosswalk จาก `0x00729F00`, module state members หรือ type token `0x00F462D4` มายัง asset นี้.

## T2/T3 — semantic และ UI bounded negative

- type-token `GMModule_Client` (`0x00F462D4`) มี image literal xrefs 4 จุด: GM tool/panel producer `0x0072883D`, dedicated GM editor producer `0x0072950A`, update-state handler `0x00729F14`, registrar `0x00C07DA1`. Census นี้ไม่พบ direct link ไป glyph loader.
- state sink `0x00727AB0` มี direct callerเดียว `0x00729F53`; ไม่มี secondary callback/render call ใน update branch.
- u32 ถูกก๊อปตรงสองทอด (`wire +0x18 → module +0x1C → type-0x25 arg +0x18`) โดยไม่มี compare/switch/arithmetic ในสองช่วงที่พิสูจน์ จึง **ห้ามเรียก `gm_level` หรือ permission bitmask**.
- byte แรก/byte ที่สองถูก normalize แยกกัน แต่ไม่มี semantic discriminator; จึง **ห้ามเลือก byte ใดเป็น `is_gm`** และห้ามตั้งอีก byte เป็น mute/talk/UI flag.
- external validation ยัง 0 frame ทั้ง W/R. เพดานที่ถูกต้องคือ capture/attended matrix ที่ควบคุม tuple `(byte0,byte1,u32)` และสังเกต dedicated GM UI/chat/event output แยกจากกัน; runner รอบนี้ไม่เปิดใบใหม่เอง.

## verifier / reproducibility

- `pf_bridge\staged\re089_gm_state_visual_static.py`
- SHA-256 `7e0bb0f636d17dfc03fa86201f2c625fdf2ffe2e5a9dad02d681d3a257378c8d`
- รัน `py -3 -B` อิสระ 2 ครั้ง: PASS เหมือนกัน · exit `0/0`
- CFG pins: handler `93/93`, GM-update branch `137/137`, state adapter `50/50`, module ctor `48/48`; gap/error `0/0` ทุกช่วง.
- image pin `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`; registry `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`; serializer fields `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`; validation `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`.

## nonclaims

1. ไม่มีหลักฐานชั้น client-observable ในใบ static นี้โดยเจตนา; ไม่อ้างว่า UI เปิด/ปิดหรือมีไอคอนใดปรากฏจริง.
2. ไม่อ้างว่า type-`0x25` adapter เป็น UI renderer; พิสูจน์เพียงการก๊อป state ไป record ที่ยัง opaque.
3. ไม่อ้างว่าไคลเอนต์ไม่มี visual GM indicator ที่อื่น; พิสูจน์เฉพาะว่า `bm_gm.tga` จุดที่ใบชี้มาเป็น damage-number green-minus และไม่มี direct state crosswalk.
4. ไม่ตั้ง semantic จาก width/offset/ค่าเท่ากัน และไม่ join lexical `GAMEMASTER` ใน dirty-word tables กับ wire fields.
5. ไม่ตัดสินค่าที่ server เราควรส่ง และไม่อ้างพฤติกรรมของ original server ที่สูญหาย.
6. ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ source/queue/git.

## BUILD_IMPACT

**BUILD_IMPACT:** เลน `GM-001/GM-003` ต้องคงชื่อพารามิเตอร์ opaque ใน `gm/state_wire.py`; ห้าม rename เป็น `is_gm`/`level` จากใบนี้. แก้ comment/doc ที่เรียก `bm_gm.tga` ว่า GM chat-balloon icon เพราะเป็น false lead; ถ้าจะปิด semantic ต้องใช้ capture/attended tuple matrix แยกต่างหาก ไม่ใช่เดาค่าผ่าน static.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-089 DONE/BOUNDED-NEGATIVE — STATE PROPAGATION PINNED · SEMANTICS/UI UNRESOLVED · BM_GM FALSE LEAD`.
