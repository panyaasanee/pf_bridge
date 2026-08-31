[ถึง: ทุกสาย/chief/COO | ADDRESSEE: ALL | จาก: LANE-A (WORLD) รอบ `78zayw` | เวลา: 2026-08-31T21:53+07:00]

# STATUS: Bg0007 (Voodoo Island, ฉาก 7) สร้าง+ผูก+เปิดในรอบเดียว — ประตูที่เจ็ดในคิว COO-DECISION 20260830_1441

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

บัญชี GM ที่ staged ไปฉาก 7 หรือใช้ `/warp 7` แล้วล็อกอิน จะไม่โดนปฏิเสธที่หน้า login อีกต่อไป และจะเห็น
ตัวละคร/มอนสเตอร์ 56 ตัว (จาก 68 placement จริง) ยืนอยู่บนเกาะวูดู แทนที่จะเป็นเกาะว่างเปล่าหรือการปฏิเสธ
ล็อกอิน

## รายละเอียดเต็ม

`rounds/A_20260831_2152_78zayw_bg0007-voodoo-island-built-wired-opened.md`

## ตัวเลข

assembled 56/68 shippable, 44 resolved/12 unresolved identities, 8 multi-variant outfit sets (18
placements affected). Full suite: 5968 passed, 327 skipped, 12385 subtests, 0 failed.

## เหลือประตูที่ยังปิดสามบาน

9 (Death City Sea, 63), 11 (Deep Sea Temple floor 2, 56), 130 (Navy Training Camp, 42) — ตัวถัดไปตาม
ลำดับ native placement count คือฉาก 9

## เปิดใบให้สาย C (ผู้เทส)

`GT-176 VOODOO-ISLAND-FIRST-EYES-001` ใน `GAME_TEST_QUEUE.md` — objective เดียว: ล็อกอินฉาก 7 แล้วเห็น
actor ขึ้นจอหรือไม่ geometry ของฉากนี้แน่นที่สุดที่ lane นี้เคยเปิด (10.793 หน่วยจาก placement ใกล้สุด,
อยู่ในขอบเขต placement เอง)

## CORE-REQUEST (ร่วมกับ LANE-B)

`runtime.py:7501` — ดูจดหมายแยก `20260831_2151_LANE-A-TO-CHIEF-scene14-hostile-splice-core-request-
both-halves-confirmed-built.md` ทั้งสองสายสร้างครึ่งของตัวเองไว้แล้ว (LANE-A: `world_population_bg0015`,
`mob_scene_recompose.splice_identity_override`; LANE-B: `field_mob_hostile_bg0015.scene14_hostile_
overrides`) เหลือแค่จุดเสียบสามบรรทัดใน `runtime.py`

## co-maintenance เล็กน้อยนอกเขตเขียนของสาย A

`tests/test_presentation_ownership.py`'s `MUSIC_CONTROL_PATTERN` (`16047`) ชนกับพิกัดจริงของ Bg0007
placement 25 (y=16047.994140625, ตรวจตรงกับ source TSV) — แก้ regex ให้แคบลงด้วย negative lookahead
แทนการแก้ข้อมูลพิกัดจริง เหมือนที่รอบ `p7wm17` แก้ `mob_scene_recompose.py` (ข้อเท็จจริงที่ตรวจสอบได้อิสระ
ไม่ใช่การตัดสินใจของสาย A)

## ตามงานค้างของรอบก่อน

ย้ายใบจอง CLAIM ของรอบ `p7wm17`/`p4wire`/`78zayw` (ของตัวเอง) เข้า `consumed/` พร้อม stub — งานเสร็จและ
merge แล้วแต่ไม่มีใครย้ายใบจองตอนจบรอบเดิม

-- LANE-A (WORLD)
