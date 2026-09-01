[ถึง: chief (สาย E) | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-GM รอบ `lmqf69` · 2026-09-02T05:59+07:00]
[อ้าง: `RE-164` (สี่ผู้ต้องสงสัย) · ใบส่งมอบของสายนี้ `20260901_2225` (สัญญาว่าจะรีวิว `FindClientCrt()` รอบนี้)
 · `PF_GM_PLUGIN_GATE.tsv` sha256 `a5f3fdeb6a830b06e3eb9dceff85fc762459ca3e4f9e7ada152937ef1c898509` (20 บรรทัด)]

# P-3: อาการเดียวบนจอ แยกเป็นคนละคำตอบได้แล้วก่อนบูตเกม + 🔴 สองข้อระดับ HIGH ในซอร์ส DLL ที่คุณจะให้เจ้าของ build

## ค้นแล้ว
- `external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (สารบัญไม่มีคำว่า GameMaster/plugin/GM-IMG เลย)
- `gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (เช่นกัน)
- แหล่งจริงที่ใช้รอบนี้คือ `notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv`/`.md` (pin sha ไว้ข้างบน)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ**
- `SPEED DENIED` ใน `pirate-force-server` — **ค้นแล้ว: ไม่เจอ** ⇒ PR ทางที่ 1 ของคุณ (`COO-DECISION 0345`)
  ยังไม่อยู่บน `main` ⇒ เงื่อนไข "LANE-GM ยืนยัน 9 ทางปฏิเสธ" (`COO-DECISION 0346`) **ยังไม่เปิด** รอบนี้จึงยังไม่ทำ

## 1. ของที่ลงแล้ว (server `main` รอ merge: PR ด้านล่าง)

`src/pirateforce_foundation/gm/plugin_image_check.py` + `tests/test_gm_plugin_image_check.py` (44 เทส)

ปัญหาที่แก้: ตั้งแต่ `RE-104` (27 ส.ค.) P-3 ให้ผลบนจอ **แบบเดียว** คือ "ปุ่มโชว์ คลิกเงียบ" และ `RE-164`
พิสูจน์แล้วว่ามีอย่างน้อยห้าสาเหตุที่ให้ผลหน้าตาเหมือนกันเป๊ะ เครื่องมือนี้แยกสาเหตุที่ **ตัดสินได้จากไฟล์**
ออกจากกันก่อนบูตเกม: `missing` / `no_such_dir` / `not_pe` / `wrong_machine` / `not_a_dll` / `no_exports` /
`export_decorated` / `export_forwarded` / `export_missing` / `manifest_missing` / `image_ok`
พร้อม sha256 และ **ทุกปัญหาที่บล็อก ไม่ใช่แค่ข้อแรก** (รอบเทส attended มีรอบเดียว ไม่ควรเจอทีละข้อต่อหนึ่ง build)

รันบนสะพานหนึ่งบรรทัด (ไม่มี package ติดตั้ง ต้องมี `PYTHONPATH=src` และใส่เครื่องหมายคำพูดถ้าพาธมีช่องว่าง):

    set PYTHONPATH=src
    py -3 -m pirateforce_foundation.gm.plugin_image_check --dll <พาธ>\GameMaster.dll --client-dir "<ที่ติดตั้ง client>"

exit code 0 เฉพาะเมื่อทุกพาธเป็น `image_ok` **และ** ไฟล์ที่ติดตั้งเป็นไฟล์เดียวกับที่เพิ่ง build
(กับดัก "เทส DLL ตัวเมื่อวานซ้ำ" ที่ `build_vs2008.bat` พิมพ์ sha256 ไว้กันอยู่แล้ว แต่ไม่มีใครเทียบให้)

สิ่งที่ `build_vs2008.bat` ทำไม่ได้และตัวนี้ทำได้: ตรวจ **ไฟล์ที่ติดตั้งข้าง client** (ไม่ใช่ไฟล์ใน build dir),
รันได้โดยไม่มี VC toolchain, และรันในชุดเทสของ repo · ตรวจ export ด้วยการอ่าน export directory จริง
ไม่ใช่ `findstr` (สะกด `_CreateGameMaster` / `CreateGameMaster@0` / `?CreateGameMaster@@YAPAXXZ` แยกได้หมด)

**ขอสองอย่างจากคุณ** (ไฟล์ที่ต้องแก้ไม่ใช่เขตเขียนของสายนี้):
- เพิ่มบรรทัดคำสั่งข้างบนลง `patches/gm_plugin/README.md` (ตารางไล่อาการ) และท้าย `build_vs2008.bat`
- ตอนเปิดใบ GT ของปลั๊กอิน ให้ขั้นที่ 0 เป็น "รันคำสั่งนี้ก่อนบูตเกม บันทึก verdict + sha256"

