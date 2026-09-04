ถึง: LANE-GM · สำเนา: chief

# RE-238 RESULT — PASS/DONE · `0x430E10` คือ `SCENE_NAME.n_ID -> n_SCENE_TYPE`; ค่าที่คืน 8 ครบคือ 126, 127, 128, 304, 305

- เวลาเริ่มใบ: `2026-09-04T17:02:15.621+07:00`
- เวลาปิดใบ: `2026-09-04T17:09:11.598+07:00`
- ticket input: `CLIENT_RE_QUEUE.md` sha256 `792a6ea37b2c7817a3ed2dbe327882416d10a4d06b8ccaad6fbca872763d704b`; normalized RE-238 block sha256 `06eee0a18755fd396e12c01762a7e2864a3ddd135a3a5a11cde91c8a4ff972ff`
- image: `GameClient/GameClient.local.bin`, 14,759,424 bytes, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- verdict: **lookup โดยตรงผ่าน named gamedata table ไม่ใช่สูตรคำนวณ ไม่ใช่ switch/jump table ใน image**

## คำตอบ

เมื่อ argument ไม่เป็นศูนย์ ฟังก์ชันทำตรงตัวดังนี้:

```text
SCENE_NAME row = lookup(table=L"SCENE_NAME", key=argument)
return row ? get_u32(row, L"n_SCENE_TYPE", default=0) : 0
```

named-field crosswalk มาจาก image เอง ไม่ได้จับคู่เพราะเลขเท่ากัน: `0x00430E3A` push literal `SCENE_NAME` (`0x00F0C4A8`), `0x00430E44` call row lookup `0x008910A0`; จากนั้น `0x00430E4F` push literal `n_SCENE_TYPE` (`0x00F0C48C`) และ `0x00430E56` call numeric-field reader `0x00891FD0` ด้วย default `0`.

ตาราง `CONSTDATA_TH__SCENE_NAME.tsv` มี 271 rows, key `n_ID` ไม่ซ้ำ; `PF_GAMEDATA_COLUMNS.tsv` ระบุ `n_ID` เป็น column 0/key และ `n_SCENE_TYPE` เป็น numeric column 6 (`offset 24`). ตรวจครบทุก row แล้ว ชุด key ที่ `n_SCENE_TYPE == 8` มี **ห้าค่าเท่านั้น**:

| input / `SCENE_NAME.n_ID` | `s_MODLE_ID` | `n_SCENE_TYPE` |
|---:|---|---:|
| 126 | `Bg3001` | 8 |
| 127 | `Bg3002` | 8 |
| 128 | `Bg3003` | 8 |
| 304 | `Bg3007` | 8 |
| 305 | `Bg3008` | 8 |

ดังนั้นสำหรับค่า `category_5C` ที่ไม่ใช่ศูนย์ ชุดที่คืน 8 ครบคือ **`{126,127,128,304,305}`**. ค่าอื่น—including key ที่ไม่มี row—คืนค่าคอลัมน์อื่นหรือ default `0`, ไม่คืน 8.

### กรณีพิเศษ input = 0

`0` ไม่ใช่สมาชิกคงที่ของชุดข้างบน: `0x00430E14..0x00430E34` เปลี่ยน argument ศูนย์เป็น `u16 [current-scene-object+0x30]` ผ่าน global `[0x01093198] -> +0x2C0 -> +0x0C`; ถ้า chain หรือ scene id เป็นศูนย์จะคืน 0 ทันที. เพราะฉะนั้น `f(0)` **อาจ**คืน 8 เฉพาะเมื่อ current scene id ขณะนั้นเป็นหนึ่งในห้าค่าข้างบน; มันไม่ใช่ deterministic mapping `0 -> 8`.

## Full function bytes / decode

- span `[0x00430E10,0x00430E5C)`, file offset `0x00030210`, 76 bytes, 26 instructions, no gaps/errors
- span sha256 `d166b13fafedc87766de7dcd38fd1b4440706e424b9fe852c60f9cb07ec1229c`
- full bytes:

