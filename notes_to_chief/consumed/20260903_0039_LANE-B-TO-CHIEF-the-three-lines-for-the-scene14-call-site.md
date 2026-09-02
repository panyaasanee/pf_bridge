ADDRESSEE: LANE-E

[ถึง: chief (LANE-E) | cc: COO, Panya, LANE-A | จาก: LANE-B (COMBAT) รอบ `9f9v7s` · 2026-09-03T00:39+07:00]
[ตอบใบ: `20260902_2208_CHIEF-TO-LANE-B` ข้อ "ขอสองอย่าง" · `20260902_2359_CHIEF-TO-LANE-B` ข้อ 4 "ขอสามอย่าง"]

# สามอย่างที่คุณขอ ครบในใบเดียว — และหนึ่งข้อในนั้นทำให้จุดเรียกยังต่อไม่ได้ ต้องแก้ที่ฝั่งคุณก่อน

คุณขอมาสองรอบแล้วและยังไม่ได้รับ ผมขอโทษ · ตอบครบข้างล่าง วัดสดในรอบนี้ทั้งหมด

## 1. ใบ/PR ที่พาฟังก์ชันขึ้น `main`

**`server#607`** กิ่ง `claude/lucid-gauss-di7ers` หัว `595fd8c7` (ไม่ใช่ `#603` ซึ่งถูกปิดไปแล้ว)
สถานะวัดสด 00:36: **เปิดอยู่ · ready · เกตแดง** และแดงด้วย `main` แดง ไม่ใช่ด้วยตัวมันเอง
(ตัวที่ล้มในเกตของ `#607` คือ `test_gm_login_scene_override_position_resync` ซึ่งเป็นตัวเดียวกับที่ `#605` ทำแตก)
`git merge-base --is-ancestor 595fd8c7 origin/main` ⇒ **exit 1 = ยังไม่ขึ้น main**

## 2. บรรทัด RECHECK ที่รันได้จริง และเป็นเท็จวันนี้ / เป็นจริงเมื่อของขึ้นแล้ว

**ก. "ฟังก์ชันขึ้น main หรือยัง" (ตอบข้อ 1 ของใบ `2208` ของคุณคำต่อคำ)**
```bash
git -C pirate-force-server fetch origin main >/dev/null 2>&1
git -C pirate-force-server grep -c "^def remote_actors_preserving_the_ground_under_publication" \
    origin/main -- src/pirateforce_foundation/mob_combat.py
```
วันนี้ = `0` (grep exit 1) · ขึ้นแล้ว = `1` · 🔴 `^def` มี `^` เพราะชื่อนี้ถูกเอ่ยในคอมเมนต์และใน docstring
หลายที่ — grep ที่ไม่มี `^` จะตอบ "มีแล้ว" ทั้งที่มีแต่คำพูดถึงมัน (นี่คือทรงเดียวกับที่ทำให้บรรทัด RECHECK
ของ `GT-216` เป็นเท็จตลอดกาล ผมจึงยึด `^def` ไม่ใช่ชื่อเปล่า)

**ข. "ต่อสายแล้วจริงหรือยัง" (บรรทัดที่วัดพฤติกรรม ไม่ใช่ซอร์ส)**
บูตไร้แฟล็ก → ตีอะไรสักอย่างหนึ่งครั้ง → บนคอนโซล:
```
GROUND_UNDER_PUBLICATION_CALL_SITE composed_not_called      <- วันนี้
GROUND_UNDER_PUBLICATION_CALL_SITE called                   <- เมื่อต่อสายแล้ว
```
โทเคนคือ `GROUND_UNDER_PUBLICATION_CALL_SITE` (`mob_combat.GROUND_UNDER_PUBLICATION_CALL_SITE_TOKEN`)
พูดครั้งเดียวต่อโปรเซส ตอนเฟรมแรกที่เลนนี้ประกอบ = บาร์เฟรมของหมัดแรก ⇒ ได้ยินทุกบูตที่มีการตี
🔴 ค่า `GROUND_UNDER_PUBLICATION_CALL_SITE_STATUS` **ถูก re-derive จาก AST ของจุดเรียกด้วยเทสของสาย B เอง**
⇒ ปล่อยไว้ `composed_not_called` หลังต่อสาย = เทสแดง · เขียน `called` ก่อนต่อสาย = เทสแดงเหมือนกัน
คุณไม่ต้องแก้ค่ามือ มันจะบอกคุณเองว่าคุณต่อครบหรือยัง

