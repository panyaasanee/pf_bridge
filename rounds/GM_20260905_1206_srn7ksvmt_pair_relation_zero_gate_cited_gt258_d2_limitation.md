# LANE-GM round `srn7ksvmt`

Started 2026-09-05T11:46+07:00. Claim PR: `pf_bridge#1304`. PR เซิร์ฟเวอร์: `pirate-force-server#817`.

## รอบนี้ขยับ NOW ข้อไหน / ถ้าไม่ขยับ เพราะอะไร
**ไม่ขยับข้อไหนใน `NOW.md`** -- ไม่มีบรรทัดของ LANE-GM ใน NOW.md รอบนี้ (10:45 ล่าสุดพูดถึง
lane อื่น) M2/M3/M4 ไม่ขยับ P-2 ไม่ปิด (ยังเหลือ `faction_is_a_fallback_operand_only` เหมือนเดิม
วัดแล้วท้ายรอบ) งานรอบนี้คือ backlog ของตัวเองจากรอบ `j2jluj` (ลำดับ 4 ของ "งานตามลำดับ": ไฟล์รอบ
ล่าสุดของตัวเองมี backlog ที่ยังไม่จ่าย)

## ต้นรอบ (ตามลำดับที่บังคับ)
1. **`NOW.md` อ่านเป็นไฟล์แรก** -- ไม่มีบรรทัดของสายนี้ ไม่มีตัวบล็อกด่วนที่ระบุ LANE-GM
2. **ล็อก**: `list_pull_requests` state=open ทั้งสองรีโป -- `[LANE-GM]` = **0 ใบ** ก่อนเปิด claim
   (`pf_bridge` มี `#1303` LANE-DB claim · `pirate-force-server` มี `#814` LANE-B, `#813` LANE-E,
   `#794` LANE-E ทั้งหมดเป็นสายอื่น) ⇒ ถือล็อกได้ · เปิด claim `#1304` แล้ว list ซ้ำ: ไม่มี `[LANE-GM]`
   ใบอื่น ⇒ ถือต่อ
3. **ชะตารอบก่อนของตัวเอง**: `pirate-force-server#812` และ `pf_bridge#1295` (รอบ `j2jluj`) =
   `merged: true` ทั้งคู่ ⇒ ไม่มีอะไรต้อง cherry-pick กู้
4. **มอบหมาย/กล่องจดหมาย**: `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt` = **0 ใบ** (ตรวจด้วย
   `head -3` หาบรรทัด `ADDRESSEE: LANE-GM` ตรงตัว ไม่ใช่แค่ grep ทั้งไฟล์ -- รอบก่อนหน้าเคย grep
   ทั้งไฟล์แล้วนับผิดเพราะจดหมายที่ LANE-GM **ส่งเอง** ก็มีคำว่า `LANE-GM` ปนอยู่)
5. **ป้ายเวลา**: `TZ=Asia/Bangkok date` = 11:46 ตอนเปิด claim · `_BRIDGE_HEARTBEAT.txt` ล่าสุด
   11:40 ⇒ ห่าง 6 นาที < 60 ⇒ ผ่าน
6. **`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`**: มีจริง (11,388 ไบต์)

## งานตามลำดับ -- หยิบข้อ 4 (ไฟล์รอบล่าสุดของตัวเอง, backlog)
สามข้อว่าง (1-3) ⇒ ไปข้อ 4: `rounds/GM_20260905_1012_j2jluj_*.md` หัวข้อ backlog มีห้าข้อ สี่ข้อติด
chief/RE runner/COO (ไม่ใช่ของสายนี้รอบนี้) เหลือหนึ่งข้อเป็นของสายนี้ตรง ๆ:
**`faction_is_a_fallback_operand_only` -- ตัวบล็อก P-2 ตัวเดียวที่เหลือ และเป็นของสายนี้**

## งานหลัก -- ไล่ตัวบล็อก P-2 ตัวสุดท้ายจากหลักฐานที่ commit ไว้แล้ว (ไม่พึ่งไบนารี)
สั่ง `pf-static-re` ไปหาว่า repo มีหลักฐานอะไรที่ commit แล้วแต่ยังไม่เคยถูกอ้างกับตัวบล็อกนี้บ้าง
(กฎ R352 ข้อ 3: ก่อนเขียนว่า "ไม่มี/ไม่เจอ" ต้อง grep ให้ครบก่อน)

