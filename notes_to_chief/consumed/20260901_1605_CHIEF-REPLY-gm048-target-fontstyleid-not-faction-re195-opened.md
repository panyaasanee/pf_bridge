[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: COO | จาก: chief (LANE-E) รอบ `2zr22w` · 2026-09-01T16:05+07:00]
[อ้าง: `20260901_1519_LANE-GM-CORE-REQUEST-GM-048-p2-rgb-closed-faction-pink-crossref.md`]

# ตอบ CORE-REQUEST-GM-048 — ผูก P-2 กับ FontStyleID ไม่ใช่ faction/relation, เปิด `RE-195` ให้แล้ว

## ตัดสินใจ (ข้อ 1 ที่ถามมา)

**เป้าหมายของ P-2 คือ FontStyleID selector (`0x00443F50` chain) ไม่ใช่ faction/relation comparator
(`0x4A1D50`)** เหตุผล: FontStyleID มีสามค่าที่ `RE-191` ปิดแล้วตรงกับสามสถานะที่เจ้าของสั่งเป๊ะ
(61=แดง/สู้, 62=ส้ม/ปกติ, 63=เทา, ไม่มีชมพู) ส่วน faction/relation ที่วัดไว้ (`SCENE-005`) เป็นความ
สัมพันธ์ไบนารี friend/foe ระหว่างสองตัวละคร ไม่ใช่สามสถานะ และคู่ที่วัดแล้ว (faction 1 vs 6) เรนเดอร์
"ชมพู/แดง" จริง — ตรงกับคำห้ามของเจ้าของ ผูก P-2 กับกลไกนี้เสี่ยงเกินไป

**แต่ยังเขียนโค้ดสีไม่ได้วันนี้ ไม่ว่าจะเลือกกลไกไหน** — เหมือนที่สายนี้สรุปเองในใบ `1519` — เพราะ
ตรวจแล้ว (`grep -rn FontStyle` ทั้งสองรีโป = 0 ผล) **ไม่มีวิถีที่เซิร์ฟเวอร์ส่ง FontStyleID อยู่แล้ว
วันนี้จริง** [MEASURED] ตรงกับที่ใบ `1519` วัดไว้แล้ว ไม่ใช่ข้อมูลใหม่

## พบ lead ใหม่ระหว่างตรวจ (ไม่ใช่ข้อสรุป — เปิด `RE-195` ให้แล้ว)

เปิด `notes_to_chief/reference_codex_attr/PF_ATTR_NAME_COLOR_SELECTOR.tsv` (ตารางเดิมของ Codex ที่มี
อยู่แล้ว) พบว่าแถว `output_fontstyle_id=60` มีคอลัมน์ `input_offset_or_key` เขียนว่า
`relationship_predicate_including_BasicAttr+0x68_fallback` — offset `+0x68` **ตรงกับ** offset ของ
faction bit ที่ `npc_hostile_hypothesis.py` พิสูจน์แล้ว (`0x0400`, runtime-proven)

🔴 **นี่เป็นแค่ lead** ไม่ใช่การยืนยันว่า FontStyleID selector's `relationship_predicate`
(`0x0043C380..0x0043C63C`) กับ relation comparator (`0x4A1D50`) เป็นฟังก์ชันเดียวกัน หรือว่า branch ที่
resolve เป็น "สู้" (style 61) พึ่งฟิลด์เดียวกันนี้จริง — แถวเดียวไม่พอสรุปตาม G6 เปิด `CLIENT_RE_QUEUE.md`
ใบ `RE-195` (`[STATIC-ON-BRIDGE]`, สายนี้บริโภคผล) ให้ตอบคำถามนี้ให้ขาดก่อนใครเขียนโค้ด

## สิ่งที่ยังไม่ตัดสิน (ข้อ 3 ที่ถามมา)

ยังไม่ต้องการ block-list ของ faction pairing ที่เรนเดอร์ชมพู วันนี้ — เพราะเลือกไม่ผูก P-2 กับกลไกนั้น
และ `npc_hostile_hypothesis.production_allowed` ยัง `False` (ตรวจแล้วรอบนี้) ความเสี่ยงจึงยังไม่ live
แต่ **ฝากไว้กับสายไหนก็ตามที่จะพลิกแฟล็กนั้นในอนาคต**: อย่าลืมตรวจ faction pairing ที่ทำให้เรนเดอร์
"ชมพู/แดง" ก่อนพลิก แม้จะไม่ใช่เส้นทางสี P-2 ก็ตาม

## nonclaims

1. ไม่อ้างว่า `0x0043C380` กับ `0x4A1D50` เป็นฟังก์ชันเดียวกัน — แค่ตั้งข้อสังเกตจาก offset ที่ตรงกัน
   `RE-195` เปิดไว้ให้ตอบขาด
2. ไม่อ้างว่า FontStyleID มีจุดเสียบพร้อมให้เขียนโค้ดได้แล้ว — ยังไม่มี ต้องรอ `RE-195`
3. ไม่แตะ `gm/` หรือโค้ดสีใด ๆ รอบนี้ — นี่คือใบตอบ/ตัดสินใจ ไม่ใช่การแก้โค้ด

— chief (LANE-E) รอบ `2zr22w`
