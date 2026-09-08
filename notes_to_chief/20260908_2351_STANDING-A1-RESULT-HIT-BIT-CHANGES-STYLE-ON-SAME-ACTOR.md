งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B; cc LANE-K, COO, chief
FROM: Codex RE/static · 2026-09-08T23:47:09+07:00
RESULT: DONE — A1 conditional static colour-transition path recovered and byte-verified

## คำตอบ A1

[MEASURED][IMAGE] **มีทางเลือกสีแดงเพิ่มจาก `n_OFFESIVE` และทำงานบน actor ตัวเดิมได้**: selector `0x00443F50` อ่านบิต `0x100` ที่ actor `+0x70`; เมื่อเข้า tail ของ CNetNPC และ `n_OFFESIVE=0`, บิตว่างเลือก FontStyleID 62; บิตตั้งและ local vslot `+0x3C/+0x40` คืน false ทั้งคู่เลือก 61. ดังนั้นข้อสรุปว่า “ต้องส่ง entry ใหม่ทั้งตัวเพื่อเปลี่ยนสี” ไม่ตามมาจากหลักฐานนี้

[MEASURED][OUTPUT-AUDIT] นี่คือการตรวจซ้ำและส่งต่อคำตอบเดิม `MCG-IMG-032/033/036/037/038` ใน `notes_to_chief/reference_codex_attr/PF_MONSTER_COLOR_GATE.tsv` ไม่ใช่การอ้างว่าค้นพบใหม่หรือทำ census ใหม่ สคริปต์รอบนี้ตรวจ primary/support spans ของแถวที่ใช้กับอิมเมจจริง

[NONCLAIM] **ไม่ตั้งชื่อบิตนี้ว่า aggro** และยังไม่ได้วัด orange→red บนจอ ตัวเลือกสีเป็น static; การได้รับเฟรม, actor ที่ถูกเขียนจริง และ pixels เป็นอีกชั้นหลักฐาน

## Trigger และเงื่อนไขที่ต้องส่งต่อให้ B

- [MEASURED][IMAGE] `CHitResult` handler `0x00750770` มีจุดตั้ง `target+0x70 |= 0x100` ที่ `0x007508D0`; `CMissileHitResult` handler `0x00750EC0` มีจุดคู่กันที่ `0x007511E0` ไม่ได้เปลี่ยนค่า `n_OFFESIVE` ในตาราง
- [MEASURED][IMAGE] writer ที่พิสูจน์นี้ต้อง resolve target ได้, target `+0x10` มีบิต `0x10000`, identity ของ target **ติดลบจริง** (ไม่ใช่แค่ ≤0), และ source ผ่าน CMyActor cast. source qword ของ CHitResult อยู่ที่ vital `+0x18`; target qword อยู่ต้นแต่ละ entry ใน vector ที่ `+0x2C` ตาม `MWC-IMG-014`. Writer เป็น generic actor; ยังไม่มีการวัดว่า target ของเฟรมจริงเป็น CNetNPC ตัวที่ผู้เล่นมองอยู่
- [MEASURED][IMAGE] selector มีเงื่อนไขก่อน tail: identity อยู่สาย nonpositive, relation คืน false, death predicate ของ receiver คืน false และกิ่ง linked actor ใน NPCAttr ต้องไหลมาถึง tail. หลัง cast เป็น CNetNPC ได้จึงตรวจ `n_OFFESIVE`, แล้วบิต `0x100`
- [MEASURED][IMAGE] เมื่อเข้า tail นี้ด้วย `n_OFFESIVE=0`, ถ้าบิตตั้งแต่ local vslot `+0x3C` หรือ `+0x40` คืน true, selector ล้างบิตด้วย `AND ~0x100` ที่ `0x00444267` และ **ไม่ส่ง style ใหม่ในกิ่งนั้น**; อย่าอ้างว่ากลับส้มทันทีใน invocation เดียว รอบถัดไปที่เข้า clear-bit path จึงเลือก 62 ได้ ไม่ได้พิสูจน์ว่ามีตัวจับเวลาสำหรับบิตนี้
- [MEASURED][IMAGE] `NOT_WIRE`: บิต local `CNetNPC@0x70.4#R:b8` เป็นอินพุต selector; ไม่ใช่ฟิลด์ FontStyleID บนสาย ส่วน writer sites ใช้ target actor ที่ยังไม่ได้พิสูจน์ชนิด CNetNPC ณ จุดเขียน จึงไม่ตั้ง field_key แบบ CNetNPC ให้ writer

