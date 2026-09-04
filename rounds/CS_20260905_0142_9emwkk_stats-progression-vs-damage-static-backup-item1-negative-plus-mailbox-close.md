# CS round 9emwkk — งานสำรองข้อ 1 (`stats_progression_hypothesis.py` เทียบ `pf_damage_hit_result_static.py`) ปิดผลลบ + ปิดกล่องจดหมาย 2 ใบ

เวลาเริ่ม 2026-09-05 01:42 +07:00 · claim `pf_bridge` PR #1238 (หัว `[LANE-CS] round 9emwkk: claim` เดิม ทับด้วยไฟล์นี้)

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]`

`pirate-force-server` open: #778 (`[LANE-DB]`) — ไม่มี `[LANE-CS]` · `pf_bridge` open: #1235/#1236/#1237
(`[LANE-GM]`/`[LANE-A]`/`[LANE-B]`) — ไม่มี `[LANE-CS]` ⇒ ไม่ถอย เปิด claim ได้ตามปกติ

## ขั้นตอน 2 — `ADVERSARY_PENDING`

ไม่มีค้างจากรอบก่อน (`h4mxrq` ปิด `#768` เต็มในรอบนั้นเอง ยืนยันจากจดหมาย `0013`/`0030`/`0043` — ไม่มี
`ADVERSARY_PENDING` เปิดค้างสำหรับ CS ตอนนี้)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` (ข้าม `.CONSUMED.txt`) เจอ 2 ใบใหม่นับจากรอบ `h4mxrq`
(00:17) ทั้งคู่มาหลังรอบนั้นปิด:

1. `20260905_0030_CHIEF-TO-LANE-CS-hypothesis-ledger-bump-answer-v002.md` — chief ตอบคำถามที่ CS ถามซ้ำเรื่อง
   วิธี bump `docs/HYPOTHESIS_LEDGER.json` (entry `HYP-PF-033`) พร้อมยืนยันว่า **chief แก้ไฟล์เองแล้ว** (ไม่ใช่
   ของ CS แตะ): `exact_value_or_transform`/`accepted_ceiling`/`stop_rule`/`expiry` แก้เป็นหกเฟรม +
   `tools/verify_hypothesis_ledger.py` re-pin sha256 ใหม่ · รันแล้วเขียว `PASS entries=50` · ตรวจซ้ำเองรอบนี้:
   `grep -n "SIX pinned frames\|LEARN-SKILL-RESULT-002" docs/HYPOTHESIS_LEDGER.json` เจอจริงตามที่ chief อ้าง
   (`SIXTH pinned frame`, `tracked_versions` มี `LEARN-SKILL-RESULT-002`) · `python3
   tools/verify_hypothesis_ledger.py` รันซ้ำเองรอบนี้ → `HYPOTHESIS_LEDGER PASS entries=50` ยืนยันตรง ⇒ ปิด
   ด้วย `.CONSUMED.txt` ไม่มีงานเหลือให้ CS
2. `20260905_0043_COO-DECISION-cs-marker-debt-accepted-1346-stays-chief-letter-gt249-body-is-chief-work-LANE-CS.md`
   — COO ตัดสิน 6 ข้อรับหมดจากใบ `0013` ของ CS (marker 10 ใบรับ · `1346` ไม่ใช่ของ CS ยืนตามเดิม · `GT-249`
   หนี้ CS จ่ายแล้ว รอ chief คัดลอกร่างเข้าคิว · งานสำรอง `plg1ne` ข้อ 2/3 ปิดผลลบรับ · งานสำรองใหม่ 3 ข้อ
   อนุมัติ · สั่งให้ CS หยิบงานสำรองข้อ 1 รอบ 01:06) ⇒ ปิดด้วย `.CONSUMED.txt` ไม่มีคำสั่งใหม่ให้ทำเพิ่ม

ไม่มีใบไหนอยู่ในเนื้อ (`head -3`) นอกจากสองใบนี้ที่จ่าหน้าจริงถึง LANE-CS

## งานที่ทำ — งานสำรองข้อ 1 (COO อนุมัติใน `0043`): อ่าน `stats_progression_hypothesis.py` เทียบ `pf_damage_hit_result_static.py`

อ่านทั้งสองไฟล์จบทั้งไฟล์ (`stats_progression_hypothesis.py` 2,681 บรรทัด · `pf_damage_hit_result_static.py`
1,220 บรรทัด) หาว่ามีตารางดาเมจที่ยัง hardcode/ซ้ำอยู่ในไฟล์แรกที่ควรอ่านจากตารางจริงในไฟล์ที่สอง (ตามพรอมป์
"สูตรดาเมจ...ยกระดับจาก hypothesis เป็นโค้ดที่ทำงานจริง") **ผลลบ**:

- `pf_damage_hit_result_static.py` เป็นตัวพิสูจน์รูปแบบไบต์จากไบนารีที่พินไว้ (byte-exact guard) ไม่ใช่แหล่งตาราง
  ตัวเลข — ข้อสรุปหลักของมันคือ **ไคลเอนต์ไม่คำนวณสูตรดาเมจเลย** (`CHitResult`/`CMissileHitResult` 0x16F7:
  ดาเมจที่ `+0x08` เป็นค่าที่เซิร์ฟเวอร์ส่งมาตรง ๆ พิมพ์ด้วย `abs()`+`"%d"` ไม่มี scale/clamp/lookup) ⇒ **ไม่มี
  ตารางตัวเลขดาเมจต่อคลาส/เลเวลให้อ้างอิงเลย เพราะไม่มีอยู่ในไคลเอนต์จริง** (พิสูจน์ระดับไบต์แล้ว)
- ตัวเลขใน `stats_progression_hypothesis.py` (STR/CON/DEX/INT/PER, XP, HP/MP, death timer ฯลฯ) เป็นค่าทดสอบ
  ที่ประกาศตรงตัวว่าเป็น attended-test fixture (`STATS_PROGRESSION_ABILITY_STR = 11` ฯลฯ) ไม่ใช่ค่าจริงจาก
  gamedata ⇒ ไม่มีอะไรให้ derive จากตารางจริงแทนค่าคงที่พวกนี้ (โมดูลบอกตรง ๆ บรรทัด 164: "the curve numbers
  are not even in the client executable")
- ยืนยัน `stats_progression_hypothesis.py`/`damage_model_hypothesis.py`/`damage_hp_link_hypothesis.py` **ไม่ใช่
  zero-caller** ทั้งสามตัว — มี dispatch caller จริงใน `runtime.py` (`_dispatch_stats_progression_hypothesis`
  บรรทัด 2622 · `_dispatch_damage_model_hypothesis` บรรทัด 3264 · `_dispatch_damage_hp_link_hypothesis` บรรทัด
  3367 เรียกจาก 7590/7621/7631 — grep ยืนยันเองรอบนี้) แต่ทุกตัวอยู่หลัง `production_allowed = False` (grep
  ยืนยัน: `stats_progression_hypothesis.py:1119,2463` `damage_model_hypothesis.py:130,1399`
  `damage_hp_link_hypothesis.py:95,1623`) ⇒ ถูกกันไว้ตามออกแบบ รอผลจับภาพ attended ไม่ใช่บั๊ก
- **สิ่งที่ไม่เกี่ยวกับดาเมจแต่เจอระหว่างอ่าน (บันทึกไว้ ไม่ใช่ของ CS แก้)**: docstring ของ
  `stats_progression_hypothesis.py` บรรทัด 42 อ้างว่า XP bar ของไคลเอนต์หารด้วย
  `STANDARD_STATUS[level+1].n_EXP_CURRENTLV` แต่โมดูลไม่เคย import `persistence_standard_status.py` จริง (grep
  ยืนยันรอบนี้: `persistence_standard_status` มีแค่ `tests/test_persistence_standard_status.py` อ้างถึง ไม่มี
  โมดูล production ไหน import) — เป็นเรื่อง XP-bar/ตารางสถานะที่ `NOW.md` บรรทัด 35 บันทึกไว้แล้วว่าเป็นของ
  LANE-DB (`STANDARD_STATUS` ต่อเลเวล ยังไม่มีกำหนดเพราะ `s_SCORE` ไม่เคย RE) **ไม่ใช่ช่องว่างสูตรดาเมจ** จึงไม่
  เปิดใบ/จดหมายใหม่ข้ามเขต

**สรุป**: งานสำรองข้อ 1 ปิดผลลบเหมือนงานสำรองก่อนหน้า (`skill_attr_hypothesis.py` ในรอบ `h4mxrq`) — ทั้งสาม
โมดูลดาเมจของ CS สมบูรณ์ในตัวเองแล้ว ไม่มีตารางให้ upgrade ทางสถิต เพราะไม่มีสูตรอยู่ในไคลเอนต์ให้ค้นต่อ
(พิสูจน์ไบต์แล้ว) ทางเดียวที่เหลือของ M ladder ข้อ 3 (สูตรดาเมจ) คือรอผล attended capture (`GT-243`/`GT-249`)
เหมือนที่ระบุไว้ทุกรอบก่อนหน้า

**เทส**: ไม่มีโค้ดเปลี่ยนรอบนี้ (`git status`/`git diff` ว่างตลอดรอบใน `pirate-force-server`) ⇒ ไม่รันชุดเต็ม
ใหม่ ไม่มีอะไรให้พิสูจน์ว่าไม่พัง

## pf-adversary

**ไม่สั่งรอบนี้** — ตรงข้อยกเว้นของ `COO-DECISION 20260904_1428` ข้อ 2 (รอบที่แก้ถ้อยคำ/อ่านอย่างเดียว = ไม่สั่ง)
ไม่มีโค้ด/เทสเปลี่ยนในต้นไม้ `pirate-force-server` และการเปลี่ยนใน `pf_bridge` มีแต่ไฟล์รอบ/จดหมาย/marker

## งานสำรอง (ทำเมื่องานหลักติด) — เติมให้ครบ 3 ข้อเสมอ

1. อ่าน `docs/HYPOTHESIS_LEDGER.json` entries ที่ผูกกับโมดูลของ CS (`skill_attr`/`learn_skill_result`/
   `learn_skill_request`/`stats_progression`/`damage_model`/`damage_hp_link`) เทียบ `stop_rule`/
   `accepted_ceiling` แต่ละอันกับโค้ดจริงบน `main` ปัจจุบันทีละตัว (ไม่ใช่แค่ตัวที่ `#768` แตะ) หา staleness
   แบบเดียวกับที่เจอใน `HYP-PF-033` ก่อนที่ adversary จะต้องมาเจอเอง — ไฟล์: `docs/HYPOTHESIS_LEDGER.json` +
   โมดูลที่เกี่ยวข้องแต่ละตัว · หลักฐานผ่าน: ตรวจครบทุก entry ที่ CS เป็นเจ้าของ (grep เจ้าของ/ชื่อโมดูล) แล้ว
   รายงานผลลบ/พบ ในไฟล์รอบ
