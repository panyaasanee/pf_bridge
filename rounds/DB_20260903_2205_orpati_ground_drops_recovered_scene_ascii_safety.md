# DB round (`orpati`) — 2026-09-03T22:05+07:00 to 22:37+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260903_2040_g65xvq_release_1006_and_alarm_672.md` (รอบนั้นปลดล็อก `pf_bridge#1006`
และพบว่า `pirate-force-server#672` ถูก reaper ปิดเพราะ gate แดง ไม่ใช่เพราะปัญหา marker) และตอบ
`COO-DECISION 20260903_2050` (กู้กิ่งของประตูของบนพื้น เปิดใบใหม่จาก main พร้อมเติม `"ground_drops"` เข้า
`EXPECTED_TABLES`)

**บรรทัดเดียวของรอบนี้: กู้ประตูของบนพื้น (ground_drops) ขึ้น PR ใหม่จาก main สำเร็จ ระหว่างทางเจอบั๊กจริง
สองตัว (จาก pf-adversary หนึ่งตัว จากชุดเต็มของรอบเองอีกหนึ่งตัว) แก้ทั้งคู่ก่อน push**

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรกก่อนแตะอะไร (ฉบับ "ตรวจล่าสุด 2026-09-03 21:41 +07:00 โดย COO") และเช็คซ้ำตอน
จบรอบ (`git fetch origin main` แล้ว `git diff` ไฟล์ `NOW.md`) — **ไม่เปลี่ยนระหว่างรอบ**

- **ไม่ขยับบรรทัดใดของ `NOW.md`** — งานนี้คือคิว DB ที่ระบุไว้แล้ว (บรรทัด 38: "คิวถัด DB = `#666` ขึ้น
  main แล้วสร้างประตู (`1843`)" ตามด้วย `COO-DECISION 20260903_2050` ที่สั่งกู้ `#672`) ยังไม่มีอะไรถึง
  เกณฑ์ย้ายขึ้น "รอ Panya ติ๊ก" (client-observable ยังเป็นศูนย์ ไม่มี call site) และยังไม่มีอะไรถึงเกณฑ์ลบ
  ไม่มีสิทธิ์แก้ `NOW.md` เอง
- **P-0 · P-1 · P-2 · P-3 · GM-A · UI-A · UI-B · /speed · M4** นอกเขตของสายนี้ ไม่แตะแม้ไฟล์เดียว
- 🔴 ไม่แตะ `gm/` `speed_wire.py` `runtime.py` `app.py` `v141` `mob_loot.py` `.github/` `AGENTS.md`
  `tools/` — ทุกไฟล์ที่แตะรอบนี้อยู่ในเขตเขียนของ LANE-DB ทั้งหมด (`migrations/010_*`,
  `src/pirateforce_foundation/store.py`, `persistence_ground_drops.py`, `tests/test_persistence_
  ground_drops_010.py`, `tests/test_npc_interaction_wire.py`)

## 1. ล็อกรอบ

- 22:05+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open ทั้งสองรีโปหัวข้อขึ้นต้น `[LANE-DB]`:
  ไม่มีใบไหนเปิดค้างในทั้งสองรีโป ⇒ ไม่ต้องปลดล็อกใคร ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`a3e21389`) commit `rounds/DB_20260903_2205_orpati_claim.md`
  (สามบรรทัด: `orpati` · `2026-09-03T22:05+07:00` · `claim`) push แล้วเปิด `pf_bridge#1021
  [LANE-DB] round orpati: claim` ไม่มี `PF-AUTOMERGE: v4` ใน body ตอนเปิด
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1021` ของผมเอง (`#1020 [LANE-B]`
  เปิดคู่ขนาน ไม่ใช่ของผม ไม่แตะ) · `pirate-force-server` ไม่มี `[LANE-DB]` เปิดเลย (มีแค่ `#678 [LANE-E]`)
  ⇒ ไม่แพ้ ทำงานต่อ
