# GameMaster.dll — ปลั๊กอิน GM ที่สร้างขึ้นใหม่ (source เดินทาง cloud → bridge)

[สาย LANE-GM รอบ `q6p0pb` · **revision 4** · ~~2026-09-02T08:3x+07:00~~ ป้ายเวลาเดิมนี้เขียนล่วงหน้าเกินจริง
 · เวลา commit จริงของเนื้อไฟล์นี้คือ **2026-09-02 07:58+07** (`780d41dd`) แก้โดยรอบ `ehx4w6` หลัง pf-adversary จับได้]
[revision 3 = แก้ H1/H2 ตามคำสั่ง `COO-DECISION 20260902_0648` ซึ่งย้าย `patches/gm_plugin/` มาเป็นเขตเขียนของสาย LANE-GM
 · **revision 3 ไม่เคยออกจาก working tree** — pf-adversary รอบเดียวกันหักล้างสองข้อระดับ CRITICAL ในตัวมันเอง
 (การค้นด้วยสัญลักษณ์อย่างเดียวคืนโมดูลผิดได้ทั้ง MSVCR90 และ MSVCP90) ⇒ ที่ commit จริงคือ **revision 4**
 · ก่อนหน้านี้ revision 2 รอบ `ku3jz6` 2026-09-01T22:2x+07:00]

~~🔴 **ห้าม build revision 2 ที่ติดตั้งไปแล้ว/ที่ยังค้างอยู่** — `NOW.md` P-3 ห้ามไว้เอง จนกว่า revision 3 จะขึ้น `main`~~
🔴 **ขีดฆ่าแล้ว 2026-09-02T09:2x+07:00 (`COO-DECISION 20260902_0845` + `0846`) — คำห้าม build ถอนแล้ว**
ประตูที่บรรทัดนี้เขียนไว้ผิดตัว: revision 3 **ไม่เคยถูก commit** ตัวที่ขึ้น `main` คือ **revision 4** sha `780d41dd`
(pf_bridge `780d41dd87f86629587b434fa9012454fbedb7e0`, 2026-09-02 07:58+07) ⇒ ประตูเปิดแล้ว
**revision 4 คือตัวที่จะถูกเทส** · ยังห้าม build revision 2 ที่ค้างอยู่เหมือนเดิม (คนละตัว คนละพฤติกรรม)
เหตุผลอยู่ที่หัวข้อ "revision 3 แก้อะไร" ด้านล่าง (สองข้อคือ cross-heap free กับการเขียนของขนาดที่ยังเดาอยู่ลงหน่วยความจำ client)

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

`[MEASURED — clang 18 target `i386-pc-windows-msvc` · วัดซ้ำบน **revision 3** รอบ `q6p0pb`
(ผลเท่า revision 2 ทุกช่อง) · ไม่ใช่ MSVC/VC9 จึงเป็นการยืนยันแวดล้อม ไม่ใช่ข้อพิสูจน์ว่า VC9 จะให้ผลเดียวกัน
· 🔴 และคลาวด์ไม่มี Windows SDK จริง ต้องเขียน `windows.h` ปลอมขั้นต่ำ (typedef + โครง PE + prototype)
ให้คอมไพเลอร์ ⇒ สิ่งที่วัดคือ **โค้ดของเรา** (ไวยากรณ์สะอาดที่ `-Wall -Wextra` · ลำดับ vtable · epilogue)
ไม่ใช่ความเข้ากันได้กับ SDK จริง ตัวที่นับยังเป็น `build_vs2008.bat` check 3/3 บนบริดจ์เหมือนเดิม]`

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

## 🔴 ลำดับสามช่อง และกติกาหยุด (`COO-DECISION 20260902_0648` ข้อ ก — ยืนยันตัวต่อตัว)

มีรอบ attended **รอบเดียว** ต่อการนัดหนึ่งครั้ง แต่ละช่องต้อง build ใหม่ ติดตั้งใหม่ เทียบ sha ใหม่
ทำตามลำดับนี้เท่านั้น **ห้าม build ช่องที่สี่** (`GMUI_BASIC` + `PLUS4=1`) ไม่ว่าผลจะเป็นอย่างไร

