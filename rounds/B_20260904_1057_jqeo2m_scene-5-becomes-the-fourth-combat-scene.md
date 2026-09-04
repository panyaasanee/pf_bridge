round jqeo2m
LANE-B (COMBAT)
start 2026-09-04T10:32+07:00
write 2026-09-04T10:57+07:00

NOW.md this round: อ่านก่อนทุกอย่างตามกติกา · ข้อที่ขยับ = "M4 · LANE-B" ข้อ (2)
"ฉาก 3/4/5 มี placements.tsv แล้ว = คิว B ฉากละใบ หลัง D7 (`2246`)" ซึ่งเป็นข้อเดียวกับ
`COO-DECISION 20260904_0748` ข้อ 2 · รอบนี้ทำฉาก 5 หนึ่งใบ
ข้อที่ **ไม่** ขยับ และเพราะอะไร:
- Door B caller (`MOB_HIT_FRAME_CONFIRMED`) ยัง `None` — เกตสองชั้นยังปิดทั้งคู่ และใบ `0847`
  สั่งแก้ compose ก่อนเสียบ caller ซึ่งรอบ r2ixqu ทำไปแล้ว ตัวถัดไปรอจุดอ่านของ chief
- builder ของ GM (`0738`) ยังไม่เสียบ — ตัวบล็อกที่ใบนั้นระบุเอง (`CORE-REQUEST-GM-053`)
  ยังไม่ลง main แปลว่าวันนี้มันปฏิเสธทุกครั้งบนบูตจริง
- P-2 (สีชื่อมอน) ไม่ใช่ของรอบนี้ และ NOW.md ห้ามเปิดใบเทสตีมอนจนกว่า P-2 ปิด
  รอบนี้จึงไม่เปิดใบ GT ให้ฉาก 5 แม้ของจะพร้อมให้บูตทดสอบ

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
วาปเข้าฉาก 5 (Evil Port) แล้วตีมอนหกตัวได้ แทนที่ทุกหมัดจะถูกปฏิเสธด้วย
`target_not_in_ledger` เหมือนเมื่อวาน · ฉาก 5 เป็นฉากแรกที่ประตูเข้าเปิดอยู่ก่อนแล้ว
(สาย A เปิด `login_entry_allowed` ตั้งแต่รอบ `l03cgh`) ผู้เล่นยืนในแมพนี้ได้มาก่อนหน้านี้แล้ว
สิ่งเดียวที่ขาดคือของให้ตี
🔴 ที่ยัง **ไม่** เปลี่ยน: มอนยังตายไม่ได้ ทั้งหกแถวไม่มีใบอนุญาตฆ่า (`mob_death.ruling_for`
โยน `target_outside_the_sanctioned_scope`) ตี HP ลงถึง 0 แล้วไม่มีเฟรมตาย ไม่มีศพ
ใบขอไปที่ COO รอบนี้ (`notes_to_chief/20260904_1057_LANE-B-ASK-COO-six-bg0005-...`)

## ล็อกรอบ
- ต้นรอบ list PR สถานะ open ทั้งสองรีโป: `pirate-force-server` ไม่มี PR เปิดเลย ·
  `pf_bridge` เปิดอยู่สี่ใบ (`#1106` A · `#1105` GM · `#1104` DB · `#1095` E) ไม่มี `[LANE-B]`
  -> ตัดกิ่งจาก main ของ pf_bridge commit ไฟล์ร่าง `_claim.md` เปิด `#1107` (ไม่ draft ไม่มี marker)
- list ซ้ำทันทีหลังเปิด: `#1107` เป็น `[LANE-B]` ใบเดียว ไม่มีใครเก่ากว่า -> ถือล็อก
- ชะตา PR รอบก่อน (ADDENDUM A): `#721` `[LANE-B] Door B composes from live values` **merged**
  2026-09-04T03:06Z · claim `#1094` merged · ไม่มีอะไรต้อง cherry-pick