- ตรวจซ้ำอีกครั้งก่อนเปิด PR เซิร์ฟเวอร์ตอนจบรอบ (22:3x+07): `[LANE-DB]` open ใน `pf_bridge` ยังมีแค่
  `#1021` ของผมเอง (`#1022 [LANE-GM]`, `#1023 [LANE-A]`, `#1024 [LANE-B]` เปิดคู่ขนาน ไม่ใช่ของผม)
  · `pirate-force-server` ไม่มี `[LANE-DB]` เปิดเลย ⇒ ยังไม่แพ้ เปิด PR เซิร์ฟเวอร์ได้

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สด แล้วหักใบที่มี `.CONSUMED.txt` คู่ ⇒ ค้างใบเดียว:

| ใบ | ทำอะไรรอบนี้ |
|---|---|
| `20260903_2050_COO-DECISION-...recover-672-and-reopen-from-main.md` | เนื้องานทั้งรอบนี้คือคำสั่งของใบนี้ตรง ๆ (ดู §3) — สร้าง `.CONSUMED.txt` แล้ว |

ไม่มีจดหมายใหม่ส่งออกรอบนี้ (ไม่มีอะไรเกินอำนาจ ไม่มีทางเลือกที่ย้อนไม่ได้/ไม่มี backup ให้ถาม COO)

## 3. ทำอะไร

### 3.1 กู้ประตูของบนพื้น (`COO-DECISION 20260903_2050` ข้อ 1-3)

- ตัดกิ่ง `claude/gifted-wright-orpati` ให้อยู่ที่ `origin/main` สด (`3b216b5e`) แล้ว
  `git cherry-pick 0723abf0` (คอมมิตของรอบ `5d02mu` บนกิ่งที่ตายแล้ว `claude/adoring-meitner-5d02mu`)
  — apply สะอาด ไม่มี conflict (10 ไฟล์, +908/-55): `migrations/010_ground_drops.sql`,
  `src/pirateforce_foundation/persistence_ground_drops.py`, `store.py` (สอง method ใหม่:
  `commit_ground_drop`/`list_ground_drops_for_scene`), `tests/test_persistence_ground_drops_010.py`
  ใหม่ทั้งไฟล์ (448 บรรทัด, 39 เทสเดิม) + แก้หมุดนับ migration 3 ไฟล์ที่คอมมิตเดิมทำไว้แล้ว (อยู่ในสิทธิ์
  `20260901_1416`/`20260901_1459` ที่คอมมิตเดิมอ้างถูกต้อง)
- เติม `"ground_drops"` เข้า `EXPECTED_TABLES` ใน `tests/test_npc_interaction_wire.py:45-53` พร้อมคอมเมนต์
  อ้าง `COO-DECISION 20260903_1843` + `20260903_2050` — วัดจริงว่าการ์ดยังใช้งานอยู่ (ไม่ใช่การ์ดที่ไม่มี
  วันถูกเรียก): revert หนึ่งบรรทัดนี้ในรอบ pf-adversary ทำให้
  `test_store_schema_owns_no_quest_shop_or_reward_table` แดงจริง
- ตรวจ migration-count pin สองไฟล์ (`test_foundation.py`, `test_item_move_capture.py`) ที่คอมมิตเดิมแก้
  ไว้แล้วเป็น `10` — ไม่ต้องแก้เพิ่ม เพราะ `main` ยังไม่มี migration ใหม่ระหว่าง `#672` ถูกปิดกับตอนนี้
  (ตรวจด้วย `git ls-tree origin/main -- migrations/` เห็นสูงสุด `009`)

### 3.2 pf-adversary รอบแรก — พบบั๊กจริง (scene ไม่บังคับ ASCII)

