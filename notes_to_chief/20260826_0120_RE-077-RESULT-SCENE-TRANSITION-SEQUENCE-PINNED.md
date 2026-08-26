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

**ขา hit / rider จากจดหมาย LANE-A 01:16:** `0x00890E70` ไม่ index vector ตามลำดับแถว แต่ค้น keyed tree ที่ `[SCENE_NAME table+0x70]`; schema ที่พินใน `PF_GAMEDATA_COLUMNS.tsv` ระบุ stored field ลำดับ `0` เป็น `n_ID` (type 0, width 4, row offset 0). ดังนั้น argument `scene_id` คือ key `n_ID` ที่ใช้เลือก row ก่อนอ่าน `s_MODLE_ID` — ไม่ใช่ `n_MARKER`, `n_CLINE_TYPE` หรือ ordinal ของแถว. สำหรับ candidate `scene_id=278`: data-row ordinal คือ `252`, แต่ row key `n_ID=278` ให้ `s_MODLE_ID=Bg1177`, `n_SCENE_TYPE=4`, `n_CLINE_TYPE=0xFFFFFFFF`, `n_MARKER=0`; client จึงส่ง `Bg1177` เข้า loader และถ้า loader สำเร็จจะเลือก `StateRunTime`. Static ยังไม่พิสูจน์ว่า resource load/render ของ `Bg1177` สำเร็จจริง.

## T3 — state sequence

- `TeleportVital apply 0x005F14B0` ปฏิเสธ target scene `0`; อ่าน live state `[0x1093198]+0x34C` และยอมเฉพาะ RTTI token `StateRunTime` (`0x004C8740`) หรือ `StateNavigation` (`0x004C7690`).
- เมื่อ gate ผ่าน จะสร้าง object `0x24` bytes ผ่าน ctor `0x004C6560` ซึ่งติด vtable `cStateSwitchScene`, copy target เข้า `[switch+0x14]`, แล้วเรียก `CState::RequestNext 0x004C7320` ที่ `0x5F16C9`.
- หลังโหลดสำเร็จ `cStateSwitchScene` อ่าน `n_SCENE_TYPE` ผ่าน `0x00430E10`: ค่า `8` สร้าง `StateNavigation` (`0x004C7600`), ค่าอื่นสร้าง `StateRunTime` (`0x004C8790`), แล้ว `RequestNext` ที่ `0x4C70C7`.
- RTTI names ถูกยืนยันจาก type_info objects: `.?AVcStateSwitchScene@@`, `.?AVStateNavigation@@`, `.?AVStateRunTime@@`; ไม่ได้ตั้งชื่อ state จากพฤติกรรมเอง.

## T4 — dedicated packet และ existing lane

scene change **ไม่ใช่ StartGame-only**: `TeleportVital apply` มี transition path ของตัวเองและเรียก `RequestNext` โดยตรง. Source ปัจจุบัน `make_teleport_target(scene_id, ...)` emit target tag `0x12` จาก argument และ `make_login_teleport(scene_id, ...)` ส่งต่อ argument นั้น; helper V137 ก็เรียกด้วยตัวแปร `V137_MARKER_SCENE_ID`. Call site login ปัจจุบันยัง hardcode `make_login_teleport(1,0)` — จึงสรุปได้ว่า lane/serializer รองรับ scene id อื่น แต่ **ยังไม่พิสูจน์ว่า server ปัจจุบันส่ง target scene ที่ต้องการใน session จริง**.

## T5 — remote actors / population rider

complete recursive CFG ของ switch-scene cleanup slot `0x004C7160` และ helper `0x004C6920` แสดงการ clear world/app collections และเรียก cleanup หลายตัวจริง แต่ยังมี indirect calls และไม่มี identity-membership crosswalk ที่พิสูจน์ว่า “remote actor ทุกตัวถูกทำลาย” หรือ “ต้องส่ง population census ใหม่ทุกครั้ง”. ปิด T5 เป็น **BOUNDED NEGATIVE**: หลักฐาน static ชุดนี้ไม่พอให้ claim ทั้งสองด้าน; ห้ามย่อเป็นว่า remote actors ถูก preserve หรือถูก drop แน่นอน.

### T5 ADDENDUM (chief R181, 2026-08-26) — ตอบ rider sub-question ②/③ เท่านั้น, ไม่แตะ verdict เดิมของ T5

