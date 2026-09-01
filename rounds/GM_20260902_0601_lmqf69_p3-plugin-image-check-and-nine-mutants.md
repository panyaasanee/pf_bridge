# LANE-GM รอบ `lmqf69` — 2026-09-02T06:01+07:00
# P-3: อาการเดียวบนจอ กลายเป็นสิบเอ็ดคำตอบที่ตัดสินได้ก่อนบูตเกม

## NOW.md ข้อไหนขยับ

**P-3 (ปุ่ม GM กดแล้วต้องเปิดใช้งานได้จริง)** — ขยับ **ครึ่งเดียว และเป็นครึ่งเครื่องมือ ไม่ใช่ครึ่งผลลัพธ์**

- ที่ขยับ: การ **แยกสาเหตุ** ของอาการ "ปุ่มโชว์ คลิกเงียบ" — จากเดิมที่ห้าสาเหตุให้ผลบนจอเหมือนกันหมด
  ตอนนี้สาเหตุที่ตัดสินได้จากไฟล์ (DLL ไม่มี / export ถูก decorate / export เป็น forwarder /
  build 64-bit / ไม่ใช่ DLL / ไม่มี manifest ⇒ loader ปฏิเสธ 14001) แยกออกจากกันได้ก่อนบูตเกม
  พร้อม sha256 และคำสั่งเดียวที่รันได้บนสะพาน
- ที่ **ไม่** ขยับ: ปุ่มยังกดไม่ติดเหมือนเดิม รอบนี้ไม่มีหลักฐาน client-observable ใหม่แม้แต่ชิ้นเดียว
  และยังไม่มีใบ GT ของปลั๊กอิน (chief บริโภคใบส่งมอบ `2225` แล้วเขียนไว้เองว่า "no round budget")

**P-1 / P-2 ไม่ขยับ:** P-1 เป็นของ LANE-B + chief (`COO 0254`/`0348`) · P-2 อยู่ที่ Codex (P0-3 quest mark)
**GM-A ไม่ขยับ:** โค้ดจบแล้วบน main รอ Panya รัน `GT-192` — ตามกฎใหม่ใน `NOW.md` ไม่ใช่ตัวบล็อกสาย
**GM-B ไม่ขยับ:** ติดที่ **chief** — grep `SPEED DENIED` ทั้ง repo เซิร์ฟเวอร์ = ไม่เจอ ⇒ PR ทางที่ 1
(`COO-DECISION 0345`, กำหนด R299) ยังไม่ลง `main` ⇒ เงื่อนไข "LANE-GM ยืนยัน 9 ทางปฏิเสธ" (`COO 0346`)
ยังไม่เปิด · **ว่างเพราะรอ chief ใบ `0345`** — ไม่ใช่ "ไม่มีอะไรทำ" และรอบนี้ก็ไม่ได้ว่าง

## ต้นรอบ (ตามลำดับที่ prompt สั่ง)

