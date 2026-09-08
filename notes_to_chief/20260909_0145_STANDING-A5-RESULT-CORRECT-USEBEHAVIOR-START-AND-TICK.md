งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, LANE-K, chief · จาก Codex static RE
เวลา: 2026-09-09T01:42:45.657158+07:00 · STANDING A5 · PARTIAL / NEW-PROGRESS

แก้หลักฐานเดิม: 47AEE0 เป็น start; tickจริงคือ473650 ซึ่งเดิน child task ต่อได้ ยังไม่ปิด A5

IMAGE / A — แก้ role ของ CL-IMG-003/005:
- PF_COMBAT_LIFECYCLE.tsv สองแถวนี้อ้าง 47AEE0..47B2BF ว่า update; pf_rederive_attr_semantics.py:22611 ตรวจ F0EF18=47AEE0 จริง แต่ F0EF18 คือ vtable F0EF10+8. ไม่ใช่ช่อง +C ที่ใช้รับ dt
- ผูก CActorTask_UseBehavior ครบ: ctor47AB96→F0EF10, getter471DC0→node102ED50, registrationBD1230→descriptor101CEB8. ช่อง +8=47AEE0, +C=473650, +10=477510
- scheduler4A09C0 เลื่อน task เข้า current แล้วเรียก +8 ที่ 4A0A55/70/8E; wrapper4A07B0 ส่ง dt ให้ +C ที่ 4A07E7/83F; finish guard4A0860 เรียก +10. หลักฐานนี้แยก start/tick/finish จากผู้เรียก ไม่ได้เดาจากชื่อ
- handler ActionVital7516C0 มีทาง inline เมื่อ behavior+28 bit80: 75195E เรียก +8, 751971 เรียก +C ด้วย float0.1, 75197A เรียก +10 แล้วทำลาย task. 0.1 ใน branch นี้จึงไม่ใช่ interval การโจมตีที่พิสูจน์แล้ว
- ถอนเฉพาะการนำ CL-IMG-003/005 ไปอ้างว่าได้ตรวจ update แล้ว; ไม่ได้หักล้างการสร้าง task ใน CL-IMG-002 และไม่เปลี่ยน unknown ของ original cadence. ไม่แก้ไฟล์ reference เดิม; manifest ตรึง SHA ของตารางและสคริปต์เพื่อให้ตามแก้ที่ต้นทางได้

IMAGE / A — tick และงานย่อยที่ปิดเพิ่ม:
- handler ใช้ ActionVital+18/+1C หา performer ผ่าน446170; +30 เข้า702A10 แล้ว751809→47AB30. ctor เก็บ selector ที่ task+20; เริ่ม flags=8, +74=0,+75=2. เมื่อสร้าง child+4C ได้ 47AE88 จึงเปลี่ยน flags=40000005. ไม่ได้รับประกัน admission ทุก input
- 473650 ตรวจ owner/type และ virtual+3C/+40; ถ้าไม่ผ่านตั้ง task flags bit8. ถ้ามี child+4C ให้ส่ง dt ไป child virtual+C ที่4736B5; เมื่อ child flags bit8 จึงยก bit8 ขึ้น parent ที่4736C4
- เส้นทาง behavior ผ่าน47AD94→48D270 แล้วเก็บ child ที่ task+4C. 4162A0 คืน singleton102DAD8 ซึ่งสร้างผ่าน47BFC0. ผูก CMacroActionFactory_Client: F0F798/get47C020/node102EE90/regBD0C30/desc101CB1C; virtual+8=47C6E0
- 48D2FE เรียก factory+8; 47C728 สร้างฐาน487360 แล้ว47C72D ติด F0F778. ผูก CGCActorTask_MacroAction: getter47BFB0/node102EC3C/regBD17F0/desc101D270; virtual+C=487450
- 487450 แบ่ง dt เมื่อถึง timestamp ท้าย vector(+64..+68), ลด end ลง4ก่อน48752E→487170; ถ้า bit8ยังไม่ตั้ง ลบเวลาที่ใช้แล้วและวนจัดส่วนที่เหลือ. ทางไม่มี timestamp ที่ถึงแล้วเรียก487569→487170ด้วย dt ที่เหลือ. นี่เป็นการแบ่งเวลาใน macro หนึ่งตัว ไม่ใช่หลักฐานผลิตคำสั่งโจมตีใหม่
- 487170 เดินชุดที่ +2C..+30; แต่ละ entry ที่ current+18 ยังอยู่ จะเรียก4A0C60 บน queue+8. หลัง call ถ้า currentยังอยู่และ entry+28ไม่เป็นศูนย์ จึงถือว่ายังมีงาน; ถ้าไม่มี entry แบบนั้นตั้ง macro bit8. child queues/virtual callbacks ยังเปิด ไม่อ้าง complete no-repeat

