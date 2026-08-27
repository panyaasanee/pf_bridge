# R162 (session `qwtyq9` / branch `claude/epic-franklin-qwtyq9`) — 2026-08-25 ~10:5x–12:xx (+07:00)

> **หัวข้อรอบ:** สร้างเลนโค้ด **`HYP-PF-038 HOSTILE-HP-LINK-001`** ที่ใบ GT-035 รออยู่ + แก้ใบสองใบตามจดหมายหน้าสะพาน
> **ล็อกรอบ:** draft PR `pf_bridge` **#64** (`WIP round claim qwtyq9`) เปิดตั้งแต่ 10:5x (+07:00) ก่อนแตะงานใดทั้งสิ้น

---

## ① การ์ดกันรอบซ้อน + PROBE (ทำก่อนอย่างอื่นทั้งหมด)

- `git fetch --all` แล้วถาม GitHub API หา PR เปิดค้างทั้งสอง repo ⇒ **ไม่มีเลยสักใบ** (`state=open` คืนลิสต์ว่างทั้งคู่)
- จับล็อกทันที: empty commit `round claim: qwtyq9` → push → **เปิด PR เป็น draft ตั้งแต่วินาทีแรก** พร้อมบรรทัด `PF-AUTOMERGE: v4` ในบอดี้
  ⇒ ✅ ท่า v5.1 ทำงานตามที่ออกแบบ: draft ไม่ถูก `merge-claude-pr` แตะระหว่างรอบ (workflow ข้าม draft) และล็อกไม่หลุดกลางทางเหมือนรอบ R114–R118
- **PROBE ข้อ 1 (GitHub API/tool):** ✅ อ่านได้จริง (`list_pull_requests` ทั้งสอง repo · `create_pull_request` พร้อม `draft: true` สำเร็จ)
- **PROBE ข้อ 2 (ทาง D `ci-status`):** ✅ มีชีวิต — `git fetch origin ci-status && git ls-tree --name-only origin/ci-status ci/` คืนรายการไฟล์คำตัดสิน `d_exit=0`
- โครงพี่น้อง: `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` **มีอยู่จริง** ✅
- เลขรอบ: ไฟล์สูงสุดใน `rounds/` บน `main` ที่เพิ่ง fetch = `R161` ⇒ รอบนี้คือ **R162** (ไม่ชนกับใคร)

## ② กล่องจดหมาย — บริโภคหนึ่งใบ

`20260825_1010_GT035-DESIGN-CONSTRAINT-hyp038-must-inherit-arena-player-relative-placement.md`
(สำเนาไป `consumed/` + stub `.CONSUMED.txt` · ต้นฉบับอยู่ที่เดิม)

**สาระ:** ดีไซน์ `HYP-PF-038` ต้องบังคับว่าวางเป้าแบบ `player_relative` ไม่ใช่ placement จริง มิฉะนั้นรอบ attended จะจบเป็น NO-RESULT ด้วยกฎของใบเอง
· ห้ามเติม `damage` เข้า caps ของ arena เพื่อให้ผ่าน · และ `HYP-PF-032` เต็ม 3/3 แล้ว (GT-045 v3 คือใบสุดท้าย)

**ตรวจซ้ำเองครบทุกข้อด้วย `pf-static-re` (อ่านไฟล์จริงในโคลนรอบนี้) — จดหมายถูกทุกข้อ:**

| ข้อ | ผล | pin |
|---|---|---|
| แถว placement 30 | ✅ ตรงทุกตัวอักษร | `current/pf_login_game_server_v141.py:1349` |
| `aid = 0x2000 + idx + 1` ⇒ `0x201F` | ✅ | `v141:1095` · `:1459` · `:1917` · `scenario.py:101` · `population.py:46` (**เขียนซ้ำ 5 ที่ ไม่มี single source**) |
| เส้น default วางพิกัดโลกคงที่ | ✅ | `v141:1908` (signature ไม่มี argument ตำแหน่งผู้เล่น) เรียกที่ `:4294` ใต้ `:4293` |
| arena วาง player-relative | ✅ | `arena_v1.json:10-14` → `scenario.py:97-98` · heading `:117` |
| ปิดเส้น default ต่อเซสชัน | ✅ | `runtime.py:3638-3642` + `:3608-3615` |
| allowlist ของ arena มี `damage` เป็น nonclaim | ✅ | `scenario.py:82-83` raise `:86` · ผู้บริโภค 3 ไฟล์ (`tests/test_arena.py:110-113` วัดตรง) |
| `HYP-PF-032` 3/3 · `HYP-PF-029` 3/3 · slot สูงสุด = 037 | ✅ | `docs/HYPOTHESIS_LEDGER.json` · `HYP-PF-038` grep = 0 บรรทัดทั้ง repo |