ส่ง pf-adversary ตรวจก่อน commit ตามระเบียบ พบข้อบกพร่องยืนยันแล้ว (ไม่ใช่สมมติฐาน): `commit_ground_drop`/
`list_ground_drops_for_scene` ตรวจ `scene` แค่ "เป็น str ไม่ว่าง" ทั้งที่คอมเมนต์ของ
`migrations/010_ground_drops.sql` เองอ้างว่า scene ทุกค่าถูกบังคับ ASCII โดย `mob_loot._require_scene`
— จริงเฉพาะเมื่อมี call site ของ LANE-B ที่สร้างผ่าน `mob_loot.GroundDrop` (ยังไม่มีในรอบนี้) ไม่จริงที่
ขอบเขตของฟังก์ชันนี้เอง เขาสาธิตสดสองผลลัพธ์:
- ตัวสะกดสองแบบที่ต่างกันแค่ตัวอักษรนอก ASCII (ตัวอักษรเยอรมัน sharp-s เทียบกับ `"STRASSE"`) ทั้งคู่
  `.casefold()` เป็น `"strasse"` เหมือนกัน ⇒ ชนกันเท็จที่ `UNIQUE(scene_fold, drop_key)`
- เส้นพิมพ์คอนโซลตอนปฏิเสธการชน (`print("...%r"...)`) พัง `UnicodeEncodeError` ทันทีที่ scene ไม่ใช่
  ASCII เพราะคอนโซลของสายนี้เป็น cp874 — ตรงกับบั๊กคลาสเดียวกับที่เคยปิด `#200` เป๊ะ แค่เกิดในประตูใหม่

**แก้แล้ว**: เพิ่ม `_require_ground_drop_scene()` ใน `store.py` (คัดลอก logic ของ `mob_loot._require_scene`
มาตรงเป๊ะ — type, non-empty, ยาว≤32, ASCII, ไม่มี whitespace, printable — โดยไม่ import `mob_loot`
ด้วยเหตุผลขอบเขตสายเดียวกับที่ไฟล์นี้อธิบายไว้แล้วสำหรับเช็คอื่น) เรียกจากทั้งสอง method ก่อนแตะ DB
เพิ่มเทส 6 ตัวใน `TheSceneMustBeASCIISafeTests` ปักทั้งสองผลลัพธ์ที่ปิดแล้ว

### 3.3 pf-adversary รอบสอง — ยืนยันปิดจริง พบจุดเสี่ยง drift เล็กน้อย

ส่งตรวจซ้ำเฉพาะจุดที่แก้ (ไม่ใช่ทวนทั้งไฟล์) — ยืนยันทั้งสองบั๊กปิดจริง ไม่มีช่องหลบเลี่ยง (ลองอินพุตเพิ่ม
เอง: Kelvin sign U+212A ก็ fold เป็น "k" เหมือน "K" ธรรมดา, zero-width space, control char — ปฏิเสธหมด)
ชี้จุดเสี่ยงเดียว: logic คัดลอกมาไม่มีตัวเช็คว่า `mob_loot._require_scene` เปลี่ยนกฎในอนาคตแล้วสำเนานี้จะ
ตามไม่ทัน (silent drift) **แก้แล้ว**: เพิ่มคลาสเทส `TheSceneCheckDoesNotSilentlyDriftFromMobLootTests`
(import `mob_loot` ในไฟล์เทสได้ — ไม่ใช่ `store.py` — จึงไม่ผิดขอบเขตสาย) เทียบ `GROUND_DROP_SCENE_MAX`
กับ `SCENE_NAME_MAX` และรันชุดอินพุต 11 ค่าผ่านทั้งสองฟังก์ชันเทียบผลลัพธ์ตรงกัน + แก้คอมเมนต์ใน
`migrations/010_ground_drops.sql` ให้บอกว่าตอนนี้บังคับที่ store boundary เองด้วย ไม่ใช่แค่ผ่าน
`mob_loot._require_scene` (ไฟล์นี้ยังไม่เคยขึ้น main จึงแก้ข้อความได้โดยไม่กระทบ checksum ของ migration
ที่ apply แล้ว)

### 3.4 ชุดเต็มรอบแรก — พบบั๊กจริงอีกตัว (cp874)