1. `pf_bridge/NOW.md` อ่านเป็นไฟล์แรก · `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง
2. ล็อกรอบ: PR ที่เปิดค้างหัวข้อขึ้นต้น `[LANE-GM]` ทั้งสอง repo = **ไม่มี** (เห็น `[LANE-A]` server#538,
   `[LANE-E]` bridge#797, `[LANE-B]` bridge#795, `[LANE-A]` bridge#794 — ไม่ใช่ล็อกของสายนี้ ไม่แตะ)
   ⇒ ยึดล็อกด้วย commit เปล่า + draft PR: bridge **#799** · server **#539**
3. ADDENDUM v2 ข้อ A — ชะตา PR รอบก่อน: bridge **#793 merged=true** · server **#536 merged=true**
   ⇒ ไม่ต้องกู้อะไร (ยืนยันด้วย GitHub API ไม่ใช่จาก `rounds/`)
4. ADDENDUM v2 ข้อ B — กล่องจดหมาย: `grep ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt` = **0 ใบ**
   (`COO 0346` บริโภคไปแล้วรอบ `ibxaf0`) ⇒ ไม่มีใบค้างของสายนี้
5. คิวงาน: ไม่มีใบจ่าหน้าสายนี้ค้าง · ไม่มี CORE-REQUEST-GM ค้างตอบ · backlog ของไฟล์รอบก่อนชี้ P-3
   ⇒ หยิบ P-3 ตาม `NOW.md` (ไม่มีใบ CLAIM ของสายอื่นเรื่องนี้ในกล่อง — ใบ CLAIM ล่าสุดเป็นของ LANE-A/B และ consumed แล้ว)

## ค้นแล้ว (กฎ "ค้นก่อนถอด")

- `external/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ** (ไม่มี GameMaster / plugin / GM-IMG ในสารบัญ)
- `gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ**
- แหล่งจริง: `notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv` (20 บรรทัด,
  sha256 `a5f3fdeb6a830b06e3eb9dceff85fc762459ca3e4f9e7ada152937ef1c898509`) + `.md` คู่กัน
- `SPEED DENIED` ใน `pirate-force-server` — **ค้นแล้ว: ไม่เจอ**

## ของที่สร้าง

`src/pirateforce_foundation/gm/plugin_image_check.py` — PE32 reader ด้วย stdlib ล้วน อ่าน export directory,
import descriptor table และ resource directory เอง คืน **verdict เดียวต่อไฟล์** พร้อม sha256 ขนาด และ
**ทุกปัญหาที่บล็อก ไม่ใช่แค่ข้อแรก**: `missing` · `no_such_dir` · `unreadable` · `not_pe` · `wrong_machine` ·
`not_a_dll` · `no_exports` · `export_decorated` · `export_forwarded` · `export_missing` ·
`manifest_missing` · `image_ok` · เทียบไฟล์ที่ build กับไฟล์ที่ติดตั้ง แล้ว **exit 1 ถ้าไม่ใช่ไฟล์เดียวกัน**

`tests/test_gm_plugin_image_check.py` — 44 เทส บนภาพ PE32 สังเคราะห์ที่ประกอบทีละฟิลด์

## pf-adversary ปฏิเสธ revision 1 — 12 ข้อ (สรุปเฉพาะที่เปลี่ยนของจริง)

| # | สิ่งที่ผิด | แก้แล้วเป็น |
|---|---|---|
| T1-4 | **ชุดเทส 30 ใบล้มไม่ได้** — mutant 6 ตัวรอด 30/30 เพราะ fixture มีเซกชันเดียว `VirtualSize == SizeOfRawData` และ directory ครบ 16 เสมอ | fixture 3 เซกชัน · export dir อยู่เซกชันที่ **สอง** · เซกชันหนึ่ง VSize<raw อีกเซกชัน VSize>raw · `directory_count` เป็นพารามิเตอร์ (และ optional header ยาวตามมัน) |
| T1-1 | พาธพิมพ์ผิด/มีช่องว่างไม่ใส่คำพูด ⇒ พิมพ์ว่า "RE-164 ยืนยันแล้วสำหรับเครื่องนี้" | ไดเรกทอรีไม่มีอยู่ = verdict ของตัวเอง (`no_such_dir`) ข้อความบอกตรง ๆ ว่า **ไม่ได้แปลว่าอะไรเลยเกี่ยวกับ client** |
| T1-3 | export name ที่มีไบต์สูง ⇒ `errors="replace"` ⇒ U+FFFD ⇒ `UnicodeEncodeError` ตาย**กลางรายงาน**บนคอนโซล cp874 | `errors="backslashreplace"` + เทสที่ปักไบต์ `0xE9` ลงในชื่อ export จริง |
| T1-2 | build กับ install คนละไฟล์ ⇒ พิมพ์เตือนแล้ว **exit 0** (กับดักเทส DLL เมื่อวานซ้ำ ผ่านเขียว) | mismatch ⇒ `verdict=stale_install` และ **exit 1** |
| T1-5 | `/MT` build ถูกตี `crt_missing` ทั้งที่ revision 2 จองจาก CRT ของ **client** อยู่แล้ว | ลดเป็น advisory |
| T1-6 | `image_ok` ครอบ forwarded export และ build ที่ไม่มี RT_MANIFEST (loader 14001) | อ่าน `AddressOfNameOrdinals`+`AddressOfFunctions` ⇒ `export_forwarded` · อ่าน resource dir ⇒ `manifest_missing` · จับ mangling `?Name@@...` เพิ่ม |
| T1-7/8/9 | ข้อความอ้างเรื่อง loader จาก fact ระดับ filesystem · คอมเมนต์อ้าง `verdict_is_ok` ที่ไม่มีอยู่จริง · คอมเมนต์อ้างว่า `_need` กันการอ่านข้ามเซกชัน (มันกันแค่ขอบไฟล์) | แก้ถ้อยคำทั้งสาม · เพิ่มการปฏิเสธ RVA ที่ตกใน uninitialised tail จริง ๆ |
| T1-10 | คำสั่งใน docstring รันไม่ได้ (ไม่มี `PYTHONPATH=src`) | เขียนวิธีรันจริงไว้ในหัวไฟล์ + ขอ chief ใส่ใน README/build script (ไม่ใช่เขตสายนี้) |
| T1-11 | verdict เดียว = เจอปัญหาทีละข้อต่อหนึ่ง build | `problems` ทั้งชุด พิมพ์เป็น `also_problem=` |

## ตัวเลขที่วัดได้จริงรอบนี้

- **mutation: ลอง 9 ตัว ตาย 9 ตัว** (ก่อนแก้ 6/6 รอด) — `span=raw_size` · `span=virtual_size` ·
  `sections[:1]` · ตัด ordinal-only guard · ตัด `NumberOfRvaAndSizes` bound · ตัด no-import early return ·
  ตัดการปฏิเสธ uninitialised tail · ตัดการตรวจ forwarder · manifest คืน True เสมอ
- **เขียว(cloud sanity):** `pytest tests -q` = **6922 passed, 327 skipped** (ก่อนแก้ adversary)
  และ `-k gm` = **1422 passed, 4 skipped, 617 subtests** (หลังแก้ครบ)
- **ตรวจข้ามกับ PE จริง** ที่มีอยู่บนเครื่องนี้ (launcher ของ distlib, MSVC สร้าง): machine · PE32/PE32+ ·
  DLL flag · section walk ที่ VSize/raw ไม่เท่ากัน · import names · RT_MANIFEST อ่านถูกทั้งหมด

## ที่ยังเป็นรู (เขียนไว้ให้รอบหน้าเห็น)

1. **ไม่มี PE fixture จริงใน repo** — ทางเดิน export directory ถูกยืนยันด้วยไบต์สังเคราะห์เท่านั้น
   (ไฟล์ PE จริงบนเครื่องนี้ไม่มี export เลย) adversary เสนอให้เก็บ `.pyd` ของ MSVC ~220KB เป็น fixture
   สายนี้ **ไม่ทำ** รอบนี้: ไฟล์ไบนารีที่ไม่เกี่ยวกับโปรเจกต์เข้า repo ควรมีคนเคาะก่อน
2. **สองข้อ HIGH ในซอร์ส DLL ยังไม่ถูกแก้** — `GetModuleHandleW(L"msvcp90.dll")` (H1) และ default ของ
   `PF_GM_SLOT0_TOUCH_PLUS4` (H2) · **ติดที่: ยังไม่มีคำตัดสินว่า `patches/gm_plugin/` เป็นเขตใคร**
   (ใบ `2225` ข้อ 2 ค้างมาตั้งแต่ 2026-09-01T22:25+07:00) + clone นี้ไม่มี Windows SDK
   ⇒ เปิด ASK-COO ใบ `20260902_0600` ให้เคาะ ระหว่างรอถือว่า **ห้าม build ตัวปัจจุบันไปลง client**
3. **ยังไม่มีใบ GT ของปลั๊กอิน** — ติดที่ **chief** (บริโภคใบ `2225` แล้วเขียนเองว่าไม่มีงบรอบนั้น)
4. **เมทริกซ์สี่ build ไม่มีกติกาหยุด** — เสนอลำดับ 3 ช่อง + กติกาหยุดไว้ในใบ ASK-COO `0600`
   ติดป้าย [สมมติของสาย GM - รอ COO ยืนยัน]

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

รันคำสั่งเดียวบนสะพาน **ก่อนเปิดเกม** แล้วรู้ว่าไฟล์ปลั๊กอินที่กำลังจะเทสมีปัญหาระดับไฟล์ข้อไหนบ้าง
พร้อม sha256 ของไฟล์ที่ **ติดตั้งจริงข้าง client** ไม่ใช่ไฟล์ใน build directory — เมื่อวานคำตอบเดียวที่มีคือ
"คลิกแล้วเงียบ" ซึ่งใช้แยกอะไรไม่ได้เลย และ `dumpbin` ก็ดูได้เฉพาะไฟล์ที่เพิ่ง build บนเครื่องที่มี VC เท่านั้น

## nonclaim

1. **ไม่อ้างว่า P-3 ขยับในสายตาเจ้าของ** — ปุ่มยังกดไม่ติด รอบนี้ไม่มีหลักฐาน client-observable ใหม่เลย
2. **`image_ok` ไม่ใช่ใบรับรอง** — เป็นคำพูดเรื่องไบต์ในไฟล์ ไม่ใช่ว่าหน้าต่าง GM จะเปิด
3. **ไม่อ้างว่า `GameMaster.dll` หายจริงบนเครื่องเจ้าของ** — ยังเป็นข้อสังเกตเชิงปฏิบัติการตาม `RE-164`
   และรอบนี้ **จงใจ** ทำให้เครื่องมือปฏิเสธที่จะสรุปแทนคน (verdict `no_such_dir` แยกจาก `missing`)
4. ไม่อ้างว่า parser ครอบคลุมทุก PE จริง — ดู "ที่ยังเป็นรู" ข้อ 1 · delay-import (directory 13) ไม่ได้เดิน
5. ไม่อ้างว่าได้ compile หรือรัน `GameMaster.cpp` — H1/H2 มาจากการอ่านซอร์ส + `PF_GM_PLUGIN_GATE` เท่านั้น
6. **GM ข้ามขั้นไหน:** รอบนี้ไม่ได้ใช้ GM ข้ามขั้นอะไรเลย (ไม่มีการบูตเกม ไม่มีเฟรม) เครื่องมือที่สร้าง
   เป็นทางลัดไปถึง "สภาพที่จะเทส" ของ P-3 ไม่ใช่หลักฐานว่า P-3 ทำงาน
7. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts` · client ยกระดับตัวเองไม่ได้ · ไม่ประกาศ milestone
8. ไม่แตะ `runtime.py` / `app.py` / `pf_login_game_server_v141.py` / canonical DB /
   `scenarios/world_*.json` / `scenarios/combat_*.json` / `gm/say_wire.py` / `gm/chat_command_action.py`
   (สองอันหลังตามคำสั่ง `COO-DECISION 0346`) · ไม่ลบประวัติเดิม
9. หมายเหตุกระบวนการ: ตอนยึดล็อก คำสั่ง `cd` ของสายนี้ผิดหนึ่งบรรทัด ทำให้ branch ชื่อ
   `claude/gallant-pasteur-lmqf69` (ชื่อของฝั่งเซิร์ฟเวอร์) ถูก push ขึ้น **pf_bridge** ไปหนึ่งใบ
   มีแต่ commit เปล่า ไม่มี PR ผูก · ลบทิ้งไม่สำเร็จ (remote hung up) จึงปล่อยไว้และบันทึกไว้ตรงนี้แทน
   การ retry — ใครเห็น branch นั้นบน bridge ลบได้เลย

## ไฟล์ที่แตะ

`pirate-force-server`: `src/pirateforce_foundation/gm/plugin_image_check.py` (ใหม่) ·
`tests/test_gm_plugin_image_check.py` (ใหม่) · `docs/GM_LANE.md`
`pf_bridge`: จดหมาย 2 ใบ (`0559` ถึง chief, `0600` ถึง COO) + ไฟล์รอบนี้

## PR

`pf_bridge` #799 · `pirate-force-server` #539
