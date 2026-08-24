ถึง: chief (cloud)

# RE-062 RESULT — (ค) inbound มีเส้นทางอื่น แต่ไม่สร้าง/ผูก `[actor+0x3E8]`

- เวลา: `2026-08-24T17:01+07:00`
- สถานะที่เสนอ: **DONE**
- วิธี: static read-only บน `GameClient.local.bin` · recursive CFG จาก entry ที่ใบกำหนด + byte-exact census ของ executable sections
- ไม่ได้เปิด server/client/game และไม่ได้แตะ canonical DB

## คำตอบสั้น

เลือก **(ค) เส้นทางอื่น**:

1. decoder สร้าง `CSkillAttr` **ชั่วคราวสำหรับข้อมูลขาเข้า** ได้จริง ผ่าน registry/factory → clone → allocator/ctor แล้วใส่ใน collection ของ `UpdateAttrVital`;
2. handler หา live target จาก **generic attribute map ด้วย class ID `0x1661`** ไม่ได้หาโดย `[actor+0x3E8]` และไม่ได้หาโดย identity tag `0x32`;
3. ถ้า map มี target จะ apply/copy เข้า target นั้น; ถ้า map ไม่มี target จะ insert incoming object เข้า **generic attribute map**;
4. ไม่มีแขนงใดใน decoder/handler/map insert/bind/apply ที่เขียน `[actor+0x3E8]`;
5. dedicated slot นี้ถูก zero แล้วสร้าง+เขียนตั้งแต่ `CMyActor` constructor. ถ้า slot กลายเป็น null ตอน bind, bind ส่ง null เข้า `CSkillAttr::apply`; apply ตรวจ null แล้ว return — ไม่ allocate, ไม่เรียก ctor, ไม่ repair slot.

ดังนั้นเฟรม inbound อาจสร้าง/เก็บ attr ใน map ได้ แต่ **ไม่สามารถสร้างความสัมพันธ์ใน dedicated slot `[actor+0x3E8]` ขึ้นใหม่**. ถ้า gate K อ่าน slot นี้และมัน null จริงใน runtime, sender อย่างเดียวซ่อม gate นี้ไม่ได้.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `UpdateAttrVital` handler `0x5F2400` ใน protocol registry, `CSkillAttr` vtable `0xF48B78`, class ID `0x1661`, validation corpus ที่ยังเป็น `NOT_OBSERVED`, และ serializer rows เดิมที่ขึ้น `EMPTY` (มี extractor caveat ที่ `+0x18`); ไม่มีคำตอบ null-branch สำเร็จรูป จึง verify SHA แล้ว trace จากอิมเมจต่อ
- **ค้น gamedata แล้ว: ไม่เจอ** token `CSkillAttr`, `UpdateAttrVital`, `0x1661`, `4698B0`, `5F2400`, `751C70`, `751B90` ในชุดที่ค้น; เจอเพียง mapping UI ที่เกี่ยวข้องคือ hotkey `75` (`K`) → `ABILITY` และ main-menu `Skill_Main2` / `Bt_main_Skill` ซึ่งไม่ตอบ target binding

## เส้นทางที่พิสูจน์

### A. incoming object ถูกสร้าง แต่เป็น decode object

`collection decoder` อ่าน class ID/body → registry lookup/factory → vtable clone ของ `CSkillAttr` → pool helper → ctor. Byte census พบ rel32 call เข้า ctor `0x751B90` ครบ 3 จุดเท่านั้น: `0x44B3A4`, `0x44B422`, `0x5F8BB8`; จุดใน receive decoder เองไม่มี direct ctor call. Factory path สร้าง object สำหรับ decode ก่อน insert เข้า incoming collection.

### B. handler resolve ด้วย class ID และ generic map

handler เรียก incoming vtable `+0x10` เพื่อได้ class ID `0x1661`, แล้วเรียก lookup wrapper → generic map lookup. เมื่อพบ target จึงเรียก incoming vtable `+0x24` เพื่อ apply; เมื่อไม่พบจะเรียก insert wrapper → generic map insert. ทั้งสองแขนงไม่อ้างหรือเขียน `[actor+0x3E8]`.

### C. dedicated slot มาจาก actor constructor

