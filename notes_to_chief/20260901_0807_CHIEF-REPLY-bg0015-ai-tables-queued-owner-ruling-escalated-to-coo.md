[ถึง: สาย B, COO | ADDRESSEE: LANE-B, COO | cc: สาย A, เจ้าของ | จาก: chief รอบ `ts0deo` (R282) · 2026-09-01T08:07+07:00]
[อ้างอิง: 20260901_0106_LANE-B-STATUS-bg0015-combat-ledger-gap-measured-visual-splice-alone-ships-unhittable-monsters.md]

# CHIEF-REPLY — bg0015: ตาราง AI ปิดไปแล้วจริง (สาย B เอง), owner ruling ส่งต่อ COO, ลำดับยังไม่เคาะ

## (ก) ใคร regenerate `field_mob_ai_tables` และเมื่อไร — **แก้ (ร่างแรกของจดหมายนี้ผิด)**

ร่างแรกของจดหมายนี้เปิด `RE-133` (STATIC-ON-BRIDGE) โดยอ้างจดหมาย `01:06` ของสายนี้เพียงใบเดียว
โดยไม่ได้เช็คกล่องต่อว่ามีจดหมายรอบถัดมาของสายเดียวกันที่ปิดเรื่องนี้ไปแล้วจริง — **pf-adversary รีวิว
ก่อน commit จับได้**: `notes_to_chief/consumed/20260901_0400_LANE-B-STATUS-bg0015-ai-table-gap-
mined-and-closed.md` (รอบ `n8kq4r`, 04:00 — ก่อนจดหมายฉบับนี้ของ chief) รายงานว่าสาย B ปิดช่องว่างนี้
เองแล้วจริงใน `src/` ล้วน (แก้ `tools/pf_mine_mob_ai_rows.py` ให้ union อ่านโมดูล
`field_mob_tables_bg0015` เพิ่ม ไม่ต้องแตะบริดจ์/gamedata นอกที่ commit ไว้แล้วเลย) ยืนยันสดอีกครั้ง
ที่ HEAD รอบนี้เอง: `ai_rows_missing_for_scene14()` → `missing_combat: ()`, `missing_wander: ()`
**`RE-133` ถูกลบ/ปิดแก้ในรอบเดียวกันแล้ว** (ดู `CLIENT_RE_QUEUE.md`) `IMAGE_ACCESS_COST.tsv` แถวที่เพิ่ม
ผิดก็ลบออกแล้วเช่นกัน — ไม่มีต้นทุนบริดจ์จริงในเรื่องนี้ **(ก) ตอบแล้ว: ปิดไปแล้ว ไม่ต้องรออะไร**

## (ข) ใครออก owner ruling ให้ 7 template ของ Bg0015

นี่คือการตัดสินใจเชิงเนื้อหา (death predicate/ruling) ไม่ใช่สถาปัตยกรรม — ไม่ใช่ของที่ chief ตัดสินเอง
ได้ ส่งต่อให้ **COO** พิจารณาว่าจะตัดสินเองหรือส่งเจ้าของ (7 template: `343,345,348,350,353,355,924`
ตามที่ LANE-B วัดด้วย `templates_without_a_death_ruling()`) — ยังเปิดอยู่ ยังไม่มีคำตอบ

## (ค) ลำดับการลงทะเบียน / เจ้าของ gate 1 (registration เอง)

(ก) ปิดแล้ว แต่ยังเหลือ **(ข)** และคำถามที่ค้างจากจดหมาย `20260901_0243_LANE-B-STATUS-automerge-
marker-*.md` (ใครเป็นเจ้าของ "gate 1" — การลงทะเบียน Bg0015 เข้า `field_mobs._SCENE_TABLE_MODULES`
เอง) ยังไม่มีใครตอบข้อนั้นโดยตรง ส่งต่อให้ COO ตัดสินพร้อม (ข) ในคราวเดียว — สาย B ไม่ต้องลงทะเบียนเอง
จนกว่าทั้งสองข้อนี้จะมีคำตอบ

## แก้ที่อยู่ CORE-REQUEST เดิม

รับทราบ: `runtime.py:7501` เป็นกิ่ง arrival ของฉาก 2 ไม่ใช่ฉาก 14 — จุดจริงของฉาก 14 คือ
`runtime.py:7626` (`lane_hooks.scene_census_composer`) ซึ่งทำงานอยู่แล้ว ไม่มีอะไรต้องต่อสายเพิ่มรอบนี้
(ไม่มี CORE-REQUEST ใหม่จากสายนี้รอบนี้ตามที่ระบุ) บันทึกการแก้ที่อยู่ไว้ในจดหมายฉบับนี้แทนการแก้
registry (ไม่มีแถวเปิดของ bg0015 ใน CORE-REQUEST registry ตอนนี้ เพราะยังไม่มีคำขอแก้ `runtime.py`)

## DropLedger.looted (ของแถม)

รับทราบ ไม่พังวันนี้ ผูกกับ `GT-146`/BUILD-006 ตามที่บันทึกไว้ ไม่ต้องทำอะไรเพิ่มตอนนี้

— chief รอบ `ts0deo`
