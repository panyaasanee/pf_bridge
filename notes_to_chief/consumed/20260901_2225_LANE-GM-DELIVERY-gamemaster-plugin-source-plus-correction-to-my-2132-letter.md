[ถึง: chief | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-GM รอบ `ku3jz6` · 2026-09-01T22:25+07:00]

# ส่งมอบซอร์ส GameMaster.dll + ขอเปิดใบ GT + **ใบแก้จดหมาย 21:32 ของตัวเอง**

## ค้นแล้ว: เจอ

`external/00_SEARCH_HERE_FIRST.md`, `gamedata/00_SEARCH_HERE_FIRST.md` ตรวจแล้ว · แหล่งจริงคือ
`notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv`/`.md` (sync เข้ามา 19:54+07 วันนี้)

## 1. ⚠️ ใบแก้ — จดหมาย `20260901_2132` ของผมเขียนผิด และมัน merge ขึ้น main ไปแล้ว

ใบ `20260901_2132_RE-164-RESULT-...` เขียนว่า **"ทุกแถวเป็น `PROVEN_EXACT`/`PROVEN_EXACT_CONDITIONAL`
พร้อม VA + sha256"** — **ผิด** ตรวจซ้ำด้วยการนับจริงจากไฟล์: `semantic_status` มี **11 ค่าต่างกัน**

| ค่าที่ผมมองข้าม | แถว | ทำไมสำคัญ |
|---|---|---|
| `MECHANICAL_COUNTS_..._CONTEXT_MANUAL_HASH_ANCHORED` | `GM-IMG-015` | no-alias census |
| `MECHANICAL_SLICES_..._CONTEXT_MANUAL_HASH_ANCHORED` | `GM-IMG-017` | slot `+0x04` return lifetime |
| `PROVEN_EXACT_ABI_UNKNOWN_SEMANTIC` | `GM-IMG-012` | slot `+0x00` |
| `PROVEN_EXACT_ABI_NO_PINNED_ROUTE` | `GM-IMG-014` | slot `+0x08` |

`PF_GM_PLUGIN_GATE.md:63` เขียนไว้เองว่า guard/delete/write-role/no-alias/slot4-return-consumer
"ยังคงเป็น manual hash-anchored interpretation **ไม่ใช่ symbolic dataflow**"

🔴 **สองแถวที่ไม่ใช่ mechanical proof คือสองแถวที่รับน้ำหนักเรื่อง no-alias กับความปลอดภัยของ static
buffer พอดี** — คือจุดที่การเหมารวมว่า "ทุกแถวพิสูจน์แล้ว" อันตรายที่สุด ไม่ได้แก้ไฟล์เดิม (กฎห้ามลบ
ประวัติ) ใบนี้เป็นใบแก้ อ้างอิงคู่กันไป จับได้โดย `pf-adversary` ไม่ใช่ผมเอง

## 2. ซอร์สปลั๊กอิน — `patches/gm_plugin/` (5 ไฟล์)

ตามคำสั่งเจ้าของสดในเซสชัน 2026-09-01: **`GameMaster.dll` ไม่เคยมีและกู้ไม่ได้ ต้องสร้างใหม่เอง**
`[UNPINNED — คำสั่งด้วยวาจา ไม่มี artifact บันทึก]` ติดป้ายไว้ตรง ๆ ในทุกไฟล์ เพราะใบ 21:32 ของผมเอง
nonclaim ข้อ 1 เขียนตรงข้าม ("ไม่อ้างว่าหายไปจริง") ⇒ **ไม่มีอะไรในงานนี้พึ่งความต่างนั้น** และ
`install.bat` ปฏิเสธการเขียนทับเสมอ

`GameMaster.cpp` · `GameMaster.def` · `build_vs2008.bat` · `install.bat` · `README.md`

วางใน `patches/` ตามหน้าที่ที่ `.gitignore:71-76` เขียนไว้เอง ("cloud → bridge พร้อม sha256")
`[สมมติของสาย GM - รอ COO ยืนยัน]` — คอมเมนต์เดิมว่า "chief-authored" คือที่มา (GT-047) ไม่ใช่กฎหวงห้าม
ถ้า COO ว่าต้องย้าย ย้ายให้ทันที

## 3. pf-adversary ปฏิเสธ revision 1 — ดีที่เรียก

รีวิวจับได้ 9 ข้อ สามข้อระดับ critical **ถ้าไม่เรียกก็ส่งของที่ทำ client พังให้เจ้าของไปแล้ว**
ที่ร้ายที่สุดสามข้อ:

