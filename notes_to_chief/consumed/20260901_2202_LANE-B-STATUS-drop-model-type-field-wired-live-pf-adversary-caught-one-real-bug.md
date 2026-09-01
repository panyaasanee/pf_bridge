[ถึง: chief, COO | ADDRESSEE: ALL | จาก: LANE-B (COMBAT) รอบ `8efcx1` · 2026-09-01T22:02+07:00]

# LANE-B ROUND 8efcx1 — wired n_DROPMODEL_TYPE field live in mob_loot.py, pf-adversary found + we fixed one real HIGH bug in the process

## สรุปสั้น

บริโภคจดหมาย `ka1-B` เรื่อง drop-model-selector field (0..12, mask bit 0x04/+0x18)
สร้างจริงใน `pirate-force-server` (3 commits, branch `claude/zen-einstein-8efcx1`,
PR #513 draft): เพิ่ม element mask ใหม่ 0x16 ที่ส่ง `n_DROPMODEL_TYPE` จาก
`field_drop_tables.ITEMS[item_id][3]` (ข้อมูลนี้ไมน์ไว้แล้วตั้งแต่ก่อนรอบนี้ ไม่ต้องเดา)
แล้ว**สลับ default จริง** — `refresh_frames` (path ที่ทุกคิลจริงเดินผ่าน) ตอนนี้ส่ง
mask 0x16 (57 ไบต์) แทน mask 0x12 เดิม (54 ไบต์) โดยไม่แตะ `runtime.py`/`app.py` เลย
เพราะจุดต่อจริงอยู่ในไฟล์ของสาย B เอง (`mob_loot.py`) — ไม่ต้องมี CORE-REQUEST

## pf-adversary 3 รอบ (ตามกฎ COO-DECISION 20260901_1744 — agent ที่เขียนโค้ดไม่มี
Agent tool ของตัวเอง เซสชันนี้จึงเรียก pf-adversary แทนหลังทุก commit)

1. commit แรก: จุดเดียวที่พบ — เอกสารอ้าง call site ผิด (ข้อมูลเก่า 2 วัน) ไม่ใช่บั๊กสาย wire
2. commit สอง (สลับ default จริง): พบจุด **HIGH** — `mob_drop_presence.py`'s trim-cap
   ยังอ้างซีลลิ่งเก่า (2426) ทั้งที่ path จริงมีซีลลิ่งเล็กกว่า (2183) ⇒ ledger 2184-2426
   แถวจะโดนปฏิเสธทั้งคิลเงียบ ๆ แทนที่จะ trim ตามดีไซน์ — pf-adversary reproduce ตรง ๆ
   ด้วย ledger จำลอง 2200 แถว ไม่ใช่แค่ทฤษฎี
3. commit สาม (แก้ข้อ 2): pf-adversary reproduce การแก้ในอีก worktree แยก ยืนยัน boundary
   ที่ 2183/2184 พอดี ไม่พบจุดใหม่ — clean bill

เทสรวมสุดท้าย: `6417 passed, 323 skipped, 0 failed`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

server ส่งไบต์ต่างจริงทุกคิล (57 ไบต์ vs 54 ไบต์เดิม) — แต่ผลบนจอ (โมเดลขึ้นหรือไม่)
**ยังไม่มีใครวัด** GT-045 เองพิสูจน์แล้วว่า `n_DROPMODEL_TYPE=1` อย่างเดียวไม่พอ ผลจริงรอ
attended test — เปิด GT ticket ใหม่ท้าย `GAME_TEST_QUEUE.md` แล้ว (pf-queue-author,
เลขที่แน่นอนดู `rounds/B_20260901_2036_8efcx1_*.md`)

## rollback

`mob_loot.DROP_MODEL_TYPE_FIELD_ENABLED = False` บรรทัดเดียว คืนไบต์เดิมทุกกรณี
(pf-adversary ยืนยันคำอ้างนี้จริง ไม่ใช่แค่คอมเมนต์ตาย)

## ตอนนี้ต้องทำอะไรต่อ

ไม่มีอะไรบล็อกใคร รอ Panya รัน GT ticket ใหม่เมื่อสะดวก (ไม่ใช่ตัวบล็อกสายไหนตามกฎใหม่ของ
NOW.md) PR ทั้งสอง repo (#513 server, #752 bridge) จะปลด draft ปิดรอบตามลำดับมาตรฐาน

-- LANE-B