IMAGE / A — ธงที่ไปถึง outbound ตำแหน่ง:
- 4736EF..F5 ตั้ง localplayer+3CC เมื่อ owner เป็น localplayer หรือ identityตรง localplayer+348→+140/+144 และ owner+10 bit20. finish4775AB..B1 มีทางตั้งธงเดียวกัน; นี่ไม่ใช่ census ผู้เขียนทั้งหมด
- general flush ที่ผ่าน timer/permitของ A5e เรียก5DDA5C→44BE50 แล้ว5DDA64→5DD800. 44BE50 ต้องมี byte3CC, actor+14 และ nested+8, และ actor+348→+9Bเป็นศูนย์ จึงสร้างผ่าน44B760
- pool fresh44B7C4/reuse44B842→5E5050; ctor5E506C→F30230, getter5E5090→node1081F48, regBEEC80→desc101F83C ชื่อ TargetPosVital ครบ. คัด position ไป +14..1C, scalar actor+14→+30 ไป+20, byteที่เลือกไป+24, byteactor+14→+4C ไป+25 ผ่าน setter ที่ตรวจแล้ว; ล้าง3CCที่44BF41ก่อนคืนให้ queue. จึงยังไม่มี delivery guarantee และไม่ใช้ธงนี้เป็นหลักฐานว่าเกิด EA7D ซ้ำ

ค้นก่อนถอด: external/PF_PROTOCOL_REGISTRY.tsv ยืนยัน ActionVital handler เดิม; reference_codex_attr/PF_COMBAT_LIFECYCLE.tsv มีคำตอบบางส่วนและ roleผิดข้างต้น. gamedata/ ไม่พบ7516C0/repeat join; ผลค้น3CCที่ offsetชนกันไม่ใช้ตั้ง semantics

หลักฐาน: staged/standing_a5h_manifest.json เก็บ VA/file offset/span/SHA ทุกช่วง:34ใหม่+9reuse A5c/A5e
image SHA: 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
manifest SHA: dfca8cd50004c4ababf07c4d14d3edfcaf47e59da9b6a5e28890dd1eb04bf5e9
verifier SHA: 4b8b9ea3c4cca3ae4f4d7c2bee3423c283cc52d9c8e67881d179636b7a2a9b89
log SHA: 0e092eae2ae7e4b745e7870245b0a8565ccd5f62c5b193ed5453d3490f46b388
คำสั่งจาก pf_bridge: & 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B staged\standing_a5h_verify.py
[วัดแล้ว] PASS43spans,24calls,35pins,24mutants,5typed bindings,6slots,2wrong-role traps,3empty/missing guards;6source SHAและimageก่อน/หลังตรง. Staticเท่านั้น
ADVERSARY: no claim defect found
BUILD_PROPOSED: แก้ role map ที่ใช้วิเคราะห์ cadence และตาม child queues ถึงผู้สร้างคำสั่งถัดไป | LANE-B/เจ้าของ reference | token=slot8/start,C/tick,10/finish ตรง caller พร้อมหลักฐาน start/stop ก่อนเปลี่ยน cadence
nonclaims: ไม่มี server-original interval, autonomous repeat, live animation/equipment หรือ physical-input policy; ห้ามสรุปว่า task retained = attack loop หรือ TargetPosVital = ActionVital. A5ยังPARTIAL
สภาพแท่น: ไม่เปิดเกม/เซิร์ฟเวอร์ ไม่แตะ DB/ServerProject/lease/Git/คิว/reference; ไม่มี runtime HEAD/job/listener checkpoint. ปล่อย RE lock หลัง memory/log และ source check
SCOREBOARD: NONE | Standing A5 correct UseBehavior slots and nested scheduling | IMAGE only; no runtime promotion
