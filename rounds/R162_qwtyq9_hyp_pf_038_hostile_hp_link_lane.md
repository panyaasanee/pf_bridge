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

**ไฟล์ใหม่ 3 · แก้ 4** — `src/pirateforce_foundation/hostile_hp_link_hypothesis.py` · `scenarios/hostile_hp_link_hypothesis_p30_sweep.json` · `tests/test_hostile_hp_link_hypothesis.py` · แก้ `app.py` `runtime.py` `docs/HYPOTHESIS_LEDGER.json` `tools/verify_hypothesis_ledger.py`

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

**สิ่งที่ **ไม่** ได้ทำ (ตั้งใจ):** ไม่มี `tools/verify_*` และไม่มี `tools/pf_*_headless_replay.py` — เลนที่ merge ล่าสุดสองเลน (036 · 037) เลิกทำสองตัวนี้แล้ว และ `evidence_refs` ของมันเหลือสองรายการ ⇒ ถอดแบบของใหม่
🔴 **ราคาที่จ่าย ต้องเขียนไว้ตรง ๆ:** ใบ GT-035 ชั้น (1) เขียนว่า *"named refusal พิสูจน์ได้ที่เดียว = ฝั่ง headless ⇒ รอบ build ต้องส่งมอบสองตัวนี้มาด้วย"* — **รอบนี้ไม่ได้ส่ง** · แทนที่ด้วยเทสในสวีต (`RefusalTests` · `DispatchTests`) ซึ่งเรียก refusal ทุกตัวจริงและตรวจว่าไม่มีไบต์ออก **แต่ผู้เทสหน้าจอยังมองไม่เห็น named refusal อยู่ดี** (คอนโซลเงียบเหมือนเดิม) ⇒ ถ้า Panya อยากได้เครื่องมือ headless แยก ให้สั่งเป็นรอบต่างหาก

**ledger:** append `HYP-PF-038` ท้ายสุด (entry ที่ 46 · ไม่ขยับ index เก่า) · **1 of 3 versions** · `production_allowed: false` · `extension_approval_ref: null`
· `tools/verify_hypothesis_ledger.py` เพิ่ม `EXPECTED_IDS` + `EXPECTED_META` + บล็อก lineage + **re-pin canonical sha** เป็น `40644A18…`

## ④ ผลรัน (ที่นี่ = cloud sanity เท่านั้น ห้ามอ่านเป็น gate)

```
python3 -m pytest tests -q      2338 passed · 324 skipped · 4484 subtests   เขียว(cloud sanity)
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