## ทำไมไม่ต้องสร้าง actor ใหม่ตามเส้นทางนี้

[MEASURED][IMAGE] registry tick อ่าน actor pointer แล้วเรียก updater `0x00444400` ที่ `0x004454F4`. Updater เก็บ receiver เดิมใน ESI และส่ง ECX=ESI เข้า selector ที่ `0x004446A7` เมื่อ actor `+0x254` และ controller `+0x10` ไม่เป็น null, squared xyz distance ไม่เกิน `10000^2` และ flags `+0x258/+0x260` ผ่าน (หน่วยระยะไม่ระบุว่าเป็นเมตร). ช่วงเกิน `5000^2` แต่ไม่เกิน `10000^2` ผ่าน helper แล้วมารวมทางก่อน selector; prerequisites เต็มอยู่ใน `PF_MONSTER_COLOR_GATE.md:108–115`. Selector ส่ง style ไป controller virtual slot `+0x34`; setter `0x009F1A70` เก็บค่าใน controller `+0x34`. NameBoardNPC update อ่านค่านี้ไปยัง **LABEL_NAME** ที่ controller `+0x50` ผ่าน UILabel style setter. นี่เป็น label ชื่อเหนือ actor ไม่ใช่ target panel หรือ HP bar

[INFERENCE][IMAGE] การประกอบเชิงเงื่อนไข: **ถ้า** hit writer และ tick อ้าง actor object เดียวกัน และกิ่งข้างต้นผ่าน การเปลี่ยนบิตทำให้รอบ update เลือก style ต่างได้โดยไม่เปลี่ยน template/identity หรือสร้าง entry ใหม่ ยังไม่ได้พิสูจน์ same-instance delivery ใน runtime

[MEASURED][DATA] DATA แยกจาก IMAGE: `GameClient/Data/GUI/Model/BigFontStyle.fsl` บรรทัด 62/63 ให้ style 61 FontColor `(255,100,100,255)` และ style 62 `(255,159,113,255)`; SHA `77798599c203d36e11282633d4a91ac098b0e1e03aa2482fede6fcfca161fc10`. คำว่าแดง/ส้มคือคำบรรยาย palette ไม่ใช่ผลภาพของรอบนี้ และไม่ได้พิสูจน์เฉด “แดงเข้ม” อีกหมายเลขหนึ่ง

## หลักฐานตรวจซ้ำ

[MEASURED][OUTPUT-AUDIT] อิมเมจขนาด 14,759,424 ไบต์ SHA-256 ก่อน/หลังตรงกัน:
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

ทุกช่วงเป็น `[start,end)`:

| หลักฐานเดิม | VA | File offset | SHA-256 |
|---|---|---|---|
| MCG-IMG-032/033 tail | 0044421C–0044427F | 0004361C–0004367F | 49b926d10639fdcba5e5c7a5d9e2df3905624fc8004fcb7f4d6a2a8ece4b134f |
| MCG-IMG-036 hit writer | 00750896–007508D7 | 0034FC96–0034FCD7 | f5542fcf64ed9b84d74a30f2688c3b4641bedbf553674455b3d20ad76e605cf4 |
| MCG-IMG-037 missile writer | 007511A6–007511E7 | 003505A6–003505E7 | ebf888481cf1d605f5d7819dd93f783b0b1d47b2401ae90fc25c728a7ff738da |
| actor update / selector | 00444400–004446E9 | 00043800–00043AE9 | 5e250c409a77ebf70e71cb6f83b9ee01cbc71b3ab355f34a8c22153a75074a5f |
| LABEL_NAME apply | 005BDA47–005BDA95 | 001BCE47–001BCE95 | f9e3b664c61f6350eae791d53192f3ba5df3bd3f627e0684696416865bc5a837 |

