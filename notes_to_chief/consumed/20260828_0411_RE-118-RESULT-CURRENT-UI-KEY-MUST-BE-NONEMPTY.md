[ถึง: chief cloud · LANE-GM · COO | จาก: RE runner local · 2026-08-28T04:11+07:00]

# RE-118 RESULT — PASS/DONE · `BT_GM` ต้องมี current UI key ที่ไม่ว่าง; `+0x18/+0x1C` ไม่ได้ gate คลิก

- ใบ: `RE-118 BT-GM-CLICK-DISPATCH-GATE-001 [STATIC-ON-BRIDGE]`
- START: `2026-08-28T04:02:05.447+07:00`; เริ่มใบหลังอ่าน objective ล่าสุดและยืนยันว่าไม่มี result letter เดิม
- วิธี: static/read-only เท่านั้น · ไม่เปิดเกม/server · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB/source/queue/git
- verdict: click chain ที่ bounded ครบอ่านค่าจาก `GM_UpdateGMStateVital` เพียง gate เดิม `GMModule_Client+0x19`; ค่า `module+0x18/+0x1C` ไม่ได้เป็น gate ของการคลิกและไม่ควร tweak. หลัง gate เดิมผ่าน handler บังคับให้ `[runtime+0x7C8]` มี current-UI object และ vfunc `+0x04` ต้องคืน UTF-16 key ที่ไม่ใช่ null/empty; central dispatcher กับ GM factory ต่างออกเงียบเมื่อ key ว่าง. ไม่มี fixed parent-panel literal ในสายนี้ — key เป็น dynamic current UI context.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** ใน tree 30 ไฟล์ / 29,900,221 ไบต์ fingerprint `399098b4eb5a61ef07fffb5867ce3a8bb5eab0a68f6fb3a39fc452515fc9c61c`: registry/serializer/validation ของ `GMModule_Client`, `GM_UpdateGMStateVital`, `ActorAttr/NPCAttr`; `GMModule_Client` registry rowพิน vtable `0x00F46208`, query adapter `0x00726D30`, factory `0x007280D0`. **ไม่เจอ** `BT_GM`, `GMUI_BASIC`, click handler หรือ parent-panel crosswalk ใน external — จึง verify SHA แล้วไล่อิมเมจจริงต่อ.
- **ค้น gamedata แล้ว: ไม่เจอ** `BT_GM|GMUI_BASIC|GMModule` ในดัชนี/คอลัมน์/188 tables/Lua/scene ของ tree 1,109 ไฟล์ / 15,319,585 ไบต์ fingerprint `cf7d8e93bd798bc425ce346bdf8b2bbdc0a52b1632d89bd980580ae384660d8a`. lexical hits กว้างเรื่อง level/MP/FONT_COLOR เป็นคนละ namespaceและไม่ใช้ join; ใบนี้เป็น UI/runtime code concern.

## T0 — SHA control

- image `GameClient.local.bin` SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, ImageBase `0x00400000`
- registry `27daac0c...fb4d`; serializer fields `99282bdf...c123`; validation `080a5f32...41c3`
- verifier เดิม `re104_gm_editor_trigger_static.py` SHA `aee5a2d5...d95e`; span ที่ reuse ทุกตัวตรงอิมเมจเดิม

## T1 — click handler และฟิลด์จาก `0x5A19`

handler `[0x0053B9B0,0x0053BC9E)` SHA `e4bf6936508a22c630b3fd77c8288f0757a82b9104c5c66f1f48eb2346bb6a75` มี branch `BT_GM` ที่ `0x0053BC51..0x0053BC96` ตามลำดับ:

1. `cmp source,[this+0x48]`; ไม่ใช่ control นี้ออกเงียบ
2. `[0x01032EC4]` connection context ต้องไม่เป็น null
3. `0x0044A3B0` query type `0x25` ต้องคืน true
4. `[0x01093198]+0x7C8` current-UI object ต้องไม่เป็น null
5. เรียก current-UI vfunc `+0x04`, push key ที่คืนมาเป็น argument แรกของ `0x00AA0710`

query adapter `[0x00726D30,0x00726D62)` SHA `bba473c4...9e48` ก๊อป `module+0x19 -> request+0x14`, `bool(module+0x18) -> request+0x20/+0x24`, `module+0x1C -> request+0x18`; แต่ wrapper `0x0044A3B0` คืนเฉพาะ byte `request+0x14`. ดังนั้น click chain นี้ **อ่านผล gate จาก `+0x19` เท่านั้น**. ปุ่มโผล่ใน GT-101-R3 พิสูจน์แล้วว่า gate นี้ผ่าน; `+0x18/+0x1C=0` ไม่ใช่สาเหตุที่ branch นี้หยุด.

## T2 — current UI key / parent context

- predicate `[0x008946C0,0x008946EA)` คืน true เมื่อ pointer null หรือ UTF-16 string length = 0 และคืน falseเมื่อ key ไม่ว่าง.
- dispatcher `[0x00AA0710,0x00AA0799)` SHA `62fd9c6f...d99` เรียก predicate นี้ก่อนงานอื่น; ถ้า true คืน `NULL` ด้วย `ret 0x10` แบบไม่มี log/error/frame.
- handler ไม่ push ชื่อ panel คงที่: argument แรกมาจาก vfunc runtime ตรง ๆ. constant อื่น `0x0102ADE0`/`0x01090958` เป็น arguments คนละช่อง ไม่ใช่ key.
- ดังนั้นเงื่อนไขที่พิสูจน์ได้คือ **ต้องมี current UI context และ key ต้อง nonempty**; static ไม่ตั้งชื่อได้ว่าต้องเปิด panel แม่ใบใด เพราะไม่มี literal/crosswalk ผูก key กับชื่อ panel ใน bounded chain.

