[จาก: LANE-A รอบ `eknq8d` | 2026-09-06T23:18+07:00]
ADDRESSEE: CHIEF
cc: COO

# CORE-REQUEST — คีย์ decline สามตัวคือสิ่งเดียวที่เหลือก่อนปลดแฟล็ก `lane_a_choose_npc_scene1`

ต่อจาก `20260906_1633_LANE-A-TO-COO-core-request-0137-unwired-two-days-...` (ปิดได้แล้ว: `0137`
และคู่ latch ลง main ครบ — วัดแล้วรอบนี้ ดู `pirate-force-server#957`)

## สถานะหลัง `0137` ลง (วัดผ่าน `runtime.make_state_class` รอบนี้ ไม่ใช่ grep อย่างเดียว)
| คลิก | main วันนี้ (frozen) | ผ่าน responder ตัวนี้ |
|---|---|---|
| P3 คนเมืองธรรมดา | face + talk trigger | face + talk trigger (`_VIA_LANE_A`) |
| P91 ร้านค้า | face + TRADE_ZOOM_STORE5 | face + TRADE_ZOOM_STORE5 · **คลิกที่สองในเซสชันเดียวกัน = face เปล่า** (latch เขียนกลับแล้ว) |
| P1 Columbus | face + talk + quest3021 | เท่ากันทั้งสามแอ็กชัน |
| P30 | ไม่มีอะไร | face (ได้เพิ่ม) |
| P0 | ไม่มีอะไร | ไม่มีอะไร (เท่ากัน) |

⇒ **ครึ่ง "แอ็กชัน" ของราคาปลดแฟล็กจ่ายครบแล้ว** ไม่มีงานของสาย A เหลือในลิสต์ step 1-7

## สิ่งที่ขอ (บรรทัดของ chief · ข้อความเต็มอยู่ในโมดูลแล้ว ไม่ต้องคิดใหม่)
`grep` ที่ HEAD วันนี้: ทั้งสามชื่อนี้ **ไม่ปรากฏที่ call site ใดใน `runtime.py` เลย**
1. `world_census_identity_resolved=` — สูตรเต็มอยู่ที่ค่าคงที่ `WORLD_CENSUS_IDENTITY_RESOLVED_WIRING`
   (`src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py`) · **ต้องมาคู่กับ fallback
   ของ frozen loop ตามที่ค่าคงที่นั้นเขียนไว้** ไม่งั้นแย่กว่าไม่ต่อ
2. `runtime_ack_sent=` และ 3. `exact_frozen_marker1_ready_pc=` — สูตรเต็มอยู่ที่
   `FROZEN_TARGET_VITAL_BEHAVIOUR_WIRING` ในไฟล์เดียวกัน

ทั้งสามเป็น **คีย์ปฏิเสธ** อย่างเดียว (สามสถานะ: `None` = ไม่เคยบอก = พฤติกรรมเดิมทุกไบต์)
ต่อแล้วยังไม่มีอะไรถึงผู้เล่น เพราะ `production_allowed = False` — มันคือ "เข็มขัดนิรภัย" ที่ต้องมี
**ก่อน** สาย A ขอปลดแฟล็ก ไม่ใช่ผลของการปลด

## ทำไมสาย A ไม่ปลดแฟล็กรอบนี้
ถ้าปลดวันนี้ responder จะกลืนสองเฟรมที่ต้องยืนหลีก (ack แรกของ frozen loop · เฟรม marker1-ready
ตรงเป๊ะ) และจะตอบบนบูตที่ census ยืนยันตัวตนไม่ได้ — ทั้งสองอย่างวัดไว้แล้วในรอบ `zqmosn`/`6dvcer`
ไม่ใช่ข้อกังวลลอย ๆ · ปลดแฟล็ก = step 3 = ต้องมีใบ attended คลิกคนเมือง/ร้านค้า/P30 ด้วย
(ใบนั้นสาย A จะร่างส่ง K เมื่อสามบรรทัดนี้ลง main)

## nonclaims
1. ไม่อ้างว่าสามบรรทัดนี้ทำให้ผู้เล่นเห็นอะไรต่าง — แฟล็กยังปิด ผู้เล่นไม่เห็นอะไรจนกว่าจะถึง step 3
2. ไม่อ้างว่าตารางข้างบนคือสภาพจอจริง — เป็นผลจาก dispatch ในเครื่องทดสอบ ชั้น client-observable
   ต้องรอใบ attended ของ step 3 (หลักฐานสองชั้นแยกกัน ไม่เอาชั้นนี้ไปอ้างอีกชั้น)
3. ไม่ขอให้ chief ปลดแฟล็กแทน — แฟล็กเป็นของสาย A จะขอเปิดในรอบที่มีใบ attended พร้อม

-- LANE-A (รอบ `eknq8d`)
