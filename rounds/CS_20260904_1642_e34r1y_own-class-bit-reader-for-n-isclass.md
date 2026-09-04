# CS round e34r1y — own_class_bit() reader for n_ISCLASS (5 Basic Training ids only)

เวลาเริ่ม 2026-09-04 16:42 +07:00 · เวลาปิด 2026-09-04 16:5x +07:00 · claim `pf_bridge#1167`

🔴 **ปิดย้อนหลังโดยรอบ `1z31do`** (`TZ=Asia/Bangkok date` ของรอบ `1z31do` = 2026-09-04 18:xx+07:00) — claim PR
`#1167` มีไฟล์นี้จริง (2 commits, `+130` บรรทัดไฟล์เดียว) แต่ถูกปิดโดยไม่ merge (`closed_at`
`2026-09-04T11:01:03Z`, `merged: false` — ตรวจผ่าน GitHub API โดยรอบ `1z31do` ไม่ใช่การเดา) งานฝั่ง
`pirate-force-server` (`00c305a`, PR `#746`) merge ขึ้น `main` จริงแล้วตั้งแต่ก่อนหน้านั้น (อยู่ใน
`git log` ของ `main` วันนี้) — เป็นแบบเดียวกับ `CS_18h0fp_claim.md` ที่ 6o11t1 เคยปิดย้อนหลัง: โค้ดจริง
ขึ้น main แล้ว ไฟล์รอบฝั่ง pf_bridge หายเพราะ claim PR ไม่ได้ merge ไม่ใช่เพราะงานไม่เสร็จ เนื้อหาด้านล่าง
คือของเดิมจากรอบ `e34r1y` (กู้จาก diff ของ PR `#1167` ที่ปิดไปแบบไม่ merge) ไม่มีการแก้เนื้อหา

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ M2/M3/M4/M5** — รอบนี้เป็น**งานสำรอง** ของ LANE-CS ตามคิวเริ่มต้นข้อ 1 ("สารบัญอาชีพและ
สกิลจากตารางจริง ... ค่า MP/CD/ระยะ") ไม่ใช่งานหลักบนจอ ต่อจากรอบที่แล้ว (`kd06fo`)

**เหตุที่ไม่ทำงานหลักรอบนี้**: `git fetch` แล้วเปิด `pf_bridge/CLIENT_RE_QUEUE.md` ตรง ๆ — `RE-240`
(บรรทัด 5005) ยัง `[OPEN -- [STATIC-ON-BRIDGE]]` ผู้ทำ = สาย RE local ยังไม่มีผลตอนปิดรอบนี้ · งาน
หลัก (ผูก `resolve_skill_damage`/`damage_by_skill.py` เข้ากับฟิลด์ `ActionVital` ที่ถือ skill id จริง)
ยังบล็อกอยู่ที่ผลของ `RE-240` เหมือนรอบก่อน ตาม `20260904_1405` (chief) ยัง**ห้ามเสียบผู้เรียกกับ
`action_u32_30`** — รอบนี้จึงไม่แตะ `damage_by_skill.py`/`mob_combat.py` เลยเหมือนเดิม

**ตรวจ `GATE_UNVERIFIED #741` ของรอบก่อนก่อนเริ่มงาน** (ตามที่ไฟล์รอบ `kd06fo` สั่งไว้): PR
`pirate-force-server#741` — `gate` ทั้งสอง run `completed`/`success` (08:55:38/08:46:10 UTC) ·
PR **merged** แล้ว → ไม่ใช่ตัวบล็อกของรอบนี้ ปิดเรื่องนี้แล้ว

ตาม `PANYA-DECISION 1450` (14:55, "รอบว่างไม่มีอีกแล้ว") รอบนี้หยิบงานสำรองข้อ 1 ต่อจากรอบ
`kd06fo`: `skill_catalog.py` มีคอลัมน์ดิบ `n_ISCLASS` อยู่ใน `skill_raw_context()` มาตั้งแต่รอบ
`iazmrv` แต่ไม่เคยมีชื่ออ่านเฉพาะ — รอบก่อนทิ้งเงื่อนไขไว้ว่า "ถ้ามีเหตุผลใช้จริง ไม่ใช่ครบทุกคอลัมน์
เพื่อครบ" — รอบนี้พบเหตุผลจริง: `tools/pf_class_skill_starting_kit_extract.py`'s docstring (รอบ
`iazmrv`) เคยวัดไว้แล้วว่า `n_ISCLASS` เป็นบิตของอาชีพตัวเองสำหรับ 5 สกิล "Basic Training" (ตรงกับ
`class_catalog.CLASS_IDS` เป๊ะ: 40000→1, 41000→4, 42000→16, 43000→2, 44000→32) — เป็นข้อเท็จจริง
ที่พิสูจน์แล้วจากสองตารางที่คอมมิตแยกกัน (`SKILL_CONTEXT` ผ่าน skill_catalog, `CHARCREATE_CLASS`
ผ่าน class_catalog) ไม่ใช่การเดา จึงเปิดเป็นเทสไขว้ตรวจความสอดคล้อง (drift guard จริง ถ้าไคลเอนต์
เปลี่ยนบิตของสกิลใดสกิลหนึ่งวันหน้า)

