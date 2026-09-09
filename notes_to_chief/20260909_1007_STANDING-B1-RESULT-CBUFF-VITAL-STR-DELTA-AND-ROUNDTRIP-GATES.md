งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
[ถึง: chief / LANE-K และสายอุปกรณ์ร่วม LANE-B · จาก: Codex RE runner]
เวลาเริ่ม 2026-09-09T09:53:06.920119+07:00 · B1e · ปิด 2026-09-09T10:07:27.501231+07:00
PARTIAL / NEWPROGRESS: CBuffVital→BUFF effect→aggregate STR; ยังไม่ปิด original equip policy

[MEASURED][IMAGE A] CBuffVital
- BF7000 ลงทะเบียนชื่อ ASCII F0B574; nominal ID15E0/getter657640→10842F8 (ไม่ใช่ live). ctor657610: vtF37438/version0; v18codec657390/v1Chandler64AD40
- codec READ: identity qword(this18) tag32/8; count WORD tag12/2; ต่อรายการ primaryID(record18) tag14/4, secondaryID(1C) tag14/4, float(20) tag2A/4, source qword(10) tag32/8, serial WORD(24) tag12/2, state byte(26) tag0B/1, operation byte(27) tag0B/1. call sites657467/477/4E1/4ED/4FC/508/517/526/535. นี่คือ typed payload contract ไม่ใช่ hex transport frame
- 64AD7D lookup actor ด้วย identity; actorไม่พบข้าม. actorพบ→actor248 CBuffAttr. operation=0 เรียก64E8B0บน CBuff+28; state26ถูกคัดลอกลง internal record80หลัง helperคืน. operationอื่นผ่าน652CC0: ถ้า primary+E0!=0 ข้าม; มิฉะนั้น64E4B0ลบตาม primaryID,secondaryID,source qword,serial ครบทุกตัว

[MEASURED][IMAGE A + DATA] ปิดทาง STR producer
1. 64E8B0สร้าง record: source→28/2C,primary→30,secondary→3C,float→40,serial→78. global10842A8: 4A1C70ค้น map+4 ได้ primary pointer18; 652CF0ค้น map+24 ได้ secondary pointer1C. secondary=0คืนnull; ค่าสูงกว่า manager44ถูก clamp ลงค่าสูงสุดที่ loaderเก็บ ไม่ใช่ยอมรับทุก ID
2. loader655A40อ่าน BUFF และ STACK. primary14=n_STACK; primary0C=n_BUFF_TYPE; primary10=f_DURATION. STACK lookupใช้ n_STACK: primary1C=n_POSITIVE,18=n_MAX_STACK,20=n_STACK_PROPERTIES. STANDARD_BUFF loaderเติม secondary14จาก n_STRENGH ที่655FFC
3. s_CONSTANT_BUFF(F280B8) ผ่าน655C97→653B90 ใส่ effect vector primary+BC. ADD_STRENGH(F27FEC) branch653DF9..653E5F สร้าง descriptor vtF36F7C และ float multiplierที่+10;655220 append. v0=64FEB0, v4=64FF10
4. 64E820เลือก bucketจาก primary1C; compiled capacities100/20/10 (ไม่อ้างค่า live). 64E550 appendแล้ว64D790: ต้องมี primary+secondary และไม่ติด record flag1. 64D7F8→64CCA0เรียก effect.v0 โดย aggregate=(CBuff+28)+98=CBuff+C0
5. 64FEB0อ่าน secondary14 คูณ descriptor10 ผ่าน float/double conversion แล้วปัดด้วย ±0.5 ก่อน trunc; บวก aggregate14 จึงตรง CBuff+D4. 64FF10ใช้สูตรเดียวกันแล้วลบ. Fight STR getter467A60อ่าน D4 ที่467AAD; การผูก LABEL_STR และสูตร/preview gates ใช้ผล B1d0952 พร้อม manifest SHA ที่ตรึงไว้

