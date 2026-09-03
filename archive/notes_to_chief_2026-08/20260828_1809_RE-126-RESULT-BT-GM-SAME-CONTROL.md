[ถึง: LANE-GM (ผู้เปิดใบ) · chief · COO · cc Panya | จาก: RE runner local · 2026-08-28T18:09+07:00]

# RE-126 RESULT — PASS/DONE · `BT_GM` คือ control เดียวกับที่ handler `0x0053B9B0` รับจริง

- ใบ: `RE-126 BT-GM-CONTROL-OBJECT-IDENTITY-001 [STATIC-ON-BRIDGE]`
- START: `2026-08-28T18:03:49.733+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB/source/queue/git
- verdict: สมมติฐาน “ปุ่มที่ render กับ control ที่ handler จดทะเบียนเป็นคนละ object” **ถูกหักล้าง**. `this` ของ helper คือ notification-list UI object (vtable `0x00F21FA8`); binder ของ object เดียวกัน lookup resource `BT_GM` แล้วเก็บ pointer ที่ `this+0x48`; event dispatcher ของ vtable เดียวกันเทียบ `event.source == this+0x48` ก่อนเรียก helper `0x0053B9B0` ด้วย `this` ตัวเดิม. ข้อ 3 จึง N/A — ไม่ต้องหา handler อื่นเพื่ออธิบาย binding.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอเฉพาะโครง GM module ไม่เจอ control binding.** ค้นทั้ง tree 30 ไฟล์ / 29,900,221 ไบต์ / fingerprint `9525161de1f79fe1c4d73f98c39a7e854c946bd0c30c0686d23f2a9854baa837` ด้วย `BT_GM|GMUI_BASIC|0053B9B0|00AA0710|7280D0|GMModule_Client`; พบ `GMModule_Client` ใน registry/serializer/validation (`NOT_OBSERVED`) แต่ไม่พบ `BT_GM`, handler หรือ event-binding crosswalk. จึงใช้ image จริงต่อ.
- **ค้นใน `pf_bridge\gamedata\` แล้ว: ไม่เจอ.** ค้นทั้ง tree 1,109 ไฟล์ / 15,319,585 ไบต์ / fingerprint `ae16237dbce6c031894e83b4fb0bc0151cdf1f32e52e5d677499eb5ba25ac54d` ด้วย `BT_GM|GMUI_BASIC|GMModule|0053B9B0|00AA0710` ได้ 0 hit. ใบนี้เป็น UI/runtime code concern ไม่มี gamedata crosswalk.

## T0 — input/SHA control และคำตอบเดิมที่ reuse

- image `GameClient.local.bin` SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, ImageBase `0x00400000`
- คำตอบเดิม RE-104 verifier `re104_gm_editor_trigger_static.py` SHA `aee5a2d56c343b68f04285e76d43c2bbbdd3968c5e61ec89cc01480fb59ad95e`; RE-118 verifier SHA `ad3aaa09f972720be029001551279f6e837f35038c003d56db3a2d215a388cb9`
- รัน verifier เดิมทั้งสองซ้ำบน image SHA เดิม: RE-104 PASS, RE-118 PASS. RE-104 มีคำตอบ binding นี้อยู่แล้วแบบ exact-byte; รอบนี้ verify SHA แล้ว reuse และเพิ่ม vtable/constructor crosswalk เพื่อปิดข้อ 1-3 โดยตรง ไม่ถอด state/factory ซ้ำ.
- หลักฐาน attended ใหม่ `20260828_1140_GT103AB-RESULT-NEGATIVE-*.md` SHA `1b070ff650aa29deb9ae3335692702bc6c2cf8b56c8e27702cb8d67f31d38e99` หักล้างเพียง BUILD_IMPACT A/B ของ RE-118; มันไม่เปลี่ยน native binding ที่ตรวจตรงใน image.

## T1 — `this` คือ object ใด และ `+0x48` ถูกเขียนที่ไหน

1. Constructor `[0x0053ACC0,0x0053ACDA)` เรียก base `0x0059D740`, zero byte `+0x50/+0x51`, แล้วเขียน vtable `0x00F21FA8` ลง `[this]` ที่ `0x0053ACD0`.
2. semantic identity ที่ตั้งชื่อได้โดยไม่เดา class symbol คือ **notification-list UI object**: binder เดียวกันผูก `PANEL_NOTIFYLIST_NORMAL`, `PANEL_NOTIFYLIST_HIDE`, `BT_IMPORTANT`, `BT_SOCIAL`, `BT_MAIL`, `BT_TEACH`, `BT_LEVELUP` และ `BT_GM`. binary ไม่มี symbol ที่อนุญาตให้ตั้งชื่อ C++ class มากกว่านี้.
3. binder vtable slot `0x00F21FA8+0x60 -> 0x0053ADE0`. ที่ `0x0053B08B` มัน push UTF-16 resource `BT_GM` (`0x00F2207C`) แล้วเรียก resource lookup `0x00AA1750`; ผลถูก type-check และ pointer เดิมถูกเขียน `mov [esi+0x48],eax` ที่ `0x0053B0CB`.

ดังนั้น write site ที่ใบถามคือ **`0x0053B0CB` ภายใน binder `0x0053ADE0`**, ไม่ใช่ ctor โดยตรง; ctor สร้าง object/vtable ส่วน binder เป็นคน resolve control จาก layout แล้วเติม `+0x48`.

## T2/T3 — ปุ่มผูกกับ handler นี้จริงหรือไม่

- vtable เดียวกัน slot `+0x28 -> 0x0053BCA0` คือ event dispatcher. มันรักษา `this` ใน `ESI`, อ่าน `event.source` จาก `[EDI]`, แล้วที่ `0x0053BCEF` เทียบ pointer นั้นกับ `[ESI+0x48]`.
- ถ้า source ตรงและ event code `[EDI+8]` ตรง click global `[0x01090DC0]`, dispatcher push event args, ตั้ง `ECX=ESI` แล้ว call `0x0053B9B0` ที่ `0x0053BD0A`.
- helper branch ที่ `0x0053BC51` เทียบ source กับ `[this+0x48]` ซ้ำอีกครั้งก่อน connection/query/current-key gates.
- นี่เป็น field/data-flow crosswalk: **resource `BT_GM` -> lookup result -> same-object `+0x48` -> same-object vtable dispatcher -> helper**. ไม่ได้จับคู่เพราะชื่อ/id เท่ากัน.
- ข้อ 3 (“ถ้าไม่ใช่ตัวเดียวกัน ให้หา handler จริง”) = **N/A เพราะข้อ 2 ตอบว่าเป็นตัวเดียวกัน**. รอบนี้ไม่อ้างว่าไม่มี indirect/hotkey entry อื่นทั่วทั้ง image; เพียงแต่ไม่ต้องใช้ entry อื่นเพื่อปิด identity objective.

## T4/T5 — ขอบเขตของคำตอบ

- ผลนี้หักล้าง candidate สาเหตุที่ใบเปิดว่า source binding ผิดตัว. มัน **ไม่** อธิบายว่ารอบ GT-103 A/B หยุดที่ connection context, query gate, current-UI object/key หรือ create path ใด; การหา runtime failure หลัง binding เป็น objective ใหม่/การ instrument คนละใบ ไม่ควรยัดเข้าข้อ identity นี้.
- ทางแชท `0xAC52` ที่ LANE-GM เปิดแล้วเป็น alternate GM-command transport แต่ **ไม่ใช่ alternate entry เข้า `GMUI_BASIC`**; อย่าใช้มันอ้างว่า factory/UI path ทำงาน.

## verifier / reproducibility

- `pf_bridge\staged\re126_bt_gm_control_identity_static.py` SHA-256 `347525023b4c3fcb5cf3cb04b99ac891b962af9e193066f317d947ba2dea2596`
- รัน `python -B` อิสระ 2 ครั้ง: PASS `18` checks / `3` pinned spans ทั้งคู่, exit `0/0`
- pin image + RE-104/118 verifier SHAs, constructor/vtable slots, named resources, exact BT_GM lookup/type-check/store bytes, event-source crosswalk และ helper gate

## nonclaims

1. ไม่ claim formal C++ class name; ใช้ชื่อ bounded “notification-list UI object” จาก resource set + exact vtable เท่านั้น.
2. ไม่ claim ว่า `this+0x48` เป็นสาเหตุ runtime failure — มันถูกผูกถูกตัวตาม image; ค่ารันไทม์ของ pointer ไม่ได้ capture ในใบ static นี้.
3. ไม่ claim ว่า current-UI key ว่าง/ไม่ว่าง หรือ connection context null ใน GT-103; attended วัดหน้าจอ/packet ไม่ได้วัด native pointer.
4. ไม่ claim ว่าไม่มี hotkey/indirect entry อื่นทั่ว image; objective 3 เป็น conditional และ binding positive ทำให้ไม่ต้องใช้ negative แบบนั้น.
5. ไม่ claim ว่า chat `0xAC52` เปิด `GMUI_BASIC`; มันเป็นคนละ transport/path.

## BUILD_IMPACT

**BUILD_IMPACT:** ปรับหัว/ขั้นต่อของ GT-103 ว่า `BT_GM` binding ถูกพิสูจน์แล้ว (`resource -> this+0x48 -> event dispatcher -> 0x0053B9B0`); ห้ามวน A/B panel เดิมหรือเปิดใบหา “handler คนละตัว” ซ้ำ. ถ้ายังต้องการ GMUI ให้ objective ถัดไป instrument/พิสูจน์ค่ารันไทม์หลัง source-match (connection context/query/current-key/create-null) ทีละ gate. ทางวิกฤตของ GM command ใช้ chat `0xAC52` ต่อได้แยกจาก GMUI ตามแผน LANE-GM.

สถานะที่ควรกรอก: `RE-126 PASS/DONE — BT_GM-SAME-CONTROL; SOURCE-BINDING-CANDIDATE-FALSIFIED`.
