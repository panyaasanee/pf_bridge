# round `B_20260827_1549` · lane B · COMBAT -- BUILD-004 re-verified end-to-end
on a fresh flagless boot (no new production behaviour: the wiring already
landed across rounds `4z0efc`/`3lzfhw`/`s7hjdb`); mailbox consumed (RE-098 +
the ADDENDUM-v2 tool-usage reply); RE-098's bounded-negative pinned into
`field_mobs.py` so nobody reaches for `b5`/`b15`/`u32@11` as a level/rank/
spawn-rate shortcut later

**opened:** 2026-08-27 ~15:10 (+07:00) · **closed:** 2026-08-27 ~15:50 (+07:00)
**branches:** `claude/admiring-galileo-yjj034` (pirate-force-server) ·
`claude/friendly-ride-yjj034` (pf_bridge)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** **ไม่มีอะไรต่างจากเมื่อวานในเกม** — สิ่งที่ทำให้ผู้เล่น
เห็นมอนสเตอร์แดง 13 ตัวจากตาราง MOBS จริงใน Port Royal บนบูตไร้แฟล็ก (ตี/ตายได้จริง,
เมืองไม่หายตอนตี/ตาย) **ต่อสายเข้า `runtime.py` ไปแล้วในรอบก่อนหน้า** (`4z0efc`,
`3lzfhw`, `s7hjdb`) รอบนี้ตรวจซ้ำด้วยบูต headless สดจริงว่ายังทำงานถูกต้องเหมือนเดิม
(ไม่มี regression) และเพิ่มแค่เอกสาร/pin ที่ไม่กระทบพฤติกรรม (อ้าง RE-098) — ไม่มี diff
ใน `runtime.py`/`app.py`/`pf_login_game_server_v141.py` เลยทั้งรอบ

## 1 กล่องจดหมาย -- สองใบที่ยังไม่บริโภคโดยสาย B

- `notes_to_chief/20260827_0710_RE-098-RESULT-DEFINITION-PAYLOAD-NOT-DIRECT-LEVEL-RANK-SPAWNCOUNT.md`
  (ระบุถึงสาย B ตรงๆ ในหัวใบ, ไม่มี stub `.CONSUMED.txt` เดิมที่ระดับ `notes_to_chief/`
  ตรงชื่อไฟล์แม้ chief จะปิด header คิวไปแล้วในรอบ R189)
- `notes_to_chief/20260827_1450_ATTENDED-REPLY-LANE-GM-1936-use-merged_at-not-merged-addendum-v2-patched.md`
  (มี `ADDENDUM: LANE-B` ในหัวใบ, ยังไม่มี stub)

ทั้งคู่ไม่ตรงกับ ticket header ที่สาย B เปิดเองใน `CLIENT_RE_QUEUE.md`/
`GAME_TEST_QUEUE.md` (RE-098 เปิดโดยสาย RE runner ตามคำสั่ง `PANYA-ORDER 0440`,
ใบ 1450 เป็นโน้ตแก้เครื่องมือของ attended session) — จึงไม่มี header ให้แก้

### RE-098 -- ใช้จริงในงานรอบนี้ (§2)
สรุปผล: ไบต์ raw ของ definition payload (`b5`/`b15`/`u32@11`) **ไม่ใช่** level/
rank/spawn-count แบบตรง (0/30, 1/30, คงที่ตามลำดับ) `field_mobs.py`/
`field_mob_tables.py` **ไม่เคยอ่านฟิลด์พวกนี้อยู่แล้ว** (`level`/`rank`/`max_hp`
มาจาก `MOBS`/`STANDARD_MOB` ผ่าน pipeline การขุดของ
`tools/pf_mine_scene_mob_roster.py` โดยตรง) — ไม่มีอะไรต้องแก้โค้ด แต่เป็นข้อยืนยัน
ที่มีค่าพอจะปักหมุดไว้กันคนในอนาคตเผลอไปใช้ทางลัดนั้น (ดู §2)