## งานสำรอง 3 ข้อของ LANE-CS (ตาม `1450` ข้อ 6 — เริ่มได้ทันทีไม่รอใคร เรียงตามบันได M)

1. **(ทำรอบนี้)** เติมชื่ออ่านให้ค่าที่ `skill_raw_context()` มีอยู่แล้วแต่ยังไม่มีฟังก์ชันเฉพาะ —
   `n_ISCLASS` เสร็จแล้ว (ขอบเขตแคบ 5/8 สกิล ตามหลักฐาน) เหลือ `n_EQUIPTYPE`/`n_EQUIPTYPE_LHAND`
   ยังไม่พบเหตุผลใช้จริง (ทุกสกิลใน 8 ตัวมีค่า 0 หมด — ไม่มีอะไรให้ cross-check หรือแยกแยะ) ยังไม่ทำ
2. เพิ่มเทสเปรียบเทียบ `resolve_damage`/`damage_by_skill.resolve_skill_damage` กับตัวเลขจากรายงาน
   static เพิ่มอีก "ฉาก"/มอน (นอกเหนือ 916) **ถ้า**พบตัวเลข static ที่คอมมิตแล้วที่ยังไม่ถูกเทียบ — ค้น
   `reports/` รอบนี้พบ `PF_DAMAGE_NPC_TARGET001_SECOND_PROFILE_20260820.md` แต่เป็นคนละเรื่อง (wire/
   encoding pins ของ HYP-PF-024 ไม่ใช่สูตรดาเมจกับสถิติมอน) — ยังไม่พบตัวเลข static ของมอนตัวที่สอง
   ที่ resolve_skill_damage ยังไม่เทียบ ยังไม่เริ่มทำ
3. อ่าน `stats_progression_hypothesis.py`/`tools/pf_stats_progression_static.py` หาช่องว่างแบบ
   เดียวกับข้อ 1 — เปิดอ่านรอบนี้ (2682 บรรทัด) พบว่าโมดูลค่อนข้างสมบูรณ์แล้ว (ทุกฟิลด์ที่มีชื่อมี
   accessor, ฟิลด์ที่ไม่มีชื่อมีเหตุผลบันทึกไว้ใน `NOT_IMPLEMENTED_*`) — ยังไม่พบช่องว่างแบบเดียวกับ
   ข้อ 1 ในรอบนี้ ต้องอ่านต่อรอบหน้า (ยังไม่ครบทั้งไฟล์)

## ส่งอะไร

**pirate-force-server** หนึ่งคอมมิตบน `claude/pensive-bardeen-e34r1y` (`00c305a`, merge
`origin/main` `33981ba` แล้ว, ไม่มีคอนฟลิกต์), PR `#746` (merged แล้วขึ้น main):

- `src/pirateforce_foundation/skill_catalog.py`:
  - `own_class_bit(skill_id) -> int` อ่าน `n_ISCLASS` **เฉพาะ 5 ไอดี Basic Training**
    (40000/41000/42000/43000/44000) — ปฏิเสธด้วย `SkillCatalogError` สำหรับ 99/110/111 (ค่าดิบ
    63/0/0 ไม่มีความหมายที่พิสูจน์แล้ว) และ `KeyError` สำหรับไอดีนอกคาตาล็อกเหมือน accessor อื่น
  - `_BASIC_TRAINING_SKILL_IDS` ทูเพิลที่ derive จากชื่อ (`SKILL_ID_TO_TITLE[...].endswith(" Basic
    Training")`) ไม่ hardcode รายชื่อสกิล
  - ย่อหน้า `[UPDATE, this round]` ในดอกสตริงโมดูล อธิบายขอบเขตแคบและเหตุผล (อ้างอิงตรง
    `tools/pf_class_skill_starting_kit_extract.py`) พร้อมเปลี่ยนป้ายย่อหน้าของรอบก่อนเป็น
    `[UPDATE, round kd06fo]` กันสับสน
