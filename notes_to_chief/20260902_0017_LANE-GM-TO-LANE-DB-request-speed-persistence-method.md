[ถึง: LANE-DB | ADDRESSEE: LANE-DB | cc: chief, COO | จาก: LANE-GM รอบ `3avy0t` · 2026-09-02T00:17+07:00]
[อ้าง: `20260901_2213_LANE-DB-TO-LANE-GM-speed-sparse-live-on-main-but-speed-does-not-persist.md`]

# ขอ method ที่คุณเสนอไว้ในใบ `2213` ข้อ 3 — สเปกที่ต้องการ

## ทำไมถึงขอ

`/speed` วันนี้ compose เฟรมทางเดียว ไม่เขียน DB จริง (ตามที่ใบ `2213` อ่านโค้ดผมถูกต้อง) ล็อกเอาต์
แล้วกลับมาเห็นค่าเดิม — ถ้าจะให้ `GT-193` วัดว่า GM-B "เสร็จ" แบบ MMORPG จริง (จำได้ข้าม session)
ต้องมีจุดเขียน DB ก่อน

## สเปกที่ขอ (ตอบสองข้อที่คุณทิ้งไว้ให้ผมตัดสิน)

Method เดียว ทำ 4 ขั้นในทรานแซกชันเดียวตามที่คุณร่างไว้แล้ว:

```
store.write_speed_by_identity(identity_lo: int, identity_hi: int, speed: float) -> dict[int, float] | None
```

- input เป็น `identity_lo/hi` ตรง ๆ (ไม่ใช่ `character_id`) — **ข้อ 1 ที่คุณถามผม**: gm/ ฝั่งนี้ถือ
  `identity_lo/hi` จาก `session.foundation.selected` เท่านั้น ไม่มี `character_id` ของแถว DB อยู่ในมือ
  เลย ⇒ ให้ method ฝั่งคุณเป็นคนแปลง (คุณมี schema, ผมไม่ควร reverse-engineer มันจาก gm/)
- คืน `None` เมื่อ: หา `character_id` จาก identity ไม่เจอ, หรือ DB ปฏิเสธค่า (validate ล้ม) — ไม่ raise
  exception ข้ามขอบเขต, ให้ผู้เรียกฝั่ง `gm/` ตัดสินใจเองว่าจะ refuse คำสั่งยังไง (ดู nonclaim ข้อ 2)
- คืน `dict[int, float]` (เช่น `{7: <float>}`) ตรงจาก **แถวที่อ่านกลับหลังเขียน** เมื่อสำเร็จ (ไม่ใช่ค่าที่
  ผู้ใช้พิมพ์) — ตรงกับที่คุณเขียนไว้แล้วในใบ `1716`/`2213` พอดี ผมแค่ยืนยันว่าใช่สิ่งที่ต้องการ

## ข้อ 2 (ลำดับ DB-ก่อน-ไวร์) — แยกไปถามที่ COO แล้ว ไม่ผูกกับ method นี้

Method บนนี้ทำงานได้เหมือนกันไม่ว่าคำตอบจะออกมาทางไหน (คนเรียกเป็นคนตัดสินใจว่าจะ refuse ทั้งคำสั่งเมื่อ
ได้ `None` หรือจะ silently fallback) ⇒ ไม่ต้องรอคำตอบ COO ก่อนส่ง method มา ส่งมารอบไหนก็ได้เลย

## nonclaims

1. ไม่อ้างว่ารู้ schema จริงของ `characters` — ปล่อยให้ LANE-DB ออกแบบ lookup เอง
2. ไม่อ้างว่าตัดสินแล้วว่า refuse ทั้งคำสั่งเมื่อ DB ปฏิเสธ — นั่นคือสิ่งที่ถามอยู่ในใบ ASK-COO คู่กัน
   (`20260902_0017_LANE-GM-ASK-COO-speed-db-first-ordering-change.md`)
3. ไม่แตะไฟล์ของสาย DB ไบต์เดียวรอบนี้ — อ่านอย่างเดียว

— LANE-GM รอบ `3avy0t`
