งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: สายอุปกรณ์ GT-272, LANE-B, CORE, LANE-K, chief และ Panya · จาก Codex static RE
B1g · ปิด 2026-09-09T11:59:40.435396+07:00 · IMAGE A / composition D · PARTIAL: ปิดคำถาม partial AvatarAttr ก่อน CopyTo ของ B1c

คำตอบ: เปลี่ยนAvatarAttrเฉพาะมือขวา(mask400)ได้โดยเติมค่ามือซ้ายและฟิลด์รูปลักษณ์ที่ละจากAvatarAttrในRuntime collectionก่อนหน้า **เมื่อฐานidentity/kind/Attrตรงครบ**. ปิดช่องว่างใน B1c ที่ยังไม่เชื่อมv30ก่อนcopy. พิสูจน์ถึงค่าหลังfill/CopyToและdirty request; ไม่รับรองภาพสุดท้ายหรือไอเท็มอยู่ในbagแล้ว.

เชน:
1. ใช้D1a: Runtime5E406E→5DCB40 ก่อนactorreconcile5E4085. app154เก่า+incoming1Cnonnull→5E0270 จับidentity64และentrykindตรง→entry.v14=5DF850 จับAttrIDเดิม→incoming.v30. เป็นฐานpreviouscollection ไม่ใช่residentavatar34Cหรือcomparison350.
2. AvatarAttr vtF0E088.v30=464400 ตรวจsource type103345C,เรียกDB.fill467740 แล้วดูincoming mask28. mask400ที่4644AB/B0: ตั้ง→คงincoming54; ไม่ตั้ง→4644B5 copyold54. mask800ที่4644B8/BD: ไม่ตั้ง→4644C2 copyold58. ฟิลด์อื่นทำรูปเดียวกัน; mask28ไม่ได้ORเพิ่มตามค่าที่เติม.
3. ตรึง21selectorของฟังก์ชันนี้: 12DWORDที่2C..58 bits1..800; bytes5C/5D/5E bits1000/2000/4000; string64 bit8000; byte60 bit10000; DWORD80 bit20000; byte5F bit40000; byte84 bit80000; DWORD88 bit100000. ไม่มีการตั้งชื่อsemanticสากลจากoffset.
4. B1c typedbindเดิม: Avatar.v38=469850 ผ่านNetActor node102CB2C→actor.v80. NetActor459F50;MyActor449BC0เรียก459F50. ถ้า sourceมีค่าและ(actor39E!=0 หรือincoming mask28!=0)→source.v24=464150 CopyToresident34Cทั้งฟิลด์;มือ54/58คัดที่4641CD/1D3โดยไม่maskซ้ำ. จากนั้น459E90รับสองค่าและ459F8Aตั้งdirty250=1.
5. mask400/800เป็นnonzeroจึงผ่านmaskgateข้างต้นแม้ค่าไอเท็มเป็น0. **mask00ต่างออกไป:** แม้fillได้ทุกค่าแล้ว แต่actor39E=0ทำให้459F69ข้ามCopyTo/dirty. ถ้า39E!=0ยังapplyได้. MyActorUIหลังsuperยังเช็คsource.mask28!=0อีก; ไม่อ้างภาพUIจากdirtyอย่างเดียว.

WireจากB1cที่ใช้ต่อ: AvatarAttr nominalID16A0; DBAttribute mask20 tag0B/1 และidentity18 tag32/8เมื่อbit1. Avatar mask28 tag26/4;RH54 bit400/LH58 bit800 tag14/4. นี่เป็นบอดี้AttrในactorentryของRuntimeRes6E9D(v4ตามB1f),คนละอย่างกับslotภาพ0B/0Cและequipmentbag bits. ไม่แนบrawpayload.

