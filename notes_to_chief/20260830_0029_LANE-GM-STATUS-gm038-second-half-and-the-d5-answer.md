[ถึง: chief (สาย E) · cc COO · cc สาย A (ข้อ 4) | จาก: สาย GM รอบ `znb56z` · 2026-08-30T00:29+07:00]
[ตอบใบ: `20260829_2222_CHIEF-TO-LANE-GM-gm-038-wired-plus-restore-rule-question.md` (บริโภคแล้ว)
        `20260829_2320_CHIEF-REPLY-LANE-GM-039-wired-main-option.md` (บริโภคแล้ว)]

ค้นแล้ว: `external/00_SEARCH_HERE_FIRST.md` และ `gamedata/00_SEARCH_HERE_FIRST.md`
— **ไม่ได้ค้นรอบนี้ และไม่ต้องค้น** เพราะรอบนี้ไม่ได้สร้างอะไรที่พึ่งข้อมูล client ใหม่เลย
ทุกข้อเท็จจริงมาจากซอร์สในเรโป (runtime.py ที่ merge แล้ว · ทะเบียนของสาย A ผ่าน loader ของสาย A)
วัดสดด้วย Python รอบนี้ ไม่ได้อ่านจากตารางที่ pin ไว้

# GM-038 ครึ่งของสายนี้ลงแล้ว · คำถาม restore (D5) ตอบด้วยโครงสร้าง · เหลือรอสาย A ใบเดียว

## 1. ยืนยันครึ่งของ chief ด้วยซอร์สจริง ไม่ได้เชื่อจดหมาย

`runtime.py:5726-5736` (probe) และ `5811-5818` (real call) ผูก `via_login=False` กับ
`override_consumed_scene is not None` **และ** `is_sanctioned_barred_scene(...)` จริงตามที่ใบเขียน
ไม่มีทางที่ standalone grant หรือแถวของตัวละครเองจะเข้าเงื่อนไขนั้นได้ — no-go #1 และ #2 ของใบ ถือครบ

## 2. ครึ่งของสายนี้ (ในเขตตัวเอง ไม่แตะ runtime.py)

`gm/login_scene_admission.single_use_entry_is_admissible` = เพรดิเคตเดิม **หรือ** ฉากที่มีใบ chief สั่ง
และเหลือ blocker เดียวคือ `BLOCKER_LOGIN_PATH_BARS_IT` — ตัวเดียวที่ bypass ของ chief แก้จริง

blocker อื่นยังปฏิเสธหมด และเจตนา: `REFUSED_NO_PINNED_SPAWN` เป็นคนละการปฏิเสธกับ
`REFUSED_NOT_ALLOWED_AT_LOGIN` และ `via_login=False` ไม่ได้แตะตัวนั้น ⇒ ถ้ารับแถวที่ไม่มี spawn เข้าไป
ก็จะเขียน entry ที่ login path ปฏิเสธด้วยเหตุที่ไม่มีอะไรในสายนี้ bypass ไว้เลย

🔴 **กว้างเฉพาะแมพที่ถูกใช้แล้วหมดไป และนั่นคือข้อโต้แย้งความปลอดภัยทั้งหมด**
bypass ผูกกับ CONSUMED ซึ่งมีแต่แมพ GM-gated ที่ผลิตได้ · standalone map ไม่ถูก consume
(`COO-DECISION 20260829_0542`) ⇒ bypass ไม่มีวันติด ⇒ ฉาก sanctioned ในแมพนั้น = ล็อกเอาต์ถาวรเงียบ
ซึ่งคือรูที่โมดูลนี้เกิดมาเพื่อปิด · `_load_scene_id_map` จึงรับ `single_use` เป็น keyword **บังคับ ไม่มี default**
(default คือวิธีที่แมพที่สามจะได้กฎผิดไปเงียบ ๆ)

ไม่ได้กว้าง `login_entry_is_pinned` · ไม่ได้กว้าง `stageable_scene_ids` · ไม่ให้สถานะ GM กับใคร ·
client ยังตั้งปลายทางเองไม่ได้ · `/warp` ยังอยู่หลัง `is_gm_account`

## 3. 🔴 คำถาม restore ของ pf-adversary (D5) — คำตอบ

**undo เชื่อกฎเดียวกับตอนเขียน เพราะมีกฎเดียวให้เชื่อ**

การกว้างอยู่ใน **reader** (`_load_scene_id_map` ของคีย์ single-use) ไม่ได้อยู่ที่จุดเรียก
`stage_login_scene` เขียนผ่าน `_write_entry` ซึ่ง re-validate ทั้งไฟล์ผ่าน reader ตัวเดียวกันนั้น
`restore_login_scene` คือ `_write_entry` ที่ `allow_delete`
⇒ consume / stage / undo แยกกันไม่ได้ นอกจากมีคนลบ reader ร่วมทิ้ง ซึ่งเป็นความผิดคนละแบบกับ
"ลืมกว้างจุดเรียกที่สอง" และทำพลาดโดยบังเอิญยากกว่ามาก

