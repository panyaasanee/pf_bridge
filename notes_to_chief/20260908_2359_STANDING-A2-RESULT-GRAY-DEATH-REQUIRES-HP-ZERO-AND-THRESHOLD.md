งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B; cc LANE-K, COO, chief
FROM: Codex RE/static · 2026-09-08T23:55:41+07:00
RESULT: DONE — A2 CNetNPC death predicate and conditional gray-name branch

## คำตอบ

[MEASURED][IMAGE] predicate ที่ A2 ถามคือ `0x0043BD70`: **HP dword ที่ BasicAttr+0x44 ต้องเท่ากับ 0 และ float32 ที่ +0x58 ต้องเป็นค่าที่เปรียบเทียบแบบ ordered แล้ว ≤0**. HP=0 อย่างเดียวไม่พอ; +0x58≤0 อย่างเดียวก็ไม่พอ. นี่เป็นเงื่อนไขจำเป็นและพอเพียงของผล true ใน predicate นี้ภายใต้ getter ที่ใช้งานได้ ไม่ใช่เงื่อนไขจำเป็นของชื่อเทาทุกเส้นทาง

[MEASURED][IMAGE] CNetNPC actor vtable `0x00F0DF58` slot `+0x3C` ชี้ predicate นี้. ภายในเรียก slot `+0x74`; สำหรับ vtable นี้คือ `0x0045CD20` ซึ่งคืน pointer ที่ **actor+0x358**. Predicate อ่าน `+0x44` และ `+0x58` จาก pointer ที่คืน ไม่ใช่ออฟเซ็ตบน nameboard หรือการอ่าน NPCAttr+0x35C แทนกัน. หลักฐานชื่อ/ชนิด BasicAttr เดิม: `MCG-IMG-034`; การตรวจ getter รอบนี้เพิ่มจุดอ้างอิงชัดเจน

[MEASURED][IMAGE] byte test เป็น HP **==0** ไม่ใช่ HP≤0. จากนั้น `XORPS` ทำค่าศูนย์, `COMISS 0,[attr+0x58]` และ `JB` ไป false. ค่าบวกทำให้ false; ศูนย์ทั้งสองเครื่องหมายและค่าลบปกติทำให้ true. NaN ไม่ผ่าน ordered comparison เมื่อ invalid exception ถูก mask; รอบนี้ไม่วัด MXCSR/exception mode จริง และไม่อ้างพฤติกรรม subnormal/DAZ/FTZ

## ฟิลด์บนสาย

[MEASURED][IMAGE] `MWC-IMG-008/009` และ codec จริง `0x004656F0` พิสูจน์สองฟิลด์แยก gate:

| field_key ฝั่ง READ | applies_to_class ในคำตอบนี้ | gate บน BasicAttr mask+0x70 | tag / len | READ call / WRITE call |
|---|---|---|---|---|
| BasicAttr@0x44.4#R:b0x00000004 | CNetNPC death predicate | 0x0004 | 0x14 / 4 | 00465893 / 00465759 |
| BasicAttr@0x58.4#R:b0x00000080 | CNetNPC death predicate | 0x0080 | 0x2A / 4 | 004658F7 / 004657BD |

[MEASURED][IMAGE] จึงเป็น **สองค่าในสถานะที่อ่านร่วมกัน** ไม่ใช่ฟิลด์ “สีเทา” แยกหรือ local IsDead latch อีกตัวใน predicate นี้. การตรวจนี้ไม่กำหนดว่าต้องส่งเฟรมเดียว/สองเฟรม และไม่พิสูจน์การ apply บาง mask ว่ารักษาค่าเก่าอย่างไร. ห้ามเอาความเป็นอิสระของ gate ไปอ้าง wire ordering

[NONCLAIM] `+0x58` ใช้ชื่อในคำตอบนี้ว่า death-threshold operand. ไม่พิสูจน์ว่ามันลดเองตามเวลา หน่วยเป็นวินาที หรือ sender ต้องเดิน timer อย่างไร. ORD-003 ที่อ่านก่อนเริ่มถาม **ผู้เล่น CMyActor** (`0x454A70/0x454AC0`), writer census และ Common_Death UI; A2 นี้ไม่ปิด ORD-003 และไม่ยกคำว่า “ไม่มี countdown” จากฟังก์ชันเล็กนี้เป็นข้อสรุปทั้งอิมเมจ

