# A round wjprxa -- 2026-09-05T21:04+07:00 start, ~21:30 close

## รอบนี้ขยับ NOW/M ข้อไหน

**M2 "ออกจากเมืองได้"** -- ข้อเดียวที่เหลือของ M2 (COO-DECISION `20260905_1947`,
ตอบ `RE-265`): record `+0x14` ของ M2 provisioning trial ต้องชี้แถวจริงใน
`SAILING_RESULT` แทนค่า 0 -- **แก้แล้ว, PR ขึ้นแล้ว, ยังไม่ผ่านจอ** (รอ `GT-233`
v3 attended). ข้ามขอบทะเล (งานที่สองตาม `1947` ข้อ 4) ไม่ได้แตะ -- เวลาหมดกับ
ข้อ 2+3 บวกรอบแก้ adversary D1.

## ทำอะไร

1. อ่าน `RE-265` result + `COO-DECISION 20260905_1947` เต็ม (mailbox, ADDRESSEE
   LANE-A) -- ทั้งสองบริโภคแล้ว (`.CONSUMED.txt` + สำเนาใน `consumed/`)
2. สร้าง `src/pirateforce_foundation/world_m2_sailing_result_key.py` (ใหม่):
   โหลดสำเนาคอมมิต 18 แถวของ `CONSTDATA_TH__SAILING_RESULT.tsv` ที่
   `n_AREA=126` (`world_data/world_sailing_result_area126.tsv`), ปัก
   `COPY_SHA256`, เทส re-derive จากบริดจ์จริงผ่าน
   `@BRIDGE_GAMEDATA.skip_unless_present()` (รันจริงในแซนด์บ็อกซ์นี้เพราะ
   `pf_bridge` เป็น sibling -- ไม่ skip)
3. ต่อสาย `world_m2_provisioning_trial.py::trial_survey_records()`: record
   ทั้งสองได้ `+0x14` เป็น `n_ID` จริงจากตาราง แทนค่า 0 เดิม
4. เทส: `test_world_m2_sailing_result_key.py` (ใหม่, 18 ใบ) +
   อัปเดต `test_world_m2_provisioning_trial.py` +
   `test_lane_a_scene17_roster_does_not_touch_gt233.py` (byte-pin repin ตาม
   ที่ตัวเองประกาศไว้ว่า "ปักจากต้นรอบ")
5. สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน (ตาม NOW ข้อ 29) -- เจอ D1 (ดูล่าง)
   -- แก้ในรอบนี้ก่อน push
6. เขียนใบ GT-233 v3 (ผ่าน `pf-queue-author`, ปรับ P1 ตามโค้ดจริงหลัง D1) ส่ง
   เป็นจดหมายให้ chief พลิกหัว -- `notes_to_chief/20260905_2130_LANE-A-TO-CHIEF-
   gt233-v3-real-sailing-result-key-ready-for-number.md`

## pf-adversary -- สั่งต้นรอบตาม NOW ข้อ 29 -- เจอ 1 ข้อ -- แก้ในรอบนี้

| # | เจออะไร | ทำอะไร |
|---|---|---|
| D1 | 🔴 **ร่างแรกให้ทั้งสองเกาะใช้ `n_ID` เดียวกัน** (`min()` ของ 18 แถว) -- ขัด
    COO-DECISION `1947` ข้อ 2 ตรงตัว ("ใส่**ทุกแถว**" ไม่ใช่แถวเดียวซ้ำ) + เสีย
    โอกาสวินิจฉัยของบูตเดียวที่ `GT-233` v3 ไม่มี BACKUP (COO `1348` ข้อ 2) --
    ถ้าค่าที่ใช้ร่วมกันไม่ resolve ทั้งสองเกาะจะเงียบเหมือน R318 โดยแยกไม่ออกว่า
    "แถวนี้ใช้ไม่ได้" กับ "ทฤษฎีทั้งหมดผิด" | **แก้**: `provisional_area_126_keys(n)`
    คืนค่า `n` แถวที่ต่างกัน (เกาะ 2 = `n_ID 1`, เกาะ 3 = `n_ID 2`) -- ผลผสม
    (เด้งเกาะเดียว) ตอนนี้เป็นหลักฐานได้จริง ไม่ใช่แค่ pass/fail รวม |

ไม่มี `ADVERSARY_PENDING` -- ผลกลับมาและจ่ายในรอบนี้แล้ว

## เทส

`BYTECODE_PURGED: PYTHONDONTWRITEBYTECODE=1 + python3 -B ทั้งรอบ` (ไม่ลบ
`__pycache__` -- ไม่เคยเขียน)

ระหว่างทาง (เฉพาะไฟล์ที่แตะ + เพื่อนบ้านใกล้สุด): `pytest
tests/test_world_m2_sailing_result_key.py tests/test_world_m2_provisioning_trial.py
tests/test_navigationex_survey_record.py tests/test_world_m2_survey_plan.py
tests/test_m2_survey_trial.py -q` = **137 passed, 113 subtests**

กวาดคำ `-k "world or lane_a or m2 or sailing or survey"` = **2239 passed, 0 failed**

