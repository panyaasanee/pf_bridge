ถึง LANE-GM (cc chief)

# RE-263 — PASS / ANSWERED: RuntimeRes CNetNPC reaches the +0x98 zero gate before the faction fallback

เวลาเริ่มใบ: `2026-09-05T13:09:53.466+07:00`  
เวลาออกผล: `2026-09-05T13:17:21.815+07:00`  
วิธี: static IMAGE/RTTI/typed-crosswalk only; ไม่เปิดเกม/เซิร์ฟเวอร์และไม่มี capture

## คำตอบสามข้อ

1. **[วัดแล้ว][IMAGE] ถึงได้ — แบบมีเงื่อนไข ไม่ได้ข้ามพร้อม typed CNetNPC tail.** typed crosswalk `MCG-IMG-025` ผูก `RuntimeRes actor type 4 -> same CNetNPC instance -> actor registry/update -> selector [0x00443F50,0x004443C5)`; ภายใน selector มี direct call ที่ decoder ยืนยันไป `0x0043C380` ที่ `0x00444018` และ `0x00444152` โดย `ARIG-IMG-012/013` ระบุ `applies_to_class=CNetNPC`. เมื่อ relation function ผ่าน preconditions/early exits และได้ `ActorAttr` ของ operand ทั้งสองแล้ว จะเดินถึง gate `[0x0043C531,0x0043C547)` จริง ไม่มี CNetNPC-specific tail ที่กระโดดข้าม gate นี้.

   ขอบเขต: พิสูจน์ **static reachability** ของ RuntimeRes-spawned type-4 CNetNPC และ same-instance selector path ภายใต้ registry/controller/readiness/call gates เท่านั้น ไม่ได้อ้างว่ามอนทุกตัวผ่าน gate ทุกเฟรม หรือว่า live branch ใดถูกเลือก.

2. **[วัดแล้ว][IMAGE] default คือ byte `0`.** ActorAttr constructor `[0x00464BE0,0x00464D6F)` ทำ `xor ebx,ebx` ที่ `0x00464C10` แล้วเขียน `BL` ไป `[ActorAttr+0x98]` ที่ `0x00464D69` (พร้อม +0x99/+0x9A) โดยไม่มี write เข้า EBX คั่นกลาง. READ codec ที่ `0x00466A99` ทดสอบ presence mask `0x04000000` ใน `[ActorAttr+0x1B4]`; ถ้า mask ไม่ตั้งจะ `je 0x00466AC9` ข้าม read ของ `+0x98`, จึงคงค่า constructor = `0`.

   **แก้ถ้อยคำสำคัญ:** `0x04000000` เป็น **presence/change mask ของ serializer** ไม่ใช่ bit ภายใน `ActorAttr+0x98`. ตัว field เป็น `uint8`; gate ที่ `0x0043C531/0x0043C53A` ใช้ `cmp byte ptr [...+0x98],0` ทั้ง byte.

3. **[วัดแล้ว][IMAGE] เป็นลำดับ override-ก่อน-fallback ใน predicate เดียวกัน ไม่ใช่ผลคู่ขนานอิสระ.** ในฟังก์ชัน `[0x0043C380,0x0043C63C)` gate +0x98 มาก่อน: ถ้า operand แรก nonzero และ operand ที่สอง nonzero จะกระโดดไป constant-false surface `0x0043C48F`. ถ้าไม่เข้า early-false นี้ control ยังผ่าน gate อื่น แล้ว fallback ที่ `[0x0043C5C9,0x0043C5FF)` อ่าน `ActorAttr+0x68` ของสอง actor และ call comparator `0x004A1D50` ที่ `0x0043C5E0`. ดังนั้น faction comparator เป็น fallback ภายหลัง; +0x98 gate สามารถตัดจบก่อนถึง faction แต่ไม่ได้ผลิต FontStyleID เอง. ผล boolean เดียวของ relation function จึงถูก selector นำไปเลือกสาขา presentation ต่อ.

## หลักฐานและ SHA

