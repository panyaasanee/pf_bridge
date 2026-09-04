# CS round ltahoi — skill-id-gated damage module built (log-only), CORE-REQUEST sent, two adversary findings fixed

เวลาเริ่ม 2026-09-04 10:37 +07:00 · เวลาปิด 2026-09-04 10:51 +07:00 · claim `pf_bridge#1108`

## ขยับ NOW/M ข้อไหน

- `COO-DECISION 20260904_0943` ข้อ 2 เต็ม: ส่งโมดูล skill-id → damage ตัวแรกในเขต CS
  (`src/pirateforce_foundation/damage_by_skill.py` + `tests/test_damage_by_skill.py`)
  ครบสามเงื่อนไข (ก)/(ข)/(ค) — รายละเอียดหัวข้อ "ส่งอะไร" ข้างล่าง
- **ไม่ขยับ M2/M3/M4/M5** — โมดูลนี้ **ไม่มีผู้เรียกในโปรดักชันเลย** (log-only ตามเงื่อนไข (ค) ตรง ๆ) ยัง
  ไม่มีจุดอ่าน skill id จริงจากเฟรม `ActionVital` ห้ามใครอ่านว่า "ตี 916 ตามสกิล" ขยับจากรอบนี้

## ส่งอะไร

- **pirate-force-server** สอง commit บน `claude/pensive-bardeen-n8u5kr`:
  - `f68d0e1` — โมดูลตัวแรก: `damage_by_skill.py` (`resolve_skill_damage(skill_id, attacker, defender)`
    + `is_classified_attack_skill` + `DamageBySkillError`) กับ `test_damage_by_skill.py` (8 เทส)
  - `79f1ca1` — **แก้ตามข้อค้นพบของ pf-adversary รอบนี้** (D1/D2 ข้างล่าง) — เพิ่มเทส 2 ตัว
    (`test_resolve_skill_damage_actually_calls_the_imported_function`,
    `test_the_formula_constants_also_match_the_other_two_proven_copies`) + แก้ docstring ของโมดูลให้
    ตรงกับข้อเท็จจริงเรื่อง `action_ack.py`
  - รวม **10 เทสผ่าน** (`python3 -m pytest tests/test_damage_by_skill.py -v` = 10 passed)
- **pf_bridge**: ไฟล์นี้ (แทน `rounds/CS_ltahoi_claim.md`) · จดหมาย
  `notes_to_chief/20260904_1041_LANE-CS-CORE-REQUEST-which-actionvital-field-carries-skill-id.md`
  (แก้ตาม D2 แล้วก่อน push รอบเดียวกับที่ส่ง — ไม่มีเวอร์ชันผิดถูก push ขึ้น main มาก่อน เพราะโค้ดกับจดหมายอยู่ใน
  commit/PR เดียวกันที่ยังไม่ merge ตอนแก้) · consume จดหมายค้างสองใบ (`.CONSUMED.txt` วางแล้วพร้อม claim)

## ทำไมโมดูลนี้ถูกต้องตามสามเงื่อนไขของ `0943` ข้อ 2

- **(ก) ค่าคงที่ import จาก `mob_combat` ไม่คัดลอก**: `from .mob_combat import Combatant, resolve_damage`
  พิสูจน์ด้วยเทส identity (`is`, ไม่ใช่ equality) + เทสที่พิสูจน์ว่า `resolve_skill_damage` **เรียกผ่าน**
  ชื่อนั้นจริง (ไม่ใช่แค่ import แล้วไม่ใช้ — ดู D1 ข้างล่างว่าทำไมต้องมีเทสนี้แยกจาก identity) + เทส AST
  ว่าไฟล์นี้ไม่ประกาศ `ATK_BASE`/ฯลฯ เอง + เทสเทียบค่าตรงกับอีกสองสำเนาที่มีอยู่ (`damage_model_hypothesis`,
  `hostile_hp_link_hypothesis`) โดยตรง
- **(ข) เป็นฟังก์ชันจริงที่ B/chief เรียกได้**: `resolve_skill_damage` เป็นฟังก์ชันโมดูลระดับบนสุด ไม่ใช่ทูล
  headless-replay — พร้อมให้ import ทันทีที่มีจุดอ่าน skill id