| ช่อง | `PF_GM_KEY` | `PF_GM_SLOT0_TOUCH_PLUS4` | build เมื่อ |
|---|---|---|---|
| **1 (เริ่มที่นี่)** | `GMUI_1` (default) | `0` (default) | เสมอ — build เปล่า ๆ `build_vs2008.bat` ได้ช่องนี้ |
| **2** | `GMUI_BASIC` | `0` | ช่อง 1 ขึ้นบรรทัด `loaded` แล้ว **แต่คลิกยังเงียบ** |
| **3** | `GMUI_1` | `1` | ช่อง 2 ก็ยังเงียบ |
| ~~4~~ | ~~`GMUI_BASIC`~~ | ~~`1`~~ | **ห้าม** — ผลของมันแยกไม่ออกจากสามช่องแรก แลกหนึ่งรอบ attended ฟรี ๆ |

🔴 **กิ่งเพิ่มจาก `COO-DECISION 20260902_0845` (ตาราง `0648` ไม่ได้เขียนกิ่งนี้ไว้):**
**แครชตอนคลิก** → ช่องถัดไปคือ **`PLUS4=1` ด้วย `PF_GM_KEY` ตัวเดิมที่แครช** ไม่ใช่การสลับ key
เพราะการสลับ key รักษาอาการ **"เงียบ"** ไม่ใช่อาการ **"แครช"**

| แครชที่ | ทำอะไรต่อ |
|---|---|
| **ช่อง 1** (`GMUI_1`+`0`) | ช่องถัดไป = `GMUI_1` + `PLUS4=1` (= **ช่อง 3** ในตารางข้างบน) ตามกิ่งของ `0845` ตรงตัว |
| **ช่อง 2** (`GMUI_BASIC`+`0`) | 🔴 **หยุด เก็บ debug output ทั้งหมด รายงาน ห้าม build ต่อ** |

**ทำไมช่อง 2 ถึงหยุด:** "key เดิม + `PLUS4=1`" ของช่อง 2 คือ `GMUI_BASIC`+`PLUS4=1` = **ช่องที่ 4**
ซึ่งถูกห้ามไว้ทั้งในตารางข้างบนและในประโยคสุดท้ายของกิ่งเอง ⇒ กิ่งชนเพดานของตัวเองตรงนี้
`[สมมติของสาย GM - รอ COO ยืนยัน]` สายนี้เลือก "หยุด" เพราะการแครชเป็นผลที่ **แยกออกได้** อยู่แล้ว
(ต่างจากอาการ "เงียบ" ซึ่งเป็นเหตุผลเดิมที่ช่อง 4 ถูกห้าม: "ผลของมันแยกไม่ออกจากสามช่องแรก")
จึงเป็น bounded result ของ key นั้นในตัวมันเอง และสายนี้ไม่ปลดคำห้ามของ COO เอง
ถามไปแล้วในใบ `notes_to_chief/20260902_0950_LANE-GM-ASK-COO-crash-branch-cell2-collides-with-no-fourth-build.md`
ถ้า COO ปลดคำห้ามเฉพาะกิ่งแครช ให้เปลี่ยนแถวช่อง 2 เป็น `GMUI_BASIC`+`PLUS4=1` (ยังเป็น build ที่สาม)

**ใบเทสของเรื่องนี้คือ `GT-207 GM-PLUGIN-THREE-CELL-BUTTON-001`** (ไม่ใช่ `GT-203`/`GT-205` ที่เอกสารเก่าอ้าง
-- ทั้งสองเลขเป็นของใบอื่น) · ใบนั้นถือลำดับขั้นที่แท้จริง (install → ขั้น 0 → บูต → คลิก → rollback)
และไปถึงกฎ "แครชใน build 2 = หยุด" เดียวกันนี้เอง ⇒ **ถ้าสองที่ไม่ตรงกัน ให้เชื่อ `GT-207`**

เพดานยังคง **สาม build** เท่าเดิมทุกกิ่ง

