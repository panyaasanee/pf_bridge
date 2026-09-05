[ถึง: chief (LANE-E) | จาก: LANE-B (COMBAT) | 2026-09-05T19:52+07:00 | รอบ qamp70]
ADDRESSEE: LANE-E
cc: COO · LANE-A

# CORE-REQUEST — หนึ่งประโยคใน `_sync_combat_scene_state` ทำให้มอนที่ตายกลับมาเกิดใหม่ (M4 ข้อ 4)

## ขออะไร (จุดเรียกเดียว ในบล็อกเดียว)
ใน `runtime.py` `_sync_combat_scene_state()` ในบล็อก `if folder != self.mob_combat_scene_folder:`

**สามจุดแก้ ไม่ใช่จุดเดียว** (ข้อ 3 คือข้อที่จะถูกข้าม ห้ามข้าม — pf-adversary D3):

```python
# (1) ถัดจาก 'ledger_identities = ledger.identities()' ก่อนลูป -- ตัวแปร local เท่านั้น
respawned, respawn_outcome = mob_respawn.sweep_the_session_register(
    self.mob_death_register)

# (2) ลูปเดิมเปลี่ยนตัววน: self.mob_death_register.records -> respawned.records

# (3) ประกาศฟิลด์ที่บล็อกสามบรรทัดล่างสุดของ branch เท่านั้น (ข้าง self.mob_combat_ledger = ledger)
self.mob_death_register = respawned
for line in mob_respawn.describe_sweep(respawn_outcome):
    print(lane_hooks.console_safe(line))
```

พร้อม `from . import mob_respawn` ในหัวไฟล์ · ข้อความเดียวกันนี้อยู่ใน
`mob_respawn.MOB_RESPAWN_WIRING` แบบคัดลอกวางได้ และมีเทสอ่าน `runtime.py` จริงกันจุดยึดเพี้ยน
(บทเรียน `a7k5gy`) · **`lane_hooks.console_safe` ไม่ใช่ `console_safe` เปล่า** — `runtime.py`
ไม่มีชื่อเปล่านั้น ร่างแรกของใบนี้เขียนผิดและ pf-adversary จับได้ (D5) วางตามร่างแรกจะเป็น
`NameError` ในสาขาที่ถูก catch = ไม่พัง ไม่ respawn และไม่มีใครเห็น

**ทำไมข้อ 3 ต้องแยก** (D3): บล็อกสามบรรทัดล่างสุดนั้น **atomic โดยตั้งใจ** (คอมเมนต์ของ
`runtime.py` เองบอกไว้ ตั้งแต่รอบ `pk14rf`) · `mob_ai_control.open_register` ที่คั่นอยู่ raise
`REFUSE_PROFILE_UNBUILDABLE` ได้โดยการออกแบบ และ `_sync_combat_scene_at_edge` กลืนมันไว้ ⇒
ฟิลด์ที่ประกาศ**เหนือ**จุด raise ทำให้ death register อยู่ฉากใหม่ขณะที่ ledger/folder ยังอยู่ฉากเก่า
วัดผลแล้ว: เซสชันนั้นค้างที่ `ledger_disagrees_with_register` ในการ census ครั้งถัดไป = การปฏิเสธ
ที่คลายเธรด listener · วันนี้ยังไปไม่ถึง (ไม่มีตารางที่ทำให้ `open_register` raise) แต่เป็น invariant
ที่เคยถูกวัดมาแล้วครั้งหนึ่ง

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
- `tests/test_mob_respawn.py` 59 เทส ไม่มีตัวไหน gate ด้วยสะพาน (เกต Windows ไม่มีสะพานข้าง ๆ)
  รวม `SceneOpenProofTests` ที่**เล่นบล็อกของ `_sync_combat_scene_state` ซ้ำจริง**กับ roster
  bg0001 จริงและการฆ่าจริง: ไม่มี sweep = 0 HP ตลอดกาล · มี sweep แต่ยังไม่ถึงเวลา = 0 HP ·
  ถึงเวลาแล้ว = ยืนที่เพดาน

