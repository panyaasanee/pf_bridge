# LANE-B round c2ikd0 -- 2026-09-06T22:32+07:00 start

## รอบนี้ขยับ NOW/M ข้อไหน
**M3/M4 · LANE-B ข้อ "รอบถัดไป = adversary `0wef26`"** ของ NOW.md ทำครบ · แต่
**PR `1955` ยังไม่ได้เริ่ม** และเหตุผลไม่ใช่เวลา: **`#946` ไม่ได้อยู่บน main** —
reaper ปิดมันตอน 13:56Z (`closed`, `merged: false`, `git merge-base
--is-ancestor 14196f3 origin/main` = ไม่ใช่) ทั้งที่ไฟล์รอบก่อนบันทึกไว้ว่า
"เปิดแล้ว รอ gate" ⇒ ของที่ `1955` ต้องต่อยอด **ไม่มีอยู่บน main** รอบนี้จึงกู้มันกลับ
ด้วย cherry-pick ตามกฎบ้าน (reaper ปิด = กิ่งเก็บไว้ กู้รอบถัดไป) แล้วจ่ายหนี้
adversary บนกิ่งเดียวกันตามลำดับที่ใบ `2047` ข้อ 1 สั่ง · หนึ่ง PR ต่อรีโปต่อรอบ
⇒ `1955` (ก)+(ข)+(ค) เป็นงานแรกของรอบถัดไป

## ล็อกรอบ
claim PR `pf_bridge#1575` (กิ่ง `claude/focused-ramanujan-c2ikd0`) เปิดก่อนแตะอะไร
ทั้งสิ้น · list ใบ `[LANE-B] round <id>: claim` ที่ open ตอนเริ่ม = **ไม่มี**
(`#1574` LANE-A · `#1573` LANE-K · `#1572` LANE-GM · `#1571` LANE-DB ·
`#1493` หัวใบเป็น `[LANE-B] round 30ja9z addendum` ไม่ใช่ `claim` จึงไม่ใช่ล็อก
ตามข้อ 1) · list ซ้ำหลังเปิด: ไม่มีใบ `[LANE-B]` ที่เก่ากว่าและยังมีชีวิต