คำตอบ T5 เดิม (BOUNDED NEGATIVE, scene-cleanup slot `0x004C7160`/`0x004C6920`) ยังเป็นอย่างนั้น ไม่เปลี่ยน.
Addendum นี้ตอบเฉพาะ rider ②/③ ที่แทรกใน `CLIENT_RE_QUEUE.md` บรรทัด 2483-2528 ("rider ที่สอง" ต่อท้าย
`RE-075` ในไฟล์ตามลำดับการแทรก แต่เนื้อหาเป็นของ `RE-077 T5` ตามที่รอบ `k69t3b` เขียนกำกับไว้เอง —
ไม่ใช่ `GAME_TEST_QUEUE.md`/`RIDER-081-A` ซึ่งเป็นริเดอร์คนละใบที่ฝั่ง attended ตอบขนานกันอยู่),
โดยใช้ผล RE-082 (PICKUP-OBJECT-REF-SOURCE-001, `notes_to_chief/20260826_1017_RE-082-RESULT-OBJECT-REF-IS-ELEMENT-KEY.md`):

ใน **consumer ที่ RE-082 วัด** (`CONSUMER [0x006AF970,0x006B03E3)`, รับ element list ผ่าน
`LIST_CODEC 0x005F85B0` / `ELEMENT_KEY_FIND 0x005F8400` — consumer นี้เชื่อมกับ list ของ
drop-object บนพื้นที่ `PickupTerrainThing` อ่าน element key มา, ไม่ใช่ consumer ที่รับ
`make_runtime_remote_actors` โดยตรง):
- generation ที่ **nonempty** ⇒ **replace-by-omission**: key เดิมที่ไม่อยู่ใน generation ใหม่ถูก erase
  (`0x006AFF84` -> `0x005E0D40`), key ที่ match ถูก update (`0x006AFDE9` -> `0x005F4C00`),
  key ใหม่ถูก insert (`0x006B014F`..`0x006B0211`)
- generation ที่ **count=0** ([PROPOSED interpretation ของ RE-082 T4 — "nonempty pointer" เป็นการตีความ
  ของ chief ไม่ใช่คำที่ RE-082 T4 เขียนตรงตัว] zero entries) ⇒ **no-op**: branch
  `0x006AF9B4`/`0x006AF9BF` ไปตรง epilogue `0x006B03BC`, ไม่ clear live tree
- incoming pointer เป็น **null** ⇒ เส้นทางที่สาม แยกจากทั้งสองข้างบน: clear/erase ทั้ง tree
  (`0x006B024F`..`0x006B0368` -> `0x005E0D40`)

🔴 **เพดานของ addendum นี้ (บังคับอ่านคู่กับผลข้างบน):**
1. ผลนี้ **ยังไม่พิสูจน์ว่าเป็น consumer เดียวกัน** กับที่รับ `make_runtime_remote_actors` /
   `GSCN_RunTimeProtocolRes` derived-mask `0x08` (ตัวที่ `mob_combat.py`/`mob_death.py`/
   `world_population_handoff.py` ใช้อยู่จริง) — ไม่มี artifact ที่ commit แล้ว
   (`PF_PROTOCOL_REGISTRY.tsv`/`PF_FIELD_VALIDATION.tsv`/จดหมาย RE-082 เอง) ผูก consumer span
   นี้กับ `GSCN_RunTimeProtocolRes` โดยชื่อ/message id
2. **`RE-092` (OPEN ณ วันที่เขียน addendum นี้)** เปิดขึ้นเพื่อตอบ crosswalk ข้อ 1 โดยตรง
   (T0 ของ `RE-092`: เทียบ element key tag ของ `PickupTerrainThing` consumer กับของ
   derived-mask `0x08` consumer) — **ห้ามอ่าน addendum นี้ว่าได้คำตอบของ mob_combat/mob_death/
   world_population_handoff แล้ว จนกว่า `RE-092` T0 จะปิด**
