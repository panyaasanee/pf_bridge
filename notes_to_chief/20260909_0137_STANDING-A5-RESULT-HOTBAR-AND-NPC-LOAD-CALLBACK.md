งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, LANE-K, chief · จาก Codex static RE
เวลา: 2026-09-09T01:35:44.507230+07:00 · STANDING A5 · PARTIAL / NEW-PROGRESS

ผูก input→hotbar และ timer→NPCLoadStream ได้ ยังไม่ปิดวงจรโจมตีซ้ำ จึงยังเปลี่ยน server cadence ไม่ได้

IMAGE / A — ทาง input:
- ใน 450610 หลังด่าน key-entry ที่ A5f พิสูจน์ไว้: actor+3F8 ต้องไม่ว่าง (450AEA); 450AFB→5CFC10, 450B0B→5CFB60, 450B1B→5CFD10 ตามลำดับ แต่ละครั้งอ่าน normalized event+8 ใหม่ และไม่ใช้ค่าคืนของสาม call นี้
- 5CFB60 รับเลข 12..69: byte table 5CFBC8 มี 58 ช่อง; 12..23→page1, 24..35→page2, 36..47→page3, 48..59→page4 โดย index 0..11 →5CFBA4→5C3550. 60..69 คืน true โดยไม่เข้าการเรียกนี้; นอกช่วงคืน false. ตาราง pointer 5CFBB4 มี 5 ช่อง ตรวจตรงจากอิมเมจแล้ว เลขเหล่านี้ยังไม่ใช่ชื่อปุ่มจริง
- ต่อกับ A5f: 5C3550→5C2CB0 type4→SkillCommand→5BF160; ค่า entry+14=99 จึงเข้าผู้ผลิต EA7D แบบมีเงื่อนไข ยังไม่ได้พิสูจน์ว่าข้อมูล hotbar ที่ผู้เล่นใช้มีค่า 99
- ด่าน pressed-key ไม่ใช่ข้อพิสูจน์กัน repeat ทุกเส้นทาง: normalized scratch ใช้ร่วมและอาจเปลี่ยนระหว่าง callback; global+348/controller อาจรับ event ก่อน; UI route อื่นเข้า 5C3550 ได้ การตรวจ key เดิมจึงไม่รับประกันว่าเป็น key ที่ส่งต่อหลัง reentry และยังไม่ปิด release/focus-loss

IMAGE / A — callback ตามเวลา:
- StateRunTime ctor 4C87D1→vtable F170E4, getter4C8740→node107A6E4, registrationBDC4A0→descriptor1022FA0 ชื่อครบพร้อม NUL. slot+14=4C8E70; ctor ตั้ง timer+14 ด้วย float 0.1 ผ่าน 4C87F7→88EDD0
- frame เรียก general flush 4C8EAB→5DD970 ก่อนตรวจ timer 4C8EC7→88E860; เมื่อผ่านจึง 4C8ED2→4C8CA0. timer ใช้กลไกที่ A5e ผูกไว้; ไม่ใช่ข้อพิสูจน์ attack cooldown 100ms
- 4C8CA0 เดิน collection จาก 402A20()+C เลือก object ที่ byte+250 ไม่เป็นศูนย์ตามระยะกำลังสองจาก player. เก็บตัวที่ใกล้สุดทั่วไป และใกล้สุดที่ผ่าน type node102D954 (CNetNPC) แยกกัน; ใช้ CNetNPC ก่อน ถ้าไม่มีจึง fallback ตัวทั่วไป. ค่าตั้งต้น F17158 ประมาณ 1e38 ไม่ใช่ radius เกมที่พิสูจน์แล้ว
- จุดสำคัญของ stack: 4C8E4C อ่าน [esp+18] (NPC); หลัง pop สามครั้ง [esp+10] ที่ 4C8E57 คือช่องเดิม +1C ของตัวทั่วไป ไม่ใช่ distance float. ผู้ถูกเลือกถูกเรียก vslot+4C พร้อม argument1 ที่ 4C8E66
- เฉพาะ receiver ที่ใช้ vtable CNetNPC F0DF58: ctor45CC3A, getter45CD10→node102D954, registrationBCEEB0→descriptor101B138 ผูกชื่อครบ. slot+4C=441710, slot+60=45DAE0. 441710 ตรวจ byte+250 แล้วเรียก +60; 45DAE0 ตรวจ NPC+80, เรียก pool45C620 ที่ 45DB47; fresh/reuse 45C687/45C70B→45C220
- ctor45C258 ติด F0DF3C; getter45C280→node102CF1C; registrationBCD9D0→descriptor101A7C0 ผูกชื่อ NPCLoadStream ครบ. 45DAE0 คัดลอกสตริงจาก NPC+358→+7C ไป object+60. 441710 ผูก NPC เข้ากับ object+38 และคัด identity NPC+78/+7C ไป +40/+44 ก่อนเสนอให้ global+180 vslot+1C ด้วย argument1; ถ้ารับจึงนำเข้า collection NPC+318
- ยังไม่ปิด virtual manager, global+20 callback, fallback object/derived override และ NPCLoadStream slot+10→454780→78DE90. ชื่อชนิดไม่ได้พิสูจน์ว่าเป็น visual-only หรือไม่มีผลข้างเคียงสร้าง action

