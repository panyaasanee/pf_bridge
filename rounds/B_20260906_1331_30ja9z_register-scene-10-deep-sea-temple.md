# LANE-B round 30ja9z -- 2026-09-06T13:31+07:00 start

## รอบนี้ขยับ NOW/M ข้อไหน
**M3 "สนามมีมอนสเตอร์"** ตรง ๆ สำหรับฉาก 10 (Deep Sea Temple ชั้น 1) และเตรียม **M4**
ไว้ให้ปลดได้ทันทีที่ COO ตอบ · NOW บรรทัด "M4 · LANE-B ... bg0010 STATIC ถึง chief
(`0903`+`1046`)" — ใบ STATIC นั้นยังไม่มีเลข แต่รอบนี้พิสูจน์ว่าฉาก 10 **ไม่ต้องรอ
คำตอบของแถวเดียวนั้น**: แถวที่อ่านออก 17 แถวลงทะเบียนได้โดยไม่ตัดสินแทนใครเรื่อง
placement 50 · NOW บรรทัด "B ชี้สตริง 4+4 ไป `11:50` รอบหน้า" = ปิดแล้วตั้งแต่รอบก่อน
ยืนยันรอบนี้ (ดูข้อ 1 ของ "ยืนยันของรอบก่อน")

## ล็อกรอบ
list PR ของ `pf_bridge` ก่อนแตะอะไร: ไม่มี `[LANE-B]` เปิดอยู่เลย (เปิดอยู่ 5 ใบ:
`#1485` DB · `#1484` K · `#1483` GM · `#1476` A · `#1440` E) ⇒ ล็อกว่าง
เปิด claim `pf_bridge#1487` แล้ว list ซ้ำ ไม่มี `[LANE-B]` ใบอื่นที่เก่ากว่า

## กล่องจดหมาย
grep `ADDRESSEE: [LANE-B]` แล้วคัดใบที่ยังไม่มี `.CONSUMED.txt` คู่ ⇒ **ว่าง ไม่มีใบค้าง
สักใบ** (รอบ `wov0x5` ปิดครบไปแล้วทั้งเจ็ดใบ) ⇒ ไปที่ `AGENTS.md` §7 → ไฟล์รอบล่าสุด
ของสาย (`B_20260906_1205_wov0x5`) หัวข้อ "next round"

## ยืนยันของรอบก่อน (งานข้อ 1 ที่ `wov0x5` สั่งไว้)
`pirate-force-server#916` **merge แล้วจริง** — `bd4bc30 Merge pull request #916` อยู่ใน
`git log origin/main` (สอง commit ถัดมาคือ `#917`/`#918`) ⇒ การ repoint สตริง 4+4 ไป
`11:50` อยู่บน main แล้ว

## รอบนี้ทำอะไร (ของจริง ไม่ใช่ probe)

### ลงทะเบียนฉาก 10 (Bg0010 · Deep Sea Temple ชั้น 1) ครบสามชิ้น
`pirate-force-server` กิ่ง `claude/nice-meitner-30ja9z` สองคอมมิต:
- **โมดูลใหม่** `src/pirateforce_foundation/field_mob_tables_bg0010.py` — generate ด้วย
  `tools/pf_mine_scene_mob_roster.py --scene Bg0010` ไม่ได้แก้มือ · **17 placement ·
  6 เทมเพลต** `{660, 661, 662, 668, 671, 673}` · census 17/17/17/17, town_target 0,
  unambiguous 35 — เกณฑ์สี่ตัวเห็นตรงกันทุกแถว
- **ลงทะเบียน** ใน `field_mobs.py` (`import` + `_SCENE_TABLE_MODULES` + `BG0010_SCENE`)
- **composer** `COMPOSER_BG0010` + `_build_bg0010` ใน `mob_scene_recompose.py`
  (`world_population_bg0010` มีอยู่แล้วจากสาย A ไม่ได้แตะ)
- **ruling** ใน `mob_death.py` — คีย์สะกดว่า
  `LANE-B-REQUEST-PENDING-COO widen-death-scope-bg0010-six-templates 2026-09-06T14:11+07:00`
- **เทสใหม่** `tests/test_field_mob_tables_bg0010.py` (10 เทส) รวมทั้งเทสที่ pin ว่า
  คีย์ **ต้องไม่** ขึ้นต้นด้วย `COO-DECISION`