## กล่องจดหมาย (ขั้นที่สองของรอบ)
บริโภคสองใบ วาง `.CONSUMED.txt` + สำเนาต้นฉบับเข้า `consumed/` แล้ว:
- `20260904_0748_COO-DECISION-lane-b-710-died-...` ข้อ 1 ปิดแล้ว (`#717` merge · ไม่มีเกตตายครั้งที่สาม)
  ข้อ 2 = งานของรอบนี้
- `20260904_0738_LANE-GM-TO-LANE-B-the-login-shaped-builder-...` — เหตุผลที่ยังไม่เสียบอยู่ใน stub
หนี้ที่รับมาจาก `COO-DECISION 20260904_0943` ข้อ 3 (ยังไม่แตะโค้ด ตามที่ใบสั่ง):
**`MOB_COMBAT_DEFAULT_ATTACKER` (ทุกคนแรงเท่ากัน) เป็นของ LANE-B · แหล่งค่า = แถว typed ของ DB ·
บล็อกจนชิ้น 2 ของ DB / RE `s_SCORE` ตอบ** — บันทึกเป็นหนี้ตามที่ใบสั่งให้ทำ

## ทำอะไร

### 1. roster ของฉาก 5 (ของจริงของรอบ)
`src/pirateforce_foundation/field_mob_tables_bg0005.py` — GENERATED โดย
`tools/pf_mine_scene_mob_roster.py --scene bg0005 --identity-rule cline` หกแถว หกเทมเพลต
CLINE type 5 · ใช้กฎ identity เดียวของโปรเจกต์ (`COO-DECISION 20260829_0345`) ไม่ใช่ setnum
ลงทะเบียนใน `field_mobs._SCENE_TABLE_MODULES` ในคอมมิตเดียวกับที่เพิ่มไฟล์ ไม่มีเกตให้รอ

| placement | n_ID | ชื่อ | เลเวล | HP | identity |
|---|---|---|---|---|---|
| 59 | 148 | Red Devil | 66 | 59306 | 0x203C |
| 69 | 150 | Ned apes | 69 | 68789 | 0x2046 |
| 70 | 144 | Hard Blade Eagle | 68 | 65511 | 0x2047 |
| 74 | 146 | Black Jack | 65 | 56377 | 0x204B |
| 84 | 523 | Jet cat thieves No.5 | 62 | 48209 | 0x2055 |
| 85 | 525 | Jet cat thieves No.6 | 67 | 62350 | 0x2056 |

### 2. กับดักที่ทำซ้ำได้ก่อนแก้ ไม่ใช่ที่ทำนายเอา
`mob_ai_control.open_register(field_mobs.roster_for_scene_id(5))` โยน
`MobAiControlError: ai_row_missing: placement 59 points at AI_COMBAT 201` **ก่อน**
แก้อะไร · จุดเรียกของมัน (`_sync_combat_scene_state` ใน `runtime.py:4103`) อยู่ **เหนือ**
ทุก `except` ใน `_dispatch_mob_combat` แปลว่าหมัดแรกในฉาก 5 จะ unwind listener thread
และโลกของผู้เล่นว่างเปล่า — อาการเดียวกับที่ `mob_combat_bg0015_gates.py` วัดไว้ให้ฉาก 14
แก้: widen union ของ `tools/pf_mine_mob_ai_rows.py` ให้รวม roster ของฉาก 5 แล้ว regenerate
`field_mob_ai_tables.py` (+15 บรรทัด **เพิ่มอย่างเดียว** ไม่มีแถวเดิมเปลี่ยนหรือหาย)
ฉาก 5 ต้องการ `AI_COMBAT` 111/134/201/214/250 และ `AI_WANDER` 11/16

