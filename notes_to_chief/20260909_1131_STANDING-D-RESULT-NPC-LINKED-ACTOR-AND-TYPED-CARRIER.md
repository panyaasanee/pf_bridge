งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, CORE, LANE-K, chief และ Panya · จาก Codex static RE
D1b · ปิด 2026-09-09T11:31:50.947225+07:00 · IMAGE A / composition D · PARTIAL: ขอบเขต ActorAttr กับ relation ผ่านตัวละครที่เชื่อมโยง

**ผลหลัก:** D1a เปิดเฟรม partial ActorAttr ได้ แต่ไม่ได้ทำให้ NPC รับ ActorAttr ได้. พบทางอ้อมที่ระบุผู้บริโภคได้: CGCVehicleModule ของ CNetNPC ใช้ NPCAttr+0xB0 เป็น identity64 ไปหาตัวละคร แล้ว query35 อาจทำให้ relation อ่าน Attr ของตัวละครนั้นแทน NPC. ไม่ตั้งowner enum

1. **ด่านชนิดสองชั้น**
- ActorAttr.v38=469760 ตรวจ actor node102CB2C แล้วคัดไป resident+348. NPC node102D954 เป็นอีกลูกของ102CE88 (D1a); ไม่ผ่านด่านนี้. NPCAttr.v38=4697B0 ตรวจ102D954แล้วคัดไป+358.
- CNetNPC ctor45CC00→45C9D0→465210 ติด NPCAttr vtF0E7E0 ลง+358. CNetNPC vtF0DF58.v74=45CD20 คืน+358; NetActor vtF0DD08.v74=44C630 คืน+348.
- 43C380 เรียก effective actor ทั้งสอง.v74 แล้ว43B9B0 cast ActorAttr node1033484. NPCAttr node1033478 กับ ActorAttr เป็นพี่น้องใต้Basic1033490; complete parent chain ลงถึงnullมีในmanifest.
- raw Attr ฝ่ายใดnull→AL1. แต่ **raw Attr มีค่าและ castฝ่ายใดล้ม→43C5C9** ใช้ BasicAttr+68 ของ raw Attr ที่เก็บไว้ ไม่อ่าน ActorAttr+98/+1A0. ส่ง ActorAttr ให้NPCใน collection จึงไม่ใช่หลักฐานว่าฟิลด์นั้นมีผล

2. **ทางอ้อมเกิดก่อน cast: query35**
43C3E9/43C42B→5F9F60 จาก actor+130 ทั้งสองข้าง. queryคืนtrue + event+6C มีตัวละครที่ผ่าน node102CE88 →เปลี่ยน effective actor ที่43C41E/43C460. ถ้าได้ตัวเดียวกันทั้งคู่→AL1ที่43C464 ก่อนอ่าน Attr. original other.CBuff+248/+A8 ยังมี early exit; app+D0 และ Attr-null gates ยังอยู่. ไม่ตั้งชื่อ booleanทั้งฟังก์ชันว่าเป็น enumสากล

**ผู้ตอบที่พบและปิดชนิด:** CGCVehicleModule node1087954 (RTTIผูกผ่านC02840), ctor6E1660 vtF409A8. v18=6E16C0 รับเฉพาะCNetNPCและเก็บhost+18; v34=6E15E0 ลงทะเบียน query35 ผ่าน5FAE30; v44=6E2BF0. 5F9F60 รวมtrueจากทุกlistener แต่ไม่ล้าง+6C; 43C380/nested queryใช้eventซ้ำ. ผู้ตอบอื่นอาจเขียนทับ หรือคืนtrueโดยใช้pointerเก่า. ผลนี้ต้องผูกกับlast writer. ข้อนี้มีเงื่อนไขว่า moduleถูกติดและลงทะเบียนแล้ว; ไม่อ้างว่า NPCทุกตัวมีmodule

