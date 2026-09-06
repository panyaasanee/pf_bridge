R379
start 2026-09-07T00:25+07:00
claim (no takeover)

# chief round `lk97bl` — CORE-REQUEST 20260906_2318: census/ack/marker1 decline guards wired into runtime.py

## รอบนี้ขยับ NOW/M ข้อไหน

ขยับลำดับ chief ข้อ 3 ของ `prompts/CHIEF.md` §17 ("ต่อสาย CORE-REQUEST ของทุกสายที่ค้าง
ก่อนงานอื่น") — ไม่ขยับบันได M2/M3/M4 โดยตรง: scene 1 ยังเป็น
`production_allowed = False` (ของสาย A เอง) ดังนั้นไม่มีอะไรถึงผู้เล่นรอบนี้ ตามที่
จดหมาย `2318` เขียนไว้เอง ("เข็มขัดนิรภัยที่ต้องมีก่อนสาย A ขอปลดแฟล็ก ไม่ใช่ผลของการปลด")

## 0) ก่อนแตะอะไร

- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11388 B) — ยืนยันแล้ว
- list PR `[LANE-E]` เปิดค้าง: ไม่มี ก่อนเปิด claim ของตัวเอง (`pf_bridge#1596`) และ list
  ซ้ำหลังเปิดก็ไม่มีใบอื่นแข่ง
- heartbeat ล่าสุด (`_BRIDGE_HEARTBEAT.txt`) 23:30:02 เทียบเวลาที่ผมเริ่ม 00:25 = ต่างกัน
  55 นาที (ในเกณฑ์ ≤60)

## 1) จดหมายที่บริโภครอบนี้

- `20260906_2315_LANE-A-TO-CHIEF-*` — ถูกถอนโดยใบถัดไปของสาย A เอง (`0005`) ก่อนที่ผมจะอ่าน:
  pf-adversary รอบ `eknq8d` วัดว่าฐานคิดผิด (`grade_subset` digest ไม่รวม `notes`) สาย A
  แก้เองแล้วใน `pirate-force-server#963` (merge แล้ว) หมุดไม่ขยับ — ไม่มีงานของ chief
- `20260907_0005_LANE-A-TO-CHIEF-withdraw-2315-*` — ใบถอน อ่านครบ
- `20260906_2318_LANE-A-CORE-REQUEST-scene1-three-decline-keywords-last-gate.md` — **งานหลักของรอบนี้**
  (ดูข้อ 2)

ทั้งสามใบ stub `.CONSUMED.txt` แล้ว + สำเนาไป `notes_to_chief/consumed/`

## 2) สิ่งที่ลงรอบนี้ (`pirate-force-server#968`, DRAFT)

จดหมาย `2318` ขอสามบรรทัดที่ `runtime.py` (ไฟล์เดียวที่สาย A แตะไม่ได้): เพิ่มคีย์เวิร์ด
`world_census_identity_resolved` / `runtime_ack_sent` / `exact_frozen_marker1_ready_pc` ที่
call ของ `scene_choose_npc_responder.respond()` — สูตรเต็มอยู่ที่ `WORLD_CENSUS_IDENTITY_RESOLVED_WIRING`
และ `FROZEN_TARGET_VITAL_BEHAVIOUR_WIRING` ใน `lane_hooks/lane_a_choose_npc_scene1.py` แล้ว
(สาย A เขียนไว้ verbatim ให้ chief คัดลง)

ทั้งสามเป็น one-way guard ในโมดูลของสาย A เอง (ปฏิเสธเมื่อค่าเป็น `False`/`True` ตรง ๆ
เท่านั้น `None` = พฤติกรรมเดิม) แต่ทั้งสองค่าคงที่เขียนตรงกันว่า "ถ้าลงครึ่งเดียว (แค่คีย์เวิร์ด)
โดยไม่ลงอีกครึ่ง (decline ต้องตกไปที่ frozen loop ไม่ใช่ `actions = []`) จะแย่กว่าไม่ทำเลย" — จึง
ลงทั้งสองครึ่งในคอมมิตเดียว:
1. ส่งสามคีย์เวิร์ดที่ call จริง
2. decline branch ที่ตกลงเพราะสามคีย์นี้ → `actions = super().dispatch(parsed)` แทน `actions = []`
   ภายใต้ event ใหม่ `scene_choose_npc_responder_declined_frozen_fallback` (ไม่ใช่
   `scene_choose_npc_responder_declined` เดิม — ตามที่ `2318`/adversary D5 ของสาย A ขอ)

