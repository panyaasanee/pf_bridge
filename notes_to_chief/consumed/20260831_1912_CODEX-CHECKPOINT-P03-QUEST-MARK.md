# CODEX CHECKPOINT P0-3 — CNetNPC QuestIconBoard / quest-mark static path

สถานะ: `LOCAL-AUTHORITATIVE / ADVERSARIAL-PASS / NOT COMMITTED / NOT RELEASED`  
เวลา: 31 สิงหาคม 2026 ประมาณ 19:12 +07:00  
จุดประสงค์: checkpoint สำหรับ Panya ให้ Claude ตรวจอ่านเท่านั้น ไม่ใช่คำสั่งแก้ ServerProject  
ขอบเขต: อ่าน GameClient/Data/รายงานเดิมแบบ read-only; ไม่รันเกมหรือเซิร์ฟเวอร์ ไม่แก้ ServerProject, Git, workflow, queue หรือ lease

## ผลหลักของ P0-3

1. ปิด static path ที่ audit แล้วสำหรับ `CNetNPC`:
   `CNetNPC+0x358 -> NPCAttr+0x78 (MOBS template key) -> client-local event kind 0x0A -> QuestAttr/MOBS/QUEST predicates -> selector 0..8 -> CNetNPC setter -> QuestIconBoard -> texture-binding lane`
2. `QuestIconBoard` อยู่ที่ `CNetNPC+0x360`, selector cache ที่ `+0x364`; เป็น sibling คนละ object กับ `NameBoard` ไม่ใช่ child ของ NameBoard
3. สร้าง `PF_ATTR_QUEST_MARK_SELECTOR.tsv` 10 IMAGE rows: selector valid 0–8 จำนวน 9 แถว และ out-of-range guard `>8` จำนวน 1 แถว
4. Resource literal ของ selector 1–8 ปิดครบ; selector 0 ตั้ง board-state bit และไม่ bind texture ใหม่ ส่วน `>8` ไม่ใช่ output จาก audited compute span
5. `ActorAttr+0x1A0` ยังคงเป็น negative control: เป็น Navy/Pirate side-icon path, scope UNKNOWN, withheld ทั้ง W/R และไม่ถูกใช้เป็น quest-mark selector
6. เพิ่ม typed `CNetNPC` W/R rows ที่ `NPCAttr+0x78` จำนวน 2 แถว โดยรักษา generic remainder W/R เป็น owner UNKNOWN; class proof ผูก type-node → vtable/getter → ctor → allocator/factory → typed filter → NPCAttr attachment → refresh consumer ครบ

## เงื่อนไข selector ที่พิสูจน์ได้แบบ bounded

- END path ใช้ QuestAttr lookup value 1 และ callback literal `Report_Check`; ให้ selector 3/4 และ fallback 5 ตาม branch ที่ตรึงไว้
- BEGIN path ใช้ lookup value 0, callback literal `Accept_Check`, `n_TYPE(+0x14)` และ opaque thresholds; ให้ selector 1/2 และ override 6/7/8
- `n_TYPE` 20/30 ถูก reject ใน audited BEGIN path; type sets 5/6/7/10/40 และ overrides 25/41 ถูกตรึงจาก IMAGE
- `n_LEVEL_QUEST(+0x18)` และ `BasicAttr+0x5E` ถูกเรียกเพียง field/opaque u16 threshold ตามหลักฐานนี้; ไม่ยก `BasicAttr+0x5E` เป็น player-level noun
- QuestAttr lookup 0 รวมทั้ง missing entry และ stored zero; values 2/4 ไม่เท่ากับ branch equality 0 หรือ 1
- ชื่อ callback ไม่ใช่ proof ว่า original server ใช้ gameplay semantics ชื่อเดียวกัน

## DATA และ proprietary boundary

