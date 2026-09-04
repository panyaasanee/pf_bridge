# CS round kd06fo — name the n_CD/n_STAMINA_COST readers on the starting-kit skill catalog

เวลาเริ่ม 2026-09-04 15:18 +07:00 · เวลาปิด 2026-09-04 15:5x +07:00 · claim `pf_bridge#1158`

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ M2/M3/M4/M5** — รอบนี้เป็น**งานสำรอง** ของ LANE-CS ตามคิวเริ่มต้นข้อ 1 ("สารบัญอาชีพและ
สกิลจากตารางจริง ... ค่า MP/CD/ระยะ") ไม่ใช่งานหลักบนจอ

**เหตุที่ไม่ทำงานหลักรอบนี้**: งานหลัก (ผูก `resolve_skill_damage`/`damage_by_skill.py` เข้ากับฟิลด์
`ActionVital` ที่ถือ skill id จริง) ยังบล็อกที่ `RE-240` — จดหมาย `20260904_1405` (chief) ตอบ
CORE-REQUEST `1041` ว่า **ไม่ใช่ห้าฟิลด์ที่เสนอสักตัว** และเปิด `RE-240` ให้แล้ว (ยังไม่มีผลตอนปิดรอบนี้)
พร้อมสั่งชัดเจนว่า **ห้ามเสียบผู้เรียกกับ `action_u32_30`** เพราะฟิลด์นั้นมีเจ้าของแล้ว (behavior lookup
ท่าโจมตี) — เสียบทับจะทำท่าโจมตีพัง รอบนี้จึงไม่แตะ `damage_by_skill.py`/`mob_combat.py` เลย

ตาม `PANYA-DECISION 1450` (14:55, "รอบว่างไม่มีอีกแล้ว — งานหลักติด = หยิบงานสำรองข้อ 1 ในรอบเดียวกัน")
รอบนี้หยิบงานสำรองข้อ 1 ของ LANE-CS: `skill_catalog.py` มีค่า `n_CD`/`n_STAMINA_COST` อยู่ใน
`skill_raw_context()` มาตั้งแต่รอบ `iazmrv` (04:53) แต่ไม่เคยมีชื่ออ่านเฉพาะแบบ `level_learn()` — ปิดช่อง
ว่างนั้น ยังอยู่ในเขตของ CS เต็ม ๆ ไม่ต้องรอ chief/RE-240

## งานสำรอง 3 ข้อของ LANE-CS (ตาม `1450` ข้อ 6 — เริ่มได้ทันทีไม่รอใคร เรียงตามบันได M)

1. **(ทำรอบนี้)** เติมชื่ออ่านให้ค่าที่ `skill_raw_context()` มีอยู่แล้วแต่ยังไม่มีฟังก์ชันเฉพาะ
   (`n_CD`/`n_STAMINA_COST` เสร็จแล้ว — เหลือ `n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND`/`n_ISCLASS` ถ้ามีเหตุผล
   ใช้จริงในรอบถัดไป ไม่ใช่ครบทุกคอลัมน์เพื่อครบ)
2. เพิ่มเทสเปรียบเทียบ `resolve_damage`/`damage_by_skill.resolve_skill_damage` กับตัวเลขจาก
   `pf_damage_hit_result_static.py`/รายงาน static เพิ่มอีกฉาก (นอกเหนือ 916) **ถ้า**พบตัวเลข static
   ที่คอมมิตแล้วที่ยังไม่ถูกเทียบ — ยังไม่ค้นในรอบนี้ ต้องหาก่อนว่ามีจริงไหม
3. อ่าน `stats_progression_hypothesis.py`/`tools/pf_stats_progression_static.py` (โมดูลที่โอนมาให้ CS
   ตาม `CHIEF_CONTINUATION.md` `0330` ข้อ 1) หาช่องว่างแบบเดียวกับข้อ 1 (ค่าที่มีอยู่แล้วแต่ไม่มีชื่ออ่าน)
   — ยังไม่เริ่มอ่านรอบนี้

## ส่งอะไร

**pirate-force-server** หนึ่งคอมมิตบน `claude/inspiring-albattani-kd06fo` (`db672c1`, merge `origin/main`
`3932307` แล้ว, ไม่มีคอนฟลิกต์), PR `#741`:

- `src/pirateforce_foundation/skill_catalog.py`:
  - `cooldown_seconds(skill_id) -> int` อ่าน `n_CD`
  - `stamina_cost(skill_id) -> int` อ่าน `n_STAMINA_COST`
  - ทั้งสองเลียนแบบรูปแบบของ `level_learn()` เป๊ะ (`skill_raw_context()` + `int()` คอลัมน์เดียว) — ไม่มี
    ผู้เรียกในโปรดักชัน เหมือน `level_learn()` เดิม (catalog ตอบคำถาม ไม่ใช่ gate)
  - เพิ่มย่อหน้า `[UPDATE, this round]` ในดอกสตริงโมดูล อธิบายว่าเพิ่มอะไร และทำไม `n_TARGET` **ไม่ได้**
    accessor ใหม่ (ไม่มีใครถอดหน่วย/ทิศทางของคอลัมน์นั้น — ให้ accessor จะเป็นการประดิษฐ์ความหมาย
    แบบเดียวกับที่ส่วน "RAW FIELDS, NOT INVENTED TYPES" เตือนไว้เรื่อง `n_PASSIVE`)
- `tests/test_skill_catalog.py`:
  - `test_cooldown_seconds_matches_the_raw_column_per_skill` / `test_stamina_cost_matches_the_raw_column_per_skill`
    — pin ค่าจริงต่อสกิลทั้ง 8 ตัว (99: CD=25/stamina=0 · 110: CD=1/stamina=22 · 111: CD=1/stamina=0 ·
    ห้า Basic Training: CD=0/stamina=0 ทั้งหมด) เทียบกับทั้งค่าคงที่และค่าจาก `skill_raw_context()` ตรง
  - `test_no_accessor_exists_for_n_target_yet` — **เขียนใหม่หลัง pf-adversary จับได้** (ดูหัวข้อ adversary)
    จากเช็คชื่อฟังก์ชันสี่ชื่อที่เดาไว้ เป็นเดิน AST หาสตริง `"n_TARGET"` ทั้งไฟล์ ต้องเจอครั้งเดียวเท่านั้น
    (ใน `_CONTEXT_COLUMNS`)

**pf_bridge**:
- ไฟล์นี้ (แทน `rounds/CS_kd06fo_claim.md`)
- `.CONSUMED.txt` ของ `notes_to_chief/20260904_1405_CHIEF-TO-LANE-CS-answer-1041-none-of-the-five-fields-re240-opened.md`

## pf-adversary

**ไม่ pending** — สั่งก่อนเริ่มเขียนโค้ด ผลคืนก่อน push ครบ พบ 1 จุดจริง แก้แล้ว:

- **(1) ค่าที่ pin ตรงกับตารางจริงไหม**: อ่าน `data/skill_context_starting_kit.tsv` เองแยกจากรายงานของ
  ผม (คอลัมน์ 14=`n_CD`, 18=`n_STAMINA_COST`) — ตรงกับทุกค่าที่เทสยืนยัน ไม่มี pin ค้าง
- **(2) ดอกสตริงอ้างเกินความหมายของคอลัมน์ไหม**: ไม่พบ — `stamina_cost()` ปฏิเสธคำว่า "MP" ชัดเจน
  `cooldown_seconds()` กำกับว่าคำต่อท้าย `_seconds` เป็นการเดาแค่ "หน่วย" ไม่ใช่ "คอลัมน์นี้วัดอะไร"
  (ข้อสังเกตอ่อน ไม่ใช่ข้อบกพร่อง: `n_CD=25` ของสกิล 99 "Normal Attack" เป็นค่าที่แปลกถ้าอ่านเป็น
  cooldown 25 วินาทีของการตีธรรมดา เทียบกับ 1 ของสกิลเดิน — ไม่ได้ทำให้คำกำกับเท็จ แต่เป็นเหตุผลที่
  ผู้เรียกในอนาคตไม่ควรเชื่อชื่อฟังก์ชันเฉย ๆ โดยไม่อ่านดอกสตริง)
- **(3) ชนกับเทสเดิม/ชื่อชนกันไหม**: ไม่พบ — `grep` ทั้งรีโปหา `cooldown_seconds|stamina_cost` ไม่มี
  จุดเรียกนอกสองไฟล์นี้ · `test_raw_context_exposes_no_invented_type_field` เช็ค **คีย์ของ dict** ไม่ใช่
  ชื่อฟังก์ชัน จึงชนกันไม่ได้ · รันคู่กับ `test_class_catalog.py` ผ่านหมด ไม่กระทบกัน · รัน bridge-gated
  drift test จริงด้วย `pf_bridge/gamedata` สด (ไม่ skip) = ผ่าน 16/16
- **(4) `test_no_accessor_exists_for_n_target_yet` เป็นยามจริงหรือหลอก**: **พบจริง** — เช็คแค่
  `hasattr` สี่ชื่อที่เดาไว้ (`target`/`target_field`/`range`/`target_mode`) มิวเทชันเพิ่มฟังก์ชันชื่อ
  `target_type(skill_id)` อ่าน `n_TARGET` ตรง ๆ หลุดผ่านเทสเดิมแบบเงียบ ๆ — **แก้แล้ว**: เปลี่ยนเป็นเดิน
  AST หาสตริง `"n_TARGET"` ทั้งโมดูล ต้องเจอครั้งเดียว ยืนยันด้วยมิวเทชันเดิมซ้ำ (ฟังก์ชันปลอมทำเทสแดง)
  และมิวเทชันบวก (สลับ `n_CD`→`n_STAMINA_COST` ในฟังก์ชันจริงทำเทส pin แดงเช่นกัน ไม่ใช่ tautology)
- **(5) ขอบเขตเลน**: `git diff --name-only` มีแค่ `skill_catalog.py`/`test_skill_catalog.py` ไม่แตะ
  `mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`/`current/pf_login_game_server_v141.py`

## nonclaims (grep กำกับตามกฎ)

- **ไม่มีผู้เรียกในโปรดักชัน**: `grep -rn "cooldown_seconds\|stamina_cost" src/ current/ 2>/dev/null |
  grep -v "src/pirateforce_foundation/skill_catalog.py\|tests/"` = ไม่พบ
- **ไม่แตะ `damage_by_skill.py`/`mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`/
  `current/pf_login_game_server_v141.py`** — `git diff --stat origin/main..HEAD` มีแค่สองไฟล์ข้างต้น
- **ไม่อ้างความหมายของ `n_CD`/`n_STAMINA_COST` เกินกว่าที่ตารางให้**: `stamina_cost()` ไม่เรียกว่า MP,
  `cooldown_seconds()` กำกับหน่วยเป็นการเดาในดอกสตริง ไม่ใช่ข้อเท็จจริงที่พิสูจน์แล้ว
  ไม่มี accessor ให้ `n_TARGET` (ไม่มีการ RE หน่วย/ทิศทาง)
- **ไม่ตัดสินใบ CORE-REQUEST `1041`/`RE-240`** — ยังไม่มีผลจาก chief ณ เวลาปิดรอบนี้ ไม่ใช่ตัวบล็อก
  ของรอบนี้ (งานสำรอง ไม่ใช่งานหลัก)
- **ไม่เปิดใบ 16-row taxonomy** — ยังพักตาม `COO-DECISION 1246`

## ติดอะไร / ใครปลด

- **`RE-240`** (chief เปิด, letter `1405`) — ยังไม่มีผล ไม่ใช่ตัวบล็อกของรอบนี้ (งานสำรองเดินได้โดยไม่รอ)
  รอบถัดไปของ LANE-CS เปิดด้วยการเช็คว่ามีผลหรือยัง
- **attacker pin สำหรับการต่อสู้จริง** — ยังเป็นหนี้ของ LANE-B รอชิ้น 2 ของ DB (`COO 0943`) ไม่เปลี่ยน
- **`n_TARGET`** — ไม่มีใครถอดความหมาย ยังเป็น RE งานเปิดสำหรับรอบถัดไปที่อยากทำ (ไม่ใช่ของรอบนี้)

## `GATE_UNVERIFIED #741` (`PANYA-DECISION 20260904_1158` §22)

push แล้วตรวจ `pull_request` gate ของ `pirate-force-server#741` — ที่ 15:38 +07:00 (≥10 นาทีหลัง push,
ทั้งสอง run เริ่ม 15:27:25/15:27:45) job `gate` ยัง `in_progress` ทั้งสอง run ยังไม่ตัดสิน ⇒ บันทึกไว้ตาม
กติกา §22 แทนที่จะจบรอบด้วย "waiting on gate — routine" **รอบถัดไปของ LANE-CS ต้องเปิดด้วยการตรวจ PR
`#741` นี้ก่อน** แดง = แก้ในรอบนั้นทันที (ไม่ใช่รอบเดิม เพราะรอบนี้ปิดไปแล้ว — แต่ต้องเป็นงานแรกของรอบ
ถัดไป ไม่ใช่งานคิว)