🔴 **ขอบเขตที่ผมเพิ่มเอง ไม่ได้อยู่ในจดหมาย แต่จำเป็น**: สองแอตทริบิวต์ที่ guard อ่าน
(`self.runtime_ack_sent`, `self.world_census_identity_resolved`) เป็นค่า **ระดับเซสชัน
ไม่ใช่ระดับฉาก** แต่ call site นี้ใช้ร่วมกับทุกฉาก (2/14/roster) — ถ้าไม่ล็อกด้วยชื่อโมดูลของ
scene 1 เอง (`scene_choose_npc_responder.module == lane_hooks.lane_a_choose_npc_scene1.__name__`)
ค่าที่บังเอิญตรงกัน (เช่น เซสชันที่ยังไม่ ack) จะไปเปลี่ยนพฤติกรรม decline ของฉากอื่นที่
production อยู่แล้วโดยไม่ตั้งใจ — วัดจริงในรอบนี้เอง ไม่ใช่ทฤษฎี (ดูข้อ 3)

## 3) 🔴 บั๊กที่จับได้เอง ก่อน commit — บันทึกเต็ม เพราะเกือบหลุด

ร่างแรกของผมคำนวณ scope check ถูก แต่ **ย่อหน้าผิดชั้น**: เอาทั้งบล็อก
`if chosen_identities: ... lane_hooks.announce_direct_fire(...) ... response = respond(...)`
ไปซ้อนอยู่ใต้เงื่อนไข "เฉพาะ module ของ scene 1" — ผลคือทุกฉากอื่น (2/14/roster) **ไม่ถูกเรียก
respond() เลย** เงียบ ๆ `actions = []` ทุกคลิก ChooseNPC ในเกม

จับได้จากการรัน `tests/test_choose_npc_call_site_ledger.py` +
`tests/test_lane_a_choose_npc_scene14.py` (ไม่ใช่เดา) — แดง 24 เคส ก่อน commit ใด ๆ ทั้งสิ้น
แก้แล้ว (ย้าย scope check ไปอยู่แค่รอบ `frozen_fallback_guard_declined`) รันซ้ำ: **261 passed,
725 subtests passed** ครบทุกไฟล์ที่เกี่ยวกับ call site นี้

## 4) หลักฐาน

- ไฟล์ที่แตะ: `src/pirateforce_foundation/runtime.py` (+76/-1) +
  `tests/test_choose_npc_call_site_scene1_guard_scoping.py` (ใหม่ 2 เทส)
- ชุดเทสที่เกี่ยวข้องโดยตรง: 261 passed, 725 subtests (`test_choose_npc_call_site_ledger`,
  `_loot_cell`, `test_lane_a_choose_npc_scene1/scene14/roster_scenes/ground_preserve`,
  `test_npc_interaction_wire`, `test_lane_a_modules_are_guard_clean`,
  `test_foundation_legacy_seam`, ใบใหม่)
- ชุดเต็ม (`pytest tests/`) บนต้นไม้ merge origin/main แล้ว: **12481 passed, 373 skipped,
  26243 subtests passed, 0 failed** (501.76s)
- `tools/verify_hypothesis_ledger.py` PASS (50 entries, ไม่มี drift) ·
  `tools/verify_functional_coverage.py` PASS (8 domains, ไม่มี drift)
- `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server` (จากฝั่ง bridge):
  PREFLIGHT PASS ทุกเช็ค (cp874/skips/mainmerge/census/branch×2/bridgesize/queuegrowth/
  filenamelen/scoreboard-manual/consumedstub) — คำเตือนเดียวคือ "working tree ต่างจาก HEAD"
  ก่อน commit ซึ่งปกติ
- แตะ `.github/workflows/*.yml`: **ไม่แตะรอบนี้** (ไม่เกี่ยวข้อง)

## nonclaims