- **(ค) log-only จนกว่าจะมีจุดอ่าน**: `grep -rn "damage_by_skill\|resolve_skill_damage" src/ current/` (ยกเว้น
  ไฟล์ตัวเอง) = **ไม่พบ** ยืนยันว่าไม่มีผู้เรียกจริง · docstring ของโมดูลเขียนตรง ๆ ว่าเป็น log-only · CORE-REQUEST
  ส่งรอบเดียวกัน (`notes_to_chief/20260904_1041_...md`)

## ทำไมเฉพาะสกิล 99 ที่ถูกจัดว่าเป็น attack

สกิล 99 ("Normal Attack") เป็นสกิลเดียวใน 8 ตัวที่ชื่อจากไคลเอนต์เองไม่กำกวมว่าเป็นการโจมตี — 110/111 คือ
"Strive Jump"/"VIP Strive Jump" (ท่ากระโดด ไม่ใช่โจมตี) ส่วนกลุ่ม 40000 คือ "<Class> Basic Training" ที่
`skill_catalog.py` เองพิสูจน์แล้ว (รอบ `6o11t1`) ว่าใช้ `n_PASSIVE` แยกไม่ได้ และตารางเดียวที่แยกได้จริง
(`s_CAST_CONDITION`/`s_CAST_BEHAVIOR`) ยังเป็น `RE-232` ที่ **OPEN** อยู่ (`grep -n "RE-232" CLIENT_RE_QUEUE.md`
= `[OPEN -- [STATIC-ON-BRIDGE]]`) — อีก 7 ตัวถูกปฏิเสธโดยระบุชื่อ ไม่ใช่เดาไปทางใดทางหนึ่ง

## pf-adversary

**ไม่ pending** — สั่งต้นรอบพร้อมเริ่มงาน ผลคืนก่อนเขียนไฟล์นี้ ครบ 5 ข้อ แก้แล้ว 2 ข้อจริง อีก 3 ข้อพิจารณาแล้ว
ไม่ต้องแก้เพิ่ม (เหตุผลด้านล่าง):

- **D0 (กระบวนการ)**: adversary ตั้งข้อสังเกตว่าโค้ดถูก commit ก่อนผลของมันจะคืน — **นี่คือกติกาที่ถูกต้องแล้ว**
  ตาม `AGENTS.md` §7: "`pf-adversary` สั่งต้นรอบ**พร้อมเริ่มงาน** ไม่ใช่ก่อน commit" ไม่ใช่ข้อบกพร่อง ไม่แก้
- **D1 (แก้แล้ว, severity สูง, พิสูจน์ด้วย mutation จริง)**: ชุดเทสเดิมพิสูจน์แค่ identity ของชื่อที่ import
  ไม่พิสูจน์ว่า `resolve_skill_damage` **เรียกผ่าน** ชื่อนั้นจริง — adversary แก้โค้ดชั่วคราวให้ inline
  เลขคงที่แทนการเรียก `resolve_damage` (สูตรสำเนาที่สี่ที่เงื่อนไข (ก) ห้าม) แล้วรัน
  `pytest tests/test_damage_by_skill.py` = **ผ่านทั้ง 8 ตัวเดิมโดยไม่รู้ตัว** ⇒ เพิ่มเทสที่ mock
  `damage_by_skill.resolve_damage` คืนค่า sentinel แล้วเช็คว่า `resolve_skill_damage` คืน sentinel นั้น —
  ทดสอบซ้ำด้วย mutation เดียวกันของ adversary เอง (คัดลอกสคริปต์มาเทียบเอง) = **เทสใหม่แดงตามที่ควร** ก่อนแก้กลับ
  เป็นโค้ดจริง (`AssertionError: Expected 'resolve_damage' to be called once. Called 0 times.`)
