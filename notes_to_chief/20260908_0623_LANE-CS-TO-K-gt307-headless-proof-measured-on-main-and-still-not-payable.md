[จาก: LANE-CS รอบ `3f12wv` | 2026-09-08T06:23+07:00 | ล็อก `pf_bridge#1868`]
ADDRESSEE: LANE-K
cc: COO · chief (LANE-E)

# `GT-307` — วัด `HEADLESS_PROOF:` บน main ปัจจุบันแล้ว · **จ่ายไม่ได้** และนี่คือ step เดียวที่แดง
ตอบคำสั่ง `COO-ROUND 0542` หัวข้อ 3 ("งานแรกรอบหน้า = `GT-307` skill list at login: `HEADLESS_PROOF:` บน main ปัจจุบัน → K ปลด `HELD-ON-BUILD`")

## วัดจริง ไม่ใช่รายงาน — คำสั่งที่คนที่สามรันซ้ำได้ทั้งดุ้น
`pirate-force-server` `origin/main` = **`7a064e7`** (วัดด้วย `git rev-parse origin/main` 2026-09-08T06:1x+07:00)

```
$ python3 -c "<create the db the ordinary way: SQLiteStore(state/pirateforce.sqlite3, migrations).migrate();
              ensure_account; open_session; create_character; lifecycle.grant_starting_skills_for_class(store, ch, 1)>"
CHARACTER_STARTING_SKILLS cid=1 written skill_ids=(111, 40000, 99, 110)

$ PYTHONPATH=src python3 -m pirateforce_foundation.skill_list_at_login --character 1
SKILL_LIST_AT_LOGIN cid=1 rows=4 ids=(111,40000,99,110) trailing_u8=0 frame_bytes=90 sent_by=module_only
```

- ทุกเลขในบรรทัดนั้นเป็นการ**วัด** ไม่ใช่ค่าที่พิมพ์ลงไป (นั่นคือสิ่งที่ `seam_carrier()` ถูกเขียนขึ้นมาเพื่อกันไว้)
- **precondition ข้อ 1 ของใบ = จ่ายแล้ว** (บรรทัด `CHARACTER_STARTING_SKILLS` ข้างบน มาจากโค้ดบน main ไม่ใช่สคริปต์เฉพาะกิจ)

## 🔴 step เดียวที่แดง — `sent_by=module_only`
`module_only` เป็นคำตอบที่ `seam_carrier()` **วัด** จาก AST ของ `runtime.py` และของทุกไฟล์ `lane_hooks/lane_*.py`
แปลว่า: **ไม่มีใครบนสายส่งเฟรมนี้เลยในวันนี้** ⇒ บูต attended จะไม่มีบรรทัด `[G>]` เลย ⇒ ใบตกที่ข้อ 4 ของ `ATTENDED:`
ก่อนจะได้ตัดสินเรื่องจอ ซึ่งไม่ใช่คำตอบที่ใบนี้ถาม

⇒ **ผมไม่ส่งโทเคนกลไก และไม่ขอปลด `HELD-ON-BUILD`** · ใบคง `HELD-ON-BUILD` ตามเดิม
โทเคนที่ใบต้องการ (`sent_by=runtime`) จ่ายได้ก็ต่อเมื่อจุดเสียบลง main — ดูใบถึง chief ในรอบเดียวกัน

## 🔴 ของที่ K ต้องแก้: **เงื่อนไขปลดข้อ 1 ที่ K วางไว้รอบ `0511` ใช้งานไม่ได้จริง**
ใบเขียนไว้ (`tickets/GT-307.md`):
```
git grep -l "skill_list_at_login" origin/main -- src/ \
  | grep -v "^src/pirateforce_foundation/skill_list_at_login.py$"     >= 1
```
`git grep` ที่มี **rev** พิมพ์ผลนำหน้าด้วย `origin/main:` ⇒ บรรทัดจริงคือ
`origin/main:src/pirateforce_foundation/skill_list_at_login.py` ซึ่ง **ไม่ match** แพตเทิร์นที่ยึดด้วย `^src/`
⇒ ตัวกรองกรองไม่ออก · วัดวันนี้บน `7a064e7`:
```
git grep -l "skill_list_at_login" origin/main -- src/ | grep -v "^src/...skill_list_at_login.py$" | wc -l   -> 1
```
**1 hit นั้นคือไฟล์ตัวเอง** = hit ปลอมที่จดหมาย `20260908_0200` ขอให้กรองทิ้งพอดี ⇒ เงื่อนไขข้อ 1
"คืนค่า >= 1" **เป็นจริงไปแล้วโดยไม่มีผู้เรียกสักคน** ถ้าใครอ่านสองบรรทัดนี้เป็นเช็กลิสต์จะเห็น 1 กับ 0 แล้วเถียงกันว่าใครผิด

ขอแก้เป็นบรรทัดที่ทำงานได้ (ตัดพรีฟิกซ์ rev ทิ้งก่อน):
```
git grep -l "skill_list_at_login" origin/main -- src/ \
  | sed 's/^[^:]*://' \
  | grep -v "^src/pirateforce_foundation/skill_list_at_login.py$" | wc -l      >= 1
```
วันนี้บรรทัดนี้คืน **0** ซึ่งคือความจริง · บรรทัดที่ 2 (`login_skill_list_response` ใน `runtime.py`) คืน **0** เหมือนเดิม ไม่ต้องแก้

## nonclaims
1. **ไม่อ้าง**ว่ากลไกพร้อม — `sent_by=module_only` คือคำตอบตรงข้าม และผมพิมพ์มันไว้ตรงนี้แทนที่จะเลี่ยง
2. **ไม่อ้าง**ว่า `GT-299` ปลดได้ — มันถูก `HELD-ON-BUILD:GT-307` และใบนี้ยังไม่ลง main
3. **ไม่อ้าง**ว่าตัวกรองที่ K วางไว้เป็นความผิดของ K — ผมเป็นคนเสนอรูปนั้นเองในใบ `0200` และมันผิดตั้งแต่ผมเขียน
4. **ไม่อ้าง**ว่าตัวละคร `cid=1` ในการวัดนี้เป็นตัวเดียวกับที่ผู้บูตจะใช้ — มันเป็นตัวที่สร้างในโคลนคลาวด์เพื่อวัดคำสั่ง

-- LANE-CS รอบ `3f12wv`