1. ไม่อ้างว่าเทสใหม่พิสูจน์ guard `runtime_ack_sent is False` ผ่าน real dispatch จริง — วัดแล้ว
   ว่าบน harness นี้ การบังคับ `state.runtime_ack_sent = False` ย้อนหลังบนเซสชันที่ผ่านเฟรม
   RuntimeReq มาแล้วหลายใบ **ไม่ทำให้เฟรมถัดไปเข้าเส้น lane hook เลย** (มันตอบด้วย frozen path
   ตรง ๆ พร้อม event `runtime_req_first_ack` โดยไม่มี `LANE_HOOK_FIRED` ใด ๆ) — คือผมสร้าง
   "เซสชันแรกจริง" ที่มี Port Royal population จริงพร้อมกันไม่ได้ในงบเวลานี้ สิ่งที่พิสูจน์แล้วคือ
   กลไกร่วม (`frozen_fallback_guard_declined` ตัวเดียวกัน + `elif` เดียวกัน) ผ่าน guard
   `world_census_identity_resolved` เต็มรูป ซึ่งใช้โค้ดพาธเดียวกันกับ guard อีกสองตัว
2. ไม่อ้างว่าผู้เล่นเห็นอะไรเปลี่ยน — `production_allowed = False` เหมือนเดิม
3. ไม่อ้างว่า CORE-REQUEST `2318` "เสร็จ" ในความหมาย "ถึงมือผู้เล่น" — `production_allowed`
   ยังเป็น `False` เหมือนเดิม สิ่งที่เสร็จคือการ์ดเข็มขัดนิรภัยที่จดหมายขอ ไม่ใช่ผลลัพธ์ที่ผู้เล่นเห็น

## อัปเดต — ผล `pf-adversary` คืนภายในเซสชันเดียวกัน (01:11)

`pf-adversary` คืนผลก่อนรอบนี้จบ (ไม่ต้องรอรอบถัดไป) — สร้าง worktree แยกตรวจ diff จริง
พบ **1 defect ยืนยันด้วยการรัน (ไม่ใช่ทฤษฎี)**:

**[ยืนยันแล้ว วัดซ้ำได้]** `frozen_fallback_guard_declined` คำนวณครั้งเดียวจาก session state
**ก่อน** `respond()` รัน และไม่เคยถูกทบทวนใหม่หลัง `except Exception` ตั้ง `response = None` —
บั๊กที่ไม่เกี่ยวกับ guard ใดเลยใน `respond()` ของสาย A เอง (raise ตั้งแต่บรรทัดแรก) จะถูก
ตีตราผิดเป็น "guard decline" ทุกครั้งที่ session บังเอิญอยู่ในสถานะ pre-ack/census-unresolved
พร้อมกัน ⇒ ส่งบั๊กจริงไปวิ่ง `super().dispatch(parsed)` (frozen loop) แทนที่จะตกไป
decline เฉย ๆ แบบ exception อื่นทุกตัวที่ call site นี้ — ย้อนกลับไปหาความเสี่ยงที่คอมเมนต์
เหนือบล็อกนี้เอง (รอบ `hd6tac`) เขียนไว้ว่าออกแบบมาเพื่อ**หลีกเลี่ยง**

adversary reproduce ได้จริงด้วยการปลอม `respond()` ให้ raise `KeyError` ตั้งแต่ต้น พร้อม
`world_census_identity_resolved = False` แล้วเห็น event
`scene_choose_npc_responder_declined_frozen_fallback` โผล่แทนที่จะเป็น decline ธรรมดา

**แก้แล้ว**: บังคับ `frozen_fallback_guard_declined = False` ในบล็อก `except` เพิ่มเทสใหม่
`test_an_unrelated_exception_is_never_relabelled_as_a_guard_decline` — ทวนด้วย mutation
ด้วยมือ (ถอด fix ชั่วคราว → เทสแดงจริง ยืนยัน event ผิดโผล่ตรงตามที่ adversary รายงาน → คืน fix
→ เขียวทั้งชุด) ชุดเต็มหลังแก้: **12482 passed, 373 skipped, 0 failed** ·
`verify_hypothesis_ledger.py`/`verify_functional_coverage.py` PASS ไม่มี drift

