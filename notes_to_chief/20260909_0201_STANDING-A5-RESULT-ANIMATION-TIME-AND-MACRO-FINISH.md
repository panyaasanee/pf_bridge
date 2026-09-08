งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, LANE-K, chief · จาก Codex static RE
เวลา: 2026-09-09T01:59:18.032643+07:00 · STANDING A5 · PARTIAL / NEW-PROGRESS

ปิดเพิ่ม: s_ANIMATION มีตัวแปลง delta/30 ไปถึง task+18; macro Start มีทางเรียก approach Finish แต่ยังไม่พิสูจน์ลูปโจมตีซ้ำ

IMAGE / A — เวลา action:
- 491832 อ่านชื่อ s_ANIMATION(F13D38) ใน BEHAVIOR(F0DA00); ถ้าคอลัมน์มีค่า 49187D→48F150 โดย this=behavior record. parser ข้าม null/empty และ record+28 bit80; ส่ง delimiter tab/space/semicolon และ newline ให้ matrix parser435C30
- เมื่อได้คู่ col0=name,col1=เลข: 48F227/23E→431910; 48F244 เรียก MSVCR90!_wtoi ผ่าน IAT C3B52C (ตรึง descriptor/INT/IAT/name). previous เริ่ม0; 48F248 ลบ previous จากเลขปัจจุบันแบบ32bit, แปลง signed delta เป็น float32→double, หาร double30.0(F0D210), แล้วกลับ float32. byte+20 ของ recordย่อย = (เลขปัจจุบัน==previous), ไม่ใช่ตรวจเลขเป็น0ทุกแถว
- 48F279→48CE60 บน behavior+84; vector begin/end อยู่ behavior+90/+94, record36ไบต์. ทางมี capacity:48CEC0→48A700→488D00 คัด scalar+0/string+4/bytes20,21. ทางขยาย capacity:48CEF1→48CA90→48B7F0→48AC10→48A700; 48B9AE/B1 เปลี่ยน end/begin เมื่อสำเร็จ. ไม่ครอบคลุม exception/tokenizer ทั้งหมด
- 48D3FA เรียก factory F0F798+18=47C750 ด้วย record+actor;47C7B6→471EB0. ผูก CActorTask_PlayActionEvent: ctor471EEE→F0EF28,get471F50→node102ECFC,regBD13F0→desc101CFB8. record+0 ถูกคัดไป task+18 ที่471F2D; bytes20/21ไป5C/5D
- ฐาน485D40→4A0750 ตั้ง flags0/time14=0; wrapper4A07B0 เมื่อ bit4ไม่ตั้งจึงใช้ task+18 เป็น threshold ของเวลาสะสม และส่งส่วนเวลาที่ถึงขอบไป virtual+C. ถ้า bit4ตั้งจะเดินอีก branch. ไม่สรุปหน่วย wall-clock จากชื่อ animation
- 48D3FF→487CE0 เลือก entry ID2 ผ่าน487B40 แล้วส่ง task เข้าคิว entry+8 ด้วย4A0C90. PlayActionEvent slots +8=475170,+C=475290,+10=475320. Start เรียก owner virtual+28; Tick เมื่อ5Dและ owner flags bit1เปลี่ยนจะสลับ stringแล้วเรียก virtual+28อีก. ไม่ตีตรา callback ว่า visual-only

DATA / A; การคำนวณตัวอย่างไม่ใช่ native execution:
- BEHAVIOR 280/282/284/286/288/290 มี s_ANIMATION `_C_ATTACK_000;30/17/28`, `_C_ATTACK_018;28`, `_C_ATTACK_000;24/24` ตามลำดับ; s_ANIMATION2ตรงกัน. ถ้าอ่านคู่ดังกล่าวเป็นแถวแรก ค่า task threshold float32 =1.0/0.5666666627/0.9333333373/0.9333333373/0.8000000119/0.8000000119
- ทั้ง6แถว s_PHASING/s_ROTATEว่าง, n_THENDO=self ID, n_MOB_CD=0. นี่ไม่ยืนยัน live equipment, cooldown, auto-repeat หรือว่า n_THENDOเป็น next attack. 

