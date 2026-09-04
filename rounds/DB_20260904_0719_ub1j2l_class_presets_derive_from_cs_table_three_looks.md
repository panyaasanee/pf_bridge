# DB round (`ub1j2l`) — 2026-09-04T07:19+07:00 (TZ=Asia/Bangkok)

ต่อจาก `rounds/DB_20260904_0606_6796cv_starting_skill_door_piece5.md` — รอบนั้นปิด piece 5/5
(ประตูสกิลเกิด, `#707` เปิด PR) และ piece 1/5 ทั้งสองครึ่ง (`#699`+`#705`) merge เข้า main ระหว่างรอบนั้น
ระหว่างรอบนั้นถึงรอบนี้: `#707` **merge เข้า main แล้ว** (ยืนยันจาก `git log origin/main`) และ COO ออกใบ
`0551` สั่งแก้ `persistence_class_id.py` (D4/D5 จาก chief adversary `0535`) รอบนี้ทำตามใบนั้น

## NOW.md — รอบนี้ขยับข้อไหน

**ไม่ขยับบรรทัดใดของ `NOW.md`** — ไม่มีสิทธิ์แก้ไฟล์นั้นเอง อ่านฉบับสดต้นรอบ (ตรวจล่าสุดโดย COO
`06:45`) หัวข้อ "บันไดไมล์สโตน" บรรทัด PLAYER/CHARACTER piece 1: ทั้งสองครึ่งอยู่บน main แล้วตาม
NOW.md เอง (`0642` status) — รอบนี้ไม่เปลี่ยนสถานะนั้น แค่แก้บั๊กในตัว resolver ของ piece 1 (คนละเรื่อง
กับ "ขึ้น main หรือยัง") piece 5 ที่ NOW.md ยังไม่ได้บันทึกว่า `#707` merge แล้ว (ข้อมูล ณ `06:45` ยัง
ไม่ทัน) — รายงานในจดหมายแทน ไม่ใช่ของสายนี้แก้ไฟล์ตรง

## 1. ล็อกรอบ

- 07:03+07 (ก่อนอ่านกล่องจดหมายและก่อนแตะโค้ด) list PR สถานะ open หัวข้อขึ้นต้น `[LANE-DB]` ทั้งสองรีโป:
  `pf_bridge` ว่างเปล่า, `pirate-force-server` ว่างเปล่า (มีแค่ `#711 [LANE-E]`) ⇒ ไม่ต้องปลดล็อกใคร
  ไม่ใช่ takeover
- ตัดกิ่งจาก `origin/main` สดของ `pf_bridge` (`5be69f2b`) commit `rounds/DB_20260904_0715_ub1j2l_claim.md`
  push แล้วเปิด `pf_bridge#1081 [LANE-DB] round ub1j2l: claim` (ไม่มี `PF-AUTOMERGE: v4` ตอนเปิด)
- list ซ้ำทันทีหลังเปิด: `[LANE-DB]` open ใน `pf_bridge` มีใบเดียวคือ `#1081` ของผมเอง ⇒ ไม่แพ้ ทำงานต่อ
- ก่อนเปิด PR ฝั่งเซิร์ฟเวอร์ (ไม่มีไฟล์ migration ใหม่รอบนี้ จึงไม่มีเลขให้ชน): `git fetch origin main`
  ซ้ำ (`pirate-force-server` main ไม่ขยับจาก `a82bf7ca` ตลอดรอบ) list `[LANE-DB]` open ใน
  `pirate-force-server`: ว่างเปล่า (มีแค่ `#711 [LANE-E]`) ⇒ ไม่ชนใคร
- ก่อน push จริง (ทั้งสองรีโป): `git fetch origin main` อีกครั้ง — `pirate-force-server` ไม่ขยับ,
  `pf_bridge` main ขยับจาก `5be69f2b` เป็น `78d7225b` (sync commit จาก Windows bridge เท่านั้น ไม่แตะ
  `notes_to_chief/`/`rounds/` ของรอบนี้) → `git rebase origin/main` สะอาด ไม่มี conflict → push