`git fetch origin main` ก่อนรันชุดเต็มตามกฎ `0053`/`0149` พบ `main` ขยับ (`#678` merge เข้ามา) `merge
origin/main --no-edit` สะอาด ไม่ชนไฟล์ของสายนี้เลย รันเทสเป้าหมายซ้ำเขียว (189 passed) แล้วรันชุดเต็ม
`pytest tests/` — **แดงจริง 2 subtest**: `tests/test_tree_is_cp874_safe.py` จับได้ว่า docstring ของ
`_require_ground_drop_scene` เขียนตัวอักษรเยอรมัน sharp-s (U+00DF) ตรง ๆ ในคอมเมนต์ยกตัวอย่าง — ไม่มี
cp874 mapping พังเงื่อนไขเดียวกับที่เคยปิด `#200` (gate แดง แล้ว `merge-claude-pr.yml` ปิด PR ทันที)
**แก้แล้ว**: เปลี่ยนคอมเมนต์ให้บรรยายตัวอักษรด้วยคำแทน (ไม่เขียนตัวอักษรจริง) — `tests/` ไม่อยู่ใน
`SCANNED_PREFIXES` ของ gate (`tools/`, `src/`, `current/` เท่านั้น) ดังนั้นข้อความเดียวกันในไฟล์เทสไม่มี
ความเสี่ยง

### 3.5 ชุดเต็มรอบสอง — เขียวสนิท

`git fetch origin main` ซ้ำ พบ `main` ขยับอีก (`#679` merge — LANE-B, แก้ `mob_loot.py`/
`mob_scene_recompose.py`/ฯลฯ) `merge origin/main --no-edit` สะอาดอีกครั้ง ไม่ชนไฟล์ของสายนี้ (ตรวจว่า
`_require_scene`/`SCENE_NAME_MAX` ที่เทส drift-guard ใหม่อ้างอิงไม่ถูกแก้ในดิฟฟ์นั้น) รันเทสเป้าหมาย+
`test_tree_is_cp874_safe.py` ซ้ำเขียว (194 passed) แล้วรันชุดเต็มอีกครั้งบน commit สุดท้ายจริง (`6f6d2f50`)
— **9092 passed, 323 skipped, 17654 subtests passed, 0 failed** — เขียวสนิท

## 4. ทำไมรันชุดเต็มสองครั้ง (ตามกฎต้องระบุเหตุผล)

รอบแรกแดงจริง (ไม่ใช่ flake) — พบบั๊กจริงที่ `test_tree_is_cp874_safe.py` (ดู §3.4) ต้องแก้แล้วรันซ้ำเพื่อ
ยืนยันว่าแก้ครบและไม่มีผลข้างเคียง ตามกฎ "ห้าม push สภาพที่ไม่เคยถูกรันเต็ม" ครั้งที่สองคือครั้งที่วัดจริง
บน commit สุดท้ายที่ push ครั้งที่หนึ่งเป็นแค่ตัวจับบั๊ก ไม่ใช่การรันซ้ำโดยไม่จำเป็น

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** — ไม่มี call site เรียก `commit_ground_drop`/`list_ground_drops_for_scene` จาก `runtime.py`
เลย (จุดเรียกตอนของตกจริงเป็นของ LANE-B ตาม `COO-DECISION 20260903_1844`) รอบนี้เป็นงาน wire/DB ล้วน

### 5.2 wire-DB

- ชุดเต็มสุดท้าย (commit `6f6d2f50`, merge กับ `main` ที่ `0138473d`/`#679`): **9092 passed, 323 skipped,
  17654 subtests passed, 0 failed**
- ไฟล์เป้าหมาย 9 ไฟล์ (รวม `test_tree_is_cp874_safe.py`): 194 passed, 630 subtests passed
- pf-adversary สองรอบ: รอบแรกพบบั๊ก scene ASCII (สาธิตสด 2 เคส) รอบสองยืนยันปิดจริง ไม่พบทางหลบเลี่ยง
  (ลองอินพุตเพิ่มเอง 3 เคส: Kelvin sign, zero-width space, control char — ปฏิเสธหมด)
- `pirate-force-server#680` `[LANE-DB] round orpati: ...` — เปิดแล้ว มี `PF-AUTOMERGE: v4` เป็นบรรทัด
  เดี่ยวท้าย body เท่านั้น (ตรวจแล้วไม่มีสตริง marker ปนในประโยคอธิบายจุดไหนเลย — บทเรียนจาก `#672`)
