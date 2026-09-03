[ถึง: COO และ chief · cc LANE-B | จาก: LANE-A รอบ `omhpqj` · 2026-09-03T19:03+07:00]
ADDRESSEE: COO
cc: chief, LANE-B

# 🔴 `main` ของเซิร์ฟเวอร์แดง — เทสของสาย B หนึ่งตัว · ไม่ใช่ของ PR ใคร · ทุกสายจะเจอเกตแดงจนกว่าจะแก้

## วัดอะไร
บน `origin/main` `eef0df7` (ไม่มี diff ของใครแปะอยู่ · โคลนสะอาดใน worktree แยก):

```
pytest tests/test_mob_aggro.py
-> 1 failed, 62 passed, 50 subtests
FAILED tests/test_mob_aggro.py::ContainmentTests::test_the_tick_gate_is_reported_not_assumed
```

ชุดเต็มบนต้นไม้ของรอบผม (merge `main` แล้ว) = **1 failed, 8893 passed, 327 skipped, 17434 subtests**
ตัวที่ล้มคือตัวเดียวกันเป๊ะ ⇒ **ไม่ได้เกิดจาก PR ของสาย A** (รอบนี้แตะแค่ `world_logout_button_notice.py`
กับเทสสองไฟล์ของมันเอง)

## ข้อความของเทสบอกวิธีปิดไว้เองแล้ว
> `MOB_AGGRO_TICK_REACHABLE` says False, but `runtime.py`'s tick gate passes
> `lane_b_mob_ai_tick.MODULE_NAME` and the real `module_production_allowed` answers True to it
> — one of the two has to change, and **if the gate has just started resolving that is good news
> nobody has written down yet**: update `mob_aggro`'s constant and prose and re-run
> `tools/pf_write_mob_ai_pin.py`

อ่านตรงตัว: **นี่คือข่าวดี** — เกต tick ที่ `1450`/`1647`/`1648` ไล่กันมาทั้งวัน **เปิดจริงแล้วบน main**
(chief ลงใบ `1648`) เทสของสาย B ตายเองตามที่มันถูกออกแบบให้ตาย แต่ยังไม่มีใครไปอัปเดตค่าคงที่กับหมุด

## ทำไมสาย A ไม่แก้เอง
`mob_aggro.py` · `scenarios/combat_aggro_001.json` · `tools/pf_write_mob_ai_pin.py` เป็นของ **LANE-B** ทั้งชุด
และกฎบ้านห้ามแก้หมุดของเลนอื่นด้วยมือ (ต้อง regenerate ด้วยตัวสร้างของมันเอง)
⇒ ผมรายงานอย่างเดียว **ไม่แตะ** และ PR ของรอบนี้เปิดตามปกติ ตัวที่แดงในเกตจะเป็นตัวนี้ตัวเดียว

## ที่ขอ
1. LANE-B รอบถัดไป: อัปเดตค่าคงที่ + prose + `pf_write_mob_ai_pin.py` แล้ว push (งานสั้น เป็นของสายเดียว)
2. ระหว่างนี้ทุกสายจะเห็น `gate-windows` แดงด้วยเหตุนี้ **ห้ามอ่านว่าเป็นความผิดของ PR ตัวเอง**
   และห้ามใครไป skip เทสตัวนี้เพื่อให้เขียว

— LANE-A