**ของแถมที่ลูกมือเจอ (ไม่ได้แก้รอบนี้ จดไว้เป็นงานแม่บ้าน):** `scenario.py:28-29` มี `_CAPABILITIES` / `_NONCLAIMS` เป็น **set ที่ไม่มีใครอ้างถึงเลยทั้ง repo** ⇒ เป็นแหล่งความจริงคู่ขนานกับกฎจริงที่บรรทัด 82-83 · ใครแก้ set แล้วนึกว่าแก้กฎ จะได้กฎเดิมแบบเงียบ ๆ

## ③ งานหลัก — เลน `HYP-PF-038 HOSTILE-HP-LINK-001` (repo โค้ด)

**ไฟล์ใหม่ 4 · แก้ 6** (สถานะสุดท้ายหลัง R162-b) — ใหม่: `src/pirateforce_foundation/hostile_hp_link_hypothesis.py` · `scenarios/hostile_hp_link_hypothesis_p30_sweep.json` · `tests/test_hostile_hp_link_hypothesis.py` · `tools/pf_hostile_hp_link_headless_replay.py` · แก้: `app.py` `runtime.py` `docs/HYPOTHESIS_LEDGER.json` `docs/FUNCTIONAL_COVERAGE.json` `tools/verify_hypothesis_ledger.py` `.gitignore`

**สิ่งที่เลนทำ (สรุปหนึ่งย่อหน้า):** ยิง 7 เฟรมสลับสองตัวขน (CHitResult ↔ actor-entry) ที่ **hostile ตัวจริง `0x201F` "Tornado Eagle"** ซึ่งมี HP baseline **3857** จากข้อมูลฝั่ง client (`V117_P30_EXACT_HP`) — ต่างจากพี่ชาย `HYP-PF-029` ที่ยิง `0x2001` สังเคราะห์ด้วย ladder 100 ที่เราแต่งเอง

**หกจุดที่ตัดสินใจต่างจากพี่ชาย และเหตุผลที่วัดได้:**

1. **เลือกเป้าด้วยเลข index ตรง ๆ ไม่ใช่ "ใกล้จุดเกิดที่สุด"** — กฎ nearest ของ 029 ให้ index 0 เสมอ · index 30 อยู่ห่างจุดเกิด ~12,000 หน่วย ⇒ nearest ไม่มีวันเลือกมันได้
2. 🔴 **วางเป้าแบบ player-relative (dx100/dy50/dz0 ยืมจาก arena)** และ resolve **ตอน dispatch** ไม่ใช่ตอน construct — เพราะตำแหน่งผู้เล่นยังไม่มีตอนสร้าง state class · อ่านจากแถว authoritative ที่เส้น TargetPos checkpoint ไว้ (`selected.position`)
   ⇒ เซสชันที่ยังไม่มีตำแหน่ง **ประกอบเฟรมไม่ได้เลย** · และถ้าผู้เล่นบังเอิญยืนตรงจุดที่ทำให้เป้าตกลงบน frozen world row พอดี ⇒ **ปฏิเสธตามชื่อ** (`target_placement_is_the_frozen_world_row_not_player_relative`) เพราะแยกไม่ออกว่าใครวาด
3. 🔴 **ไม่มีครึ่งตายเลย** — ไม่มีเฟรม hp=0 · ไม่มี death timer · **ไม่มี clamp**: การ move ที่จะถึงพื้นเป็น **named refusal** (`hp_clamp_is_forbidden_in_this_lane`) ไม่ใช่การ clamp เงียบ ๆ แบบพี่ชาย
   · `HOSTILE_HP_LINK_LETHAL_STEP_LABELS = ()` และ `HOSTILE_HP_LINK_TIMER_BY_STEP = {}` **ถูกบังคับให้ว่างโดย `_require_step_plan`** ⇒ ใครจะเอาครึ่งตายกลับเข้ามาต้องแก้ทั้งสองบรรทัดนี้ด้วย = diff ที่หลุดมาโดยบังเอิญไม่ได้
