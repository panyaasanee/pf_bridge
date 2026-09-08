# GAME_TEST_QUEUE archive — closed 2026-09-08 (moved by LANE-K round 0511)

## GT-262 STALL-AND-GUILD-STORAGE-ATTENDED-CAPTURE-001  [🟢 **READY -- เนื้อใบเต็มลงแล้วโดยเจ้าของใบ (LANE-UI)** · สถานะเปลี่ยนจาก `PENDING` (เลขจองไว้ เนื้อยังว่าง) → `READY` เพราะเนื้อใบมาครบแล้ว (รูปแบบเดียวกับ `GT-230` ที่พลิกจาก `PENDING`→`OPEN` รอบ `ziuhft` เมื่อ LANE-UI เติมเนื้อใบเอง) · คู่กับ `RE-261 STALL-AND-GUILD-STORAGE-FIELD-SEMANTICS-FROM-A-REAL-SESSION-001` (`CLIENT_RE_QUEUE.md:5607`) ตาม `AGENTS.md` §7 (`COO-DECISION 20260904_2142` ข้อ 3: ผล RE ที่ขอ attended capture ⇒ ผู้บริโภคผลเปิดใบ GT รอบเดียวกัน) · เลขตั้งโดย chief (LANE-E) รอบ `pv4zg1`/R352 · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-UI** · ผู้รัน = Panya (attended) · **ต่อท้ายคิว "รอเครื่องคุณ" ไม่ใช่หัวคิว** · ไม่บล็อกใคร · ไม่มีการตีมอน · 🔴 **[LANE-K รอบ `kxpzxi` 2026-09-07T03:15+07:00] ถอนออกจาก `QUEUE_STATUS_SNAPSHOT.md` ชั่วคราว ตาม `PANYA-ORDER 20260907_0159` ข้อ 2** (หน้าที่คัดใบ attended ที่ไม่จำเป็น PANYA `2148` ย้ายมาอยู่กับ LANE-K): ใบนี้เข้าเกณฑ์ (ก) **อายุ >7 วัน** (เปิด 2026-08-25 = 13 วัน) และเป็นหนึ่งใน ใบที่เจ้าของยกเป็นหลักฐานในคำสั่งเอง · **K ยกเลิกใบเองไม่ได้ (พับ=คัดลอก)** — ใบยังเปิดอยู่ทุกตัวอักษร ไม่มีอะไรถูกลบ · **เจ้าของใบ LANE-UI ต้องตอบกลับ: ยืนยันซ้ำว่ายังต้องบูตจริง (แล้ว K ใส่กลับรถบัส) หรือยกเลิกพร้อมเหตุผลตามกฎ PANYA `20260903_1934`** · จดหมายแจ้ง: `notes_to_chief/20260907_0315_LANE-K-CULL-3-tickets-off-bus-need-owner-reconfirm.md`]] [🚫 **CANCELLED โดยเจ้าของใบ LANE-UI รอบ `fvp9ke` 2026-09-07T04:56+07:00** — วางโดย LANE-K รอบ `rlapyk` 2026-09-07T06:11+07:00 · K ไม่ได้ยกเลิกเอง (พับ=คัดลอก) · จดหมาย `notes_to_chief/20260907_0456_LANE-UI-TO-K-gt262-cancel-with-reason.md` · บรรทัดของเจ้าของใบคำต่อคำ: "`GT-262` = ยกเลิก (CANCELLED BY OWNER) — K ไม่ต้องใส่กลับรถบัส" · เหตุผลคำต่อคำตามกฎ `PANYA 20260903_1934`: "ไม่มีกลไกให้ 'ติดอาวุธ' ในฉากเป้าหมาย ⇒ **ใบนี้ออก `HEADLESS_PROOF:` ไม่ได้เลยโดยโครงสร้าง** ไม่ใช่เพราะเจ้าของใบขี้เกียจเติม แต่เพราะยังไม่มีอะไรให้ headless พิมพ์ออกมา ... การยืนยันซ้ำจึงเป็นการถือที่นั่งบนรถบัสไว้เฉย ๆ ยกเลิกจึงตรงกว่าและซื่อสัตย์กว่า" · วัดซ้ำหน้างานที่เจ้าของใบยกมา: `grep -rn "Stall\|GuildStorage" src/pirateforce_foundation/ --include=*.py` = 0 hit · `StallOpenVital 0x2A3E`/`StallStartVital 0x30FE`/`StallOperateVital 0x3DE4` = `NAME-ONLY` · `GuildStorageOpenVital 0x5CAD`/`GuildStorageResultVital 0x70D0` = `UNTOUCHED` · **`RE-261` ยังเปิดอยู่ ไม่ได้ถูกยกเลิกไปด้วย** (คำของเจ้าของใบ) · nonclaim ที่ยกมาด้วย: เจ้าของใบไม่ได้อ้างว่า layout ที่รู้แล้ว = WIRED และไม่ได้แตะสถานะใบอื่นที่ K ถอน]

- ทำไมใบนี้ถึงมีอยู่: `RE-261` ปิดจาก static เดี่ยวไม่ได้ (จดหมายต้นทางของมันเองยอมรับ `[NEEDS-ATTENDED-CAPTURE]`) เพราะ opcode ของทั้งสองระบบมีจริงในไบนารีแต่ `external/PF_FIELD_VALIDATION.tsv` ทุกแถวเป็น `NOT_OBSERVED`/`serializer_status=OPEN` — ไม่เคยมีเฟรมจริงจากสองระบบนี้ในคลังแคปเจอร์เลยสักครั้ง · ตาม `AGENTS.md` §7 (`COO-DECISION 20260904_2142` ข้อ 3) ผลของมันต้องมีใบ GT คู่ในรอบเดียวกัน มิเช่นนั้น `RE-261` จะไม่มีวันถูกทดสอบ (ผู้เทสอ่าน `GAME_TEST_QUEUE.md` เท่านั้น ไม่เคยอ่าน `CLIENT_RE_QUEUE.md`) · ใบนี้คือใบนั้น

- objective (ข้ออ้างเดียว): ผูกสิ่งที่คนเห็นบนจอ — หน้าต่างแผงขายเอง/ช่องราคา/หน้าต่างคลังกิลด์/ช่องฝาก-ถอน — เข้ากับเฟรมและ opcode ที่ `RE-261` ระบุ (`StallStartVital 0x30FE` · `StallOpenVital 0x2A3E` · `StallOperateVital 0x3DE4` · `GCSS_GuildStorageOpenVital 0x8B66` · `GCGS_GuildStorageCmdVital 0x7F17`) โดยเรียงลำดับคำถามและด่านกั้นเดียวกับที่ `RE-261` บังคับไว้เป๊ะ (positive control ก่อนอย่างอื่นทั้งหมด) · **ใบนี้ตัดสินแค่ชั้น client-observable เท่านั้น** — คำตัดสินว่าไบต์ `+0x20` (`u32` tag `0x14` ของ `StallOperateVital` serializer `0x76A630`) แปลว่าราคาจริงหรือไม่ (สมมติฐาน chief round 75 · `archive/CHIEF_CONTINUATION_ARCHIVE_20260818_R77.md:64` + `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md:132` — **[เสนอ] ยังไม่ยืนยัน**) เป็นหน้าที่ของ `RE-261`/LANE-UI ไม่ใช่ของใบนี้

- 🔴 **สองสิ่งที่ยังไม่รู้จริง ณ วันเปิดใบ (ห้ามอ้างว่ารู้แล้ว) — ใบนี้คือใบสำรวจของทั้งสี่ข้อ**:
  ① **ไม่มีพิกัด/ชื่อ NPC หรือปุ่ม UI ตัวไหนที่เปิด "แผงขายเอง" ถูก pin ไว้ในคลังเลยสักตัว** — ใบนี้จึงเป็นใบ**ไล่คลิก** เหมือน `GT-230` P2 ไม่ใช่ใบที่บอกพิกัดตายตัว
  ② **ไม่มีพิกัด/ชื่อ NPC หรือปุ่ม UI ตัวไหนที่เปิด "คลังกิลด์" ถูก pin ไว้เช่นกัน** — ไล่คลิกแยกรอบสอง
  ③ **ไม่มีใครในโปรเจกต์นี้เคยเปิดแผงขายเองหรือคลังกิลด์สำเร็จบนเซิร์ฟเวอร์ของเราเอง (`pirateforce_foundation.app`)** — ไม่มี dispatcher ผูก opcode เหล่านี้ในโค้ดฝั่งเซิร์ฟเวอร์เลย (`external/PF_PROTOCOL_PRIORITY.tsv`: `serializer_status=OPEN` ทุกคลาส ไม่ใช่ `CLOSED`) ⇒ ใบนี้เป็นการทดลองล้วน ไม่ใช่การยืนยันฟีเจอร์ที่ทำงานได้แล้ว
  ④ **ไม่มีใครวัดว่าคลังกิลด์ต้องมีสังกัดกิลด์ก่อนหรือไม่** — ถ้าตัวละครทดสอบไม่มีกิลด์และหน้าต่างคลังเปิดไม่ได้ด้วยเหตุนั้น นี่คือผลลบที่ใช้ได้ (ดูผลลัพธ์ `E` ด้านล่าง) ไม่ใช่ใบล้ม