### ใบ 1450 -- บันทึกไว้ ไม่มีอะไรให้ทำตอนนี้
คำแนะนำคือใช้ `merged_at != null` แทน `merged` ตอนเช็คว่า PR merge จริงหรือยัง
(ผ่าน GitHub list-PRs endpoint) รอบนี้สาย B ไม่มี PR เปิดค้างให้เช็ค (ไม่ push/ไม่เปิด
PR เอง ตามกฎเขตเขียน) จึงไม่มีความเสี่ยง cherry-pick ทับงานที่ merge แล้วให้แก้ — บันทึก
ไว้ใช้รอบถัดไปที่ต้องเช็คสถานะ PR ผ่าน API จริง

**ทำ:** สร้าง `notes_to_chief/<original>.CONSUMED.txt` (สองไฟล์ ที่ระดับบนของ
`notes_to_chief/` ตรงชื่อไฟล์ต้นฉบับ) + คัดลอกต้นฉบับเข้า `notes_to_chief/consumed/`
(ไฟล์ RE-098 มีอยู่แล้วในนั้นจากรอบ chief R189 — ไม่มีอะไรเปลี่ยน, ไฟล์ 1450 เป็นของใหม่)
ไม่ลบต้นฉบับจาก `notes_to_chief/`

## 2 สิ่งที่สร้าง -- ปักหมุด RE-098 ใน `field_mobs.py` (`pirate-force-server`)

`src/pirateforce_foundation/field_mobs.py`:
- เพิ่มย่อหน้าในโมดูล docstring ใต้ "WHY THE SELECTION RULE CAN BE TRUSTED" อ้าง
  RE-098 ตรงๆ (ตัวเลข 0/30, 1/30, ค่าคงที่ 100) บอกว่าโมดูลนี้ไม่เคยอ่าน
  `b5`/`b15`/`u32@11` อยู่แล้ว — `level`/`rank`/`max_hp` มาจาก MOBS/STANDARD_MOB
  ผ่าน pipeline จริง
- เพิ่มบรรทัดใน `pin_document()`'s `nonclaims` list อ้าง RE-098 เดียวกัน (ให้คนอ่าน
  pin แล้วเห็นโดยไม่ต้องเปิด docstring)
- regenerate `scenarios/field_mobs_hostile_001.json` ให้ตรงกับ `pin_document()`
  ที่เปลี่ยน (ใช้ `json.dump(..., indent=2)` ตัวเดียวกับไฟล์เดิม, diff สะอาด — เพิ่ม
  แค่ 1 บรรทัดใน `nonclaims`)

**ไม่แตะ:** `field_mob_tables.py` (GENERATED - do not hand-edit ตามหัวไฟล์เอง),
`tools/` (นอกเขตเขียนของสาย B), `runtime.py`/`app.py`

### `pf-adversary` ตัวเอง
มิวเทตข้อความ nonclaim ใหม่ให้ผิด (`"...come from somewhere else entirely"`) →
`tests/test_field_mobs.py::test_the_committed_pin_is_what_the_code_produces`
ล้มด้วย `AssertionError` ที่เทียบ dict ตรงๆ (ไม่ใช่ byte-for-byte ของไฟล์ แต่เทียบ
`json.loads(committed) == field_mobs.pin_document(legacy)`) → revert กลับ (`git
diff` ยืนยันว่าเหลือแค่การเพิ่มที่ตั้งใจ 19 บรรทัด ไม่มีอะไรหลงเหลือ) → รันซ้ำเขียว —
ยืนยันว่า pin-drift guard ที่มีอยู่แล้วจับการแก้ nonclaims ได้จริง ไม่ vacuous

## 3 ตรวจซ้ำ BUILD-004 แบบสดบนลำดับจริง (login → StartGame → TargetPos → โจมตี/ฆ่า)

รันเทสที่ขับลำดับจริง (ไม่ใช่แค่เรียก encoder ลอยๆ) สดใหม่รอบนี้:

```
tests/test_mob_combat_dispatch.py::test_a_hit_after_real_arrival_recomposes_the_bar_frame_over_115   PASSED
tests/test_mob_combat_dispatch.py::test_a_kill_after_real_arrival_recomposes_dying_and_dead_over_115  PASSED
```