- **D2 (แก้แล้ว, severity สูง, ข้อเท็จจริงผิดจริง)**: docstring ของโมดูลกับร่างแรกของ CORE-REQUEST เขียนว่า
  ห้าฟิลด์นั้น "ไม่มีผู้เรียกไหนใน `action_ack.py`/`mob_combat.py` อ่านเลย" — **ผิดสำหรับ `action_ack.py`**
  ตรวจเองซ้ำ: `action_ack.parse_scene006_ea7d` (บรรทัด 60-71) และ `make_scene007_action_ack` (บรรทัด 90-103)
  อ่านและเช็คทั้งห้าฟิลด์แบบ strict equality จริง (คนละเส้นทางกับการตีมอน — SCENE-006/007 relocation ack ที่
  ผูกจาก `scene_load.py:173` `SceneActionAck(0xEA7D, 0x203D, 1)`) แก้ทั้ง docstring และจดหมายแล้ว พร้อม
  ประกาศความเสี่ยงชนกัน (ถ้าคำตอบคือ `field_u16_4a` ต้องมีคนตัดสินว่าเกต `==1` ของ action_ack กับความเงียบของ
  mob_combat อันไหนผิด — ไม่ใช่ผมเพราะทั้งสองไฟล์อยู่นอกเขต CS)
- **D3 (พิจารณาแล้ว, severity ปานกลาง, แก้เพิ่มเพื่อให้ตรงตัวอักษร)**: เงื่อนไข (ก) พูดถึง "เทสกันเหลื่อมกับสาม
  สำเนาเดิม" ตามตัวอักษรชุดเทสเดิมพิสูจน์แค่ identity กับ `mob_combat` (ถูกต้องโดย transitivity แต่ไม่ตรงตัวอักษร)
  ⇒ เพิ่มเทสเทียบค่าตรงกับ `damage_model_hypothesis`/`hostile_hp_link_hypothesis` โดยตรง (ซ้ำกับเทสของ
  `test_mob_combat.py` แต่ไฟล์นี้ไม่ควรพึ่งไฟล์อื่นให้รอด)
- **D4 (ไม่ต้องแก้)**: ไฟล์รอบยังไม่มีตอนที่ adversary ตรวจ — ไฟล์นี้เองคือคำตอบ

## nonclaims (grep กำกับตามกฎ)

- **ไม่มีผู้เรียกในโปรดักชัน**: `grep -rn "damage_by_skill\|resolve_skill_damage" src/pirateforce_foundation/
  current/ 2>/dev/null | grep -v "src/pirateforce_foundation/damage_by_skill.py"` = **ไม่พบ** (รันจริงรอบนี้
  หลัง commit สุดท้าย)
- **ไม่แตะ `mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`/`action_ack.py`/
  `current/pf_login_game_server_v141.py`** — `git diff --stat f68d0e1^..79f1ca1` (สอง commit ของรอบนี้) =
  มีแค่ `src/pirateforce_foundation/damage_by_skill.py` และ `tests/test_damage_by_skill.py`
- **ไม่ได้ถอด `s_CAST_CONDITION`/`s_CAST_BEHAVIOR`** — รอ `RE-232` (OPEN, เจ้าของ chief)
- **ไม่อ้างว่า "ผู้เล่นตี 916 ตามสกิลที่กด แล้ว HP ลดบนจอ" มีใบ GT PASS** — ไม่มีใบ GT เปิดรอบนี้ (โมดูลไม่มี
  ผู้เรียก จึงไม่มีอะไรให้เทสบนจอ) `grep -n "916\|Training Iron Man" GAME_TEST_QUEUE.md` ยังตอบเหมือนรอบ
  `go74te` (ไม่มีใบไหนปิด PASS เรื่องนี้ตรง ๆ)
- **ไม่อ้างว่าค่าคงที่ตัวไหนใน `damage_by_skill.py` เป็นของใหม่** — ทุกตัวเป็นชื่อที่ import มา ไม่มีการประกาศ
  ค่าคงที่เองเลยสักตัว (เทส AST ยืนยัน)

## ติดอะไร / ใครปลด

**ไม่ติดจุดเสียบใหม่** — CORE-REQUEST ที่ส่งรอบนี้ (`notes_to_chief/20260904_1041_...md`) รอ chief ตอบว่าฟิลด์
ไหนของ `ActionVital` ถือ skill id (ถ้ามี) ก่อนโมดูลนี้จะมีผู้เรียกจริง ไม่ใช่ตัวบล็อกของรอบนี้ — โมดูลรอบนี้
ทำงานถูกตามเทสที่มีแล้วโดยไม่ต้องรอคำตอบ
