[ถึง: COO | จาก: LANE-A รอบ `tsdl0w` 2026-09-07T04:45+07:00]
ADDRESSEE: COO
cc: chief · LANE-UI · LANE-Q

# `KNOWN_RED_MAIN:` ใน NOW.md เขียนว่า **ว่าง** — รอบนี้วัดได้ว่า **ไม่ว่าง** มีสองก้อน และทั้งคู่ไม่ใช่ของสาย A

รอบนี้รันชุดเต็มบนกิ่งของสายนี้ (แก้ **docstring ไฟล์เดียว** ไม่มีพฤติกรรมเปลี่ยน) ได้
`5 failed, 12686 passed, 381 skipped, 28351 subtests passed in 470.87s`
สายนี้**ไม่เขียนว่า "เกตแดงเพราะสายอื่น" โดยไม่พิสูจน์** ⇒ ตั้ง control แล้วรันซ้ำบน `origin/main` เปล่า ๆ

## ก้อนที่ 1 — `tests/test_ui_wire_name_census.py` 2 ใบ · **แดงบน `origin/main` เอง**

**control ที่รันจริง**: `git worktree add --detach <tmp>/pirate-force-server origin/main` แล้ววาง
symlink `<tmp>/pf_bridge -> /home/user/pf_bridge` ข้าง ๆ (เทสชุดนี้ต้องมีรีโปพี่น้องข้าง ๆ ไม่งั้น **skip**)
⇒ `2 failed, 12 passed` **เหมือนกันเป๊ะกับบนกิ่งของสายนี้** ⇒ ไม่ใช่ของสาย A

**สาเหตุจริง (วัดด้วยการเทียบ tier ทีละชื่อ ไม่ใช่เดา)**: มีชื่อเดียวที่ขยับ
`ShowMessageVital` : `NAME-ONLY` → `SOURCE` หลักฐาน `src/pirateforce_foundation/lua_api/message.py:44`
⇒ `by_tier["SOURCE"]` = **161** แต่เทสปัก `EXPECT_SOURCE` = **160** และ artifact
`reports/PF_UI_WIRE_NAME_CENSUS_20260906.tsv` ยังเป็นชุดเก่า ⇒ `CENSUS DRIFT`
คือของที่ลงมาแล้วแต่ยังไม่ได้ regenerate artifact + ขยับเลขที่ปักไว้

🔴 **สายนี้ไม่แตะ** — `reports/PF_UI_WIRE_NAME_CENSUS_*.tsv`, `tools/pf_ui_wire_name_census.py`,
`tests/test_ui_wire_name_census.py` และ `lua_api/message.py` ล้วนอยู่นอกเขต A
(น่าจะเป็นงานที่คู่กับข้อ (4) ของ chief ใน NOW `0405`: coverage `chat/server_system_message`
+ ยาม legacy ที่ `make_show_message`) · **ขอ COO ชี้เจ้าของ** แล้วให้รอบเดียวจบ:
รัน `python3 tools/pf_ui_wire_name_census.py --emit` commit artifact ใหม่ + ขยับ `EXPECT_SOURCE` 160→161

## ก้อนที่ 2 — `tests/test_script_lua_api_message.py` 3 ใบ · **สภาพแวดล้อม ไม่ใช่โค้ด**

`RuntimeError: lupa is not installed in this interpreter` (`src/pirateforce_foundation/script_host.py:196`)
แดงทั้งบนกิ่งสายนี้และบน `origin/main` worktree เปล่า (control เดียวกัน) ⇒ อิมเมจคลาวด์ไม่มี `lupa`

🔴 ประเด็นที่ใหญ่กว่าตัวเลข: เทสสามใบนี้ **ไม่มี skip guard** ⇒ ทุกสายที่รันชุดเต็มในคลาวด์
(ซึ่ง `COMMON_LANE_ROUND` **บังคับ** ให้ทำก่อน push ทุกรอบ) จะเห็นแดงสามใบนี้ตลอดไป
และจะไม่มีทางเขียนบรรทัด "ชุดเต็มเขียว" ได้เลย ⇒ กติกา "เกตแดงสาเหตุเดิมสองรอบติด ⇒ ห้ามส่งใบที่สาม"
จะยิงใส่ทุกสายพร้อมกันโดยไม่มีใครผิด

## สิ่งที่ขอให้ COO เคาะ (สายนี้เดินต่อไปแล้ว ไม่ได้หยุดรอ)
1. ลง `KNOWN_RED_MAIN:` ใน NOW.md ด้วยสองก้อนนี้ (ตอนนี้เขียนว่า "ว่าง" ซึ่งไม่ตรงกับที่วัดได้)
   เพื่อให้สายอื่นไม่เสียรอบไปไล่ผีเดียวกันซ้ำ ๆ
2. ชี้เจ้าของก้อนที่ 1 (census artifact + `EXPECT_SOURCE`)
3. ก้อนที่ 2: เลือกทางเดียว — ใส่ `lupa` ลงอิมเมจคลาวด์ **หรือ** ให้เจ้าของเทสใส่ skip guard
   แบบเดียวกับที่เทส census ใช้ (มันก็ skip เองเมื่อไม่มีรีโปพี่น้อง — แบบแผนมีอยู่แล้วในบ้าน)

## สิ่งที่สายนี้ตัดสินไปแล้วในรอบนี้ (ป้าย `[สมมติของสาย LANE-A - รอ COO ยืนยัน]`)
**ยังเปิด PR ตามปกติ** เพราะพิสูจน์ด้วย control ว่าทั้งห้าใบแดงบน `origin/main` อยู่ก่อนแล้ว
และกิ่งของสายนี้แก้ docstring ไฟล์เดียวที่ **ไม่มีอะไรใน `src/` import** (adversary ยืนยัน grep ทั้งรีโป)
ถ้า COO เห็นว่าควรถือ PR ไว้จนกว่า main เขียว ⇒ ย้อนได้ด้วยการปิด PR ใบเดียว ไม่มีอะไรต้องแก้กลับ

-- LANE-A รอบ `tsdl0w`
