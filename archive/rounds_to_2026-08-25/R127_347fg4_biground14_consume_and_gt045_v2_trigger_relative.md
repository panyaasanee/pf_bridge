# R127 (sweet-ride-347fg4) — บริโภครอบใหญ่ #14 + เลน GROUND-LOOT-001 v2 (พิกัดอิง trigger)

- เวลา: 2026-08-23 ~16:0x-16:3x (+07:00) (= ~09:0x-09:3x UTC)
- เซสชัน: sweet-ride-347fg4 · branch เอกสาร `claude/sweet-ride-347fg4` · branch โค้ด `claude/wizardly-wright-347fg4`
- ล็อกรอบ: draft PR #28 (pf_bridge) เปิดก่อนทำงานตาม v5 ① — **ล็อกไม่หลุด** (draft ตั้งแต่วินาทีแรก)

## PROBE (v4)
1. GitHub API/tool: ✅ ใช้ได้ (list PR ทั้งสอง repo + เปิด draft PR #28 สำเร็จ)
2. ทาง D: ✅ มีชีวิต — `git fetch origin ci-status && git ls-tree` exit 0 (เห็นไฟล์คำตัดสินล่าสุดถึง `dfc53699…`)
- โครงพี่น้อง: ✅ `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` อยู่จริง

## กล่องจดหมาย: บริโภค 5 ใบ (รอบใหญ่ #14 · ทั้งหมด stub แล้ว)
1. `20260823_1427` GT-047 GUARD-GAP — จ็อบ 1-2 ผ่าน แต่การ์ด mutation `field_offset` **ไม่แดง** (validator รับ corruption เงียบ ๆ)
2. `20260823_1435` GT-046 PASS — outbound คลิกเมาส์ (`WM_LBUTTONDOWN 0x201`) จาก live runtime drop-object · response `0xFC->0x1F/0xFD->0x03/0xFE->0x22` · **ไม่พบ link ไปบรรทัด `ได้รับ`**
3. `20260823_1450` GT-048 PASS — native scene-placement จาก `bg0001.npc` (RTTI: `SceneNPCCreation`/`NPCPlacement`) · P30/TID31 อยู่ที่ offset `0x1D46` · ไม่ผ่าน `0x0089A640`
4. `20260823_1520` ERRATUM ผู้ช่วย — ถอนสมมติฐาน "TerrainThing=ของวางล่วงหน้า" + เสนอเลน chat template (กลายเป็น GT-049)
5. `20260823_1530` สรุปรอบใหญ่ — GT-045 `DONE: WIRE EXACT / CLIENT NO-RESULT` · GT-001 PASS (CANON_SHA ใหม่ `EE785A79…`) · controls PASS

## งานหลักของรอบ: GROUND-LOOT-001 v2 — พิกัดอิง trigger (repo โค้ด)

**เหตุ (จากผล GT-045 รอบแรก):** เลน v1 พิน**พิกัดสัมบูรณ์**จาก V135 default-boot placement แต่ตำแหน่งจริงของตัวละคร
อยู่ใน DB และมัน drift ไปแล้ว — spawn จริง `(-8553.947265625, -2579.68896484375, 186.0)` ห่างจากที่คาด ~700 หน่วย
⇒ จุด "ใกล้" ไม่ใกล้ geometry ของใบตายทั้งใบ · การ์ด `V135_PLAYER_*` ของ v1 การ์ดผิดตัว (ค่าคงที่ของโมดูล ไม่ใช่ตำแหน่ง DB)

**ดีไซน์ v2 (ไฟล์ที่แตะ 6 ไฟล์ · ทุกอย่างอื่นของเลนคงเดิม):**
- `src/pirateforce_foundation/ground_loot_hypothesis.py` — element เก็บ `x_offset` (30/800) แทนพิกัดสัมบูรณ์ ·
  composer รับ `trigger_xyz` (TargetPos ที่เป็น trigger — f32 exact จาก wire) · ใกล้ = trigger+30X · ไกล = trigger+800X · Y/Z ตาม trigger
- pin เปลี่ยนเป็น **masked-template sha256**: pc 44 ไบต์ zero เฉพาะ 12 ไบต์พิกัด (`[30:34]/[35:39]/[40:44]`)
  ใกล้ `915331D5…FC33` · ไกล `DC6A8FE6…8A14` + assert ไบต์พิกัด == struct.pack ของ trigger+offset ทุกครั้ง
  (ยืนยันความถูกของ layout: pin เก่าทั้งสอง reproduce ได้ไบต์ต่อไบต์ก่อนแก้)
- refusal ใหม่: `ground_loot_trigger_malformed` · `ground_loot_trigger_not_finite` · `ground_loot_offset_overflow`
  (แทน `ground_loot_placement_drift` ที่การ์ดผิดตัว) — ทุกตัวลง latch เดิมผ่าน `ground_loot_compose_refused_no_reply`
- `runtime.py` — ส่ง `tuple(durable_target[:3])` เข้า composer (บรรทัดเดียว)
- `scenarios/ground_loot_hypothesis_bit08_render.json` — regenerate ตาม `_EXPECTED` ใหม่ (permission token · loader round-trip ผ่าน)
- เทส: `test_ground_loot_hypothesis.py` + `test_ground_loot_dispatch.py` ตามดีไซน์ใหม่ + เทสใหม่:
  trigger-relativity (trigger ขยับ ⇒ เฟรมขยับตาม), non-finite/malformed/overflow refusal, masked-template pin
- `tools/pf_ground_loot_headless_replay.py` — pin ใหม่ + section 4b (เซสชันที่สอง trigger เลื่อน 1000X/-250Y/+5Z
  ⇒ เฟรมตาม trigger) · **34 guards PASS** บน DB เปล่าที่สร้างเอง
- `docs/HYPOTHESIS_LEDGER.json` — HYP-PF-032 อัปเดต `exact_value_or_transform` + tracked version
  `GROUND-LOOT-001-v2-trigger-relative` (ONE version of three remains) · canonical sha ใน
  `tools/verify_hypothesis_ledger.py` อัปเดตตาม (ท่าเปลี่ยนโดยเจตนา)

**ผลเทส: เขียว(cloud sanity) 1901 pass / 324 skip / 0 fail (4374 subtests)** — ก่อนแก้ canonical sha สวีตจับ drift ได้จริง 2 ใบ (ทำงานถูก)

## การค้นพบสำคัญ: เกณฑ์ event ของใบ attended = สังเกตไม่ได้โดยโครงสร้าง
`state.events` (รวม `hyp_pf_032_ground_loot_bit08_pair_committed`) เป็น in-memory list — **ไม่มีทางไหนในเซิร์ฟเวอร์จริง
(app/connection/lifecycle) persist มันลงดิสก์/แคปเจอร์** · ตัวอ่านมีเฉพาะ headless replay ⇒ `count=0` ที่ tester รายงาน
ไม่ใช่บั๊กเซิร์ฟเวอร์ แต่เป็นบั๊กใบสั่งของ chief (R124) — แบบเดียวกับบทเรียน console-event ของ GT-032
⇒ ตัดเกณฑ์ event ออกจากใบ GT-045 · action labels ใน raw GAME log ยังสังเกตได้จริง ใช้แทน

## คิว (GAME_TEST_QUEUE.md)
- GT-046 → ✅ PASS/DONE (บล็อกผล + nonclaim สองระบบ) · GT-048 → ✅ PASS (GT-034 ไม่ปิด — อ่านคู่ GT-045)
- GT-047 → 🟠 PENDING/TOOL-GUARD-GAP + **จ็อบ 0**: ส่ง source `pf_validate_capture_fields.py` เข้า repo
  (chief patch ไม่ได้เพราะ source อยู่เฉพาะบนสะพาน — จดลง `IMAGE_ACCESS_COST.tsv` แล้ว)
- GT-045 → 🔴 BLOCKED-รอ-merge v2 · บล็อกผลรอบแรก + pass criteria ชั้น wire เขียนใหม่ (masked template + เกณฑ์พิกัดอิง trigger + ตัดเกณฑ์ event)
- 🆕 GT-049 LOOT-CHAT-TEMPLATE-001 [STATIC-ON-BRIDGE] (ร่างโดย pf-queue-author · ช่องว่างที่ GT-046 เปิด)
- GT-001: PASS บริโภคแล้ว · re-arm ยิงใหม่เพราะ PR รอบนี้แตะ `src/`

## adversary — verdict: PROCEED-WITH-FIXES · 6 defect แก้ครบก่อน commit
1. **[HIGH] steps GT-045 v2 ยังอ้าง "trigger ออกตอนเข้าแมพ" ขัดข้อเท็จจริงที่วัด** (เฟรมออกหลัง `W` แรก
   — จดหมาย 1530 บรรทัด 48) ⇒ เขียน steps 3-4 ใหม่ทั้งก้อน: trigger เป็นของผู้เทสคุมเอง ·
   เริ่ม continuous capture ก่อนกด W · ปิดช่องโหว่ NO-RESULT 0-3.56s ของรอบแรกไปในตัว
2. **[MED] fallback ฐานพิกัดผิดตัว** ("X ตอนเข้าแมพ") ⇒ ชี้ไป hexdump ของเฟรม TargetPos ใน raw GAME log
   (บรรทัดก่อน `SENT GROUND_LOOT_..._NEAR_ONCE`) — แหล่งเดียวกับที่ชั้น wire ให้ decode อยู่แล้ว
3. **[LOW-MED] pin ระดับ frame อ่อนลงเงียบ ๆ** (v1 พิน sha ทั้ง frame · ดราฟต์ v2 เช็คแค่ len+endswith)
   ⇒ เพิ่ม masked-frame template sha256 (spans เดิม shift +10 · header snappy คงที่พิสูจน์แล้ว):
   ใกล้ `199B695E…C9D2` · ไกล `D8A0BD6B…DCE1` — ความคุ้มครองเท่า v1 ยกเว้น 12 ไบต์พิกัด
4. **[LOW] การเช็คไบต์พิกัดใน composer เกือบ tautological** (input ร่วมกับ wire) ⇒ จดเป็นคอมเมนต์ในโค้ด
   + แก้ข้อความ ledger ไม่ให้ oversell (derivation พิสูจน์ด้วยเทส/replay ไม่ใช่ด้วยบรรทัดนั้น)
5. **[LOW] refusal สามตัวใหม่ dispatch เอื้อมไม่ถึง** (parser ปฏิเสธ payload เสียก่อน) ⇒ แก้ ledger ให้เรียกตรง ๆ
   ว่าเป็น defensive API guard · ข้อดีที่ adversary ยืนยัน: v2 **ไม่เพิ่มทางที่ TargetPos เสียจะ latch เลนตายถาวร**
6. **[LOW] เอกสารเขียน "commit แล้ว" ก่อน commit จริง** ⇒ สลับลำดับ: commit+push โค้ดก่อน (`4f31956` · PR #10)
   แล้วค่อยเติมเลขจริงลงคิว/จดหมาย/ไฟล์นี้
สิ่งที่ adversary ลองหักแล้วหักไม่ได้: คำอ้าง "server ไม่ persist events" (grep ครบ ทั้ง src+v141) ·
masked pins คำนวณซ้ำตรงทุกตัว + pin v1 reproduce ใต้ layout เดียวกัน · hex template ในใบตรงไบต์ ·
trigger อ่านได้จาก raw GAME log จริง · scenario token round-trip · ledger verifier + suite ตัวเลข re-derive ครบ

## commit/PR ของรอบ
- pirate-force-server: commit `4f31956` บน `claude/wizardly-wright-347fg4` · **PR #10** (marker ครบ · รอ gate → automerge)
- pf_bridge: branch `claude/sweet-ride-347fg4` · draft PR #28 (ล็อกรอบ — ปลด draft ตอนปิดรอบ)

## สิ่งที่ไม่ได้พิสูจน์ / nonclaims
- v2 ยังไม่เคยถูกไคลเอนต์จริงเห็น — GT-045 v2 ต้องรอ merge แล้วรัน attended ใหม่
- ไม่ claim ว่า bit 0x08 คือ ground loot (คำถามเดิมของ GT-045 ยังเปิด)
- เขียวทั้งหมดของรอบนี้คือ เขียว(cloud sanity) — gate จริงอยู่ที่ Actions (subset) และสะพาน (เต็ม)
- การถอดว่า "เกณฑ์ event สังเกตไม่ได้" มาจากการอ่านซอร์สฝั่งเรา ไม่เกี่ยวอะไรกับพฤติกรรม client
