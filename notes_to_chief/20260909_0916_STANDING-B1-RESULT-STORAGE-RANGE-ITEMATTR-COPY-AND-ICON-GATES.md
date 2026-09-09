งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: chief / LANE-K / LANE-DB
สถานะ: PARTIAL / Standing B1 · B1b · ปิด 2026-09-09T09:16:30.992485+07:00 · IMAGE เท่านั้น
คำถาม: reply รับของเข้าช่องใด และอะไรทำให้ไอคอน regular Char_Info2 เปลี่ยน

1. [MEASURED] IMAGE A — เลขช่องเก็บกับเลข bit เป็นคนละค่า
ItemAttr codec46BD30 อ่าน +34 เป็น2bytes/tag0F ที่46BE01/09 และ +39 เป็น1byte/tag08 ที่46BE1F/27
5A8A00 รับรายการสำเร็จตาม B1a; ที่5A8F91 sign-extend ItemAttr+34 แล้ว5A8F9Eส่งให้5A1240. เมื่อupperเป็นบวกตามinitializerนี้ setterรับเฉพาะ 0<=slot<upper; -1 ถูกตัดก่อน lookup. หา key ใน manager+10 ไม่พบก็return ไม่ได้สร้างช่องใหม่
nonnull ItemAttr ->5A12D8/5C15B0 -> pool46BAA0 -> destinationrecord+20; source.v24 ที่5C1634 ใช้46BC50 (F0EBB0+24). copy +34 ที่46BCAC และ +39 ที่46BCB9 แยกกัน ไม่คำนวณ slot=200+N. destinationต้องผ่านtype-checkและ allocation ต้องสำเร็จ

2. [MEASURED] IMAGE A — ที่มาของขอบเขต ไม่ใช่เลขเดา
signed WORD ในอิมเมจ102208C/90/94/98/9C =40/40/80/40/30
BEB490..BEB4C1 รวมทั้งห้าแล้วเขียน1080B70; BEB4D0..BEB4E6 ลบค่า102209Cแล้วเขียน1080B74. pointer D7BA64/D7BA68 ชี้สอง initializer นี้ตามลำดับ
องค์ประกอบนี้ให้ upper230/lower200. ยังไม่ได้วัดการรัน startup หรือพิสูจน์ว่าไม่มี writer อื่น; ตัวเลขนี้เป็นผลจาก initializer กับค่า IMAGE ที่ตรึงไว้
5AA2E0 constructor สร้าง record ทุก key เริ่ม0จนก่อนupper ผ่าน58A650→5C1370 แล้ว708E20→4F16B0→59EE20 ซึ่งเก็บkeyที่node+0Cและrecordที่node+10. เงื่อนไขคือ initialization/allocation สำเร็จตามทางปกติ
40AAD0 constructor prefix เรียกตัวนี้ด้วยthis+590ที่40AB94/9F ตรงoffset receiverของreplyใน B1a. ไม่อ้าง actual instance จากเพียง offset
regular lookup5A1630 ใช้ [lower,upper) แล้วทดสอบ ItemAttr39 เป็น1<<(N&31) กับwidget94. ดังนั้นเมื่อขอบเขตเป็นค่าข้างบน ช่วงregularคือ200..229; เลขbitไม่ได้เลือกabsolutekey
WIDGET-SLOT reused B1a: Char_Info2 / ITEM_RH_ONE (315,177), regular this170; mask8/N3. ที่58407Dเลือกrecordแล้วเรียก5AA750(widget,record,0). ไม่รวมfashion this190

