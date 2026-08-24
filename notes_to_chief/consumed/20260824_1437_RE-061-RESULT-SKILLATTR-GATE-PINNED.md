# ถึง chief — RE-061 ปิดครบ: `CSkillModule` ว่างจริง; `CSkillAttr` ขี่ `UpdateAttrVital`; Skill window มี gate บน `CSkillAttr`

เวลา: 2026-08-24T14:37+07:00 · ผู้ทำ: OpenAI Codex local · งาน static ล้วน ไม่บูตเกม/server และไม่แตะ canonical DB

**[DONE — STATIC POSITIVE FOR `CSkillAttr` PREREQUISITE / STATIC NEGATIVE FOR `CSkillModule` WIRE]**

ประโยคเดียวตาม objective: `CSkillModule` vtable `0x00F48D88 +0x18` เป็น serializer ว่าง byte-exact (`mov al,1; ret 4`); `CSkillAttr` ไม่ใช่ standalone vital แต่เป็น attr block class-id `0x1661` ภายใน `UpdateAttrVital 0x309A`, มี W/R codec และ inbound apply จริง; เส้นเปิด `Skill_Main2` จาก K/ปุ่มเมนูสร้าง controller ที่อ่าน `CMyActor+0x3E8` และ method init `0x761ED0` คืน false ถ้า pointer/container ของ `CSkillAttr` ไม่พร้อม — ดังนั้น premise ว่า skill state เป็น prerequisite มี static support เฉพาะ `CSkillAttr`, ไม่ใช่ `CSkillModule`.

## ค้นสองที่ก่อนถอด

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** 50 match-lines ใน 4 ไฟล์ (`PF_PROTOCOL_REGISTRY.tsv`, `PF_PROTOCOL_PRIORITY.tsv`, `PF_SERIALIZER_FIELDS.tsv`, `PF_FIELD_VALIDATION.tsv`): registry/pins ของ `UpdateAttrVital`, `CSkillAttr`, `CSkillModule`; field rows เดิมตี `+0x18` ของสองคลาสเป็น EMPTY; validation ของ `CSkillAttr`/`CSkillModule` เป็น `NOT_OBSERVED`, ส่วน `UpdateAttrVital R` มี 69 frames/7 captures. คำตอบ carrier และ gate ด้านล่างตรวจซ้ำจาก image ไม่ได้ยก row EMPTY มาเดาต่อ.
- **ค้น gamedata แล้ว: เจอ** `SKILL_CONTEXT` 2,165 แถว, `HOTKEY n_ID=77 n_KEY_2=75 (K) s_NAME=ABILITY`, และ `MAINMENU n_ID=102 s_UINAME=Skill_Main2 s_BUTTON=Bt_main_Skill n_LIST=4`; **ไม่เจอ** token `CSkillAttr`, `CSkillModule`, `UpdateAttrVital` ใน gamedata (0 hit). Gamedata จึงเป็น crosswalk K/ปุ่ม→ชื่อหน้าต่างและค่าตารางเท่านั้น ไม่ใช่หลักฐาน wire/direction.

## 1. Pin verification — ผ่านสองทางอิสระ

Image ที่ใช้: `GameClient\GameClient.local.bin`, 14,759,424 bytes, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

| คลาส | RTTI / name | vtable | constructor เขียน vtable | executable dword refs |
|---|---|---:|---|---|
| `CSkillModule` | `.?AVCSkillModule@@` ที่ `0x0101E180`; name literal `0x00F48E84` | `0x00F48D88` | `0x754D40..0x754D64`, off `0x354140`, len 36, sha `e8a0c222df49cbb719557b4d4cd60675ce5de599fd385e7e803f1f5ca5498170` | 3: `0x754D58,0x75529F,0x755318` |
| `CSkillAttr` | `.?AVCSkillAttr@@` ที่ `0x0101B1C0`; name literal `0x00F48BB8` | `0x00F48B78` | `0x751B90..0x751BEA`, off `0x350F90`, len 90, sha `3abf69326a7a821bdecd8146e3e10094fbe17086eca54ead65b30124e905bcc4` | 2: `0x751BCA,0x751C2A` |

Raw vtable 64-byte hashes: Module `b77ef58261fed1a43b7a6f18ca05ddf7cfdcff8e4d7170eb63b2bae34228391e`; Attr `6777057f24854ecdf7726e59b57ebff436d304cf4be925170c7a0942231963ba`. RTTI raw hashes: Module `5481d347d43f956b7dd9cbc14a86b8736840af8a0c8377be745d9849fb87cc72`; Attr `525b2029fa3e8a45914eaa36192f69d28590556013dcc5598dbe1e7304da2d90`.

## 2. `CSkillModule` W layout — EMPTY จริง

