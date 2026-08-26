[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-090 RESULT — PASS/DONE: TELEPORT / FORCEPOS / WARP FIELD LAYOUTS PINNED

เวลา: `2026-08-26T23:46:33+07:00`  
ใบ: `RE-090 TELEPORT-FORCEPOS-WARP-FIELDS-001`  
หมวด: `STATIC-ON-BRIDGE` · ไม่บูต server/client · ไม่จับ `LOCK_GAME` · ไม่มีชั้น client-observable  
ผล: **T0-T2 ปิดครบ; T3 (optional TeleportCheckVital) ปิดเพิ่ม**

## คำตอบ objective

ชุดส่งมอบ RE มี field rows ของทั้งสี่ message อยู่แล้ว จึงเปลี่ยนใบจาก “ไปถอด” เป็น
**verify SHA → re-derive ปฏิปักษ์ → ใช้** ตามกฎบ้าน ผลหลังเทียบกับอิมเมจจริง:

1. **`ForcePos`** (`serializer 0x005E4250`) มี wire body เป็น vec3 เท่านั้น:
   `tag 0x2A / 4B` สามตัวตามลำดับ X/Y/Z. ตัว wrapper เรียก writer helper `0x005F3490`
   เมื่อ mode เป็น W และ reader helper `0x005F34D0` เมื่อ mode เป็น R.
2. **`CWarpResult`** (`serializer 0x005E51F0`) มีลำดับ:
   `tag 0x32 / 8B @+0x18` → `tag 0x2A / 4B @+0x20,+0x24,+0x28` →
   `tag 0x12 / 2B @+0x2C`. Codec มีทั้ง W/R รูปเดียวกัน.
3. **`TeleportVital`** (`serializer 0x005EB470`) มี top-level presence-gated object สองก้อน แล้วตามด้วย
   scalar สองตัว; layout เต็มอยู่ด้านล่าง. `PF_SERIALIZER_FIELDS.tsv` เคยติดป้าย UNKNOWN หกแถวต่อทิศ
   เพราะเห็น allocator/refcount calls แต่ยังไม่จำแนก. รอบนี้ปิดช่องนั้นแล้ว: calls เหล่านั้นเป็น
   **object-pool allocation + reference counting เท่านั้น ไม่แตะ stream** จึงไม่ใช่ wire fields ที่หาย.
4. **`TeleportCheckVital`** (`serializer 0x005E6670`, optional T3) มีเพียง
   `tag 0x0F / 2B @+0x14` หนึ่งตัว ทั้ง W/R. ความหมายเชิง semantic ของ word นี้ยัง UNKNOWN.

`ForcePos` จึงต่างจาก `TeleportVital` อย่างชัดเจนในระดับ field: ตัวแรกมีแค่ vec3; ตัวหลังมี
scene/sequence/vec3 + optional auxiliary object + controls. รูปนี้ **สอดคล้อง**กับการใช้ ForcePos ภายในฉาก
และ Teleport ข้ามฉาก แต่ชื่อ/shape อย่างเดียวไม่พิสูจน์ semantic นั้น จึงไม่ยกเป็นข้อเท็จจริง.

## สองช่องบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** — `PF_PROTOCOL_REGISTRY.tsv` มี registry rows ครบทั้งสี่;
  `PF_SERIALIZER_FIELDS.tsv` มี 74 rows รวม (ForcePos 8, CWarpResult 10, TeleportVital 54,
  TeleportCheckVital 2); `PF_FIELD_VALIDATION.tsv` ระบุ ForcePos/CWarpResult `NOT_OBSERVED`,
  TeleportVital 132 candidate frames แต่ยัง `A2_STATIC_OPEN`, TeleportCheckVital W=8/R=9 `VALIDATED`.
  ตรวจ span SHA ทั้ง 8 spans กับ image จริงผ่านทั้งหมด. ป้าย validation ไม่ถูกใช้ข้ามชั้นเพื่ออ้าง natural direction.
- **ค้น gamedata แล้ว: เจอของเกี่ยวข้อง แต่ไม่เจอ protocol crosswalk** — exact search ชื่อ message/VA/id
  (`TeleportVital`, `ForcePos`, `CWarpResult`, `TeleportCheckVital`, `0x25A2`, `0x4477`,
  `0x005EB470`, `0x005E4250`) ทั่ว `gamedata\` = **0 hit**. พบ Lua API/data-layer
  `Player.Teleport` 35 scripts, `Player.Warp` 10, `TeleportThenPlayMovie` 8,
  `TeleportWithVehicle` 6, `TeleportCheck` 1, `WarpNearestMarker` 1; ทุก delegate ที่ index ระบุเป็น
  `STUB_NOOP 0x0045FA00`. ของเหล่านี้พิสูจน์ว่าชื่อ API อยู่ในข้อมูลเกม แต่ **ไม่มี field จริงที่ผูก API →
  protocol message** จึงไม่ join จากชื่อหรือเลขที่คล้ายกัน.

## T0 — ForcePos และ TeleportVital

### ForcePos (`ImageBase 0x00400000`)

- registry: getter `0x005E51C0`, serializer `0x005E4250`, handler `0x00710440`,
  id global `0x01081FE4`.
- wrapper `[0x005E4250,0x005E427C)` SHA
  `7c6f6cb751692845d2eb5973fc9499a10dce4eda7caff5f80f82f968bc860e0d`.
- W vec3 helper `[0x005F3490,0x005F34C7)` และ R helper `[0x005F34D0,0x005F3507)`
  มีไบต์เท่ากันยกเว้น primitive target, SHA เดียวกัน
  `b5f5a2063ff9fc8f22830e3238a8b30387d781505ace23d889c3a1500ea47454`.
- wire order W/R เหมือนกัน: `0x2A f32`, `0x2A f32`, `0x2A f32`.
- natural network direction ยัง **ไม่พบหลักฐาน**ใน corpus ที่ตรวจ (`NOT_OBSERVED` ทั้ง W/R) —
  serializer ที่มีสองแขนงพิสูจน์ codec ได้ แต่ไม่พิสูจน์ว่า original server/client ใช้ทิศไหนจริง.

### TeleportVital (`ImageBase 0x00400000`)

registry: getter `0x005E5470`, serializer `0x005EB470`, handler `0x005F14B0`,
id global `0x01081FF0`. Top-level serializer `[0x005EB470,0x005EB609)` SHA
`fbe813dbd1f9b94d87ee3c101867e8b12aaa36d69c08e68068c8ff06df990487`;
mode nonzero เดิน writer `0x0089A600`, mode zeroเดิน reader `0x0089A640`.

wire order ที่พิสูจน์ได้:

1. `tag 0x0B / 1B` จาก object `+0x18` — semantic UNKNOWN.
2. `tag 0x0B / 1B` = presence ของ target object ที่ `+0x14`.
3. ถ้า present: target serializer `[0x005DF250,0x005DF2F9)` SHA
   `ec9a5421ad5304372e440ecbb35184d6e93624444a262b3058569a724df0b5ef`:
   - `tag 0x12 / 2B @target+0x12` = `scene_id` (crosswalk จริงจาก RE-077)
   - `tag 0x32 / 8B @target+0x18` = sequence/identity qword ที่ existing builder เรียก `scene_seq`
   - `tag 0x0B / 1B @target+0x10` — semantic UNKNOWN
   - `tag 0x0B / 1B @target+0x11` — semantic UNKNOWN
   - `tag 0x2A / 4B @target+0x20,+0x24,+0x28` = vec3 X/Y/Z
4. `tag 0x0B / 1B` = presence ของ auxiliary object ที่ `+0x1C`.
5. ถ้า present: auxiliary serializer `[0x005DEF10,0x005DEFE9)` SHA
   `105bad91394ee1dc636ef80cfe3444c293a4114d5f371fafe3ebc76ccc049c93`:
   - untagged `uint32le byte_len + UTF-16LE` string `@aux+0x10`
   - `tag 0x0F / 2B @aux+0x2C`
   - `tag 0x14 / 4B @aux+0x30`
   - `tag 0x19 / 4B @aux+0x34`
   - `tag 0x32 / 8B @aux+0x40`
   - `tag 0x19 / 4B @aux+0x38` (**wire order เป็น +0x40 ก่อน +0x38 จริง**)
6. `tag 0x0B / 1B @top+0x20` — semantic UNKNOWN.
7. `tag 0x0F / 2B @top+0x22` — semantic UNKNOWN.

🔴 **correction ต่อ comment ปัจจุบัน (ไม่แก้ source ในรอบนี้):**
`current/pf_login_game_server_v141.py:2435-2441` compose base branch ถูกไบต์อยู่แล้ว — หลัง target ใส่
`u8tag(0x0B,0)` สองตัว. แต่ comment/assert ที่ `:5892-5894` เรียกสองตัวนั้นว่า
`TeleportVital +0x20` และ `+0x21/default byte`. ตัวแรกจริงคือ **aux-object presence (`top+0x1C`)**;
ตัวที่สองจึงเป็น `top+0x20`; **ไม่มี wire field `top+0x21` ใน serializer นี้**. เสนอ chief แก้ comment เท่านั้น;
builder bytes ไม่ต้องเปลี่ยนจากผลนี้.

### ปิดหก UNKNOWN rows ต่อทิศโดยไม่ใช้ linear negative

- read target-presence branch เรียก pool helper `0x004B1C40`, full recursive CFG
  `[0x004B1C40,0x004B1D4B)`, gap/error `0/0`, alloc `0x30`, ctor `0x005DF210`.
- read aux-presence branch เรียก pool helper `0x005EA810`, full recursive CFG
  `[0x005EA810,0x005EA91B)`, gap/error `0/0`, alloc `0x48`, ctor `0x005DEE20`.
- ทั้งสอง pool helpers มี direct-call census ครบและ **ไม่มี** `0x0089A600/0x0089A640`.
- `0x0088D050` / `0x0088D060` เป็น increment/decrement helpers; full CFG gap `0`, ไม่มี stream primitive.
- top-level full recursive CFG `[0x005EB470,0x005EB609)` = 148 instructions, gap/error `0/0`;
  direct calls มี W primitive 5, R primitive 5, nested codecs, allocatorsสองตัว, refcountสองตัว — ไม่มี call อื่นค้าง.

ดังนั้นป้าย `CALL_UNCLASSIFIED` / atomic lifecycle เดิมเป็นความระมัดระวังที่ถูกในชุดส่งมอบ แต่สำหรับ
objective ระดับ wire-field ของ RE-090 ปิดได้ว่า **ไม่ใช่ field เพิ่มเติม**.

## T1 — CWarpResult

registry: getter `0x005E51E0`, serializer `0x005E51F0`, handler `0x005EFB80`,
id global `0x01081FE8`. Full W/R codec `[0x005E51F0,0x005E529D)` SHA
`5e3acf83944a252a9c22b4cc42939589e2c1f373ee49881b782e66986c6db6a9`, recursive CFG
71 instructions, gap/error `0/0`.

wire order W/R:

1. `tag 0x32 / 8B @+0x18`
2. `tag 0x2A / 4B @+0x20`
3. `tag 0x2A / 4B @+0x24`
4. `tag 0x2A / 4B @+0x28`
5. `tag 0x12 / 2B @+0x2C`

`0x2A` เป็น float32 ตาม tag census; `0x12` เป็น uint16. ความหมายของ qword/u16 และ natural network
direction ยังไม่พบ (`PF_FIELD_VALIDATION` W/R = `NOT_OBSERVED`) — ชื่อ `Result` ไม่นับเป็นหลักฐานทิศ.

## T2 — comparison

- `ForcePos`: vec3 อย่างเดียว; ไม่มี presence bit, scene id, sequence, string หรือ extra control.
- `TeleportVital`: มี target presence + scene id + qword + target flags + vec3; มี optional auxiliary object;
  มี top byte `+0x18`, byte `+0x20`, word `+0x22` เพิ่ม.
- `CWarpResult`: qword + vec3 + u16 แบบ flat; ไม่มี nested presence objects.

จึง compose/decode แยกสามชนิดได้แล้ว ห้ามใช้ codec ของอันหนึ่งแทนอีกอันเพราะมี vec3 เหมือนกัน.

## T3 optional — TeleportCheckVital

registry: getter `0x00449430`, serializer `0x005E6670`, handler `0x005F2190`,
id global `0x01082074`; span `[0x005E6670,0x005E6693)` SHA
`bda2f64f997282a326dd01b0b77c1afe15d62dbae43a01e51584fa4083e3ce51`.
W/R ต่างกันแค่ primitive; ทั้งคู่มี `tag 0x0F / 2B @+0x14` หนึ่งตัว.

รันเครื่องมือเดิม read-only `tools/pf_teleportcheck_0x4477_static.py` ด้วย `py -B`:
**PASS 31 guards** — static image + 6/8 wire rows; สอง capture ที่ไม่มีสำเนาใน worktree ถูกติดป้าย
UNPINNABLE และ exclude ไม่ได้นับผ่าน. หกเฟรมที่ pin ได้เป็น client→server RuntimeReq body
`12 77 44 0B 00 0F 01 00`; นี่เป็น emulator/corpus evidence ไม่ใช่ original-server semantics.
ค่าที่ `+0x14` ยังต้องเรียก `field_u16_14`; ไม่ upgrade เป็น ack/result/scene id.

## verifier / reproducibility

- ใหม่: `pf_bridge/staged/re090_teleport_forcepos_wire_static.py`
- SHA-256: `7578fd6ae41819e36dab7cef2408fbdf5cad65862b488d5d15460c0317be8e61`
- final run สองรอบ: `53 guards / failed 0` ทั้งคู่; ใช้ `py -B`, ไม่สร้าง `.pyc`.
- recursive CFG 12 spans ทุก span gap `0`; table/image spans 8 จุดตรง SHA ทั้งหมด.
- draft แรก fail 2 guards เพราะ verifier นับ `tag 0x0B` ใน Teleport เป็น 5 แทน 6 — ลืมนับ
  **aux presence**. แก้เฉพาะ expected census จาก 5→6 ให้ตรง listing/CFG แล้วรันใหม่; ไม่เปลี่ยน input,
  semantic value หรือไบต์เพื่อให้ผ่าน. ความผิดนี้เองยืนยัน correction เรื่อง `+0x21` ข้างบน.

## integrity

- image `GameClient.local.bin` ก่อน/หลัง: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`,
  size `14,759,424` B.
- external tree ก่อน/หลัง: `30 files`, fingerprint
  `180424fe457e680e47b38b5b8e9a8094d2dc33c0c9c1f904b9f5a9a040dd11c5`.
- gamedata tree ก่อน/หลัง: `1,109 files`, fingerprint
  `6c7d05ca272d2fbb53098861606478af2c6ad41bdb637378c4554526357aee59`.
- server/current/docs/tools search inputs 13 files: SHA ก่อน/หลังตรง `13/13`; key files:
  `current/pf_login_game_server_v141.py` `2eb05ed2...4ea4c22`,
  `world_travel_gate.py` `06ba9ef8...1d5de2a`,
  `pf_teleportcheck_0x4477_static.py` `d74dfaf5...00412`,
  `docs/GM_LANE.md` `12331d23...a4b29`.
- RE-077 result/readback SHA `daf7b3c9...ffd39`; legacy vital registry SHA `b5880451...fce1f`.
- `AGENTS.md` `63d7de90...6026a`; queue `0571614a...f41a`; `NEW_ORDERS.txt` `6cf91534...a8030`;
  ไม่แก้ทั้งสามและไม่มี sync drift ระหว่างเลือกใบ/ส่งผล.

## nonclaims

1. ผลนี้เป็น shipped client image + static table/source/corpus เท่านั้น; ไม่มี client-observable claim.
2. ไม่อ้างความหมาย tag จากความกว้าง ยกเว้น `0x2A=float32` และ `0x12=uint16` ที่ tag census พิสูจน์ไว้แล้ว.
3. ไม่อ้าง natural direction ของ ForcePos/CWarpResult; ทั้งคู่ยัง `NOT_OBSERVED`.
4. ไม่อ้างว่า Teleport auxiliary object ใช้เพื่อ Columbus/ทะเล/GM; พิสูจน์แค่ wire shape.
5. ไม่ผูก `TeleportCheckVital field_u16_14` กับ ack/scene/marker เพราะยังไม่มี crosswalk.
6. ไม่ตัดสิน dock trigger (`RE-086`) หรือ captain-report confirm (`RE-087`) ว่าใช้ message ไหน.
7. ไม่พิสูจน์ candidate scene-id crosswalk/render และไม่เปลี่ยนผล RE-077.
8. ไม่แก้ source/external/gamedata/queue/registry; correction `+0x21` เป็นข้อเสนอ comment-only ถึง chief.

## BUILD_IMPACT

**BUILD_IMPACT:** ทำให้ compose/decode packet สำหรับเส้นทางผู้เล่น `Columbus → ทะเล → เกาะ` และ GM warp
ต่อได้โดยไม่ใช้ codec ผิดชนิด: `TeleportVital` base branch ที่มีอยู่แล้วตรงกับไบนารี, `ForcePos` เป็น vec3-only,
`CWarpResult` เป็น flat qword+vec3+u16. ความรู้นี้ส่งต่อโดยตรงให้ใบที่มีอยู่จริง `RE-085`, `RE-086`,
`RE-087` และ dependency “GM warp” ใน `docs/GM_LANE.md`/GM-003; natural trigger/direction ที่ยังไม่วัดต้องคง guard.

`BUILD_IMPACT_NONE: 0/1`

## static-only audit

ไม่เปิดเกม · ไม่บูต server/client · ไม่จับ/แตะ `LOCK_GAME` · ไม่แตะ canonical DB · ไม่แก้
GameClient/external/gamedata/source/tools/tests/docs/queue · ไม่ทำ git operation · ไม่เปิดใบใหม่