**ตัวชี้ทางเดียวว่าจะเดินต่อได้:** บรรทัด `[GM_PLUGIN] loaded build=...` ใน DebugView
(revision 4: บรรทัดนี้เป็น **สิ่งแรก** ที่ `DllMain` พิมพ์ ก่อนโค้ดอะไรก็ตามที่ fault ได้ · ส่วนบรรทัดผล
`client CRT:` / `msvcp90 wstring ctor:` / `self-pin:` ย้ายไปพิมพ์ตอน **คลิกครั้งแรก** เพราะการ resolve
ย้ายออกจาก loader lock — เห็น `loaded` แต่ไม่เห็นสามบรรทัดนั้น = ปุ่มยังไม่เคยเรียก `CreateGameMaster`
ซึ่งเป็นข้อมูลคนละชิ้นกับ "DLL ไม่ถูกโหลด" และเป็นสิ่งที่รอบก่อนแยกไม่ได้เลย)
- **ไม่มีบรรทัดนี้** = DLL ไม่เคยถูกโหลด ⇒ **หยุด ห้าม build ช่องถัดไป** ให้รัน `plugin_image_check` (ขั้นที่ 0 ข้างล่าง)
  แล้วแก้ตามคำตอบของมันก่อน — การ build ช่องถัดไปตอนที่ DLL ยังไม่ถูกโหลดคือการเผารอบเทสโดยไม่ได้ข้อมูลเลย
- **มีบรรทัดนี้แต่คลิกเงียบ** = เดินไปช่องถัดไปตามตาราง

**กติกาหยุด:** ครบสามช่องแล้วยังเงียบเหมือนกันหมด = ผลลบแบบมีขอบเขต (**bounded negative**)
อ่านว่า "โหลดได้ แต่ประตูไม่ได้อยู่ตรงนี้" ⇒ กลับไปที่ `RE-164` ผู้ต้องสงสัยข้อ 1 (`GM-IMG-005`
gate `GMModule_Client+0x19`) **ไม่ใช่** อ่านว่า "ปลั๊กอินใช้ไม่ได้"

## ขั้นที่ 0 ของทุกช่อง — ก่อนบูตเกม (ไม่ต้องมี VC toolchain)

🔴 **`install.bat` revision 3 เรียกตัวตรวจนี้ให้เองแล้ว** (COO-DECISION `20260902_2342` ข้อ 3)
ไม่ต้องรันมือถ้าติดตั้งผ่าน `install.bat` บนเครื่องที่มี Python 3 และมี checkout ของ `pirate-force-server`
— มันหาจาก `%PF_SERVER_REPO%\src` ก่อน แล้วค่อยมองข้าง ๆ โฟลเดอร์ที่เก็บ `pf_bridge`
(`Pirate Force ServerProject\src` แล้ว `pirate-force-server\src`)
· **หาไม่เจอ หรือไม่มีล่าม = `[warn]` แล้วติดตั้งต่อ** (ไม่บล็อกบิลด์ดีเพราะเครื่องเกมไม่มีเครื่องมือ)
· **ตอบว่าไม่ใช่ `image_ok` = `[FAIL]` ไม่ copy อะไรเลย**
· `install.bat` ส่งแค่ `--dll` **ห้ามเติม `--client-dir`** — มันรันใต้เกต `[STOP]` ที่พิสูจน์ไปแล้วว่าโฟลเดอร์ปลายทาง
  **ไม่มี** `GameMaster.dll` ⇒ `--client-dir` จะได้ `verdict=missing` แล้ว exit 1 **ทุกครั้ง** = ปฏิเสธติดตั้งถาวร
· ถ้าจะเทียบ build กับ install (กับดัก "เทส DLL ตัวเมื่อวานซ้ำ") ให้รันมือ **หลัง** ติดตั้ง ด้วยคำสั่งข้างล่าง
· 🔴 **มันกัดที่บริดจ์ ไม่ใช่ที่เครื่องเกม** — เครื่องเกมปกติไม่มี checkout ของ `pirate-force-server` และไม่มี Python
  ⇒ ตกกิ่ง `[warn]` แล้วติดตั้งต่อ **ห้ามอ่านว่า "ภาพถูกตรวจแล้ว"** (pf-adversary รอบ `b8xrod` H3)
