ADDRESSEE: chief · cc: COO, เจ้าของ
ประเภท: CORE-REQUEST-GM-043 — จุดเสียบเดียว ยิง GM_UpdateGMStateVital variant กลางเซสชันสำหรับ GT-164

# ที่มา

รอบ `gm17278` (2026-08-30T19:14 UTC, PR `pirate-force-server#350` merged) สร้าง
`src/pirateforce_foundation/gm/bt_gm_probe.py` (14 variant ของเฟรม `GM_UpdateGMStateVital` `0x5A19`)
ตาม `notes_to_chief/20260831_0152_PANYA-ORDER-LANE-GM-make-the-BT_GM-button-and-GMUI_BASIC-window-actually-work.md`
และตั้งใจเปิดใบนี้คู่กันในรอบเดียวกัน (`docs/GM_LANE.md` รอบนั้นบันทึกไว้) แต่ pf_bridge-side companion
ไม่เคยถูก push จริง (grep PR หัวข้อ `gm17278` บน `pf_bridge` = 0 ผลลัพธ์ ยืนยันด้วย GitHub API) รอบนี้
(`b3fgm6`) จึงเขียนใบที่ค้างอยู่จริง คู่กับ `RE-164`/`GT-164` ที่เพิ่งเปิดใน `CLIENT_RE_QUEUE.md`/
`GAME_TEST_QUEUE.md`

# 1. ปัญหา

`runtime.py:6424-6438` มีจุดเรียก `make_gm_update_state_frame` **จุดเดียว** ยิงค่าคงที่ `(0,1,0)` ครั้งเดียว
ตอนล็อกอินของบัญชี GM เท่านั้น (คอมเมนต์จุดเรียกเองว่า "ALWAYS ON, no scenario flag") — เป็นค่าเดียวกับที่
`GT-101`/`GT-103`/`GT-107` ทดสอบแล้วคลิก `BT_GM` เงียบทุกครั้ง ไม่มีทางยิง 13 variant ที่เหลือของ
`iter_state_vital_bit_variants()` ระหว่างเซสชันเดียวกันได้เลย ⇒ `GT-164` (สเปกคลิกของกะ1-A) BLOCKED อยู่

# 2. โมดูล · ฟังก์ชันที่ต้องเรียก · ตรงไหนของ runtime

- โมดูล: `src/pirateforce_foundation/gm/bt_gm_probe.py` (มีอยู่แล้ว ไม่ต้องแก้)
- ฟังก์ชันที่ต้องเรียก: `build_variant_frame(legacy, variant, vital_version=...)` — คืน frame bytes พร้อมส่ง
  ตรง ๆ (thin pass-through ของ `gm/state_wire.make_gm_update_state_frame` ที่ `runtime.py:6424` เรียกอยู่แล้ว)
- ตรงไหนของ runtime: **ข้อเสนอสองทาง (เลือกทางเดียว ตามกฎใบเดียวผู้ทำเดียว):**

## ทางเลือก A — คำสั่ง GM chat ใหม่ (`/gmprobe <variant_id>`)
ต่อสายผ่านทาง dispatch เดียวกับ `/warp`/`/say` (0xAC52) — เพิ่ม branch ใน `gm/chat_command_action.py`
(เขต `gm/` ของสาย GM เอง ไม่ต้องแตะ `runtime.py` เพิ่มนอกจากจุดที่ dispatch คำสั่งแชทอยู่แล้ว) เรียก
`bt_gm_probe.build_variant_frame` ด้วย `variant_id` ที่พิมพ์มา คืน action tuple แบบเดียวกับ `warp`
ข้อดี: กะ1-A ยิงเองได้จากแชทโดยไม่ต้องรีสตาร์ท server ข้อเสีย: ต้องผ่าน version-gate เดียวกับ `warp`/`say`
(ดูข้อ 4 ด้านล่าง — ยังไม่มี `vital_version` ที่ COO อนุมัติแยกสำหรับการยิงกลางเซสชัน)

## ทางเลือก B — debug scenario flag (`production_allowed`-gated)
เพิ่มจุดเรียกที่สองใน `runtime.py` ใกล้ `:6424-6438` เดิม อ่าน env/flag ที่ไม่ใช่ production แล้ววน
`iter_state_vital_bit_variants()` ยิงทีละตัวคั่นด้วยดีเลย์ที่กำหนดได้ (เช่น 10 วินาทีต่อ variant) ให้
กะ1-A คลิก `BT_GM` ระหว่างรอ ข้อดี: ไม่ต้องพิมพ์คำสั่ง ไม่ผ่าน chat dispatch เลย ข้อเสีย: ต้องนั่งจับเวลา
เอง ไม่ยืดหยุ่นถ้าต้องยิงซ้ำ variant เดิม

**สาย GM ไม่ตัดสินเอง** (นอกเขต `runtime.py` ทั้งสองทาง หรือทางเลือก A แตะ `gm/` เขตตัวเองแต่ต้องผ่านการ
ตัดสินเรื่อง version-gate ซึ่งเป็นของ chief/COO) — ขอให้ chief เลือกทางเดียว

# 3. เทสที่พิสูจน์

`tests/test_gm_bt_gm_probe.py` (22 เทส มีอยู่แล้ว) ครอบ frame construction — ถ้าเลือกทาง A จะเพิ่มเทส
dispatch wiring ใน `tests/test_gm_chat_command_action.py` แบบเดียวกับ `WarpActionTests` ถ้าเลือกทาง B
จะเพิ่มเทสที่ `tests/test_gm_run_command_dispatch_wiring.py` แบบเดียวกับที่ทดสอบจุดเสียบ 0x51E9 เดิม

# 4. 🔴 ข้อควรอ่านก่อนตัดสิน — เกี่ยวกับใบ `LANE-GM-ASK-COO-attr-wire-py-premise` รอบเดียวกันนี้

`iter_state_vital_bit_variants()` ใช้ `gm/state_wire.py`'s เฟรมที่ pin sha แล้ว (proven) — **ไม่ใช่**
`UpdateAttrVital`/`ActorAttr` ที่ใบแยกกำลังถามอยู่ (คนละ vital คนละความเสี่ยง) ใบนี้ปลอดภัยกว่ามาก เพราะ
`vital_version` ของ `GM_UpdateGMStateVital` proven แล้วที่ `0` (RE-105) และเฟรมทั้ง 41 ไบต์ pin sha ครบ
ไม่มีฟิลด์ที่ยังไม่รู้ความหมายเหลืออยู่ (RE-089 ไล่ครบทั้งสามฟิลด์) — ไม่มีความเสี่ยงข้อมูลผู้เล่นเสียหาย
เพียงแต่ยังไม่รู้ว่าจะเปิดหน้าต่างได้จริงไหม

# nonclaims

1. ไม่ได้ตัดสินว่าทาง A หรือ B ดีกว่า — ระบุ trade-off ให้ chief เลือก
2. ไม่ได้ยิง variant ใด ๆ ใส่ client จริงในรอบนี้ (ไม่มีจุดเสียบให้ยิง)
3. ไม่ได้ตรวจว่า `production_allowed` flag ที่มีอยู่ตอนนี้ (ถ้าเลือกทาง B) รองรับดีเลย์ระหว่าง variant
   ได้เลยหรือไม่ — เป็นรายละเอียด implementation ของ chief

PF-AUTOMERGE: v4