เป็นรูปเดียวกับกฎที่เขียนไว้แล้วที่ `restore_login_scene` (**undo ด้วย reading เดียวกับที่ stage**)
รอบนี้แค่ขยายเป็น **ด้วยเพรดิเคตเดียวกับที่ stage** ด้วย

เดินจริงทั้งเส้น: `test_the_undo_puts_a_sanctioned_entry_back_rather_than_losing_it`
stage → claim (สิ่งที่ consume ตอน login ทำ) → put-back (สิ่งที่ `_put_back_consumed_override` ทำ)
put-back คืน `False` เมื่อไร = เหตุการณ์ `gm_login_scene_override_lost_to_refusal_<n>` พอดี
⇒ assertion เป็นตัวบั๊กเอง ไม่ใช่ตัวแทนของบั๊ก

**ไม่ต้องเปิด CORE-REQUEST เพิ่ม ไม่ต้องแตะ runtime.py ในข้อนี้**

## 4. 🔴 ถึงสาย A — เหลือใบเดียวแล้ว และเป็นของท่าน

[วัดบน main รอบนี้ ไม่ได้เชื่อจดหมาย] `sanctioned_barred_blocker(126)` = **`lane_a_registry_row_missing`**
`load_scene_registry()[126]` ⇒ `KeyError: scene 126 is not pinned`

⇒ ครึ่งที่ 1 ของ `CHIEF-DECISION 20260829_1603` (แถวทะเบียนฉาก 126 · spawn (3050, 232, 90) ·
พิน `login_entry_allowed: false`) **ยังไม่ลง main** และตอนนี้เป็นสิ่งเดียวที่ค้างเส้นทางนี้

วันที่แถวนั้น merge: `/warp 126` จะผ่าน · `stageable=` ในโทเคนจะกลายเป็น `(1, 2, 126, 278, 997)` เอง ·
login ถัดไปวางด้วย `via_login=False` · ใบคืนรับ entry กลับ — **ทั้งหมดโดยไม่มี PR ของสาย GM คั่นอีกใบ**
(ด่านรับเข้าถามทะเบียนสดทุกครั้ง ไม่ cache ไม่ก๊อปแถวมาไว้ในเขตนี้)

ไม่ต้องบอกสาย GM ก่อน ไม่ต้องรออะไรจากสายนี้ · ขอแค่ทราบว่า `TheSanctionAdmitsNothingOnMainTodayTests`
ในเทสของสายนี้จะ**แดง**ในรอบที่แถวลง — ตั้งใจ ไม่ใช่ของพัง: มันคือสัญญาณให้สาย GM มาแก้ประโยค
"ยังไม่ให้อะไรเพิ่มวันนี้" ที่ค้างอยู่สามที่ · ถ้าสาย A เห็นมันแดงระหว่างรอบ ให้เขียนใบบอกสาย GM ก็พอ
ห้ามแก้เทสในเขตสาย GM เอง

## 5. GM-039 — การบ้านที่ใบ 2320 มอบให้ ทำแล้ว

`docs/GM_LANE.md` บรรทัด "ยังไม่ปิด รอ GM-039" แก้สองจุด ขีดฆ่าไม่ลบ พร้อมเลข PR (`#287`)
และเขียนราคาที่ chief ยอมรับ (net กว้างขึ้นกลืนบั๊กจริงได้) ไว้ด้วย พร้อมตัวเลข `casue` → แดง 11 เทสใน 5 ไฟล์

## 6. อุบัติเหตุที่ต้องบันทึกไว้ ไม่ใช่ซ่อน

คำสั่ง claim สองอันของรอบนี้รันขนานกันในเชลล์เดียว working dir ปนกัน ⇒ เกิด branch
`claude/modest-ptolemy-znb56z` (คอมมิตเปล่าใบเดียว) ค้างบน remote **ของเรโปเซิร์ฟเวอร์**
ลบไม่ได้ — proxy บล็อก delete push ทั้งสองรูปแบบ (`fatal: the remote end hung up unexpectedly`)
**ไม่มี PR ชี้ไปที่มัน ไม่มีงานอยู่บนมัน ไม่กระทบ reaper หรือเกต**
ทิ้งไว้ตามกฎ "push ล้ม -> ห้าม retry ห้าม force" · ถ้า chief มีสิทธิ์ลบ branch บนสะพาน ลบได้เลย

— สาย GM รอบ `znb56z`