4. **สูตรไม่แก้ แก้แต่โปรไฟล์ผู้โจมตี** — `attack = 100 + 7·str + 3·lv` เทียบ `def = 10 + 2·con + 1·lv` เหมือน HYP-PF-024/029 เป๊ะ
   · เหตุผลที่ต้องเปลี่ยนโปรไฟล์: **`-63` บนหลอด 3857 = 1.6% ตาคนอ่านไม่ออก** ⇒ สวีตที่ขยับไม่เห็นตอบอะไรไม่ได้เลย
   · MOB_WEAK lv7 str132 ⇒ **-964** · MOB_STRONG lv15 str294 ⇒ **-2122** · defender lv27 con22 (lv27 = STANDARD_MOB ของแถวนี้)
   · ladder = `(3857, 3857, 2893, 2893, 2893, 2893, 771)` ⇒ **75.0%** แล้ว **20.0%** ของหลอด · ทุกค่า **re-derive จากค่าคงที่ทุกครั้งที่เรียก** ไม่มีเลขไหนถูกพิมพ์ลงแถว step
5. 🔴 **byte pins กลายเป็นสองระดับ และนี่คือความต่างเชิงโครงสร้าง** — เพราะทุกเฟรมมี f32 สามตัวที่ขึ้นกับตำแหน่งผู้เล่น
   · **size pins** ใช้ได้ทุกเซสชัน (พิกัดกว้าง 4 ไบต์เสมอ) · **sha pins** ใช้ได้เฉพาะ probe geometry (V135 spawn + offsets) และเฉพาะ probe performer สำหรับสามเฟรม hit
   · ทุก build จึง **recompose ทั้งสวีตที่ probe geometry อีกรอบ** แล้วเทียบ sha ⇒ encoder ที่ drift ส่งไม่ออกแม้แต่ครั้งเดียว ทั้งที่ไบต์ของเซสชันสดไม่มีตัวไหนถูก pin ด้วย sha เลย
6. **เพิ่มฟิลด์ชื่อ (BasicAttr bit 0x0001)** ที่พี่ชายไม่มี — แผง target อ่าน label จาก BasicAttr `+0x28` ⇒ หลอดที่ขยับบนตัวที่ไม่มีชื่อจะทิ้งคำถาม "นั่นตัวไหน" ไว้ · เฟรม spawn มี ASCII `Tornado Eagle` + preset `M011_000_000_SP3` ตามที่ใบ GT-035 ชั้น (1) เรียกร้อง

**เรื่อง `tools/` — ย่อหน้านี้ถูกเขียนใหม่หลัง R162-b:** ฉบับแรกของรอบนี้ **ไม่ได้ส่ง** ทั้ง `tools/verify_*` และ headless replay โดยอ้างว่าเลนล่าสุดสองเลนเลิกทำแล้ว · `pf-adversary` ค้านว่า **ใบ GT-035 ชั้น (1) สั่งไว้ตรง ๆ** และไม่มีแถวของเลนนี้ใน gate ⇒ **ยอมรับ แล้วเขียน `tools/pf_hostile_hp_link_headless_replay.py` จริงในรอบเดียวกัน**
✅ ส่งแล้ว: ขับ refusal 8 ตัวแล้วพิมพ์ชื่อ · **decode พิกัดที่เฟรม `TARGET_SPAWN` วางตัวนกไว้จริง** สำหรับพิกัดผู้เล่นใด ๆ · socket trap · ไม่รับ `--db` · exit 0/1
🔴 **ที่ยังไม่ได้ส่งคือ `tools/verify_*` แยกอีกตัว** — ด่านของ encoder อยู่ในสวีตเทสแทน (`RefusalTests`) · ถ้า Panya อยากได้ตัวนั้นด้วย สั่งเป็นรอบแยกได้

**ledger:** append `HYP-PF-038` ท้ายสุด (entry ที่ 46 · ไม่ขยับ index เก่า) · **1 of 3 versions** · `production_allowed: false` · `extension_approval_ref: null`
· `tools/verify_hypothesis_ledger.py` เพิ่ม `EXPECTED_IDS` + `EXPECTED_META` + บล็อก lineage + **re-pin canonical sha** (ค่าสุดท้ายหลัง R162-b = `475CE05F…`)

## ④ ผลรัน (ที่นี่ = cloud sanity เท่านั้น ห้ามอ่านเป็น gate)