ใน `CMyActor` ctor: `0x44CA71` zero `[esi+0x3E8]`; จากนั้น pool helper สร้าง `CSkillAttr`, `0x44CBC1` เขียน pointer ลง slot และ register object เข้า live attribute manager. นี่เกิดก่อนรับเฟรม ไม่ใช่ null-repair branch ของ inbound.

### D. bind ตอน null เป็น no-op

bind type-check actor แล้วอ่าน `[actor+0x3E8]` ที่ `0x4698DF` โดยไม่สร้าง object. ค่านั้นถูกส่งเข้า apply; apply ตรวจ target null และคืนทันที. Exhaustive overlapping decode รอบ raw displacement `0x3E8` พบ candidate 65 จุด/เขียน 13 จุดทั้ง executable image แต่ intersection กับ exact inbound spans (decode, handler, lookup/insert, bind, apply) เท่ากับ **0**. ผลลบนี้จึงไม่ได้อาศัย linear disassembly.

## ความสัมพันธ์กับ DBAttribute identity tag `0x32`

DBAttribute serializer ใช้ mask byte ที่ `this+0x20`; เมื่อ bit 0 ติดจึง serialize qword tag `0x32` จาก `this+0x18/+0x1C`. แต่ handler เลือก target ก่อนด้วย class ID `0x1661` ใน generic map. หลังเลือก targetแล้ว DB-base copy จึงคัดลอก qword identity จาก incoming ไป target. ใน CFG ที่ trace ไม่มี equality check/crosswalk ที่ใช้ qword นี้ resolve target — มันเป็น **payload ที่ถูก copy ภายหลัง ไม่ใช่ lookup key**.

## spans / offsets / SHA-256

| หน้าที่ | entry/span | file offset / len | SHA-256 |
|---|---|---:|---|
| collection decoder | `0x463DE0 [0x463DE0,0x463FA2)` | `0x631E0 / 450` | `888c2fac20948b7896ed105f46b84e94d01c9442f6535df9be36e6baa2335fc3` |
| registry/factory lookup | `0x5E2E00 [0x5E2E00,0x5E2E6C)` | `0x1E2200 / 108` | `c6d356a1e8ee06128aa2c579cbd80a4777b1f61c7f7e4ae666d618abdd0ed449` |
| CSkillAttr clone/factory | `0x751FA0 [0x751FA0,0x751FB2)` | `0x3513A0 / 18` | `dc1e7f4bff93db88790b21961276beee1e53e2b37ed1f8eaa31f7d115a3d3c46` |
| CSkillAttr pool helper | `0x44B340 [0x44B340,0x44B44B)` | `0x4A740 / 267` | `0125607e31d0c31ef7ac9d4146352133add2e7c591dce65a326930d807189928` |
| CSkillAttr ctor | `0x751B90 [0x751B90,0x751BEA)` | `0x350F90 / 90` | `3abf69326a7a821bdecd8146e3e10094fbe17086eca54ead65b30124e905bcc4` |
| UpdateAttrVital handler | `0x5F2400 [0x5F2400,0x5F261A)` | `0x1F1800 / 538` | `65a7095cc493e33988f816efcd63d48220ee9cf39437e543389d54e3718acfaf` |
| lookup wrapper | `0x5F8C30 [0x5F8C30,0x5F8C38)` | `0x1F8030 / 8` | `4ac9cc919c1940986e14a9fb18344c6507b796d927507d033db5ee9865441066` |
| generic map lookup | `0x463800 [0x463800,0x463866)` | `0x62C00 / 102` | `96b26fce649bee2a7fe0da51722b7834543f0fb7f9026de81772b0a230d8daa3` |
| insert wrapper | `0x5F8DC0 [0x5F8DC0,0x5F8DDA)` | `0x1F81C0 / 26` | `4764bc9fc16895683115af4040ac6a2ed58419575cddef5c8d45fd94d8a7f49e` |
| generic map insert | `0x463720 [0x463720,0x4637F6)` | `0x62B20 / 214` | `1a9279dd7589c6e1b48a27044434274565212220daae4c34f0b4c6928a6840b3` |
| CSkillAttr bind | `0x4698B0 [0x4698B0,0x4698F2)` | `0x68CB0 / 66` | `8faf7ce6e971b9a0a35bd1e7c13ceb09d0b3d4789cd188cbc1e75541d5d104e3` |
| CSkillAttr apply | `0x751C70 [0x751C70,0x751CB8)` | `0x351070 / 72` | `1e8d5b2e6a7814bc88cec812188d05a8673aa5d3c69e9ba9c963a2d0cd98738e` |
| DBAttribute base copy | `0x4676A0 [0x4676A0,0x4676E4)` | `0x66AA0 / 68` | `385340e6daf6b1adaf73ef2fd0cb6fc90088cf72a3b8b395b309521a91b6e17e` |
| DBAttribute serializer | `0x467790 [0x467790,0x4677E8)` | `0x66B90 / 88` | `379f37ad0307e785fb4a230fc9f1871f69587e6a314da5930a3a4ed289e55608` |
| CMyActor ctor | `0x44C990 [0x44C990,0x44CC64)` | `0x4BD90 / 724` | `2fca43bcce327186a180e8be6f88b41df98ef2c26cbd20fb5ec0e6ccb443c0ae` |
| live-register wrapper | `0x5F8C10 [0x5F8C10,0x5F8C29)` | `0x1F8010 / 25` | `7172630f82334eff079f3e5466bf1abc449330842c7f8e686ecd546d64dc891c` |
| live-register implementation | `0x463930 [0x463930,0x4639BB)` | `0x62D30 / 139` | `fb0df5fe3c64badfffb6f15703544c9be427f5c90e7f03f7040e6635faee6303` |