IMAGE / A — macro Start อาจจบงานเดิม:
- A5h ordinary behavior path47AD94→48D270เก็บ macroที่ UseBehavior+4C. UseBehavior Start47B077..7Fเรียก child+8; macro F0F778+8=4881C0
- เมื่อ behavior vector+C0..C4 มี record24ไบต์ให้เดิน 48D4B9 ตั้ง macro flags20000000 หลัง factory+1C/487C80. การตั้ง flagนี้ไม่ตรวจ child return ว่าไม่เป็นnull; ห้ามเพิ่มเงื่อนไข allocation-successเอง. ยังไม่ปิด field-writer censusของ vectorนี้
- MacroStart4881E1 ตรวจ flag20000000; ownerต้องมี. 4881F4เลือก owner+20 queue; ถ้า bytequeue+1D==1ข้าม. ไม่เท่ากับ1จึงเขียน1ก่อนอ่าน current+10 และ48820D→4A0860เมื่อcurrentมี
- ถ้า current เป็น A5c CActorTask_ActorAutoMoveToUseSkill(F0F548) และ finish guard bit10ยังไม่ตั้ง:4A0860ตั้งbits18ก่อนvirtual+10=475B80. เมื่อ owner/type/retained target/rangeผ่าน marker0ใช้selector48, marker1ใช้EA7D;475C21/31→44D260. targetที่ตรวจคือ retained50/54 แต่ producerคัด currentC8/CC ตาม A5c

D — สถานการณ์ที่ยังต้องพิสูจน์: inbound ActionVital ต้องหา performerตัวเดียวกับ ownerของ approachที่ยังcurrent; behaviorนั้นต้องสร้างและเริ่ม macroผ่านทุกgate รวม vector/flagข้างต้น; queueยังไม่พัก, guardยังไม่จบ, target/rangeผ่าน. คำตอบมาหลัง approachจบแล้วเป็น counterexample ที่ไม่ส่งเพิ่มด้วยทางนี้. ยังไม่มีหลักฐานว่าลำดับนี้เกิดได้จริง ต่อเนื่องเอง หรือทุกresponseทำซ้ำ; callback reentry/lifetimeยังเปิด

ค้นก่อนถอด: reference_codex_attr/PF_COMBAT_LIFECYCLE.tsv CL-DATA-001..008 มี equip→behavior/animation cohort เดิม; gamedata/tables/CONSTDATA_TH__BEHAVIOR.tsv ยืนยัน6แถวข้างต้น. external/PF_SERIALIZER_FIELDS.tsv:6547/6560 มี ActionVital+34 tag19 แต่ไม่ให้ความหมาย interval. หลักฐานใหม่: parser/task threshold และ Start→Finish

หลักฐาน: staged/standing_a5i_manifest.json เก็บ VA/file offset/span/SHA 34ใหม่+24reuse A5c/A5h และ6source SHA
image SHA: 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
manifest SHA: 2075997b0aee97c0ae8e553f46b3831b6a278a19add62d0e5baca19bc2346e47
verifier SHA: 06f7ebf08dbba0c5fcf4a67bd38e0a3d2fae9b5b192db5bb1d8a2c1e5dc8cfaf
log SHA: 7c9dda92311e1543719b91bb5f1bfe79be89e697df115173c3fc1db273d2c5b4
คำสั่งจาก pf_bridge: & 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B staged\standing_a5i_verify.py
[วัดแล้ว] PASS58spans,23calls,31pins,23call-mutants,8slots,1PlayActionEvent binding,1import,7arithmetic examples,6table rows,4empty/missing guards; source/imageก่อนหลังตรง. Staticเท่านั้น
ADVERSARY: P2 empty-proof fixed; no semantic defect found
BUILD_PROPOSED: แยก action duration ออกจาก request cadence และพิสูจน์ conditional Start→Finishด้วย owner/current/guard/target ordering | LANE-B | token=exact table-parser-task join + attained event ordering ก่อนเปลี่ยน cadence
nonclaims: ไม่มี original attack interval/seconds, autonomous repeat, live table selection หรือ server authorization. A5ยังPARTIAL
สภาพแท่น: ไม่เปิดเกม/server ไม่แตะ DB/ServerProject/lease/Git/คิว/reference; ไม่มี runtime HEAD/job/listener checkpoint. ปล่อย RE lockหลัง memory/log/source check
SCOREBOARD: NONE | Standing A5 animation threshold and conditional macro finish | IMAGE only; no runtime promotion