3. 🔴 **แก้คำ 2026-08-26 ~21:1x — เวอร์ชันแรกของข้อนี้เขียนกลับทิศ ตัวโมดูลอ้างตรงกันข้าม:**
   `world_population_handoff.py` (sha `51faa81`) เขียนสมมติฐานของตัวเอง (docstring, ติดป้าย
   `[INFERENCE, NOT MEASURED]`) ว่า **generation ว่างทำให้ไคลเอนต์ล้างลิสต์ actor ออก** (กลไก
   `KIND_CLEAR`) — **ไม่ใช่ "ไม่ลบใคร"** ตามที่แก้ไขนี้เคยเขียนผิด
   ⇒ **ถ้า** consumer ที่ `RE-082` วัด (`PickupTerrainThing`) เป็นตัวเดียวกับที่โมดูลนี้ใช้จริง (ยังไม่พิสูจน์
   — ข้อ 1/2 ข้างบน) ผล "zero-entry ⇒ no-op" ของ `RE-082` จะ **ขัดกันตรง ๆ** กับสมมติฐานของโมดูลนี้:
   เฟรม 0-entry ที่ตั้งใจส่งไปล้างคนของท่าเรืออาจไม่ทำอะไรเลยบนจอจริง ๆ — **นี่คือคำถามเปิดที่สำคัญที่สุด
   ของ addendum นี้ ไม่ใช่จุดที่ปิดแล้ว และห้ามอ่านว่า "เข้ากันได้" อีกต่อไป**
4. layer = static image (CFG) ล้วน — ไม่พิสูจน์ client-observable despawn/render และไม่แตะ
   nonclaim เดิมของ T5 ข้อ 6 (ท้ายใบนี้ หัวข้อ "nonclaims (ตามใบ)" รายการที่ 6 — เลขบรรทัดขยับทุกครั้งที่
   ใบนี้ถูกต่อท้าย ห้ามผูกเลขบรรทัดตายตัว)

## span pins / reproducibility

| function | span | instr | gap/errors | SHA-256 |
|---|---|---:|---:|---|
| `TeleportVital apply 0x5F14B0` | `[0x5F14B0,0x5F16F9)` | 163 | `0/0` | `85723791e07493270b605313632013614d98a52c5c1ca9a4b0c809235ebd3694` |
| `cStateSwitchScene ctor 0x4C6560` | `[0x4C6560,0x4C65C5)` | 29 | `0/0` | `ace67ca58967a21728fdd7dd19fbe9f221b4d583f187f7609cf14ff34bbdcf5f` |
| model lookup `0x4C6660` | `[0x4C6660,0x4C6769)` | 75 | `0/0` | `482f99ae7c34a21953753859c6eb065bf64a03b6f50019382d8849b7c9568ce0` |
| typed row/field `0x8923B0` | `[0x8923B0,0x892417)` | 35 | `0/0` | `f41d0425fe5b23a079c5bbc5c55dd486abd238c0cf40ef9474195745db8f4130` |
| keyed row lookup `0x890E70` | `[0x890E70,0x890EE5)` | 51 | `0/0` | `cb6809072db9b73a7ac43226b54cb413409d67e8ad35079e476073a672548f78` |
| scene loader `0xB02870` | `[0xB02870,0xB02AAC)` | 194 | `0/0` | `2aecc11cc2dd955eb9a99fe570d14f672a2eac1b5e006d5ffa059acb881a22cb` |
| switch tick `0x4C6E80` | `[0x4C6E80,0x4C7154)` | 199 | `0/0` | `57266c910929c0745f3c9a3cf4836938299b9e04439f3b100ddd06911e0c978c` |
| BasicAttr serializer `0x4656F0` | `[0x4656F0,0x465986)` | 252 | `0/0` | `4a8e1b0c95ec929c08bfe944f7f6bfc82d6c64b8b5154f1cbbfb387b5df5ef25` |
| cleanup slot `0x4C7160` | `[0x4C7160,0x4C7309)` | 98 | `0/0` | `e2d4729e5d287d4be4e38834bd4b0cdd53fb79d1cc28f4d293f8fc4bd56bfe18` |

- image: `GameClient.local.bin`, `14,759,424` B, SHA ก่อน/หลัง `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- source ที่อ่าน: `Pirate Force ServerProject\current\pf_login_game_server_v141.py`, SHA ก่อน/หลัง `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- verifier ใหม่: `staged\re077_static_verify.py`, SHA `6f93302dfcd0201e425b40234db3883fc1a92be36c719f1e4d8232f577ca588f`, exit `0`, `90 guards / failed 0`
- verifier พิน shared probe, image, source, SCENE_NAME table/columns, 13 complete recursive CFGs และ byte-exact crosswalks; draft แรกมี 6 guard slices ยาว/offset ไม่ตรง listing จึงแก้ expected slices ให้ตรง bytes จริงแล้ว rerun; หลังอ่าน rider เพิ่ม keyed-row guards แล้ว final rerun `90/90` — ไม่ได้ tweak input หรือ semantic value ให้ผ่าน

## integrity / concurrent sync

