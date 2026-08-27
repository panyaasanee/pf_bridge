[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-071 RESULT — DONE / STATIC-CONTRADICTION-PINNED

- เวลา: `2026-08-25T21:21+07:00` (ค.ศ.)
- หมวด: `STATIC-ON-BRIDGE` เท่านั้น — ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่ทำ git operation, ไม่แก้ source/queue
- อิมเมจ: `GameClient\GameClient.local.bin` · 14,759,424 B · SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- วิธี: PE section mapping รายเซกชัน + byte-exact guards + bounded/recursive CFG บนช่วงที่ระบุ; **ไม่ได้ใช้ linear disassembler เป็นหลักฐานของผลลบ**

## ช่องบังคับก่อนขุด

- **ค้นใน `pf_bridge\external\` แล้ว:** เจอ `BasicAttr`/`ActorAttr`/`MovementAttr` ใน `PF_PROTOCOL_REGISTRY.tsv`, `PF_SERIALIZER_FIELDS.tsv`, `PF_FIELD_VALIDATION.tsv`; `BasicAttr`/`ActorAttr` ถูก capture-mark เป็น `NOT_OBSERVED`; และเจอกับดักตามใบว่า `0x0043BB80` เป็น stub ร่วม `wire_empty_argument_value_copier` ไม่ใช่ serializer จริงของ `MovementAttr` จึง **ไม่ใช้ EMPTY เป็นผลลบ**
- **ค้น `gamedata` แล้ว:** เจอ template คู่ควบคุมครบ — `TEXTDATA_TH__MESSAGE.tsv` id 413 = ` $V1  บาดเจ็บหนักและล้มลง!`, id 414 = ` $V1  ตาย!`; `TEXTDATA_TH__MESSAGE_BATTLE.tsv` id 13 = `$V1 บาดเจ็บล้มลง!`, id 14 = `$V1 ตาย!`; และเจอ `_F_DIE_000` ใน `CONSTDATA_TH__BEHAVIOR.tsv`/`BUFF.tsv` หลายแถว (ข้อมูลเกม ไม่ใช่ proof ของ execution path)

## S0/S0b — ด่านคุม

- image sha/size ตรง pin
- VA→file offset ใช้ section table จริง: `.text` delta `0x400C00`, `.code` `0x401000`, `.rdata` `0x401C00`, `.data` `0x402800`
- rerun `tools/pf_runtimeres_actor_entry_static.py --json`: binary controls รวม `0x446F30` ตรง แต่ process exit 1 เพราะ source-census รุ่นเก่าคาดจำนวน call/module ก่อนงานใหม่ใน `src/`; **ไม่ใช่ binary mismatch**
- verifier เฉพาะ RE-071 ที่อ่านอิมเมจอย่างเดียว: guards `15/15` ผ่าน

## คำตอบ T1–T7

### T1 — ActorAttr ของ entry ถึง actor จริง

`actor_type=2` เลือก jump-table case `0x4469E1` → `CNetActor`. ที่ spawn path `0x446AAD` เรียก actor vtable `+0x10 = 0x454920`; `CNetActor::init` เรียก attr-list loop `0x5DF080` ที่ `0x454949`. Loop เดินสมาชิกจริงจาก vector `[entry+0x30..+0x34)` และเรียก attr vtable `+0x38` ทุกสมาชิก (`0x5DF0AF..0x5DF0BB`). ดังนั้น `ActorAttr` ของ `SPAWN_BARE` **ไม่ถูกข้ามโดย construction path**.

### T2 — resident object และ ctor defaults

`CNetActor` ctor เก็บผล pool `0x1031500` ที่ `[actor+0x348]` (`0x4573CA`). ไล่ allocator `0x456D20` ต่อแล้ว: fallback จอง `0x1C0` bytes และเรียก `ActorAttr::ctor 0x464BE0` ซึ่ง chain `BasicAttr::ctor 0x464A80` — ปิดช่องเดิมที่รายงาน CHUNK2 ติดป้ายเพียง INFERRED ว่า pool นี้คืน ActorAttr.

ค่า fresh ctor ที่ยืนยันจากไบต์:

- `BasicAttr +0x28` name = `L""`
- `+0x44` current HP = `0`
- `+0x48` max HP = `0`
- `+0x58` timer = `0.0f`
- `+0x5E` level = `1`

### T3 — bind gate ผ่านและ CopyTo ต้องเขียน resident

`ActorAttr` vtable `+0x38 = 0x469760`; gate `CNetActor` ผ่านสำหรับ actor ที่ case 2 เพิ่งสร้าง. ที่ `0x46978F` อ่าน `[actor+0x348]`, แล้ว `0x469795` เลือก incoming attr vtable `+0x24 = 0x464F30` และเรียก `incoming->CopyTo(resident)`. `0x464F30` chain `BasicAttr::CopyTo 0x464B40` ซึ่งก๊อป name `+0x28` และ HP `+0x44/+0x48` **โดยไม่ดู mask**.

ผลชี้ขาด: ถ้า parsed `SPAWN_BARE ActorAttr` มี name `ProbePlayer01` และ HP `100/100` ตามไบต์ encoder ที่ใบพินไว้ ค่าเหล่านี้ **ต้อง**ไปถึง resident `[actor+0x348]`; เส้นทางนี้ไม่ให้ผล name ว่าง/HP 0.

### T4 — HP 0 + timer 0 ตก death-task branch

- actor vt `+0x40 = 0x454AC0`: `HP==0 && timer>0` → false เมื่อ timer `0.0`
- actor vt `+0x3C = 0x454A70`: `HP==0 && timer<=0` → true
- `0x4437C0` เก็บผล `+0x3C` ที่ `[esp+0x13]`; gate `0x443990` เปิด → `0x4439E9` สร้าง `CActorTask_Dead 0x472810`

จึงยืนยันกลไกตายเมื่อ resident เป็น ctor-default แต่ **ไม่อธิบายว่าทำไม incoming 100/100 ไม่ถูก CopyTo**.

### T5 — producer ของ `$V1 ตาย!` ผูกกับ GetName โดยตรง

เจอคู่ producer/control แบบ byte-exact:

- death `0x5CB830`: เลือก id `0x019E` (= MESSAGE 414) หรือ `0x032E` (= MESSAGE_BATTLE 14) ตาม `[actor+0x358]`; actor ที่ไม่ใช่ local ถูกเรียก vtable `+0x78` (GetName) แล้วส่งสตริงนั้นเป็น `$V1` เข้า `0x5CA2F0`
- downed control `0x5CB9A0`: โครงเดียวกัน ใช้ id `0x019D` (= 413) / `0x032D` (= 13) และส่ง GetName เป็น `$V1` เหมือนกัน

ดังนั้นข้อความ `ตาย!` ที่ไม่มีชื่อนำหน้า = producer ได้ GetName ว่างจริง; ไม่ใช่ template ที่ไม่มีช่องชื่อ.

### T6 — target panel อ่าน resident HP pair; ไม่มี branch “ซ่อน /max เมื่อ max=0”

- target selection `0x51F920` resolve actor → vt `+0x74` resident attr → ใช้ `attr+0x28` ทำชื่อ
- target-panel update `0x51F150`: `0x51F194 mov ecx,[esi+0x44]` และ `0x51F197 mov ebp,[esi+0x48]`; ส่ง current/max เข้า helper `0x5AA5E0`
- helper ถ้า max เป็น 0 จะ **บังคับเป็น 1** (`0x5AA624 test edi,edi; jne; mov edi,1`) ก่อนอัปเดต progress/text; ไม่พบ branch ที่ซ่อน denominator เพราะ max=0 ใน CFG เต็ม `0x5AA5E0..0x5AA744`

ดังนั้นภาพ `HP. 0` สนับสนุน current HP=0 แต่ **การไม่เห็น `/max` ไม่พิสูจน์ max=0**; widget/layout/crop ยังเป็นตัวแปรเปิด.

### T7 — ท่านอนมาจาก task เดียว สอง lifecycle slots

`CActorTask_Dead` vtable `0xF0F048` มี `+0x08 = 0x4765C0` และ `+0x0C = 0x472850`; ทั้งคู่ gate `[actor+0x70] & 0x40` แล้ว push literal เดียว `L"_F_DIE_000"` เข้า actor vtable `+0x28`. `0x4765C0` ยังเรียก death producer `0x5CB830` ด้วย จึงรู้จากข้อความ `ตาย!` ว่า slot นี้รันในรอบจริง; แต่ภาพนิ่งแยกไม่ได้ว่าคำสั่ง pose ที่เห็นมาจาก `+0x08` หรือ update `+0x0C` เพราะทั้งคู่ส่ง literal เดียวกัน.

## คำตอบ objective / สถานะที่เสนอ

**เสนอปิด `RE-071` เป็น `DONE / STATIC-CONTRADICTION-PINNED`.** Static path ให้คำตอบกลับด้านอย่างชี้ขาด:

> actor ที่ถูกสร้างจาก `SPAWN_BARE` และรับ `ActorAttr` ที่มี name + HP `100/100` สำเร็จ ต้องมี resident name + HP `100/100`; name ว่าง/HP 0 เป็นค่า fresh ctor ซึ่งเกิดได้เมื่อ CopyTo ไม่ได้เขียนก้อนนั้น หรือเมื่อมี actor/attr คนละก้อน/การเขียนทับภายหลัง.

ดังนั้น **จอ name ว่าง/HP 0 ไม่สามารถถูกอธิบายว่าเป็นผลปกติของ ActorAttr ใน `SPAWN_BARE` เดียวกัน**. สิ่งที่ถูกหักล้างคือการเท่ากันโดยปริยายระหว่าง “ไบต์ SPAWN_BARE identity A ที่ server ประกอบ” กับ “actor ที่ถูก target/นอนตายในภาพ”. จุดแยกที่เหลือต้องวัด runtime identity/slot/wire หรือ `GT-072`; static จากอิมเมจใบนี้ไปต่อไม่ได้โดยไม่เดา.

## span pins ใหม่/ที่ re-verify

- `0x446990..0x446B2C` `5f68239f8661419da2ea9bea4e4a2cb9bcdcaa37fe6e4cd53b701116aeeb697d`
- `0x454920..0x4549DD` `d907227d59491e7955f5e22598979ae4d81a22492beb87791688a27c52bcc831`
- `0x45739A..0x4573F3` `3b79caa051d184d51cc0a7ec572172adfe8a8af6825a62767dee86f545b5b9bb`
- `0x464A80..0x464B34` `aefa3a436f15deb03fe6390bf3f7d05c67e420cfb22a58c254e8f0eea5e58dd6`
- `0x469760..0x4697A2` `6f8a3251bde10432e1352a93e082937957be89bff8f6aa28bfcec8b43a48aec1`
- `0x464F30..0x46520E` `48b18bc342646c53235ecabb466a177e3b41b61e72ba50b2ad5e5be8c62faf8f`
- `0x43BD70..0x43BDD2` `d71fdd888d1eeca36da6bd4ce3da0424360b1b7e741ca806eb9f59d2c8b3ac24`
- death/downed producers `0x5CB830..0x5CB99E` `2beed307f2ba44f550dc08c6900b6f8f6df3d2eb1a082dac49c3fdb274e64e37`; `0x5CB9A0..0x5CBAE9` `b9636cb17a381d658b6911c77183d569c2fc8cdc0e879cddc3a7808654c1ac97`
- target HP path `0x51F150..0x51F2AE` `4925925b19ac50520e6bad9e3719e5c9229c89a3dba1b191650e72cf357152e1`; helper `0x5AA5E0..0x5AA744` `e1d6795e1f79161cd07c357b52d821d3fb1340caffab556e5b2d32416f02ff18`
- dead-task slots `0x472850..0x4728F3` `e04385a8cd54b800add22c4c8c5cc751b4243e19d208d684acdb8af2b6350999`; `0x4765C0..0x47673F` `4d9bef4032398d41a5e2ab55619759dd9a10356b7402468d0287a98f8e22da60`

## nonclaims

- ไม่พิสูจน์ว่า actor ในภาพคือ identity A ของ `SPAWN_BARE`; ตรงกันด้านตำแหน่ง/เวลาไม่ใช่ identity crosswalk.
- ไม่พิสูจน์ว่า wire ที่ client รับตรงกับ bytes ที่ server-side encoder re-derive; รอบนี้ไม่เปิด capture และไม่เปิดเกม.
- ไม่ exclude การ overwrite resident ActorAttr หลัง `SPAWN_BARE` จากเส้นอื่นที่ไม่ได้อยู่ใน actor-entry list ของห้าเฟรมนี้.
- ไม่ตัดสิน `GT-036`, ไม่ออกแบบ `HYP-PF-038 v2`, ไม่แตะ displacement/NPC disappearance ของ `GT-072`.
- ข้อสรุปเป็นกฎของ shipped client image นี้ ไม่ใช่กฎของ original server.

## read-only integrity

- before: image SHA/size/256-byte guards ตรง; `external` tree 30 files SHA `cad40e792c35c993a7b98226fa6bbffa298e9db019a16dc330856efc694edbaa`; `gamedata` tree 1,109 files SHA `a3d01a9f4bc06703357849b16fd6f0d2fdfeec4bb03d2b33d89b24d97d5d5e66`
- after: ให้ดูบรรทัด `AFTER` ใน `logs/re_runner.log`; ต้อง IDENTICAL ก่อนปล่อย lock