3. [MEASURED] IMAGE A — ทางไอคอนมีเงื่อนไขเพิ่ม
5AA750 guard record+20 และ template30>0 ก่อนทำงาน; 5AA7B2เรียกA93B00ให้path Icon_Blank_Alpha.tga เมื่อwidget2710=1, แบบ _L เมื่อmodeอื่น ผ่านA93800. ไม่อ้างว่าโหลดภาพสำเร็จ
5AA82Dถามproperty kind0E: ALtrueใช้lowDWORDผล; falseใช้ItemAttr30 เป็นkeyให้892DD0(global108CDD0). หาrowไม่พบออก5AADF9หลังresetข้างต้น
rowที่พบถูกถาม UTF16 s_ID_ICON(F0C144) ผ่าน892050; stringempty ออก5AADE1. nonempty: mode1สร้าง .\Data\GUI\Icon\ +ชื่อ+ .tga; mode2ใช้ _L.tga. modeอื่นส่งpathเริ่มต้นว่างที่5AA976→A93800
A93800 มีทางresource mode2เฉพาะ; ทางทั่วไปA93AB1..AD3ส่งผลA9F350ให้ embedded widget+1440.v1D8. นี่คือเส้นทางส่งresourceให้widget ไม่ใช่ผลจอหรือการเปลี่ยนอาวุธบนactor

4. [PROPOSED] D — ส่งต่อสร้าง/วัด
BUILD_PROPOSED: GT-272 reply ใช้ ItemAttr34 เป็น storage key ในช่วงregularที่พิสูจน์จาก initializer และ ItemAttr39 เป็น bit indexตามslot table; บันทึก key/identity/template/N พร้อมตรวจไอคอน ITEM_RH_ONE และแยกหลักฐาน model/stat | LANE-DB | GT272_STORAGE_BIT_ICON_SEPARATE
เลือก key ตามสถานะช่องว่าง/การย้ายของที่serverถือจริง ไม่ hardcode200+N. รักษาidentityและclear source/replace destination ให้สอดคล้องกัน; lifecycleดังกล่าวยังต้องพิสูจน์ ไม่ได้ปิดในรอบนี้
ผลที่ควรวัด: รับreplyแล้วitemเข้าrecord, noticeเลือกrecordถูก, iconresourceพบ/แสดง แล้วจึงตรวจactor modelกับstatแยก. ถ้าiconไม่ขึ้นตรวจtemplate/property0E/s_ID_ICON/mode; ห้ามสรุปว่าslotผิดจากจอว่างเพียงอย่างเดียว
nonclaims: ยังไม่มีoriginal reply/runtime pass/GUI screenshot; ไม่ยืนยันslot allocation policyของserverเดิม, startup/all writers, property0Eชื่อสากล, appearance/stat/unequip/reconnect. ไม่ยกระดับV140/V141หรือหลักฐานRE280

ผลการค้นก่อนทำ: 1080B70|1080B74|5AA750|BEB4B0|equip.*(range|index)|equipment.*(range|index) ในMD/PY: external1, gamedata0, reference1, archive2, consumed0. พบpf_rederive_attr_semantics.py:22680เป็นequipment tableอื่น; archive20260907:592คือRE280 และarchive20260827:867คือRE060. log staged/standing_b1b_search.log; ไม่ใช่หลักฐานว่าIMAGEไม่มีทางอื่น
หลักฐาน: GameClient.local.bin SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
VA/offset/span/SHAครบ33ช่วง +source5ไฟล์: staged/standing_b1b_manifest.json SHA 0a1ae999f801a92fc77b7b2045f3c8aa4670dca100668708002c98fb67850000
ตัวอย่าง setter5A1240..5A1309 offset1A0640 SHA6434f0f14a829a398e3dab276bbc8823f808d075ca0ede62c7db901e260bf971
verifier staged/standing_b1b_verify.py SHA 55acfc00864ad4a7f154dd23c58be61525075435175c9b7698f173079332f2c5; log standing_b1b_verify.log SHA dff8919850c35de5e079649729e0cec6fb48d2a50e4e42279e9e3866911f4c4e
รันซ้ำ: C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe -B pf_bridge\staged\standing_b1b_verify.py (cwd Pirate Force)
PASS33 spans/22 complete decodes/5 sources/28 calls/46 operands/5 pointers/5 WORDs/7 strings; static verifier ไม่ใช่ native/UI test
ADVERSARY: a6f_review rerun exit0; แก้2จุดที่พบ: qualify upperบวก และเทียบUTF16LE+NULทั้ง7ข้อความตรงIMAGE. ผู้ตรวจยืนยัน copy/initializer/icon branches ตรงdisassembly; ไม่มีruntime claim
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
