[ถึง: **COO** | จาก: **chief cloud (สาย E)** · รอบ R177 (`mdj01v`) · 2026-08-26T16:00+07:00]

# CHIEF-ASK-COO — `mob_combat_ledger`/`mob_death_register` เป็น per-session ไม่ใช่ server-wide จะยอมรับไหมสำหรับ `v4`

ไม่บล็อกฉัน — เดินงานอื่นต่อแล้ว ตอบเมื่อสะดวก

## บริบท

รอบนี้เดินสาย `CORE-REQUEST-005` (`MOB-COMBAT-001`, ค้างเลยกำหนด COO 26 ส.ค. 08:00 มาแล้ว) — `runtime.py`
เรียก `mob_combat`/`mob_death` แบบไม่มีแฟล็ก ผ่าน `pf-adversary` บังคับก่อน commit (2 Low + 1 Informational
ทั้งหมดติดป้ายในโค้ดแล้ว ไม่มี CRITICAL/HIGH) commit `6105d26` push แล้ว สวีตเต็มเขียว(cloud sanity)
`3097 passed, 327 skipped, 4986 subtests, 0 failed`

## คำถาม

`self.mob_combat_ledger` / `self.mob_death_register` ถูกเก็บเป็น **per-session state** (ในตัวเดียวกับที่เก็บ
`self.world_travel_gates` อยู่แล้ว) ตามที่โจทย์รอบนี้สั่งไว้ตรง ๆ ("hold as session state, follow the existing
pattern") — ผลคือถ้าผู้เล่นสองคนต่อคนละ session ตีมอนสเตอร์ตัวเดียวกัน **แต่ละคนเห็น HP ของมันคนละค่า**
(session ของใครก็ตามที่ยังไม่เห็นการตีของอีกฝ่าย) และถ้า session หลุดแล้วต่อใหม่ ledger เปิดใหม่เต็มเลือด
ทับของเดิมที่อีก session หนึ่งอาจทำเลือดค้างไว้

## ทำไมถึงถามแทนที่จะตัดสินเอง

เข้าเกณฑ์ `[เก็บไว้ถามเจ้าของ]` ตามนโยบาย 5 ("multiplayer ก้อน 2 จบต้องให้เจ้าของเคาะก่อนเดินก้อน 3")
— นี่คือรอยต่อ session-state ↔ multiplayer โดยตรง ไม่ใช่แค่รายละเอียด implementation

## ตัวเลือก

1. **ยอมรับสำหรับ `v4`** — `v4` เป้าคือ "ตีได้ตายได้" ด้วยผู้เล่นคนเดียวในเซสชันเดียว ยังไม่ประกาศ multiplayer
   จริง ⇒ ความเพี้ยนนี้ไม่มีใครเห็นจนกว่าจะมีสอง connection พร้อมกันจริง — เลื่อนแก้ไปพร้อม persistence
   (นโยบาย 7 "Lane 2/3 เลื่อนท้ายสุด")
2. **ยกเป็น server-wide ledger ตอนนี้** — ต้องออกแบบ locking/single-writer ใหม่ (ตอนนี้ `REFUSE_LEDGER_STALE`
   retry เข้าไม่ถึงเพราะ per-session รับประกัน single-writer โดยธรรมชาติ) งานเพิ่มก่อน `M4` ปิด (29 ส.ค.)

**คำแนะนำของฉัน:** ทาง 1 — เข้าเกณฑ์ "ทำครั้งเดียวจบ" ไม่ได้จริง ๆ จนกว่าจะรู้ทรงของ persistence/reconnect
ก่อน (ยังไม่ออกแบบ) ยกเป็น server-wide ตอนนี้เสี่ยงต้องรื้อซ้ำเมื่อ persistence ลงจริง

— chief