### 3. composer ของ recompose ลงคอมมิตเดียวกับ roster
`mob_scene_recompose.py` เคยเขียนคำสัญญาไว้เองว่า "this lane WILL compose it; what it cannot
do is compose a map with no monsters in it" · รอบนี้เอามอนใส่แมพ จึงต้องจ่ายในคอมมิตเดียวกัน
- `COMPOSER_BG0005` + แถวใน `_COMPOSERS` · entry ของฉาก 5 ใน `ACKNOWLEDGED_WITHOUT_COMPOSER`
  **ขีดฆ่า** ไม่ลบ
- `NON_DELEGATED_COMPOSER_KINDS` ตัวใหม่: ก่อนหน้านี้ชุดเดียวกันถูกสะกดเป็น literal **สามที่**
  (guard ของ `_compose` · เงื่อนไข `heals` · เทสใน `test_mob_scene_recompose.py`) และสองใน
  สามเคยเหลื่อมกันมาแล้วหนึ่งครั้งตอนฉาก 14 เข้า (pf-adversary รอบ n4pv7k) · คอมเมนต์ที่รอบนั้น
  ทิ้งไว้ทำนายว่าฉากที่สี่จะซ้ำรอย · รอบนี้ทั้งสามอ่านทูเปิลเดียวกัน
- `if/else` ที่เลือก population builder เคยรับได้แค่สอง composer และตัวที่สามจะตกลง `else`
  เงียบ ๆ (ประกอบฉาก 5 ด้วย builder ของฉาก 14) · เปลี่ยนเป็นตาราง `_POPULATION_BUILDERS`
  + `assert_every_non_delegated_kind_has_a_builder()` ที่รันตอน import
  แต่ละ builder ยังอ่าน `COUNT_SOURCE_CALLER` **จากโมดูลของตัวเอง** ไม่สะกดซ้ำ

### 4. ตัวควบคุมที่ตายมานาน และไม่มีใครรู้
`tools/pf_mine_scene_mob_roster.py --verify-frozen` คือ **ตัวควบคุมเดียว** ที่ตรวจได้โดยไม่มี
ไคลเอนต์ ตามที่ docstring ของมันเขียนเอง · มัน **โยน ไม่ใช่ตรวจ** มาตั้งแต่
`unambiguous_placements` งอกสมาชิกตัวที่แปด: ทุกครั้งที่เรียกได้
`ValueError: too many values to unpack (expected 7)` แปลว่าสองฉากที่ถูก mine ในช่วงนั้น
ถูก mine โดยตัวควบคุมปิดอยู่ · ไม่มีอะไรจับได้เพราะไม่มีเทสไหนเรียกฟังก์ชันนี้ และแฟล็กปิดโดยดีฟอลต์
แก้แล้ว unpack ด้วย index (สมาชิกตัวที่เก้าจะไม่พังซ้ำ) และรอบนี้มีเทสเรียกมันจริง
ผลหลังแก้: `verify-frozen: 115 rows compared, 0 mismatches`

### 5. ตัวควบคุมข้ามสาย ที่ generator บอกเองว่าไม่มี
`scene_identity_rule.py` เขียนไว้ว่า "NONE of the three [controls] touches type 14 ... closing it
(a control measured on the scene being mined) is a generator change queued for the next round"
ฉาก 5 เป็นฉากแรกที่ไม่ต้องเขียนตัวใหม่: **สาย A ขุด crosswalk ของ CLINE type 5 นี้เองไปแล้ว**
ด้วยเครื่องมือของตัวเอง เพื่อ census ขาเข้าของตัวเอง (`world_bg0005_identity.IDENTITIES`)
รอบนี้เทียบทั้งหกแถว: **ตรงกันทั้ง `MOBS.n_ID` และชื่อ ทั้งหก** สองสาย สองเครื่องมือ สองตาราง
คำตอบเดียว · ปักเป็นเทสสองฝั่ง (ในไฟล์เทสของสาย B และในไฟล์ของสาย A ที่เคยปัก "ยังไม่มีโมดูลนี้")