· 🔴 **checkout เก่าตอบไม่ได้อีกแล้ว** — ตัวตรวจพิมพ์บรรทัด `GM_PLUGIN_IMAGE build rules=...,manifest_id2`
  บอกว่าสำเนานั้นบังคับกฎอะไรบ้าง · `install.bat` บังคับว่าต้องมีคำว่า `manifest_id2` ถึงจะเชื่อคำว่า `image_ok`
  เหตุ: สำเนาก่อนรอบ `selrsl` พิมพ์ `verdict=image_ok` + exit 0 ให้ manifest ที่ id 1 = ทรงเดียวกับที่เกตนี้มีไว้จับ
  ⇒ เจอ verdict แต่ไม่เจอ `rules=` = ปฏิบัติเหมือน **ไม่มีเครื่องมือ** (`[warn]` แล้วไปต่อ) ไม่ใช่ "ผ่าน"
· `verdict=image_ok` บอกว่า **id ถูก** ไม่ได้บอกว่า **เนื้อ manifest ใช้ได้** — manifest ที่ id 2 แต่ว่าง/เวอร์ชัน CRT ผิด
  ยังตอบ 14001 อยู่ดี (pf-adversary รอบ `b8xrod` M5) สคริปต์พิมพ์ nonclaim นี้ออกจอเองแล้ว

รันมือจาก checkout ของ `pirate-force-server`:

```
set PYTHONPATH=src
py -3 -m pirateforce_foundation.gm.plugin_image_check --dll <build>\GameMaster.dll --client-dir "<ที่ติดตั้ง client>"
```

บันทึก **verdict + sha256** ลงใบเทสทุกครั้ง · exit code 0 เมื่อทุกพาธเป็น `image_ok` **และ**
ไฟล์ที่ติดตั้งข้าง client เป็นไฟล์เดียวกับที่เพิ่ง build (กันกับดัก "เทส DLL ตัวเมื่อวานซ้ำ")
มันบอก **ทุกปัญหาที่บล็อกพร้อมกัน** ไม่ใช่ทีละข้อต่อหนึ่ง build:
`missing` / `no_such_dir` / `not_pe` / `wrong_machine` / `not_a_dll` / `no_exports` /
`export_decorated` / `export_forwarded` / `export_missing` / `manifest_missing` / `image_ok`

## revision 3 แก้อะไร (สองข้อ HIGH ที่ pf-adversary ของสายนี้เจอในซอร์สของสายนี้เอง)

**H1 — `DllMain` เคยหา MSVCP90 ด้วย `GetModuleHandleW(L"msvcp90.dll")`**
คือวิธีค้นด้วยชื่อฐานแบบเดียวกับที่ revision 2 เพิ่งกำจัดทิ้งไปสำหรับ MSVCR90 ในไฟล์เดียวกัน
และมันแย่กว่าตรงที่ MSVCP90: `basic_string` ที่ `_SECURE_SCL=1` จอง `_Container_proxy` ผ่าน allocator
**แม้เป็นสตริงว่าง** ⇒ จองผ่าน instance A แล้ว client ทำลายผ่าน instance B ที่มัน pin ไว้ = cross-heap free
⇒ revision 3 ใช้ **การเดิน import table ของ client** ตัวเดียวกันกับทั้งสองฝั่ง (`FindClientImport`)
สองชั้น: (1) หา thunk ที่ client ผูกไว้กับ ctor ตัวนั้นตรง ๆ แล้ว**เรียกที่อยู่นั้นเลย**
(2) ถ้าไม่มี ให้หา instance ของ `msvcp90.dll` ที่ client ผูกอยู่ แล้ว `GetProcAddress` จากตัวนั้น
บรรทัด `[GM_PLUGIN]` ตอนโหลดบอกว่าใช้ทางไหน — เป็นหลักฐานที่ต้องแนบในใบเทส

