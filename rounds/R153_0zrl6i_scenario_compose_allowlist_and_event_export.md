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

### ผลรวมเทส (ตัวเลขสุดท้าย หลังแก้ defect ของ adversary)

- สวีตเต็ม: **2166 passed / 324 skipped / 4437 subtests เขียว(cloud sanity)** — เพิ่ม +16 จาก main
  (2150): pickup 47→50 (+3 — ถอด 2 เติม 6 แต่มี 1 เทสในไฟล์เกิด runtime) · event_export ใหม่ +13
- skip count **ไม่ขยับ** (324 — `docs/PYTEST_SKIP_PINS.json` ไม่แตะ · หมายเหตุจาก adversary D6:
  ไฟล์นั้น pin design-skip ตัวเดียว ส่วน 324 คือ skip ระดับสวีต — สองข้อเท็จจริงคนละชั้น)
- ไฟล์ที่แตะ 7: `src/pirateforce_foundation/app.py` · `src/pirateforce_foundation/runtime.py` ·
  `tests/test_pickup_listener_hypothesis.py` · `tests/test_event_export.py` (ใหม่) ·
  `tests/test_foundation_legacy_seam.py` (docstring — ตามกฎ same-commit ของไฟล์เอง · adversary D4) ·
  `docs/HYPOTHESIS_LEDGER.json` · `tools/verify_hypothesis_ledger.py`
- **commit `99bfa96` บน `claude/amazing-goodall-0zrl6i` → PR โค้ด #23** (มี marker · รอ gate ·
  workflow merge เองเมื่อเขียว) — รอบถัดไปอ่านคำตัดสิน gate ของ head นี้ตามทาง D

## adversary (รันจบก่อน commit จริง · defect 6 ข้อ — แก้ครบ D1–D5 · D6 แก้ที่ถ้อยคำเอกสารรอบนี้)

- **D1 (medium):** exporter ฉบับแรก raise ทะลุเข้า dispatch ได้ (stream ตาย/BrokenPipe) —
  สาธิตแล้วว่า latch one-shot ถูกเผาและ **game listener thread ตายเงียบทั้งเส้น**
  ⇒ แก้: ห่อ export ทั้งก้อนด้วย try/except — เสียบรรทัด diagnostic หนึ่งบรรทัด ดีกว่า dispatch เปลี่ยนพฤติกรรม
  + เทสใหม่ dead-stream
- **D2:** อักขระควบคุม ASCII (`\x0b` `\x0c` `\x1c`–`\x1e`) รอด backslashreplace ⇒ หนึ่ง event
  แตกเป็นสองบรรทัดได้ ⇒ แก้: escape ทุกตัวนอกช่วง printable เป็น `\xNN` + เทส
- **D3:** docstring อ้าง "seq ทั้ง process" แต่ implementation เป็นต่อ exporter ⇒ แก้ docstring ให้ตรงจริง
- **D4:** กฎใน docstring ของ seam file ("ทำ mode ให้ประกอบกันได้ ต้องประกาศใน commit เดียวกัน")
  ⇒ เติมบล็อกประกาศลงวันที่ใน docstring (ไม่มีเทสของไฟล์นั้นขยับ)
- **D5 (info):** เส้น `stream=None → sys.stdout` ไม่เคยถูกเทส ⇒ เติมเทส redirect_stdout ·
  ส่วน **เส้น CLI composed happy-path เต็ม (app.main + --db จริง) ยังไม่เคยรัน** — จดเป็น nonclaim ข้างล่าง
- **D6 (info):** ข้ออ้าง "ทุกไฟล์ที่แตะ ascii+cp874" เป็นเท็จสำหรับ 2 ไฟล์ที่มีไทยอยู่ก่อนแล้ว
  (ledger/tool — ของเดิม ไม่ใช่ diff รอบนี้ · บรรทัดที่เพิ่มรอบนี้ ASCII ล้วนทุกบรรทัด) + ถ้อยคำ skip-pin ข้างบน
- **ข้ออ้างที่ adversary พยายามหักแล้วหักไม่ได้ (verify เองทั้งหมด):** กวาดครบ 276 คู่ + 22 สามตัว —
  มีคู่เดียวผ่าน gate · ไม่มีทางเขียน/แทน `self.events` นอก append (grep ครบทั้ง src/ current/) ·
  default boot ไม่เปลี่ยน · สองเลน disjoint จริง (ชื่อ event ไม่ชนกัน — วินัย attribution ใช้ได้) ·
  ledger amendment ตรงจดหมายและ pin เดินถูก · ลำดับด่าน CLI พิสูจน์เทส CLI-pair จริง ·
  adversary รันสวีตเต็มซ้ำเอง exit 0 ตรงตัวเลข

## คิว / ใบเทส (ผล pf-queue-author — ใส่ลง GAME_TEST_QUEUE.md แล้วในรอบนี้)

- **GT-063 ITEMOPERATE-RES-GREENLINE-SHAPE-001** เปิดแล้ว (เลขยืนยันว่างจากคิว ณ ต้นรอบ):
  sweep 3 ทรงของ `0x4C13` (control count=0 ตรง capture · count=1 id `2400901` qty 1 · qty 5) ·
  P1–P4 · pass criteria สองชั้น · **BLOCKED (ก) เลน sweep ฝั่ง server ยังไม่มีในโค้ด — เลนโค้ดรอบถัดไป
  แล้วรอ merge · ชื่อ flag/label ในใบเป็น [เสนอ] ทั้งหมด ห้ามบูตด้วยชื่อเดา** · (ข) รอปลดพัก attended
- **GT-060 เงื่อนไข (ข) แคบลง:** คำเคาะ composition มาแล้ว ⇒ เหลือ GT-045 เทสตา PASS (นัด 26 ส.ค.)
  + โค้ด composed-boot (PR #23) merge เข้า main
- ข้อควรระวังที่จดไว้ในใบ: การรวม GT-063 เข้าบูตคู่ GT-060 = composition **สามเลน** ซึ่งเกิน
  allow-list ปัจจุบัน (อนุมัติแค่คู่) — ต้องขอ Panya เพิ่มทีละคู่ ห้าม chief อนุมัติเอง

## สิ่งที่ยังไม่ได้พิสูจน์ (nonclaims ของรอบ)

- ไม่ได้พิสูจน์ว่า client จริงยิง `0x4543` หรือวาด drop-object — นั่นคือหน้าที่ GT-045/GT-060/GT-063
- เขียว(cloud sanity) ไม่ใช่ gate ตัวจริง — gate = Actions (subset) ตอน PR #23 + gate เต็มบนสะพาน
- exporter ยังไม่เคยถูกเห็นบน console cp874 จริง — พิสูจน์ด้วยเครื่องมือ encode ในเทสเท่านั้น
- **เส้น CLI composed happy-path เต็ม** (app.main ด้วยสอง flag + `--db` มีจริง จนถึงบูต) ยังไม่เคยรัน —
  พิสูจน์ถึงชั้น make_state_class + ลำดับด่าน CLI เท่านั้น (adversary D5) · ป้าย mode composed
  บน console ก็ยังไม่เคยแสดงจริงเช่นกัน — ผู้เทสตรวจหัวหน้าต่างตอนบูต composed ครั้งแรก
- ตัวเลขรอบ: จบรอบโดยใช้ ~290k token (วัดจาก budget ของเซสชัน ณ จุดเขียนบรรทัดนี้ — จดตามกติกา
  "รอบข้ามต้องถูก" เพื่อให้มีฐานเทียบ; รอบนี้เป็นรอบทำงานเต็ม ไม่ใช่รอบข้าม)
