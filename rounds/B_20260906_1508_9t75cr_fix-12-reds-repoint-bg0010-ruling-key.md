# LANE-B round 9t75cr -- 2026-09-06T15:08+07:00 start

## รอบนี้ขยับ NOW/M ข้อไหน
**M4 "ตีได้ตายได้"** สำหรับฉาก 10 (Deep Sea Temple ชั้น 1): เมื่อรอบก่อน
(`30ja9z`) ลงทะเบียนมอนไว้แล้วแต่ยังฆ่าไม่ได้ตามกฎหมายจริง (คีย์ PENDING),
รอบนี้เปลี่ยนเป็นคีย์ที่ COO เซ็นจริง (`COO-DECISION widen-death-scope-
bg0010-six-templates 2026-09-06T14:53+07:00`) — สิทธิ์ฆ่าจึงเป็นของจริงตั้งแต่
รอบนี้ แม้ P-2 ยังปิดใบเทสตีมอนก็ตาม (คนละเรื่องกับกฎหมาย). NOW บรรทัด
"M4 LANE-B" ไม่ได้ระบุฉาก 10 ตรง ๆ แต่ `1453` (คำตอบต่อใบขอของรอบก่อน)
สั่งตรง ๆ ให้ทำเรื่องนี้เป็นงานแรกของรอบถัดไป.

## ล็อกรอบ
list PR `[LANE-B] round <id>: claim` ใน `pf_bridge` ก่อนแตะอะไร: มีเปิดอยู่
ใบเดียว (`pf_bridge#1493`) แต่หัวเรื่องคือ "round 30ja9z addendum: post-
unlock findings" ไม่ใช่ "claim" — ไม่ตรงรูปแบบล็อกที่กฎกำหนด (ล็อกต้องเป็น
`[LANE-B] round <id>: claim` เท่านั้น) ⇒ ล็อกว่างจริง เปิด claim `pf_bridge#1507`
(กิ่ง `claude/practical-knuth-9t75cr`) แล้ว list ซ้ำทันที: ไม่มี `[LANE-B]
round <id>: claim` ใบอื่นที่เก่ากว่ายังมีชีวิต ⇒ ล็อกติด

## กล่องจดหมาย
grep `ADDRESSEE:.*LANE-B` (แยกจาก `cc:` ให้ถูก ครั้งแรกที่ grep หยาบจับ `cc:`
ปนมาด้วยเพราะทั้งสองอยู่บรรทัดเดียวกัน) แล้วคัดใบที่ยังไม่มี `<ชื่อไฟล์>.CONSUMED.txt`
คู่ (สังเกตว่า stub คือ `<ชื่อ>.md.CONSUMED.txt` ไม่ใช่ `<ชื่อไม่มี.md>.CONSUMED.txt`
— ถ้า grep ผิดรูปจะเห็นจดหมายเก่าเป็นร้อยใบราวกับยังไม่ถูกบริโภค ทั้งที่บริโภคแล้ว)
พบใบเดียวที่ใหม่จริงและยังไม่บริโภค:
`20260906_1453_COO-DECISION-b1411-widen-death-scope-bg0010-six-templates-
ratified-placement-50-stays-out-until-static-0903-answered-LANE-B.md`
(ตอบใบขอของรอบก่อนเอง `20260906_1411_...`) — บริโภคทั้งคู่รอบนี้ (ดูหัวข้อถัดไป)

จดหมาย broadcast ห้ารายการ (`PANYA-DECISION`/`PANYA-CLARIFICATION` เรื่อง
shared world และบันไดไมล์สโตน) ที่ `cc:` ถึง LANE-B แต่ยังไม่มี stub ส่วนตัว
ของสาย B — ทั้งหมดสะท้อนอยู่ใน `NOW.md`/`AGENTS.md` แล้ว (shared world,
บันไดไมล์สโตน) ไม่ใช่ของใหม่ที่รอบนี้ต้องตอบสนอง จึงไม่ได้ทำ stub ให้ (หนี้เดิม
ก่อนรอบนี้เริ่ม ไม่ใช่สิ่งที่รอบนี้สร้างขึ้น) — ทิ้งให้ COO/chief ตัดสินว่าต้องมี stub
ต่อจดหมาย broadcast แต่ละสายหรือไม่ ไม่ใช่การตัดสินใจของรอบนี้

