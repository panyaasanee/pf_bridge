# LANE-B round 0wef26 -- 2026-09-06T19:31+07:00 start

## รอบนี้ขยับ NOW/M ข้อไหน
**M3 "สนามมีมอนสเตอร์"** — งานแรกของ M4·LANE-B ใน NOW.md ("ตาราง diff กฎ `MOBS`
vs ต่อฉาก + เกต CI คีย์ทาง 2") **ขึ้น main ครบทั้งสองชิ้นแล้ว** (ยืนยันด้วย
`git log` ไม่ใช่ด้วยคำอ้างของรอบก่อน: ตาราง diff = จดหมาย `1824` · เกตคีย์ =
`tests/test_mob_death_widening_schema_gate.py` มาจาก `#940` merge แล้ว) จึงหมด
เงื่อนไขที่ `1648` ข้อ 2 ตั้งไว้ รอบนี้ทำ**การสลับ**ที่ใบนั้นสั่งไว้เป็นขั้นถัดไป

**ขยับครบ**: `pirate-force-server#946` เปิดแล้ว ไม่ draft มี marker · ชุดเต็มเขียว
12447 passed 0 failed · preflight PASS · ฉากใหม่ที่ roster ลงจะฆ่าได้ทันทีโดยไม่ต้องมี
ใบ COO ใบที่ 12

## ล็อกรอบ
claim PR `pf_bridge#1550` (กิ่ง `claude/focused-ramanujan-0wef26`) เปิดก่อนแตะ
อะไรทั้งสิ้น · list ใบ `[LANE-B] round <id>: claim` ที่ open ตอนเริ่ม = **ไม่มี**
(`#1548` LANE-A · `#1546` LANE-GM · `#1540` LANE-E · `#1493` เป็น
`[LANE-B] round 30ja9z addendum` ซึ่งหัวใบไม่ใช่ `claim` จึงไม่ใช่ล็อกตามข้อ 1)

## กล่องจดหมาย
`grep -l "ADDRESSEE: LANE-B" notes_to_chief/*.md` — ใบ COO ที่ตอบสายนี้ล่าสุด
(`1647` `1648` `1745`×3) **มี `.CONSUMED.txt` คู่ครบทุกใบแล้ว** (รอบ `bvaptp`
บริโภคไปแล้ว) รอบนี้ไม่มีใบใหม่ที่ยังไม่บริโภค
`NO_FEATURE_WAITING:` ไม่มีผล RE/CORE-REQUEST ใหม่ที่ตอบถึงสายนี้ในรอบนี้

