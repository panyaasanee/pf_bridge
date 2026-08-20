# GAME TEST QUEUE — คิวเทสในเกม

> 📌 **รอบ 109 (2026-08-20 ~19:3x) — คิวนี้ไม่ขยับ ไม่มีรายการใหม่ ไม่มีรายการไหนถูกปิดหรือย้าย**
> รอบนี้แตะ **CI อย่างเดียว**: gate ประกาศผลของตัวเองลง branch `ci-status` ได้แล้ว (ใบสั่ง Panya 19:10 "ทาง D")
> 🔴 **HEAD ของ repo โค้ดขยับ `9045978` → `89ce13b`** — เช็คก่อนบูตตามปกติและจดลงธง
> ✅ **แต่ไม่แตะ `src/` ไม่แตะ scenario ไม่แตะ tool ที่ผู้เทสใช้** ⇒ **พฤติกรรมเซิร์ฟเวอร์และเกมไม่เปลี่ยนเลย
> คิวทุกใบยังใช้ได้เหมือนเดิมทุกประการ**
> ที่ค้างอยู่เหมือนเดิม: **GT-030 · GT-031 · GT-032 · GT-033 · GT-001** (GT-031 ก่อน — เก็บภาพของ GT-028 ได้ในตัว)
> 🔴 **ยังค้าง: รอบใหญ่ #10 (GT-027 รันซ้ำ) ไม่เคย teardown** — รายละเอียดและ nonclaims อยู่ใน `LOCK_GAME.txt`
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R109_TO_ATTENDED_20260820_1930.md`

> 🔔🔔 **รอบ 108 (2026-08-20 ~18:45) — ขั้นแรกของทุกเซสชันเปลี่ยนแล้ว: อ่าน `pf_bridge\NEW_ORDERS.txt` ก่อนเปิดคิวนี้**
> chief กำลังย้ายไปอยู่บน cloud · ตัว sync (`pf_git_sync.ps1`, ทุก 5 นาที) จะดึงของที่ chief push ลงมาที่ดิสก์
> แล้วเขียน `NEW_ORDERS.txt` บอกว่ามีจดหมายใบไหนใหม่และ **คิวนี้ขยับหรือเปล่า**
> 🔴 **ถ้าไม่มีของใหม่ ไฟล์นั้นจะไม่ถูกแตะเลย ⇒ mtime ของมันคือสัญญาณ** · ถ้าคิวขยับ **ห้ามทำงานจากความจำ เปิดอ่านใหม่**
> 🔴 **ห้ามลบ/ย้ายไฟล์ใน `notes_to_chief\`** — ตัว sync ปฏิเสธ commit ที่มีการลบ *ทั้งก้อน* (เทส T6 พิสูจน์แล้ว)
> บริโภคจดหมายเสร็จ = **สำเนา**ไป `consumed\` + วาง stub `.CONSUMED.txt` · **ต้นฉบับอยู่ที่เดิมเสมอ**
> 🛡 **ระหว่างถือ `LOCK_GAME.txt` ตัว sync จะไม่แตะ repo โค้ดเลย** — โค้ดใต้เท้าคุณจะไม่เปลี่ยนกลางรอบเทส
> รายละเอียด: `FROM_CHIEF_R108_TO_ATTENDED_20260820_1845.md` · ติดตั้ง: `HOWTO_INSTALL_GIT_SYNC.md`
> ⚠️ **ทั้งหมดนี้ยังไม่มีผลจนกว่า Panya จะกด `SETUP_GIT_SYNC.bat`** — ยังไม่มีใครติดตั้ง

> 🗂 **โน้ตรอบ 78 (หลังบริโภคผลรอบใหญ่ #3) ย้ายไป `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R85_HOUSEKEEPING.md`**
> (chief รอบ 85) — ทุกข้อปิดแล้ว: canonical sha ย้ายไฟล์เดียวเสร็จ (`CANON_SHA.txt`) ·
> GT-016 job รับเข้า `staged\` เสร็จ · lead เรื่อง GT-011/GT-013 ไม่รีเฟรช UI ถูกตอบแล้วโดย
> UI-REFRESH-001 รอบ 80 (ไม่มี erase-by-key ในไบนารี) → สืบทอดเป็น GT-018 (PASS แล้ว) ·
> GT-015 ที่ข้อ 4 พูดถึงยังเป็น 🟢 PENDING อยู่ในคิวนี้เหมือนเดิม ไม่มีอะไรเปลี่ยน

> 🗂 **แบนเนอร์อัปเดตรอบ 63 / 66 / 67 ย้ายไป `pf_bridge\archive\GAME_TEST_QUEUE_BANNERS_ARCHIVE_20260818_R75.md`** (chief รอบ 75) — ผลรอบปิดแล้ว เนื้อหาเต็มอยู่ใน CHIEF_CONTINUATION + reports/ · โน้ต decode และบล็อกนโยบายด้านล่าง **ยังใช้อยู่ อย่าข้าม**


> 🟢 **โน้ต decode (อัปเดตรอบ 52 จากรอบ 40):** unknown id ใน GT captures decode หมดแล้ว —
> `0x3D4B` = GetWorldInfoVital payload ครบทุกไบต์ (FINDINGS_R40): เฟรม 248B ก่อนกด logout
> ทุกครั้ง = เฟรมเปิด dialog ปกติ server ignore ได้ **อย่านับเป็น FAIL evidence** ·
> `0x1B40 LogoutVital` มี handler แล้ว (HYP-PF-012 echo + HYP-PF-013 ack_close — ทั้งคู่
> opt-in) แต่ **GT-007/GT-008/GT-026 พิสูจน์แล้วว่า echo/ack+close ไม่ทำให้ client ออกจากแมพ**
> 🆕 **รอบ 100 (agent D static RE) พบกลไกว่าทำไม: inbound `0x446F30` เป็น actor-vital reconcile pass ล้วน
> → echo ไม่มีวันทำ transition · การเปลี่ยนหน้าจริงขับโดย session/connection orchestrator (`0xf45030`) ที่รอแล้วปิด connection**
> ⇒ คำตอบที่ถูกน่าจะเป็น **ปิด/redirect GSCN connection** (candidate `ReturnSelectServerVital 0x709E`) → ต้อง attended A/B (GT-033)
> → **0x3D4B-first landed แล้วรอบ 53 (HYP-PF-016 opt-in — มีผลเฉพาะ GT-013 ที่บูตด้วย scenario worldinfo_first)**
> 🆕🔴 **แก้ความเชื่อเก่า (GT-026 2026-08-20):** "ปุ่ม logout ไม่มีธง = client freeze ต้อง End task" **ไม่จริง** —
> บน default scenario client **ไม่ freeze** แค่ไม่มีอะไรเกิด (ยังรับคลิก ปิดด้วย X ได้) · เทสอื่นยังวางแผน End task ได้เพื่อความปลอดภัย แต่ไม่ต้องกลัว freeze
> 🆕 **ทางเข้า logout ในเกม = ปุ่มหกเหลี่ยม `HOME` มุมซ้ายล่าง → เมนู → `ออก` (ล่างสุด ไอคอนประตู) → หน้าต่าง 3 ปุ่ม
> `กลับเข้าเกม`/`กลับหน้าเลือกตัวละคร`/`ออกจากเกม`** · ⚠️ **ปุ่มเฟือง (gear) มุมซ้ายล่าง = OPTIONS ไม่ใช่ logout** · X ในแมพ = dialog ยืนยัน "ต้องการปิดเกมหรือไม่?" (`ยืนยัน`/`ยกเลิก`)
> `0xAC52` = Channel_LocalTalkMessageVital (CHAT-ECHO-002) ไม่ใช่ unknown แล้ว

> 🔵🔵🔵 **นโยบายทีมใหม่จาก Panya (17:40 — เขียน 17:51, บล็อกเต็มอยู่หัว CHIEF_CONTINUATION.md):**
> คิวนี้เดินแบบ "รอบใหญ่" — chief สะสมรายการ UI test เป็น PENDING ให้**พร้อมรันทันที**
> (steps ทีละคลิก + pass criteria สองชั้น + nonclaims) · headless replay chief ทำเองได้เลย
> ไม่ต้องเข้าคิวนี้ · เมื่อถึงจังหวะ Panya จะปลุกเซสชันหลัก (game tester, skill
> `pf-attended-test`) มารันทั้งคิวรวดเดียว แล้วกรอกผลกลับให้ chief ประมวล
> — ธง PANYA_PRESENT ยกเลิกถาวร ข้อความ "รอธง/รอ Panya attend" เก่ากว่านี้ = ล้าสมัย

> 🔑 **วิธีขอสิทธิ์เกมที่ถูกต้อง (บทเรียนจริงจากเซสชันหลัก 03:31 vs 03:52 — อย่าคลำเอง):**
> `request_access(["GameClient.local.bin"])` ตอนเกม**ไม่ได้เปิด** → ระบบตอบ `notInstalled`
> **เงียบ ๆ ไม่มี dialog ขึ้นบนจอเลย** (เกมเป็น .bin ไม่อยู่ใน Start menu)
> ลำดับที่ถูก: ① เปิด server ผ่าน bridge ② เปิดเกมผ่าน bridge (ProcessStartInfo —
> สองขั้นนี้ไม่ต้องใช้สิทธิ์) ③ รอหน้าต่าง 'Pirate Force' โผล่ ④ **แล้วค่อย** เรียก
> `request_access(["GameClient.local.bin"])` → dialog จะขึ้นจริง → Panya กด Allow
> (พิสูจน์แล้ว 03:52: ขอตอนเกมเปิดอยู่ → granted tier full ทันที)

> 🔴 **กฎใหม่ที่ตามมาจากรอบ 17 — ทุกเกณฑ์ผ่านในคิวนี้ต้องระบุว่าตัวเองอยู่ชั้นไหน:**
> รอบ 11 วางกฎว่า "อย่านับ `count(*)` เปล่า ให้นับ `selected_character_id IS NOT NULL`"
> เพื่อกันแถวที่งอกจากการต่อ TCP เปล่า — **กฎนั้นยังถูกและยังจำเป็น แต่ไม่พออีกแล้ว**
> รอบ 17 พิสูจน์ว่า **สคริปต์ ~200 บรรทัดสร้างแถวที่ `selected_character_id IS NOT NULL`
> ได้ และแยกไม่ออกจากแถวของ client จริงในทุกคอลัมน์ที่เกณฑ์ดูอยู่**
> → DB พิสูจน์ได้แค่ว่า *มีบางอย่างพูดโปรโตคอลถูก* ไม่ได้พิสูจน์ว่า *เกมจริงทำงาน*
>
> | ชั้น | ตัวอย่างเกณฑ์ | ใครทำได้ |
> |---|---|---|
> | **wire/DB** | เฟรมที่ server ส่ง, label, `sessions`, `lease_generation`, integrity | 🟢 headless — **ไม่ต้องรอ Panya** |
> | **client-observable** | HP bar, minimap, ชื่อแมพ, ข้อความที่ *ตาเห็นในกล่องแชท*, การเรนเดอร์ | 🔴 **ต้องมี Panya เสมอ** (เช่น GT-006) |
>
> เวลาที่เขียนรายการใหม่ ให้แยกเกณฑ์เป็นสองหัวข้อนี้ และอย่าอ้างชั้นบนเป็นหลักฐานของชั้นล่าง

การประสานงาน (chief-continue อ่านตรงนี้):
- ทุกครั้งที่จบรอบ chief-continue ระบบจะส่ง notification ปลุกเซสชันหลักอัตโนมัติ
  (notifyOnCompletion เปิดแล้ว) — **แค่จบรอบให้เรียบร้อยก็คือการปลุกผู้เทสแล้ว**
  ⚠️ **แต่ notification จะมีผลก็ต่อเมื่อมีคนอ่าน** — ยืนยัน `notifyOnCompletion` จาก API ไม่ได้
  (ไม่มีในผลลัพธ์ของ `list_scheduled_tasks`) และ 24 รอบที่ผ่านมาอยู่ในช่วงตีห้าถึงเช้า
  → **ห้ามเขียนรายงานว่า "รอผู้เทส" เฉย ๆ อีก ให้เขียนตรง ๆ ว่า "รอ Panya มา attended session"**
- ถ้าต้องการเทส: เขียนรายการ PENDING ลงคิวนี้ให้ละเอียด แล้วจบรอบได้เลย
- ถ้ายังไม่ต้องการเทส: จบรอบตามปกติ ผู้เทสจะเห็นว่าคิวว่างและไม่ทำอะไร
- ผลเทสจะถูกกรอกกลับในคิวนี้ → รอบถัดไปของ chief เอาไปประมวล/commit ต่อ

รูปแบบรายการ:

```
## GT-NNN <ชื่อ>  [PENDING|RUNNING|PASS|FAIL|BLOCKED]
- objective: (claim เดียวที่เทสนี้พิสูจน์)
- db: (ไฟล์ DB ที่ใช้ — ค่าเริ่มต้น state\pirateforce.sqlite3)
- server args: (เช่น -SecondPasswordMode bypass)
- steps: (ทีละคลิก อ้างพิกัด/ภาพจาก playbook)
- pass criteria: (ต้องเห็นอะไรใน UI + server log + DB)
- nonclaims: (อะไรที่เทสนี้ไม่พิสูจน์)
- result: (game-tester กรอก: ผล + หลักฐาน + เวลา)
```

## PLAYBOOK — ขั้นตอน full-loop ที่พิสูจน์แล้ว (2026-08-17 04:17–04:24)

1. job เปิด server: copy แบบจาก `pf_bridge\done\014_fullloop_canonical.ps1`
   (Ctrl+C server เก่าก่อนถ้า port ไม่ว่าง) — server ต้องขึ้น listener 2 ตัวใน ~2 วิ
2. job เปิด client: แบบจาก `done\015_launch_client.ps1` (ProcessStartInfo เท่านั้น)
3. รอ ~30 วิ → หน้าเลือกเซิร์ฟเวอร์: คลิกปุ่มซ้ายล่างใต้ panel (ตำแหน่งสัมพัทธ์กับ
   หน้าต่าง — ยึดภาพ ไม่ยึดพิกัดตายตัว เพราะหน้าต่างย้ายได้)
4. dialog เตือน PVP → คลิกปุ่มซ้าย (ยืนยัน)
5. หน้าเลือกตัวละคร: เห็น Arena01 + nameboard → ตัวละครต้องถูกเลือกอยู่
   (มี panel ชื่อด้านบน) ถ้าไม่มี ให้คลิกที่ตัวโมเดลก่อน → คลิกปุ่ม **กลางสุด** จาก 5 ปุ่ม
   แถวล่าง = เข้าเกม (⚠️ แก้ 2026-08-18 จาก GT-010 zoom ยืนยัน: **ปุ่มแรกซ้ายสุด =
   ลบตัวละคร** · ปุ่มที่ 2 = สร้างตัวละคร — โน้ตเก่าที่ว่า "ปุ่ม 2 = ลบ" ผิด · กดลบเฉพาะ
   เทสที่สั่งเท่านั้น · X ที่หน้านี้ปิดหน้าต่างทันทีไม่มี dialog ยืนยัน)
6. loading (โปสเตอร์ WANTED) ~20-30 วิ → เข้าแมพ: ต้องเห็น HP bar, minimap,
   ชื่อแมพมุมขวาบน, chat "[ระบบ] : Pirate Force local server online"
7. ออก: คลิก X มุมขวาบนหน้าต่าง **ครั้งเดียว** → dialog ยืนยัน → คลิกปุ่มซ้าย (ยืนยัน)
8. job ปิด server + เก็บหลักฐาน: แบบจาก `done\016_stop_server_collect.ps1`

ข้อควรระวังที่เจอมาแล้ว:
- ถ้า StartGame แล้วเงียบ (ไม่ loading) = server ปฏิเสธเงียบ → อ่าน
  `server_console_live.out.txt` หา `StartGameReq` แล้วดูว่ามี response ไหม
  อย่าคลิกวนซ้ำ; client ที่ค้างสถานะนี้จะไม่รับ X/Alt+F4 ต้องให้ผู้ใช้ End task
- DB post-move (identity1 ที่ slot≠0) จะโดน guard ปฏิเสธ เว้นแต่เปิด scenario opt-in
- 🔴 **ห้ามใช้ `count(*) FROM sessions` เป็นเกณฑ์ผ่าน (พิสูจน์แล้วรอบ 11 ว่าเชื่อไม่ได้)**
  การต่อ TCP เข้าพอร์ต GAME `10189` **โดยไม่ส่งไบต์ใด ๆ เลย** ก็สร้างแถว `sessions`
  ผูกกับ `account_id=1` (`localtest`) ได้ 1 แถวต่อ 1 การเชื่อมต่อ และดัน `lease_generation`
  ขึ้น 1 (พอร์ต LOGIN `10188` ไม่สร้าง; การบูตเปล่าก็ไม่สร้าง)
  → แถวอาจงอกจากอะไรก็ได้ที่ไม่ใช่ client → เทสจะ **ผ่านด้วยเหตุผลผิด** หรือตกทั้งที่ไม่ผิด
  **ให้นับเฉพาะแถวที่เป็น client จริงเสมอ:**
  ```sql
  SELECT count(*) FROM sessions WHERE selected_character_id IS NOT NULL;
  ```
  และทุกเทสต้องบันทึก `SELECT max(lease_generation) FROM sessions;` ทั้งก่อนและหลัง
  ส่วนแถวที่ `selected_character_id IS NULL` ให้รายงานแยกเป็น "แถวจากการเชื่อมต่อเปล่า"
  **ไม่ถือเป็นความผิดพลาด** (รายละเอียด: `pf_bridge\FINDINGS_R11_ZEROBYTE_GAME_SESSION.md`)
- 🟢 **precondition ยืนยันแล้วที่ HEAD `eef51fa` (รอบ 11, job 033 — ไม่มี client):**
  server ขึ้น listener 2 ตัวใน **1 วินาที**, accept ได้จริงทั้งสองพอร์ต, Ctrl+C helper
  ปิดสะอาด **exit 0 ทั้ง server และ shim**, `[FOUNDATION] stopped` ×1, stderr **0 ไบต์**,
  listener เหลือ 0, `integrity_check=ok`, backpack `[1@0,2@1,4@3]` ไม่ขยับ
  → **ฝั่ง server ไม่มีอะไรบล็อกคิวนี้ ขาดแค่คนเปิดเกม**
- 🔴 **บังคับทุกเทสที่ใช้ `state\pirateforce.sqlite3`:** ขั้นแรกของ job ต้อง copy DB
  ไปเป็น `pf_bridge\backup\pirateforce_before_<GT-id>_<yyyyMMdd_HHmmss>.sqlite3`
  แล้ว **เทียบ sha256 กับต้นฉบับทันที ถ้าไม่ตรงให้หยุด**
  (รอบ 08:07 พบว่า DB ตัวนี้ **ไม่มีสำเนาสำรองเลย** และ **ไม่ได้อยู่ใน git**
  → commit/stash/checkout กู้มันไม่ได้ทางเดียวที่กันได้คือ copy ไฟล์
  ตอนนี้มีฐานอ้างอิงแล้วที่ `backup\pirateforce_canonical_20260817_080705.sqlite3`
  sha256 `673f4bfb…` — รายละเอียด + ค่าฐานทุกแถวอยู่ใน `backup\DB_CANONICAL_BASELINE.md`)

---

## PLAYBOOK เพิ่มเติม — บทเรียนจากรอบใหญ่ #7 (GT-022) · เขียนโดย chief รอบ 91 จากผลของผู้เทส

**การเดินตัวละคร (Panya สอนเอง ~18:5x — การคลิกพื้นเพื่อเดินถูกปิดไปแล้ว):**
`W/A/S/D` เดิน · `Q/E` หมุนกล้อง · `spacebar + WASD` กระโดด (ใช้ขึ้นจากน้ำได้) · ล้อเมาส์ซูม ·
คลิกขวาค้างลากเมาส์หมุน 360° **แต่เครื่องมือของผู้เทสลากได้แค่ปุ่มซ้าย ⇒ ใช้ได้แค่ Q/E**
🔴 **แกน a/d เปลี่ยนตามทิศที่หันทุกครั้ง** ⇒ **สูตรที่เวิร์ค:** กด W สั้น ๆ 0.3–0.4 วิ → อ่าน X/Y บน HUD
→ ได้ basis vector → แก้สมการ 2 ตัวแปรว่าจะกด s/a/d กี่วินาที · **ต้องวัดใหม่ทุกครั้งหลังหมุนกล้องหรือ strafe**

**หาพิกัด NPC โดยไม่ต้องเดินสุ่ม:** เฟรม `SPAWN` มี float 3 ตัวท้าย `MovementAttr` = X/Y/Z ตรง ๆ
(ตัวอย่างจริง `2A D4CF0EC6 / 2A B9C02DC5 / 2A C74A5F43` → X `-9139.96` Y `-2780.05` Z `223.29`)

**เครื่องมือ/จ็อบ — สี่ข้อนี้ทำให้รอบ #3 เสียเวลาไปเยอะ:**
1. 🔴 **จ็อบที่เปิด GameClient แบบ redirect stdout/stderr จะบล็อก bridge จนหน้าต่างเกมปิด**
   ⇒ จ็อบที่เขียนมาเพื่อไปฆ่า client ที่ค้าง **รันไม่ได้ เพราะถูกบล็อกโดย client ตัวนั้นเอง**
   **ให้เปิด client โดยไม่ redirect หรือแยกเป็นจ็อบ launch ที่ปล่อยลูกแล้วจบทันที**
2. 🔴 **`Get-Process` ครั้งเดียวไม่ใช่หลักฐานว่าไม่มีอะไรค้าง** — จ็อบ 907 เช็คว่า process client หายแล้วจึงเปิดตัวใหม่
   แต่สิ่งที่ต้องเช็คจริงคือ **เซิร์ฟเวอร์ปล่อย session แล้วหรือยัง** (server เป็น serial ตาม R18 ⇒ รายที่สองค้าง "กำลังเชื่อมต่อ...")
   **กฎ: ถ้า client เก่าไม่ได้ปิดแบบสวย ๆ (ไม่ได้กด "ออก" จนถึงหน้า server select) → รีบูตเซิร์ฟเวอร์เสมอ**
3. **จ็อบเดียวไม่ควรทำทั้ง "ปิด" และ "เปิด"** — ถ้าขั้นปิดสรุปผิด ขั้นเปิดจะเดินหน้าต่ออย่างมีความสุข
4. **one-shot ผูกกับ connection ไม่ใช่ process ของเซิร์ฟ** (`self.runtimeres_death_sweep_count`)
   ⇒ ปิด client สวย ๆ แล้วเปิดใหม่ = รีอาร์ม sweep ได้โดยไม่ต้องรีบูตเซิร์ฟ
5. **boot job ควรอ่าน expected sha จาก `CANON_SHA.txt` เสมอ** ไม่ฝังค่าตาย (job 905 ทำแบบนี้)
6. 🔴 **`py -3 -m pirateforce_foundation.app --help` คืน 0 บรรทัด (exit 0) ผ่านสะพาน**
   **ห้ามใช้ `--help` ตรวจว่ามี flag ไหม — ให้ `git grep` ที่ source แทน**
7. **`computer_batch` ที่มี `hold_key`/`key` มักโดน `focus anomaly`** — แยกเป็น call เดี่ยว (`left_click` ก่อน แล้วค่อย `hold_key`) เสถียรกว่า
8. ✏️ **[แก้แล้ว รอบ 92 — ข้อความเดิมอ่านหลักฐานผิด]** เดิมเขียนว่า *"ปุ่ม X / ปุ่ม 'ออก' ไม่รับคลิกสังเคราะห์"*
   🔴 **ผิด — LOCALTEST-001 (2026-08-19 23:06) พิสูจน์แล้วว่ามันรับคลิกสังเคราะห์ปกติ กดครั้งเดียวปิดได้**
   **สาเหตุจริงคือหน้าต่างแอป Claude ทับ title bar ฝั่งขวาของเกม ตรงที่ปุ่ม X อยู่พอดี**
   และเซสชันฝั่ง cloud **มองไม่เห็นหน้าต่างตัวเองใน screenshot** จึงไม่มีทางรู้ว่าโดนบัง
   ⇒ **ท่าที่ถูก:** ผู้เทส local เห็นหน้าต่างตัวเองในภาพ ⇒ **ตรวจว่าโดนบังไหมก่อนคลิกทุกครั้ง**
   ถ้าโดนบัง ให้ `left_click_drag` ลากหน้าต่างเกมออกมาก่อน แล้วค่อยกด X (จ็อบ 916 เป็นใบเสร็จ: `pid does not exist`)
   ⚠️ **ยังไม่พิสูจน์:** ปุ่ม X ตอนอยู่ **ในแมพ** (มี dialog ยืนยัน) และ **ปุ่ม logout ในเกม** — สองอย่างนี้ยังไม่เคยเทสจากฝั่ง local
8b. 🔴 **วิธีเปิด client ที่ถูกต้อง = `Invoke-CimMethod Win32_Process Create`** (บทเรียน LOCALTEST-001)
   · `Start-Process 'xxx.bin'` **ที่ไม่มี** `-Redirect*` = ShellExecute → **ล้มเงียบ** `-PassThru` คืน `$null` (จ็อบ 912)
   · `-RedirectStandardOutput` ใน boot job ตระกูล 072/087/090/097 **ไม่ได้ใส่ไว้เพื่อเก็บ log อย่างเดียว** —
     มันคือสิ่งที่บังคับ `UseShellExecute=false` ให้ `.bin` รันได้ **ใครลบออกเพื่อเลี่ยงการบล็อก จะได้จ็อบที่ไม่เปิดอะไรเลยและไม่ error**
   · `Win32_Process.Create` ได้ทั้งสองอย่าง: client เปิดจริง **และ bridge กลับ idle ทันที** (จ็อบ 913/915 เป็นใบเสร็จ)
9. **run DB เป็นสำเนาใหม่ทุกครั้งที่บูต ⇒ ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกรอบ** เผื่อเวลาเดินไว้ในแผน
10. 🆕🔴 **รอบเทสที่จบเพราะคนเลิกเล่น ไม่ใช่เพราะเทสจบ ก็ยังต้อง teardown** (คำสั่ง Panya 1440 ข้อ B ·
   บทเรียนรอบใหญ่ #10: บูต 11:37 แล้วเลิกกลางคัน ไม่มี teardown · LOCK_GAME ค้าง HELD ~3 ชม.
   ไม่มีใครตรวจ canonical guard เลยทั้งรอบ) — สองข้อย่อยที่ต้องรู้:
   - ⚠️ **teardown template ปฏิเสธรอบที่ถูกทิ้ง >180 นาที โดยดีไซน์** (stamp age guard → exit 12 —
     จ็อบ 0947 เป็นใบเสร็จจริง) ⇒ แท่นที่ถูกทิ้งข้ามคืน/ข้ามชั่วโมง **อย่าฝืน template** ให้ใช้
     `staged\TOOL_stop_stale_server.ps1` (ทางกู้ที่ออกแบบมาเพื่อกรณีนี้ ไม่อ่าน info file) แล้วตามด้วย
     receipt อ่านอย่างเดียว `staged\0949_gt027_stalepad_canonical_guard.ps1` (แบบร่างพร้อมใช้ รอบ 105)
   - 💡 การ์ดเชิงระบบ (เริ่มรอบ 105): **chief ทุกรอบ scheduled ถ้าเห็น `LOCK_GAME` HELD และ heartbeat
     เก่ากว่า ~30 นาที ให้รายงานธงค้างในจดหมายถึงเซสชันหลัก** — รายงานอย่างเดียว ห้ามเก็บกวาดเอง
11. 🆕🔴 **ห้ามยืดระยะเฟรมของ scenario เพื่อให้ผู้เทสถ่ายทัน — ให้ถ่ายวิดีโอแทน**
   (คำสั่งเชิงวิธีการจาก Panya 2026-08-20 ~15:1x · ผู้เทสรับแล้วและยอมรับว่าเหตุผลของท่านถูก)
   - **เหตุผล:** ตัวเหตุการณ์บนจอ**เองสั้น** ไม่ใช่ว่าเฟรมถี่เกินไป ⇒ ยืด spacing ไปก็ไม่ได้อะไรเพิ่ม
     เสียเวลารอบเทสเปล่า และเพิ่มโอกาสที่รอบจะถูกทิ้งกลางคัน (ดูข้อ 10)
   - **ทางแก้ที่พิสูจน์แล้วสองรอบ:** ถ่ายวิดีโอ — ได้ทั้งภาพคมทุกเฟรม **และนาฬิกาที่ไม่ใช่ของผู้เทสเอง**
     (แก้ปัญหา Nyquist โดยไม่ต้องแตะ scenario สักไบต์ · GT-027 rerun คือใบเสร็จ: วิดีโอ 58 วิ เห็นครบ)
   - ⇒ **ข้อเสนอ "ทำ profile 15–20 วิ/เฟรมเพื่อผู้เทส" ที่ chief เคยส่งไป = ถอนแล้ว ห้ามหยิบกลับมา**
     GT-030 / GT-031 ที่ยังเขียนว่า 15 วิ/เฟรม **คงค่าเดิมไว้ตามที่ commit ไปแล้ว** (ไม่ใช่ profile ยืดเวลา
     มันคือค่าที่ scenario ถูก commit มาแต่แรก) — ห้ามสร้าง profile ใหม่ที่ยืดกว่านี้
12. 🆕⚠️ **ลูกศรเหลืองสองอันเหนือหัว NPC = เครื่องหมาย "เป้าหมายที่ถูกเลือก" ไม่ใช่เอฟเฟกต์ของ hit**
   (มันอยู่ตรงนั้นตั้งแต่ก่อนยิงแล้ว — เห็นชัดในเฟรม t=18 วิ ของวิดีโอ GT-027 rerun)
   ⇒ ห้ามใครอ่านลูกศรนี้เป็นหลักฐานว่าดาเมจถึงเป้า

---

> 📦 **[archive]** ประวัติศาสตร์รอบใหญ่ #2 (Q1/Q2 รอบ 22 · โน้ตรอบ 15–19 · GT-008/009/010 · GT-001 ครั้ง 1–3)
> → `pf_bridge/archive/GAME_TEST_QUEUE_ARCHIVE_20260818.md` · ประมวลเข้า repo แล้ว: `reports/PF_BIGROUND2_ATTENDED_RESULTS_20260818.md` · ledger PF-013/014/015 amended · matrix chat_input_echo → runtime_pass

## รายการที่ปิดแล้ว (GT-002..006 · 011 · 015 · 017 · 018-022 · 023-025) — ⤴ stub ทั้งหมดย้ายไป archive (รอบ 97)

> pointer รวม: `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R97_CLOSED_STUBS.md`
> (ในนั้นชี้ต่อไปยัง archive เนื้อหาเต็มของแต่ละรายการอีกชั้น — ไม่มีอะไรถูกลบ)
> ใจความที่ยังต้องรู้: GT-019 พิสูจน์ hp0+timer ตายบนจอ · GT-021 พิสูจน์ client ไม่ลดตัวนับเอง
> · GT-022/025 พิสูจน์ท่านอน = DYING_LATCH (`_F_DIE_000` ยังไม่เคยถูกสังเกต — ห้าม flip HYP-PF-023)
> · GT-024 พิสูจน์เลขเรนเดอร์บนผู้เล่น + HP ไม่ลด (สองปาก) — ที่มาของ GT-031

## GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ  [🟢 PENDING ที่ `af10536` — 🔁 re-arm รอบ 97 · PASS ล่าสุดที่ `f286945` รอบใหญ่ #3] 🔁

> ✅ **RESULT รอบใหญ่ #3 — PASS ทุกเกณฑ์ที่ `f286945`** · รายละเอียดเต็มย้ายไป archive รอบ 97:
> `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R97_CLOSED_STUBS.md` ก้อน 2
> 🔴 ที่ยังต้องรู้: **canonical sha = `159F40EF758D567503828F0381F088247743E9663C13C692854C950F1F32DBC6`** (ตรง `CANON_SHA.txt`)
> - 🔁 **re-arm รอบ 78:** commit รอบ 78 แตะ `src/` (app.py + runtime.py + โมดูลใหม่ — ทุกจุดอยู่หลังธง scenario ที่ boot ปกติไม่ใช้ → ความเสี่ยง regression ต่ำมาก) → เทสที่ HEAD ใหม่ของรอบ 78
> - 🔁 **re-arm รอบ 95:** commit `72d6129` แตะ `src/` (damage_model_hypothesis.py + runtime.py — ทั้งหมดอยู่หลังธง scenario opt-in ที่ boot ปกติไม่ใช้ · full suite 1530 passed บน Windows · ความเสี่ยง regression ต่ำมาก)
> - 🔁 **re-arm รอบ 97 (ล่าสุด — ครอบ commit รอบ 96+97):** `8dfd303` (remote_player) และ `af10536` (damage_hp_link) แตะ `src/` ทั้งคู่ (app.py + runtime.py + โมดูลใหม่ — ทุกจุดอยู่หลังธง scenario opt-in ที่ boot ปกติไม่ใช้ · full suite **1803 passed 1 skipped** บน Windows · ความเสี่ยง regression ต่ำมาก) → **GT-001 = PENDING ที่ `af10536`** รันในรอบใหญ่ถัดไปตามท่ามาตรฐาน PLAYBOOK

> 🗂 **ประวัติ re-arm รอบ 52 / 53 / 65 (superseded โดย re-arm รอบ 78 ด้านบน) ย้ายไป
> `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260819_R85_HOUSEKEEPING.md`** (chief รอบ 85)

- objective: ยืนยันว่า commit ล่าสุดบน main ไม่ทำให้ loop พื้นฐานพัง
  (login → select → เข้าแมพ → ออก → server exit 0)
- db: `state\pirateforce.sqlite3` (ค่าเริ่มต้น)
- server args: `-SecondPasswordMode bypass`
- steps: ตาม PLAYBOOK ทั้ง 8 ข้อ
- pass criteria: เข้าแมพเห็นครบ (HP/minimap/ชื่อแมพ/chat online) + ออกสะอาด X+ยืนยัน +
  stopped ×1 + stderr 0B + listeners 0 + sessions +1 (นับแบบ selected_character_id IS NOT
  NULL) + lease +1 + backpack `[1@0,2@1,4@3]` เดิม + position เดิม (ถ้าไม่เดิน) + integrity ok
- nonclaims: ไม่พิสูจน์ inventory/combat/movement · path delete/logout/chat แยกเทสของตัวเอง
- หมายเหตุ recurring: หลัง commit ใดแตะ src/ ให้ตั้งกลับเป็น PENDING พร้อม hash ที่จะเทส
- result: (ผู้เทสกรอก)

## GT-026 EXIT-PATHS-001: ปิดเกม "ตอนอยู่ในแมพ" และปุ่ม logout ในเกม  [ท่อน A ✅ **PASS** · ท่อน B 🟡 **รันแล้ว (default scenario) — request ยืนยัน · ไม่ freeze · handler เป็น opt-in ไม่ active** · ข้อ 8 🔴 **BLOCKED** บน logout-transition ที่ทำงาน → ดู GT-033]

> 🟡 **รันแล้วรอบใหญ่ #9 (2026-08-20 09:52→10:20, HEAD `87f0769`, จ็อบ 933-937, tester next 938) — ผลเต็มบริโภคโดย chief รอบ 100:** ท่อน A PASS สองชั้น (X ในแมพ → dialog "ต้องการปิดเกมหรือไม่?" ปุ่ม `ยืนยัน`/`ยกเลิก` → กดยืนยัน หน้าต่างหาย ≤1 วิ · wire/DB: `closed_at` ถูกเติมตรงเวลากด = ออกสะอาดในสายตา server) · ท่อน B รันบน **default scenario** (handler HYP-PF-012/013 เป็น opt-in จึงไม่ active): client ส่ง `LogoutVital 0x1B40` จริงถูกต้อง มี **mode discriminator `08 03`=กลับหน้าเลือกตัวละคร / `08 01`=ออกจากเกม** · server default ไม่ตอบ · **client ไม่ transition แต่ก็ไม่ freeze** (รับคลิกปกติ ปิดด้วย X ได้) — ปมอยู่ที่ response shape ที่ทำให้ client เปลี่ยนหน้า ซึ่งรอบ 100 static RE (agent D) พบว่า **echo ทำไม่ได้แน่นอน** (inbound 0x446F30 เป็น reconcile pass ล้วน) → ดู GT-033

> **เปิดโดย chief รอบ 92 (2026-08-20)** — มาจาก **nonclaims ของ LOCALTEST-001 โดยตรง**
> ผู้เทส local พิสูจน์แล้วว่าปุ่ม X ใช้ได้ **แต่พิสูจน์จากหน้า disconnect dialog เท่านั้น**
> ⇒ ยังไม่มีใครรู้ว่า **ตอนอยู่ในแมพ** (ซึ่งมี dialog ยืนยัน) และ **ปุ่ม logout ในเกม** ทำงานยังไงจากฝั่ง local
> 🔴 นี่ไม่ใช่รายการ "ของแถม" — **ทุกรอบใหญ่จบด้วยการออกจากเกม** ถ้าเส้นทางออกไม่ถูกพิสูจน์
> teardown ของทุกเทสจะยืนอยู่บนสมมติฐาน และ **การออกไม่สะอาดคือต้นเหตุของวงจรอุดตันที่กินเวลาเราไปทั้งคืน 2 รอบแล้ว**

- **ไม่ต้อง commit อะไรก่อน** — เทสพฤติกรรม client + เส้นทางออก ไม่ได้เทสฟีเจอร์ใหม่
- **scenario:** ค่าเริ่มต้น (ไม่ต้องเปิด flag ใด ๆ) · **db:** สำเนา canonical ตามปกติ · **server args:** `-SecondPasswordMode bypass`
- **เปิด client ด้วย `Invoke-CimMethod Win32_Process Create`** (ข้อ 8b ในหัวไฟล์ — อย่าใช้ `Start-Process` กับ `.bin`)

### steps (สองท่อน แยกจ็อบ อย่ารวม)

**ท่อน A — ปุ่ม X ตอนอยู่ในแมพ**
1. บูต server + client ตามปกติ → เข้าแมพให้เห็น HP/minimap/ชื่อแมพครบ
2. 🔴 **ถ่าย screenshot ก่อนคลิกทุกครั้ง แล้วดูว่าหน้าต่างแอป Claude ทับ title bar ฝั่งขวาไหม**
   ถ้าทับ → `left_click_drag` ลากหน้าต่างเกมออกมาก่อน (บทเรียน LOCALTEST-001)
3. กดปุ่ม X **หนึ่งครั้ง** → **ถ่ายภาพ dialog ยืนยันที่ขึ้นมา** (นี่คือของที่ยังไม่เคยมีใครเห็นจากฝั่ง local)
4. บันทึกข้อความบน dialog + ตำแหน่ง/ชื่อปุ่มทุกปุ่ม **ก่อน** กดอะไร
5. กดปุ่มยืนยัน → จับเวลาว่าหน้าต่างหายในกี่วินาที

**ท่อน B — ปุ่ม logout ในเกม** (บูตใหม่ อย่าใช้ต่อจากท่อน A)
6. เข้าแมพใหม่ → หาปุ่ม logout/ออกจากเกมใน UI → บันทึกตำแหน่ง
7. กด → บันทึกว่าไปหน้าไหนต่อ (server select? character select? ปิดทั้งโปรแกรม?)
8. ถ้ากลับถึงหน้า character/server select **ให้ลองเข้าเกมซ้ำโดยไม่รีบูตเซิร์ฟ** — ตอบคำถามว่า
   *"ออกแบบสวย ๆ แล้วเข้าใหม่ได้เลยไหม"* ซึ่งข้อ 4 ในหัวไฟล์อ้างว่าได้ **แต่ไม่เคยพิสูจน์กับปุ่ม logout จริง**

### pass criteria (สองชั้น)

**ชั้น client-observable:** มีภาพ dialog ยืนยัน · มีภาพ/บันทึกว่ากด logout แล้วไปหน้าไหน · หน้าต่างหายจากจอ + ไอคอน taskbar หาย
**ชั้น wire/DB:** จ็อบ PID guard ยืนยัน `pid does not exist` (ใช้ Id + StartTime แบบจ็อบ 916) ·
`GameClient` = 0 · listeners 10188/10189 = **0** · console ของ server ไม่เดิน keepalive ต่อ ·
`sessions` +1 (กรอง `selected_character_id IS NOT NULL`, order by `opened_at`) · canonical sha ไม่เปลี่ยน

### nonclaims ที่ต้องเขียนติดผลเสมอ
- ไม่พิสูจน์ว่า logout ทำให้ **persistence** เกิด — เรื่องนั้นเป็นของ GT-001 และเลน persistence
- ไม่พิสูจน์ว่าเส้นทางออกทั้งสองเหมือนกันในทุกแมพ — เทสแมพเดียว
- ถ้ากดแล้วไม่มีอะไรเกิด **ห้ามสรุปว่า "ปุ่มไม่รับคลิก"** จนกว่าจะยืนยันด้วย screenshot ว่าไม่มีหน้าต่างอื่นบัง
  (นี่คือความผิดพลาดเป๊ะ ๆ ที่ข้อ 8 ในหัวไฟล์เคยทำมาแล้ว)

- **result:** ✅ **ท่อน A = PASS** (ภาพ `gt026_exit_dialog_text.png` / `gt026_exit_buttons.png` · closed_at เติมตรงเวลากด) · 🟡 **ท่อน B = รันบน default (handler opt-in ไม่ active): request + discriminator ยืนยัน · ไม่ freeze · ไม่ transition** (ภาพ `gt026_logout_menu.png`) · ❌ **ข้อ 8 ตอบไม่ได้** (ไม่เคยถึงหน้า char select) → BLOCKED บน GT-033 · **PLAYBOOK แก้แล้ว** (logout ไม่ freeze · gear=OPTIONS · ทางเข้า HOME→ออก)

---

## GT-033 LOGOUT-TRANSITION A/B: response ไหนทำให้ client เปลี่ยนหน้าจริง  [🟢 **PENDING — พร้อมรันทั้งสอง variant แล้ว (chief รอบ 101 build เสร็จ · commit หลัง job 163)**]

> **เปิดโดย chief รอบ 100** จากผล GT-026 ท่อน B + static RE agent D (`pf_bridge\FACTPACK_R100_LOGOUT_TRANSITION_STATIC.md`)
> 🎯 **ปมที่ต้องปลด:** client ส่ง `LogoutVital 0x1B40` (subcode 03=char-select / 01=exit) แล้ว **รอ** อะไรบางอย่างจาก server เพื่อ transition · **echo (HYP-PF-012) พิสูจน์แล้วว่าไม่ทำงาน และรอบ 100 พบกลไกว่าทำไม** — inbound handler `0x446F30` เป็น actor-vital reconcile pass ล้วน ไม่มี branch เปลี่ยน scene/state/connection · การ transition จริงขับโดย session/connection orchestrator (vtable `0xf45030`) ที่ **รอแล้ว tear down connection** (gate ที่ mode +0x28 ∈ {1,4} + timestamp +0x24)
> ⇒ คำตอบที่ถูกน่าจะเป็น **(b) ปิด/redirect GSCN connection** ไม่ใช่ echo · `ReturnSelectServerVital 0x709E` = candidate ชื่อที่ดีที่สุดของ "กลับ char-select" แต่ยังไม่ยืนยัน (ไม่เจอ code ที่ consume มัน) · **static ตัดสินไม่ได้ → ต้อง A/B test**

- **✅ ทั้งสอง variant พร้อมแล้ว (chief รอบ 101 · pre-approved ใต้ policy #4 "แก้ปุ่มออกเกม" · production_allowed=false · fail closed · headless-proven):**
  - **variant A = HYP-PF-013 (มีอยู่แล้ว):** บูต `--logout-hypothesis-scenario scenarios\logout_hypothesis_ack_close.json` → รับ LogoutVital → ack + **ปิด socket/connection** ที่ 250ms (reuse close path ที่พิสูจน์แล้ว ไม่มี encoder ใหม่)
  - **variant B = HYP-PF-028 (build รอบ 101):** บูต `--logout-hypothesis-scenario scenarios\logout_hypothesis_return_select_server.json` → รับ LogoutVital → **ส่ง `ReturnSelectServerVital 0x709E` ก่อน** (body 16 ไบต์จาก serializer จริงของ client 0x5e69f0 · ทุกไบต์ tag มาจาก client · ค่า field = 0 เพราะไม่มี producer) → ตามด้วย ack เดิม → ปิด socket · headless: verifier 34 guards + replay 45 guards
  - ⚠️ **ทั้งสอง flag ใช้ `--logout-hypothesis-scenario` ตัวเดียว (ไม่ใช่ flag ใหม่)** · mutually exclusive · ต้องมี `--db` สำเนา canonical เหมือนเทสอื่น
- **steps (attended):** บูต **variant B ก่อน** (candidate ที่ตรง lead ชื่อที่สุด) → เข้าแมพ → HOME→ออก→`กลับหน้าเลือกตัวละคร` (subcode 03) → **ดูว่า client กลับหน้า character select ไหม** (ถ่ายภาพ) · ถ้าไม่เปลี่ยน → บูต variant A (close-only) ทำซ้ำ · แล้วทดสอบ subcode 01 (`ออกจากเกม`) ทั้งสอง variant
- **pass criteria สองชั้น:** client-observable = client เปลี่ยนไปหน้า char-select จริง (หรือ process exit สำหรับ subcode 01) · wire/DB = closed_at เติม (พิสูจน์แล้ว headless) · ถ้า variant B ทำให้ transition = **0x709E ยืนยันเป็น trigger** (ยกจาก candidate → confirmed) · ถ้า variant A ทำแต่ B ไม่ทำ = **response ที่ถูกคือ connection-teardown ไม่ใช่ vital** · ถ้าทั้งคู่ไม่ทำ = คำตอบอยู่ที่อื่น (mode/timer ที่ orchestrator รอ) — ผลลบมีค่าทุกกรณี
- **ปลดข้อ 8 ของ GT-026:** ถ้ากลับถึง char-select ได้ → ลองเข้าเกมซ้ำโดยไม่รีบูตเซิร์ฟ
- **nonclaims:** ไม่ claim ว่า response ของเรา = ของ server ต้นฉบับ (กู้ไม่ได้) · echo ถูกหักล้างพร้อมกลไกแล้ว · 0x709E เป็น candidate ไม่ใช่ข้อพิสูจน์ · field values ของ 0x709E = zero default ไม่มี producer · static ตัดสิน response shape ไม่ได้ (agent D) — นี่คือเหตุที่ต้อง attended A/B · **ยังไม่เคยมี client เห็น 0x709E แม้แต่ไบต์เดียว**
- **evidence (chief รอบ 101):** `reports\PF_LOGOUT_RETURN_SELECT001_HYP028_20260820.md` · ledger HYP-PF-028 · `tools\verify_logout_return_select_encoder.py` (34) · `tools\pf_logout_return_select_headless_replay.py` (45)


## GT-027 DAMAGE-ON-NPC-001  [✅ **PASS — รอบใหญ่ #10 (rerun ที่ Panya ขับเอง) 2026-08-20 11:37–11:52**]

**ผล:** เลขขึ้นครบสี่เฟรม **เกาะเหนือหัว NPC** — `63` → `379` (ตรง damage_wire เป๊ะ ไม่ scale ไม่มีเครื่องหมายลบ) → marker `MISS!` → `63` · NPC กระตุกตอนเลขขึ้น (ไม่กระตุกตอน MISS) · HP ทุกคนไม่เปลี่ยน (100/100)
**หลักฐาน:** วิดีโอ 58 วิ 60fps ของ Panya + ภาพนิ่งทุกเฟรม `pf_bridge\evidence_screens\biground10_gt027\` · wire ครบสองรอบ (จ็อบ 944)
🔴 **ผลลบฉบับผู้เทส 11:30 ("ไม่มีเลขเลย") ถูกถอนโดยผู้เทสเอง** — สมมติฐาน "0x2001 ไม่อยู่ใน map" ตกไป (client resolve `0x2001` → placement P0 'Navy Transfer' — ยืนยันจาก TargetVital ในล็อก)
**คำอธิบายที่เข้าเค้าที่สุดว่าทำไมผู้เทสไม่เห็น (static R102, `FACTPACK_R102_TARGETVITAL_AND_FXNUMBER_GATES_STATIC.md`):** toggle `[localplayer+0x420]` (ดูบทเรียนเครื่องมือ ⬇) หรือ resolve-timing — ตัดสินจริงที่ **GT-038**
ข้อความเต็มตอน PENDING: `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R102_GT027_028_029.md`

## GT-028 DAMAGE-SLOW-SWEEP-001  [✅ **PASS (เหลือข้อ ⑥ เดียว) — ได้ภาพจากรอบ rerun ของ GT-027**]

**ได้แล้ว:** ไฟล์ภาพ `63` (`gt027_f1_...png`) · `379` · marker `MISS!` (`gt027_f3_MISS_marker.png` — เป็นเท็กซ์เจอร์ `bm_miss.tga` ตาม FINDINGS_R93 เป๊ะ) · `63` เฟรม HIT_REACTION
🟡 **ค้างข้อเดียว: ⑥ `HIT_REACTION` (flags 0x0009) ต่างจาก `HIT_WEAK` (flags 0x0001) ตรงไหนบนจอ** — ภาพนิ่งเหมือนกันทุกประการ · ถ้าจะปิดต้องเทียบวิดีโอทีละเฟรมหรือรอเลนอื่นที่ใช้ flag เดียวกัน — **ไม่บล็อกอะไร ไม่ต้องรันรอบใหม่เพื่อข้อนี้**
🔴 **คำทำนายเดิมในคิว "เฟรม MISS ต้องเงียบ" = ผิด** — มี marker `MISS!` ชัดเจน (แก้แล้วในบรรทัดนี้)
🆕⭐ **ปิดท้ายด้วยวิดีโอ (บันทึกรอบ 106 จากจดหมาย 1520):** รอบซ้ำ Panya **คลิกเลือก NPC ก่อนยิง**
   (`12:31:58 TargetVital 0x2001 'Navy Transfer'`) ⇒ **แถบ HP ของเป้าหมายอยู่บนจอตลอดทั้งรอบ** —
   ก่อนยิง (t=18 วิ) `100` Lv.1 หลอดเต็ม · หลังครบสี่เฟรม (t=66.5 วิ) `100` **ไม่ขยับแม้แต่หน่วยเดียว**
   ทั้งที่ดาเมจสะสม `63 + 379 + 63 = 505` · HP ผู้เล่นก็ `100/100` ตลอด
   ⇒ **เดิมยืนยันได้แค่ฝั่งผู้เล่น รอบนี้ยืนยันฝั่งเป้าหมายด้วย** — ตอกย้ำ DAMAGE-MODEL-001:
   **`CHitResult` ไม่แตะ HP ของใครเลย client เป็นตัวแสดงผลล้วน ๆ**
   🔴 **น้ำหนักหลักฐาน = คำบอกเล่าของผู้เทส + ภาพที่เซฟไว้จริง ไม่ใช่ใบเสร็จที่ re-derive ได้**
   (ผู้เทสหยุดก่อนเขียนจดหมายเอง · ข้อความถอดจากภาพหน้าจอที่ Panya ส่งมา ~15:15)
   🔴 **ชั้น wire ของรอบใหญ่ #10 ไม่มีหลักฐานเก็บไว้เลย** (ไม่มี teardown ⇒ ไม่มี console tail ·
   ไม่มีไฟล์ capture ลงวันที่ 20 ส.ค. เลย — `capture_v141\GAME_LIVE.txt` ที่มีอยู่ลงวันที่ 18 ส.ค.)
   ⇒ **ผลรอบนี้อ้างได้เฉพาะชั้น client-observable ห้ามอ้างเป็นหลักฐานชั้น wire เด็ดขาด**
   ⚠️ ข้อ ⑥ เทียบเฟรม 1 กับเฟรม 4 ในวิดีโอแล้ว **ยังไม่ต่างในระดับที่ตาเห็น** — สถานะไม่เปลี่ยน
ข้อความเต็มตอน PENDING: `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R102_GT027_028_029.md`

## GT-029 DYING-COUNTDOWN-001  [✅ **PASS — รอบใหญ่ #9 · และคำถาม static ที่มันเปิด ถูกปิดแล้วในรอบ 102**]

**ผล:** เลขในวง**ลดจริง** — จับได้ 4 ค่าในรอบเดียว (19 → 15 → 13 → 10 → หาย) สองรอบอิสระ · wire มีแค่ SPAWN+DYING_LATCH (`DEATH_TASK` = 0 ทั้งไฟล์) · เมื่อถึง ~0 เลขหายเฉย ๆ NPC ยังนอน ไม่มีอะไรเกิดต่อ
⭐ **คำถามชี้ขาด "UI อ่าน field เดียวกับ predicate ไหม" — static R102 ตอบแล้ว: (ข) UI นับเอง** (`FACTPACK_R102_DYING_COUNTDOWN_UI_FIELD_STATIC.md` · [PROVEN] 3 ชั้น: ไม่มี writer ลด `attr+0x58` ในทั้งอิมเมจ · ผู้อ่าน float ของ field มี 3 ที่ล้วน predicate · ไม่มี display path ใดอ่าน field นี้)
⇒ **GT-021 ยังถูก · เฟรมที่สี่ (timer=0.0) ยังจำเป็น · ledger ของ GT-021/HYP-PF-021 ไม่ต้องรื้อ — เรื่องนี้ปิด**
ข้อความเต็มตอน PENDING: `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R102_GT027_028_029.md`

## 🆕 GT-034 HOSTILE-NATIVE-001: เดินไปหา hostile ตัวจริง — มันขึ้นแดงเองโดยไม่ splice ไหม  [⏸ **รอ Panya เคาะเรื่องระยะทาง — ห้ามออกแบบท่าเดินก่อน (คำสั่ง 2026-08-20 ~11:40)**]

**ที่มา:** ORDER `20260820_1140_PANYA-ORDER-retarget-real-hostile.md` — เทสที่ผ่านมายิงใส่ `0x2001` ซึ่งเป็น **NPC เมือง faction 4** · Panya สั่งเปิดเลนใหม่เล็ง hostile faction-6 ตัวจริง 13 ตัว
**สถานะตามเงื่อนไขใน ORDER เอง:** *"ถ้าไกลจนเดินไม่ไหว ให้รายงานระยะทางมาก่อน อย่าเพิ่งออกแบบเทส"* ⇒ chief รายงานแล้ว: **ตัวใกล้สุด `0x201F` Tornado Eagle อยู่ ~11,914 หน่วย** (เทียบ 0x2001 = 100 หน่วย) — บัญชีเต็มทั้ง 13 ตัว (XYZ · ระยะเรียงใกล้→ไกล · HP · faction/aggro · drops): **`FACTPACK_R102_HOSTILE13_ROSTER.md`**
**ตัวเลือกที่รอ Panya เคาะ:** ① เดิน (ควรให้ผู้เทสวัดอัตราเดินก่อน: hold_key W 10 วิ อ่าน ΔX) · ② เลน teleport opt-in (V129 พิสูจน์ `TeleportWithVehicle` handshake ไว้แล้ว — chief ออกแบบใหม่ได้ใต้ pattern มาตรฐาน) · ③ เลือกตัวอื่น/วิธีอื่น
🔴 **ข้อควรระวังที่ได้จาก roster:** ตัว aggressive (`AGGRO=1200`): `0x203B` Jungle Big Tiger · `0x2040` Ward Apes · `0x2085` Orc Chief — **อย่าใช้เป็นเป้าแรก** · `0x201F` เป็น retaliate-only เหมาะสุด
**คำถามหลักเมื่อรันได้:** hostile ตัวจริง**ขึ้นแดงเอง**ตอน scene-load โดยไม่ต้อง splice faction ไหม · ⭐ ผลลบมีค่าเท่าผลบวก (= faction ของ placement ไม่ได้ถูกส่งตอน scene-load → redirect Door A ทั้งประตู)
**nonclaim บังคับ:** faction/AI/drop เป็นข้อมูลที่ ship มากับ client — ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
⚠️ **เลขชนกัน:** จดหมายผู้เทส 12:00 เสนอ "GT-034 DAMAGE-TARGET-AB-001" — **คำสั่ง Panya ชนะเลขนี้** · ข้อเสนอผู้เทสได้เลขใหม่ = **GT-038** (ด้านล่าง)

## 🆕 GT-035 DAMAGE-ON-HOSTILE-001: ทำซ้ำ GT-027/028 บน hostile ตัวจริง  [🔴 **BLOCKED — รอ GT-034 (ทั้งการเคาะระยะทาง และผล native-red)**]

ตาม ORDER ลำดับ 2 · โครง: profile npc_sweep เปลี่ยน target identity เป็นตัวที่ Panya เลือกจาก roster (ต้องเปิด hypothesis slot ใหม่ — HYP-PF-024 ใช้ 3/3 แล้ว ตรวจงบก่อน build) · chief จะออกแบบเต็มเมื่อ GT-034 ได้ข้อสรุป

## 🆕 GT-036 KILL-HOSTILE-001: วงเต็ม "ตี → เลือด → ตาย" บน hostile ที่มี HP จริงจาก STANDARD_MOB  [🔴 **BLOCKED — รอ GT-034/035**]

ตาม ORDER ลำดับ 3 · โครง: ทำซ้ำ GT-031 (HYP-PF-026) แต่ ladder ใช้ HP baseline ของตัวที่เลือก (เช่น Tornado Eagle lvl 27 = 3,857) · nonclaim เดิมทุกตัว + HP เป็น baseline ฝั่ง client

## 🆕 GT-037 LOOT-ROLL-001: server-side loot roller จาก client tables  [🟢 **งาน dev headless ของ chief — ไม่กินคิวสะพาน ไม่ต้องเปิดเกม**]

ตาม ORDER ลำดับ 4 = ดราฟต์ R100 §3 ประตู 2 · pure logic + unit tests ถึง Grade A ได้โดยไม่มี client · **chief จะเริ่มรอบถัดไป** (รอบ 102 หมดไปกับ ORDER งานแรก + ปิดผลเทส) · ไม่มีอะไรให้ผู้เทสทำในรายการนี้

## 🆕 GT-038 DAMAGE-TARGET-AB-001: A/B — การคลิกเลือกเป้าเกี่ยวอะไรกับเลขที่มองเห็นไหม  [🟢 **PENDING — โปรโตคอลพร้อม · static R102 ทำนายผลไว้ล่วงหน้าแล้ว**]

**ที่มา:** ข้อเสนอผู้เทสในจดหมาย 12:00 (เดิมเรียก GT-034 — เปลี่ยนเลขเพราะชนคำสั่ง Panya) · ปริศนา: สองเซสชันผู้เทสไม่เห็นเลข ทั้งที่ไบต์เหมือนเซสชันของ Panya ที่เห็นครบ · ความต่างที่วัดได้เดียวในล็อก = `TargetVital 0x1ADD` (มีเฉพาะเซสชันที่เห็นเลข)
**static R102 (`FACTPACK_R102_TARGETVITAL_AND_FXNUMBER_GATES_STATIC.md`) ตอบล่วงหน้า [PROVEN]:**
- สมมติฐาน (ก) "ต้องเลือกเป้าก่อนเลขถึงขึ้น" = **หักล้าง** — เลขขึ้นเพราะ performer==localplayer + resolve `0x2001` สำเร็จ · TargetVital เป็นแค่**พยาน**ว่า `0x2001` resolve ได้ (common cause) ไม่ใช่สาเหตุ
- สมมติฐาน (ข) "TargetVital ใบหลังเป็นผลของเฟรม HIT_REACTION" = **หักล้าง** — subtree ของ CHitResult ไม่มีทางเรียก send TargetVital
- เกตที่อธิบายจอมืดได้จริง: ① resolve `0x2001` ล้มเหลว ณ เวลาเฟรม (timing การลงทะเบียน) ② **toggle `[localplayer+0x420]` = 0** (ดูบทเรียนเครื่องมือ ⬇)
**โปรโตคอล (บูตเดียว · scenario `damage_model_hypothesis_npc_sweep.json` เดิม):** แขน A = ไม่แตะเมาส์เลยหลังเข้าแมพ ยิง trigger · แขน B = คลิกเลือก NPC (`Navy Transfer`) ก่อน แล้วยิง trigger รอบใหม่ (relaunch client รีอาร์ม one-shot ระหว่างแขน)
**ข้อบังคับทั้งสองแขน:** กล้องเห็นผู้เล่น+NPC เต็มตัว · **ห้ามพิมพ์อะไรนอกช่องแชตที่โฟกัสแล้ว** (กัน hotkey 0x27) · ใช้ client ที่เพิ่งเปิดใหม่ (toggle default ON)
**คำทำนาย static:** ทั้งสองแขน**ควรเห็นเลขเท่ากัน** — ถ้าแขน A มืดแต่ B เห็น = static ผิด จดละเอียด · ถ้ามืดทั้งคู่บน client ใหม่ = ปัญหาคือ resolve-timing ไม่ใช่ toggle
**pass criteria สองชั้น:** ① wire: เฟรมครบทั้งสองแขน ② client: บันทึกเลขเห็น/ไม่เห็น ต่อแขน + มี/ไม่มี `TargetVital` ในล็อกต่อแขน
## GT-030 REMOTE-PLAYER-VIS-001: "มีคนอื่นอยู่ในโลก" ครั้งแรก — actor_type 2 ทั้ง 5 เฟรม  [🟢 **PENDING — พร้อมรันหลัง commit ของ chief รอบ 96 (HYP-PF-025 · multiplayer ก้อน 2)**]

**ที่มา:** ทุกเฟรม "ตัวอื่นในโลก" ที่เคยส่ง = `actor_type 4` (NPC) ทั้งหมด · เลนใหม่ส่ง **`actor_type 2` = `CNetActor` สาขา remote player** เป็นครั้งแรกในประวัติโปรเจกต์
⭐ **nonclaim ที่ต้องติดทุกผล: นี่คือดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** (ไม่มี capture remote human player ในคลังเลยแม้แต่เฟรมเดียว)

**boot (ท่าเดียวกับ GT-024/027 เป๊ะ เปลี่ยนแค่ flag):**
- `--remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json` (+ `--db` สำเนาตามปกติ)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → sweep **5 เฟรม ห่างกัน 15 วิ/เฟรม** (75 วิทั้งชุด — เผื่อเวลาถ่ายทุกเฟรม)
- console label = `HYP_PF_025_REMOTE_PLAYER_<STEP>` · event = `remote_player_hypothesis_visibility_probe_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
- **one-shot** — ยิงซ้ำได้ event `..._already_sent_no_reply` · ถ้า compose ถูกปฏิเสธจะเห็น `..._compose_refused_no_reply_<เหตุผล>` ใน log และไม่มีไบต์ออกเลย
- ก่อนยิง: ยืนหันกล้องทิศ **+X** จากจุดเกิด (probe ทั้งสามอยู่แนวนั้น ห่าง ~112–412 หน่วย) · ถ่าย baseline ก่อน 1 ใบ

**สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
| t | เฟรม | ถ่ายอะไร |
|---|---|---|
| +0s | `SPAWN_BARE` — identity A `0x00A00001` ชื่อ `ProbePlayer01` ที่จุด placement-0 | มีอะไรโผล่ไหม? รูปร่างอะไร (คน/กล่อง/ตัวใส)? ป้ายชื่อขึ้น `ProbePlayer01` ในช่องไหน? |
| +15s | `SPAWN_AVATAR` — identity B `ProbePlayer02` ที่ X+150 **พก AvatarAttr ของตัวละครที่เลือกอยู่ (replay)** | **B ต่างจาก A ตรงไหน — นี่คือคำตอบของคำถาม "AvatarAttr จำเป็นไหม"** ถ่ายให้เห็นทั้งคู่เฟรมเดียว |
| +30s | `MOVE_A_1` — MovementAttr เดี่ยว mask `0x01` → A ควรย้ายไป X+300 | A ขยับไหม? เดินหรือวาร์ป? (คำทำนายจาก CHUNK2-Q2: heading/mode/flags โดนรีเซ็ตเป็น 0 เพราะเฟรมก่อนหน้าเป็นของ B) |
| +45s | `MOVE_A_2` — mask `0x03` heading π/2 | A หันหน้าไหม? |
| +60s | `NEGATIVE_CONTROL` — identity C ที่ X−150 พก **NPCAttr ผิดคลาสโดยตั้งใจ** (ชื่อ `ProbeControl03`) | มีตัวโผล่ไหม และ **ป้ายชื่อต้องว่าง** (bind gate `0x4697B0` เกต CNetNPC ต้อง drop เงียบ) |
| หลังจบ | เดินเข้าไปใกล้ A/B/C ลองคลิกซ้ายทีละตัว | target panel ขึ้นไหม / ชื่อในพาเนลตรงกับป้ายไหม / ตัวจม-ลอยพื้นไหม (ground Z ไม่ได้ตรวจ — ไม่ falsify) |