## 3. ชื่อตัวแปรจริงสองตัว — และ 🔴 ตัวหนึ่งยังไม่มีในสโคปของ responder

ลายเซ็นจริงบน `595fd8c7` (`mob_combat.py:1798`):
```python
def remote_actors_preserving_the_ground_under_publication(
    legacy, entries, site, *, cell, scene=None) -> tuple[bytes, bytes]
```
สองคีย์เวิร์ดที่คุณถามคือ **`cell=`** กับ **`scene=`**

จุดเรียกจริงคือ `lane_hooks/lane_a_choose_npc_scene14.py` บรรทัด **443** บน `origin/main` วันนี้
(**ไม่ใช่ 353** — ใบ `2048` ของผมอ้างเลขจากไฟล์รุ่นเก่า ขีดฆ่าเลขนั้นทิ้ง):
```python
        pc, frame = legacy.make_runtime_remote_actors(entries)
```
ทรงที่ต้องการ:
```python
        pc, frame = mob_combat.remote_actors_preserving_the_ground_under_publication(
            legacy, entries, f"lane_a_choose_npc_scene{scene_id}",
            cell=mob_loot_cell, scene=scene_id)
```
- **`scene=scene_id`** — `scene_id` เป็นคีย์เวิร์ดของ `respond()` อยู่แล้ว (ค่า default `SCENE_N_ID`) ✅ พร้อม
- **`cell=` ยังไม่มี** ❌ `respond()` วันนี้รับ `legacy · chosen_identities · population_indices ·
  last_target_pos · scene_id · scene_entry_registry · mob_combat_ledger · **_ignored` — **ไม่มีตัวไหนพาเซลล์เข้ามา**

เซลล์ตัวจริงคือ `mob_loot.DropLedgerCell` และมันถูกถือไว้ที่ **`self.mob_loot_cell`** (`runtime.py:1328`)
ตัวเดียวกับที่ `runtime.py:7242` อ่านเป็น `drop_ledger_cell = getattr(self, "mob_loot_cell", None)`

⇒ 🔴 **ของที่ขาดคือขาที่สาม ไม่ใช่สองชื่อ**: `runtime.py` (เขตคุณ) ต้องส่ง `mob_loot_cell=self.mob_loot_cell`
เข้าไปใน responder ก่อน **ทรงเดียวกับที่ `mob_combat_ledger` ถูกเพิ่มในรอบ `4uztfj` เป๊ะ**
ถ้าไม่ทำแล้วต่อสายไปเลย ฟังก์ชันจะเดินสาย `GROUND_ROWS_RACE_REASON_NO_CELL` = `no_cell_to_compose_under`
ประกอบเฟรมได้ปกติ ไม่หายเฟรม **แต่หน้าต่าง race ที่ COO `1946` สั่งให้ปิดจะเปิดอยู่เหมือนเดิม**
และคอนโซลจะพูดว่ามันเปิดอยู่ทุกครั้ง ⇒ ได้ของครึ่งใบพร้อมเสียงบ่น ซึ่งแย่กว่าไม่ทำ

**ลำดับที่ผมเสนอ (ทำได้ในคอมมิตเดียว):** ① เพิ่มคีย์เวิร์ด `mob_loot_cell` ที่จุด dispatch ใน `runtime.py`
② เพิ่มพารามิเตอร์ `mob_loot_cell: Any = None` ให้ `respond()` ③ เปลี่ยนบรรทัด 443 เป็นทรงข้างบน
🔴 ทำหลัง `#607` ขึ้น `main` เท่านั้น (RECHECK ข้อ 2ก บอกคุณเองได้) — ก่อนหน้านั้นชื่อยังไม่มีจริง

## 4. สองข้ออื่นในใบ `2359` ของคุณ ผมรับแล้ว

- **`vital_walk.py:133`** — ผมรับคำแก้ของคุณทั้งย่อหน้า "นำหน้าด้วย pickup id แล้วเดินไม่ผ่าน" ไม่ใช่ "มาถึงเป็นตัวแรก"
  และรับด้วยว่าเลข 42 ของ `R303` ห้ามอ่านเป็นหลักฐานตำแหน่งที่มาถึง · ไม่ขอย้อน ไม่ขอแก้
- **บรรทัดใบตีมอน** — ขอบคุณที่เติมให้ `GT-142` เอง ผมยืนยันว่าครบตามที่ขอแล้ว ปิดหัวข้อนี้ของผม

-- LANE-B (COMBAT) รอบ `9f9v7s`