## รอบนี้ทำอะไร (ของจริง ไม่ใช่ probe)

### 1. แก้ 12 เทสแดงที่ pf-adversary เจอหลังปลดล็อกรอบ `30ja9z`
ต่อกิ่ง `claude/nice-meitner-30ja9z` (`pirate-force-server#922`) มาเป็น
`claude/practical-knuth-9t75cr` (ตาม head `ce7bf293` ที่ pf-adversary วัด
"12 failed, 12202 passed" ไว้) — ไม่ใช่กิ่งใหม่จาก main เพราะรอบนี้ต่อยอด
โค้ดของ PR ที่ยังไม่ merge ตามกฎล็อกรอบข้อ 1

ทั้ง 12 ใบเป็นแบบเดียวกันหมด: **ตัวอย่างเทสที่อ้างว่าฉาก 10 "ยังไม่ถูก mine"
ถูกทำให้เป็นเท็จโดยคอมมิตเดียวกับที่เขียนตัวอย่างนั้น** (รอบ `30ja9z` เอง mine
+ ลงทะเบียนฉาก 10 สำเร็จ 17/17 แถว ในคอมมิตเดียวกับที่ไฟล์เทสพี่น้องยังเขียนว่า
"ฉาก 10 ยังไม่ถูก mine") — เป็นรูปแบบเดิมที่โปรเจกต์เจอมาแล้วสองครั้ง (ฉาก 9
แล้วฉาก 6) แต่ครั้งนี้เกิดขึ้น**ภายในรอบเดียวกับที่เขียนตัวอย่าง** ไม่ใช่รอบถัดมา

แก้ทีละไฟล์:
- `tests/test_world_population_bg0010.py`, `tests/test_world_bg0010_identity.py`
  (LANE-A's tests, cross-lane edit พร้อมคอมเมนต์กำกับ): เปลี่ยน tripwire
  "ยังไม่มีใครนำเข้าโมดูลนี้" / "ยังไม่มีโมดูล roster ของ LANE-B" ให้กลับทิศ
  เหมือนที่ฉาก 11 เคยทำ (`4tnhzw`)
- `tests/test_field_mob_tables_bg0004.py`: digest ตาราง AI (`AI_TABLES_SHA256`)
  ค้างจากรอบก่อน (regenerate ตารางแล้วไม่ recompute digest) — recompute แล้ว
  ตรวจ diff เป็น additions-only จริง (`git diff 154f0f19 ce7bf293`) พบแถวซ้ำ
  หนึ่งแถวใน `PLACEMENT_AI_LINKS` (`(47, 16, 301)`, Bg0007 placement 47 กับ
  Bg0010 placement 47 ใช้ AI id เดียวกัน) — pf-adversary วัดไว้แล้วว่า runtime
  ปลอดภัย (lookup ใช้ AI id ของแถว roster เอง ไม่ใช่ placement index ของตาราง
  นี้) บันทึกเป็นหนี้ที่ยังไม่แก้ (ต้องเพิ่มคอลัมน์ฉากถึงจะ dedup ได้ปลอดภัย
  นอกเขตรอบนี้)
- `tests/test_field_mob_tables_bg0005.py`: ตัวนับฉาก lane-composed เก้า -> สิบ
- `tests/test_lane_a_scene_census.py`: สองเทสใช้ฉาก 10 เป็นตัวอย่าง "ฉากที่
  ยังไม่ mine" — ย้ายไปฉาก 130 (Navy Training Camp, เพิ่มค่าคงที่
  `NAVY_TRAINING_CAMP` ใหม่) เปิดที่ login แล้วยังไม่เคยถูก LANE-B mine เลย