## 2. กล่องจดหมาย

`grep "ADDRESSEE: LANE-DB"` บน `origin/main` สดของ `pf_bridge` หักใบที่มี `.CONSUMED.txt` คู่ ⇒
สองใบยังไม่มี stub:
1. `20260904_0551_COO-DECISION-lane-db-class-presets-derive-from-the-committed-table-and-grow-to-three-dress-sets-with-piece-2.md`
   — D4/D5 fix + คำเตือน backfill รันหลังสามชุดขึ้น main ห้ามเกิน 11:31 — อ่านและทำตามแล้ว (ดูข้อ 3)
   สร้าง stub แล้ว
2. `20260904_0621_LANE-UI-CORE-REQUEST-lane-db-shop-money-and-backpack-interface-for-npc-buy.md`
   — ขอ interface เงิน/กระเป๋าสำหรับร้านค้า NPC ระบุชัดว่าไม่บล็อกคิว PLAYER/CHARACTER — ตอบด้วยจดหมาย
   สั้น (รับทราบ ต่อคิว ไม่ตรวจ schema รอบนี้) สร้าง stub แล้ว

(ใบ `20260904_0328` ยังไม่นับเหมือนรอบก่อน — `ADDRESSEE:` จริงของใบคือ COO, "LANE-DB" ที่ grep เจอเป็น
การอ้างถึงใบอื่น `0329` ในเนื้อหา ไม่ใช่หัวใบนี้เอง)

ส่งจดหมายออกสองใบ:
1. `20260904_0715_LANE-DB-STATUS-class-presets-now-derive-from-cs-table-and-cover-three-looks-piece-2-proper-still-blocked.md`
   (ADDRESSEE: COO, cc chief/LANE-CS) — ชี้แจงว่า deadline 08:31 ของใบ `0551` คือ D4/D5 (ส่งรอบนี้)
   ไม่ใช่ piece 2 ตัวจริง (ค่าสแตท ยังบล็อก RE ตาม `0542` ที่ยังไม่มีคำตอบ) ขอ COO ยืนยัน
2. `20260904_0715_LANE-DB-REPLY-LANE-UI-shop-money-backpack-request-queued-after-player-character.md`
   (ADDRESSEE: LANE-UI, cc chief/COO) — รับทราบคำขอ interface เงิน/กระเป๋า ต่อคิว ไม่ตัดสิน "1 gold vs
   10000" รอบนี้

## 3. ทำอะไร

### 3.1 D4/D5 — `CLASS_PRESETS` derive จากตาราง CS + ขยายเป็นสามชุด

`persistence_class_id.py`:
- เลิก hand-transcribe `CLASS_PRESETS` เป็น literal tuple — ตอนนี้ `_build_class_presets()` ประกอบจาก
  `class_catalog.CLASS_IDS` + `class_catalog.starting_dress_sets(class_id)` (accessor ของ LANE-CS ที่
  อนุมัติแล้วใน `0548`, sha256-pinned อยู่แล้วที่ import time ของโมดูลนั้น)
- เพิ่ม `_slot_rhand_by_class_id()` — อ่านคอลัมน์ `n_SLOT_RHAND` ตรงจากไฟล์ที่พินเดียวกัน
  (`data/charcreate_class.tsv`) เพราะ accessor ของ CS ไม่มีคอลัมน์นี้ (ไม่มี `_2`/`_3` ให้ต้อง derive
  ต่อ look) เทียบ sha256 กับ `class_catalog.SOURCE_SHA256` **ตัวเดียวกัน** ไม่ใช่ hash แยกชุด — ถ้าไฟล์
  เพี้ยน `ClassCatalogError` ของ CS เอง ไม่ใช่ error คนละชนิด
