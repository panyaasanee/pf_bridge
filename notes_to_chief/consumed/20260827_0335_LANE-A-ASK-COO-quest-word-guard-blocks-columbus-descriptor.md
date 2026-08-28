[ถึง: chief / COO · cc Panya | จาก: สาย A (WORLD) `pf-builder` | รอบ `A_20260827_0335` | 2026-08-27T03:35+07:00]

# LANE-A-ASK-COO — RE-095 ให้ crosswalk เชิงบวกของ Columbus แล้ว แต่ความสามารถที่ต้องสร้างชนกับ tripwire ของโปรเจกต์เองที่ห้าม "quest" ปรากฏใน `src/pirateforce_foundation/`

## สรุปสั้น

`RE-095` (ปิดแล้ว 03:10) ให้ข้อมูลบวกที่ใช้สร้างได้จริงเป็นครั้งแรกสำหรับเส้นทาง Columbus→ทะเล: Columbus =
`MOBS.n_ID=36`, quest `3023` (ไม่ใช่ `3020`/`3301-3303`). สาย A สร้างโมดูลจริง (`world_npc_conversation.py` +
pin JSON + 26 เทส, เทสผ่านหมด, byte-exact กับสูตร payload เดิมของ `make_npc_conversation_quest3020`) แล้ว
**ถอนออกเองก่อน commit** เพราะรันชุดเทสเต็มพบว่ามันทำให้เทสที่เขียวอยู่ก่อนแล้วกลายเป็นแดง:

```
tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests
  ::test_no_foundation_module_implements_quest_or_shop_behavior
```

เทสนี้ grep คำเต็มคำ `quest`/`shop`/`store5`/`price`/`reward`/`trade` ทั่ว `src/pirateforce_foundation/*.py`
ทุกไฟล์ทุกคำและล้มถ้าเจอแม้แต่คำเดียว docstring ของคลาสเทสเขียนตรงๆ ว่า:

> "coverage rows npc_interaction/quest_accept_and_progress and shop_buy_sell. Both notes state that nothing
> is persisted or implemented server-side. If someone lands quest tracking, a shop inventory or a price
> authority, these guards break so the matrix has to be re-graded first."

โมดูลที่สร้างรอบนี้ (ชื่อความสามารถและตัวแปรก็ตาม) เข้าเกณฑ์นี้พอดี — ไม่ใช่ปัญหา false positive ที่หลบด้วยการ
เปลี่ยนชื่อได้อย่างสุจริต เพราะความสามารถนั้น**คือ**การสร้าง descriptor ที่มี quest id จริงๆ

## ทำไมสาย A ไม่แก้เอง

เปลี่ยนชื่อ/คำเพื่อให้ grep ผ่านโดยไม่เปลี่ยนความหมายจะเป็นการหลอกเทสที่มีอยู่โดยเจตนา ขัดกับกฎ
"ไม่ประดิษฐ์/ไม่หลอกเกต" ของโปรเจกต์นี้ตรงๆ และการแก้/ลบเทส guard นี้เอง หรือแก้เกรดของ coverage matrix
เป็นการตัดสินใจระดับ charter (matrix เป็นบันทึกสถานะของทั้งโปรเจกต์ว่า quest/shop ยังไม่ implement
ฝั่งเซิร์ฟเวอร์ ไม่ใช่ไฟล์ที่สาย A เป็นเจ้าของ) — สาย A "ไม่ตัดสินใจแทนใครในเกณฑ์ 3 ข้อที่ต้องหยุดรอจริง"
แต่กรณีนี้เข้าเกณฑ์ตรง: การลง quest capability ใน Foundation อาจเปลี่ยนสถานะที่ทั้งโปรเจกต์บันทึกไว้ว่ายังไม่ทำ
ซึ่งเป็นคำถามทิศทาง ไม่ใช่คำถามโค้ด

## สิ่งที่ต้องตัดสิน

1. **ยืนตาม guard เดิม** (quest/shop capability ยังไม่ควรลง Foundation จนกว่าจะมีการตัดสินใจแยกต่างหากเรื่อง
   ขอบเขต M2) ⇒ เส้นทาง Columbus conversation ของ `BUILD-002` หยุดที่ชั้นข้อมูล (crosswalk มีแล้วจาก `RE-095`)
   รอคำสั่งเปิดทางจาก COO/เจ้าของก่อนเขียนโค้ดที่มีคำว่า quest ใน `src/` อีก
2. **Re-grade coverage-matrix rows `npc_interaction/quest_accept_and_progress`/`shop_buy_sell`** อย่างมีสติ
   (คนละเรื่องกับที่สาย A แก้ไฟล์เทส/matrix เอง) แล้วอนุญาตความสามารถนี้อย่างเป็นทางการ — โค้ด+เทสที่ถอนไปรอบนี้
   พร้อมนำกลับทันที (พิสูจน์แล้วว่าเทสผ่าน 26/26 และ byte-exact กับสูตรเดิม)

สาย A ไม่มีความเห็นว่าทางไหนถูก — แค่รายงานว่าทางแรก (ทำเงียบๆ ต่อ) จะทำให้เทส tripwire ที่ตั้งใจออกแบบมาให้พัง
กรณีนี้ **พังจริงตามที่ออกแบบ** และสาย A เลือกไม่ข้ามมันเอง

## ไฟล์ที่แตะ

- `pf_bridge/CLIENT_RE_QUEUE.md` — เพิ่ม `RE-097` (identity crosswalk ของ Columbus ใน bg0001, คนละคำถามจาก
  `RE-093`, ไม่ชน guard นี้เพราะเป็นใบใน `pf_bridge` ไม่ใช่ `src/`)
- `pf_bridge/rounds/A_20260827_0335_*.md` — รอบนี้ฉบับเต็ม (มี diff/เทสที่ถอนไปอธิบายละเอียดกว่านี้)
- `pirate-force-server` — **0 ไฟล์เมื่อปิดรอบ** (สร้างจริง 3 ไฟล์ระหว่างรอบแล้วลบเองก่อน commit)

## CORE-REQUEST

none — ไม่มีจุดที่ต้องแก้ `runtime.py`/`app.py` รอบนี้ (ไม่มีอะไรให้ wire เพราะไม่มีอะไรส่ง)

— สาย A · WORLD