2. เมื่อ RE-240 attended capture (กด skill 99 จาก hotbar + control กด Z, `GT-243`) ได้ผล — เตรียม caller จริง
   ของ `resolve_skill_damage` ตามฟิลด์ที่ผลชี้ (ยังทำไม่ได้ล่วงหน้า แต่ต้องอ่าน diff ทันทีที่ผลถึง อยู่ในคิวหลัก
   ไม่ใช่คิวสำรองจริง — คงข้อนี้ไว้ตามที่ `0013`/`0043` ระบุ)
3. ทบทวน `persistence_class_id.py` + `persistence_starting_skills.py` คู่กันตอนถึงคิวเริ่มต้นข้อ 5 (ระบบเรียน
   สกิล/skill point) — ยังไม่ถึงคิวนี้จนกว่าข้อ 1-4 ของคิวเริ่มต้นเดินหน้าได้มากกว่านี้

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ** — รอบนี้ไม่มีโค้ด/เทสใหม่ในต้นไม้ `pirate-force-server` เลย งานหลักของ CS ที่ขยับ M ได้จริง (ผูก
`resolve_skill_damage`/`damage_by_skill.py` เข้าฟิลด์ skill id จริงจากผล attended) ยังติดผลจับภาพของ
`GT-243`/`GT-249` (รอเครื่อง Panya) เหมือนเดิม — ไม่นับเป็น "รอบว่าง" ตาม `1450` เพราะหยิบงานสำรองข้อ 1 ทำจริง
ในรอบเดียวกัน (ผลลบมีหลักฐาน grep กำกับทุกข้อข้างบน)

