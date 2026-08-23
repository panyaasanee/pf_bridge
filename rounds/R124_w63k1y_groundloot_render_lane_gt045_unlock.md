# R124 (w63k1y) — สร้างเลน ground-loot render ปลดบล็อก GT-045

**เวลา:** 2026-08-23 เริ่ม 02:39Z = 09:39 (+07:00) · เซสชัน `w63k1y` · branch `claude/sweet-ride-w63k1y` (bridge) / `claude/wizardly-wright-w63k1y` (server)

## 0) การ์ด + probe (v5)

- ล็อก: ไม่มี PR เปิดค้างทั้งสอง repo ⇒ จับล็อกด้วย empty commit + **draft PR #25** (`pf_bridge`) ก่อนงานทั้งหมด
- probe ①: GitHub MCP tool อ่านรายการ PR ได้จริง (ใช้เป็นทางหลัก) ✅
- probe ② ทาง D: `git fetch origin ci-status` + `ls-tree` บน `pirate-force-server` มีชีวิต (เห็น `ci/*.json` รวม `b665d92`, `e816e73`) ✅ `d_exit=0`
- โครงพี่น้อง: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง ✅ · `git status` ต้นรอบสะอาดทั้งสอง repo ✅

## 1) กล่องจดหมาย

- ไม่มีใบใหม่ค้าง — เช็คทั้งสอง convention ของ stub (`<ชื่อ>.CONSUMED.txt` และ `<ชื่อ.md>.CONSUMED.txt` — ตามหมายเหตุ R123)
  ใบ `20260821_1104_PANYA-DECISION-GT034-spawn-relocate.md` มี stub แบบ convention เก่า = บริโภคแล้ว (R122) จริง

## 2) งานหลักของรอบ — สร้างเลน HYP-PF-032 GROUND-LOOT-001 ปลดบล็อก GT-045

**ที่มา:** GT-045 ในคิวเขียนว่า "BLOCKED — รอ chief สร้างเลนเซิร์ฟเวอร์ใหม่" · เข้าเกณฑ์ pre-approval ข้อ 3
ของ Panya (ฟังก์ชัน gameplay ที่พบใหม่ ใต้ pattern มาตรฐาน opt-in + fail closed + ledger + headless proof)

**ฐานข้อเท็จจริง (ลูกมือ pf-static-re ขุดจาก artifact ที่ commit แล้ว):**
- container = `GSCN_RunTimeProtocolRes 0x6E9D` v4 · derived mask bit `0x08` -> obj `+0x20` -> parser `0x5F85B0`
  (span sha `ce0a58f7...` — **ผ่าน re-derive ปฏิปักษ์ GT-042 ทั้งตาราง** ทั้งขา write `0x89A600` และ read `0x89A640`)
- element บน wire: `tag14 u32 key(+0x10)` เสมอ · `tag0B u8 mask(+0x28)` เสมอ · ตาม bit: `0x02`->tag14 u32 ·
  `0x10`->tag2A f32 x3 · list มี count นำ (tag12 u16) · โครง envelope ลอกจาก encoder พี่น้อง bit `0x02`
  (`make_runtime_remote_actors` ใน v141 — byte-exact อยู่แล้ว)
- ⚠️ แก้ stale ระหว่างทาง: จุดเกิดจริงของ boot ปกติคือ **V135 = (-9239.957..., -2830.045..., 223.292...)**
  (P0-100X-50Y) — docstring ใน report R102 ที่เขียน "P0+100X observation point" เก่ากว่าโค้ด v141 จริง
- ไม่มี id ของ "Red leaves Hammer" ใน artifact ที่ commit ⇒ dword ใช้ `2600001` (ITEM_MISC row 1 สไตล์ loot roller)
  พร้อม nonclaim ว่าไม่พิสูจน์ว่า `+0x14` เป็น item id

