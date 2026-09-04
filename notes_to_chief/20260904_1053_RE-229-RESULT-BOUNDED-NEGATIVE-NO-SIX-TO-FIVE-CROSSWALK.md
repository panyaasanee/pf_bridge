[ถึง: LANE-DB | cc: chief cloud · COO | จาก: RE runner local · 2026-09-04T10:50:03+07:00]

# RE-229 RESULT — ไม่พบ crosswalk ที่พิสูจน์ six-axis `s_SCORE` ไป five-field ActorAttr

## สถานะ

**DONE / BOUNDED-NEGATIVE (static-only; method ceiling)** — ปิดเฉพาะคำถามที่ R334 เปิดใหม่: corpus และ client image ปัจจุบันยืนยันว่า `s_SCORE` เป็นคะแนนแสดงผลหกแกนของหน้าสร้างตัวละคร แต่ไม่พบ field/consumer ที่ผูก component ทั้งหกเข้ากับ ActorAttr wire fields ห้าช่อง จึงระบุไม่ได้อย่างมีหลักฐานว่าแกนใดหาย และห้ามใช้สมมติฐาน `AGI -> DEX` หรือทิ้ง `CHA` เป็น crosswalk

- ticket START: `2026-09-04T10:41:18.756+07:00`
- ticket block SHA-256: `BF5AEF547795C8D49F0830153C82199AB48184D01D70A103756F10C51CBA28A7`
- client: `GameClient.local.bin` SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
- reused verified result: `20260828_0815_RE-122-RESULT-SCORE-IS-SIX-AXIS-MP-UNPROVEN.md` SHA-256 `59480125E049F0C17D3D1F7DC69886CC57799BCEAC23E627E4A96CD7CBC3B88C`
- verifier: `staged/verify_re122.py` SHA-256 `D16A4024C104367DB9AC70DE1B0271C85D22058F271883C2D02D2DF8DDBB329D`; rerun result `PASS 44/44`

## Mandatory searches

ค้น `pf_bridge/external/` ครบ 2,683 files / 930,201,065 bytes, manifest fingerprint SHA-256 `9AFA09D3832F9A427C2E818C3ADBC6B3734C8479DA194101868CB5CD579F9C6A` โดยใช้ terms `s_SCORE`, ชื่อ `STATUS_*` ทั้งหก, `n_AGILITY`, `n_DEXTERITY`, `CHARCREATE_CLASS`, `POTENTIAL` และ terms ของ RE-232 ที่แชร์ manifest รอบเดียวกัน

- พบ table/schema และรายงาน/binding เดิมที่ยืนยันชื่อ field กับตำแหน่ง ActorAttr
- ไม่พบ field หรือ consumer ที่ crosswalk component ของ `s_SCORE` ไป STR/CON/DEX/INT/PER

ค้น `pf_bridge/gamedata/` ครบ 1,109 files / 15,319,585 bytes, manifest fingerprint SHA-256 `E3ECBFC23FF7EC8D7490BBD9343ED1F0528C5333328942AC2C988EBEC39196F9`

- พบ `CHARCREATE_CLASS.s_SCORE` ที่ schema offset `+8`, type string; class 1 มี `4;3;4;1;1;2`
- พบ `POTENTIAL` ซึ่งมีชื่อคอลัมน์ห้าแกน แต่ตารางมี 0 data rows และไม่มี field ผูกไปยังลำดับหกค่า
- ไม่พบ crosswalk หรือ formula เพิ่มเติมในขอบเขต manifest นี้

## คำตอบ component-by-component

UI model `GameClient/Data/GUI/Model/Login_CharCreate_Main.model` SHA-256 `EEF1EB1A45929D6770E1FE4E7DFAD31208A3DE99CDE768A6103B35C6E206066C` ระบุแกนเรียงเป็น:

1. `STATUS_STR` — พิสูจน์ได้ว่าเป็นแกนแสดงผล; ไม่พบ consumer ที่เขียน ActorAttr STR
2. `STATUS_AGI` — พิสูจน์ได้ว่าเป็นแกนแสดงผล; ไม่พบ consumer/crosswalk ที่แปลงเป็น ActorAttr DEX
3. `STATUS_CON` — พิสูจน์ได้ว่าเป็นแกนแสดงผล; ไม่พบ consumer ที่เขียน ActorAttr CON
4. `STATUS_INT` — พิสูจน์ได้ว่าเป็นแกนแสดงผล; ไม่พบ consumer ที่เขียน ActorAttr INT
5. `STATUS_PER` — พิสูจน์ได้ว่าเป็นแกนแสดงผล; ไม่พบ consumer ที่เขียน ActorAttr PER
6. `STATUS_CHA` — พิสูจน์ได้ว่าเป็นแกนแสดงผล; ไม่พบหลักฐานว่าถูกทิ้งหรือถูกนำไปใช้กับ wire field อื่น

