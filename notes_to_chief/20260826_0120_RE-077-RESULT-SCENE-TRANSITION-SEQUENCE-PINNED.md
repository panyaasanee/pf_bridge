[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-077 RESULT — DONE / PASS: SCENE TRANSITION SEQUENCE PINNED

เวลา: `2026-08-26T01:20:44+07:00`  
ใบ: `RE-077 SCENE-TRANSITION-SEQUENCE-001`  
หมวด: `STATIC-ON-BRIDGE` · ไม่บูต server/client · ไม่มีชั้น client-observable  
งานที่ปิด: `T0-T4`; `T5` ปิดเป็น bounded negative ตามเพดานหลักฐาน static

## คำตอบ objective

ลำดับที่ shipped client ต้องการคือ:

`StateRunTime | StateNavigation` → รับ `TeleportVital` ที่ target `scene_id != 0` → สร้าง `cStateSwitchScene` และ `RequestNext` → lookup `SCENE_NAME[n_ID=scene_id].s_MODLE_ID` แล้วโหลด scene → ถ้า `n_SCENE_TYPE == 8` ไป `StateNavigation`, มิฉะนั้นไป `StateRunTime`.

ถ้า `scene_id` ไม่มี row ใน `SCENE_NAME`, typed lookup คืน flag false + empty string, loader ปฏิเสธ empty model ID, และ `cStateSwitchScene` ตั้ง status `+0x0C = 2` แล้วคืน — **ไม่พบ fallback ไป scene default/code-name และไม่เกิด RequestNext ตัวถัดไปใน miss branch นี้**.

## สองช่องบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** — `PF_PROTOCOL_REGISTRY.tsv` มี `BasicAttr`, `ActorAttr`, `StartGameReq/Res`, `TeleportVital`, `TeleportCheckVital`; `PF_SERIALIZER_FIELDS.tsv` พิน `TeleportVital` serializer `0x005EB470` และ nested target serializer `0x005DF250` ซึ่งมี target `+0x12` tag `0x12` length `2`; `PF_FIELD_VALIDATION.tsv` ระบุ TeleportVital W/R observed แต่ BasicAttr/ActorAttr ยัง `NOT_OBSERVED`. ตรวจ byte/CFG กับ image จริงแล้ว ไม่ใช้ registry stub `0x0043BB80` เป็น serializer จริงของ BasicAttr.
- **ค้น gamedata แล้ว: เจอ** — `pf_bridge\gamedata\tables\CONSTDATA_TH__SCENE_NAME.tsv` มี `271` data rows, key `n_ID`, ฟิลด์ `s_MODLE_ID` และ `n_SCENE_TYPE`; SHA-256 `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b`. ตารางบอกเฉพาะ row ที่ shipped มา ไม่ได้พิสูจน์ runtime execution.

## T0 — field crosswalk ปิด

- `BasicAttr` virtual serializer จริง `0x004656F0` ภายใต้ mask `0x0100` เขียนและอ่าน `object+0x5C` ด้วย tag `0x12`, length `2` (`0x4657C2..0x4657E3`, `0x4658FC..0x46591D`).
- `BasicAttr::CopyTo 0x00464B40` copy word `+0x5C` → `+0x5C` ที่ `0x464BB3..0x464BBA`.
- live actor consumer อ่าน word `[ActorAttr/BasicAttr+0x5C]` ที่ `0x424FBA`.
- bridge function ที่ `0x4B4C67` copy `[actor+0x5C]` → Teleport target `[target+0x12]`; และ `[actor+0x60/+0x64]` → target `[+0x18/+0x1C]`.
- source ปัจจุบัน `make_npc_attr(... scene_id ...)` และ `make_actor_attr_minimal` emit `u16tag(0x12, scene_id)` ใน BasicAttr mask `0x0100`; จึงเป็น field เดียวกับที่ client เก็บที่ `+0x5C` และใช้สร้าง target `+0x12`. นี่คือ crosswalk จริง ไม่ใช่ join เพราะเลข id คล้ายกัน.

## T1 — consumer taxonomy

`BasicAttr/ActorAttr scene_id` เป็น resident/store field ก่อน: serializer + CopyTo เก็บที่ `+0x5C`, active-scene logic อ่านมัน, และ transport builder copy ไป dedicated target `+0x12`. ตัว scene-table loader **ไม่ได้**อ่าน ActorAttr serializer โดยตรง; `cStateSwitchScene` อ่าน `scene_id` จาก target object ที่ `[switch+0x14]+0x12` แล้วค่อย lookup/load. ดังนั้น ActorAttr scene field กับ transition target เชื่อมกันผ่าน copy site `0x4B4C67`, ไม่ใช่ implicit numeric equality.

## T2 — SCENE_NAME lookup และ miss behavior

1. `cStateSwitchScene` tick `0x004C6E80` เรียก helper `0x004C6660`.
2. helper เปิด table literal `L"SCENE_NAME"`, อ่าน target `+0x12`, แล้วเรียก `0x008923B0(table, scene_id, L"s_MODLE_ID")`.
3. `0x008923B0` เรียก row helper `0x00890E70`; row null หรือ field absent/type ไม่ใช่ string (`type != 3`) คืน flag `0` + global empty string `0x0108CDB0`.
4. scene loader `0x00B02870` ใช้ empty predicate `0x008946F0` (`string length +0x14 == 0`) และคืน false เมื่อ model ID ว่าง.
5. call site `0x4C6EED` เห็น false แล้วเขียน `[cStateSwitchScene+0x0C] = 2`; ไม่มี fallback/default path ใน complete recursive CFG นี้.

T2 จึงตอบทั้งกรณี key miss และ field/type miss โดยไม่อ้างว่า scene id ที่ไม่อยู่ใน TSV “ไม่มีในโลก”; ข้อสรุปจำกัดที่ shipped table/image ชุดนี้.

## T3 — state sequence

- `TeleportVital apply 0x005F14B0` ปฏิเสธ target scene `0`; อ่าน live state `[0x1093198]+0x34C` และยอมเฉพาะ RTTI token `StateRunTime` (`0x004C8740`) หรือ `StateNavigation` (`0x004C7690`).
- เมื่อ gate ผ่าน จะสร้าง object `0x24` bytes ผ่าน ctor `0x004C6560` ซึ่งติด vtable `cStateSwitchScene`, copy target เข้า `[switch+0x14]`, แล้วเรียก `CState::RequestNext 0x004C7320` ที่ `0x5F16C9`.
- หลังโหลดสำเร็จ `cStateSwitchScene` อ่าน `n_SCENE_TYPE` ผ่าน `0x00430E10`: ค่า `8` สร้าง `StateNavigation` (`0x004C7600`), ค่าอื่นสร้าง `StateRunTime` (`0x004C8790`), แล้ว `RequestNext` ที่ `0x4C70C7`.
- RTTI names ถูกยืนยันจาก type_info objects: `.?AVcStateSwitchScene@@`, `.?AVStateNavigation@@`, `.?AVStateRunTime@@`; ไม่ได้ตั้งชื่อ state จากพฤติกรรมเอง.

## T4 — dedicated packet และ existing lane

scene change **ไม่ใช่ StartGame-only**: `TeleportVital apply` มี transition path ของตัวเองและเรียก `RequestNext` โดยตรง. Source ปัจจุบัน `make_teleport_target(scene_id, ...)` emit target tag `0x12` จาก argument และ `make_login_teleport(scene_id, ...)` ส่งต่อ argument นั้น; helper V137 ก็เรียกด้วยตัวแปร `V137_MARKER_SCENE_ID`. Call site login ปัจจุบันยัง hardcode `make_login_teleport(1,0)` — จึงสรุปได้ว่า lane/serializer รองรับ scene id อื่น แต่ **ยังไม่พิสูจน์ว่า server ปัจจุบันส่ง target scene ที่ต้องการใน session จริง**.

## T5 — remote actors / population rider

complete recursive CFG ของ switch-scene cleanup slot `0x004C7160` และ helper `0x004C6920` แสดงการ clear world/app collections และเรียก cleanup หลายตัวจริง แต่ยังมี indirect calls และไม่มี identity-membership crosswalk ที่พิสูจน์ว่า “remote actor ทุกตัวถูกทำลาย” หรือ “ต้องส่ง population census ใหม่ทุกครั้ง”. ปิด T5 เป็น **BOUNDED NEGATIVE**: หลักฐาน static ชุดนี้ไม่พอให้ claim ทั้งสองด้าน; ห้ามย่อเป็นว่า remote actors ถูก preserve หรือถูก drop แน่นอน.

## span pins / reproducibility

| function | span | instr | gap/errors | SHA-256 |
|---|---|---:|---:|---|
| `TeleportVital apply 0x5F14B0` | `[0x5F14B0,0x5F16F9)` | 163 | `0/0` | `85723791e07493270b605313632013614d98a52c5c1ca9a4b0c809235ebd3694` |
| `cStateSwitchScene ctor 0x4C6560` | `[0x4C6560,0x4C65C5)` | 29 | `0/0` | `ace67ca58967a21728fdd7dd19fbe9f221b4d583f187f7609cf14ff34bbdcf5f` |
| model lookup `0x4C6660` | `[0x4C6660,0x4C6769)` | 75 | `0/0` | `482f99ae7c34a21953753859c6eb065bf64a03b6f50019382d8849b7c9568ce0` |
| typed row/field `0x8923B0` | `[0x8923B0,0x892417)` | 35 | `0/0` | `f41d0425fe5b23a079c5bbc5c55dd486abd238c0cf40ef9474195745db8f4130` |
| scene loader `0xB02870` | `[0xB02870,0xB02AAC)` | 194 | `0/0` | `2aecc11cc2dd955eb9a99fe570d14f672a2eac1b5e006d5ffa059acb881a22cb` |
| switch tick `0x4C6E80` | `[0x4C6E80,0x4C7154)` | 199 | `0/0` | `57266c910929c0745f3c9a3cf4836938299b9e04439f3b100ddd06911e0c978c` |
| BasicAttr serializer `0x4656F0` | `[0x4656F0,0x465986)` | 252 | `0/0` | `4a8e1b0c95ec929c08bfe944f7f6bfc82d6c64b8b5154f1cbbfb387b5df5ef25` |
| cleanup slot `0x4C7160` | `[0x4C7160,0x4C7309)` | 98 | `0/0` | `e2d4729e5d287d4be4e38834bd4b0cdd53fb79d1cc28f4d293f8fc4bd56bfe18` |

- image: `GameClient.local.bin`, `14,759,424` B, SHA ก่อน/หลัง `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- source ที่อ่าน: `Pirate Force ServerProject\current\pf_login_game_server_v141.py`, SHA ก่อน/หลัง `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- verifier ใหม่: `staged\re077_static_verify.py`, SHA `922b594d1076db502c4bdb245c6f21097014cac9f63dd761a0d34e43f45932b2`, exit `0`, `82 guards / failed 0`
- verifier พิน shared probe, image, source, SCENE_NAME table, 12 complete recursive CFGs และ byte-exact crosswalks; draft แรกมี 6 guard slices ยาว/offset ไม่ตรง listing จึงแก้ expected slices ให้ตรง bytes จริงแล้ว rerun 82/82 — ไม่ได้ tweak input หรือ semantic value ให้ผ่าน

## nonclaims (ตามใบ)

1. ผลนี้เป็น client image + static source/table เท่านั้น ไม่แทน client-observable evidence.
2. ไม่พิสูจน์ว่า server ปัจจุบันส่ง TeleportVital scene id อื่นใน session จริง.
3. ไม่ตัดสินให้ยกสาม guards เดิมใน server; policy/implementation decision เป็นของ chief/Panya.
4. ไม่ตอบ geometry / collision / spawn coordinates และไม่อ้างว่าแก้ `RE-073`.
5. static นี้ไม่ upgrade `SCENE-001` direct-load result; dedicated TeleportVital path เป็นคนละ experiment/path.
6. T5 ไม่ claim ว่า remote actors drop หรือ population resend จำเป็น เพราะ unresolved indirects + ไม่มี identity crosswalk.

## BUILD_IMPACT:

ใช้ transition packet `TeleportVital` เดิมได้ในเชิง wire/build เพราะ builder รับ `scene_id` เป็น argument อยู่แล้ว; ถ้าจะทำ attended experiment ใหม่ จุดเปลี่ยนที่เล็กสุดคือเลือก **existing `n_ID` ที่มี `s_MODLE_ID`** แล้วเปลี่ยน call-site argument จาก `1` เป็น target id ภายใต้ guard/policy ที่ chief อนุมัติ. **ห้าม**เพิ่ม fallback สำหรับ id miss จากผลนี้: shipped client จงใจ fail loader/status 2 เมื่อ model lookup ว่าง. การ resend remote population หลัง switch ยังเป็นคำถามเปิด ต้องวัด client-observable/wire แยก.

## static-only audit

ไม่เปิดเกม · ไม่บูต server · ไม่จับ/แตะ `LOCK_GAME` · ไม่แตะ canonical DB · ไม่แก้ GameClient/external/gamedata/source/tools/tests/docs/queue · ไม่ทำ git operation · ไม่เปิดใบใหม่
