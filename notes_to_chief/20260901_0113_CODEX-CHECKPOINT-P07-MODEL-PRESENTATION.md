[ถึง: Panya / ผู้ออกใบสั่ง / chief · จาก: OpenAI Codex]

# CODEX CHECKPOINT P0-7 — MODEL PRESENTATION · CHECKPOINT_1

- เวลา checkpoint: `2026-09-01 01:13 +07:00`
- แก้ไขหลัง adversarial review: `2026-09-01 02:18 +07:00` — ถอน comparator V1 ที่ไม่มี stable row identity, แทนด้วย V2 และแก้ provenance labels; generation/artifact rows ไม่เปลี่ยน
- สถานะ: `REVIEW ONLY / HOLD FOR PANYA` — Claude อ่านตรวจได้ แต่ไฟล์นี้ไม่ใช่คำสั่ง ingest, แก้ ServerProject, commit หรือ release
- generation: `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`
- image: `GameClient.local.bin`, 14,759,424 ไบต์, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- สถานะรวม P0-7: `PARTIAL / CHECKPOINT_1`; active lane ยังเป็น P0-7 และยังไม่ปลดไป P0-8
- รอบนี้ไม่แก้/รัน ServerProject, server, เกม, dump หรือ capture และไม่ commit/push

## ผลสำคัญ

1. **[ORIGINAL EVIDENCE: IMAGE]** ปิด narrow runtime mapping ใหม่ 3 ช่อง: `n_BOUNDARY -> MOBS_RUNTIME+0x04`, `n_HEIGHT -> +0x08`, `s_OUTFIT -> +0x108` token vector. ทั้งสามแถวเป็น `PROVEN_EXACT` เฉพาะ loader/copy/tokenization ที่ระบุ ไม่พิสูจน์ render, collision, physics หรือ selection policy
2. **[ORIGINAL EVIDENCE: IMAGE]** `f_SCALE -> +0x0C` พิสูจน์ได้เฉพาะ exact key, constructor default `0.0` และ load. Typed effect consumer, หน่วย และความหมายของศูนย์ยังไม่พิสูจน์; ห้ามเรียก `0.0` ว่า no-op
3. **[MEASURED][LOCAL TOOLING over source-separated rows]** เพิ่ม `PF_MONSTER_PRESENTATION.tsv/.md`: 2,697 แถว = DATA 2,688 / IMAGE 9. IMAGE มี canonical MOBS runtime refs 4 ช่อง (`+0x04/+0x08/+0x0C/+0x108`) และหลักฐานใหม่ 5 แถว; ไม่มีแถวผสม source และไม่มี proprietary raw bytes
4. **[ORIGINAL EVIDENCE: DATA]** Pike ID 5 เก็บ token `P_MALE_002_000_PAK`; descriptor เป็น composite 6 Parts / 6 ordered NifFiles และมี ActionList หนึ่งชุดที่มี Action 0 รายการ. ข้อนี้ไม่พิสูจน์ว่า runtime เลือก token นี้หรือ render เทียบเท่า original server
5. **[ORIGINAL EVIDENCE: DATA]** Mountain Deer ID 27 มี SP1/SP2 และทั้งคู่มี active SENTRY metadata เหมือนกัน. DATA จึงไม่สนับสนุนข้อสรุปว่าเปลี่ยน SP1 เป็น SP2 แล้วจะแก้ initial pose และไม่พิสูจน์ runtime selection/visual equivalence
6. **[ORIGINAL EVIDENCE: IMAGE]** candidate `Actived` ที่เคยโยงไป Avatar ถูกหักล้าง: exact path ที่พบเป็น property family ของ `SceneFogCmp`. หลัง bounded alias rounds ยังไม่มี type-preserving bridge จาก `MOBS +0x108` ไป Avatar filename/parser/active selection

## ความเปลี่ยนจาก P0-6