**H2 — `PF_GM_SLOT0_TOUCH_PLUS4` เคย default = 1**
คือ build ปกติจะ construct ของขนาดที่ **ยังเดาอยู่** (24 หรือ 28 ไบต์ แล้วแต่ `_SECURE_SCL` ของ client
ซึ่งเราไม่รู้) ทับ `first+4 ..` ในหน่วยความจำของ client — `GM-IMG-012` **ไม่ได้บอกชนิดของ `+4`**
ถ้าของจริงเล็กกว่า = เขียนล้น (ถ้า `first` เป็น temporary บนสแตกผู้เรียก = ทับ return address ตอนคลิก)
⇒ default ใหม่ = **0** เขียนเฉพาะ `-1` ที่แถวนั้นเขียนไว้ตรง ๆ · การแตะ `+4` เป็นช่องที่ 3 แบบ opt-in

**revision 4 (รอบเดียวกัน หลัง pf-adversary รอบสองของสายนี้เอง) แก้เพิ่มอีกแปดข้อ:**
`FindClientImport` **ต้องกรองชื่อ descriptor เสมอ** — `??3@YAXPAX@Z` ไม่ได้มีแต่ MSVCR90 (MFC90 และโมดูล
anti-cheat ที่ inject เข้ามาก็ import) และชื่อ mangled ของ wstring ctor **เหมือนกันเป๊ะใน MSVCP80/90/100**
⇒ revision 3 ที่ค้นด้วยสัญลักษณ์อย่างเดียวคืนโมดูลผิดได้ = cross-heap free ตัวเดิมที่ H1 สั่งให้กำจัด
(วัดจริงด้วย harness ของ adversary) · โหมดค้นด้วยชื่อ dll ต้องยืนยันว่าโมดูลนั้น **export ตัวที่เราต้องการ**
ไม่ใช่เชื่อ thunk แรก · เจอ binding ที่หาโมดูลไม่ได้แล้วต้องค้นต่อ ไม่ใช่เลิกทั้งตาราง · **การ resolve
ทั้งหมดย้ายออกจาก `DllMain`** ไปทำตอน `CreateGameMaster` (GetProcAddress บน forwarded export เรียก
loader ซ้อน = ห้ามทำใต้ loader lock) และ `loaded` พิมพ์เป็นบรรทัดแรกสุด · `Announce` เหลือ
`OutputDebugStringW` ครั้งเดียวต่อบรรทัด และตัดช่องว่างซ้ำใน `loaded  build=` ⇒ grep ตรงกับที่เอกสารเขียน ·
ผลของ self-pin ถูกตรวจและรายงาน · slot `+0x08` **คืน pointer เดิม** (ไม่ใช่ NULL) เพราะกรณี hidden sret
ผู้เรียกทำลาย buffer ของตัวเองอยู่แล้ว การคืน NULL ไม่ได้กันอะไรแต่เพิ่ม NULL-deref
· ทางยอมแพ้เชิงโครงสร้าง (header ไม่ใช่ PE ฯลฯ) มีข้อความของตัวเองแล้ว

**ยังไม่แก้ (จงใจ ไม่ใช่ตกหล่น):** `build_vs2008.bat` check 3 ยัง grep `ret 8`/`ret 4` ทั้งอิมเมจ จึงผูกกับ
slot ไหนไม่ได้ และ "slot `+0x04` ต้องเป็น `ret` เปล่า" ยังเป็นคำสั่งให้คนอ่านเอง ไม่ใช่การตรวจ
— เขียน batch state machine โดยรันไม่ได้เลยเสี่ยงกว่าปล่อยไว้พร้อมบรรทัดนี้ · จองไว้ในไฟล์รอบแล้ว

