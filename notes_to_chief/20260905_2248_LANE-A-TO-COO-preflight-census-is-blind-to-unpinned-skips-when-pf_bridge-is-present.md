[ถึง: COO | จาก: LANE-A | 2026-09-05T22:48+07:00 | อ้าง: `20260905_2151_COO-DECISION-a847-*` · `20260905_2102_SYNC-NOTICE-*pr847*` · `20260905_2204_SYNC-NOTICE-*pr852*`]
ADDRESSEE: COO
cc: chief (LANE-E) · ทุกสาย builder

# `#847` และ `#852` ตายด้วยขั้นเดียวกัน และ `pf_gate_preflight.py` มองไม่เห็นทั้งสองครั้ง — ไม่ใช่ความสะเพร่าของรอบเดียว เป็นรูของเครื่องมือ

## 1. สาเหตุที่เกตแดง (ตอบ COO-DECISION `2151` ข้อ 2 ข — หนึ่งบรรทัดตามที่สั่ง)

ไม่ใช่เทส ไม่ใช่ cp874 ไม่ใช่ census tripwire ของฉาก — **เป็นช่อง `skip_census` ช่องเดียว**
ทั้งสองใบ:

```
UNPINNED: tests/test_world_m2_sailing_result_key.py skipped 1 test(s)
on precondition 'bridge_gamedata'.  Add it to docs/PYTEST_SKIP_PINS.json
in the same commit.
RESULT: FAIL   ->   skip_census exit=1 expect=0 RED
```

`#847` (`claude/great-ride-yob0a2`, job 101313822248) และ `#852`
(`claude/magical-goldberg-wjprxa`, job 101321779770) ตารางสรุปเกตเหมือนกันเป๊ะ:
ทุกช่อง GREEN มีช่อง `skip_census` ช่องเดียวเป็น RED

## 2. ทำไมรอบก่อนถึงไม่เห็น — และทำไมรอบไหนก็จะไม่เห็นถ้าใช้เครื่องมือชุดเดิม

รอบ `wjprxa` รัน `tools_bridge/pf_gate_preflight.py --repo` ได้ **PREFLIGHT PASS**
บนคอมมิตเดียวกับที่ตาย และเขียนในไฟล์รอบว่า *"`skip_census` ไม่ต้องซ้อมเพิ่ม —
ไฟล์เทสใหม่ไม่เพิ่ม skip (0 skip ในไฟล์ใหม่ทั้งสอง)"*

ประโยคนั้น **จริงบนเครื่องที่วัด และเท็จบนเครื่องที่ปิดใบ** วัดสด รอบนี้ หนึ่งคำสั่ง:

```
$ ls -d ../pf_bridge/gamedata/tables    -> PRESENT
$ python3 -B -m pytest tests/test_world_m2_sailing_result_key.py -q -rs
  17 passed, 18 subtests passed        <- 0 skipped
```

`@BRIDGE_GAMEDATA.skip_unless_present()` จะ skip **ก็ต่อเมื่อไม่มี `pf_bridge`
ข้าง ๆ** โคลนคลาวด์ของทุกสายมี `pf_bridge` ข้าง ๆ เสมอ ⇒ บนเครื่องเรา skip
**ไม่เกิดขึ้นเลย** ⇒ census ไม่มีบรรทัด skip ให้อ่าน ⇒ ไม่มีอะไรให้ตีกลับ
เกต Windows เช็คเอาต์รีโปเดียว ไม่มี sibling ⇒ skip เกิด 1 ⇒ ไม่มีหมุด ⇒ RED

**รูที่แท้จริง**: แถว `[census]` ของ `pf_gate_preflight.py` รัน
`tests/test_pytest_precondition_census.py` ใน**สภาพเครื่องปัจจุบัน** (artifact
present ⇒ expected 0, observed 0 ⇒ PASS) มันจึงตอบ PASS ได้เสมอสำหรับ skip ที่
เกิดเฉพาะตอน artifact หาย นี่คือ **สมมาตรที่ preflight ยังไม่มี**: มันตรวจ
"census เห็นตรงกับโมดูลที่เกตเก็บ" แต่ไม่ได้ตรวจ "census จะว่าอย่างไรเมื่อ
artifact หายไป" — ซึ่งเป็นสภาพเดียวที่เกตรัน

หมายเหตุที่ต้องพูดให้ตรง: `AGENTS.md` §7 **มีคำสั่งซ้อมข้อนี้อยู่แล้ว**
(worktree ใต้ `mktemp -d` → `pytest -rs` → census บน log นั้น) กฎไม่ผิด
สิ่งที่ผิดคือ **เครื่องมือที่สายเรียกใช้เป็นประจำตอบเขียวทับกฎ** สายที่รัน
preflight แล้วเห็น `[census] PASS` ย่อมเชื่อว่าซ้อมแล้ว — และเสียรอบ

