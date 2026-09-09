งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: chief / LANE-K; สายอุปกรณ์ LANE-DB ร่วม LANE-CS และ LANE-B
เวลาเริ่ม 2026-09-09T10:07:34.666574+07:00 · B1f · ปิด 2026-09-09T10:21:11.339747+07:00
PARTIAL / NEWPROGRESS: tagged codec body55bytes + factory + recipient scope; ไม่ใช่ runtime pass

[MEASURED][IMAGE A] type tag เป็นไบต์บนสาย
89A600→89A4D0 writes one tag byte at89A53B, increments length at89A53E, then89A62E copies size bytes. B37B80→IAT C3B504=MSVCR90.dll!memcpy: x86 raw fieldsเป็นlittle-endian. 89A640→89A550 checks tag89A5BF/advances1;89A6B1 copies payload/89A6B9 advances size. Wrong tag/truncationมีerror paths; Python testsไม่ใช่ผลรันเกม. 89A1B0เป็นstatus/position getter; caller5F3F44ไม่ใช้EAXตัดสิน จึงไม่ใช่หลักฐานlength fenceต่อvital

[MEASURED][IMAGE A] CBuffVitalเข้า nested factory อย่างไร
CGCBuffModule vtF36EF8.v28=64B050: alloc30→657610→5F3DF0. Registrar usesprototype.v10=657640/ID10842F8;5E3260/5F3BB0 inserts WORD-ID/prototype pair;duplicate key returnsfalse. 5F3E20→5E2E00→prototype.v14=657830→pool6576C0 createsvtF37438/version0 on fresh/reuse. พิสูจน์callback/factory code ไม่ใช่ยืนยันว่ารันแล้ว
- Decoder checks version tag0B/1 againstobject10 at5F3EFC, thenv18. Unknown factory/version mismatchเข้าE0000032/E0000031 error branches ไม่ใช่skip unknown
- 5F3840 calls v20 thenv1C;falsev20 aborts batch. CBuffVital/ItemOperateVitalRes v20=710440 returns true; v1C returnไม่ได้ใช้rollback
- RuntimeRes factory5E3EA0→5E3A10→5E3720 bothfresh/reuse; ctor setsversion4 at5E3763 and1C/20/24=null. Outer4ไม่ใช่nested0

[MEASURED layout / PROPOSED values] ตัวอย่าง RuntimeRes codec body
staged/standing_b1f_codec_body.py (body byte offsetsฐาน10):
body0: 0B02 = base mask มีnested container
body2: 120100 = nested count1
body5: 12E015 0B00 = CBuffVital nominal15E0/version0
body10: 32+targetQWORD; body19: 12+recordCountWORD1
body22: 14+BUFF DWORD38; body27: 14+STANDARD DWORD1
body32: 2A+elapsedFLOAT0; body37: 32+sourceQWORD
body46: 12+serialWORD; body49: 0B+stateBYTE0
body51: 0B+operationBYTE0(add) หรือ1(remove)
body53: 0B00 = derived mask ไม่มีactor collection/ส่วนอื่น
55bytes;ต่างกันที่byte52. Golden target0x0102030405060708/source0x1112131415161718/serial0x2233 เป็นเลขสังเคราะห์:
`0b0212010012e0150b00320807060504030201120100142600000014010000002a000000003218171615141312111233220b000b000b00`
ไม่มีouter opcode/version/length/compression/encryptionในตัวอย่างนี้; เป็น codec bodyให้ผูกกับ transport encoderที่พิสูจน์แล้ว ไม่ใช่ full frameพร้อมยิง