## T3 — dispatcher ถึง factory

- dispatcher ใช้ dynamic key หา existing UI (`0x00A9EF00`) หรือ create (`0x00A9E080`), แล้วค่อย apply visibility/flags; key ว่างหรือ create คืน null จะจบเงียบ.
- `GMModule_Client` vtable `0x00F46208 + 0x48 -> 0x007280D0` เป็น field crosswalk ตรง ไม่จับคู่ด้วยชื่อ/id เท่ากัน.
- factory `[0x007280D0,0x007281B8)` SHA `e6209b90...8de34` อ่าน current key จาก global/vfunc ชุดเดียวกัน, ปฏิเสธ null/empty ซ้ำ, เปรียบเทียบ dynamic key กับ dispatcher argument แล้วจึง allocate `0xEC` และสร้าง `GMUI_BASIC`; ไม่มีการอ่าน `GMModule_Client+0x18/+0x19/+0x1C` ใน factory.
- vtable post-create `+0x1D8 -> 0x00729FB0` ไม่ใช่ 0x5A19-field gate: มันคืน type id global ที่ initializer `0x00C08130` สร้างจาก literal `ChangeEquipLevelModule_Client`. ห้ามตั้ง semantic เพิ่มจากชื่อ class นี้.

## T4/T5 — ค่าที่ควรส่ง / เพดาน

- **ไม่มีค่าใหม่จากเฟรม `0x5A19` ที่ static บอกให้เปลี่ยน.** คง `field_0x0b_second=1` เพื่อให้ `module+0x19` ผ่านตาม RE-104/GT-101-R3; ห้าม tweak `field_0x0b_first` หรือ u32 เพื่อลองสุ่ม.
- สาเหตุ runtime เฉพาะรอบ GT-101-R3 ว่า current object เป็น null หรือ key เป็น empty ยังพิสูจน์ตรงจาก static ไม่ได้; ต้องทำ attended A/B โดยเปิด panel ที่ให้ current key ไม่ว่างก่อนคลิก แล้วเทียบกับคลิกจาก HUD เปล่า. ผล static ปิดคำถามกลไก/gate แต่ไม่อ้างค่ารันไทม์ที่ไม่ได้ capture.

## verifier / reproducibility

- `pf_bridge\staged\re118_bt_gm_click_gate_static.py` SHA-256 `ad3aaa09f972720be029001551279f6e837f35038c003d56db3a2d215a388cb9`
- รัน `python -B` อิสระ 2 ครั้ง: PASS `27` checks / `8` pinned spans ทั้งคู่, exit `0/0`
- probe `pf_bridge\staged\re118_disasm_probe.py` SHA ณ ตอนปิดใบ `e3d810d4fb28e45d39f5f091c027fb4e929a5af0f41160d2cdfb99562718ff1f`
- source SHA ก่อน/หลังงานตรงกัน: image/queue/AGENTS/NEW_ORDERS/registry/serializer/validation ไม่ขยับ

## nonclaims

1. ไม่อ้างว่า GT-101-R3 มี key ว่างจริง; ไม่มี runtime trace ของ vfunc return ในใบ static นี้ — ระบุเพียง gate ที่อธิบายอาการได้ตรงและวิธี A/B ที่แยกได้.
2. ไม่อ้างชื่อ parent panel หรือ sentinel key; factoryเทียบ dynamic string และไม่มี fixed parent literalในสายที่ pin.
3. ไม่ตั้งชื่อ `module+0x18/+0x1C`; พิสูจน์เพียงว่า click branch ไม่ใช้สองฟิลด์นี้เป็น gate.
4. ไม่อ้างว่า factory ไม่มี failure path อื่นนอก bounded dispatcher/create chain; รายงานทุก null/empty/create-null early exit ใน span ที่ตรวจ.
5. ไม่มีหลักฐาน client-observable ใหม่ในใบนี้; ผลหน้าจอที่อ้างมาจาก GT-101-R3 และแยกชั้นจาก static image evidence.

## BUILD_IMPACT

**BUILD_IMPACT:** ปรับ procedure ของ `GT-103`/`GT-107-R3` ให้ทำ A/B: (A) คลิก `BT_GM` จาก HUD ที่ไม่มี panel current, (B) เปิด panel ที่รู้ว่ามี nonempty current UI key แล้วคลิกซ้ำ; อย่าแก้ `0x5A19 +0x14/+0x18` แบบสุ่ม. ถ้า B เปิด `GMUI_BASIC` ได้ ให้ wiring ฝั่ง serverคงเดิมและแก้เพียงขั้น UI; ถ้า B ยังเงียบ ให้ instrument current-key return/create-null เป็นงานถัดไป.

BUILD_IMPACT_NONE: 0/1

สถานะที่ chief ควรกรอก: `RE-118 PASS/DONE — CURRENT-UI-KEY-MUST-BE-NONEMPTY; NO-NEW-0x5A19-FIELD-GATE`.
