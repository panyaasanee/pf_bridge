งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: chief, LANE-K, สายอุปกรณ์ GT-272; cc LANE-B

# B1 PARTIAL — AvatarAttr ถึงตัวละครและขอบเขตการโหลดของในมือ

เวลาเริ่ม 2026-09-09T09:16:38.986192+07:00 · B1c · ปิด 2026-09-09T09:38:32.461259+07:00
[MEASURED][IMAGE A] ปิดทางจาก actor collection ใน RuntimeRes ผ่าน AvatarAttr ไปถึง CNetActor/CMyActor แบบมีเงื่อนไข; bag/UIใช้ B1a–B1b; statยังเปิด

1. เฟรมภายนอก GSCN_RunTimeProtocolRes nominal ID **0x6E9D** รองรับทั้ง nested Vital ที่ +18 และ actor collection ที่ +1C: base codec 5F4070 เลือก nested ด้วย mask0x02; derived codec 5E3EE0 เลือก collection ด้วย maskอีกตัว0x02 ดังนั้น “คนละส่วนข้อมูล” ไม่ได้บังคับว่าเป็นคนละแพ็กเก็ต [PROPOSED D] รวม ItemOperateVitalRes+actor collectionใน envelopeเดียวได้เมื่อfactory/version/dispatchผ่าน; original policyยังไม่วัด
2. ลำดับ handler เดียวกันชัดเจน: **5E4085→446F30 actor reconcile ก่อน 5E40DE→5F39E0 nested dispatch**; 5F3840 เรียก nested.v20 ให้ผ่านก่อน nested.v1C (ItemOperateVitalRes v1C=5EF5E0 ตาม B1a) ไม่รับรองว่าโมเดลโหลดเสร็จก่อนUI
3. collection reader 5E1AD0 อ่าน count tag12/2 แล้วสร้าง entry (pool445370→ctor5E1200/vtableF2FE78) และอ่าน entry.v18=5E21D0: byte+10 tag0B/1, actor qword+18 tag32/8, Attr count tag0B/1, แต่ละตัว type key tag12/2→factory463CF0/5E2E00→Attr.v34→entry vector30..34; ไม่มี declared payload lengthแบบ UpdateAttrVitalในลำดับนี้
4. identityที่พบใน actor map ไป actor.v20; CNetActor/CMyActor ใช้456630→4446F0→5DF080 ซึ่งเรียกแต่ละ Attr.v38(target actor). AvatarAttr v38=469850 ตรวจ type node102CB2C แล้วเรียก actor.v80; CNetActor=459F50, CMyActor=449BC0→459F50. ctor457340 สร้าง AvatarAttrที่ actor+34C ผ่าน456C00→464080
5. 459F50 ต้องมี source และ (actor+39Eไม่เป็น0 หรือ AvatarAttr+28ไม่เป็น0) จึงเรียก source.v24 ไปยัง actor+34C, ส่งมือขวา/ซ้ายให้459E90 และตั้ง actor byte250=1. เมื่อ441710ถูกเรียกและdirtyนี้เป็น1 จะขอ actor.v60=45A1C0; ยังมี query/pool/resource gatesก่อนส่งstream
6. 45A1C0 ส่ง actor+34C เป็น current appearance และ +350 เป็น comparison appearance ให้78EBF0. ทางมือขวาอ่าน current+54 (78F9D8), เรียก78BF60ด้วย slot0B, สร้าง record +9C=0B / string weapon-nod01 ใน branchปกติ แล้ว78FC7C→78E540เพิ่มรายการเข้า stream. มือซ้ายอ่าน current+58 (78FCCF), slot0C / weapon-nod02 แล้ว78FE7B→78E540. 0B/0Cเป็นช่องโหลดภาพ ไม่ใช่equipment slot
7. ชนิดอาวุธมีผลใน loader: อ่าน n_EQUIPTYPE; currentขวาชนิด0x10 ทำให้ branch78FC81..FCA3 คัดค่าขวาลง current+58 ถ้าต่าง และเรียก v1C(1); ยังมี branchล้างซ้ายผ่าน4277F0. ไม่สรุปว่าfieldมืออิสระหรือ0x10ชื่อประเภทใด