ชุดเต็ม **รันสองครั้ง** (กติกาบังคับ): ครั้งแรกบนโค้ดก่อนแก้ D1 -- **11301
passed, 327 skipped, 0 failed** (677.82s) -- sanity ว่าต้นไม้เดิมเขียวก่อนแก้
ครั้งที่สอง (ตัวที่นับ, บน commit สุดท้ายจริง merge กับ `origin/main` `6e0e863`
แล้ว): **11307 passed, 327 skipped, 21008 subtests passed, 0 failed** (655.33s)
-- 6 ใบเพิ่มจากเทสใหม่ที่คุม D1 (`ProvisionalKeysPluralTests`)

`skip_census` ไม่ต้องซ้อมเพิ่ม -- ไฟล์เทสใหม่ไม่เพิ่ม skip (0 skip ในไฟล์ใหม่ทั้งสอง)
`tools_bridge/pf_gate_preflight.py --repo` = **PREFLIGHT PASS**

## nonclaim

- ไม่อ้างว่า `n_ID 1`/`n_ID 2` คือแถวที่ "ถูก" สำหรับเกาะ 2/เกาะ 3 -- ตารางไม่บอก
  ตัวเลือกนี้เป็น provisional ตามที่ COO สั่งไว้ตรง ๆ ไม่ใช่การเดาของสายนี้
- ไม่อ้างว่า `Common_Confirm` จะเด้งจริงบนจอ -- นั่นเป็นของ `GT-233` v3 (attended)
  ไม่ใช่ของรอบนี้
- ไม่แตะ `runtime.py`/`app.py` -- call site เดิมอ่าน default ของ
  `encode_trial_records` โดยไม่ต้องแก้ ไม่มี CORE-REQUEST ใหม่รอบนี้
- ไม่แตะเขตสายอื่น (`combat_*.json` = B, `gm/` = GM)

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว -- รอบนี้ไม่แตะสถานะโลกต่อฉากที่แก้ไขได้เลย
มีแต่ตารางนิ่ง (คอมมิตสำเนา TSV) กับฟังก์ชันอ่านอย่างเดียว

## จดหมายรอบนี้

- บริโภค: `20260905_1932_RE-265-RESULT-*.md` (`.CONSUMED.txt` + `consumed/`)
- บริโภค: `20260905_1947_COO-DECISION-re265-*.md` (`.CONSUMED.txt` + `consumed/`)
- ส่ง: `20260905_2130_LANE-A-TO-CHIEF-gt233-v3-real-sailing-result-key-ready-for-
  number.md` (ADDRESSEE: chief) -- ขอพลิกหัว `GT-233` เป็น v3, ไม่ขอเลขใหม่

## งานสำรอง 3 ข้อ (ถือไว้ทุกรอบตามคำสั่ง Panya 0904_14:4x)

1. **ข้ามขอบทะเล 304/305** (COO `1947` ข้อ 4, งานที่สองของรอบนี้ที่ไม่ได้แตะ --
   ต่อคิวรอบหน้าเป็นข้อแรก) -- ทิศเข้า 304 = `n_ID 343` / 305 = `n_ID 345`
   provisional จาก `1748`
2. **cast ของฉาก 305 (Bg3008)** -- คู่แฝดของ 304 ที่ `yob0a2` สร้างแล้ว, 55/59
   placement resolve แล้ว
3. **ฉาก 127/128 (Bermuda / Bg3002)** ocean panel อีกสองฉากที่
   `world_m2_sea_scene_cast` นับไว้แล้ว ยังไม่มีทั้งจุดมาถึงและ cast

## Status

PR เซิร์ฟเวอร์: **`pirate-force-server#852`** เปิดแล้ว ไม่ draft ·
`PF-AUTOMERGE: v4` อยู่ใน body ตั้งแต่เปิด · รอเกต · ยังไม่อยู่บน main
claim `pf_bridge#1372` เติม marker ตอนจบรอบนี้ตามลำดับ (ไฟล์รอบ + จดหมาย +
stub ลงกิ่งเดียวกัน · ลบ `_claim.md` แล้ว)

**กำหนดตก 21:21 · ปิดจริง ~21:30 (ช้า 9 นาที)** -- เหตุ: pf-adversary เจอ D1
จริง (ไม่ใช่ของปลอม) หลังชุดเต็มรอบแรกผ่านแล้ว ต้องแก้ + รันชุดเต็มซ้ำก่อน
push ตามกติกาต้นไม้ที่รันแล้วเท่านั้นถึง push ได้ -- ไม่ใช่รอบว่างงาน เขียนเหตุผล
ตรง ๆ ให้ COO เห็นแทนที่จะรายงานว่าตรงเวลาเมื่อไม่ตรง

SCOREBOARD: COMING | โค้ดที่ทำให้หน้า "รายงานกัปตัน" มีโอกาสเด้งขึ้นเองตอนเรือชน
เกาะ 2/3 (M2 เกณฑ์เดียวที่เหลือ) ขึ้น PR แล้ว รอเกต + รอ `GT-233` v3 ยืนยันบนจอ
เจ้าของ -- ผู้เล่นยังไม่เห็นหน้าต่างนี้จริงจนกว่านั้น | PR:
pirate-force-server#852, claim pf_bridge#1372, ชุดเต็ม 11307 passed/0 failed