## 2. 🔴 สองข้อ HIGH ในซอร์ส `patches/gm_plugin/GameMaster.cpp` — เจอโดย pf-adversary รอบนี้ (ตามที่สัญญาไว้ในใบ `2225`)

**สายนี้ไม่ได้แก้ให้** สองเหตุผลตรง ๆ: `patches/` ไม่ใช่เขตเขียนของสายนี้ (ยังรอ COO เคาะตามใบ `2225` ข้อ 2)
และ clone นี้ไม่มี Windows SDK จึง compile-check ไม่ได้เลย — แก้แบบมองไม่เห็นว่าคอมไพล์ผ่านไหม
ในไฟล์ที่เจ้าของจะ build ไปลง client จริง อันตรายกว่าปล่อยไว้พร้อมใบนี้

**H1 — `DllMain` เอาความกำกวม side-by-side ที่ `FindClientCrt()` เขียนมาเพื่อกำจัด กลับเข้ามาให้ MSVCP90**

    HMODULE cpp = GetModuleHandleW(L"msvcp90.dll");   /* GameMaster.cpp:403 */

เป็นการค้นด้วย **ชื่อฐาน** แบบเดียวกับที่หัวไฟล์ (บรรทัด 29-33) อธิบายเองว่าใช้ไม่ได้กับ MSVCR90
และผลที่ตามมาแย่กว่าเดิม: MSVCP90 build ด้วย `_SECURE_SCL=1` ⇒ ctor ของ `basic_string` จอง
`_Container_proxy` ผ่าน allocator **แม้สตริงว่าง** ⇒ ถ้าเครื่องมี app-local `Microsoft.VC90.CRT` และ WinSxS
map พร้อมกัน เราจองด้วย instance A แล้ว client ทำลายผ่าน import ที่ pin ไว้ = instance B ⇒ `HeapFree`
บนบล็อกที่ไม่ใช่ของตัวเอง = heap พังหรือแครชตอนคลิก/ตอนปิดเกม = รอบ attended ตายทั้งรอบ

รูปที่เสนอ (ใช้ของที่ไฟล์นั้นมีอยู่แล้ว): แยก `FindClientCrt()` เป็นตัวทั่วไป เช่น
`HMODULE FindClientModuleImporting(const char* mangledSymbol)` แล้วเรียกสองครั้ง —
`"??3@YAXPAX@Z"` ได้ CRT เหมือนเดิม และ **ชื่อ mangled ของ wstring ctor** ได้ instance MSVCP90 ที่ถูกตัว
โดยไม่ต้องเดา · ของแถมที่ได้ฟรี: ถ้า client ไม่ได้ import ctor ตัวนั้นจริง เราจะ **รู้ตั้งแต่ตอนโหลด**
แทนที่จะรู้ตอนคลิก (`GM-IMG-014` เขียนเองว่า "through the pinned MSVCP90 import" — ชี้ไปที่ import table
ซึ่งเป็นสิ่งที่ `FindClientCrt()` เดินเป็นอยู่แล้ว)

**H2 — ค่า default ของ `PF_GM_SLOT0_TOUCH_PLUS4` เขียนของขนาดที่ยังเดาอยู่ ลงหน่วยความจำของ client**

`PF_GM_PLUGIN_GATE.md` บอกแค่ว่า fallback "เขียน dword แรกเป็น -1 และ init subobject `+4`" —
**ไม่ได้บอกชนิดและขนาดของ `+4`** แต่โค้ดตั้ง default = 1 คือ construct `basic_string<wchar_t>` (28 ไบต์
ถ้า `_SECURE_SCL=1`) ทับ `first+4 .. first+31` ถ้าของจริงเล็กกว่านั้น = เขียนล้นในหน่วยความจำ client
(ถ้า `first` เป็น temporary บนสแตกของผู้เรียก = ทับ return address ตอนคลิก)

และทางหนีที่ README เขียนไว้ (`PF_GM_SLOT0_TOUCH_PLUS4=0` เมื่อแครช) **คือสภาพที่ซอร์สเองประณาม**:
`CreateGameMaster` ปฏิเสธไม่สร้าง object เมื่อ `g_wstringCtor == NULL` โดยให้เหตุผลว่า "เขียน -1 แล้วปล่อย
`+4` ไม่ init = ความพังใหม่ที่แย่กว่าปุ่มตายที่มีอยู่" — แต่ `=0` ให้ผลลัพธ์นั้นเป๊ะ และ guard ไม่ยิง
เพราะมันเช็ค `g_wstringCtor` ไม่ได้เช็ค macro

