# ka1-A — GT-219 ขั้น A + สคริปต์รันจริงครั้งแรก: (ก) `image_ok` EXIT=0 · (ข) ไม่มีในเครื่อง (ตามคำทำนาย) · `find_mt.bat` เจอ mt.exe · `install.bat` ติดตั้งแล้ว rollback แล้ว · ขั้น B (กดปุ่ม GM) ยังรอรอบ attended

**ADDRESSEE: chief** (ผู้บริโภคผลตามใบ) · cc: LANE-GM (เจ้าของ P-3) · COO
**เวลา:** 2026-09-04 15:05-15:07 +07:00 · jobs `1497_gt219_stepA_recheck_and_scripts` + `1497b_gt219_rollback_and_hashes` (log ใน `outbox\`) · ไม่มีเซิร์ฟเวอร์ ไม่มีเกม ไม่แตะ DB · checkout ที่รันตัวตรวจ = worktree `Pirate Force ServerProject` (main)

## RECHECK
1. **PASS** — `patches\gm_plugin\GameMaster.dll` size=**14848** sha256=`4a0ecb5817c15b0bf08964bc16972bc7340666357c494e9d0308ee9ce72d743b` (certutil ใน install.bat + Get-FileHash ใน 1497b ตรงกัน)
   (job 1497 พิมพ์ `RECHECK1=FAIL` ผิดเพราะฟังก์ชันชื่อ `H` ของผมถูก alias `Get-History` ของ PowerShell บัง — ค่า sha ที่พิมพ์ในบรรทัดอื่นของ log เดียวกันยืนยันว่าไฟล์ถูก · บทเรียนเครื่องมือ ไม่ใช่ผลวัด)
2. **NOT FOUND (ตามคำทำนาย)** — `GameMaster*.dll` ทั้งโฟลเดอร์ `C:\Users\Panya\Desktop\Pirate Force` (recursive) มีไฟล์เดียวคือ (ก) · ไม่มี 13,824/`67501f7e…` ⇒ ตาม `COO 0213`: เดินต่อด้วย (ก) อย่างเดียว ไม่ rebuild · **A2 = NO-RESULT (ข)**
3. **PASS** — บรรทัด `rules=` มี `manifest_id2` (ตัวตรวจใหม่กว่ารอบ `selrsl`)

## ขั้น A1 (คำต่อคำ · `--dll` อย่างเดียว ไม่มี `--client-dir`)
```
GM_PLUGIN_IMAGE build rules=pe32_dll,export_exact,manifest_id2
GM_PLUGIN_IMAGE build verdict=image_ok path=C:\Users\Panya\Desktop\Pirate Force\pf_bridge\patches\gm_plugin\GameMaster.dll
GM_PLUGIN_IMAGE build failed_rules=none not_evaluated=none
GM_PLUGIN_IMAGE build sha256=4a0ecb5817c15b0bf08964bc16972bc7340666357c494e9d0308ee9ce72d743b size=14848
GM_PLUGIN_IMAGE build exports=CreateGameMaster
GM_PLUGIN_IMAGE build imports=MSVCR90.dll,KERNEL32.dll
GM_PLUGIN_IMAGE build embedded_manifest=yes manifest_ids=2 manifest_named_ids=0
GM_PLUGIN_IMAGE build detail=PE32 DLL exporting CreateGameMaster exactly -- none of the file-level failure modes this module can see is present in these bytes
GM_PLUGIN_IMAGE build advisory=msvcp90.dll is not imported; revision 2 resolves the wstring constructor dynamically, so this is not fatal by itself
GM_PLUGIN_IMAGE build nonclaim=file-level only; this says nothing about whether the GM window opens, and nothing about whether the manifest at id 2 CONTAINS a usable assembly reference -- an empty or wrong-version manifest still answers 14001
EXIT=0
```
(3) หลังขั้น A โฟลเดอร์ไคลเอนต์ **ไม่มี** `GameMaster.dll` (`dir` = 0) ✓ — ไม่มีการ copy เกิดขึ้นในขั้น A

## สคริปต์รันจริงครั้งแรก (ตาม NOW ข้อ 2)
- `find_mt.bat`: `[ok] mt.exe: C:\Program Files\Microsoft SDKs\Windows\v6.0A\bin\mt.exe` · `FIND_MT_EXIT=0` (ตำแหน่งเดียวกับที่ R304 เคยเจอ) · หมายเหตุ: ค่า `MT` ไม่ตกทอดมาถึง shell ผู้เรียกในท่าที่ผมรัน (`cmd /c "call … & echo %MT%"` ขยาย `%MT%` ก่อน call — ข้อจำกัดของวิธีเรียกของผม ไม่ใช่ของสคริปต์)
- `install.bat "C:\Users\Panya\Desktop\Pirate Force\GameClient"` (ไม่ตั้ง PFGM_FORCE): `[warn] dumpbin is not on PATH …` → `[..] plugin_image_check (py -3) is reading the file about to be copied` → บล็อก `GM_PLUGIN_IMAGE` ชุดเดียวกับ A1 → `[ok] plugin_image_check: verdict=image_ok` (+ NONCLAIM 5 บรรทัด) → **`[OK] installed: C:\Users\Panya\Desktop\Pirate Force\GameClient\GameMaster.dll`** → certutil `4a0ecb58…d743b` → `INSTALL_EXIT=0` · ไม่มี `[STOP]` (ไม่มีไฟล์เดิมในโฟลเดอร์ไคลเอนต์) ไม่มี `[FAIL]` ไม่มี `[FORCED]`
- **rollback ทำแล้ว** (1497b 15:06): ลบไฟล์ที่ติดตั้ง (sha ตรง 4a0ecb58 เท่านั้น) `removed=1 left=0` · (ก) ต้นฉบับยังอยู่ครบ size 14848 sha เดิม
- **ไม่รัน `build_vs2008.bat`** — `COO 0213` ห้าม rebuild และสคริปต์นั้นจะเขียนทับ (ก) ในโฟลเดอร์เดียวกัน (ทำลาย provenance ของไฟล์ที่ GT-207 โหลดได้)

## สถานะใบ
- wire/DB (1) ✓ (2) NO-RESULT (ข) (3) ✓ (4) ✓ (บรรทัด install.bat ครบ + rollback ยืนยัน) (5) ไม่แตะ DB — ไม่มีอะไรจะเปรียบเทียบ
- client-observable: **ยังไม่ได้ทำ** — ขั้น B (ติดตั้ง (ก) → DebugView → บูต → กดปุ่ม GM → `GMUI` เปิด/ไม่เปิด → rollback) ต้องมี Panya หน้าจอ · ผมจะพ่วงเข้ารอบ attended ถัดไป (~5 นาทีหน้าจอ) · หมายเหตุ: `GT-207` build 1 เคยเห็น GMUI เปิดด้วยไฟล์ sha เดียวกันนี้แล้ว — ขั้น B จึงเป็นการยืนยันซ้ำภายใต้ตัวตรวจใหม่
- คำทำนาย: **P1 ครึ่ง A1 ถูก** (image_ok exit 0) · ครึ่ง A2/P3 **วัดไม่ได้** (ไม่มี (ข)) · P2 ไม่เกิด · P4 ไม่เกิด
⇒ เสนอหัวใบ: `🟡 ขั้น A เสร็จ (A1 image_ok · A2 NO-RESULT (ข)) · สคริปต์ install/find_mt รันสะอาดครั้งแรก · ขั้น B รอ attended` — chief ตัดสิน

## nonclaims
① ไม่พิสูจน์ว่า GMUI เปิด (ขั้น B) ② ไม่พิสูจน์ negative control (ข) — ของไม่มี ③ ไม่ได้รัน build_vs2008.bat ④ ไม่พิสูจน์เนื้อ manifest (ตามที่ตัวตรวจเขียนเอง) ⑤ ไม่แตะ DB/เซิร์ฟ/เกม ⑥ ไม่ commit

— ka1-A, 2026-09-04 15:08 +07:00
