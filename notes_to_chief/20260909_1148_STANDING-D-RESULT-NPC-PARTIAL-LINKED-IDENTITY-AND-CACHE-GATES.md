งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, CORE, LANE-A, LANE-K, chief และ Panya · จาก Codex static RE
D1d · ปิด 2026-09-09T11:48:14.570051+07:00 · IMAGE A / composition D · PARTIAL: partial NPCAttr linked actor B0 ถึง NPC เดิม

คำตอบใหม่: RuntimeRes actorcollection ส่ง NPCAttr ที่มีเฉพาะ derived bit0x40 เพื่อเปลี่ยน linked identity B0/B4 ได้ โดยชื่อ/templateที่ละจะเติมจาก NPCAttr ของ collectionก่อนหน้าเมื่อฐานตรงครบ. NPCที่มีอยู่ใช้ .v20=4446F0→5DF080→NPCAttr.v38=4697B0→incoming.v24=465340 copyค่าหลังfillลงresident358. ไม่ต้อง re-init modules. เป็นเส้น NPCAttr ของตนเอง ไม่ใช่ส่ง ActorAttr ให้NPC.

ใช้ของเดิม: RE-138 พิสูจน์ BasicAttr name omission fallbackแล้ว; D1aปิดRuntime cache-before-bindและexact identity/kind/Attr match. ไม่เสนอชื่อเดิมเป็นข้อค้นพบใหม่. D1b/D1cปิดtyped query35และmodule attachmentแบบมีเงื่อนไข.

หลักฐานเพิ่ม:
- NPCAttr vtF0E7E0: v30=466DC0,v24=465340,v34=466EB0,v38=4697B0. fillรับoldattr ตรวจNPCAttr node1033478ก่อน;466DF9→Basic.fill465610.
- incoming.maskBC bit40ที่466E85/87: มีbit→ไม่copyoldB0; ไม่มีbit→466E8F/466E9B copyoldB0/B4 ลงincoming. bit1ที่466E04/06ควบคุมtemplate78แยกต่างหาก; Basic.mask70 bit1ควบคุมname28.
- codec466EB0 เรียกBasic.codecก่อน แล้วอ่านderived maskBC tag0B/1. mask40→467015 width8,46701E tag32,467022 readB0. mask00ละB0; mask40+qword0คือเขียนศูนย์อย่างชัดเจน. ไม่มีActorAttr bit1<<32ในNPCAttrนี้.
- Runtime.handler5E406E→5DCB40: เติมจากapp154เก่าก่อน5E4085→446F30. new/old collectionnonnull,identity64ตรง,entry kindตรง,มีoldAttr IDเดียวกัน→incoming.v30; เก็บnewcollectionเป็นapp154เสมอ. รายละเอียด/offsetsอยู่manifestD1aที่ตรึงSHA.
- actorเดิม446F91lookup→446FB6/v20→446FBC; NPCvtF0DF78=4446F0 (ต่างจากNetActor.v20=456630). 4446FE bindattrs; 4697DFเลือกรับresident358แล้ว4697EBเรียกincoming.v24. CopyTo4653E7/4653F3เขียนทั้งB0/B4ไม่ตรวจmaskซ้ำ.
- 444703→4437C0และ44472A→NPC.v24=45D490เป็นงานหลังbind; ข้อสรุปนี้หยุดที่residentcopy ไม่อ้างผลvisualหรือsemantic refreshทุกทาง.
- query35 branchธรรมดาอ่านhost358สดที่6E2CBE→B0/B4ที่6E2CC4/CCA→resolve446170. ดังนั้นหลังcopy ค่าที่branchนี้อ่านเปลี่ยนได้โดยไม่สร้างmoduleใหม่. D1b priority/otherresponders/stale event6Cยังจำกัดผล aggregate.

