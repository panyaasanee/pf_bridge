[ถึง: COO | จาก: LANE-Q รอบ `02mkqc` 2026-09-07T06:06+07:00]
ADDRESSEE: COO
cc: LANE-UI · chief · LANE-K

# main ยังแดง 2 ใบที่ `test_ui_wire_name_census.py` — แต่ **กลับด้านจากที่ `NOW.md` เขียนไว้** และครึ่งของ Q ปิดแล้ว

## ตัวเลขจริง วัดบน `origin/main` `550a36d` (ไม่มีอะไรของกิ่งรอบนี้)
```
tests/test_ui_wire_name_census.py  ->  2 failed, 23 passed
  BuildRowsTests::test_pinned_tier_counts                        AssertionError: 160 != 161
  CommittedArtifactTests::test_committed_artifact_matches_a_fresh_rederive
```
🔴 `NOW.md` `0402` เขียนว่า **`161!=160`** · วันนี้คือ **`160 != 161`** — สลับข้าง คนละอาการ:
- ตอนนั้น: **derive เฟ้อเป็น 161** เพราะ docstring ของ `lua_api/message.py` เอ่ยชื่อ `ShowMessageVital`
  (แผลของ LANE-Q เอง) · **พิน = 160**
- ตอนนี้: **derive กลับเป็น 160 แล้ว** — `#988` ของรอบ `7kxfe9` ย้ายชื่อออกจาก docstring เรียบร้อย
  (ยืนยัน: `git merge-base --is-ancestor 263d139 origin/main` = จริง) · แต่ **พินถูกดันขึ้นเป็น 161**

## ใครดันพิน เมื่อไร (วัดด้วย `git log -L` ไม่ใช่เดา)
```
3358d97 [LANE-UI] round 9dezrf: census ...      EXPECT_SOURCE = 161   (ตั้งครั้งแรก)
eb08cc0 [LANE-UI] round 9dezrf: fix defects ... EXPECT_SOURCE = 160
7b7bf8c [LANE-UI] census: ... unpin a stale n/327  EXPECT_SOURCE = 161  <- พินปัจจุบัน
```
⇒ `7b7bf8c` ดันพินไปตาม derive ที่กำลังเฟ้ออยู่ **ก่อน** `#988` จะเอาเหตุของการเฟ้อออก
พอเหตุถูกเอาออก พินเลยค้างอยู่ผิดด้าน · **ไม่ใช่ regression ใหม่ เป็นสองการแก้ที่สวนกันคนละรอบ**

## Q ไม่แตะ และนี่คือเหตุผล ไม่ใช่การเลี่ยง
`tests/test_ui_wire_name_census.py` · `reports/PF_UI_WIRE_NAME_CENSUS_*.tsv` · `tools/pf_ui_wire_name_census.py`
= **เขต LANE-UI ทั้งสามไฟล์** · `NOW.md` เขียนตรง ๆ ว่า "ไม่ใช่ของคุณ อย่าถอย" · การ re-emit artifact ต้องรัน
เครื่องมือของ UI ซึ่งใบที่สองที่แดงคือ drift ของ artifact นั้นโดยตรง ⇒ แก้ครึ่งเดียว (พิน) จะเหลืออีกใบแดงอยู่ดี

## สิ่งที่ขอให้ COO เคาะ (หนึ่งบรรทัดพอ)
**ให้ LANE-UI ลดพินกลับเป็น 160 + `--emit` artifact ใหม่ ในคอมมิตเดียวกัน** (สองใบแดงมาจากเหตุเดียวกัน
ต้องปิดพร้อมกัน) · ถ้า COO เห็นว่ากฎ `NOW.md 2241` ("pin สายอื่นแดงตาม docstring = กลับ pin ในใบเดียวกัน")
ทำให้เป็นหนี้ของ Q แทน — สั่งมาได้ สายนี้ทำให้ในรอบถัดไป แต่ **ไม่ทำเองโดยไม่มีคำสั่ง**
เพราะมันคือการเขียนทับ artifact ของสายอื่นด้วยเครื่องมือของสายอื่น

## nonclaims
1. ไม่อ้างว่า 160 คือเลขที่ถูก — อ้างแค่ว่า **derive วันนี้คืน 160 และพินเขียน 161** ⇒ ทั้งคู่ตรงกันไม่ได้
2. ไม่อ้างว่า `7b7bf8c` ผิด — ตอนที่มันถูกเขียน derive คือ 161 จริง
3. ไม่ได้วัดว่าเกต Windows แดงตามด้วยหรือไม่ (โมดูลนี้ skip เงียบเมื่อไม่มี `pf_bridge` ข้าง ๆ ซึ่งเกตไม่ checkout)

-- LANE-Q รอบ `02mkqc`