- **[MEASURED][LOCAL TOOLING]** Artifact count `46 -> 48`
- **[MEASURED][LOCAL TOOLING]** Runtime rows `13 -> 16`; ปัจจุบัน `PROVEN_EXACT 9 / PROVEN_ROLE_ONLY 6 / UNKNOWN 1`; runtime-open คง `7`
- **[MEASURED][LOCAL TOOLING]** Unified unresolved `976 -> 977`: active claims `464 -> 465`, standalone conflict workคง `512`. แถวใหม่หนึ่งแถวคือ `MONSTER_PRESENTATION@ACTIVE_SELECTION#N`; เป็น coverage expansion ของ boundary ที่เดิมไม่ได้ลงทะเบียน ไม่ใช่ field regression
- **[MEASURED][LOCAL TOOLING]** Field semantics คง `490` แถวและ hash เดิม `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`; field semantic/status/scope เดิมเปลี่ยน `0` แถว
- **[MEASURED][LOCAL TOOLING]** Conflicts คง `1,286` (`OPEN 640 / non-OPEN 646`); DATA bindingsคง `78`; probe requestsคง `0`

## การสร้างซ้ำและ fail-closed

**[MEASURED][LOCAL TOOLING]** ค่าต่อไปนี้มาจาก hash/count/reader checks ของ generation ที่ระบุ; ประโยคโครงสร้าง Pike แยกอ้าง **[ORIGINAL EVIDENCE: DATA]**:

- **[MEASURED][LOCAL TOOLING]** generator SHA-256 `afd0dd0820882e4cd93e21009c488dc08ea6960c0a03bb00236de0ddaf66fb9e`
- **[MEASURED][LOCAL TOOLING]** manifest SHA-256 `45c85e4200aae9b677f63ae3d495f57771ae0ff9b14726fd55a417472138f94e`
- **[MEASURED][LOCAL TOOLING]** การรันครั้งแรกหยุดก่อน publish ที่ Pike Nif cardinality เพราะ parser เดิมคาด NifFile เดียว; **[ORIGINAL EVIDENCE: DATA]** Pike มี exact six-part / six ordered NifFiles และ ActionList ว่างหนึ่งชุด. จากนั้นแก้ branch เฉพาะ Pike โดยคง invariant ของ lexical M descriptors อีก 615 ไฟล์
- **[MEASURED][LOCAL TOOLING]** หลังแก้ รันสำเร็จสองรอบได้ generation ID เดิมทุกครั้ง; checkpoint reader ผ่าน, hashes/sizes/mirrors ผ่าน 48/48, stage ค้าง 0 และ image hash ก่อน/หลังไม่เปลี่ยน
- **[MEASURED][LOCAL TOOLING]** independent adversarial review recompute generation ID, canonical row digests, source partitions, Pike structure, unresolved/conflict counts และไม่พบ generated-artifact defect

## CHECKPOINT comparator ที่บังคับใช้ stop rule

**[MEASURED][LOCAL TOOLING]** ไฟล์นี้เป็น checkpoint record; หลักฐาน authoritative คือ generation `b96e420c…`. Comparator V1 ถูกถอนก่อน handoff เพราะไม่มี stable row identity และอาจพลาดการสลับ status ระหว่างคนละแถว. Comparator V2 prepend identity column ของแต่ละตาราง แล้วสร้างแต่ละบรรทัดด้วยค่าคอลัมน์ตามลำดับคั่น TAB, sort แบบ ordinal, join ด้วย LF โดย **ไม่มี trailing LF**, แล้ว SHA-256 UTF-8:

- `field_status_vector_v2`: `semantic_row_key,field_key,direction,semantic_status,scope_status` จาก field rows; unique identity `490/490` → `570a068f3776786a3de5487800f26300fa31b441fb13a7e7c3bf15039bedbf17`
- `runtime_status_vector_v2`: `runtime_key,class,offset,semantic_status` จาก runtime rows; unique identity `16/16` → `8ec1fc7bbab71dd71026234ba9774227b55b5d26317c71535e577c11612e8728`
- `presentation_status_vector_v2`: `presentation_id,field_key,row_kind,semantic_status` จาก presentation rows; unique identity `2,697/2,697` → `70cab27f6bcf9c8c1a5895e0f4f751fcecd6026518fd2f0cfba116dae6898bef`
- `active_unresolved_vector_v2`: `unresolved_key,field_key,unresolved_kind,semantic_status,scope_status` จาก unresolved rows หลังตัดเฉพาะ `OPEN_CONFLICT_WORK_ITEM` ออก; active rows และ unique identity `465/465` → `7c4d2178986c391e91fa7c3fae6c84b8fcaacdfce4b50ef07bfc0be5559571a2`

