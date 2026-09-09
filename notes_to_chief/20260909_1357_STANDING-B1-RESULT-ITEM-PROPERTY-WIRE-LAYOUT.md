งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: GT-272 equipment owner / LANE-B / CORE / LANE-K / chief / Panya · Codex static RE
B1p · IMAGE A / integration D · ปิดผลลัพธ์ 2026-09-09 · NEWPROGRESS: exact ItemAttr property wire layout for keys 4 and 7

[MEASURED] คำตอบ: ItemAttr มี presence byte สำหรับ property collection แล้ว collection ส่ง `u8 count`; ต่อหนึ่งสมาชิกส่ง `u8 key` ก่อน payload ที่เลือกชนิดจากช่วงของ key. Key 4 และ 7 อยู่ในช่วง `<0x63` จึงใช้ชนิด qword และส่ง `tag 0x32 + u64 little-endian`. ดังนั้นสอง key ที่ B1o พบไม่ใช่ opcode: เป็นค่าของ field key ใน record แบบ `0B key 32 value64` ภายใน collection จริง

ค้นชุดส่งมอบแล้ว: B1b พิสูจน์ ItemAttr codec และ B1o พิสูจน์ accessor key4/key7 แต่ทั้งคู่เปิด serializer layout ไว้. ค้น focused ใน notes/external/staged ก่อนถอดแล้วไม่พบคำตอบ exact ของ `ItemAttr+0x3C -> collection -> key4/7 qword`; ไม่มีข้ออ้าง global absence.

[MEASURED][IMAGE A] เส้นทางและ layout:
- ItemAttr codec `0x0046BD30..0x0046BEA1` มี field ก่อนหน้า `+0x28 tag32/u64`, `+0x30 tag14/u32`, `+0x36 tag0F/u16`, `+0x34 tag0F/u16`, `+0x38 tag08/u8`, `+0x39 tag08/u8`; จากนั้นเขียน `tag0B/u8` ว่า `+0x3C` nonnull หรือไม่. ถ้าเป็น 1 จึง dispatch virtual `+0x34` ของ collection. ฝั่งอ่านสร้าง collection จาก pool `0x0103107C`, เรียก codec แล้วผูกกลับ ItemAttr+0x3C. นี่เป็น nested tail ของ ItemAttr ไม่ใช่ vital id ใหม่.
- Concrete collection vtable `0x00F0EE10` ชี้ serializer slot `+0x34` ไป `0x00470BB0`. Serializer `0x00470BB0..0x00470D8D` เขียน `tag0B/u8 count`; แต่ละสมาชิกเขียน `tag0B/u8 key` จาก object+0x10 แล้วเรียก virtual `+0x28` ของ property object. Reader อ่าน count/key ตามลำดับเดียวกันและเลือก factory ด้วย unsigned key: `<0x63`, `0x63..0x76`, หรือ `>=0x77`.
- ช่วง `<0x63` ใช้ factory `0x00470250..0x0047033E`, ขนาด object 0x20, vtable `0x00F0ED7C`, key ที่ object+0x10 และ qword ที่ +0x18/+0x1C. vtable slot `+0x28` ชี้ `0x006C0180`; codec `0x006C0180..0x006C01A3` เขียน/อ่าน `tag0x32`, length8, ที่ object+0x18. Constructor ตั้ง qword เริ่มต้นเป็น `0xFFFFFFFFFFFFFFFF`; ค่าที่อ่านจากสายแทนที่มันได้ รวมศูนย์.
- Layout เฉพาะ collection ที่มี key4=0x1122334455667788 และ key7=0x0102030405060708 คือ known-answer `0b02 0b04 32 8877665544332211 0b07 32 0807060504030201`. นี่เริ่มที่ count ของ collection; ถ้าอยู่ใน ItemAttr เต็มต้องมี field ก่อนหน้าและ presence `0b01` ตาม codec ข้างบน.

หลักฐานทุกช่วงเป็น `[start,end)` จาก `GameClient.local.bin` 14,759,424 bytes SHA256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`:
- ItemAttr codec VA `0x0046BD30..0x0046BEA1`, file `0x0006B130`, SHA `b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1`.
- qword-property factory VA `0x00470250..0x0047033E`, file `0x0006F650`, SHA `083a11cb3df908f09314275f6ad2d8a297c47f3c4ab18d8381ee8daea0f6b872`.
- collection codec VA `0x00470BB0..0x00470D8D`, file `0x0006FFB0`, SHA `124e4437b8293c8105e470827a08a3a31a4be4ba51c3ece84342cd67fa4c8b97`.
- qword-property codec VA `0x006C0180..0x006C01A3`, file `0x002BF580`, SHA `c0910c6ea5ebd56e25c4d3c64c7bd97f939a01e97baef3f489057467ac943bce`.
- qword-property vtable VA `0x00F0ED7C..0x00F0EDAC`, file `0x00B0D17C`, SHA `6ddeddc11383cb3e695749355cbefc422393896e0d51c136dcd04a84acd73587`.

[PROPOSED][D] B1o arithmetic controls now have an exact nested property encoding: absent collection; present empty collection; key7=1/key4=0; key7=1/key4=1; and typed key7=0. Build the complete ItemAttr through the already proved outer codec rather than splicing these bytes at a guessed frame offset.
BUILD_PROPOSED: Add GT-272 ItemAttr builder support for optional property collection with qword-family keys `<0x63`, preserving `u8 count -> (u8 key, u64 value)` order; add B1o key4/key7 preview controls and log the decoded collection before dispatch | LANE-B / equipment owner; LANE-K to bind | `GT272_PROPERTY_QWORD_CODEC_GUARD_PASS`

BUILD_IMPACT: ปิด blocker “property serializer proof” ของ B1o และทำให้สร้าง control key4/key7 ได้โดยไม่เดา bytes. ยังไม่ปิดว่า frame ตอบการสวมใส่ตัวใดเป็น producer ของ ItemAttr เต็ม หรือว่าค่า property นี้ถูก server เดิมสร้างเมื่อใด.
nonclaims: no semantic name for key4 or key7; no claim that `s_VARYDATA="71"` means property7; no legitimacy/range policy for values; no proof that duplicate keys are accepted or which duplicate wins; no original equip response vital; no equip-to-CBuff producer; no native/server/client run, GUI result, persistence, reconnect, or regression promotion.
Artifacts: `pf_bridge/staged/standing_b1p_probe.py`, `standing_b1p_probe.log`, `standing_b1p_verify.py`. The verifier is stdlib-only, pins five IMAGE spans, reproduces a two-property known answer, rejects a changed qword tag, and detects an IMAGE-byte trap.
End state: static read only; no native/server/client opened; no queue/lease/workflow/reference/ServerProject/Git edits.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