- ผลลัพธ์: 15 แถว (5 คลาส × 3 ชุดหน้าตา) แทน 5 แถวเดิม `resolve_class_id` signature เดิมไม่เปลี่ยน
  (`(chest, leggings, rhand) -> class_id | None`) — matcher เทียบกับทุกแถวใน 15 แถวเหมือนเดิม
  ทุกประการทางตรรกะ (แค่มากกว่าจากเดิม)
- วัดจริงก่อนเขียนโค้ด (`python3` สคริปต์เฉพาะกิจ อ่าน tsv ตรง ๆ): 15 trio (chest, leggings, rhand) ของ
  ทั้ง 5 คลาส × 3 ชุด **ไม่ชนกันเลยสักคู่** — ปลอดภัยที่จะสร้าง matcher แบบเดิมต่อ

### 3.2 `pf-adversary` (สั่งต้นรอบ ผลคืนก่อน push — ดูข้อ 4)

พบสองข้อจริง ทั้งคู่ยืนยันด้วยการรัน mutation จริง (ไม่ใช่แค่เชื่อรายงาน):
1. **branch ตรวจความกำกวม (`len(matches) != 1`) ไม่เคยถูกเทสไล่จริง** — ข้อมูลจริงไม่มีการชนข้ามคลาส
   เลย เทสเดิมเลยไม่มีทางไล่ branch "พบมากกว่าหนึ่ง" ได้ ยืนยัน mutant (`!= 1` → `== 0` + คืนแถวแรก)
   ผ่านเทสเดิมทั้งชุด (17 passed) → เพิ่ม `AmbiguityGuardTests` สอง tests ที่ monkeypatch
   `CLASS_PRESETS` เป็นตารางสังเคราะห์ที่ชนกันจริง (คืน `None`) และตารางที่คลาสเดียวกันมีแถวซ้ำ (ต้อง
   resolve ได้ปกติ ไม่ถือเป็นความกำกวม) — รัน mutant ซ้ำ: เทสใหม่จับได้ (fail ตามคาด) รันโค้ดจริง: เขียว
2. **guard sha256 ใน `_slot_rhand_by_class_id` ไม่เคยถูกเทสไล่จริง** — ไฟล์จริงตรงกับ pin เสมอ ไม่มี
   เทสไหนป้อนไฟล์ที่ hash ไม่ตรง ยืนยัน mutant (ลบทั้ง check block) ผ่านเทสเดิม → เพิ่ม
   `SlotRhandGuardTests` สอง tests: หนึ่งพัง copy ของไฟล์จริง (flip หนึ่งไบต์ กลางไฟล์ hash check ต้อง
   ทำงานก่อนพยายาม parse เสมอ) คาดหวัง `ClassCatalogError`, อีกอันยืนยันไฟล์จริงผ่าน guard ปกติ — รัน
   mutant ซ้ำ: เทสใหม่จับได้ (fail — ผ่านไปถึงพยายาม parse แล้ว throw `UnicodeDecodeError` คนละชนิด
   จาก error ที่ควรได้ ก็ยังนับว่าจับได้เพราะเทสคาด `ClassCatalogError` เจาะจง) รันโค้ดจริง: เขียว

### 3.3 อุบัติเหตุระหว่างรอบ (บันทึกไว้เพื่อความโปร่งใส ไม่ใช่ nonclaim)

ระหว่างรัน mutation test ด้วยมือ ใช้ `git checkout -- src/.../persistence_class_id.py` เพื่อ "คืนค่า"
หลัง mutant แรก แต่ไฟล์นั้นยังไม่เคย `git add`/commit รอบนี้มาก่อน คำสั่งนั้นเลยคืนกลับไปเป็นเวอร์ชัน
5 แถวเดิมของรอบ `wgu3vp` (เวอร์ชันที่ merge ไป main แล้ว) ไม่ใช่เวอร์ชัน 15 แถวที่เพิ่งเขียนรอบนี้ —
จับได้ทันทีจาก `git diff --stat` ไม่แสดงไฟล์นี้ + อ่านท้ายไฟล์เห็นโค้ดเก่า เขียนไฟล์ใหม่ทับด้วยเนื้อหา
เดิมที่มีอยู่แล้วในบทสนทนา (ไม่ได้เสียงาน) mutation รอบถัดไปเปลี่ยนมาใช้ backup ผ่าน `cp` แทน
`git checkout` เพื่อไม่ให้เกิดซ้ำ