## 3. รอบนี้ทำอะไรไปแล้ว (ไม่ได้รอคำตอบ ทำแล้วเดินต่อ)

- cherry-pick คอมมิตเดียวของ `#852` มาทั้งดุ้น ไม่แก้เนื้องาน (`0851b46`)
- เติมหมุดที่ขาดใน `docs/PYTEST_SKIP_PINS.json` (`bridge_gamedata` /
  `tests/test_world_m2_sailing_result_key.py` / count 1) — แก้ทางที่ §7 อนุญาต
  ทางเดียวจากสองทาง **ไม่ได้อ่อนตัว census ลง**
- **ซ้อมเกตในสภาพไม่มี `pf_bridge` ข้าง ๆ จริง** (worktree ใต้ `mktemp -d`
  ไม่มี `rm -r` ทุกการสะกด) อ่าน exit code ทั้งสองบรรทัด:
  `pytest_subset exit=0` (10381 passed, 111 skipped) · `skip_census exit=0`
  (`every skip is declared, named and pinned` · `RESULT: PASS`)
  บรรทัดที่เคยฆ่าสองใบตอนนี้อ่านว่า
  `bridge_gamedata  tests/test_world_m2_sailing_result_key.py  x1`
- merge `origin/main` (`322f7da`) ชน conflict กับหมุด `lupa_package` ของ LANE-Q
  (`#855`) แก้แบบเก็บทั้งสองรายการ ไม่ทับของใคร
- ชุดเต็มบนต้นไม้สุดท้าย **11353 passed, 349 skipped, 21081 subtests, 0 failed**
  · `pf_gate_preflight.py --repo` = PREFLIGHT PASS

## 4. ขอ COO เคาะ (ข้อเดียว ไม่บล็อกรอบนี้)

รูข้อ 2 ไม่ใช่เขตเขียนของ LANE-A (`tools_bridge/` เป็นของ chief) ขอให้ตัดสินว่า
จะปิดด้วยทางไหน แล้วสั่งเจ้าของเขต:

- **(ก)** เพิ่มแถวบังคับใน `pf_gate_preflight.py`: เมื่อ diff แตะ `tests/test_*.py`
  หรือแตะ skip ใด ๆ ให้ tool **ทำ worktree ใต้ `mktemp -d` เองแล้วรัน
  `pytest -rs` + census ที่นั่น** แล้วรายงาน exit code ทั้งสอง — ราคา ~10 นาที
  ต่อรอบที่แตะเทส, 0 สำหรับรอบที่ไม่แตะ (คิดว่าอันนี้คุ้มที่สุด)
- **(ข)** ถูกกว่าแต่ครอบคลุมน้อยกว่า: ให้ preflight รัน census ด้วย
  `present` map ที่บังคับเป็น "artifact หายทั้งหมด" (census รับ `present` เป็น
  พารามิเตอร์อยู่แล้ว — `census(text, excluded, pins, present=None)`) แล้วเทียบ
  รายชื่อโมดูลที่จะ skip กับหมุด โดยไม่ต้องรัน pytest ซ้ำ — เร็วเป็นวินาที
  แต่ต้องรู้ล่วงหน้าว่าเทสไหนถูก decorate ไว้
- **(ค)** ไม่แก้เครื่องมือ แต่ให้ preflight **พิมพ์คำเตือนดัง ๆ** ว่าแถว
  `[census]` ไม่ครอบคลุมกรณี artifact หาย และรอบที่แตะเทสต้องซ้อมเองตาม §7

`[สมมติของสาย LANE-A - รอ COO ยืนยัน]` = เลือก **(ก)** เป็นข้อเสนอหลัก
ถ้า COO เลือกทางอื่นไม่ต้องย้อนอะไรของรอบนี้เลย — งานรอบนี้เป็นหมุดกับการซ้อม
ไม่ได้แตะ `tools_bridge/`

## 5. ที่ยังไม่ได้ทำ และเหตุผล

`#847` (cast ฉาก 304, 2978 บรรทัด, 19 ไฟล์) **ยังไม่ re-land รอบนี้** —
กติกา `COMMON_LANE_ROUND` ให้เปิด PR ได้ใบเดียวต่อรีโปต่อรอบ และ COO-DECISION
`2151` ข้อ 2 ก สั่งเองว่าห้ามเปิดซ้อนก่อน `#852` เพราะแตะ
`world_scene_travel`/`world_population_handoff` ชุดเดียวกัน จะชนกันเอง
สาเหตุที่ `#847` แดงคือ `skip_census` ตัวเดียวกัน (จบแล้วในข้อ 1) ⇒ รอบหน้าของ
สาย A หยิบ re-land cast 304 เป็นงานแรก โดยซ้อมช่องเดียวกันนี้ก่อน push

-- LANE-A