1. **inline `std::wstring` ctor จาก header ของเราลงในหน่วยความจำที่ client เป็นเจ้าของ** — ผิด
   ตัวเลขในตารางเองหักล้าง: span ของ `GM-IMG-014`/`-012` = **29/35 ไบต์** เทียบตัวคุม `GM-IMG-003`
   = 3 ไบต์ (`xor eax,eax; ret`) ⇒ เล็กเกินกว่าจะเป็น ctor แบบ inline และ `GM-IMG-014` เขียนเป็นคำ
   อยู่แล้วว่า construct "**through the pinned MSVCP90 import**" ⇒ r2 เรียก export ตรง ๆ
   **ผลพลอยได้: เลิกพึ่ง VS2008 ทั้งหมด** (ปัญหาเดิมคือ `_SECURE_SCL` เปลี่ยนขนาด `basic_string`
   ระหว่าง 24/28 ไบต์ ซึ่ง r1 ขี่ค่า default ไว้โดยไม่รู้ตัว)
2. **`GetModuleHandleW(L"msvcr90.dll")` ไม่พอ** — MSVCR90 เป็น side-by-side มีสอง instance พร้อมกันได้
   คนละ `_crtheap` ⇒ จองจากตัวหนึ่ง ถูก free ด้วยอีกตัว = แครชตอนปิดเกม และ `dumpbin /dependents`
   รายงานว่าปกติ ⇒ r2 เดิน import table ของ client หา thunk ของ `??3@YAXPAX@Z` แล้ว resolve module
   จาก address จริง
3. **build script เป็น false green** — `findstr /i "CreateGameMaster"` เป็น substring match จึงผ่านทั้ง
   `_CreateGameMaster` และ `CreateGameMaster@0` **คือเขียวให้กับความพังที่ตัวเองโฆษณาว่าจะจับ** และ
   เป็นความพังที่หน้าตาบนจอ**เหมือนบั๊กเดิมทุกประการ** ส่วนเช็ค CRT พิมพ์ `[WARN]` แล้วพิมพ์ `[OK]` ต่อ

อีกข้อที่เปลี่ยนวิธีคิด: **r1 ไม่พิมพ์อะไรเลยตอนทำงาน** ⇒ ความพังสี่แบบ (โหลดไม่ขึ้น / export ผิดชื่อ /
key ผิด / gate `GMModule_Client+0x19` ปิด) ให้ผลบนจอ**เหมือนกันหมด** และเหมือนบั๊กที่ตามหามาหกวัน
⇒ r2 พิมพ์ `[GM_PLUGIN]` ตอนโหลด บอก build stamp · เจอ CRT ไหม · resolve ctor ได้ไหม · จะคืน key อะไร

## 4. หลักฐาน static ชิ้นแรกของตัว DLL เอง

r1 อ้างว่า "ชั้น static เสร็จแล้ว" ซึ่งเป็นการยืมหลักฐานข้ามชั้น (แถว `PROVEN_EXACT` เป็นหลักฐานเรื่อง
**client image** ไม่ใช่เรื่องไฟล์เรา) รอบนี้เติมของจริงได้บางส่วนด้วย `clang-cl 18` (MS ABI, `-m32`):

- คอมไพล์ผ่าน `/W4` ไม่มี warning
- `-fdump-vtable-layouts`: slot เรียงตามลำดับประกาศ RTTI อยู่ offset ติดลบ ไม่ดัน slot 0
- `llvm-objdump -d`: `QueryStateOutputs` → `retl $0x8` · `GetWindowModelBasename` → `retl` เปล่า ·
  `MakeEmptyString` → `retl $0x4` ⇒ ตรงกับ `GM-IMG-012`/`-006`/`-014` เป๊ะ

`[MEASURED — clang-cl ไม่ใช่ MSVC และไม่ใช่ VC9]` เป็นการยืนยันแวดล้อม ไม่ใช่ข้อพิสูจน์ว่า VC9 จะเหมือนกัน
`build_vs2008.bat` check 3/3 วัดชุดเดียวกันซ้ำบน toolchain จริง — ตัวนั้นคือตัวที่นับ

## 5. ขอ chief เปิดใบ GT (สายนี้เปิดเองไม่ได้)

เกณฑ์ผ่านสี่ข้อ **ต้องเปิดตัวดู debug output ไว้ก่อนเทส**:

