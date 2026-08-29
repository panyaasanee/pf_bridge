[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-108 RESULT — DONE / LOCAL-PANEL-GATE-NO-RESPONSE-FRAME

- เวลาเริ่มใบ/ปิดใบ: `2026-08-27T17:13:04+07:00` / `2026-08-27T17:19:21+07:00` (Gregorian, +07:00)
- หมวด: `STATIC-ON-BRIDGE` เท่านั้น — ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ source/queue
- อิมเมจ: `GameClient\GameClient.local.bin` · SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- ticket/input SHA: `CLIENT_RE_QUEUE.md` `0f04061378c69ab3ede55c9e3e9532c537dc88ba417d29594c849b9b8ef55a7c`; `field_mob_tables.py` `158704080cc23180d0829d81848119327f335461519a848a1cab599aefaabb9e`; `field_mobs.py` `58bd7757efe3e48037c0376dbde3d5e491bf0782fd9497de3e35de9c0a31638e`
- วิธี: exact GUI resources + PE section mapping + SHA-pinned spans + recursive CFG; ไม่ใช้ linear disassembly เป็นหลักฐานผลลบ

## ช่องบังคับก่อนถอด

- **ค้น `pf_bridge\external\` แล้ว:** reuse manifest 30 files/fingerprint `42010a39b31acfb7b5770b899cee15f01e759eabf4cf13827373e28ce3e27ae1`. คำค้น `TargetVital|Main_Panel_Target|LABEL_NAME|PANEL_TARGET` เจอ 6 ไฟล์; คำตอบสำคัญอยู่ใน `PF_PROTOCOL_REGISTRY.tsv`/`PF_FIELD_VALIDATION.tsv`: `TargetVital` outbound มี capture 65, inbound 0 และ class handler ชี้ shared stub `0xA106C0`. ไม่พบ server→client target-panel verb อื่นในขอบเขตคำค้น.
- **ค้น `gamedata` แล้ว:** reuse manifest 1,109 files/fingerprint `8a87a0ddc5f76f33145b3140fdfc58d0ee5a3178905595f02715eb87c26d68d0`; คำค้นชุดเดียวกัน = **0 hit files**. แผงเป็น GUI/client code ไม่ใช่ CONST/TEXT gamedata row.

## T0 — ด่านคุม

image SHA/size ตรง pin. Verifier `staged/re108_target_panel_static.py` SHA-256 `0bfe9b9459a82795173964a773c75bc293b49f30997e3642665aead21c780cb0` รันผ่าน (`RESULT=PASS failures=0`). Recursive CFG ของ handler `0x51F2F0..0x51F494` ครบ 420/420 B, zero gap/error; span SHA `2c30e97a2624541afbff34ee08db4abc5f9b127b0dd4526f4d0c387aa01cf346`.

## T1 — ลูกศร/nameboard กับแผงบนจอเป็นคนละ resource และคนละ path

- `Data\GUI\Model\NameBoard_NPC.model` SHA `1442982e64543b9d53a328df84f0dfb246861ce964dbbb713426b73612f95dae`: มี `PANEL_TARGET` (selection arrows) ภายใน nameboard.
- `Main_Panel_Target_Enemy.model` SHA `bba55cec782cc057e8fdd935c502d599284bbf684be79224ea7a5047286a0238` และ `Main_Panel_Target_Enemy_New.model` SHA `621fab71bc66ac53069c724f4cdb791560825d0ae7310078167b512f7fa76cb8`: เป็น top target windows แยกไฟล์ มี `LABEL_NAME`, HP widgets และ level graphics ของตนเอง.

ดังนั้นผล GT-084-R2 “ขอบ/ลูกศรขึ้น แต่ top panel ไม่ขึ้น” ไม่ขัดกับโครงสร้าง client: สอง surface ไม่ได้เป็น widget เดียวกัน.

## T1/T2 — handler เปิดแผงและ gate ที่อ่านจริง

complete handler `0x51F2F0..0x51F494` ทำตามลำดับ:

1. ต้องมี local player และ event object (`0x51F32A..0x51F338`).
2. รับเฉพาะ event object สอง slot ที่ object เจ้าของเก็บไว้ (`this+0x34` หรือ `this+0x40`) แล้วดึง qword identity จากคู่ `+0x50/+0x54` หรือ `+0x58/+0x5C` (`0x51F366..0x51F386`).
3. resolve identity ผ่าน actor map `0x446170`; NULL หรือ identity ของ actor เป็นศูนย์ → ออกเงียบ (`0x51F38D..0x51F3A6`).
4. เทียบ relation กับ local player ที่ `0x43C380`; branch หนึ่งเรียก `0x43E010`, อีก branch เรียก `0x43E1D0` (`0x51F3AC..0x51F403`).
5. branch หลัง downcast actor ด้วย `0x469700`; helper นี้ pin token `0x102D954 = CNetNPC`. ถ้าผ่านจึงเรียก UI manager `0xAA0710` โดยชื่อ exact `L"Main_Panel_Target_Enemy_New"` (`0x51F432..0x51F45D`).

ใน complete handler นี้ **ไม่มี actor vt+0x74 GetAttr และไม่อ่าน BasicAttr name `+0x28`, HP `+0x44/+0x48` หรือ level `+0x5E`**. ฟิลด์เหล่านี้เป็น consumer หลังเปิดแล้ว:

- name/selection consumer `0x51F920..0x51FC10` SHA `5765ee333d54e9817299e353f709a4da22caa450ff17ac13b702d8d959f40094` อ่าน BasicAttr `+0x28`.
- target HP consumer `0x51F150..0x51F2B2` SHA `85b49baee8283e0efcab245f637c454e4c86bcd34897f15ec0e161b1beca50e4` อ่าน `+0x44/+0x48`.

ผลเทียบ roster: `field_mob_tables.py` มี level 27 ของ Tornado Eagle แต่ `field_mobs.py` wire body ส่ง name/current+max HP/scene/faction ผ่าน NPCAttr และ **ไม่ได้ส่ง BasicAttr level**. นั่นอธิบายได้เพียงว่าถ้าแผงเปิดอาจแสดง ctor default LV1; **ไม่ใช่ gate เปิดแผง** และห้ามเติม level เพื่อหวังแก้อาการนี้.

## T2 — ไม่มี select-target response vital ที่เปิดแผง

`PF_PROTOCOL_REGISTRY.tsv` ผูก inbound handler ของ `TargetVital` กับ `0xA106C0`; ไบต์ exact `32 C0 C2 04 00` = `xor al,al ; ret 4`, shared false/no-op stub. Serializer มีเพียง qword actor identity + u8 kind; `PF_FIELD_VALIDATION.tsv` มี W=65/R=0. Runtime precedent SCENE-005 เปิด red target panel พร้อม client ส่ง `TargetVital` kind 1 และ V96 จงใจไม่ตอบ TargetVital.

ดังนั้น **TargetVital เป็นรายงานขาออกหลัง/ระหว่างการเลือก ไม่ใช่คำขอที่ต้องมี server response เพื่อเปิดแผง**. การสร้าง echo/ack จะเข้าถึง no-op และไม่แก้ UI; ไม่มี provenance ให้เพิ่ม frame ใดจากเซิร์ฟเวอร์.

## T3 — คำตอบ bounded negative และ capture ถัดไปที่แคบที่สุด

**เสนอปิด RE-108 เป็น DONE.** Static ให้ handler/gates และตอบข้อ “ต้องส่งอะไรเพิ่ม” เป็น **ไม่มี field/frame ที่พิสูจน์ได้**: open decision อยู่ก่อน attr consumers และเป็น client-local identity/event/relation/CNetNPC path. สิ่งที่ static ยังบอกไม่ได้คือ GT-084-R2 หลุดที่ event slot ใดหรือ relation branch ใดใน runtime.

capture ที่แคบที่สุด: ใน session เดียว/actor wire เดิม ให้ A = single-click `0x201F`, B = Tab-select `0x201F`; เก็บจอ + raw outbound RuntimeReq/TargetVital โดยไม่ให้ server ตอบอะไร. ถ้า B เปิดแผงแต่ A ไม่เปิด ⇒ แยกได้ว่า input event object/path ต่างกัน. ถ้าทั้งคู่ไม่เปิด ให้เพิ่ม control C single-click CNetNPC ที่รู้ว่าเปิดแผงได้ใน session เดียว แล้วเทียบ TargetVital actor id/kind และ UI; **ห้ามเปลี่ยนหรือเติม attr/frame พร้อมกัน**.

## nonclaims

- ไม่ claim ว่า server ถูกหรือผิดจากการไม่มีแผง; พิสูจน์เฉพาะว่าไม่มี response vital/attr gate ใน handler ที่ถอดครบ.
- ไม่ claim ว่า relation `0x43C380` คืนความหมายเชิงชื่อใดในเคส runtime นี้; บันทึกเพียง branch/call ที่อ่านจริง.
- ไม่ claim ว่า outbound TargetVital ทำให้ panel เปิด; handler inbound ของมันเป็น no-op และ correlation ไม่ใช่ causation.
- ไม่อ้างว่า level 27 บนตารางถึง wire; แยก table metadata ออกจาก BasicAttr field อย่างชัดเจน.

## BUILD_IMPACT

`BUILD_IMPACT: NONE` — ห้ามเพิ่ม TargetVital response หรือ BasicAttr level เป็น guess-fix. ถ้าจะทำต่อให้ทำ attended A/B ที่เปลี่ยนเฉพาะ input method ตามข้างบน.

## read-only integrity

ก่อน/หลัง: image, queue, NEW_ORDERS, `field_mob_tables.py`, `field_mobs.py` SHA ตรงค่าหัวจดหมาย; source inputs ไม่ถูกแก้.