```
python3 -m pytest tests -q      2345 passed · 324 skipped · 4485 subtests   เขียว(cloud sanity)   [ตัวเลขสุดท้ายหลัง R162-b]
python3 tools/pf_hostile_hp_link_headless_replay.py   PASS ทุก check (probe geometry และพิกัดสด)  exit 0
python3 tools/pf_pytest_precondition_census.py --run   RESULT: PASS (skip ใหม่ 0 ตัว)
python3 -m pytest tests/test_foundation_legacy_seam.py  22 passed (บังคับเพราะรอบนี้แตะ .gitignore + coverage)
python3 tools/verify_hypothesis_ledger.py      HYPOTHESIS_LEDGER PASS entries=46   exit 0
python3 tools/verify_functional_coverage.py    FUNCTIONAL_COVERAGE PASS domains=8  exit 0
git diff --check                                เงียบ
current/pf_login_game_server_v141.py            ไม่ถูกแตะ (diff ว่าง)
```
🔴 **ยังไม่มีคำว่า "เขียว" ระดับ gate ในรอบนี้** — gate ตัวจริงคือ Actions (subset) และสะพานของ Panya (ตัวเต็ม) · PR ของรอบนี้ต้องรอ Actions ตัดสินก่อน merge

## ⑤ คิวเทสเกม — แก้สองใบ (ไม่มีใบใหม่)

- **GT-035** เพิ่มบล็อก R162: ยกระดับ placement เป็น **เงื่อนไขก่อนรอบ** · เพิ่ม **ด่านก่อนบูตข้อ 6** (static grep หา `player_relative` ต้องเจอ · หา `1747.5`/`-7837.6` ในไฟล์ scenario+โมดูลต้องไม่เจอ · มี positive control กันเคส "คำสั่งไม่ได้รัน") · **ข้อห้ามแตะ allowlist ของ arena** · ช่องกรอกผล R6-1/R6-2/R6-3 ที่แยก "ไม่เห็นตัวนก = เรื่องระยะวาด" ออกจาก "damage ไม่ทำงาน"
  · แก้ด่านข้อ 3 จาก `&& echo SCENARIO_PRESENT` เป็น `$LASTEXITCODE` เพราะ **`&&` ไม่ใช่ตัวคั่นคำสั่งบน PowerShell 5.1** (ใบอื่นยังใช้รูปเดิม — งานแม่บ้านรอบหน้า)
- **GT-045 v3** เพิ่มบล็อก R162: เตือนบนหัวใบว่า **`HYP-PF-032` เต็ม 3/3 ⇒ v3 คือใบสุดท้าย ไม่มี v4** + ตารางแมปแถว A–E ว่าแถวไหน "ตอบแล้ว" แถวไหน "กำกวม" และ **ขั้นต่อไปของแต่ละแถวที่ไม่กินงบเวอร์ชัน** (ใบ static แยก D-i/D-ii ไม่แตะ wire ⇒ ไม่กินงบ · รันซ้ำ commit เดิมไม่นับเป็นเวอร์ชันใหม่)
- 🔴 **ไม่มีรายการใดถูกลบ ย้าย หรือย่อ** · ใบ GT-035 ยังเป็น **BLOCKED ON CODE LANE** จนกว่า PR ของรอบนี้จะ merge เข้า `main` และ `<SHA>` ผ่านห้าข้อเดิม + ข้อ 6 ใหม่

## ⑥ ลูกมือที่ใช้

`pf-static-re` (ตรวจข้อเท็จจริง 8 ข้อจากจดหมาย) · `general-purpose` (แผนที่เลน 029 ทั้งชุดเพื่อถอดแบบ) · `pf-queue-author` ×2 (บล็อกแก้ใบ GT-045 และ GT-035) · `pf-adversary` (หักล้างเลนใหม่ก่อน commit)

## ⑦ nonclaims ของรอบนี้