- Packed quest textures 8 รายการถูก decode เฉพาะในหน่วยความจำเพื่อคำนวณ packed/decoded/alpha hashes, 64×64×32 header, alpha-plane geometry class และ alpha-weighted RGB palette class
- ไม่เขียน decoded/raw proprietary bytes ออกไฟล์แม้แต่ไบต์เดียว
- Texture rows เป็น `source=DATA`, subject `UNJOINED_GUI_TEXTURE_DATA`, และระบุ `binding_status=UNJOINED_TO_IMAGE_LITERAL`
- Selector rows เป็น `source=IMAGE` ทั้ง 10 แถว; ไม่มีแถวใดผสม IMAGE กับ DATA
- `.tga -> .tg_` live resolver ยังไม่พิสูจน์ จึงห้ามอ้างว่า client โหลด DATA asset เหล่านี้จริงจาก filename consistency อย่างเดียว

## ตัวเลขสะสมล่าสุด

- Field rows 490; unique wire keys 482
- Semantic: EXACT 231 / ROLE 190 / PARTIAL 27 / UNKNOWN 42
- Scope: EXACT 280 / UNKNOWN 210
- Exact semantic + exact scope 117; server-safe 100; exact/exact ที่ถูก OPEN conflict hold 17
- A2 overlay 206 = YES 33 / NO 173
- Semantic delta 300; unresolved ledger 966; conflicts 1,283 = OPEN 638 / non-OPEN 645
- Quarantine 0; approved probe requests 0
- DATA bindings 78 = DATA 77 + IMAGE loader-layout 1

## การตรวจ fail-closed

- Generation: `ffb2f17e4ed5d9ee44f59bb118525b49042baf3e88ec62496a96c946913d0b1e`
- Generator SHA-256: `b76aecc0be7b8bbc576f2da137335911627cf67f38ddf162d531d599c5808e16`
- สร้างซ้ำ 2 รอบได้ generation เดิม; authoritative reader ผ่าน; manifest ผูก 41 artifacts และ hashes/sizes ตรง 41/41
- IMAGE SHA-256 ก่อนและหลัง publish: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
- Fixed golden claim census ผูก selector claims 10/10 กับ evidence/selector keys
- Adversarial mutation 4 แบบถูกปฏิเสธจริง: BEGIN↔END, `n_TYPE`↔`n_LEVEL_QUEST`, lookup 0↔1 และ effect sets↔clears
- Pixel classification, DATA ownership/source separation และ final-PASS ordering ผ่าน re-review; ไม่พบ residual publication blockerในขอบเขต P0-3

## ไฟล์ที่ควรอ่าน

1. `pf_bridge/external/PF_ATTR_GENERATION_MANIFEST.json` — จุดเริ่มที่ authoritative; size 7,200; SHA-256 `d471ac122c25c3aaa720af83a0064dfff5d5f203cea031eccc6b4179d4c39f6e`
2. `pf_bridge/external/.pf_attr_generations/ffb2f17e4ed5d9ee44f59bb118525b49042baf3e88ec62496a96c946913d0b1e/PF_ATTR_QUEST_MARK_SELECTOR.tsv`
3. generation เดียวกัน: `PF_ATTR_FIELD_SEMANTICS.tsv`, `PF_ATTR_DATA_BINDINGS.tsv`, `PF_ATTR_SEMANTIC_REPORT.md`, `PF_ATTR_FOR_SERVER.md`, `PF_A2_ATTR_FIELD_DELTA.tsv`, `PF_ATTR_UNRESOLVED.tsv`, `PF_ATTR_CONFLICTS.tsv`
4. รายงานสะสมฉบับเดียวใน root: `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — ยังคง `HOLD FOR PANYA`

ห้ามหยิบ top-level TSV แยกชิ้นหรืออ้างว่า committed/released; ต้องอ่าน manifest แล้ว resolve generation directory นี้และตรวจ hash ก่อนเสมอ

## สิ่งที่ยังเปิดหลัง static P0-3

1. exhaustive subscriber/final-writer census ของ event kind `0x0A`
2. exact `.tga -> .tg_` runtime resolver
3. client-observable presentation/state lifecycle และ timing
4. แหล่ง state/transition ที่ original server ส่งจริง
5. selector 0 ห้ามตั้งชื่อ hidden/no-icon จนมี proof เพิ่ม

P0-3 static checkpoint จบแล้ว งานถัดไปตามลำดับ audit คือ P0-4: discriminator ที่ client ใช้แยก NPC / monster / training dummy โดยยังห้ามใช้ replacement-server behavior เป็นหลักฐานของ original client/server
