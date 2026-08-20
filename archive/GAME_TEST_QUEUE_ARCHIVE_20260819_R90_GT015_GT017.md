# GAME TEST QUEUE — archive: GT-015 + GT-017 (ย้ายโดย chief รอบ 90, 2026-08-19 ~20:0x)

> **ทำไมถึงย้าย:** ทั้งสองรายการ **PASS แล้วในรอบใหญ่ #6** และ chief รอบ 89 บริโภคผลครบแล้ว
> (กรอกผลลงคิว + ปิดคำถามที่ค้าง) ⇒ ไม่มีอะไรค้างให้ผู้เทสทำอีก · ย้ายมาที่นี่เพราะไฟล์คิว
> โตเกิน 60KB ตามเกณฑ์งานแม่บ้าน · **เนื้อหาเดิมครบทุกบรรทัด ไม่มีการตัดทอน**
> pointer อยู่ในคิวหลักที่ตำแหน่งเดิม

---

## GT-015 HYP-PF-017: ลากไอเทมทับ slot ที่มีของ — client ยอมรับ swap response ไหม  [✅ PASS — รอบใหญ่ #6 · 2026-08-19 11:2x · บันทึกโดย chief รอบ 89]

✅ **PASS ทุกเกณฑ์ (รอบใหญ่ #6, HEAD ที่เทส `32878e0`, jobs 150/151, canonical ไม่ขยับ)** — ปิดคำถามที่ค้างตั้งแต่รอบ 65
- ลากไอเทมทับช่องที่มีของ → **สลับตำแหน่งจริงบนจอ** และ client ยิง `ItemOperateVitalReq op=4` tuple เดิม
- รายละเอียดเต็ม + ผังก่อน/หลัง อยู่ใน `notes_to_chief\consumed\20260819_1130_biground6-results-GT021-GT017-GT015.md`
- 🔴 nonclaim: ไม่มี persistence — เลนนี้ไม่มี write path ของกระเป๋าลง DB (เหมือนเดิม)

**— ด้านล่างนี้คือสเปกเดิมของรายการ เก็บไว้อ้างอิง (ผลจริงอยู่ข้างบน) —**


- objective: (claim เดียว — ชั้น client-observable) เมื่อลากไอเทมทับ slot ที่มีไอเทมอื่นอยู่
  ภายใต้ swap profile: **client แสดงผลทั้งสองไอเทมสลับที่กันไหม** (ของที่ลาก → slot ปลายทาง,
  ของเดิม → slot ต้นทาง, จำนวน/ชนิดไม่เปลี่ยน) · เทสนี้ยังเก็บข้อเท็จจริงสำคัญอีกข้อ:
  **client ยิง request แบบไหนตอนลากทับของ** (อาจ gate ฝั่ง client ไม่ยิงเลย / ยิง operation-4
  tuple เดิม / ยิง operation อื่น — มีแค่กรณี tuple เดิมที่ผ่าน lane นี้) · ชั้น wire/DB
  พิสูจน์แล้ว headless (`reports/PF_ITEM_SWAP001_OCCUPIED_DESTINATION_SWAP_HEADLESS_20260818.md`
  probe 5/5) — **อย่านับชั้น wire เป็นเกณฑ์**
- db: สำเนา canonical สด (copy + เช็ค sha ตาม LOCK — แก้ตามถ้าเปลี่ยน) · canonical ต้องไม่ขยับ
- server args: **boot ตรงผ่าน `pirateforce_foundation.app`** (launcher ไม่ forward ธง — บทเรียน GT-002)
  `--item-move-hypothesis-scenario scenarios\item_move_hypothesis_v111_occupied_swap.json`
  + `-SecondPasswordMode bypass` (แบบ job `067` เปลี่ยนเฉพาะชื่อไฟล์ scenario)
- steps:
  1. boot + login → เลือกตัวละคร → เข้าแมพ (PLAYBOOK 3–6) → เปิด backpack
  2. จดผังของใน backpack ก่อนเทส (คาด: 3 ช่องมีของ ตาม state canonical — จดจริงที่เห็น)
  3. **ลากไอเทมช่องแรกไปทับไอเทมช่องที่สอง** ปล่อยเมาส์ → สังเกต ~5 วิ:
     ทั้งสองสลับที่? / ของหาย? / เด้งกลับ? / error dialog (จดเลข ErrorData เป๊ะ ๆ)? / ค้าง?
  4. ถ้าสลับสำเร็จ: ลากกลับ (ทับอีกรอบ) → ต้องสลับกลับได้เหมือนกัน
  5. เปิด-ปิด backpack 1 รอบ → ผังยังถูกไหม (display consistency — คำเตือน CONSUMER-001:
     collection ภายใน client อาจ desync จาก display)
  6. teardown ตาม PLAYBOOK 7 + End task ตามแผนออกเกมปกติ
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** ทั้งสองไอเทมสลับ slot บนจอทันทีหลังปล่อยเมาส์ โดยไม่มี
    error dialog + ผังยังถูกหลังเปิด-ปิด backpack + (ถ้าทำได้) login รอบสองยังเห็นผังสลับ
  - **wire-DB (ยืนยันซ้ำตอน teardown):** `GAME_EVENTS_LIVE.txt` มี ItemOperateVitalReq
    ตอนลากทับ · console เห็น marker `HYP_PF_017_ITEM_SWAP_..._COMMITTED` (108B) ·
    `character_backpack_items` ใน run copy สลับ slot จริง · canonical ไม่ขยับ
- nonclaims: ไม่ claim นโยบาย server เดิม (ไม่มี golden — R21: 23/24 shape เงียบ) ·
  ไม่ claim stack merge ตอนลากทับของชนิดเดียวกัน (same-template ก็ swap — merge เป็น lane
  ของ stack_merge_and_limit) · ไม่ claim displacement ไปช่องว่าง · **ถ้า client ไม่ยิง
  frame เลยตอนลากทับ** = client-side gate → จดเป็น observation สำคัญ (falsify ครึ่ง client
  ของ HYP-PF-017 โดยไม่แตะครึ่ง server) · ถ้าเจอ ErrorData ใหม่ จดเลข = ข้อมูลออกแบบรอบถัดไป
- result: (ผู้เทสกรอก)
- 📌 **โน้ต ride-along รอบ 71 (ITEM-MERGE-001 / HYP-PF-018) — ถ้ามีเวลาเหลือหลังจบ GT-015 หลัก:**
  ชั้น wire/DB ของ **merge profile** พิสูจน์แล้ว headless
  (`reports/PF_ITEM_MERGE001_OCCUPIED_SAMETEMPLATE_MERGE_HEADLESS_20260818.md` probe 6/6 —
  ทิศ V111 เป๊ะ byte-equal golden เดิมที่ client เคยรับจริง + instance ใหม่ที่ slot 7) ·
  **ที่ยังไม่รู้ = client รับ merge delta ที่ slot ≠ 0 ไหม** · เทสนี้**ใช้ canonical copy ไม่ได้**
  (canonical = merged 3 ชิ้น ไม่มีคู่ same-template เหลือ) → ต้อง boot แยก: scratch DB สด (dev
  create flow ให้ INITIAL 4 ชิ้น) + `--item-move-hypothesis-scenario
  scenarios\item_move_hypothesis_v111_occupied_merge.json` → ลาก id1 (Adventure Key ช่อง 0)
  ไปช่องว่างไกล ๆ (เช่น 7) → แล้วลาก id3 (ชิ้น template เดียวกัน ช่อง 2) **ทับ** →
  คาด: เหลือ stack เดียวจำนวน 2 ที่ช่องปลายทาง, id3 หายจากจอ, ไม่มี error dialog ·
  console marker `HYP_PF_018_ITEM_MERGE_..._COMMITTED` (91B) · ลากทับของ**ต่างชนิด**ใต้
  merge profile ต้องเงียบ (fail closed) · optional ไม่บล็อกคิวหลัก — ถ้าไม่ทัน จดข้ามได้ ตอนทำ GT-015 ถ้าเปิด backpack แล้ว **ลากไอเทม stack (จำนวน > 1) ทับช่องว่าง** ระบบจะเด้ง dialog ถามจำนวน → นี่คือ path ของ **operation=6** (quantity-op, verb `eax==0x16`, dialog `0x5a1630`, dialog resource `0x12`). ถ้าเจอ dialog นี้ให้ **จับเฟรม `ItemOperateVitalReq` จริงจาก `GAME_EVENTS_LIVE.txt`** (op byte=6, value32=item handle, qword=จำนวนที่กรอก) — นี่คือหลักฐานที่จะ pin `verb 0x16 ≡ split`. **🩹 แก้จากรอบ 75 (USE-DROP-SELL-001):** ข้อความเดิมข้างบนที่เขียนว่า "dialog resource `0x12`" **ผิด** — `mov dword [esp+0x180],0x12` @`0x5A34D7` คือ **MSVC EH trylevel store** ไม่ใช่ dialog id (สล็อตเดียวกันรับ `0xFFFFFFFF` และ `0x0A` ด้วย) → **อย่าไปตามหา "dialog หมายเลข 0x12"** ให้จดเฉพาะ **caption ที่ขึ้นบนจอจริง** + เฟรมบน wire เท่านั้น (โครงสร้าง `0x5A349B → 0x5A1630 → guard>0 → op6` ยังถูกทุกอย่าง ยืนยันซ้ำแล้ว 88 guards)
  · **รอบ 69→70 ทำให้แคบสุดทาง static แล้ว (SPLIT-OPERATE-002 `08fb65b` + 003 รอบ 70):** op6 = **quantity-op family 4 call site** (`0x57D1F4`,`0x58294D`,`0x5A3532`,`0x5BA208`). **2 ใน 4 site gate ด้วย `cmp eax,0x16`** — site C `0x5A3532` ใน dispatcher `[0x5A2A70,0x5A40B0)` (เดียวกับ op4=move verb 2) **และ** site D `0x5BA208` ใน fn แยก `0x5B9F70` — ทั้งคู่วิ่งผ่าน dialog helper เดียวกัน `0x5A1630` ก่อน op6. คือ verb 0x16 + dialog ตัวเดียวกัน **ถูก reuse ข้ามพาเนล** (สอดคล้อง generic split-by-quantity แต่ยังไม่ใช่ป้าย split เชิงบวก เพราะ op6 ไม่มี dest-slot = เข้ากันได้กับ drop-N/destroy-N ด้วย). **🔴 static caption route ปิดแล้ว (evidenced):** dialog เป็น control กลาง `Common_NumInput.model` (plaintext XML ไม่มี caption ในตัว) — caption มาจาก text table `B_TEXTDATA_TH.pc_` ที่ **packed (`$pcz`)** → อ่านป้ายจากไฟล์ไม่ได้ถ้าไม่แตะ proprietary. **เหลือทางเดียว = live capture ตอน GT-015 นี้:** เมื่อเจอ dialog จำนวน ให้จด (ก) **caption/หัวข้อ dialog ที่ขึ้นบนจอ** (อ่านด้วยตา = ป้าย split/แบ่ง จริงไหม) และ (ข) จับเฟรม `ItemOperateVitalReq` จาก `GAME_EVENTS_LIVE.txt` (op byte=6, value32=handle, qword=จำนวน). ไม่ใช่ GT แยก — เก็บพ่วง GT-015 · server ยังไม่มี handler op6 → คาดว่า client ยิงแล้วเงียบ (จดยิง/ไม่ยิง = ข้อมูลออกแบบ handler)

> 📦 **[ย้ายไป archive รอบ 78]** GT-016 CHAT-CHANNEL-001 channel sweep — **✅✅ PASS ชี้ขาด (รอบใหญ่ #3)**: payload ไบต์เดียวกัน 5 เฟรม → client เรนเดอร์ 5 ช่อง 5 สี (`[ทั่วไป]`/`[ปาร์ตี้]`/`[กิลด์]`/`[GM]`/`[ทั้งหมด]`) ⇒ **channel id = class id พิสูจน์ที่ชั้น client แล้ว** · job = `staged\126/127` → `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260818_R78_BIGROUND3.md`

## GT-017 STATS-PROG-001: หลอด XP / เลข level บนจอขยับตาม UpdateAttrVital จริงไหม  [✅ PASS (มี 1 ข้อ "ไม่ยืนยัน") — รอบใหญ่ #6 · 2026-08-19 11:1x · บันทึกโดย chief รอบ 89]

✅ **PASS เต็ม ทั้ง 9 เฟรม client เรนเดอร์จริง** (รอบใหญ่ #6, jobs 148/149)
- `LV. 1` → `LV. 7` บน HUD · แชตขึ้น `ได้รับ EXP 1234` แล้ว `986420` ตามลำดับที่ส่ง · ข้อความเลเวลอัพของระบบ
- ability 5 ตัวลงหน้า `Char_Info2` ครบและ**เรียงตรงตามที่ static ทำนาย** (16/27/38/49/60)
  ⇒ ปิดข้อที่รอบ 76 จงใจไม่ claim (POTENTIAL column → offset) ที่ชั้น client แล้ว
- ⚠️ **ข้อเดียวที่ยัง "ไม่ยืนยัน" (ไม่ใช่ "ไม่ขยับ"): หลอด XP เอง** — แถบใต้หลอด HP หน้าตาไม่เปลี่ยนที่ตาเห็น
  ⇒ **งานค้างของ chief:** หาตำแหน่งหลอด XP จาก static (`.model` ของ HUD) แล้วบอกพิกัดให้ผู้เทสซูมตรงจุดรอบหน้า

**— ด้านล่างนี้คือสเปกเดิมของรายการ เก็บไว้อ้างอิง (ผลจริงอยู่ข้างบน) —**


- 🟢 **ปลดบล็อกแล้วรอบ 78 (commit `fc204c7`)** — prerequisite `STATS-PROG-002 server encoder` **เสร็จและ commit แล้ว**
  · encoder generic mask-driven 23 ฟิลด์ · **18/18 pin chief คำนวณสดใหม่ตรงหมด**
  · **หลักฐานที่แข็งที่สุด:** baseline body **73 ไบต์ byte-identical กับ `player_wire.make_actor_attr_with_name`**
    = โปรเจกชันที่ client จริงรับไปแล้วตั้งแต่ CHARACTER-NAME-002 ⇒ ไม่ใช่ของประดิษฐ์ใหม่
  · EXPERIENCE_1 vs EXPERIENCE_2 ต่างกัน **3 ตำแหน่งเป๊ะ (79,80,81)** ใน qword `+0xA0` ไม่รั่วไปที่อื่น
- 🔴 **server args (บังคับ — ต่างจากเทสอื่น):**
  `--stats-progression-hypothesis-scenario "<repo>\scenarios\stats_progression_hypothesis_xp_sweep.json"`
  · **mutually exclusive กับทุกเลน chat** (ชน vital id เดียวกัน) — อย่าใส่ธง chat มาด้วย
  · บังคับ `--db` ที่มีอยู่จริง · ใช้ **สำเนา canonical** ไม่ใช่ตัวจริง
- 🔴 **trigger = พิมพ์แชท ascii12 (เช่น `PFCHATPROBE1`) แล้ว Enter** — เนื้อหาไม่ถูกอ่านเลย
  เป็นแค่ปุ่มยิง · หนึ่ง request → **9 เฟรมเรียง เว้น 3 วิ/เฟรม (รวม ~24 วิ)**
  ลำดับ: `BASELINE → EXPERIENCE_1 → EXPERIENCE_2 → LEVEL → ABILITY_STR → CON → DEX → INT → PER`
- ⚠️ **ทุกเฟรมส่ง cumulative ไม่ใช่ delta** (client apply copy ทั้งอ็อบเจกต์ ฟิลด์ที่ตกหล่นจะถูกรีเซ็ต)
  ⇒ **เทสนี้ไม่ได้พิสูจน์ semantics ของ sparse delta เลย** — อย่า claim เกินนี้
- 📌 ยังไม่มี staged job ของ GT-017 — ผู้เทสสร้างจาก `staged\126_gt016_boot.ps1` ได้ (เปลี่ยนธง+scenario+ป้าย log)
- objective: (claim เดียว — ชั้น client-observable) ฟิลด์ progression ที่ STATS-PROG-001 ตั้งชื่อไว้จาก static
  **ควบคุมตัวเลข/หลอดบนจอจริง** — ยิง `UpdateAttrVital` mask bit `0x0400` (experience, ActorAttr qword `+0xA0`)
  แล้ว **หลอด XP ขยับ** · **ใช้ client เดียวพอ ไม่ต้อง two-client**
- ฐานหลักฐานที่มีแล้ว (static — **อย่านับเป็นเกณฑ์ผ่าน**):
  `reports/PF_STATS_PROG001_CHARACTER_STATS_AND_PROGRESSION_STATIC_20260818.md`
  — exp bar `0x519299` อ่าน `ActorAttr+0xA0` หารด้วย `STANDARD_STATUS[lv+1].n_EXP_CURRENTLV` แล้ว ×100 ·
  level `BasicAttr u16 +0x5E` mask `0x0002` (`GetLv` `0x460050`) ·
  ability `u16 +0x82..+0x8A` mask `0x20..0x200` → `LABEL_STR..PER` ใน `Char_Info2`
- db: สำเนา canonical สด · canonical ต้องไม่ขยับ
- steps (ร่างไว้ให้พร้อมเมื่อปลดบล็อก):
  1. boot + login → เลือกตัวละคร → เข้าแมพ (PLAYBOOK 3–6) · **จด XP/level/ability ที่เห็นบนจอเป็น baseline ก่อน**
  2. ยิง `UpdateAttrVital` mask `0x0400` ค่า exp = ครึ่งหนึ่งของ `n_EXP_CURRENTLV` ของเลเวลปัจจุบัน → **หลอด XP ควรไปที่ ~50%**
  3. ยิงซ้ำด้วยค่าที่มากกว่า → หลอดควรขยับตาม (ทดสอบว่ามัน render ค่าจริง ไม่ใช่ animation ครั้งเดียว)
  4. ยิง mask `0x0002` (level) → **เลข level บนจอเปลี่ยนไหม และหลอด XP คำนวณใหม่ตามเลเวลใหม่ไหม**
     (ข้อนี้ทดสอบ `STANDARD_STATUS[lv+1]` lookup ทางอ้อม)
  5. ยิง mask `0x20..0x200` (STR/CON/DEX/INT/PER) แล้วเปิดหน้า `Char_Info2` → เลข 5 ตัวตรงลำดับที่ static บอกไหม
     · **นี่คือข้อที่จะพิสูจน์/หักล้าง "การผูก POTENTIAL column → offset" ที่รอบ 76 จงใจไม่ claim**
  6. teardown ตาม PLAYBOOK 7 + End task
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** หลอด XP ขยับตามค่าที่ส่ง ≥2 ค่าที่ต่างกัน · ไม่มี error dialog · client ไม่ค้าง
  - **wire-DB (ยืนยันซ้ำ):** `GAME_EVENTS_LIVE.txt` เห็นเฟรม `0x309A` พร้อม mask ที่ยิง · canonical ไม่ขยับ
- nonclaims: ไม่ claim ตัวเลข curve (อยู่ใน static-data ภายนอก exe ไม่ใช่ในไบนารี) · ไม่ claim ว่า server
  ต้นฉบับให้ exp ด้วยวิธีนี้ · ไม่ claim persistence (ยังไม่มี write path ของ characters) ·
  **ถ้าหลอดไม่ขยับ = ผลลบที่มีค่า** → แปลว่า client ต้องการฟิลด์อื่นร่วมด้วย (เช่น level ต้องมาคู่กัน) จดเป็น observation
