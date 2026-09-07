# LANE-B รอบ `najn72` — 2026-09-08T03:02+07:00 → ~03:5x+07:00 · ล็อก `pf_bridge#1841`

## รอบนี้ขยับ NOW/M ข้อไหน
**M3 → M4** และเป็นข้อที่ **เจ้าของติ๊กเอง** (`notes_to_chief/20260908_0025_KA1A-PANYA-TICK-COO-4-items-...` ข้อ 1 คำต่อคำ **"ทำพร้อมกัน"**) ซึ่ง `NOW.md` บรรทัด LANE-B วางไว้เป็นงานถัดจาก `#1098`:

> **`0025` `bg0002` roster 12→52 + death scope `{27..35}` คอมมิตเดียว**

ทำครบทั้งสองครึ่ง **ในคอมมิตเดียวจริง** (`92d3ba7`) ตามที่เจ้าของสั่ง

- งานแรกตาม NOW (**ดัน `#1098` เขียว+merge**) — **จ่ายแล้วก่อนรอบนี้เริ่ม**: `#1098` merge 2026-09-08 02:50 +07 (`github-actions`) · ยืนยัน `git merge-base --is-ancestor b712762 origin/main` ✅
- **ปิด `#1089`/`#1077`** — ไม่ต้องทำ: วัดผ่าน API รอบนี้ ทั้งสองใบ `state=closed` `merged=true` ไปแล้วทั้งคู่ (19:50Z)

## เกณฑ์วัดที่เจ้าของเขียนไว้ในใบติ๊ก — ตรงทั้งสองข้อ
เจ้าของเขียนว่า *"เกณฑ์วัด: `MOB_DEATH_WIDENING_COVERAGE scene=bg0002` ครอบครบ + census ฉาก 2 roster=52 บนคอนโซล headless"*

```
MOB_DEATH_WIDENING_COVERAGE scene=Bg0002 letter_covers=52 of 52 (authorisation only - ...)
field_mobs.load_roster(scene='Bg0002') -> 52
MOB_CENSUS_HOSTILITY scene_id=2 scene=Bg0002 roster=52 backed=52 unbacked=none refused=8 ...
```

**ครอบครบ = 52 of 52 ไม่มีบรรทัด `UNKILLABLE` เลย** — ไม่มีมอนตัวไหนบนแมพที่หมัดไปถึงแล้วไม่มีใบไหนอนุญาตให้ตาย

## สิ่งที่รอบนี้ส่ง (`pirate-force-server` PR ของรอบ)
### คอมมิตที่หนึ่ง `92d3ba7` — สองครึ่งที่เจ้าของสั่งให้ไปด้วยกัน
- `field_mob_tables_bg0002.py` regenerate ด้วย `--identity-rule cline --outfit-rule any` (กฎที่เคาะ `1313`): **17 แถวในตาราง / 12 แถวที่ ship → 52 แถว** · เทมเพลต `{31,34,35,103}` → **`{27..35}`** ครบบล็อกที่ ADDENDUM ตั้งชื่อไว้ · **ไม่มีค่าไหนพิมพ์เอง** ทุกแถวออกจากเครื่องมือ
- `mob_death.WIDENING_RULINGS[... widen-death-scope-bg0002]`: `{31,34,35,103}` → `frozenset(range(27,36))`
- **103 ออกจากใบ** พร้อมแถวที่เคยถือมัน: placement 92-96 เป็นแถวที่เจ้าของห้ามวาง และกฎ cline ไม่ resolve เป็นร่างที่มีชื่อเลย ⇒ ใบที่อนุญาต 103 = อนุญาตร่างที่สายนี้ไม่ส่ง
- **27 เข้าใบ** และไปทับกับใบ `diag-mountain-deer-template-27` — แยกกันด้วย **ฉาก** ไม่ใช่เทมเพลต (`WIDENING_RULING_SCENES` + `kill()` เช็ค `mob.scene`) เดินจริงในเทส ไม่ใช่อ่านคอมเมนต์

