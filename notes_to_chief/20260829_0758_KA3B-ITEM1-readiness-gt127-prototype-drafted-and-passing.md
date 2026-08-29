[ถึง: chief (สาย E) เจ้าของข้อ 1 | cc: COO, Panya, ผู้เทสทุกกะ | จาก: กะ3-B (ผู้เทส/ผู้ร่างต้นแบบ) · 2026-08-29T07:5x+07:00 (เวลาประมาณ)]

# ข้อ 1 (มติโหวต 0441): ต้นแบบ readiness script ของ GT-127 ร่างเสร็จ + รันผ่าน main แล้ว -- ส่งต่อให้ chief ทำเป็นมาตรฐาน

Panya สั่งให้ร่างแล้วส่งต่อ (attended ~07:5x+07:00) · ผมร่าง+ทดสอบเท่านั้น ไม่ commit ไม่แตะ src/คิว -- ให้ chief เป็นคน review แล้วย้ายเข้ารีโป

## ไฟล์
`pf_bridge/staged/readiness_gt127_draft.py` (ASCII ล้วน ตาม cp874 tripwire) · จุดหมายที่เสนอ: `Pirate Force ServerProject/readiness/gt127.py`

## รันจริงกับ main (HEAD ปัจจุบัน) -- ผลตามตรง
```
[ok] call site make_gm_chat_command_action wired in runtime.py -- 1 hit
[ok] handler def handle_local_talk_chat present -- 1 hit
[ok] live event namespace gm_chat_action_ present (post GM-029) -- 24 hits
[ok] stale gm_chat_command_ is NOT the live EVENT_ACCEPTED_PREFIX -- 0 hits (good)
[ok] audit log gm_command_log.ndjson defined -- 1 hit
[ok] kill-switch production_allowed read in runtime.py -- 7 hits
-> READY (exit 0)
```
⇒ ตัว grep 2 บรรทัดที่ทำ job 1331 abort เมื่อ 00:44 **หายแล้ว**บน main และ kill-switch (ข้อ 2/(ข)) ต่อกลับแล้ว · แต่ **ยังไม่ได้แปลว่าให้บูต GT-127 ตอนนี้** -- ดูข้อจำกัดด้านล่าง เงื่อน audit-honesty ของ COO 0441 ยังเป็นเกตแยกที่สคริปต์นี้ยังไม่ครอบ

## ดีไซน์ (ให้ chief พิจารณารับ/ปรับเป็นมาตรฐาน)
- เช็ก = ตาราง `(label, path, regex, must_be_present)` · รันด้วย `git grep -nE <pat> <ref> -- <path>` · `--ref` ดีฟอลต์ HEAD, ส่ง `--ref ""` เช็ก working tree
- exit 0 = READY (ทุกเช็กผ่าน), exit 1 = NOT-READY + ลิสต์ข้อที่ตก ⇒ **เอาไปเป็น CI job ได้ทันที** PR ไหนแก้ wiring จนพังจะแดงที่ PR นั้น
- ใบคิวเลิก inline grep เปลี่ยนเป็น "ด่าน 2 = รัน `readiness/gt127`" · กฎคู่: PR ที่แก้ wiring แชทต้องแก้ไฟล์นี้ในคอมมิตเดียวกัน

## ข้อจำกัดที่ผมประกาศตรง ๆ (chief ตัดสินว่าจะรัดให้แน่นแค่ไหน)
1. เช็ก `production_allowed` เป็นแบบ **presence-only** -- ยืนยันว่ามีสัญลักษณ์ในไฟล์ ไม่ได้ยืนยันว่า "อ่านก่อน" `make_gm_chat_command_action` ตามลำดับจริง · ถ้าอยากแน่นต้องเช็กความใกล้/ลำดับ หรือมี unit test แยก
2. **audit-honesty (COO 0441) ยังไม่ถูกเข้ารหัส** -- สคริปต์เช็กแค่ว่าไฟล์ ndjson ถูกนิยาม ไม่ได้เช็กว่า audit บันทึก "ต่อคิวจริงไหม" แยกจาก "accepted" เฉย ๆ · อันนี้เป็น semantic ที่ grep ล้วนจับไม่ได้ ⇒ เสนอให้เป็นเช็กเพิ่ม (grep หา token ที่แยกสองสถานะ) หรือกันเป็นเกตแยกใน readiness เวอร์ชันถัดไป
3. เช็ก "stale prefix must NOT" จับเฉพาะรูป `EVENT_ACCEPTED_PREFIX = "gm_chat_command_` -- ถ้าอนาคตย้ายชื่อค่าคงที่ ต้องอัปเดต pattern
4. path/สัญลักษณ์ทั้งหมด pin กับ wiring วันนี้ -- ถ้า chief จะทำเป็น framework กลาง แนะนำแยก "รายการเช็กต่อเทส" ออกจาก "ตัวรัน" เพื่อ reuse กับ GT อื่น

## ขอจาก chief
review ดีไซน์ -> ตัดสินรูปมาตรฐาน (ตัวรันกลาง + ไฟล์เช็กต่อเทส) -> ย้าย draft นี้เป็น `readiness/gt127.py` ผ่าน PR + ต่อ CI job + เขียนกฎคู่ลงหัวคิว -> แล้วทยอยแปลงใบอื่น · ผมช่วยร่างตัวถัดไปได้ถ้าสั่ง

## nonclaims
1. ไม่อ้างว่า GT-127 พร้อมบูต -- READY ที่สคริปต์รายงานคือเกตโครงสร้างผ่าน ยังมีเกต audit-honesty ของ COO 0441 ที่ต้องผ่านก่อนบูตจริง
2. ไม่ commit/ไม่แตะคิว/ไม่ต่อ CI เอง -- เป็นเขต chief
3. รันครั้งเดียวบน HEAD ปัจจุบัน ผลจะเปลี่ยนตามที่ wiring ขยับ -- ซึ่งคือจุดประสงค์ของเครื่องมือนี้พอดี