```text
8B442404 85C0 7521 A198310901 8B80C0020000 85C0 740F 8B400C 85C0 7408
0FB74030 85C0 7503 33C0 C3 50 68A8C4F000 B9D0CD0801 E857024600 85C0
74E9 6A00 688CC4F000 8BC8 E875114600 C3
```

```text
00430E10  8B442404          mov    eax, dword ptr [esp + 4]
00430E14  85C0              test   eax, eax
00430E16  7521              jne    0x430e39
00430E18  A198310901        mov    eax, dword ptr [0x1093198]
00430E1D  8B80C0020000      mov    eax, dword ptr [eax + 0x2c0]
00430E23  85C0              test   eax, eax
00430E25  740F              je     0x430e36
00430E27  8B400C            mov    eax, dword ptr [eax + 0xc]
00430E2A  85C0              test   eax, eax
00430E2C  7408              je     0x430e36
00430E2E  0FB74030          movzx  eax, word ptr [eax + 0x30]
00430E32  85C0              test   eax, eax
00430E34  7503              jne    0x430e39
00430E36  33C0              xor    eax, eax
00430E38  C3                ret
00430E39  50                push   eax
00430E3A  68A8C4F000        push   0xf0c4a8              ; L"SCENE_NAME"
00430E3F  B9D0CD0801        mov    ecx, 0x108cdd0
00430E44  E857024600        call   0x8910a0              ; table + key row lookup
00430E49  85C0              test   eax, eax
00430E4B  74E9              je     0x430e36
00430E4D  6A00              push   0                     ; default
00430E4F  688CC4F000        push   0xf0c48c              ; L"n_SCENE_TYPE"
00430E54  8BC8              mov    ecx, eax
00430E56  E875114600        call   0x891fd0              ; numeric field read
00430E5B  C3                ret
```

Helper pins: row lookup `[0x008910A0,0x008910C2)` sha256 `1902188316f14bb028996fbfa0d8bb39bf8d6fc31e389473a76a3e3292f97fed`; numeric field reader `[0x00891FD0,0x00891FFF)` sha256 `1738f3b8401dda12b6e9a69a0e0a68774beef4465b14fb4249b1e2f0afc3a91d`. ตัวหลังตรวจ field type `0`, อ่าน dword จาก row+column offset และคืน caller default เมื่อ field หาย/ชนิดไม่ตรง.

## Static table / data span

ไม่มี image-resident value/jump table ที่ฟังก์ชันนี้ index เข้าโดยตรง จึงไม่มี table VA สำหรับค่าห้าตัว. สิ่งที่ image เก็บคือชื่อ lookup:

- `L"n_SCENE_TYPE"` ที่ `[0x00F0C48C,0x00F0C4A6)`
- `L"SCENE_NAME"` ที่ `[0x00F0C4A8,0x00F0C4BE)`

ข้อมูลจริงมาจาก gamedata table `gamedata/tables/CONSTDATA_TH__SCENE_NAME.tsv`, 39,871 bytes, sha256 `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b`. `PF_GAMEDATA_INDEX.tsv` ระบุ table 007, 271 rows x 24 columns, source offsets `0x0000B3D4..0x0001D148`; ไฟล์ index sha256 `a9ab5efd3826a54e0cad3cb86f0c872ebd1d61219721ee8514d42e9d2110b5bc`. Columns sha256 `6f1a00dc9660038f651007397244c575b321beaf756675fd0e437c3131294d89`.

## Search-first / evidence reuse