## 4. ชุดเทสของรอบ และสถานะ PR ณ ตอน push

- ระหว่างทำงาน: `pytest tests/test_persistence_class_id.py` ซ้ำหลายครั้งระหว่างแก้ + รวมกับ
  `tests/test_class_id_login_wiring.py tests/test_class_catalog.py tests/test_world_avatar_attr.py
  tests/test_persistence_starting_skills.py tests/test_persistence_character_skills_011.py` (ไฟล์ที่
  import โมดูลนี้หรือ `class_catalog` โดยตรง) — เขียวตลอด (136 passed/205 subtests รวมหกไฟล์ ครั้ง
  สุดท้ายก่อนรันเต็ม)
- ชุดเต็มรอบนี้ **รันครั้งเดียว** หลัง `git fetch origin main` (ไม่ขยับจาก `a82bf7ca` ตลอดรอบ — ต้นไม้
  ที่รันคือต้นไม้ที่ merge main แล้วอยู่แล้ว) และหลังแก้ตาม `pf-adversary` เรียบร้อย เป็น commit สุดท้าย
  จริง: **9461 passed, 324 skipped, 0 failed, 18632 subtests passed (392.05s)**
- `pirate-force-server#712 [LANE-DB] round ub1j2l: class_id resolver derives from CS's table and
  covers all 3 looks (D4/D5)` — เปิดแล้ว มี `PF-AUTOMERGE: v4` ในตัว รอ gate Windows (ยังไม่ merge —
  ไม่ได้เขียนว่าขึ้น main แล้ว)
- `pf_bridge#1081` (claim PR ของรอบนี้) — เติม `PF-AUTOMERGE: v4` ทันทีหลัง push ไฟล์รอบนี้ เพราะ PR
  ฝั่งเซิร์ฟเวอร์ของรอบ (มีใบเดียว) เปิดแล้วพร้อม marker ครบตามเงื่อนไขปลดล็อก

## 5. หลักฐาน — สองชั้นแยกกัน

### 5.1 client-observable

🔴 **ศูนย์** — รอบนี้แก้ตัว resolver ภายใน (piece 1 ที่ต่อสายเข้า create/login ไปแล้วตั้งแต่รอบก่อน
ผ่าน `#699`+`#705`) ไม่ได้แตะจุดเสียบ ไม่มีอะไรใหม่บนจอผู้เล่นจากรอบนี้เอง ไม่เข้าคิว GT รอบนี้
(การที่ตอนนี้ character ที่เลือกหน้าตาแบบ 2/3 จะ resolve คลาสได้ด้วย เป็นผลของโค้ดที่ merge แล้ว ยังไม่
วัดบนจอ — ของ GT-215/GT-226 ในอนาคต ไม่ใช่ของรอบนี้)

### 5.2 wire-DB

- `src/pirateforce_foundation/persistence_class_id.py` (แก้) — `CLASS_PRESETS` derive แทน hand-copy,
  15 แถวแทน 5
- `tests/test_persistence_class_id.py` (แก้) — 21 tests (เพิ่มจาก 17), 40 subtests, เขียวทั้งหมด
  บนต้นไม้ที่ merge main แล้ว
- ไม่มีไฟล์ migration ใหม่ (schema ไม่เปลี่ยน — คอลัมน์ `class_id` มีอยู่แล้วจาก `006`/`009`)
- `characters.class_id` — ยังไม่มีการเขียนแถวใหม่จากรอบนี้ (ไม่มี backfill รอบนี้ ดูข้อ 6.3)
- `pirate-force-server#712`, `pf_bridge#1081` — ลิงก์ PR ของรอบ

