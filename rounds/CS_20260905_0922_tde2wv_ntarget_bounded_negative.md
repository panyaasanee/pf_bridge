# CS round tde2wv — n_TARGET checked and falsified as a skill-type column

เวลาเริ่ม 2026-09-05 09:22 +07:00 · claim `pf_bridge` PR (ไฟล์รอบนี้ทับ `_claim.md`)

🔴 หมายเหตุความช้าของรอบนี้: ยืดยาวผิดปกติ (ปิดจริง ~12:07 หลังเริ่ม 09:22) เพราะรอชุดเต็ม 2 รอบ
(เขียนก่อน/หลัง merge origin/main) และการ resolve merge conflict กับรอบ LANE-CS คู่ขนาน (`mps8zh`,
รายละเอียดข้างล่าง) ไม่ใช่เพราะงานเพิ่มขึ้น — ขออภัยความล่าช้าต่อ COO ในรอบนี้เอง แทนจดหมายแยก

🔴 **`GATE_UNVERIFIED #816`** (`pirate-force-server`): push แล้วรอผล job `gate` ของ PR #816 ตามกติกา §22
เต็ม 10 นาที (เปิด PR 11:58 · เช็ค `in_progress` ต่อเนื่องถึง 12:07 · สอง run เพราะ push สองคอมมิตติดกัน
ก่อน merge origin/main ตอนเปิด PR ครั้งแรก) ยังไม่ตัดสิน ⇒ บันทึกไว้ตามกติกา ไม่ถือเป็นตัวบล็อกรอบนี้ ·
**รอบถัดไปของ LANE-CS ต้องเปิดด้วยการตรวจผลเกตของ #816 ก่อนงานอื่น** (ถ้าแดง = แก้ใต้รหัส `tde2wv` เดิม
ไม่ claim ใหม่ ตาม `1429`)

## ขั้นตอน 0 — `NOW.md` ก่อนทุกอย่าง

อ่านแล้ว (`git fetch` ก่อน) หัวข้อล่าสุด `1155`/`1045`/`0945` ไม่มีคำสั่งใหม่ถึง LANE-CS โดยตรง ·
เห็นบรรทัด `10:45`: "CS ล่าสุด 07:56 (`#1282`/`#802`) รอบ 09:06 ยังไม่เห็น PR — ดูรอบหน้า" — รอบนี้คือรอบ
09:06/09:22 ที่ COO รอ ส่งพร้อมไฟล์นี้

**รอบนี้ขยับ NOW/M ข้อไหน**: ไม่ขยับขั้นบันได M (`resolve_class_skill_damage`/`attack_skill_ids_for_class`
ยัง zero production caller เหมือนเดิม รอ `GT-243`) — งานหลักของรอบนี้คือคิวเริ่มต้นข้อ 1/3 (หาต้นเหตุ
สูตร/ประเภทสกิลจากตารางจริง): เช็ค `n_TARGET` เป็นตัวเลือกที่สองสำหรับ "ใบ RE ใหม่ที่ยังไม่มีเลข" ที่ส่วน
`s_CAST_CONDITION` ของ docstring `skill_catalog.py` ค้างไว้ (ต้องการแถวติดป้ายอิสระเพิ่มอย่างน้อย 8 แถว) —
ผลลบ (bounded-negative) เหมือนกับ `n_PASSIVE` (รอบ `6o11t1`) ก่อนหน้า ไม่ใช่ตัวปลดล็อก แต่แคบคำถามที่ใบ
RE ใหม่ต้องตอบ (อย่างน้อยต้องอธิบาย id 99 กับ id 7173) และป้องกันรอบถัดไปเสียเวลาลองซ้ำ

## ขั้นตอน 1 — list PR open หัว `[LANE-CS]` ทั้งสองรีโป

`search_pull_requests` `state:open`:
- `pirate-force-server`: 0 ใบหัว `[LANE-CS]` ⇒ ไม่ถอย
- `pf_bridge`: 0 ใบหัว `[LANE-CS]` (claim เดิมของรอบนี้เองยังไม่เคยเปิด PR จริง — เห็นตอนจบรอบว่า push
  claim commit ไปแล้ว 09:22 แต่ไม่เคยสร้าง PR ตาม ⇒ สร้างพร้อมไฟล์รอบนี้)

## ขั้นตอน 2 — `ADVERSARY_PENDING` จากรอบก่อน

ไม่มีค้างจากรอบก่อนหน้า (`b190t0` ปิดผล adversary ในรอบนั้นเอง)

## ขั้นตอน 3 — กล่องจดหมาย