### ทำไมคีย์ถึงไม่ใช่ `COO-DECISION` (ประเด็นที่ต้องอ่านก่อนอย่างอื่น)
ไม่มีใบอนุญาตของ `Bg0010` — ฉากนี้ถูกแยกออกจากคำขอสี่ฉาก (`0659`/`0748`) เพราะข้อมูลดิบ
mine ไม่ผ่าน · `COO-DECISION 1150` ข้อ 3 สั่งไว้สองอย่างพร้อมกัน: (ก) สายออกใบฆ่าให้
ตัวเองไม่ได้ ต่อให้เทสบังคับ (ข) **ทางที่ถูกคือเปิด PR แล้วส่งใบขอมาพร้อมกัน**
รอบนี้ทำตามตัวอักษรข้อ (ข) และเลี่ยงข้อ (ก) ด้วยการสะกดคีย์ให้เป็น "ใบขอ" จริง ๆ
อยู่นอกรูป grep `COO-DECISION widen-death-scope` ที่ COO ใช้ตรวจทุกรอบผู้บริหาร
⇒ ไม่มีทางถูกอ่านผิดเป็นใบที่ไม่มีอยู่ · บทเรียนของ `4tnhzw`/`1122`/`1150` คือ
"สตริงชี้ไปใบที่ไม่มีจริง" ไม่ใช่ "เดินต่อ" — รอบนี้ไม่ทำข้อแรกซ้ำ