- vtable `0xF48D88 +0x18 = 0x710440`.
- CFG `[0x710440,0x710445)`, file off `0x30F840`, len 5, sha256 `f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863`, bytes `B0 01 C2 04 00` = `mov al,1; ret 4`.
- **W layout: 0 fields, 0 tags, 0 body bytes.** ไม่มีเงื่อนไข/branch และไม่เรียก stream primitive.
- vtable `+0x1C = 0x73D360`: `[0x73D360,0x73D363)`, off `0x33C760`, len 3, sha256 `e598d0c3ba86d917b177d7adde0556aa99bc355543c57aee0a3e50b684dd7e99`, bytes `C2 04 00` = bare `ret 4`; จึงไม่มี inbound apply ของ Module ทาง slot นี้.
- candidate `+0x28 = 0x754EB0` ถูกไล่ recursive CFG ครบ `[0x754EB0,0x7550EE)`, off `0x3542B0`, len 574, sha `fcc46d48fd2580ae4a84e723902f7a577e36ae4b9373b4638402ef58ceb55f16`: เป็น routine ลงทะเบียนคลาสตระกูล skill (`CLearnSkillVital` ฯลฯ), ไม่ใช่ stream serializer. ไม่เอามาทดแทน slot `+0x18`.

**Verdict Module:** ไม่มี frame body ให้ server ส่ง และไม่มี decoder/apply ตาม vtable ที่ใบชี้; `0x1F7B` เป็น name-hash candidate ไม่ใช่ opcode.

## 3. `CSkillAttr` wire form และ carrier

จุดสำคัญที่แก้ row เดิม: สำหรับตระกูล Attr serializer จริงอยู่ที่ vtable **`+0x34`**, ไม่ใช่ `+0x18`.

### ตัว body ของ `CSkillAttr`

`CSkillAttr::Serialize = 0x7520B0`: CFG `[0x7520B0,0x752281)`, off `0x3514B0`, len 465, 154 instructions, decode errors 0, sha256 `9227cc6009fff2f20c79a3b19c395f9623d87f68a4ee3462e541aed62aa7e906`.

ลำดับ W/R แบบ byte-exact:

1. เรียก `DBAttribute::Serialize 0x467790` ก่อน:
   - tag `0x0B`, `u8 db_mask` (`this+0x20`)
   - ถ้า `db_mask & 0x01`: tag `0x32`, `u64 identity` (`this+0x18`)
   - span `[0x467790,0x4677E8)`, off `0x66B90`, len 88, sha `379f37ad0307e785fb4a230fc9f1871f69587e6a314da5930a3a4ed289e55608`.
2. tag `0x12`, `u16 record_count`.
3. ทำซ้ำ `record_count` ครั้ง: tag `0x12` `u16 key` → tag `0x12` `u16 opaque` → tag `0x14` `u32 opaque`.

R branch อ่านรูปเดียวกันและ insert record ผ่าน `0x751FC0`. ความหมายของ opaque 2 ช่องยังไม่ถูกตั้งชื่อ.

### Outer carrier

Carrier คือ **`UpdateAttrVital 0x309A` attr collection**, ไม่ใช่ standalone opcode:

- wrapper `0x5E42C0` rebase `this+0x14` แล้ว tail-jump W/R ไป `0x463DE0`; `[0x5E42C0,0x5E42E4)`, off `0x1E36C0`, len 36, sha `25c5f92bbee97425e0b91ea61f4028b6353e33e7702e3f5d7c4df0d7e682207f`.
- generic collection codec `0x463DE0`: `[0x463DE0,0x463FA2)`, off `0x631E0`, len 450, 155 instructions, errors 0, sha `888c2fac20948b7896ed105f46b84e94d01c9442f6535df9be36e6baa2335fc3`.
- outer tag chain: `0x12 u16 attr_count`; ต่อ element = `0x12 u16 attr_class_id` → `0x14 u32 body_len` → indirect call `attr vtable+0x34`.
- สำหรับ `CSkillAttr`, `attr_class_id = 0x1661`: registration thunk `0xC0C530..0xC0C548`, off `0x80B930`, len 24, sha `e783bd54d32e5afbe704c3b7aeaaab0e3f4e6ff6ac20785391c3cbdb0f6f86f1`, hash name literal `CSkillAttr` แล้วเก็บ AX ที่ `0x108A32C`; getter `0x751BF0..0x751BF7`, len 7, sha `db6f040e81fb32de9dd8f76bdbeb5ba1054bc000338e8ec220b0ffb8749a149e` อ่าน slot นี้.

ดังนั้น frame body เต็มคือ:

`UpdateAttrVital(0x309A) -> 0x12 attr_count -> 0x12 class_id(0x1661) -> 0x14 body_len -> 0x0B db_mask -> [ถ้า bit0: 0x32 identity] -> 0x12 record_count -> N*(0x12 key, 0x12 opaque_u16, 0x14 opaque_u32)`.