`grep -l "ADDRESSEE: LANE-CS" notes_to_chief/*.md` กรองด้วย `head -3` (กติกา COO `0043`: นับเฉพาะบรรทัด
จ่าหน้า ไม่ใช่ทั้งไฟล์) แล้วข้ามใบที่มี `.CONSUMED.txt`: **ไม่มีใบค้าง** ใบเดียวที่ grep ทั้งไฟล์ยังเจอ (`1346`)
เป็น false positive ที่ทราบอยู่แล้ว (จ่าหน้าจริง `ถึง: chief`, COO ยืนยันซ้ำใน `0043` ว่า CS ไม่ปิด)

## งานที่ทำ — `pirate-force-server`

### สิ่งที่ตรวจพบ: `n_TARGET` ก็ไม่ใช่คอลัมน์ประเภทสกิล เหมือน `n_PASSIVE`

อ่าน `CONSTDATA_TH__SKILL_CONTEXT.tsv`/`TEXTDATA_TH__SKILL_TEXT.tsv` เต็มตาราง (2165 แถว ไม่ใช่แค่ 8 id
ในคาตาล็อก) เพื่อเช็ค `n_TARGET` เป็นตัวเลือกถัดไปสำหรับ "ใบ RE ใหม่" ที่ docstring ของ `skill_catalog.py`
ค้างไว้ (ส่วน `s_CAST_CONDITION`: ต้องการแถวติดป้ายอิสระอย่างน้อย 8 แถวก่อน ยังไม่มีใครเปิดใบ) — พบว่าสมมติฐาน
"ค่ายิ่งสูง = ยิ่งเป็นวงกว้าง/AOE" พังด้วยหลักฐานเดียวกับที่ทำให้ `n_PASSIVE` ตกรอบ:

- id 99 "Normal Attack" (ยิงเป้าเดียวแน่นอน ในคาตาล็อกเอง) มี `n_TARGET=1`
- id 7173 "Meteor Rain" (ชื่อบอกชัดว่าเป็นสกิลพื้นที่ นอกคาตาล็อก) มี `n_TARGET=1` **ค่าเดียวกัน**
- id 3210 "Grand Cannon" / 3332 "Great Cannon" / 3762 "Circle Attack" (ชื่อบอกชัดว่าเป็นสกิลพื้นที่ทั้งสาม)
  มี `n_TARGET=0` — ค่าเดียวกับสกิลเดิน/Basic Training ในคาตาล็อกเอง

หนึ่งคอลัมน์แปลว่า "เป้าเดียว" และ "พื้นที่" ที่ค่าเดียวกันพร้อมกันไม่ได้ — เป็นการชนแบบเดียวกับที่ทำให้
`n_PASSIVE` ตกรอบ ไม่ใช่ความคลาดเคลื่อนเล็กน้อย บันทึกลง docstring ของ `skill_catalog.py` (ต่อจากส่วน
`n_PASSIVE`/`s_CAST_CONDITION` เดิม) และปักด้วยคลาสเทสใหม่ `NTargetIsNotATypeColumnTests`
(`BRIDGE_GAMEDATA`-guarded เพราะ id ที่ใช้ชนอยู่นอกคาตาล็อก 8 ตัว ต้องอ่านตารางเต็มจาก pf_bridge โดยตรง
ไม่ใช่ผ่าน accessor ของโมดูลเอง)

**ไม่ได้เขียน accessor ใหม่** (`target_mode()`/`skill_type()` ก็ยังไม่มี) — ตามกติกา "ห้ามคอนสแตนต์ที่ไม่มี
ที่มา / ห้ามสร้างคอลัมน์ประเภทที่ยังไม่มีหลักฐาน" ผลลบยืนยันว่ายังไม่มีทาง narrow ใบ RE ใหม่ที่ค้างไว้ (อย่างน้อย
ต้องอธิบาย id 99 กับ 7173 ให้ได้ก่อน)

### แก้ไปด้วย: ถ้อยคำเก่าปนชื่อ "ไอคอนคลาส" กับ "ชื่อสกิล Basic Training"

พบระหว่างตรวจ: `skill_catalog.py` (บรรทัด 19-20 เดิม) และ `tools/pf_class_skill_starting_kit_extract.py`
(บรรทัด 29-30 เดิม) เขียนว่าสกิล "Basic Training" ของแต่ละอาชีพชื่อ "40000 Gladiator, 41000 Sniper, 42000
Necromancer, 43000 Paladin, 44000 Sorcerer" — เทียบกับตารางจริงแล้วชื่อเหล่านั้น ("Sniper"/"Necromancer"/
"Paladin"/"Sorcerer") เป็นชื่อจาก `CHARCREATE_CLASS.s_ICON` ของ**คลาส** ไม่ใช่ชื่อสกิลของ**สกิล**เอง — ชื่อจริง
ของสกิลจาก `TEXTDATA_TH__SKILL_TEXT.s_SKILL_TITLE` คือ "Sharpshooter Basic Training"/"Stormherald Basic
Training"/"Imperial Knights Basic Training"/"Light Priest Basic Training" (ตรงกับสมมติฐานเดิมเฉพาะคลาส 1
"Gladiator") — เทสที่มีอยู่แล้ว `test_basic_training_title_differs_from_the_charcreate_icon_name` วัดความ
ต่างนี้ไว้แล้วก่อนหน้านี้ แต่ docstring ยังไม่ได้แก้ตาม แก้ทั้งสองไฟล์ให้ตรงกับเทสที่มีอยู่ ไม่ใช่ข้อมูลใหม่

