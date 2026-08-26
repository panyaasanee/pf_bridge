# รอบ `A_20260826_1833` · สาย A · WORLD (`pf-builder`)
# `BUILD-001`: NPC ใน Port Royal ได้ป้ายชื่อคืน — แก้ครึ่งหนึ่งของสิ่งที่ `GT-078` ปฏิเสธ

**เวลา:** 2026-08-26 18:33 -> 19:3x (+07:00) · **รอบ:** cloud routine `yxbbc4`
**ล็อกของสาย:** PR หัวข้อ `[LANE-A]` ที่เปิดค้าง = 0 ใบ (repo `pirate-force-server`) ตอนเริ่มรอบ
**ล็อกจริงพลาดกฎ:** เปิด PR ไม่สำเร็จตอนต้นรอบ (`create_pull_request` สองครั้งแรกล้มเหลว — "no commits between main and branch" เพราะยังไม่มี commit ใด ๆ บนสาขา) แล้ว**ลืมลองใหม่**หลัง commit แรกเสร็จ — เดินหน้าทำงานทั้งรอบโดยไม่มี PR เปิดค้างเป็นล็อกจริง จนมาเปิดสำเร็จตอนจบรอบเป็น **PR #73** 🔴 **นี่คือรูรั่วของกติกาที่ต้องจดไว้ ไม่ใช่ครั้งเดียวจบ**: ระหว่างที่ไม่มีล็อก มีสายอื่นเปิด/merge PR #69-72 ไปโดยไม่มีใครชนกับ LANE-A แต่เป็นโชคดี ไม่ใช่ระบบทำงานถูก
**ไม่แตะ PR ของสายอื่น** (`#69` LANE-GM, `#70` LANE-B merged ระหว่างรอบ, `#71` LANE-E)
**branch:** `claude/eloquent-thompson-yxbbc4` (pirate-force-server, จาก `main` ตอนนั้น)

---

## ① ปัญหาที่แก้จริง

`GT-078` (M1 acceptance) เจ้าของรัน 2026-08-26 12:55-13:37 (+07:00): ชั้น wire/placement **PASS** (115/115 ตัว ตำแหน่งถูก) แต่ **OWNER-REJECTED ชั้น identity** — NPC ทุกตัวในเมืองไม่มีป้ายชื่อเลย มีแต่ title บรรทัดเดียว และหลายตัวเป็นคนละตัวกับเซิร์ฟเวอร์ต้นฉบับ (ดู `notes_to_chief/consumed/20260826_1430_GT078-RESULT-*.md` + `20260826_1440_GT078-ADDENDUM-*.md` + `COO-DECISION` `20260826_1442`)

`pf-static-re` (dispatch แรกของรอบนี้) เจอกลไก: ไคลเอนต์วาดป้ายชื่อสีเหลืองก็ต่อเมื่อ `BasicAttr` bit `0x0001` ถูกตั้ง ผ่าน `basic_name` ที่ไม่ว่างเปล่าใน `make_npc_attr()` (`current/pf_login_game_server_v141.py:1139-1178`, ห่วงโซ่ static 0x466EB0/0x4656F0/0x89A810/0x51F920) และ `src/pirateforce_foundation/world_population.py::_entry()` ส่ง `basic_name=""` ให้ทุก placement ยกเว้น P30 diagnostic override — **ทั้งที่ทุกหนึ่งใน 115 แถวของ `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` (v141) มีชื่อจริงอยู่แล้วในฟิลด์ที่ 7 (`source_name`)** เช่น P0=`Navy Transfer`, P91=`Local people`, P35/65/140=`Columbus` — ไม่เคยถูกใช้เลยตั้งแต่โมดูลนี้ถูกสร้าง (round `jjxgz3`, วันเดียวกัน ตอน 00:22)

🔴 **สิ่งที่ยังไม่แก้ (แยกเรื่องกันชัดเจน):** ตัว template_id/identity ที่ผิดตัว (Hields/Sase ที่ม้านั่งลานกลางเมือง) — พิกัดของสอง NPC นี้**ไม่มีอยู่ในตารางที่ commit ไว้เลย** (`bg0001.placements.tsv` grep `159`/`796` = 0 hit, grep 312 ไฟล์ lua = 0 hit) ต้องถอดรหัส placement block ชนิดที่สอง ที่ยังไม่มีใครเปิดมาก่อน (ceiling ของ block "Mob_Set" หยุดที่ 113 definitions แต่ placements จริงมี 149 แถว — ช่องว่างนี้น่าจะเป็นที่อยู่ของ NPC บริการอย่าง Hields/Sase) — **เปิดใบให้สาย RE ตามกฎ** ท้ายรอบ

## ② การแก้

`src/pirateforce_foundation/world_population.py::_entry()`:
```
เดิม : basic_name=(legacy.V119_P30_TARGET_NAME if is_monster else ""),
ใหม่ : basic_name=(legacy.V119_P30_TARGET_NAME if is_monster else placement.source_name),
```
ไม่แตะว่า template_id ไหนถูกส่ง (คนละบั๊กกับ Hields/Sase) · ไม่แตะเงื่อนไข `is_monster`/P30 (ใช้เป็น control ของเลนวัดอื่น)

## ③ `pf-adversary` — ไม่อนุมัติรอบแรก 2 ข้อ ทั้งคู่แก้แล้ว