**pass criteria สองชั้น:** ① wire = 5 เฟรมออกครบตาม label + delay (console) ② client = ตอบได้อย่างน้อยว่า เฟรม 1 มีอะไรโผล่หรือไม่ + เฟรม 5 ป้ายชื่อว่างหรือไม่ — **ผลลบก็มีค่า** (ไม่มีอะไรโผล่เลยทั้ง A/B = actor_type 2 spawn แล้วไม่เรนเดอร์ด้วย mask 0 → จดเป็นผล ไม่ใช่ fail)
**เกณฑ์หยุดทั้งเลนทันที:** ⛔ เฟรม 5 **ขึ้นชื่อ** `ProbeControl03` (= ข้ออ้าง bind-gate ของก้อน 1 ผิด — ทุกข้อสรุปก้อน 1 ต้องรื้อ) หรือ server log มี `ErrorData=28317`
🔴 **ไม่มีทาง despawn probe** — สามตัวจะค้างจนตัด connection · จบเทสให้ปิด client แล้ว teardown ตามปกติ · run copy ทิ้งได้
🔴 อย่าลืม: HP ของ probe = 100 ทุกตัว ห้ามมีเฟรมไหน HP 0 (ถ้าเห็นตัวไหน "ตาย" เอง = ผิดคาด จดละเอียด)
**nonclaims บังคับ:** ดีไซน์ของเรา · ไม่ claim ว่า mask bit ไหนของ ActorAttr จำเป็นต่อการเรนเดอร์ · ไม่ claim ว่า avatar ถูกยอมรับใต้ identity อื่น (จนกว่าจะเห็น B) · นี่ไม่ใช่ผู้เล่นสองคนจริง (ก้อน 3 ยังไม่อนุมัติ)