### คอมมิตที่สอง `1f702cc` — ตารางที่ต้องตามไปด้วย ไม่งั้นผู้เล่นเจอมอนที่เซิร์ฟเวอร์ให้บริการไม่ได้
🔴 **สองอย่างนี้ไม่ใช่หมุดค้าง แต่เป็นดีเฟกต์จริงที่การพลิกสร้างขึ้น และวัดได้ก่อนแก้:**
1. `field_mob_ai_tables` — 40 แถวที่กลับเข้ามาชี้ `AI_COMBAT` แถว **110 / 150 / 164 / 210** ซึ่ง**ไม่เคยถูกขุด** ⇒ ตีมอนใหม่ตัวใดก็ได้ = `MobAiControlError: ai_row_missing` (เห็นจริงใน `test_scene_scoped_combat_wiring` ก่อน regenerate)
2. `field_drop_tables` + `scenarios/combat_loot_001.json` — แถวใหม่ถือ `DROPS_SPECIALLY` เซต **2802202** ที่ไม่อยู่ในตารางที่ขุด ⇒ ฆ่าแล้ว `MobLootContractError: unknown_drop_set`
regenerate ทั้งคู่ด้วยเครื่องมือของมันเอง (ห้าม patch มือ): AI +4 แถวคอมแบต · ไอเทม 85 → 88 · เซต specially +1

## สองข้อที่ไม่ใช่หมุดค้าง แต่เป็น "ผลที่วัดได้" ของการพลิก — บันทึกเป็นการวัด ไม่ใช่กลบ
1. **ฉาก 2 ไม่มีมอนที่เข้าตีเองแล้วเลย** — 52 แถวเป็น `ai_wander 16` (`n_OFFESIVE = 0`) ทั้งหมด · ห้าแถว Orc Chief ที่เคยเป็น wander 11 คือแถวที่ crosswalk ไม่ resolve
   ⇒ ฟิกซ์เจอร์ทุกไฟล์ที่ต้องการ "มอนที่ชาร์จเข้ามา" ย้ายไป **Bg0003 placement 33 (Ward Apes, wander 11)** ซึ่ง **สายนี้ ship จริง** — ของเดิมคือแถวที่ `OWNER_REFUSED_PLACEMENTS` กันออกจากทุก roster อยู่แล้ว แปลว่าเทสพวกนั้นวัดร่างที่ไม่มีผู้เล่นคนไหนเจอได้ (ดีขึ้น ไม่ใช่แค่ย้าย)
   แก้ประโยควัดใน `mob_aggro.py` ตามที่การ์ดของมันเองสั่งไว้: ประโยคที่ขีดฆ่ายัง**ขีดฆ่าอยู่** (เพราะมันอ้าง "ทุก roster") แต่ตัวเลขที่มันอ้างวัดใหม่บน Bg0003
2. **actor identity ชนข้ามฉาก 52 → 103 คู่** (ใหม่ 56 · หายไป 5) เพราะ placement index ของฉาก 2 เดินยาว **31-88 ไม่ขาด** = แถบเดียวกับที่ทุกฉากใช้ · identity คือ `0x2000 + placement + 1` ไม่มีเทอมฉาก
   เดินซ้ำ ไม่รับมรดก: death register คีย์ `(scene, identity)` · ledger เปิดต่อ scene id · admission ปฏิเสธ ledger ต่างฉากเป็น `other_scene` · loot cell ผูกฉากปัจจุบัน · **ไม่มีคู่ไหนเทมเพลตตรงกันทั้งสองข้าง** (เช็คทั้ง 103 คู่ด้วยลูปของเทสเอง)
   ห้าคู่ที่ **หายไป** คือ `0x205D-0x2061` (Bg0002/Bg0010) — คือแถว Orc Chief นั่นเอง · การ์ดนี้ตั้งชื่อคู่แทนที่จะนับ ก็เพื่อให้ "คู่ที่หายไป" มองเห็นได้แบบนี้

## หมุดที่ re-pin (ทุกจุดมีเหตุผลกำกับในที่ ไม่ใช่สลับตัวเลข)
`test_field_mob_tables_bg0002` (17→52 · 4→9 เทมเพลต · 49→104 unambiguous · byte-for-byte control เรียกกฎใหม่ทั้งสองตัวโดยระบุชื่อ ไม่รับค่า default) · `test_field_mobs` (12→52 · ตำแหน่งไม่ซ้ำยังจริงทั้ง 52 · การ์ดชน 52→103) · `test_mob_death` · `test_mob_census_hostility` (ghost ย้ายไป Bg0008 placement 69 "Nina" ซึ่งยัง filter จริง) · `test_mob_ledger_admission` · `test_mob_combat` (STANDARD_MOB +4 เลเวล 16/17/19/23 · ตารางราคาใน `mob_combat.py` 2 แถว→6 แถว) · `test_mob_combat_dispatch_bg0002_kill` (drop rate 252/24/84 → 1092/104/364 · สัดส่วนเท่าเดิม) · `test_mob_combat_bg0015_gates` (ชน Bg0002×Bg0015 1→8 คู่) · `test_mob_ai_scheduler` · `test_lane_b_mob_ai_tick` · `test_mob_ai_control` · `test_mob_ai_control_rule_join` (99→139) · `test_scene_identity_rule` · `test_mob_diag_multi_object` · `test_mob_death_rule_derived_widening` · `test_pf_mine_scene_mob_roster_outfit_rule` · `docs/PYTEST_SKIP_PINS.json` (สองใบเปลี่ยนชื่อเทส ไม่ได้เพิ่ม/ลบ/ย้าย skip)

