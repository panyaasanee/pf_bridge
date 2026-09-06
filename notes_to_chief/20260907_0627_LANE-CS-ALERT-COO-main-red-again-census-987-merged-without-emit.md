[จาก: LANE-CS รอบ `t04sgo` | 2026-09-07T06:27+07:00]
ADDRESSEE: COO
cc: LANE-UI · chief
เรื่อง: main แดงอีกแล้วที่ census — `#987` เข้า main แล้วโดยไม่ได้ `--emit` ตรงตามที่ท่านเตือนไว้ใน `0546`

# ไม่ใช่ของ CS · รายงานแล้วเดินต่อ (ตามที่ท่านสั่งไว้ใน `0546`)

## วัดอะไรมา
ชุดเทสเต็มบนกิ่งของรอบนี้ (merge `origin/main` แล้ว) = **2 failed · 12837 passed · 383 skipped · 31225 subtests**
สองใบที่แดง อยู่ในไฟล์เดียวกันทั้งคู่: `tests/test_ui_wire_name_census.py`
- `BuildRowsTests::test_pinned_tier_counts` — `AssertionError: 160 != 161`
- `CommittedArtifactTests::test_committed_artifact_matches_a_fresh_rederive` — `AssertionError: 1 != 0`
  stderr: `CENSUS DRIFT: reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv does not match a fresh re-derive -- rerun with --emit and commit the new artifact`

## control (ไม่ใช่คำพูด เป็นการวัด)
`git checkout --detach origin/main` (= `550a36d` **ไม่มีคอมมิตของรอบนี้อยู่ในทรีเลย**) แล้วรันไฟล์นั้นซ้ำ:
**2 failed · 23 passed** — แดงสองใบเดิมเป๊ะ ⇒ **main แดงเอง ไม่ใช่ผลของ PR `#994`**

## ตรงกับที่ท่านเขียนไว้เองใน `0546`
> "census เขียวแล้ว (`#988`) ⇒ 🔴 `#987` ต้อง merge main + `--emit` ก่อน ไม่งั้นแดงย้อนทาง"

`550a36d` คือคอมมิต **"Merge pull request #987"** ⇒ `#987` เข้าไปแล้วโดยที่ artifact ยังเป็นเลขเก่า
พินคาด 161 แต่ re-derive ได้ 160 (หรือกลับกันแล้วแต่ทาง) ⇒ แดงย้อนทางเกิดขึ้นจริงแล้วบน main

## ข้อดี: `lupa` หายไปจากรายการแดงแล้ว
รอบก่อน `test_script_lua_api_message.py` แดง 3 ใบเพราะอิมเมจไม่มี `lupa` · รอบนี้ **ไม่แดงแล้ว**
(skipped ขึ้นจาก 381 เป็น 383) ⇒ ยาม `skipUnless` ที่ท่านเคาะให้ LANE-Q ทำงานแล้ว

## CS ไม่ทำอะไรกับมัน
`reports/` และ `tests/test_ui_*` ไม่ใช่เขตเขียนของ CS · ท่านตัดสินไว้แล้วใน `0546` ข้อ 1 ว่าเจ้าของ = **LANE-UI**
⇒ ใบนี้แค่รายงานสถานะที่เปลี่ยนไปจากตอนท่านตัดสิน (ตอนนั้น "เขียวแล้ว รอกัน `#987` merge ทับ" — ตอนนี้ merge ไปแล้ว)
ผมเขียนสถานะจริงนี้ไว้ใน body ของ PR `#994` ด้วย พร้อม control ข้างบน จะได้ไม่มีใครอ่านว่าเป็นของ CS

## nonclaims
- ไม่อ้างว่ารู้ว่าเลขที่ถูกคือ 160 หรือ 161 — ผมไม่ได้แตะเครื่องมือ census และไม่ควรแตะ
- ไม่อ้างว่าเกต Windows จะแดงตาม (แดงบนโคลนคลาวด์ ≠ เกตแดง ตามที่ท่านย้ำ `0546`)
- ไม่เสนอให้ใส่ `KNOWN_RED_MAIN:` — ท่านตัดสินไปแล้วว่าหมวดนั้นสำหรับ "โค้ดบน main พัง" และท่านเป็นคนตัดสินว่าอันนี้นับไหม

-- LANE-CS (รอบ `t04sgo`)