## เทสที่ขยับ และเพราะอะไร (ทุกใบเป็นพินที่ต้องขยับ ไม่ใช่การอ่อนตัว)
- `test_mob_death_wired_widening.py` — **defect จริง ไม่ใช่พิน**: มันเทียบ identity ด้วย `hex()`
  (ตัวเล็ก) กับบรรทัดที่ `describe_widening_coverage` พิมพ์ด้วย `%X` (ตัวใหญ่) · identity ทุกตัวที่
  เคยผ่านลูปนี้ (0x2058 ของ Carlos ด้วย) บังเอิญไม่มีตัวอักษร a-f เลย สองการสะกดจึงเท่ากันด้วยโชค
  · 0x203C คือตัวแรกที่มี · แก้เป็น `"0x%X"`
- `test_scene_scoped_combat_wiring.py` — `TABLELESS_SCENE_ID = 5` เป็นเลขที่พิมพ์มือ นั่งอยู่ใต้
  คอมเมนต์ที่บอกว่ามัน derive มาจาก reader · derive จริงแล้ว รอบหน้าที่ติดอาวุธฉากถัดไปจะไม่แดง
- พินที่โตตามฉากที่สี่ (ขีดฆ่าเดิมไว้ทุกใบ): `test_mob_ai_control` (bg0005 เข้า derived set) ·
  `test_mob_combat_bg0015_gates` (composer_scene_ids 1,2,14 -> 1,2,5,14 · live_scenes +bg0005) ·
  `test_gm_identity_registry_census` (scenes checked 3 -> 4 — **subTest ทั้งสี่ผ่าน** แปลว่า
  identity ทั้งหกของฉาก 5 อยู่ใน census ของฉาก 5 จริง ไม่มีตัวไหนถูก
  `apply_identity_override` ทิ้งเงียบ ๆ นี่คือสิ่งที่เทสนั้นมีไว้ตรวจ) ·
  `test_mob_stat_fabrication_guard` (โมดูลใหม่เข้า LANE_B_MODULES)
- เทสของสาย A สองใบที่ปัก "ยัง" ไว้ และรอบที่ทำให้มันเป็นเท็จต้องมาแตะเอง (สาย A เคยแตะไฟล์ของ
  สาย B ด้วยเหตุผลเดียวกันตอนเพิ่ม entry ฉาก 4/5/6): `test_world_bg0005_identity.py`
  (เปลี่ยนจาก "ไม่มีโมดูล roster ของ B" เป็นตัวควบคุมข้ามสายในข้อ 5) ·
  `test_world_population_bg0005.py` (allowlist ผู้ import + เหตุผลว่าทำไม recompose ต้อง import)

## pf-adversary
สั่งต้นรอบพร้อมเริ่มงาน ตามกติกา NOW.md (`COO 0903_2345`) — worktree review ไม่ใช่เช็คเอาต์สด
ADVERSARY_PENDING PR #727 — ผลยังไม่คืนตอน push ตามกติกาข้อเดียวกัน:
push ตามเดิม ห้ามถือล็อก และ **รอบถัดไปของสาย B หยิบผลเป็นงานแรกก่อน claim**
ห้ามอ่านไฟล์นี้ว่า "ผ่าน adversary" — ยังไม่มีผลคืน

