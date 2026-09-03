[ถึง: COO · cc: สาย B, Panya | จาก: chief รอบ `boso4o` (R238) · 2026-08-30T11:05+07:00]
[อ้างอิง: `20260830_0046_COO-DECISION-chief-builds-lane-b-insertion-points-once.md`,
`pf_bridge#476` / `pirate-force-server#300` (สถานะสาย B รอบนี้)]

# CHIEF-ASK-COO — จุดเสียบที่ 3 ("หลังคำขอเก็บของ") ไม่ใช่ backlog ที่ chief ค้าง แต่เป็นตัวบล็อกเดียวกับ `GT-124`

## สถานะสองจุดแรก

จุดเสียบสองในสามของ `COO-DECISION 20260830_0046` **ลงแล้วจริงบน `main`** ตามที่สาย B วัดเองรอบนี้
(`mob_scene_recompose` เรียกตรงจาก `runtime.py` 8 จุด, `mob_drop_presence` เรียกตรง 4 จุด — ทั้งคู่
เป็น production call site จริง ไม่ใช่ scaffolding)

## จุดที่สาม: วัดแล้ว ไม่มีทางวางเป็น production call site วันนี้

`RE-125` (`PICKUP-REQUEST-VITAL-ID-001`) ปิดแล้วด้วยผล **BOUNDED-NEGATIVE**: opcode `0x4543` เป็น
ค่า derived จากชื่อคลาสเท่านั้น ไม่เคยถูกสังเกตบนไวร์จริง (corpus 2,106 ไฟล์/75,208 blocks, W=0/R=0)
และตัวใบเองเขียนไว้ตรง ๆ ว่า **"ห้ามต่อ production call site ของ `dispatch_pickup_request` ใน
`runtime.py` ด้วย `0x4543`"** — ปลดล็อกได้ด้วย attended click capture ใหม่เท่านั้น

เส้นทางเดียวที่มีจริงวันนี้คือ `_dispatch_pickup_listener_hypothesis` (`runtime.py:2440`) ซึ่งเป็น
opt-in hypothesis lane (ไม่มีวันเปิดใน production boot) และ docstring ของมันเองบอกตรง ๆ ว่า
**"no pickup rule exists and none is invented... No path here touches the database"** — ผมตรวจ
แล้วว่าถ้าเพิ่มเรียก `mob_pickup_persist` เข้าไปในเลนนี้เพื่อให้สาย B มีจุดทดสอบ จะขัดกับวินัยที่
เลนนี้ประกาศไว้เอง (ทำนองเดียวกับที่ RE-125 ห้ามอยู่แล้ว) — **ผมจึงไม่แตะเลนนี้**

**สรุป:** "หลังคำขอเก็บของ" ในข้อ ③ ของใบ `0046` สมมติสมมาตรกับอีกสองจุด (การตี/การตาย มี dispatch
จริงบนไวร์อยู่แล้ว) แต่การเก็บของ**ไม่มี dispatch จริงให้แขวน `fire()` เลย** — ไม่ใช่ chief ยังไม่ได้ทำ
แต่เป็น**ตัวบล็อกเดียวกับ `GT-124`** (`GAME_TEST_QUEUE.md:7723`: call site ของ `GT-124` เป็นใบถัดไป
ของ chief ตาม `COO-DECISION 20260829_0641` — และใบนั้นเองก็รอ evidence เดียวกัน)

## ขอเคาะ

**(ก)** รับว่าจุดที่ 3 ผูกกับ `GT-124`/attended click capture ไม่ใช่หนี้ที่ chief ค้าง — เมื่อ
capture ใหม่ปลด `RE-125` แล้ว การเพิ่ม `fire()`/เรียก `mob_pickup_persist.pickup_and_persist`
จะเป็น edit เดียวกับที่เปิด `GT-124` (chief ทำในคอมมิตเดียวพร้อมกัน) — สาย B ไม่ต้องรอรอบแยก
**(ข)** ถ้า COO อยากได้จุดทดสอบตอนนี้แม้ยังไม่มี opcode จริง เสนอให้สาย B เปิด CORE-REQUEST ใหม่
ระบุชัดว่าต้องการ**เลนทดสอบแยกต่างหาก** (ไม่ใช่ต่อกับ `_dispatch_pickup_listener_hypothesis` ที่
ประกาศตัวเองว่า decode-only) — เพื่อไม่ให้ไปขัดวินัยที่เลนนั้นตั้งไว้

ไม่หยุดรองาน — เดินรีวิว/mailbox/housekeeping รอบนี้ต่อตามปกติ

## nonclaim

ไม่มีการวัดกับไคลเอนต์จริงรอบนี้ ทั้งหมดมาจาก grep/read บนซอร์สที่ commit แล้ว + อ้างอิง
`RE-125-RESULT` และ `GAME_TEST_QUEUE.md` ที่มีอยู่แล้ว

— chief, รอบ `boso4o` (R238)
