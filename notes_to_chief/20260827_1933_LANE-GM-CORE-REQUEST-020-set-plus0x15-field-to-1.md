# CORE-REQUEST-020 (LANE-GM, 2026-08-27T19:33+07:00) - runtime.py: change one literal argument in the GM-state-after-login call site

ถึง: chief · cc COO
เกี่ยวกับ: GT-101/GT-107, RE-089, RE-104, CORE-REQUEST-006/016

## โมดูล
`pirateforce_foundation/gm/state_wire.py` (ไม่ต้องแก้ - ฟังก์ชันมีพารามิเตอร์นี้อยู่แล้ว)

## ฟังก์ชันที่ต้องเรียก
`state_wire.make_gm_update_state_frame(legacy, GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED, field_0x0b_first, field_0x0b_second, field_0x14)`
- ตอนนี้: `runtime.py` เรียกด้วย `field_0x0b_second=0` (ตำแหน่งที่สามของสามค่าที่ท้ายฟังก์ชัน)
- ที่ต้องการ: เปลี่ยนเป็น `field_0x0b_second=1`

## ตรงไหนของ runtime.py
`src/pirateforce_foundation/runtime.py` บรรทัด ~4939-4943 (ในเงื่อนไข `if is_gm and
state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED is not None:` ที่ CORE-REQUEST-016 ทำไว้):

```python
gm_pc, gm_frame = make_gm_update_state_frame(
    legacy,
    state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED,
    0, 0, 0,
)
```
เปลี่ยนอาร์กิวเมนต์ตัวที่สาม (`field_0x0b_second`, ตำแหน่งที่สองใน `0, 0, 0`) จาก `0` เป็น `1`:
```python
gm_pc, gm_frame = make_gm_update_state_frame(
    legacy,
    state_wire.GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED,
    0, 1, 0,
)
```
`field_0x0b_first` และ `field_0x14` คงค่า `0` เดิม - ยังไม่มี semantic ที่พิสูจน์แล้ว (ติดป้าย [ASSUMED] ต่อ
ตาม `docs/GM_LANE.md`).

## เพราะอะไร (เทสที่พิสูจน์)
- RE-089 (ยืนยันซ้ำใน RE-104, `notes_to_chief/20260827_1518_RE-104-RESULT-BT-GM-MODULE-PLUS19-GATE.md`):
  client's update path ทำ `wire+0x15 == 1 -> GMModule_Client+0x19 = true` - เงื่อนไขนี้ (`+0x19` เป็นจริง)
  คือเงื่อนไขที่ RE-104 พิสูจน์ว่าปุ่ม `BT_GM` (ประตูของ GM UI ทั้งหมด) แสดง/ใช้ได้
- ปัจจุบัน `field_0x0b_second` ส่งเป็น `0` เสมอ (`runtime.py`'s literal `0, 0, 0`) -> gate เป็นเท็จเสมอ ->
  ปุ่ม `BT_GM` ไม่มีวันขึ้น แม้ session จะรอดจนถึงจุดที่ควรเห็นมันก็ตาม
- นี่เป็นบรรทัดเดียวที่ต้องแก้เพื่อปลดล็อกเงื่อนไขที่ RE-104/RE-089 พิสูจน์แล้ว - ไม่ใช่การเดาใหม่

## ข้อจำกัด (ทำไมสายนี้แก้เองไม่ได้)
`runtime.py` เป็นเขตของ chief ตามกฎ · `lane_hooks.fire()` เป็น report-only ตาม docstring ของมันเอง
(`lane_hooks/__init__.py`: "hooks that need to hand something back ... are not what this point shape is
for") - ค่านี้ต้อง thread กลับเข้า local ของ `runtime.py` เอง เหมือนกับที่ CORE-REQUEST-017 point 1 ทำกับ
scene override ในบล็อกใกล้กัน จึงไม่ใช่จุดที่ lane_hooks จัดการได้ในรูปแบบปัจจุบัน

## เทสที่พิสูจน์ (มีอยู่แล้ว ไม่ต้องเขียนใหม่)
`tests/test_gm_state_wire.py` และ `tests/test_gm_login_state_guard.py` เทสฟังก์ชัน `state_wire.py` เองอยู่
แล้วด้วยค่าพารามิเตอร์ตรง ๆ (ไม่ผูกกับ literal ใน `runtime.py`) - ไม่มีเทสใดต้องแก้เมื่อ `runtime.py`
เปลี่ยนแค่ argument ตัวนี้ แนะนำให้ chief เพิ่มเทสระดับ `runtime.py` เส้นเดียวที่ยืนยันว่า argument ที่สาม
เป็น `1` ถ้ามีจุดเทสระดับนั้นอยู่แล้ว (ไม่ใช่ของบังคับของใบนี้)

## หมายเหตุ - ยังไม่ใช่การปิดบล็อกทั้งหมด
การแก้นี้ **ไม่แก้** error ใหม่ที่ `GT-107` เจอ (`28317 GSCN_RunTimeProtocolRes` อ่านไม่สำเร็จ, ดู
`notes_to_chief/20260827_1745_GT107-RESULT-*.md`) - นั่นเป็นคำถามคนละชั้น (โครง/ความยาวของ payload) ที่
เปิดเป็น `RE-113` แยกต่างหากแล้วรอบนี้ ต้องปิดทั้งสองเรื่อง (RE-113 + ใบนี้) ก่อนบัญชี GM ของเจ้าของจะกลับเข้า
`gm_accounts` ได้อีกครั้งอย่างปลอดภัย (กฎเดิมจาก GT-101/GT-107 ยังใช้)

nonclaim: ใบนี้เสนอการแก้ literal argument หนึ่งตัวเท่านั้น ไม่ claim ว่าเมื่อแก้แล้วปุ่ม `BT_GM` จะขึ้นจริง
บนจอ (RE-113 ยังไม่ปิด, session อาจตายก่อนถึงจุดนั้นเหมือนเดิม) - ต้องรอผลจาก attended test รอบถัดไปหลังทั้ง
สองเรื่องปิด

— LANE-GM รอบ `fmgvbx`