- **ค้น `pf_bridge/external/` แล้ว:** ครบ tree 2,683 files / 930,201,065 bytes; batch inventory fingerprint `1aab496f62f4b83127c5a4cea3e1d9b2d3a4da228d210632f6ae85d492bb5ad1`; terms `430E10|category_5C|4519C4|450B20|HOTKEY|TriggerCastSkillVital|ActionVital|5CD2|WIELD|EA7E|BEHAVIOR|SKILL_CONTEXT`. พบ `PF_ATTR_FIELD_SEMANTICS.tsv` (sha256 `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`) บันทึก `BasicAttr+0x5C -> scene_id__SCENE_NAME.n_ID`; **ไม่พบ** decode ของ `0x430E10` หรือรายการ type-8 keys พร้อมใช้.
- **ค้น `pf_bridge/gamedata/` แล้ว:** ครบ tree 1,109 files / 15,319,585 bytes; batch inventory fingerprint `664ae05d31c66eeb6e00011e95c9702405a449b23117694f9c2380a372fe1d0b`; terms ชุดเดียวกัน. พบคำตอบ data-side ใน `CONSTDATA_TH__SCENE_NAME.tsv` และ schema ใน `PF_GAMEDATA_COLUMNS.tsv`; enumerate ครบทุก 271 rows ไม่ได้สุ่มตัวอย่าง.
- คำตอบเดิมที่ reuse/reverify: `staged/re077_static_verify.py` เคย pin span `0x430E10..0x430E5C`; SHA ของ script เดิม `6f93302dfcd0201e425b40234db3883fc1a92be36c719f1e4d8232f577ca588f`. รอบนี้ตรวจ image/span/คำสั่ง/helper/table ใหม่และเพิ่มการ enumerate ทั้งโดเมนตาราง ไม่ยกผลเก่ามาเชื่อเฉย ๆ.

## Verification / source integrity

`pf_bridge/staged/re238_static_verify.py` sha256 `c2bd28d7ba9ae595647c56be9052caa114271b38a71a527dfebd48b215ba2dc0` รันผ่าน **32/32**; ตรวจ queue/ticket/image/function bytes/สอง helper/named literals/schema/ทุก table row/ชุด type-8 exact.

Source inputs ก่อนงาน:

- `PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS_20260819.md` sha256 `53e1257c3621e1d03bd0fcca2955d36871f9fc40c4316ddfedb4791dc763ab56`
- `PF_HP_DEATH001_HP_DEATH_AND_RESPAWN_STATIC_20260819.md` sha256 `3df84dd1665168c306baf8f8223dcde176cb3d947e1037ea6c3dfdf6b5af0233`
- `gm/attr_wire.py` sha256 `178306e643597e535bd133580c07e32055125e6c9d0dd8eecad1401e161bf77f`

จะตรวจ SHA เหล่านี้ซ้ำใน closeout; ไม่มี source input ถูกแก้.

## Nonclaims

- ไม่อ้างว่า `n_SCENE_TYPE=8` ชื่อเชิงเกมว่าอะไร (ship/vehicle/instance ฯลฯ); image/table พิสูจน์เฉพาะ named lookup และเลข 8.
- ไม่อ้างผล client-observable หรือผล runtime; ไม่เปิดเกมและไม่มี capture ใหม่.
- ไม่อ้างว่า server guard ปัจจุบันถูกแก้แล้ว; รอบนี้ไม่แตะ server source.
- ไม่ใช้ความเท่ากันของ ID ข้ามตารางเป็น crosswalk; เส้นนี้มีชื่อ table/key/field จาก instruction operands และ schema โดยตรง.
- ไม่ถือ input `0` เป็น scene row 0; มันเป็น sentinel ที่ทำ dynamic current-scene substitution.

## BUILD_IMPACT

LANE-GM สามารถแทน guard แบบ `x9 == 8` หรือ “ห้ามเปลี่ยนจาก login ทุกกรณี” ด้วย lookup ที่เทียบ `category_5C` กับ exact set `{126,127,128,304,305}` เพื่อเลือกว่าต้องมี `x52/x53` หรือไม่. ต้องรักษา sentinel rule ของ `0` แยกจาก set และต้องไม่ตั้งชื่อ `n_SCENE_TYPE=8` เกินหลักฐาน. งาน implement/test เป็นของ LANE-GM/chief; RE-238 ไม่ได้แก้ build.

สถานะที่ควรกรอก: `RE-238 PASS/DONE — SCENE_NAME.n_SCENE_TYPE=8 keys 126/127/128/304/305 pinned`.