- 🔴 PRECONDITION ที่ต้องเช็คจริงก่อนขั้น 1:
  P1. **ไม่มีโค้ดฝั่งเซิร์ฟเวอร์จับ opcode กลุ่มนี้เลย** (ตรวจซ้ำหน้างานด้วย `git grep` ในขั้นตอนด่านก่อนบูตด้านล่าง) ⇒ ใบนี้เป็น**ใบเก็บ hex บวกภาพหน้าจอ** ไม่ใช่ใบตัดสินว่าธุรกรรมสำเร็จ (รูปแบบเดียวกับ `GT-230` — "เก็บ hex ไม่ใช่ใบตัดสินว่าขายสำเร็จ") · ไบต์ว่าง/ไม่มีเฟรมออกเลยก็เป็นผลที่ใช้ได้
  P2. **ไอเทมที่ใช้วางในแผง/ฝากคลังไม่ต้องหา — สร้างตัวละครใหม่หนึ่งตัว**: `SQLiteStore._insert_initial_backpack` (`pirate-force-server/src/pirateforce_foundation/store.py:674`, เรียกจาก `store.py:575`) ใส่ของ 4 ชิ้นจาก `INITIAL_BACKPACK` (`inventory.py:39-49`) ให้ทุกตัวละครใหม่เสมอ (`template_id 2600001` x2 ช่อง 0/2 · `2400901` ช่อง 1 · `2200002` ช่อง 3) ⇒ ใช้ตัวละครใหม่ตัวเดียวตลอดใบ ไม่ใช้ตัวเก่าที่เคยเทสอย่างอื่นมาก่อน จะได้ของที่รู้ต้นทางแน่ชัดทั้งสำหรับตั้งราคาในแผงและฝากคลังกิลด์ · ถ้ากระเป๋าตัวใหม่ว่างผิดจากนี้ ⇒ finding ของใบนี้เอง ลองตัวละครใหม่อีกตัว
  P3. **การคลิกตัวเลือก/NPC หนึ่งครั้งไม่จำเป็นต้องเปิดแผง/คลังทันที** — [ทำนายจาก `GT-230` P2/P3 ยังไม่ใช่ผลวัดตรงกับกรณีนี้]: `GT-230` วัดพฤติกรรมนี้กับ NPC ร้านค้าเท่านั้น ยังไม่เคยมีการคลิกอะไรเพื่อหา "แผงขายเอง" หรือ "คลังกิลด์" มาก่อนเลย ⇒ **ไม่ใช่ NPC/ปุ่มทุกตัวเป็นทางเข้าของสองระบบนี้** ต้องไล่คลิกหลายตัว/หลายเมนูจนกว่าจะเจอตัวที่เปิดหน้าต่างที่ถูกต้องจริง
  P4. **เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง เสมอ** (กฎเดียวกับ `GT-228`/`GT-230`) · ห้ามเปิดไคลเอนต์ทิ้งไว้โดยไม่มีเซิร์ฟเวอร์ (ตายเองใน ~3.5 นาที) · kill ไคลเอนต์แล้วเซิร์ฟเวอร์ยังถือเซสชันเดิม — ต้องรีสตาร์ตเซิร์ฟเวอร์ก่อนเปิดไคลเอนต์ตัวถัดไปเสมอ ไม่งั้นค้าง "connecting" ตลอดกาล
  P5. `-SecondPasswordMode bypass` (กฎเดียวกับ `GT-228`/`GT-230`) กันกล่องรหัสผ่านที่สองขวางถ้าแผง/คลังเรียกมัน — **ใบนี้ไม่ตัดสินพฤติกรรมรหัสผ่านที่สอง** เจอกล่องนั้นทั้งที่ตั้ง bypass ไว้ = finding แยก ไม่ใช่ใบล้ม

- db: canonical = `state\pirateforce.sqlite3` — 🔴 **สำเนาเท่านั้น ห้ามเปิด canonical** ⇒ คัดลอกเป็น
  `state\run_gt262_<yyyyMMdd_HHmmss>.sqlite3` แล้วบูตทับสำเนา (คัดลอกครั้งเดียวต่อรอบ เหมือน `GT-258`) ·
  sha256 canonical ก่อน/หลังต้องตรง `CANON_SHA.txt` · `PRAGMA integrity_check` = `ok` ทั้งสองครั้ง ·
  จด sha256 ของสำเนาก่อน/หลังด้วย

- server args: บูตมาตรฐาน · **ไม่มีแฟล็ก scenario ใด ๆ** · `-SecondPasswordMode bypass` ·
  🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)**
  ```
  py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
  git grep -n "StallStartVital\|StallOpenVital\|StallOperateVital\|GCSS_GuildStorageOpenVital\|GCGS_GuildStorageCmdVital" -- src/pirateforce_foundation
  py -3 -u -m pirateforce_foundation.app --db state\run_gt262_<stamp>.sqlite3 2>&1
  ```
  ต้องมีตัวจับแพ็กเก็ตเปิดอยู่ตลอดใบ: `capture_v141\GAME_LIVE.txt` (hex ดิบ) และ `GAME_EVENTS_LIVE.txt`

- steps: (**จดเวลานาฬิกา `HH:MM:SS+07:00` ทุกครั้งที่เขียนว่า "จดเวลา"** — ใช้ตัดหน้าต่าง hex ทีหลัง)
  0. **ด่านก่อนบูต**: รัน `git grep` ข้างบน — คาดว่า**ไม่เจอ** dispatcher ผูก opcode กลุ่มนี้ (สอดคล้อง P1) · **ถ้าเจอจริง** (มีคนเพิ่ม handler ระหว่างนี้) นี่คือการเปลี่ยนแปลงที่ `RE-261` ยังไม่รู้ ⇒ บันทึกเป็น finding แยกทันที แล้วเดินใบต่อตามเดิม (ไม่ใช่เหตุ BLOCK) · `LOCK_GAME` · boot stamp · sha canonical · คัดลอก DB เป็น run copy
  1. บูตเซิร์ฟเวอร์ใหม่สด · เปิดตัวจับแพ็กเก็ต
  2. บูตไคลเอนต์ · **สร้างตัวละครใหม่หนึ่งตัว** (ตาม P2) · ล็อกอิน · ภาพนิ่ง `S00-HOME` · เปิดกระเป๋ายืนยัน 4 ช่องตาม `INITIAL_BACKPACK` จริง — ถ้าไม่ตรง บันทึกของจริงแทน ไม่เดา
  3. **ข้อ 1 ของ `RE-261` (positive control ก่อนอย่างอื่นทั้งหมด — ห้ามข้าม ห้ามสลับลำดับ)**: ไล่คลิก/ไล่เมนูหาทางเข้า "แผงขายเอง" (NPC/ปุ่ม/hotkey ก็ได้ ยังไม่รู้ว่าเป็นแบบไหน) · **จดเวลา** ทุกครั้งที่คลิก + สิ่งที่คลิก + ผลลัพธ์ที่เห็น
     🔴 **เพดานการไล่คลิกรอบนี้: ไม่เกิน 15 นาทีนาฬิกาจริงหรือ 20 จุดคลิก แล้วแต่ถึงก่อน** — เกินแล้วยังไม่เจอ ⇒ ไปผลลัพธ์ `C`
  4. เจอทางเข้าแล้ว: เปิดแผง (`StallStartVital`) · ภาพนิ่ง `S1-STALL-OPEN` · **จดเวลา** · วางไอเทมหนึ่งชิ้นจากกระเป๋าลงช่องขาย (`StallOpenVital`) · ภาพนิ่ง `S1-ITEM-PLACED` · **จดเวลา**
  5. **trial A**: ตั้งราคาค่าที่ 1 บนช่องราคา (`StallOperateVital`) · **จดเวลาทันทีก่อน/หลังยืนยันราคา** · ภาพนิ่งเต็มความละเอียด `S1-PRICE-A` ให้เห็นตัวเลขราคาชัดบนจอ
  6. **trial B (เซสชันเดียวกัน ห้ามปิดไคลเอนต์/รีล็อกอินระหว่างนี้)**: เปลี่ยนราคาช่องเดิมเป็นค่าที่ 2 ที่ต่างจาก trial A (`StallOperateVital` อีกเฟรม) · **จดเวลา** · ภาพนิ่งเต็มความละเอียด `S1-PRICE-B` ให้เห็นตัวเลขราคาใหม่ชัดบนจอ · 🔴 **ทั้งสอง trial ต้องต่างกันเฉพาะตัวเลขราคาเท่านั้น** (ไอเทมเดิม ช่องเดิม ไม่ปิด-เปิดแผงใหม่ระหว่างนั้น) — นี่คือ positive control ที่ `RE-261` ขอ ถ้าทำสิ่งอื่นเปลี่ยนไปด้วย (เช่น สลับไอเทม) การเทียบไบต์จะสกปรก บันทึกไว้ตรง ๆ แล้วทำ trial ใหม่
  7. ปิดแผง · ภาพนิ่ง `S1-STALL-CLOSE`
  8. **ข้อ 3 ของ `RE-261`**: ไล่คลิก/ไล่เมนูหาทางเข้า "คลังกิลด์" แยกรอบใหม่ · **จดเวลา** ทุกครั้งที่คลิก + สิ่งที่คลิก + ผลลัพธ์ที่เห็น · **ทำต่อไม่ว่าผลลัพธ์ trial A/B ข้างบนจะออกทางบวกหรือลบ** (การผูก opcode กับหน้าจอของคลังกิลด์เป็นคนละคำถามจากไบต์ราคา ตาม `RE-261`)
     🔴 **เพดานการไล่คลิกรอบนี้: ไม่เกิน 10 นาทีนาฬิกาจริงหรือ 15 จุดคลิก แล้วแต่ถึงก่อน** — เกินแล้วยังไม่เจอ ⇒ ไปผลลัพธ์ `C` (ส่วนคลังกิลด์)
  9. เจอทางเข้าแล้ว: เปิดคลังกิลด์ (`GCSS_GuildStorageOpenVital`) · ภาพนิ่ง `S3-GS-OPEN` · **จดเวลา** · ถ้าเปิดไม่ได้เพราะไม่มีสังกัดกิลด์หรือเหตุอื่นที่ระบุได้ ⇒ ผลลัพธ์ `E` (บันทึกข้อความ/เหตุผลที่จอบอกตามตัวอักษร)
  10. ฝากไอเทมหนึ่งชิ้นจากกระเป๋าเข้าคลัง (`GCGS_GuildStorageCmdVital`) · **จดเวลา** · ภาพนิ่ง `S3-GS-DEPOSIT`
  11. ถอนไอเทมชิ้นเดิมกลับ (`GCGS_GuildStorageCmdVital` อีกเฟรม) · **จดเวลา** · ภาพนิ่ง `S3-GS-WITHDRAW`
  12. ปิดคลัง · ภาพนิ่ง `S3-GS-CLOSE` · เช็ก NO-CRASH ด้วย**คลิกขวาค้างลาก** (กล้องอย่างเดียว ทิศทางตัวละครไม่ขยับ ไม่มีไบต์ออกสาย) · 🔴 **ห้ามใช้ `Q`/`E` เป็น NO-CRASH check**
  13. ปิดเซิร์ฟเวอร์ · เก็บ `.out`/`.err` + `capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt` + sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน `TEMPLATE_teardown_generic.ps1` เสมอ** (**boot stamp ต้องไม่เกิน 420 นาที** ตาม `TEMPLATE_teardown_generic.ps1:135` — รอบที่จบเพราะเลิกเล่นก็ต้อง teardown)

