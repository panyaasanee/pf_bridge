งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B, CORE, LANE-K, chief และ Panya · จาก Codex static RE
D1c · ปิด 2026-09-09T11:43:25.955272+07:00 · IMAGE A / composition D · PARTIAL: ขั้นติด query35 ให้ CNetNPC ตามทางสร้างปกติ

คำตอบต่อ D1b: CNetNPC ปกติเลือก CGCVehicleModule ด้วย module mask4 แล้วเพิ่ม listener query35 ก่อน apply Attr จากบอดี้. เงื่อนไข: prototype/query registration พร้อม, allocation/lookup สำเร็จ และ host เป็น NPC จริง. ไม่ใช่ผลที่วัดจากเกม

เชนสร้างถึงติดผู้ตอบ:
1. Runtime actorcollection446F30 หาidentityไม่พบ→446FA3→446990. entry+10 เป็นkind; table446B2Cเลือก kind4→446A3D→444F00(CNetNPC allocator), มี manager+6D gate.
2. NPC ctor45CC00 ตั้ง +230=4,+234=1. vtF0DF58.v10=45D200 รับentryจาก446AB5. ถ้าentrynonnull 45D237เรียก.v2C=43B7F0 ก่อน45D24A→5DF080 apply Attr.
3. 43B7F0 ส่ง(module mask4, attribute mask1,host)→5FBA00: 5FB910เติมdefault Attr→5FA680ติดmodules→5FB5D0เพิ่มlisteners. maskสองตัวมีคนละหน้าที่ ไม่ใช่faction enum.
4. 41872D→6E1660สร้างprototype(module10=4),418742→5FB800ลงregistry; เรียก.v20 registerdefault Attr และ.v34=6E15E0 register query35. ยังไม่ใช่การผูกกับNPCตัวหนึ่ง.
5. 5FA680 เลือก `(prototype+10 & module mask)!=0`; มีmodule IDแล้วข้ามclone. มิฉะนั้น.v14=6E2640→6E2320(pool): fresh/reusedตั้งvtF409A8,mask4 แล้ว.v18=6E16C0(host).
6. bindตรวจ CNetNPC node102D954 เก็บhostที่module18; lookup CVehicleAttr จากhost+130 เก็บmodule1Cเมื่อtypeผ่าน. หาAttrไม่พบก็คืนtrue6E1746. hostผิดชนิด→false→5FA71D..26ทำลายclone; ผ่าน→5FA72F→5FA470ลงcomponent.
7. 5FB5D0 เดินmodules ใช้ชื่อชนิดค้น registry+20(query kinds). 5FB782→5FA950(kind,module) เลือกcomponent+A0 ค้น/สร้างvector แล้ว5FAA1E→64F2D0เพิ่มpointer. ตรงกับ5F9F60ที่อ่าน+A0และเรียกlistener.v44=6E2BF0ในD1b.

default CVehicleAttr ctor6E2D60: eligibility10=1, identity18/1C=0. v14=6E3420→6E3350 pool เรียกctorทั้งfresh6E3388/reused6E33EE; ไม่อ้างว่าคง0หลังapplyบอดี้.

แก้ QME-IMG-016 เฉพาะข้อพิสูจน์ได้: PF_QUEST_MARK_EVENT_CENSUS.tsv เรียก5FB5D0ว่าMODULE_REMOVE_BOUNDARY/UNREGISTER_LISTENER_FROM_BOTH_CHANNELS แต่เส้นนี้เพิ่มสมาชิก: fast path64F2FEเขียนที่end,64F300เพิ่ม4,64F303เก็บend. QME-IMG-013 query35 controlไม่ถูกล้ม; ไม่แก้referenceเดิม ไม่อ้างว่าพิสูจน์teardown.

