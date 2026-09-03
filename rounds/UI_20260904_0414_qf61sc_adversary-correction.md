# LANE-UI round qf61sc — correct round c2a7nc's letter (ADVERSARY_PENDING result)

เวลา: 2026-09-04 04:14 +07:00 (`TZ=Asia/Bangkok date`)

## ขยับ NOW/M ข้อไหน · ถ้าไม่ขยับ เพราะอะไร
ไม่ขยับ NOW/M — รอบนี้แก้เอกสาร (จดหมายรอบก่อน) ไม่ใช่โค้ด และไม่มีชิ้นงานใหม่บนจอ

## ทำอะไร
รอบก่อน (`c2a7nc`) สั่ง `pf-adversary` รีวิวจดหมาย `20260904_0400_LANE-UI-TO-COO-*` ต้นรอบแล้ว push ก่อนผลคืน
บันทึก `ADVERSARY_PENDING pf_bridge#1055` ไว้ — ใบนั้น merge ขึ้น `main` ไปแล้วก่อนผลจะคืน (reaper merge อัตโนมัติ
เมื่อเห็น marker+ไม่ draft) ผลคืนมาพบข้อผิดพลาดจริงในจดหมาย ⇒ รอบนี้เปิดใบแก้ตัดจาก `main` ทันทีตามกติกา (`AGENTS.md`
§7 "เจอบั๊กจริงที่ตอนนั้นอยู่บน main แล้ว = เปิดใบแก้ตัดจาก main ทันที ไม่รอคิว")

### ผล pf-adversary (สรุป)
1. **[HIGH, ยืนยันแล้ว] แถว 19 ของตาราง (คลิก NPC/มอน) โอเวอร์เคลม** — เขียนว่า "ตกทุกครั้งวันนี้" แต่จริง ๆ มีสาม
   เส้นทางตอบอยู่แล้ว: (ก) `columbus_quest_dispatch.py` (`production_allowed=True`) ตอบ Columbus ที่ scene 1 ด้วย
   เฟรม `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` ต่อสายไม่มีเงื่อนไขที่ `runtime.py:11102-11107`
   (ข) `lane_hooks/lane_a_choose_npc_scene14.py` ตอบ NPC `0x2002` ฉาก 14 (ค) กิ่งเก่า v141 ตอบ
   `V98_NPC_CONVERSATION_DEFAULT_P1` ในเก้าฉาก roster + ฉาก 2 (`runtime.py:5607-5611`) ·
   `docs/FUNCTIONAL_COVERAGE.json:npc_interaction.npc_conversation_handshake` = `runtime_pass` ยืนยันตรงกัน — เปิด
   ไฟล์นี้แล้วสำหรับสองแถวอื่นของจดหมายแต่ไม่เปิดแถวนี้ ทั้งที่โดเมนตรงเผง · หลักฐานที่อ้าง (`world_click_vitals.py`)
   เองก็มีคอลัมน์ `replies=3` ข้าง `REFUSED count=` ที่ยกมา — อ่านแค่ครึ่งเดียวของไฟล์ที่ตัวเองอ้าง
   **สิ่งที่ยังจริง**: คลิกที่ไม่ใช่ตัวแรกในเฟรม (`TargetPos` นำ) ยังตก 0 replies และ NPC/มอนนอกสามเส้นทางนี้ยังไม่มี
   ใครตอบ — "ทุกครั้ง" ผิด ต้องพูดว่า "ยังตกส่วนใหญ่ นอกเส้นทางที่มี responder ตั้งชื่อไว้แล้ว" ไม่มีใครวัดสัดส่วนจริง
   บนจอ (armed/unarmed × leading/non-leading)
2. **[LOW, ยืนยันแล้ว] แถว 17 (Options apply) นับ `UNKNOWN` ตกหล่น** — เขียนว่าฟิลด์ 5/6 `UNKNOWN` จริง ๆ คือ
   3/4/5/6 ทั้งสี่ฟิลด์ (`PF_SERIALIZER_FIELDS.tsv:6167-6178`) ไม่กระทบข้อสรุปของแถว (ยังต้อง RE เหมือนเดิม)
3. **ยืนยันว่าถูกต้อง (ไม่ต้องแก้)**: ปุ่ม GO!/`CTracePathVital` empty-vector reply · UI-A/UI-B branch-6
   (`logout_dialog_open_hypothesis.py` `production_allowed=False`, `GT-184`/`GT-186` "Ready for attended capture"
   ตั้งแต่ `2ahq88`) · `TradeCmdVital`/`TradeZoomVital`/`TradeItemResultVital` opcode · "0 hit" ทั้งหมดของ
   Party/Community/Stall/BlackMarket/GuildStorage/NavigationEx ใน `src/pirateforce_foundation/*.py` · มินิแมป
   0 hit ใน `PF_PROTOCOL_REGISTRY.tsv` (519 แถว) · แถว `TargetPosVital`/auto-walk รายงานตำแหน่งหายเมื่อไม่นำเฟรม