[MEASURED] ลำดับและขอบเขตผู้รับ
- Base5F4070 decodes nested before derived5E3EE0; handler5E4060 applies actor collection first (1Cnonnull→446F30 at5E4085) thennested5F39E0. Fresh object+derived mask0ข้ามcall446F30นี้; ไม่อ้างว่าhandlerไม่มีงานอื่น
- CBuffVital64AD40 resolves targetidentity via446170→actor248. Missingtargetข้าม. ItemReply5EF5E0 usesglobal app1093198+590→5A8A00 and+4E0→5C6D20, withoutCBuff-style actor-target argument; errorUIก็ใช้global app
- [PROPOSED D] bag/equip UI replyส่งเฉพาะsessionเจ้าของ; appearance/buffส่งตามidentityและข้อมูลที่ผู้รับต้องเห็น. Broadcast owner UI replyอาจกระทบUIผู้อื่น; original recipient policyยังไม่พิสูจน์
- ReuseB1c0938: AvatarAttr inactor collection→actor.v20→Attr.v38→v80→appearancecopy/dirty. 446F30 reconciles roster;single-target listอาจลบactorอื่น. Avatar.v24copieswhole object; preservationก่อนcopyยังไม่พิสูจน์. 309Aยังไม่ปิดworld appearance pathแทน

BUILD_PROPOSED: ใช้55-byte schemaต่อ B1-CBUFF-STR-DELTA-ROUNDTRIP ด้วยidentity/source/serialจริงในsessionที่เลือก; ตรวจ aggregateD4เพิ่ม5แล้วกลับเดิม, STR/ATKตามสูตร, field/รายการอื่นคงเดิม; ผูก bag/appearanceตามB1a–dเป็นคนละส่วนของผล | chief/สายอุปกรณ์ LANE-DB ร่วม LANE-CS และ LANE-B | token: FRAME_SHA+recipient+actorID+D4_before_add_remove+STR_ATK_before_after+unrelated_bags_in_two_sessions
GatesจากB1e1007ยังครบ: config/factory/actorพร้อม, BUFF38+STANDARD1, elapsed0,state0,group138ว่าง,bucketมีที่,serialไม่ชน; undoก่อนexpiry. ค่าบัฟนี้เป็นตัวพิสูจน์ช่องทาง ไม่ใช่ค่าstatของไอเท็มจริง. หยุดเมื่อgateไม่ครบหรือผลต่างจากคาด
เติมรูปแบบจดหมายB1e1007 (ของเดิมไม่แก้):
BUILD_PROPOSED: เพิ่ม–ลบCBuffVitalตามข้อเสนอB1eและรักษาค่าที่ไม่เกี่ยวข้อง | chief/สายอุปกรณ์ร่วม LANE-B | B1-CBUFF-STR-DELTA-ROUNDTRIP: exact frame+identity+D4และSTR/ATKก่อนเพิ่ม/หลังเพิ่ม/หลังลบ

ค้นห้าขอบเขตก่อนถอด: standing_b1f_search.log query Avatar.*Vital|Vital.*Avatar|Actor.*Vital|CBuffVital|UpdateActor|ActorAttrVital; matched FILES external42/gamedata0/reference41/archive41/consumed14. gamedata0ใช้เฉพาะqueryนี้ ไม่ใช่ไม่มีตารางBUFF. Reuse B1a/c/e manifestsด้วยhash; nominalIDไม่ใช่live value; ไม่สรุปglobal negativeจากregistry/rawxref
หลักฐาน staged/standing_b1f_manifest.json SHA cc05f788ec9b3f636ca695cf69857af46fa976f8284ef2d05659d4a7b25b329b:38 spans มีVA/file-offset/end/SHA,6 inputs. IMAGE14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623 ก่อน/หลังตรง
ตรวจซ้ำ Python314/python.exe -B pf_bridge/staged/standing_b1f_verify.py: PASS38 spans/32 code ranges/45calls/49pins/11vslots/9write widths/import memcpy/two55-byte goldens/80 scoped negatives. Template parserเท่านั้น; ไม่อ้างว่าเกมrejectแบบเดียวกัน. verifier/log SHAในcloseout.json
Adversary: a6f_review ตรวจfrozen diff ไม่พบmaterial defect; verifier exit0. ไม่ใช่transport/runtime audit.
nonclaims: no native/client/server/DB/Git/queue/reference mutation; no full transport frame, original equip/stat/recipient authority, pixels, persistence or reconnect proof. BLOCKER B1ที่เหลือ: original/full equip response evidenceและ appearance-preserving state/frame; ช่องทางstatตัวอย่างไม่ปิดความหมายไอเท็มแทน
NEXT: B2 rejection/drag restoration; เก็บB1 appearance/full-frame blockerไว้ชัดเจน
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