## เรื่องที่ต้องรู้ก่อนอ่านต่อ: งานของรอบ `bvaptp` **ไม่ได้หายไป**
ไฟล์รอบ `bvaptp` เขียนว่า commit `cbc96a3` ยัง local และ "orchestrating session
เป็นผู้ push ต่อ" — ตรวจแล้วว่ามันขึ้น main จริงผ่าน `#940` (`git log --oneline
-1 -- tests/test_mob_death_widening_schema_gate.py` → `cbc96a3`) ไม่ต้องกู้
เขียนไว้เพราะถ้าไม่ตรวจ รอบนี้จะทำเกตคีย์ซ้ำทั้งก้อน

## รอบนี้ทำอะไร (ของจริง)

### การสลับ: ใบอนุญาตฆ่าต่อฉาก 11 ใบ → กฎเดียว derive ต่อฉาก
`src/pirateforce_foundation/mob_death.py` (+170 บรรทัด, ไฟล์เดียวฝั่งโค้ด):
- `derive_rule_widened_templates()` เดิน `field_mobs.live_scenes()` แล้วเก็บ
  `template_id` ของ roster ที่ shipped จริงต่อฉาก — roster เป็นเอาต์พุตของกฎ
  `n_RANK != 0 and n_AI_COMBAT != 0` อยู่แล้ว (`tools/pf_mine_scene_mob_
  roster.py`) จึงเป็นการอ่านคอลัมน์ที่ ka1-A `1635` ชี้ ไม่ใช่รายชื่อมือชุดที่สอง
- `_register_rule_derived_permits()` ยัดใบอนุญาตที่ derive ได้ลง
  `WIDENING_RULINGS` **พร้อมกับ** ผูกฉากใน `WIDENING_RULING_SCENES` ในสเตตเมนต์
  เดียว · ฉากใหม่ที่มาทีหลังจึงฆ่าได้ทันทีโดยไม่ต้องมีใบ COO ใหม่ = สิ่งที่
  `1648` ข้อ 2 สั่ง
- ชื่อคีย์เป็น**ฟังก์ชันของชื่อฉาก** (`rule_derived_ruling_name`) ไม่ใช่สตริงมือ
  เพราะ `kill` fail-closed กับสตริงที่ไม่ตรง — สะกดสองแบบ = ถูกปฏิเสธ

**ทำไมเป็นใบต่อฉาก ไม่ใช่ใบเดียวทั้งโลก**: รอบนี้เขียนใบเดียวไม่ผูกฉากก่อน แล้ว
**ชุดเทสเดิมปฏิเสธ และมันถูก** — `test_every_registered_kill_letter_has_a_scene
_tie` บังคับว่าทุกใบต้องผูกฉาก เพราะใบที่ผูกแค่ template ทำให้ template นั้นฆ่าได้
**ทุกฉาก** (รูตูนี้ pf-adversary พิสูจน์ด้วยการรันมาแล้วรอบ `r6isy5` และเป็นเหตุผล
ที่ใบ bg0001/Bg0002 ซึ่งใช้ template 31/34/35/103 ร่วมกันต้องผูกฉาก) วัดผลจริงตอน
ใช้รูปใบเดียว: `describe_widening_coverage` เปลี่ยนจาก 12 บรรทัด UNKILLABLE เหลือ
0 — คือ **มอนที่ shipped อยู่ 12 ตัวที่วันนี้ฆ่าไม่ได้เพราะติดการผูกฉาก จะกลายเป็น
ฆ่าได้** นั่นคือการ widen ฉากที่ COO ratify ไปแล้ว ไม่ใช่การรับฉากใหม่ **การ derive
กฎไม่ได้ให้สิทธิ์เปิดรูนั้น** จึงเปลี่ยนเป็นใบต่อฉาก 12 ใบที่ generate จาก loop
ไม่ใช่พิมพ์มือ — แกนฉากแน่นเท่าเดิมเป๊ะ

**พิสูจน์ว่าไม่ widen อะไรเลยวันนี้** (วัด ไม่ใช่อ้าง): เซ็ตที่ derive ได้เป็น
**สับเซตแท้**ของยูเนียนใบมือ 11 ใบ — 59 template ต่อ 60 · ตัวเดียวที่ฝั่งเก่ามีแต่
ฝั่ง derive ไม่มีคือ template 27 (Mountain Deer diagnostic) ซึ่งไม่มี roster ไหน
ใส่ · placement ที่ withheld/owner-refused ถูกตัดออกจาก roster ก่อนที่ derivation
จะเห็น → template 924 (Bg0015 placement 87) **ยังไม่อยู่ในเซตที่ derive** ตามที่
`1648` ข้อ 4 สั่งให้คงไว้จนใบ 924/529 ตอบ

`tests/test_mob_death_rule_derived_widening.py` (ไฟล์ใหม่, 7 เทส) ถือ 5 ข้อ:
ค่าที่ลงทะเบียนยังเป็นเอาต์พุตของกฎ (ไม่ใช่ literal ที่ใครแปะทับ) และทุกใบยังผูกฉาก ·
ฉากที่ ratify แล้วไม่ได้อะไรเพิ่มจากการสลับ (= "เท่ากับตารางเดิม" ของ `1648` ข้อ 2
บนแกนฆ่า ส่วนแกน roster จดหมาย `1824` วัดไปแล้ว 0/106) — ผูกกับ **รายชื่อฉากที่
pin ไว้** ตั้งใจ เพราะฉากที่ 13 ที่มาทีหลัง *ต้อง* ทำให้เซตกว้างขึ้น (นั่นคือทั้งหมด
ของเรื่อง) และต้องไม่ทำให้เทสแดง · มอนทุกตัวที่ฉากที่ลงทะเบียนแล้ว ship จริงฆ่าได้
ผ่าน `rulings_covering` (เส้นตอบของโมดูลเอง ไม่ใช่แค่ frozenset) · withheld/refused
ไม่ถูกแตะ และเทสข้อนี้ล้มถ้าไม่มี withheld ให้ตรวจเลย (กัน vacuous pass)

## เทสเดิม 4 ตัวที่สมมติฐานหมดอายุเพราะการสลับ (เขียนใหม่ ไม่ได้ผ่อนให้ผ่าน)
ทั้งสี่เป็น pin บน `WIDENING_RULINGS` ที่พิมพ์มือ พอ dict กลายเป็นครึ่ง-derive จึงแดง
**ไม่มีอันไหนเป็นการ widen** และทุกอันยังแดงกับ defect ที่มันถูกเขียนมาจับ:
1. `test_every_shipped_answer_is_unchanged_by_the_new_tie_break` — เคยคำนวณลำดับ
   เก่าที่ถูกแทนแล้วเป็น**ตัวแทน**ของ "ไม่มีอะไรขยับ" ซึ่งเป็นตัวแทนที่ใช้ได้แค่ตอนที่ทุก
   เซตพิมพ์มือ · เปลี่ยนเป็นวัดตรง ๆ: เทียบคำตอบสดของแต่ละแถวกับคำตอบที่คำนวณจาก
   เซตคลุม**ก่อนมี derivation**
2. `test_the_coverage_report_names_a_monster_no_letter_covers` — จำลองโดยถอนใบ
   มือใบเดียวแล้วคาดว่า roster bg0002 จะกลายเป็น UNKILLABLE · ตอนนี้ใบ derive ยัง
   คลุมอยู่ การจำลองจึง**ล้มไม่ได้** = ไร้ค่า (จำลองที่ล้มไม่ได้แย่กว่าไม่จำลอง) · เปลี่ยน
   เป็นถอน**ทุกใบที่คลุมฉากนั้น** ซึ่งคือความหมายของ "ไม่มีใบไหนคลุม" หลังการสลับ
3-4. การ์ดต่อฉาก `test_field_mob_tables_bg0004.py` / `bg0010.py` pin ว่าแต่ละแถวมีใบ
   คลุม**ใบเดียว** · ตอนนี้แต่ละฉากมีสองใบ (ใบมือ + ใบ derive ของฉากตัวเอง) จึง pin
   เป็น**เซต** ส่วนสิ่งที่การ์ดมีไว้วัดจริง (ใบของ**ฉากอื่น**ต้องไม่เอื้อมถึงศพฉากนี้) ยัง
   ยืนยันเหมือนเดิมทุกบรรทัด

## defect ที่รอบนี้จับได้เอง (สองตัว ทั้งคู่ชุดเทสเดิมชี้ ไม่ใช่การอ่านโค้ด)
### D1 · ใบ derive แย่งที่มาของการฆ่าไปจากใบที่คนเซ็น
ใบ `0848` ข้อ 1 เรียง (ก) เซตแคบกว่า (ข) ใบเก่ากว่า (ค) ชื่อ และเขียนเหตุผลว่าห้ามให้
ใบที่เขียนพรุ่งนี้ย้ายที่มาของการฆ่าที่บันทึกใต้ใบเมื่อวาน — บังคับผ่านเทอม (ข) อายุ
**ใบ derive ลอดเทอมนั้นได้โดยไม่แตะมัน** เพราะมันมัก**แคบกว่า**ใบมือ และแคบกว่า
คือเทอม (ก) ที่อยู่เหนืออายุ · **วัดจริงก่อนแก้**: แถว Bg0002 ที่ shipped **ทั้ง 17 แถว**
เปลี่ยนใบที่ถูกบันทึก จากใบ `PANYA-DECISION 2026-08-27T20:10` (4 template) ไปเป็นใบ
derive (3) **แก้แล้ว**: `ruling_for` แบ่งสองกอง ใบที่คนเซ็นชนะเสมอ ใบ derive ใช้เฉพาะ
แถวที่ไม่มีใบเซ็นคลุมเลย · ติดป้าย `[สมมติของสาย LANE-B - รอ COO ยืนยัน]` ส่งเป็น D1
ในจดหมาย `2022`
### D2 · รูป "ใบเดียวทั้งโลก" widen 12 แถวที่ ratify แล้ว
เขียนใบเดียวไม่ผูกฉากก่อน (ตามที่ ka1-A `1635` เสนอตรง ๆ) แล้วชุดเทสเดิมปฏิเสธ
**และมันถูก** — `describe_widening_coverage` เปลี่ยนจาก 12 บรรทัด UNKILLABLE เหลือ
**0** คือมอนที่ shipped อยู่ 12 ตัวซึ่งวันนี้ฆ่าไม่ได้เพราะติดการผูกฉาก จะกลายเป็นฆ่าได้
จึงทิ้งรูปนั้น เปลี่ยนเป็นใบต่อฉากที่ generate จาก loop — แกนฉากแน่นเท่าเดิมเป๊ะ

## ที่ไม่ได้แตะ
- ไม่ได้แตะ `runtime.py` / `app.py` / `current/pf_login_game_server_v141.py`
- ไม่ได้แตะ `field_mob_tables_bg00xx.py` ไฟล์ไหนเลย · ไม่ได้แตะ roster ทะเล ·
  ไม่ได้แตะ `Bg3001` · `1644` (สิทธิ์ฆ่า `{8041,8180}`) ยัง DEFERRED ตามเดิม
  ไม่ได้เขียนคีย์ใหม่ให้ — และตอนนี้ยังยื่นซ้ำไม่ได้ เพราะกิ่ง
  `claude/nice-meitner-mf71tm` (roster ฉากทะเล) **ยังไม่ merge เข้า main**
  (`grep -c "300[1238]" src/pirateforce_foundation/field_mobs.py` = 0)
- ไม่ได้ปลดใบอนุญาตต่อฉากใบมือใบใดออก — ทั้ง 11 ใบยังอยู่ครบ ยังผูกฉากเหมือนเดิม
- ไม่ได้ออกคีย์ widen-death-scope **ต่อฉากใหม่** ตามที่ `1648` ข้อ 3 ห้าม (ใบที่
  เพิ่มเป็นใบ derive ที่อ้างใบ `1648` ใบเดียวกันหมด ไม่ใช่ใบขอใหม่ต่อเกาะ)

## pf-adversary
`ADVERSARY_PENDING claude/nice-meitner-0wef26` — สั่ง `pf-adversary` ตั้งแต่ต้นรอบ
พร้อมโจทย์โจมตี 6 ข้อ (a-f: การ widen ที่มองไม่เห็น · แกนฉาก · import-time
derivation + การ mutate `WIDENING_RULINGS` หลังสร้าง literal · เกตคีย์ยังจับของ
ปลอมไหม · เทสใหม่ vacuous ไหม · เกตเดิมสองไฟล์) **ผลยังไม่คืนตอนจบรอบ** ห้ามอ่าน
ไฟล์รอบนี้ว่า "ผ่าน adversary" — **รอบถัดไปของสาย B สั่ง adversary บนกิ่งนี้เป็น
งานแรก** ตามกฎ PENDING
Self-review ที่ทำจริงระหว่างรอบ: อ่าน `git diff --cached` ทุก hunk ก่อน commit ·
stage ทีละไฟล์ ไม่ใช้ `git add -A` · วัดสับเซต 59/60 ด้วยการรันจริงไม่ใช่การอ่าน ·
รูปใบเดียวไม่ผูกฉากถูก**ทดสอบแล้วว่าทำให้ 12 แถวที่ฆ่าไม่ได้กลายเป็นฆ่าได้** จึงถูก
ทิ้ง — นั่นคือ defect ที่รอบนี้จับได้เองก่อน adversary คืน

## verification
- `pytest tests/test_mob_death.py tests/test_mob_death_rule_derived_widening.py`
  → **107 passed**
- **ชุดเต็ม `pytest tests/` บนต้นไม้ที่ commit จริง (`14196f3`, หลัง
  `git merge origin/main` = no-op): 12447 passed · 373 skipped · 27507 subtests ·
  0 failed** (499.95s)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS**
  (cp874 · ไม่มี skip ใหม่ · main อยู่ในกิ่ง · census ตรง · ทั้งสองกิ่ง mergeable ·
  ไม่มีไฟล์สะพานโตเกิน ceiling · ไม่แตะแถว scoreboard มือ)
- **มิวเทชันสองแบบ รันจริง ไม่ใช่คำอ้าง**: ถอนการแบ่งกอง D1 ออกจาก `ruling_for` →
  **แดง 13 ตัว** · ถอนบรรทัดผูกฉากของใบ derive → **แดง 13 ตัว** (เทสไม่ vacuous)
- `pytest tests/test_mob_death_widening_schema_gate.py` → **passed** (เกตคีย์ของ
  รอบ `bvaptp` ยังจับได้ · ใบ derive ทุกใบตรง schema `1647` และชี้จดหมาย
  `20260906_1648_COO-DECISION-...-widen-...md` ที่มีอยู่จริง)
- `pytest tests/test_mob_scene_registration_contract.py` → **passed** (เทสแกนฉาก
  ที่ปฏิเสธรูปใบเดียว ตอนนี้เขียว)
- `pytest tests/test_mob_death_wired_widening.py` → **13 failed** (สามสาเหตุ
  ข้างบน) — **ไม่รันชุดเต็มและไม่ push PR เพราะรู้อยู่แล้วว่าไม่เขียว**
- ไฟล์ที่แตะทั้งสองเป็น ASCII ล้วน (`str.isascii()` ต่อไฟล์)
- ไม่ได้รัน `pf_gate_preflight.py` เพราะไม่เปิด PR เซิร์ฟเวอร์รอบนี้

## PR/status
- `pf_bridge` claim `#1550` (`claude/focused-ramanujan-0wef26`) — ปลดเมื่อจบรอบ
- `pirate-force-server` **`#946` เปิดแล้ว ไม่ draft** body มี `PF-AUTOMERGE: v4`
  ตั้งแต่เปิด GET ยืนยันแล้วว่า marker อยู่จริง · กิ่ง `claude/nice-meitner-0wef26`
  หัว `14196f3` · **สถานะตามจริง: เปิดแล้ว รอ gate** (ไม่ใช่ landed ไม่ใช่อยู่บน main —
  รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor` เอง)

## รอบหน้าทำอะไร (เรียงแล้ว)
1. **สั่ง `pf-adversary` บนกิ่ง `claude/nice-meitner-0wef26` เป็นงานแรก** (PENDING)
   — โจทย์ 6 ข้อที่สั่งไว้อยู่ในไฟล์นี้หัวข้อ pf-adversary เจอของต้องแก้ให้แก้บน `#946`
2. บริโภคคำตอบ D1 ของ COO (จดหมาย `2022`) — ถ้า COO ไม่เห็นด้วยกับ "ใบที่คนเซ็น
   ชนะใบ derive เสมอ" ย้อนบล็อกเดียวใน `ruling_for` + เทสคู่ของมัน
3. กิ่ง `claude/nice-meitner-mf71tm` (roster ฉากทะเล) merge แล้วเมื่อไร → ยื่น 1
   บรรทัดอ้าง `1644` ขอสิทธิ์ฆ่า `{8041,8180}` (Bg3001) · ตอนนี้ยื่นไม่ได้เพราะไม่มี
   ฉากทะเลที่ลงทะเบียนให้กฎ derive ถึง
4. ถ้า `#946` merge แล้ว: ฉากที่ 13 ที่ roster ลงจะเป็นตัวพิสูจน์จริงตัวแรกของ
   "เข้าอัตโนมัติ" — ต้องมี GT ยืนยันบนจอจึงจะย้าย SCOREBOARD เป็น DONE ได้
5. หนี้เดิมจากรอบ `mf71tm`: `tools/pf_scan_field_scene_candidates.py` ไม่ตรงกับ
   miner ยังไม่แก้
6. ตัดสินใจว่าจะบริโภค broadcast `20260904_0233_PANYA-DECISION-*` เมื่อไร (รอบ
   `bvaptp` เห็นแล้วและปล่อยไว้ ยังไม่มีใครตัดสิน)

TWO_SESSIONS_SAME_SCENE: ไม่เปลี่ยน — รอบนี้ไม่แตะ `DeathRegister` ไม่แตะ
`runtime.py` ไม่สร้าง state ต่อ session ใหม่แม้แต่ตัวเดียว การ derive เป็นการอ่าน
ตารางที่ commit แล้วตอน import ผลเท่ากันทุก process ที่ import โมดูลเดียวกัน

SCOREBOARD: COMING | monster in a new field scene becomes killable the day its roster lands, with no per-island COO letter -- 11 such letters were written before this, the 12th is not needed | pirate-force-server#946 (open, awaiting gate, head 14196f3) - full suite 12447 passed 0 failed - preflight PASS - letter notes_to_chief/20260906_2022_LANE-B-TO-COO-switch-done-one-rule-replaces-eleven-kill-permits.md
