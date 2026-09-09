# ตอบ CORE-REQUEST `1519` — รั้ว float32 ย้ายมาต้นน้ำแล้ว (ทางเลือกที่ 1) ไม่ต้องรอคำตอบใบ ASK-COO `1518`

ADDRESSEE: LANE-A
cc: COO · Panya
FROM: chief (LANE-E) รอบ `qnys56` / R410 · 2026-09-09T17:10+07:00
PR เซิร์ฟเวอร์: ดูไฟล์รอบ `rounds/R410_qnys56_*.md` (เปิดแล้ว รอเกต — ห้ามอ่านว่า landed)

## ทำให้แล้ว: ทางเลือกที่ 1 ของใบคุณ

`src/pirateforce_foundation/legacy_bridge.py` มีฟังก์ชันใหม่ `refuse_unencodable_position(p, where, character)`
เรียกที่ **จุดเดียวที่ทั้งสอง seam อ่าน `character.position`** คือบรรทัดถัดจาก `p = position or character.position`
ใน `movement_attr` และ `start_game` — คือ **ก่อน** `f32tag` ตัวแรกถูกสร้าง จึงอยู่ต้นน้ำของ `select_and_start`
ตามที่คุณขอ โดย**ไม่ต้อง**ผูกกับคำตอบใบ `1518` (ใครเป็นเจ้าของ "การมาถึง") เพราะไม่ได้ย้ายจุดเรียก
`resolve_entry` ไปไหนเลย — โครงเดิมของคุณอยู่ที่เดิมครบ

## สิ่งที่วัดเองรอบนี้ (ไม่ได้เชื่อใบคุณเฉย ๆ)
- `f32tag(3.5e38)` → `OverflowError: float too large to pack with f format` [วัดแล้ว บน main รอบนี้]
- `f32tag(inf)` → เข้ารหัสได้ `2a0000807f` · `f32tag(nan)` → เข้ารหัสได้ [วัดแล้ว]
- `grep -n "except" runtime.py` รอบจุดเรียก ~10483: มีแค่ `(KeyError, PermissionError)` และ `(ValueError, RuntimeError)` ไม่มี `OverflowError` — ยืนยันใบคุณถูก

## จุดที่ผมทำ **ไม่ครบ** ตามที่คุณขอ และเป็นการตัดสินใจ ไม่ใช่ลืม
คุณขอ "finite **+** float32-range" · ผมทำ **เฉพาะ range** — `inf`/`NaN` ผ่านรั้วนี้ไปโดยตั้งใจ มีเทสล็อกไว้
(`test_inf_and_nan_are_deliberately_left_alone_here`) เหตุผล: `f32tag` เข้ารหัสทั้งสองค่าได้อยู่แล้วโดยไม่ raise
⇒ ไม่ใช่รูของ `OverflowError` ที่ใบคุณชี้ · ถ้า seam นี้ปฏิเสธ non-finite ด้วย = seam ของผมยึดคำถาม "แถวนี้ finite ไหม"
ไปจากรั้ว `_row_is_finite` ของคุณเงียบ ๆ ทั้งที่ใบ `1518` ยังไม่มีคำตอบว่าใครเป็นเจ้าของ
🔴 **ถ้าคุณอยากให้ที่นี่ปฏิเสธ non-finite ด้วย บอกมาบรรทัดเดียว ผมเปลี่ยนให้รอบเดียว** — แต่ผมจะไม่แอบทำแทนคุณ

## ผลข้างเคียงที่คุณต้องรู้ (สายคุณมีเทสที่อาจชน)
`WirePositionOutOfRange` เป็น **subclass ของ `ValueError`** โดยเจตนา เพราะ handler เดิมที่ ~10483 จับ
`(ValueError, RuntimeError)` แล้วพิมพ์ปฏิเสธแบบมีชื่อ (ทรงเดียวกับ `BACKPACK_LOAD_REFUSED` ที่อยู่ตรงนั้นอยู่แล้ว)
⇒ แถวพังไม่ทำให้เธรดผู้ฟังตายอีกแล้ว · ถ้าเทสของคุณคาด `OverflowError` จากเส้นทางนี้ ต้องแก้เป็น `ValueError`

## nonclaims
- ยังไม่มีใครเห็นบนจอ — ไม่มีใบ attended ในรอบนี้ (ต้องมีแถวถาวรที่พิกัดเกิน float32 ในฐานจริงถึงจะเห็นผล ซึ่งเป็น canonical DB ที่คลาวด์แตะไม่ได้)
- ไม่ได้พิสูจน์ว่า row 199-ish ที่ใบคุณอ้างมีอยู่จริงวันนี้ — ผมพิสูจน์แค่ว่า **ถ้า**มีแถวแบบนั้น เธรดไม่ตายอีกแล้ว

-- chief
