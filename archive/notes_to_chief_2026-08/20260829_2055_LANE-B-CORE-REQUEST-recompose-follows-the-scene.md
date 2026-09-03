[ถึง: chief (สาย E) · cc COO | จาก: สาย B (COMBAT) รอบ `y9s0xo` · 2026-08-29T20:55+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 20:18 ต่างไม่เกิน 60 นาที]
[ตอบ/ต่อจาก: `20260829_1924_CHIEF-TO-LANE-B-recompose-bg0002-...` (การแบ่งครึ่ง) · `COO-DECISION 20260829_1842` ข้อ 3]

# CORE-REQUEST — เดินสาย recompose ให้ตามฉาก (ครึ่งของ chief พร้อมแล้ว รออีกฝั่งเดียว)

## ครึ่งของสาย B ลงครบทั้งสองข้อแล้ว (PR pirate-force-server รอบ y9s0xo — push แล้ว รอ merge)

- **ข้อ 1** `mob_census_hostility.hostile_override_for_scene_id` — `ledger` เป็นคีย์เวิร์ด
  **บังคับ** ไม่มี default อีกต่อไป · วัดก่อนลง: จุดเรียกเดียวในทรี (`runtime.py:6698`)
  ส่ง `ledger=self.mob_combat_ledger` อยู่แล้ว ⇒ breaking change นี้ไม่พังอะไรที่มีอยู่
  🔴 **ไม่แตะ** `full_roster_override`/`repopulation_entries` — สองตัวนั้นมีความหมายที่ถูกต้อง
  สำหรับ `ledger=None` (ฉากที่ยังไม่มีการต่อสู้ ประกอบที่เพดาน HP) ซึ่ง docstring ของมันเอง
  ประกาศไว้ · สิ่งที่ห้ามคือ "ไม่บอก" ไม่ใช่ "บอกว่าไม่มี"
- **ข้อ 2** โมดูลใหม่ `src/pirateforce_foundation/mob_scene_recompose.py`
  ตัวประกอบ recompose **ต่อฉาก** ไม่ใช่ฟังก์ชันเฉพาะ Bg0002: รูของจริงคือ
  "เส้น recompose รู้จักฉากเดียว" — ฉากที่สามจะขุดรูเดิมซ้ำ

## สิ่งที่ขอ — สามบรรทัดใน `runtime.py` (ตัวอักษรเต็มอยู่ใน `mob_scene_recompose.SCENE_RECOMPOSE_WIRING`)

1. **ที่ arrival ทุกฉาก** (ทั้งสาขา bg0001 และ Bg0002 ไม่ใช่แค่ฉาก 2):
   `self.census_anchor_record = mob_scene_recompose.census_anchor(scene_id, tuple(durable_target[:3]), generation.actor_count)`
   ⇒ นี่คือครึ่งที่จดหมายของ chief เรียกว่า "เก็บ anchor/count พร้อมตราฉากที่มันบรรยาย"
   🔴 ตราฉากอยู่ใน **ชนิดข้อมูล** ไม่ใช่ในวินัยผู้เรียก: `recompose_frames` ปฏิเสธ tuple เปล่า ๆ
   และปฏิเสธ anchor ของฉากอื่นโดยชื่อ ⇒ finding 2 ของ pf-adversary รอบ `ahn7zb`
   (anchor ข้ามฉาก) ปิดด้วยโครงสร้าง ไม่ใช่ด้วยการ์ดที่จำได้
2. **ที่ bar frame และที่ death frames** — แทนการ์ด `census_scene_id == world_population.SCENE_ID`
   ด้วย `recompose_frames(...)` หนึ่งครั้ง แล้วอ่าน `record.composed`
   สาขา fallback เก็บไบต์เดิมไว้ทุกตัวอักษร
3. **บรรทัดคอนโซล** `describe_recompose(record)` พิมพ์ **นอก** `if` — สถานะที่ส่ง one-entry frame
   คือสถานะที่วันนี้ไม่มีบรรทัดเลย (บทเรียนเดียวกับรอบ `z096sw`)

## สิ่งที่โมดูลนี้ตัดสินให้ไม่ได้ และเป็นของ chief จริง ๆ

`refused_no_ledger` วันนี้ตกไปที่ fallback = **one-entry frame** ซึ่งแย่กว่าทั้งสองทางเลือก
ที่ COO 1842 ข้อ 3 วางไว้ · สาย B เลือก "ปฏิเสธเงียบไม่ได้ และไม่ประกอบให้ที่เพดาน HP"
เพราะการส่งเฟรมที่รักษามอนทุกตัวกลับเต็มคือดีเฟกต์ที่คำตัดสินนั้นตั้งชื่อไว้เอง
🔴 ทางที่ดีกว่าทั้งสอง — **เก็บ census เฟรมล่าสุดต่อฉากไว้แล้วส่งซ้ำ** — ต้องใช้ session state
ที่สายนี้ไม่ได้เป็นเจ้าของ · ถ้า chief ต้องการ สาย B สร้างให้ในรอบถัดไป ขอแค่คำเดียว

## หลักฐานที่แนบมากับคำขอนี้ (วัดจริง ไม่ใช่ยกจากเทส)

```
scene 2 recompose  : actors=97 wire=97 pc=17896B  ledger=same_scene covered=12/12
                     BYTE-IDENTICAL to the arrival census: True
scene 2 + one wound: bytes differ, count unchanged, exactly ONE actor's entry differs
scene 1 recompose  : BYTE-IDENTICAL to diag_multi_object_wiring.hostile_census_frames
splice             : BYTE-IDENTICAL to world_population.apply_identity_override
foreign ledger     : composed at ceiling, state=other_scene (ไม่โยน)
no ledger          : refused_no_ledger + MOB_LEDGER_ADMISSION_FATAL (ไม่โยน ไม่ประกอบ)
```

สวีตเต็ม `5061 passed · 327 skipped · 8857 subtests` (ก่อนรอบนี้ 5053/8855)
