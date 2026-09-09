งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: สายอุปกรณ์ GT-272, CORE, LANE-B, LANE-K, chief และ Panya · จาก Codex static RE
B1h · ปิด 2026-09-09T12:15:33.766149+07:00 · IMAGE A / DATA A / composition D · PARTIAL: ตัวอย่างมือขวา/ซ้ายสำหรับ B1g

คำตอบ: เลือก RH 2200201→2200203 และ LH 2200601→2200603 ได้จากตารางต้นฉบับ พร้อมพิสูจน์กุญแจโมเดลที่ตัวโหลดประกอบและพบไฟล์ชื่อตรงกัน. ทั้งค่า RH เก่าและใหม่มี equiptype1 จึงไม่เข้าสองสาขาที่เขียน/ล้าง LH เพราะtype10. นี่เป็น fixture เสนอ ยังไม่ใช่ native pass.

หลักฐานใหม่ที่ทำให้รหัสเต็มไม่ต้องพึ่ง matrix ของ RE-060:
- แตก B_CONSTDATA_TH.pc_ แบบ LZMA ในหน่วยความจำ: raw SHA496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8; decoded8443000bytes SHA496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d.
- ตาราง EQUIPMENT_BASE ช่วง decoded[500F38,546BC6): หลังชื่อที่500F58เป็น16000000 =22; ตามด้วยversion5และlinked name EQUIPMENT_BASE_TIP. ไม่ใช่ลำดับตาราง037. parserเดิมเรียกฟิลด์นี้ serialized_size แต่ consumerพิสูจน์ว่าใช้เป็นกุญแจตาราง; ไม่แก้ไฟล์ parserเดิม.
- 893860 อ่านชื่อ→table10 ที่893893,อ่านDWORD→table2C ที่893898/89E,ถัดไปversion30. 899C40 อ่าน4bytes. 893960 ตรวจชื่อ/กุญแจซ้ำ; ถ้ารับลงทะเบียน อ่านtable2Cที่893A3E→manager48 map-slot8927A0→assignAC5BB0(เขียนptrAC5BC9). 8941C0 เรียกread893860ก่อนregister893960; caller4095DA/DF ใช้manager108CDD0เดียวกับมือ.
- 892DD0→892610: fullID>100000 ใช้magic14F8B589 quotient /100000→890FC0 ค้นmanager48; remainder→890E70 ค้นtable70. ตัวลงrow893770อ่านDWORDแรกของrowbufferเป็นkey; EQUIPMENT_BASE columnแรก n_ID/type0/size4/offset0. ดังนั้นเมื่อชุดนี้ลงทะเบียนสำเร็จ 2200201→table22,row201. ไม่อ้าง runtime tree ที่ยังไม่ได้วัดหรือ tableที่ลงทะเบียนซ้ำแล้วถูกปฏิเสธ.

เส้นทางสร้างชื่อ 78BF60..78C24C:
- itemlookup892DD0 ต้องสำเร็จ;อ่าน s_ID_MODEL_PARTS,n_ID_MODEL,n_ID_MAP,n_TAG_LOOT ผ่าน891F80/891EE0. ขาดpropertyใด→78C219คืนว่าง.
- tag64→prefixW; else256→V; else128→D. slot0B→R,0C→L แล้ว '_' +parts+'_%03d'(model). สำเนาauxต่อ'_%03d'(map).
- LH ที่type!=4เปลี่ยนauxด้วยwstring.replace(1,1,"R")ที่78C1EE; modelkeyหลักไม่เปลี่ยน. โล่type4ข้ามทางนี้. import signatureและargumentsตรึงแล้ว.

| fullID | type | model key | map key |
|---|---:|---|---|
|2200201|1|WR_SWORD_003|WR_SWORD_003_002|
|2200203|1|WR_SWORD_004|WR_SWORD_004_002|
|2200601|4|WL_SHIELD_001|WL_SHIELD_001_000|
|2200603|4|WL_SHIELD_003|WL_SHIELD_003_004|
ทั้ง4แถว tag4168 มีbit64. อ่านrawtable974แถว; เทียบเฉพาะ4fixtureแถว ×7คอลัมน์กับTSV. พบ GameClient/Data/GC/M/<modelkeyตัวเล็ก>.ni_ และ <mapkeyตัวเล็ก>.dd_ ครบ8ไฟล์; path/size/SHAรายไฟล์กับraw-row rangesอยู่manifest. เป็น DATA existence; ยังไม่พิสูจน์ค่าของpath globals108B740/724/708ขณะรันหรือการโหลดไฟล์สำเร็จ.

