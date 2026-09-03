[ถึง: Panya / ผู้ออกใบสั่ง / chief cloud (cc) · จาก: OpenAI Codex LOCAL]

# CORRECTIVE CHECKPOINT P0-7 — MODEL PRESENTATION / COMPARATOR V2

- เวลา `2026-09-01T02:22:55+07:00` จาก `TZ=Asia/Bangkok date`
- สถานะ `REVIEW ONLY / HOLD FOR PANYA`
- ไฟล์นี้ **แทนที่** `20260901_0113_CODEX-CHECKPOINT-P07-MODEL-PRESENTATION.md` สำหรับการส่งต่อทั้งหมด เพราะไฟล์เดิมถูกแก้ทับภายหลังโดยผิดกฎ append-only ของ `notes_to_chief`; ห้ามใช้ข้อความ comparator V1 จากฉบับเดิม
- HEAD ที่ตรวจแบบ read-only `2de431daf70ceb93e3db668c16b88be8a0a0948f`; ไม่ได้บูต HEAD นี้
- จ็อบที่ใช้: ไม่มี (static-only, ไม่แตะคิว); เลขถัดไป: ไม่จองและไม่เปลี่ยน
- generation authoritative `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`
- IMAGE `GameClient.local.bin`, 14,759,424 ไบต์, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## ผลที่ยังมีผล

สถานะ P0-7 คือ `PARTIAL / CHECKPOINT_1`; ยังไม่ปลดไป P0-8

- **[ORIGINAL EVIDENCE: IMAGE]** ปิด narrow loader/runtime mapping เพิ่ม 3 ช่อง: `n_BOUNDARY -> MOBS_RUNTIME+0x04`, `n_HEIGHT -> +0x08`, `s_OUTFIT -> +0x108` token vector. นี่ไม่พิสูจน์ render, collision, physics หรือ selection policy
- **[ORIGINAL EVIDENCE: IMAGE]** `f_SCALE -> +0x0C` พิสูจน์ exact key, constructor default `0.0` และ load เท่านั้น; typed effect consumer, หน่วย และความหมายของศูนย์ยังเปิด
- **[MEASURED][LOCAL TOOLING over source-separated rows]** เพิ่ม `PF_MONSTER_PRESENTATION.tsv/.md` 2,697 แถว = DATA 2,688 / IMAGE 9; ไม่มีแถวผสม source
- **[ORIGINAL EVIDENCE: DATA]** Pike ID 5 มี token `P_MALE_002_000_PAK`, composite 6 Parts / 6 ordered NifFiles และ ActionList ว่างหนึ่งชุด; ไม่พิสูจน์ runtime selection/render equivalence
- **[ORIGINAL EVIDENCE: DATA]** Mountain Deer ID 27 มี SP1/SP2 พร้อม active SENTRY metadata เหมือนกัน; ไม่พิสูจน์ว่าเปลี่ยน SP จะแก้ pose หรือภาพจริง
- **[ORIGINAL EVIDENCE: IMAGE]** candidate `Actived` ถูก refute ว่าเป็น `SceneFogCmp`; type-preserving bridge จาก `MOBS+0x108` ไป Avatar filename/parser/active selection ยังไม่พบ

## Comparator ที่บังคับใช้ต่อจากนี้

Comparator V1 **เกษียณและห้ามใช้** เพราะไม่มี stable row identity. V2 สร้างบรรทัดด้วยคอลัมน์ตามลำดับคั่น TAB, sort แบบ ordinal, join LF โดยไม่มี trailing LF แล้ว SHA-256 UTF-8:

- field: `semantic_row_key,field_key,direction,semantic_status,scope_status`; identity `490/490`; `570a068f3776786a3de5487800f26300fa31b441fb13a7e7c3bf15039bedbf17`
- runtime: `runtime_key,class,offset,semantic_status`; identity `16/16`; `8ec1fc7bbab71dd71026234ba9774227b55b5d26317c71535e577c11612e8728`
- presentation: `presentation_id,field_key,row_kind,semantic_status`; identity `2697/2697`; `70cab27f6bcf9c8c1a5895e0f4f751fcecd6026518fd2f0cfba116dae6898bef`
- active unresolved หลังตัดเฉพาะ `OPEN_CONFLICT_WORK_ITEM`: `unresolved_key,field_key,unresolved_kind,semantic_status,scope_status`; identity `465/465`; `7c4d2178986c391e91fa7c3fae6c84b8fcaacdfce4b50ef07bfc0be5559571a2`

**[RECONSTRUCTED POLICY]** `no_change_streak=0`. CHECKPOINT_2 ต้องคำนวณ V2 ทั้งสี่ใหม่: เหมือนทั้งหมดจึงเป็น streak 1; ตัวใดเปลี่ยนให้ reset 0. พักแบบ static ได้เมื่อ future no-change checkpoints ติดต่อกันถึง 2 เท่านั้น

## สิ่งที่ยังเปิด / nonclaims

ยังเปิด: typed effect consumer ของ `f_SCALE`; type-preserving `MOBS+0x108 -> Avatar` selection bridge; runtime cause ของ Pike pose/deer density/size

รอบนี้ไม่มี client-observable หรือ wire/DB runtime result ใหม่; ไม่ได้รัน server, GameClient, dump หรือ capture; ไม่ได้แก้ ServerProject, workflow, queue, lease, Git หรือ canonical DB. DATA metadata ไม่ใช่ original-server policy และ checkpoint นี้ไม่อนุญาตให้ implement ค่าเดา

## ไฟล์ตรวจและสภาพแท่นตอนจบ

- manifest 8,202 ไบต์ SHA-256 `45c85e4200aae9b677f63ae3d495f57771ae0ff9b14726fd55a417472138f94e`
- `PF_MONSTER_PRESENTATION.tsv` 4,685,803 ไบต์ SHA-256 `07135e4ff488cdd98c68f02c3be673479279c0e8361bf7a34721ea925bfe9f81`
- `PF_ATTR_RUNTIME_FIELDS.tsv` 20,578 ไบต์ SHA-256 `e62c446a4f887a337e16e5a63b7c9b382a8f890bf0a98a93572b9744eaf8ff6b`
- `PF_ATTR_UNRESOLVED.tsv` 2,355,364 ไบต์ SHA-256 `07f3012fbdf5b9c1c61a455b1ce949f27e1d1c0d0e73ac1102bf97a4220463a0`
- cumulative audit 108,446 ไบต์ SHA-256 `6381f478f98d9b59e0c04abd8556387a9f340caa5c8c63c1e21d59fdb27f7224`
- immutable pre-edit snapshot `...b96e420c2902_20260901_0222.md`, 108,156 ไบต์ SHA-256 `49fffde386935c6ebd2259db174fe1b2f4268154aac22ecfef224b1f934fb5fb`
- project listener count `0`
- canonical DB SHA-256 `4ff37060d3a2e876a41a479a348e062557d6c2fa2ff355548faf81830a548454`, ตรง `CANON_SHA.txt`; ไม่ขยับจากค่าที่กำหนด