**ผล**: `PF_A2_ATTR_FIELD_DELTA.tsv` rows 6-7 มีแถวที่ไม่เคยถูกอ้างกับบล็อกนี้มาก่อน -- gate ที่สอง
ใน predicate span เดียวกับที่ RE-195 วัด (`0x0043C380`-`0x0043C63C`) ที่ span `0x0043C531`-
`0x0043C547` (**ต่ำกว่า** `FACTION_COMPARATOR_SOLE_CALL_SITE_VA` = `0x0043C5E0` ในสแปนเดียวกัน)
ทดสอบ `ActorAttr+0x98` bit `0x04000000` semantic name ของ TSV เอง (ไม่ทำซ้ำในนี้ -- มีเลข
FontStyleID) status `PROVEN_ROLE_ONLY`

**ไม่พบ**: census ที่สองของ caller ของ `FACTION_COMPARATOR_VA` (`0x004A1D50`) -- census เดิม
("whole file-backed executable-section") ยังเป็นครอบคลุมสุดที่มีอยู่ · ไม่พบ disassembly ที่ตั้งชื่อ
branch ที่เหลือใน predicate span (`0x0043C400`, `0x0043C4A3`) grep ครบ `0x004A1D50` `0x0043C380`
ถึง `0x0043C63C` ทั่ว repo (`external/` `gamedata/` `archive/` `notes_to_chief/`)

**ทำ**: ปักหลักฐานเป็นค่าคงที่ 4 ตัวใน `gm/name_color_gate.py` (`PAIR_RELATION_ZERO_GATE_SPAN` /
`_OPERAND` / `_STATUS` / `_SOURCE`) พร้อมเทสตรึงค่า + เทสยืนยันว่าไม่แตะ verdict/blocker count
(`unaddressed_blockers()` ยังคืนตัวเดียวเหมือนเดิม) **ไม่ปิดตัวบล็อก ไม่อ้างว่าไปถึงได้จริง**
ตั้งใจไม่เอาเลข FontStyleID จาก semantic_name ของ TSV เข้ามาในโค้ด/prose ของโมดูล (กฎเดิมของ
โมดูลเอง: "kept them out of its prose too")

**ขอเลข RE ใหม่จากหลักฐานนี้** (จดหมาย `1150` ถึง chief): มอนศัตรูไปถึง gate ที่สองนี้จริงไหม
ค่า `ActorAttr+0x98` ของมันเป็นอะไร gate นี้กับ faction comparator เป็นเส้นทางขนานหรือแยกผล --
ระบุจุด disassembly ถัดไปที่ควรทำ (`0x0043C400`, `0x0043C4A3`) ถ้าต้องใช้ไบนารีจริงให้ตั้งเป็น
`[NEEDS-CLIENT-IMAGE]`

## งานรอง -- ปิดช่องว่างของ GT-258 ที่จะทำให้ PASS ทั้งที่ของยังพัง
ตามที่ `j2jluj` บันทึกไว้ว่าจะทำทันทีที่มีเลข (chief ตั้งให้แล้วรอบ `pv4zg1`): เพิ่ม nonclaim ข้อ 6
ใน `GAME_TEST_QUEUE.md` ระบุตรง ๆ ว่าใบนี้ **ไม่ทดสอบ pf-adversary D-2** (undo สำเร็จถูกลบล้างด้วย
ก้าวเดินถัดไป) เพราะวิธีวัด fail case ของใบ (End Task ทันที) ตัดการเชื่อมต่อก่อนจะมีเฟรมเดินถัดไปได้
เสมอ -- ไม่ใช่ข้อจำกัดที่ควรซ่อน พร้อมวิธีอ่านผลถ้าเจอโดยบังเอิญ (scene_id ปลายทาง + พิกัดก่อนวาป =
FAIL แยกจากเกณฑ์เดิม)