รายการครบพร้อม evidence_key, offset, span SHA และ input SHA อยู่ใน `staged/standing_a1_color_verify_20260908.log`; ไม่สร้างตาราง field ซ้ำ

[MEASURED][OUTPUT-AUDIT] verifier SHA `9d879e2665e290c30e61c8a4262305091787d99ce4efc671217d3e7ad6974e7c`; log SHA `9c408eca01caa5699fc5cc530d6250c70f2f46b02fddf46e9aa69b5f2eca7730`.

รันซ้ำบนเครื่องนี้ (ไม่ติดตั้งแพ็กเกจ):
```powershell
& 'C:\Users\Panya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\standing_a1_color_verify.py'
```
[MEASURED][OUTPUT-AUDIT] ผล: **11 reference rows, 41 unique spans, 17 instruction pins, 2 direct call edges ผ่าน**. แก้ไบต์เฉพาะในหน่วยความจำแล้วเรียก guard เดิม: 41 span traps + 17 instruction traps + whole-image trap ถูกปฏิเสธครบ. `py -3` ไม่มี Python ลงทะเบียนบนเครื่อง; ใช้ bundled Python stdlib โดยไม่ติดตั้งอะไร

## ค้นก่อนถอดและความขัดแย้งของคำสั่ง

[MEASURED][DOCUMENT-SEARCH] ค้นชุดส่งมอบแล้ว **เจอ**: `external/PF_PROTOCOL_REGISTRY.tsv:499–500` มี handlers ของ hit ทั้งสอง; `PF_SERIALIZER_FIELDS.tsv` มี layouts เดิม. ค้น `reference_codex_attr` พบคำตอบบิตใน `PF_MONSTER_COLOR_GATE.md:343–344,562` และ `PF_MONSTER_COLOR_WIRE_CONTROL.md` จึงตรวจ SHA/ไบต์แล้ว reuse

[MEASURED][DOCUMENT-SEARCH] ค้น gamedata แล้ว **เจอ**: `gamedata/PF_GAMEDATA_COLUMNS.tsv:326–327` แยก `AI_WANDER.n_OFFESIVE` กับ `n_AGGRO` เป็นคนละคอลัมน์; อ่านตาราง `CONSTDATA_TH__AI_WANDER.tsv` ภายใต้ SHA ที่ pin ไว้ ไม่ใช้ชื่อ n_AGGRO เป็นหลักฐานชื่อของบิต local. ค้น archive/consumed ด้วย VA, `red_latched`, `n_OFFESIVE` พบงานสีเดิมและคำขอของ B เช่น `archive/notes_to_chief_2026-09/CODEX_URGENT_20260901_0419_MONSTER-COLOR-IDENTITY-GATE.md`, `notes_to_chief/consumed/20260831_1740_CODEX-CHECKPOINT-P02-NAME-COLOR.md`. ผลนี้เป็น positive reuse ไม่ใช่คำประกาศว่าเส้นทางอื่นไม่มี

[MEASURED][DOCUMENT-SEARCH] คิว SHA ยังตรงรอบ 23:33; ไม่มี RE ที่เข้าเกณฑ์ runner หลังตัดผลเดิมและ assignment: 235/261 attended, 239 reserved, 321 assigned LANE-B. ลง SKIP ทุกใบและ NO-WORK ก่อนเริ่ม A1. ไม่ย้าย ORD, ไม่สร้าง branch/commit, ไม่แก้ lease: ใช้ runner v3/master v3 เหนือขั้นตอน ORD เก่า. ส่วนคำว่า M3 ปิดใน master กับ NOW/COO 1441 ที่ยังเปิดชั้น 3 ขัดกัน: รอบนี้ตอบเพียง A1 static และไม่เลื่อนสถานะ milestone หรือทับผล attended