- `tests/test_skill_catalog.py`:
  - `test_own_class_bit_matches_the_raw_n_isclass_column` — pin ค่าดิบ 5 ค่า
  - `test_own_class_bit_equals_the_class_id_that_grants_it` — cross-derive จาก
    `class_catalog.CLASS_IDS`/`starting_skill_ids()` พร้อมตัวนับ `checked == 5`
  - `test_own_class_bit_refuses_the_three_non_basic_training_ids` / `..._raises_key_error_for_an_
    unknown_id`
  - `test_basic_training_skill_ids_is_exactly_the_five_known_ids` — **เพิ่มหลัง pf-adversary เสนอ**
    (ดูหัวข้อ adversary)

**pf_bridge**:
- ไฟล์นี้ (แทน `rounds/CS_e34r1y_claim.md`) — กู้และวางโดยรอบ `1z31do` หลังพบว่า claim PR `#1167`
  ปิดไม่ merge

## pf-adversary

**ไม่ pending** — สั่งต้นรอบพร้อมเริ่มเขียนโค้ด ผลคืนก่อน push ครบ ไม่พบข้อบกพร่องจริง เสนอ hardening
หนึ่งจุด แก้แล้ว:

- **(1) `_BASIC_TRAINING_SKILL_IDS` ถูกต้องไหม**: อ่าน `skill_context_starting_kit.tsv`/
  `skill_text_starting_kit.tsv` เองแยกจากรายงานของผม — ตรงกับทุกค่าที่เทสยืนยัน (99→63, 110→0,
  111→0, 40000→1, 41000→4, 42000→16, 43000→2, 44000→32) และมีแค่ 5 ไอดีที่ title ลงท้ายด้วย
  `" Basic Training"` จริง
- **(2) title-suffix อาจ match ผิด/พลาดไหม**: ไม่พบปัญหากับตารางปัจจุบัน — ความเสี่ยงเดียวคือ
  อนาคตถ้าตารางขยายเป็น 9 ไอดีและไอดีใหม่ชื่อลงท้ายแบบเดียวกันโดยไม่ใช่แถวบิตอาชีพจริง จะไม่มีเทส
  จับที่จุด derive โดยตรง (มีแค่ pin จำนวน 8 ไอดีทางอ้อม) → **แก้แล้ว**: เพิ่ม
  `test_basic_training_skill_ids_is_exactly_the_five_known_ids` pin ทูเพิลตรง ๆ
- **(3) ตัวนับ `checked == 5` มีความหมายจริงไหม**: พิสูจน์ด้วยมิวเทชันจริงที่ `class_catalog.py`
  (ทำให้ทูเพิลของคลาสหนึ่งซ้ำสล็อต Basic Training โดยไม่เปลี่ยนความยาวทูเพิล หลบ pin รูปทรงของ
  `test_class_catalog.py`) — เทสต่อไอดียังเขียวหมด (สกิล/คลาสเดิม แค่นับซ้ำ) มีแต่ `checked==5`
  ที่จับได้ (`checked=10`) ยืนยันว่าตัวนับไม่ใช่ของตกแต่ง
- **(4) ชื่อ/ข้อความปฏิเสธกันคนเข้าใจผิดว่าเป็น "เช็คทั่วไปว่าสกิลนี้ใช้ได้กับอาชีพไหน" ไหม**: ไม่พบ
  ช่องโหว่ — ชื่อฟังก์ชัน (`own_` prefix) + ดอกสตริง + ย่อหน้าดอกสตริงโมดูล + ข้อความ exception ชี้ตรง
  ไปที่ขอบเขตแคบและอ้างอิงเครื่องมือต้นทาง `SkillCatalogError`/`KeyError` เป็นคนละชนิด ไม่ชนกัน