**สามใบที่เคยเป็น "ยามกันวันนั้น" และรอบนี้คือวันนั้น** — ไม่ได้ลบ แต่กลับด้าน:
- `test_pf_mine_scene_mob_roster_outfit_rule::...says_so_by_absence` → กลายเป็น **อินเทอร์ล็อก**: เทมเพลตของ roster ต้อง `==` เซตของใบ death ⇒ ครึ่งไหนขยับเดี่ยว = แดง (นี่คือ "ทำพร้อมกัน" ที่เขียนเป็นโค้ด)
- `test_scene_identity_rule::..._still_ships_under_the_legacy_rule_this_round` → docstring ของมันบอกว่า "รอบที่พลิกต้องตอบเรื่องแมพจาก 17 เหลือ 12" · **ตอบแล้ว**: เลข 12 เป็นเลขของ crosswalk เดี่ยว ๆ เจ้าของเปลี่ยนกฎที่สองพร้อมกัน (`s_OUTFIT` ไม่ตัดสิน) ⇒ **17 → 52** ปักทั้งสองกฎเพื่อไม่ให้พลิกทีละอันแล้วผ่าน
- `test_mob_death_rule_derived_widening::..._does_not_excuse_another` → พยานเดิม (เทมเพลต 27) ใช้ไม่ได้แล้วเพราะ 27 อยู่ในใบของ Bg0002 จริง ๆ · ย้ายพยานไป **103** (อยู่ใน union แต่ไม่อยู่ในใบของ Bg0002) — คุณสมบัติที่ป้องกันเหมือนเดิมทุกตัวอักษร

## แตะไฟล์เทสของสาย A หนึ่งไฟล์ — บอกไว้ตรง ๆ ไม่ได้ทำเงียบ
`tests/test_lane_a_choose_npc_scene2.py` สองบรรทัด: `HOSTILE_COUNT 12→52` · `from_ledger=11→51`
**ไม่ผ่อน assertion ใดเลย** · `ROSTER_COUNT = 97` ไม่ขยับ · `test_every_hostile_row_is_one_of_the_ninety_seven` เขียวโดยไม่ต้องแก้ (ทั้ง 52 แถวอยู่ใน census 97 ของ A ครบ · วัดอิสระอีกทางด้วย `census_backing_report` → `unbacked=()`)
เหตุผลที่แก้แทนที่จะปล่อย: ปล่อยไว้ = main แดงให้ทุกสาย · จดหมาย `20260908_0340_LANE-B-TO-LANE-A-...` บอก A แล้ว พร้อมเสนอถอนคืนถ้า A อยากเขียนเอง

## หลักฐาน
- `MOB_DEATH_WIDENING_COVERAGE scene=Bg0002 letter_covers=52 of 52` · `roster=52` (headless บนทรีนี้)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS** (ครั้งแรกแดงที่ `[census]` เพราะรอบนี้เปลี่ยนชื่อเทสที่มียาม 2 ใบ — แก้ `PYTEST_SKIP_PINS.json` ให้ตรงชื่อ ไม่ได้เพิ่ม/ลบ skip)
- ชุดเต็ม `pytest tests/` บนต้นไม้ที่ merge `origin/main` แล้ว: **`14039 passed, 632 skipped, 38390 subtests` ไม่มีแดง** (rc 0 · 536 วินาที · คอมมิต `ae5cffe`) · รันซ้ำบน `b5226fc` (คอมมิตสุดท้ายจริง หลังบริโภค adversary) ผลใน PR
- ซ้อมรูปเกต worktree ไร้ sibling: **การรันข้างบน *คือ* การซ้อมนั้น** — รันในworktree ที่ parent ไม่มี `pf_bridge` ข้าง ๆ (`.../scratchpad/gate/pirate-force-server`) ⇒ เทสที่ต้องพึ่งสะพาน skip ตามหมุด (632 skipped) และไม่มีอะไรแดง · `pf_gate_preflight` เขียวบนคอมมิตสุดท้าย
- ไม่มีไบต์นอก ASCII ในดิฟฝั่งเซิร์ฟเวอร์ (`git diff | grep -cP '^[+].*[^\x00-\x7F]'` → 0)

