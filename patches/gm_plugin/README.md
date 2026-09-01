# GameMaster.dll — ปลั๊กอิน GM ที่สร้างขึ้นใหม่ (source เดินทาง cloud → bridge)

[สาย LANE-GM รอบ `ku3jz6` · revision 2 · 2026-09-01T22:2x+07:00]

## ทำไมมีโฟลเดอร์นี้

เจ้าของตัดสินสดในเซสชัน 2026-09-01: **`GameMaster.dll` ไม่เคยมีและกู้ไม่ได้ ต้องสร้างขึ้นใหม่เองเท่านั้น**

🔴 `[UNPINNED — คำสั่งด้วยวาจาในเซสชัน ไม่มี artifact ใน repo บันทึกไว้]` ต้องติดป้ายนี้ให้ตรง เพราะใบ
ล่าสุดของสายนี้เอง (`notes_to_chief/20260901_2132_RE-164-RESULT-...`) เขียนตรงข้าม: บอกแค่ว่า
**inventory ของบริดจ์หาไฟล์ไม่เจอ** และ nonclaim ข้อ 1 ของใบนั้นปฏิเสธชัด ๆ ว่า "ไม่อ้างว่าหายไปจริง"
ส่วน `PF_GM_PLUGIN_GATE.md:14` ก็ติดป้าย inventory นั้นเองว่า **อาจ stale**
⇒ ไม่มีอะไรในโฟลเดอร์นี้พึ่งความต่างนั้น และ `install.bat` **ปฏิเสธการเขียนทับ** เสมอ (ดูล่าง)

วางใน `patches/` ตามหน้าที่ที่ `.gitignore:71-76` เขียนไว้เอง — "ของที่เดินทางจาก cloud ไป bridge พร้อม
sha256 แทนการ paste ผ่าน code block" และเป็น allowlist แบบ recursive อยู่แล้ว
🔴 `[สมมติของสาย GM - รอ COO ยืนยัน]` คอมเมนต์เดิมเขียนว่า "chief-authored" ซึ่งเป็นที่มา (GT-047)
ไม่ใช่กฎห้ามสายอื่นเขียน — ถ้า COO เห็นว่าต้องย้าย ย้ายให้ทันที

## ปัญหาที่ปลั๊กอินตัวนี้ตั้งใจแก้

ตั้งแต่ `RE-104` (27 ส.ค.) เราไล่หาว่าทำไม **ปุ่ม `BT_GM` โชว์ได้แต่กดแล้วเงียบ**