- `tests/test_mob_death_persistence.py`: ตัวอย่างเดียวกัน ย้ายไปฉาก 304
  (Dark Fog Sea / Bg3007) ที่ไฟล์อื่นในรอบนี้ก็เลือกเป็นตัวอย่างเดียวกัน
- `tests/test_gm_identity_registry_census.py`: ตัวนับฉาก 11 -> 12
- `tests/test_field_mobs.py`, `tests/test_mob_combat_bg0015_gates.py`: การ์ด
  collision ข้ามฉากเพิ่ม 14 คู่ใหม่ (วัดจาก `cross_scene_identity_collisions()`
  จริง ไม่ได้ประกอบมือ) — สองคู่เดิม (`0x2020`, `0x202F`) กลายเป็นสามทาง
- `docs/PYTEST_SKIP_PINS.json`: pin ใบ skip ของ `test_field_mob_tables_bg0010.py`
  (รอบก่อนส่งไม่ pin — หนึ่งใน 12 ใบแดง)

### 2. repoint คีย์ ruling ตาม COO-DECISION `1453`
`src/pirateforce_foundation/mob_death.py` (`WIDENING_RULINGS` +
`WIDENING_RULING_SCENES`), `field_mobs.py`'s comment,
`tests/test_field_mob_tables_bg0010.py` (`RULING_NAME` + เทสที่ pin ว่าคีย์
ต้องไม่ขึ้นต้น `COO-DECISION` — รอบนี้กลับทิศเทสนั้น เพราะตอนนี้คีย์ต้องขึ้นต้น
`COO-DECISION` แล้ว) และ `tests/test_mob_death_wired_widening.py` (pin เวลา
ลงทะเบียน) จาก
`"LANE-B-REQUEST-PENDING-COO widen-death-scope-bg0010-six-templates
2026-09-06T14:11+07:00"` เป็น
`"COO-DECISION widen-death-scope-bg0010-six-templates 2026-09-06T14:53+07:00"`
— ชุด template ที่ครอบคลุมไม่เปลี่ยน (`{660, 661, 662, 668, 671, 673}`) ยืนยัน
ด้วย diff review ว่าไม่มี literal frozenset เปลี่ยนเลย. Placement 50 ไม่อยู่ใน
ใบนี้เหมือนเดิม (ใบ STATIC `0903`+`1046` ยังไม่มีเลขไม่มีคำตอบ).

## ใบที่บริโภครอบนี้
1. `20260906_1453_COO-DECISION-...` — ใช้แล้ว (หัวข้อ 2 ข้างบน) วาง
   `.CONSUMED.txt` + สำเนาไป `consumed/`
2. `20260906_1411_LANE-B-ASK-COO-...` (ใบขอของตัวเองที่รอบก่อนส่ง) —
   ถูกตอบแล้วโดยใบข้างบน วาง `.CONSUMED.txt` เช่นกัน (ชี้ไปใบตอบ)

## เปิดใบให้สาย C / COO
`notes_to_chief/20260906_1525_LANE-B-ASK-COO-your-own-grep-misses-7-of-14-
live-ruling-keys-three-are-real-grants.md` — D5 จาก addendum `1493`: grep
ตรง ๆ ของ COO (`"COO-DECISION widen-death-scope"` เป็น substring ต่อเนื่อง)
reconciles ได้แค่ 7 จาก 14 คีย์ที่ใช้งานอยู่วันนี้ (ก่อนรอบนี้คือ 6/14 ตรงกับ
ตัวเลขที่ pf-adversary รายงานไว้เป๊ะ) — วัดสดด้วย `re.search` กับทุกคีย์ใน
`mob_death.WIDENING_RULINGS` ก่อนส่งใบ ไม่ใช่ยกตัวเลขเดิมมาลอย ๆ. สามใน
เจ็ดที่พลาดเป็น**ใบอนุญาตจริง** (bg0003/bg0004/bg0005) เพราะสะกดวันที่ไว้
**คั่นกลาง** ระหว่าง `COO-DECISION` กับ `widen-death-scope` แทนที่จะอยู่ท้ายคีย์
แบบ 6 คีย์ล่าสุด — เสนอสามทางเลือกให้ COO เคาะ (grep ยืดหยุ่นขึ้น /
บังคับ schema เดียวสำหรับคีย์ใหม่ / ทั้งสอง) ไม่ได้ตัดสินแทน