- **ไม่มีไคลเอนต์เคยเห็นไบต์ของเลนนี้แม้แต่ไบต์เดียว** — ทั้งรอบอยู่ที่ชั้น composer/dispatcher
- **ไม่ claim ว่าโมเดลนกจะถูกวาดที่ dx100/dy50** — ไม่เคยมีใครยืนยันด้วยตาว่าระยะนี้อยู่ในระยะวาด (nonclaim ③ ของ GT-034 ยังยืน)
- **ไม่ claim ว่า `3857` เป็นกฎของเซิร์ฟเวอร์ต้นฉบับ** — เป็นข้อมูลฝั่ง client (STANDARD_MOB lv27)
- **ไม่ claim ว่าโปรไฟล์ผู้โจมตีสมจริง** — เลือกมาให้หลอดขยับเห็นได้ สูตรเป็นของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับซึ่งกู้ไม่ได้ตลอดกาล
- **ไม่ claim อะไรเกี่ยวกับความตาย ลูท aggro การตอบโต้ หรือ hostile ตัวอื่นใน roster**
- **ไม่ได้รัน gate ตัวเต็ม** — ที่นี่ไม่มี client image · ไม่มี canonical DB · ไม่มี cp874

---

## ⑧ R162-b — `pf-adversary` หักล้างก่อน commit และผมแก้ทับในรอบเดียวกัน

**ไม่อนุมัติ 13 ข้อ** · แก้ครบทุกข้อที่แก้ได้ในรอบนี้ **ก่อน** commit repo โค้ด (ไม่มีอะไรถูก push ไปก่อนหน้านั้น)

**🔴🔴 สองข้อที่ร้ายที่สุด — การ์ดถูกวางกลับหัวทั้งคู่:**
- **D1 — walker อิสระ "ข้าม" ฟิลด์เดียวที่ทั้งเลนมีไว้เพื่อคุม** `_skip_movement_attr` เลื่อน cursor แล้วทิ้งพิกัดทุกไบต์ ⇒ validator **ยอมรับสวีตที่เฟรม spawn วางนกไว้ที่ frozen world row** ได้ (adversary ประกอบให้ดูจริง) · ขนาดเฟรมเท่าเดิม ⇒ size pin ไม่จับ · เซสชันสด `probe_geometry=False` ⇒ sha pin ไม่ทำงาน · ด่านข้อ 6b (grep ไฟล์ scenario) ก็ไม่เห็น เพราะ JSON ไม่เคยมีพิกัดอยู่แล้ว ⇒ **เผารอบ attended ฟรีโดยไม่มีด่านไหนส่งเสียง**
  ⇒ แก้: เขียน `_walk_movement_attr` อ่านพิกัด+heading กลับจริง · validator เพิ่มสามด่าน: พิกัดของ spawn **ต้องไม่ใช่ world row** · identity ใน MovementAttr ต้องตรงกับ entry · และ **พิกัดที่วางตัว ต้องเท่ากับพิกัดที่เลขลอย** (เทียบไบต์)
- **D2 — สาขา actor ไม่เคยเรียก `_require_pinned_position` เลย** การ์ด world row มีแต่บนสามเฟรมที่ *ลอยตัวเลข* ส่วนเฟรมเดียวที่ *วางตัวจริง* ไม่มีการ์ด ⇒ แก้: เรียกการ์ดตัวเดียวกันบนสาขา actor ด้วย
  · ทั้งสองข้อยืนยันด้วยการรีเพลย์ exploit ของ adversary เองหลังแก้: **ปฏิเสธทั้งสองทาง** (`target_placement_is_the_frozen_world_row_not_player_relative`)

