งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, LANE-A, LANE-K, chief และ Panya · จาก Codex static RE
D1a · ปิด 2026-09-09T11:14:21.494609+07:00 · IMAGE A / ข้อเสนอ D · PARTIAL: ปิดทางเติมค่าก่อน apply; ยังไม่ปลด ActorAttr บน CNetNPC

**คำตอบ:** มี carrier ที่เติมฟิลด์ขาดก่อน CopyTo: RuntimeRes `0x6E9D` v4 bit02/collection+1C แต่เติมจาก **collection ของ RuntimeRes ก่อนหน้า** ที่ app+154 ไม่ใช่ resident actor. ต้องตรง identity64, entry+10 byte และชนิด Attr.

เชน IMAGE ที่ re-derive:
1. handler 5E4060 เรียก 5DCB40 ที่ 5E406E **ก่อน** reconcile 446F30 ที่ 5E4085. getter 5DC980 คืน incoming+1C. เมื่อ app+154 มีค่าและ incoming+1C มีค่า: 5DCBC1 เรียก 5E0270(incoming, &previous).
2. 5E0270 เดินเฉพาะ entries ใหม่ ค้น identity64 ในเก่าผ่าน 493880/623280. พบ key และ byte entry+10 เท่ากันที่ 5E034F..5E0355 จึงเรียก incoming.v14 ที่ 5E035F. vtable F2FE78+14 = 5DF850.
3. 5DF850 เดินเฉพาะ Attr ใหม่ ค้น Attr เก่าด้วย type ID ผ่าน 5DEFF0 (เทียบ WORD ที่ 5DF03C). พบแล้วเรียก **incoming Attr.v30(old Attr)** ที่ 5DF8C0. ActorAttr F0E7A0+30 = 465E60; เติมเฉพาะช่องที่ mask ใหม่ไม่ได้ส่ง.
4. ActorAttr.fill เรียก BasicAttr.fill 465610 ก่อน. BasicAttr mask+70 bit1 ขาด → คัดลอก name+28 เก่าที่ 46565B. ActorAttr mask+1B4 bit40 ขาด → CON+84 เก่าที่ 465F07; high DWORD+1B8 bit1 ขาด → byte+1A0 เก่าที่ 46615F. ถ้าบิตตั้ง เก็บ decoded/default incoming. ต่อจากนั้น 469760 ตรวจ type node102CB2C, ส่ง resident+348 ให้ incoming.v24=464F30 CopyTo.
5. app+154 ถูกแทนด้วย incoming+1C ที่ 5DCBFE..5DCC00 ทุกครั้ง แม้เป็น null. **RuntimeRes ที่ไม่ส่ง actor collection คั่นหนึ่งใบล้างฐาน merge**; ไม่ได้แปลว่า reconcile ถูกเรียกหรือลบ actor ในใบ null นั้น.

wire: entry+10 tag0B/u8; identity tag32/8; Attr count0B/u8; type12/u16; Attr.v34 body. ActorAttr+1A0 tag0B/u8 ที่466B73 ใต้ mask64 bit32. Envelope ใช้ B1c/B1f; ไม่ใช่ original frame
field_key: `BasicAttr@0x28.var#R:b0x1`, `ActorAttr@0x84.2#R:b0x40`, `ActorAttr@0x1A0.1#R:b0x100000000`