vtable `0xF48B78`, 16 slots, file offset `0xB46F78`, SHA-256 `6777057f24854ecdf7726e59b57ebff436d304cf4be925170c7a0942231963ba`.

## SHA before/after และหลักฐาน

- image: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`, 14,759,424 bytes
- input manifest ก่อน/หลังเทียบทั้ง SHA/size/path แล้ว: **IDENTICAL 7/7**
- manifests: `staged/re062_input_hashes_before.tsv`, `staged/re062_input_hashes_after.tsv`
- recursive CFG: `staged/re062_cfg_probe_output.txt`, `re062_helper_cfg_output.txt`, `re062_map_cfg_output.txt`, `re062_ctor_paths_cfg_output.txt`, `re062_decode_factory_cfg_output.txt`, `re062_identity_clone_cfg_output.txt`
- byte-exact census + guard: `staged/re062_static_probe.py`, `staged/re062_byte_census_output.txt`
- artifact hashes: `staged/re062_artifact_hashes.tsv`

## Nonclaims / ขอบเขตผล

- ไม่อ้างว่า `[actor+0x3E8]` เป็น null หรือ non-null จริงใน GT-058/GT-059; ใบนี้เป็น static semantics เท่านั้น
- ไม่อ้างว่า dedicated slot ไม่มีทางถูก clear ภายหลัง actor construction; พิสูจน์เฉพาะ receive/bind path ที่ใบถาม
- ไม่อ้างว่า generic-map object เท่ากับ dedicated-slot object เมื่อ slot ถูกทำให้ null; ไม่มี crosswalk field รองรับการ join เช่นนั้น
- ไม่อ้างว่าเฟรม HYP-PF-035 เพียงพอเปิด K; ถ้า runtime slot null เฟรมนี้ repair ไม่ได้ และถ้า slot non-null ยังอาจมี gate อื่น
- `external` แถว `EMPTY` เดิมมี extractor caveat จึงไม่ใช้เป็นหลักฐานผลลบ
- raw overlapping decode ที่อยู่นอก exact inbound CFG เป็น census candidate เท่านั้น; ไม่ตีความเป็น global semantic writes

## ผลต่อ GT-059

RE-062 ปิดคำถามโครงสร้าง: **sender ไม่สร้าง dedicated slot เมื่อมัน null**. แต่ normal `CMyActor` construction สร้าง slot นี้ไว้ก่อนแล้ว จึงยังต้องวัด runtime ใน attended GT-059 ว่ากรณีจริงอยู่ฝั่งใด. ถ้าผล wire ถึง client แต่ K ยังไม่เปิด ต้องแยกอย่างน้อย `slot null/no-op` ออกจาก `slot non-null + gate อื่น` ด้วยหลักฐาน runtime; static ใบนี้ไม่แทนการเปิดเกม.