คอนโซลที่พิมพ์จริง (บูตไร้แฟล็ก, ไม่มี `--*-scenario` ตัวไหนทำงาน):

```
PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game
MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13 missing=none
WORLD_CENSUS assembled=115/115 wire=115 bodies=ok pc=21007B frame=21021B anchor=(-9239.957,-2830.045,223.292) reapply_ms=3000 source=full_census shortfall=none
```

อ่านเป็นตัวเลข: **13/13 มอนจริงจากตาราง MOBS ถูก override เป็นร่างศัตรู+มีชื่อ**
บนบูตไร้แฟล็ก, สำมะโนทั้งเมืองยัง **115/115** ทั้งก่อนและหลังตี/หลังฆ่า (world-wipe
fix ยังทำงาน — ไม่ใช่แค่ยืนยันครั้งเดียวรอบก่อน แต่รันซ้ำสดวันนี้แล้วผลเดิม)

รันสวีตที่เกี่ยวข้องเต็ม: `test_field_mobs.py` (20) + `test_mob_death.py` +
`test_mob_combat_dispatch.py` + `test_world_census_wiring.py` = **130 passed, 14
subtests passed** สวีตเต็มอิสระทั้งรีโป (`PYTHONPATH=.`): **3370 passed, 212
skipped, 17 errors (เดิมทั้งหมด — `ModuleNotFoundError: No module named
'tools'`/`capstone`, ปัญหา environment ไม่ใช่โค้ด), 5001 subtests passed, 0 FAIL
ใหม่** — ตัวเลขเท่ากับ baseline ที่วัดก่อนแก้อะไรเลยในรอบนี้ (รันสองครั้ง เทียบกันแล้ว)

## 4 item G (world-wipe fix + headless proof สำหรับ `GT-084-R2`) -- ตรวจแล้ว: ทำเสร็จ
ไปแล้วในรอบ `s7hjdb` (13:49), ไม่มีอะไรให้ทำซ้ำ

เช็ค `src/pirateforce_foundation/lane_hooks/` ก่อน: **ไม่มีอยู่จริง** ในรอบนี้ (สิทธิ์
พิเศษยังไม่หมดอายุ) แต่เมื่ออ่านโค้ดจริงที่ `runtime.py` รอบบล็อก `MOB_COMBAT_BAR`/
`MOB_DEATH_DYING`/`MOB_DEATH_DEAD` (บรรทัดขยับจากที่คำสั่งอ้างแล้ว) พบว่า
`mob_death.hostile_census_frames()` ถูกเรียกอยู่แล้วทั้งสองจุด พร้อม fail-closed
guard และ console gate `MOB_COMBAT_BAR_CENSUS_RECOMPOSE`/
`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE` — **เกณฑ์ปิดของ `PANYA-ORDER 12:30 §3`
(บูต headless ไร้แฟล็ก → ตี 1 + ตาย 1 → census หลังเหตุการณ์ยัง 115/115,
คอมมิตซ้ำได้) ทำเสร็จและคอมมิตไปแล้วในรอบ `s7hjdb`** (สองเทสที่รันซ้ำใน §3 ข้างบน
คือหลักฐานนั้น ไม่ใช่หลักฐานใหม่) จึงไม่ได้ใช้สิทธิ์แก้ `runtime.py` รอบนี้ เพราะไม่มี
บล็อกให้แก้ ตรงกับที่รอบ `s7hjdb` เองสรุปไว้แล้ว

🔴 **ไม่แก้ `GAME_TEST_QUEUE.md` เอง** แม้คำสั่งรอบนี้บอกให้ "เติมบรรทัด
`พร้อมสำหรับ GT-084-R2`" — ไฟล์นี้ไม่อยู่ในเขตเขียนของสาย B ตามกฎ 6 ข้อของรอบนี้เอง
(รายการเขตเขียนไม่มี `GAME_TEST_QUEUE.md`) และ `notes_to_chief/README.md`
บันทึกไว้ชัดว่า **"chief เป็นคนเขียนไฟล์ใหญ่คนเดียว = ไม่มีวันชนกัน"** — รอบ `s7hjdb`
ก็ทำแบบเดียวกัน (ส่งจดหมายให้ chief แทนแก้ไฟล์เอง) เขียนในจดหมายนี้แทน: **หลักฐาน
พร้อมสำหรับ `GT-084-R2` แล้วตั้งแต่รอบ `s7hjdb`, รอบนี้ยืนยันซ้ำสดว่ายังจริง** —
chief/COO อ่านแล้วเติมบรรทัดในไฟล์ของตัวเองได้เลย (ไม่ต้องรอบข้ามการแก้)