ดังนั้นคำตอบของ “แกนใด disappear” คือ **UNPROVEN** ไม่ใช่ `CHA` โดยอัตโนมัติ และการที่ชื่อสี่แกนตรงกันไม่ได้พิสูจน์ว่าค่าใน `s_SCORE` เป็น base ActorAttr values

## Binary/table boundary

- binary มี UTF-16 literal `CHARCREATE_CLASS` ที่ VA `0x00F0C650` และ direct pointer xrefs 18 จุด; path ที่ตรวจซ้ำครอบคลุม acquisition/UI initialization และ class name/icon/appearance consumers
- function `[0x00501E30,0x005020BA)` span SHA-256 `5682D748AC37E777F82F178CDFC260D5CEE321A2D5BA676BE82B2546B44F6A95` ใช้ class content/name/icon แต่ไม่ให้ six-to-five mapping
- function `[0x00503510,0x00503780)` span SHA-256 `A99E1D913D35B7782E657893A7411ABD3F436E4161672C2F3143C2CBBA036FB5` acquire ตารางและ bind controls แต่ไม่ให้ six-to-five mapping
- รายงาน static ที่ pin ActorAttr getters/wire serialization (`PF_STATS_PROG001_CHARACTER_STATS_AND_PROGRESSION_STATIC_20260818.md`) SHA-256 `CC8B701CB988B74EE1A95FFD40D33D22B220F2D81EC72538FEF0BDCB16ABF05E` ยืนยันห้า resident fields STR/CON/DEX/INT/PER แต่ระบุ `AGILITY <-> DEX` เป็นเพียง cardinality inference
- `PF_GAMEDATA_COLUMNS.tsv` SHA-256 `6F1A00DC9660038F651007397244C575B321BEAF756675FD0E437C3131294D89`; `PF_ATTR_COMPUTED_SEMANTICS.tsv` SHA-256 `6813A941D672A54F3F2B75D2AAF2715812D713A855F4C18D10CEED0FB8509C8A`

ผลลบนี้จำกัดอยู่ที่ exact tables, full-tree manifests, direct named-table xref census, pinned UI model และ bounded functions/reports ข้างต้น ไม่ได้ใช้ linear disassembly เป็นหลักฐานผลลบแต่เพียงอย่างเดียว

## Nonclaims

- ไม่กล่าวว่า `s_SCORE` ไม่มีผลต่อ UI; มันเป็น six-axis display score ที่พิสูจน์แล้ว
- ไม่กล่าวว่า `CHA` ต้องหาย หรือ `AGI` ต้องเท่ากับ `DEX`; ทั้งสองเป็นสมมติฐานที่ยังไม่มี crosswalk field/consumer
- ไม่กล่าวว่า ActorAttr wire positions ผิด; ปัญหาคือไม่มี provenance ของค่าที่จะใส่
- ไม่ใช้ผล client-observable เพื่อพิสูจน์ wire/DB และรอบนี้ไม่มีเกม/server boot หรือ capture ใหม่
- ไม่แก้ client/server/source/external/gamedata/queue/canonical DB

## BUILD_IMPACT

`BUILD_IMPACT: hard guard / keep current fallback` — LANE-DB ต้องคง `DEFAULT_PRIMARY_STAT = 100` และห้าม seed ค่า `4;3;4;1;1` หรือ permutation ใดจาก `s_SCORE` ลง ActorAttr. Piece 2 ของงาน stat seeding ยังคง blocked จนมี authoritative crosswalk field/consumer หรือ capture ที่ผูก six UI axes กับ five wire fields โดยตรง

นี่เป็น **method ceiling** ไม่ใช่ time checkpoint: ห้าม rerun RE-229 ด้วย corpus/image เดิมจน chief เปลี่ยน objective หรือเพิ่ม artifact ที่มี crosswalk อย่างมีสาระ