## กติกาที่รอบนี้ทำ/ไม่ได้ทำ
- **ADVERSARY RETURNED — และผลไม่สะอาด** สั่ง `pf-adversary` ต้นรอบบนกิ่งนี้ ผลคืน**ก่อนปลดล็อก** จึงบริโภคในรอบเดียวกัน ไม่ผลักไปรอบหน้า
  🔴 **สองข้อ CRITICAL ของมันคือ D1/D2 ที่รอบนี้เจอเองและแก้ไปแล้วใน `1f702cc`** — แต่มันวัดลึกกว่าที่รอบนี้อ้าง: ทั้งสอง `raise` **หลุดออกจาก `dispatch()`** (นอก `except`) ไม่ใช่แค่เทสแดง
     - D1: บน `92d3ba7` ฉาก 2 **ไม่ส่ง census เลย** (`world_census_sent: False`) ⇒ ผู้เล่นเข้าเมืองแล้วเจอ**โลกว่าง 97 ตัวหายหมด** · และ ActionVital ใด ๆ ในฉาก 2 = traceback หลุดออก dispatch (เธรด listener ตายแบบ v141:7558)
     - D2: 16 จาก 52 แถวฆ่าแล้ว `raise` ออกจากเลนลูท (`roll_drops` อยู่**นอก** `try`) · เซตที่ขาดมี **สาม** ตัว (2802202/2802222/2802228) ไม่ใช่ตัวเดียวอย่างที่คอมมิตแรกเขียน
  **แก้เพิ่มในรอบนี้ (`b5226fc`)**: **D3** (`refused=8` เป็นเลขเท็จ — ฟิลด์นับ *ใบสั่ง* ไม่ใช่ *ผล* · แก้เป็น intersection + เพิ่ม `refused_ruled` เก็บความกว้างของใบไว้) · **D8** (docstring สองที่ใน `src/` อ้างเลขที่ derive ซ้ำไม่ได้แล้ว)
  **ยังไม่แก้ ยกไปรอบหน้า พร้อมความรุนแรง**: D4 (HIGH · ledger ของฉาก 2 ครอบ **เต็ม 100%** ของ bg0005/bg0006/Bg0009 ⇒ คอลัมน์ `covered=6/6` แยกจาก ledger ที่ถูกต้องไม่ได้ · เหลือแค่การเทียบสตริงฉากที่กัน) · D5 (MEDIUM · ครึ่ง widening **ไม่มีผลเชิงพฤติกรรม** — derived permit ครอบทุกแถวอยู่แล้ว วัดด้วยการใส่เซตเก่ากลับ → uncovered 0 ⇒ ประโยค "ไม่งั้นฉากจะมีมอนที่ไม่มีใบให้ตาย" ในคอมมิตแรก**ผิด** แก้ถ้อยคำใน PR แล้ว) · D6 (MEDIUM · drift guard ของ owner-refusal join ของสองอย่างที่ทั้งคู่มาจากกฎที่ถูกถอน · และ placement **97 ไม่อยู่ในลิสต์ไหนเลย**ของโมดูลใหม่ ⇒ ประโยค "89,90,92-97 withdrawn หรือ unresolved ทั้งหมด" ในคอมมิตแรกผิดสำหรับ 97) · D7 (MEDIUM · survey self-aggro ครอบ 1 จาก 12 ฉาก และ premise ผิด — wander 10/21/22 ก็ `n_OFFESIVE=1`) · D9 (MEDIUM · บรรทัดคอนโซล 466 อักขระ ไม่มีเพดาน) · D10 (MEDIUM · `scene_door_walk` เห็น D1 ทั้งหมดแล้วไม่มีเทสถาม Bg0002) · D11 (MEDIUM · เกณฑ์ที่สองของเจ้าของคือบรรทัด **census** ไม่ใช่การอ่านตาราง)
  🔴 **คำถามออกแบบที่มันตั้งและรอบนี้ตอบไม่ได้**: `field_mob_ai_tables` · `field_drop_tables` · `field_mob_tables_bg0002` เป็น**หน่วย regenerate เดียวกัน** แต่ไม่มีอะไรที่ *รันได้* พูดแบบนั้น — ยามของสองตัวแรกไปอยู่ในไฟล์เทสของ **ฉากที่สี่** ⇒ regenerate ครึ่งเดียวแล้วแดงหลัง push เท่านั้น · เสนอ COO รอบหน้า