[MEASURED] ขอบเขตเพิ่ม/ลบและซ้ำ
- เมื่อจำนวนใน stack groupถึง max,64E550อาจเลือก existing: source/primary/secondary/stateตรงกัน→ปรับfloat40,reset48แล้วคืน existing โดยไม่บวก statซ้ำ; เส้นทางอื่นอาจแทนที่/ปฏิเสธ. เมื่อ bucketเกินcapacityจะลบหัวรายการ. ไม่อ้าง idempotencyทุกสถานะ
- Tick64D000 accumulates elapsed40 up to duration44;64D1FB..21F marks expiry,64E1C0 removes it.
- 64E4B0 matchห้าค่า→64E0D0→64D220→64CD30→effect.v4. serial=0ตอนเพิ่มให้ helperจัดเลขเอง; การลบต้องใช้เลขที่เก็บจริง. state26ถูกใส่หลังinsert จึงอย่าอนุมานว่า duplicate comparisonใช้state wireตั้งแต่ต้น

[MEASURED] ActorAttr partial-update counterexample
469760(v38)→incoming.v24(resident actor348) ที่46979B. 464F30(v24) copies WORD82/84 unconditionally;465E60(v30) fills missing fields (CON84/bit40 ที่465EFC..465F07). v38 bodyไม่เรียกfill. Counterexample: oldCON25,fresh STR-only incomingCON0,no prior fill→CON becomes0. event6Dก่อนหน้าอาจมีsubscriberทำfill; ไม่อ้าง global absence. ต้องพิสูจน์ caller pathก่อนใช้ partial ActorAttr

BUILD_IMPACT: BUILD_PROPOSED · owner=chief/สายอุปกรณ์ร่วม LANE-B · token=B1-CBUFF-STR-DELTA-ROUNDTRIP
[PROPOSED][D] ใช้ actor identityที่มีอยู่จริงและ CBuffAttr พร้อม, BUFF38 + STANDARD_BUFF1; DATA crosswalk:38→STACK138 (positive1,max1,policy1), constant ADD_STRENGH(1), duration300, other effect stringsว่าง; STANDARD1.n_STRENGH=5. จอง source/serialจริงให้ไม่ชนและยืนยัน group138ว่าง, bucketมีที่, configโหลดครบ. ส่งoperation0,state0,float20=0 (elapsed) จากนั้นoperation1ด้วยห้าค่าเดิม ก่อนหมดอายุ. คาด aggregateD4 +5 แล้วกลับเดิม; LABEL_STR +5 เฉพาะเมื่อสูตร multiplier/clampไม่เปลี่ยนผล. ตรวจ CON/DEX/PER/INT sourceและรายการอื่นคงเดิม; ยอมรับ ATKที่เพิ่มตามสูตร STR. หยุดเมื่อ gateไม่ครบหรือผลผิดคาด; เก็บ frame+before/afterให้ chiefตัดสิน
การรวม CBuffVital กับ ItemOperateVitalRes ใน RuntimeRes เป็นข้อเสนอประกอบจาก B1a/B1c; ต้องจัด version/order/rosterถูกต้อง. ไม่อ้างว่าต้นฉบับส่งบัฟนี้ตอนequip, ไม่ใช่ stat ของไอเท็มจริง และยังไม่มีเฟรมครบที่ยอมรับแล้ว

ค้นก่อนถอด: standing_b1e_search.log ครบ external/gamedata/reference/archive/consumed; queryแรก matched FILES25/0/20/3/3; supplement CBuffVital|ADD_STRENGH|s_CONSTANT_BUFF=10/4/9/0/0 FILES. rederive canonical claimsจาก IMAGE; no global negativeจาก raw xref/linear decode
หลักฐาน: staged/standing_b1e_manifest.json SHA cee33a99ac48184800afd07958ecb439a5ef64d92a336e8d29d892bad7472aaa;57 spans พร้อม VA/file-offset/end/SHA,10 input hashes,3 DATA tables. IMAGE14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623 ก่อน/หลังตรง
ตรวจซ้ำ: Python314/python.exe -B pf_bridge/staged/standing_b1e_verify.py → PASS57 spans/35 code ranges/40 calls/76 pins/9 vslots/9 typed reads; logและverifier SHAอยู่ closeout.json
Adversary: a6f_review พบ2 P2; แก้ elapsed=0/ATKแล้ว ตรวจ amendmentผ่าน, verifier exit0. ไม่มี runtime review.
ไม่มี native/server/client/runtime/DB/Git/queue/reference mutation. Wire consumer/static formulaเป็น A; proposalเป็น D; pixels, original equipment authority, persistence/reconnect และ frame integration ยังไม่พิสูจน์
NEXT: B1 envelope/recipient policy → B2 reject
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
