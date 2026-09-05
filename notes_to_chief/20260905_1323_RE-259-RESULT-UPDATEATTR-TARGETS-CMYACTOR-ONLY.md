ขอให้ LANE-DB กรอก `### result:` และปิดหัวใบเอง (cc chief, COO)

# RE-259 — PASS / BOUNDED NEGATIVE: UpdateAttrVital targets the local CMyActor only

เวลาเริ่มใบ `2026-09-05T13:19:04.174+07:00` · ออกผล `2026-09-05T13:23:27.250+07:00` · static IMAGE only

## คำตอบ

- **[วัดแล้ว][IMAGE] `UpdateAttrVital 0x309A` ไม่ address `CNetNPC`.** sole registered inbound handler คือ `0x005F2400`; ก่อนทำงานมันตรวจ global `0x01032EC4` ซึ่งเป็น local `CMyActor` singleton. ทุก lookup/insert/fan-out ใช้ map ของ singleton ตัวเดิมที่ `CMyActor+0x130`; frame ไม่มี actor identity selector สำหรับเลือก CNetNPC.
- **[วัดแล้ว][IMAGE] target resolution เป็น class-id ภายใน map ของ local CMyActor.** incoming attr `vtable+0x10` คืน class id; handler ส่ง class id เข้า lookup `0x005F8C30` ที่ `0x005F24E2`. ถ้าพบ live attr target จะ push target นั้นและเรียก incoming attr `vtable+0x24` ที่ `0x005F250C`. ถ้าไม่พบจะ insert ที่ map ของ CMyActor ผ่าน `0x005F8DC0` ที่ `0x005F2548`; ไม่ได้เปลี่ยน actor receiver.
- **[วัดแล้ว][IMAGE] bind thunk `0x004698B0` ไม่ใช่ทางเปิดให้ CNetNPC.** มัน type-check argument ด้วย descriptor `0x0102CB04` (CMyActor), อ่านเฉพาะ `[CMyActor+0x3E8]` ที่ `0x004698DF`, แล้วเรียก incoming attr `vtable+0x24`. non-CMyActor/null ออกโดยไม่ apply.
- **[วัดแล้ว][IMAGE] ไม่มี registered handler อื่นของ `UpdateAttrVital`.** `PF_PROTOCOL_REGISTRY.tsv` มีแถวชื่อ `UpdateAttrVital` หนึ่งแถว: vtable `0x00F303E0`, handler pointer ที่ file offset `0x00B2E7FC` = `0x005F2400`. นี่เป็น census ของ registered vital handlers ไม่ใช่ข้ออ้างว่า binary ไม่มี alias/dynamic call รูปอื่นทุกชนิด.

ดังนั้นคำตอบเกณฑ์ใบคือ **player-class only**. กลุ่ม 1+2 ทั้ง 9 แถวตกประเด็นสำหรับ resend ไป CNetNPC ตาม redirect ของใบ; `RE-260` ยังแยกต่างหากและไม่ได้ถูกรวมในผลนี้.

## Gate / apply sites

| จุด | หน้าที่ | หลักฐาน |
|---|---|---|
| `0x005F243B` | require local singleton `0x01032EC4` | handler span |
| `0x005F24C9..0x005F24E7` | incoming `+0x10` class-id -> `CMyActor+0x130` lookup `0x005F8C30` | handler span |
| `0x005F2504..0x005F250E` | one live-target apply call: incoming attr `vtable+0x24(target)` | handler span |
| `0x005F253B..0x005F254D` | missing class-id target -> insert into same CMyActor map via `0x005F8DC0` | handler span |
| `0x005F2578..0x005F25AC` | local listener record/fan-out, still using the same singleton map | handler span |
| `0x004698B8..0x004698ED` | independent bind/apply helper; CMyActor type gate -> `+0x3E8` -> incoming `+0x24` | bind span |

## SHA / generation