- `GameClient.local.bin`: size `14,759,424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- relation predicate `[0x0043C380,0x0043C63C)`: SHA-256 `1d99f8557252742914c4f7358853aac06f0b54603f78a4b4d073aaea2afcbd89`.
- +0x98 gate `[0x0043C531,0x0043C547)`: SHA-256 `95198f2c96c0307b59d368369ed313df5742067aeada9c30bacfbdc8a3634981`.
- gate through faction call `[0x0043C531,0x0043C5E5)`: SHA-256 `9dc06e529a8d74c6df5cbd9d2725b488256ed624db08045d617dc30847a67f10`.
- ActorAttr ctor/default `[0x00464BE0,0x00464D6F)`: SHA-256 `c7fa9fb1d6688d9b66776cb82997531bee23a15a5dbc21a0c4de5b3c60003082`.
- read presence gate `[0x00466A99,0x00466AC9)`: SHA-256 `bb33e95dfe642429073d90ee621a961ca2b26d25c7c23956b2ae4f467b8fb565`.
- `external/PF_MONSTER_COLOR_GATE.tsv`: SHA-256 `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0`; ใช้ typed same-instance row `MCG-IMG-025`.
- `external/PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv`: SHA-256 `0192050fab1df86346a8aac069a3f0f3fbe90620589879a89890461780e812ad`; ใช้ typed CNetNPC direct-call rows `ARIG-IMG-012/013`.
- verifier `staged/re263_pair_relation_gate_static_verify.py`: SHA-256 `c15c5607442f69a6587b36bb41a567f36e6a110dc1de10ed3e423e3fb4d24b45`; รัน `py -3 -B` ผ่าน 2/2 ครั้ง.
- ticket snapshot SHA-256 `33efe2d27c76273970e0f5672c138089fe023464ac797f19b40a1910cd1a38ba`.

## ค้นก่อนถอด

- **external:** ค้น text artifacts ทั้ง `pf_bridge/external/` จำนวน `2,683` ไฟล์ / `930,201,065` bytes, fingerprint `d8d8daf84316d099126f01b33c5fd0489ea9f3609823af5722bbab4e95542f69`, terms `CNetNPC|CMyActor|ActorAttr|UpdateAttrVital|0x0043C531|0x0043C5E0|FontStyle`. พบคำตอบเดิมบางส่วนใน `PF_A2_ATTR_FIELD_DELTA.tsv` rows 6-7 และ typed crosswalk/callsite ใน `PF_MONSTER_COLOR_GATE.tsv` กับ `PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv`; รอบนี้ verify SHA และ re-derive control flow/default จาก image อีกครั้ง. ช่องค้นในใบที่ว่า external ไม่มี hit จึงเก่ากว่าสถานะ external ปัจจุบัน.
- **gamedata:** ค้น text files ทั้ง `GameClient/gamedata/` จำนวน `1,109` ไฟล์ / `15,319,585` bytes, fingerprint `af1fdeb059fa1b23e9f99a1d3095e06c6c512d655ddbD2ef9ed51be3ead6a554` ด้วย terms เดียวกัน: **ไม่พบ hit**. ผลลบจำกัดเฉพาะ text files/terms/tree นี้; ไม่ใช้ linear disassembly เป็นหลักฐานผลลบ.

## Nonclaims

- ไม่ตั้งชื่อ gameplay ของค่า `ActorAttr+0x98`; รู้เพียง default, codec presence และ consumer control flow.
- ไม่อ้างว่า value 0/1 หมายถึง hostile/friendly/monster/NPC และไม่อ้างว่ามอนทุกตัวเดินถึง faction fallback.
- ไม่อ้างว่าค่า default 0 ทำให้ได้ Style55 หรือ Style56 โดยลำพัง; style selector ยังมี identity/relation/controller gates อื่น.
- ไม่เปลี่ยนคำตัดสิน client-observable ของ FontStyle 55/56 และไม่สร้าง capture ใหม่.
- แยก IMAGE จาก DATA/wire/client-observable ตลอด; ไม่มี DB หรือ live server policy ในผลนี้.

## BUILD_IMPACT

- **ไม่มี source/build change ในรอบนี้.** คำตอบนี้ไม่ปลด `P2_COLOR_WIRING_BLOCKERS` โดยตรงตามขอบเขตใบ.
- สำหรับ server: การไม่ส่ง presence mask `0x04000000` ทำให้ CNetNPC ใช้ `ActorAttr+0x98 = 0`; อย่าเริ่ม emit ค่า nonzero เพราะความหมาย gameplay/full value domain ยังไม่พิสูจน์. Static result บอกเพียงว่าเมื่อทั้งสอง operand nonzero จะ early-false ก่อน faction comparator.
- LANE-GM ปิดหัว `RE-263` เป็น `PASS/ANSWERED` ได้; faction fallback ยังเป็นเส้นทางที่ต้องวัด live หากจะผูกกับสีของมอนจริง.