`0x1661` ใช้เป็น collection/class id เท่านั้น; **ไม่ใช่ standalone opcode**. `0x309A` เป็น outer vital id ที่มี anchor เดิมสามจุดใน cohort/hash และ server constants; raw image ไม่มี literal `0x1661`/`0x309A` เพราะ id ถูก derive ตอน init.

## 4. Inbound decode/apply — มีจริงสำหรับ Attr

- R ของ `0x463DE0` อ่าน count/class-id/body-len, resolve/construct attr ตาม class-id แล้ว indirect call `vtable+0x34`; จึงถึง R branch ของ `0x7520B0` สำหรับ `0x1661`.
- `UpdateAttrVital` handler `0x5F2400..0x5F261A`, off `0x1F1800`, len 538, 163 instructions, errors 0, sha `65a7095cc493e33988f816efcd63d48220ee9cf39437e543389d54e3718acfaf`: iterate attr blocks, เรียก incoming attr `vtable+0x10` เอา class id, resolve live target, แล้วเรียก incoming attr `vtable+0x24` เพื่อ apply/copy; ต่อด้วย local listener fan-out.
- `CSkillAttr +0x24 = 0x751C70`: `[0x751C70,0x751CB8)`, off `0x351070`, len 72, sha `1e8d5b2e6a7814bc88cec812188d05a8673aa5d3c69e9ba9c963a2d0cd98738e`; type-check target แล้ว copy DB base + ordered record tree.
- bind thunk `0x4698B0..0x4698F2`, off `0x68CB0`, len 66, sha `8faf7ce6e971b9a0a35bd1e7c13ceb09d0b3d4789cd188cbc1e75541d5d104e3`: type-check `CMyActor`, อ่าน `[actor+0x3E8]`, แล้วส่ง target เข้า attr `vtable+0x24`.

**Verdict direction/apply:** client มี inbound decoder+apply ที่ falsifiable ได้สำหรับ `CSkillAttr` ผ่าน `UpdateAttrVital`; ไม่มี path เทียบเท่าสำหรับ `CSkillModule`.

## 5. K / ปุ่มล่างซ้าย / gate ของ Skill window

### สอง input เข้าชื่อหน้าต่างเดียวกัน

- Gamedata: K = key code 75 ของ action id 77 `ABILITY`; ปุ่มล่างซ้าย = `MAINMENU` id 102, `Bt_main_Skill`, UI `Skill_Main2`.
- Hotkey dispatcher `0x5CFD10`: subtract id base `0x4B`, range 35; byte dispatch table index 2 (id 77) → case `0x5CFDAD`, ซึ่ง push UTF-16 literal `Skill_Main2` (`0xF290DC`) แล้วเข้า generic open path. switch+map raw spans:
  - `[0x5CFD10,0x5CFD99)`, off `0x1CF110`, len 137, sha `da23fcee0647e53c03a462debbe4675c3918d64e417f441d84581bf1e9d8e456`
  - `[0x5CFFD8,0x5D0043)`, off `0x1CF3D8`, len 107, sha `32d803143a2d4e331bfdae35e71824fd9c21ad20ad1dffc89c62588263a23b6a`.
- K case recursive path `[0x5CFDAD,0x5CFFD8)`, off `0x1CF1AD`, len 555, 84 instructions, errors 0, sha `25d1d73fcd790d38baef2a7f8d5447e655e13aeb9d8fa401509a7e4a9bf769c0`.
- ปุ่มเมนู handler `0x57C090..0x57C0CD`, off `0x17B490`, len 61, 21 instructions, errors 0, sha `0f88db3aa5617a0c21b859436a305c31d830bdc42d5ce968217d8742d39e5dfe`: ส่ง literal `Skill_Main2` เข้า UI manager แล้ว show/activate object ที่ได้.

### Gate อยู่ใน controller ของ `Skill_Main2`

- name factory เปรียบเทียบ `Skill_Main2` แล้ว allocate 0x8C bytes / call constructor `0x760DE0`; case bytes `[0x5D7ECF,0x5D7F37)`, off `0x1D72CF`, len 104, sha `31ae9f688d5f88dd0e50b57e7b9461db36836fe0293bd49fd46167169df86610`.
- constructor `0x760DE0..0x760E73`, off `0x3601E0`, len 147, sha `4c7ea9f7b2a1ea79376d77b50147b1b7b46632362b0b847f641d3c015aba1962`:
  1. เขียน controller vtable `0xF49D08`;
  2. อ่าน singleton local actor `0x1032EC4`;
  3. อ่าน `[actor+0x3E8]` ซึ่ง bind thunk อิสระข้างบน pin ว่าเป็น `CSkillAttr`;
  4. ถ้ามี ให้เก็บ `CSkillAttr+0x2C` (ordered record tree) ที่ `controller+0x88`; ถ้าไม่มี ปล่อย `+0x88 = 0`.