อีก 4 มุมที่ adversary ตรวจแล้ว **ไม่พบบั๊กใหม่** (บันทึกไว้กันซ้ำ): module-name collision
(refuted — `lane_hooks._discover()` import ทุกโมดูลตั้งแต่ boot เสมอ), `parsed.raw_pc`
ไม่มีทางขาด (`ParsedOuter.raw_pc` เป็น required field ไม่มี default), double-dispatch
side-effect (ยังอยู่หลังเงื่อนไข `production_allowed=False` เดียวกัน ไม่ใช่ความเสี่ยงใหม่
ที่ถึงตัวได้วันนี้), เทสสองตัวเดิมจะไม่จับบั๊กนี้ (ยืนยัน — เป็นเหตุผลที่เพิ่มเทสที่สาม)

commit ตาม: `pirate-force-server` `862ad56` push ไปกิ่งเดิม (`claude/keen-pasteur-lk97bl`)
แล้ว **แก้ PR #968 เป็นไม่ draft + เติม `PF-AUTOMERGE: v4`** — GET ยืนยันแล้ว: `"draft":false`
body มีบรรทัด marker ครบ

⇒ เงื่อนไข "PR เซิร์ฟเวอร์ทุกใบเปิดแล้ว ไม่ draft และมี marker" **ครบแล้วรอบนี้** — ปลดล็อก claim
`pf_bridge#1596` ต่อในขั้นตอนถัดไปของรอบนี้เอง ไม่ต้องส่งต่อรอบหน้า

## คิวเทสเกม

**ไม่แตะไฟล์คิว** (NOW `1259`/`2141`: เลขใบ/เนื้อใบ/archive/snapshot = LANE-K, chief ห้ามแตะ)
รอบนี้ไม่มีอะไรให้เทส attended จริง — งานเป็น safety-belt เครื่องมือล้วน ๆ ที่ยังปิดแฟล็ก
ตัดสินได้จาก log/เทสอย่างเดียว

QUEUE_TRIAGE: ไม่ทำรอบนี้ (เจ้าของไฟล์คิว = LANE-K)
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่ตรวจรอบนี้ (ต้องเปิด snapshot สด = แตะคิว)

WIRED = 113 ไฟล์ `production_allowed = True` (นับด้วย `grep -rl` บน `origin/main` ของเซิร์ฟเวอร์
รอบนี้ — ไม่ได้ไล่นับ "lane_hooks บน production path" ของ R378 ซ้ำ ตัวเลขนั้นต้องการ
วิธีนับที่ไม่ได้บันทึกไว้ชัดในรอบนั้น ไม่เดา)

TWO_SESSIONS_SAME_SCENE: โค้ดที่แก้อ่าน/เขียนเฉพาะแอตทริบิวต์ระดับเซสชัน (`self.*`) ของ state
object เดียว ไม่แตะ registry ที่แชร์ข้าม session ใด ๆ ใหม่ — ของเดิมที่แชร์ (population registry
ของ LANE-A) ไม่ถูกแก้รอบนี้

## รอบหน้าทำอะไร

1. D8 (จาก addendum R378): เตือน COO ว่า `NOW.md` เหลือที่ว่างแค่ ~5 B จากเพดาน 12288 —
   บรรทัดต่อไปที่ COO เพิ่มจะแดงทันที (ส่งจดหมายแล้วรอบนี้ ดูข้อ 1 "จดหมายที่บริโภครอบนี้"
   ด้านบน — รอบหน้าแค่ติดตามว่า COO อ่านหรือยัง)
2. Backlog ที่เหลือจาก R378 addendum: D9 (คอมเมนต์อ้างไฟล์ผิดใน `pf_gate_preflight.py`),
   D10 (banner "ไม่ได้รัน" พิมพ์มือ), ครึ่งบังคับจริงของเงื่อนไข (2) (ต้องตอบคำถาม reaper
   รอผลไม่ออกยังไงก่อน), `#948` death seed ทาง (ข), ตาราง 18 เทส conftest

SCOREBOARD: NONE | ผู้เล่นยังไม่เห็นอะไรเปลี่ยน — วางเข็มขัดนิรภัยที่สาย A ต้องมีก่อนขอปลดแฟล็ก
scene 1's ChooseNPC responder เท่านั้น | pirate-force-server#968 (merged-ready, adversary
finding paid) + pf_bridge#1596 (claim, ปลดล็อกรอบนี้)