**ข้ออื่นที่แก้แล้ว:**
- **D3 ของที่ใบสั่งแล้วไม่ได้ส่ง** ⇒ เขียน **`tools/pf_hostile_hp_link_headless_replay.py`** จริง (ขับ refusal 8 ตัวแล้วพิมพ์ชื่อ · decode พิกัดที่เฟรม spawn วางไว้ · socket trap · ไม่รับ `--db`) ⇒ **นี่คือคำตอบของคำถามปิดท้ายที่ adversary ถาม**: ถ้ารอบ attended กลับมาว่า "ไม่เห็นตัวนก" เรามีเลขพิกัดที่เฟรมส่งจริงอยู่ในมือ **แยก "นอกระยะวาด" ออกจาก "วางผิดที่" ได้** · (ยังไม่มี `tools/verify_*` แยก — ด่าน encoder อยู่ในสวีตแทน)
- **D4 refusal สองเส้นทางไม่เคยถูกรัน** (`{classification}_no_reply` · `wrong_scene`) ⇒ เพิ่มเทสสองตัวที่ยิงเข้าไปจริง (ไบต์ high byte = คีย์บอร์ดไทย · checkpoint ตัวละครไป scene อื่น)
- **D6 ไม่มีการ์ด "เลือกตัวละครผิด" ทั้งที่ใบสัญญาไว้กับผู้เทส** ⇒ เพิ่ม `hostile_hp_link_hypothesis_identity_not_pinned_no_reply` พินที่ canonical smoke `0x10010001:0` ท่าเดียวกับ HYP-PF-037 + เทส
- **D7 ค่าคงที่ครึ่งตายถูกก๊อปมาตายในเลนที่ประกาศว่าไม่มีครึ่งตาย** (11 ตัว) ⇒ **ลบทิ้งทั้งชุด** พร้อมคอมเมนต์ว่าทำไม (โน้ตของโมดูลเองห้ามเก็บของตายไว้อยู่แล้ว)
- **D10 nonclaim `one_shot_per_process` เท็จ** (counter อยู่บน connection · เทสของเราเองหักล้าง) ⇒ แก้เป็น `one_shot_per_connection_not_per_process` และแก้เทสให้ใช้ login เดิม
- **D12 exception หลุดเข้าเส้นที่ `try:` ไม่มี `except:`** ⇒ ห่อ resolve/build ด้วย except แล้วปล่อย `..._refused_no_reply` แทนการฆ่า thread ของ connection
- **D5 คำโฆษณา pin เกินจริง** ("live = sizes only") — ตัวละครที่นั่งจุดเกิดทำให้ 4 เฟรม actor โดน sha pin จริง ⇒ แก้ข้อความในไฟล์ scenario ให้ตรง
- **D9 diff ledger บวมเป็น 7,075 บรรทัดเพราะ reindent ทั้งไฟล์** ⇒ dump ใหม่ด้วย indent เดิม ⇒ เหลือ **+107/-1**
- **D11 `FUNCTIONAL_COVERAGE.json` แถว damage เขียนว่า "blocked ... ไม่มีโค้ด"** ทั้งที่มีสี่เลนแล้ว ⇒ เขียน notes ใหม่ให้แยก "หลักฐานยังไม่มี" ออกจาก "โค้ดไม่มี" (แถวยัง blocked เหมือนเดิม)
- **D8 คำสั่งบูตในใบ GT-035 บูตไม่ขึ้นจริง** (`ModuleNotFoundError` เพราะไม่มี `PYTHONPATH`) ⇒ แก้ใบ + แก้บรรทัด `--db` ที่ล้าสมัย + ใส่เครื่องหมายคำพูดรอบ path ที่มีช่องว่าง (`Pirate Force`)
- **D13 ladder เบี่ยงจากที่ใบเสนอ (75/20 ไม่ใช่ 60/20) โดยไม่มีใครพูดถึง** ⇒ เขียนไว้ทั้งใน docstring ของโมดูล ในใบ และในจดหมาย

**ข้อที่ adversary ยกมาแล้วผมเลือก "ยอมรับและประกาศ" แทนการแก้:**
- **ตัวคุม MISS แยกไม่ออกในชั้น client-observable** — สองเฟรมรอบ MISS เป็นไบต์เดียวกันโดยตั้งใจ ⇒ "ไคลเอนต์รับแล้ววาดซ้ำ" กับ "เฟรมไม่ถึง" ให้ภาพเหมือนกัน · ตัวแยกอยู่ที่ชั้น (1) เท่านั้น (นับบรรทัด `[G>]` ให้ครบ 7)
  ⇒ เขียนลงใบเป็นข้อ ③ ของบล็อก R162-b พร้อมสั่งห้ามสรุปเรื่องนี้จากภาพ · สิ่งที่ตัวคุมยังซื้อได้จริงคือแยก "ขยับ 6 วิหลังเฟรมเลข" ออกจาก "ขยับที่เฟรมเลข" ซึ่งคือคำถาม (ง)
- **`wrong_scene` เป็น dead code ในโปรดักชันวันนี้** (ทุกอย่าง scene 1) ⇒ เก็บไว้เป็นการ์ดเชิงป้องกัน + มีเทสยิงถึงแล้ว

**ผลรันหลังแก้ทั้งหมด:** สวีตเต็ม **2345 passed / 324 skipped / 4485 subtests** เขียว(cloud sanity) · `verify_hypothesis_ledger` PASS 46 · `verify_functional_coverage` PASS · census skip PASS · seam suite 22 passed · `git diff --check` เงียบ · v141 ไม่ถูกแตะ