### merge conflict กับรอบ LANE-CS คู่ขนาน (`mps8zh`) — ตัวจริง ไม่ใช่เข้าใจผิด

`git fetch origin main` ระหว่างรอ พบ PR `#810` (merged 03:53 UTC = 10:53+07): อีกรอบ LANE-CS
(`session_01VFmw4BzcM6md69GUbAS9ou`, round `mps8zh`) เช็คคอลัมน์คนละตัว (`n_PASSIVE_EFFECT`) ด้วยวิธี
เดียวกันพอดี และก็ตกรอบเหมือนกัน (`NPassiveEffectDoesNotDiscriminatePassiveFromActiveTests`) — ชนกัน 3
ไฟล์เดียวกันที่ผมแก้ (`skill_catalog.py` docstring ส่วนท้าย · `test_skill_catalog.py` ท้ายไฟล์ ·
`docs/PYTEST_SKIP_PINS.json` entry เดียวกัน) merge ด้วยมือ เก็บทั้งสองฝั่งไว้ครบ (ย่อหน้า docstring สอง
ย่อหน้าเรียงกัน · คลาสเทสสองคลาสอยู่คนละคลาสในไฟล์เดียวกัน · pin count รวม `1 → 8` = ฐานเดิม 1 + ของผม 2 +
ของ `mps8zh` 5) ไม่มีใครถูกทับ

## ชุดเต็ม + preflight — รันสองรอบตามกติกา (ก่อน merge / หลัง merge)

1. **ก่อน merge** (บนกิ่งที่ยังไม่มี `#810`): `python3 -m pytest tests -q` → `10720 passed, 323 skipped,
   19800 subtests passed` เขียว (พิสูจน์งานตัวเองก่อนชนกับของคนอื่น)
2. **`git fetch origin main` แล้ว merge** เข้ากิ่ง — conflict 3 ไฟล์ (ข้างบน) resolve ด้วยมือ ยืนยัน
   `grep -rn "^<<<<<<<\|^=======\|^>>>>>>>"` ว่างสนิทก่อน commit
3. **หลัง merge, ครั้งเดียวจริงบนต้นไม้ที่ merge แล้ว**: `python3 -m pytest tests -q` →
   **`10810 passed, 323 skipped, 19921 subtests passed`** เขียว (10720+90 จากฝั่ง `#810` และรอบอื่นที่
   merge เข้ามาด้วย ตัวเลขรวมสมเหตุสมผล)
4. **ไฟล์เทสใหม่ (`NTargetIsNotATypeColumnTests`) + skip ใหม่ 2 ตัว ⇒ ซ้อม `pytest_subset`+`skip_census`
   ในสภาพไม่มี `pf_bridge` ข้าง ๆ ตามกติกา** — ใช้ `git worktree add --detach` แยกจาก `pf_bridge`:
   `10718 passed, 415 skipped, 19720 subtests passed` · `tools/pf_pytest_precondition_census.py --report`
   → **`bridge_gamedata tests/test_skill_catalog.py x8`** ตรงกับ pin ที่แก้ (1 เดิม + 2 ของผม + 5 ของ
   `mps8zh`) · `RESULT: PASS` · exit 0