**ข้อจำกัด:**
- บิต CON40 ตั้งแต่ +1BC=0 → decoder4667E7 ข้ามอ่าน; fill ก็ข้าม → CON25 เก่าถูกทับด้วย0. ต้องตรวจ mask/group gate/cache ให้ตรงกันก่อนส่ง.
- 465610 เติม BasicAttr ตามบิตที่ขาด ไม่กลับขั้ว Actor mask (ขยาย RE-310 ภาคผนวก2).
- partial ใบแรก / key ใหม่ / entry byte เปลี่ยน / Attr เดิมไม่มี → ไม่มีฐานเติม. การมีตัวละครบนจอไม่เพียงพอ.
- ไม่ส่ง ActorAttr ทั้งก้อนใน entry ใหม่ → fill ไม่เพิ่ม Attr นั้นให้. แคชใบถัดไปจึงไม่มี ActorAttr แม้ resident ยังมี; ส่ง partial ActorAttr อีกครั้งอาจทับ name/CON ด้วย default.
- A(full) → A(partial1) → A(partial2) ติดกันยังรักษาค่าที่เติมแล้ว เพราะเก็บ incoming ที่ merge แล้วเป็นฐานใหม่. แต่ไม่รวมการแก้ resident ผ่าน carrier อื่นกลับเข้าแคช: ค่าในแคชอาจเก่ากว่า resident.
- reconcile actor collection ยังมีผลต่อ actor ที่ขาดจากรายชื่อ ตาม B1c; อย่าแปลฟิลด์ delta เป็นคำอนุญาตส่งรายชื่อเพียงคนเดียวในโลกหลายผู้เล่น.
- ActorAttr.bind ตรวจ node102CB2C; NPCAttr.bind 4697B0 ตรวจ102D954 และใช้ resident+358. registration BCE450/BCEEB0 ตั้งทั้งสอง node ให้ parent102CE88 ผ่าน88F2E0; เป็น sibling ในสายที่ตรวจนี้. **carrier นี้ไม่พิสูจน์ว่า ActorAttr ใช้แก้ฝ่ายบน CNetNPC ได้**. ต้องปิดตัวรับ NPC แยก.

ประวัติ: archive FROM_CHIEF_R120_TO_ATTENDED_20260821_1055.md:25–27 รู้ cache แล้ว. ใหม่คือ typed fill/gates. remote_player_hypothesis.py คำว่า NEVER ต้องจำกัด bind thunk; Q2 อ้าง cache ถูก. ไม่พบ runtime contradiction

ค้น5โดเมน FILES (external/gamedata/reference/archive/consumed): query456630|465E60|partial…ActorAttr =3/0/8/0/0; focused5DCB40|5E0270|5DF850|RuntimeRes…cache =0/0/0/3/0. queryเต็ม+paths: staged/standing_d1a_search*.log. linear event/v30 scan เป็น candidate ไม่ใช่ whole-program census

หลักฐาน image SHA 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623:
- Runtime.cache_update: VA 005DCB40..005DCCC9 (end-exclusive), file 001DBF40, SHA `fddae33904b60cdf2f79148cee9f9030617c2f8519e58bfd0527073ee3139d9c`
- ActorCollection.fill: VA 005E0270..005E038F (end-exclusive), file 001DF670, SHA `287383ea571e5356bc30929bae321016cc12bcaa131887ac317beccaa33daa31`
- ActorAttr.fill: VA 00465E60..0046622C (end-exclusive), file 00065260, SHA `ae42593007f32d954a25990b2599aaabcc040dd20a4c3c27e87cb18464ab0cb5`
ครบ 34 spans/end-exclusive/file offset/SHA : staged/standing_d1a_manifest.json SHA 81e51d188deb4cc8adc32060ba91d6cdf00ae2950e06953b3dd64c634f23b0be
verifier SHA 8f5f7180604e201061ef9d4c27ab9750fd35b6176a96f1dbe6470365f76630b5; verify.log SHA 541c12204ad5ee4cd634028bbead6181548834178af4314606296f3590bcbb33. PASS34 spans/31 ranges/2656 instructions/9 inputs/21 calls/113 pins/7 slots/8 field-mask cases/16 cache-gate cases/5 sequence/divergence/gate checks. offline reconstruction
Review a6f_review: P2 +1BC corrected; verifier rerun below.

BUILD_IMPACT: เปิดทาง sparse ActorAttr สำหรับผู้รับที่ผ่าน class gate ภายใต้การรักษาฐานก่อนหน้า; NPC faction ยัง PARTIAL
BUILD_PROPOSED: ตัวจัดลำดับ RuntimeRes ต่อ recipient ที่รักษา full actor key set และฐาน Attr พร้อม full fallback เมื่อแคชหาย | LANE-A/CORE + LANE-B review | full→partial→partial และ null/Attr-omission/other-carrier negative, ownerยืนยันชื่อ/HP/ค่าที่ตั้งและผู้เล่นอีกคนไม่หาย
nonclaims: ไม่อ้าง runtime/original policy/NPC ownership/ทุก mask/pixels/persistence. ไม่แก้ src/DB/lease/Git/คิว; ไม่รัน client/server; job9xxไม่ใช้
SCOREBOARD: NONE | Standing D IMAGE evidence | no runtime promotion