| # | สิ่งที่ RED ยิง | ผล |
|---|---|---|
| 1 | Docstring เดิมใน `world_population.py` อ้างว่า rung 3 byte-identical กับ `make_v112_monster_shop_population_state()` และทุกตัวไม่มีชื่อ — ทั้งคู่เท็จตั้งแต่การแก้นี้ | ✅ ขีดฆ่า (ไม่ลบ) + เขียน AMENDMENT ลงวันที่อธิบายว่าเปลี่ยนอะไรและทำไม |
| 2 | เงื่อนไข P30 (`V119_P30_TARGET_NAME` vs `placement.source_name`) ไม่มีเทสคุมเลย — ชื่อทั้งสองบังเอิญเป็น `"Tornado Eagle"` เหมือนกันวันนี้ พิสูจน์ด้วย mutation ว่าลบเงื่อนไขทิ้ง (ให้ทุกตัวใช้ `source_name` รวม P30) เทสที่เกี่ยวข้องทั้ง 134 ตัวยังผ่านหมด | ✅ เพิ่มเทสบังคับให้สองค่าต่างกัน (drifted legacy stand-in) แล้วยืนยันว่า override ชนะ |

RED ยังตรวจเลขไบต์/hash ที่ pf-builder คำนวณใหม่ทั้งหมดด้วยตัวเอง (ไม่เชื่อ diff เฉย ๆ) ตรงทุกตัว · ยืนยัน P30 control frame ไม่ถูกแตะ (`current/pf_login_game_server_v141.py` diff = 0) · ยืนยันว่าเทสใหม่จะจับบั๊กเดิมได้จริง (revert แล้วเทสแดง) · ไม่พบปัญหา non-ASCII/ความยาวชื่อ (ชื่อยาวสุด 33 ตัวอักษร ทุกตัว ASCII)

## ④ ของที่ commit จริง (3 commits, PR #73, ยังไม่ merge)

- `72a0ac8` การแก้หลัก
- `f6580e0` ปรับเทส/pin ที่ hardcode byte-exact ไว้ (6 ไฟล์: `scenarios/world_population_full_001.json`, `tests/test_world_population.py`, `tests/test_world_census_wiring.py`, `tests/test_population_adapter.py`, `tests/test_ground_loot_dispatch.py`, `tests/test_ground_loot_nameprop_hypothesis.py`) — เก็บค่าเดิมไว้ในคอมเมนต์/amendment ไม่ลบ
- `00299dd` แก้ 2 ข้อของ `pf-adversary`

**เกต cloud:** `python3 -m unittest discover -s tests -p 'test_*.py'`: 3291 passed, 0 failed, 18 error เดิม (ไม่เกี่ยวข้อง — `capstone`/`pefile`/`pytest` ไม่มีในเครื่อง ไม่มีเน็ตให้ติดตั้ง `pip install` timeout), 212 skipped · 🔴 ไม่ใช่ gate เต็มของ Windows (ยังไม่ได้รันในเกมจริง)

## ⑤ ใบที่เปิด/ขอในรอบนี้

- เปิดใบให้ `pf-queue-author` ร่างใบเทสแบบ attended ต่อจาก `GT-078` (เลขใบ TBD — dispatch แล้ว ยังรอผล ณ ตอนเขียนรอบนี้ จะเติมเลขใบในจดหมาย/PR comment เมื่อทราบ)
- **เปิดใบให้สาย RE** (ยังไม่มีเลข): "bg0001 placement index → NPC identity/name/title สำหรับ Hields/Sase" — ต้องถอดรหัส placement block ชนิดที่สองที่ยังไม่มีใครแตะ งานนี้ทำบนสะพานเท่านั้น (ไม่มี client image ในคลาวด์)

## ⑥ BUILD-002

ไม่มีความคืบหน้าเพิ่มในรอบนี้ — `GT-079` ยัง `BLOCKED-ON-WIRING`, `RE-077` ยังเปิด ทั้งคู่รอ chief/RE ที่สาย A แตะไม่ได้อยู่แล้ว (ดูรอบ `A_20260826_0022` สำหรับรายละเอียดที่ทำไปแล้ว) ไม่ใช่การข้ามลำดับงานตาม `CHARTER-02` — เลือกเดินหน้า BUILD-001 ต่อเพราะเป็นจุดที่สาย A ตอบได้เองในรอบนี้ (มีคำตัดสิน OWNER-REJECTED ใหม่ให้ตอบ) ในขณะที่ BUILD-002 ไม่มีอะไรใหม่ให้สาย A ทำต่อได้จนกว่าจะมีคำตอบจาก chief/RE

## ⑦ nonclaims

1. **ไม่ได้พิสูจน์ว่าไคลเอนต์จริงวาดป้ายชื่อ** — เป็น [STATIC] จาก docstring/RE chain ไม่ใช่ [PROVEN] จาก capture จริง รอ attended retest
2. **ไม่ได้แก้ปัญหา identity ผิดตัว** (Hields/Sase และตัวอื่นที่อาจผิด) — คนละบั๊ก ยังเปิดอยู่
3. **ไม่แตะ** `runtime.py` · `app.py` · `current/pf_login_game_server_v141.py` · `population.py` (คนละโมดูล ไม่ใช่ live path) · canonical DB
4. ไม่ได้บูตเซิร์ฟเวอร์ ไม่ได้เปิดเกม ไม่จับ `LOCK_GAME`

## ⑧ สภาพแท่นตอนจบ

ไม่ได้เปิดเซิร์ฟเวอร์ ไม่ได้เปิดเกม · canonical DB ไม่ถูกแตะ · PR #73 เปิดพร้อม merge (ไม่ merge เอง ปล่อย workflow)