## ส่งอะไร

**pirate-force-server**: ไม่มีการเปลี่ยนแปลง — ไม่เปิด PR ใหม่

**pf_bridge**: PR #1238 (แทน `rounds/CS_9emwkk_claim.md` ด้วยไฟล์นี้), เพิ่ม:
- `.CONSUMED.txt` ของ `20260905_0030_CHIEF-TO-LANE-CS-hypothesis-ledger-bump-answer-v002.md`
- `.CONSUMED.txt` ของ `20260905_0043_COO-DECISION-cs-marker-debt-accepted-1346-stays-chief-letter-gt249-body-is-chief-work-LANE-CS.md`

## nonclaims

- ไม่อ้างว่าสูตรดาเมจจริงถูกเขียนแล้ว — ยังไม่มี ยังรอ attended capture
- ไม่อ้างว่า `persistence_standard_status.py` เป็นบั๊กของ CS — เป็นของ LANE-DB (`NOW.md` บรรทัด 35 บันทึกแล้ว)
  บันทึกไว้เผื่อ DB ต้องการอ้างอิง ไม่เปิดใบข้ามเขต
- ไม่อ้างว่า `1346` ถูกปิด — ยังเปิดอยู่ ไม่ใช่ของ CS (ยืนตามรอบก่อน)
- ไม่อ้างว่างานสำรองข้อ 1 ใหม่ (ledger staleness sweep) เจออะไร — ยังไม่ได้ทำ แค่ตั้งคิว

## ติดอะไร / ใครปลด

- **งานหลัก CS (skill id → damage caller จริง)** — ติดผลจับภาพ attended `GT-243`/`GT-249` (รอเครื่อง Panya)
  ไม่มีอะไรใหม่ให้รายงาน

-- LANE-CS
