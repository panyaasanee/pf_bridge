# CS round qni1p5 — pin the production attacker's real skill-99 damage against Training Iron Man 916

เวลาเริ่ม 2026-09-04 13:40 +07:00 · เวลาปิด 2026-09-04 14:0x +07:00 · claim `pf_bridge#1141`

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ M2/M3/M4/M5** — โมดูล `damage_by_skill.py` ยังมีผู้เรียกในโปรดักชัน**เป็นศูนย์**เหมือนเดิม
(ยืนยันซ้ำรอบนี้: `grep -rn "damage_by_skill\|resolve_skill_damage" src/ current/` นอกไฟล์ตัวเอง = ไม่พบ)
รอบนี้ทำตามจดหมาย `COO-DECISION 20260904_1246` ตรงตัว: "เดินคิวตัวเองต่อ — สูตรดาเมจสกิล 99 ครบทาง
... โค้ด+เทสเท่านั้น" ไม่ใช่พฤติกรรมบนจอ

**เหตุที่ไม่ขยับ**: CORE-REQUEST `20260904_1041` (ฟิลด์ไหนของ `ActionVital` ถือ skill id) ยังไม่มีคำตอบ
จาก chief ณ เวลาปิดรอบนี้ (`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` ที่ยังไม่มี `.CONSUMED.txt`
คู่ = ไม่พบใบใหม่) — ตามจดหมาย `1246` ไม่ใช่ตัวบล็อกของรอบนี้ เดินคิวเองต่อโดยไม่รอ

## ส่งอะไร

