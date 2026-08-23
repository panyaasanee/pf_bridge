# R140 (2ke1il) — เลน LEARN-SKILL-REQUEST: inbound decoder `CLearnSkillVital 0x36AA` + แม่บ้าน continuation

- **เซสชัน:** branch `claude/exciting-goldberg-2ke1il` (pf_bridge) · `claude/amazing-goodall-2ke1il` (server)
- **เวลา:** 2026-08-24 ~05:5x–0x:xx +07:00 (2026-08-23 22:5x–xx:xx UTC) — timestamp ในไฟล์นี้เป็น +07:00 เว้นแต่กำกับ
- **ล็อกรอบ:** ตรวจแล้วทั้งสอง repo ว่าง ⇒ จับล็อกด้วย draft PR #41 (pf_bridge) เปิดเป็น draft ตั้งแต่ก่อนเริ่มงาน (ยืนยัน `draft:true` จาก API หลังเปิด)

## Probe ต้นรอบ
- GitHub API/tool: ✅ อ่านรายการ PR ได้ทั้งสอง repo + เปิด draft PR ได้ (ใช้เป็นทางหลัก)
- ทาง D (`ci-status`): ✅ มีชีวิต — `git ls-tree origin/ci-status ci/` คืนรายการไฟล์ · d_exit=0
- โครงพี่น้อง: ✅ `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง
- 🔎 หมายเหตุสภาพแวดล้อม: clone ในอิมเมจรอบนี้ค้างมาจากยุค pf_bridge มี commit เดียว (fetch ขึ้น `forced update` เพราะ root commit เก่า `2accb96` ไม่อยู่ในประวัติ main ปัจจุบัน) — ไม่ใช่ force-push บน main จริง · แก้ด้วย fetch + checkout `origin/main` ก่อนเริ่มงานแล้ว ทุกอย่างอยู่บน main ล่าสุด

## กล่องจดหมาย
- ไม่มีจดหมายผู้เทสใบใหม่ (ทุกใบมีคู่ `.CONSUMED.txt` แล้ว — ตรวจด้วย stub-pairing ที่ตัดนามสกุล `.md` ก่อนต่อ `.CONSUMED.txt`)
- ⚠️ บันทึกกันพลาดให้รอบถัดไป: stub ตั้งชื่อแบบ `<ชื่อไฟล์ตัด .md>.CONSUMED.txt` — เช็คด้วย `<ชื่อไฟล์เต็ม>.CONSUMED.txt` จะเห็น "ค้าง 70+ ใบ" ปลอม ๆ (รอบนี้เกือบหลงบริโภคซ้ำทั้งกล่อง)

## งานรอบนี้ — ทำไมเลือกเลนนี้
- เลน attended: ⏸ พักตามคำสั่ง Panya 16:56 — ไม่แตะ · `GT-055`/`RE-056`/`RE-057`: งานหน้าสะพานล้วน — รอสะพาน
- `PF_VITAL_NAMES` 3 id + guard ฝาแฝด + rename external→clientbin: ติดรอคำตอบ Panya (คำถามค้าง R134/R135/R138)
- ⇒ milestone สำรองที่ปลดล็อกแล้วและยังไม่มีใครหยิบ: **inbound decoder `CLearnSkillVital 0x36AA`** —
  R138 จด nonclaim ไว้ตรง ๆ ว่า "inbound `CLearnSkillVital 0x36AA` ไม่ทำ" = ครึ่งที่เหลือของเลน learn-skill
  เข้าเกณฑ์ pre-approved ข้อ 3 (ฟังก์ชัน gameplay ใต้ pattern มาตรฐาน) + ข้อ 2 (headless = เส้นทางหลัก)
- ฐาน wire shape จาก artifact ที่ commit แล้วล้วน ๆ (ไม่ต้องใช้อิมเมจ):
  `pf_bridge/external/PF_SERIALIZER_FIELDS.tsv` 4 แถวของ `CLearnSkillVital` — W/R สมมาตร:
  `u32 tag 0x14 @+0x14` แล้ว `u8 tag 0x0B @+0x18` · gate ALWAYS · span `[0x00755AC0,0x00755B13)` len 83
  SHA `b99487413ffa79784deda46283aafc2f3954d98a85362d35304b745d6c062fc4` (ตรง pin GT-050 job 1 ที่ผ่าน
  re-derive ปฏิปักษ์บนสะพานแล้ว 2026-08-24 00:46)
- 🔴 nonclaim ตั้งต้น: **natural direction ของ 0x36AA ยังไม่ถูกพิสูจน์** (GT-050 พิสูจน์แค่ client มี W+R codec) —
  decoder ฝั่ง server ยืนบน "client เขียนเฟรมนี้ได้" ไม่ใช่ "client ส่งจริง" · จดลง `IMAGE_ACCESS_COST.tsv` แล้ว
  (แถว 2026-08-24T06:1x — งานพิสูจน์ direction เข้าเลนสะพานภายหลัง)

## แม่บ้าน (ทำแล้ว)
- `CHIEF_CONTINUATION.md` 99.3KB ชนเพดาน ~100KB ⇒ ย้ายบล็อกปิดแล้ว R108–R111 + แบนเนอร์ครั้งเดียว 2130
  ไป `archive/CHIEF_CONTINUATION_ARCHIVE_20260824_R108_R111.md` ทิ้ง pointer (ไฟล์เหลือ 45.3KB ·
  ผลรวม archive+ไฟล์ใหม่ = ต้นฉบับ+stub ไม่มีเนื้อหาย)

## สิ่งที่ทำ

### 1) LEARN-SKILL-REQUEST-001 / HYP-PF-034 — inbound strict decoder + opt-in dispatch (repo โค้ด)
- ลูกมือ Explore สำรวจ pattern บ้านก่อนเขียน (โมดูลแม่แบบ: `delete_actor.py` pure decoder ·
  `chat_input_hypothesis.py` classifier · `learn_skill_result_hypothesis.py` scenario gate)
- ไฟล์ใหม่ 3: `src/pirateforce_foundation/learn_skill_request_hypothesis.py` (strict decoder ของ body 7 ไบต์
  `u32 tag 0x14` + `u8 tag 0x0B` · encoder ฝั่งเทส decoder-inverse-checked · classifier envelope ·
  probe pins 3 ชุด ZERO/MID/MAX คำนวณสด) · `scenarios/learn_skill_request_hypothesis_decode_probe.json`
  (permission token · exact allowlist) · `tests/test_learn_skill_request_hypothesis.py` (41 เทส รวม dispatch จริง
  ผ่าน make_state_class + ASCII/cp874 guard)
- นโยบาย dispatch: **decode-count-and-record เท่านั้น** — ไม่ตอบ ไม่เขียน DB ไม่เรียก composer 0x673C
  (semantics ของ field ทั้งสองยัง opaque ⇒ การออกแบบ response = เดา จึงไม่ทำ) · ทุก refusal เป็น event ชื่อชัด
- governance: ตาม stop_rule ของ HYP-PF-033 ("inbound 0x36AA = new version หรือ entry ใหม่") ⇒ เปิด **entry ใหม่
  HYP-PF-034** (ledger 42 entries · canonical sha re-pin + lineage paragraph) · coverage `skill_use` เติม refs+notes ·
  `stats_and_progression` แก้ประโยค "inbound of all five unimplemented" ที่จะกลายเป็นเท็จ
- twin-guard (บทเรียน R138 D1): เติม triple `("learn_skill_request_hypothesis.py","CLearnSkillVital",1)`
  ทั้งฝั่ง tool และ test ใน commit เดียว · แก้ prose "inbound 0 for all five" ของ tool ·
  ขยาย context-restriction loop ของ test 24 ให้ resolve docstring ต่อไฟล์ (ของเดิมอ่าน owner ตายตัวไฟล์เดียว)
- grade digest ของ coverage re-pin ใน `test_foundation_legacy_seam.py` (ท่าเดียวกับที่ R138 ทำ) พร้อม
  paragraph ประวัติตาม convention
- ผลเทส: ชุดเต็ม **2017 passed / 324 skipped / 0 failed** เขียว(cloud sanity) · skip census PASS ·
  `verify_hypothesis_ledger` PASS (entries=42) · `verify_functional_coverage` PASS (8 open domains)

### 2) แม่บ้าน + คิว (repo เอกสาร)
- continuation archive (ดูหัวข้อ "แม่บ้าน" ด้านบน)
- 🆕 ใบ **RE-058 LEARNSKILL-DIRECTION-001** เข้า `CLIENT_RE_QUEUE.md` — direction census ของ 0x36AA บนสะพาน
  (ครึ่งหลักฐานที่ decoder ยังไม่มี · วิธีลอก GT-050 job 4 · ผลจะแก้สถานะ nonclaim ของ HYP-PF-034)

## adversary
- (กำลังรอ) pf-adversary ตรวจก่อน commit — ผลจะบันทึกท้ายรอบ

## คิวเทสเกม
- ✅ ตอบกฎข้อ ⑤: รอบนี้เพิ่มใบ **RE-058** ใน `CLIENT_RE_QUEUE.md` (งานสะพาน static) · **ไม่เพิ่มใบ attended ใหม่**
  เพราะเลน attended พักตามคำสั่ง Panya 16:56 และครึ่ง client-observable ของเลนสกิลมี GT-058 รออยู่แล้ว —
  ใบ attended ของ "client ยิง 0x36AA ตอนเรียนสกิลจริง" จะเปิดได้ก็ต่อเมื่อ RE-058 พิสูจน์ direction ก่อน
  (เปิดตอนนี้ = ใบที่ยืนบนสมมติฐานที่ยังไม่พิสูจน์)