## ที่ไม่ได้แตะ (นอกขอบเขตรอบนี้)
- `PLACEMENT_AI_LINKS` แถวซ้ำ `(47, 16, 301)` — บันทึกเป็นหนี้ ไม่แก้ (ดูข้างบน)
- `mob_death_persistence` ยังไม่ต่อสาย `runtime.py` — สอง session เข้าฉาก 10
  พร้อมกันยังเห็นมอนเดิม HP เต็มถ้าตัวหนึ่งฆ่าไปแล้ว (หนี้เดิมจากรอบ `30ja9z`
  ไม่ใช่ของใหม่รอบนี้)
- placement 50 ของ Bg0010 — ยังรอใบ STATIC `0903`/`1046`
- ใบเทสตีมอนทุกใบ — P-2 ยังปิดอยู่ ใบนี้เป็นโค้ด ไม่ใช่ GT ตาม `1453` ข้อ 4
- เขตสาย A: อ่าน `world_population_bg0010.py`/`world_scene_registry.py`
  อย่างเดียว ไม่แก้ · ไม่แตะ `world_*.json` · ไม่แตะ `runtime.py`/`app.py`/v141

## pf-adversary
เซสชันนี้ค้นแล้วไม่มี Agent/pf-adversary ให้เรียกจริง ⇒
**ADVERSARY_UNAVAILABLE claude/practical-knuth-9t75cr** ตาม token มาตรฐาน
self-review แทน: อ่านทุก hunk ใน `git diff --cached` ก่อน commit (ตรวจ
`mob_death.py` และ `field_mobs.py` ทีละบรรทัดเพราะเป็นจุดกฎหมายฆ่ามอน) ·
stage ทีละไฟล์ ไม่ใช้ `git add -A` · ตรวจ cp874-encodability ของทุกไฟล์ที่แตะ
ด้วยสคริปต์แยก (ผ่านหมด) · รันไฟล์เทสที่แตะทุกไฟล์ระหว่างทาง แล้วรันชุดเต็ม
สองครั้ง (ก่อน merge main และหลัง merge main เป็นคอมมิตสุดท้ายจริง)
**รอบ LANE-B ถัดไปสั่ง adversary บนกิ่งนี้เป็นงานแรก** ตามกฎ

## verification
- ก่อน merge main: `pytest tests -q` → **12218 passed, 365 skipped, 0 failed,
  26025 subtests, 475.46s** (เขียวเต็มจริง ต่างจากรอบ `30ja9z` ที่ปลดล็อกโดย
  ไม่รอผลชุดเต็ม)
- `python3 tools/pf_pytest_precondition_census.py --run` → **RESULT: PASS**
  (365 skip ทุกตัวมีชื่อ+เหตุผล+เลขที่ตรงกับที่ pin ไว้ ไม่มี skip ใหม่ที่ไม่ได้ pin)
- `git merge origin/main` เข้ากิ่ง → clean, no conflicts (22 ไฟล์จาก main
  ระหว่างรอบ ไม่ทับไฟล์ที่รอบนี้แตะเลย)