รูปที่เสนอ: **สลับ default เป็น 0** (เขียนเฉพาะสิ่งที่ `GM-IMG-012` เขียนไว้ตรง ๆ) แล้วให้ `=1` เป็น build ที่สอง
ถ้าคลิกแล้วยังเงียบ · และผูก guard กับ macro ไม่ใช่กับ `g_wstringCtor` (ข้อ 3 ของ adversary: เมื่อ `=0`
ไม่มีใครใช้ ctor นั้นเลย การปฏิเสธทั้งใบเพราะ resolve ไม่ได้ = เผารอบเทสฟรี ๆ)

**อีกห้าข้อ (MED/LOW)** อยู่ในไฟล์รอบ `rounds/GM_20260902_0559_lmqf69_*.md` หัวข้อเดียวกัน:
`client CRT: located` พิมพ์ก่อนที่ `??2@YAPAXI@Z` จะถูก resolve จริง · ทางยอมแพ้เงียบ ๆ หลายทางใน
`FindClientCrt` · ลูป import ไม่มีขอบเขตใน `DllMain` (ล้มใต้ loader lock = client ไม่สตาร์ต) ·
`build_vs2008.bat` check 3 grep `ret 8` ทั้งอิมเมจ จึงผูกกับ slot ไหนไม่ได้เลย

## 3. คำถามเปิดที่ adversary ทิ้งไว้ และสายนี้ตอบแทนไม่ได้ (ส่งต่อให้ COO ในใบคู่กัน)

`PF_GM_KEY` (`GMUI_1` vs `GMUI_BASIC`) กับ `PF_GM_SLOT0_TOUCH_PLUS4` (1 vs 0) = **เมทริกซ์สี่ build**
แต่ละช่องต้อง build ใหม่ ติดตั้งใหม่ เทียบ sha ใหม่ · มีรอบ attended รอบเดียว และยังไม่มีใบ GT ด้วยซ้ำ
ไม่มีที่ไหนเขียนว่า **เริ่มช่องไหน อะไรทำให้ย้ายช่อง และถ้าครบสี่ช่องแล้วเงียบเหมือนกันหมดจะสรุปอะไรได้**

## nonclaim
1. ไม่อ้างว่า `image_ok` แปลว่าหน้าต่าง GM เปิด — เป็นคำพูดเรื่อง **ไบต์ในไฟล์** เท่านั้น ชั้น client-observable ยังต้องมีคนหน้าจอ
2. ไม่อ้างว่า `GameMaster.dll` หายจริงบนเครื่องเจ้าของ — ยังเป็นข้อสังเกตเชิงปฏิบัติการตาม `RE-164` เหมือนเดิม
   เครื่องมือนี้ไม่ตัดสินให้ และ**จงใจ**แยก "ไดเรกทอรีไม่มีอยู่" ออกจาก "ไดเรกทอรีมีแต่ไม่มีไฟล์" เพราะพาธพิมพ์ผิดเคยสร้างข้อสรุปนั้นได้
3. ไม่อ้างว่า parser ถูกต้องกับทุก DLL จริง — ทางเดิน export directory ถูกทดสอบด้วยไบต์สังเคราะห์เท่านั้น
   (ตรวจข้ามกับ PE จริงของ MSVC ที่มีบนเครื่องนี้ได้เฉพาะ header/section/import/manifest — ไฟล์พวกนั้นไม่มี export)
4. ไม่อ้างว่ารีวิว H1/H2 มาจากการรันโค้ด — อ่านซอร์สกับ `PF_GM_PLUGIN_GATE` เท่านั้น ไม่เคย compile ไม่เคยโหลด
5. **GM ข้ามขั้นไหน:** เครื่องมือรอบนี้ไม่ได้ให้สถานะ GM กับใคร และไม่ได้พิสูจน์ฟีเจอร์ใด — เป็นทางลัด
   ไปถึงสภาพที่จะเทสเท่านั้น ปุ่ม GM เปิดได้จริงหรือไม่ยังไม่มีหลักฐานใหม่แม้แต่ชิ้นเดียวในรอบนี้
6. ไม่แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / canonical DB / `scenarios/world_*.json` /
   `scenarios/combat_*.json` / `say_wire.py` / `chat_command_action.py` (สองอันหลัง = คำสั่ง COO `0346`)
7. ใบนี้จ่าหน้าสายเดียว (chief) ตามคำตัดสิน `20260830_2244` / เจ้าของ `20260830_2356`

-- LANE-GM รอบ `lmqf69`
