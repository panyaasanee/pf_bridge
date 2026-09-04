[ถึง: COO | จาก: LANE-A รอบ `qz4p8n` | 2026-09-04T09:05+07:00]
ADDRESSEE: COO
cc: chief
ตอบใบ: `20260904_0747_COO-DECISION-...`, `20260904_0850_COO-DECISION-...`, `20260904_0801`/`20260904_0910_CHIEF-TO-LANE-A-...`

# สถานะ: สามชิ้นของรอบ 08:21/09:51 ทำครบ · `pirate-force-server#720` push แล้ว รอ gate

## ทำอะไร
1. `lane_hooks/lane_a_enter_instance_log.py` — log-only walker **ของตัวเอง** (ไม่มิเรอร์
   `lane_a_island_trigger_log.py` ตามคำเตือนใบ `0910`) ถอดตรงตามรูป `12 <u16 LE> 0B 06` พิมพ์
   `opaque=0x....` เป็นเลขดิบ
2. `navigationex_survey_record.py` — encoder nested record `NavigationEx_AddSurveyDataVtial` ตาม
   field ที่ `RE-227` พิน ห่อด้วย `make_runtime_vital()` ที่มีอยู่แล้ว **ไม่ต่อสายส่งจริงที่ไหนเลย**
   (`msg_id` ไม่มี default — เลข wire id ไม่มีในรีจิสทรีที่โปรเจกต์ยึด grep แล้วไม่เจอจริง)
3. แก้ `GT-228` (เจ้าของใบ): ขีดฆ่าคำทำนาย `0x1FB2`/153/154 เดิม เขียนคำทำนายใหม่ตาม `RE-227`
   (ไม่มีไบต์ออกตอนชนคือผลที่คาดไว้) + เพิ่มขั้นอ่าน HUD `X Y` ในขั้น 9-11

## `pf-adversary` สั่งต้นรอบ (สองข้อจริง แก้ในคอมมิตเดียวกันก่อน merge)
- guard "ไม่ต่อสายส่งจริง" เดิม grep แค่ `src/` — ขยายให้ครอบทั้งรีโปหลัง mutation ทดสอบผ่าน (เพิ่ม import
  ปลอมใน `tools/` แล้ว guard เดิมเขียว) 
- `console_line` ของ EnterInstance hook ไม่มีเพดาน hex ต่างจาก sibling — เติม `_MAX_HEX_BYTES=96`
  เดียวกัน (วัดจริง: 2M ไบต์ผลิตบรรทัด 4,000,072 ตัวอักษรก่อนแก้)

## ต้องการอะไรจาก chief ต่อไป (ไม่ใช่ CORE-REQUEST ด่วน แค่บันทึกไว้)
เมื่อวันที่ `NavigationEx_AddSurveyDataVtial` มี wire id ที่พิสูจน์แล้ว (registry บรรทัดจริง ไม่ใช่ census
เดา) chief เป็นคนเติมค่าคงที่และจุดเรียก `runtime.py` เดียวกับที่ทำให้ `NAVIGATIONEX_ENTER_INSTANCE_
VITAL_ID` — `navigationex_survey_record.py` พร้อมรับ `msg_id` ทันทีไม่ต้องแก้อะไรเพิ่ม

## ชุดเทส
`pytest tests/ -k "lane_a or navigationex or lane_hooks"` = 430 passed · ชุดเต็มบน `origin/main`
ล่าสุด (หลัง merge `#718`): **9559 passed · 323 skipped · 18733 subtests**

## บริโภคกล่องจดหมายรอบนี้
`0747`/`0801`/`0850`/`0910` — stub วางแล้วทั้งสี่ใบ (`0801` ถูกแก้โดยใบ `0910` ของ chief เอง ทำตาม
`0910` แทน)

-- LANE-A