- บริโภคจดหมายถึงสายนี้ครบ: chief `0204` (R396) · COO `0242` §3 — stub `.CONSUMED.txt` + สำเนาไป `consumed/`
- **ไม่แตะ** `runtime.py` · `app.py` · v141 · `world_*.json` · ไม่แตะ canonical DB · ไม่ skip/xfail/disable เทสใด
- `TWO_SESSIONS_SAME_SCENE:` — รอบนี้ไม่เขียน combat state ลง registry ของ A เพิ่ม สิ่งที่ขยับคือ**เนื้อหาของ roster ที่ A อ่านผ่าน interface เดิม** (`load_roster` / `roster_for_scene_id`) ⇒ สองเซสชันในฉาก 2 เห็น 52 ตัวเดียวกัน ไม่ใช่คนละชุด เพราะ census ของ A ยังเป็น 97 actor ชุดเดิม
- RE `0032` (`IsOffensive()` = `AI_WANDER[key].n_OFFESIVE`) **บริโภคแล้วในรอบนี้ ไม่ใช่ `NO_FEATURE_WAITING:`**: เป็นเครื่องมือที่ทำให้ข้อ 1 ข้างบนเป็นการวัด ไม่ใช่ความเห็น — ฉาก 2 ทุกแถวชี้ wander 16 ⇒ `IsOffensive()` คืน false ทั้งฉาก และเทสปักไว้ทั้งสองด้าน

## ส่งอะไรให้ใครแล้ว
- `notes_to_chief/20260908_0340_LANE-B-TO-K-flagged-mechanism-proof-...` — โทเคน `set=ALL actors=22 ... commit=b279c4b` วัดบน `origin/main` สะอาดแล้ว (เพราะ `#1098` ลง main) ⇒ K ใส่สแนปช็อต `GT-288` ชุด 3 ได้
- `notes_to_chief/20260908_0340_LANE-B-TO-LANE-A-...` — roster 52 แถว + หมุดสองจุดในไฟล์ของ A + เรื่อง identity ชน 103 คู่

## รอบหน้าทำอะไร (งานแรกก่อน)
1. บริโภคผล `pf-adversary` ของ PR รอบนี้ (ถ้าคืนหลังปลดล็อก) แล้วแก้ของที่มันเจอ
2. หนี้ adversary ค้างจากรอบ `ubmvj1` ที่ยังไม่จ่าย: **D4 · D5 · D7 · D9** (D7 หนักสุด — พิกัด X/Y ยังผูกกับลำดับวาด ต้องผูกกับป้ายก่อน chief เสียบ viewer identity)
3. ยึดชื่อสองตัวที่ chief ฝากคืนให้สายนี้ (`0204`): ประกาศ `name_colour_sweep.SWEEP_SETS_WANTING_AN_EMPTY_WORLD` และรับ `viewer_identity=` เมื่อ `#1099` ลง main → ALL เป็น 24 ป้าย → วัด `NAME_COLOUR_SWEEP_ARMED` บน main ส่ง `HEADLESS_PROOF:` ให้ K
4. ตามคิว `NOW.md` ต่อ: `name_tokens` → `GT-300` → **respawn 120 s** (มอนที่ตายแล้วเกิดใหม่ = ครึ่งหลังของ M4 ที่ยังไม่มี)
5. ออกใบ GT ให้ฉาก 2: 52 ตัวบนแมพ ตีได้ ตายได้ ของตก — ตอนนี้มีทั้ง roster และใบอนุญาตครบแล้ว ขาดแค่คนไปยืนดู

SCOREBOARD: COMING | เกาะคุก (ฉาก 2) มีมอนศัตรูจริง 52 ตัวจาก 9 ชนิด แทนที่จะเป็น 12 ตัวจาก 3 ชนิด: 40 ร่างที่เมื่อวานเป็นฉากหลังคลิกไม่ได้ วันนี้คลิกแล้วขึ้นแผงเป้าหมายพร้อมเลือดจริง ตีได้ ตายได้ด้วยใบอนุญาตของฉากตัวเอง และมีตารางลูทกับ AI ของตัวเองครบ | pirate-force-server PR รอบนี้ (`b5226fc`) + pf_bridge#1841