Adversary พบ P2: verifierเดิมจำลองempty vectorที่มีcapacity3 จึงไม่ครอบคลุมNPCใหม่. แก้โดยตรึงctor B13AE0 (B13B1C/1F/22 ตั้งbegin/end/capacity=0), insert64F328→5F68D0→5F66D0(count1), allocation5F674D→7026A0, fill5F676E→64CFD0(store64CFE9), copy75CFA0บนempty ranges, และ stores5F67C1(begin)/C7(capacity)/CA(end). เมื่อallocationสำเร็จ end=begin+4. เพิ่มzero-capacity/growth/pointer controlsแล้วผ่าน. Allocation failureไม่ได้พิสูจน์เป็นsafe return.

ขอบเขต:
- mask4อย่างเดียวไม่พอ: NetActorยังไม่ผ่านtypedNPC bind. ไม่ขยายถ้อยคำกว้างใน RE-085 ไปplayer actor.
- existing moduleข้ามclone แต่hookยังappendซ้ำได้ ทั้งfast/growth; re-initไม่ใช่idempotent proof. ไม่กล่าวว่าruntimeปกติเรียกซ้ำแล้ว.
- query35รวมหลายlistener ใช้eventเดิม(D1b P2). moduleมีอยู่ไม่พิสูจน์B0เป็นlast writer; ต้องดูaggregate/lastwriter/effectiveactor.
- ลำดับglobal registrationเสร็จก่อนfresh-spawn controlยังเป็นprecondition ต้องตรวจในtrace.

field_key: CNetNPC@0x230.4#R(module mask), CNetNPC@0x234.1#R(Attr mask), CGCVehicleModule@0x10.4#R(eligibility). NPCAttrB0 semantics: D1b.
Search5domains: staged/standing_d1c_search.log; external6/gamedata0/reference6/archive17/consumed2. RE-085 prior binder; PROCESS_GATES read.
IMAGE SHA 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623; spans end-exclusive:
- attach_modules VA005FA680..005FA74D file001F9A80 SHA9801fa46b0d3d0668c70924777b8d80ed10dd89f7d4f245bf5d1db1cc8cb1ec2
- grow_insert VA005F66D0..005F6878 file001F5AD0 SHA9ddf7cba54fa7645ed4b63c6a5d742beb42e2e268b1d0293239cf913af3c116e
40spans/offsets/SHAครบ staged/standing_d1c_manifest.json SHA 841db026536247b568002ea9aad3701cdec3abc07dc83370d727fb04802b4860
verifier SHA cb89c65e95ae863f8a061cc1fbfff5b0b0dc7347763583dad688e8a34384bae9; log SHA 6ca9606f87fc6919a3ef4ce1a0e78b62753fd89eaf68b147bb3b397080fe7504
PASS40spans/36ranges/2129instructions/6sources/137calls/125pins/10slots/5kindtargets/16mask-type/4attach/5fast-append/4growth-pointer/3init/1prior-row contradiction; offline exit0.
Frozen review: /root/a6f_review; P2 corrected above; mask/order/type/append findings survived. Static only.
BUILD_IMPACT: ใช้normalNPC create pathเตรียมquery35; ตรวจlinked actorก่อนพยายามแก้campผ่านActorAttr. ถอนข้ออ้างQME016 unregister.
BUILD_PROPOSED: แยกdirectNetActor partial(D1a)กับNPC linked relation(D1b); ตรวจprototype/query registrationพร้อม แล้วfresh spawn NPC และส่งB0ชี้actorที่มีอยู่ คงfull key set | LANE-B + CORE | registry/moduleid/hostclass/query35listener/lastwriter+6C/effective identity+Attrtype ตรงในtrace และownerยืนยันผลในเกม; ไม่ใช้re-init/cycles
nonclaims: native pass/teardown/idempotency/ทุกderivedclass/original policy/UIสี/persistence/reconnect. ไม่แก้src/DB/lease/Git/คิว/reference; ไม่เปิดclient/server ไม่ใช้job9xx
SCOREBOARD: NONE | Standing D IMAGE evidence | no runtime promotion