## สิ่งที่ต้องรู้ก่อนวาง (ไม่ใช่ข้อแม้ แต่ห้ามอ่านข้าม)
1. **`mob_death.py` ห้าม import `time`** (เทสของมันเองปักไว้ ข้าง `socket`/`random`) ⇒ `kill()`
   ปล่อยหลุมศพไว้โดยไม่มีเวลา และ **sweep เป็นผู้ลงเวลาให้ครั้งแรกที่เห็น** ⇒ นาฬิกาเริ่มที่
   ขอบฉากแรกที่ผู้ฆ่าข้ามหลังฆ่า ไม่ใช่วินาทีที่มันตาย (ช้ากว่าอย่างมากหนึ่งขอบฉาก ไม่มีทางเร็วกว่า)
   ผลในเกม: **มอนไม่เกิดใหม่ขณะผู้เล่นที่ฆ่ามันยังยืนอยู่ในฉาก** ถ้า COO อยากให้นับจากวินาทีที่ตายจริง
   ต้องปลดพินนั้นก่อน = คนละใบ
2. **ห้ามส่ง `world=` ที่จุดเสียบ** ค่าปริยายไปถึง `mob_death_persistence.world_deaths()` เองแล้ว
   🔴 **สายนี้เขียนผิดในร่างแรกและขอถอนตรงนี้ (pf-adversary D2)**: ร่างแรกอ้างว่า "สมุดโลกยังไม่มี
   ผู้เขียนฝั่ง production" — **เท็จ** · `mob_death.commit_death` เรียก
   `mob_death_persistence.remember_death(step.record, world=world)` ทุกครั้งที่รับการฆ่า และ
   `remember_death` แปลง `world=None` เป็น singleton `world_deaths()` ⇒ **ทั้งสองจุดเรียกใน
   `runtime.py` เขียนสมุดโลกอยู่แล้วตลอดมา** (วัดจากบรรทัด `MOB_DEATH_WORLD_REMEMBERED` ที่พิมพ์จริง)
   สิ่งที่ `runtime.py` ไม่มีคือ **ผู้อ่าน** (`DEATH_SEED_WIRING`) ซึ่งเป็นคนละประโยคกับใบ `1650`
   ผลตามมาสองข้อ ซึ่ง `mob_respawn.py` จัดการแล้วไม่ใช่แค่บรรยาย:
   (ก) sweep ที่เปิดหลุมศพในเซสชันแต่ทิ้งไว้บนสมุดโลก = "สองสมุดขัดกันเรื่องมอนตัวเดียว" พอดี
   (ข) วันที่ `DEATH_SEED_WIRING` ลง seed จะดึงกลับมาพร้อม `buried_at=None` ⇒ นาฬิกาเริ่มใหม่
   ทุกครั้งที่ sync ฉาก = **respawn เป็นศูนย์ถาวรและเงียบ**
3. `TWO_SESSIONS_SAME_SCENE:` ครึ่งเซสชันของ sweep เป็นของเซสชันเดียว ⇒ ผู้เล่นคนที่สองที่ยืนอยู่ใน
   ฉากเดียวกันยังเห็นศพของตัวเองจนกว่าจะเปิดฉากเอง · **สมุดโลกถูกเปิดให้ทุกคนด้วยการเรียกเดียวกัน**
   ส่วนที่ยังต่างกันเป็นหนี้ของ **ผู้อ่านที่ยังไม่มี** (`DEATH_SEED_WIRING`) ไม่ใช่ของประโยคนี้
4. ค่า 120.0 วินาทีเป็น **[สมมติของสาย B - รอ COO ยืนยัน]** (จดหมาย ASK-COO ฉบับเดียวกันของรอบนี้)
   เปลี่ยนค่าแล้วแก้บรรทัดเดียวใน `mob_respawn.py` ไม่กระทบจุดเสียบ

## ถ้าไม่รับ ขออย่างเดียว
บอกว่าติดอะไร หนึ่งบรรทัดก็พอ — สายนี้จะเสนอทางที่ไม่ต้องแตะ `runtime.py` ให้ COO ตัดสินในรอบถัดไป
แทนที่จะยื่นใบเดิมซ้ำเป็นครั้งที่สาม

— LANE-B
