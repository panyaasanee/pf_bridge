[ถึง: chief cloud (cc), LANE-A และ Panya · จาก: RE runner LOCAL]

# RE-209 RESULT — 11-byte prologue ยืนยันว่า `+0x70`, `+0x360`, `+0x364` ใช้ object เดียวกัน

- เวลา: `2026-09-02T11:43:33.637+07:00`
- สถานะ: **DONE / PASS static**; ไม่มีชั้น client-observable ตามเกณฑ์ใบ
- queue section `RE-209`: 4,723 UTF-8 bytes, SHA-256 `291d72282d7d0f2fc212fe3826a8cf64047498bb93c4eb12b40d9631305506f2`
- image: `GameClient.local.bin`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## 11 ไบต์ที่ถาม

สแปน `[0x0045BC80,0x0045BC8B)` อยู่ raw `[0x0005B080,0x0005B08B)`:

`56 8B F1 F6 46 70 40 74 2F 0F BE`

คำสั่ง:

- `0x0045BC80  56` — `push esi`
- `0x0045BC81  8B F1` — `mov esi, ecx`
- `0x0045BC83  F6 46 70 40` — `test byte ptr [esi+0x70],0x40`
- `0x0045BC87  74 2F` — `je 0x0045BCB8`
- `0x0045BC89  0F BE` — สองไบต์แรกของคำสั่ง 7 ไบต์ `0F BE 86 64 03 00 00`, `movsx eax,byte ptr [esi+0x364]`, ซึ่งจบที่ `0x0045BC90`

คำตอบตรงเกณฑ์: **ESI ถูกเขียนก่อนถึง `0x0045BC83` แต่เขียนจาก `ECX` (`this`) ไม่ใช่ `EDX`; หลังจากนั้นไม่มีการเขียน ESI ซ้ำในฟังก์ชันเต็ม `[0x0045BC80,0x0045BCBC)`** สองไบต์กลางเป็น `jcc` จริง ดังนั้น test `+0x70`, read/write `+0x364` และ pointer `+0x360` ทั้งหมดอ้าง base object ตัวเดียวกัน นี่อุดรูของ `RE-202` และสนับสนุนคำตอบ **ข. (`+0x70` เป็นของ `CNetNPC`)** โดยไม่ต้องเปิด `RE-202` ใหม่

สแปนเต็ม 60 bytes `[0x0045BC80,0x0045BCBC)` ได้ SHA-256 `f808c0d68b1a782d3441e118a25a94ee73e1f4aea37824b06fd2e2c6fb112bc5` **ตรงกับ pin ในใบทุกตัวอักษร**

## ค้นก่อนถอด

- `pf_bridge/external/`: ตรวจ inventory ร่วม 2,683 ไฟล์ / 930,201,065 bytes, manifest fingerprint `89390abfef41fa1fb4618edbb07dd8dccf4c187568fbcdc99a01f08b1c4d891f`; ค้น `45BC80`, `45BC8A`, `45BCBC`, full-span SHA และ `QUEST_MARK_SELECTOR` พบ 6 ไฟล์ ได้แก่ `PF_ATTR_SEMANTIC_DELTA.tsv`, `PF_ATTR_FIELD_SEMANTICS.tsv`, `PF_A2_ATTR_FIELD_DELTA.tsv`, manifest/report สองชุด สิ่งที่พบ pin ชื่อ/สแปน/full SHA แต่ไม่มี raw 11 bytes หรือ disassembly ที่ใบถาม จึงใช้เป็นคำตอบสำเร็จรูปไม่ได้
- `GameClient/gamedata/`: ตรวจ inventory ร่วม 1,109 ไฟล์ / 15,319,585 bytes; ไม่พบคำค้นชุดเดียวกันแม้แต่ไฟล์เดียว คำถามนี้เป็น code provenance ไม่ใช่ตาราง DATA

## BUILD_IMPACT

- ไม่มีการแก้ build/source/data
- LANE-A บริโภคผลนี้เพื่อปิดเส้นทางพิสูจน์ของ `RE-202` ได้; ไม่ต้องย้อนคำตอบ ข. และไม่ต้องเปิดงาน quest-mark ฝั่ง server จากข้อกังวล ESI นี้

## Nonclaims

1. ผลนี้พิสูจน์ identity ของ base register ภายในฟังก์ชันนี้เท่านั้น ไม่ได้ตั้งชื่อ gameplay semantics ของบิต `0x40` หรือ selector
2. ไม่อ้างว่า compute handler นี้เป็น writer เดียว/สุดท้ายของ quest state ทั้งระบบ
3. ไม่ใช้เลข offset เท่ากันเป็น crosswalk; การผูก object มาจาก `mov esi,ecx` แล้วใช้ ESI เดิมตลอดฟังก์ชัน
4. ไม่เปิดเกม/เซิร์ฟเวอร์ ไม่แตะ wire/DB และไม่มี client-observable claim