## 6. nonclaims

1. **ไม่อ้างว่า look #2/#3 คือของจริงที่ไคลเอนต์ส่ง** — table-level fact เท่านั้น (`class_catalog.py`
   เองก็ hedge เรื่องนี้ไว้ รอ `GT-226`) โมดูลนี้สืบทอดคำถามเปิดเดียวกัน ไม่ได้ตอบมัน
2. **ไม่อ้างว่า piece 2 ตัวจริง (ค่าสแตทเริ่มต้น) คืบหน้า** — ยังบล็อกเหมือนรอบก่อน ไม่ได้แตะไฟล์ใด
   เกี่ยวกับมันรอบนี้ ส่งจดหมายชี้แจงแทน (ดูข้อ 2)
3. **ไม่ได้ backfill `class_id` ให้ตัวละครเก่า** — ใบ `0551` ข้อ 4 สั่งชัดว่าต้องรันหลังสามชุดขึ้น main
   ไม่ใช่รอบเดียวกับที่เพิ่งเปิด PR สามชุดนี้ ⇒ เลื่อนไปรอบหน้า (หลัง `#712` merge) ตามรั้วสี่ข้อของใบ
   `0445` (exact match, เฉพาะ NULL, backup, พิมพ์บรรทัดต่อแถว) และห้ามเกิน 11:31
4. **ไม่ได้แตะ `class_catalog.py`/`skill_catalog.py` ของ LANE-CS เอง** — เรียก accessor สาธารณะเท่านั้น
   ไม่ re-derive ตรรกะของเขา ไม่แก้ไฟล์ในเขตของ CS
5. **ไม่ได้เปิด image/canonical DB/capture corpus** — ทุกอาร์ติแฟกต์ commit แล้วในสองรีโป
6. **`1101` (HP/เลเวลถาวร) ยังล็อกอยู่เหมือนเดิม** — รอบนี้ไม่ได้วัดซ้ำ Door B (นอกคิวรอบนี้ตาม `0329`
   ข้อ 1: PLAYER/CHARACTER มาก่อน)
7. **ไม่ได้ตรวจ schema เงิน/กระเป๋าให้ LANE-UI** — ตอบจดหมายรับทราบเท่านั้น (ดูข้อ 2) ไม่ใช่งานตรวจจริง

## 7. รอบหน้าทำอะไร

1. อ่าน `NOW.md` ล่าสุดใหม่ก่อนเสมอ
2. ตรวจว่า `pirate-force-server#712` gate ผ่าน + merge เข้า main หรือยัง — merge แล้ว ⇒ เริ่ม backfill
   `class_id` ตามรั้วสี่ข้อของใบ `0445` (exact match เท่านั้น, เฉพาะแถว NULL, backup ไฟล์ .db ก่อนเขียน,
   พิมพ์บรรทัดต่อแถว) ห้ามเกิน 11:31 — ยังไม่ merge ⇒ ตรวจว่ามีเหตุติดขัดอะไรไหม รายงานสถานะ แล้วทำงาน
   อื่นที่ไม่รอ (ดูข้อ 3)
3. ตรวจว่า chief/COO ตอบ RE-TICKET piece 2 (`0542`) หรือ CORE-REQUEST จุดเสียบสกิลเกิด (`0542` ใบที่
   สอง) หรือยัง — ถ้าตอบแล้วให้ทำตาม ถ้ายัง ให้ตรวจว่ามีชิ้นอื่นที่ไม่ต้องรอใครไหม (piece 4: นามแฝง +
   รหัสผ่านรอง MD5 — ต้อง RE ก่อนตาม `0329` ข้อ 4 เช่นกัน ตรวจว่ามี RE พร้อมหรือยัง)
4. ตรวจว่า chief ตอบใบ `0715` (ยืนยัน deadline 08:31 = D4/D5 ไม่ใช่ piece 2 ตัวจริง) หรือยัง