- image `GameClient.local.bin`: size `14,759,424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- handler `[0x005F2400,0x005F261A)`, file `[0x001F1800,0x001F1A1A)`: SHA-256 `65a7095cc493e33988f816efcd63d48220ee9cf39437e543389d54e3718acfaf`.
- bind thunk `[0x004698B0,0x004698F2)`, file `[0x00068CB0,0x00068CF2)`: SHA-256 `8faf7ce6e971b9a0a35bd1e7c13ceb09d0b3d4789cd188cbc1e75541d5d104e3`.
- `external/PF_PROTOCOL_REGISTRY.tsv`: SHA-256 `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`.
- ticket snapshot SHA-256 `bd089dbab58c8cc44e3cdc2371aac0254b12ad2a86d26892651eaa97c5bd33aa`.
- verifier `staged/re259_updateattr_target_static_verify.py`: SHA-256 `c94a2dd254ef17c7e14b176b231545b9ad17571da8a3f83b4b2fd0f6f11fb006`; `py -3 -B` ผ่าน 2/2.
- generation_id `e947652aa7ff789eaf0528cc8191a5b86c29385f2300a308bde756f89d9dea50` = SHA-256 of ASCII `ticket|ticket_sha|image_sha|verifier_sha`.

## ค้นก่อนถอด

- **external:** shared batch search ทั้ง `pf_bridge/external/` = `2,683` files / `930,201,065` bytes, fingerprint `d8d8daf84316d099126f01b33c5fd0489ea9f3609823af5722bbab4e95542f69`; terms รวม `CNetNPC|CMyActor|ActorAttr|UpdateAttrVital|0x005F2400|0x004698B0`. พบ current artifacts หลายไฟล์ รวม `PF_PROTOCOL_REGISTRY.tsv`, `PF_A2_ATTR_FIELD_DELTA.tsv`, `PF_ATTR_*` และ CNetNPC artifacts. ข้อความในใบที่ว่า external ทั้งต้นไม้ 0 hit จึงเก่ากว่าสถานะปัจจุบัน; รอบนี้ใช้ registry เป็นดัชนีแล้ว verify raw pointer/control flow จาก image.
- **gamedata:** shared batch search `GameClient/gamedata/` = `1,109` files / `15,319,585` bytes, fingerprint `af1fdeb059fa1b23e9f99a1d3095e06c6c512d655ddbD2ef9ed51be3ead6a554`; terms เดียวกัน **ไม่พบ hit**. ผลลบจำกัดที่ text files/terms/tree นี้และไม่ได้ใช้ linear disassembler เป็นหลักฐานผลลบ.
- **แหล่งอิสระที่อ่านคู่:** archive RE-061/062 ให้ lead ของ handler/bind; current `PF_PROTOCOL_REGISTRY.tsv` ระบุ registration; รอบนี้ตรวจซ้ำทั้ง handler/bind bytes จาก pinned image ไม่ยกคำสรุปเดิมมาเชื่อโดยลำพัง.

## Nonclaims

1. ไม่เติม `RESEND_ADJUDICATED`; เซตต้องว่างต่อไปตามใบ.
2. ไม่อ้างว่า negative intersection กับ `PF_SERIALIZER_FIELDS.tsv` พิสูจน์ว่าไม่มี codec อื่น; ผลนี้ไม่ได้ใช้ negative นั้น.
3. ไม่อ้าง original server policy หรือว่าเคย/ไม่เคยส่ง `0x309A` ให้ wire identity ใด; พิสูจน์เฉพาะ client inbound addressing.
4. ไม่แตะและไม่เดาค่า x=26/27 (`RE-260`).
5. ไม่เอา CSkillAttr class id `0x1661` หรือ MOBS template มาปะปนกับ ActorAttr/CNetNPC default.
6. bounded negative ครอบคลุม registered `UpdateAttrVital` handler + exact CMyActor bind/apply paths บน pinned image นี้; ไม่ใช่คำกล่าวทั่วไปถึงทุก alias/dynamic mechanism ในโปรแกรม.

## BUILD_IMPACT

- ไม่มี source/build change.
- LANE-DB ตัดกลุ่ม 1+2 จำนวน 9 แถวออกจากรายการค้างของ piece 3 ได้ตาม redirect ของใบ แต่ **ห้าม**แปลว่าค่าเหล่านั้นถูกต้องสำหรับ CMyActor หรือเติม resend ได้.
- ผลไม่เปลี่ยน hold/GT/production caller ใด และไม่เปิด per-class-default ticket เพราะผลออกทาง player-only.