ค้นก่อนถอด: external/ พบ 45DAE0 ใน PF_ATTR_FIELD_SEMANTICS และสอง delta: NPCAttr@7C มีบทบาท resource basename เดิม จึง reuse เป็นบริบท ไม่ยกเป็นหลักฐาน cadence. gamedata/ ไม่พบ address ที่ค้น (4C8CA0,45DAE0,441710,450B0B); HOTKEY table ถูกตรึง SHA แต่ยังไม่มี physical-key crosswalk. reference_codex_attr/ พบสำเนาหลักฐาน 45DAE0 เดิม ไม่พบ join ใหม่ของ repeat

หลักฐานทำซ้ำ: staged/standing_a5g_manifest.json ระบุ VA, file offset, span และ SHA ของ 16 ช่วงใหม่+8 ช่วง A5f ที่ reuse; image ก่อน/หลังตรงกัน
image SHA: 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
manifest SHA: b8d76fb17badb4d7d911de90effe7b152c24b6fb7319b9bb0c630f46c4bbcfa9
verifier SHA: 51c96047cc33818e4dff152b89570d7c63a0645f93e019f6dfe453ff603ac94f
log SHA: f5f49b020b6ba4cd67ef3fd8d18c18290cdc380e2a0993cfa2fce43827356fff
คำสั่งจาก pf_bridge: & 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B staged\standing_a5g_verify.py
[วัดแล้ว] PASS 24 spans,16 calls,25 pins,16 mutants,3 named bindings,2 exact tables,4 empty/missing guards; source SHA 5 ไฟล์ก่อน/หลัง. เป็น static verification ไม่ใช่ runtime replay
ADVERSARY: ไม่พบ claim defect; ยืนยัน DE3→DEF ยังเข้า type check และ E23 ใช้ best-distance อีกช่อง ตรวจ branch pins เพิ่มแล้ว

BUILD_PROPOSED: ผูกทาง input/hold/release กับ EA7D และ response ก่อนเปลี่ยน provisional cadence; ใช้ผลนี้แยก callback ที่ระบุตัวตนแล้ว | LANE-B | token ต้องมี call path ถึงผู้ผลิต EA7D พร้อม start/stop และหลักฐาน release/reentry ไม่สร้างผลเกินขอบเขต
nonclaims: ยังไม่ปิด A5; ไม่มี click-once repeat, original rate, delivery/response conservation, physical key, live hotbar99 หรือผลบนจอ. ไม่ใช้ชื่อ NPCLoadStream ปิด transitive effects
สภาพแท่น: static เท่านั้น ไม่เปิด process เกม/เซิร์ฟเวอร์ ไม่แตะ DB/ServerProject/lease/Git/คิว; ไม่มี runtime HEAD/job/listener checkpoint; ปล่อย RE lock หลังตรวจ source/queue และบันทึก memory/log
SCOREBOARD: NONE | Standing A5 input-to-hotbar and typed periodic callback | IMAGE only; no runtime promotion
