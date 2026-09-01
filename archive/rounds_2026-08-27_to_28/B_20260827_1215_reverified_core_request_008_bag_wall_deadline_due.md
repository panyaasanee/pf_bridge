# round `B_20260827_1215` (`p955sh`) · lane B · COMBAT -- independent re-verification of CORE-REQUEST-008 wiring (R188), bag-wall deadline now due, no new buildable surface in this lane's own zone

**opened:** 2026-08-27 12:00 (+07:00) · **closed:** 2026-08-27 ~12:2x (+07:00)
**branches:** `claude/serene-darwin-p955sh` (pirate-force-server, PR #95) ·
`claude/relaxed-goldberg-p955sh` (pf_bridge, PR #169)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็นอะไรใหม่จาก**รอบนี้**เอง (รอบนี้ไม่มี diff โค้ด เป็นรอบตรวจสด
อย่างเดียว) แต่สืบเนื่องจากรอบก่อน (`R188`, chief cloud, ปิด ~11:30): **ถ้า attended ยืนยัน `GT-084`/
`RIDER-084-A` ผ่าน** ผู้เล่นจะเห็นว่าเมือง/มอนสเตอร์รอบตัว**ไม่หายวับ**ทุกครั้งที่ต่อสู้หรือมีมอนสเตอร์ตายอีก
ต่อไป (บั๊ก world-wipe ที่สาย B เปิดไว้ในรอบ `1015` ถูกต่อสายปิดจริงแล้วที่ `runtime.py`) -- ชั้น
client-observable ของเรื่องนี้ยังไม่มีใครยืนยันด้วยตา (ดูข้อ 2)

## 1 ตรวจสอบ brief ที่ล้าสมัยอีกครั้ง -- CHARTER-02 อ้างว่าเริ่มจากศูนย์ ไม่จริงเหมือนเดิม

Brief รอบนี้ (`CHARTER-02`, 2026-08-25) อ้างถึง `BUILD-004/005/006` ราวกับยังไม่เริ่ม -- ตรวจสดแล้วไม่จริงมาตั้งแต่
รอบ `sifsfg` (`1015`) และรอบก่อนหน้านั้นทั้งหมด: มอนสเตอร์แดงจากตาราง MOBS จริง (`field_mobs.py` +
`field_mob_tables.py`, 13 ตัวที่ผ่านเกณฑ์ `ai_combat` ∧ `rank` ∧ `unambiguous` จาก 115 placement ทั้งหมด --
**ตัวเลข 13 คือเกณฑ์ที่ถูกต้องของ generator เอง ไม่ใช่ของที่ต้องขยาย**), ตี/เลือดลด/ตาย (`mob_combat.py`,
`mob_death.py`, `mob_aggro.py`), ของหล่น/เก็บครึ่งแรก (`mob_loot.py`, `mob_pickup.py`) มีอยู่แล้วครบและมีเทส
ปกป้องอยู่หลายร้อยตัว ไม่ได้เริ่มใหม่จาก M2 จบ -- นี่คือรอบต่อจากรอบ `R188` ของ chief cloud โดยตรง (branch
`claude/serene-darwin-p955sh` แตกจาก HEAD หลัง PR #93/#94 merge เข้า `main` แล้ว)

## 2 ตรวจสดอิสระ -- CORE-REQUEST-008 ที่ chief อ้างว่าต่อสายแล้วใน R188

อ่านจดหมาย `20260827_1130_CHIEF-REPLY-*` และ `rounds/R188_*` -- chief อ้างว่าต่อสาย
`mob_death.hostile_census_frames` เข้าสามจุดใน `_dispatch_mob_combat` แล้ว พร้อม fail-closed guard และ scene
guard **ไม่เชื่อจดหมายเฉย ๆ -- ตรวจเอง:**

- `grep -n "MOB_COMBAT_BAR_CENSUS_RECOMPOSE\|MOB_DEATH_FRAMES_CENSUS_RECOMPOSE" src/pirateforce_foundation/runtime.py`
  → พบจริงที่บรรทัด 3892, 4063 -- ตรงกับที่จดหมายอ้าง
- `grep -n "describe_roster_override_coverage" src/pirateforce_foundation/runtime.py` → พบจริงที่บรรทัด 5080
  (คนละตำแหน่งจากที่รอบ `lp6hg4`/`xx69nd` เคยขอไว้ที่ ~4905-4909 เดิม แต่**เป็นบรรทัดเดียวกันในทางความหมาย** --
  ปิดข้อค้างเดิมนั้นได้จริง ไม่ใช่แค่คำอ้าง)
- รันสวีตเต็มอิสระ (`python3 -m unittest discover -s tests -p "test_*.py"`, คนละคำสั่งจาก pytest ที่ R188 ใช้):
  **3429 ทดสอบ, error 18 ตัวเดิม (`ModuleNotFoundError: capstone` ล้วน ใน static-RE test ชุดเดิมที่ sandbox นี้
  ไม่มี), skip 212** -- ไม่มี `FAIL:` ใหม่เกิดขึ้น ตรงกับ baseline ที่ทุกรอบก่อนหน้ายืนยันไว้
- **ไม่แตะ `mob_combat.py`/`mob_death.py`/`runtime.py` เลยในรอบนี้** -- ตรวจแบบอ่านอย่างเดียว

**สรุป:** คำอ้างของ R188 ตรวจสดผ่านจริง ไม่ใช่การเชื่อจดหมายต่อ

## 3 BUILD-006 ครึ่ง relog -- กำแพงกระเป๋ายังไม่ถูกแก้ และเส้นตายมาถึงแล้ว

`COO-DECISION` (`20260826_0950`) มอบงานผ่า `inventory.require_known_backpack` + migration คอลัมน์
`next_item_identity` + สำเนา DB ให้ **chief** เป็นก้อนเดียว กำหนด **"ไม่เกิน 27 ส.ค. 12:00"**

ตรวจสดรอบนี้: `git log --oneline -- src/pirateforce_foundation/inventory.py` → commit เดียวที่แตะไฟล์นี้ยังคือ
`1e0b20b` (PR #12, เก่ากว่าคำเคาะ COO มาก) **ยังไม่ถูกแก้เลยแม้แต่บรรทัดเดียว** `grep -rn
"next_item_identity" src/pirateforce_foundation/*.py` → มีแค่ใน `mob_pickup.py` (ฝั่งของสาย B เองที่สร้างรอ
ไว้ตั้งแต่รอบก่อน ๆ: `next_item_identity()` เผื่อคอลัมน์ที่ยังไม่มี) `inventory.py`/`store.py` (ไฟล์ของ chief)
ไม่มีคำนี้เลย ⇒ **การ์ดยังอยู่ครบ ไม่มีอะไรขยับ**

รอบนี้เขียนเวลาที่ 2026-08-27 12:00 (+07:00) พอดีกับเส้นตาย -- **เส้นตายถึงแล้วและงานยังไม่เริ่ม** (อย่างน้อยก็
ยังไม่ปรากฏในโค้ดที่ push แล้ว) นี่ไม่ใช่ของใหม่ (สาย B เคยยืนยันสดเรื่องนี้แล้วในรอบ `xx69nd`, `0345`) แต่
**เส้นตายที่เพิ่งมาถึงเป็นข้อเท็จจริงใหม่ที่ต้องแจ้ง** -- ไม่ใช่แค่ยืนยันซ้ำเฉย ๆ ดูจดหมายข้อ ①

## 4 ทำไมสาย B ไม่แก้กำแพงเอง

`inventory.require_known_backpack` อยู่ใต้ `src/pirateforce_foundation/` ซึ่งเป็นเขตเขียนของสาย B ตามกฎบัตร
แต่ `COO-DECISION 20260826_0950` มอบไฟล์นี้ให้ chief ตรง ๆ ("กำแพงกระเป๋าเป็นของ chief") พร้อมเหตุผลชัดว่า
**"ขยาย allowlist" คือทำให้เส้นทางของผู้เล่นยอมรับของที่ไม่มีใครตรวจ** -- เป็นคำเคาะแยกเฉพาะไฟล์ ไม่ใช่กฎบัตร
เขตเขียนทั่วไป **ยึดตามคำเคาะที่แคบกว่านั้น** ไม่แตะไฟล์นี้ต่อไป

## 5 ค้นหาพื้นที่สร้างใหม่ในเขตของสาย B เอง -- ไม่พบของใหม่จริง

ตรวจตามธรรมเนียมของรอบ "confirmed no new buildable surface" ก่อนหน้า (`0340`, `xx69nd`) ซ้ำอีกครั้ง:

- roster 13 ตัวของ field mob combat: ตรวจ `field_mob_tables.py`'s `PREDICATE_CENSUS` แล้ว -- `ai_combat=13`,
  `rank=13`, `unambiguous=115` **ตรงตามเกณฑ์ที่ generator เขียนไว้เอง** ไม่ใช่ตัวเลขที่ต้องขยาย (BUILD-004 ขอ
  "แถวจริงจากตาราง MOBS" -- ตอนนี้ทำอยู่แล้วถูกต้อง ไม่ใช่ attr ประกอบเอง)
- `GT-084`/`RIDER-084-A` (client-render ของ census/combat/death) -- ยังเปิด รอ attended เท่านั้น ไม่ใช่งาน
  server-side เพิ่มเติมของสาย B
- ค้นหาคำอ้าง "unreached today"/"ยังไม่ถูกเรียก" ที่อาจค้างในโมดูลของสาย B เอง (`mob_combat.py`,
  `mob_death.py`, `mob_aggro.py`, `mob_loot.py`, `mob_pickup.py`, `field_mobs.py`) -- ไม่พบข้อความค้างที่ไม่ตรง
  กับโค้ดจริง (R188 แก้คอมเมนต์เท็จจุดเดียวที่เคยพบไปแล้วใน `runtime.py` ไฟล์ของ chief คนละไฟล์)

**สรุป:** ไม่มีพื้นที่สร้างใหม่ที่มีความหมายในเขตเขียนของสาย B ตอนนี้ นอกจากรอ chief ปลดกำแพงกระเป๋า (ข้อ 3)

## 6 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | ตรวจสด `runtime.py` (อ่านอย่างเดียว) ยืนยันคำอ้าง R188 ตรงจริงทุกจุดที่อ้าง · รันสวีตเต็มอิสระ 3429 ทดสอบ error 18 ตัวเดิม (capstone) ไม่มี FAIL ใหม่ · `git log` ยืนยัน `inventory.py` ไม่ถูกแตะตั้งแต่คำเคาะ COO |
| **client-observable** | ไม่มี -- ไม่มีใครดูจอรอบนี้ รอบนี้ไม่ใช่รอบ attended · `GT-084`/`RIDER-084-A` ยังเปิดเหมือนเดิม |

## 7 ถ้าผิดต้องย้อนอะไรบ้าง

รอบนี้**ไม่มี diff โค้ด** ทั้งสอง repo มีแค่คอมมิต `round claim: p955sh` (empty) และไฟล์บันทึกรอบ/จดหมายนี้เอง --
ย้อนได้ทันทีด้วยการปิด PR (branch เก็บไว้) ไม่กระทบ production path ใด ๆ

## 8 `pf-adversary`

**ไม่เรียกรอบนี้** -- ไม่มี diff โค้ดให้พิสูจน์ (เฉพาะไฟล์บันทึกรอบ + จดหมาย) ตรงตามธรรมเนียมของรอบ
"confirmed no new buildable surface" ก่อนหน้า (`0340`, `xx69nd`)

## 9 จดหมาย

`notes_to_chief/20260827_1215_LANE-B-STATUS-bag-wall-deadline-due-core-request-008-reverified.md`

-- **สาย B · COMBAT**