**ดีไซน์ที่ลง (ไฟล์ใน `pirate-force-server` branch `claude/wizardly-wright-w63k1y`):**
- `src/pirateforce_foundation/ground_loot_hypothesis.py` ใหม่ — loader/require แบบ permission-token
  (ท่าเดียวกับ HYP-PF-030) + composer **สองเฟรม เฟรมละหนึ่ง element** pin เฟรมละ pc 44B/frame 54B
  (ใกล้ pc sha `A3570BC9...` · ไกล pc sha `4B14A026...`) + การ์ด V135 drift (จุดเกิดขยับ = refuse)
  🔴 **ดีไซน์แรกเป็นหนึ่งเฟรม count=2 — pf-adversary ยิงตกก่อน commit** (V43 เคยวัดจริง: collection
  หลาย record ในเฟรม RuntimeRes เดียวทำ client ยิง `ErrorData=28317` · ท่าที่รอดคือ record เดียวต่อเฟรม
  ตาม `make_port_royal_npc_single_packets`) ⇒ แก้เป็นสองเฟรมก่อนของจริงออกประตู
- `scenarios/ground_loot_hypothesis_bit08_render.json` ใหม่ — สอง element: ใกล้ +30X / ไกล +800X จาก V135
  mask `0x12` ทั้งคู่ · dword `2600001`
- `app.py` 8 จุด (flag `--ground-loot-hypothesis-scenario` + mutual exclusion + ต้องมี --db + mode title)
- `runtime.py`: latch `ground_loot_pair_sent` + dispatch branch ที่ TargetPos แรกหลัง runtime ack —
  **แนบสอง action ต่อท้าย actions ของ super()** (`NEAR_ONCE` 0.0s · `FAR_ONCE` 0.10s — ไม่กลืน
  checkpoint/population ของเฟรม trigger) · ยิงครั้งเดียว/เซสชัน
  · compose drift = event `ground_loot_compose_refused_no_reply` + latch (ไม่ retry ลง wire)
- `docs/HYPOTHESIS_LEDGER.json` + `tools/verify_hypothesis_ledger.py`: entry HYP-PF-032 (append ท้าย ·
  index เดิมนิ่ง) + EXPECTED_IDS/META + re-pin `CANONICAL_CONTENT_SHA256` -> `58549E5B...`
- `.gitignore`: allowlist `tools/pf_ground_loot_headless_replay.py`
- coverage row `npc_interaction/monster_spawn_and_loot` **ไม่ขยับ** (ส่งเฟรม candidate ไม่พิสูจน์ loot —
  เขียนไว้ใน stop_rule ของ entry)

**ฝั่ง `pf_bridge`:** อัปเดตใบ GT-045 — ยืนยันชื่อ flag/scenario จริง (ชื่อเสนอเดิมเลิกใช้) ·
สถานะ -> BLOCKED-รอ-merge · แก้ steps เป็นดีไซน์ยิงอัตโนมัติ (สองเฟรม เฟรมละ element) + พิกัด HUD ที่คาด ·
เพิ่ม hex เต็มเฟรมละ 44 ไบต์ + sha + action labels ลง pass criteria ชั้น wire
(แก้ใบเดิมที่ pf-queue-author ร่างไว้ R123 — เป็นการยืนยันชื่อ/ดีไซน์ ไม่ใช่รายการใหม่ จึงไม่เรียก pf-queue-author ซ้ำ)

**หลักฐาน (เขียวจากที่ไหนระบุเสมอ):**
- เทสเลนใหม่ 29 ใบ ผ่านหมด · headless replay ใหม่ `tools/pf_ground_loot_headless_replay.py`
  **30/30 guards exit 0** บนสำเนา DB ชั่วคราว (walker อิสระอ่านทั้งสองเฟรมกลับจาก byte 0 ไม่พึ่ง composer ·
  ปฏิเสธ count!=1 โดยชื่อ · one-shot คลุมทั้งสอง label · DB ต้นทางไม่ถูกแตะ)