- เกณฑ์สองชั้น (🔴 **ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น**):
    wire/DB (อ่านคอนโซลเซิร์ฟเวอร์ + hex ดิบ + ไฟล์ DB · ไม่ต้องมีตาคน · 🔴 **การตัดสินว่าไบต์ `+0x20` แปลว่าราคาหรือไม่ ไม่ใช่ของใบนี้ — เป็นของ `RE-261`/`CLIENT_RE_QUEUE.md` เท่านั้น**):
      W1. hex ครบทั้งสองเฟรมของ trial A/B (`StallOperateVital`) พร้อมเลข `[G<#N]` และเวลาที่จับคู่กับขั้น 5-6
      W2. hex ของเฟรม `StallStartVital`/`StallOpenVital` (ถ้าเจอทางเข้า) จับคู่เวลากับขั้น 4
      W3. hex ของเฟรม `GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital` (ถ้าเจอทางเข้า) จับคู่เวลากับขั้น 9-11
      W4. sha canonical ก่อน=หลัง ตรง `CANON_SHA.txt` · `integrity_check = ok` สองครั้ง · บูตบนสำเนาเสมอ · `sessions` +1 ต่อการล็อกอิน · `lease_generation` ไม่ถอยหลัง · ไม่มี traceback
      🔴 **ชั้นนี้ตอบไม่ได้ว่าคนเห็นอะไรบนจอ — ห้ามใช้แทนชั้นล่าง**
    client-observable (🔴 ต้องมีตาคน ห้ามอนุมานจาก hex):
      C1. ภาพ `S1-PRICE-A`/`S1-PRICE-B` แสดงตัวเลขราคาที่ต่างกันจริงบนจอ อ่านได้ชัดจากภาพเต็มความละเอียด
      C2. ภาพ `S1-STALL-OPEN`/`S1-ITEM-PLACED` แสดงหน้าต่างแผงขายเองเปิดจริง + ไอเทมอยู่ในช่อง
      C3. ภาพ `S3-GS-OPEN`/`S3-GS-DEPOSIT`/`S3-GS-WITHDRAW` แสดงหน้าต่างคลังกิลด์เปิดจริง + ไอเทมย้ายเข้า/ออกจริง (หรือข้อความปฏิเสธตามตัวอักษรถ้าเปิดไม่ได้ — ผลลัพธ์ `E`)
      C4. **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** (ข้อบังคับ R163 คำสั่ง Panya 2026-08-25): หนึ่งบรรทัดต่อหนึ่งป้ายต่อหนึ่งภาพ · "none" เขียนออกมา ไม่เว้นว่าง · อ่านจากภาพนิ่งเต็มความละเอียดเท่านั้น (ห้าม contact sheet/ภาพย่อ/วิดีโอ) · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ** (`RE-067` เป็นเจ้าของคำถามนั้น) · ต่างจากภาพเซิร์ฟเวอร์เดิม = ลง `REAL_SERVER_DIVERGENCE.tsv` แถวละหนึ่งข้อ
      C5. NO-CRASH check ผ่านทุกครั้งที่กำหนด
      **`OBSERVER_CONFIRMED: <ISO+07:00>` เป็นข้อบังคับแข็งของชั้นนี้ (G-OBS) — ไม่มี = ชั้นนี้ไม่ PASS**

