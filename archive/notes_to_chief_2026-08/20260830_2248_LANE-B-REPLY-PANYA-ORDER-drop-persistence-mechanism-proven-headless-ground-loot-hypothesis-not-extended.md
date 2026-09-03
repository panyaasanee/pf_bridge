[ถึง: Panya · chief · cc COO, สาย A/GM, กะอื่น ๆ | ADDRESSEE: chief, cc PANYA | จาก: สาย B (COMBAT) รอบ u98etz · 2026-08-30T22:48+07:00]

# 🔴 SUPERSEDED ก่อน push — สาย B ชนกับรอบ `xt0g9c`/`qb1ytr` ที่ตอบใบนี้ไปแล้วครบ ก่อนแอตเทนเดดวัดจริงและ COO เคาะปิดทางแล้ว

## สิ่งที่เกิดขึ้น

รอบนี้ (`u98etz`) เริ่มจาก `origin/main` ที่ยังเก่า (`5fc4f6e`) แล้วใช้เวลาสร้างเทส/วิเคราะห์นานพอที่จะพลาดรอบสาย B อื่นถึงสามรอบที่ตอบคำถามเดียวกันนี้ไปแล้วจริง (`xt0g9c`, `qb1ytr`, และรอบที่ตามมา) รวมถึงรอบ **attended จริง** (`GT143-GT132-GT149-RESULT`, `20260830_1554`) ที่วัด `label_life = 0.2 วิ` และ **COO-DECISION 2026-08-30T17:42+07:00** ที่ปิดทางไม่ให้เปิด resend ใด ๆ ตอนนี้ ก่อน `git push`/เปิด PR รอบนี้จะไปชนกับ `main` ตรง ๆ (merge conflict บน `GAME_TEST_QUEUE.md` และ mailbox stub 2 ไฟล์) — fetch แล้วพบว่างานที่ทำไปซ้ำกับที่มีอยู่แล้วเกือบทั้งหมด

**ตามกติกาใหม่ที่เพิ่งประกาศ (`COO-DECISION 20260830_2244` — claim-before-work สำหรับใบเปิดกว้าง)**: ใบ `PANYA-ORDER` เป็นใบเปิดกว้างที่มากกว่าหนึ่งรอบของสาย B หยิบได้พร้อมกันโดยไม่รู้ตัว — รอบนี้ไม่ได้เขียนไฟล์ `CLAIM-*` ก่อนเริ่ม (กติกาเพิ่งประกาศตอน 22:44 ระหว่างที่รอบนี้กำลังทำงานอยู่แล้ว) ถือเป็นเคสตัวอย่างที่กติกาใหม่มีไว้ป้องกัน

## สิ่งที่ยังเป็นความจริง (ไม่ต้องถอน)

`mob_drop_presence.sustain_a_kill(cell, legacy, drops=())` เรียกซ้ำแล้ว resend เฟรมทั้ง ledger ได้จริงโดยไม่มีต้นทุนเพิ่ม พิสูจน์ headless ด้วยจังหวะไม่เท่ากันรวม 34 วินาที (`pirate-force-server/tests/test_mob_drop_presence_sustained_resend_hypothesis.py`, ผ่าน pf-adversary 3 มุม) — **ข้อเท็จจริงนี้ยังจริง** และสอดคล้องกับที่รอบ `xt0g9c` วัดไว้ก่อนแล้ว (`tests/test_mob_drop_presence.py` 48/48) ไม่มีอะไรขัดแย้งกันในชั้นนี้

## สิ่งที่ถอน — CORE-REQUEST resend-on-movement

รอบนี้เคยเขียน CORE-REQUEST เสนอต่อสาย `runtime.py` ให้ resend ทุกครั้งที่มี `TargetPosVital` ขณะ scenario flag เปิด **ถอนแล้วก่อน push** (เปลี่ยนชื่อ constant เป็น `WITHDRAWN_DROP_PRESENCE_RESEND_ON_MOVEMENT_WIRING` ใน `mob_drop_presence.py` ขีดฆ่าไม่ลบ) เพราะ:

1. **แอตเทนเดดวัดจริงแล้วว่าคอขวดไม่ใช่ที่นี่**: `label_life = 0.2 วิ` เท่าเดิม ไม่ว่า ledger ฝั่งเซิร์ฟเวอร์จะรอด 120 วิหรือไม่ — ปัญหาอยู่ที่ป้ายฝั่งไคลเอนต์ไม่ถูก redraw ไม่ใช่ที่ฝั่งเซิร์ฟเวอร์ resend ได้ไหม (ตอบไปแล้วว่า "ได้" ตั้งแต่รอบ `xt0g9c`)
2. **COO-DECISION 20260830_1742 ปิดทาง resend ที่มีเพดานหรือ movement-driven ไว้ตรง ๆ** จนกว่าจะมีรอบ attended ที่ยิง resend **ครั้งเดียว** (ไม่ใช่ต่อเนื่อง) แล้ววัดว่าป้ายกลับมาไหม ข้อเสนอ resend-on-every-movement ของรอบนี้เป็นรูปแบบที่ COO ปฏิเสธไปแล้วตรง ๆ

## GT-146 / `GAME_TEST_QUEUE.md`

ไม่แก้ทับ — ใช้เวอร์ชันบน `main` ที่รอบ `xt0g9c`/`qb1ytr` และรอบ attended แก้ไว้แล้ว (P0 gate ยืนยันด้วยข้อมูลจริงว่า ABORT ทุกรอบจนกว่าจะมีเงื่อนไขใหม่, nonclaim ③ ชี้ไปที่ `REEMISSION_REDRAWS_THE_LABEL` ตรง ๆ) เวอร์ชันนั้นถูกต้องกว่าที่รอบนี้เคยแก้เอง

## กล่องจดหมาย

ใบ `PANYA-ORDER 1450` และใบ `กะ1-A 1509` มี `.CONSUMED.txt` บน `main` แล้ว (จากรอบ `xt0g9c`) — ไม่ต้องบริโภคซ้ำ รอบนี้ไม่สร้าง stub ทับ

## เทส

`pirate-force-server`: `pytest tests/ -q` เขียวหลัง merge `origin/main` (รวมงานทุกรอบที่แทรกเข้ามาระหว่างนี้) ดูผลเต็มใน round record

## บทเรียน

ยืนยันเหตุผลของกติกา claim-before-work ที่ COO เพิ่งประกาศด้วยตัวเอง — รอบนี้คือตัวอย่างสดของปัญหาเดียวกับที่สาย GM เจอกับ `pf_bridge#534`

PF-AUTOMERGE: v4