**พ่วงมาด้วย (จาก MED list ใบ `0559`):** `client CRT: located` ไม่พิมพ์ก่อน `??2@YAPAXI@Z` ถูก resolve จริง
อีกต่อไป (resolve ตอนโหลด แล้วรายงานผลจริง) · ทุกลูปที่เดิน import table มีขอบเขตแล้ว (ลูปไม่รู้จบใต้
loader lock = client ไม่สตาร์ต ไม่ใช่แค่ปุ่มตาย) · slot `+0x08` เมื่อ resolve ctor ไม่ได้จะ **คืน NULL
พร้อมพิมพ์บอก** แทนการคืน buffer ที่ไม่ได้ construct (ดู `GM-IMG-014` blocker `NO_PINNED_CALL_ROUTE_FOR_SLOT8`
— ไม่มี route ไหนที่พิสูจน์แล้วว่าเรียก slot นี้ **ถ้าเห็นบรรทัดนี้บนจอ = หลักฐานใหม่ ต้องรายงาน**)

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
set EXTRA_DEFS=/D PF_GM_SLOT0_TOUCH_PLUS4=1
```

🔴 revision 3 **สลับค่า default ของ `PF_GM_SLOT0_TOUCH_PLUS4` จาก 1 เป็น 0** ⇒ บรรทัดที่สองข้างบน
ตอนนี้คือ "เปิด" ไม่ใช่ "ปิด" อย่างที่ revision 2 เขียนไว้ ใช้เฉพาะช่องที่ 3 ของตาราง "ลำดับสามช่อง" ด้านบน

🔴 **SHA256 ที่สคริปต์พิมพ์ ไม่ใช่ตัวพิสูจน์ว่าแฟล็กถึง compiler** (แก้คำของ revision 2/3 ที่เขียนกลับกัน):
DLL ฝัง `__DATE__`/`__TIME__` และ PE header มี link timestamp ⇒ **ทุก rebuild ทำให้ sha เปลี่ยนเสมอ**
ต่อให้ลืม `set EXTRA_DEFS` ก็ตาม ⇒ "sha เปลี่ยน = แฟล็กถึงแล้ว" เป็นข้อสรุปผิดที่พาไปบันทึกว่า
`GMUI_BASIC` ถูกหักล้างทั้งที่ไม่เคย build มัน
ตัวควบคุมจริงมีสองอัน: บรรทัด `EXTRA_DEFS=` ที่สคริปต์พิมพ์ก่อน build และบรรทัด `[GM_PLUGIN] key=` /
`slot +0x00 +4 init:` ใน DebugView · sha256 ใช้เพื่อพิสูจน์ว่า **ไฟล์ที่ติดตั้ง = ไฟล์ที่เพิ่ง build**
(หน้าที่ของ `plugin_image_check`) เท่านั้น

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
| 0b | บรรทัด `client CRT:` / `msvcp90 wstring ctor:` / `self-pin:` **หลังคลิก** | **client เรียก `CreateGameMaster` จริง** — มี `loaded` แต่ไม่มีสามบรรทัดนี้ = ยังไม่เคยถูกเรียก |
| 1 | ปุ่ม GM ยังโชว์ | ผ่านได้แม้ไม่ติดตั้งอะไรเลย ⇒ ไม่ใช่ตัวตัดสิน แต่ถ้า**หาย**แปลว่าผิดปกติหนัก |
| 2 | **คลิกแล้ว `GMUI_1` เปิด ถึง tab `GMUI_BASIC`** | ← ข้อที่ตัดสินทั้งหมด |
| 3 | ปิดเกมไม่แครช | ผ่านได้แม้ไม่ติดตั้งอะไรเลย ⇒ มีความหมายก็ต่อเมื่อข้อ 0 ผ่านแล้ว |

ข้อ 1 กับ 3 **ผ่านได้ด้วยการไม่ติดตั้ง DLL เลย** (วางผิดโฟลเดอร์ก็ผ่าน) — ข้อ 0 คือสิ่งที่ทำให้ทั้งชุดมี
ความหมาย ยังไม่มีใบ `GT` สำหรับสี่ข้อนี้ สายนี้เปิดใบ GT เองไม่ได้ ขอ chief เปิดให้

## ถ้าพัง — ไล่ตามลำดับนี้

| อาการ | ผู้ต้องสงสัย |
|---|---|
| **ไม่มีบรรทัด `[GM_PLUGIN]` เลย** | DLL ไม่ถูกโหลด: วางผิดโฟลเดอร์ · SxS manifest หาย (error 14001 — ต้องมี VC9 redistributable) · `dumpbin /exports` ซ้ำ |
| **~~`build_vs2008.bat` ทำ DLL ที่โหลดไม่ได้~~ (ปิดแล้ว revision 5)** | วัดจริงโดย ka1-A รอบ attended R304 (2026-09-02): สคริปต์เดิม**ไม่เรียก `mt.exe`** ⇒ DLL ไม่มี RT_MANIFEST ฝัง แต่ import `MSVCR90.dll` ⇒ loader ตอบ 14001 และไม่มีโค้ดในปลั๊กอินได้รันเลย · **ทุกบิลด์ที่สคริปต์ทำก่อน revision 5 โหลดไม่ได้** และมันเงียบสนิท (13,824 ไบต์ เช็คเดิมผ่านครบสามข้อ) · revision 5 ฝัง manifest ให้เอง แล้ว `check 0/4` **อ่านภาพที่จะถูกติดตั้งจริง** ยืนยันว่ามีเซกชัน `.rsrc` (สภาพที่ ka1-A วัดว่า **ไม่มี** บนบิลด์ที่โหลดไม่ได้) · การอ่าน RT_MANIFEST `#2` ด้วย `mt.exe` เป็นคำเตือน ไม่ใช่เกต เพราะยังไม่มีใครเคยรันคำสั่งนั้นเลย — ถ้ามันขึ้น `[warn]` ให้ตัดสินด้วย `plugin_image_check` ก่อนบูตเกม · `install.bat` ปฏิเสธถ้า `dumpbin` **บอกว่า** ไม่มี `.rsrc` และเตือนดัง ๆ ถ้าหา `dumpbin` ไม่เจอ (เครื่องเกมไม่มี VC) ⇒ ถ้าเจออาการนี้กับบิลด์ใหม่ แปลว่าเป็นสาเหตุอื่นในแถวบน ไม่ใช่ข้อนี้ |
| พิมพ์ `client CRT: NOT FOUND` | import walk ไม่เจอ `??3@YAXPAX@Z` ⇒ คืน NULL ⇒ สภาพเท่าเดิม |
| พิมพ์ `wstring ctor: NOT RESOLVED` | ชื่อ decorated ผิด — `dumpbin /exports msvcp90.dll` แล้วแก้ |
| โหลดแล้วแต่**คลิกยังเงียบ** | **key ผิด** (`GMUI_1` เทียบ `GMUI_BASIC` — ดู A/B ข้างบน) · หรือ gate `GMModule_Client+0x19` (`GM-IMG-005`) ปิดอยู่ |
| ปุ่ม GM **หายไป** | ไม่ใช่เพราะเราคืน NULL (`GM-IMG-002` ⇒ ปุ่มยังโชว์) แต่คือ fallback allocation ของ client เองล้ม — เรื่องอื่น |
| **แครชตอนคลิก** | ช่องที่ 3 (`PLUS4=1`) = การ init `+4` เขียนของขนาดที่เดาไว้ทับหน่วยความจำ client → กลับไปช่อง 1/2 · **ช่อง 1/2 ก็แครชตอนคลิกได้เหมือนกัน**: default ปล่อย `+4` ไม่ init ทั้งที่ `GM-IMG-012` บอกว่า fallback จริง init ให้ ⇒ ผู้เรียกอาจทำลายของที่ไม่ได้ init — **นี่คือผู้ต้องสงสัยที่หนึ่งของช่อง 1/2 ไม่ใช่ "คนละสาเหตุ"** (revision 3 เขียนผิดตรงนี้) เก็บ debug output ทั้งหมดมา |
| **แครชตอนปิดเกม** | อ่านบรรทัด `self-pin:` ก่อน — `FAILED` = pointer ที่ค้างอยู่ dangling ไม่ใช่เรื่อง heap · จากนั้นดู `client CRT:` ถ้าเขียนว่า **REFUSING** แปลว่ามีคนอื่นใน process import `??3@YAXPAX@Z` ไว้ (MFC90/anti-cheat) และเราปฏิเสธไปแล้ว = ไม่ใช่สาเหตุ · heap คนละตัวเป็นผู้ต้องสงสัยลำดับหลัง เพราะ revision 4 กรองชื่อ descriptor เป็น `msvcr90.dll` แล้ว |

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

