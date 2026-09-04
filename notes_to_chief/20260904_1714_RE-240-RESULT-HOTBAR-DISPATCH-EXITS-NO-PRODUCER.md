ถึง: LANE-CS · สำเนา: chief

# RE-240 RESULT — DONE / BOUNDED-NEGATIVE · HOTKEY `TOOLBAR*`/`SKILLBAR*` ทั้งหมดออกที่ dispatcher epilogue ไม่ถึง producer ใด

- เวลาเริ่มใบ: `2026-09-04T17:11:13.944+07:00`
- เวลาปิดใบ: `2026-09-04T17:14:51.370+07:00`
- ticket input: `CLIENT_RE_QUEUE.md` sha256 `792a6ea37b2c7817a3ed2dbe327882416d10a4d06b8ccaad6fbca872763d704b`; normalized RE-240 block sha256 `55a1d780c7cc7fcb52e7035e72c777966e15ec5b58f7bbf44a55690ac7e4abf2`
- image: `GameClient/GameClient.local.bin`, 14,759,424 bytes, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- verdict: **เส้นทางที่ใบกำหนดไม่ถึงทั้ง `0x44D260`/`0x74E6A0` (`ActionVital`) และ `0x600A60` (`TriggerCastSkillVital`)**. จบเพดาน static ที่ `0x4518F3` ก่อนมีการสร้าง frame จึงไม่มี skill-id offset/tag/width ให้ตั้งชื่อจากเส้นนี้.

## Skill/hotbar walk

dispatcher ทำดังนี้:

```text
0x450B20  mov   ecx,[edi+8]                 ; normalized HOTKEY id
0x450B23  lea   eax,[ecx-1]
0x450B26  cmp   eax,0x80                    ; ids 1..129
0x450B2B  ja    0x4518F3
0x450B31  movzx eax,byte [eax+0x4519C4]     ; class = table[id-1]
0x450B38  jmp   dword [eax*4+0x451970]      ; class branch
```

- selector span `[0x00450B20,0x00450B3F)`, 31 bytes, sha256 `f340b16436c9f7e75612e8ccbcbf51aacae769ab3db68143d6adcbe1d4af1b2b`
- class table `[0x004519C4,0x00451A45)`, 129 bytes, sha256 `c45aa425697c074ab8ca11947e8c1fc08047ded8b5b5f5e517598af01369b440`
- jump table `[0x00451970,0x004519C4)`, 21 dwords, sha256 `865229976ca0fa095f388fd9855b7ee4cd1a15306a601a1b5112cc0188bdc3f9`

จาก `CONSTDATA_TH__HOTKEY.tsv` (sha256 `040f047c0de5fd0aa18b7e7ddcb463a914c15b3d0de4533c1c1dc761555457f4`) มี named hotbar rows สองชุด:

- `TOOLBAR1_01..12`, `TOOLBAR2_01..12`, `TOOLBAR3_01..12`: HOTKEY ids `12..47`
- `SKILLBAR1..10`: HOTKEY ids `111..120`

ทั้ง 46 rows มี `n_TYPE=2`; ทุก byte ที่ `0x4519C4 + (id-1)` เท่ากับ `0x14` (class 20). Jump-table slot 20 ที่ `0x4519C0` เท่ากับ `0x004518F3`, ซึ่งเป็น epilogue (`xor eax,eax` แล้ว restore/return). ไม่มี call, allocation, object-field write หรือ queue send ระหว่าง branch target กับ return.

ดังนั้นคำตอบของทางเลือกในใบคือ **neither**:

- ไม่ถึง producer `0x0044D260` และจึงไม่มีหลักฐานว่าใช้ serializer `0x0074E6A0` จากเส้นนี้
- ไม่ถึง serializer `0x00600A60`
- skill ID ใน frame: **N/A / unresolved by this route**, เพราะ route จบก่อนมี frame; ห้ามเลือก `+0x14`, `+0x18` หรือ `ActionVital+0x30` เพียงเพราะชนิด/เลขดูเหมาะ

นี่เป็นผลลบแบบ bounded ต่อ dispatcher `0x450B20` และ table `0x4519C4` เท่านั้น ไม่ใช่คำกล่าวว่า client ไม่ส่ง skill frame จาก UI callback/เส้นทางอื่น.

## Mandatory WIELD control — PASS

เปิดและตรวจรายงานบังคับครบทั้ง `PF_RE_V128_Wield_Z_ActionVital_Capture_20260814.md:25-33` และ `:47-60` (file sha256 `03763b92b1f041bf85c85ba44f0fc58ea91723833169de0910b2a601bbdc3126`). ผล static รอบนี้ตรงทุกจุด:

1. `CONSTDATA_TH__HOTKEY.tsv`: id `71`, `s_NAME=WIELD`, `n_TYPE=3`, `n_KEY_2=90` (Z).
2. `0x4519C4 + (71-1) = 0x0B` ⇒ class 11.
3. jump slot 11 ที่ `0x45199C` ⇒ `0x00451026`.
4. `[0x00451026,0x00451032)` bytes `8B CE E8 43 AC FF FF E9 C1 08 00 00`, sha256 `97086dd19a647ffe3626179a186dcc8fe9db8b8b72bf52890c4de8d8639d3388`: call producer `0x0044BC70`, then exit.
5. producer full CFG `[0x0044BC70,0x0044BE4E)`, 478 bytes / 145 instructions / no gaps, sha256 `bdb6241cb8bbe5a1e46b690a1cf2130503a319c007699a5912e52347bf163e2f`.
6. `0x0044BD0C`: `mov dword [edi+0x30],0xEA7E`; `0x0044BD72..0x0044BD7E`: queue object through `0x005DD800`.
7. attended control ในรายงานเดิมเห็น `ActionVital 0x1AEA`, fixed 64-byte body และ action `+0x30=0xEA7E` ตรงกัน.

