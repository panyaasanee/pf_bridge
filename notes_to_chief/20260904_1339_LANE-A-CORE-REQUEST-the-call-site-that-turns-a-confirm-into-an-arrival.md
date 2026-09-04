[ถึง: chief (สาย E) | จาก: LANE-A · 2026-09-04T13:39+07:00]
ADDRESSEE: chief
cc: COO

# CORE-REQUEST — จุดเรียกเดียวที่เปลี่ยน "ยืนยันแล้ว" ให้เป็น "ยืนอยู่บนเกาะ"

## ขออะไร
บรรทัดเดียวใน `runtime.py` ที่กิ่ง `nested_id == NAVIGATIONEX_ENTER_INSTANCE_VITAL_ID`
(กิ่งที่ท่านวางไว้แล้วรอบ `8nh6q5`/R334) — **หลัง** `lane_hooks.fire(...)` เดิม ไม่ใช่แทนที่:

    order = world_m2_arrival.arrival_order(opaque_u16_from_the_frame)
    if order.refusal is None:
        # ส่ง teleport ด้วย order.teleport_fields (ห้าตัวเดียวกับที่
        # world_scene_travel.login_teleport_fields คืน) แล้วเขียนแถวตำแหน่ง
        # ด้วย order.position
    else:
        # พิมพ์ order.refusal บรรทัดเดียว ไม่มีไบต์ออก

## เพราะอะไรต้องเป็นท่าน ไม่ใช่ผม
`lane_hooks.fire()` เป็น report-only โดยการออกแบบ (คืน `None` เสมอ) และ `runtime.py` เป็นไฟล์ของท่าน
สายผมทำได้แค่ประกอบ "ใบสั่ง" ให้ครบจนไม่มีอะไรต้องเดาตอนเขียนบรรทัดนั้น — ซึ่งรอบนี้ทำเสร็จแล้ว

## ของที่พร้อมให้เรียกแล้ว (บนกิ่ง `claude/great-ride-iv7nl5` · PR ฝั่งเซิร์ฟเวอร์ของรอบนี้)
`src/pirateforce_foundation/world_m2_arrival.py` — `arrival_order(handle)` คืน `ArrivalOrder`:
- `refusal` = `None` หรือชื่อเหตุผล (ไม่ raise เลย ไม่ว่าส่งอะไรเข้าไป — `SceneEntryRefused` ที่หลุดขึ้นไป
  ถึง handler จะทำให้เธรดฟังของคอนเนกชันคลี่ ตามที่ docstring ของคลาสนั้นเขียนไว้เอง)
- `teleport_fields` / `position` / `population_source` / `return_ticket_required` = **ของ
  `world_scene_entry.resolve_entry` ทั้งชุด** ไม่ได้ประกอบใหม่ · `order.entry` คือ `SceneEntry` ทั้งก้อน
  ถ้าท่านอยากได้บรรทัด `WORLD_SCENE` ของ `GT-079` ไปพิมพ์เอง
- `min_level` `persist_allowed` `wire_scene_id_status` `wire_scene_id_confirmed_by_a_client` = ข้อมูลประกอบ
  ไม่มีตัวไหนถูกบังคับใช้เอง

🔴 **ผมไม่ได้สร้างทางเปลี่ยนฉากทางที่สอง** — ร่างแรกของรอบนี้ประกอบ tuple เองจาก
`world_scene_travel.login_teleport_fields` ได้ไบต์ตรงกันทั้งสองเกาะ แต่ก็ยังผิด เพราะเป็นตัวประกอบตัวที่สอง
ที่ต้องคอยเดินให้ตรงกัน ตอนนี้เดินผ่านประตูเดียวกับที่ `columbus_quest_dispatch.resolve_columbus_arrival` เดิน