## sha256 ของซอร์สในโฟลเดอร์นี้ (ตามธรรมเนียม `patches/` — revision 5)

```
eecd367419a6ae394d07188c6cd0799d263ba04c29f822336d74eb3fa24ee68b  GameMaster.cpp
9e2a3adc808189ba9ee31060469617e1eb32ab90c8d3094ec0a09a541aba2190  GameMaster.def
58b576f5fd89622493c774db829a5f16acd82b5b6bd4dc2826b17e065677171e  build_vs2008.bat
c48a340ed5b6a7364b3149ac75ea307a2588ad982c741b2ff83ac57b127d185a  install.bat
83c75d3955a7448e93d30a07511ff3a19b12f0217689c9d35ac8533bb582b9ea  find_mt.bat
```

บรรทัดบนคือ sha256 ของ **เนื้อในรีโป (LF)** ตามรูปแบบที่ revision 2 บันทึกไว้
🔴 `.gitattributes` บังคับ `*.bat text eol=crlf` ⇒ ไฟล์ `.bat` **บนดิสก์ฝั่ง Windows จะไม่ตรงกับค่าข้างบน**
ค่าที่ `certutil -hashfile` จะให้บนบริดจ์ (CRLF) คือ:

```
1a3157ade227cef1bfec8fe1e76d6c8a2ffbf63e097b6d7fda8a5524d25f83a4  build_vs2008.bat   (CRLF บนดิสก์)
0e192fa3d0b8be3f31948bd1a52d8b2e7e14727daefde2d4b05456a3fb44323b  install.bat   (CRLF บนดิสก์)
4033da06059525cb525d3a132239e3f60ae7b636fe5768f94d5bee1c28924b64  find_mt.bat   (CRLF บนดิสก์)
```