Controlsเสนอ:
- fullAvatar seedของidentity/kindเดิม→mask400 RH=B: ณcopy RH=B,LH+ฟิลด์อื่นจากcachedseed;mask800 LH=Cรอบถัดไปต้องเก็บRH=B. คงfullactor key setและฐานAttrที่ต้องใช้ทุกตัว.
- mask400 RH=0 คือclearstorageอย่างชัดเจน ไม่ใช่omit; LHยังเติมจากฐาน. mask00+39E0ควรไม่ขอcopy/dirtyจาก459F50.
- omitwholeAvatarAttrหนึ่งรอบ หรือRuntimeactorcollectionnull → basisขาด. residentอาจยังดูปกติ แต่partialnonzeroถัดไปมีเพียงdecoded/defaultในฟิลด์ที่ไม่ได้รับ;ไม่มีfallbackจาก34C. ต้องreseedข้อมูลที่ต้องเก็บเมื่อไม่รู้cachehistory.
- ค่าที่rendererเปลี่ยนในresidentไม่ย้อนเข้าฐานwire: B1cพบชนิดอาวุธ n_EQUIPTYPE10 ที่78FC81..FCA3คัดRHลงcurrent58 และมีbranchล้างซ้าย. partialรอบถัดไปอาจนำcachedLHเดิมกลับมาที่copy ก่อนloaderจัดการอีกครั้ง. ดังนั้น “LHเก็บเดิมในfill” ไม่เท่ากับ “ภาพมือซ้ายไม่เปลี่ยน”. เริ่มcontrolด้วยชนิดที่ไม่เข้าทางนี้และtrace branchจริง.

field_key: AvatarAttr@0x54.4#R:b0x400 / @0x58.4#R:b0x800 (mask28), CNetActor@0x34C.4#R(resident pointer), CNetActor@0x250.1#W(dirty). PROVEN_EXACT storage/mask; nativeappearanceยังPARTIAL.
Search5domains staged/standing_b1g_search.log: external12/gamedata0/reference9/archive1/consumed0. B1cเคยตรึงfillแต่เปิดcallerไว้; รอบนี้ใช้D1aเชื่อม ไม่ทำcensusAttrทั่วไป/ไม่ทำสีชื่อM3ซ้ำ.
IMAGE SHA 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623; end-exclusive:
- Avatar.fill VA464400..46455C file63800 SHA68eebcfb2e725c8e7e0c9ffe5387b5c038439647e8a02c3618e07e2a5a961d4c
- NetActor.apply VA459F50..459F96 file59350 SHA4215507b25cd403f485cd0f6b9aeaefd781540b25a9f3a56b5ddc31ed03d0764
27spans/offsets/SHAครบ staged/standing_b1g_manifest.json SHA db1ad20bca3d5b09fff19169a3955bd8be7b8306e9fcf043cc42a244167e59fc
verifier SHA e55fb303409a518bf0241bfc37e5bc1112e5a8b1d954a5241cec49f66e658736; log SHA a746277052073b073bd6d44f229ab38a49e1c770b5d367e1138bf128fa9fc4f7
PASS27spans/23ranges/1286instructions/5sources/88calls/85pins/7slots/21selectors/21single-field+8mixed-mask/4apply-gate/4cache-resident controls; offline exit0.
Rerun: Python314/python.exe -B staged/standing_b1g_verify.py จากpf_bridge.
Frozen review /root/a6f_review: ไม่พบmaterial defect; verifierรันจริงexit0. ยังต้องเลือกRH/LH itemที่ไม่เข้าทางrewriteซ้ายสำหรับvisual control.
BUILD_IMPACT: partialAvatarบนRuntimeมีทางpreserveค่าอื่นก่อนcopy; ไม่ต้องตีความว่าจำเป็นต้องส่งทุกappearancefieldทุกครั้ง แต่ต้องมีcachebasis. ไม่ยก309Aเป็นcarrierเทียบเท่าและไม่เปลี่ยนoriginalpolicy.
BUILD_PROPOSED: fullseed→RH-only→LH-only→RH0 พร้อมcachebreak negative ต่อจากbagresultB1a/b | สายอุปกรณ์ + LANE-B + CORE | old/newcachematch, incomingfill/resident34C/comparison350/dirty250/loaderbranch ตรง พร้อมภาพslotสวมและมือก่อนหลัง; หยุดถ้าactorอื่นหายหรือรูปลักษณ์reset
nonclaims: nativepixels/stat/inventoryownership/ทุกderivedactor/weaponkindsemantic/originalreplypolicy/persistence/reconnect. ไม่แก้src/DB/lease/Git/คิว/reference; ไม่เปิดclient/server ไม่ใช้job9xx
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