| ขั้น | เกิดอะไร | แถว |
|---|---|---|
| 1 | client เรียก `LoadLibraryW(L"GameMaster.dll")` → `GetProcAddress("CreateGameMaster")` | `GM-IMG-001` |
| 2 | ถ้า DLL/export/**ผลลัพธ์**หายไป → สร้าง fallback object 4 ไบต์แทน | `GM-IMG-002` |
| 3 | fallback slot `+0x04` คืน `NULL` เสมอ | `GM-IMG-003` |
| 4 | คลิกเรียก slot `+0x04` แล้วส่งค่าต่อให้ dispatcher | `GM-IMG-006` |
| 5 | dispatcher เห็น NULL/ว่าง → `ret` ทันที ไม่ถึง factory ไม่มี log ไม่มีเฟรม | `GM-IMG-007` |
| — | ปุ่มยัง **โชว์** ได้ เพราะ show path เช็คแค่ `application+0x7C8` ไม่ null | `GM-IMG-004` |

🔴 **ระวังคำ:** `PF_GM_PLUGIN_GATE.md:14` ให้น้ำหนักเรื่องนี้ไว้แค่ **"เพียงสอดคล้องกับ"** เส้น fallback
ไม่ใช่ "คือลายเซ็นเป๊ะ ๆ" — และ `GM-IMG-005` ให้ตัวผลิตอาการเงียบแบบเดียวกันอีกตัวที่เป็นอิสระจากกัน
(gate `GMModule_Client+0x19` ซึ่ง `GT-164` ยิงทดสอบไป 14 variant แล้ว) ⇒ ไฟล์นี้ **ไม่อ้างว่าเจอสาเหตุ
ที่แท้จริง** อ้างแค่ว่ากำจัดสาเหตุที่เป็นไปได้ออกไปหนึ่งตัว

เช่นกัน: `RE-118`/`RE-126`/`RE-164` ที่ไล่ประตูอื่นไปแล้ว **ไม่ใช่ "พิสูจน์แล้วว่าทุกจุดถูกต้อง"** —
เป็นการสืบสวนสี่ครั้งที่ยังเปิดหน้าต่างไม่ได้ (`GM-IMG-008` blocker:
`REQUEST_TO_FACTORY_RUNTIME_BINDING_NOT_OBSERVED`) และ `RE-118` เองก็ถูกแก้ไปแล้วบางส่วน
(`20260901_0254_CODEX-CORRECTION-GM-PLUGIN-ROOT-CAUSE.md:15`)

## สัญญา ABI ที่ต้องทำให้ครบ

| slot | สัญญา | แถว |
|---|---|---|
| `+0x00` | output pointer 2 ตัว, `ret 8`, คืนตัวแรกใน EAX | `GM-IMG-012` |
| `+0x04` | ไม่มี argument, `ret` เปล่า, คืน pointer ไปยังสตริง UTF-16 ปิดท้าย NUL | `GM-IMG-006` |
| `+0x08` | destination pointer 1 ตัว, `ret 4`, default-construct MSVCP90 wstring | `GM-IMG-014` |

`[MEASURED — clang-cl 18 targeting the 32-bit MS ABI, รอบ ku3jz6 · ไม่ใช่ MSVC/VC9 จึงเป็นการยืนยัน
แวดล้อม ไม่ใช่ข้อพิสูจน์ว่า VC9 จะให้ผลเดียวกัน]`

คอมไพล์จริงด้วย `clang-cl` (MS ABI, `-m32`, `/W4`) ผ่านสะอาดไม่มี warning แล้ววัดสองอย่าง:

`-fdump-vtable-layouts` → slot เรียงตาม**ลำดับที่ประกาศ** และ RTTI ของ `/GR` อยู่ที่ offset ติดลบ
จึง**ไม่ดัน** slot 0 ตามที่ออกแบบไว้:

```
VFTable indices for 'GameMasterInterface'
  0 | QueryStateOutputs(void*, void*)      -> +0x00
  1 | GetWindowModelBasename()             -> +0x04
  2 | MakeEmptyString(void*)               -> +0x08
```

`llvm-objdump -d` → epilogue ตรงตามที่แต่ละแถวบังคับเป๊ะ:

| ฟังก์ชัน | slot | epilogue | แถว |
|---|---|---|---|
| `QueryStateOutputs` | `+0x00` | `retl $0x8` | `GM-IMG-012` (2 stack args) |
| `GetWindowModelBasename` | `+0x04` | `retl` (เปล่า) | `GM-IMG-006` (0 args, plain ret) |
| `MakeEmptyString` | `+0x08` | `retl $0x4` | `GM-IMG-014` (1 stack arg) |

mangled name ขึ้นต้นด้วย `UAE` = public virtual `__thiscall` (`this` ใน ECX, callee เก็บกวาด) ตามต้องการ
**`build_vs2008.bat` check 3/3 ทำการวัดชุดเดียวกันนี้ซ้ำบน MSVC จริง** ซึ่งเป็นตัวที่นับ

## ทำไม revision 2 ถึงเลิกพึ่ง VS2008

revision 1 **inline `std::wstring` ctor จาก header ของ compiler เราเอง** ลงในหน่วยความจำที่ client เป็น
เจ้าของ ซึ่งผิด — ตัวเลขในตารางเองหักล้าง:

| แถว | span | ยาว |
|---|---|---|
| `GM-IMG-003` (คืน NULL) | `0x009F17E0..0x009F17E3` | **3 ไบต์** = `xor eax,eax; ret` (ตัวคุม) |
| `GM-IMG-014` (slot `+0x08`) | `0x00403C00..0x00403C1D` | **29 ไบต์** |
| `GM-IMG-012` (slot `+0x00`) | `0x00407E10..0x00407E33` | **35 ไบต์** |

29/35 ไบต์คือ prologue + `call` import หนึ่งครั้ง + epilogue **ไม่ใช่** wstring ctor แบบ inline (ลำพัง
`_SECURE_SCL=1` ก็ต้องมี proxy allocation + `_Tidy` + เก็บ `_Myproxy` แล้ว) และ `GM-IMG-014` เขียนเป็น
คำอยู่แล้วว่า "default-constructs that destination **through the pinned MSVCP90 import**"

⇒ revision 2 **เรียก export ตัวนั้นตรง ๆ** (resolve ตอน `DllMain`) layout จึงตรงโดยโครงสร้าง ไม่ขึ้นกับ
compiler ของเรา ไม่ขึ้นกับ `_SECURE_SCL` (ค่า default ของ VC9 ที่ revision 1 ขี่ไว้โดยไม่รู้ตัว และเปลี่ยน
ขนาด `basic_string` ระหว่าง 24 กับ 28 ไบต์) ⇒ สวิตช์ `PF_GM_ALLOW_NON_VC9` **ถูกลบทิ้งทั้งอัน** เพราะ
ไม่จำเป็นอีกต่อไป (และของเดิมมันทำให้ slot `+0x08` คืน pointer ที่ยังไม่ init = แย่กว่าไม่ทำอะไรเลย)

`[MEASURED — llvm-undname]` ชื่อ decorated ทั้งสามตัวถอดกลับแล้วตรงตามที่ตั้งใจ:
`??3@YAXPAX@Z` = `void __cdecl operator delete(void*)` · `??2@YAPAXI@Z` =
`void* __cdecl operator new(unsigned int)` ·
`??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ` =
`public: __thiscall std::basic_string<wchar_t,...>::basic_string(void)`
(revision 2 เคยติดป้ายตัวหลังว่า `[PROPOSED]` ซึ่ง **ระวังเกินจริง** — pf-adversary รอบสองชี้ว่าการสะกด
ตรวจได้และตรวจแล้วถูก การติดป้ายอ่อนเกินก็เป็นการรายงานน้ำหนักหลักฐานผิดเหมือนกัน)

สิ่งที่**ยังไม่รู้จริง ๆ** คือ `msvcp90.dll` บนเครื่องนั้น **export ตัวนี้ออกมาหรือเปล่า** — ถ้าไม่ เรา
resolve ไม่ได้ แล้ว `CreateGameMaster` จะ **คืน NULL ไปเลย** (ไม่ใช่คืน object ที่ construct ไม่ครบ)
พร้อมพิมพ์บอก ⇒ กลับไปสภาพเดิมของวันนี้ ไม่ใช่ failure แบบใหม่ ไม่มีการ fallback ไป inline ctor เด็ดขาด
ตรวจล่วงหน้าได้ด้วย `dumpbin /exports msvcp90.dll | findstr basic_string@_W`

## กฎหน่วยความจำ

`GM-IMG-010`: client ส่ง pointer ของเราเข้า **MSVCR90 `operator delete` ที่มัน import** ตรง ๆ **โดยไม่
เรียก virtual destructor** แล้วค่อย `FreeLibrary`

revision 1 หา CRT ด้วย `GetModuleHandleW(L"msvcr90.dll")` ซึ่ง **ไม่พอ**: MSVCR90 เป็น side-by-side
assembly มีสอง instance พร้อมกันได้ (app-local + WinSxS) ชื่อ base เดียวกัน **คนละ `_crtheap`** —
จองจากตัวหนึ่งแล้วถูก free ด้วยอีกตัว = แครชตอนปิดเกม และ `dumpbin /dependents` รายงานว่าปกติทุกอย่าง

revision 2 เดิน **import table ของตัว client เอง** หา thunk ที่ผูกกับ `??3@YAXPAX@Z` (`operator delete`
ตัวที่ `GM-IMG-010` พิสูจน์ว่าจะถูกเรียกใส่เรา) แล้ว resolve module จาก address ที่ผูกไว้จริง ⇒ ได้
instance ที่ถูกต้อง**โดยโครงสร้าง** ไม่ใช่โดยการเดาจากชื่อ

ถ้าหาไม่เจอ → **คืน `NULL`** ไม่ใช่ `new` ธรรมดา (revision 1 ทำแบบนั้น ซึ่งเป็น cross-heap free แน่นอน)
`GM-IMG-002` ระบุ "the returned object is absent" ไว้ข้าง ๆ library/export ที่หาย ⇒ คืน NULL = client
ติดตั้ง fallback ของมันเอง = **สภาพเดียวกับวันนี้เป๊ะ ๆ** ไม่ใช่ failure แบบใหม่

ยังมี: `DllMain` **pin ตัวเอง** (`GET_MODULE_HANDLE_EX_FLAG_PIN`) เพราะ `GM-IMG-017` blocker
(`DOWNSTREAM_RETENTION_AND_ORIGINAL_OWNERSHIP_UNPROVEN`) ไม่ปิดความเป็นไปได้ที่ panel เก็บ pointer ของ
สตริงเราไว้ ถ้า `FreeLibrary` unmap เราแล้วมีคนอ่านต่อ = แครชตอนปิดที่ไล่สาเหตุยากมาก

## 🔴 ตรวจก่อน build หนึ่งอย่าง — ยังไม่มีใครตรวจ

ทุกการจองหน่วยความจำของปลั๊กอินนี้พึ่ง `FindClientCrt()` ที่เดิน import table ของ client ไปหา thunk ของ
`??3@YAXPAX@Z` **แต่ยังไม่มีใครเปิด import table ของ client จริงมาดูเลยว่า `operator delete` ถูก import
มาแบบมีชื่อ (by name) และ descriptor นั้นมี INT (`OriginalFirstThunk`) อยู่จริงหรือไม่** — ไม่มีแถวไหนใน
gate TSV พิสูจน์เรื่องนี้ ถ้า import มาแบบ ordinal หรือ INT ถูก strip เราจะหาไม่เจอแล้วคืน NULL
(ผลคือปุ่มตายเหมือนเดิม ไม่ได้แครช — และปลั๊กอินจะพิมพ์ `client CRT: NOT FOUND` บอก)

บนบริดจ์ทำได้ในคำสั่งเดียว:

```
dumpbin /imports GameClient.exe | findstr /i "msvcr90 ??3@YAXPAX@Z"
```

เห็น `??3@YAXPAX@Z` ในรายการ = ผ่าน · เห็นแต่ตัวเลข ordinal = ต้องเปลี่ยนวิธีหา CRT (บอกกลับมา)

## build

```
build_vs2008.bat
```

(สคริปต์ `pushd "%~dp0"` เองแล้ว รันจากโฟลเดอร์ไหนก็ได้ — revision 2 แก้จุดที่ path อ้างอิง cwd
ซึ่งอาจทำให้ไปตรวจไฟล์คนละตัวกับที่ copy)

ตรวจให้สามอย่าง **และ fail จริงทุกข้อ** (revision 1 มีสองข้อแรกแต่ทั้งคู่เป็น false green):

1. **ชื่อ export** — revision 1 ใช้ `findstr /i "CreateGameMaster"` ซึ่งเป็น substring match จึง**ผ่าน
   ทั้ง `_CreateGameMaster` และ `CreateGameMaster@0`** คือเขียวให้กับความพังที่ตัวเองโฆษณาว่าจะจับ
   ตอนนี้ปฏิเสธ decoration แต่ละแบบตรง ๆ
2. **CRT dependency** — revision 1 พิมพ์ `[WARN]` แล้วพิมพ์ `[OK]` ต่อ ตอนนี้ `exit /b 1`
3. **epilogue `ret 8`/`ret 4`** จาก `dumpbin /disasm` — ของใหม่

เปลี่ยน option โดยไม่แก้ซอร์ส (revision 1 บอกให้ rebuild ด้วยแฟล็กที่**ส่งเข้าไปไม่ได้จริง**):

```
set EXTRA_DEFS=/D PF_GM_KEY=L\"GMUI_BASIC\"
set EXTRA_DEFS=/D PF_GM_SLOT0_TOUCH_PLUS4=0
```

🔴 **เทียบ SHA256 ที่สคริปต์พิมพ์กับ build ก่อนหน้าทุกครั้ง** ถ้าเท่าเดิม = แฟล็กไม่ถึง compiler และคุณ
กำลังจะเทส DLL ตัวเดิมซ้ำ แล้วสรุปผิดว่าสมมติฐานถูกหักล้างไปแล้ว

## ติดตั้ง

```
install.bat "C:\path\to\client\folder"
```

**ห้าม copy เอง** — `install.bat` **ปฏิเสธการเขียนทับ** ถ้าเจอ `GameMaster.dll` อยู่แล้ว จะหยุด พิมพ์
sha256 ของไฟล์เดิม แล้วบอกให้เก็บสำเนาและรายงาน chief/COO ก่อน เพราะถ้า inventory stale จริง ไฟล์นั้นคือ
ของที่โปรเจกต์นี้ตามหามาตั้งแต่ 27 ส.ค. และยังไม่เคยมีใคร disassemble — ผลของสองทางไม่สมมาตรกัน

🔴 **ห้าม patch `0x009F17E0` ตรง ๆ** (`PF_GM_PLUGIN_GATE.md` ห้ามไว้เอง)

## เกณฑ์ผ่าน — สองชั้น แยกกันเด็ดขาด

**ชั้น static ของ *ตัว DLL นี้*: มีบางส่วนแล้ว (revision 2) แต่ยังไม่ใช่ MSVC**

revision 1 เขียนว่า "ชั้น static ทำเสร็จแล้ว" ซึ่งผิด — เป็นการยืมหลักฐานข้ามชั้น: แถว `PROVEN_EXACT`
ทั้งหลายเป็นหลักฐานเกี่ยวกับ **client image** ไม่ใช่เกี่ยวกับไฟล์นี้ ตอนนั้นชั้นนี้ว่างเปล่าจริง ๆ

รอบนี้เติมได้บางส่วน (ดูหัวข้อ "สัญญา ABI"): คอมไพล์ผ่าน `/W4` สะอาด · vtable เรียงตามลำดับประกาศ ·
epilogue `ret 8`/`ret`/`ret 4` ครบ — **แต่ทั้งหมดวัดด้วย `clang-cl` ไม่ใช่ MSVC และไม่ใช่ VC9**
⇒ ยังต้องให้ `build_vs2008.bat` check 3/3 วัดซ้ำบน toolchain จริงบนบริดจ์ นั่นคือตัวที่นับ

**ชั้น client-observable: ยังไม่มีเลย ต้องมีคนนั่งหน้าจอ**

🔴 **ก่อนเทส ต้องเปิดตัวดู debug output (DebugView หรือ debugger) ไว้ก่อน** ปลั๊กอินพิมพ์บรรทัด
`[GM_PLUGIN]` ตอนโหลด บอก build timestamp · หา client CRT เจอไหม · resolve wstring ctor ได้ไหม · จะคืน
key อะไร — **ถ้าไม่มีบรรทัดพวกนี้ แปลว่า DLL ไม่เคยถูกโหลด** ซึ่งบนจอหน้าตาเหมือนกับ "โหลดแล้วแต่ key
ผิด" ทุกประการ

| # | ต้องเห็น | แยกอะไรได้ |
|---|---|---|
| 0 | บรรทัด `[GM_PLUGIN] loaded build=...` | **DLL เราถูกโหลดจริง** — ถ้าไม่มี ข้อ 1-3 ไม่มีความหมายเลย |
| 1 | ปุ่ม GM ยังโชว์ | ผ่านได้แม้ไม่ติดตั้งอะไรเลย ⇒ ไม่ใช่ตัวตัดสิน แต่ถ้า**หาย**แปลว่าผิดปกติหนัก |
| 2 | **คลิกแล้ว `GMUI_1` เปิด ถึง tab `GMUI_BASIC`** | ← ข้อที่ตัดสินทั้งหมด |
| 3 | ปิดเกมไม่แครช | ผ่านได้แม้ไม่ติดตั้งอะไรเลย ⇒ มีความหมายก็ต่อเมื่อข้อ 0 ผ่านแล้ว |

ข้อ 1 กับ 3 **ผ่านได้ด้วยการไม่ติดตั้ง DLL เลย** (วางผิดโฟลเดอร์ก็ผ่าน) — ข้อ 0 คือสิ่งที่ทำให้ทั้งชุดมี
ความหมาย ยังไม่มีใบ `GT` สำหรับสี่ข้อนี้ สายนี้เปิดใบ GT เองไม่ได้ ขอ chief เปิดให้

## ถ้าพัง — ไล่ตามลำดับนี้

| อาการ | ผู้ต้องสงสัย |
|---|---|
| **ไม่มีบรรทัด `[GM_PLUGIN]` เลย** | DLL ไม่ถูกโหลด: วางผิดโฟลเดอร์ · SxS manifest หาย (error 14001 — ต้องมี VC9 redistributable) · `dumpbin /exports` ซ้ำ |
| พิมพ์ `client CRT: NOT FOUND` | import walk ไม่เจอ `??3@YAXPAX@Z` ⇒ คืน NULL ⇒ สภาพเท่าเดิม |
| พิมพ์ `wstring ctor: NOT RESOLVED` | ชื่อ decorated ผิด — `dumpbin /exports msvcp90.dll` แล้วแก้ |
| โหลดแล้วแต่**คลิกยังเงียบ** | **key ผิด** (`GMUI_1` เทียบ `GMUI_BASIC` — ดู A/B ข้างบน) · หรือ gate `GMModule_Client+0x19` (`GM-IMG-005`) ปิดอยู่ |
| ปุ่ม GM **หายไป** | ไม่ใช่เพราะเราคืน NULL (`GM-IMG-002` ⇒ ปุ่มยังโชว์) แต่คือ fallback allocation ของ client เองล้ม — เรื่องอื่น |
| **แครชตอนคลิก** | slot `+0x00` การ init `+4` → rebuild ด้วย `PF_GM_SLOT0_TOUCH_PLUS4=0` **แล้วเช็คว่า sha256 เปลี่ยนจริง** |
| **แครชตอนปิดเกม** | heap คนละตัว (แต่ import walk ควรกันไว้แล้ว) — เก็บ debug output มาด้วย |

**rollback: ลบไฟล์ `GameMaster.dll` ทิ้ง** client กลับไปเดิน fallback ที่พิสูจน์แล้ว (`GM-IMG-002`) —
เราไม่ได้ patch ไบต์ไหนของ client เลย ไม่ได้เขียน registry เพิ่มไฟล์ใหม่หนึ่งไฟล์เท่านั้น
(ข้อความนี้จริงก็ต่อเมื่อใช้ `install.bat` ซึ่งไม่เขียนทับ — นี่คือเหตุผลที่มันมีอยู่)

## nonclaim

1. **ไม่อ้างว่าหน้าต่างจะเปิดได้จริง** — **ไม่มีการ compile ด้วย MSVC/VC9 ไม่มีการรัน ไม่มีการ boot เกม**
   session คลาวด์ไม่มี MSVC ไม่มี Windows ไม่มี client image ⇒ **ชั้น client-observable ว่างเปล่าสนิท**
   สิ่งที่มีคือ ABI cross-check ด้วย `clang-cl` (ดูหัวข้อ "สัญญา ABI") ซึ่งเป็น **การยืนยันแวดล้อมเท่านั้น**
   ไม่ใช่ข้อพิสูจน์ว่า VC9 จะให้ผลเดียวกัน
   (revision 1 ของ nonclaim ข้อนี้เขียนว่า "ไม่มีการ compile เลย" ซึ่งขัดกับหัวข้อ MEASURED ในไฟล์เดียวกัน
   หลังเพิ่มผล clang-cl เข้ามา — pf-adversary รอบสองจับได้ แก้แล้วตรงนี้)
2. **ไม่อ้างว่า `GMUI_1` คือค่าที่ DLL เดิมคืน** — `[RECONSTRUCTED POLICY — PROPOSED]` และการเทียบใน
   `GM-IMG-008` เป็น tautology (เทียบค่าของเรากับค่าของเราเอง) ⇒ ตัวตัดสินจริงคือ dispatcher lookup ซึ่ง
   blocker เขียนไว้เองว่า `REQUEST_TO_FACTORY_RUNTIME_BINDING_NOT_OBSERVED` ⇒ ต้อง A/B
3. **การ init `+4` ของ slot `+0x00` เป็นการตีความ** — `GM-IMG-012` (`PROVEN_EXACT_ABI_UNKNOWN_SEMANTIC`)
   ไม่บอกชนิด ที่เลือก wstring เพราะช่องข้างเคียงทำแบบนั้น + ความยาว 35 ไบต์สอดคล้องกับ prologue +
   เขียน -1 + call import + epilogue — **เป็นการยืนยันแวดล้อม ไม่ใช่การพิสูจน์**
4. **ไม่อ้างว่าเหมือน DLL เดิม** — เข้ากันได้กับสัญญาที่พิสูจน์แล้วเท่านั้น `GM-IMG-014` ระบุเองว่าไม่ปิด
   ความเป็นไปได้ที่ DLL เดิมมี private method อื่น
5. **ไม่อ้างว่าทุกแถวใน TSV เป็น `PROVEN_EXACT`** — มี 11 ค่าต่างกัน รวม
   `MECHANICAL_..._MANUAL_HASH_ANCHORED` สองแถว (`GM-IMG-015`, `GM-IMG-017`) ซึ่งเป็น manual
   interpretation ไม่ใช่ symbolic dataflow (`PF_GM_PLUGIN_GATE.md:63`) — **และสองแถวนั้นคือแถวที่รับ
   น้ำหนักเรื่อง no-alias กับความปลอดภัยของ static buffer พอดี**
   🔴 revision 1 กับ **จดหมาย `20260901_2132` ที่ merge ขึ้น main ไปแล้ว** เขียนผิดข้อนี้ ต้องออกใบแก้
6. **ไม่อ้างว่าเจอสาเหตุที่แท้จริงของ P-3** — กำจัดสาเหตุที่เป็นไปได้ออกหนึ่งตัวเท่านั้น
   (`GM-IMG-005` ยังเป็นตัวผลิตอาการเดียวกันที่เป็นอิสระ)
7. **ไม่แตะสิทธิ์ GM ฝั่งเซิร์ฟเวอร์เลย** — เปิดได้แค่หน้าต่าง UI ฝั่ง client ใครเป็น GM ยังตัดสินที่
   `gm_accounts` เหมือนเดิม client ยังขอเป็น GM เองไม่ได้ ไม่มีวัน
8. ไม่แตะไฟล์ client เดิม ไม่แตะ canonical DB ไม่แตะ `runtime.py`/`app.py`/
   `pf_login_game_server_v141.py`

## ที่มา

`notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv` (17 IMAGE row + 2 DATA row — `semantic_status`
ต่างกัน 11 ค่า ดู nonclaim 5) และ `.md` คู่กัน
TSV SHA-256: `a5f3fdeb6a830b06e3eb9dceff85fc762459ca3e4f9e7ada152937ef1c898509`
IMAGE SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## sha256 ของซอร์สในโฟลเดอร์นี้ (ตามธรรมเนียม `patches/` — revision 2)

```
7212fc5745f6b336cac42d4a27f81e8db5b33ea3f8ef4de947d07dd9a9d9f032  GameMaster.cpp
9e2a3adc808189ba9ee31060469617e1eb32ab90c8d3094ec0a09a541aba2190  GameMaster.def
40c6f348a7b195b92100edd381feb2e2ce96285feb9c9132dbb1581d6ceda4d3  build_vs2008.bat
abe8b0b98113405f93431170617bc3a7074b7377c16e6bbcfec2475a5c576ab6  install.bat
```
