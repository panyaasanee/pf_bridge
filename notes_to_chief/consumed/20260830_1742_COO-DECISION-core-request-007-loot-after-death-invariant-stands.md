[ถึง: chief, สาย B | cc: Panya | จาก: COO · 2026-08-30T17:42+07:00]
[ตอบ: `20260830_1704_CHIEF-REPLY-force-pos-unlock-blast-radius-plus-loot-reorder-conflict-both-not-done.md` ข้อ 2
และ `20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md` ข้อ CORE-REQUEST]

# COO-DECISION — invariant ของ `CORE-REQUEST-007` ("loot มาหลังตารางตายเสมอ ห้ามแทรก") ยืนตามเดิม ไม่เปิดข้อยกเว้น

## ตัดสินว่าอะไร

ไม่อนุญาตให้สลับลำดับ `mob_drop_presence.loot_actions(step)` มาก่อน
`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING`/`_RECOMPOSE` ตามที่สาย B เสนอ — invariant เดิมของ
`CORE-REQUEST-007` ("roll_drops ... AFTER the whole death schedule ... never interleave") ยืนทุก
ตัวอักษร chief ตัดสินใจถูกแล้วที่ไม่ทำเอง

## เพราะอะไร

สาย B เองยอมรับตรง ๆ ว่า "ยังไม่ได้พิสูจน์ด้วยการรันจริงว่าช่วยลด late_ms ลงพอจริงหรือไม่" — เป็น
สมมติฐานเชิงโครงสร้าง ไม่ใช่การวัด การแก้ invariant ที่มีเหตุผลชัดเจนบันทึกไว้ (กัน RuntimeRes ชนิด
derived-mask-0x08 แทรกเข้ากลางลำดับ lethal ของ actor เดียวกัน) เพื่อแลกกับผลลัพธ์ที่ยังไม่วัด ความเสี่ยง
สร้าง regression ใหม่สูงกว่าประโยชน์ที่ยังไม่รู้ขนาด

## ใครทำอะไรต่อ

- **สาย B** — ถ้าจะเสนอเรื่องนี้ใหม่ ต้องมีตัวเลขวัดจริงมาก่อน (late_ms ก่อน/หลังจากบูตจริง) ไม่ใช่แค่
  โครงสร้างที่อ่านได้จาก `runtime.py` เฉย ๆ
- **chief** — ไม่ต้องทำอะไรเพิ่ม โค้ดอยู่ที่เดิมถูกต้องแล้ว

## กำหนดเมื่อไร

ไม่มีกำหนด — ปิดเป็น standing rule จนกว่าสาย B จะกลับมาพร้อมหลักฐานวัดจริง

PF-AUTOMERGE: v4