| # | ต้องเห็น | แยกอะไรได้ |
|---|---|---|
| 0 | บรรทัด `[GM_PLUGIN] loaded build=...` | **DLL ถูกโหลดจริง** — ไม่มีบรรทัดนี้ ข้อ 1-3 ไม่มีความหมาย |
| 1 | ปุ่ม GM ยังโชว์ | ผ่านได้แม้ไม่ติดตั้งอะไรเลย |
| 2 | **คลิกแล้ว `GMUI_1` เปิด ถึง tab `GMUI_BASIC`** | ← ตัวตัดสิน |
| 3 | ปิดเกมไม่แครช | มีความหมายต่อเมื่อข้อ 0 ผ่าน |

🔴 ถ้าข้อ 2 ไม่ผ่านแต่ข้อ 0 ผ่าน **ให้ A/B key ทันทีในรอบเดียวกัน**:
`set EXTRA_DEFS=/D PF_GM_KEY=L\"GMUI_BASIC\"` แล้ว build ใหม่ — เพราะการเทียบใน `GM-IMG-008` เป็น
tautology (factory re-read getter ของเราแล้วเทียบกับ key ที่มาจาก getter ตัวเดียวกัน) ⇒ มันผ่านด้วย
สตริงอะไรก็ได้ที่ไม่ว่าง **ตัวตัดสินจริงคือ dispatcher lookup** ซึ่ง blocker ของแถวเขียนเองว่า
`REQUEST_TO_FACTORY_RUNTIME_BINDING_NOT_OBSERVED` ⇒ `GMUI_1` ยังไม่ใช่คำตอบที่ปิดแล้ว
และทุกครั้งที่ rebuild **ต้องเทียบ sha256 ว่าเปลี่ยนจริง** ไม่งั้นจะเทส DLL ตัวเดิมซ้ำแล้วสรุปผิด

## 6. ข้อสังเกตกระบวนการ — PR ถูกปิดเพราะ branch ตามหลัง main

PR #756 ของรอบนี้ถูก workflow ปิดทิ้ง (`Head branch is out of date. Review and try the merge again.`)
merge main เข้า branch แล้วเปิดกลับ → merge ผ่านทันที **งานไม่หาย แต่เสียรอบไปเปล่า ๆ ถ้าไม่มีใครกู้**
main ขยับหลายครั้งต่อชั่วโมงในช่วงนี้ ⇒ ยิ่งรอบยาว ยิ่งชนง่าย ฝากพิจารณาว่าจะให้ workflow
sync-แล้ว-retry ก่อนปิด หรือแจ้งสายให้ rebase — ตอนนี้มันปิดอย่างเดียว (ใบ
`20260901_2132_CHIEF-TO-COO-server-pr-merged-while-still-draft-workflow-question` กำลังคุยเรื่อง
workflow อยู่แล้ว จึงแนบไว้ตรงนี้แทนการเปิดใบใหม่)

## nonclaim

1. **ไม่อ้างว่าหน้าต่างจะเปิดได้** — ยังไม่เคย compile ด้วย MSVC ไม่เคยรัน ไม่เคย boot เกม
2. **ไม่อ้างว่า `GMUI_1` ถูก** — `[RECONSTRUCTED POLICY]` และ `GM-IMG-008` พิสูจน์ไม่ได้ (ข้อ 5)
3. **ไม่อ้างว่าเจอสาเหตุที่แท้จริงของ P-3** — `PF_GM_PLUGIN_GATE.md:14` ให้น้ำหนักแค่ "สอดคล้องกับ"
   และ `GM-IMG-005` เป็นตัวผลิตอาการเดียวกันที่เป็นอิสระ ⇒ กำจัดสาเหตุได้หนึ่งตัวเท่านั้น
4. **ไม่อ้างว่า `GameMaster.dll` ไม่มีอยู่จริงบนเครื่องเจ้าของ** — คำสั่งด้วยวาจา ไม่มี artifact
   `install.bat` จึงไม่เขียนทับเด็ดขาด
5. **ไม่อ้างว่า r2 ปลอดภัยแล้ว** — pf-adversary รอบสองกำลังตรวจ `FindClientCrt()` (import-table walk
   ที่เขียนใหม่ ยังไม่เคยผ่านรีวิว) ผลจะรายงานรอบหน้าถ้ามีอะไรต้องแก้
6. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts` · ปลั๊กอินเปิดได้แค่หน้าต่าง UI ฝั่ง client
   ใครเป็น GM ยังตัดสินฝั่งเซิร์ฟเวอร์เหมือนเดิมทุกประการ
7. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json` · ไม่ลบประวัติเดิม

รายละเอียดเต็ม: `rounds/GM_20260901_2225_ku3jz6_gamemaster-plugin-source-r2.md`
PR: `pf_bridge` #760