## 5 ไฟล์ที่แตะ

`pirate-force-server` (2 ไฟล์):
- `src/pirateforce_foundation/field_mobs.py` -- +19 บรรทัด (docstring + nonclaim
  อ้าง RE-098), ไม่แก้พฤติกรรม/ไม่มีฟิลด์ใหม่
- `scenarios/field_mobs_hostile_001.json` -- regenerate ให้ตรงกับ `pin_document()`
  (+1 บรรทัดใน `nonclaims`)

`pf_bridge` (4 ไฟล์ใหม่):
- `notes_to_chief/20260827_0710_RE-098-RESULT-DEFINITION-PAYLOAD-NOT-DIRECT-LEVEL-RANK-SPAWNCOUNT.md.CONSUMED.txt`
- `notes_to_chief/20260827_1450_ATTENDED-REPLY-LANE-GM-1936-use-merged_at-not-merged-addendum-v2-patched.md.CONSUMED.txt`
- `notes_to_chief/consumed/20260827_1450_ATTENDED-REPLY-LANE-GM-1936-use-merged_at-not-merged-addendum-v2-patched.md`
  (คัดลอก, ไม่ลบต้นฉบับ)
- `rounds/B_20260827_1549_build004_reverify_and_re098_consumed.md` (ใบนี้)

## 6 ตัวเลขที่วัดได้ (สรุปรวม)

- assembled/matched: **13/13 field-mob ถูก override เป็นร่างศัตรู+มีชื่อ**, **115/115
  สำมะโนทั้งฉาก** (ก่อนตี/หลังตี/หลังฆ่า เท่ากันทั้งสามจุดที่วัด)
  ไม่มีการลดตัวเลขไหนเงียบๆ
- เทสที่เกี่ยวข้องตรง: 130 passed / 14 subtests
- สวีตเต็ม: 3370 passed, 212 skipped, 17 errors (environment เดิม), 0 FAIL ใหม่
  (เทียบ baseline ก่อนแก้ในรอบนี้ ตัวเลขเท่ากันทุกตัว)

## 7 ยังไม่ได้พิสูจน์ (ต้องมีคนนั่งหน้าจอเกม)

ทุกอย่างในรอบนี้เป็นชั้น wire/DB/headless เท่านั้น — **ไม่มีใครเห็นชื่อ/แถบเลือดสีแดง
บนจอไคลเอนต์จริงในรอบนี้** คำถามนั้นเปิดอยู่ที่ `GT-084-R2` (attended, PENDING ใน
`GAME_TEST_QUEUE.md`) ตามเดิม — รอบนี้ไม่เปลี่ยนสถานะนั้น

## 8 รอบถัดไปควรทำอะไร (สาย B)

1. ตรวจว่า chief/COO เติมบรรทัดพร้อมของ `GT-084-R2` ใน `GAME_TEST_QUEUE.md`
   แล้วหรือยัง (§4)
2. ตรวจว่า `lane_hooks/` ลง `main` หรือยัง — ถ้าใช่ ย้ายงาน CORE-REQUEST ค้างไป
   เขียนเองที่ `lane_hooks/lane_b_*.py`
3. `combat_aggro` tick loop ยังไม่ต่อสายเข้า `runtime.py` -- เส้นตาย `BUILD-005`
   29 ส.ค. 23:59 (ไม่ใช่งานของรอบนี้ แต่ใกล้ครบกำหนดขึ้นเรื่อยๆ)
4. `GT-060`/`combat_pickup` (THE WALL) ยังรอ attended capture

-- **สาย B · COMBAT**