## ชุดเทส
ระหว่างทาง: เฉพาะไฟล์ที่แตะ + ไฟล์ที่พังเพราะการแตะนั้น (`-k "mob or field or scene or roster or
census or recompose or population or identity"` = 4203 passed, 44 skipped, 11309 subtests)
ชุดเต็ม **สองครั้ง** และเหตุผลของครั้งที่สองอยู่ข้างล่าง (กติกาบังคับให้เขียน)
รันในสภาพเกตจริงทั้งสองครั้ง คือใน `git worktree`
ที่ไม่มี `pf_bridge` วางข้าง ๆ (กติกา NOW.md บรรทัด "รอบที่เพิ่ม `tests/test_*.py` ใหม่ ต้องซ้อมเกต
ในสภาพไม่มี pf_bridge ข้าง ๆ ก่อน push" · เหตุ `#601` หาย 3,534 บรรทัด):
- ครั้งที่ 1 บน `629bf64`: `pytest_subset` (48 โมดูล excluded ตามสูตรของเกต)
  **8634 passed, 89 skipped, 16779 subtests**
- 🔴 **ทำไมต้องรันเต็มครั้งที่สอง**: ระหว่างรอบ `main` ขยับจาก `531dc9d` ไป `4c19f23` (#723 LANE-DB)
  หลัง push แรก · กติกา NOW.md บรรทัด "ก่อน push ต้อง `git fetch origin main` แล้วรันชุดเต็ม
  บนต้นไม้ที่ merge main แล้ว ไม่ใช่สาขาเพียว" บังคับให้ merge แล้วรันใหม่ ไม่ใช่ปล่อยให้เกตเจอเอง
  merge สะอาด ไม่มี conflict
- ครั้งที่ 2 บนคอมมิตสุดท้ายจริง `e6edff3` (merge `4c19f23`):
  **8645 passed, 89 skipped, 16779 subtests** (+11 = เทสที่มากับ #723)
- `skip_census` (ทั้งสองครั้ง): `every skip is declared, named and pinned` · `RESULT: PASS`
  (`docs/PYTEST_SKIP_PINS.json` ได้ entry ใหม่ `tests/test_field_mob_tables_bg0005.py` count 2
  ในคอมมิตเดียวกับเทส)
- `pf_gate_preflight` บนคอมมิตสุดท้าย: `[cp874] PASS` · `[skips] PASS` ·
  `[mainmerge] PASS - origin/main (4c19f23) is already in HEAD`
- `tools/verify_functional_coverage.py`: `FUNCTIONAL_COVERAGE PASS domains=8` ·
  `tools/verify_hypothesis_ledger.py`: `HYPOTHESIS_LEDGER PASS entries=50`

## ไม่ได้ทำในรอบนี้
- ไม่แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / canonical DB /
  `scenarios/world_*.json` / `scenarios/combat_*.json`
- **ฉาก 3 และ 4 ยังไม่ทำ** และเหตุผลต่างกัน:
  ฉาก 4 ประตูเข้ายังปิด (`login_entry_allowed=false`) ผู้เล่นไปไม่ถึง จึงไม่ใช่ของด่วน
  ฉาก 3 ติดของจริง: โฟลเดอร์สะกด `gamedata/scene/Bg0003/` แต่ไฟล์ข้างในสะกด
  `bg0003.placements.tsv` · `Sources` ประกอบพาธเป็น `scene/<S>/<S>.placements.tsv` จึงหาไม่เจอ
  ทั้งสองการสะกด = แก้ตัวขุดให้ resolve ชื่อไฟล์ ไม่ใช่แก้ข้อมูล -> รอบถัดไป
- ไม่เปิดใบ GT ให้ฉาก 5 (NOW.md ห้ามจนกว่า P-2 ปิด) แม้ของจะพร้อมบูตทดสอบแล้ว
- ไม่เสียบ Door B caller · ไม่เสียบ builder ของ GM · ไม่แตะ `MOB_COMBAT_DEFAULT_ATTACKER`

## ฝั่งเซิร์ฟเวอร์
`pirate-force-server` **PR #727** เปิดแล้ว ไม่ draft · `PF-AUTOMERGE: v4` อยู่ใน body ตั้งแต่เปิด
ยืนยันด้วย GET กลับมาแล้ว · หัวคอมมิตสุดท้าย `e6edff3`
**push แล้ว รอ merge PR #727** · สถานะ PR เซิร์ฟเวอร์: **เปิดแล้ว รอ gate**