- predictions (ทายผิด = finding ไม่ใช่ความล้มเหลว — carry-over hedge เดียวกับที่ `RE-261` ติดป้าย):
  - P1 [เสนอ, ยกจาก chief round 75 / `docs/FUNCTIONAL_COVERAGE.json`'s `use_drop_sell`]: ไบต์ `+0x20` ของ `StallOperateVital` เปลี่ยนตามราคาที่ตั้งบนจอ
  - P2 [เสนอ]: ทางเข้า "แผงขายเอง" หาเจอภายในเพดาน 15 นาที/20 จุดคลิก
  - P3 [เสนอ]: ทางเข้า "คลังกิลด์" อาจต้องมีสังกัดกิลด์ก่อน — ยังไม่มีใครวัด อาจจบที่ผลลัพธ์ `E`

- ทำอย่างไรกับผลแต่ละแบบ:
  A. **trial A/B ต่างกันแค่ราคาสำเร็จ + เจอทางเข้าแผง/คลังทั้งคู่ + ผูก opcode กับหน้าจอได้ครบ** ⇒ **PASS** (ชั้น client-observable ของใบนี้) · เกณฑ์ C1-C5 ตัดสิน · คำตัดสินไบต์ `+0x20` ให้ LANE-UI เขียนแยกลง `RE-261:result`
  B. **เจอทั้งแผง/คลัง ผูก opcode กับหน้าจอได้ แต่ hex ของ trial A/B (เมื่อ LANE-UI อ่าน) พบว่า `+0x20` ไม่ขยับตามราคา** ⇒ **PASS พร้อมคำตัดสิน `PRICE-BYTE-NOT-CONFIRMED`** — เป็นผลลบที่มีค่าเท่าผลบวก หักล้างสมมติฐาน chief round 75 (เขียนเป็น finding ไม่ใช่ความล้มเหลว) · ชั้น client-observable ของใบนี้ (การผูกหน้าจอกับ opcode) ยัง **PASS ได้ตามปกติ** เพราะเป็นคนละคำถามจากไบต์ราคา
  C. **ไล่คลิกจนครบเพดานแล้วไม่เจอทางเข้าแผงหรือคลังเลย (แยกกันได้ — เจอแผงแต่ไม่เจอคลัง หรือกลับกัน)** ⇒ **PASS พร้อมคำตัดสิน `NO-STALL-ENTRY-FOUND`/`NO-GUILDSTORAGE-ENTRY-FOUND`** (มีค่าเท่าผลบวก เหมือน `NO-SHOP-FOUND` ของ `GT-230`) · redirect: ทางเข้าอยู่นอกระยะที่ไล่คลิกถึง หรือบิลด์นี้ยังไม่มี UI/NPC ที่ประกาศเป็นทางเข้าเลย ⇒ ใบถัดไปต้องขอพิกัด/เมนูจากฝั่ง static RE
  D. **ไคลเอนต์ตาย/ตัวจับแพ็กเก็ตไม่เขียนไฟล์** ⇒ **NO-RESULT** พร้อมเหตุผลหนึ่งบรรทัด
  E. **เจอทางเข้าคลังกิลด์แต่เปิดไม่ได้เพราะไม่มีสังกัดกิลด์ (หรือเหตุอื่นที่ระบุได้จากข้อความบนจอ)** ⇒ **PASS พร้อมคำตัดสิน `NO-GUILDSTORAGE-ACCESS`** (ผลลบที่ใช้ได้ ไม่ใช่ใบล้ม) · ส่วนแผงขายเอง (trial A/B) ยังตัดสินแยกตามผลลัพธ์ A/B/C ข้างบนตามปกติ · redirect: ต้องมีใบ/ฟีเจอร์สร้าง-เข้าร่วมกิลด์ก่อนถึงจะไล่ต่อได้

- nonclaims:
  1. 🔴 **ห้ามเดาความหมาย tag ที่เหลือ** (`+0x14`/`+0x18`/`+0xB0` ฯลฯ) — `RE-261` สั่งห้ามตรง ๆ ว่าห้ามเดาก่อนข้อ 1 ผ่าน ใบนี้ก็ไม่เดาเช่นกัน ไม่ว่า trial A/B จะออกผล A หรือ B ก็ตาม
  2. ไม่ตัดสินว่าเซิร์ฟเวอร์เราเอง (`pirateforce_foundation.app`) จำลองพฤติกรรมแผงขายเอง/คลังกิลด์ของเซิร์ฟเวอร์ค่ายได้ถูกต้อง — **ไม่มีโค้ดฝั่งเซิร์ฟเวอร์จับ opcode กลุ่มนี้เลยตอนเปิดใบ** (`serializer_status=OPEN` ทุกคลาส) ใบนี้แค่จับสิ่งที่บิลด์นี้ทำจริงตอนนี้
  3. ไม่อ้างว่าถอดฟิลด์ในเฟรมได้มากกว่า hex ดิบที่จับได้จริง — ระดับฟิลด์ที่เหลือของ `StallOpenVital`/`StallOperateVital`/ตระกูล guild storage อีก 12 คลาส ยังไม่แกะราย field (ของ `RE-261`/รอบ static ถัดไป ไม่ใช่ของใบนี้)
  4. **ใบนี้ไม่ปิด `RE-261` ด้วยตัวเอง** — `RE-261` ปิดเมื่อ LANE-UI เขียนคำตัดสินชั้น wire/DB (ไบต์ `+0x20` ขยับตามราคาหรือไม่) ลง `CLIENT_RE_QUEUE.md:RE-261` เอง ตามที่ "ผลไปถึงใคร" ของใบนั้นระบุไว้
  5. ไม่อ้างว่า `STALL_SET.n_ID` ที่เห็นบนจอ (ถ้าอ่านได้) ตรงกับแถวใดใน `gamedata/PF_GAMEDATA_INDEX.tsv:117`/คอลัมน์ `gamedata/PF_GAMEDATA_COLUMNS.tsv:1924-1933` เว้นแต่ผู้เทสอ่านค่าออกมาตรง ๆ จากจอ — ตารางนั้น**ไม่มีคอลัมน์ราคา** จึงช่วยระบุ "แผงชนิดไหน" เท่านั้น ไม่ช่วยตอบคำถามไบต์ราคา
  6. ไม่ทดสอบ/ไม่อ้างอะไรเกี่ยวกับ `GuildStorageOpenVital`(`0x5CAD`)/`GuildStorageResultVital`(`0x70D0`) — สองคลาสชื่อเปล่าที่ `RE-261` เองระบุว่า "ใบนี้ไม่ขอ" (ไม่มีแถวให้เทียบเลย)
  7. ไม่มีการซื้อขายจริงข้ามผู้เล่นสองคน (ไม่มีตัวละครที่สองมากดซื้อของในแผง) — ใบนี้จบที่ "ของอยู่ในช่องขาย + ตั้งราคาสองค่า" ตามขอบเขตที่ chief ระบุไว้ในหัวใบเดิม ไม่ใช่การยืนยันธุรกรรมสำเร็จ
  8. ไม่ยืนยัน/ปฏิเสธว่าคลังกิลด์ต้องมีสังกัดกิลด์ก่อนหรือไม่โดยทั่วไป — บันทึกแค่สิ่งที่จอบอกจริงในรอบนี้ (ดูผลลัพธ์ `E`)

- STOP:
  1. STOP ถ้าไคลเอนต์ปิดตัวเองนอกจังหวะที่ใบสั่งให้ปิด — บันทึกว่าหยุดที่ขั้นไหน แล้ว teardown อยู่ดี
  2. STOP ถ้าเจอ `ErrorData` ใด ๆ ที่ไม่เกี่ยวกับใบนี้ — บันทึกเป็น finding แยก ไม่ใช่ทำให้ใบนี้ล้ม
  3. STOP การไล่คลิกทันทีที่ถึงเพดานของแต่ละรอบ (ข้อ 3/8 ของ steps) แล้วไปผลลัพธ์ `C` ของส่วนนั้น — ห้ามยืดเพดานเอง
  4. STOP การเดาความหมาย tag ใด ๆ นอกเหนือจาก `+0x20`/ราคา ไม่ว่าที่จุดใดของใบ (ตามข้อห้ามของ `RE-261`)

- links: `CLIENT_RE_QUEUE.md:RE-261` (`RE-261 STALL-AND-GUILD-STORAGE-FIELD-SEMANTICS-FROM-A-REAL-SESSION-001`) ·
  `notes_to_chief/20260905_0456_LANE-UI-RE-TICKET-stall-and-guild-storage-opcodes-known-fields-partial.md` (จดหมายต้นทาง เนื้อเต็ม) ·
  `GT-230` (ใบต้นแบบของรูปแบบ — ใบเก็บ hex ไม่ใช่ใบตัดสิน) ·
  `gamedata/PF_GAMEDATA_INDEX.tsv:117` + `gamedata/PF_GAMEDATA_COLUMNS.tsv:1924-1933` (`STALL_SET`, ไม่มีคอลัมน์ราคา) ·
  `gamedata/PF_GAMEDATA_LUA_API.tsv:122` (`Guild.OpenGuildStorage`, `Quest/q_guildstorage.lua`, สถานะ `UNRESOLVED`) ·
  `external/PF_SERIALIZER_FIELDS.tsv` (แถว `StallStartVital`/`StallOpenVital`/`StallOperateVital`/`GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital`) ·
  `external/PF_FIELD_VALIDATION.tsv:1018-1023,418-421` (ทุกแถว `NOT_OBSERVED` ก่อนใบนี้) ·
  `pirate-force-server/src/pirateforce_foundation/inventory.py:39-49` (`INITIAL_BACKPACK`) · `pirate-force-server/src/pirateforce_foundation/store.py:575,674` (`_insert_initial_backpack`) ·
  `ATTENDED_SESSION_RUNBOOK.md` + `BRIDGE_BOOT_PROCEDURE.md` + `TEMPLATE_teardown_generic.ps1`

ATTENDED: สร้างตัวละครใหม่ 1 ตัว ไล่คลิก/ไล่เมนูหาทางเข้า "แผงขายเอง" (เพดาน 15 นาที/20 คลิก) -- เจอแล้วเปิดแผง วางไอเทม 1 ชิ้น ตั้งราคา trial A แล้วเปลี่ยนเป็นราคา trial B ในเซสชันเดียวกัน (ห้ามปิด-เปิดแผงใหม่) -- แยกรอบไล่คลิกหา "คลังกิลด์" (เพดาน 10 นาที/15 คลิก) เปิดแล้วฝากไอเทม 1 ชิ้นแล้วถอนกลับ
ATTENDED: ดูเฟรม `StallStartVital 0x30FE`/`StallOpenVital 0x2A3E`/`StallOperateVital 0x3DE4` (สองเฟรม trial A/B) และ `GCSS_GuildStorageOpenVital 0x8B66`/`GCGS_GuildStorageCmdVital 0x7F17` (ฝาก/ถอน) -- ใบนี้ไม่ตัดสินว่า `+0x20` แปลว่าราคา (เป็นของ `RE-261`)
ATTENDED: PASS ชั้นจอ = ภาพ `S1-PRICE-A`/`S1-PRICE-B` อ่านตัวเลขราคาต่างกันได้ชัด + แผง/คลังเปิดจริงเห็นไอเทมย้าย (หรือข้อความปฏิเสธตามตัวอักษรถ้าเปิดไม่ได้ = ผล `E`) + บรรทัดสีป้ายครบทุกภาพ + `OBSERVER_CONFIRMED: <ISO+07:00>` -- ไม่มี = ไม่ PASS
ATTENDED: บูตมาตรฐาน ไม่มีแฟล็ก scenario ใด ๆ `-SecondPasswordMode bypass` ตัวจับแพ็กเก็ตต้องเปิดตลอดใบ (`capture_v141\GAME_LIVE.txt` + `GAME_EVENTS_LIVE.txt`)
ATTENDED: ไล่คลิกครบเพดานแล้วไม่เจอทางเข้า = ไปผล `C` (`NO-STALL-ENTRY-FOUND`/`NO-GUILDSTORAGE-ENTRY-FOUND`) แยกกันได้ต่อระบบ -- ไม่ใช่ใบล้ม

- result: (ผู้เทสกรอก: PASS `A`/`PRICE-BYTE-NOT-CONFIRMED`/`NO-STALL-ENTRY-FOUND`/`NO-GUILDSTORAGE-ENTRY-FOUND`/`NO-GUILDSTORAGE-ACCESS` หรือ `NO-RESULT` · branch+commit ที่บูต · ผลของ `git grep` ด่านข้อ 0 · ทุกจุดคลิกของทั้งสองรอบไล่คลิกพร้อมเวลาและผลลัพธ์ · hex ดิบครบของ trial A/B (`StallOperateVital`) พร้อม `[G<#N]` · hex ดิบของ `StallStartVital`/`StallOpenVital`/`GCSS_GuildStorageOpenVital`/`GCGS_GuildStorageCmdVital` ถ้าจับได้ · ภาพ `S00-HOME`/`S1-STALL-OPEN`/`S1-ITEM-PLACED`/`S1-PRICE-A`/`S1-PRICE-B`/`S1-STALL-CLOSE`/`S3-GS-OPEN`/`S3-GS-DEPOSIT`/`S3-GS-WITHDRAW`/`S3-GS-CLOSE` (เฉพาะที่ถ่ายได้จริง) + sha256 ทุกภาพ · **บรรทัดสีป้ายครบทุกป้ายทุกภาพ** · sha canonical ก่อน/หลัง · `integrity_check` สองครั้ง · NO-CRASH/CRASH · teardown รันแล้ว (boot stamp ไม่เกิน 420 นาที) · `OBSERVER_CONFIRMED: <YYYY-MM-DDTHH:MM+07:00>` · 🔴 **คัดลอกผล hex + คำตัดสิน `+0x20` (ถ้าวัดได้) ไปกรอกใน `RE-261:result` ด้วยตัวเอง (LANE-UI) — ใบนี้ไม่กรอกให้**)

- **ลำดับ**: ต่อท้าย "รอเครื่องคุณ" ของ `NOW.md` — **ไม่แซง** `GT-233` / `GT-230` / `GT-243` (งานที่ค้างอยู่ก่อนแล้ว) · ไม่บล็อกใคร

## numbering
`GT-262`/`RE-262` = **0 hit ทั้งสามที่** (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*`) ก่อนวาง [วัดแล้ว chief `pv4zg1`/R352] · ตัวนับร่วมสองคิวคืนสูงสุดที่ `256` ก่อนรอบนี้ · รอบนี้กิน `257`-`262`


---

## GT-276 LEARN-SKILL-RESULT-WALKLOCK-ISOLATE-001  [🟢 **READY -- attended -- เจ้าของใบ/ผู้บริโภคผล = LANE-CS** · ตั้งเลขโดย LANE-K รอบ `slug54r2` 2026-09-06T13:40+07:00 ตามคำขอ `notes_to_chief/20260906_1252_LANE-CS-TO-CHIEF-gt249-grade-plus-walklock-isolate-ticket.md` ข้อ 2 (เนื้อใบวางคำต่อคำจากร่างท้ายจดหมายนั้น) · เลขว่างตัวถัดไปหลัง `GT-274`/`GT-275` (จองไว้ก่อนหน้า ยังไม่วางเนื้อใบ — ไม่ชนกัน) · ยืนยันไม่ซ้ำ: grep `GT-276`/`RE-276` ทั้ง `GAME_TEST_QUEUE.md` `CLIENT_RE_QUEUE.md` `archive/` `notes_to_chief/` `NOW.md` = ไม่เจอที่อื่นก่อนวาง] 🔴 [LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00] เนื้อใบส่วน `boot:`/`ATTENDED:` **ถูกแทนคำต่อคำ** ตามคำขอเจ้าของใบ (`notes_to_chief/20260907_0437_LANE-CS-TO-K-gt-body-gt276-headless-proof-plus-corrected-boot.md`) เพราะใบเดิมสั่งใช้เครื่องมือที่ไม่มีในทรี = ใบตกรถแน่นอน · `HEADLESS_PROOF:` มาแล้วแต่ผูกกับคอมมิต `c6a9a95` ซึ่ง**ยังไม่ใช่ main** ⇒ ยังไม่ขึ้นรถบัส (หมวด ค.) [🟢 **เงื่อนไขข้อ (1) ของเจ้าของใบเป็นจริงแล้ว — K วัดเอง รอบ `rlapyk` 2026-09-07T06:11+07:00** · เจ้าของใบ LANE-CS เขียนเงื่อนไขไว้เองสามข้อ: (1) PR รอบ `li5jc1` เข้า main (2) LANE-CS รันคำสั่งเดิมซ้ำบน main (3) เปลี่ยนเลขคอมมิตในใบ · K วัดสดบนโคลนที่ `git fetch origin main` (`pirate-force-server` head `550a36d`): `git cat-file -e c6a9a95^{commit}` = **มีแล้ว** และ `git merge-base --is-ancestor c6a9a95 origin/main` = **ผ่าน** ⇒ คอมมิตที่ผลิตโทเคน `LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS` **อยู่บน `origin/main` แล้ว** (รอบก่อน `70l5du` วัดตอน main = `e4670a5` ยังไม่มีอ็อบเจกต์นี้) · 🔴 **K ไม่พลิกใบขึ้นรถบัสเอง** — ข้อ (2)(3) เป็นของเจ้าของใบ (พับ=คัดลอก ไม่ใช่ตัดสิน) · จดหมายแจ้ง LANE-CS: `notes_to_chief/20260907_0611_LANE-K-TO-CS-gt276-token-commit-is-on-main-now.md` · ใบจะขึ้นหมวด ข. ของสแนปช็อตในรอบแรกที่ LANE-CS ตอบกลับ] [🟢 **LANE-CS ตอบกลับแล้ว — ใบขึ้นรถบัสได้ (หมวด ก.)** · พับโดย LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00 · จดหมาย `notes_to_chief/20260907_0618_LANE-CS-TO-K-gt276-headless-proof-on-main-550a36d.md` (06:18) · เจ้าของใบทำครบทั้งสามข้อที่ตั้งไว้เอง: (1) `c6a9a95` เข้า main แล้ว (2) รันคำสั่งเดิมซ้ำบนทรี main สะอาด `550a36d` (3) เปลี่ยนเลขคอมมิตในบรรทัด `HEADLESS_PROOF:` ⇒ บรรทัดนั้นถูกแทนคำต่อคำแล้วในเนื้อใบ · 🔴 K ไม่ได้ตัดสินสถานะผลของใบ (ยัง READY เหมือนเดิม ยังไม่มีผลเทส) — เปลี่ยนแค่ 'ขึ้นรถบัสได้/ไม่ได้' ตามหลักฐานที่เจ้าของใบส่งมา] [✅ **PASS: ระบุตัวการได้ — R323C** 2026-09-07T21:33+07:00 (trailing u8 ของเฟรม HYP_PF_033 = 1 ล็อกการเดิน · = 0 เดินได้ · ไม่ขึ้นกับจำนวนรายการ) · ผลเต็ม `notes_to_chief/20260907_2140_KA1A-R323C-RESULTS-GT276-PASS-trailing-u8-1-locks-walking-not-record-count.md` (`OBSERVER_CONFIRMED 2026-09-07T21:27+07:00`, `21:33+07:00`) · พับโดย LANE-K รอบ `lruqz2` 2026-09-07T22:16+07:00 · ดู `### result:` ท้ายใบ]

**คำถามของใบ**: ส่งทีละเฟรมของ sweep 6 ขั้น `learn_skill_result_hypothesis_learn_sweep.json` (คนละรอบจาก `GT-249` ที่ส่งครบ 6 เฟรมรวด) แล้ว "เดินไม่ได้" (พบครั้งแรกใน `GT-249`/R312) มาจากเฟรมไหน

owner/consumer = LANE-CS -- ต้องการ capture บนเครื่อง Panya

HEADLESS_PROOF: 2026-09-07 main 6b5b6b8 | cmd: python3 src/pirateforce_foundation/skill_learn_step_headless.py | LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS
> [LANE-K รอบ `ek1gk9` 2026-09-07T09:4x+07:00] บรรทัดข้างบนวางคำต่อคำจาก `notes_to_chief/20260907_0746_LANE-CS-TO-K-gt276-plain-command-works-on-main-6b5b6b8.md` — เจ้าของใบรันซ้ำเองบนทรี `main` สะอาด `6b5b6b8` โดยไม่ตั้ง env ใด ๆ เลย
> ทำไมต้องเปลี่ยน: ฟอร์มเก่าต้องตั้ง `PYTHONPATH=src` เอง — ka1-A ที่รันโทเคนซ้ำก่อนบูตบนเช็คเอาต์เปล่าจะได้ `ModuleNotFoundError` ไม่ใช่โทเคน = ตัดใบทั้งที่กลไกติดอาวุธจริง (`NOW.md` `0159`)
> ที่ K วัดเอง (ไม่ได้เชื่อจดหมาย): `git merge-base --is-ancestor 6b5b6b8 origin/main` ผ่าน · `git cat-file -e origin/main:src/pirateforce_foundation/skill_learn_step_headless.py` ผ่าน (ไฟล์มีจริงบน main) · K **ไม่ได้** รันโมดูลเอง — ค่าโทเคนเป็นคำของเจ้าของใบ
> บรรทัดเดิม (เก็บไว้ ไม่ลบ — เจ้าของใบยืนยันว่ายังวัดได้จริงบนคอมมิตนั้น): `HEADLESS_PROOF: 2026-09-07 main 550a36d | cmd (บน 550a36d): PYTHONPATH=src python3 -m pirateforce_foundation.skill_learn_step_headless | LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS`
ATTENDED: บูตด้วยไฟล์ขั้นแรก (count0_trail0) เข้าเกม Gladiator lv1 ยืนยันเดินได้ก่อน (baseline)
ATTENDED: พิมพ์แชททริกเกอร์หนึ่งครั้ง (ทริกเกอร์เดิมของ sweep) รอ >=5 วิ แล้วลองเดิน (WASD/คลิกพื้น) ถ่ายภาพ
ATTENDED: เดินได้ = ปิดเซิร์ฟเวอร์ บูตด้วยไฟล์ขั้นถัดไป relog แล้วทำซ้ำ · เดินไม่ได้ = หยุด ขั้นนั้นคือตัวต้องสงสัย
ATTENDED: ดูคอนโซลเซิร์ฟเวอร์ว่าออก action label ชื่อ HYP_PF_033_LEARN_SKILL_RESULT_<LABEL> ครั้งเดียวต่อทริกเกอร์
ATTENDED: ผ่าน = ระบุขั้นที่ล็อกการเดินได้ หรือครบหกขั้นแล้วไม่ล็อกเลย (แปลว่า R312 เจอเงื่อนไขอื่น เขียนตรง ๆ ห้ามเดา)

> 🔴 [LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00] **`c6a9a95` ยังไม่ใช่ `main`** — เจ้าของใบเขียนข้อจำกัดนี้มาเอง: โทเคนมาจากหัวกิ่งรอบ CS `li5jc1` (= `origin/main` + PR ของรอบนั้น) · `NOW.md` บังคับว่า `HEADLESS_PROOF:` ต้องมาจากรัน "บนคอมมิต main ปัจจุบัน" ⇒ **ใบนี้ยังขึ้นรถบัสไม่ได้จนกว่า PR รอบ `li5jc1` เข้า main แล้ว LANE-CS รันซ้ำบน main และยืนยันด้วย `git merge-base --is-ancestor`** · K ไม่ได้นับใบนี้ว่าผ่านล่วงหน้า (ดูหมวด ค. ใน `QUEUE_STATUS_SNAPSHOT.md`) · ห้าบรรทัด `ATTENDED:` เดิมและบรรทัด boot เดิมถูกแทนคำต่อคำจาก `notes_to_chief/20260907_0437_LANE-CS-TO-K-gt-body-gt276-headless-proof-plus-corrected-boot.md` §3/§5

> 🟢 [LANE-K รอบ `4af3qf` 2026-09-07T07:12+07:00] **ข้อจำกัดข้างบนหมดอายุแล้ว** — เจ้าของใบ LANE-CS รันซ้ำบนทรี `main` สะอาด `550a36d` เองแล้วส่งบรรทัดใหม่มา (`notes_to_chief/20260907_0618_LANE-CS-TO-K-gt276-headless-proof-on-main-550a36d.md` 2026-09-07T06:18+07:00) · บรรทัด `HEADLESS_PROOF:` ข้างบนถูก**แทนคำต่อคำตามคำขอเจ้าของใบ** (แทนของใบ `0437` และ `0620` เฉพาะสองบรรทัดนั้น) · สองบรรทัดเดิมที่ถูกแทน เก็บคำต่อคำไว้ตรงนี้ ไม่ได้หายไป: `HEADLESS_PROOF: LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS` / `HEADLESS_PROOF: (python3 -m pirateforce_foundation.skill_learn_step_headless) 2026-09-07 commit c6a9a95` · เจ้าของใบยืนยันเองว่า `git merge-base --is-ancestor c6a9a95 origin/main` = จริง แล้ว stash งานของรอบออกก่อนรันบนทรี main เปล่า · หกบรรทัดคอนโซลเต็ม ๆ อยู่ในจดหมายฉบับนั้น · 🔴 **ข้อที่ ka1-A ต้องรู้ (คำของเจ้าของใบ)**: บน `550a36d` คำสั่งต้องมี `PYTHONPATH=src` — ไม่งั้นได้ `ModuleNotFoundError` ซึ่งเป็นช่องว่างของคำสั่ง **ไม่ใช่กลไกไม่ติดอาวุธ** · ถ้า PR รอบ `t04sgo` ของ LANE-CS เข้า main แล้ว ใช้ฟอร์ม `python3 src/pirateforce_foundation/skill_learn_step_headless.py` ได้ โทเคนเหมือนกัน · 🔴 K ไม่ได้รันโทเคนนี้เอง และไม่ได้ตัดสินว่าใบนี้ PASS — คัดลอกอย่างเดียว
boot: หนึ่งขั้น = หนึ่งบูต (โปรเซสหนึ่งรับแผนเดียว โมดูลปฏิเสธการเปลี่ยนแผนกลางคัน)
boot: py -3 -u -m pirateforce_foundation.app --db state\run_gt276_<stamp>.sqlite3 --learn-skill-result-hypothesis-scenario scenarios\learn_skill_result_hypothesis_learn_step_<label>.json
boot: <label> เรียงตามลำดับ: count0_trail0 · count1_trail0 · count1_trail1 · count3_trail0 · count3_trail1 · count4_real_skill_ids_class1_trail0

> [LANE-K รอบ `70l5du` 2026-09-07T05:10+07:00] สามบรรทัด `boot:` ข้างบนแทนบรรทัด boot เดิมทั้งบรรทัด คำต่อคำจาก `notes_to_chief/20260907_0437_LANE-CS-TO-K-gt-body-gt276-headless-proof-plus-corrected-boot.md` §4 (เจ้าของใบ LANE-CS) · บรรทัด boot เดิมที่ถูกแทน: "`py -3 -u -m pirateforce_foundation.app --db state\run_gt276_<stamp>.sqlite3` (ไม่มีแฟล็ก `--*-scenario` ใด ๆ ... รายละเอียดเครื่องมือส่งเฟรมเดี่ยวให้ผู้รันเลือกจากที่มีอยู่แล้วในทรี)" — เจ้าของใบ grep แล้วว่าเครื่องมือนั้น**ไม่มีอยู่ในทรี** (`send_raw` `inject_frame` `single_frame` `raw_frame` `dev_console` = 0 hit ทั้ง `tools/` และ `src/`)

**เกณฑ์ผ่านสองชั้น**
- **client-observable**: ภาพ/บันทึกการเดินไม่ได้ที่ขั้นใดขั้นหนึ่ง (หรือครบ 6 ขั้นไม่ล็อก)
- **wire**: label ของเฟรมที่ส่งไปก่อนแต่ละครั้งลองเดิน (จาก sweep json)

### result:
พับโดย LANE-K รอบ `lruqz2` 2026-09-07T22:16+07:00 (แก้ให้เป็นคำต่อคำจริงโดย LANE-K รอบ `0kois4` 2026-09-07T22:42+07:00 หลัง `pf-adversary` จับได้ว่าฉบับแรกสรุปย่อแทนที่จะยกคำต่อคำตามที่บรรทัดนี้อ้าง — ฉบับแก้ยกทั้งฉบับยกเว้นบรรทัดขนส่ง `ADDRESSEE:`/`ส่งทาง:` และหัวเรื่องซ้ำที่ซ้ำกับ bracket ข้างบนแล้ว) อ้างจาก `notes_to_chief/20260907_2140_KA1A-R323C-RESULTS-GT276-PASS-trailing-u8-1-locks-walking-not-record-count.md` คำต่อคำ:

> OBSERVER_CONFIRMED: 2026-09-07T21:27+07:00 (Panya: "เดินไม่ได้" ขั้น 5 + ภาพ `evidence_screens/R323C_GT276_step5_count3_trail1_walklock_20260907_2128.png`) · 2026-09-07T21:33+07:00 (Panya: "เดินไม่ได้" ขั้น 3 ซ้ำ)
>
> ## บูต (หนึ่งขั้น = หนึ่งบูต ตามใบ · ธงเดียว `--learn-skill-result-hypothesis-scenario scenarios/learn_skill_result_hypothesis_learn_step_<label>.json` + `--db` สำเนา · ไม่มี env)
> - BOOT_COMMIT ขั้น 1 `2df49cc2` · ขั้น 2–3 `b2b952a6` · ขั้น 4–5 และ 3-ซ้ำ `718707f8` (resolver เลือกหัวเขียวล่าสุดทุกครั้ง · main ขยับระหว่างรอบ) · RECHECK ทุกบูต: `merge-base --is-ancestor 6b5b6b8` ผ่าน · pytest learn_skill_result/skill_learn_step ผ่าน · `skill_learn_step_headless.py` บนทรีบูต → `LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS` · ธงบน command line ยืนยันตัวเดียว
> - jobs 1571–1575 (ขั้น 1–5) · 1579 (ขั้น 3 ซ้ำ) · teardown 1577_s1..s5,s3b · release 1578 · run DB `state/run_gt276_*` ต่อกันทุกขั้น · canonical sha **ไม่เปลี่ยน** `4FF37060…A548454` · captures `GameClient/capture_r323c_s1_… s2_… s3_… s4_… s5_… s3b_…`
> - ตัวละคร: **Arena01 (Gladiator LV60)** ทุกขั้น (`LOGIN_VITALS from_row level=60`) — ใบเขียน "Gladiator lv1"; คลาสเดียวกัน ระดับต่างกัน (deviation บันทึกไว้)
> - ทริกเกอร์: แชท 12 ตัวอักษร `SKILLCONTENT` (ascii12 · เฟรม 0xAC52 54 B) · ขั้น 3 ครั้งแรกเจ้าของพิมพ์ข้อความยาว (0xAC52 83 B) → server ไม่รับเป็นทริกเกอร์ ไม่ส่งเฟรม → **ไม่นับ** ทำซ้ำเป็นบูตสุดท้าย
>
> ## ผลทีละขั้น (ชั้นจอ = คำเจ้าของ · ชั้นสาย = คอนโซล `[G>] HYP_PF_033_LEARN_SKILL_RESULT_<LABEL>` ครั้งเดียวต่อทริกเกอร์ทุกขั้น)
> | ขั้น | label | เฟรม | ไบต์ท้าย | เดิน |
> |---|---|---|---|---|
> | 1 | COUNT0_TRAIL0 | 37 B | `0B 00` | **ได้** |
> | 2 | COUNT1_TRAIL0 | 50 B | `0B 00` | **ได้** |
> | 3 (ซ้ำ) | COUNT1_TRAIL1 | 50 B | `0B 01` | **ไม่ได้** |
> | 4 | COUNT3_TRAIL0 | 77 B | `0B 00` | **ได้** |
> | 5 | COUNT3_TRAIL1 | 77 B | `0B 01` | **ไม่ได้** |
> | 6 | COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 | — | — | ไม่ได้บูต (ใบ: เดินไม่ได้ = หยุด) |
>
> ### หลักฐานไบต์ (จากคอนโซล hex ของเฟรมที่ส่งจริง)
> - ขั้น 2 vs ขั้น 3-ซ้ำ (50 B ทั้งคู่) **ต่างกันไบต์เดียว** offset 0x25: `00` → `01`
>   - ขั้น 2: `… 12 0B 00 14 81 84 1E 00 0B 00 0B 00`
>   - ขั้น 3: `… 12 0B 00 14 81 84 1E 00 0B 01 0B 00`
> - ขั้น 4 vs ขั้น 5 (77 B ทั้งคู่) ต่างกันไบต์เดียวเช่นกัน: `… 14 60 60 60 60 0B 00 0B 00` → `… 0B 01 0B 00`
> ⇒ **trailing u8 = 1 คือสิ่งที่ล็อกการเดิน** · จำนวนรายการ (1 หรือ 3) และเนื้อรายการ (ค่าหลอก) ไม่มีผล
>
> ## สถานะที่เสนอ
> - GT-276 → **PASS** (ระบุขั้นที่ล็อกได้: ทุกขั้นที่ TRAIL=1 · ทุกขั้นที่ TRAIL=0 เดินได้) · R312 ล็อกเพราะ sweep รวดเดียวมีขั้น TRAIL1 อยู่ในชุด
> - ผลพวงถึง GT-299/รายการสกิลตอน login: ส่งเฟรมนี้ด้วย **TRAIL=0** จะไม่ล็อกผู้เล่น — CS ใช้ได้ทันทีเป็นเงื่อนไขของเฟรม production
> - BUILD_PROPOSED: skill list at login without walk-lock | LANE-CS | send HYP_PF_033-shaped frame with real skill ids (step 6 records) and trailing u8 = 0 on flagless StartGame; token: client skill window non-empty AND owner walks after login
>
> ## nonclaims
> - ไม่อ้างความหมายของ trailing u8 (แค่ "1 = ล็อกเดิน, 0 = ไม่ล็อก" บน client build นี้) · ไม่ได้วัดว่าล็อกถาวรหรือปลดเมื่อไหร่ (เจ้าของปิดเกมด้วย X หลังยืนยัน) · ไม่ได้รันขั้น 6 จึงไม่ยืนยันว่ารายการ id จริง + TRAIL=0 แสดงบนจอโดยไม่ล็อก (ต้องบูตแยก) · หน้าต่างสกิล (K) ว่างทุกขั้น 1–5 ตามคาด เพราะ records เป็นค่าหลอก · ตัวละครเป็น LV60 ไม่ใช่ lv1 ตามใบ
>
> RESULT: GT-276 PASS R323C 2026-09-07 21:33 (walk-lock = trailing u8 == 1 · steps COUNT1_TRAIL1 and COUNT3_TRAIL1 lock, COUNT0/1/3_TRAIL0 walk · one-byte diff at frame tail · step 6 not booted per ticket)
> SCOREBOARD: COMING | รู้แล้วว่าเฟรมรายการสกิลต้องปิดไบต์ท้ายเป็น 0 ผู้เล่นถึงจะเดินต่อได้ — ทางเปิดให้ CS ส่งรายการสกิลตอน login โดยไม่ล็อกผู้เล่น | 20260907_2140_KA1A-R323C-RESULTS-*

`RESULT: GT-276 PASS R323C 2026-09-07 21:33 (walk-lock = trailing u8 == 1 · steps COUNT1_TRAIL1 and COUNT3_TRAIL1 lock, COUNT0/1/3_TRAIL0 walk · one-byte diff at frame tail · step 6 not booted per ticket)`

## nonclaims
- ไม่อ้างว่ารู้สาเหตุ "เดินไม่ได้" แล้ว -- แค่รายงานว่าเกิดขึ้นจริงและยังไม่แยกเฟรม (จากจดหมาย `20260905_0154_KA1A-R312-RESULTS-*.md` เอง)
- ไม่อ้างว่า `GT-249` ปิดแล้วด้วยใบนี้ -- ดูข้อ 1 ของคำขอเดียวกัน (พับแยกลงหัวใบ `GT-249` แล้วโดย LANE-K รอบเดียวกัน)
- ไม่อ้างว่าใบนี้เข้าคิวจริงมาก่อนรอบนี้ -- เพิ่งวางเลข+เนื้อใบรอบนี้เป็นครั้งแรก
- ไม่อ้างว่า `production_allowed` ของโมดูลใดขยับรอบนี้ -- ยังคง `False` ทั้งคู่

> numbering: เลขว่างตัวถัดไปหลัง `RE-273`/`GT-274`/`GT-275` (จองไว้ก่อนหน้า ยังไม่ลงเนื้อใบ) ⇒ **276** [ตรวจโดย LANE-K รอบ `slug54r2` — grep ไม่เจอ `GT-276`/`RE-276` ที่อื่นในรีโปก่อนวาง]

---

## archived 2026-09-08T07:11+07:00 by LANE-K round `8c7cfo` -- moved verbatim from GAME_TEST_QUEUE.md (closed, RESULT already folded, part of the Contents-API size-reduction task from round `0511`)

## GT-274 PRODUCTION-ATTACK-POSE-BY-CLASS-CONFIRMED-001  [✅ **PASS ทั้งสองชั้น (arm i เต็ม · arm ii รอ GT-272) — R322B/R322C** 2026-09-07T01:36+07:00 (Gladiator ตี Fighting Fish: จอฟันดาบ · wire `POSE_PRODUCTION class=1 equip_type=1 base=2 behavior=280` (R322B 00:5x) · Paladin look #1 ตี Training Iron Man 916: จอฟาดกระบอง (ดาเมจ 891 ตรงจอ) · wire `POSE_PRODUCTION class=2 equip_type=2 base=3 behavior=284` ×4 (R322C) · arm ii (สวมอาวุธ+relog) ไม่ได้ทำ — GT-272 ยังไม่ผ่าน) · ผลเต็ม `notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-*.md` (`OBSERVER_CONFIRMED 2026-09-07T01:48+07:00`) · พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00 · เดิม: 🟢 **READY -- arm (i) บูตได้ทันที ไม่มีธง (ต้องผ่านกาน "ก่อนบูต (gate)" ด้านล่างก่อน) · arm (ii) พ่วงได้เมื่อ `GT-272` ผ่านก่อนในบูตเดียวกัน** · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-CS** · ผู้ตรวจคู่เนื้อใบ (ท่าเป็นเขต B) = LANE-B ไม่ต้องรอ B ก่อนวาง (`COO-DECISION 20260906_0645`) · เปิดตาม `COO-DECISION 20260906_0645` ข้อ 1 -- **ยกเว้น P-2 ในฐานะผู้สืบทอดใบที่สองของ `ATTACK-POSE-ONE-FIELD-AB-001`/`GT-247`** (วัดชนิดเดียว: ท่าเปลี่ยนตามคลาส ไม่วัดสี/ดาเมจ/ดรอป/ตาย) · เลขนับเลขสดเอง (`0434`, ไม่ต้องรอ chief ตั้ง) · **ไม่ปิด `PANYA-ORDER 20260906_0156`** (ปิดด้วย `GT-272` แขน ข ของ DB) และ**ไม่ใช่เกณฑ์ผ่าน M4** (M4 = `GT-224` ของ LANE-B) · v2 แก้ตาม pf-adversary รอบ `rabwxj-adv` (ดูหมายเหตุ v2 ท้ายใบ) · เนื้อใบวาง (v2 คำต่อคำ) โดย LANE-K รอบ `rsmsia` 2026-09-06T15:09+07:00 จาก `notes_to_chief/20260906_0805_LANE-CS-TO-CHIEF-gt274-v2-supersedes-0749-adversary-found-two-real-gaps.md`]

**คำถามของใบ**: บนบูต production ไม่มีแฟล็ก เมื่อตัวละคร Gladiator (class_id=1) ตี Training Iron Man (`n_ID 916`) หนึ่งครั้งที่ยอมรับ ท่าตีบนจอตรงกับดาบตามที่ `GT-247`/R315 ยืนยันแล้วหรือไม่ (BEHAVIOR 280) -- และเมื่อตัวละครอีกตัวที่สร้างใหม่เลือกอาชีพ Paladin ตอนสร้างตัว (look #1 -- ตัวเลือกแรก/ซ้ายสุดในแผงเลือกหน้าตา ณ จอสร้างตัวละคร ถ้าจอไม่มีตัวเลือกแยกชัดเจนให้ใช้ค่าเริ่มต้นที่จอเลือกไว้แล้วบันทึกว่าเลือกโดยไม่ได้กดเปลี่ยน) ตี Training Iron Man ตัวเดิม ท่าต่างจากตัวแรกอย่างเห็นได้ชัดหรือไม่ (คาด BEHAVIOR 284 ค้อน) -- อ่านคู่กับบรรทัดคอนโซล `POSE_PRODUCTION`/`POSE_REFUSED`/`POSE_NO_EQUIP_PROVENANCE` ของ `combat_pose.py` ที่พิมพ์สดต่อฮิต ไม่ใช่สร้างย้อนหลัง

**ก่อนบูต (gate 0/1/2 -- เนื้อจริง ไม่ใช่แค่ชื่อ)**: arm (i) พึ่ง `pirate-force-server` commit `d52cae3` (`CORE-REQUEST 20260905_2242`, ต่อ `class_id=selected.class_id` เข้า `combat_pose` ที่ `runtime.py` บรรทัด ~5172) ต้องเป็นบรรพบุรุษของคอมมิตที่จะบูต -- ตรวจด้วย `git merge-base --is-ancestor d52cae3 <commit ที่จะบูต>` (ผ่าน = เจอ exit 0) แล้วยืนยันซ้ำด้วย `git grep -n "class_id=selected.class_id" <commit นั้น> -- src/pirateforce_foundation/runtime.py` ต้องเจอ 1 บรรทัด -- ใช้ `tools/pf_resolve_green_boot.py` หา `BOOT_COMMIT` ที่ผ่านเกตแล้วรันสองคำสั่งนี้กับ SHA ที่มันคืนมา ห้ามเดา SHA เอง · **ไม่ผ่านสองคำสั่งนี้ = ห้ามบูต**: ตัวละคร Gladiator จะขึ้น `POSE_NO_EQUIP_PROVENANCE` แทน `POSE_PRODUCTION` ทั้งที่ `combat_pose.py` เองไม่มีปัญหา (คอมมิตที่บูตแค่ยังไม่มีสายที่ป้อน `class_id` เข้าไป) -- นี่คือผลลวงที่เช็คนี้มีไว้กันโดยเฉพาะ

**หมายเหตุ (ไม่ใช่ FAIL)**: `persistence_class_id.py`'s docstring เองบันทึกไว้ว่า capture ของคลาสที่สอง (ไม่ใช่ Gladiator) ยังไม่เคยมีใครยืนยันว่า class-selection ตอนสร้างตัวจับคู่กับแถวถูกต้อง (`GT-226` เปิดอยู่) -- ตัวละคร Paladin ที่คืนค่า `class_id` ผิด/`None` ที่ล็อกอินขึ้น `POSE_NO_EQUIP_PROVENANCE reason=no_class_id` ส่วนที่คืนค่าเป็นคลาสอื่นที่ถูกต้องแต่ผิดคาด (เช่น class=4) จะขึ้น `POSE_PRODUCTION class=4 ... behavior=282` ไม่ใช่ `POSE_NO_EQUIP_PROVENANCE` -- ทั้งสองแบบเป็น**ผลลบจริงของคำถามที่สอง** บันทึกบรรทัดคอนโซลจริงเป็น finding ให้ `persistence_class_id.py`/`GT-226` ไม่ใช่ทำให้ใบนี้ FAIL ทั้งใบ (คำถามแรก Gladiator/280 ยังยืนได้ตามลำพัง -- อาศัย `app.py`'s `backfill_missing_class_ids` ที่รันทุกบูตเติม `class_id` ให้ตัวละครเก่าที่แถวยังว่าง ตรวจแล้วว่ามีจริงในบูตปกติไม่มีแฟล็ก)

**ส่วนขยาย (arm ii, ไม่บังคับ)**: ถ้า `GT-272` (DB แขน ข, สวมอาวุธจากกระเป๋าคงอยู่ข้าม relog) ผ่านแล้วในบูตเดียวกัน ให้ตัวละคร Gladiator ตีหุ่นซ้ำอีกครั้งหลังสวมอาวุธ+relog -- คาดว่าท่ายังเป็นดาบ 280 เหมือนเดิม (`combat_pose.py` อ่านอาวุธเริ่มต้นของคลาสเท่านั้น ยังไม่อ่านช่องอุปกรณ์ที่สวมจริง ตามที่โมดูลระบุเป็นรอยต่อที่ยังไม่ต่อ) -- arm (ii) ไม่ผ่าน/ไม่ได้ทำ **ห้ามบล็อก arm (i)**

ATTENDED: บูตปกติ ไม่มีธง (ผ่านกาน "ก่อนบูต (gate)" ข้างบนก่อน) ล็อกอินตัวละคร Gladiator (class 1, ตัวเดิมจาก `GT-116`/`GT-243`/`GT-249`) เดินไปตี Training Iron Man (`n_ID 916`) หนึ่งครั้งที่ยอมรับ ถ่ายภาพท่าตี + คัดลอกบรรทัดคอนโซล `POSE_*` คู่ฮิตนั้น
ATTENDED: ล็อกเอาต์ สร้างตัวละครใหม่เลือกอาชีพ Paladin (look #1) หน้าจอสร้างตัวละคร ล็อกอินตัวใหม่ เดินไปตี Training Iron Man ตัวเดิมหนึ่งครั้งที่ยอมรับ ถ่ายภาพท่าตี + คัดลอกบรรทัดคอนโซล `POSE_*` คู่ฮิตนั้น
ATTENDED: (ถ้า `GT-272` ผ่านแล้วในบูตนี้) ให้ตัวละคร Gladiator สวมอาวุธจากกระเป๋าตาม `GT-272` ขั้น 2 แล้ว relog แล้วตีหุ่นซ้ำหนึ่งครั้ง ถ่ายภาพ + คัดลอกบรรทัดคอนโซลอีกชุด (arm ii ส่วนขยาย ข้ามได้ถ้า `GT-272` ยังไม่ผ่าน)
ATTENDED: ผ่าน = สองภาพแรกต่างกันจริงบนจอ **และ** คอนโซลตัวแรกอ่าน `POSE_PRODUCTION class=1 ... behavior=280` -- ตัวที่สองอ่าน `POSE_PRODUCTION class=2 ... behavior=284` ถือเป็นผ่านเต็ม ถ้าตัวที่สองอ่านอย่างอื่นถือเป็นผ่านคำถามแรกอย่างเดียว + finding แยกตามหมายเหตุข้างบน (ไม่ใช่ FAIL ทั้งใบ)
ATTENDED: ไม่ผ่าน = ตัวแรก (Gladiator) ไม่ขึ้น `POSE_PRODUCTION class=1` หรือท่าไม่ใช่ดาบ หรือคอนโซลไม่มีบรรทัด `POSE_*` เลยคู่ฮิตนั้น **หลังผ่านกาน "ก่อนบูต (gate)" แล้ว** -- ไม่ผ่านกานเองไม่นับ FAIL ให้หยุดก่อนบูตตามที่กานสั่ง

**เกณฑ์ผ่านสองชั้น**
- **client-observable**: ภาพท่าตีของสองตัวละครต่างกันจริงบนจอ (ผู้สังเกตยืนยัน)
- **wire/DB**: บรรทัดคอนโซล `POSE_PRODUCTION`/`POSE_REFUSED`/`POSE_NO_EQUIP_PROVENANCE` ที่ `combat_pose.production_behavior_for_class` พิมพ์สดต่อฮิต (ค่าเดียวกับ selector ที่ประกอบเป็นเฟรม ไม่ใช่ reconstructed) -- ห้ามอ้างชั้นนี้แทนชั้นบน หรือกลับกัน

**nonclaims**: ไม่วัดสีชื่อ ไม่วัด HP ลด ไม่วัดดรอป ไม่วัดตาย (ขอบเขตยกเว้น P-2 แคบเฉพาะท่า -- พบสีผิดระหว่างเทสให้จดเป็นข้อสังเกตของ P-2 ห้ามนับผ่าน/ตกของใบนี้) · ไม่อ้างว่า `persistence_class_id.py` ยืนยันคลาสที่สองถูกต้องเสมอไป -- capture ของ Paladin ในใบนี้คือครั้งแรก ไม่ว่าผลจะออกทางไหน (ดูหมายเหตุข้างบน) · ไม่อ้างว่าอาวุธที่สวมจาก `GT-272` เปลี่ยนท่า -- `combat_pose.py` อ่านอาวุธเริ่มต้นของคลาสเท่านั้น (module docstring, seam ยังไม่ต่อ) · ไม่อ้างว่าใบนี้ปิด `PANYA-ORDER 0156` หรือผ่านเกณฑ์ M4 · ไม่อ้างว่ามอนอื่นหรือใบตีมอนที่วัดดาเมจ/ดรอป/สีได้รับยกเว้นเดียวกัน (ยกเว้นเฉพาะใบนี้กับ `GT-247`/`ATTACK-POSE-ONE-FIELD-AB-001` เท่านั้น)

### result:
อ้างจาก `notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-GT274-PASS-mace-284-GT178-NEGATIVE-no-ai-tick-scene14.md` (R322C, ka1-A attended, OBSERVER_CONFIRMED 2026-09-07T01:48+07:00) คำต่อคำ, ต่อจากครึ่งแรกใน R322B:

> ครึ่งแรก (R322B 00:5x): Gladiator (Arena01) ตี Fighting Fish → จอ: ฟันดาบ · wire: `POSE_PRODUCTION class=1 equip_type=1 base=2 behavior=280`
> ครึ่งหลัง (R322C): สร้างตัวใหม่ **Paladin หน้าตา #1** → ตี Training Iron Man (916) ในเมือง 4 ครั้ง → จอ: **ฟาดกระบอง** (เจ้าของยืนยัน + ภาพ ดาเมจ 891 บนจอ) · wire: `POSE_PRODUCTION class=2 equip_type=2 base=3 behavior=284` ×4 · `damage announced -891, applied 891` HP 192779→189215/198125 ตรงจอ
> ขั้น 3 ของใบ (สวมอาวุธแล้วตีซ้ำ) ไม่ได้ทำ — GT-272 ยังไม่ผ่าน (RE-280) · `TWO_SESSIONS_SAME_SCENE:` ไม่ได้วัด (ผู้เล่นคนเดียว)

RESULT: GT-274 PASS R322C 2026-09-07 01:36 (Paladin mace pose · POSE_PRODUCTION class=2 behavior=284 · Gladiator half class=1 behavior=280 in R322B)

พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00

TWO_SESSIONS_SAME_SCENE: ไม่เกี่ยว -- ใบนี้อ่าน `class_id` จาก `Character` ที่ผูกกับ session/connection ของผู้ตีเอง (`combat_pose.production_behavior_for_class` ต่อฮิตต่อคน) ไม่แตะ world registry/มอน/ตำแหน่ง/ของพื้น/ศพที่แชร์ข้าม session ตามกฎ shared-world (สอดคล้องกับที่ chief เองตอบไว้ใน `CORE-REQUEST 2242` ที่ใบนี้อ้างอิงโค้ดเดียวกัน)

> 🔴 **ห้ามสายอื่นใช้เลข `GT-274`** · numbering: เลขจองไว้ก่อนหน้า (จดหมาย `0749`/`0805`) ⇒ **274** -- ตรวจซ้ำโดย LANE-K รอบ `rsmsia`: `GT-274`/`RE-274` = 0 hit จริงใน `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md`/`archive/*QUEUE*ARCHIVE*` ก่อนวาง (สองที่ที่ขึ้นตอน grep คือ "จองไว้" ในหัวใบ `GT-276` เท่านั้น ไม่ใช่เนื้อใบซ้ำ)

> v2 (รอบ `rabwxj-adv`): pf-adversary จับได้สองข้อจาก v1 -- (1) ขาดบรรทัด `TWO_SESSIONS_SAME_SCENE:` บังคับตาม `PROCESS_GATES.md` §25 -- เติมแล้วข้างบน (2) วลี "gate 0/1/2 ผ่านก่อนบูต ห้ามเดา SHA" ที่ยกมาจาก `GT-249` เป็นชื่อเปล่าไม่มีเนื้อหา (v1 ไม่มี PR/SHA/grep ให้ตรวจจริง ขณะที่ arm (i) พึ่ง `d52cae3` ที่เพิ่งขึ้น main ~3.5 ชม.ก่อนร่างใบ) -- เติมย่อหน้า "ก่อนบูต (gate)" ให้มีคำสั่งตรวจจริงแล้วข้างบน · แก้เพิ่มสองจุดเล็ก: หมายเหตุ (แยก `POSE_NO_EQUIP_PROVENANCE` ออกจากกรณี class อื่นที่ถูกต้อง) และ "look #1" (นิยามสั้นกันทดสอบเข้าใจผิด)

**ผู้เปิดใบ: LANE-CS (ผ่าน `notes_to_chief/20260906_0749_LANE-CS-TO-CHIEF-gt274-ticket-body-ready-for-numbering.md` + v2 `20260906_0805_*`) -- ตั้งเลข/วาง: LANE-K รอบ `rsmsia` -- ผู้บริโภคผล: LANE-CS**


## GT-281 BASIC-FACTION-EVERY-LOGIN-SCENE-SEA-126-001  [✅ **PASS ทั้งสองชั้น — R322B** 2026-09-07T00:55+07:00 (client-observable: login กลางทะเลผ่าน return ticket → `/warp 2` → Fighting Fish ชื่อชมพู ไม่เขียว คลิกโจมตีติด มอนตาย · wire: `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` บน login ทะเล) · หลอดฟ้าใต้ชื่อ/HP -1 ยังอยู่แต่วัดแล้วว่าไม่ใช่เรื่อง faction — แยกเป็นใบสร้างใหม่ของ A/DB (BoatHealth ไม่ถูกตั้งกลับเป็น HP ตัวละครตอนออกจาก 126) ไม่ใช่เกณฑ์ตกของใบนี้ · ปลดล็อก GT-220/GT-223 · ผลเต็ม `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-*.md` (`OBSERVER_CONFIRMED 2026-09-07T01:05+07:00`) · พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00 · เดิม: 🟢 **READY — ชั้น wire PASS R322A** (`PLAYER_FACTION basic_faction=1` on sea login) · ชั้นจอ NOT MEASURED ยัง เหลือ `/warp 2` ดูสีชื่อมอน (ผล `notes_to_chief/20260906_1909_KA1A-R322A-RESULTS-*.md` · เติมโดย LANE-K รอบ `cu7c2r` ตาม `COO-DECISION 20260906_1955` ข้อ 1) — precondition ปลดแล้ว ตรวจสดโดย LANE-K รอบ `cm9v9y` 2026-09-06T17:10+07:00: `pirate-force-server` PR `#1501` (LANE-A round `q02brx`) merge เข้า `origin/main` (`b9a552d`) แล้ว · `git show origin/main:src/pirateforce_foundation/world_faction_admission.py` ยืนยัน `admits()` ไม่เช็ค registry อีกต่อไป ("every scene a login can legally carry ... is admitted") ตรงเงื่อนไขที่ตั้งไว้ ~~[เดิม: 🔴 BLOCKED-ON-WIRING จนกว่า PR ของรอบนี้ (`pirate-force-server` LANE-A round `q02brx`, แก้ `world_faction_admission.admits` ให้ไม่เช็ค registry — ทุกฉากที่ login ได้ = ได้ faction) จะขึ้น main]~~ · **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-A** · ตั้งเลขโดย LANE-K รอบ `zqq4qz` 2026-09-06T16:09+07:00 ตาม `NOW.md` ("P-2 ชั้นแรกเจอต้นเหตุ ... LANE-A งานแรกรอบถัดไป ส่งfaction ทุก login scene + ใบ GT (`1347`)") · เนื้อใบมาจากจดหมาย `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md` คำต่อคำ · อ้าง: `COO-DECISION 20260906_1347` · `KA1A-R321-RESULTS §1`]

**คำถาม**: login ผ่านตั๋ว relog เข้าฉาก 126 (ทะเล, Atlantis ocean panel) ทำให้ผู้เล่นได้ `basic_faction` เหมือน login บกหรือไม่ — และหลัง `/warp 2` มอนในฉาก 2 ตีได้ปกติหรือไม่ (ก่อนหน้านี้ login ผ่าน 126 ทำให้ผู้เล่นไร้ฝ่ายถาวรทุกฉากจนกว่าจะ login ใหม่บนบก — `KA1A-R321 §1`)

**เกณฑ์สองชั้น**:
- ชั้น client-observable (บนจอ): `/warp 126` (ต้องเป็นบัญชี GM ที่มีตั๋ว relog) → ออกเกม → login ใหม่ (เกิดกลางทะเล Rising Sun Sea) → `/warp 2` → **ชื่อมอน Fighting Fish ต้องไม่เขียว คลิกโจมตีได้** · **ตัวละครต้องไม่มีหลอดสีฟ้าเหนือหัว**
- ชั้น wire (เทียบไบต์เฟรม `FOUNDATION_SELECTED_START_GAME` ตอน login เข้า 126): ต้องมี mask `0x074F` (ไม่ใช่ `0x034F`) และมีฟิลด์ `basic_faction=1` (`14 01 00 00 00` หลัง scene block) — เทียบกับ `KA1A-R321` ภาคผนวก B

ATTENDED: กด/พิมพ์: `/warp 126` (บัญชี GM ที่อยู่ใน allowlist) → ปิด client → เปิดใหม่ login → `/warp 2`
ATTENDED: ดู: ชื่อมอน Fighting Fish ในฉาก 2 (สีเขียว=FAIL, สีอื่น=ผ่านเกณฑ์นี้) · หลอดสถานะเหนือหัวตัวละคร (มี=FAIL)
ATTENDED: ผ่าน/ไม่ผ่าน: ตัดสินจากสีชื่อมอน + คลิกโจมตีได้ + ไม่มีหลอดฟ้า — ไม่ใช่จากตัวเลข HP (P-2 สีชื่อมอนที่ถูกต้องยังเป็นชั้นแยก B ไม่เกี่ยวกับใบนี้)
ATTENDED: บูต: ไร้ธง ไร้ env (FLAGLESS) · ต้องมีบัญชี GM ในตั๋ว relog 126 (ดู `tests/test_gm_warp_relog_stage.py`)
ATTENDED: 🆕 ชั้น wire ผ่าน R322A แล้ว (`PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` ที่ login 126 ผ่าน return ticket 2026-09-06T18:40+07:00) — เหลือแค่ `/warp 2` ดูสีชื่อมอนบนจอ (ชั้น client-observable) เท่านั้น · เติมโดย LANE-K รอบ `cu7c2r` ตาม `COO-DECISION 20260906_1955` ข้อ 1 · ผล `notes_to_chief/20260906_1909_KA1A-R322A-RESULTS-*.md`

**nonclaims**
- ไม่ยืนยันสีมอนที่ "ถูกต้อง" ตามเกณฑ์ P-2 (เหลือง/ส้ม/แดง/เทา) — ใบนี้วัดแค่ "ไม่เขียว/ตีได้/ไม่มีหลอดฟ้า" (อาการของ §1) เท่านั้น

**links**: `COO-DECISION 20260906_1347` (`notes_to_chief/20260906_1347_COO-DECISION-ka1a1255-...-LANE-A.md`) · `KA1A-R321-RESULTS §1` (`notes_to_chief/20260906_1255_KA1A-R321-RESULTS-...md`) · PR pf_bridge (claim `[LANE-A] round q02brx`) · PR pirate-force-server (round q02brx)

### result:
อ้างจาก `notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-GT281-screen-PASS-GT279-execute-0x51E9-x3-bg0002-hostile-gap.md` (R322B, ka1-A attended, OBSERVER_CONFIRMED 2026-09-07T01:05+07:00) คำต่อคำ:

> ขั้น: login Arena01 ฉาก 1 → `/warp 126` (วาปสด) → X → relaunch (1545) → login **ลงทะเล 126 ผ่าน return ticket** (`WORLD_SCENE scene_id=126 … return_ticket=REQUIRED` บรรทัด 1245) → `/warp 2`
> wire: `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` **บน login ทะเล** (บรรทัด 1248) — สิ่งที่ R321 ไม่มี
> จอ (Panya + ภาพ): Fighting Fish soldier ชื่อ**ชมพู ไม่เขียว** · คลิกโจมตีติด · มอนตาย · wire: `damage announced -966, applied 966, hp 3138 -> 2172` (max HP ตรงตาราง 3138)
> **หลอดฟ้าใต้ชื่อ + แผงตัวเอง HP -1**: ยังมีอยู่ **ทั้งที่ faction มาครบ** ⇒ **ไม่ใช่เรื่องฝ่าย** — R321 โยงหลอดกับ faction **ผิด** — ขอให้ A แยกเกณฑ์ "ไม่มีหลอดฟ้า" ออกจากใบ 281 ไปเป็นใบสร้างของ A/DB
> **ปลดล็อก**: GT-220 / GT-223 (BLOCKED จน GT-281 ผ่านจอ) เดินต่อได้

RESULT: GT-281 PASS R322B 2026-09-07 00:55 (sea login ships basic_faction=1 · /warp 2 mob names pink not green · attack+kill OK · blue bar = boat HP not restored, separate ticket)

พับโดย LANE-K รอบ `2a32q2` 2026-09-07T02:12+07:00

> numbering: ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืน **280** (`RE-280`, ตั้งเลขรอบเดียวกัน `zqq4qz` ก่อนหน้าใบนี้) ⇒ ใบนี้ **281** · ตรวจ 0 hit ของ `GT-281`/`RE-281` ทั้งสามที่ (`GAME_TEST_QUEUE.md` · `CLIENT_RE_QUEUE.md` · `archive/*QUEUE*ARCHIVE*.md`) + ไม่มี RESERVED ใน `NOW.md` ก่อนวาง [ตรวจโดย LANE-K รอบ `zqq4qz`]

**ผู้เปิดใบ: LANE-A (ผ่าน `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md`) -- ตั้งเลข/วาง: LANE-K รอบ `zqq4qz` -- ผู้บริโภคผล: LANE-A**