- external tree ก่อน/หลัง: `30 files / 29,900,221 bytes`, fingerprint `50c7f6162cdd03845bb9dfdb10620f2692d2c23b571167993a8cd3e60672538f`
- gamedata tree ก่อน/หลัง: `1,109 files / 15,319,585 bytes`, fingerprint `9ba992357c2e6a7edbd366b996a801d3b354930babf695f35b615251bce3a3ab`
- `AGENTS.md` SHA `5ff41a9d897b288325b822186bc5ec3cc96b0087c31e79c1a2be2aa4d74b8519`; `CLIENT_RE_QUEUE.md` final SHA `df3216ff2fe592bc6dec60b8f1bb3ae88177ac5de30b087417597947d8d8af0d`; ไม่แก้ทั้งคู่
- ระหว่างรอบ sync เปลี่ยน `NEW_ORDERS.txt` จาก SHA `c53c56235b91ccd1238ceb18682da4bb21a80f894dd38ee1cd2f144fbea79363` เป็น `b146fa44c078d13636f54c39977b27bb6bca4a86866ceb6ede5612d795fbd536` เวลา 01:16 (+07). จึงอ่าน `CLIENT_RE_QUEUE.md` ทั้งไฟล์ซ้ำและอ่านจดหมายล่าสุด `20260826_0130_LANE-A-BUILD-002-...md`; ไม่มี result letter ของ RE-077 ก่อนจดหมายฉบับนี้ และ rider ขา hit ถูกใส่ใน T2 ด้านบน
- interpreter สร้าง cache byproduct ในเขต `staged\__pycache__` สองไฟล์ระหว่าง probe (`re075_static_probe.cpython-314.pyc`, `re075_static_verify.cpython-314.pyc`); ไม่ใช่ input/evidence และไม่ได้แก้ `.py` ต้นทาง. Final verifier ใช้ `python -B` เพื่อไม่สร้างเพิ่ม

## nonclaims (ตามใบ)

1. ผลนี้เป็น client image + static source/table เท่านั้น ไม่แทน client-observable evidence.
2. ไม่พิสูจน์ว่า server ปัจจุบันส่ง TeleportVital scene id อื่นใน session จริง.
3. ไม่ตัดสินให้ยกสาม guards เดิมใน server; policy/implementation decision เป็นของ chief/Panya.
4. ไม่ตอบ geometry / collision / spawn coordinates และไม่อ้างว่าแก้ `RE-073`.
5. static นี้ไม่ upgrade `SCENE-001` direct-load result; dedicated TeleportVital path เป็นคนละ experiment/path.
6. T5 ไม่ claim ว่า remote actors drop หรือ population resend จำเป็น เพราะ unresolved indirects + ไม่มี identity crosswalk.
7. สำหรับ scene 278 พิสูจน์แค่ keyed row hit → model id `Bg1177` → loader call; ไม่ upgrade เป็น “โหลด/render ผ่าน” จนกว่าจะมี client-observable evidence.

## BUILD_IMPACT:

ใช้ transition packet `TeleportVital` เดิมได้ในเชิง wire/build เพราะ builder รับ `scene_id` เป็น argument อยู่แล้ว; ถ้าจะทำ attended experiment ใหม่ จุดเปลี่ยนที่เล็กสุดคือเลือก **existing `n_ID` ที่มี `s_MODLE_ID`** แล้วเปลี่ยน normal-path call-site argument จาก `1` เป็น target id ภายใต้ guard/policy ที่ chief อนุมัติ. ตามผล LANE-A ล่าสุด “สาม guards” อยู่บน diagnostic/scenario lanes ไม่ใช่ normal path; blocker ของ normal path คือ hardcoded `make_login_teleport(1,0)` ตัวเดียว — ผล RE-077 นี้ไม่ใช่คำสั่งให้แก้หรือปลด guard ใด. **ห้าม**เพิ่ม fallback สำหรับ id miss จากผลนี้: shipped client จงใจ fail loader/status 2 เมื่อ model lookup ว่าง. การ resend remote population หลัง switch ยังเป็นคำถามเปิด ต้องวัด client-observable/wire แยก.

## static-only audit

ไม่เปิดเกม · ไม่บูต server · ไม่จับ/แตะ `LOCK_GAME` · ไม่แตะ canonical DB · ไม่แก้ GameClient/external/gamedata/source/tools/tests/docs/queue · ไม่ทำ git operation · ไม่เปิดใบใหม่