Control ตรง จึงใช้ผลลบของ skill/hotbar branch ได้.

## Serializer facts held separate from producer result

`external/PF_SERIALIZER_FIELDS.tsv` sha256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123` ยืนยัน schema ที่ใบสั่งให้ถือไว้:

- `TriggerCastSkillVital` W: `0x0F@+0x14/2`, `0x08@+0x16/1`, `0x14@+0x18/4`, ทั้งหมด `ALWAYS`, serializer `0x00600A60`.
- `ActionVital` W: `0x14@+0x30/4` เป็นฟิลด์ที่ control WIELD ใส่ action `0xEA7E`, serializer `0x0074E6A0`.

ข้อมูลนี้บอก layout แต่ **ไม่บอกว่าฟิลด์ใดคือ skill ID**; ไม่มี producer-to-input copy ใน route ที่ตรวจ. `PF_FIELD_VALIDATION.tsv` sha256 `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` ที่เขียน `TriggerCastSkillVital=NOT_OBSERVED` เป็นเพียง corpus boundary เช่นกัน ไม่ใช่ negative proof.

## Search-first

- **ค้น `pf_bridge/external/` แล้ว:** ครบ tree 2,683 files / 930,201,065 bytes; batch inventory fingerprint `1aab496f62f4b83127c5a4cea3e1d9b2d3a4da228d210632f6ae85d492bb5ad1`; terms `430E10|category_5C|4519C4|450B20|HOTKEY|TriggerCastSkillVital|ActionVital|5CD2|WIELD|EA7E|BEHAVIOR|SKILL_CONTEXT`. พบ serializer/schema/corpus facts ข้างบนและรายงาน WIELD; **ไม่พบ** producer crosswalk ของ skillbar หรือ named skill-id field.
- **ค้น `pf_bridge/gamedata/` แล้ว:** ครบ tree 1,109 files / 15,319,585 bytes; batch inventory fingerprint `664ae05d31c66e6e00011e95c9702405a449b23117694f9c2380a372fe1d0b`; terms ชุดเดียวกัน. พบ HOTKEY rows และยืนยันว่า `BEHAVIOR.n_ID=99` กับ `SKILL_CONTEXT.n_ID=99` มีอยู่ทั้งคู่ แต่ไม่มี crosswalk field เชื่อมกัน. File SHA: `BEHAVIOR` `79ee11e480db92db0da8e9d08a0911badeef8d2942cc1c072cdb0e9a6562bf4e`; `SKILL_CONTEXT` `41d642c535bfefd9a560cb8fc92a530a51bd3ca55168eddae93cfd64dca7c4f4`.

## Verification / nonclaims

`pf_bridge/staged/re240_static_verify.py` sha256 `45a92ec1844d04b622d82722632c9eed69627c849d1e16f7677fd4752ab4fbb3` ผ่าน **31/31**: pin queue/ticket/image/table/dispatcher/jump targets/control producer/report ranges/serializer rows.

- ไม่เชื่อม `BEHAVIOR.n_ID=99` กับ `SKILL_CONTEXT.n_ID=99`; ตัวเลขเท่ากันไม่มี crosswalk.
- ไม่ใช้ `RE-056 METHOD-FAIL`, `GT-050 TRIGGER-DIRECTION-UNRESOLVED` หรือ `NOT_OBSERVED` เป็นหลักฐานว่าไม่มี wire.
- ไม่อ้างว่า `ActionVital+0x30` คือ skill ID; control พิสูจน์เฉพาะ action `0xEA7E` และ RE-110 แยกมันเป็น action/behavior selector.
- ไม่อ้างว่า `TriggerCastSkillVital` เป็นหรือไม่เป็น frame ของการกด skill; route ที่ใบสั่งให้เดินไม่ได้แตะ serializer นี้.
- ไม่อ้าง client-observable outcome ใหม่; รอบนี้ static เท่านั้นและไม่ได้เปิดเกม.

## BUILD_IMPACT / next evidence

**ไม่มี server build change ที่ปลอดภัยจากผลนี้**: ห้ามใส่ชื่อ skill ID ให้ field ใดของสอง frame. เพื่อปิด semantic ที่เหลือ ให้ทำ attended capture ตามเกณฑ์ใบเดิมในเซสชันเดียวกัน: (A) กด skill `99` จาก hotbar และ (B) control กด Z; เก็บ decompressed RuntimeReq hex แล้วเทียบกับ V128. การเปลี่ยน field ระหว่าง A/B จะให้ candidate แต่ยังต้องผูก slot/UI-selected skill object ไปยังค่าใน frame ด้วยหลักฐานคนละชั้นก่อนตั้งชื่อ definitive.

สถานะที่ควรกรอก: `RE-240 DONE/BOUNDED-NEGATIVE — HOTBAR/SKILLBAR class 20 exits at 0x4518F3; no producer or skill-id field on this route; attended capture required`.