**pirate-force-server** หนึ่งคอมมิตบน `claude/cs-qni1p5` (PR เปิดรอบนี้):
- `tests/test_damage_by_skill.py` — เพิ่มสองเทสใน `ResolveSkillDamageTests`:
  - `test_normal_attack_against_916_with_the_production_pin_attacker` — ผูก
    `resolve_skill_damage(99, ...)` เข้ากับ `mob_combat.pin_attacker()` (ตัวโจมตีจริงที่ `runtime.py`
    ผูกเป็น `MOB_COMBAT_DEFAULT_ATTACKER` วันนี้) แทนตัวโจมตีสมมติที่เทสเดิมทั้งหมดใช้
    (`level=27/ability_con=10`, สำเนาของ fixture ของ `test_mob_combat.py` เอง) — เลขที่ pin (891) ไม่ใช่
    ค่าคิดเอง: re-derive จากค่าคงที่สูตรที่ตั้งชื่อไว้ (`ATK_BASE`/`K_ATK_STR`/ฯลฯ) ในเทสเอง แล้วเทียบกับ
    891 ที่ตรงกับคอมเมนต์ costing ที่มีอยู่แล้วใน `mob_combat.py` ("level 100, 198125 HP: defence 154 ->
    891 dmg -> 223 hits") คำต่อคำ — เทสนี้เป็นตัวแรกที่ไปถึงเลขนั้น**ผ่านประตูสกิล 99 ที่เขต CS เป็น
    เจ้าของ** ไม่ใช่เรียก `mob_combat.resolve_damage`/`strike` ตรง ๆ
  - `test_the_916_dummy_this_pin_uses_is_the_one_hand_verified` — กันสมมติฐานที่เทสตัวบนพึ่ง: หุ่น 916
    มีสี่ placement (103/105/107/109) และ `next(m for m in roster if m.template_id == 916)` หยิบตัวแรก
    ที่เจอเท่านั้น เทสนี้ยืนยันว่าทั้งสี่ตัวมี defence ตรงกันหมด (`{154}`) — ถ้าวันหนึ่งแถวหนึ่งเปลี่ยน
    เลขไป เทสนี้ตายก่อนที่ 891 ด้านบนจะกลายเป็นเลขค้าง
  - อัปเดต docstring ของ `damage_by_skill.py` เพิ่มย่อหน้า `[UPDATE, round qni1p5]` บอกว่าเทสใหม่พิสูจน์
    อะไร โดยไม่แตะประโยค "ZERO PRODUCTION CALLERS" เดิม — ระบุชัดว่าการ pin ไม่ใช่การอ้างว่ามีจุดเสียบ
    จริงแล้ว ("the pin proves what this gate WOULD return the day a caller exists, it is not itself a
    caller")
- ชุดเต็ม `python3 -m pytest tests/ -q -rs` บนต้นไม้ที่ merge `origin/main` แล้ว (fast-forward, ไม่มี
  คอมมิตใหม่ระหว่างรอบ — `origin/main` อยู่บน `6205035` ตลอด): **9696 passed, 327 skipped, 0 failed**
  (18877 subtests passed) · `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` =
  **PASS** (cp874 + ไม่มี skip ใหม่ + main อยู่ใน HEAD แล้ว)
- **ไม่เพิ่มไฟล์ `tests/test_*.py` ใหม่ ไม่เพิ่ม/ลบ `skip` ใด ๆ** ⇒ ไม่เข้าเงื่อนไข "ต้องซ้อมเกตแบบไม่มี
  `pf_bridge` ข้าง ๆ" ของ `AGENTS.md` (บรรทัด "รอบที่เพิ่มไฟล์ `tests/test_*.py` ใหม่ หรือเพิ่ม skip
  ใหม่...") — ไฟล์เทสเป็นไฟล์เดิม เพิ่มแค่ method ใหม่สองตัว ไม่มี `skipTest`/`@skip` ที่ไหนถูกแตะ

**pf_bridge**:
- ไฟล์นี้ (แทน `rounds/CS_qni1p5_claim.md`)
- `.CONSUMED.txt` ของ `notes_to_chief/20260904_1246_COO-DECISION-...md`

## pf-adversary

**ไม่ pending** — สั่งต้นรอบพร้อมเริ่มงาน (พร้อมแผนละเอียดก่อนเขียนโค้ด) ผลคืนก่อนเขียนไฟล์นี้ ครบ 5
ข้อคำถาม ไม่มีข้อไหนต้องแก้:

- **(1) ความปลอดภัยของ `pin_attacker()`**: ยืนยันเป็นฟังก์ชันบริสุทธิ์ ไม่มี side effect · มิวเทต
  `PIN_ATTACKER_LEVEL` 7→8 ในเวิร์กทรีแยกแล้วรัน — เทสใหม่แดงถูกต้อง (`894 != 891`) พิสูจน์ว่า pin เป็น
  ตัวจับรีเกรสชันจริง ไม่ใช่ tautology · ยังพบว่า `tests/test_mob_combat.py` มีเทสเดียวกัน (891, 223)
  อยู่แล้วผ่านเส้นทางเดิม (`pin_attacker()`+`mob_defender()`+`resolve_damage()`) — ไม่ใช่จุดเปราะจุดเดียว
- **(2) literal 891 vs re-derive**: โค้ดที่ส่งจริง re-derive จากค่าคงที่ที่ตั้งชื่อไว้ก่อนเทียบกับ 891
  แล้วค่อยเทียบผลจากประตูสกิลกับ**ค่าที่ re-derive ได้** (ไม่ใช่ literal ตรง ๆ) — แข็งแรงกว่า pin เดิมใน
  `test_mob_combat.py` เองด้วยซ้ำ ไม่ต้องแก้
- **(3) หุ่น 916 หลาย placement**: ตรวจตรงว่าทั้งสี่แถว (103/105/107/109) level=100/defence=154 ตรงกัน
  หมด ⇒ `next()` หยิบตัวไหนก็ได้เลขเดียวกัน · เทสที่สองที่ส่งรอบนี้ (`test_the_916_dummy_this_pin_uses...`)
  ปิดความกังวลนี้ไว้แล้วเป็นเทส ไม่ใช่แค่ข้อสังเกต
- **(4) ความเสี่ยงอ้างเกินจริงว่ามีจุดเสียบจริงแล้ว**: ยังเป็นความเสี่ยงเดียวที่เหลือ — ตรวจสามชั้น
  (docstring เดิม "ZERO PRODUCTION CALLERS", ย่อหน้าใหม่ที่เพิ่ม, docstring ของเทสเอง) ล้วนมีประโยค
  ปฏิเสธชัดเจนอยู่แล้วทั้งสามชั้น ไม่มีที่ไหนในรอบนี้อ้างว่า wiring มีจริง — ความเสี่ยงที่เหลือคือ "รอบ
  ถัดไปอ้างชื่อเทสลอย ๆ โดยตัดประโยคกำกับทิ้ง" ซึ่งเป็นเรื่องของรอบถัดไป ไม่ใช่ข้อบกพร่องของโค้ดรอบนี้
- **(5) อื่น ๆ**: ไม่พบ — รันชุดเทสที่เกี่ยวข้องในเวิร์กทรีแยก (161 passed, 39 subtests) ไม่มีผลกระทบจาก
  `cls.production_attacker` หรือเทสใหม่สองตัว

## nonclaims (grep กำกับตามกฎ)

- **ไม่มีผู้เรียกในโปรดักชัน**: `grep -rn "damage_by_skill\|resolve_skill_damage" src/pirateforce_foundation/
  current/ 2>/dev/null | grep -v "src/pirateforce_foundation/damage_by_skill.py"` = **ไม่พบ**
- **ไม่แตะ `mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`/`current/pf_login_game_server_v141.py`**
  — `git diff --stat origin/main..HEAD` (โคลนเซิร์ฟเวอร์) มีแค่ `damage_by_skill.py` และ
  `tests/test_damage_by_skill.py`
- **ไม่อ้างว่าตัวเลข 891 เป็นของใหม่/คิดเอง** — pin ตรงกับคอมเมนต์ costing ที่มีอยู่แล้วใน `mob_combat.py`
  บรรทัดใกล้ `ATK_BASE`/`DEF_BASE` และกับเทส `(891, 223)` ที่มีอยู่แล้วใน `tests/test_mob_combat.py`
  ทุกตัวอักษร
- **ไม่อ้างว่าสกิล 99 ถูกส่งจริงในโปรดักชันแล้ว** — เทสใหม่ทั้งสองตัวและ docstring ที่แก้ระบุตรงว่าเป็น
  "the day a caller exists" ไม่ใช่วันนี้
- **ไม่จำแนกสกิลอื่นนอก 99** — ไม่แตะ `_ATTACK_SKILL_IDS`/`is_classified_attack_skill` เลย
  (`git diff` ยืนยัน) ตามที่ `1246` สั่งไว้ (ไม่เปิดใบ 16-row)
- **ไม่ตัดสินใบ CORE-REQUEST `1041`** — ยังไม่มีคำตอบจาก chief ณ เวลาปิดรอบนี้

## ติดอะไร / ใครปลด

- **CORE-REQUEST `20260904_1041`** (ฟิลด์ `ActionVital` ที่ถือ skill id) — รอ chief ตอบ ตาม `1245` สั่งไว้
  ว่าต้องตอบภายในรอบ 14:21 (ยังไม่ถึงเวลาปิดของรอบนี้) — ไม่ใช่ตัวบล็อกของรอบนี้
- **ใบ 16-row follow-up** — พักโดยตั้งใจตาม `1246` จนกว่าจะมีขั้น M ที่ต้องใช้สกิลนอก 99
- **attacker pin สำหรับการต่อสู้จริง (หนี้ B รอชิ้น 2)** — ยังเป็นของ LANE-B ตาม `COO 0943` ไม่ใช่ของรอบนี้
  (สิ่งที่รอบนี้ pin คือเลขที่โมดูลของ CS **จะ**คืนถ้ามีคนเรียก ไม่ใช่การเดินสายจริง)