- `pf_bridge#1021` — เปิดแล้ว เป็นล็อกของรอบนี้ (จะเติม marker ท้ายรอบหลัง §6 เสร็จ)

## 6. nonclaims

1. **ไม่มีอะไร client-observable รอบนี้** — ไม่มี call site (§5.1)
2. **`pirate-force-server#680` ยังไม่ merge ณ ตอนจบรอบนี้** — เปิดแล้วมี marker แต่ reaper ทำงานแบบ async
   ตาม `workflow_run` event หลัง gate ของมันจบ ไม่รอ gate เขียวจริงตามกฎ (ไม่ต้องรอ)
3. **บั๊ก scene ASCII ที่แก้รอบนี้เป็นบั๊กแฝง (latent) ไม่ใช่บั๊กที่ถึงมือผู้เล่นได้จริงตอนนี้** — เพราะยังไม่มี
   call site เรียกฟังก์ชันนี้เลย จะกลายเป็นบั๊กจริงก็ต่อเมื่อ call site ของ LANE-B (ยังไม่สร้าง) ส่ง scene ที่
   ไม่ผ่าน `mob_loot`'s ของตัวเองมาก่อน
4. **ไม่ได้ตรวจว่า call site ในอนาคตของ LANE-B จะส่ง scene ผ่าน `mob_loot._require_scene` ก่อนเสมอไหม** —
   นอกเขตของรอบนี้ (ยังไม่มี call site ให้ตรวจ) pf-adversary รอบสองระบุไว้เป็นคำถามเปิดเช่นกัน
5. **ไม่ได้แก้ `.github/workflows/`, `AGENTS.md`, `PROCESS_GATES.md`** — นอกเขตเขียนทั้งหมด ไม่มีจดหมายใหม่
   ส่งออกรอบนี้เพราะไม่มีอะไรเกินอำนาจหรือย้อนไม่ได้ให้ถาม
6. **เวลารันชุดเต็มสองครั้งรวม ~16 นาที (480s + 496s) เป็นต้นทุนจริงของบั๊กที่เจอ ไม่ใช่การรันซ้ำเพราะ
   ไม่มั่นใจ** — ดู §4

## 7. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงาน: รันเฉพาะไฟล์เทสที่เกี่ยวข้อง (9 ไฟล์) หลายรอบ ไม่รันชุดเต็มระหว่างทาง — ตามกฎ
- ชุดเต็ม: รันสองครั้ง เหตุผลใน §4 ครั้งที่สอง (บน commit `6f6d2f50` ที่ push จริง) คือครั้งที่นับ:
  **9092 passed, 323 skipped, 17654 subtests passed, 0 failed**
- `pirate-force-server#680`: เปิดแล้ว มี `PF-AUTOMERGE: v4` — สถานะ ณ ตอนเขียนไฟล์นี้ "เปิดแล้ว รอ gate"
  (ไม่เขียนว่าขึ้น main แล้ว)
- `pf_bridge#1021`: จะเติม marker ทันทีหลัง push ไฟล์รอบนี้ (§ ถัดไปของรอบ)

## 8. รอบหน้าทำอะไร

1. **ตรวจว่า `pirate-force-server#680` merge จริงหรือยัง** — ถ้ายัง ตรวจ gate log ว่าติดตรงไหน
2. **คิว DB ถัดไป**: ตาม `COO-DECISION 20260903_1649` ข้อ 4/`1048` — ครึ่ง DB ของ M4 ลงครบแล้ว (ประตูเขียน
   + ตัวฟื้นตอนล็อกอิน) HP/เลเวลตามใบ `1101` ยังรอ M4 ปลดล็อกเต็มจาก LANE-B (`apply_hp_damage` ผู้เรียก)
   ก่อน — รอบหน้าต้องอ่าน `NOW.md` ล่าสุดใหม่ก่อนตัดสินใจว่าคิวขยับหรือยัง อย่าเดาจากไฟล์รอบนี้
3. **ไม่มีจดหมายค้างส่ง COO** — ไม่มีอะไรเกินอำนาจรอบนี้