- `verify_hypothesis_ledger.py` PASS 40 entries · ledger tests 10 pass/387 subtests · seam 22 pass
- สวีตเต็ม **เขียว(cloud sanity) 1897 pass / 324 skip / 4362 subtests** (baseline ต้นรอบ 1868/324 —
  +29 คือเทสเลนใหม่พอดี · skip ไม่ขยับ = ไม่แตะ SKIP-CENSUS-001)
- **สถานะเขียวสุดท้ายอ่านจาก gate (Actions) ไม่ใช่จากที่นี่** — PR ฝั่ง server รอ gate ตอนปิดรอบ
- เวลาเทียบ: จับเวลาจริงจาก git — R123 จบ 02:06Z · รอบนี้เริ่ม ~02:39Z (09:39 +07:00)

**erratum ที่พบระหว่างรอบ (จดในจดหมายด้วย):** เวลาใน R123 ทุกไฟล์ +7 ชม. เกินจริง
(เวลาจริง 01:30-02:06Z = 08:30-09:06 +07:00 · R123 เขียน "08:2xZ (15:2x-16:xx +07:00)" —
เอา +07:00 ไปติดป้าย Z แล้วบวกซ้ำ) · เนื้อหางาน R123 ไม่กระทบ · ไฟล์ R123 commit แล้วไม่แก้ย้อน

## 2b) ลูกมือที่ใช้ + ผลตรวจปฏิปักษ์

- `pf-static-re` ×1 (fact pack `0x5F85B0`/envelope/พิกัด) · `general-purpose` ×1 (เทส+replay tool สองรอบ) ·
  `pf-adversary` ×1 (ตรวจ diff ทั้งสอง repo ก่อน commit)
- **adversary: ไม่มี BLOCKER · NOTE 3 ข้อ:**
  ① **(แก้แล้วก่อน commit — ข้อใหญ่)** ดราฟต์แรกส่งหนึ่งเฟรม count=2 = รูปแบบเดียวกับที่ V43 วัดจริงว่า client
  ยิง `ErrorData=28317` (collection หลาย record) ⇒ แก้เป็นสองเฟรม เฟรมละ element ตามท่า
  `make_port_royal_npc_single_packets` ที่พิสูจน์แล้วว่ารอด — กันรอบ attended เสียเปล่า
  ② (governance — จดไว้) chief แก้ใบ GT-045 ที่ pf-queue-author ร่าง — ถือเป็น name/design confirmation
  ไม่ใช่รายการใหม่ · ไม่มีรายการไหนถูกลบ/ย้าย
  ③ (จิ๋ว) เวลาแบนเนอร์ปัดขึ้นเล็กน้อย — เวลา R124 อื่นถูกต้อง · erratum เวลา R123 ตรวจเลขแล้วถูก
- adversary ยืนยันอิสระ: pins reproduce ที่ HEAD · envelope byte-เท่า sibling ยกเว้น mask byte ·
  layout ตรงตาราง GT-042 · ledger sha recompute ตรง · ASCII/cp874 สะอาด · ไม่มีทาง fire นอก opt-in ·
  ไม่มี NameError path · inherited behavior ไม่ถูกกลืน

## 3) สิ่งที่ *ไม่* ได้พิสูจน์ / งานค้าง

- **ไม่มี client เคยเห็นเฟรม bit `0x08`** — เลนนี้พิสูจน์ถึงชั้น wire/dispatcher เท่านั้น · การวาดคือคำถามของ GT-045
- bit `0x08` = ground loot **ยังเป็นสมมติฐาน** — ผลลบ attended ที่ wire ผ่าน = ตัดตัวต้องสงสัยทิ้งถาวร (คำตอบสมบูรณ์)
- dword `2600001` ไม่ claim ว่าเป็น item template id
- GT-034 ทางไปต่อยังรอ Panya เคาะ (NO-RESULT ไม่เห็นตัว — R123) · GT-035/036 คง BLOCKED
- เลน encoder อื่นจาก span GT-040/042 ที่ปลดสิทธิ์แล้ว (เช่น bit `0x04`) ยังไม่เริ่ม — คิวจดหมาย/GT-045 มาก่อน
