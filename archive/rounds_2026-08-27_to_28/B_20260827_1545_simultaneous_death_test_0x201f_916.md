# round `B_20260827_1545` (`67jejl`) · lane B · COMBAT -- simultaneous-death
test for `0x201F` + `916` (Training Iron Man) per COO-DECISION 0955, plus a
`widened=` scope hole `pf-adversary` found and closed in the same round

**opened:** 2026-08-27 10:37 (+07:00, real wall clock -- see note in §1) ·
**closed:** 2026-08-27 ~11:10 (+07:00)
**branches:** `claude/trusting-curie-67jejl` (pirate-force-server, PR #108) ·
`claude/lucid-hamilton-67jejl` (pf_bridge, PR #184)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็นอะไรใหม่ในเกม -- รอบนี้แตะแค่ `mob_death.py`
(ฟังก์ชัน `kill()` เดิม เพิ่ม guard, ไม่มีบรรทัดโปรดักชันใหม่ที่เปลี่ยนพฤติกรรมของ
`0x201F`) กับ `tests/test_mob_death.py` สถานะที่ผู้เล่นเห็นได้จริงตอนนี้เหมือนรอบก่อน
(`t48epl`): มอนสเตอร์แดงจากตาราง MOBS จริงในสนาม, ตี/เลือดลด/ตายได้ที่ `0x201F` ตัวเดียว,
ของหล่น/เก็บครึ่งแรก สิ่งที่รอบนี้ทำคือปลดล็อกเงื่อนไขก่อนต่อสายของ COO สำหรับ `916`
(Training Iron Man) **อย่างปลอดภัยกว่าที่ขอมา** -- ดู §3.2 ก่อนเชื่อว่าใส่บรรทัดเดียวที่
`runtime.py:3925` แล้วจบ

## 1 ล็อกต้นรอบ + หมายเหตุนาฬิกา

**0 ใบ** PR `[LANE-B]` เปิดค้างทั้งสองรีโปก่อนรอบนี้ (ตรวจสดผ่าน `list_pull_requests`,
ใบล่าสุดของสาย B คือ `pf_bridge#177` / `pirate-force-server#103` ปิดแล้วด้วย
`merged=true` -- งานอยู่บน `main` แล้ว ไม่ต้องกู้คืนตามข้อ A ของ ADDENDUM v6.2) ยึดล็อก
ด้วย draft PR `pf_bridge#184` · `pirate-force-server#108` เวลาจริงที่ยึดล็อก (จาก
GitHub `created_at` ของ PR #184): `2026-08-27T03:37:09Z` = **10:37:09 +07:00** --
บันทึกไว้เพราะ label ภายในของไฟล์รอบก่อนหน้า (`1500`, `1515`) *ไม่ใช่* นาฬิกาจริงของ UTC+7
(นาฬิกาจริงตอนนั้นคือ ~10:1x-10:2x +07:00 ตาม PR `pf_bridge#182`/`#183` ของสายอื่น) --
รอบนี้เดินป้ายต่อจาก label `1515` ของรอบก่อน (ไม่ใช่จากนาฬิกาจริง) เพื่อให้ลำดับไฟล์อ่านง่าย
แต่ **ข้อ 6 ของรอบนี้ (หลักฐานสองชั้น) ใช้เวลาจริงเสมอ** -- นี่คือ drift เดิมที่เคยถูกพูดถึง
(`R173` clock-drift) ไม่ใช่ของใหม่ ไม่ต้องเปิดใบขอ COO ซ้ำ

## 2 อ่านก่อนเขียน

`notes_to_chief/20260827_0955_COO-DECISION-...`, `...0950_PANYA-DECISION-...`: COO
อนุมัติขยาย `mob_death.kill()` จาก `0x201F` ไปที่ **identity เดียว**: Training Iron Man
(`MOBS.n_ID 916`) -- ไม่ใช่ roster 13 ตัวเดิมของ `field_mob_tables.py` (ยังผิดอยู่ตามเดิม,
`0954` ไม่ได้แก้เรื่องนั้น) เงื่อนไขก่อนต่อสาย: **สาย B เขียนเทสตายพร้อมกัน `0x201F` + `916`
หนึ่งตัวใน `tests/test_mob_death.py` ก่อน** (ไม่ใช่บล็อกยาว) แล้วรายงานผลให้ chief เดินสาย
`runtime.py:3925`

## 3 ของที่รอบนี้เขียน -- สามคอมมิต, สามรอบ `pf-adversary`

### 3.1 คอมมิต `bd74ebe` -- เทสตายพร้อมกันที่ COO ขอ

`tests/test_mob_death.py::test_simultaneous_death_of_0x201f_and_916_training_iron_man`
อ่าน `mob_death.py` ทั้งโมดูล (`kill`, `commit_death`, `DeathRegister`, `DeathStep`)
และเทสเดิมก่อนเขียน fixture มอนสเตอร์ทดสอบ (`template_id=916`, `placement_index=9001`
นอกช่วง roster จริง 13 ตัว) มาจากแถวจริงใน `gamedata/tables/CONSTDATA_TH__MOBS.tsv`
(`n_ID 916`: `M016`, outfit `M016_000_000_N`, level 100/100, rank 0, `n_AI_WANDER 21`,
`n_AI_COMBAT 0`, ไม่มี drop) ตาราง MOBS **ไม่มีคอลัมน์ HP เลยสักตัว** จึงใช้ `max_hp=100`
โดยอิง convention ของ `RE-071` ติดป้าย **[สมมติของสาย B - รอ COO/chief ยืนยัน]**
ไว้ในคอมเมนต์เทสเอง (`FieldMob.actor_identity` คำนวณจาก placement_index คนละสเกลกับ
`MOBS.n_ID` -- `template_id=916` คือค่าที่ผูกกับข้อเท็จจริง ไม่ใช่ `actor_identity`)

### 3.2 คอมมิต `59a0ed5` + `ed35215` -- ช่องโหว่ที่ `pf-adversary` เจอ ไม่ใช่แค่เทสอย่างเดียว

รอบนี้เรียก `pf-adversary` **สามครั้ง** ไม่ใช่ครั้งเดียว เพราะครั้งแรกพบข้อบกพร่องจริงใน
โค้ดโปรดักชันเดิม ไม่ใช่แค่ในเทสที่เขียนรอบนี้:

1. **รอบที่ 1** (ตรวจเทส `bd74ebe`): พบว่า `mob_death.kill()` เช็ก `widened=` แค่ว่า
   "ไม่ใช่ string ว่าง" ไม่เช็กว่าเป็น mob ตัวไหน `runtime.py:3925` มีจุดเรียก
   `kill()` จุดเดียวที่ทุก identity ที่ตายวิ่งผ่าน -- ถ้า chief ทำตามตัวหนังสือของ
   คำสั่ง COO (hardcode widened= string ที่จุดนั้น) จะกลายเป็นอนุญาตให้ตัวอื่นอีก 12
   ตัวใน roster ตายได้ด้วย **รวมถึงตัวที่คำเคาะเดียวกันบอกว่ายังวางผิดที่อยู่**
   (Tornado Eagle/Toxic Vine/Fighting Fish จาก Prison Exile) -> แก้ที่คอมมิต
   `59a0ed5`: เพิ่ม `mob_death.WIDENING_RULINGS` (dict คำเคาะ -> เซ็ต `template_id`
   ที่อนุญาต) `kill()` เช็กเพิ่มว่า `mob.template_id` อยู่ใน scope ที่คำเคาะนั้นระบุจริง
2. **รอบที่ 2** (ตรวจ `59a0ed5`): พิสูจน์ด้วยสคริปต์จริงว่า string ที่ "ไม่รู้จัก" (ไม่ใช่
   key ใน `WIDENING_RULINGS`) ยัง fallback ไปพฤติกรรมเดิม (ไม่ว่าง = ผ่าน) -- ถ้า chief
   พิมพ์คำเคาะผิดแม้เล็กน้อย (paraphrase/transcribe ผิดจาก notes_to_chief) ก็ยังเปิดช่อง
   เดิมได้อีก โดยไม่ต้องตั้งใจด้วยซ้ำ -> แก้ที่คอมมิต `ed35215`: `kill()` ปฏิเสธ
   `widened=` ที่ไม่ตรง key เป๊ะทันที (fail closed) เหมือน string ว่าง ปรับเทสเดิม 3
   ตัวที่ใช้ `widened=WIDENED` ทั่วไป (ไม่เกี่ยวกับ scope gate) ให้ลงทะเบียนคำเคาะ
   ทดสอบชั่วคราวผ่าน context manager ใหม่ `registered_widening()`
3. **รอบที่ 3** (ตรวจ `ed35215`): พยายามหา bypass เพิ่ม (str subclass, whitespace
   padding, unicode normalization, race ระหว่างเทส, จุดเรียกอื่นที่พลาดไป) --
   **ไม่พบช่องเพิ่ม** ยืนยัน `runtime.py:3927-3929` ยังไม่ส่ง `widened=` เลยตอนนี้
   (แก้นี้เป็นการป้องกันล่วงหน้าก่อน chief เขียนบรรทัดนั้น ไม่ใช่การแก้บั๊กที่ยิงอยู่
   จริงบน `main` วันนี้) จุดที่ยังเหลือ (ไม่บล็อก): `registered_widening()` mutate
   dict module-level ร่วมกัน ปลอดภัยภายใต้ `unittest` sequential runner ปัจจุบัน
   แต่ไม่มี lock ถ้าสวีตเปลี่ยนไปรันแบบขนานในอนาคต (`pytest-xdist` ไม่ได้ติดตั้งตอนนี้)

**สิ่งที่เทสตายพร้อมกันพิสูจน์จริง:** สองการตายที่คำนวณจาก register generation เดียวกัน
ไม่หายไปสักตัว (`REFUSE_REGISTER_STALE` แล้ว retry ครบทั้งคู่), เฟรม dying/dead ของสองตัว
ไม่ซ้ำกัน, ตัวจับเวลาทั้งคู่ยังอยู่ฝั่งที่ถูกของ gate **สิ่งที่ยังไม่พิสูจน์ (บอกตรง ๆ):** wire
actor_identity จริงของ Training Iron Man ในเมือง (chief กำหนดตอนเดินสาย ไม่ใช่ค่า 9001 ที่
เทสใช้), HP จริงของ 916 (ไม่มีในตาราง), และ **path ที่ `runtime.py` จะเจอ 916 เลย** --
`roster` ที่ loop ที่ `3923` มองหา `mob = next(m for m in roster if m.actor_identity ==
target)` ตอนนี้คือ field-mob roster 13 ตัว (`field_mobs.load_roster()`) Training Iron
Man เป็น NPC ในเมือง คนละ roster ยังไม่มีสายเชื่อมให้ target นี้ไปถึง branch นี้ได้เลย --
**นี่เป็นงานของ chief/สาย A เพิ่มเติมนอกเหนือจากบรรทัดเดียวที่ `3925`** ไม่ใช่แค่ใส่
`widened=` (`WIDENING_RULINGS` จะรอเงียบ ๆ ไม่ทำอะไรจนกว่า target จะไปถึง `kill()` ได้จริง)

## 4 เขตเขียน

`mob_death.py` เป็นโมดูลเดิมของสาย B (M4 second half, `MOB_DEATH_LANE = "B_COMBAT"`)
อยู่ในเขตเขียนของสายนี้ ไม่ใช่การแตะไฟล์นอกเขต `runtime.py`/`app.py`/
`pf_login_game_server_v141.py` ไม่ถูกแตะเลยทั้งรอบ

## 5 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | เทสใหม่ + เทสที่แก้ทั้งหมดรันผ่าน (`mob_death` suite 67/67) · สวีตเต็มอิสระ 3 ครั้ง (หลังแต่ละคอมมิต) ล่าสุด **3469 เทส**, error 18 ตัวเดิม (`capstone`, environment เท่านั้น), skip 212, **0 FAIL ใหม่** ทุกครั้ง · `grep runtime.py` ยืนยันสด: `widened=` ยังไม่ถูกใส่ที่ `3925` (ตามคาด -- รอ chief) และ `roster` ที่ loop ใช้คือ field-mob roster ไม่ใช่ city roster (เวลาจริง ~11:0x +07:00) |
| **client-observable** | ไม่มี -- รอบนี้ไม่ใช่รอบ attended ไม่มีใครดูจอ |

## 6 ถ้าผิดต้องย้อนอะไรบ้าง

สามคอมมิต แตะสองไฟล์ (`mob_death.py`, `tests/test_mob_death.py`) ย้อนได้ทันทีด้วย
`git revert ed35215 59a0ed5 bd74ebe` (ลำดับย้อนจากล่าสุด) หรือปิด PR -- ไม่กระทบ
production path ใด ๆ เพราะ `runtime.py` ยังไม่ส่ง `widened=` เลย `WIDENING_RULINGS`
เดินอยู่เฉย ๆ

## 7 `pf-adversary` -- สามรอบ, ดูรายละเอียดที่ §3.2

## 8 รอบถัดไปควรทำอะไร

1. เช็คว่า chief เขียน `widened=` ที่ `runtime.py:3925` แล้วหรือยัง -- ถ้าเขียนแล้ว
   **ต้องไล่ต่อว่า `roster` ที่ loop ใช้พา Training Iron Man มาถึง branch นี้ได้จริง
   หรือยัง** (ดู §3.2 ท้ายย่อหน้า ยังไม่มี ณ ตอนที่เขียนรอบนี้) ถ้ายัง นั่นคืองานที่ต้อง
   เปิดใบขอ/แจ้ง chief/สาย A ต่อ ไม่ใช่แค่บรรทัดเดียวที่คิดไว้เดิม
2. ถ้า COO ออกคำเคาะขยายขอบเขตตัวใหม่อีกในอนาคต ต้องเพิ่มเข้า `mob_death.
   WIDENING_RULINGS` ด้วยชื่อคำเคาะเป๊ะ ๆ ก่อน caller ไหนจะใช้ `widened=` นั้นได้ --
   ไม่มี fallback ให้คำเคาะที่ยังไม่ได้ขึ้นทะเบียน
3. `BUILD-004` (28 ส.ค. 12:00) -- ยังพร้อม (`field_mobs`/`mob_combat`/`mob_death`
   ทั้งหมด `production_allowed = True`, wired unconditional ใน `runtime.py` ยืนยันสด
   รอบนี้) ไม่มีความเสี่ยงใหม่
4. `BUILD-005` (29 ส.ค. 23:59) -- `0x201F` พร้อมเหมือนเดิม `916` รอ chief เดินสาย
   ตามข้อ 1 ข้างบน (สองขั้น ไม่ใช่ขั้นเดียว)
5. `BUILD-006` (31 ส.ค. 12:00) -- ไม่เปลี่ยนจากรอบก่อน ครึ่งแรกเสร็จ ครึ่ง relog รอ
   gate 2/3 ของเขตเขียนเลนไอเทม ไม่ใช่ของสายนี้ ไม่ขอซ้ำ

-- **สาย B · COMBAT**