- หลัง merge main: ไฟล์เทสที่แตะทั้งหมด → 414 passed, 3736 subtests passed
  (5.83s) · ชุดเต็มหลัง merge (คอมมิตสุดท้ายจริงบนต้นไม้ที่ push) →
  **12366 passed, 365 skipped, 0 failed, 26121 subtests, 478.31s** — เขียว
  เต็มจริงทั้งสองครั้ง (ก่อน/หลัง merge main)
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` → **PREFLIGHT PASS**
  (cp874 + ไม่มี skip ใหม่ + main อยู่ในกิ่ง + precondition census ตรง + สองกิ่ง
  reaper merge ได้ + ไฟล์สะพานไม่โต + ไม่แตะแถว scoreboard มือ)
- `--pr-body pr_body_server.md --pr-stage final` → **PASS** มี marker บรรทัดเดียว
  (บรรทัด 90) ก่อนโพสต์จริงไป `pirate-force-server#930`

TWO_SESSIONS_SAME_SCENE: ไม่เปลี่ยนจากที่รอบ `30ja9z` บันทึกไว้ — roster เป็น
ตารางค่าคงที่ระดับโมดูล อ่านอย่างเดียว ไม่มี state ต่อ session, composer เป็น
ฟังก์ชันบริสุทธิ์ของ (scene, roster, ledger) รอบนี้ไม่เพิ่ม state ต่อ session ใหม่
เลย (แก้แค่เทส + คีย์สตริง)

## PR/status
- `pf_bridge` claim `pf_bridge#1507` (`claude/practical-knuth-9t75cr`)
- `pirate-force-server#930` (`claude/practical-knuth-9t75cr`) — **เปิดแล้ว ไม่ draft
  มี `PF-AUTOMERGE: v4`** (GET ยืนยันแล้ว)
- จดหมาย `notes_to_chief/20260906_1525_LANE-B-ASK-COO-your-own-grep-misses-
  7-of-14-live-ruling-keys-three-are-real-grants.md`

## รอบหน้าทำอะไร
1. **สั่ง pf-adversary บนกิ่งนี้เป็นงานแรก** (ADVERSARY_UNAVAILABLE ของรอบนี้)
2. บริโภคคำตอบใบ D5 (`1525`) ถ้า COO ตอบมา — grep pattern เก่ายังใช้ต่อได้
   จนกว่าจะมีคำสั่งเปลี่ยน
3. หนี้ `PLACEMENT_AI_LINKS` แถวซ้ำ — ตัดสินว่าจะเพิ่มคอลัมน์ฉากหรือปล่อยไว้
4. `mob_death_persistence` ต่อสาย `runtime.py` (CORE-REQUEST รอบก่อนหน้ายังไม่
   ได้ส่ง — ถ้าจะทำ ต้องเขียน CORE-REQUEST ให้ chief เพราะ runtime.py เป็น
   ของ chief)
5. ยังติดเหมือนเดิม (P-2) ⇒ ปลดแฟล็กจาก `docs/PROMOTION_BACKLOG.md` — รอบ
   `30ja9z` ตรวจ `ground_loot_hypothesis.py` แล้วว่ายังโปรโมตไม่ได้ (ผลบนจอ
   ยังเป็นแค่ฝุ่น ไม่มีโมเดล/ป้ายชื่อ) แถว B ที่เหลือรอ P-2 ทั้งหมด

SCOREBOARD: COMING | ฉาก 10 (Deep Sea Temple ชั้น 1) มีมอนสเตอร์ 17 ตัวที่ตอนนี้ตายได้ภายใต้ใบอนุญาตจริงของ COO (ไม่ใช่คีย์รออนุมัติแบบรอบก่อน) แต่ผู้เล่นยังไม่เห็นบนจอ (P-2 ยังปิดใบเทสตีมอน) | `pirate-force-server#930` · `notes_to_chief/20260906_1453_COO-DECISION-...LANE-B.md` · full suite (post-merge, final commit) 12366 passed / 0 failed / 26121 subtests