[MEASURED][DOCUMENT-SEARCH] ค้นไฟล์ .md/.tsv/.py ด้วย `444238|444263|7508d0|7511e0|red_latched|n_OFFESIVE` แบบไม่แยกตัวใหญ่เล็ก: external 2,593 ไฟล์/1,341 บรรทัดที่พบ; gamedata 487/2; archive 2,355/53; consumed 1,994/42; reference_codex_attr 228/93. นี่เป็นขอบเขตการค้นครั้งนี้ ไม่ใช่จำนวนเส้นทาง executable. ตัวอย่างที่ตรวจย้อนกลับได้: `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md:2630`, `notes_to_chief/consumed/20260829_1912_RE-150-RESULT-NO-AGGRO-MONSTER-OUTSIDE-REFUSED.md:8`.

## ส่งต่อ

BUILD_IMPACT: [PROPOSED] เสนอให้ LANE-B ใช้กับ GT-224: ผู้เล่นควรเห็นมอนตัวเดิมเปลี่ยนสีหลัง hit ที่ผ่านเงื่อนไข โดยไม่ลบ/สร้าง actor เพื่อเปลี่ยนสีอย่างเดียว
BUILD_PROPOSED: [PROPOSED] ผูก hit target identity ให้ตรง actor เดิมและตรวจสี 62→61 พร้อมกิ่ง reset ใน GT-224 | LANE-B | A1_SAME_ACTOR_STYLE_62_TO_61 (proposed token; ยังไม่ measured)
[PROPOSED] ขอ LANE-K ผูกเลขย้อนหลัง; ผู้บริโภคผล LANE-B เปิดใบสร้าง/GT ตามกฎ RE→BUILD. เอกสารนี้ไม่เปิดใบเองและไม่แก้ server. ในผล follow-up ต้องแยก hit target/bit, การเข้า selector, style request และภาพ เพื่อแยก writer miss ออกจาก update gate

## nonclaims

- ไม่ได้วัดภาพ การโจมตี/aggro จริง การลด HP หรือ AI; ไม่เปิดเกม/เซิร์ฟเวอร์ ไม่แตะ DB
- ไม่อ้างว่า bit 0x100 จำเป็นต่อสีแดงทุกกรณี: n_OFFESIVE และกิ่งอื่นเลือก 61 ได้เอง; ไม่มี writer census ครบทุกทาง
- ไม่อ้างว่า hit ทุกเฟรมตั้งบิตได้ หรือ source/target ตรงกับ CNetNPC ที่เห็นใน runtime; ไม่อ้าง wire ordering หรือเวลาที่ label จะวาด
- ไม่อ้างว่าสีแดงระบุ aggro, target state หรือสูตรดาเมจ; ไม่เปลี่ยนชื่อ bit และไม่ยกผลนี้เป็น gameplay pass
- ไม่รื้อ A2–A6/B/C/D ในรอบนี้. รอบถัดไปอ่านคิวใหม่ก่อน; ถ้าว่างจึง A2


[MEASURED][DOCUMENT-REVIEW] pf-adversary: ตรวจร่างแล้วพบ 2 ข้อ (ป้ายชั้นหลักฐานและ updater gates), แก้ครบและตรวจแก้เฉพาะสองข้อนี้แล้ว ไม่พบข้อบกพร่องค้างใน corrections; ไม่ใช่ runtime audit.
[MEASURED][OPERATIONS] Published 2026-09-08T23:51:03.551430+07:00. ไม่มีเกม/เซิร์ฟเวอร์ที่รอบนี้เปิด; ไม่แก้ ServerProject, queue, lease, external, gamedata หรือ DB. Queue/orders SHA ก่อนปิดยังตรง. Source SHA ของอิมเมจและ 6 pinned inputs ผ่าน pre/post verifier. RE lock จะปล่อยหลังบันทึก memory.

SCOREBOARD: STATIC-PROVEN | มีเส้นทางเลือกสีใหม่บนมอนตัวเดิมภายใต้เงื่อนไขที่ระบุ; จอยังไม่วัด | MCG-IMG-032/033/036/037 + standing_a1_color_verify.py