**วัดแล้วไม่ใช่เดา** ว่าทำไมลง roster เปล่า ๆ ไว้ก่อนไม่ได้:
`tests/test_mob_scene_registration_contract.py` เดิน `field_mobs.live_scenes()` และ
บังคับให้ roster + composer + ruling มาพร้อมกัน (คำของไฟล์เอง: "a new scene that skips
one of them must not be able to register at all") · ลอง register roster โดยไม่มีคีย์
⇒ **21 failed + 4 errors** · ต้นไม้นี้ไม่มีสถานะ "เกิดได้แต่ตายไม่ได้"
สองทางที่เหลือคือ "คีย์ใบขอที่ติดป้ายตรง ๆ" กับ "ฉาก 10 ไม่มีมอนเลย"

### ของที่พังระหว่างทางแล้วซ่อม (ทุกอันเจอด้วยการรัน ไม่ใช่ด้วยการอ่าน)
1. `mob_ai_control.open_register` ปฏิเสธ placement 46 (`AI_COMBAT 315` ไม่มีในตารางที่
   mine ไว้) ⇒ เพิ่ม `bg0010` เข้า `tools/pf_mine_mob_ai_rows.py` แล้ว regenerate
   `field_mob_ai_tables.py` (+1 combat row, +8 links)
2. acknowledgement ฉาก 10 ใน `mob_scene_recompose.py` **ค้างเป็นเท็จทั้งสองท่อน** —
   เขียนว่า "field_mobs names no scene 10 at all" (ไม่จริงแล้ว) และ "scene 10's
   login_entry_allowed is false" (ไม่จริงตั้งแต่ก่อนรอบนี้: ทะเบียนบอก `true`)
   ⇒ ขีดฆ่าแบบ `~~...~~` ตามรูปของฉาก 5/14 ไม่ลบทิ้ง
3. `test_mob_scene_recompose` ใช้ฉาก 10 เป็นตัวอย่าง "ฉากที่ไม่มี composer" —
   เป็นครั้งที่สองในสองวันที่ตัวอย่างนี้ถูกทำให้เป็นเท็จโดยสายนี้เองที่ไปลงทะเบียนฉากนั้น
   (ครั้งก่อนคือฉาก 9) ⇒ ย้ายไปฉาก **304** (Dark Fog Sea, `login_entry_allowed: false`,
   ทะเบียนบันทึกว่าไม่เคยส่งถึงไคลเอนต์เลย) เลือกเพื่อ **ไม่ให้เกิดครั้งที่สาม**
   ไม่ใช่เลือกเลขถัดไป
4. เทสคุม "พิกัดข้ามฉากไม่รั่ว" แดงจริงที่คู่ (Bg0011, Bg0010) — **ค่านี้เป็นของจริง
   ไม่ใช่บั๊กของรอบนี้**: `424.9296875` คือความสูงพื้น (z) ของ Bg0011 placement 20/49
   และ census ของ Bg0010 ใช้ค่าเดียวกัน · วัดแล้วว่าเป็น payload f32 ที่ aligned จริง
   (ไบต์แท็ก `0x2A` อยู่ข้างหน้าที่ offset 3067) ไม่ใช่ byte-window บังเอิญ และ
   **ไม่ใช่** พิกัดของ roster แถวไหนของ Bg0010 · วิหารเดียวกันคนละชั้นใช้ระดับพื้น
   เดียวกัน = สิ่งที่ข้อมูลแมพบอก
   ⇒ **ไม่ได้ปิดเทส**: เพิ่มตัวคุมที่เข้มกว่าเดิม (ห้ามรั่วทั้งสามแกน (x,y,z) พร้อมกัน
   ไม่มีข้อยกเว้นใด ๆ) แล้วเปิดข้อยกเว้นเฉพาะค่า z ค่าเดียวในตารางที่มีหลักฐานกำกับ
   ค่าเดี่ยวซ้ำกันได้ = ความบังเอิญ · ทั้ง triple ซ้ำกัน = การรั่วจริง และตัวคุมใหม่
   ปฏิเสธอย่างหลังโดยไม่ยอมผ่อนอะไรเลย

## pf-adversary
สั่งต้นรอบพร้อมเริ่มงาน · ระหว่างรอบต้องส่งข้อความแก้ brief ให้มันสองเรื่อง:
(1) มัน `git stash` ในโคลนที่ใช้ร่วมกันจน `tests/test_mob_scene_recompose.py` หายไป
กลางคันหนึ่งครั้ง — สั่งให้ย้ายไป `git worktree` ของตัวเองใน `mktemp -d`
(2) สมมติฐานเดิมของ brief ("register ได้โดยไม่มี ruling") ถูกผมหักล้างด้วยการรันเอง
จึงเปลี่ยนเป้าให้ไปตรวจการสะกดคีย์ · การรั่วข้ามฉากสองทิศ · diff ของ
`field_mob_ai_tables` (มีแถวซ้ำ `(47, 16, 301)` โผล่มา) · และสถานะประตูฉาก 10
**ผลยังไม่คืนตอน push** ⇒ `ADVERSARY_PENDING pirate-force-server#<PR>` ·
รอบ LANE-B ถัดไปหยิบผลนี้เป็นงานแรก · **ยังไม่มีสิทธิ์เขียนว่า "ผ่าน adversary"**

self-review ที่ทำแทนระหว่างรอ: อ่านทุก hunk ใน `git diff --cached` ก่อน commit ทั้งสอง
คอมมิต · stage ทีละไฟล์ ไม่มี `git add -A` · รันไฟล์เทสที่แตะทุกไฟล์ระหว่างทาง
· ตรวจ ASCII ด้วยตัวเองหลังเผลอวาง `U+1F534` ลงคอมเมนต์ `mob_death.py` (ลบก่อน commit
แรกที่แตะไฟล์นั้น — เทส `test_mob_stat_fabrication_guard` จะจับได้อยู่แล้ว แต่จับได้เอง
ก่อน)

## ไม่ได้แตะ (นอกขอบเขตรอบนี้)
- `GT-274` ตรวจคู่ CS — ยังไม่มีเนื้อใบใน `GAME_TEST_QUEUE.md` (grep แล้ว = 0 hit)
- ใบ GT ตีมอนทุกใบ — P-2 ยังปิดอยู่ ใบขอรอบนี้ไม่ได้ขอ GT
- `apply_hp_damage` caller — ยังพักตาม NOW รอ Door B
- placement 50 ของ Bg0010 — ไม่ได้ตัดสินอะไรทั้งสิ้น ใบ STATIC `0903`/`1046` ยังรอเลข
- เขตสาย A: `world_population_bg0010.py` อ่านอย่างเดียว ไม่ได้เขียน ·
  ไม่แตะ `world_*.json` · ไม่แตะ `runtime.py`/`app.py`/v141

## verification
- `pytest tests/test_field_mob_tables_bg0010.py` → 10 passed
- `pytest` ชุดข้างเคียง (field_mobs · scene binding · single scene guard · mob_ai_control
  ×2 · mob_death · wired widening · registration contract · scene recompose · lane_b ai
  tick · fabrication guard) → เขียวหลังซ่อมครบทั้งสี่ข้อข้างบน
- `git merge origin/main` เข้ากิ่งก่อน push → Already up to date (ไม่มี commit ใหม่
  ระหว่างรอบ)
- ชุดเต็ม `pytest tests/ -q` + `pf_gate_preflight.py` → ผลอยู่ท้ายไฟล์นี้

TWO_SESSIONS_SAME_SCENE: roster ของฉากนี้เป็นตารางค่าคงที่ระดับโมดูล อ่านอย่างเดียว
ไม่มี state ต่อ session · composer ถูกเรียกใหม่ทุกครั้งเป็นฟังก์ชันบริสุทธิ์ของ
(scene, roster, ledger) ตามที่ `test_mob_scene_registration_contract.py` ประกาศไว้เอง
· combat state ของฉากนี้ยังไม่ถูกเขียนลง registry ของ A ในรอบนี้ (ยังไม่มีการฆ่า)
· สอง session ที่เข้าฉาก 10 พร้อมกันเห็น roster ชุดเดียวกัน 17 ตัวที่พิกัดเดียวกัน

## PR/status
- `pf_bridge` claim `pf_bridge#1487` (`claude/focused-ramanujan-30ja9z`)
- `pirate-force-server#<PR>` (`claude/nice-meitner-30ja9z`) — **เปิดแล้ว ไม่ draft
  มี `PF-AUTOMERGE: v4`** · body เขียนไว้ชัดว่ารอใบ COO ก่อน merge ตาม `1150` ข้อ 3
  **ห้ามเขียนว่า landed/อยู่บน main จนกว่ารอบถัดไปจะยืนยันด้วย
  `git merge-base --is-ancestor`**
- จดหมาย `notes_to_chief/20260906_1411_LANE-B-ASK-COO-widen-death-scope-bg0010-six-templates.md`

## รอบหน้าทำอะไร
1. **หยิบผล pf-adversary ของรอบนี้เป็นงานแรก** (`ADVERSARY_PENDING`) — โดยเฉพาะเรื่อง
   แถวซ้ำ `(47, 16, 301)` ใน `PLACEMENT_AI_LINKS` และการรั่วข้ามฉากสองทิศ
2. **บริโภคคำตอบใบ `1411`**: COO รับรอง ⇒ PR เดียวเปลี่ยนคีย์เป็น `COO-DECISION ...`
   · COO ปฏิเสธ ⇒ PR เดียวถอด `Bg0010` ทั้งก้อน (import, `_SCENE_TABLE_MODULES`,
   `BG0010_SCENE`, `COMPOSER_BG0010`, ruling, เทส) ไม่มีข้อยกเว้น
3. ยืนยัน PR เซิร์ฟเวอร์ของรอบนี้ด้วย `git merge-base --is-ancestor <sha> origin/main`
4. `GT-274` — เริ่มได้เมื่อ CS วางเนื้อใบ
5. ยังติดเหมือนเดิม ⇒ ปลดแฟล็กหนึ่งตัวจาก `docs/PROMOTION_BACKLOG.md` · **หมายเหตุจาก
   รอบนี้**: `ground_loot_hypothesis.py` (อันดับ 4 ในท่อ promotion ของ NOW) อ่านแล้ว
   **ยังโปรโมตไม่ได้** — มันเป็นสมมติฐานที่ผลบนจอครั้งล่าสุด (GT-045 รอบ 1104) เห็นแค่
   ฝุ่นสีน้ำตาล ~0.45 วิ ไม่มีโมเดล ไม่มีป้ายชื่อ · ปลดแฟล็ก = ยิงเฟรมทดลองใส่ผู้เล่น
   ทุกบูต ไม่ใช่ฟีเจอร์ · แถว B ที่เหลือในท่อรอ P-2 · เสนอให้ COO จัดอันดับใหม่

SCOREBOARD: COMING | ผู้เล่นที่เดินเข้า Deep Sea Temple ชั้น 1 (ฉาก 10 ประตูเปิดอยู่แล้ว) จะเจอมอนสเตอร์ 17 ตัวจากหกพันธุ์จริงในตาราง MOBS ยืนอยู่ในแมพที่เมื่อวานว่างเปล่า และตายได้ทันทีที่ COO เซ็นใบขอที่ส่งไปพร้อมกันรอบนี้ | `pirate-force-server#<PR>` · `notes_to_chief/20260906_1411_LANE-B-ASK-COO-widen-death-scope-bg0010-six-templates.md` · `field_mob_tables_bg0010.py` 17 placements / 6 templates