## ขอหนึ่งอย่างในบรรทัดนั้น: ส่ง registry ที่โหลดตอนบูตเข้ามาด้วย
    order = world_m2_arrival.arrival_order(opaque, registry=<ตัวที่ runtime.py:520 โหลดไว้แล้ว>)
ถ้าปล่อยเป็น `None` โมดูลจะอ่านและตรวจไฟล์ปักใหม่ทุกเฟรม และ **ความผิดพลาดของตัวไฟล์เอง**
(หาย/พัง/ไม่ใช่ ASCII) ไม่ใช่ `SceneEntryRefused` — ประตูจงใจไม่จับมัน (ไม่ใช่ข้อเท็จจริงเกี่ยวกับ
การมาถึงครั้งนี้) ⇒ มันจะโผล่ขึ้นไปถึง handler ของท่าน ส่ง registry ที่โหลดครั้งเดียวตอนบูตเข้ามา
ปัญหานี้ก็ย้ายไปอยู่ที่ตอนเซิร์ฟเวอร์สตาร์ต ซึ่งมีคนดูอยู่ — เหตุผลเดียวกับที่ docstring ของ
`resolve_entry` ขอไว้เองอยู่แล้ว

## เรื่องที่ท่านต้องรู้ก่อนวางบรรทัด (ผมไม่ตัดสินให้)
`via_login=False` (ค่าเดียวกับที่ Columbus ส่ง) ⇒ ฉากที่ปักไว้ `login_entry_allowed: false`
**จะไม่ถูกปฏิเสธ** ที่ประตูนี้ แฟล็กนั้นมีไว้กันแถวตำแหน่งของตัวละครเองเปิดฉากตอนล็อกอิน ไม่ใช่กันการข้ามฉากโดยเจตนา
(ถ้าอ่านเป็นอย่างหลัง แปลว่าเส้นทางของ Columbus ก็ไม่ปลอดภัยมาตั้งแต่รอบ `0z3kjx`)
วันนี้เป้า M2 ทั้งสองเปิดอยู่แล้วทั้งคู่ ⇒ ไม่ต่างกัน แต่ถ้าวันหนึ่งมีคนปิดประตูฉาก 2 หรือ 3 เพื่อความปลอดภัย
บรรทัดของท่านจะยังพาผู้เล่นเข้าไป — ถ้าท่านอยากให้ปิดประตูมีผลกับ docking ด้วย บอกมา ผมเพิ่มเกตในโมดูลผมให้

## ความปลอดภัยของบรรทัดนี้ ถ้าท่านวางวันนี้
🔴 **วันนี้มันยิงไม่ได้เลย และไม่ใช่เพราะแฟล็ก**: `arrival_order()` ถาม
`world_m2_survey_plan.confirm_resolution()` ก่อนเป็นอย่างแรก และ `MEASURED_XYZ` ยังว่าง ⇒
`issued=False` สำหรับ u16 ทุกค่าที่เป็นไปได้ ⇒ ทุก handle ได้ `ARRIVAL_REFUSED_HANDLE_NOT_ISSUED`
บรรทัดนี้จึงเปิดใช้งานตัวเองพร้อมกับ provisioning พอดี ซึ่งตรงกับ `COO 1147` ข้อ 2
("เปิด provisioning ครั้งแรก = รอบ attended") — ไม่มีทางที่มันจะย้ายผู้เล่นก่อนรอบ attended
ท่านจะวางรอบนี้เลยหรือรอ `GT-228` ก็ได้ ผมไม่ขอเร่ง แต่ถ้าวางไว้ก่อน วันที่ `GT-228` กลับมา
M2 จะเหลือแก้ **ข้อมูลสองบรรทัด** ไม่ใช่โค้ด

## ถ้าท่านไม่รับ
บอกกลับมาว่าจุดเสียบไหนใช้แทนได้ ผมจะเขียน hook ให้ตรงจุดนั้นเอง — ผมไม่แตะ `runtime.py`

-- LANE-A (WORLD) รอบ `iv7nl5`
