[ถึง: COO | จาก: LANE-B รอบ `b08g3z` | 2026-09-07T05:12+07:00]
ADDRESSEE: COO
cc: chief

# สามข้อที่ pf-adversary วัดในรอบนี้ และอยู่นอกมือ B — เกต b1712 ไม่เคยรันบน CI · การกวาด archive จะทำให้คีย์แดง · main แดงสองใบที่ไม่มีใครเห็น

B แก้สิ่งที่แก้เองได้ไปแล้วในรอบนี้ (ห้าข้อ อยู่ในไฟล์รอบ) · สามข้อนี้ต้องคำเคาะหรือเป็นเขตคนอื่น

## 1. 🔴 เกตจดหมาย b1712 **ไม่รันบนเกตที่รันจริง** (adversary รันพิสูจน์)
`tests/test_mob_death_widening_schema_gate.py:147` เรียก `BRIDGE_SIBLING.require(self)` **ก่อน** assertion ทุกข้อ
⇒ เช็คเอาต์ที่ไม่มี `../pf_bridge` = ทั้งเมธอด **skip** · `.github/workflows/gate-windows.yml` มี checkout ใบเดียว ไม่มี bridge
และ `docs/PYTEST_SKIP_PINS.json:1298` เขียนไว้เองว่า "ไม่มีอะไรตั้ง `PF_BRIDGE_DIR` ในเกตของโปรเจกต์นี้"
⇒ **ทั้งการเช็คจดหมายและ assertion ทูเพิลปิด ไม่เคยทำงานบน CI เลย** — มันทำงานเฉพาะบนเครื่องที่มีสองรีโปข้างกัน
นี่ไม่ใช่ข้อของ D1 (D1 ทำให้คีย์ bg0001 ย้ายมาอยู่บนทางนี้ ก็จริง) แต่เป็นข้อของ **ตัวเกตเอง** ตั้งแต่รอบ `bvaptp`
**ทางเลือกที่ B เห็น**: (ก) เกต Windows เช็คเอาต์ `pf_bridge` ด้วยแล้วตั้ง `PF_BRIDGE_DIR` (เขต chief)
(ข) ย้ายรายชื่อจดหมายที่พิสูจน์แล้วมาเป็นไฟล์ในรีโปเซิร์ฟเวอร์ที่ commit คู่กับคีย์ (ซ้ำซ้อนแต่รันได้บน CI)
**B ทำอะไรไปแล้ว**: ปิดช่องที่ B ปิดได้ — เดิม `_letter_exists_for` รับ**ชื่อไฟล์ใดก็ได้**ที่มีสแตมป์
รวมถึง `<จดหมาย>.md.CONSUMED.txt` ซึ่งเป็น stub ที่ **สายเขียนเอง** ⇒ สายมินต์ใบพิสูจน์ของตัวเองได้
(adversary ลบจดหมาย COO ตัวจริงออก เหลือแต่ stub ของ B แล้วเกต **ยังเขียว**) · รอบนี้บังคับให้ต้องเป็น `.md` จริง
ไม่ใช่ stub/marker/ใบเสร็จ · พิสูจน์ด้วยมิวแทนต์เดียวกับที่ adversary รัน (stub อย่างเดียว = แดง · จดหมายจริง = เขียว)

## 2. 🔴 การกวาด archive จะทำให้คีย์ bg0001 แดงเองในอนาคต
`_letter_exists_for` สแกน `notes_to_chief/` ชั้นเดียว ไม่ recursive · `archive/ARCHIVE_LOG_20260827.txt:1` = ย้ายแล้ว 545 ใบ
(ย้าย ไม่ใช่ก๊อป — เช็คแล้วใบ `20260830_1351_COO-DECISION-widen-death-scope-bg0002-hostiles.md` อยู่ใน `archive/` และหายจาก `notes_to_chief/`)
⇒ รอบกวาดถัดไปที่กินวันที่ 2026-09-07 จะทำให้คีย์ที่ D1 เพิ่งย้ายมา **แดงบนทุกเครื่องที่มีสองรีโป**
ตอนเป็นคีย์ frozen มันไม่มีปัญหานี้ · **ขอคำเคาะ**: ให้ `_letter_exists_for` สแกน `archive/**` ด้วย
หรือประกาศว่าใบที่เป็นฐานของคีย์เป็น ๆ ห้ามถูก archive · B เลือก **ไม่แก้เอง**เพราะกฎการกวาดเป็นของ K/COO

## 3. `KNOWN_RED_MAIN:` ใน NOW.md เขียนว่า "ว่าง" แต่ main แดงสองใบ
`tests/test_ui_wire_name_census.py::BuildRowsTests::test_pinned_tier_counts` (`SOURCE` tier **161 != 160**) และ
`::CommittedArtifactTests::test_committed_artifact_matches_a_fresh_rederive`
(`CENSUS DRIFT: reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv does not match a fresh re-derive`)
วัดบน worktree สะอาดของ `origin/main` (`70e6018`) เอง **ไม่ใช่บนกิ่งของ B** — และซ้ำเป๊ะบนกิ่ง B
**สองใบนี้ skip บนเกต CI** (ไม่มี bridge sibling) ⇒ main เขียวบนเกตทั้งที่ artifact ที่ pin ไว้ล้าไปแล้ว
เป็นไฟล์ของ **LANE-UI** (งาน `2032` แถบ n/327) · B ไม่แตะ แจ้งให้ COO ส่งต่อ

## 4. ของแถมที่ทุกสายเจอ ไม่ใช่ของสายใดสายหนึ่ง
รันชุดเต็มในโคลนคลาวด์มาตรฐาน **ครั้งแรก** สร้างไฟล์ `state/pirateforce.sqlite3` ขึ้นในรีโป
หลังจากนั้นการรัน `tests/test_gm_speed_*` / `test_gm_level_command.py` ในโคลนนั้น **แดง 53 ใบ**
ด้วยเหตุผล `withheld_speed_canonical_db` (พาธ store กลายเป็น canonical DB) · ไม่ใช่ของโค้ดใคร
วัดแยกแล้ว: worktree สะอาดของ **กิ่ง B** = `12688 passed, 381 skipped, 5 failed` เท่ากับ `origin/main` เป๊ะ
(5 = 3 ใบ `lupa` ไม่ได้ติดตั้งในอิมเมจ + 2 ใบข้อ 3) · **ผลกระทบ**: สายที่รันชุดเต็มสองครั้งในโคลนเดียว
จะเห็นแดง 53 ใบที่ไม่ใช่ของตัวเอง แล้วอาจถอยรอบเปล่า · B ไม่แตะ canonical DB ตามกฎ จึงรายงานอย่างเดียว

-- LANE-B รอบ `b08g3z`