**[RECONSTRUCTED POLICY]** `no_change_streak=0` เพราะ CHECKPOINT_1 เพิ่มสาม exact runtime rows/coverage. CHECKPOINT_2 ต้อง recompute ทั้งสี่ vector: ถ้าทั้งสี่เท่าเดิมให้ streak เป็น 1; ถ้ามีตัวใดเปลี่ยนให้ reset เป็น 0. อนุญาตให้พัก P0-7 แบบ static ได้เมื่อมี future no-change checkpoint records ติดต่อกันจน `streak=2` เท่านั้น—checkpoint ถัดไปเพียงรอบเดียวไม่ทำให้หยุดอัตโนมัติ

## สิ่งที่ยังเปิด

1. typed effect consumer ของ `f_SCALE +0x0C`, รวมหน่วยและความหมายของ default `0.0`
2. type-preserving `MOBS +0x108` token-vector -> Avatar filename/parser/selected descriptor/initial action bridge
3. runtime handling ที่อธิบายความต่าง Pike pose/deer herd density/size โดยไม่ยกภาพนิ่งหรือ DATA token order เป็น original-server policy

P0-6 ถูกพักไว้ที่ `PARTIAL / PAUSED BY STOP RULE`; ห้ามเปิด FightingDrop search กลับมา preempt P0-7 เว้นแต่มี genuinely new exact evidence หรือ owner direction

## ไฟล์ให้ตรวจ

**[MEASURED][LOCAL TOOLING]** ขนาดและ SHA-256 ต่อไปนี้ตรวจจากไฟล์ local โดยตรง; source ของแถวภายใน artifact ยังคงแยกตามคอลัมน์ของแต่ละไฟล์:

- `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_GENERATION_MANIFEST.json` — 8,202 ไบต์ — SHA-256 `45c85e4200aae9b677f63ae3d495f57771ae0ff9b14726fd55a417472138f94e`
- generation `...\.pf_attr_generations\b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae\PF_MONSTER_PRESENTATION.tsv` — 4,685,803 ไบต์ — SHA-256 `07135e4ff488cdd98c68f02c3be673479279c0e8361bf7a34721ea925bfe9f81`
- generation `...\PF_MONSTER_PRESENTATION.md` — 5,105 ไบต์ — SHA-256 `cf92eb5cc6955e6b443058a663f99c68c21865f0f9bf027db76cd9e33aeaffa4`
- generation `...\PF_ATTR_RUNTIME_FIELDS.tsv` — 20,578 ไบต์ — SHA-256 `e62c446a4f887a337e16e5a63b7c9b382a8f890bf0a98a93572b9744eaf8ff6b`
- generation `...\PF_ATTR_UNRESOLVED.tsv` — 2,355,364 ไบต์ — SHA-256 `07f3012fbdf5b9c1c61a455b1ce949f27e1d1c0d0e73ac1102bf97a4220463a0`
- cumulative audit `C:\Users\Panya\Desktop\Pirate Force\Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 108,156 ไบต์ — SHA-256 `49fffde386935c6ebd2259db174fe1b2f4268154aac22ecfef224b1f934fb5fb`
- immutable pre-edit snapshot `C:\Users\Panya\Desktop\Pirate Force\audit_history\Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_0218.md` — 106,095 ไบต์ — SHA-256 `5ea8f78517b6c5eaecabbfdb8a6cab055f36907014a95d332b4e9fea9048d322`

ไฟล์ทั้งหมดเป็น local external/audit artifacts ยังไม่ใช่ committed/released package. รายงานหลักคง `HOLD FOR PANYA`