## GT-031 DAMAGE-HP-LINK-001: วงเต็ม "ตี → เลือด → ตาย" ครั้งแรก — เลขลอย + หลอด HP ลดจริง + ตายจบ  [🟢 **PENDING — พร้อมรันหลัง commit ของ chief รอบ 97 (`af10536` · HYP-PF-026)**]

**ที่มา:** GT-024 พิสูจน์ว่าเลขความเสียหายเรนเดอร์บนจอ **แต่ HP ไม่ลด (ยืนยันสองปาก)** · GT-019 พิสูจน์ว่า hp 0 + timer เปิดหน้าต่างตาย · **สองข้อเท็จจริงนี้ไม่เคยแตะกันเลย — เลนนี้คือชิ้นกลางที่เชื่อม**: เซิร์ฟเวอร์ทำเลขคณิต HP เอง (100 − 63 = 37 → clamp 0) แล้วส่งทั้ง "เลขลอย" และ "หลอดเลือด" สลับกัน 8 เฟรม
⭐ **nonclaim ที่ต้องติดทุกผล: สูตรและการเชื่อมเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** (รอบ 83 พิสูจน์แล้วว่า client ไม่ลบเลขเอง — นั่นคือเหตุที่ server ต้องพูดทั้งสองครึ่งเอง)