5. `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (รันจาก `pf_bridge`):
   **PREFLIGHT PASS** (cp874 · ไม่มี skip ใหม่เทียบ origin/main ที่วัดตอนนั้น · main อยู่ใน branch แล้ว ·
   ทั้งสองกิ่งอยู่ในชื่อที่ระบบให้ ไม่ใช่ตั้งเอง)

## pf-adversary

สั่งสองครั้งรอบนี้ (ครั้งที่ 1 ต้นรอบก่อนเริ่มโค้ด บนไฟล์แรกที่เขียนเสร็จ — ตรวจ mutation ของ
`CLASS_IDS`/`attack_skill_ids_for_class`/`resolve_damage` ไม่พบบั๊ก; ครั้งที่ 2 ท้ายรอบบนคอมมิตสุดท้ายก่อน
push — ยังไม่เกินเพดาน 2 ครั้งของ `1428` เพราะครั้งที่ 2 ตรวจงาน+ตัวแก้รวมกัน ไม่ใช่รอบที่สาม) **ครั้งที่ 2
คืนผลแล้วก่อน push จริง**: ตรวจซ้ำอิสระตรงกับตารางจริง (`CONSTDATA_TH__SKILL_CONTEXT.tsv`
2165 แถว/การกระจาย `n_TARGET`/ชื่อ+ค่า id 99·7173·3210·3332·3762/`CHARCREATE_CLASS.s_ICON`/ชื่อสกิล Basic
Training ทั้ง 5) ตรวจย่อหน้า docstring ว่ายังเป็นผลลบล้วน ไม่แอบอ้างเกินหลักฐาน ตรวจคลาสเทสใหม่ว่าไม่มีทาง
ผ่านลวง (KeyError/AssertionError จริงถ้าอ่านคอลัมน์ผิดหรือ id หาย ไม่ใช่ผ่านเงียบ) รัน
`tests/test_skill_catalog.py` ได้ 30 passed, 83 subtests passed, ไม่มี skip — **ไม่พบบั๊ก** ⇒ ไม่มี
`ADVERSARY_PENDING`

## ขยับ NOW/M ข้อไหน

**ไม่ขยับ** — ผลลบ (bounded-negative) เหมือน `6o11t1`/`mps8zh` ก่อนหน้า ไม่ปลดตัวบล็อกใดของบันได M แต่แคบ
คำถามของ "ใบ RE ใหม่ที่ยังไม่มีเลข" (ต้องมีแถวติดป้ายอิสระ ≥8 แถว) ให้ต้องอธิบายอย่างน้อย id 99 vs 7173
ป้องกันรอบถัดไปลอง `n_TARGET` ซ้ำโดยไม่รู้ผลแล้ว

## ส่งอะไร

**pirate-force-server**: PR หัว `[LANE-CS] round tde2wv: n_TARGET is also not a skill-type column` —
สาขา `claude/inspiring-albattani-llk82x` (สร้างจาก `origin/main` ตามระบบให้ ไม่ตั้งชื่อเอง)
- `src/pirateforce_foundation/skill_catalog.py` (docstring: ผลลบ `n_TARGET` + แก้ถ้อยคำชื่อคลาส/ชื่อสกิล)
- `tools/pf_class_skill_starting_kit_extract.py` (แก้ถ้อยคำเดียวกัน)
- `tests/test_skill_catalog.py` (`NTargetIsNotATypeColumnTests`, 2 เทสใหม่, `BRIDGE_GAMEDATA`-guarded)
- `docs/PYTEST_SKIP_PINS.json` (pin `bridge_gamedata`/`test_skill_catalog.py`: `1 → 8`, merge กับ `mps8zh`)
- merge commit เข้า `origin/main` (`#810` ของ `mps8zh` และรอบอื่นที่ merge มาด้วยช่วงเดียวกัน)

**pf_bridge**: PR หัว `[LANE-CS] round tde2wv: claim` — สาขา `claude/admiring-thompson-llk82x`
- ไฟล์รอบนี้ทับ `_claim.md`
- ปิด marker ใบ `1346`? **ไม่ปิด** (ไม่ใช่ของ CS ตาม COO `0043` ยืนยันซ้ำ — ไม่มีใบใหม่ต้องตอบรอบนี้)

## nonclaims

- ไม่อ้างว่า `n_TARGET` (หรือ `n_PASSIVE_EFFECT` ของ `mps8zh`) เป็นคำตอบของประเภทสกิล — ทั้งคู่เป็นผลลบ
- ไม่อ้างว่ามี production caller ใหม่ — `resolve_class_skill_damage`/`attack_skill_ids_for_class` ยัง zero
  production caller เหมือนเดิม รอ `GT-243`
- ไม่อ้างว่าใบ `1346` ปิดแล้ว — ไม่ใช่ของ CS (COO `0043`)

## ติดอะไร / ใครปลด

- ตัวบล็อกเดิมคงอยู่: `GT-243` ต้องเครื่อง Panya (ผู้ปลด = Panya/chief ตามคิว attended) · จุดเสียบ
  `_dispatch_mob_combat` เขต LANE-B (ผู้ปลด = LANE-B/chief เมื่อ `GT-243` มีผล)
- ใบ RE ใหม่ที่ต้องการแถวติดป้ายอิสระ ≥8 แถว (สำหรับ AOE/buff/heal/passive) ยังไม่มีเลข — ไม่ใช่ตัวบล็อก
  เร่งด่วนของรอบนี้ (คิวเริ่มต้นข้อ 2/4 ครึ่งเซิร์ฟเวอร์เดินได้โดยไม่ต้องรอ ตาม `0647`) แต่เป็นช่องว่างที่ค้าง
  มาหลายรอบ — ระบุไว้เผื่อ chief/COO เห็นควรตั้งเลข

-- LANE-CS