ผูกกับ B1c/B1g:
- resource_request78EBF0 อ่านcurrentRH54และcomparisonRH54→n_EQUIPTYPEทั้งคู่. currenttype10→78FC99เขียนcurrentLH58=RH; else oldtype10และoldLH==currentLH→78FCBEเรียก4277F0(0). เลือกเพียงcurrenttype!=10ยังไม่พอ ต้องคุมoldด้วย. type8/20ยังมีrecordพิเศษ จึงเลือกRHtype1.
- RHslot0B→weapon-nod01; LHslot0C→weapon-nod02; ไม่ใช่ absolute equipmentbag slots. n_EQUIPSLOTของแถวนี้เป็นbitmap16384/16; ไม่แปลงเป็น200+N.
- เสนอseed AvatarครบตามฐานB1g: RH2200201,LH2200601,รอผลการโหลดก่อนเปลี่ยน; mask400→RH2200203 ควรเก็บLH2200601ที่fill/CopyTo; ต่อmask800→LH2200603 ควรเก็บRH2200203. คงidentity/kind/fullactor keyset/Attr cache และฟิลด์อื่นตามฐาน. การรอเสร็จ/ภาพยังเป็นเงื่อนไขทดสอบ ไม่ได้วัดรอบนี้.
- Stop: fixtureก่อนหน้าเป็นtype10,ฐานcacheขาด,lookup/propertyขาด,หรือmodelไม่โหลด ให้แยกสาเหตุ ห้ามสรุปว่าการเก็บมือซ้ายล้มเพียงจากภาพ. การเปลี่ยนshapeเสนอเพื่ออ่านผล ไม่รับรองว่าตาแยกได้ทุกระยะ.

BUILD_PROPOSED: NONE | Codex-static-RE | b1h-20260909-hand-fixtures
BUILD_IMPACT: ไม่มี source/runtime patch; ส่ง fixtureพร้อมฐานรหัสและข้อจำกัดให้เจ้าของใบ.
nonclaims: ไม่พิสูจน์ itemอยู่ในbag,สิทธิ์สวม/คลาส,atomic equip,stat bonus,animation,async completion,reconnect หรือภาพจริง;ไม่ทดแทน GT. ไม่อ้างว่าได้เปิดserver/client.

ค้นตามลำดับ external/gamedata/reference/archive/consumedแล้ว; reuse B1c loader,B1g cache,RE-060 matrix. ใหม่คือraw table-code consumer closure+four resource keys. ไม่แก้ประวัติเดิม.
Review: pf-adversary found P2 (28 unchecked pairs); fixed36-pair grid +4LH controls and four-row wording. Targeted recheck PASS; runtime paths/load remain open.
Verification: PASS34spans/19ranges/3112ins/16sources/186calls/616pins/14strings; raw→974rows→4fixtures/8files;12ID controls/36potential-type/4LH-equality/2partial/2LHtexture. ตรึงimage/sourceก่อนและหลัง.
Artifacts pf_bridge/staged/: standing_b1h_manifest.json SHA319a54a4ed6d017c68c72235e0231ef0a42073d14229121700c7fff72d3787e8; standing_b1h_verify.py SHAb635343613f7d0fdc0872d5b29bc0ad55d46333fba29c154345d95a020c08bb2; standing_b1h_verify.log SHAb65bf39375e97c84ae646c26e02c04d7da9317dac577ab62c8aba80d10210f13; standing_b1h_data.py และbuild.py. Rerun: Python314/python.exe -B pf_bridge/staged/standing_b1h_verify.py (offline).
NEXT: เฉพาะหากต้องปิดresource-load gap ให้ตามpath globalsหรือcompletionของ4keysนี้;ไม่ทำcensusอุปกรณ์ทั้งเกม.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