🔴 **ค่าทั้งหกอัปเดตในรอบ `hj2cry` พร้อมกับตัวสคริปต์เอง** — pf-adversary (D8) วัดได้ว่า revision 4
ทิ้งค่าเดิมไว้ทั้งชุดหลังแก้สคริปต์ ⇒ คนที่เช็คบนบริดจ์จะเห็นไม่ตรง แล้วสรุปผิด **ตามคำเตือนของไฟล์นี้เอง**
ว่าไฟล์ถูกแก้ระหว่างทาง ทั้งที่มันถูกต้อง · `find_mt.bat` เป็นไฟล์ใหม่ของรอบนี้ จึงไม่เคยมีค่าปักมาก่อน
**กฎ: แก้สคริปต์ในโฟลเดอร์นี้ ต้องอัปเดตบล็อกนี้ในคอมมิตเดียวกัน**
🔴 รอบ `selrsl` (2026-09-02T22:51+07:00): `find_mt.bat` เปลี่ยน (ข้อความ `[FAIL]` มีบล็อก `NEXT STEP`)
⇒ **ค่าของ `find_mt.bat` ทั้งสองบรรทัดอัปเดตในคอมมิตเดียวกันกับสคริปต์** · อีกสี่ค่าไม่ขยับ เพราะไฟล์อื่นไม่ถูกแตะ
· pf-adversary จับข้อนี้ได้เป็นรอบที่สอง (D3 ของรอบ `selrsl` หลัง D8 ของรอบ `hj2cry`) — กฎบรรทัดบนมีอยู่เพราะเรื่องนี้
🔴 รอบ `b8xrod` (2026-09-03T00:xx+07:00): `install.bat` เปลี่ยนเป็น revision 3 ⇒ **สองค่าของ `install.bat` อัปเดตในคอมมิตเดียวกัน**
· อีกสี่ค่าไม่ขยับ เพราะ `GameMaster.cpp` `GameMaster.def` `build_vs2008.bat` `find_mt.bat` ไม่ถูกแตะ
· pf-adversary จับข้อนี้ได้เป็น **รอบที่สาม** (H1 ของรอบ `b8xrod`) — ร่างแรกของรอบนี้ก็ทิ้งค่าเดิมไว้อีก

(revision 2 บันทึกไว้ชุดเดียวโดยไม่บอกว่าเป็นชุดไหน ⇒ ใครเช็คบนบริดจ์จะเห็นไม่ตรงและสรุปผิดว่าไฟล์ถูกแก้ระหว่างทาง)
