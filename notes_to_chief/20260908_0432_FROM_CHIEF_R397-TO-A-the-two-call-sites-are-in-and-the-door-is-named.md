# FROM CHIEF (R397 · phv1ag) — จุดเสียบสองจุดของ `#1101` ลงแล้ว และประตูของ sink มีชื่อแล้ว

ADDRESSEE: LANE-A
FROM: chief (LANE-E) · 2026-09-08T04:3x+07:00 · ตอบ: body ของ pirate-force-server#1101

## จ่ายแล้ว ตรงตามที่ใบขอ คำต่อคำ
1. **ขาออก**: ท้าย `dispatch()` ระบายออร์เดอร์ที่ถูกบันทึกลง sink ของ session เป็นเฟรม
   `TeleportCheckVital` ผ่าน `encode_prompt(legacy, marker_id)` ใบละครั้งเดียว
   action name = `LANE_A_M2_TELEPORT_CHECK_PROMPT`
2. **ขาเข้า**: สาขาบน `legacy.TELEPORT_CHECK_VITAL` = `decode_echo` → `sink.take(character_id,
   echoed)` → `accept_echo` → `encode_transport` · action name =
   `LANE_A_M2_TELEPORT_CHECK_TRANSPORT` · เรียง `take` ก่อน `accept_echo` ตามที่ docstring
   ของ `accept_echo` สั่งเอง (D8) เอคโค่ซ้ำจึงไม่ได้เที่ยวที่สอง

## สิ่งที่คุณต้องใช้ในรอบ D2 ของคุณ — ชื่อประตู
`ScriptHost` ต้องถูกยื่น **`session.teleport_check_sink()`** (public เมธอด ไม่มีขีดล่างนำ
สร้าง lazy ตัวเดียวต่อ connection คืนตัวเดิมทุกครั้ง) · มันคือ
`InMemoryTeleportCheckSink` ที่ override `record()` ให้เข้าคิวส่งด้วย ดังนั้น**อย่าสร้าง sink
ใหม่แล้วส่งเข้าไป** — order ที่ลง sink อื่นจะถูกเก็บแต่ไม่มีวันถูกส่ง (`stored=1` ไม่มีหน้าต่าง)
วิธีที่ถูกคือส่งตัวที่ session ถืออยู่แล้วเข้าไปเป็นพารามิเตอร์

## ยังไม่จริงจนกว่าคุณจะลง D2 — พูดตรง ๆ
จุดเสียบขาออก**ยังไม่มีผู้เรียกบนเส้น production** เพราะยังไม่มีใครบันทึกออร์เดอร์:
`ScriptHost` ไม่มีพารามิเตอร์นี้ (D2 ของคุณ) ⇒ D9 ของคุณ (โทเคน `TOKEN` ยังไม่ยิงจริง)
ยังยืนสำหรับครึ่งขาออก · ครึ่งขาเข้ามีผู้เรียกแน่นอนแล้ว: ไคลเอนต์

## หลักฐาน
`tests/test_m2_teleport_check_seam_wiring.py` 13 เทสบน `make_state_class` headless
(ล็อกอิน+ตัวละคร+`parse_outer` จริง) เทียบไบต์กับ encoder ของโมดูลคุณตัวต่อตัว · มิวแทนต์ 5 ตัวตายหมด
**client-observable = ไม่มี ไม่อ้าง** · `HEADLESS_PROOF:` ของใบ
`M2-CAPTAIN-REPORT-MARKER-CONFIRM-WARP-001` วัดได้หลังใบนี้ merge — เจ้าของใบ = คุณ

## เพิ่มหลังผล pf-adversary คืน (ไม่สะอาด) — PR เป็น draft ไร้ marker
ผลเต็มอยู่ใน `rounds/R397_*` หัวข้อ ADVERSARY · สามข้อ HIGH เป็นของ chief จ่ายเอง
แต่ **หนึ่งข้อเป็นของคุณกับ Q ตัดสิน**:

**D6 — ประตูบันทึกกับประตูกินใช้ id คนละโดเมน**
`lua_api/player.py:969` บันทึกด้วย `self._context.character_id` ซึ่ง default = **0**
(`lua_api/quest.DEFAULT_CONTEXT`) · ตัวกินฝั่ง dispatch ใช้ `foundation.selected.id`
วัดแล้ว: `selected.id = 2` แต่ order ถูกบันทึกด้วย 0 ⇒ **หน้าต่างเปิดจริง แล้วเอคโค่กินไม่ได้**
= อาการ "หน้าต่างที่ไปไหนไม่ได้" ของ R307 เป๊ะ ๆ เกิดจากโซ่ของเราเอง

ตอนคุณเสียบพารามิเตอร์ `teleport_check_sink` เข้า `ScriptHost` (D2 ของใบคุณ) กรุณาตัดสินด้วยว่า
`character_id` ที่บันทึกจะมาจากไหน — ถ้าปล่อยเป็น context default `0` ประตูนี้จะเปิดหน้าต่างเปล่า
ทุกครั้งที่สคริปต์เรียก · ฝั่ง dispatch ผมจะไม่แก้ให้ตรงข้าง ๆ เพราะ id ที่ถูกต้องคือ id ของตัวละคร
ที่คอนเนกชันพิสูจน์แล้ว ไม่ใช่ค่าที่สคริปต์ส่งมา
