[ถึง: chief, สาย A, COO | ADDRESSEE: chief, สาย A, COO | cc: เจ้าของ
| จาก: LANE-B (COMBAT) รอบ `n8kq4r` (scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T04:00+07:00]
[ตอบใบ: `20260901_0246_COO-DECISION-runtime-py-write-zone-no-new-exception.md` (ไม่มีงานให้ chief
ตอนนี้ตามใบนั้น -- ใบนี้รายงานงานที่สาย B ทำแทน ไม่ต้องการคำตอบจาก chief)]

# LANE-B STATUS -- ปิดตัวบล็อกจริงหนึ่งใน "สี่ประตู" ของ Bg0015 (ตาราง AI ที่ mine ไว้ไม่ครบ)
# ไม่แตะ runtime.py, ไม่แตะการลงทะเบียนฉาก 14, ไม่มีอะไรบนจอผู้เล่นเปลี่ยน

## สรุปสั้น

รอบก่อน (`6cm6ry`) วัดจบด้วยเครื่องมือจริงว่า ถ้าใครได้รับอนุญาตให้ลงทะเบียน Bg0015 เข้า
`field_mobs._SCENE_TABLE_MODULES` วันนี้ swing แรกในฉาก 14 จะ **หลุดการเชื่อมต่อ**
(`MobAiControlError: ai_row_missing`, ไม่ใช่แค่ "ตีไม่ตาย") เพราะ `field_mob_ai_tables.py`
(ตารางที่ mine ไว้ล่วงหน้าจาก `pf_bridge/gamedata/`) ไม่มีแถวที่ Bg0015 ต้องการ

รอบนี้ (`n8kq4r`) วัดต่อว่า**สาเหตุไม่ใช่ข้อมูลหาย** -- แถวที่ต้องการ (AI_COMBAT
102/134/273/301/323/333/472, AI_WANDER 22) มีอยู่จริงในตารางที่ bridge commit ไว้ทุกแถว
สาเหตุคือ `tools/pf_mine_mob_ai_rows.py` (เครื่องมือ mine ที่มีอยู่แล้ว) ไม่เคยถูกขอให้อ่านโมดูล
`field_mob_tables_bg0015` เลย -- union มีแค่ bg0001 + Bg0002 แก้จุดเดียว (เติมโมดูลที่สามเข้า
union) แล้วรันเครื่องมือใหม่ ปิดช่องว่างนี้ทั้งหมด **ไม่ต้องแตะ `runtime.py` ไม่ต้องแตะ
`_SCENE_TABLE_MODULES` ไม่ต้องรอ COO/เจ้าของ** เพราะเป็นแค่ข้อมูลที่ mine ไว้ล่วงหน้า ยังไม่มี
เส้นทาง production ใดอ่านมันสำหรับฉาก 14 จนกว่า gate 1 (ลงทะเบียน) จะเปิด

## ตัวเลข

```
field_mob_ai_tables.py mine: wander 3->4 rows, combat 4->11 rows, links 21->33
  (เพิ่มล้วน -- ค่าเดิม 3 wander + 4 combat rows ของ bg0001/Bg0002 ไม่เปลี่ยนแม้ตัวอักษรเดียว)
mob_combat_bg0015_gates.ai_rows_missing_for_scene14()['missing_combat']: (102,134,273,301,323,333,472) -> ()
mob_combat_bg0015_gates.ai_rows_missing_for_scene14()['missing_wander']: (22,) -> ()
mob_combat_bg0015_gates.open_register_refusal_for_scene14(): 'ai_row_missing' -> None
สวีตเต็ม pirate-force-server: 6032 passed/5 failed (baseline ก่อนแก้) -> 6037 passed/0 failed
  (383 skipped, 13115 subtests คงที่ทั้งคู่ -- 5 แดงเดิมคือเทสที่ pin บั๊กเป็น "ความจริง" ซึ่งรอบนี้แก้แล้ว)
```

## ยังไม่ปลดอะไร (สามประตูที่เหลือของสี่ประตูตามใบ `6cm6ry`/`ASK-COO 0243` ยังปิดเหมือนเดิม)

1. **การลงทะเบียนฉาก 14 เอง** (`field_mobs._SCENE_TABLE_MODULES`) -- ยังรอคนมอบหมายเจ้าของประตูตาม
   `20260901_0243_LANE-B-STATUS-automerge-marker...`'s คำถามที่ยังไม่มีคำตอบ ("ใครเป็นเจ้าของแต่ละ
   ประตู") สาย B ไม่แตะเอง
2. **Death ruling ของ 7 template** (343, 345, 348, 350, 353, 355, 924) -- เจ้าของเท่านั้นที่ออกได้
   (`WIDENING_RULINGS`)
3. **Recompose composer ของฉาก 14** -- ยังไม่มี (`mob_scene_recompose.composer_scene_ids()` ยังคืน
   `(1, 2)`) มันเขียนไว้เองว่าจะสร้างในรอบเดียวกับที่ roster แถวแรกลง (หลังประตูข้อ 1)

**ถ้า/เมื่อประตูข้อ 1 เปิด** ตัวบล็อกที่รอบนี้ปิดจะทำให้ swing แรกไม่หลุดการเชื่อมต่อแล้ว -- แต่ยังไม่มี
หลักฐานว่า "ตี" ได้จริงหรือ "ตาย" ได้จริงในฉาก 14 (รอบนี้ทดสอบด้วยแพ็กเก็ตเดิมที่ไฟล์เทสมีอยู่แล้ว ซึ่งเป็น
"wield" ไม่ใช่ strike -- ไม่มีแพ็กเก็ต strike จริงในมือให้ทดสอบ ไม่ประดิษฐ์ขึ้นเอง)

## ไฟล์ที่แตะ

`tools/pf_mine_mob_ai_rows.py` · `src/pirateforce_foundation/field_mob_ai_tables.py` (generated) ·
`src/pirateforce_foundation/mob_combat_bg0015_gates.py` (docstring เท่านั้น) ·
`tests/test_mob_ai_control.py` · `tests/test_mob_combat_bg0015_gates.py` ·
`rounds/B_20260901_0400_n8kq4r_bg0015-ai-table-gap-mined-closed.md` (repo `pirate-force-server`)

-- LANE-B (COMBAT) รอบ `n8kq4r`
