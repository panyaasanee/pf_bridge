[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-104 RESULT — PASS/DONE: `BT_GM` เปิด dedicated GM editor หลัง gate `GMModule_Client+0x19`

- เวลา: `2026-08-27T15:18+07:00`
- ใบ: `RE-104 GM-EDITOR-WIDGET-OPEN-TRIGGER-001 [STATIC-ON-BRIDGE]`
- verdict: **PASS/DONE** — trigger ที่พิสูจน์ได้คือปุ่ม UI ชื่อ resource `BT_GM`; control นี้ถูกแสดง/เปิดใช้เมื่อ query type `0x25` คืนค่า `GMModule_Client+0x19` เป็นจริง และ click path ตรวจ gate เดิมซ้ำก่อนส่ง current UI key เข้า central UI open/create dispatcher ซึ่ง crosswalk ไปยัง factory ของ `GMModule_Client` ที่สร้าง dedicated GM UI (`GMUI_BASIC`) ที่มี `Radiobutton_Message` และ `TextBox_Message`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ client/server/external/gamedata/queue/git
- ImageBase ของ VA ทุกจุดด้านล่าง: `0x00400000`

## ค้นสองที่ก่อนถอด (บังคับ)

- **ค้นใน `pf_bridge/external/` แล้ว:** ค้นทั้ง tree 30 ไฟล์ (fingerprint `180424fe457e680e47b38b5b8e9a8094d2dc33c0c9c1f904b9f5a9a040dd11c5`) ด้วย `GM_RunGMCommandVital|GM_UpdateGMStateVital|GMModule_Client|BT_GM|PANEL_SYSTEM_GM|TextBox_Message|GMUI_BASIC|00729410|0053B9B0|0044A3B0`; พบ registry/serializer/validation ของ `GMModule_Client`, `GM_UpdateGMStateVital`, `GM_RunGMCommandVital` และ state validation ยัง `NOT_OBSERVED`; **ไม่พบ** `BT_GM`, widget resource หรือ UI-open trigger/crosswalk ใน external
- **ค้น gamedata แล้ว:** ค้นทั้ง `pf_bridge/gamedata/` 1,109 ไฟล์ (fingerprint `6c7d05ca272d2fbb53098861606478af2c6ad41bdb637378c4554526357aee59`) ด้วย pattern ชุดเดียวกัน; **ไม่พบ hit** จึงไม่มี layout coordinate หรือ gamedata crosswalk ให้ join

## T0 — image/table gate

- `GameClient.local.bin` sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `PF_PROTOCOL_REGISTRY.tsv` sha256 `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv` sha256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_FIELD_VALIDATION.tsv` sha256 `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- ตรงกับ pins ของ verifiers `RE-089`/`RE-091`; ทั้งสอง verifier PASS ซ้ำ และใช้ผลเดิมหลัง verify SHA แทนการถอด state/sender ซ้ำ

## T1 — trigger, gate และ factory crosswalk

### 1. provenance ของปุ่มและ control slot

- UTF-16 resource `BT_GM` อยู่ที่ `0x00F2207C`; literal xref มีหนึ่งจุดที่ `0x0053B08B` ภายใน binder `[0x0053ADE0,0x0053B144)` sha256 `af339f5e84ca0656e7b2a26086901136be8eb8da22e9a392e72aa009d811ba34`
- binder เรียก resource lookup `0x00AA1750`; ผล type-checked ถูกเก็บที่ object `+0x48` (`0x0053B0CB`)
- periodic UI state `[0x0053B150,0x0053B324)` sha256 `2f4c81d867e1f3c6b3286872d7866af8485bfd0b184a12d5d72afeaec8f15a35`: ถ้า control `+0x48` และ client context มีอยู่ จะเรียก `0x0044A3B0` ที่ `0x0053B1B4` แล้วส่ง boolean ไปยัง virtual method `+0xF4` ของ `BT_GM` ที่ `0x0053B1C7..0x0053B1D7`

### 2. gate มี field crosswalk ไม่ใช่การจับคู่ชื่อ/id

- query `[0x0044A3B0,0x0044A45D)` sha256 `755bd9a1ebbb74267afd4143c3df2032065b152e0082bffcfc4fe3993fce386e` สร้าง request type `0x25`, dispatch ผ่าน connection module registry แล้วคืน byte request `+0x14`
- `GMModule_Client` vtable `0x00F46208` slot `+0x44` ชี้ exact ไป `0x00726D30`; adapter `[0x00726D30,0x00726D62)` sha256 `bba473c432f5bedf3f6f2d281c4450e304601faa44e7999b29b1b31898159e48` ตรวจ type `0x25` แล้วทำ `module+0x19 -> request+0x14` (`0x00726D3B..0x00726D3E`)
- verifier `RE-089` ยืนยันเพิ่มว่า update path `GM_UpdateGMStateVital` ทำ `wire+0x15 == 1 -> GMModule_Client+0x19`; semantic label ของ field ยัง unresolved จึงเรียกเพียง `module+0x19 gate` ไม่ตั้งชื่อว่า `is_gm`

### 3. click เปิด GM UI จริง

- event dispatcher `[0x0053BCA0,0x0053BD14)` sha256 `396666e352bb1e37233b9de85d91b14cac3ae96a69435e88137100e6d27807ed` เทียบ event source กับ control `+0x48` ที่ `0x0053BCEF`; เมื่อเป็น click event (`[0x01090DC0]`) จะเรียก handler `0x0053B9B0`
- handler `[0x0053B9B0,0x0053BC9E)` sha256 `e4bf6936508a22c630b3fd77c8288f0757a82b9104c5c66f1f48eb2346bb6a75` branch `0x0053BC51..0x0053BC96` เทียบ source กับ `+0x48`, เรียก `0x0044A3B0` ตรวจ `module+0x19` ซ้ำ, ขอ current UI key ผ่าน `[0x01093198]+0x7C8` vfunc `+0x04`, แล้วส่ง key/flags เข้า central dispatcher `0x00AA0710`
- `[0x00AA0710,0x00AA0799)` sha256 `62fd9c6fdb6a85443ec6f2657495caf2c26f1ea580b432195c26f89b171a2d99` ใช้ key หา existing UI (`0x00A9EF00`) หรือ create (`0x00A9E080`) แล้ว apply visibility/flags
- crosswalk ถึง dedicated GM UI มาจาก field/table จริง: `GMModule_Client` vtable `0x00F46208` slot `+0x48` ชี้ `0x007280D0`; factory `[0x007280D0,0x007281B8)` sha256 `e6209b9021e4e3c689c3b8b75c18b8b1c60840e8761229ab6d4b4e37eb98de34` อ่าน current UI key ด้วย global/vfunc ชุดเดียวกัน, เทียบกับ dispatcher argument, allocate `0xEC`, เรียก base constructor และตั้ง widget vtable `0x00F46258`

## T2 — resource ของ widget ที่ผู้เทสต้องหา

- widget binder `[0x00726DF0,0x00727A40)` sha256 `90089e86b7f54a523050c68c40b11971aad77a1402576e683cd8e86061a1142b` ผูก:
  - `GMUI_BASIC` (`0x00F461EC`) เป็น panel object `+0x14`
  - `Radiobutton_Message` (`0x00F46104`) เป็น control `+0x2C`
  - `TextBox_Message` (`0x00F45FF0`) เป็น editor `+0x50`
  - ยังมี tabs `GMUI_ADVAN`, `GMUI_ACTIVITY` และ `BUTTON_OK`
- widget event dispatcher `[0x00729580,0x007295D3)` sha256 `b6a0d43053c100e116213d1945b4a8976d0cad8fd1e9ff97525244ff394fbc90` ส่ง textbox event ไป producer `0x00729410`; producer `[0x00729410,0x0072957D)` ตรวจ active panel, selected `Radiobutton_Message`, Enter `0x0D`, ข้อความไม่ว่าง แล้วส่งตามผล `RE-091`
- static corpus ไม่ให้ coordinate บนจอ; procedure ที่พิสูจน์ได้คือ **หา/กด control resource `BT_GM` ใน notification/system UI แล้วใช้ `GMUI_BASIC > Radiobutton_Message > TextBox_Message`**

## T3

ไม่ใช้ bounded-negative exit เพราะ T1/T2 พบ positive trigger และ field/resource crosswalk ครบ; ใบนี้ **ไม่ claim ว่าไม่มี hotkey อื่น** เพียงแต่ไม่จำเป็นต้องเดา hotkey เพื่อปิด objective

## Reproducer / verifier

`pf_bridge/staged/re104_gm_editor_trigger_static.py`

- script sha256 `aee5a2d56c343b68f04285e76d43c2bbbdd3968c5e61ec89cc01480fb59ad95e`
- รัน `py -3 -B` สองครั้ง: **PASS เหมือนกัน**
- pin image/3 external tables, 12 exact spans, 7 UTF-16 UI resources, vtable slots, gate dataflow, click dispatcher, factory และ Enter producer
- เป็น positive exact-byte/data-flow proof; ไม่ใช้ linear disassembler เป็นหลักฐานผลลบ

## Integrity / provenance

| input | sha256 ก่อน | sha256 หลัง |
|---|---|---|
| `GameClient/GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| `external/PF_PROTOCOL_REGISTRY.tsv` | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` | `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d` |
| `external/PF_SERIALIZER_FIELDS.tsv` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` | `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` |
| `external/PF_FIELD_VALIDATION.tsv` | `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` | `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` |
| `staged/re089_gm_state_visual_static.py` | `7e0bb0f636d17dfc03fa86201f2c625fdf2ffe2e5a9dad02d681d3a257378c8d` | `7e0bb0f636d17dfc03fa86201f2c625fdf2ffe2e5a9dad02d681d3a257378c8d` |
| `staged/re091_cheat_chat_trigger_static.py` | `c2067b311d9d721896809767c9ee030eb5b0408bce02c2422c91a074322d6407` | `c2067b311d9d721896809767c9ee030eb5b0408bce02c2422c91a074322d6407` |

`CLIENT_RE_QUEUE.md`/`NEW_ORDERS.txt` mtime และ SHA ไม่เปลี่ยนระหว่างวิเคราะห์ (`5bd6b2b2dfa90465944dbc303d77c59af3e8998d20c642de5062932eef1be4f5` / `f28673d1b76b31e6045017bd4179d793ec4db400adca63e3661994185466393f`).

## nonclaims

1. ไม่ตัดสินว่า account ที่ไม่ใช่ GM มองเห็นหรือเปิด widget ได้หรือไม่; ข้อสรุปคือ client gate ด้วย `module+0x19` เท่านั้น และ semantic/authorization policy ยังไม่ถูกตั้งชื่อ
2. ไม่ claim screen coordinate, icon texture, hotkey สำรอง หรือ runtime observation; gamedata ไม่มี crosswalk และรอบนี้ static เท่านั้น
3. ไม่ claim ว่า `module+0x18`, `+0x19`, `+0x1C` คือ field ใดจาก id/ตำแหน่งอย่างเดียว; ใช้เฉพาะ crosswalk exact ของ type `0x25`
4. ไม่ claim ว่า `GT-103` ถูกบล็อก; ผลนี้เป็น procedure input ให้ attended tester เลิกสุ่มหา trigger ได้

## BUILD_IMPACT

**BUILD_IMPACT:** หากจะเลียนพฤติกรรม original client ให้ notification/system UI bind ปุ่ม `BT_GM`, แสดง/enable จาก connection query type `0x25` ซึ่งคืน `GMModule_Client+0x19`, และ recheck gate เมื่อ click ก่อนขอสร้าง dedicated `GMUI_BASIC`; ภายใน UI ให้ `Radiobutton_Message` เลือก lane และ `TextBox_Message` ส่งเมื่อ Enter ตาม producer `0x00729410`. อย่าผูกการเปิดหน้าต่างกับ id เท่ากันหรือเดา hotkey และอย่าตั้งชื่อ `+0x19` ว่า `is_gm` จนมี semantic/authorization evidence เพิ่ม.