6E2BF0 มีลำดับทางเลือก:
- module+1C มีค่า และ identity64 ที่ +18/+1C resolveได้ →เขียน event+6C แล้วคืนtrueที่6E2C45.
- special host node102E668 ผ่าน → ใช้ host+400/+404 เฉพาะด่าน6E2BC0คืน1; ด่านไม่ผ่านคืนfalse ไม่ไหลลงB0.
- hostทั่วไปมาถึง6E2CBB →อ่าน host+358 (=NPCAttr), **+B0/+B4**→446170. หาไม่พบคืนfalse. พบแล้ว query35 บนตัวที่เชื่อมโยงอีกครั้ง; nestedผลtrueและcast CActorผ่านจึงใช้ผลnested ไม่เช่นนั้นใช้ตัวที่resolveครั้งแรก. เขียน event+6C ที่6E2D06 และคืนtrue.
- ไม่อ้างว่า B0 ชนะทางเลือกก่อนหน้า หรือเกิดการเปลี่ยนสีจริง. วง self-link/cycle ต้องไม่ใช้เป็น control เพราะทางนี้มี recursive query

field_key: `NPCAttr@0xB0.8#R:b0x40`, `NPCAttr@0xB0.8#W:b0x40`; applies_to_class=CNetNPC ผ่าน CGCVehicleModule.host. NPC mask+BC แยกจาก Actor mask+1B4/+1B8. codec466EB0: read test40ที่467010, width8/tag32ที่467015/46701E, read467022. NPC copy:4653E7/4653F3. ไม่ใช่NPC camp

ตาราง D: early gatesผ่าน, moduleใช้งาน, คุมผู้ตอบและที่มาของevent+6C:
| target และผล query | relation ไปทางไหน |
|---|---|
| NPCไม่ส่งproxy; อีกฝ่ายActorAttr | Basic68 fallback |
| NPC B0 resolveไปอีก NetActor ที่มีActorAttr | ActorAttr gates ของตัวที่เชื่อมโยง |
| NPC B0 resolveกลับ local actorที่เป็นอีกฝ่าย | same-effective-actor→AL1; ไม่อ่านcamp |
| B0 resolveไปNPCที่ไม่มีproxyต่อ | Basic68 fallback |
| B0=0/หาไม่พบ และไม่มีทางเลือกก่อนหน้า | listenerนี้false; aggregatefalseเมื่อทุกlistenerfalseเท่านั้น |
Static only; M3 not reopened.

Prior RE-310/ARIG/QME-IMG-013 reused; new typed B0→query→Attr join. Search5domains in staged/standing_d1b_search.log; V141 frozen.

IMAGE SHA 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. spans end-exclusive:
- relation: VA 0043C380..0043C63C, file 0003B780, SHA `1d99f8557252742914c4f7358853aac06f0b54603f78a4b4d073aaea2afcbd89`
- vehicle.query: VA 006E2BF0..006E2D27, file 002E1FF0, SHA `b7264e57ad0c826277240cb4fbd9109f836daa578f6b02165e1bb6469a3d53cc`
47 spans: staged/standing_d1b_manifest.json SHA 510ebb82fc51e7ead60e0da38e1612533d0a34e8702eff22a0f9990e63364125
verifier SHA fb69fb98a93e5d8bf2d86f6a05138562dfc5068a50b7f1efe044302470147d33; log SHA e3eaa8033cf0a584231fa01f6c652c6cb2657c414e36771a89f81b2def125674
PASS47 spans/42 ranges/1397 instructions/6 sources/112 calls/118 pins/12 slots/7 type nodes/9 type pairs/3 early exits/9 query +5 freshness controls; offline exit0
Review P2 corrected: aggregate result != one listener result; freshness controls added. Offline rerun exit0.
BUILD_IMPACT: partial ActorAttr ต้องกำหนดชนิดผู้รับและeffective actor; B0เป็นทางlinked relationแบบมีเงื่อนไข ไม่ใช่ใส่campในNPC
BUILD_PROPOSED: ใช้ D1a กับNetActorและคงfull key set; หากทดสอบlinked relationให้ใช้NPCที่มีCGCVehicleModuleและB0ชี้actorที่มีจริง แยก0/missing/self/other | LANE-B + CORE | traceทุกlistener/last writer+6C/effective identity/v74type/branch พร้อมผลในเกม; ห้ามใช้วงcycle
nonclaims: ไม่ยืนยันoriginal policy/owner enum, moduleบนNPCทุกตัว, exact UIช่อง/สี, native relationผล, persistence/reconnect หรือยกเลิกM3. ไม่แก้server/src/DB/lease/Git/คิว ไม่ใช้job9xx ไม่เปิดnativeprocess
SCOREBOARD: NONE | Standing D IMAGE evidence | no runtime promotion