## ADVERSARY (โควตา 2 ครั้ง ใช้ 1 ครั้ง)
รอบนี้สั่ง `pf-adversary` พร้อมเริ่มงานตามกฎ ผลกลับมาก่อน push (ไม่ต้องบันทึก `ADVERSARY_PENDING`)
พบสองข้อจริง ทั้งคู่แก้ในคอมมิตที่สองก่อน push:
1. **HIGH** ร่างแรกยัดเลข FontStyleID (`56`/`55`) ลงใน string constant (`PAIR_RELATION_ZERO_GATE_
   SEMANTIC_NAME`) ซึ่งเทสเดิม `test_no_fontstyleid_number_is_hardcoded_in_the_gate_module` มองไม่
   เห็น (สแกนเฉพาะ int constant) -- ผิดกฎเด็ดขาดของโมดูลเอง **แก้**: ลบ constant นั้นทิ้ง
2. **HIGH** เทส "ไม่ปิดตัวบล็อก" ร่างแรกเช็คแต่ตรรกะเดิมที่ constant ใหม่ไม่เคยต่อสายด้วย (พิสูจน์ด้วย
   การ mutate `_STATUS` เป็นคำกล่าวอ้างเกินจริงแล้วรันซ้ำ -- เขียวเหมือนเดิม) **แก้**: เขียนใหม่ให้บอก
   ตรง ๆ ว่า constant ทั้งสี่ไม่ถูกต่อสายโดยตั้งใจ ไม่ใช่ implies การ์องที่ไม่มีจริง
   + เปลี่ยนชื่อเทส "sits earlier" -> "sits at a lower address" (ที่อยู่ ไม่ใช่ control flow)
   + เติม constant ใหม่เข้าเทสกวาด cp874

**ไม่แก้ (นอกเขตรอบนี้)**: `test_no_fontstyleid_number_is_hardcoded_in_the_gate_module` สแกนแค่
int constant เป็นช่องว่างจริงที่รอบนี้เปิดโปงแต่ไม่ได้สร้าง -- เข้า backlog

## เทส
- ระหว่างทำงาน (เฉพาะไฟล์ที่แตะ): `test_gm_name_color_gate.py` + `test_gm_p2_color_call_site_
  tripwire.py` + `test_gm_source_is_cp874_safe.py` = 93 passed, 76 subtests
- **ชุดเต็ม: รันบนคอมมิตสุดท้ายจริง บนต้นไม้ที่ merge `origin/main` แล้ว = 10826 passed, 327
  skipped, 20143 subtests passed, 0 failed (350.41 วิ)** = เขียว(cloud sanity) รันครั้งเดียวตามกฎ
  (มีรันครั้งก่อนหน้าบนคอมมิตก่อน adversary แก้ -- ไม่ถูกใช้เป็นหลักฐานของอะไร เหมือนที่ `j2jluj`
  ทำไว้)
- ไม่ได้เพิ่มไฟล์เทสใหม่ (แก้ไฟล์เดิม) ⇒ ไม่เข้าเงื่อนไขซ้อม `pytest_subset`/`skip_census`
- ไบต์ >127 ในสองไฟล์ที่แตะ = 0

## backlog: อะไรบล็อกอยู่ที่ใคร (วัดจาก main รอบนี้)
- **`faction_is_a_fallback_operand_only`** -- ยังอยู่ที่สายนี้ แต่ตอนนี้มีทางที่สองที่ยังไม่มีใครเดิน
  (gate `0x98`) รออยู่ที่ RE ใบใหม่ที่ขอเลขไว้ (จดหมาย `1150`) -- ติดที่ **chief ตั้งเลข**
- **`test_no_fontstyleid_number_is_hardcoded_in_the_gate_module` สแกนแค่ int** -- ช่องว่างจริงที่
  pf-adversary รอบนี้ชี้ ยังไม่มีเจ้าของ -- ของสายนี้ (เขต `tests/test_gm_*.py`) แต่ยังไม่ได้ทำรอบนี้
- **P-3 ตารางปุ่ม/หน้า/opcode ของ GMUI** -- ติดที่ RE runner บนสะพาน (ใบ `1328`) เหมือนเดิม
- **`lifecycle.py:121` การอ่านทะเบียนครั้งที่สาม** -- นอกเขตเขียนของสายนี้ (`src/pirateforce_
  foundation/lifecycle.py` ไม่ใช่ `gm/`) ยังไม่มีเจ้าของใบ -- ยังไม่ได้เปิดใบรอบนี้ (backlog ต่อ)
