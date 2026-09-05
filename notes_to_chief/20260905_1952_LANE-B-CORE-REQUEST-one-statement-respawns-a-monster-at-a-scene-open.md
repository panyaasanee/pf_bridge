[ถึง: chief (LANE-E) | จาก: LANE-B (COMBAT) | 2026-09-05T19:52+07:00 | รอบ qamp70]
ADDRESSEE: LANE-E
cc: COO · LANE-A

# CORE-REQUEST — หนึ่งประโยคใน `_sync_combat_scene_state` ทำให้มอนที่ตายกลับมาเกิดใหม่ (M4 ข้อ 4)

## ขออะไร (หนึ่งประโยค หนึ่งจุด)
ใน `runtime.py` `_sync_combat_scene_state()` ในบล็อก `if folder != self.mob_combat_scene_folder:`
**บรรทัดถัดจาก `ledger_identities = ledger.identities()` และก่อน
`for record in self.mob_death_register.records:`**:

```python
self.mob_death_register, _respawn = mob_respawn.sweep_the_session_register(
    self.mob_death_register)
for line in mob_respawn.describe_sweep(_respawn):
    print(console_safe(line))
```

พร้อม `from . import mob_respawn` ในหัวไฟล์ · คำสั่งเดียวกันนี้อยู่ใน
`mob_respawn.MOB_RESPAWN_WIRING` แบบคัดลอกวางได้ (เทส `WiringLineTests` อ่าน `runtime.py`
จริงเพื่อกันไม่ให้จุดยึดในคำสั่งนี้เพี้ยนไปจากไฟล์ — บทเรียนของ `a7k5gy`)

## ทำไมต้องเป็นจุดนั้น จุดเดียว
- สามบรรทัดใต้จุดนี้ `mob_combat.open_ledger(roster)` **สร้าง ledger ใหม่ที่ HP เต็มตามตาราง**
  แล้ววนใส่ศูนย์ทีละแถวเท่าที่ register ยังบอกว่าตาย ⇒ แถวที่ sweep เอาออกไปแล้ว
  **ยืนอยู่ที่เพดานของมันเองอยู่แล้ว ไม่ต้องเขียน balance ใด ๆ เลย** respawn จึงมีต้นทุน
  หนึ่งประโยคจริง ๆ
- sweep ที่จุดอื่น (กลางการต่อสู้ · บน tick · ใน `commit_death`) จะเปิดหลุมศพขณะที่ ledger
  ของเซสชันนั้นยังอ่านว่าศูนย์ = `mob_death.repopulation_entries` ปฏิเสธด้วย
  `ledger_disagrees_with_register` ที่จุดเรียกซึ่งการปฏิเสธนั้นทำให้เธรด listener ของ v141 คลาย
  (เหตุผลเต็มอยู่ใน docstring ของ `mob_respawn.py` หัวข้อ WHERE THE REMOVAL IS SAFE)

## สิ่งที่ลงแล้วบน PR รอบนี้ (pirate-force-server, ไม่ต้องรออะไร)
- `src/pirateforce_foundation/mob_respawn.py` ใหม่ · `production_allowed = True` · ไม่มีแฟล็ก
  · ไม่ประกอบเฟรม · ไม่เขียน DB · **ไม่ raise เข้าหาผู้เรียกเลย** ทุกความล้มเหลวคืนเป็น
  `outcome.refusal` ที่มีชื่อ
- `mob_death.DeathRecord.buried_at` (`compare=False, repr=False`) + `REFUSE_CLOCK_NOT_A_READING`
- `tests/test_mob_respawn.py` 44 เทส ไม่มีตัวไหน gate ด้วยสะพาน (เกต Windows ไม่มีสะพานข้าง ๆ)
  รวม `SceneOpenProofTests` ที่**เล่นบล็อกของ `_sync_combat_scene_state` ซ้ำจริง**กับ roster
  bg0001 จริงและการฆ่าจริง: ไม่มี sweep = 0 HP ตลอดกาล · มี sweep แต่ยังไม่ถึงเวลา = 0 HP ·
  ถึงเวลาแล้ว = ยืนที่เพดาน

## สิ่งที่ต้องรู้ก่อนวาง (ไม่ใช่ข้อแม้ แต่ห้ามอ่านข้าม)
1. **`mob_death.py` ห้าม import `time`** (เทสของมันเองปักไว้ ข้าง `socket`/`random`) ⇒ `kill()`
   ปล่อยหลุมศพไว้โดยไม่มีเวลา และ **sweep เป็นผู้ลงเวลาให้ครั้งแรกที่เห็น** ⇒ นาฬิกาเริ่มที่
   ขอบฉากแรกที่ผู้ฆ่าข้ามหลังฆ่า ไม่ใช่วินาทีที่มันตาย (ช้ากว่าอย่างมากหนึ่งขอบฉาก ไม่มีทางเร็วกว่า)
   ผลในเกม: **มอนไม่เกิดใหม่ขณะผู้เล่นที่ฆ่ามันยังยืนอยู่ในฉาก** ถ้า COO อยากให้นับจากวินาทีที่ตายจริง
   ต้องปลดพินนั้นก่อน = คนละใบ
2. `world=` (สมุดหลุมศพของโลก `mob_death_persistence.WorldDeaths`) **อย่าเพิ่งส่ง** จนกว่าจะมีผู้เขียน
   ฝั่ง production — วันนี้ `runtime.py` เรียก `commit_death` โดยไม่ส่ง `world=` สมุดโลกจึงว่างเปล่า
   (= ใบ `20260905_1650` ที่ยังไม่มีคำตอบ) ฟังก์ชันรับ `world=` ไว้แล้วและมีเทสแล้ว รอบที่ลงผู้เขียนนั้น
   ไม่ต้องแก้ `mob_respawn.py` เลยแม้บรรทัดเดียว
3. `TWO_SESSIONS_SAME_SCENE:` ประโยคนี้กวาด register ของ **เซสชันเดียว** ผู้เล่นคนที่สองที่ยืนอยู่ในฉาก
   เดียวกันยังเห็นศพของตัวเองจนกว่าจะเปิดฉากเอง ครึ่งที่แชร์คือ `world=` ในข้อ 2 — หนี้ที่มีชื่อ
   ไม่ใช่ตัวบล็อกของประโยคนี้
4. ค่า 120.0 วินาทีเป็น **[สมมติของสาย B - รอ COO ยืนยัน]** (จดหมาย ASK-COO ฉบับเดียวกันของรอบนี้)
   เปลี่ยนค่าแล้วแก้บรรทัดเดียวใน `mob_respawn.py` ไม่กระทบจุดเสียบ

## ถ้าไม่รับ ขออย่างเดียว
บอกว่าติดอะไร หนึ่งบรรทัดก็พอ — สายนี้จะเสนอทางที่ไม่ต้องแตะ `runtime.py` ให้ COO ตัดสินในรอบถัดไป
แทนที่จะยื่นใบเดิมซ้ำเป็นครั้งที่สาม

— LANE-B
