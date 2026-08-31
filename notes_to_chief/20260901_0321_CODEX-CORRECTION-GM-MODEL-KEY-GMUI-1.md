[ถึง: chief · LANE-GM · COO | จาก: Codex static RE | 2026-09-01T03:21:42+07:00]

# CODEX CORRECTION 2 — model key ที่ผ่าน GM factory คือ GMUI_1

## คำแก้ที่ต้องใช้แทนบันทึก 02:54

บันทึก `20260901_0254_CODEX-CORRECTION-GM-PLUGIN-ROOT-CAUSE.md` ระบุถูกว่าปุ่ม GM ติดที่ plug-in interface และ fallback slot `+0x04` คืน NULL แต่ประโยคที่เสนอ `GMUI_BASIC` เป็น candidate น้ำหนักสูงของค่าคืน slot นั้น **ถูกถอนแล้ว**.

**[ORIGINAL EVIDENCE: IMAGE]** slot `+0x04` คืนชื่อฐานของ GUI model. Resolver `0x00A91070..0x00A91356` ประกอบ path รูป `.\Data\GUI\Model\<key>.model` ก่อนส่งเข้า factory. Literal `GMUI_BASIC` มี xref เดียวที่ `0x00726DF2` และถูกใช้หลังสร้าง panel แล้วเพื่อค้น child/tab; มันไม่ใช่ชื่อ model ที่ resolver ต้องการ.

**[ORIGINAL EVIDENCE: DATA]** `Data\GUI\Model\GMUI.project` ประกาศ `<Model Name="GMUI_1"/>`; `GMUI_1.model` มี root window ID `GMUI_1` และมี child tab ID `GMUI_BASIC`. ตรวจ model corpus 534 ไฟล์แล้วพบ `GMUI_BASIC` ใน model นี้เพียงไฟล์เดียว.

ดังนั้น **[RECONSTRUCTED POLICY — PROPOSED, NOT EXECUTED]** compatibility plug-in ควรให้ slot `+0x04` คืน static-lifetime `L"GMUI_1"` ไม่ใช่ `L"GMUI_BASIC"`. นี่เป็นผลประกอบ IMAGE + DATA; ไม่ใช่หลักฐานว่าเห็น DLL เดิมคืนค่านี้ที่ runtime.

## ABI ที่ปิดเพิ่ม

- application member `+0x7C8` มี reference จริงครบ 15 จุด: read 10 / write 5; raw displacement อีกหนึ่งจุดเป็น `LEA [ESP+0x7C8]` ที่ไม่เกี่ยวข้อง.
- interface มี call จริงเพียง slot `+0x00` หนึ่งครั้งและ slot `+0x04` สี่ครั้ง; ไม่พบ slot อื่นหรือ virtual destructor/release.
- slot `+0x00`: `ECX=this`, stack output-pointer 2 ตัว, callee `ret 8`; fallback เขียน dword แรกเป็น `-1` และ init subobject `+4`. ชื่อ semantic ของ output ยัง UNKNOWN.
- slot `+0x04`: `ECX=this`, ไม่มี explicit argument, plain `ret`, คืน NUL-terminated `const wchar_t*`; client ไม่ free string.
- application ลบ object ด้วย imported MSVCR90 scalar `operator delete(void*)` แล้ว `FreeLibrary` โดยไม่เรียก destructor. ห้ามคืน static/global object และห้ามพึ่ง destructor cleanup.

## ผลลัพธ์ตรวจซ้ำได้

- `external/PF_GM_PLUGIN_GATE.tsv`: 15 แถว — IMAGE 13 / DATA 2, 16,795 ไบต์, SHA-256 `14581a25e62c7c5eb1c8b805efae68ff6341c9ba1bcef951536484a11064bd25`.
- `external/PF_GM_PLUGIN_GATE.md`: 9,281 ไบต์, SHA-256 `b9e28552a542110d995f051ccd88cb2b0167b8d2d7798bda64c8e40acf17929f`.
- `external/pf_rederive_gm_plugin_gate.py`: 48,525 ไบต์, SHA-256 `a65328259a92a14ece5f2f0e01b81c61321a7a8295f950c1a077d7aa78e19d18`; write และ `--check` ผ่านตรงกัน.
- IMAGE ก่อน/หลัง: 14,759,424 ไบต์, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `GMUI.project`: 148 ไบต์, SHA-256 `392f17ba4aba1342ed1e0ec8133e1f2f074b94081fa1ee41bf718021746c0632`.
- `GMUI_1.model`: 25,434 ไบต์, SHA-256 `ffd7e5d1c44ffe36b5bacc2857aa049ae6cbea69e11f62541bd0632162bbc69f`.

## Acceptance ที่ยังต้องทำโดย lane runtime ที่ได้รับอนุญาต

ต้องเห็นปุ่ม GM → คลิก → panel `GMUI_1` เปิด → เข้าถึง tab `GMUI_BASIC` และปิดเกมสะอาดโดยไม่ crash. Static checkpoint นี้ส่งมอบ contract สำหรับ implementation แต่ยังไม่อ้างผล runtime pass และไม่ได้แก้ ServerProject หรือรัน GameClient/server/DLL.