## จาก true ไปป้ายชื่อเทา

[MEASURED][IMAGE] ใน selector `0x00443F50` หลัง identity เข้า nonpositive lane และ relationship คืน false, call receiver slot `+0x3C` ที่ `0x0044418E`. ถ้า true กิ่ง `0x0044419F` ส่ง FontStyleID **63** ให้ controller ของ actor นั้น. ผู้บริโภค UI คือ **LABEL_NAME** ที่ controller+0x50 — ป้ายชื่อเหนือ actor ไม่ใช่หลอด HP หรือแผง target

[MEASURED][IMAGE] ต้องผ่าน updater ด้วย: actor+0x254/controller+0x10 ไม่เป็น null, squared xyz distance ≤10000² และ flags actor+0x258/+0x260 พร้อม. หลักฐาน binding/label/readiness เดิมอยู่ใน `PF_MONSTER_COLOR_GATE.md:108–115,354–362` และจดหมาย A1 `20260908_2351_STANDING-A1-RESULT-HIT-BIT-CHANGES-STYLE-ON-SAME-ACTOR.md`. การเป็นศพไม่ได้รับประกันว่าจะเข้า selector ทุก invocation

[MEASURED][DATA] `GameClient/Data/GUI/Model/BigFontStyle.fsl:64` กำหนด style63 FontColor `(179,179,179,255)`, outline `(60,60,60,255)`; file SHA `77798599c203d36e11282633d4a91ac098b0e1e03aa2482fede6fcfca161fc10`. นี่คือ palette สีเทา ไม่ใช่หลักฐานว่ารอบนี้เห็นภาพนั้น

[MEASURED][IMAGE] **ชื่อเทาไม่เท่ากับตายเสมอ**: selector ยังมีการขอ63 ที่ `0x00444214/0x00444218` จากกิ่ง associated actor/local context. ใช้ scope/nonclaims ของแถวเดิมใน `PF_ATTR_NAME_COLOR_SELECTOR.tsv`; ไม่ขยาย owner-class ของแถวเหล่านั้น. การทดสอบ death branch ต้องแยกจากกิ่งข้างเคียง ไม่ใช้สีอย่างเดียวตัดสิน

## หลักฐานและวิธีตรวจ

[MEASURED][OUTPUT-AUDIT] ภาพอิมเมจ 14,759,424 bytes; SHA ก่อน/หลังตรง:
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
Reuse `MCG-IMG-030/034` + `MWC-IMG-008/009`; ไม่เพิ่ม field census ซ้ำ

| ขอบเขต [start,end) | VA | File offset | SHA-256 |
|---|---|---|---|
| predicate เดิม | 0043BD70–0043BD9D | 0003B170–0003B19D | 1df3c62b4bbe0aab1ebf1404320a7b2466ef20390db060e67ba183a1178127aa |
| death→63 | 00444187–004441A8 | 00043587–000435A8 | 5f3e5fb833e3b2f4742ae23b8ac93368c97f01ecf7d373240fc1e049af59b876 |
| BasicAttr codec | 004656F0–00465983 | 00064AF0–00064D83 | d0c15b74a36077df30a0e60dbeb8441e878c08b82587c1ea55365ab2ebd70020 |
| slot74 getter รวม padding | 0045CD20–0045CD30 | 0005C120–0005C130 | 97170e9079209a8ba93c20b1fcabb1bf06e939b94a467f2918c5dcca1a23d329 |

[MEASURED][OUTPUT-AUDIT] `staged/standing_a2_dead_verify.py` เป็น stdlib ล้วน. ผล `standing_a2_dead_verify_20260908.log`: 8 spans, 6 instruction pins, 2 vslots, 4 primitive edges ผ่าน. แก้ byte ในหน่วยความจำแล้วเรียก guard จริง: 8 span traps, 6 instruction traps, whole-image trap ถูกปฏิเสธครบ. มี bounded instruction model เดิน branch displacement จากฟังก์ชันจริง 10 cases/20 instruction starts; **เป็น model ไม่ใช่ native execution**. HP1/HP-1→false, HP0+20→false, HP0±0/−1→true เป็น controls หลัก

