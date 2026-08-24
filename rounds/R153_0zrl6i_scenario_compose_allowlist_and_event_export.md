# R153 (exciting-goldberg-0zrl6i) — SCENARIO-COMPOSE-001 allow-list + EVENT-EXPORT-001

**เวลา:** 2026-08-24 ~18:5x–19:xx (+07:00) · **เซสชัน:** exciting-goldberg-0zrl6i (cloud Routine)
**branch pf_bridge:** `claude/exciting-goldberg-0zrl6i` (ล็อกรอบ = draft PR #54 เปิดก่อนเริ่มงานตาม v5)
**branch โค้ด:** `claude/amazing-goodall-0zrl6i`

## ล็อกรอบ + probe (ทำตามลำดับ v5 ครบ)

- ต้นรอบไม่มี PR เปิดค้าง `claude/*` ทั้งสอง repo ⇒ จับล็อก: empty commit `round claim` + push + **เปิด draft PR #54 ทันทีก่อนงานอื่น** (body มี marker)
- **probe ข้อ 1 (GitHub API/tool):** ✅ ใช้งานได้จริง — list PR ทั้งสอง repo สำเร็จ และเปิด PR ได้ (PR #54)
- **probe ข้อ 2 (ทาง D `ci-status`):** ✅ มีชีวิต — `git fetch origin ci-status` + `ls-tree` สำเร็จ (`d_exit=0`, มีไฟล์ `ci/<sha>.json` ครบถึง `fa1e804...`)
- โครงพี่น้อง: `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง ✅

## จดหมายที่บริโภค (2 ใบ — สำเนา + stub ตามท่า R108 ห้ามลบต้นฉบับ)

1. `20260824_1831_PANYA-RULINGS-combine-scenarios-and-open-GT-063.md` — **คำเคาะ Panya 2 ข้อ**:
   ① อนุญาตรวม scenario แบบ **allow-list** เริ่มคู่เดียว `ground-loot-hypothesis + pickup-listener-hypothesis`
   (อีก 22 เลน exclusive เหมือนเดิม · เงื่อนไขวินัย: ข้อสังเกตที่ระบุเลนต้นเหตุไม่ได้ = NO-RESULT)
   ② อนุมัติเปิดใบ `GT-063 ITEMOPERATE-RES-GREENLINE-SHAPE-001` (ทรงไหนของ `0x4C13` ทำให้บรรทัดเขียวขึ้น)
   · ข้อ ④ ของจดหมาย: **เลน attended ยังพักอยู่ ห้ามบูต**
2. `20260823_1605_PANYA-DIRECTION-pause-attended-open-class-skill-lane.md` — หลุมศพชื่อไฟล์
   (เนื้อจริงอยู่ฉบับ `1656` ซึ่งบริโภคไปแล้ว) — วาง stub เพื่อให้ census กล่องเลิกฟ้องเท่านั้น

## งานโค้ด (repo `pirate-force-server` · ทั้งสองงาน pre-approved)

### A. SCENARIO-COMPOSE-001 — allow-list คู่ scenario ตามคำเคาะ ①

- `runtime.py`: เพิ่มค่าคงที่ `COMPOSABLE_SCENARIO_LANE_PAIRS` (มีคู่เดียว: ground_loot + pickup_listener)
  · เปลี่ยนด่าน `active_modes > 1` เป็นชุดชื่อเลน แล้วยกเว้น **เฉพาะ** คู่ที่อยู่ใน allow-list
  · ข้อความ error เดิมคงไว้ (คู่/สามตัวอื่นโดนปฏิเสธเหมือนเดิมทุกตัวอักษร)
- `app.py`: ด่าน CLI ใช้ **ค่าคงที่ตัวเดียวกัน** (import จาก runtime — สองด่าน drift กันไม่ได้)
  · บูต composed ติดป้าย mode `ground-loot-hypothesis+pickup-listener-hypothesis` บน console title
- เหตุที่คู่นี้ประกอบกันได้เชิงโครงสร้าง (ตรวจจากซอร์สก่อนแก้): spawner ผูกกับ TargetPos + latch
  `ground_loot_pair_sent` · listener ผูกกับ vital id ของตัวเอง `0x4543` · ไม่แชร์ state กัน
- เทส: flip 2 เทสเดิมใน `test_pickup_listener_hypothesis.py` (ที่เคย pin ว่า "คู่นี้ต้อง refuse
  จนกว่ามี owner ruling" — ตอนนี้ ruling มาแล้ว) เป็นชุดใหม่ 6 เทส:
  คู่ allow-list ประกอบได้ + **ทั้งสองเลนทำงานจริงในบูตเดียว** (listener นับ accepted=1 ·
  spawner ยิงคู่เฟรม NEAR/FAR บน TargetPos แรก) · คู่+ตัวที่สาม refuse · คู่นอกลิสต์ refuse
  (ทั้งชั้น factory และชั้น CLI) · CLI รับคู่แล้วยังบังคับ `--db` เหมือนเดิม
- `docs/HYPOTHESIS_LEDGER.json`: dated amendment 2 รายการ (HYP-PF-032 · HYP-PF-036 — วลี
  "mutually exclusive with every other scenario mode" ถูกกำกับด้วย AMENDED BY SCENARIO-COMPOSE-001)
  · ขยับพิน `CANONICAL_CONTENT_SHA256` ใน `tools/verify_hypothesis_ledger.py` พร้อมคอมเมนต์ลงวันที่
  (แบบอย่าง R151) ⇒ `verify_hypothesis_ledger.py` **PASS entries=44**
- seam test (`test_foundation_legacy_seam.py`) **ไม่แตะ**: sweep ของมันครอบเฉพาะ 5 โหมดแรก
  ซึ่งไม่มีตัวไหนอยู่ในคู่ allow-list — ยังเขียวโดยไม่แก้

### B. EVENT-EXPORT-001 — exporter พิมพ์ scenario event ออก console (งานแรกที่ R152 สั่ง)

- ที่มา: R152 พิสูจน์จากซอร์สว่า build ปัจจุบัน append event 179 จุดใน `runtime.py`
  แต่**ไม่มีผู้อ่านเลยนอกจากเทส** ⇒ ใบเทสที่อ้าง event string เป็นหลักฐานไม่มีวันเป็นจริง
- ดีไซน์: flag opt-in `--export-events` (default ปิด = บูตปกติไม่เปลี่ยนแม้แต่บรรทัดเดียว)
  ⇒ `make_state_class(event_exporter=...)` ติดตั้ง `_EventEchoList` แทน list เปล่า **ก่อน dispatch แรก**
  ⇒ ทุก `self.events.append` (dispatch และ reject — ทุก event ผ่าน append เท่านั้น ไม่มีทางอื่น)
  สะท้อนออก stdout เป็น `PF-EVENT <seq> <event>` หนึ่งบรรทัด ASCII ล้วน
  (backslashreplace + escape \n \r — กัน console cp874 ตายกลางรายงาน ตามแผลรอบ 86/142)
- เทสใหม่ `tests/test_event_export.py` 11 เทส: format/seq · sanitize payload ร้าย ·
  echo-list เท่ากับ list ปกติ · เส้นทาง make_state_class จริง: event ฝั่ง accept และฝั่ง refuse
  ของเลน pickup ถึง exporter ทั้งคู่ · default = list ธรรมดา ไม่มี output · CLI wiring (ast-bound)

### ผลรวมเทส

- สวีตเต็ม: **2164 passed / 324 skipped / 4437 subtests เขียว(cloud sanity)** — เพิ่ม +14 จาก main
  (2150) = เทสใหม่พอดี (pickup: −2 +6 ⇒ +3? จริง 47→50 = +3 · event_export +11)
- skip count **ไม่ขยับ** (324 ตรงพิน SKIP-CENSUS)
- ไฟล์ที่แตะ 6: `src/pirateforce_foundation/app.py` · `src/pirateforce_foundation/runtime.py` ·
  `tests/test_pickup_listener_hypothesis.py` · `tests/test_event_export.py` (ใหม่) ·
  `docs/HYPOTHESIS_LEDGER.json` · `tools/verify_hypothesis_ledger.py`

## adversary (บังคับก่อน commit)

- ⏳ pf-adversary กำลังรัน ณ เวลาที่เขียนบล็อกนี้ — ผลจะเติมท้ายไฟล์นี้ก่อนเปิด PR โค้ด
  (กติกา: commit โค้ดเกิดหลัง adversary จบและแก้ defect ครบเท่านั้น)

## คิว / ใบเทส

- ⏳ pf-queue-author กำลังร่าง **GT-063** (เลขยืนยันว่างแล้วจากคิว ณ ต้นรอบ) + snippet แก้เงื่อนไข (ข)
  ของ **GT-060** (คำเคาะ composition มาแล้ว ⇒ (ข) เหลือ GT-045 เทสตา PASS + รอ merge โค้ด composed)
- ทั้ง GT-060/GT-063 ยังติด (ค) ปลดพัก attended — Panya ยังไม่ปลด (จดหมาย 1831 ข้อ ④)

## สิ่งที่ยังไม่ได้พิสูจน์ (nonclaims ของรอบ)

- ไม่ได้พิสูจน์ว่า client จริงยิง `0x4543` หรือวาด drop-object — นั่นคือหน้าที่ GT-045/GT-060/GT-063
- เขียว(cloud sanity) ไม่ใช่ gate ตัวจริง — gate = Actions (subset) ตอน PR + gate เต็มบนสะพาน
- exporter ยังไม่เคยถูกเห็นบน console cp874 จริง — พิสูจน์ด้วยเครื่องมือ encode ในเทสเท่านั้น