- **(5) มิวเทชันตรรกะปฏิเสธ 4 แบบ**: สลับชนิด exception ระหว่างสองสาขา / กลับทิศ `not in` /
  ลบการ์ด `SkillCatalogError` ทิ้ง / จัดเรียง if ใหม่แบบพฤติกรรมเดิม — สามแบบแรกถูกเทสจับหมด (4/13/3
  จุดแดงตามลำดับ) แบบที่สี่ไม่ใช่มิวแทนต์จริง (พฤติกรรมเหมือนเดิม) ไม่นับ
- **(6) ขอบเขตเลน**: `git diff --stat origin/main..HEAD` มีแค่ `skill_catalog.py`/
  `test_skill_catalog.py` ไม่แตะ `mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`/
  `current/pf_login_game_server_v141.py`
- **(7) เทสที่แตะ**: `python3 -m pytest tests/test_skill_catalog.py tests/test_class_catalog.py -q
  -rs` = 32 passed, 2 skipped (BRIDGE_GAMEDATA precondition, ทั้งสองไฟล์), 62 subtests — ก่อนเพิ่ม
  เทส hardening ข้อ (2) รอบนี้เพิ่มเป็น 35 passed หลังเพิ่ม

## nonclaims (grep กำกับตามกฎ)

- **ไม่มีผู้เรียกในโปรดักชัน**: `grep -rn "own_class_bit" src/ current/ 2>/dev/null | grep -v
  "src/pirateforce_foundation/skill_catalog.py\|tests/"` = ไม่พบ
- **ไม่แตะ `damage_by_skill.py`/`mob_combat.py`/`runtime.py`/`app.py`/`store.py`/`gm/`/
  `current/pf_login_game_server_v141.py`** — `git diff --stat origin/main..HEAD` มีแค่สองไฟล์
  ข้างต้น
- **ไม่อ้างว่า `n_ISCLASS` เป็น general skill-to-class foreign key** — `own_class_bit()` ปฏิเสธ
  ทุกไอดีนอก 5 ไอดี Basic Training ตามหลักฐานของ `tools/pf_class_skill_starting_kit_extract.py`
  ไม่มีการขยายความหมายเกินที่มี
- **ไม่ตัดสินใบ CORE-REQUEST `1041`/`RE-240`** — `grep -n "RE-240" pf_bridge/CLIENT_RE_QUEUE.md`
  ยังขึ้น `[OPEN` ไม่ใช่ตัวบล็อกของรอบนี้ (งานสำรอง ไม่ใช่งานหลัก)
- **ไม่เปิดใบ 16-row taxonomy** — ยังพักตาม `COO-DECISION 1246`
- **ไม่พบตัวเลข static ของมอนตัวที่สองสำหรับงานสำรองข้อ 2** — `grep -rln "916\|template_id"
  reports/*.md` มีแค่รายงานที่เกี่ยวกับ wire encoding (`PF_DAMAGE_NPC_TARGET001...`) ไม่ใช่สูตร
  ดาเมจกับสถิติมอนที่ resolve_skill_damage เทียบได้

## ติดอะไร / ใครปลด

- **`RE-240`** (chief เปิด, letter `1405`) — ตอนปิดรอบ `e34r1y` ยังไม่มีผล **อัปเดตโดยรอบ `1z31do`**:
  ผลกลับมาแล้ว 17:14+07:00 = `DONE/BOUNDED-NEGATIVE` (ดูไฟล์รอบของ `1z31do` สำหรับรายละเอียดและ
  สิ่งที่ทำต่อ) ไม่ใช่ตัวบล็อกของรอบนี้อีกต่อไป
- **attacker pin สำหรับการต่อสู้จริง** — ยังเป็นหนี้ของ LANE-B รอชิ้น 2 ของ DB (`COO 0943`) ไม่เปลี่ยน
- **งานสำรองข้อ 2/3** — ยังเปิดอยู่สำหรับรอบถัดไป (ดูหัวข้อ nonclaims/งานสำรองข้างบนสำหรับสถานะ
  การค้นรอบนี้)

## `GATE_UNVERIFIED`

**ปิดโดยรอบ `1z31do`**: PR `pirate-force-server#746` merged แล้วขึ้น `main` (ยืนยันจาก `git log`
ของ `main` วันนี้ — commit `00c305a` อยู่ใน history) ไม่ใช่ตัวบล็อกของรอบถัดไปอีกต่อไป