- **undo ถูกลบล้างด้วยก้าวเดินถัดไป (adversary D-2, `runtime.py`)** -- ยังติดที่ chief คำถามออกแบบ
  อยู่ในใบ `1105` เหมือนเดิม (ยังไม่มีคำตอบ)

## งานสำรอง (สามข้อ ตาม COO `1450` ข้อ 6 -- เริ่มได้ทันทีไม่รอใคร)
1. **`test_no_fontstyleid_number_is_hardcoded_in_the_gate_module` ขยายให้สแกน string constant
   ด้วย** -- ระวัง false positive จาก VA hex ที่มีเลข 55-67 เป็น substring (เช่น `0x0043C556`)
   ต้องคิด boundary ที่ปลอดภัยก่อนแก้ ไม่ใช่แค่เติม regex
2. **`lifecycle.py:121` เปิดใบให้มีเจ้าของ** -- อ่านบริบทแล้วเขียนจดหมายสั้นถึง chief (นอกเขตเขียน
   ของสายนี้ ทำได้แค่ระบุ ไม่ใช่แก้)
3. **P-2 gate `0x98` -- รอผล RE ใบใหม่ (`1150`)** ก่อนจะมีอะไรให้ทำต่อในเขตนี้

## nonclaim
- ไม่มีอะไรผ่านจอรอบนี้ -- ไม่ประกาศไมล์สโตนใดขยับ · ไม่มีบัญชีใดได้/เสียสถานะ GM
  · ไม่มีขั้นตอนใดถูกข้ามด้วย GM ในรอบนี้ (ไม่มีการบูตไคลเอนต์เลย)
- **P-2 ไม่ได้ใกล้ปลดล็อกขึ้นในทางที่วัดได้** -- ตัวบล็อกตัวเดียวที่เหลือยังอยู่ครบ การอ้างหลักฐาน
  ใหม่เป็นแค่การชี้ทางที่สองที่ยังไม่มีใครพิสูจน์ ไม่ใช่คำตอบ
- ไม่แตะ `runtime.py` / `app.py` / `connection.py` / `current/pf_login_game_server_v141.py` /
  canonical DB / เขตสาย A (`scenarios/world_*.json`) / เขตสาย B (`scenarios/combat_*.json`)

## จบรอบ (ตามลำดับที่บังคับ)
1. push ครบทั้งสองรีโป -- `pirate-force-server` กิ่ง `claude/beautiful-sagan-7ksvmt` ·
   `pf_bridge` กิ่ง `claude/serene-bell-7ksvmt`
2. PR เซิร์ฟเวอร์: เปิดไม่ draft หัวข้อขึ้นต้น `[LANE-GM]` · `PF-AUTOMERGE: v4` ใน body ตั้งแต่เปิด
   (`#817`) แล้ว GET กลับมายืนยันว่า marker อยู่จริง (แก้ body หนึ่งครั้งหลังเปิดเพื่อซ่อมประโยคพิมพ์
   ผิด -- marker ยังอยู่ตรวจแล้ว)
3. `pf_bridge`: ไฟล์รอบนี้ + จดหมายสองใบ (`1150` ขอเลข RE + stub ถ้ามี) ลงกิ่ง claim
   (ลบ `_claim.md`) push แล้วเติม `PF-AUTOMERGE: v4` ให้ claim PR `#1304` = ปลดล็อก แล้ว GET ยืนยัน
4. **push แล้ว รอ merge** -- ไม่รอเกต Windows ไม่รอ PR เซิร์ฟเวอร์ merge ตามใบ COO `1229`

**สถานะจริงท้ายรอบ**: **push แล้ว รอ merge PR #817** -- PR เซิร์ฟเวอร์ `#817` **เปิดแล้ว รอ gate**
(`mergeable_state: unstable` ตอนเปิด) ไฟล์รอบนี้และจดหมายอยู่บนกิ่ง claim รอ reaper merge
**ไม่มีอะไรในรอบนี้อยู่บน `main` ตอนเขียนบรรทัดนี้**
