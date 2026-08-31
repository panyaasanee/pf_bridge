[ถึง: chief · LANE-GM · COO | จาก: Codex static RE | 2026-09-01T02:54:34+07:00]

# CODEX CORRECTION — ต้นเหตุปุ่ม GM อยู่ที่ plug-in interface ไม่ใช่ panel ปัจจุบัน

## คำตัดสินที่ต้องหยิบใช้ทันที

**[ORIGINAL EVIDENCE: IMAGE]** `application+0x7C8` ที่ `RE-118` เรียกว่า “current-UI object” ถูกระบุ owner ใหม่แบบ exact แล้ว: application init `0x0040A46F` เรียก loader `0x00406720`; loader ทำ `LoadLibraryW(L"GameMaster.dll")` → `GetProcAddress("CreateGameMaster")` → เรียก export → เก็บ pointer ที่ `application+0x7C8`.

ถ้า DLL/export/object ไม่มี loader จะสร้าง fallback 4 ไบต์ vtable `0x00F09AF0`. Fallback **ไม่ใช่ NULL** จึงผ่านเงื่อนไขแสดงปุ่มที่ `0x0053B19C..0x0053B1D9`, แต่ vtable slot `+0x04` ชี้ `0x009F17E0` ซึ่งคืน `NULL` เสมอ. เมื่อคลิก `BT_GM`, `0x0053BC51..0x0053BC96` เรียก slot นี้ แล้ว dispatcher `0x00AA0710..0x00AA0799` ตัดจบทันทีเพราะ key เป็น NULL/empty ก่อนถึง factory.

ดังนั้นเมื่อนำ IMAGE fact ไปประกอบกับ **บัญชีไฟล์ตามคำสั่งเจ้าของ** ที่วัดแล้วว่าเครื่องนี้ไม่มี `GameMaster.dll`, อาการ “ปุ่มโผล่แต่คลิกเงียบ” มี root cause ครบสายโดยไม่ต้องเปลี่ยน `GM_UpdateGMStateVital` เพิ่ม.

## สิ่งที่แก้จากรายงานเดิม

- **แก้ `RE-118` เฉพาะ semantic owner:** `+0x7C8` ไม่ใช่ panel/map/bag “current UI context”; มันคือ interface object จาก `GameMaster.dll` หรือ fallback ของ interface นั้น.
- **ถอน procedure A/B เปิด map/bag เพื่อทำ key ให้ไม่ว่าง:** `GT-103 A/B` สี่สถานะที่เงียบยังเป็นผลชั้นจอจริงและสอดคล้องกับ fallback; ผลลบไม่สูญหาย แต่คำอธิบายเดิมถูกแทนที่.
- **คงข้อจริงจาก `RE-118`:** query type `0x25` อ่าน `GMModule_Client+0x19`; dispatcher/factory ต้องการ key non-null/nonempty; factory `0x007280D0` เปรียบเทียบ key แบบ UTF-16 exact ก่อนสร้าง object ขนาด `0xEC`.
- **คง `RE-126`:** `BT_GM` ผูก control เดียวกับ handler จริง; ไม่ต้องเปิดใบหา binding ซ้ำ.
- ผล `GT-164` ที่ลอง state variants 14 แบบแล้วยังไม่เปิด ไม่ใช่เรื่องแปลก: state byte เปิดปุ่มได้ แต่ไม่สามารถทำให้ fallback getter คืน key ได้.

## ทางปลดที่หลักฐานรองรับ แต่ยังไม่ใช่ runtime pass

**[RECONSTRUCTED POLICY — PROPOSED]** ทางตรงที่สุดคือ compatibility `GameMaster.dll` แบบ 32-bit ที่ export `CreateGameMaster`, คืน object ABI ตรง และให้ vtable slot `+0x04` คืน UTF-16 key ที่ไม่ว่าง/ตรงกับ factory request. IMAGE พบ request literal `GMUI_BASIC` ที่ `0x00726DF2`; ให้ใช้เป็น candidate น้ำหนักสูงสำหรับการยืนยันเท่านั้น ยังห้ามอ้างว่า DLL เดิมคืนค่านี้เสมอ.

Application cleanup ส่ง object pointer เข้า imported `MSVCR90 operator delete(void*)` โดยตรง แล้ว `FreeLibrary`; compatibility implementation ต้องรักษา allocator/cleanup boundary และต้องทดสอบทั้งเปิดหน้าต่างกับปิดเกมสะอาด. ห้าม patch shared null stub `0x009F17E0`.

## หลักฐานและไฟล์ผล

- ค้นชุดส่งมอบก่อนเริ่ม: ไม่พบ `GameMaster.dll|CreateGameMaster|GMUI_BASIC|0x00406720`; จึงเป็นหลักฐาน IMAGE ใหม่ ไม่คัดลอกแถวเก่า.
- `external/PF_GM_PLUGIN_GATE.tsv` — 10 IMAGE rows, 9,873 ไบต์, SHA-256 `83825528c4819398711951234fe21655efdec1309a93fc650b08f57ae07a93e9`.
- `external/PF_GM_PLUGIN_GATE.md` — 6,218 ไบต์, SHA-256 `f61def58b17c3371db83257dd781c95fc7b4e95cb84f791e06698588ab9fbfe9`.
- `external/pf_rederive_gm_plugin_gate.py` — dependency-free, fail-closed; write/check สร้างผลตรงกัน.
- span หลัก: loader `0x00406720..0x00406791` SHA `120604819103b24b0563d1d68c568a98be3bdc5d547451697cc8f6bf4dbb6894`; click SHA `0fbd32d41059ee8370a1e89aeb30c7c5c8bea1ec73688e9a14363759e1a86338`; dispatcher SHA `62fd9c6fdb6a85443ec6f2657495caf2c26f1ea580b432195c26f89b171a2d99`; factory SHA `e6209b9021e4e3c689c3b8b75c18b8b1c60840e8761229ab6d4b4e37eb98de34`.
- GameClient.local.bin ก่อน/หลัง: 14,759,424 ไบต์, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

## ขอบเขต

ไม่มีการรัน/แก้ GameClient, server, DLL, dump, capture, ServerProject, workflow, queue, lease หรือ Git. ทุกแถวเป็น `source=IMAGE`; ไม่มีชั้นหลักฐานอื่นผสม. ยังไม่อ้างว่าปุ่มเปิดสำเร็จบนจอจนกว่าจะมี runtime validation ตามสิทธิ์และเจ้าของยืนยัน.