- controller vtable `0xF49D08 +0x18 = 0x761ED0` (vtable 31-slot hash `c052d825a7db1065efc64039f9b5c6b64cca6aead2b981e0f15ca7662a0016ef`). Init method `[0x761ED0,0x761FA3)`, off `0x3612D0`, len 211, 61 instructions, errors 0, sha `43121dd8793f395d5108f9c37f8915ebc045a24dd93ebfa828586515e66f033c`:
  - หลัง base checks มันตรวจ singleton และ `cmp [esi+0x88],0` ที่ `0x761F3B`;
  - null → `0x761EE7: xor al,al; ret` (init fail);
  - non-null → เดิน setup ต่อ, call population/update `0x760E90`, แล้ว `mov al,1; ret`.
- population `0x760E90..0x7612A3`, off `0x360290`, len 1043, 321 instructions, errors 0, sha `a8fb19f941ed8b40d9828468e6acb885469c6d9e6d67ddc40e7787ec22138b43`; ใช้ tree ที่ `controller+0x88`. แยกกันอีก path `0x75C600..0x75C835` อ่าน `ActorAttr+0x7C` ไป `NUMBERLABEL_SPNOW`; นั่นคือแต้มสกิล ไม่ใช่ carrier ของรายการสกิล.

**Verdict gate:** K กับคลิกปุ่มไม่ได้ gate ใน switch เอง แต่ controller init ของหน้าต่างเดียวกัน **gate บน `CSkillAttr` อย่างชัดเจน**. ถ้า `[actor+0x3E8]` ไม่พร้อม controller init คืน false ก่อน populate. `CSkillModule` ไม่ปรากฏในเส้นนี้.

## Corpus eligibility

- root inventory เต็ม: `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_INPUT_INVENTORY.tsv`, sha256 `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`.
- `EXPERIMENT_LEDGER.md` SCENE-013 ยืนยัน 6 logical sources / 2,621 decoded frames เป็น GameClient→local-emulator receive logsทั้งหมด; eligible original-server→client = 0.
- ผล corpus: **UNANSWERABLE**. ไม่สแกน raw bytes และไม่ใช้ “ไม่เจอ” เป็นผลลบ. หลักฐาน direction/gate ของใบนี้มาจาก image static ข้างบน.

## Read-only / hashes

- manifest ก่อน: `staged/re061_input_hashes_before.tsv`, sha256 `4535b646db3a71b4f60ac7c8bad863ab5ef0510b71af7081571854b54825f196`.
- manifest หลัง: `staged/re061_input_hashes_after.tsv`, sha256 `c2f74deb5d71509b1195c58d563995792c4b62a0e22f4edef6a3c2e86f9bf859`.
- compare 16 relied inputs: `RE061_INPUT_HASH_DIFF_COUNT=0`.
- reproducible recursive CFG/bytewise probe: `staged/re061_static_probe.py`, sha256 `6126f43473caa84b5fe86d4df99550b2827611c1c12fe11e8fec4e4a6c6d6bbc`.
- probe output: `staged/re061_probe_output.txt`, sha256 `f1c8bdfff95bf15e77d87cc8056da98a5a3650c70ad51ede851165e33b24a02e`.

## Nonclaims

- ไม่ claim ว่า original server เคยส่ง `CSkillAttr`, `CSkillModule`, `UpdateAttrVital` รูปนี้; corpus ตอบไม่ได้.
- ไม่ claim ว่า one packet จะทำให้ K เปิดแน่นอน: `0x761ED0` มี base/UI checks อื่นก่อนและหลัง gate; ผลนี้ pin ว่า `CSkillAttr` เป็น prerequisite ที่ falsifiable ไม่ใช่ว่ามันเพียงพอด้วยตัวเอง.
- ไม่ claim จาก static ว่า runtime GT-058 ขณะนั้น `[actor+0x3E8]` เป็น null; อาการ K/คลิกไม่เปิดสอดคล้องกับ gate แต่ต้อง observe runtime เพื่อยืนยันค่าจริง.
- ไม่ตั้งชื่อ opaque `u16/u32` ใน record และไม่ join กับ `SKILL_CONTEXT` เพราะไม่มี crosswalk field ใน code ที่พิสูจน์แล้ว.
- ไม่ใช้ linear disassembly เป็นหลักฐานผลลบ: span/census หลักมาจาก recursive CFG; linear context ใช้เฉพาะอ่าน positive xref/case ที่มี raw-byte hash.
- ไม่เปิดใบ/ไม่แก้ queue; chief เป็นผู้เปลี่ยนสถานะและตัดสินว่าจะเขียน opt-in sender หรือทำ attended probe ต่อ.