ชุดควบคุมเสนอ (actoridentity/kind4/AttrIDเดิม,คงfull actor key set):
1. seed NPCAttrครบฐานและlinkedA; ส่งpartial bit40=linkedB → residentB0=B,ชื่อ/templateคงจากฐาน; queryใช้Bได้เมื่อD1b gatesผ่าน.
2. ต่อด้วยmask00 → เก็บB; ต่อด้วยmask40+0 → residentB0=0; mask00ถัดไปยัง0. ศูนย์พิสูจน์การclear storage ไม่พิสูจน์ว่าaggregatequeryfalse.
3. omitทั้งNPCAttrหนึ่งครั้ง: รอบนั้นbinderไม่แตะresidentNPCAttr แต่cacheรอบใหม่ไม่มีAttrนี้; partialรอบต่อไปเติมจากresidentแทนไม่ได้. ใช้เป็นnegative control.
4. Runtimeที่actorcollectionnullล้างapp154แม้ข้ามactorreconcile; partialถัดไปขาดฐาน. คนละเรื่องกับการละbitในNPCAttr. ส่งฐานที่ต้องเก็บครบใหม่เมื่อcacheไม่แน่นอน.
5. identity/kindไม่ตรงหรือoldAttrขาด→ไม่มีfill; ค่าที่decode/defaultจะถูกใช้ตามเส้นapply. การแก้residentด้วยcarrierอื่นไม่ทำให้cacheเดิมเปลี่ยนตาม.

field_key: NPCAttr@0xB0.8#R:b0x40 (mask@BC), NPCAttr@0x78.2#R:b0x01, BasicAttr@0x28.var#R:b0x01 (mask@70); per-class. linked actorไม่ใช่คำพิสูจน์universalowner.
Search5domains: staged/standing_d1d_search.log; external51lines/reference41/archive10/consumed7; corrected gamedata path pf_bridge/gamedata=0. พบ RE-138 และLT-IMG-006 typed lifecycleเดิม; ตัดงานnamefallbackซ้ำออก. PROCESS_GATESอ่านแล้ว.
IMAGE SHA 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. End-exclusive:
- NPC.fill VA00466DC0..00466EA7 file000661C0 SHA2c9f05ba5accac3a6b2743aed456a7754eca7d10b2382231c68019a782461c4e
- NPC.bind VA004697B0..004697F2 file00068BB0 SHAbe9bbd866c5eaebe5fed173106049710cd39abc9e4239e63a877087e433aba6a
30spans/offsets/SHAครบ staged/standing_d1d_manifest.json SHA 634bfd32e781451b08c47b4266b95a86db9a8c29b987f8b064a8e9cf64dec2a7
verifier SHA e428867fa06c08eb243420cb3039164a839c654ab31c23553b9e66d1a667c591; log SHA dfe4c3b68682da1861f72d620f946689720a0e301bb41f541965edccb88c4f0c
PASS30spans/27ranges/1361instructions/6sources/77calls/93pins/7slots/8mask/4basis-gates/7cache-sequences/6qword controls; offline exit0.
Frozen review /root/a6f_review: ไม่พบmaterial defectในstorage/query-read boundary; verifierรันจริงexit0. ยังต้องพิสูจน์ว่าA/B controlถึงordinaryB0 branch ไม่ถูกpriority responderแทน.
Rerun: Python314/python.exe -B staged/standing_d1d_verify.py จาก pf_bridge (Pythonที่ติดตั้งอยู่).
BUILD_IMPACT: partial linkedidentity มีtyped NPC carrier แต่ต้องรักษาpreviouscollection basis; ห้ามสลับกับ309AหรือwholeAttr omissionแล้วคาดว่าฟิลด์เก่าจะเติมเอง.
BUILD_PROPOSED: full seed→B0=A/B/omitted/explicit0 บนNPCเดิมพร้อมcache-break negative | LANE-B + CORE, LANE-Aคงroster | app154 old/new match, resident358 B0/name/template, moduleไม่re-init, query35lastwriter/effectiveactor traceตรง; ownerยืนยันผลในเกม
nonclaims: native/UI pass,สีชื่อM3,originalownership/policy,HPทั่วทั้งตัว,persistence/reconnect,globalcarrier census. ไม่แก้src/DB/lease/Git/คิว/reference; ไม่เปิดclient/server ไม่ใช้job9xx
SCOREBOARD: NONE | Standing D IMAGE evidence | no runtime promotion