[MEASURED][IMAGE A] AvatarAttr nominal type ID **0x16A0**; +28 mask tag26/4; +54 อยู่bit400, +58อยู่bit800 ทั้งคู่tag14/4. ก่อนหน้านั้นมี DBAttribute maskbyte+20 tag0B/1 และ qword+18 tag32/8 เมื่อbit1ตั้ง. IDจาก89B220 weighted name; 89BD00คืน0ถ้าลงทะเบียนล้มเหลว ไม่ใช่live ID

**ขอบเขต partial update:** 464150/v24 คัดลอกฟิลด์รูปลักษณ์ทั้งหมดหลัง type gateโดยไม่กรองแต่ละฟิลด์ด้วยmask. 464400/v30 เป็นอีกฟังก์ชันที่เติมฟิลด์ซึ่งmaskไม่ตั้งจากค่าเก่า แต่การมี v30 ไม่ได้พิสูจน์ว่าถูกเรียกก่อนcopyในเส้นตอบนี้ จึงยังรับรองส่งเพียง+54แล้วรักษาหน้าตาเดิมไม่ได้; ไม่ใช่global no-merge

[MEASURED] UpdateAttrVital0x309A/5F2400 คัดลอก incoming.v24 ลง component attribute แล้วส่ง event7 ผ่าน5F9C70→subscriber.v40. ยังไม่ได้เชื่อม subscriberเส้นนั้นกับการตั้งdirty250 จึงไม่เสนอว่า0x309Aแทน actor collection ได้

BUILD_PROPOSED: ต่อผล GT-272 โดยผูก bag resultตามB1a/B1b กับ AvatarAttrใน actor collectionของidentityเดิม รักษารูปลักษณ์เดิมครบก่อนเปลี่ยนอาวุธ และแยกหลักฐาน UI/มือบนตัว/ค่าพลัง | สายอุปกรณ์ร่วม chief/LANE-B | token: FRAME_SHA+actor identity+ภาพช่องสวม/มือขวาซ้ายก่อนหลัง+รูปลักษณ์ส่วนอื่นคงอยู่; หยุดเมื่อ actorอื่นหาย/หน้าตาถูกreset/loaderไม่ผ่าน; tokenยังไม่มี

[PROPOSED D] คง rosterเมื่อreconcileตามA3 omission/erase. B1dตามstatต่อ; original reply policyยังPARTIAL

ค้นก่อนถอด: standing_b1c_search.log (MD/PY, equip appearance/model/คำไทย): external18/gamedata0/reference19/archive7/consumed2 ไฟล์ตรงคำค้น ไม่ใช่global negative. semanticsเดิมใช้57BB80 fitting-room/4BEF20 create-character UI; รอบนี้ใช้ world chainข้างต้น

หลักฐาน: GameClient.local.bin 14,759,424ไบต์ SHAก่อน=หลัง
9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
VA/file-offset/ช่วง/hashครบใน staged/standing_b1c_manifest.json:
6fecbba31f9454305dfb4f9adb9a99c3f2f5b6f267d03c57d57a79fb02e8e3e8
VAครึ่งเปิด: 5E21D0..5E2433, 459F50..459F96, 78EBF0..790766. manifest8แหล่งรวมB1a/b. Re-run Python314 -B staged/standing_b1c_verify.py: PASS67 spans/49decode/40calls/77operands/16vslots/11strings/3IDs; ตรวจbytes ไม่รันnative

ADVERSARY: /root/a6f_review ตรวจ frozenชุดนี้และรันซ้ำexit0; ไม่พบข้อผิดพลาดสาระสำคัญ. enrollment/callback/factory/original policyและการรักษารูปลักษณ์ในเกมยังไม่พิสูจน์
NONCLAIMS: ไม่มี native/pixels/stat/persistence/full weapon types/original ordering; ไม่ใช่slot=200+N. ไม่บูตเกม/server/DB/Git/ServerProject/queue edit. Runtimeไม่ได้สำรวจใหม่
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