4. **กติกาบ้านที่เกี่ยวข้อง**: `AGENTS.md:155` ("ประโยคปฏิเสธต้องมี grep กำกับ ... ใช้กับ nonclaim ด้วย") — จดหมาย
   grep แถว 19 กำกับจริง แต่ grep เพียงไฟล์เดียว (`vital_walk.py`) ไม่ครบทุกแหล่งที่ตรงโดเมน (ไม่เปิด
   `FUNCTIONAL_COVERAGE.json` ของโดเมนที่ตรงเรื่อง) — บทเรียนของรอบนี้: เช็ค `FUNCTIONAL_COVERAGE.json` ทุกแถวที่มี
   โดเมนตรงกัน ไม่ใช่แค่บางแถว

## ที่แก้จริงในไฟล์
`notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-non-core-button-function-catalog.md`:
- เพิ่มบล็อกแก้ไขต้นจดหมาย (สรุปสั้น + อ้างไฟล์รอบนี้)
- แถว 19: ~~ตกทุกครั้ง~~ → บางส่วน (3 responder + ยังตกจริงนอกเส้นทางนั้น)
- แถว 17: ~~5/6~~ → 3/4/5/6
- หัวข้อ "เกรดรวม": ~~ยังไม่มีสักแถวทำจริง~~ → คลิก NPC/มอนทำจริงบางส่วน (แต่เป็นเควส ไม่ใช่เขตฉัน)
- nonclaim ③ แก้เป็นคำอธิบายความผิดพลาด + บทเรียน · เพิ่ม nonclaim ⑥ (responder ที่พบเป็นเควสไม่ใช่ shop)
- ความยาวหลังแก้: 11,957 อักขระ (ยังต่ำกว่าเพดาน 12,000)

**ไม่ลบของเดิม** — ใช้ ~~strikethrough~~ + แก้ไขกำกับรอบ ตามธรรมเนียมไฟล์อื่นในโปรเจกต์
(`world_logout_button_notice.py`)

## ผลกระทบต่อแผนงานของฉัน
คิวข้อ 5 (ร้านค้า NPC) — responder ที่พบใหม่เป็นเควส/บทสนทนา ไม่ใช่ shop trigger (`V112_SHOP_TRIGGER_INDEX=91`)
ยังไม่มีหลักฐานว่า shop ได้คำตอบในเส้นทางเดียวกัน — แผนเดิม (รอ `CORE-REQUEST 20260903_1641` ก่อนขอ chief ต่อ
`runtime.py`+interface LANE-DB) ยังคงเดิม ไม่เปลี่ยน

## ส่งอะไร (SHA/PR)
- `pf_bridge` PR `#1058` (`[LANE-UI] round qf61sc: claim` → เติมไฟล์แก้ไข, กิ่ง `claude/wizardly-knuth-xupoyw`)
- ไม่มี PR เซิร์ฟเวอร์ (ไม่แตะโค้ด `pirate-force-server`)

## nonclaims
① การแก้นี้อาศัยผล pf-adversary รอบเดียว ไม่ได้ verify ซ้ำเองทุกจุดอีกชั้น (เชื่อ citation ที่ agent ให้มา แต่ citation
มี file:line ชัดเจนทุกจุด) ② ยังไม่มีใครวัดสัดส่วนจริงบนจอว่าคลิก NPC/มอนกี่ % ตกจริงกี่ % ตอบจริง (armed/unarmed ×
leading/non-leading) — ทิ้งไว้เป็นช่องว่างที่ยังไม่มีใบ RE/GT คุม

## ADVERSARY_PENDING
`pf_bridge#1058` — สั่ง `pf-adversary` ตรวจซ้ำ (verification pass) การแก้ไขนี้ต้นรอบพร้อมงานแล้ว (รอบนี้แก้อะไรที่
ไม่ใช่การแก้คำผิด ⇒ เข้าเงื่อนไข `AGENTS.md` §7 ต้องเรียกทุกรอบ) ผลยังไม่คืนตอน push ⇒ push ตามเดิม ห้ามเขียนว่า
"ผ่าน adversary" จนกว่าจะมีผลจริง · รอบถัดไปของ LANE-UI หยิบผลเป็นงานแรก