## กล่องจดหมาย — บริโภคครบ 5 ใบในรอบนี้ (ทุกใบวาง `.CONSUMED.txt` + สำเนาไป `consumed/`)
1. `1955_COO-DECISION-b1824` (กฎเดียวพารามิเตอร์ครอบครัว + กู้ #936) — **ยังไม่ได้ทำ**
   เหตุผลข้างบน · เป็นงานแรกรอบหน้า
2. `2047_COO-DECISION-b2022` (D1 ยืนยัน · `#946` รับ · แล้วค่อย `1955`) — **ทำตามลำดับ**
   ข้อ 1 (adversary/defect) ครบ · การแบ่งกอง D1 ยังอยู่ครบและมีเทสคุม ไม่ได้ถอด
3. `2047_COO-DECISION-panya2032-job1` (ตัวแปลกฎ AI_COMBAT+wander) — คิวหลัง `1955`
   ตามที่ใบเขียนเอง ยังไม่เริ่ม
4. `2141_COO-DECISION-e2015-bg0002` (เทสแดงตามลำดับรัน) — **reproduce ไม่ได้ 3 ชุด**
   รายละเอียดข้างล่าง ขอคำสั่งรันของ chief ในจดหมาย `2245`
5. `2141_COO-DECISION-e2115-buried-at` (นาฬิกา respawn เป็นของโลก) — **คำตอบหนึ่งบรรทัด
   ที่ใบขอ: รวมกับงาน respawn 120 s ใบเดียว ไม่แยก** (ผิวเดียวกัน คือเวลาตาย/เวลาฟื้น
   ของมอน ต้องเขียนลง registry ของ A ที่เดียว) · เคารพขอบเขต: ไม่แตะ
   `mob_death_persistence.py` จน `#948` merge

`NO_FEATURE_WAITING:` ไม่มีผล RE/CORE-REQUEST ใหม่ถึงสายนี้ในรอบนี้

## รอบนี้ทำอะไร (ของจริง)

### ก. กู้ `#946` ที่ reaper ปิด
`git cherry-pick c5c87d2 14196f3` ขึ้น `claude/nice-meitner-c2ikd0` ที่ตัดจาก
`origin/main` วันนี้ (`cf961be`) — **ไม่ conflict** · 5 ไฟล์เท่าเดิม ไม่มีการแก้เนื้อ
ระหว่างกู้

### ข. จ่ายหนี้ adversary 4 ข้อ ทุกข้อมีมิวแทนต์ยืนยัน (รันจริง ไม่ใช่การอ่านโค้ด)
**1. [HIGH] `test_ratified_scenes_gain_nothing_from_the_switch` วัดไม่ตรงชื่อตัวเอง**
เดิมเทียบ *ยูเนียนของ roster ทุกฉาก* กับ *ยูเนียนของใบมือทั้งหมด* ⇒ เขียวทันทีที่
template อยู่ในใบของฉากไหนก็ได้ และ**ไม่เคยอ่านใบ derive เลย** (มันคำนวณกฎใหม่แทน
ที่จะอ่าน `WIDENING_RULINGS` ซึ่งเป็นสิ่งที่ `kill` อ่านจริง)
เขียนใหม่เป็น **ต่อฉาก**: `WIDENING_RULINGS[derived_key(scene)] ⊆ ยูเนียนของใบเซ็นที่
ผูกกับฉากนั้น` + การ์ดสองทาง (ใบ derive ต้องไม่ว่าง · ฉากต้องมีใบเซ็นของตัวเอง)
🔴 **วัดก่อนเขียน ไม่ใช่หวังว่าจะจริง**: ส่วนต่างต่อฉากเป็น **ว่างทั้ง 12 ฉาก**
(roster/ใบผูกฉาก: Bg0002 3/4 · Bg0003 7/7 · Bg0007 7/7 · Bg0008 6/6 · Bg0009 5/5 ·
Bg0010 6/6 · Bg0011 5/5 · Bg0015 6/6 · bg0001 1/2 · bg0004 5/5 · bg0005 6/6 ·
bg0006 2/2) ⇒ **เงื่อนไข `1648` ข้อ 2 ("เท่ากับตารางเดิมทุกฉากที่ ratify") ถูกทำให้
เป็นเทสจริงแล้ว** ไม่ใช่แค่ประโยคในไฟล์รอบ

**2. [MEDIUM-HIGH] การ์ด anti-vacuity ที่ไม่ guard**
`test_a_signed_letter_outranks_a_derived_permit_on_every_shipped_row` นับ `checked`
เมื่อมีใบเซ็นอย่างน้อยหนึ่งใบ (จริงเกือบทุกแถว) ⇒ เปลี่ยนเป็นต้องมี**ทั้งใบเซ็นและใบ
derive**บนแถวเดียวกันจึงนับ

**3. [MEDIUM] ข้อ 4 ของ `1648` คุมแค่ 924 ไม่คุม 529**
เขียน pin ในรูปที่ใบสั่งจริง (**template id ที่ฉากซึ่ง placement เป็นเหตุ**): ทุก
placement ที่ withheld/owner-refused ต้องไม่มี template ของมันอยู่ใน**ใบ derive ของฉาก
ตัวเอง** (วัดครบ 10 placement) + pin 924 และ **529** ด้วย id อีกชั้น

**4. [LOW] คอมเมนต์เท็จสองที่ใน `mob_death.py`**
- "withheld/owner-refused ไม่อยู่ในเซต derive" **เป็นเท็จ**: template 103 ถูกปฏิเสธที่
  Bg0002 placement 92-96 แต่**อยู่ใน**ใบ derive ของ bg0004 เพราะ bg0004 ship มัน ·
  ที่กันไม่ให้ถึงกันคือ**การผูกฉากอย่างเดียว** เขียนใหม่เป็นประโยคต่อฉาก + บอกตรง ๆ ว่า
  scene tie คือกลไกทั้งหมดของข้อ 4 ไม่มีเข็มขัดเส้นที่สอง
- "17 แถว Bg0002" → **12** (`HOSTILE_PLACEMENTS` = 17 · 5 แถวเจ้าของปฏิเสธ ไม่เคย ship)

### ค. มิวแทนต์ที่รันจริงในรอบนี้ (ก่อนแก้ → หลังแก้)
| มิวแทนต์ | ก่อน | หลัง |
|---|---|---|
| `derive_rule_widened_templates() -> {}` | เขียว 5/7 | **แดง 4** |
| ยัด template 669 (ใบ Bg0011 ใบเดียว) เข้าใบ derive ของฉากอื่น | เขียว 12/12 | **แดง** (เทสต่อฉาก) |
| ยัด 529 (Nina) เข้าใบ derive ทุกใบ | เขียว 7/7 | **แดง 3** |
| ถอดการแบ่งกอง D1 (`hand_written = []`) | แดง | **แดง** (ยังคุมอยู่) |

## bg0002 order-dependent (`2141`) — reproduce ไม่ได้ ยังไม่แก้ และไม่แก้แบบเดา
ลองสามชุด **เขียวหมด**: (1) dispatch+bg0002_kill+mob_death+wired_widening+
persistence+rule_derived = 210 passed · (2) `tests/test_mob_*.py` = 1675 passed ·
(3) world_scene_registry+entry+folder+scene_scoped_combat_wiring+census_wiring+
bg0002_kill = 192 passed · ไฟล์ `tests/test_death_seed_call_site.py` ที่ใบยกเป็นแบบ
**ยังไม่มีบน main** (มากับ `#948` ซึ่งยัง draft)
ขอคำสั่ง `pytest` ที่ chief ได้ `1 failed, 159 passed` ในจดหมาย `2245` · **ไม่ใส่
`install_world_deaths()` ใน `setUp` แบบเดา** เพราะจะเป็นการจำลองที่ล้มไม่ได้ ซึ่งเป็น
สิ่งที่รอบ `0wef26` เพิ่งถูก adversary จับได้ว่าแย่กว่าไม่จำลอง

## ที่ไม่ได้แตะ
- ไม่แตะ `runtime.py` / `app.py` / `current/pf_login_game_server_v141.py`
- ไม่แตะ `field_mob_tables_*.py` · ไม่แตะ roster · ไม่ mint คีย์ใหม่แม้แต่ใบเดียว
  (จำนวนคีย์เท่าเดิมกับ `#946` เป๊ะ) · ไม่แตะ `Bg3001IsNotKillableYetTests` ·
  `1644` ยัง DEFERRED ตาม `1955` ข้อ 4
- ไม่แตะ `mob_death_persistence.py` (ขอบเขตของ `2141` e2115)
- ไม่ปลดใบมือใบใดออก · ไม่แตะเขตสาย A

## pf-adversary
สั่งตั้งแต่ต้นรอบบนกิ่ง `claude/nice-meitner-c2ikd0` พร้อมโจทย์ 5 ข้อ (a) ตรวจซ้ำ 3 คำ
อ้างที่รับมา (b) เซ็ตส่วนต่างต่อฉากจริงก่อนเขียนเทส (c) หามิวเทชันที่ widen การฆ่าได้
จริงแต่เทสต่อฉากยังเขียว (d) กวาดแกนฆ่า main vs กิ่งนี้ (e) ช่องทางอื่นที่ roster ฉากใหม่
ทำให้ฉากที่ ratify แล้วกว้างขึ้นเงียบ ๆ
`ADVERSARY_PENDING claude/nice-meitner-c2ikd0` — **ผลยังไม่คืนตอน push** ห้ามอ่านไฟล์นี้
ว่า "ผ่าน adversary" · รอบถัดไปของสาย B สั่ง adversary บนกิ่งนี้/PR `#958` เป็นงานแรก
ตามกฎ PENDING · self-review ที่ทำจริง: อ่าน `git diff --cached` ทุก hunk ก่อน commit ·
รันมิวแทนต์สี่แบบข้างบนจริง ไม่ใช่การอ่านโค้ด · วัดเซตส่วนต่างต่อฉากก่อนเขียนเทส

## verification
- **ชุดเต็ม `pytest tests/` บนต้นไม้ที่ commit จริง (`4d3adfb`, หลัง `git merge origin/main`
  = no-op): 12483 passed · 373 skipped · 27515 subtests · 1 failed (413.56s)** · แถวที่แดง
  คือ `test_lane_a_choose_npc_scene1.py::...::test_the_talk_trigger_is_still_missing_at_
  real_dispatch_today` = `KNOWN_RED_MAIN:` แถว 2 ของ NOW.md (ของ LANE-A) · **พิสูจน์ว่า
  ไม่ใช่ของกิ่งนี้**: worktree แยกบน `origin/main` เปล่า รันไฟล์เดียว → แดงแถวเดียวกัน
  (1 failed, 69 passed)
- `pytest tests/test_mob_death_rule_derived_widening.py` → **7 passed**
- `pytest tests/test_mob_*.py` → **1675 passed, 6335 subtests**
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS**
  (รวม `--pr-body ... --pr-stage final` → marker บรรทัดเดียว) · เกตชื่อไฟล์: stub
  `.CONSUMED.txt` สามใบยาวเกิน 100 แต่เป็นชื่อที่สืบมาจาก main ซึ่งเป็นข้อยกเว้น (ก) ที่
  เกตรับแล้ว
- ทุกไฟล์ที่แตะเป็น ASCII ล้วน (`str.isascii()` ต่อไฟล์) · stage ทีละไฟล์ อ่าน
  `git diff --cached` ทุก hunk ก่อน commit · ไม่ใช้ `git add -A`

## PR/status
- `pf_bridge` claim `#1575` (`claude/focused-ramanujan-c2ikd0`) — ปลดเมื่อจบรอบ
- `pirate-force-server` **PR `#958` เปิดแล้ว ไม่ draft** body มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด GET ยืนยันแล้ว ·
  กิ่ง `claude/nice-meitner-c2ikd0` หัว `4d3adfb` · **สถานะตามจริง: เปิดแล้ว รอ gate**
  (ไม่ใช่ landed) · คาดว่าเกต Windows จะแดงด้วยแถวของ LANE-A เหมือนที่ปิด `#946`
  จนกว่า LANE-A จะกลับ assertion

## รอบหน้าทำอะไร (เรียงแล้ว ตามใบ `2047` ข้อ "ลำดับรอบถัดไป")
1. **PR `1955` (ก)+(ข)+(ค)** — `hostile_roster()` รับพารามิเตอร์ครอบครัวจาก world
   registry ของ A · ตาราง `1824` เป็นเทส (12 เมือง 106 แถว + ทะเล 2/1/0/0/0) ·
   กู้ `#936` (กิ่ง `claude/nice-meitner-mf71tm`) เข้า PR เดียวกัน · **ก่อนทำ ตรวจว่า
   PR ของรอบนี้อยู่บน main จริงด้วย `git merge-base --is-ancestor` ก่อน ไม่เชื่อไฟล์รอบ**
   (บทเรียนตรง ๆ ของรอบนี้)
2. bg0002 order-dependent เมื่อได้คำสั่งรันจาก chief (`2245` ข้อ 4)
3. นาฬิกา respawn เป็นของโลก **รวมกับ respawn 120 s ใบเดียว** หลัง `#948` merge
4. P-2 ชั้นสอง (สี/attr) เมื่อ `GT-281` จอผ่าน · ไม่มีงาน startable ⇒ งาน 1 PANYA `2032`
5. หนี้เดิมยังค้าง: `tools/pf_scan_field_scene_candidates.py` ไม่ตรงกับ miner

TWO_SESSIONS_SAME_SCENE: ไม่เปลี่ยนจาก `#946` — รอบนี้แตะเทสกับคอมเมนต์เท่านั้น ไม่มี
state ต่อ session ใหม่ ไม่แตะ `DeathRegister` · การ derive ยังเป็นการอ่านตารางที่ commit
แล้วตอน import ผลเท่ากันทุก process ที่ import โมดูลเดียวกัน

SCOREBOARD: STUCK | a monster in a brand-new field scene is killable the day its roster lands, with no per-island COO letter -- proven and tested, but it is not on main: the reaper closed #946 on a red gate that belongs to LANE-A, so this round rebuilt it and hardened the tests that were supposed to be guarding it | pirate-force-server#958 (open, awaiting gate, head 4d3adfb) - full suite 12483 passed, 1 failed = KNOWN_RED_MAIN row 2 reproduced on clean main - preflight PASS - letter notes_to_chief/20260906_2245_LANE-B-TO-COO-946-recovered-adversary-paid-bg0002-repro-blocked.md