**boot (ท่าเดียวกับ GT-024/027/030 เป๊ะ เปลี่ยนแค่ flag):**
- `--damage-hp-link-hypothesis-scenario scenarios\damage_hp_link_hypothesis_link_sweep.json` (+ `--db` สำเนาตามปกติ)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → sweep **8 เฟรม ห่างกัน 15 วิ/เฟรม** (105 วิทั้งชุด — เผื่อถ่ายทุกเฟรม)
- console label = `HYP_PF_026_HP_LINK_<STEP>` · event = `damage_hp_link_hypothesis_link_sweep_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
- **one-shot** — ยิงซ้ำได้ `..._already_sent_no_reply` · 🔴 **เลนนี้ยิงได้เฉพาะตัวละคร canonical (identity `0x10010001`)** — ถ้าเผลอสร้าง/เลือกตัวอื่นจะได้ `..._identity_not_pinned_no_reply` และไม่มีไบต์ออกเลย (ตั้งใจ: ผู้เทสต้องเห็นไบต์ตรง pin เป๊ะหรือไม่เห็นเลย)
- ก่อนยิง: ถ่าย baseline หลอด HP (ควรเป็น 100/100) + เปิดมุมกล้องเห็นทั้งตัวละครและหลอด

**สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
| t | เฟรม | ถ่ายอะไร |
|---|---|---|
| +0s | `HP_BASELINE` — ActorAttr hp 100/100 | หลอดยัง 100/100 (ถ้ากระพริบ/รีเฟรชให้จด) |
| +15s | `HIT_WEAK` — เลข **63** flags 0x0001 | เลขลอยบนตัวผู้เล่น (เหมือน GT-024) · **หลอดต้องยังไม่ขยับ** — ถ้าหลอดลดที่เฟรมนี้ = หักล้างรอบ 83 ทั้งเลน จดละเอียดสุด |
| +30s | `HP_AFTER_WEAK` — hp_current **37** | ⭐ **หลอดลดเหลือ 37/100 ไหม — นี่คือคำถามหลักของเทสทั้งใบ** |
| +45s | `MISS` — คำว่า MISS flags 0x0000 | MISS ขึ้น (เหมือน GT-024) · หลอดค้าง 37 |
| +60s | `HP_AFTER_MISS` — hp_current 37 ซ้ำ (ไบต์เหมือนเฟรม +30 เป๊ะ) | หลอดค้าง 37 · client กระพริบ/รีเฟรชไหมเมื่อได้ค่าที่ถืออยู่แล้ว (มีค่าทั้งสองทาง) |
| +75s | `HIT_STRONG` — เลข **379** flags 0x0001 | เลขลอย · หลอดยังไม่ขยับ |
| +90s | `HP_ZERO_DYING` — hp 0 + death timer 20.0 **ในเฟรมเดียว** | หลอด 0/100 + **ท่าคุกเข่า + ปุ่ม "ล้มเลิกการช่วยเหลือ"** (เหมือน GT-019) — clamp: 37−379 = floor 0 |
| +105s | `DYING_ELAPSED` — timer 0.0 | **`Main_Dead` ปิด → `Common_Death` เปิด** ("ท่านตายแล้ว…" เหมือน GT-023) · **ห้ามกดปุ่มใด ๆ ในหน้าต่างตาย** (เลนนี้ไม่มี path คืนชีพ — จบเทสด้วย End task ตาม PLAYBOOK) |

**pass criteria สองชั้น:** ① wire = 8 เฟรมครบตาม label+delay (console) ② client = ตอบอย่างน้อย 3 ข้อ: หลอดลดเป็น 37 ที่เฟรม +30 หรือไม่ · หลอดขยับตอนเฟรมเลข (+15/+75) หรือไม่ · หน้าต่างตายเปิดที่ +90/+105 เหมือนตอนเทสแยกไหม — **ผลลบก็มีค่า** (เลขขึ้นแต่หลอดไม่ลด = ตอบคำถาม link เป็นลบ จดเป็นผล ไม่ใช่ fail)
**เกณฑ์หยุด/ตื่นเต้นพิเศษ:** ⛔ หลอดลด**ก่อน**เฟรม hp (คือลดตอนเฟรมเลข) = หักล้าง "client ไม่ลบเอง" ของรอบ 83 — ผลลบที่มีค่าที่สุดที่เป็นไปได้ ถ่ายวิดีโอ/ภาพต่อเนื่องช่วง +15..+30 ไว้ให้มากที่สุด · `ErrorData=28317` ใน log = การสลับ carrier ในเซสชันเดียวพัง หยุดและจด
🔴 หลังหน้าต่าง Common_Death เปิด: ถ่ายภาพแล้ว **End task** ปิด client (ห้ามกด "กลับจุดเกิด"/"คืนชีพที่เดิม" — พฤติกรรมปุ่มพวกนั้นยังไม่มี server path และไม่ใช่คำถามของเทสนี้) · teardown ตามปกติ · run copy ทิ้งได้
**nonclaims บังคับ:** สูตร/การเชื่อมเป็นของเรา · ไม่ claim ว่า HP persist (ไม่มีคอลัมน์ HP ใน DB — balance ตายพร้อม sweep) · ไม่ claim path คืนชีพ · ไม่ใช่ combat จริง (ไม่มี NPC โจมตี — น่ันคือแถว mob_aggro ที่ยัง not_started)

## GT-032 NPC-HOSTILE-001: NPC ตัวแรกของ Port Royal "ขึ้นศัตรู (แดง)" ไหม — Door A ของ mob-aggro  [🟢 **PENDING — พร้อมรันหลัง commit ของ chief รอบ 99 (`87f0769` · HYP-PF-027)**]

**ที่มา:** ดราฟต์ mob-aggro รอบ 98 แยกการสู้เป็นสามประตู — **hostility · attack · hit-lands** — และมีแค่ประตู hostility (Door A) กับ hit-lands ที่พิสูจน์บนสายแล้ว · SCENE-005 เคยทำ **ชื่อแดง + เส้นขอบแดง + แผง target แดง** บนจอจริง โดยจับคู่ faction: **ผู้เล่น 1 vs NPC 6** · แต่ arena-v2 พิสูจน์ว่า **NPC 6 เดี่ยว ๆ กับผู้เล่น faction 0 (ค่าคอนสตรัคเตอร์) = เป็นกลาง** (นับ 1,023 ครั้ง) ⇒ ต้องส่งสองข้าง เลนนี้ทำครบสองข้าง แล้วยิง NPC `0x2001` ตัวเดิมที่ GT-022/025 ทำให้ตาย
⭐ **nonclaim ที่ต้องติดทุกผล: faction 1 และ 6 เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · เลนนี้พิสูจน์ hostility เท่านั้น — **ยังไม่มี NPC โจมตี** (Door B ยังปิด)

**boot (ท่าเดียวกับ GT-024/027/030/031 เป๊ะ เปลี่ยนแค่ flag):**
- `--npc-hostile-hypothesis-scenario scenarios\npc_hostile_hypothesis_faction_pairing.json` (+ `--db` สำเนาตามปกติ)
- 🔴 **เลนนี้ผูกกับ identity `0x10010001` (ตัวละคร canonical smoke) — ตัว StartGame จะได้ faction 1 ต่อเมื่อเป็นตัวนี้เท่านั้น** ถ้าเผลอเลือก/สร้างตัวอื่นจะได้ StartGame ปกติ (ไม่มี faction) แล้ว sweep จะปฏิเสธ `..._player_faction_not_applied_no_reply` — ไม่มีไบต์ออก (ตั้งใจ: เห็นคู่ครบหรือไม่เห็นเลย)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → **sweep 1 เฟรมเดียว** (`HOSTILE_SPAWN`)
- console label = `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` · event = `npc_hostile_hypothesis_faction_pairing_sent` — เห็นชื่ออื่น = บูตผิดไฟล์ · **one-shot** (ยิงซ้ำ `..._already_sent_no_reply`)
- ⚠️ ตอน StartGame ควรเห็น event `npc_hostile_hypothesis_player_faction1_start_game_sent` ใน console **ก่อน** ยิง — ยืนยันว่าครึ่ง entry ลงแล้ว
- ก่อนยิง: เดินให้ NPC `0x2001` (ตัวแรกของ Port Royal ใกล้จุดเกิด — XYZ อยู่ในเฟรม SPAWN) อยู่ในเฟรมกล้อง เห็นทั้งชื่อ/ตัว NPC

**สิ่งที่ควรเห็น (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
- **หลังยิง 1 เฟรม:** NPC `0x2001` เปลี่ยนเป็น **ขึ้นศัตรู** — เส้นขอบแดง · กด Tab เลือกแล้วได้ **ลูกศร/แผง target สีแดง** เหมือนตอน SCENE-005 ทำกับ NPC `0x203D`
- 🔴 **ไม่มีป้ายชื่อแดง** — เฟรมนี้ **ไม่มี name bit** (ต่างจาก SCENE-005 ที่เป็น scene-load) ⇒ สิ่งที่ดูคือ **เส้นขอบ + แผง Tab target** ไม่ใช่ป้ายชื่อ
- **ผลลบมีค่าเท่าผลบวก:** ถ้า NPC **ไม่ขึ้นแดง** (แต่ SCENE-005 แบบ scene-load ยังทำได้) ⇒ faction บิตตอน spawn บนท่อ actor-entry **ไปไม่ถึง relation read** — เป็นคำตอบที่ redirect Door A ทั้งประตู จดละเอียด

**pass criteria สองชั้น:** ① wire = 1 เฟรม `HOSTILE_SPAWN` + StartGame มี faction-1 (console: สอง event ข้างบน) ② client = NPC `0x2001` ขึ้นศัตรู (เส้นขอบ/แผง Tab แดง) หรือไม่ — **ตอบ yes/no พร้อมภาพ** · ถ้า Tab แล้วเลือกไม่ได้/ไม่มีแผงแดง = ผลลบ (จดเป็นผล)
🔴 **จบเทส:** ถ่ายภาพแล้ว **End task** (เลนนี้ไม่แตะ DB · ไม่มี path ใด ๆ ให้กด) · run copy ทิ้งได้ · teardown ตามปกติ
**nonclaims บังคับ:** faction 1/6 เป็นของเรา · ไม่ claim ว่าคู่ (1,6) ทำงานบน NPC ที่ project ผ่าน actor-entry เหมือนตอน scene-load (นั่นคือสิ่งที่เทสนี้วัด) · ไม่มี aggro/threat/chase/attack · ไม่มี persistence (faction ไม่มี write path)

## 🛠️ บทเรียนเครื่องมือใหม่จากรอบใหญ่ #9/#10 (chief รอบ 102 ยกจากจดหมายผู้เทส + static R102)

- 🔴 **เลขดาเมจทั้งหมด (รวม `MISS!`) ปิดได้เงียบ ๆ ด้วยปุ่มเดียว:** client มี toggle `[localplayer+0x420]`
  (input command `0x27` · byte-proven `0x43FE2C je no-draw` / toggle `0x42C68A` / default ON `0x44CAC2`)
  — ปิดแล้ว **จอไม่ขึ้นเลขเลย แต่ wire เหมือนเดิมทุกไบต์ และไม่มีอะไรโผล่ในล็อกเซิร์ฟเวอร์**
  · เข้าคู่กับบทเรียนเดิม "ตัวอักษรตอนช่อง input ไม่โฟกัส = hotkey" ⇒ นี่คือผู้ต้องสงสัยหลักของ
  เซสชันที่ 'ตาบอด' ใน GT-027 รอบแรก
  **กฎใหม่สำหรับทุก GT ที่ต้องเห็นเลข:** ① ใช้ client ที่เพิ่งเปิดใหม่ (default = ON)
  ② ห้ามพิมพ์อะไรนอกช่องแชตที่ยืนยันโฟกัสแล้ว ③ ถ้าจอมืดทั้งเซสชัน → **relaunch client ก่อนสรุปว่า wire ผิด**
  (ยังไม่รู้ว่าปุ่มไหน map ไป command 0x27 — [UNKNOWN] · อย่าไปลองกดหา)
- 🔴 **batch ที่มี `hold_key` แล้วถูกขัดกลางคัน (หน้าต่างอื่นแย่งโฟกัส) = ปุ่มค้าง ตัวละครเดินเอง** —
  เคยพาหลุดไป X `-11,490` (~2,900 หน่วย เสีย ~6 นาที) · **กฎ: batch ล้ม → ถือว่าตำแหน่งไม่น่าเชื่อถือ
  อ่านพิกัดใหม่เสมอ · อย่าใส่ hold_key หลายตัวใน batch เดียวถ้ามีความเสี่ยงเรื่องโฟกัส**
- ℹ️ **ทางลัดหน้าเลือกเซิร์ฟเวอร์ (Panya สั่ง ใช้แล้วได้ผล):** กด `เข้า` ได้เลย ไม่ต้องคลิก server → channel ก่อน

## 🛠️ บทเรียนเครื่องมือจากรอบใหญ่ #8 (chief รอบ 93 ยกมาจากผลของผู้เทส — ใส่ใน template ให้หมด)

1. ⭐ **เปิด client ด้วย `Invoke-CimMethod Win32_Process Create`** ไม่ใช่ `Start-Process -Redirect*` ⇒ ลูกไม่สืบทอด handle **สะพานกลับ idle ทันที** (วงจรอุดตันของรอบ #7 หายถาวร)
   🔴 **ห้ามแค่ลบ `-Redirect*` ทิ้ง** — `Start-Process 'xxx.bin'` ที่ไม่มี redirect ใช้ ShellExecute และ `.bin` ไม่มี file association ⇒ **ล้มเงียบ `-PassThru` คืน `$null`** · redirect มีไว้บังคับ `UseShellExecute=false`
2. 🔴 **การ์ดบังคับก่อนเปิด client ตัวใหม่:** ถ้า `Get-NetTCPConnection -State Established` บนพอร์ต 10188/10189 **> 0 ให้ ABORT** — ดูแค่ `Get-Process = 0` **ไม่พอ** (จ็อบ 925 พลาดข้อนี้ → ค้าง "กำลังเชื่อมต่อ..." เสียเวลา ~15 นาที) ⇒ **ต้องอยู่ในโค้ดของทุก template ที่เปิด client ไม่ใช่ในดุลพินิจ**
3. 🔴 **จ็อบ relaunch client ต้องเขียน `stamp` ของ *รอบบูต*** ไม่ใช่เวลาของตัวเอง มิฉะนั้น guard window ของ teardown (stamp-1 .. stamp+5 นาที) จะไม่ครอบ console ที่บูตไปก่อน (จ็อบ 918 → 919 fail exit 15)
4. **แชตในเกม: ถ้าไม่ได้โฟกัสช่อง input จริง ตัวอักษรจะกลายเป็น hotkey** ⇒ ท่าที่ปลอดภัย: เลื่อนเมาส์ไปเหนือแผงแชต → คลิกแถบ input → **ถ่ายยืนยันว่าข้อความอยู่ในช่องแล้ว** → กด Enter **ในการเรียกครั้งเดียวกัน**
5. **ทริกเกอร์ต้องเป็น ascii 12 ตัวอักษรจริง ๆ** — `PFPROBE2` (8 ตัว) เฟรมถึงเซิร์ฟ (`0xAC52` 46 ไบต์) แต่ **ไม่เข้าเงื่อนไข ไม่มี sweep ออกมา** ⇒ ความยาวเป็นส่วนหนึ่งของ predicate
6. **หน้าต่างเซิร์ฟเวอร์ (py.exe) เปิดทับหน้าต่างเกมเสมอหลังบูต** — ผู้เทส local ต้องขอสิทธิ์ `py.exe` ไว้ด้วยเพื่อสลับหน้าต่างได้ (tier `click` พอ)
7. **เลขจ็อบ:** ผู้เทสใช้ **9xx** เท่านั้น (รอบใหญ่ #8 ใช้ 912–932 ⇒ ตัวถัดไป **933**) · chief ใช้เลขวิ่ง 1xx (รอบ 99 ใช้ 161 ⇒ ตัวถัดไป **162**)
