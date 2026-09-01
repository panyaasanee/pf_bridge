[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: สาย A (WORLD) รอบ `njkvcc` · 2026-09-01T17:37+07:00]

## ติดอะไร

รอบนี้ไม่มีงานในเขต (มือถือ P-1/P-2/P-3/UI-A/GM-B/UI-B ทุกใบ, ไมล์สโตนพักตาม PANYA-ORDER
20260901_0215, กล่องจดหมายว่าง) เลยหยิบ technical debt ตามกฎ F: เซสชันนี้มี Agent tool จริง (สอง
รอบก่อน `tmizmk`/`2ahq88` ไม่มี ต้องรีวิวมือแทน pf-adversary แล้วติดเป็นคำถามค้างถึง COO) เลยส่ง
pf-adversary ไปตรวจซ้ำโปรไฟล์ที่ 6 ของ `logout_hypothesis.py` (ที่ merge ไปแล้วจาก PR #484)
แบบจริงจัง

ผลตรวจ 6 เรื่องผ่านหมด (production_allowed escalation, allowlist bypass, hash-pin drift, CI
ไม่ข้ามเทสเงียบ, double-count/routing, race บน one-shot latch) — รายละเอียดเต็มใน
`rounds/A_20260901_1737_njkvcc_*.md`

แต่เจอจุดหนึ่ง: คอมเมนต์ใน `logout_hypothesis.py:193` อ้างว่า *"EVERY TAG BYTE (0x08 / 0x32 / 0x44)
IS READ FROM THE CLIENT'S OWN SERIALIZER; nothing structural is invented"* — แต่หลักฐานสถิตที่มีจริง
(`pf_bridge/external/PF_SERIALIZER_FIELDS.tsv:1125`) บอกว่า field 3 ของ `ReturnSelectServerVital`
คือ `UNTAGGED_STRING8_LEN32LE` ไม่ใช่ tag `0x44` — ค่า `0x44` ถูกยืนยันจริงเฉพาะข้อความอื่น
(`DeleteActorVital`, GT-018) แล้วเหมาเอาไปใช้กับทั้งตระกูล ไม่เคยวัดตรงกับ `ReturnSelectServerVital`
เอง (RE-070 erratum ก็บันทึกไว้แล้วว่าสองเฟรมที่จับได้เป็น W-direction เท่านั้น) เครื่องมือที่อ้างว่า
"independent walker" (`tools/verify_logout_return_select_encoder.py:72`) ก็ hardcode
`FIELD3_TAG = 0x44` ตัวเดียวกัน — อิสระจากโค้ด composer แต่ไม่อิสระจากสมมติฐาน schema เดียวกัน

ไม่ใช่บั๊กที่พิสูจน์แล้ว (production_allowed ยังคง False ทุกที่, เคยยิงจริงแล้วครั้งหนึ่งใน
`GT-033` Variant B ได้ผลลบ ไม่มีใครโยงผลลบนั้นเข้ากับไบต์นี้) — เป็น **ข้อสงสัยที่มีหลักฐานจริง**
ว่าคำอ้าง "ไม่มีอะไรถูกประดิษฐ์ขึ้น" อาจเกินจริงสำหรับฟิลด์นี้โดยเฉพาะ

`logout_hypothesis.py` และ `logout_dialog_open_hypothesis.py` อยู่ใต้ข้อจำกัดที่ chief เขียนไว้เอง
ในใบ `20260901_1605` ("ไม่เปิดเขตเขียนถาวร งานครั้งถัดไปกลับมาเป็นของ chief") สายนี้เลยไม่แก้เอง

## ทางเลือกที่เห็น

(ก) chief แก้คอมเมนต์ตรงเองรอบหน้า — ต่อท้ายด้วย `[STALE][MEASURED]` ตามธรรมเนียม ระบุว่า
    ค่า `0x44` ของฟิลด์ 3 เป็นการเหมาจาก `DeleteActorVital` ไม่ใช่วัดตรงกับ `ReturnSelectServerVital`
    เอง แล้วแก้คอมเมนต์ของ `tools/verify_logout_return_select_encoder.py` ให้บอกตรง ๆ ว่ามันตรวจ
    ความสอดคล้องภายใน ไม่ใช่แหล่งอิสระที่สอง
(ข) chief ให้สิทธิ์สายนี้แก้ครั้งเดียวอีกครั้ง (เหมือนใบ 1605) เฉพาะคอมเมนต์/docstring แบบ
    append-only ไม่แตะ logic/allowlist
(ค) เปิด RE ใบใหม่ถาม static-RE ว่ามีทางหา raw capture ของ `ReturnSelectServerVital` field 3
    เพิ่มเติมไหม (ปิดคำถามที่ pf-adversary ทิ้งไว้ตอนท้ายรอบนี้) แยกจากเรื่องแก้คอมเมนต์
(ง) ไม่ทำอะไร — ปล่อยคำอ้างเดิมไว้ เพราะ production_allowed ยัง False และไม่ใช่บั๊กที่พิสูจน์แล้ว

## เลือกอันไหนไปแล้ว

ยังไม่เลือก — รอ chief ตัดสิน (ก)/(ข) ระหว่างสองอย่างนี้ ส่วน (ค) เสนอให้เปิดคู่ขนานไม่ว่าจะเลือก
อะไร เพราะเป็นคำถามเปิดจริงที่ pf-adversary หาไม่ได้ต่อจากคลังไฟล์ที่ clone นี้มี รอบนี้เลือก (ง)
ชั่วคราวเท่านั้น (ไม่แก้อะไร) จนกว่าจะได้คำตอบ — [สมมติของสาย A - รอ chief/COO ยืนยัน]

## ถ้าผิดต้องย้อนอะไรบ้าง

ไม่มีอะไรต้องย้อน — รอบนี้ไม่ได้แก้โค้ด/ข้อความใด ๆ ในไฟล์ที่ล็อก ถ้า chief เลือก (ก) หรือ (ข) แล้ว
พบภายหลังว่าคำอ้างเดิมถูกต้องจริง (เช่นได้ raw capture มายืนยัน `0x44` ตรงกับ
`ReturnSelectServerVital`) ก็แค่ลบ `[STALE]` แล้วเขียน `[MEASURED, confirmed]` ทับ — ไม่มีผลกระทบ
เชิง production เพราะ `production_allowed` ปิดอยู่ตลอด

## เพิ่มเติมสำหรับ COO

ปิดคำถามค้างจากรอบ `2ahq88`: "รีวิวมือใช้แทน pf-adversary จริงได้ถาวรไหม" — คำตอบจากการทดลองจริง
รอบนี้คือ **ไม่เต็มร้อย**: diff เดียวกันที่ผ่านรีวิวมือสองรอบมาแล้ว พอส่งเข้า pf-adversary จริง
เจอช่องโหว่หลักฐานที่รีวิวมือทั้งสองรอบไม่เห็น เสนอกฎ: เซสชันไหนมี Agent tool จริง (เซสชันนี้มี)
ต้องเรียก subagent จริงก่อน commit เสมอ รีวิวมือเป็นทางสำรองเฉพาะเซสชันที่ยืนยันแล้วว่าไม่มีเครื่องมือ
จริง ๆ เท่านั้น

PF-AUTOMERGE: v4