```powershell
& 'C:\Users\Panya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\standing_a2_dead_verify.py'
```

[MEASURED][DOCUMENT-SEARCH] ค้นชุดส่งมอบแล้ว **เจอ** registry BasicAttr ที่ `external/PF_PROTOCOL_REGISTRY.tsv:4`, แต่แถว `PF_SERIALIZER_FIELDS.tsv:6–7` เป็น argument copier ที่ slot คนละตัว จึงใช้ codec+0x34 ที่พิสูจน์แล้วใน MWC แทน. ค้น gamedata index/columns ด้วย `43BD70|43bd70|IsDead|hp_death_timer` ไม่พบในสองไฟล์นี้; ไม่ใช่ข้อสรุปว่าไม่มีข้อมูลในเกม. ค้น archive/consumed/reference แล้ว **เจอ** predicate และข้อเตือนแยก actor/controller: `archive/notes_to_chief_2026-09/CODEX_URGENT_20260901_1040_COLOR-CROSSWALK-CORRECTION.md:10–11`, `notes_to_chief/consumed/20260901_0921_LANE-GM-STATUS-p2-color-static-research-fontstyle63-gap-re-followup-proposed.md:19`, `reference_codex_attr/PF_MONSTER_COLOR_GATE.md:354–362`

## ส่งต่อ

BUILD_IMPACT: [PROPOSED] LANE-B ใช้กับ GT-224 เพื่อให้ชื่อมอนที่ตายเปลี่ยนเทาโดยมีเงื่อนไขสถานะทั้งสองค่าครบ และแยกจาก gray เพราะ lookup ไม่สำเร็จ
BUILD_PROPOSED: [PROPOSED] ผูก BasicAttr HP=0 และ death-threshold≤0 ให้ actor เดิม พร้อมตรวจการถึง death→style63 branch และ LABEL_NAME | LANE-B | A2_DEATH_BRANCH_STYLE63 (proposed; ยังไม่ measured)
[PROPOSED] ขอ LANE-K ผูกเลขย้อนหลัง; ผู้บริโภคผลเปิดใบสร้าง/GT ตามกฎ. รอบต่อไปอ่านคิวใหม่ก่อน แล้ว A3 หากคิวยังว่าง

## nonclaims

- ไม่เปิดเกม/เซิร์ฟเวอร์ ไม่แก้ source, queue, lease หรือ DB; ไม่อ้างจอผ่าน
- ไม่พิสูจน์ animation ตาย, corpse removal/respawn, timer writers ทั้งอิมเมจ, death→loot, หรือ revive UI
- ไม่อ้างสองค่าพอให้เห็นสีโดยไม่ผ่าน identity/relation/controller/update gates; ไม่อ้างว่า style63 มีสาเหตุเดียว
- ไม่ promote M3/M4 และไม่สรุป semantics จากชื่อแถวหรือ offset เดียวกันข้ามคลาส


[MEASURED][OUTPUT-AUDIT] หลังแก้ข้อพบของ pf-adversary: ตัวเลขรายงาน derive จาก checks ที่รันจริง และบังคับ exact coverage ของ span/pin/case/20 instruction starts; empty-coverage traps อีก4ชุดถูกปฏิเสธ. ตรวจแก้เฉพาะ false-green defect แล้วไม่พบข้อบกพร่องค้างในขอบนี้. Verifier SHA `89dbc82621f17e46de2d76c58ea72bff2f9a9955006729bc6b8dc85bdb616ed2`; log SHA `34d819e68be7f08b9565dc291d875d12f0bfa2b4f9763a27b9cb7a3d2bc817ba`.
[MEASURED][OPERATIONS] Published 2026-09-08T23:59:13.395637+07:00. อิมเมจและ4 pinned inputsผ่าน pre/post verifier; queue/orders SHAตรงก่อนปิด. ไม่เปิดเกม/เซิร์ฟเวอร์หรือแตะ DB/source/queue/lease. บันทึก memory แล้วปล่อย RE lock เป็นขั้นถัดไป.

SCOREBOARD: STATIC-PROVEN | ระบุสองค่าที่ death predicate ของ CNetNPC ต้องอ่านก่อนขอป้ายเทา; จอยังไม่วัด | MCG-IMG-030/034 + standing_a2_dead_verify.py
