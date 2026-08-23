# GAME TEST QUEUE — คิวเทสในเกม

> 📌 **R124 (2026-08-23 ~10:4x +07:00 · chief cloud) — GT-045 ปลดจาก "รอ chief" · คิวขยับใบเดียว:**
> **GT-045 → 🟡 BLOCKED-รอ-merge** — เลนเซิร์ฟเวอร์สร้างแล้ว (HYP-PF-032 GROUND-LOOT-001 · PR รอ gate)
> ชื่อจริง: flag `--ground-loot-hypothesis-scenario` · scenario `scenarios/ground_loot_hypothesis_bit08_render.json`
> (ชื่อเสนอเดิม `groundloot-render-*` **เลิกใช้**) · ดีไซน์จริง: สองเฟรม เฟรมละหนึ่ง element ยิงเองตอนเข้าแมพ —
> **อ่านใบ GT-045 ฉบับแก้ใหม่ทั้งใบก่อนบูต** (steps/พิกัด/pass criteria เปลี่ยนหมด)
> ที่ค้างไม่เปลี่ยน: **GT-047 → GT-046 → GT-045 (เมื่อ merge) → GT-001 re-arm** · GT-034/035/036 รอคำเคาะ
> ⚠️ erratum เวลา: ทุกที่ที่ R123 เขียน "~16:xx +07:00" ให้อ่านเป็น **~09:0x +07:00** (แปลงโซนซ้ำ — ดูจดหมาย R124)
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R124_TO_ATTENDED_20260823_1030.md`

> 📌 **R123 (2026-08-23 ~16:xx +07:00 · chief cloud) — บริโภครอบใหญ่ #13 (14 ใบ) · flip 11 รายการ + ใบใหม่ 3:**
> ✅ PASS: **GT-038** (selection ไม่ใช่เงื่อนไขของเลข) · **GT-041** (no-rejection · relog = last-wire) · **GT-043** (survival · 0–3.524s unobserved) · **GT-042** (re-derive + erratum handler len 47) · **GT-044** (BG0001 = scene id 1) · **GT-001** (smoke `cf81730` · CANON_SHA ใหม่ `23FD885A…`)
> 🟡 **GT-034 NO-RESULT** (ไปถึงพิกัดคาดแต่ไม่เห็นตัว — GT-035/036 คง BLOCKED · รอ Panya เคาะทางไป) · 🟡 **GT-033C** ผลลบมีค่า (ไม่ transition · A/B ยัง BLOCKED-INPUT) · 🟠 **GT-030 CLIENT NO-RENDER** — ห้ามรันรอบสาม
> 🆕 ท้ายไฟล์: **GT-045** GROUNDDROP-RENDER [attended · 🔴 BLOCKED รอเลนใหม่+gate] · **GT-046** PICKUP-DIRECTION [STATIC-ON-BRIDGE · พร้อม] · **GT-047** RUNTIMEPROTO-CAPTURE-VALIDATE ปิด F2 [STATIC-ON-BRIDGE · พร้อม · ต้องรันบน Windows]
> **ที่ค้างสำหรับรอบเทสถัดไป: GT-047 → GT-046 → (GT-001 re-arm หลัง merge สำคัญถัดไป)** · GT-034/035/036 รอคำเคาะ · GT-045 รอ chief
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R123_TO_ATTENDED_20260823_1615.md`

> 📌 **R122 (2026-08-21 ~14:4x +07:00 · chief cloud) — คำตัดสิน Panya 11:04 บริโภคแล้ว · คิวขยับ 3 จุด:**
> ① **GT-034 → 🔴 BLOCKED-รอ-merge** (ปลดจาก "รอ Panya เคาะ") — เป้า `0x201F` Tornado Eagle · วิธี = ย้ายจุดวางตัวละคร+heading (GEO-PF-006 · commit `b665d92` รอ gate) · ใบเขียนใหม่ทั้งใบ มีบล็อกยืนยันสามข้อก่อนบูต
> ② **GT-035** แก้หัวข้อ: เหลือรอผล native-red อย่างเดียว (ระยะทางเคาะแล้ว) · GT-036 ไม่เปลี่ยน
> ③ 🆕 **GT-044** SCENEID-BG0001-001 [STATIC-ON-BRIDGE] = dump SCENE_NAME/MAP_SCENE_LIST ปิดเลข scene id ของ bg0001 (ท้ายไฟล์)
> ที่ค้าง: **GT-030(rerun) · GT-033(variant C) · GT-038 · GT-041 · GT-001 · GT-042 · GT-043 · GT-044** · GT-034 รอ merge · GT-035/036 BLOCKED
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R122_TO_ATTENDED_20260821_1500.md`

> 📌 **R120 (2026-08-21 ~10:4x +07:00 · chief cloud) — บริโภครอบใหญ่ #12 ต่อ + จดหมายผู้ช่วย GT-040 สามฉบับ · คิวขยับ 5 จุด:**
> ① **GT-032 → ✅ PASS** (ทั้งสองชั้น · เกณฑ์ console-event เดิมของ chief สังเกตไม่ได้โดยโครงสร้าง — แก้แล้ว ดูบล็อกผลใน entry)
> ② **GT-033 → 🟢 variant C พร้อมรัน** (HYP-PF-031 merge แล้ว · ปลดโดย chief R121 — ท่าบูตในบล็อก variant C ท้าย entry · A/B ยัง BLOCKED-INPUT)
> ③ **GT-040 → ✅ DONE** (ผู้ช่วยปิดครบ A/B/C · ผลยังไม่ผ่าน re-derive ปฏิปักษ์)
> ④ 🆕 **GT-042** DROPTHING-REDERIVE-001 [STATIC-ON-BRIDGE] = ใบตรวจซ้ำ GT-040 + decode `0x402A20` (ท้ายไฟล์)
> ⑤ 🆕 **GT-043** POP-SURVIVAL-001 = observation พ่วงเลนบิต `0x02` รอบใหญ่หน้า: ประชากรหายไหมหลังเฟรม count-1 (ท้ายไฟล์)
> ที่ค้าง: **GT-030(rerun) · GT-033(variant C) · GT-038 · GT-041 · GT-001 · GT-042 · GT-043** · GT-034 รอ Panya เคาะ · GT-035/036 BLOCKED
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R120_TO_ATTENDED_20260821_1055.md`

> 📌 **R119 (2026-08-21 ~09:2x +07:00 · chief cloud) — บริโภคผลรอบใหญ่ #12 แล้ว คิวขยับ 3 จุด:**
> ① **GT-031 → ✅ PASS** (ทั้งสองชั้น — ดูบล็อกผลใน entry) ② **GT-030 → 🟡 RERUN โปรโตคอลแก้ใหม่ทั้งใบ**
> (wire ผ่านแล้ว · สาเหตุที่หา probe ไม่เจอ = บรรทัดพิกัดฉบับเดิม stale — probe ผูกกับ NPC 'Navy Transfer' ไม่ใช่จุดที่ยืน
> ⇒ ท่าใหม่: เดินไป landmark ก่อนยิง + ระบุตัวด้วย target panel · **ไม่ต้องรอ merge อะไร — โค้ดเดิมใช้ได้เลย**)
> ③ บทเรียนเครื่องมือรอบ #12 ลงหมวด 🛠️ แล้ว (Return-ก่อน-คลิก ฯลฯ)
> ที่ค้าง: **GT-030(rerun) · GT-032 · GT-033 · GT-038 · GT-041 · GT-001** · GT-040 [STATIC-ON-BRIDGE] · GT-034 รอ Panya เคาะ · GT-035/036 BLOCKED
> จดหมายรอบนี้: `notes_to_chief\FROM_CHIEF_R119_TO_ATTENDED_20260821_0920.md`

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
   - ⚠️ **teardown template ปฏิเสธรอบที่ถูกทิ้ง >420 นาที โดยดีไซน์** (เดิม 180 — ยกเป็น 420 เมื่อ 2026-08-20 ·
     `TEMPLATE_teardown_generic.ps1:135` · แก้ stale โดย chief R119) (stamp age guard → exit 12 —
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

## GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ  [🟢 PENDING (recurring) — 🔁 re-arm หลัง merge สำคัญถัดไป · **PASS ล่าสุดที่ `cf81730` 2026-08-23 01:14 (+07:00)**] 🔁

> ✅ **RESULT 2026-08-23 01:10–01:14 (+07:00) — PASS บน main HEAD `cf81730` (worktree clean)** · full loop: login → Channel 1 → PVP → Arena01 → เข้าแมพ (HP 100/100 · Port Royal · chat online) → ออกด้วย X+ยืนยัน → Ctrl+C สะอาด
> canonical DB SHA เปลี่ยน**แบบคาดหมาย** (session +1): `6BFCEDD5…FE498FC7` → `23FD885AC4CBBFAC5E06C9B11506F6EA9F985DA82F4522383DFCC14A91C1816A` · `CANON_SHA.txt` อัปเดตแล้วโดยผู้เทส · backup ค่าเก่ายังอยู่
> ผลเต็ม: `notes_to_chief/20260823_0115_GT001-PASS-latest-main-smoke.md` (บริโภค R123)

> ✅ **RESULT รอบใหญ่ #3 — PASS ทุกเกณฑ์ที่ `f286945`** · รายละเอียดเต็มย้ายไป archive รอบ 97:
> `archive\GAME_TEST_QUEUE_ARCHIVE_20260820_R97_CLOSED_STUBS.md` ก้อน 2
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

## GT-033 LOGOUT-TRANSITION A/B: response ไหนทำให้ client เปลี่ยนหน้าจริง  [🟡 **variant C รันแล้ว 2026-08-23 00:06 (+07:00) — ผลลบมีค่า: push `0x709E` เฟรมเดียวใน runtime-ready state ไม่ทำให้เกิด persistent transition** · A/B ยัง 🔴 BLOCKED-INPUT (เมนู HOME→`ออก` ไม่รับคลิกสังเคราะห์) · ห้ามอ่านเป็นผลลบของ A/B]

> 🟡 **RESULT variant C 2026-08-23 00:01–00:06 (+07:00)** (บูต green `7b80025` exact tree): server รับ ascii12 trigger + ส่ง pinned `0x709E` 1 ครั้งจริง (PC 38 B / frame 48 B SHA ตรง pin) · client **อยู่หน้าแมพเดิม** ส่ง runtime req ต่อเนื่อง (#44→#95) จนผู้เทสออกเอง ~63 วิ หลัง push
> - ตอบเฉพาะ variant C: **ไม่มี persistent transition** · แยกไม่ได้ระหว่าง "wrong trigger" กับ "right trigger, wrong client state" (อาจต้องอยู่ใน logout-dialog state ก่อน — adversary caveat เดิม)
> - ไม่ claim ว่าไม่มี flash <4s (screenshot latency) · ไม่ได้เทส subcode 01 · ไม่ได้ส่ง `LogoutVital`
> - ผลเต็ม: `notes_to_chief/20260823_0007_GT033C-NO-TRANSITION-709E-PUSH.md` (บริโภค R123)

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

> 🔴 **สถานะรอบใหญ่ #12 ต่อ (จ็อบ 968/969 · บริโภคโดย chief R120):** บูต variant B ได้ เข้าแมพได้ เปิดเมนู HOME ได้
> **แต่รายการ `ออก` ไม่รับคลิกสังเคราะห์ 4 ครั้งติด** (zoom ยืนยันพิกัด · mouse_move ก่อนคลิก · double-click — เงียบ) ·
> `Return` ช่วยไม่ได้เพราะรายการเมนูไม่ใช่ปุ่ม default ⇒ **client ไม่เคยส่ง LogoutVital ⇒ ไม่มีผล variant ใดทั้งสิ้น — ห้ามอ่านเป็นผลลบ**
> 🆕 **variant C (chief R120 build · HYP-PF-031 LOGOUT-CHAT-PUSH-001 · ✅ gate เขียว + merge แล้ว — ปลดโดย chief R121):**
> ตัด HOME→`ออก` ออกจากสมการ — บูต `--logout-hypothesis-scenario scenarios\logout_hypothesis_chat_push_return_select.json`
> แล้วพิมพ์แชต ascii 12 ตัว (ท่า trigger เดียวกับ GT-032 ที่ผู้เทสทำได้แน่ผ่าน `Return`) ⇒ server **push**
> `ReturnSelectServerVital 0x709E` (เฟรม 48 ไบต์แช่แข็งตัวเดียวกับ variant B · sha256 pin เดิม) **โดยไม่รอ LogoutVital** ·
> คำถามที่ใบนี้ตอบ: client transition จาก push เดี่ยว ๆ ไหม — **yes = 0x709E คือ trigger จริงและไม่ต้องการ request pairing** ·
> no = transition ต้องการ pairing/ตัวอื่น (แล้ว variant A close-path ยังต้องรอเมนูหรือคนกดจริง ⇒ ยกเป็นใบที่ต้องมี Panya หน้าจอ)
> 🔴 **คาเวียตจาก pf-adversary (R120) — อ่านก่อนตีความผล:**
> ① **ผลลบของ variant C กำกวมโดยธรรมชาติ** — client อาจ consume `0x709E` เฉพาะตอนอยู่ใน state ของ logout dialog
> (state ที่เราไปไม่ถึงเพราะเมนูกดไม่ได้ — ตัวบล็อกเดียวกันที่ทำให้ต้องมีใบนี้) ⇒ ผลลบแยกไม่ออกว่า
> "0x709E ไม่ใช่ trigger" หรือ "เป็น trigger เฉพาะ state ที่เราสร้างไม่ได้" · **ผลลบห้ามสรุปข้ามไปหา connection-teardown ทันที** — จดว่า client ทำอะไร (เมิน? แชตค้าง? อาการใด ๆ)
> ② **one-shot latch เป็นราย connection** — ถ้า relog/reconnect ระหว่างเทส แชตอีกครั้งจะ push ซ้ำได้ ⇒ ถ้าเห็น push ครั้งที่สอง **จดว่ามี relog เกิดขึ้น** อย่าอ่านเป็นบั๊ก
> ✅ **ปลดแล้ว (chief R121 · 2026-08-21 ~11:1x +07:00):** HYP-PF-031 merge เข้า `main` แล้ว (merge commit `c6146a3`) ·
> **ท่าบูต: `git checkout 7b8002522fedeecf9bcd5ea9d0d4ec5e732e4034` (detached HEAD — บูตคำตัดสิน ไม่ใช่ branch)**
> commit นี้มีคำตัดสินเขียวของตัวเอง (`conclusion=success` run 32444037989 · 2026-08-21T03:44:20Z UTC = ~10:44 +07:00)
> และ tree byte-identical กับ main `c6146a3` (วัดโดย `pf_resolve_green_boot.py` — จะยืนยันสดก่อนบูตก็ได้:
> `py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch`) · เขียวนี้คือ subset บน Actions ไม่ใช่ gate เต็ม  [✅ **PASS ทั้งสามใบ — ⤴ ย้ายเนื้อหาเต็มไป archive แล้ว (chief รอบ 111)**]

เนื้อหาเต็ม (ผล · หลักฐาน · nonclaims · ข้อความตอน PENDING) อยู่ที่ `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260821_R111_GT027_028_029_CLOSED.md` — **ไม่มีอะไรถูกลบ**
- **GT-027 DAMAGE-ON-NPC-001** ✅ PASS (รอบใหญ่ #10 rerun ที่ Panya ขับเอง) — เลขเรนเดอร์ครบ แต่ **HP ของเป้าไม่ขยับแม้แต่หน่วยเดียวทั้งที่ดาเมจสะสม 505** ⇒ รายงานที่ re-derive ได้: `ServerProject\reports\PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md` ⇒ เป็นที่มาของ **GT-039** ด้านล่าง
- **GT-028 DAMAGE-SLOW-SWEEP-001** ✅ PASS — เหลือข้อ ⑥ (flags `0x0009` vs `0x0001` ต่างกันตรงไหนบนจอ) ที่ยังตอบไม่ได้ · **ไม่บล็อกอะไร ไม่ต้องรันรอบใหม่เพื่อข้อนี้**
- **GT-029 DYING-COUNTDOWN-001** ✅ PASS — เลขในวงลดจริง และคำถาม static ที่มันเปิด (UI นับเอง) ปิดแล้วในรอบ 102

## 🆕⭐ GT-034 HOSTILE-NATIVE-001: hostile ตัวจริงขึ้นแดงเองตอน scene-load โดยไม่ต้อง splice faction ไหม — เป้า `0x201F` Tornado Eagle · วิธี = ย้ายจุดวางตัวละคร + heading ตอนเข้าเกม  [🟡 **PENDING / NO-RESULT — รันแล้ว 2026-08-22 23:56 (+07:00) กรณี 3: ไปถึงพิกัดคาดจริงแต่ไม่เห็นตัวนกเลยหลังกวาด 360° — คำถามหลักยังไม่ถูกตอบ · ห้าม redirect Door A · GT-035/036 ยัง BLOCKED**]

> 🟡 **RESULT 2026-08-22 23:47–23:56 (+07:00) — NO-RESULT ตามตารางกรณี 3** (บูต green `b665d92` exact tree):
> - placement ทำงานตามดีไซน์: HUD `X 1,847 / Y -7,837` ตรงค่าคาดเป๊ะ (wire `1847.5244, -7837.6978, z 931.04, heading π` · TeleportVital รายงานกลับตรงทุกค่า **ยกเว้น z ที่ client ปัดเป็น `931.0`**) — **GEO-PF-006 ชั้น wire/client พิสูจน์แล้ว**
> - แต่กวาด Q ครบ 360° ที่จุดวาง: **ไม่เห็นมอนสเตอร์รูปนก/ป้ายชื่อ `Tornado Eagle` เลย** ไม่ถูกโจมตี · ไม่มี S2 (โดยเจตนา — ไม่มีเป้าให้เลือก)
> - runtime outbound **ไม่มี** label ตระกูล population/NPC/actor (scenario เป็น load-only ตามดีไซน์) ⇒ แยกไม่ได้ว่า "client ไม่ spawn จากข้อมูล ship เอง" หรือ "ตัวอยู่แต่ไกล/มุมอื่น/เงื่อนไข render อื่น"
> - 🔴 ห้ามอ่านเป็น "เห็นตัวแต่ไม่แดง" (ผลลบนิยามแคบของใบนี้) · **ห้าม redirect Door A** · GT-035/036 คง BLOCKED
> - คำถามถัดไปที่ต้องเคาะก่อนออกแบบรอบใหม่ (chief จะเสนอในจดหมาย): ตัวเลือกการแตกสาเหตุ เช่น วางจุดสังเกตหลายจุด / ตรวจว่า client มีเงื่อนไข spawn NPC ฝั่ง data ที่ต้องการเฟรมจาก server
> - ผลเต็ม: `notes_to_chief/20260822_2359_GT034-NO-RESULT-native-render.md` (บริโภค R123) · tooling notes: right-drag ทำกล้อง top-down ค้าง · teardown template เลือก capture root ผิดเมื่อไม่ส่ง `CaptureFilter` (ฝากเจ้าของ tooling)

**ที่มา:** ORDER `20260820_1140_PANYA-ORDER-retarget-real-hostile.md` + **คำตัดสิน Panya
`notes_to_chief/consumed/20260821_1104_PANYA-DECISION-GT034-spawn-relocate.md` (2026-08-21 11:04 +07:00)** —
ปลดสถานะ "⏸ รอเคาะเรื่องระยะทาง" ที่ค้างตั้งแต่ 2026-08-20 ~11:40
- ① เป้า = **`0x201F` Tornado Eagle** (ตัวเดียวใน 13 ตัวที่ **retaliate-only** · บัญชีเต็ม: `FACTPACK_R102_HOSTILE13_ROSTER.md`)
- ② วิธี = **แก้จุดวางตัวละครตอนเข้าเกม + ตั้ง heading หันเข้าเป้าตั้งแต่วินาทีแรก**
  🔴 **ห้ามออกแบบท่าเดิน · ห้ามให้ผู้เทสวัดอัตราเดิน · ห้ามเปิดเลน teleport เพื่อใบนี้** — Panya ตัดทิ้งทั้งสองทางเอง
- 🔴 **ห้ามเปลี่ยนเป้าเป็นตัว aggressive** (`0x203B` Jungle Big Tiger · `0x2040` Ward Apes · `0x2085` Orc Chief — AGGRO=1200) — Panya ไม่ได้อนุญาต
- เลนที่ build แล้ว (chief รอบ 122 · GEO-PF-006): scenario `scenarios/port_royal_tornado_eagle_p30_load_only.json`
  บนเลน scene_load เดิม — **read-only session = เขียน DB ไม่ได้โดยโครงสร้าง** · เขียว(cloud sanity) 1868 pass · **ยังไม่ merge**

**คำถามหลัก (คำต่อคำจาก Panya — ห้ามแก้แม้แต่ตัวอักษรเดียว):**
> **hostile ตัวจริงขึ้นแดงเองตอน scene-load โดยไม่ต้อง splice faction ไหม**

⭐ **ผลลบมีค่าเท่าผลบวก** — ถ้าไม่ขึ้นแดงเอง = faction ของ placement ไม่ได้ถูกส่งตอน scene-load
⇒ **redirect ประตู A ทั้งประตู** ซึ่งเป็นคำตอบที่แพงพอ ๆ กัน · **จดเป็นผล ไม่ใช่ fail**
🔴 **แต่ผลลบของคำถามหลักมีนิยามแคบ: "เห็นตัวมัน แต่ชื่อ/กรอบไม่แดง" เท่านั้น** — "ไม่เห็นตัวมันเลย" คือ NO-RESULT
ของคำถามหลัก (ดูตารางผลด้านล่าง) **ห้าม redirect Door A จากการไม่เห็นตัว** (กติกาจาก adversary review R122)

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-041 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)

```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว — บูต*คำตัดสิน* ไม่ใช่ branch)
- **exit 3** = ห้ามบูต จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · มีบรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- ⚠️ ณ วันที่เขียน (รอบ 122) โค้ดใบนี้อยู่บน branch `claude/wizardly-wright-hk4raq` (commit `b665d92`) **ยังไม่ merge เข้า `main`**
  ⇒ เครื่องมืออาจคืน commit เขียวที่**ยังไม่มี scenario ใบนี้** — จึงต้องยืนยันสามข้อนี้กับ `<SHA>` ที่จะบูตจริง:
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "scene-load-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/port_royal_tornado_eagle_p30_load_only.json && echo SCENARIO_PRESENT
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (`success` = subset บน Actions ไม่ใช่ gate เต็ม)
2. `git grep` เจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐาน** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6)
3. เห็นคำว่า `SCENARIO_PRESENT`
- **ไม่ครบสามข้อ = ห้ามบูต** ใบนี้อยู่ BLOCKED ต่อ · **ปล่อยไว้ที่เดิม ห้ามลบ ห้ามย้าย**

### คาเวียตแมพ/โซน (ข้อบังคับข้อ 1 ของ Panya — สถานะการยืนยัน ณ รอบ 122)

- **ระดับสูงสุดที่ artifact ที่ commit แล้วตอบได้ = "แมพเดียวกัน":** จุดสังเกตปัจจุบัน (P0+100X) กับเป้า (P30)
  เป็นแถวของ**ตาราง frozen เดียวกัน** `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` 115 แถว (bg0001 / Port Royal)
  และแข็งกว่านั้น: V127/V128 เคยให้ client จริง**ยืนที่จุด +100X ของ P30 นี้เป๊ะ ๆ** ในเลน runtime ที่ผ่านแล้ว
- 🔴 **เลข scene id เชิงตัวเลขยังไม่ถูกพิสูจน์** — ต้อง dump SCENE_NAME (007) + MAP_SCENE_LIST (101) บนเครื่องสะพาน = **GT-044** (ท้ายไฟล์)
- ⇒ ถ้า client โหลดแล้วเจอ**พื้นที่ผิด/ว่างเปล่า** — **นั่นแหละคือคำตอบเรื่องโซนที่เดินทางมาถึง** ถ่ายภาพ จดพิกัด HUD
  ออกจากเกม รายงานกลับ · **ห้ามวนบูตซ้ำเพื่อ "ลองใหม่"** (คำสั่ง Panya: คนละโซนให้หยุด อย่าเดา อย่าดันต่อ)

### คาเวียต Z และทิศกล้อง (การตีความของ chief — เปิดเผยต่อ Panya ในจดหมาย R122 · ถ้าไม่เห็นด้วยแก้ค่าเดียวจบ)

- **Z ของจุดวาง = Z ของแถวเป้าเป๊ะ (931.0413208007812) โดยเจตนา** — จดหมายสั่ง "อย่าวางที่ Z เดียวกับเป้าเป๊ะ"
  แต่ความเสี่ยงที่เธอระบุคือลอย/ร่วง (ΔZ +707.7 จากจุดเก่า) · จุดที่เลือกคือจุดที่ **client จริงเคยยืนได้** (V127/V128)
  = หลักฐานกันร่วง/ลอยที่แข็งที่สุดที่มี — ตีความตามเจตนา ไม่ใช่ตามตัวอักษร · **ตัวละครร่วง/ลอย/จมพื้น = จดพิกัด HUD Z
  แล้วดำเนินต่อได้ ไม่ใช่ falsify**
- **trade-off ที่แลกมา:** จุด +100X ยืนได้แน่ แต่ตามแบบแผนที่พิสูจน์แล้ว (V134 camera workaround + R119)
  **กล้องแรกเข้าน่าจะหัน +X = หันหนีเป้า** — heading π ที่เซิร์ฟเวอร์ส่งเป็น **heading ผู้เล่นแรกเข้าที่ไม่ใช่ศูนย์ครั้งแรก
  ของทั้ง lineage** และไม่มีหลักฐานว่า client ใช้มันกับ avatar/กล้อง (nonclaims: `heading_mapping` / `camera_orientation`)
  ⇒ **การหมุนกล้องหาเป้า (~180°) เป็นส่วนหนึ่งของโปรโตคอล ไม่ใช่ความผิดพลาด** · ถ้าเข้าเกมแล้วหันเข้าเป้าเลย
  = การวัด heading_mapping ครั้งแรกที่มีค่ามาก จดทันที

- **objective:** พิสูจน์หนึ่งข้อ: **`0x201F` Tornado Eagle (hostile faction-6 ตัวจริง) แสดงสถานะแดงเองตอน scene-load
  โดยที่เซิร์ฟเวอร์ไม่ splice faction ใด ๆ หรือไม่** — สังเกตล้วน ไม่มีการโจมตี ไม่มีการเดิน

- **db:** สำเนาเสมอ ห้ามเปิด canonical · เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ**
  ```
  copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-034_<yyyyMMdd_HHmmss>.sqlite3
  copy state\pirateforce.sqlite3 state\run_gt034.sqlite3
  ```
  - เลนนี้เป็น **read-only session โดยโครงสร้าง** — คำทำนายคือ*ไม่มีไบต์ไหนของสำเนาเปลี่ยนเลย* ⇒ เก็บ sha256 ของ
    `state\run_gt034.sqlite3` ก่อน-หลังไว้เทียบด้วย (ถ้าขยับ = ผิดคำทำนาย จดว่าแถวไหนขยับ — นั่นคือข้อมูล ไม่ใช่ fail)
  - scenario บังคับตัวละครชื่อ **`Arena01`** · pre-flight บนสำเนา (อ่านอย่างเดียว `mode=ro`):
    `SELECT id,name FROM characters WHERE name='Arena01' AND deleted_at IS NULL;`
    ⇒ ถ้าไม่เจอ **หยุด รายงานกลับ** ห้ามสร้างตัวละครสดเพื่อใบนี้
  - เพราะจุดยืนถูก override โดย scenario ทุกบูต ตำแหน่งเดิมใน DB ไม่มีผลกับใบนี้

- **server args (เป๊ะ · รันจาก working tree ของ checkout ที่ผ่านสามข้อยืนยัน):**
  ```
  py -3 -u -m pirateforce_foundation.app --db state\run_gt034.sqlite3 --scene-load-scenario scenarios\port_royal_tornado_eagle_p30_load_only.json
  ```
  - flag นี้ mutually exclusive กับ scenario โหมดอื่นทุกตัว · 🔴 **ต้องใส่ `--db` ชี้สำเนาเสมอ** — ถ้าลืม เลน scene-load
    จะเงียบ ๆ ไปใช้ `state\test_arena_v1.sqlite3` เป็น default (`app.py:362`) ไม่ใช่ไฟล์ของรอบนี้
  - **เลนนี้ไม่มี chat trigger — ไม่ต้องพิมพ์อะไรเลยทั้งรอบ** (และอย่าลืม: ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส = hotkey)

- **คำทำนาย (จดไว้ล่วงหน้า — คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว):**
  - **P1:** HUD แสดงตัวละครยืนใกล้ `(1847.5, -7837.7)` Z ~931 (ค่าเต็มที่เซิร์ฟเวอร์ส่ง: `1847.5244140625, -7837.69775390625, 931.0413208007812`)
    ⚠️ anomaly ที่รู้ตัว: รอบใหญ่ #12 ผู้เทสยืนห่างจากจุดที่เซิร์ฟเวอร์ส่ง **~731 หน่วย** สาเหตุ [UNKNOWN] —
    **ถ้ายืนไม่ตรงคำทำนาย จดพิกัด HUD จริง แล้วเดินหน้าต่อ นั่นคือข้อมูล**
  - **P2:** Tornado Eagle (มอนสเตอร์รูปนก) อยู่ **~100 หน่วยทาง −X ของตัวละคร** — client เรนเดอร์ placement จาก map data
    ของตัวเอง (พิสูจน์กับ `0x2001` ที่จุดเก่า ระยะ 100 หน่วยเท่ากัน · แต่ **ไม่มีใครเคยเห็น `0x201F` บนจอมาก่อน** — nonclaim `native_render`)
  - **P3 (คำทำนายหลักของกล้อง):** กล้องแรกเข้า**หัน +X = เป้าอยู่ข้างหลัง** ตาม V134/R119 ⇒ ต้องหมุน ~180° จึงเห็นเป้า ·
    ถ้าเข้าเกมแล้วเห็นเป้าเลยโดยไม่หมุน = client ใช้ heading π ที่ส่งไป — **การวัด heading_mapping ครั้งแรก** จดละเอียด
  - **P4 (คำถามของใบ):** ชื่อ/กรอบของมัน**แดงเอง**แบบเดียวกับที่ GT-032 เคยเห็นตอน splice `0x2001` —
    แต่รอบนี้**ไม่มี splice สักไบต์** · ทำนายจาก faction=6 ใน client tables — **นี่คือสิ่งที่ยังไม่รู้จริง**

- **steps (บูตเดียว · สังเกตล้วน ~5 นาทีในเกม):**
  1. ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบ + pre-flight `Arena01` ตามบล็อก db
  2. เปิด **server ก่อนเสมอ** ด้วย args ข้างบน (client ที่บูตโดยไม่มี server ตายใน ~3.5 นาที)
  3. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย
  4. หน้าเลือกตัวละคร → เลือก **`Arena01`** → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
  5. เข้าแมพแล้ว **ห้ามแตะเมาส์/คีย์บอร์ดก่อนถ่าย S0** → **ถ่าย S0 ทันที** ให้เห็น X/Y บน HUD + นาฬิกาบนจอ —
    บันทึกว่า ณ วินาทีแรก กล้องหันทางไหน เห็นอะไรตรงหน้า
  6. **ยืนนิ่ง** สังเกต ~30 วินาที → **ถ่าย S1** มุมมองตรงหน้า
  7. 🔴 **ขั้นบังคับ ไม่ว่าเห็นเป้าหรือไม่:** หมุน**กล้องอย่างเดียว** (เมาส์/Q/E) ให้ครบ **360°** ช้า ๆ — คำทำนาย P3 บอกว่า
    เป้าน่าจะอยู่ข้างหลัง (~180°) · ระหว่างหมุน ถ่ายภาพทุกครั้งที่เห็นสิ่งมีชีวิต/ป้ายชื่อ —
    🔴 **ห้ามกด W/A/S/D ห้ามขยับตำแหน่งเด็ดขาด** (คำสั่ง Panya: ไม่มีท่าเดินในใบนี้)
  8. ถ้าเห็นเป้า: **คลิกซ้ายเลือกมันหนึ่งคลิก** (ท่า target-panel เดียวกับ GT-030/GT-038) → **ถ่าย S2** ให้เห็น target panel:
    ชื่ออะไร · กรอบ/ชื่อแดงหรือไม่ · 🔴 **ห้ามกดสกิล ห้ามกดปุ่มโจมตี ห้ามดับเบิลคลิก** — `0x201F` เป็น retaliate-only
    และ GT-035/036 ยัง BLOCKED · การตีคือใบอื่น
  9. **ถ่าย S3** ภาพสุดท้ายก่อนออก (HUD + นาฬิกา) → ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย
  10. ปิด server · เก็บ raw GAME log ทั้งไฟล์ + console out/err **ห้ามลบ** · เทียบ sha canonical + sha สำเนา อีกครั้ง
  11. **teardown เสมอ แม้เลิกกลางคัน** (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 · `staged\TOOL_stop_stale_server.ps1`) ·
    ⚠️ ถ้า kill client กลางคัน **server ยังถือ session อยู่ — ต้อง restart server ก่อนเปิด client ใหม่** ไม่งั้นค้าง "connecting" ตลอดกาล

- **pass criteria — สองชั้น แยกกันเด็ดขาด ห้ามอ้างชั้นหนึ่งแทนอีกชั้น:**
  - **ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ):**
    - raw GAME log แสดง **StartGameRes พา f32 สี่ตัว** `x=1847.5244140625 · y=-7837.69775390625 · z=931.0413208007812 · heading=pi(3.14159...)`
      และ **เฟรม teleport scene 1 พา XYZ ชุดเดียวกัน** (ไม่ใช่กับดัก `(1,0,(0,0,0))` ของ boot ปกติ)
    - **ต้องไม่มีเฟรม splice/faction injection ใด ๆ ในล็อก** — เลนนี้ population=none, ไม่มี remote_actor (หัวใจของใบ: ไม่ splice)
    - sha256 canonical ก่อน-หลังตรง `CANON_SHA.txt` ทั้งสองครั้ง · sha สำเนา `run_gt034.sqlite3` ก่อน-หลัง (คำทำนาย: เท่าเดิม)
    - **ชั้นนี้ตอบไม่ได้:** มีอะไรบนจอ · นกแดงหรือไม่แดง · กล้องหันทางไหน
  - **ชั้น (2) client-observable (ต้องมีคนหน้าจอ):**
    - ภาพนิ่งบังคับ **S0 · S1 · S2 · S3** ทุกใบเห็นนาฬิกาบนจอ + จด **sha256 ของไฟล์ภาพทุกใบ** ลงในผล
    - ตอบสี่ข้อเป็นภาษาคน: **(ก)** เห็นมอนสเตอร์รูปนกไหม ทิศไหน (เทียบทิศกล้องแรกเข้า) ระยะประมาณเท่าไร
      **(ข)** ชื่อที่แสดง (ป้ายลอย และ/หรือ target panel) คืออะไร · **ชื่อ/กรอบแดง (hostile) หรือสีปกติ (neutral)** — คำตอบของใบทั้งใบอยู่ข้อนี้
      **(ค)** HUD X/Y/Z ที่ยืนจริง เทียบคำทำนาย P1 ห่างกี่หน่วย
      **(ง)** ตอนโหลดเสร็จ (ก่อนแตะอะไร) กล้องหันทิศไหน — เห็นเป้าโดยไม่ต้องหมุนไหม (= คำตอบ P3/heading_mapping)
    - **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ส่ง/ไม่ส่งไบต์อะไร

- **ตารางผล (จดเป็นผลทุกกรณี — ไม่มีกรณีไหนเป็น fail ของผู้เทส):**
  1. **เห็นนก + ชื่อแดงเอง** ⇒ native-red ยืนยัน · GT-035/036 รอ chief/Panya ปลด (**ห้ามปลดเอง**)
  2. **เห็นนก แต่ชื่อไม่แดง** ⇒ **ผลลบของคำถามหลัก — กรณีเดียวที่ redirect ประตู A** (faction ของ placement ไม่ได้ถูกส่ง/ใช้ตอน scene-load)
  3. **หมุนครบ 360° แล้วไม่เห็นนกเลย** ⇒ 🔴 **NO-RESULT ของคำถามหลัก — ห้าม redirect Door A** · จดเป็นผลเรื่อง
    `native_render`/ตำแหน่งยืนจริงแทน (ระยะ/เงื่อนไขเรนเดอร์ = ข้อมูลใหม่) — จดพิกัด HUD + ทุกทิศที่กวาดแล้ว
  4. **โหลดเข้าพื้นที่ผิด/ว่างเปล่า** ⇒ คำตอบเรื่องโซน — หยุด ถ่ายภาพ รายงาน **ห้ามวนบูตซ้ำ**
- **เกณฑ์หยุดเพิ่ม:** นกเข้าโจมตีเองทั้งที่ไม่ถูกตี (ขัด retaliate-only ใน client tables) = ข่าวใหญ่ — ถ่ายภาพ/จดเวลา
  แล้วออกจากเกมทันที ห้ามสู้กลับ

- **nonclaims (บังคับจากคำตัดสิน — ติดไปกับผลทุกกรณี):**
  - faction / AI / drops **เป็นข้อมูลที่ ship มากับ client** ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
  - **การย้ายจุดวางตัวละครเป็นดีไซน์ของเรา** (GEO-PF-006) ไม่ใช่ท่าของเซิร์ฟเวอร์ต้นฉบับ · **ห้าม claim ว่าผู้เล่นจริงเคยเกิดตรงนั้น**
  - ใบนี้**ไม่ตอบ**ว่าตีมันได้ไหม (GT-035) หรือฆ่าได้ไหม (GT-036) — ตอบแค่ "ขึ้นแดงเองไหม"
  - `heading_mapping` / `camera_orientation` / `native_render` / `client_standing_position` / `scene_id_numeric_provenance` /
    `scene_seq_provenance` = nonclaims ทางการของเลน (ตาม scenario JSON + GEO-PF-006)
  - "แมพเดียวกัน" พิสูจน์ที่ระดับตาราง placement + จุดยืน V127/V128 — **เลข scene id เชิงตัวเลขยังเปิดอยู่ (GT-044)**

- **result:** (ผู้เทสกรอก: คำตอบ (ก)(ข)(ค)(ง) · หมายเลขกรณีจากตารางผล · ภาพ S0–S3 พร้อม sha256 · เวลา ·
  sha canonical ก่อน-หลัง · sha สำเนา run_gt034 ก่อน-หลัง · path ของ raw GAME log + console · BOOT_COMMIT ที่ใช้จริง + ผลสามข้อยืนยัน)

⚠️ **เลขชนกัน (ประวัติ — คงไว้):** จดหมายผู้เทส 12:00 (2026-08-20) เสนอ "GT-034 DAMAGE-TARGET-AB-001" — **คำสั่ง Panya ชนะเลขนี้** · ข้อเสนอผู้เทสได้เลขใหม่ = **GT-038**

## 🆕 GT-035 DAMAGE-ON-HOSTILE-001: ทำซ้ำ GT-027/028 บน hostile ตัวจริง  [🔴 **BLOCKED — GT-034 รันแล้ว 2026-08-22 แต่ได้ NO-RESULT (ไม่เห็นตัว) ⇒ ยังไม่มีผล native-red ให้ปลด**]

ตาม ORDER ลำดับ 2 · โครง: profile npc_sweep เปลี่ยน target identity เป็นตัวที่ Panya เลือกจาก roster (ต้องเปิด hypothesis slot ใหม่ — HYP-PF-024 ใช้ 3/3 แล้ว ตรวจงบก่อน build) · chief จะออกแบบเต็มเมื่อ GT-034 ได้ข้อสรุป

## 🆕 GT-036 KILL-HOSTILE-001: วงเต็ม "ตี → เลือด → ตาย" บน hostile ที่มี HP จริงจาก STANDARD_MOB  [🔴 **BLOCKED — รอ GT-034/035 (GT-034 ล่าสุด = NO-RESULT ไม่เห็นตัว · ยังไม่ปลด)**]

ตาม ORDER ลำดับ 3 · โครง: ทำซ้ำ GT-031 (HYP-PF-026) แต่ ladder ใช้ HP baseline ของตัวที่เลือก (เช่น Tornado Eagle lvl 27 = 3,857) · nonclaim เดิมทุกตัว + HP เป็น baseline ฝั่ง client

> ⚠️🔴 **คาเวียตรอบ 118 (static ล้วน — ไม่ได้บูตอะไร ไม่ได้แตะสถานะ/pass criteria ของใบนี้แม้แต่ตัวเดียว):
> เป้าเดียวที่เซิร์ฟเวอร์ของเรา spawn-แล้ว-ฆ่า ได้แบบ headless คือ `0x2001` ซึ่ง "ไม่ดรอปอะไรเลย"**
> - `0x2001` = placement index 0 = MOBS template `n_ID = 1` "Navy Transfer" · `n_RANK = 0` ·
>   `n_MOB_USAGE = 2` (NPC เมือง ไม่ใช่ mob) · `n_DROPS_EQUIPMENT` / `n_DROPS_NORMAL` / `n_DROPS_SPECIALLY`
>   = **0 ทั้งสามช่อง** · `n_DROPS_QUEST` low part **ไม่มีอยู่ในตาราง DROPS_QUEST ที่ ship มากับ client**
>   ⇒ ที่มา: `pf_bridge\FACTPACK_R100_CONSTDATA_MONSTER_LOOT.md` หัวข้อ 7
> - `n_RANK = 0` ซ้ำอีกชั้นหนึ่ง: ถ้ามี roller อยู่ในสายจริง มันจะตอบ named refusal
>   `loot_roll_refused_no_quality_row_for_rank_and_level` ทุกครั้งที่เดินไปถึงขั้น equipment drop
>   (E_DROPS_QUALITY จับ rank แบบ **เท่ากันเป๊ะ ไม่ใช่ bitmask**)
>   ⇒ `reports/PF_LOOT_ROLL001_SERVER_SIDE_ROLLER_20260820.md` (อยู่ใน repo โค้ด ไม่ใช่ bridge)
> - 🔴 **ผลที่ต้องจำให้ได้:** ถ้ารอบไหนในอนาคตต่อ loot roller เข้าสายจริงแล้วเอาเทสฆ่ามารันบน `0x2001`
>   **"ผลว่างเปล่า" คือคำตอบที่ถูกต้องของข้อมูล ไม่ใช่หลักฐานว่าลูทพัง** — ห้ามใครอ่านเป็น FAIL หรือ regression
> - hostile ตัวจริงทั้ง 13 ตัว **มี drop ref จริง** (เช่น `0x201f` Tornado Eagle = `2701001/5400001/2802234`)
>   ⇒ `pf_bridge\FACTPACK_R102_HOSTILE13_ROSTER.md` บรรทัด 18-32 · **แต่ยังไม่มีเลนเซิร์ฟเวอร์ใบไหนเล็งตัวใดตัวหนึ่งได้เลย**
>   และตัวใกล้สุดอยู่ ~11,914 หน่วย = คำถามระยะทางที่ GT-034 จอดรออยู่พอดี
>   ⇒ **คาเวียตนี้ไม่ปลดบล็อกอะไรทั้งสิ้น ใบนี้ยัง 🔴 BLOCKED เหมือนเดิม**
> - **สถานะลูทจริง ณ รอบ 118:** `src/pirateforce_foundation/loot_roll.py` เป็น **ไลบรารีที่ไม่มีใครเรียก** —
>   `production_allowed = False` และ `tools/verify_loot_roller.py` เฝ้าไว้ว่า **ห้ามมีโมดูลอื่นใน `src/` อ้างถึงมัน** ·
>   ไม่มี wire path และไม่มีตาราง DB สำหรับผลการตัดสินลูทเลยสักช่อง
>   ⇒ **GT-036 วันนี้คือ "ตี -> เลือด -> ตาย" ล้วน ๆ ไม่มีครึ่งลูทอยู่ในใบนี้แม้แต่บรรทัดเดียว**
>   (ครึ่งลูทอยู่ที่ GT-037 ✅ DONE และ GT-040 🟢 PENDING)
>
> **บันทึกเพิ่ม — มีผลเฉพาะรอบที่ลูทถูกต่อเข้าสายจริงแล้วเท่านั้น (pass criteria เดิมของใบนี้ไม่เปลี่ยน):**
> - **ชั้น wire/DB:** จด **identity ของเป้าที่ยิงจริง** (`0x2001` หรือเลขจาก roster) ลงในผลทุกครั้ง ·
>   ถ้ามี roller ในสาย ต้องเห็น **refusal ตามชื่อ** ในคอนโซล/ล็อก (`loot_roll_refused_drop_set_id_zero`
>   สำหรับสามช่องที่เป็น 0 · `loot_roll_refused_no_quality_row_for_rank_and_level` สำหรับ rank 0) —
>   🔴 **"เงียบ ไม่มีบรรทัดเลย" ไม่เท่ากับ "ปฏิเสธตามชื่อ" ต้องจดเป็นคนละผลกัน**
> - **ชั้น client-observable:** จดว่าบนจอ **ไม่มี** ของตกพื้น / หน้าต่างลูท / ข้อความใด ๆ หลัง NPC ตาย —
>   นี่คือ **ค่าที่คาดไว้ล่วงหน้า (คำทำนาย ไม่ใช่ข้อเท็จจริง)** สำหรับ `0x2001` และผลลบมีค่าเท่าผลบวก ·
>   ถ้า **เห็น** อะไรโผล่มาจริง = ข่าวใหญ่ จดทันทีพร้อมเวลาบนนาฬิกาในวิดีโอ
>
> **nonclaims ของคาเวียตนี้:** อ่าน artifact ที่ commit แล้วอย่างเดียว — ไม่ได้บูตเซิร์ฟเวอร์ ไม่ได้เปิด client
> ไม่ได้แตะ canonical DB · ตาราง drops ทั้งหมดเป็นข้อมูลที่ ship มากับ client **ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ
> ซึ่งกู้ไม่ได้ตลอดกาล** · ไม่ได้พิสูจน์ว่า hostile ตัวจริงจะดรอปอะไรออกมาบนจอ — พิสูจน์แค่ว่า
> **ตารางของมันไม่ว่าง ส่วนของ `0x2001` ว่าง** · ชื่อ refusal ทั้งสองตัวยืนยันแล้วกับ
> `src/pirateforce_foundation/loot_roll.py` (`REFUSAL_ID_ZERO` · `REFUSAL_NO_QUALITY_ROW`) ในรอบนี้

## 🆕 GT-037 LOOT-ROLL-001: server-side loot roller จาก client tables  [✅ **DONE — chief รอบ 113 (cloud) build เสร็จ · เขียว(cloud sanity) 992 pass · gate Actions ตัดสินแล้ว: โค้ดอยู่บน `main` ที่ `74b8add` พร้อมคำตัดสิน `conclusion=success` (ยืนยันรอบ 117) — ไม่มีอะไรค้างรอใครอีก**]

ตาม ORDER ลำดับ 4 = ดราฟต์ R100 §3 ประตู 2 · pure logic + unit tests ถึง Grade A ได้โดยไม่มี client · ไม่มีอะไรให้ผู้เทสทำในรายการนี้
✅ **รอบ 113 ส่งมอบ:** `src/pirateforce_foundation/loot_roll.py` + 66 เทส + verifier 30 guards + fixture + `reports/PF_LOOT_ROLL001_SERVER_SIDE_ROLLER_20260820.md` · DROPS_QUEST = named refusal โดยเจตนา (client มี 311/2478 ชุด) · **ยังไม่มีทางส่งผล roll ถึงผู้เล่น** (Door 3/4 ไม่มี wire path) · coverage `monster_spawn_and_loot` ยัง `not_started` — ถูกต้องตามกติกา (ไม่มี client เห็นสักไบต์)
🔎 **re-derive คำตัดสินได้ตลอด:** `git show origin/ci-status:ci/74b8add309cd2f7b5e7626393652c36582cb00dd.json`
ต้องเห็น `"conclusion": "success"` และ `"sha"` ตรงกับชื่อไฟล์ · ถ้าอยากได้ commit เขียวล่าสุดของ `main` ใช้
`py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch` (เครื่องมือรอบ 117)

## 🆕 GT-038 DAMAGE-TARGET-AB-001: A/B — การคลิกเลือกเป้าเกี่ยวอะไรกับเลขที่มองเห็นไหม  [✅ **PASS — 2026-08-22 23:24 (+07:00): target selection ไม่ใช่เงื่อนไขจำเป็นของเลข — ตรงคำทำนาย static R102**]

> ✅ **RESULT 2026-08-22 22:57–23:24 (+07:00) — PASS** (บูต main HEAD `cf81730` worktree สะอาด — tree เดียวกับ green `b665d92` ยืนยันย้อนหลังโดย resolver ของ GT-041 · รอบนี้ไม่ได้รัน resolver ก่อนบูต):
> - แขน A (ไม่เลือกเป้า · ไม่มี `TargetVital`/`ChooseNPC` ใน log): **เห็นเลขแดง `379`** ชัดเจน ≥2 sample
> - แขน B2 (เลือก `Navy Transfer` · `ChooseNPC 0x2001`): **เห็นเลขแดง `63`** (+1.265s เห็นซ้ำสองครั้ง) + **reaction `63`** (~+45.5s/+47.9s)
> - wire ครบ `HIT_WEAK → HIT_STRONG → MISS → HIT_REACTION` ทั้ง A/B1/B2 (label ละ 3 ครั้ง · 95 B ทุกใบ) · canonical ไม่ขยับ
> - 🔴 qualification ติดถาวร: เฟรม transient ที่ไม่ติดภาพ = **non-observed ไม่ใช่ absent** (เอฟเฟกต์สั้นกว่า cadence จับภาพ)
> - รอบก่อนหน้าคืนเดียวกัน (22:40–22:49) = NO-RESULT/BLOCKED-INPUT (เป้าอยู่นอกภาพ) — ไม่ใช่ผลลบ · ผลเต็มสองใบ:
>   `notes_to_chief/20260822_2328_GT038-PASS-TARGET-SELECTION-NOT-CAUSAL.md` + `20260822_2250_GT038-NO-RESULT-BLOCKED-INPUT.md` (บริโภค R123)
> - ✅ ตอบคำถามผู้เทสข้อ 3 (chief R123 ตรวจซอร์สแล้ว): `damage_model_hypothesis_npc_sweep_sent` เป็น `self.events` **ในหน่วยความจำโดยดีไซน์** (`runtime.py:1819` — พินโดย dispatch tests + headless replay) ไม่เคยถูก print ⇒ **เกณฑ์ attended ต้องอ้าง wire label 4 ใบจาก server console เท่านั้น** — ไม่มีบั๊ก ไม่ต้องแก้โค้ด

**ที่มา:** ข้อเสนอผู้เทสในจดหมาย 12:00 (เดิมเรียก GT-034 — เปลี่ยนเลขเพราะชนคำสั่ง Panya) · ปริศนา: สองเซสชันผู้เทสไม่เห็นเลข ทั้งที่ไบต์เหมือนเซสชันของ Panya ที่เห็นครบ · ความต่างที่วัดได้เดียวในล็อก = `TargetVital 0x1ADD` (มีเฉพาะเซสชันที่เห็นเลข)
**static R102 (`FACTPACK_R102_TARGETVITAL_AND_FXNUMBER_GATES_STATIC.md`) ตอบล่วงหน้า [PROVEN]:**
- สมมติฐาน (ก) "ต้องเลือกเป้าก่อนเลขถึงขึ้น" = **หักล้าง** — เลขขึ้นเพราะ performer==localplayer + resolve `0x2001` สำเร็จ · TargetVital เป็นแค่**พยาน**ว่า `0x2001` resolve ได้ (common cause) ไม่ใช่สาเหตุ
- สมมติฐาน (ข) "TargetVital ใบหลังเป็นผลของเฟรม HIT_REACTION" = **หักล้าง** — subtree ของ CHitResult ไม่มีทางเรียก send TargetVital
- เกตที่อธิบายจอมืดได้จริง: ① resolve `0x2001` ล้มเหลว ณ เวลาเฟรม (timing การลงทะเบียน) ② **toggle `[localplayer+0x420]` = 0** (ดูบทเรียนเครื่องมือ ⬇)
**โปรโตคอล (บูตเดียว · scenario `damage_model_hypothesis_npc_sweep.json` เดิม):** แขน A = ไม่แตะเมาส์เลยหลังเข้าแมพ ยิง trigger · แขน B = คลิกเลือก NPC (`Navy Transfer`) ก่อน แล้วยิง trigger รอบใหม่ (relaunch client รีอาร์ม one-shot ระหว่างแขน)
**ข้อบังคับทั้งสองแขน:** กล้องเห็นผู้เล่น+NPC เต็มตัว · **ห้ามพิมพ์อะไรนอกช่องแชตที่โฟกัสแล้ว** (กัน hotkey 0x27) · ใช้ client ที่เพิ่งเปิดใหม่ (toggle default ON)
**คำทำนาย static:** ทั้งสองแขน**ควรเห็นเลขเท่ากัน** — ถ้าแขน A มืดแต่ B เห็น = static ผิด จดละเอียด · ถ้ามืดทั้งคู่บน client ใหม่ = ปัญหาคือ resolve-timing ไม่ใช่ toggle
**pass criteria สองชั้น:** ① wire: เฟรมครบทั้งสองแขน ② client: บันทึกเลขเห็น/ไม่เห็น ต่อแขน + มี/ไม่มี `TargetVital` ในล็อกต่อแขน
## 🆕🎯 GT-039 NPC-HP-LINK-001: **หลอดเลือดของ "เป้าหมาย" ลดจริงไหม**  [✅✅ **PASS — รอบใหญ่ #11 (UNATTENDED) 2026-08-21 02:05–02:25 · HEAD `cc46a03`**]

> ### 🏆 **ครั้งแรกในประวัติโปรเจกต์ที่ HP ของ "เป้าหมาย" ขยับ**
> **แถบเลือดของ NPC ลด `100 → 37 → 0` ตรงตามค่าที่เซิร์ฟเวอร์ส่ง และ NPC ล้มจริง**
> · 8 เฟรมครบเรียงถูกทุกใบ · **`grep -c 28317` = 0** ⇒ **การสลับสองสายพานในเซสชันเดียวไม่พัง**
> (นี่คือความเสี่ยงเฉพาะที่คิวใบนี้เตือนไว้เอง — ตอบแล้วว่าไม่เกิด)
> · `MISS` ไม่ทำให้ HP ขยับ — ค้าง 37 สังเกตได้ 4 ภาพติด (ตัวควบคุมทำงาน)
> · teardown สะอาด · canonical sha ไม่ขยับ · ผลเต็ม: `notes_to_chief\20260821_0225_GT039-RESULTS-and-teardown-template-bug.md`
>
> ⭐ **คำตอบของคำถามที่ค้างมาตั้งแต่รอบ 83:** client ไม่ลบเลขเอง — **แต่มันเชื่อสิ่งที่เซิร์ฟเวอร์บอก**
> ⇒ วง "ตี → เลือด → ตาย" ปิดครบบนเป้าหมายจริงแล้ว
> 🔴 **nonclaim ที่ยังต้องติดทุกครั้ง: เลขคณิต บันได และการเชื่อม เป็นดีไซน์ของเรา**
> **ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · ยังไม่ใช่ combat จริง (NPC ไม่โจมตีกลับ) · HP ไม่ persist
> 🟡 ข้อที่ยังไม่ปิด: ไม่มีวิดีโอ/พยานตาเปล่ารอบนี้ (unattended ตามที่ประกาศไว้ตอนถือธง)

<details><summary>ข้อความตอน PENDING (เก็บไว้ทั้งก้อน — เป็นคำทำนายที่ตรวจสอบย้อนได้)</summary>

[🟢 เดิมเป็น PENDING — พร้อมรันหลัง commit ของ chief รอบ 111 (จ็อบ 178 · HYP-PF-029) — อ่าน SHA จาก `outbox\178_round111_*`**]

#### (ฉบับ PENDING ที่ chief cloud รอบ 114/117 ปรับท่าบูต — เก็บไว้ทั้งก้อน)

🗄 (หัวข้อเดิมตอน PENDING — เก็บไว้เป็นคำทำนายที่ตรวจย้อนได้) 🆕⭐ GT-039 NPC-HP-LINK-001: **หลอดเลือดของ "เป้าหมาย" ลดจริงไหม** — ชิ้นกลางที่วิดีโอรอบใหญ่ #10 พิสูจน์ว่าหายไป  [🟢 **PENDING (HYP-PF-029) — บูตที่ commit ที่ `pf_resolve_green_boot.py` ชี้ให้ (ดูบล็อก 🔎 ใต้หัวข้อ)** · โมดูล + scenario + dispatcher + CLI flag เข้า main ตั้งแต่ `cc46a03` (CI success run 32406182274) · แก้ pointer chief รอบ 114 (เดิมชี้ `outbox\178_round111_*` ซึ่ง gitignored หา SHA ไม่ได้) · แก้ท่าบูต chief รอบ 117 (ประโยคเดิม "HEAD ล่าสุดที่ ci-status = success" **รันไม่ได้แล้ว** — เหตุผลอยู่ในบล็อกใต้หัวข้อ) · เนื้อการทดสอบและ pass criteria ไม่เปลี่ยนแม้แต่ตัวเดียว]

> 🔎 **หา SHA ที่จะบูต — ใช้เครื่องมือรอบ 117 อย่า hard-pin และอย่าอ่านที่ HEAD:**
> `py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch`
> (รันจากโฟลเดอร์ `pf_bridge` · แทน `C:\path\to\pirate-force-server` ด้วยพาธ clone จริงบนสะพาน · คำสั่งเป็น ASCII ล้วน ปลอดภัยกับคอนโซล cp874)
> - **exit 0** + บรรทัด `BOOT_COMMIT: <sha>` ⇒ บูต sha นั้น: `git checkout <sha>` (detached HEAD ถูกแล้ว — เราบูต *คำตัดสิน* ไม่ใช่ branch)
> - **exit 3** + `BOOT_COMMIT: NONE` ⇒ **ห้ามบูต** · จดในผลว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
> - 🔴 มีบรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ **จดลงในผลด้วย** (มี commit แดงบนสาย main เหนือคำตอบ)
> - ⚠️ `success` ที่เครื่องมือส่งต่อ = **subset ของ gate บน GitHub runner** ไม่ใช่ "ผ่าน gate เต็ม" (gate จริงอยู่บนสะพาน)
> 🔴 **ทำไมประโยคเดิม ("บูต `origin/main` HEAD ล่าสุดที่ ci-status = success") รันไม่ได้แล้ว:** HEAD ของ `main` หลัง automerge เป็น
> **merge commit** ที่ push ด้วย `GITHUB_TOKEN` ⇒ **ไม่ trigger workflow ⇒ ไม่มีใครเขียน `ci/<sha>.json` ให้มันเลย ตลอดไป**
> (วัดรอบ 116 จาก Actions API · ยืนยันซ้ำรอบ 117 ที่ HEAD `520e2cf`) — นี่ไม่ใช่ "คำตัดสินยังไม่มา" แต่คือ "จะไม่มีใครเขียนให้"
> ⇒ คนที่ทำตามประโยคเดิมจะไม่เจอไฟล์คำตัดสิน แล้ว **ปฏิเสธการบูตอย่างถูกกฎ** ทั้งที่โค้ดเขียวนั่งอยู่ต่ำลงไปแค่คอมมิตเดียว
> ⇒ เครื่องมือจึง **เดินไล่ ancestor** ให้ แทนการ lookup ที่ HEAD (ค่าปริยาย: `origin/main` · `origin/ci-status` · ย้อน 60 commit)
> **ยืนยันด้วยมือ (ทำได้ ไม่บังคับ · แทน `<SHA>` ด้วยเลขที่เครื่องมือให้):**
> `git show origin/ci-status:ci/<SHA>.json` ต้องเห็น `"sha"` ตรงชื่อไฟล์ **และ** `"conclusion": "success"` (สี่กฎการอ่าน ci-status)
> `git grep -n "npc-hp-link-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py` ต้องเจอบรรทัดจริง
> 🔴 **ห้ามใช้ `--help` เป็นหลักฐานว่ามี flag** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6)
> ถ้า sha ที่เครื่องมือชี้ **ไม่มี** โมดูล `npc_hp_link_hypothesis.py` (มีตั้งแต่ `cc46a03`) ⇒ **หยุดและรายงาน** อย่าไล่ลง commit เองด้วยมือ

</details>

**ที่มา (นี่คือเทสที่เกิดจากผลของพวกท่านโดยตรง):** รอบใหญ่ #10 ที่ Panya ขับเอง ยิงใส่ `Navy Transfer` `0x2001` โดย**คลิกเลือกเป้าก่อน** ⇒ แถบ HP ของเป้าอยู่บนจอตลอดทั้งรอบ · ดาเมจสะสม **63 + 379 + 63 = 505** · **แถบไม่ขยับแม้แต่หน่วยเดียว** (100 Lv.1 เต็มหลอด ทั้งก่อนและหลัง) ⇒ ตอกย้ำรอบ 83: **client ไม่ลบเลขเอง เป็นตัวแสดงผลล้วน ๆ**
⇒ เลนใหม่นี้คือคำตอบตรง ๆ ของผลนั้น: **เซิร์ฟเวอร์พูดทั้งสองครึ่งเอง** — ทำเลขคณิต HP ของ *เป้าหมาย* เอง (100 − 63 = 37 → clamp 0) แล้วสลับสองสายพานส่งออก 8 เฟรม
🆕 **ของใหม่ที่ไม่เคยมีในโปรเจกต์:** GT-031 (HYP-PF-026) เดินบันได HP ของ **ผู้เล่นเอง** บนสายพาน VitalData เท่านั้น — **ไม่เคยมีเลนไหนขยับ HP ของเป้าหมาย** เลนนี้เป็นเลนแรก และเป็น**เลนแรกที่สลับสองสายพานในเซสชันเดียว** (VitalData `+0x18` สำหรับเฟรมเลข · actor-entry `+0x1C` actor_type 4 สำหรับเฟรมหลอด)
⭐ **nonclaim ที่ต้องติดทุกผล: เลขคณิต บันได และการเชื่อม เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · ไม่มี capture ใบไหนในคลังแสดงว่า HP ของเป้าขยับตามดาเมจ ไม่ว่าทางใด

**boot (ท่าเดียวกับ GT-027/031 เป๊ะ เปลี่ยนแค่ flag):**
- `--npc-hp-link-hypothesis-scenario scenarios\npc_hp_link_hypothesis_target_sweep.json` (+ `--db` สำเนาตามปกติ)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → sweep **8 เฟรม ห่างกัน 6 วิ/เฟรม (42 วิทั้งชุด)**
- 🔴 **6 วิเป็นความตั้งใจ ไม่ใช่ความพลาด** — ตามคำสั่ง Panya 2026-08-20: *เลิกยืดระยะเฟรมเพื่อผู้เทส* เพราะตัวเหตุการณ์เองสั้น ไม่ใช่เฟรมถี่เกินไป · **ทางแก้ที่ถูกคือถ่ายวิดีโอ** (พิสูจน์แล้วสองรอบว่าได้ทั้งภาพคมและนาฬิกาที่ไม่ใช่ของผู้เทสเอง)
- console label = `HYP_PF_029_NPC_HP_LINK_<STEP>` · event = `npc_hp_link_hypothesis_target_sweep_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
- **one-shot** — ยิงซ้ำได้ `..._already_sent_no_reply` (relaunch client เพื่อรีอาร์ม)

**🔴 ข้อบังคับก่อนยิง — ข้อนี้คือสิ่งที่ทำให้รอบใหญ่ #10 มีค่า อย่าข้าม:**
① **คลิกเลือก NPC `Navy Transfer` ก่อนเสมอ** เพื่อให้**แถบ HP ของเป้าโผล่บนจอ** (ยืนยันใน client log ว่ามี `TargetVital 0x2001 'Navy Transfer'`) — ไม่เลือก = ไม่มีแถบให้ดู = เทสทั้งใบเสียเปล่า
② **ถ่ายวิดีโอทั้ง 42 วินาทีต่อเนื่อง** ตั้งแต่ก่อนกด trigger — ไม่ใช่ภาพนิ่งรายเฟรม
③ กล้องเห็นทั้งตัวผู้เล่น · NPC · **แถบ HP ของเป้า** · และแถบ HP ผู้เล่น ในเฟรมเดียว
④ client ที่เพิ่งเปิดใหม่ · ห้ามพิมพ์อะไรนอกช่องแชตที่ยืนยันโฟกัสแล้ว (กัน hotkey 0x27)

**สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
| t | เฟรม | สายพาน | ถ่าย/ดูอะไร |
|---|---|---|---|
| +0s | `TARGET_SPAWN` hp 100/100 | actor-entry | NPC อยู่ครบ แถบเป้า 100 (ถ้ากระพริบ/รีสปอว์นให้จด) |
| +6s | `HIT_WEAK` เลข **63** flags 0x0001 | VitalData | เลขลอยบน NPC · **แถบเป้าต้องยังไม่ขยับ** — ถ้าขยับที่เฟรมนี้ = หักล้างรอบ 83 ทั้งเลน จดละเอียดสุด |
| +12s | `TARGET_HP_AFTER_WEAK` hp **37**/100 | actor-entry | ⭐⭐ **แถบของเป้าลดเหลือ 37 ไหม — นี่คือคำถามเดียวของเทสทั้งใบ** |
| +18s | `MISS` flags 0x0000 | VitalData | marker `MISS!` ขึ้น (texture `bm_miss.tga`) · แถบค้าง 37 |
| +24s | `TARGET_HP_AFTER_MISS` hp 37 ซ้ำ (**ไบต์เหมือนเฟรม +12 เป๊ะ**) | actor-entry | แถบค้าง 37 · client กระพริบ/รีเฟรชไหมเมื่อได้ค่าที่ถืออยู่แล้ว (มีค่าทั้งสองทาง) |
| +30s | `HIT_STRONG` เลข **379** flags 0x0001 | VitalData | เลขลอย · แถบยังไม่ขยับ |
| +36s | `TARGET_HP_ZERO_DYING` hp 0 + death timer 20.0 **ในเฟรมเดียว** | actor-entry | แถบเป้า 0/100 + **วงนับถอยหลังเหนือ NPC** (เหมือน GT-021/029) — clamp: 37−379 = floor 0 |
| +42s | `TARGET_DYING_ELAPSED` timer 0.0 | actor-entry | เลขในวงหายไป NPC ยังนอน ไม่มีอะไรเกิดต่อ (พฤติกรรมเดิมของ GT-029 — **ไม่ใช่บั๊ก**) |

**pass criteria สองชั้น:**
① **wire** = 8 เฟรมครบตาม label + delay ใน console + event `npc_hp_link_hypothesis_target_sweep_sent` ใบเดียว
② **client-observable** = ตอบสามข้อ: **(ก) แถบของเป้าลดเป็น 37 ที่ +12 หรือไม่** · (ข) แถบขยับตอนเฟรมเลข (+6/+30) หรือไม่ · (ค) วงนับถอยหลังเปิดที่ +36 เหมือนตอน GT-029 ที่รันแยกไหม
🔴 **ผลลบมีค่าเท่าผลบวก** — "เลขขึ้นครบแต่แถบไม่ลดเลยแม้เซิร์ฟเวอร์ส่ง ActorAttr hp 37" = คำตอบที่ชี้ขาดพอ ๆ กัน และแปลว่าปัญหาไม่ได้อยู่ที่ "ใครทำเลขคณิต" แต่อยู่ที่ทางเข้า reconcile ของ actor ที่รู้จักแล้ว **จดเป็นผล ไม่ใช่ fail**

**⛔ เกณฑ์หยุด / ตื่นเต้นพิเศษ:**
- แถบลด **ก่อน** เฟรม hp (คือลดตอนเฟรมเลข +6/+30) = **หักล้าง "client ไม่ลบเอง" ของรอบ 83** — ผลลบที่มีค่าที่สุดที่เป็นไปได้ · วิดีโอช่วง +6..+12 คือหลักฐานชิ้นเอก
- 🔴 **`ErrorData=28317` ในล็อก = การสลับสองสายพานในเซสชันเดียวพัง** — เลนนี้เป็นเลนแรกที่ทำ ⇒ นี่คือความเสี่ยงเฉพาะตัวของเทสใบนี้ **หยุด จด แล้วเก็บ console log ทั้งไฟล์** (headless พิสูจน์แล้วว่าประกอบไบต์ได้ถูก แต่ **ไม่มี client ตัวไหนเคยเห็นไบต์ชุดนี้แม้เฟรมเดียว**)
- NPC หายไปทั้งตัวแทนที่จะแค่ HP ลด = จด แล้วดูว่าเป็นที่เฟรมไหน

**หลังจบ:** ถ่ายภาพปิดท้าย → ปิด client ตาม PLAYBOOK → **teardown เสมอ แม้รอบจะจบเพราะเลิกเล่น** (บทเรียนรอบใหญ่ #10: ไม่ teardown = ชั้น wire หายถาวร) · ถ้าเลยเวลาไปแล้ว ใช้ `-Salvage` ของ template teardown (ดู `HOWTO_SALVAGE_A_DEAD_ROUND.md` — ของใหม่รอบ 111)

**nonclaims บังคับ:**
- สูตร/บันได/การเชื่อม **เป็นของเรา** ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
- **ไม่ claim ว่า HP ของ NPC persist** — ไม่มีคอลัมน์ HP ให้เขียน balance ตายพร้อม sweep
- ไม่ใช่ combat จริง — **ไม่มี NPC โจมตีกลับ** (แถว mob_aggro ยัง not_started) · ผู้เล่นไม่ได้เป็นคนสั่งตี เซิร์ฟเวอร์เป็นคนเล่าเรื่อง
- ไม่ claim path คืนชีพ/ลูท/XP
- **ผลของรอบใหญ่ #10 ที่เป็นที่มาของเลนนี้ = ชั้น client-observable เท่านั้น** (ไม่มี teardown ⇒ ไม่มีหลักฐานชั้น wire เลย) — บันทึกเต็มพร้อม sha256 ของภาพทั้งห้าใบอยู่ที่ `reports\PF_NPC_HP_LINK029_GT027_RERUN_ATTENDED_RESULT_20260820.md` (ของใหม่รอบ 111)

## 🆕🔬 GT-040 DROPTHING-TRANSPORT-PROBE-001 [STATIC-ON-BRIDGE]: "วัตถุลูทบนพื้น" มี transport อยู่ในอิมเมจจริงไหม — สามจุดที่ยังไม่มีใครเปิดสักครั้ง  [✅ **DONE — ผู้ช่วยของ Panya ปิดครบสามท่อน A/B/C (2026-08-21 09:36-09:56 +07:00) · ผลเต็ม: `notes_to_chief/20260821_09{36,51,56}_GT040-PART-{A,B,C}-RESULTS-from-assistant.md` · บริโภค+ตรวจสอบเอกสารโดย chief R120 · ✅ GT-042 ปิดแล้ว (PASS 2026-08-23 พร้อม erratum ขอบเขต handler: len 47 ไม่ใช่ 712) ⇒ ข้อห้ามเขียนโมดูล/encoder **ปลดเฉพาะแถวที่รอด re-derive/ขอบเขตที่แก้แล้ว** — ดู GT-042**]

**หมวด:** `STATIC-ON-BRIDGE` — งานที่ **ต้องเปิด `GameClient.local.bin`** จึงทำบน cloud clone ไม่ได้เลย
ผู้รับงานคือคนที่นั่งอยู่หน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** (ดู "ชั้น ②" ด้านล่าง)

**ที่มา:** รอบ 113 ส่ง **ประตู 2** ของดีไซน์ลูทรอบ 100 เสร็จ (`src/pirateforce_foundation/loot_roll.py`
= loot roller ฝั่ง server, Grade A บน pure logic — GT-037 ✅ DONE) · รอบ 115 สำรวจ **ประตู 3 "ของลูทโผล่บนพื้น"**
แล้วพบว่า **ทำบน cloud ไม่ได้เลยสักข้อ** — ทุกคำถามที่เหลือต้องอ่านไบต์จากอิมเมจ
⇒ ใบนี้คือใบสั่งที่ปลดล็อกประตู 3/4 · 🔴 **การเขียนโมดูลก่อนได้คำตอบ = การประดิษฐ์ wire format ขึ้นเอง ซึ่งบ้านนี้ห้าม**
⇒ **ใบนี้ขอ "ข้อเท็จจริง" เท่านั้น ไม่ขอดีไซน์ ไม่ขอโมดูล ไม่ขอ encoder**

### objective (claim เดียวที่ใบนี้พิสูจน์)
**อิมเมจของ client มีทางส่ง/ทางเก็บ "วัตถุบนพื้น" (ground thing) อยู่จริงหรือไม่** —
ตอบด้วยการเปิดสามจุดที่ยัง `[UNKNOWN]` แล้วบอกว่าแต่ละจุด **มี** หรือ **ไม่มี**
🔴 **ผลลบคือคำตอบเต็มใบ ไม่ใช่ความล้มเหลว** (ดูบล็อกผลลบท้ายใบ)

### 🔒 ข้อเท็จจริงที่ "ปิดแล้ว" — ห้ามเอาใบนี้ไปรื้อซ้ำ
- **[NEGATIVE, ปิดสนิท] ท่อ actor-entry ส่งของบนพื้นไม่ได้** — jump table `0x4469BD` รับ `actor_type`
  **เป๊ะ ๆ แค่ 2..6** (`add eax,-2; cmp eax,4; ja -> return NULL`, entry ที่ไม่เข้าเงื่อนไข **ถูกทิ้งเงียบ**)
  2=`CNetActor` · 3=`CMyActor` · 4=`CNetNPC` · 5=`CAvatarNPC` · 6=`Pet` — **ไม่มีเคสของ item/object เลย**
  ที่มา: `pf_bridge\FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md` — **grep คำว่า `0x4469BD` แทนการนับบรรทัด**
  (เลขบรรทัดขยับแล้วเพราะ ERRATUM ของรอบ 115) ⇒ **ห้ามเสียเวลาไล่หา actor_type ตัวที่ 7** มันไม่มี
- **[NEGATIVE, re-derive แล้วรอบ 115] ไม่มีชื่อ DropThing/Pickup ในทะเบียนชื่อของเราเลย** —
  0 hit ใน `pf_bridge\VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` และ 0 hit ใน
  `pirate-force-server\docs\PF_VITAL_NAMES.json` ⇒ **อย่าไปค้นสองไฟล์นั้นซ้ำ** ต้องอ่านอิมเมจอย่างเดียว

### 📌 ข้อแก้ที่ต้องอ่านก่อนหยิบ citation เก่า (✅ **merge แล้ว** — ฝั่ง repo โค้ดเข้า `main` ที่ `24d5b94` ซึ่งมีคำตัดสิน `conclusion=success` · ยืนยันรอบ 117)
`DropThingBoard` และ `DropThingGameObj` **ไม่ได้อยู่ใน 521-class registration join** — ทั้งคู่ `literal_kind=none`
และ `in_round86_census=False` (`pf_bridge\FACTPACK_L2_CLASSCENSUS001_20260820.tsv:482,483`)
ส่วน 521 join นิยามไว้ว่า "มี **ทั้ง** RTTI type descriptor **และ** runtime name literal ใน `.rdata`"
(`FACTPACK_L2_CLASSCENSUS001_20260820.md:34`) ⇒ สองตัวนั้นเป็น **RTTI descriptor ล้วน ๆ** เข้าไม่ได้
มีแค่สองตัวนี้ที่ถือ runtime literal จริง:

| คลาส | บรรทัดใน tsv | literal VA | ใช้เป็นหลักฐานอะไรได้ |
|---|---|---|---|
| `DropThingModule_Client` | `:484` | `0x00F0BAD0` | มี literal (ยังไม่พิสูจน์ว่าถูก register) |
| `PickupTerrainThing` | `:1003` | `0x00F3093C` | มี literal **และ** registration พิสูจน์แล้ว (ท่อน C) |

ข้อความ erratum เต็มอยู่ใน `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md` (ERRATUM E1, รอบ 115)
🔴 **ใบนี้ไม่ได้พึ่ง erratum ในการทำงาน** — ทั้งสามท่อนอ่านจากอิมเมจตรง ๆ · erratum แค่กันไม่ให้ใครหยิบ
citation ผิดไปอ้างว่า "DropThingBoard/GameObj ถูก register แล้ว" · ⏳ ถ้ายังหา erratum ไม่เจอบน `main` = PR ยังไม่ merge ทำงานต่อได้ตามปกติ

### สิ่งที่ต้องมี (precondition)
- **อิมเมจ:** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  (ค่าอ้างอิงจาก `pf_bridge\factpack_L1\MANIFEST.md:21-22`) — 🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ไม่ต้องมี:** เซิร์ฟเวอร์ · client ที่บูตแล้ว · canonical DB · สำเนา DB · `LOCK_GAME` · teardown · boot stamp
  ⇒ ใบนี้ **ไม่ใช่รอบเทสในเกม** กติกา stamp 420 นาที (เดิม 180)/teardown ไม่เกี่ยวกับใบนี้เลย
- **capture corpus:** ไม่บังคับ · หยิบมาได้ถ้าอยากเช็คว่าเคยมีเฟรมรูปร่างนี้ผ่านสายจริงไหม (คาดว่า 0 — ถ้าเจอ **นั่นคือข่าวใหญ่ จดทันที**)
- **ท่าทำงาน:** ตามวินัยของ `pf-static-re` (`pf_bridge\.claude\agents\pf-static-re.md`) และเมธอดของ
  RUNTIMERES-ACTOR-ENTRY-001: 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative** (มันหยุดที่ไบต์แรกที่ decode ไม่ได้
  แล้วรายงาน negative อย่างมั่นใจ = ความผิดพลาดรอบ 83 เป๊ะ ๆ) · ให้ census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต ·
  dword sweep ทั้งไฟล์สำหรับ table/vtable/immediate) · **สวีปทั้งสอง executable section: `.text` (`0x401000`) และ `.code` (`0xC3A000`)**
- **บันทึกต้นทุน:** สามแถวของ Door 3/4 ลงใน `pf_bridge\IMAGE_ACCESS_COST.tsv` แล้วโดยรอบ 115

### steps — สามท่อน **แยกจ็อบ แยกผล อย่ารวม** (ทำตามลำดับความสำคัญ A → B → C)

**ท่อน A (สำคัญสุด) — สอง derived bit ของ `0x6E9D` ที่ยังไม่มีใครเปิด**
พาหะ: `GSCN_RunTimeProtocolRes` · literal `0xF2FFF8` · id `0x6E9D` (=28317) · vtable `0xF2FFC0` · sizeof `0x28` ·
Serialize `0x5E3EE0` (เรียก base `0x5F4070` ก่อน) · inbound handler `0x5E4060` → `0x446F30`
bit `0x02`/obj `+0x1C` = actor-entry collection = **decode แล้ว ไม่ต้องแตะ**

| derived bit | object | sub-serializer | สถานะวันนี้ |
|---|---|---|---|
| `0x04` | `+0x24` | `0x5E2960` | **ยังไม่ decode** · ฝั่ง inbound รู้แค่ว่า `[+0x10]` → `[0x1093198]+0x7BC` · `[+0x14]` → `0x5F6B70` · `[+0x18]` → `[actor+0x574]` |
| `0x08` | `+0x20` | `0x5F85B0` | **ยังไม่ decode เลยแม้แต่บรรทัดเดียว** |

(ที่มาของตาราง: `pirate-force-server\reports\PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md:54-55`
และรายการ "explicitly not examined" ที่ `:343`)

1. decode `0x5E2960` และ `0x5F85B0` ให้ได้ **ตารางฟิลด์** (tag ไบต์ · offset ในอ็อบเจกต์ · ชนิด) —
   **รูปแบบคำตอบที่นับว่าเป็นคำตอบ = ตารางหน้าตาเดียวกับ disassembly ของ `StallOperateVital` ที่**
   `pirate-force-server\reports\PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md:160-166`
2. แนบ span `[start,end)` + sha256 ของ span ทุกอันที่อ้าง (cross-check กับ `factpack_L1\blocks_256.tsv` ได้)
3. ตอบคำถามเดียวของท่อนนี้: **สอง sub-object นี้ พา "อ็อบเจกต์ที่ไม่ใช่ actor" มาด้วยไหม**
   (เช่นอ้าง literal VA `0x00F3093C` / `0x00F0BAD0`, สร้างอ็อบเจกต์ผ่าน vtable ที่ไม่ใช่ actor 2..6, หรือแตะ terrain/ground container)

**ท่อน B — reconcile/removal pass `0x446FE1..0x4470E5`** (ลูปที่สองของ `0x446F30`)
เหตุผลที่ต้องเปิด: มันคุม **การถอด/อายุของอ็อบเจกต์** และวันนี้มี **[TENSION, UNRESOLVED]** ค้างอยู่ระหว่าง
"V91 = actor-entry list เป็น authoritative membership ต่อ generation" (ละตัวไหน ตัวนั้นหายจากจอ+เรดาร์)
กับ **เฟรม count-1 ที่เลน HYP-PF-023/025 ส่งอยู่ทุกวันนี้** (ถ้า membership authoritative จริง เฟรม count-1 ควรกวาดประชากรที่เหลือหายหมด — ไม่มีใครรายงานว่าเกิด)
ที่มา: `FACTPACK_R100_INREPO_LOOT_SPAWN_GAPLIST.md` §4.2 (**grep `0x446FE1`** แทนการนับบรรทัด)

4. decode ลูปนั้นและตอบว่า: มัน diff กับ **สำเนา collection ของเฟรมก่อนหน้า** (singleton `[0x01081A90]+0x154` ตามที่ CHUNK2-Q2 อ้าง)
   หรือ diff กับ actor registry · ต่อ entry ที่ถูกละ มันเรียกอะไร · และ **เฟรม count-1 กวาดประชากรที่เหลือหรือไม่**
5. 🔴 **ของบนพื้นที่โผล่แล้วไม่มีวันหาย ไม่ใช่ฟีเจอร์** — ถ้าท่อน A ได้ผลบวก ท่อนนี้คือสิ่งที่ตัดสินว่าลูทมี "อายุ" ได้ไหม

**ท่อน C — serializer ของ `PickupTerrainThing` (ประตู 4 ฝั่ง request)**
วันนี้มีอยู่แค่ **ชื่อกับที่อยู่**: name VA `0xF3093C` · registration `0xBEE5E5` (ท่า `push <name>` → `call 0x89C080`)
ที่มา: `PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md:158` · derived id `0x4543`
**[DERIVED, เลขคณิตล้วน]** จากแฮชชื่อ `sum((i+1)*ord(c)) & 0xFFFF` — **id ที่ derive มาไม่ใช่หลักฐาน**
รายงานใบเดียวกันพิมพ์ serializer เต็มของ `StallOperateVital` ไว้ที่ `:160-166` แต่ **ไม่มีของ `PickupTerrainThing` แม้บรรทัดเดียว**

6. จาก registration `0xBEE5E5` ไล่ไปหา **vtable** ของคลาสนี้ แล้วอ่าน **slot `+0x18` = serializer**
   (ท่าเดียวกับที่ `StallOperateVital` ทำ: vtable `0xF4A418` → `+0x18` = `0x76A630`)
7. พิมพ์ตารางฟิลด์ + span + sha แบบเดียวกับท่อน A ข้อ 1-2

### pass criteria — **สองชั้น แยกกันเด็ดขาด**

**ชั้น ① wire/DB (ไบต์+ดิสแอสเซมบลี — headless ล้วน ไม่ต้องมีคนเฝ้าจอ)**
ใบนี้ผ่านเมื่อ **ทุกท่อนได้คำตอบชี้ขาด ไม่ว่าบวกหรือลบ** โดยแต่ละคำตอบต้องมี VA + span + sha:
- **ท่อน A ผลบวก** = ชี้ได้ว่า bit `0x04`/`+0x24` หรือ bit `0x08`/`+0x20` สร้าง/อัปเดต **อ็อบเจกต์ที่ไม่ใช่ actor ในตาราง 2..6**
  พร้อมตารางฟิลด์ของ `0x5E2960` และ/หรือ `0x5F85B0`
  **ท่อน A ผลลบ** = ทั้งสองบิต decode ออกมาแล้วเป็นข้อมูล scene/zone/กล้อง/สภาพแวดล้อม **ไม่มีการสร้างอ็อบเจกต์** และ
  **ไม่มีการอ้าง `0x00F3093C` หรือ `0x00F0BAD0` เลย** ⇒ ประตู 3 ปิดผ่านท่อนี้ด้วย **อีกหนึ่ง [NEGATIVE] ที่ระบุตัวได้**
- **ท่อน B ผลบวก** = ระบุได้ว่า `0x446FE1..0x4470E5` diff กับอะไร และ **ปิด TENSION** ได้ว่าเฟรม count-1 กวาดหรือไม่กวาด
  **ท่อน B ผลลบ** = static ตัดสินไม่ได้ (เช่นจบที่ vtable dispatch ที่ resolve ชนิดไม่ได้) ⇒ **พูดออกมาตรง ๆ** ว่า
  ทางเดียวที่เหลือคือ membership-omission GT ที่มีขอบเขต บน identity เดียวที่รู้จัก — **นั่นจะเป็นใบใหม่ ไม่ใช่ใบนี้**
- **ท่อน C ผลบวก** = ได้ **serializer VA จริง** + ตารางฟิลด์ + span sha ของ `PickupTerrainThing`
  **ท่อน C ผลลบ** = slot `+0x18` เป็น stub/ตกไปที่ base หรือหา vtable ไม่เจอ ⇒ ประตู 4 **ยังไม่มีรูปร่าง request ให้สร้าง** คงสถานะ `[NO PATH KNOWN]`
- ทุกท่อน: **sha256 ของอิมเมจก่อน-หลัง ต้องตรงกัน** · ถ้าเขียนสคริปต์ ให้ commit ลง `tools/` แบบรันซ้ำได้พร้อมจำนวน guard
  (ท่ามาตรฐานของบ้านนี้: verifier + guard count + exit 0)

**ชั้น ② client-observable (ต้องมีคนอยู่หน้าจอเกม)**
🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้แม้แต่ชิ้นเดียว และห้ามใครอ้างชั้น ① เป็นหลักฐานของชั้น ②**
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย ไม่มีจอให้ดู · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**
**สิ่งที่ผลบวกจะไปปลดล็อก (ยังไม่ใช่ตอนนี้):** เมื่อท่อน A หรือ C คืน "รูปร่างไบต์" มาได้จริง
ถึงจะมีสิทธิ์เขียนใบ GT ตัวถัดไปที่เป็น **attended** และถามคำถามชั้น ② ว่า *"มีอะไรโผล่ขึ้นบนพื้นให้ตาเห็นไหม"*
🔴 **ก่อนถึงตอนนั้น ห้ามเขียนโมดูล/encoder/scenario ใด ๆ** — ไม่มีรูปร่างไบต์ = การเขียนคือการแต่ง wire format ขึ้นมาเอง

### 🔴 ผลลบมีค่าเท่าผลบวก — เขียนไว้ล่วงหน้าว่าจะทำอะไรต่อ
ถ้า **ทั้งสามท่อนเป็นลบ** (สอง derived bit ไม่พาอ็อบเจกต์อะไรมา · removal pass ตัดสินด้วย static ไม่ได้ ·
`PickupTerrainThing` ไม่มี serializer ของตัวเอง) ⇒ **นั่นคือผลที่สมบูรณ์ ไม่ใช่ FAIL** และโครงการเดินต่อแบบนี้:
1. **ประตู 3 ปิดต่อไป** และคราวนี้ปิดพร้อมเหตุผลที่ระบุตัวได้ ไม่ใช่ปิดเพราะ "ยังไม่มีใครดู"
2. **loot roller คงเป็นเลน pure-logic ต่อไป** (GT-037 ที่ DONE แล้ว) — coverage `monster_spawn_and_loot`
   คง `not_started` **ซึ่งถูกต้องตามกติกา** เพราะยังไม่มี client เห็นสักไบต์
3. **ไม่มีโมดูลใหม่ถูกเขียน ไม่มี hypothesis slot ถูกใช้ ไม่มีใบ attended ถูกเปิด**
4. คำถามที่เหลืออยู่จะย้ายไปอยู่บนเลนที่แพงกว่า (เช่น membership-omission GT ในเกม) — **และต้องเป็นใบใหม่ที่เขียนขึ้นหลังเห็นผลใบนี้เท่านั้น**

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ claim ว่าอะไรก็ตามที่เจอ ถูกส่งจริงโดยเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว ไม่เคยเผยแพร่ และกู้ไม่ได้ตลอดกาล
- **ไม่ claim ว่ามีอะไรเรนเดอร์บนจอ** — ทั้งใบเป็นชั้น ① ล้วน · การมี literal/serializer อยู่ในอิมเมจ
  **ไม่ได้พิสูจน์ว่าคลาสนั้นถูกสร้าง ถูก register หรือเคยขึ้นสาย** (nonclaim หัวตารางของ CLASSCENSUS-001 · `tsv:3`)
- **ไม่ claim ว่า derived id `0x4543` ถูก** — เป็นเลขคณิตจากชื่อ ไม่ได้อ่านจากตารางใดในอิมเมจ
- **ไม่ claim ว่า `DropThingBoard` / `DropThingGameObj` ถูก register** — ดูบล็อก erratum ด้านบน
- **ไม่รื้อ** [NEGATIVE] ของ jump table `0x4469BD` (actor_type 2..6) — ปิดแล้ว
- ไม่แตะ DB · ไม่แตะเกม · ไม่แตะ `LOCK_GAME` · ไม่มีรอบเทสไหนถูกเปิดหรือปิดด้วยใบนี้
- **ไม่มีดีไซน์ ไม่มีโมดูล ไม่มีข้อเสนอ wire ในผลของใบนี้** — ถ้าผลกลับมาพร้อมดีไซน์ = ทำเกินใบสั่ง ให้ตัดทิ้ง

> ℹ️ ถ้าฝ่ายคิวถือกฎ **"หนึ่งใบ = หนึ่ง claim"** อย่างเคร่งครัด: ทั้งสามท่อนเขียนแบบพึ่งตัวเองได้
> ⇒ แยก **ท่อน B → GT-041** และ **ท่อน C → GT-042** ได้ทันทีโดยไม่ต้องแก้ข้อความสักบรรทัด
> (ท่อน A คงเลข GT-040 ไว้ เพราะเป็นลำดับความสำคัญที่หนึ่ง)

- **result:** (ผู้รับงาน static บนสะพานกรอก: ผลรายท่อน + VA/span/sha + เวลา + sha อิมเมจก่อน-หลัง)

## 🆕⭐ GT-041 MOVE-AUTHORITY-002: เซิร์ฟเวอร์ "ไม่ยอมเขียน" ตำแหน่งที่ client รายงาน — ผู้เล่นเห็นอะไรไหม  [✅ **PASS (no-rejection) — 2026-08-23 01:01 (+07:00): การเดินธรรมดาไม่ชน gate เลย · relog กลับจุดล่าสุดที่ขึ้นสาย**]

> ✅ **RESULT 2026-08-23 00:32–01:01 (+07:00) — PASS แบบ no-rejection** (บูต green `b665d92`):
> - `TargetPosVital` 122 เฟรม ถอดครบ 122/122 · over-budget **0/122** (max planar step 847.192/งบ 2000 · max speed 411.858/เพดาน 1500 · |dz| 186/งบ 400) — falsification ของ HYP-PF-030 ("เดินธรรมดาถูกปฏิเสธ") **ไม่ถูกยิง**
> - เฟรมสุดท้าย = แถว DB ทุกค่าพอดี · relog (บูต B) กลับเข้า **จุดล่าสุดที่ client เคยส่งขึ้นสาย** (T6) ไม่ใช่จุด HUD สุดท้าย (A4 ไม่เคยอยู่บนสาย — ต่างกัน 2187.65 หน่วย = ตำแหน่ง local ล้วน)
> - ไม่เห็น rubber-band คงอยู่ · client เดินเข้าน้ำ/ทะลุ geometry ได้ (ไม่ claim collision/terrain)
> - ผลเต็ม: `notes_to_chief/20260823_0106_GT041-PASS-NO-REJECTION-RELOG-LAST-WIRE.md` (บริโภค R123) · วิดีโอ 13:30 นาทียังไม่ทบทวนทุกเฟรม — transient <1s = non-observed

**ที่มา:** chief รอบ 116 (HYP-PF-030) — เลนแรกของโปรเจกต์ที่เซิร์ฟเวอร์ **ปฏิเสธการเขียนตำแหน่งที่ client รายงาน** ได้
(`reports/PF_MOVE_AUTHORITY002_SERVER_SIDE_GATE_20260821.md` · `src/pirateforce_foundation/move_authority_hypothesis.py`)
ชั้น wire/DB พิสูจน์จบแบบ headless แล้ว (63 เทส + verifier 87 guards) · **ชั้น client-observable = ศูนย์** นั่นคือใบนี้

### ✅ merge แล้ว (ยืนยันรอบ 117) — ท่าบูต: SHA ตรง ๆ + วิธี re-derive ถ้า `main` ขยับไปอีก

🔴 **ขั้นแรกคือรันเครื่องมือ ไม่ใช่ก๊อป SHA** — SHA ข้างล่างเป็น *คำตอบที่คาดไว้* ไว้เทียบ ไม่ใช่คำสั่ง
(เหตุผล: `git checkout <sha เก่า>` สำเร็จเงียบ ๆ เสมอ ต่อให้ `main` เดินไปอีกสามรอบแล้ว — ผู้เทสจะบูตของเก่า
โดยไม่มีสัญญาณอะไรเลย นี่คือความพังชิ้นเดียวกับที่เครื่องมือถูกเขียนขึ้นมาเพื่อฆ่า · `pf-adversary` ชี้ให้รอบ 117)

```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · แทน `C:\path\to\pirate-force-server` ด้วยพาธ clone จริง (คำสั่ง ASCII ล้วน ปลอดภัยกับคอนโซล cp874)
- **exit 0** + `BOOT_COMMIT: <sha>` ⇒ บูต sha นั้น: `git checkout <sha>` (detached HEAD ถูกแล้ว — เราบูต *คำตัดสิน* ไม่ใช่ branch)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ **ห้ามบูต** · จดในผลว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
- 🔴 ถ้า output มีบรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ **จดลงในผลด้วยเสมอ** (มี commit แดงอยู่บนสาย main
  เหนือคำตอบ — เป็นปัญหาของ chief ไม่ใช่ของคุณ แต่รายงานที่ไม่พูดถึงมันจะดูเหมือนไม่เคยเกิดขึ้น)

**คำตอบที่คาดไว้ ณ วันที่เขียนใบนี้ (รอบ 117):** `cdc52f11b8d93b0eec9db42c83a06f0ed57e2050`
= head ของ PR รอบ 116 (MOVE-AUTHORITY-002) · `conclusion=success` run_id `32426106992` · `2026-08-20T22:54:09Z`
· และเครื่องมือยืนยันเองว่า **tree ของมันเท่ากับ tree ของ `520e2cf` (HEAD ของ main) ทุกไบต์** ⇒ โค้ดที่ถูก gate
กับโค้ดที่อยู่บน branch เป็นก้อนเดียวกันจริง (วัด ไม่ใช่สมมติ)
- ได้ SHA เดียวกัน ⇒ เดินต่อได้เลย · ได้ SHA **ใหม่กว่า** ⇒ ปกติ (มีรอบใหม่ merge เข้าไป) ให้ยืนยันสามข้อข้างล่างกับตัวใหม่
- รันเซิร์ฟเวอร์จาก working tree ของ checkout นี้เท่านั้น · บล็อก **server args** ด้านล่างไม่เปลี่ยนแม้แต่ตัวอักษรเดียว
- ⚠️ คำว่า `success` ที่เครื่องมือส่งต่อ = **subset ของ gate บน GitHub runner** (เก้า check รันบนนั้นไม่ได้)
  **ไม่ใช่ "ผ่าน gate เต็ม"** — gate ตัวจริงยังเป็นจ็อบบนสะพานของคุณ

🔴 **ห้ามบูต HEAD ของ `origin/main` เฉย ๆ และห้ามตีความว่า "คำตัดสินยังไม่มา":**
HEAD (รอบ 117 = `520e2cf`) เป็น **merge commit** ที่ automerge push ด้วย `GITHUB_TOKEN` ⇒ ไม่ trigger Actions
⇒ **ไม่มี `ci/520e2cf....json` และจะไม่มีตลอดไป** (วัดรอบ 116 จาก Actions API · ยืนยันซ้ำรอบ 117)
⇒ ของที่ถูก gate จริงคือ **parent ฝั่ง PR** = SHA ข้างบน · ใครก็ตามที่ไปอ่านคำตัดสินที่ HEAD จะไม่เจอไฟล์
แล้วปฏิเสธการบูตอย่างถูกกฎ ทั้งที่โค้ดเขียวอยู่ต่ำลงไปแค่คอมมิตเดียว — **นี่คือกับดัก ไม่ใช่ความผิดของผู้เทส**

**ยืนยันสามข้อก่อนบูต (ต้องผ่านครบสามข้อ · แทน `<SHA>` ด้วย commit ที่จะบูตจริง):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "move-authority-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/move_authority_hypothesis_speed_gate.json && echo SCENARIO_PRESENT
```
1. ไฟล์คำตัดสินต้องมี `"conclusion": "success"` **และ** `"sha"` ตรงกับชื่อไฟล์
2. `git grep` ต้องเจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐานว่ามี flag** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6) ใช้ `git grep` เท่านั้น
3. ต้องเห็นคำว่า `SCENARIO_PRESENT`
- ไม่ครบสามข้อ = **ห้ามบูต** ใบนี้กลับไป BLOCKED · **ปล่อยไว้ที่เดิม ห้ามลบ ห้ามย้าย**

### 🔴 อ่านก่อนออกแบบท่าทำงาน — เลนนี้ "เงียบสองทาง"

1. **ไม่ประกอบไบต์แม้แต่ตัวเดียว** — ทำได้อย่างเดียวคือ *ไม่เขียน* แถวใน `character_positions`
   เฟรมเดียวกัน เซสชันที่เปิด gate กับไม่เปิด **คืน action list เท่ากันเป๊ะ** (พิสูจน์ headless แล้ว)
   ⇒ **ไม่มีเฟรมใหม่ให้หาใน capture** อย่าเสียเวลาไล่หา
2. **ชื่อ event ของเลน (`move_authority_hypothesis_..._admitted` / `..._no_write`) ไม่ถูกพิมพ์ที่ไหนเลย**
   มันอยู่ใน `state.events` ในหน่วยความจำล้วน ๆ · คอนโซลจะเหมือนบูตปกติทุกประการ = **ถูกแล้ว ไม่ใช่บูตผิดไฟล์**
   ⇒ **สัญญาณที่จับได้จริงมีสองอย่าง:** (ก) hexdump ของ `TargetPosVital` ทุกเฟรมใน raw GAME log
   (ข) แถว `character_positions` ในสำเนา DB · **ลายเซ็นของการปฏิเสธ = ตำแหน่งโผล่ใน log แต่ไม่โผล่ในแถว DB**
   ⇒ **เก็บ raw GAME log ทั้งไฟล์ + สำเนา DB ของรอบไว้ ห้ามลบ** (chief re-derive ขั้นบันไดทีหลัง ท่าเดียวกับ MOVE-CADENCE-001)

### objective (claim เดียว)

**การที่เซิร์ฟเวอร์ปฏิเสธการเขียนตำแหน่ง เปลี่ยนอะไรที่ผู้เล่นมองเห็นหรือไม่ — และการเดินธรรมดาทำให้มันทำงานหรือเปล่า**
(เลนนี้ mutually exclusive กับทุกโหมด ⇒ ไม่มีทางยั่วยุด้วยเลนอื่น · **การเดินธรรมดาคือเครื่องมือเดียวที่มี**)

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-041_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt041.sqlite3
```
- เทียบ sha256 ของ canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง**
- 🔴 **บูตที่สองต้องชี้ `--db state\run_gt041.sqlite3` ไฟล์เดิม ห้าม copy ใหม่** ไม่งั้นการ relog ไม่มีความหมาย (แถวถูกทับ)

### server args (เป๊ะ)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt041.sqlite3 --move-authority-hypothesis-scenario scenarios\move_authority_hypothesis_speed_gate.json
```
- flag นี้ **ห้ามใช้ร่วมกับ scenario โหมดอื่น** และ **ไม่ยอมสตาร์ตถ้าไม่มี `--db` ที่มีอยู่จริง**
  pre-flight ราคาถูก (argparse ตายก่อนแตะไฟล์ใด ๆ): รันคำสั่งเดิมโดยไม่ใส่ `--db` ⇒ คาด exit 2 + ข้อความ
  `--move-authority-hypothesis-scenario requires an explicit existing --db`
- **ไม่มี chat trigger** ไม่ต้องพิมพ์อะไร · ⚠️ ตัวอักษรที่พิมพ์ตอนช่องแชตไม่โฟกัส = hotkey ⇒ ใช้แค่ `W/A/S/D`, `Q/E`, `spacebar`
  (การคลิกพื้นเพื่อเดินถูกปิดไปแล้ว — ดู PLAYBOOK)

### งบที่ ship มา (ทุกตัวเป็นดีไซน์ของเรา)
`max_step_units 2000.0` · `max_speed_units_per_second 1200.0` (+tolerance 0.25 ⇒ เพดานจริง **1500/วินาที**)
· `max_vertical_step_units 400.0` · `min_measurable_elapsed_seconds 0.5` · **`enforce_moving_flag false`**
· `teleport_grace_reports 1` (ให้เฉพาะตอน **เซิร์ฟเวอร์เป็นฝ่าย teleport** เช่นตอนเข้าฉาก ไม่ใช่ตอนต่อเชื่อมใหม่)

🔴 **ห้ามอ้าง `n_SPEED_WALK`/`n_SPEED_RUN` เป็นที่มาของงบ** — เป็นคอลัมน์ของ mob หน่วยไม่รู้ ไม่มีคอลัมน์ของผู้เล่น

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)

- **P1 — คาดว่า "ไม่มีการปฏิเสธเลย" ในการเดินธรรมดา** · chief replay ตารางเดินจริงใบเดียวที่มี
  (`reports/move_cadence001_smoke/replay_output.txt` 29 รายงานของ GT-005) ผ่านบันไดนี้แล้ว: **ปฏิเสธ 0 จาก 29**
  · step ใหญ่สุด 538.4 (งบ 2000) · เร็วสุด 269.2/วินาที (เพดาน 1500) · dz สูงสุด 8.0 (งบ 400)
  ⚠️ นี่คือ **เส้นทางเดียว บูตเดียว ผู้เล่นคนเดียว** — ถ้าเดินจริงแล้วโดนปฏิเสธ **นั่นคือผลที่มีค่าที่สุดของใบนี้**
- **P1b — สองงบถูกหักล้างไปแล้วก่อน ship** (จากตารางเดียวกัน): ถ้าเราบังคับ `moving` flag จะปฏิเสธ **23 จาก 29**
  และถ้าหารด้วยเวลาที่ต่ำกว่าพื้น จะปฏิเสธรายงานปกติเพราะสองเฟรมอยู่ใน heartbeat เดียวกัน ⇒ **แก้ไปแล้วทั้งคู่**
- **P2 — ระหว่างเดินจะไม่มีอะไรเกิดบนจอเลย** (เซิร์ฟเวอร์ไม่ส่งไบต์) · ผลที่เห็นได้คือ **ผลที่มาช้า**: ตอน relog
  ตัวละครจะยืนที่ตำแหน่ง *ที่ถูกยอมรับล่าสุด* (อ้าง GT-005 ที่พิสูจน์แล้วว่า client เข้ามายืนตามแถวใน DB)
- **P3 — ช่องโหว่ที่เรารู้ตัวและจดไว้:** รายงาน **หนึ่งใบแรกหลังเซิร์ฟเวอร์ teleport (ตอนเข้าฉาก) ไม่ถูกวัดเลย**
  ⇒ ถ้าเห็นตำแหน่งแปลก ๆ ถูกเขียนทันทีหลังเข้าแมพ **ไม่ใช่บั๊กใหม่** เป็นช่องที่เขียนไว้ในรายงานแล้ว

### steps (สองบูต)

**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db ·
อ่านสแนปช็อต **T0** จากสำเนาแบบอ่านอย่างเดียว (`mode=ro`):
`SELECT character_id,x,y,z,heading,updated_at FROM character_positions;`
+ `SELECT count(*) FROM sessions WHERE selected_character_id IS NOT NULL;` + `SELECT max(lease_generation) FROM sessions;`

**บูต A**
1. เปิด server ด้วย args ข้างบน (listener 2 ตัวใน ~2 วิ) — **เปิด server ก่อน client เสมอ**
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย
3. หน้าเลือกตัวละคร → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
4. เข้าแมพแล้ว **ถ่าย A0 ทันที ให้เห็น X/Y บน HUD** (จุดที่เซิร์ฟเวอร์วางเราไว้)
5. **ยืนนิ่ง 60 วินาที** → อ่าน DB (**T1**) · คาด: ไม่มี `TargetPosVital` เข้ามาเลย (GT-005 บูต 2 = 0 เฟรม)
6. **กด W ค้างเดินตรง ~20 วินาที** → หยุด → **ถ่าย A1** → อ่าน DB (**T2**) → **เทียบ HUD กับแถว DB ทันที**
7. **เดินข้ามแมพ 2–3 นาที** เลี้ยวด้วย `Q/E` สลับเดินสั้น-ยาว → หยุด → **ถ่าย A2** → อ่าน DB (**T3**)
8. **ขึ้น-ลงทางลาด/บันได + กระโดด (`spacebar`+`W`) อย่างน้อย 5 ครั้ง** → หยุด → **ถ่าย A3** → อ่าน DB (**T4**)
9. **ยืนนิ่ง 30 วินาที** → อ่าน DB (**T5**) → **ถ่าย A4 = จุดสุดท้ายก่อนออก (หลักฐานชิ้นเอก)**
10. ออกจากเกม: **X** มุมขวาบน → dialog ยืนยัน → ปุ่มซ้าย (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X)
11. **ปิด server** เก็บ raw GAME log + console out/err → อ่าน DB หลัง server หยุดสนิท = **T6** + `PRAGMA integrity_check;`

**บูต B (relog)**
12. เปิด server ใหม่ **คำสั่งเดิมเป๊ะ ชี้ไฟล์ DB เดิม** → เปิด client → ทำซ้ำข้อ 2–3
13. **ถ่าย B0 ทันทีที่เข้าแมพ ให้เห็น X/Y** — คำตอบของคำถามที่สอง
    เทียบสามค่า: **A4** (ที่ผู้เล่นยืนตอนออก) vs **T6** (แถวใน DB) vs **B0** (ที่ client วางเราไว้)
14. ยืนนิ่ง 30 วินาที → ออกตามข้อ 10 → ปิด server เก็บหลักฐาน → **T7** + `PRAGMA integrity_check;`
15. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template จะปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · ใช้ `staged\TOOL_stop_stale_server.ps1`)
16. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง **ต้องเท่าเดิม**

### pass criteria — สองชั้น แยกกันเด็ดขาด

**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ)** — ผ่านเมื่อเก็บครบและตอบได้ชี้ขาด ไม่ว่าบวกหรือลบ:
- raw GAME log ทั้งสองบูตครบทั้งไฟล์ (มี hexdump `TargetPosVital` ทุกเฟรม) + console out/err **ห้ามลบ**
- สแนปช็อต `character_positions` ครบ 8 จุด `T0..T7`
- ตอบได้ว่า **มีตำแหน่งที่โผล่ใน log แต่ไม่เคยโผล่ในแถว DB ไหม**
  (ถ้ามี: `updated_at` ต้องค้างช่วงหนึ่งทั้งที่ยังมีรายงานเข้ามา · ถ้าไม่มี: แถวสุดท้าย = รายงานล่าสุด)
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` เพิ่ม **+1 ต่อการเข้าเกมหนึ่งครั้ง** (สองบูต ⇒ +2)
- `PRAGMA integrity_check` = `ok` · sha256 canonical ก่อน-หลังตรงกัน
- **ต้องไม่มี `[G>]` บรรทัดใหม่ที่เป็นของเลนนี้** (เลนนี้ไม่ส่งไบต์ — ถ้าเห็น ให้หยุด)
- **ชั้นนี้ตอบไม่ได้:** ผู้เล่นเห็นอะไร · จอกระตุกไหม · **และขั้นไหนของบันไดทำงาน** (chief re-derive offline)

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)**
- **วิดีโอต่อเนื่อง** ช่วงเดินข้อ 6–8 เห็นตัวละคร + ค่าพิกัด HUD ในเฟรมเดียว
- ตอบสามข้อเป็นภาษาคน: **(ก)** ระหว่างเดินจอ rubber-band/กระตุก/ถูกดึงกลับไหม หรือไม่มีอะไรเลย
  **(ข)** ที่ T2/T3/T4 ค่า HUD กับแถว DB ตรงกันหรือแยกกัน แยกกี่หน่วย
  **(ค)** ตอน relog **B0 = A4 หรือ B0 = T6**
- ภาพนิ่งบังคับ **A0 · A1 · A2 · A3 · A4 · B0** อ่านค่า X/Y ได้ทุกใบ
- **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ไม่ได้เขียนแถว **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### เกณฑ์หยุด
- **จอ rubber-band หรือถูกดึงกลับจริง ทั้งที่เซิร์ฟเวอร์ไม่ส่งไบต์ใหม่เลย** = ข่าวใหญ่ที่สุดที่ใบนี้เป็นไปได้
  ⇒ หยุด เก็บวิดีโอช่วงนั้น + console ทั้งไฟล์ + raw GAME log แล้วจดให้ละเอียด
- มี `[G>]` เฟรมใหม่ที่ไม่มีในบูตปกติ ⇒ หยุด · `ErrorData=28317` ⇒ หยุด เก็บ console ทั้งไฟล์
- ตัวละครจม/ลอย/หลุดพื้นหลัง relog = จด แต่ **ไม่ใช่ falsify** (ground Z ไม่เคยถูกตรวจ)

### ผลลบมีค่าเท่าผลบวก
1. **ไม่มีการปฏิเสธเลย** ⇒ **ผลเต็มใบ** งบรอดจากการเดินจริง (ยืนยัน P1) · คำถามชั้น client-observable **ยังไม่ถูกตอบ**
   ต้องเป็นใบใหม่ที่หาวิธียั่วยุอย่างถูกกติกา — **ให้ chief/Panya เคาะ ห้ามออกแบบเองในใบนี้**
2. **เดินธรรมดาแล้วโดนปฏิเสธ** ⇒ **ผลที่มีค่าที่สุด** — หักล้าง *ตัวเลข* โดยไม่หักล้าง *กลไก*
   ⇒ chief re-derive ขั้นบันไดจาก log แล้วแก้ scenario · `production_allowed` ยัง false · **coverage ไม่ขยับ**
3. **มีการปฏิเสธ แต่ผู้เล่นไม่เห็นอะไรระหว่างเล่น และ B0 = T6** ⇒ **ผลเต็มใบ** = "การไม่ยอมเขียนมองไม่เห็นจนกว่าจะ relog"
   ⇒ authority ที่มีผลในเซสชันต้องมี corrective wire ซึ่ง **เราไม่มีหลักฐานและห้ามประดิษฐ์** ⇒ คงไว้ที่ stop rule เดิม

### nonclaims (ติดไปกับผลทุกกรณี)
- **บันได ลำดับ และทุกตัวเลขในงบ เป็นดีไซน์ของเรา ไม่ใช่นโยบายของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล**
- **ห้ามอ้าง `n_SPEED_WALK`/`n_SPEED_RUN` เป็นที่มาของงบ** · หน่วยพิกัดโลกแปลงเป็นหน่วยจริงไม่ได้
- **ไม่ใช่การตรวจ collision / terrain / line-of-sight** — เซิร์ฟเวอร์ไม่มีเรขาคณิตของแมพ
- **ไม่มี client ตัวไหนเคยเห็นไบต์ของเลนนี้ เพราะมันไม่มีไบต์**
- **ไม่ claim ว่า corrective reposition ควรมีหน้าตาอย่างไร** — TELEPORT มีในฐานะ transport แต่ผลกับ client เป็น UNKNOWN
- **ความเร็วแนวดิ่งไม่ถูกจำกัด** (หารด้วยเวลาเฉพาะแนวราบ) · **หนึ่งรายงานแรกหลังเซิร์ฟเวอร์ teleport ไม่ถูกวัด**
- `production_allowed=false` · **แถว coverage ไม่ขยับไม่ว่าใบนี้จะออกหัวหรือก้อย**

> ℹ️ **เลขชนกัน:** บันทึกท้าย GT-040 เสนอให้แยกท่อน B เป็น GT-041 — **เลข 041 ถูกใช้โดยใบนี้แล้ว**
> ถ้าจะแยกท่อน B/C ของ GT-040 ให้ใช้ **GT-042 / GT-043**

- **result:** (ผู้เทสกรอก: T0..T7 · ภาพ A0–A4/B0 พร้อม sha256 · วิดีโอช่วงเดิน · คำตอบ (ก)(ข)(ค) · เวลา ·
  sha canonical ก่อน-หลัง · path ของ raw GAME log ทั้งสองบูต · **สำเนา `state\run_gt041.sqlite3` เก็บไว้ให้ chief re-derive**)


## GT-030 REMOTE-PLAYER-VIS-001: "มีคนอื่นอยู่ในโลก" ครั้งแรก — actor_type 2 ทั้ง 5 เฟรม  [🟠 **ผล substantive แล้ว — rerun 2026-08-23 00:25 (+07:00): CLIENT NO-RENDER ใต้ mask ชุดนี้ (ตรวจถึงพิกัดจริงระยะประชิด) · 🔴 ห้ามรันรอบสาม — เส้นทางต่อ = static render-mask/selection**]

> 🟠 **RESULT rerun 2026-08-23 00:09–00:25 (+07:00)** (บูต green `b665d92`): wire ครบ 5 เฟรม (`SPAWN_BARE → SPAWN_AVATAR → MOVE_A_1 → MOVE_A_2 → NEGATIVE_CONTROL`) ไม่มี refuse/error · ผู้เทสเดินไปตรวจ**พิกัดจริง**:
> - B `ProbePlayer02` (ยืนห่าง ~33 หน่วย · กวาด 4 มุม): **ไม่เห็นโมเดล/ตัวใส/ป้ายใด**
> - A หลัง MOVE (ยืนห่าง ~52 หน่วย · ระยะประชิด + Tab ×4): **ไม่เห็นโมเดล ไม่มี target panel**
> ⇒ ยกระดับจาก "ระบุตัวไม่ได้" (รอบ #12) เป็น **no-render ใต้ mask/เฟรมชุดนี้** — ผลลบที่ใช้ได้จริง
> - ⚠️ ภาพ before/after ทุก cadence ไม่ครบฟอร์ม (ภาพแรก +3.487s · baseline ไม่คงอยู่ใน root) ⇒ transient <3.487s = non-observed · no-render ยึดจาก persistent check เท่านั้น
> - 📌 เส้นทางต่อ (ห้ามรันเกมเพิ่ม): งาน static — mask bit ไหนจำเป็นต่อ render ของ actor_type 2 / เส้นทาง selection — รอ chief ออกใบ STATIC-ON-BRIDGE เมื่อคำถามคมพอ
> - ผลเต็ม: `notes_to_chief/20260823_0030_GT030-NO-RENDER-GT043-PARTIAL.md` (บริโภค R123)

> 🟡 **ผลรอบใหญ่ #12 (2026-08-21 07:55→08:37 +07:00 · จดหมาย `notes_to_chief\20260821_0840_GT031-PASS-GT030-PARTIAL.md`):**
> - **ชั้น wire: ผ่านครบ** — 5 เฟรมออกครบ ขนาดตรงดีไซน์ทุกเฟรม
>   (`SPAWN_BARE` 181 B · `SPAWN_AVATAR` 288 B · `MOVE_A_1` 72 B · `MOVE_A_2` 77 B · `NEGATIVE_CONTROL` 218 B)
>   grep `compose_refused` / `already_sent` = ไม่พบ
> - **ชั้น client: ยังตัดสินไม่ได้** — ผู้เทสไม่พบป้ายชื่อ `ProbePlayer01/02/ProbeControl03` ที่ไหนเลย
>   คลิกตัวที่สงสัยแล้ว target panel ไม่ขึ้น ⇒ **ระบุ identity ไม่ได้** (ไม่ใช่ "ไม่เรนเดอร์" — ผู้เทสติด nonclaim นี้ไว้เอง ถูกต้องแล้ว)
> - ⭐ **การพบเห็นที่ยังไม่อธิบาย (ห้ามหล่นหาย — chief R119 เติมกลับตามผล adversary):** ผู้เทสเห็น
>   **ตัวละครหน้าตาแบบผู้เล่น (ชายหนุ่มชุดน้ำเงิน-ขาว) ยืนที่ X ≈ `-8681`** — ต่างจาก NPC Navy Transfer ที่คุ้นเคย
>   คลิกแล้ว target panel ไม่ขึ้น · จุดนั้นห่างตำแหน่ง ProbePlayer01 หลัง MOVE (`-8839.957`) ~159 หน่วยทาง +X
>   ⇒ **อาจเป็น actor_type 2 ตัวแรกที่เรนเดอร์จริงในประวัติโปรเจกต์ หรืออาจเป็น NPC ประจำแมพ — ยังตัดสินไม่ได้ทั้งสองทาง**
>   รอบ rerun มีขั้นตรวจจุดนี้ซ้ำโดยเฉพาะ (steps ข้อ 7)
> - เกณฑ์หยุดทั้งเลน (ชื่อ `ProbeControl03` โผล่) **ไม่ถูกยิง** · ไม่มี `ErrorData=28317`
> - ผู้เทสยิงจากจุดเกิดที่รายงาน X `-8553` Y `-2579` กวาดกล้อง 360° แล้วเดิน +X ถึงช่วง X `-8681..-8414`
>
> **วินิจฉัย static ของ chief R119 (มี provenance ครบใน `rounds\R119_mrcii9_gt031_pass_gt030_diagnosis.md`):**
> 1. **ชื่ออยู่ในไบต์ขาออกจริงทั้งสามเฟรม spawn** — BasicAttr bit `0x0001` + wstring tag `0x48` (UTF-16LE)
>    encoder **ปฏิเสธ compose ถ้าไม่มีชื่อ** (`remote_player_hypothesis.py:651-652,668`) · 181 B สอดคล้องเฉพาะกรณีมีชื่อ
>    (ไม่มีชื่อจะเหลือ 150 B) ⇒ **"ไม่เห็นป้ายชื่อ" ไม่ใช่ความล้มเหลวของ wire**
> 2. **ไม่มี claim ที่ commit แล้วว่า nameplate ลอยหัวเรนเดอร์สำหรับ actor_type 2** — ผู้บริโภคชื่อ (BasicAttr+0x28)
>    ที่พิสูจน์ static ได้มีตัวเดียวคือ **target panel** (updater `0x51F920` → `LABEL_NAME 0x5BD624`)
>    ⇒ วิธีระบุตัวในรอบ rerun ต้องเป็น **"คลิก/Tab → อ่าน target panel"** ไม่ใช่ "มองหาป้ายลอยหัว"
> 3. **พิกัดจริงของ probe** — ยึด placement-0 NPC **'Navy Transfer'** ที่ X `-9139.957` Y `-2780.045` Z `223.292`
>    (`pf_login_game_server_v141.py:1324`) · 🔴 **NPC ตัวนี้คือ actor identity `0x2001`** — ตัวเดียวกับที่
>    **GT-032 ทำให้ขึ้นศัตรู** และ GT-022/025 เคยฆ่า ⇒ **ในรอบใหญ่เดียวกัน ให้รัน GT-030 ก่อน GT-032 เสมอ**
>    (landmark ที่เพิ่งถูกทำให้แดง/ตาย ใช้เป็นจุดอ้างอิงกลาง ๆ ไม่ได้):
>    `ProbePlayer01` = **ทับตำแหน่ง Navy Transfer เป๊ะ (ตั้งใจ — จะเห็นตัวซ้อนกัน)** · `ProbePlayer02` = X+150 (`-8989.957`)
>    · `ProbeControl03` = X−150 (`-9289.957`) · A หลัง MOVE = X+300 (`-8839.957`)
> 4. 🔴 **บรรทัดเดิม "probe อยู่แนว +X ~112–412 หน่วยจากจุดเกิด" ผิด/ค้างสองทาง:** (ก) จริงเฉพาะเมื่อยืนที่ค่าคงที่
>    spawn v135 (`-9239.957, -2830.045`) — รอบ #12 ผู้เทสยืนห่างจากจุดนั้น ~731 หน่วย · (ข) `ProbeControl03` อยู่ทาง **−X**
>    คือ**หลังกล้อง**ที่หัน +X · จากจุดที่ผู้เทสยืนจริง probe ทุกตัวอยู่ **350–765 หน่วยทาง −X** — อาจพ้นระยะเรนเดอร์/ระบุ
>    (ระยะเรนเดอร์ของ client = **[UNKNOWN]**)
> 5. ข้อเสนอของผู้เทสข้อ 1 (ให้ client console พิมพ์ identity ของ actor) **ทำไม่ได้ — client binary แก้ไม่ได้**
>    ⇒ แทนด้วยวิธี landmark + target panel ตามโปรโตคอลด้านล่าง
> - **rerun ไม่ต้องแก้โค้ด** — one-shot flag เป็นของ**ต่อ GAME connection** (`remote_player_sweep_count` อยู่ใน
>   session state ที่สร้างใหม่ต่อ connection ที่ accept — `runtime.py:509` · accept loop `pf_login_game_server_v141.py:7399`)
>   ⇒ บูตใหม่ = connection ใหม่ = flag รีเซ็ตแน่นอน · แต่ **reconnect ในบูตเดียวกันก็ได้ sweep ชุดใหม่ได้เช่นกัน** —
>   ถ้าเกิด reconnect กลางรอบ จดไว้ว่า probe อาจถูก spawn ซ้ำ (ตัวเก่าไม่ despawn)

- **objective:** พิสูจน์หนึ่งข้อ: **client เรนเดอร์และให้ระบุตัว actor_type 2 (remote player) ที่เซิร์ฟเวอร์ spawn ได้หรือไม่**
  (ทุกเฟรม "ตัวอื่นในโลก" ก่อนหน้านี้ = actor_type 4 ทั้งหมด · นี่คือ actor_type 2 = `CNetActor` สาขา remote player ครั้งแรกของโปรเจกต์)
- **db:** สำเนา `state\pirateforce.sqlite3` ตามปกติ — **ห้ามเปิด canonical** · ตรวจ sha256 canonical ก่อน-หลังรอบ ต้องตรงกัน
  (เพราะเป็นสำเนา ตำแหน่งตัวละครจะรีเซ็ตกลับจุดเกิดทุกบูต — โปรโตคอลข้างล่างนับข้อนี้ไว้แล้ว)
- **server args:** `--remote-player-hypothesis-scenario scenarios\remote_player_hypothesis_visibility_probe.json` (+ `--db` สำเนา)
  ท่าบูตเดียวกับ GT-024/027 เป๊ะ เปลี่ยนแค่ flag · console label = `HYP_PF_025_REMOTE_PLAYER_<STEP>` ·
  event = `remote_player_hypothesis_visibility_probe_sent` — เห็นชื่ออื่น = บูตผิดไฟล์
  **one-shot ต่อ GAME connection** — ยิงซ้ำใน connection เดียวได้ `..._already_sent_no_reply` · **reconnect = ยิงใหม่ได้**
  (ดูโน้ตในบล็อกวินิจฉัยข้างบน) · compose ถูกปฏิเสธ = `..._compose_refused_no_reply_<เหตุผล>` และไม่มีไบต์ออกเลย
- **steps:**
  1. preflight จอว่าง (การ์ด elevated ของรอบ 111) → **สตาร์ตเซิร์ฟเวอร์ก่อน แล้วค่อยบูต client** (client ไร้เซิร์ฟเวอร์ตายใน ~3.5 นาที ·
     ถ้ารอบก่อนเพิ่งฆ่า client ไป **ต้อง restart เซิร์ฟเวอร์ก่อน** ไม่งั้นค้าง "connecting")
  2. เข้าเกมด้วยตัวละครเดิม (ท่า `Return` → เข้าเกม ตามบทเรียนรอบ #12 — คลิกปุ่มอาจไม่ติด)
  3. 🔴 **เดินไปหา NPC 'Navy Transfer' ก่อน** (landmark ใกล้จุดเกิด · X `-9139.957` Y `-2780.045`) — **ห้ามยิงจากจุดเกิด**
  4. ยืนข้าง Navy Transfer แล้วถ่าย **baseline สองใบก่อนยิง**: ใบหนึ่งหันกล้องเห็นฝั่ง **X+150** ใบหนึ่งเห็นฝั่ง **X−150**
     (หรือเฟรมเดียวที่เห็นทั้งสองฝั่งถ้ามุมกว้างพอ) — จำกรอบกล้องทั้งสองไว้ใช้ซ้ำทุกเฟรม
  5. ยิง trigger: **`Return` → พิมพ์ ascii 12 ตัวเป๊ะ → `Return`** (สั้นกว่านี้ = ถึงเซิร์ฟเวอร์แต่เงื่อนไขเงียบ ·
     พิมพ์ตอนช่องแชตไม่โฟกัส = กลายเป็น hotkey)
  6. sweep **5 เฟรม ห่างกัน 15 วิ/เฟรม (75 วิทั้งชุด — cadence เดิม)**: ทุกเฟรมถ่าย before/after **ที่กรอบกล้องเดียวกับ baseline**
     ทั้งสองฝั่ง ตามตารางคำทำนายข้างล่าง
  7. หลังจบชุด: **ระบุตัวด้วยตำแหน่งเทียบ Navy Transfer + คลิกซ้าย (ลอง Tab ด้วยถ้าคลิกไม่ติด) → อ่านชื่อใน target panel**
     ทีละตัว: จุดทับ Navy Transfer (คาด ProbePlayer01 ซ้อน — คลิกอาจโดน NPC ก่อน จดว่าโดนตัวไหน) · X+150/X+300 · X−150
     · ⭐ **เทียบหน้าตากับ "ชายหนุ่มชุดน้ำเงิน-ขาว" ที่รอบ #12 เห็นที่ X ≈ −8681** — ตัวแบบเดียวกันโผล่อีกไหม
     ที่จุดไหน ขยับตาม MOVE ไหม ถ่ายภาพเสมอแม้ target panel ไม่ขึ้น
  8. จบเทส: ปิด client → teardown ตามปกติ **ภายใน 420 นาทีจาก boot stamp** (เพดานถูกยกจาก 180 → 420 เมื่อ 2026-08-20 —
     `staged\TEMPLATE_teardown_generic.ps1:135` · เลข 180 ที่เห็นในใบเก่า ๆ = stale) · run copy ทิ้งได้ ·
     restart เซิร์ฟเวอร์ก่อนบูตรอบถัดไป
- **สิ่งที่ควรเห็นทีละเฟรม (คำทำนาย — ไม่ใช่ข้อเท็จจริง · พิกัดแก้เป็นค่าจริงยึด Navy Transfer แล้ว):**
  | t | เฟรม | ถ่ายอะไร |
  |---|---|---|
  | +0s | `SPAWN_BARE` — identity A `0x00A00001` ชื่อ `ProbePlayer01` **ทับตำแหน่ง Navy Transfer เป๊ะ** | มีตัว**ซ้อน/stack** กับ Navy Transfer ไหม? รูปร่างอะไร (คน/กล่อง/ตัวใส)? |
  | +15s | `SPAWN_AVATAR` — identity B `ProbePlayer02` ที่ **X `-8989.957`** (X+150) **พก AvatarAttr ของตัวละครที่เลือกอยู่ (replay)** | **B ต่างจาก A ตรงไหน — คำตอบของ "AvatarAttr จำเป็นไหม"** ถ่ายให้เห็นทั้งคู่เฟรมเดียวถ้าทำได้ |
  | +30s | `MOVE_A_1` — MovementAttr เดี่ยว mask `0x01` → A ควรย้ายไป **X `-8839.957`** (X+300) | ตัวที่ซ้อน Navy Transfer หายจากจุดเดิม/ไปโผล่จุดใหม่ไหม? เดินหรือวาร์ป? |
  | +45s | `MOVE_A_2` — mask `0x03` heading π/2 | A หันหน้าไหม? |
  | +60s | `NEGATIVE_CONTROL` — identity C ที่ **X `-9289.957`** (X−150 — **ฝั่งตรงข้ามกับ B/A**) พก **NPCAttr ผิดคลาสโดยตั้งใจ** (ชื่อ `ProbeControl03`) | ฝั่ง −X มีตัวโผล่ไหม? (bind gate `0x4697B0` เกต CNetNPC ต้อง drop เงียบ) |
  | หลังจบ | ขั้นระบุตัวตาม steps ข้อ 7 | target panel ขึ้นไหม / ชื่อในพาเนลคือ `ProbePlayer01`/`ProbePlayer02` ไหม / ตัวจม-ลอยพื้น (ground Z ไม่ได้ตรวจ — ไม่ falsify) |
- **pass criteria (สองชั้น แยกกัน — ห้ามอ้างชั้นหนึ่งแทนอีกชั้น):**
  - **wire/DB (headless ได้ ไม่ต้องมีคน):**
    - 5 เฟรมออกครบตาม label + delay 15 วิ · ขนาด **181/288/72/77/218 B ตามลำดับ** (ตรงกับรอบ #12 — เบี่ยงจากนี้ = จดทันที
      **ยกเว้น 288 B ของ `SPAWN_AVATAR`**: หาง avatar เป็น replay ของตัวละครที่เลือกอยู่ scenario ตั้งใจไม่พินหาง
      (`avatar_tail_excluded_from_pin: true` — พินเฉพาะโครง 172 B) ⇒ 288 เป็นตัวเลขผูกตัวละคร ณ รอบ #12 เปลี่ยนได้โดยไม่ผิด)
    - ไม่มี `compose_refused` / `already_sent` (ในบูตแรกของรอบ) · ไม่มี `ErrorData=28317`
    - sessions +1 ต่อการเข้าเกม · `PRAGMA integrity_check` = `ok` · sha256 canonical ก่อน-หลังตรงกัน
    - **ชั้นนี้ตอบไม่ได้ว่าจอเห็นอะไร** — 181 B พิสูจน์ว่า *ชื่ออยู่ในไบต์* ไม่ใช่ว่า *ชื่อเรนเดอร์*
  - **client-observable (ต้องมีคนหน้าจอ):**
    - ตอบได้อย่างน้อย: **(ก)** เฟรม +0 มีอะไรโผล่/ซ้อนที่ตำแหน่ง Navy Transfer หรือไม่ (เทียบ baseline กรอบเดียวกัน)
      **(ข)** target panel ของตัวที่ X+150 (หรือ X+300 หลัง MOVE) ขึ้นชื่อ `ProbePlayer02`/`ProbePlayer01` หรือไม่
      **(ค)** ฝั่ง X−150 มีตัวโผล่หรือไม่ และถ้าโผล่ target panel ว่าง/ไม่ขึ้นหรือไม่
    - ภาพบังคับ: baseline 2 ใบ + before/after ทุกเฟรม (กรอบกล้องเดิม) + ภาพ target panel ทุกครั้งที่เปิดได้
    - **ผลลบมีค่าเท่าผลบวก:** ข้อสรุป "ไม่เรนเดอร์" ให้ยึดจาก **B (X+150) และ A หลัง MOVE (X+300) เท่านั้น** —
      เฟรม +0/+15 ของ A ทับตัว NPC จึงอาจถูกโมเดล NPC บังทั้งตัว (ตัดสินจากจุด stack ไม่ได้) ·
      ถ้า B และ A-หลัง-MOVE **ไม่โผล่ทั้งคู่** = "actor_type 2 spawn แล้วไม่เรนเดอร์ด้วย mask ชุดนี้"
      — เป็น**ผลเต็มใบ ไม่ใช่ fail** · redirect: chief สอบ mask bit ฝั่ง render แบบ static ก่อนออกใบใหม่ (ห้ามเดา bit ในใบนี้)
      ส่วน "โผล่แต่ target panel ไม่ขึ้นชื่อ" = ผลอีกแบบ (เรนเดอร์ได้แต่ bind ชื่อไม่ถึงพาเนล) — จดแยกข้อ ห้ามยุบรวม
- **เกณฑ์หยุดทั้งเลนทันที (คงเดิม):** ⛔ ชื่อ **`ProbeControl03` โผล่ที่ไหนก็ตาม** (ป้ายหรือพาเนล) = ข้ออ้าง bind-gate ของก้อน 1 ผิด —
  ทุกข้อสรุปก้อน 1 ต้องรื้อ · หรือ server log มี `ErrorData=28317` ⇒ หยุด เก็บ console ทั้งไฟล์
- 🔴 **ไม่มีทาง despawn probe** — สามตัวค้างจนตัด connection · จบเทสปิด client แล้ว teardown ตามปกติ
- 🔴 HP ของ probe = 100 ทุกตัว — ถ้าเห็นตัวไหน "ตาย" เอง = ผิดคาด จดละเอียด
- **nonclaims:** (คงของเดิมครบ + เพิ่มจาก R119)
  - ดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล (ไม่มี capture remote human player แม้แต่เฟรมเดียว)
  - ไม่ claim ว่า mask bit ไหนของ ActorAttr จำเป็นต่อการเรนเดอร์
  - ไม่ claim ว่า avatar ถูกยอมรับใต้ identity อื่น (จนกว่าจะเห็น B)
  - นี่ไม่ใช่ผู้เล่นสองคนจริง (ก้อน 3 ยังไม่อนุมัติ)
  - **ไม่ claim ว่า nameplate ลอยหัวมีอยู่สำหรับ actor_type 2** — ผู้บริโภคชื่อที่พิสูจน์แล้วมีแค่ target panel · "ไม่เห็นป้าย" ตัดสินอะไรไม่ได้
  - **ระยะเรนเดอร์ของ client = [UNKNOWN]** — ใบนี้ลดตัวแปรด้วยการยืนติด landmark ไม่ใช่การวัดระยะ
  - "ระบุตัวไม่ได้" (รอบ #12) ≠ "ไม่เรนเดอร์" — สองประโยคนี้ห้ามใช้แทนกันในทุกผลของใบนี้
  - **ยังไม่มีหลักฐาน static ว่า click/Tab targeting bind กับ actor_type 2 ได้เลย** — เส้น `0x51F920→LABEL_NAME`
    พิสูจน์เฉพาะ "copy ชื่อหลัง bind แล้ว" ไม่ใช่ "bind ได้" · ถ้า rerun จบที่ "พาเนลไม่ขึ้นทุกตัว" อีก
    **อย่ารันซ้ำรอบสาม** — chief ต้องสอบ selection path ฝั่ง client แบบ static ก่อน (จดเป็นงาน static รอบหน้าแล้ว)
- **result:** (ผู้เทสกรอกรอบ rerun: คำตอบ (ก)(ข)(ค) · ภาพ baseline + before/after ทุกเฟรม + target panel พร้อม sha256 ·
  เวลา · sha canonical ก่อน-หลัง · path raw GAME log — *ผลรอบ #12 ถูกจดไว้ในบล็อกหัวใบแล้ว ห้ามลบ*)

## GT-031 DAMAGE-HP-LINK-001: วงเต็ม "ตี → เลือด → ตาย" ครั้งแรก (ฝั่ง**ผู้เล่นเอง**)  [✅ **PASS — รอบใหญ่ #12 (2026-08-21 ~08:0x +07:00)**]

> ✅ **PASS ทั้งสองชั้น (chief R119 จดจากจดหมายผู้เทส `notes_to_chief\20260821_0840_GT031-PASS-GT030-PARTIAL.md`):**
> - **wire:** ครบ 8 เฟรมเรียงถูกลำดับ (`HP_BASELINE`…`DYING_ELAPSED` — ขนาดไบต์ตรงดีไซน์ทุกเฟรม)
> - **client:** หลอด HP ลดเป็น `37/100` **เฉพาะช่วงเฟรม `HP_AFTER_WEAK` (+30)** — ที่ ~21 วิ (หลัง `HIT_WEAK` +15)
>   หลอดยัง `100/100` ⇒ **การเชื่อมเป็นของเฟรม hp ไม่ใช่ของเฟรมเลข** (เกณฑ์หักล้างรอบ 83 **ไม่ทำงาน** — เรื่องดี)
> - จบชุด: `0/100` + ตัวละครนอนพื้น + หน้าต่าง `Common_Death` เปิด · ไม่กดปุ่มคืนชีพใด ๆ ตามข้อห้าม
> - teardown สะอาด: `AFTER listeners = 0` · `canonical guard OK: unchanged` · ภาพ: `outputs\screenshot-1787274365547-01eea183.jpg`
> - **nonclaims ที่ผู้เทสติดไว้ (คงไว้ทั้งหมด):** ไม่ได้สังเกตเลขลอย 63/379/MISS รอบนี้ · ไม่ได้สังเกตช่วง ~45–100 วิ
>   (MISS/HP_AFTER_MISS/HIT_STRONG — ถูกขัดจังหวะ) = "ไม่ได้สังเกต" ไม่ใช่ "ไม่เกิด" · สูตร/การเชื่อมเป็นดีไซน์ของเรา · ไม่ claim HP persist
> โปรโตคอลด้านล่างเก็บไว้เพื่อ re-run ในอนาคต (เช่น GT-038 ที่ใช้ HP baseline ตัวจริง)

[🟢 เดิม: PENDING — บล็อกรอบใหญ่ #11 โดยหน้าต่าง elevated (preflight guard จับได้แล้ว · รอบ #12 blockers = 0)]

> 🔴 **รอบใหญ่ #11 (2026-08-21 ~02:3x): บล็อกโดยหน้าต่าง `Administrator: Windows PowerShell` (elevated, always-on-top)**
> ที่ค้างอยู่กลางจอ · Windows ห้าม process ธรรมดาแตะหน้าต่าง elevated **ทุกช่องทาง** — ผู้เทสวัดครบทั้งสาม:
> คลิก = ไม่มีผล · `ShowWindow(SW_MINIMIZE)` = ไม่มีผล · `SetWindowPos` = **`False` `lastError=5` ACCESS DENIED**
> ย้าย**หน้าต่างเกม**หนีได้ (จ็อบ 955/956) แต่เกมยังไม่รับคลิก — คาดว่า foreground lock **แต่ยังไม่ได้พิสูจน์**
> ⇒ **ไม่ได้ยิงทริกเกอร์ ไม่ได้เข้าแมพ ⇒ ไม่มีผลใด ๆ ทั้งสิ้น** · เสียเวลาไป ~20 นาที
> ✅ **การ์ดใหม่ (chief รอบ 111): `staged\TEMPLATE_preflight_unattended.ps1`** — ลิสต์หน้าต่างที่มองเห็นทั้งหมด
> แล้ว **ABORT ทั้งรอบพร้อมบอกชื่อ ถ้าเจอหน้าต่าง elevated** (อ่านอย่างเดียว ไม่ย้าย ไม่ปิด ไม่ฆ่าอะไร)
> · "ตรวจไม่ได้ว่า elevated หรือไม่" ถูกนับเป็น **สิ่งที่ต้องรายงาน ไม่ใช่ผ่าน** (นั่นคืออาการปกติของ elevated)
> 🔴 **ข้อเสนอถึง Panya: ก่อนสั่งรอบ unattended ให้เหลือแต่หน้าต่างธรรมดาบนจอ** — ผู้เทสแก้เองไม่ได้จริง ๆ
> 🟢 **ตัวเทสเองไม่มีอะไรเปลี่ยน** — โปรโตคอลด้านล่างยังใช้ได้ทั้งหมด รันได้ทันทีที่จอว่าง
> 💡 **บริบทใหม่:** GT-039 (ฝั่งเป้าหมาย) PASS ไปแล้ว ⇒ ใบนี้ตอบคำถามที่เหลือคือ **ฝั่งผู้เล่นเอง**

[🟢 เดิมเป็น PENDING — พร้อมรันหลัง commit ของ chief รอบ 97 (`af10536` · HYP-PF-026)**]

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

## GT-032 NPC-HOSTILE-001: NPC ตัวแรกของ Port Royal "ขึ้นศัตรู (แดง)" ไหม — Door A ของ mob-aggro  [✅ **PASS — รอบใหญ่ #12 ต่อ (2026-08-21 ~09:00 +07:00 · จ็อบ 966/967) · ผลเต็มบริโภคโดย chief R120**]

> ✅ **ผล (chief R120 บริโภคจาก `notes_to_chief/20260821_0900_GT032-PASS-GT033-BLOCKED-input.md`):**
> wire = 1 เฟรม `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` (190 bytes · late 0.5ms · ไม่มี refusal) ·
> client = NPC `0x2001` กด Tab เลือกเป็นศัตรูได้จริง — **แถบเป้าหมายสีแดง `HP 100/100 Lv.1` + ไอคอนศัตรู** ·
> ไม่มีป้ายชื่อแดง (ตรงคำทำนาย — เฟรมนี้ไม่มี name bit) · ภาพ `outputs\screenshot-1787276810199-d317fb3d.jpg`
> 🔴 **แก้เกณฑ์ที่ chief เขียนผิดเอง (สืบโดย R120):** ข้อ "ควรเห็น event `..._start_game_sent` ใน console" **สังเกตไม่ได้โดยโครงสร้าง**
> — `self.events` เป็น list ในหน่วยความจำ ไม่มีบรรทัดไหนใน src/ พิมพ์มันออก console (ตัวพิมพ์เดียวคือ `[G>] label (N bytes)`
> ที่ `current/pf_login_game_server_v141.py:7762` ซึ่งพิมพ์เฉพาะเฟรมขาออก) ⇒ การ grep ไม่เจอของผู้เทส = พฤติกรรมปกติ ไม่ใช่ความผิดปกติ
> ✅ **pairing ครบทั้งสองข้างพิสูจน์ทางอ้อมได้แน่น:** dispatch มี guard `runtime.py` — ถ้า faction-1 StartGame ไม่ถูกส่ง
> จะปฏิเสธ `npc_hostile_hypothesis_player_faction_not_applied_no_reply` และไม่มีไบต์ออก ⇒ **การที่ HOSTILE_SPAWN ออกไปได้เลย = faction-1 ลงแล้วจริง**
> (ทางเลือก (ค) ของผู้เทส "hostility ไม่ต้องพึ่ง player faction" ตกไปด้วย arena-v2 อยู่แล้ว: NPC 6 เดี่ยว vs player faction 0 = เป็นกลาง 1,023 ครั้ง)
> 🟡 **ค้างหนึ่งข้อ (ยกเป็นเกณฑ์แถมของรอบใหญ่หน้า ไม่เปิดใบใหม่):** แยกไม่ออกว่า "เส้นขอบแดงรอบตัว" เป็นผลของ hostility
> หรือของการเลือกเป้า — ผู้เทสถ่ายก่อน Tab (ไม่มีขอบ) กับหลัง Tab (มีขอบ) ⇒ ครั้งหน้าถ้าแวะเลนนี้ **ถ่ายหลังยิงแต่ก่อนกด Tab** หนึ่งภาพ

**ที่มา:** ดราฟต์ mob-aggro รอบ 98 แยกการสู้เป็นสามประตู — **hostility · attack · hit-lands** — และมีแค่ประตู hostility (Door A) กับ hit-lands ที่พิสูจน์บนสายแล้ว · SCENE-005 เคยทำ **ชื่อแดง + เส้นขอบแดง + แผง target แดง** บนจอจริง โดยจับคู่ faction: **ผู้เล่น 1 vs NPC 6** · แต่ arena-v2 พิสูจน์ว่า **NPC 6 เดี่ยว ๆ กับผู้เล่น faction 0 (ค่าคอนสตรัคเตอร์) = เป็นกลาง** (นับ 1,023 ครั้ง) ⇒ ต้องส่งสองข้าง เลนนี้ทำครบสองข้าง แล้วยิง NPC `0x2001` ตัวเดิมที่ GT-022/025 ทำให้ตาย
⭐ **nonclaim ที่ต้องติดทุกผล: faction 1 และ 6 เป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล** · เลนนี้พิสูจน์ hostility เท่านั้น — **ยังไม่มี NPC โจมตี** (Door B ยังปิด)

**boot (ท่าเดียวกับ GT-024/027/030/031 เป๊ะ เปลี่ยนแค่ flag):**
- `--npc-hostile-hypothesis-scenario scenarios\npc_hostile_hypothesis_faction_pairing.json` (+ `--db` สำเนาตามปกติ)
- 🔴 **เลนนี้ผูกกับ identity `0x10010001` (ตัวละคร canonical smoke) — ตัว StartGame จะได้ faction 1 ต่อเมื่อเป็นตัวนี้เท่านั้น** ถ้าเผลอเลือก/สร้างตัวอื่นจะได้ StartGame ปกติ (ไม่มี faction) แล้ว sweep จะปฏิเสธ `..._player_faction_not_applied_no_reply` — ไม่มีไบต์ออก (ตั้งใจ: เห็นคู่ครบหรือไม่เห็นเลย)
- trigger เดิม: แชต **ascii 12 ตัวเป๊ะ** → **sweep 1 เฟรมเดียว** (`HOSTILE_SPAWN`)
- console label = `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` · event = `npc_hostile_hypothesis_faction_pairing_sent` — เห็นชื่ออื่น = บูตผิดไฟล์ · **one-shot** (ยิงซ้ำ `..._already_sent_no_reply`)
- ⚠️ ตอน StartGame ควรเห็น event `npc_hostile_hypothesis_player_faction1_start_game_sent` ใน console **ก่อน** ยิง — ยืนยันว่าครึ่ง entry ลงแล้ว
- ก่อนยิง: เดินให้ NPC `0x2001` (ตัวแรกของ Port Royal ใกล้จุดเกิด — XYZ อยู่ในเฟรม SPAWN) อยู่ในเฟรมกล้อง เห็นทั้งชื่อ/ตัว NPC
- 🔴 **โน้ตข้ามใบ (chief R119):** `0x2001` = NPC **'Navy Transfer'** = **landmark ของ GT-030 rerun** ⇒
  **ในรอบใหญ่เดียวกัน รัน GT-030 ให้จบก่อนใบนี้เสมอ** — ใบนี้ทำให้ landmark ขึ้นศัตรู ใช้เป็นจุดอ้างอิงกลาง ๆ ต่อไม่ได้

**สิ่งที่ควรเห็น (คำทำนาย — ไม่ใช่ข้อเท็จจริง):**
- **หลังยิง 1 เฟรม:** NPC `0x2001` เปลี่ยนเป็น **ขึ้นศัตรู** — เส้นขอบแดง · กด Tab เลือกแล้วได้ **ลูกศร/แผง target สีแดง** เหมือนตอน SCENE-005 ทำกับ NPC `0x203D`
- 🔴 **ไม่มีป้ายชื่อแดง** — เฟรมนี้ **ไม่มี name bit** (ต่างจาก SCENE-005 ที่เป็น scene-load) ⇒ สิ่งที่ดูคือ **เส้นขอบ + แผง Tab target** ไม่ใช่ป้ายชื่อ
- **ผลลบมีค่าเท่าผลบวก:** ถ้า NPC **ไม่ขึ้นแดง** (แต่ SCENE-005 แบบ scene-load ยังทำได้) ⇒ faction บิตตอน spawn บนท่อ actor-entry **ไปไม่ถึง relation read** — เป็นคำตอบที่ redirect Door A ทั้งประตู จดละเอียด

**pass criteria สองชั้น:** ① wire = 1 เฟรม `HOSTILE_SPAWN` + StartGame มี faction-1 (console: สอง event ข้างบน) ② client = NPC `0x2001` ขึ้นศัตรู (เส้นขอบ/แผง Tab แดง) หรือไม่ — **ตอบ yes/no พร้อมภาพ** · ถ้า Tab แล้วเลือกไม่ได้/ไม่มีแผงแดง = ผลลบ (จดเป็นผล)
🔴 **จบเทส:** ถ่ายภาพแล้ว **End task** (เลนนี้ไม่แตะ DB · ไม่มี path ใด ๆ ให้กด) · run copy ทิ้งได้ · teardown ตามปกติ
**nonclaims บังคับ:** faction 1/6 เป็นของเรา · ไม่ claim ว่าคู่ (1,6) ทำงานบน NPC ที่ project ผ่าน actor-entry เหมือนตอน scene-load (นั่นคือสิ่งที่เทสนี้วัด) · ไม่มี aggro/threat/chase/attack · ไม่มี persistence (faction ไม่มี write path)

## 🛠️ บทเรียนเครื่องมือใหม่จากรอบใหญ่ #12 (chief R119 ยกจากจดหมายผู้เทส 2026-08-21 08:37 +07:00)

1. 🔴🔴 **ปุ่มในเกมไม่ตอบสนองคลิกสังเคราะห์เป็นช่วง ๆ — แต่ `Return` ใช้ได้เสมอ**
   - หน้า character select: คลิกปุ่ม `เข้าเกม` ไม่ติดเลยสักครั้ง (เคอร์เซอร์อยู่บนปุ่ม ปุ่มขึ้น hover ด้วยซ้ำ) · กด `Return` เข้าเกมทันที
   - ช่องแชต: คลิกแล้วพิมพ์ → ตัวอักษรหาย · **กด `Return` ก่อน → ช่องโฟกัส → พิมพ์ได้ปกติ**
   ⇒ **ท่ามาตรฐานใหม่ทุก GT: `Return` → พิมพ์ → `Return`** · ปุ่มไหนไม่ยอมติดให้ลอง `Return` ก่อนเสมอ
2. 🔴 **หน้าต่าง PowerShell ของ watchdog เด้งทุก ~5 นาทีและแย่งโฟกัส** (เห็นสองครั้งในรอบ #12)
   — เป็นคำอธิบายที่เข้ากับ "คลิกไม่ติดเป็นช่วง ๆ" ข้อ 1 แต่**ยังไม่ได้พิสูจน์ว่าเป็นสาเหตุเดียว**
   ⇒ เข้าคู่บทเรียนเดิมรอบ #9/#10 เรื่อง `hold_key` ค้างเมื่อโฟกัสถูกแย่ง — ความเสี่ยงเดียวกัน คนละอาการ
   🔴 **ข้อเสนอถึง Panya (chief R119): watchdog console โผล่บนจอ = มันไม่ได้รันแบบ hidden** —
   ถ้าจะให้รอบ unattended นิ่ง ควรสลับ task ให้รันแบบซ่อน/ไม่แตะ desktop ของเซสชันเทส (ตัดสินใจฝั่งเครื่องเท่านั้น chief ทำจากคลาวด์ไม่ได้)
3. **คลิกท้องฟ้า/พื้นในหน้า character select = ยกเลิกการเลือกตัวละคร** (ปุ่มเหลือ 3 ปุ่ม) — ต้องคลิกตัวละครเลือกใหม่ก่อน

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


## 🆕🔬 GT-042 DROPTHING-REDERIVE-001 [STATIC-ON-BRIDGE]: ตรวจซ้ำแบบ "ปฏิปักษ์" ผลสามท่อน A/B/C ของ GT-040 + ปิดชิ้นที่ขาดชิ้นเดียว (`0x402A20`)  [✅ **PASS — 2026-08-23 02:03 (+07:00) หลัง adversarial re-derive · มี erratum ขอบเขต handler หนึ่งจุด · แถว semantic รอดทั้งหมด**]

> ✅ **RESULT 2026-08-23 01:54–02:03 (+07:00) — PASS พร้อม erratum** (อิมเมจ SHA ก่อน/หลังทุกจ็อบตรง `9627211412ac…8b623` · read-only):
> - แถว semantic ของ GT-040 A/B/C **รอดทั้งหมด**: ตารางฟิลด์สอง sub-serializer (`0x5E2960` bit 0x04 · `0x5F85B0` bit 0x08) · generation-stamp reconcile (`0x446F30`/`0x441C40`) · gate bit `0x02` · vtable/serializer/handler ของ `PickupTerrainThing`
> - 🔴 **ERRATUM ต้องพกไปทุกที่ที่อ้าง:** span เดิม `[0x005EF640,0x005EF908)` len 712 "hash ตรงแต่ป้ายผิด" — **ไม่ใช่** handler ฟังก์ชันเดียว · handler จริง = `[0x005EF640,0x005EF66F)` len 47 SHA `5d17fc4…8d602e` (อ่าน `+0x18` แยก FC/FD/FE → message 1F/03/22)
> - ชิ้นที่ขาดปิดแล้ว: `0x402A20` **ไม่อ่าน argument** — one-time init คืน singleton `0x0102C6C0` · **`[mgr+0x24]` = ordered registry ของ network actor objects (actor_type 2..6) ที่ singleton นี้ลงทะเบียน — subset ของ runtime actors ไม่ใช่ collection เฟรมล่าสุด และไม่ใช่ scene-load population ทั้งหมด** · สมมติฐาน `[esi+0x1C]+0x10` เป็นตัวเลือก manager = ตาย
> - ⭐ **คำสั่งปลดล็อกของ GT-040 มีผล:** ใบนี้ปิด ⇒ ข้อห้าม "เขียนโมดูล/encoder จาก span GT-040" **ปลดเฉพาะแถวที่รอด/ขอบเขตที่แก้แล้ว** (การเขียนจริงยังต้องเดินตาม pattern มาตรฐาน: opt-in · production_allowed=false · fail closed · ledger/verifier/matrix · headless proof)
> - ผลเต็ม + artifact 9 ใบใน `pf_bridge/outbox/`: `notes_to_chief/20260823_0203_GT042-REDERIVE-PASS-WITH-HANDLER-SPAN-ERRATUM.md` (บริโภค R123)

**หมวด:** `STATIC-ON-BRIDGE` — ต้องเปิด `GameClient.local.bin` จึงทำบน cloud clone ไม่ได้เลย
ผู้รับงานคือคนที่นั่งอยู่หน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว** (ดู "ชั้น ②")

**ที่มา:** GT-040 ปิดครบสามท่อนโดยเซสชันผู้ช่วยของ Panya (2026-08-21 09:36-09:56 +07:00)
จดหมายผลสามฉบับประกาศเงื่อนไขของตัวเองไว้ชัด: **(ก) ไม่มี subagent ตัวไหนเดินซ้ำผลเลย**
**(ข) ผลทั้งหมดเป็นชั้น wire/static ล้วน** **(ค) ห้ามเขียนโมดูล/encoder จาก span พวกนี้จนกว่าจะมีคนตรวจซ้ำ**
ทุกข้ออ้างในสามใบแนบ **span VA + file offset + len + sha256** ไว้ให้เดินซ้ำเอง ⇒ ใบนี้คือการเดินซ้ำนั้น
🔴 **ท่าคือ "พยายามหักล้าง ไม่ใช่พยายามยืนยัน"** — ถ้าเดินตามรอยเดิมเพื่อจะเห็นสิ่งเดียวกัน จะมองข้ามจุดที่ผิดเสมอ

### objective (claim เดียวที่ใบนี้พิสูจน์)
**ผลสามท่อนของ GT-040 ตรวจซ้ำแบบปฏิปักษ์บนอิมเมจแล้ว "รอด" หรือ "ตาย" แถวไหนบ้าง** —
และปิดชิ้นที่ขาดชิ้นเดียวที่ท่อน B ระบุ (`0x402A20` -> ขอบเขตของ `[mgr+0x24]`) เพื่อดัน TENSION ไป 100%
🔴 **ทุกแถวที่ "ตาย" (ปฏิปักษ์หักล้างได้) มีค่าเท่าหรือมากกว่าทุกแถวที่ "รอด"** — จดเป็นผล ไม่ใช่ fail

### db
**ไม่ใช้ DB เลย** — ไม่แตะ canonical ไม่ทำสำเนา ไม่มีรอบเทสในเกม (กติกา stamp 420 นาที/teardown ไม่เกี่ยวกับใบนี้)

### server args
**ไม่มี** — ไม่บูตเซิร์ฟเวอร์ ไม่บูต client · เปิดอ่านอิมเมจอย่างเดียว

### สิ่งที่ต้องมี (precondition)
- **อิมเมจ:** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ไม่ต้องมี:** เซิร์ฟเวอร์ · client ที่บูตแล้ว · canonical DB · สำเนา DB · `LOCK_GAME` · teardown · boot stamp
- **ท่าทำงาน:** ตามวินัย `pf-static-re` · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative**
  (มันหยุดที่ไบต์แรกที่ decode ไม่ได้แล้วรายงาน negative อย่างมั่นใจ = ความผิดพลาดรอบ 83) · census ด้วย byte matching
  (`E8`/`E9 rel32` ทุกออฟเซ็ต · dword sweep ทั้งไฟล์สำหรับ table/vtable/immediate) · สวีปทั้งสอง exec section:
  `.text` (`0x00401000`, Vsize `0x00838A2C`) และ `.code` (`0x00C3A000`, Vsize เพียง `0x2E1` ไบต์)

### 🔴 กติกาข้อแรก — verify sha ของ span **ก่อน** re-derive
สำหรับทุกฟังก์ชันข้างล่าง: ตัดไบต์ตาม file offset ที่บันทึกไว้ แล้ว sha256 เทียบกับค่าที่จดหมายให้มา **ก่อน** เริ่ม decode
- **sha ของ span ตรง** ⇒ เดินซ้ำ decode บนไบต์ชุดนั้นได้
- 🔴 **sha ไม่ตรงแม้ตัวเดียว = หยุดทันที รายงานว่า span ไหนเพี้ยน ห้าม re-derive ทับ** (span เพี้ยน = ฐานผิด ทุกอย่างที่ต่อยอดไร้ค่า)

### span ที่ต้องตรวจ (จาก GT-040 A/B/C — จดหมายอยู่บน `main` แล้ว ผู้เทส push ผ่าน sync ก่อนรอบ R120:
`notes_to_chief\20260821_09{36,51,56}_GT040-PART-{A,B,C}-RESULTS-from-assistant.md`)

| ฟังก์ชัน | บทบาท | span VA `[start,end)` | file offset | len | sha256 ที่ต้องเจอ |
|---|---|---|---|---|---|
| `0x005E2960` | tag table บิต `0x04` / obj `+0x24` | `[0x005E2960,0x005E2AF6)` | `[0x1E1D60,0x1E1EF6)` | 406 | `259e551604b81fece3659d38f74be5f5a9148cbf44c9cc7d74c2301c995d8acc` |
| `0x005F85B0` | dirty-mask table บิต `0x08` / obj `+0x20` | `[0x005F85B0,0x005F8869)` | `[0x1F79B0,0x1F7C69)` | 697 | `ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b` |
| `0x00446F30` | generation-stamp reconcile (ลูป1+ลูป2) | `[0x00446F30,0x004470DE)` | `[0x046330,0x0464DE)` | 430 | `9c1157d3109c27c41783d6eed630a6eb46511ef6789a4e121306944ec1271d7d` |
| `0x005E5E30` | serializer ของ `PickupTerrainThing` (vtable `0x00F3005C` slot `+0x18`) | `[0x005E5E30,0x005E5E83)` | `[0x1E5230,0x1E5283)` | 83 | `8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066` |
| `0x005EF640` | handler สองทาง (slot `+0x1C`) | `[0x005EF640,0x005EF908)` | `[0x1EEA40,0x1EED08)` | 712 | `22da3ff4c2bcf8f7a006fab20d48f6ed5102617954cad3c68305c82480726c83` |

**span สนับสนุน (ตรวจ sha ด้วยถ้าจะพึ่ง):** `0x005F3490` (3 float · sha `b5f5a2063ff9...`) · `0x005E2630`/`0x005F82C0` (pool alloc)
· `0x00441C40` (removal จริง · sha `f7b9b6afd070...`) · `0x005E4060` (inbound handler · sha `85ff71ffceff...`)
· `0x0088F2B0` (`IsKindOf` comparator · sha `00076eb0d61b...`) · `0x005E46A0` (GetId · sha `d3fc621e95d5...`)
· `0x00BEE5E0` (registration · sha `8fa9ec1ebc0b...`)

### steps — สี่จ็อบ แยกผล อย่ารวม (ทำตามลำดับ 1 -> 2 -> 3 -> 4)

**จ็อบ 1 (แกน) — หักล้างตารางฟิลด์ของ `0x5E2960` และ `0x5F85B0`**
1. verify sha ของทั้งสอง span ก่อน (กติกาข้อแรก)
2. decode ใหม่จากศูนย์ **โดยไม่เปิดตารางเดิม** แล้วค่อยเทียบ · ต้องยืนยัน/หักล้างทุกแถว:
   - `0x5E2960`: หัว 4 แถว (`0x14`->`+0x10`/4 · `0x0B`->`+0x14`/1 · `0x0B`->`+0x18`/1 · `0x12`=จำนวนสมาชิก/2)
     + ลูปสมาชิก (`0x0B`->`elem+0x10`/1 · `0x2A`->`elem+0x14`/4) · ขนาดสมาชิก `0x18` จาก `push 0x18` ใน `0x5E2630`
   - `0x5F85B0`: หัว (`0x12`=`[obj+0x2C]`/2) + ต่อสมาชิก (`0x14`->`+0x10` เสมอ · `0x0B`->`+0x28`=mask เสมอ ·
     mask`0x02`->`0x14`/`+0x14` · mask`0x04`->`0x0F`/`+0x18` · mask`0x08`->`0x05`/`+0x1B` ·
     mask`0x10`->`0x2A`x3/`+0x1C,+0x20,+0x24` · mask`0x20`->`0x08`/`+0x1A`) · ขนาดสมาชิก `0x2C` จาก `push 0x2C` ใน `0x5F82C0`
3. หักล้างข้ออ้างสำคัญของท่อน A ให้ตรง: **bit `0x08`/`+0x20` พา record ที่มีพิกัดโลก (สาม float ที่ `+0x1C`) ที่ไม่ใช่ actor type 2..6**
   — ตรวจว่า record นี้ **ไม่** ผ่าน jump table `0x4469BD` และ **ไม่** อ้าง literal `0x00F3093C`/`0x00F0BAD0`
   (จดหมาย A ยืนยัน census `E8/E9` ในสองฟังก์ชันไม่แตะ terrain/ground เลย — เดินซ้ำเอง)

**จ็อบ 2 — หักล้าง generation-stamp reconcile ของ `0x446F30` (Part B)**
4. verify sha แล้ว decode ลูป1/ลูป2 ใหม่ · ยืนยัน/หักล้าง: `inc [mgr+0x04]` ที่ `0x446F37` ·
   ประทับ `[obj+0xD0]=[mgr+0x04]` ที่ `0x446FBE` · ลูป2 เก็บตัวที่ประทับแล้วหรือ `IsKindOf` ผ่าน · ที่เหลือเรียก `0x441C40` ถอดจริง
5. 🔴 **หักล้างข้ออ้างเชิงลบของจดหมาย B โดยตรง** (ข้ออ้างเชิงลบหักล้างง่ายที่สุดถ้ามันผิด): dword sweep เฉพาะช่วง
   `[0x046330,0x0464DE)` หา `0x01081A90` และ `0x01093198` — จดหมายอ้างว่า **0/0** (คือไม่ diff กับสำเนาเฟรมก่อนของ CHUNK2-Q2)
   ถ้าเจอแม้ครั้งเดียว = **ข่าวใหญ่ จดทันที** (พลิกคำวินิจฉัย TENSION)
6. ยืนยัน census ผู้เรียก: `0x446F30` ถูกเรียกจุดเดียว `0x5E4085` · `0x441C40` ถูกเรียกจุดเดียว `0x4470B2`
   (สแกน `E8/E9 rel32` ทั้ง `.text` เอง — ถ้าเจอผู้เรียกตัวที่สอง gate ที่คิดว่าปิดอาจไม่ปิด)

**จ็อบ 3 (ชิ้นที่ขาด — ดัน TENSION ไป 100%) — decode `0x402A20`**
7. `0x402A20` คือฟังก์ชันที่ค่า return กลายเป็น `mgr` (`ecx`) ของ `0x446F30` — เรียกที่ `0x5E407E` โดยอาร์กิวเมนต์ = `[esi+0x1C]+0x10`
   (sub-object ของ derived bit `0x02`) · จดหมาย B เตือนว่า **มี SEH ไม่ใช่ getter สั้น ๆ** จึงยังไม่มีใครเปิด
8. ตอบคำถามเดียวของจ็อบนี้: **`[mgr+0x24]` (ลิสต์ที่ลูป2 กวาด) ครอบคลุมประชากรอะไร** —
   scene-load population ทั้งหมด · หรือเฉพาะ actor-entry ของเฟรมล่าสุด · หรือ subset อื่น
   นี่คือชิ้นเดียวที่กั้นไม่ให้ปิด TENSION 100% และเป็นตัวตัดสินความเป็นไปได้ (ข) ของ GT-043 ล่วงหน้า
9. แนบ span `[start,end)` + file offset + len + sha256 ของ `0x402A20` (และทุกฟังก์ชันใหม่ที่อ้าง) แบบเดียวกับจดหมายเดิม

**จ็อบ 4 (ของแถมถ้าเหลือเวลา) — สามบิตที่ว่าง `0x01`/`0x40`/`0x80` ของ mask ใน `0x5F85B0`**
10. จดหมาย A อ้างว่าสามบิตนี้ **ไม่เคยถูก test เลยทั้งขาเขียนขาอ่านในฟังก์ชันนี้** · ตรวจว่า **ที่อื่นในอิมเมจ**
    มีจุดไหน test บิตเหล่านี้ของ byte `[member+0x28]` หรือไม่ (ถ้ามี ⇒ mask มีความหมายมากกว่าที่ decode ในฟังก์ชันเดียว — จด)
    🔴 ถ้าเวลาไม่พอ **ข้ามจ็อบนี้ได้ ไม่กระทบการปิดใบ** — จ็อบ 1-3 คือแกน

### pass criteria — **สองชั้น แยกกันเด็ดขาด**

**ชั้น ① wire/DB (ไบต์+ดิสแอสเซมบลี — headless ล้วน ไม่ต้องมีคนเฝ้าจอ)**
ใบนี้ผ่านเมื่อครบทั้งสองส่วนนี้:
- **(layer 1a — ราย row) ทุกแถวของสามตารางแกน** (`0x5E2960` · `0x5F85B0` · `0x446F30`) และตารางฟิลด์ของ `0x5E5E30`
  ถูก **ยืนยันหรือหักล้างทีละแถวด้วยหลักฐานไบต์ที่ file offset ที่บันทึกไว้** — ไม่ใช่ "อ่านผ่านแล้วเหมือนเดิม"
  ต้องเห็น sha ของทุก span (verify ก่อน) และไบต์จริงของแถวที่ตัดสิน
- **(layer 1b — บัญชีรอด/ตาย) รายการชัดเจนสองคอลัมน์:** ข้ออ้างของ GT-040 **ตัวไหนรอดการตรวจปฏิปักษ์ · ตัวไหนตาย**
  โดยเฉพาะสี่ข้ออ้างเสาหลัก: (i) bit `0x08` พา record มีพิกัดที่ไม่ใช่ actor · (ii) reconcile ใช้ generation stamp ไม่ diff สำเนา
  (ข้ออ้างเชิงลบ `0x01081A90`/`0x01093198` = 0/0) · (iii) เฟรม count-1 กวาดจริงแต่มี gate ที่ `[res+0x1C]` (`0x5E4078 je`) ·
  (iv) vtable `0x00F3005C` -> serializer `0x5E5E30` / handler สองทาง `0x5EF640`
- **จ็อบ 3 ต้องตอบเป็นประโยคเดียวได้:** `[mgr+0x24]` ครอบคลุม `<...>` พร้อม span+sha ของ `0x402A20`
  **ถ้า static ตัดสินขอบเขตนี้ไม่ได้** (เช่นจบที่ lookup รันไทม์อย่างที่ descriptor `0x0102CB04` เป็น) ⇒ **พูดตรง ๆ ว่าตัดสินไม่ได้**
  และระบุว่าเหลือทางเดียวคือ GT-043 (attended) — **นั่นคือผลที่สมบูรณ์ ไม่ใช่ fail**
- ทุกจ็อบ: **sha256 ของอิมเมจก่อน-หลัง ต้องตรงกัน** · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น ② client-observable (ต้องมีคนอยู่หน้าจอเกม)**
🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้แม้แต่ชิ้นเดียว และห้ามใครอ้างชั้น ① เป็นหลักฐานของชั้น ②**
ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**
**สิ่งที่ผลบวกจะไปปลดล็อก (ยังไม่ใช่ตอนนี้):** เมื่อสามท่อนรอดการตรวจ ⇒ ปลดล็อก **สิทธิ์เขียนโมดูล/encoder** (ก่อนหน้านี้ห้าม)
และจ็อบ 3 ป้อนคำตอบขอบเขต `[mgr+0x24]` ให้ GT-043 ตีความผลบนจอได้

### 🔴 ผลลบมีค่าเท่าผลบวก — เขียนไว้ล่วงหน้า
- **ถ้าทุกแถวรอด** ⇒ GT-040 ผ่านการตรวจปฏิปักษ์ · ปลดล็อกสิทธิ์เขียนโค้ด (ยังไม่ใช่คำสั่งให้เขียน)
- **ถ้ามีแถวตาย** ⇒ ระบุแถว + ไบต์ที่หักล้าง + ผลกระทบ (เช่น ถ้า gate `0x5E4078` ไม่มีจริง TENSION พลิก · ถ้า `0x01081A90` โผล่ คำวินิจฉัย diff พลิก)
  ⇒ cc ลง erratum · **ห้ามเขียนโค้ดจาก span ที่เกี่ยวข้องกับแถวที่ตายจนกว่าจะ decode ใหม่**
- **ถ้า `0x402A20` ตัดสินขอบเขตด้วย static ไม่ได้** ⇒ ส่งไม้ต่อให้ GT-043 อย่างเป็นทางการ · TENSION ค้างที่ <100% อย่างมีเหตุผลระบุตัวได้

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ claim ว่าอะไรก็ตามที่เจอ ถูกส่งจริงโดยเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว ไม่เคยเผยแพร่ และกู้ไม่ได้ตลอดกาล ·
  **การประกอบ/ตีความของเราไม่ใช่ของเซิร์ฟเวอร์เดิม ซึ่งกู้ไม่ได้**
- **ไม่ claim ว่ามีอะไรเรนเดอร์บนจอ** — ทั้งใบเป็นชั้น ① ล้วน · การมี serializer/vtable ในอิมเมจ **ไม่พิสูจน์ว่าคลาสถูกสร้าง ถูก register หรือเคยขึ้นสาย**
- **ไม่ claim ว่ารู้ชื่อคลาสของ record บิต `0x08` หรือคลาสที่ `IsKindOf` ยกเว้น** — สอง vtable ไม่มี RTTI/name literal ·
  descriptor `0x0102CB04` เป็นศูนย์ในไฟล์ (สร้างตอนรัน) · **ห้ามเดาชื่อ = ห้ามประดิษฐ์ wire format**
- **ไม่ claim ว่ารู้ความหมายของ tag** — ยืนยันได้แค่ len (`0x2A`=float32/4 · `0x12`=uint16/2 · ที่เหลือรู้แค่ len)
- **ไม่ claim ว่า derived id `0x4543` ถูก** — id จริงมาจาก `0x89BD00` รันไทม์เก็บใน `ds:0x0108202C` ซึ่ง `.data` เป็นศูนย์ในไฟล์ ⇒ static พิสูจน์เลข id ไม่ได้
- **ไม่รื้อ** [NEGATIVE] ของ jump table `0x4469BD` (actor_type 2..6) — ปิดแล้ว
- ไม่แตะ DB · ไม่แตะเกม · ไม่แตะ `LOCK_GAME` · **ไม่มีดีไซน์/โมดูล/ข้อเสนอ wire ในผลของใบนี้** (ถ้าผลกลับมาพร้อมดีไซน์ = ทำเกินใบสั่ง ตัดทิ้ง)

- **result:** (ผู้รับงาน static บนสะพานกรอก: บัญชีรอด/ตายรายแถว + ไบต์ที่ตัดสิน + คำตอบขอบเขต `[mgr+0x24]` + span/sha ของ `0x402A20`
  + เวลา + sha อิมเมจก่อน-หลัง · ⏳ ถ้าเดินซ้ำแล้ว span sha ไม่ตรง = หยุดตรงนั้น รายงาน span ที่เพี้ยน ห้าม re-derive ทับ)


## 🆕⭐ GT-043 POP-SURVIVAL-001 [attended, ของแถมสังเกตล้วน]: หลังยิงเฟรม count-1 บิต `0x02` แล้ว NPC/วัตถุตัวอื่นในโลก "หายไหม"  [✅ **PASS-PERSISTENT-SURVIVAL / subsecond-unobserved — 2026-08-23 01:50 (+07:00): ไม่พบ NPC/วัตถุที่ติดตามหายแบบค้าง · ช่วง 0–3.524s ห้ามสรุป**]

> ✅ **RESULT 2026-08-23 01:33–01:50 (+07:00) — PASS-PERSISTENT-SURVIVAL** (host lane HYP-PF-027 · เฟรม `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` 1×190 B ออกจริง):
> - หลังเฟรม count-1 bit `0x02`: Navy Transfer + landmark ฉาก (เรือ/โคม/เสา/โซ่) **ยังอยู่ครบ** ในภาพมุมเดิม +3.524..+9.978s และหลังแพน P2
> - 🔴 qualification: เครื่องมือจับภาพให้ภาพแรกช้า +3.524s แม้ขอ 0ms ⇒ **ปิดได้เฉพาะ "ไม่มีการหายแบบค้าง" — transient ต่ำกว่านั้น = non-observed**
> - ⭐ side-note ตอบ GT-032: **เส้นแดง/target panel เกิดหลัง Tab-select ไม่ใช่จาก hostility frame เพียงอย่างเดียว** (ภาพก่อน/หลัง Tab แยกกัน · target HP 100/100 Lv.1)
> - รอบ partial ก่อนหน้า (00:30 ใบ GT-030/043) นับเป็นหลักฐานเสริม ไม่ใช่ตัวปิด · รอบแรกคืนนี้ (boot 1012) ยกเลิกก่อน trigger — ไม่มี label ออก
> - ผลเต็ม: `notes_to_chief/20260823_0156_GT043-PASS-PERSISTENT-SURVIVAL-subsecond-unobserved.md` (บริโภค R123)

**ที่มา:** GT-040 ท่อน B decode ว่า **เฟรม `0x6E9D` ขาเข้าที่พา derived bit `0x02` (actor-entry collection) จะ trigger reconcile เต็ม**:
ทุกอ็อบเจกต์ใน `[mgr+0x24]` ของ client ที่ **ไม่อยู่ใน entry list ของเฟรมนั้น และไม่ผ่าน `IsKindOf` ที่ยกเว้น** จะถูกถอดจากทะเบียนกลางในการเรียกเดียวกัน
เลนที่พิสูจน์แล้วของเรา (HYP-PF-023/025/027 เช่น `HOSTILE_SPAWN` ของ GT-032) ส่งเฟรมแบบนี้ด้วย **count 1 เป๊ะ**
แต่ **ไม่เคยมีใครรายงานว่าประชากรถูกกวาด** (และไม่เคยมีใคร assert ว่าไม่ถูกกวาด — คือไม่เคยมีใครดู)
ท่อน B ทิ้งความเป็นไปได้สามข้อที่ตัดสินไม่ได้ด้วย static: **(ก)** เฟรมเราไม่ได้เดินเข้า path นั้นจริง ·
**(ข)** ประชากร scene-load ไม่ได้อยู่ใน `[mgr+0x24]` · **(ค)** ไม่เคยมีใครดูผลหลังยิงจริง
🔴 **ใบนี้ปิดข้อ (ค) ด้วยวินัยการสังเกตล้วน — ศูนย์โค้ดใหม่ ศูนย์ flag บูตใหม่** แนบเข้ากับเลนที่ยิงอยู่แล้ว

### objective (claim เดียว)
**หลังยิงเฟรม count-1 ที่พาบิต `0x02` หนึ่งเฟรม NPC/วัตถุตัวอื่นที่อยู่ในโลกก่อนหน้า "หายจากโลก/เรดาร์" หรือไม่**
🔴 **ทั้งสองผลชี้ขาด:** **หาย** = reconcile ทำงาน live กับประชากรฉากจริง (ใหญ่มาก — ทุกเฟรม count-1 ในอนาคตเป็น destructive) ·
**ไม่หาย** = ประชากร scene-load อยู่นอก `[mgr+0x24]` หรือได้รับการยกเว้น (จำกัดกรอบดีไซน์ loot-despawn ทั้งหมด)

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
- ใช้ **db และ args ของเลนเจ้าบ้านที่แนบไป** เป๊ะ (GT-030 rerun หรือ GT-032-family) — **ใบนี้ไม่เพิ่ม flag ไม่เปลี่ยน args แม้ตัวอักษรเดียว**
- เทียบ sha256 canonical กับ `CANON_SHA.txt` ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง

### server args (เป๊ะ)
**= args ของเลนเจ้าบ้าน** (เช่น `--npc-hostile-hypothesis-scenario scenarios\npc_hostile_hypothesis_faction_pairing.json` สำหรับตระกูล GT-032
หรือ scenario ของ GT-030 rerun) + `--db` สำเนาตามปกติ · ไม่มีอะไรใหม่
🔴 **แนบกับเลนไหน ให้ยืนยันก่อนว่าเฟรมของเลนนั้นเป็น count-1 บิต `0x02` จริง** (GT-032 `HOSTILE_SPAWN` = ใช่ · GT-030 actor_type 2 = ใช่)
เลนที่ไม่พาบิต `0x02` **ไม่เข้าข่ายใบนี้** (ตาม gate `0x5E4078 je` ที่ท่อน B เจอ — ไม่มีบิต `0x02` = ไม่แตะประชากรเลย)

### 🔴 อ่านก่อน — ท่ามาตรฐานอินพุตของรอบใหญ่ #12
- **ปุ่ม/ช่องแชตคลิกสังเคราะห์ไม่ติดเป็นช่วง ๆ · `Return` ใช้ได้เสมอ** ⇒ ท่า: `Return` -> พิมพ์ -> `Return`
- trigger แชต = **ascii 12 ตัวเป๊ะ** (สั้นกว่านั้นถึงเซิร์ฟแต่ไม่เข้าเงื่อนไข เงียบ ไม่มี sweep) · ตัวอักษรตอนช่องไม่โฟกัส = hotkey
- เปิด server ก่อน client เสมอ · การ์ด `Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client

### steps (แนบเข้ากับการยิงเฟรมของเลนเจ้าบ้าน — เพิ่มแค่การถ่ายภาพรอบการยิง)
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · ทำสำเนา DB ตามเลนเจ้าบ้าน
1. บูตตามเลนเจ้าบ้านจนเข้าแมพ (server -> client -> เลือกตัว -> เข้าเกม ด้วย `Return`)
2. เดินให้ **NPC/วัตถุอื่นหลายตัว** อยู่ในเฟรมกล้องพร้อมกับเป้าของเลนเจ้าบ้าน — เลือกมุมที่เห็น landmark หลายตัว (เช่น NPC ประจำแมพรอบจุดเกิด Port Royal)
3. 🔴 **BEFORE — ถ่ายชุดหลักฐานก่อนยิง:**
   - ภาพ **P0** = ภาพรวมมุมกล้องเห็น NPC/วัตถุอื่นหลายตัว (นับจำนวน จดตำแหน่ง/ชื่อที่อ่านได้)
   - **เฟรมทีละตัว:** คลิก/Tab เลือก NPC อื่นแต่ละตัวที่เห็น ถ่ายแผง target ให้เห็นว่า "มีตัวตนก่อนยิง" (P0a, P0b, ...)
   - เปิดเรดาร์/มินิแมพถ้ามี ถ่ายให้เห็นจุดของตัวอื่น (P0r)
4. **ยิงเฟรมของเลนเจ้าบ้าน** (แชต ascii 12 ตัว -> sweep 1 เฟรม) · ยืนยัน console เห็น label ของเลนนั้นออก 1 เฟรม
5. 🔴 **AFTER — ถ่ายชุดเดียวกันจากมุมเดิมเป๊ะ:**
   - ภาพ **P1** = มุมเดิม นับ NPC/วัตถุอื่นที่ยังเหลือ เทียบกับ P0
   - เฟรมทีละตัวซ้ำ NPC ชุดเดิม (P1a, P1b, ...) — ตัวไหนคลิก/Tab ไม่ขึ้นแผงแล้ว = ผู้ต้องสงสัยว่าหาย
   - เรดาร์/มินิแมพ (P1r) เทียบจุด
6. **เดิน/แพนกล้องยืนยัน:** เดินเข้าหาจุดที่ NPC อื่นเคยยืน (จาก P0) ถ่าย **P2** — ถ้าตัวนั้นหายจริง ต้องหายทั้งจากภาพและจากการเดินเข้าไปใกล้ (กันกรณี culling ระยะไกล)
7. **โน้ตข้ามใบจาก GT-032 (เก็บพร้อมกัน ประหยัดรอบ):** ที่เป้าของเลนเจ้าบ้านเอง **ถ่ายหลังยิงแต่ก่อนกด Tab หนึ่งภาพ (P-tab-before)** แล้วค่อยกด Tab ถ่าย (P-tab-after)
   — เพื่อแยก "เส้นขอบแดงจาก hostility" ออกจาก "เส้นขอบจากการเลือกเป้า" ที่ GT-032 ค้างไว้
8. ออกจากเกมตาม PLAYBOOK -> ปิด server เก็บ raw GAME log + console -> `PRAGMA integrity_check;`
9. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 · `TEMPLATE_teardown_generic.ps1:135`)
10. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด

**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ)** — เก็บเพื่อพิสูจน์ว่า "เฟรมออกไปจริง" (ถ้าไม่ออก การไม่หายไม่มีความหมาย):
- raw GAME log เห็นเฟรมของเลนเจ้าบ้านออก **1 เฟรม** (label ถูกต้อง · ขนาดตรงดีไซน์ของเลนนั้น · ไม่มี `compose_refused`/`already_sent`/refusal)
- ไม่มี `ErrorData=28317` · `PRAGMA integrity_check` = `ok` · sha canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** NPC ตัวอื่นหายหรือไม่ (การถอดจากทะเบียนกลางไม่พิมพ์อะไรใน log ฝั่งเซิร์ฟเวอร์ — ท่อน B nonclaim ข้อ 1) ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)** — คือหัวใจของใบนี้:
- ชุดภาพ **P0/P0a../P0r (ก่อน)** และ **P1/P1a../P1r (หลัง)** จากมุมเดิม + **P2 (เดินยืนยัน)** ครบ อ่านได้
- ตอบข้อเดียวเป็นภาษาคน: **NPC/วัตถุตัวอื่น (ที่ไม่ใช่เป้าของเลน และไม่ใช่ผู้เล่นเอง) หายจากโลก/เรดาร์หลังยิงหรือไม่ · ถ้าหาย หายกี่ตัว ตัวไหน**
- เก็บ **P-tab-before / P-tab-after** ของเป้าเลนเจ้าบ้าน (โน้ต GT-032)
- **ชั้นนี้ตอบไม่ได้:** ทำไมถึงหาย/ไม่หาย (เป็นข้อ ก/ข/ค ของท่อน B ซึ่ง static ต้องปิด — ดู GT-042 จ็อบ 3) · **ภาพหน้าจอไม่ใช่หลักฐานของการถอดทะเบียนระดับไบต์ ห้ามอ้างข้ามชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
1. **มีตัวอื่นหาย** ⇒ **ข่าวใหญ่ที่สุดของใบนี้** — reconcile ทำงาน live กับประชากรฉาก ⇒ ทุกเฟรม count-1 บิต `0x02` ในอนาคตเป็น destructive
   ⇒ หยุด เก็บวิดีโอ/ภาพช่วงยิง + console + raw GAME log ทั้งไฟล์ · เลนที่ยิงเฟรมแบบนี้ทั้งหมดต้องทบทวนใหม่
2. **ไม่มีตัวไหนหายเลย** ⇒ **ผลเต็มใบเท่ากัน** — ประชากร scene-load อยู่นอก `[mgr+0x24]` หรือได้รับการยกเว้น `IsKindOf`
   ⇒ ตัดความเป็นไปได้ (ก) ของท่อน B ทิ้ง เหลือ (ข) เป็นคำอธิบายหลัก · จำกัดกรอบดีไซน์ loot-despawn (ลูทที่โผล่จะไม่โดนกวาดโดยเฟรม actor ปกติ)
   ⇒ ส่งไม้ต่อให้ GT-042 จ็อบ 3 ยืนยันขอบเขต `[mgr+0x24]` ฝั่ง static

### เกณฑ์หยุด
- NPC ตัวใดตัวหนึ่งหายทันทีหลังยิง = หยุด เก็บภาพ/วิดีโอ + console ทั้งไฟล์ + raw GAME log
- `ErrorData=28317` = หยุด เก็บ console ทั้งไฟล์ (การสลับสองสายพานในเซสชันเดียวพัง)
- ชื่อเกณฑ์หยุดของเลนเจ้าบ้านโผล่ (เช่น `ProbeControl03` ของ GT-030) = ปฏิบัติตามเกณฑ์หยุดของเลนนั้นก่อน

### nonclaims (ติดไปกับผลทุกกรณี)
- **การประกอบเฟรม/faction/สูตรของเลนเจ้าบ้านเป็นดีไซน์ของเรา ไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล**
- **ไม่ claim ว่า "ถอดจากทะเบียน" = "หายจากจอ"** ในทางกลับกันด้วย — ใบนี้วัดสิ่งที่ตาเห็นเท่านั้น · การเชื่อมไปถึงไบต์ `[mgr+0x24]`/`0x441C40` เป็นงานของ GT-042 (static)
- **ไม่ claim ว่ารู้ว่าทำไมหาย/ไม่หาย** — ข้อ ก/ข/ค ตัดสินด้วยใบนี้ใบเดียวไม่ได้ ต้องคู่กับ GT-042
- **ไม่ใช่ combat/aggro/persistence** — ไม่มี NPC โจมตี ไม่มี HP write path · เลนเจ้าบ้านพิสูจน์สิ่งของมันเอง ใบนี้พ่วงการสังเกตประชากรเท่านั้น
- **ไม่ claim ว่า "ของลูทบนพื้น" มีอยู่จริงในเกม** — record บิต `0x08` ที่ท่อน A เจอยังไม่พิสูจน์ว่าเรนเดอร์ · ใบนี้ไม่แตะเรื่องนั้น
- **แถว coverage ไม่ขยับไม่ว่าใบนี้ออกหัวหรือก้อย** — เป็นการสังเกตพ่วง ไม่เปิด/ปิดรอบเทสด้วยตัวเอง

- **result:** (ผู้เทสกรอก: เลนเจ้าบ้านที่แนบ + label เฟรมที่ออก + ชุดภาพ P0../P1../P2 + P-tab-before/after พร้อม sha256 ทุกใบ
  + คำตอบ "ตัวอื่นหายไหม กี่ตัว" เป็นภาษาคน + เวลา + sha canonical ก่อน-หลัง + path raw GAME log)

## 🆕🔬 GT-044 SCENEID-BG0001-001 [STATIC-ON-BRIDGE]: dump SCENE_NAME (ตาราง 007) + MAP_SCENE_LIST (ตาราง 101) จาก `B_CONSTDATA_TH.pc_.dec` — ปิดเลข scene id เชิงตัวเลขของ bg0001  [✅ **PASS — 2026-08-23 02:07 (+07:00): `BG0001` = numeric scene id `1` ตรงกับที่ lane scene_load ส่งอยู่**]

> ✅ **RESULT 2026-08-23 02:03–02:07 (+07:00) — PASS** (source read-only · SHA ก่อน/หลังตรง):
> - `SCENE_NAME` (007) แถว index 0: `n_ID = 1` · `s_MODLE_ID = BG0001` · `s_SCENE_NAME = 皇家港` · `s_IMAGENAME = Bg0001_air` ⇒ **mapping ตรงจากตารางเดียว ไม่พึ่ง numeric coincidence**
> - dump เต็มสองตาราง: `outbox/GT044_SCENE_NAME_007.tsv` (271 แถว) + `GT044_MAP_SCENE_LIST_101.tsv` (15 แถว)
> - 🔴 ข้อห้ามที่ได้มาด้วย: **ห้าม join `MAP_SCENE_LIST.n_ID=1` กับ `SCENE_NAME.n_ID=1` เพียงเพราะเลขเท่ากัน** — ไม่มี crosswalk field พิสูจน์ · namespace แยกกัน
> - nonclaim: พิสูจน์ mapping ใน client data เท่านั้น ไม่พิสูจน์ว่า runtime ใช้เลขนี้อย่างไร · ไม่เปลี่ยนผล GT-034
> - ผลเต็ม: `notes_to_chief/20260823_0207_GT044-PASS-bg0001-scene-id-1.md` (บริโภค R123) ⇒ nonclaim `scene_id_numeric_provenance` ของ GEO-PF-006 **ปิดที่ชั้น client-table แล้ว**

**ที่มา:** รอบ 122 ยืนยันโซนให้ GT-034 ได้สูงสุดแค่ระดับ **file-membership** (P0 กับ P30 เป็นแถวของตาราง frozen
`PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` 115 แถวเดียวกัน ที่ derive จาก `bg0001_npc_placements_decoded.tsv`) —
**เลข scene id เชิงตัวเลขของ bg0001 ไม่เคยถูก dump** เพราะสองตารางนี้อยู่ในอิมเมจที่เข้าถึงได้จากเครื่องสะพานเท่านั้น
(จดคำขอลง `IMAGE_ACCESS_COST.tsv` แล้วรอบ 122)

- **objective:** พิสูจน์หนึ่งข้อ: **scene id เชิงตัวเลขของ bg0001/Port Royal ตาม client tables คือเลขอะไร** —
  และเลขนั้นตรงกับ `scene_id: 1` ที่เลน scene_load ส่งอยู่หรือไม่
- **แหล่ง (อ่านอย่างเดียว ห้ามแก้อิมเมจ · จด sha อิมเมจก่อน-หลัง):**
  `Pirate Force ServerProject/backups/v103_one_item_backpack_20260814_103143/derived/v97_mapping_audit/B_CONSTDATA_TH.pc_.dec`
  - ตาราง **007 SCENE_NAME**: offset `0x0000B3D4-0x0001D148` · 271 แถว x 24 คอลัมน์
  - ตาราง **101 MAP_SCENE_LIST**: offset `0x007F9580-0x007FA044` · 15 แถว x 15 คอลัมน์
  - (offsets จาก `FACTPACK_R100_CONSTDATA_MONSTER_LOOT.md` หัวข้อดัชนีตาราง · เครื่องมือ: `parse_pc_tables.py` ตัวเดิมที่ใช้ parse STANDARD_MOB)
- **steps:** ① parse สองตารางเป็น TSV เต็มทุกแถวทุกคอลัมน์ ② หาแถวที่ผูกกับ bg0001 / Port Royal
  (ชื่อไฟล์ฉาก, ชื่อแสดงผล, หรือ mapping ใน MAP_SCENE_LIST) ③ จดเลข id + เส้นทางการ join ที่ใช้หาให้ re-derive ได้
- **pass criteria:**
  - **ชั้น static (ชั้นเดียวของใบนี้ — ไม่มีชั้น client-observable):** TSV dump ครบสองตาราง + sha256 ของ TSV +
    คำตอบชี้ขาด: bg0001 = scene id เลขอะไร · ตรง/ไม่ตรงกับ `1` ที่เลนส่ง
  - **ผลลบมีค่าเท่าผลบวก:** ถ้าสองตารางไม่มี mapping ที่ resolve ได้ = จดเป็นผล ("ตอบจาก tables ชุดนี้ไม่ได้") —
    คาเวียตใน GT-034 คงอยู่ต่อไปตามเดิม ไม่มีใครต้องรันอะไรซ้ำ
- **ผลต่อใบอื่น:** ยกระดับคำตอบ "แมพเดียวกัน" ของ GT-034 จาก file-membership เป็นเลขตัวเลข ·
  **ไม่บล็อกและไม่ปลดบล็อกการรัน GT-034** — GT-034 รันได้ก่อนใบนี้ปิด (คาเวียตแมพ/โซนในใบนั้นรองรับแล้ว)
- **nonclaims:** ตารางทั้งสองเป็นข้อมูลที่ ship มากับ client — ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล ·
  ไม่พิสูจน์ว่า client *ใช้* เลขนี้ที่ runtime ตอนตัดสินใจโหลดฉาก — พิสูจน์แค่ mapping ในไฟล์ข้อมูล
- **result:** (ผู้รับงาน static บนสะพานกรอก: เลข id + เส้นทาง join · path TSV + sha256 · sha อิมเมจก่อน-หลัง · เวลา)


## 🆕⭐ GT-045 GROUNDDROP-RENDER-001 [attended, in-game]: บิต `0x08` ของ `0x5F85B0` คือ "วัตถุลูทบนพื้น" ไหม — ยิงเรคคอร์ดที่มีพิกัดโลกเข้าไปแล้วดูว่าไคลเอนต์วาดอะไร  [🟡 **BLOCKED-รอ-merge — เลนสร้างแล้ว (R124 · HYP-PF-032 GROUND-LOOT-001) · รอ gate เขียว + merge เข้า `main` ก่อนบูต** · สิทธิ์เขียน encoder จาก span นี้ปลดแล้วโดย GT-042 PASS (R123)]

**ที่มา:** ร่างผู้ช่วย `notes_to_chief\20260823_0805_GT-TICKET-DRAFT-ground-drop-and-pickup-direction.md`
(อ่านคู่กับหลักฐานวัดเฟรม `notes_to_chief\20260823_0800_GROUND-DROP-FRAME-MEASUREMENT-pickup-is-not-contact.md`)
การวัดเฟรมพิสูจน์แล้วว่า: ของโผล่บนพื้นเป็นวัตถุ 3 มิติ + ป้ายชื่อลอย อยู่ 0.633 s แล้วหาย · ตอนหายไม่มีใครแตะ ·
ของหาย + บรรทัด `ได้รับ [Red leaves Hammer] * 1` เกิดเฟรมเดียวกัน ⇒ คำถามเดิม "เดินทับ/กดปุ่ม" ตายทั้งคู่
ใบนี้ตอบคำถามที่แคบลง: **ไคลเอนต์รับเรคคอร์ดบิต `0x08` แล้ววาดของบนพื้นออกมาไหม**

### 🟡 สถานะ BLOCKED-รอ-merge (อัปเดต R124 — เหลือข้อเดียว)
1. ✅ **เลนเซิร์ฟเวอร์สร้างแล้ว (R124):** HYP-PF-032 GROUND-LOOT-001 — flag จริงคือ
   `--ground-loot-hypothesis-scenario` · scenario จริงคือ `scenarios/ground_loot_hypothesis_bit08_render.json`
   (ชื่อที่เสนอไว้เดิม `groundloot-render-...`/`groundloot_render_...bit08.json` **เลิกใช้** — เปลี่ยนตาม house convention)
   ดีไซน์ที่ลงจริง: **สองเฟรม เฟรมละหนึ่ง element** (ใกล้ก่อน แล้วไกลตามใน 0.10 วินาที) ออกอัตโนมัติที่
   TargetPos แรกหลัง runtime ack ครั้งเดียวต่อเซสชัน — ผู้เทสไม่ต้องกดอะไรเพื่อยิง
   (เฟรมละ element เดียวโดยเจตนา: V43 เคยวัดจริงว่า collection หลาย record ในเฟรมเดียวทำ client ยิง
   `ErrorData=28317` — adversary ของ R124 จับดราฟต์ count=2 ได้ก่อน commit) ·
   element mask `0x12` (`0x10` พิกัด + `0x02` dword `2600001`)
   พิกัดใกล้ = จุดเกิด +30X `(-9209.95703125, -2830.045166015625, 223.29209899902344)` ·
   พิกัดไกล = จุดเกิด +800X `(-8439.95703125, -2830.045166015625, 223.29209899902344)`
2. 🔴 **ยังต้องรอ: gate เขียว + merge เข้า `main`** — เหมือน GT-034/GT-041 (บูตคำตัดสิน ไม่ใช่ branch)
✅ เงื่อนไขที่สามเดิม (GT-042 ต้อง PASS เพื่อปลดสิทธิ์เขียน encoder) **ครบแล้ว** — GT-042 PASS 2026-08-23 (+erratum handler len 47) · สิทธิ์ปลดเฉพาะแถวที่รอด re-derive ซึ่งรวม `0x5F85B0` ทั้งตาราง
🔴 **ปล่อยใบนี้ไว้ที่เดิม ห้ามลบ ห้ามย้าย** จนกว่า merge จะเกิด · ถ้าใครเปิดคิวมาเจอใบนี้ยัง BLOCKED-รอ-merge = เช็ค resolver ก่อน ถ้าได้ commit ที่มีเลนนี้ = ถึงคิวมันแล้ว

### สมมติฐาน (จาก GT-040 ท่อน A · เฉพาะตารางฟิลด์ของ `0x5F85B0` ผ่าน re-derive ปฏิปักษ์ใน GT-042 — VA ประกอบอื่น (`0xF313C4`/`0x5F34D0`) มาจาก GT-040 ยังไม่ผ่านปฏิปักษ์ · verify sha ก่อนพึ่งเสมอ)
`0x5F85B0` (บิต `0x08` / obj `+0x20`) = list แบบ dirty-mask · element ยาว `0x2C` ไบต์ · vtable `0xF313C4`
float 3 ตัวที่ `+0x1C/+0x20/+0x24` = ตำแหน่งในโลก (เขียนผ่าน `0x5F3490` / อ่านผ่าน `0x5F34D0`)
mask: `0x02`->`+0x14` tag `0x14` · `0x04`->`+0x18` tag `0x0F` · `0x08`->`+0x1B` tag `0x05` · `0x10`->ตำแหน่ง · `0x20`->`+0x1A` tag `0x08`

### objective (claim เดียว)
**เมื่อเซิร์ฟเวอร์ส่ง element ของ `0x5F85B0` (mask `0x10|0x02`) ที่พิกัดใกล้ตัวผู้เล่น ไคลเอนต์วาดป้ายชื่อ/โมเดลบนพื้นที่จุดนั้นหรือไม่**
(ดีไซน์จริง R124: สองเฟรม เฟรมละหนึ่ง element — ใกล้ +30X และไกล +800X ห่างกัน 0.10s — เพื่อแยก "ไม่วาด" จาก
"วาดนอกจอ" · เฟรมละ element เดียวตามบทเรียน V43 กัน `ErrorData=28317` จาก collection หลาย record)

### คำทำนาย (คำทำนายที่ผิด = ผล ไม่ใช่ความล้มเหลว)
- **P1 — ถ้าสมมติฐานถูก:** จอขึ้นป้ายชื่อสีขาวลอยเหนือพื้น และ/หรือ โมเดลชิ้นเล็กวางบนพื้น ที่พิกัดที่ยิง
- **P2 — ถ้าไม่วาดอะไรเลยทั้งสองพิกัด:** บิต `0x08` ไม่ใช่ช่องของวัตถุบนพื้น ⇒ ตัดตัวต้องสงสัยนี้ทิ้งถาวร (ดู "ผลลบ")

### 🔴 ก่อนบูต — resolve commit เขียว (ท่าเดียวกับ GT-041/GT-034 · รันเครื่องมือ ไม่ใช่ก๊อป SHA)
```
py -3 pf_resolve_green_boot.py --repo C:\path\to\pirate-force-server --fetch
```
- รันจากโฟลเดอร์ `pf_bridge` · **exit 0** + `BOOT_COMMIT: <sha>` ⇒ `git checkout <sha>` (detached HEAD ถูกแล้ว)
- **exit 3** + `BOOT_COMMIT: NONE` ⇒ ห้ามบูต จดว่า "ใบนี้รอ gate ไม่ได้รอผู้เทส" · **exit 2** = พาธผิด/git ล้ม
- 🔴 บรรทัด `THE GATE JUDGED ... AS FAILED` ⇒ จดลงผลเสมอ
- **ยืนยันสามข้อกับ `<SHA>` ที่จะบูตจริง (ต้องครบสามข้อ · flag/scenario ชื่อจริงตามที่ chief ตั้งตอนสร้างเลน):**
```
git show origin/ci-status:ci/<SHA>.json
git grep -n "ground-loot-hypothesis-scenario" <SHA> -- src/pirateforce_foundation/app.py
git cat-file -e <SHA>:scenarios/ground_loot_hypothesis_bit08_render.json && echo SCENARIO_PRESENT
```
1. ไฟล์คำตัดสินมี `"conclusion": "success"` และ `"sha"` ตรงชื่อไฟล์ (`success` = subset บน Actions ไม่ใช่ gate เต็ม)
2. `git grep` เจอ flag จริง — **ห้ามใช้ `--help` เป็นหลักฐาน** (คืน 0 บรรทัดผ่านสะพาน — บทเรียนรอบใหญ่ #7 ข้อ 6)
3. เห็นคำว่า `SCENARIO_PRESENT`
- ไม่ครบสามข้อ = **ห้ามบูต** ใบนี้อยู่ BLOCKED ต่อ
✅ **ชื่อ flag/scenario ข้างบนเป็นชื่อจริงแล้ว (R124 ยืนยันจากโค้ดที่ commit)** — ไม่ใช่ชื่อเสนออีกต่อไป

### db (สำเนาเสมอ ห้ามแตะตัวจริง)
```
copy state\pirateforce.sqlite3 pf_bridge\backup\pirateforce_before_GT-045_<yyyyMMdd_HHmmss>.sqlite3
copy state\pirateforce.sqlite3 state\run_gt045.sqlite3
```
- เทียบ sha256 canonical กับ `CANON_SHA.txt` **ก่อนเริ่มและหลังจบ ต้องตรงทั้งสองครั้ง** (canonical เปิดอ่านไม่ได้ตลอดรอบ)
- เลนนี้ควรเป็น read-only session ถ้าออกแบบได้ · ตำแหน่งตัวละครรีเซ็ตกลับจุดเกิดทุกบูต (สำเนา DB ใหม่ทุกครั้ง)

### server args (เป๊ะ — ชื่อจริง ยืนยันแล้ว R124)
```
py -3 -u -m pirateforce_foundation.app --db state\run_gt045.sqlite3 --ground-loot-hypothesis-scenario scenarios\ground_loot_hypothesis_bit08_render.json
```
- **opt-in เท่านั้น ห้าม default-on** (บังคับในโค้ด: mutually exclusive กับ scenario โหมดอื่น + ต้องมี `--db` ชี้ไฟล์ที่มีจริง)
- หัวหน้าต่าง console ของ server จะขึ้น mode `ground-loot-hypothesis` — ใช้เช็คว่าบูตถูกโหมด
- ⚠️ **ไม่มี chat trigger และไม่มีปุ่มยิง** — เฟรมออกเองที่ TargetPos แรกหลัง runtime ack (= เกือบทันทีที่เข้าแมพ)
  ครั้งเดียวต่อเซสชัน · ตัวอักษรตอนช่องแชตไม่โฟกัส = hotkey ⇒ ใช้แค่ `W/A/S/D`, `Q/E`, `spacebar`

### steps
**ก่อนเริ่ม:** ถือ `LOCK_GAME` · จด boot stamp · เทียบ sha canonical · copy DB สองใบตามบล็อก db
1. เปิด server ก่อน client เสมอ (`Get-NetTCPConnection -State Established` พอร์ต 10188/10189 = 0 ก่อนเปิด client)
2. เปิด client (`Invoke-CimMethod Win32_Process Create`) → เลือกเซิร์ฟเวอร์ → dialog PVP ปุ่มซ้าย → หน้าเลือกตัวละคร
   → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** (ปุ่มซ้ายสุด = ลบตัวละคร **ห้ามกด**)
3. เข้าแมพ เห็น HP/minimap/ชื่อแมพ → **ถ่าย G0 ทันทีที่ควบคุมได้** ให้เห็น X/Y บน HUD และพื้นที่รอบตัว
   ⚠️ เฟรม element **ออกไปแล้วตั้งแต่วินาทีแรกที่เข้าแมพ** (ยิงเองที่ TargetPos แรก) — G0 จึงไม่ใช่ "ก่อนยิง"
   แต่คือ "มุมกว้างที่จุดเกิด" · **จดเวลาที่เข้าแมพ** ใช้แทนเวลายิง
4. **พิกัดใกล้ (+30X จากจุดเกิด · HUD ควรอ่าน X≈-9210, Y≈-2830):** หมุนกล้อง `Q/E` กวาด 360° หาอะไรที่โผล่
   บนพื้น/ป้ายชื่อลอย → ถ่าย **G1** มุมที่เห็น (หรือมุมที่ควรเห็นแล้วไม่มี)
5. **เดินเข้าไปถึงจุดนั้น** (`W/A/S/D` ไปทาง +X ประมาณ 30 หน่วย) → ถ่าย **G1b** ระยะใกล้ —
   ถ้ามีอะไรโผล่ ให้เห็นทั้งป้ายชื่อและ/หรือโมเดลชัด ๆ
6. **พิกัดไกล (+800X · HUD ควรอ่าน X≈-8440, Y≈-2830):** เดินต่อไปทาง +X จนถึง → ถ่าย **G2**
   (สองพิกัดเพื่อแยก "ไม่วาด" ออกจาก "วาดแต่อยู่นอกจอ/นอกระยะ culling" — ถ้าตัวใกล้วาดแต่ตัวไกลตอนแรกไม่วาด
   แล้วมาวาดเมื่อเดินเข้าใกล้ = จดแยกเป็นเรื่อง culling)
7. บันทึกว่า element อยู่ค้างหรือถูกลบเอง — ถ้าหายเอง จับเวลาว่าอยู่กี่วินาที (เทียบกับ 0.633 s ในหลักฐานคลิป)
   ⚠️ เซิร์ฟเวอร์เรา **ไม่เคยส่งเฟรมลบ/หมดอายุ** — ถ้าของหายเอง นั่นคือพฤติกรรม client ล้วน จดให้ชัด
8. ออกจากเกม: **X** มุมขวาบน (ตรวจก่อนว่าหน้าต่างแอปตัวเองไม่บังปุ่ม X) → dialog ยืนยัน → ปุ่มซ้าย
9. ปิด server เก็บ raw GAME log + console out/err → `PRAGMA integrity_check;`
10. **teardown เสมอ** แม้เลิกกลางคัน (boot stamp เกิน 420 นาที template ปฏิเสธ exit 12 — เพดานยกจาก 180 เมื่อ 2026-08-20 ·
    `TEMPLATE_teardown_generic.ps1:135` · ใช้ `staged\TOOL_stop_stale_server.ps1` สำหรับแท่นที่ถูกทิ้งข้ามชั่วโมง)
11. เทียบ sha256 canonical กับ `CANON_SHA.txt` อีกครั้ง ต้องเท่าเดิม

### pass criteria — สองชั้น แยกกันเด็ดขาด
**ชั้น (1) wire/DB (ไม่ต้องใช้สายตาคนหน้าจอ)**
- raw GAME log มี **สองเฟรม** ที่เซิร์ฟเวอร์เขียน element ออกไปจริง (เฟรมละพิกัด · ใกล้ก่อน ไกลตาม 0.10s) — ไบต์ตรง pin (pc เฟรมละ 44 ไบต์):
  เฟรมใกล้ sha256 `A3570BC9185BEF70ABB3810448F6E3F605437B2F1BFAB1DF474882AD3661EA03`
  hex: `129d6e140000000008040b000b0812010014010000000b121441ac27002ad4e70fc62ab9e030c52ac74a5f43`
  เฟรมไกล sha256 `4B14A026763F53FFD65210C2F2BCC0122B096A6877455C84DAAED71366F07F3A`
  hex: `129d6e140000000008040b000b0812010014020000000b121441ac27002ad4df03c62ab9e030c52ac74a5f43`
  (อ่าน: msg `0x6E9D` v4 · base mask 0 · derived `0x08` · count 1 · element: key 1/2 · mask `0x12` · dword `2600001` · f32 x,y,z)
  · action labels ฝั่ง server: `GROUND_LOOT_BIT08_RENDER_NEAR_ONCE` แล้ว `GROUND_LOOT_BIT08_RENDER_FAR_ONCE`
  · event: `hyp_pf_032_ground_loot_bit08_pair_committed` · เก็บ hexdump ทั้งไฟล์ **ห้ามลบ**
- `sessions`: `count(*) WHERE selected_character_id IS NOT NULL` +1 ต่อการเข้าเกมหนึ่งครั้ง · `PRAGMA integrity_check` = `ok` ·
  sha256 canonical ก่อน-หลังตรงกัน
- **ชั้นนี้ตอบไม่ได้:** จอวาดอะไร (การมีเฟรมออกไม่พิสูจน์ว่าไคลเอนต์วาด) ⇒ **ห้ามอ้างชั้นนี้แทนชั้น (2)**

**ชั้น (2) client-observable (ต้องมีคนหน้าจอ)**
- ภาพ **G0/G1/G1b/G2** อ่านค่า X/Y ได้ทุกใบ · วิดีโอต่อเนื่องช่วงยิงถ้าเหตุการณ์สั้น
- ตอบเป็นภาษาคน: **ที่พิกัดที่ยิง ขึ้นป้ายชื่อ/โมเดลบนพื้นหรือไม่ · ทั้งสองพิกัดหรือพิกัดเดียว · อยู่ค้างหรือหายเองในกี่วินาที**
- **ชั้นนี้ตอบไม่ได้:** ภาพหน้าจอไม่ใช่หลักฐานว่าเฟรมออกจากเซิร์ฟเวอร์จริง **ห้ามอ้างชั้นหนึ่งแทนอีกชั้น**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **wire ผ่านแต่จอไม่ขึ้นอะไรทั้งสองพิกัด** = ผลลบที่สมบูรณ์ **ไม่ใช่ FAIL ของใบ** ⇒ ประกาศชัดว่า
  "บิต `0x08` ไม่ใช่ช่องของวัตถุบนพื้น" ตัดตัวต้องสงสัยนี้ทิ้งถาวร แล้ว redirect ไปหาช่องทางอื่น (คำตอบที่ใช้ได้จริง)
- **ขึ้นพิกัดเดียว (ใกล้) แต่พิกัดไกลไม่ขึ้น** = อาจเป็นเรื่อง culling ระยะ ไม่ใช่ "ไม่วาด" — จดแยก

### nonclaims (ติดไปกับผลทุกกรณี)
- **ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับ (ปิดไปแล้ว กู้ไม่ได้ตลอดกาล) เคยใช้ช่องนี้** — ใบนี้ทดสอบแค่ว่าไคลเอนต์รับได้ไหม
- **ไม่ claim ว่าที่วาดออกมา = ไอเทมที่หยิบได้** — การวาดกับการหยิบเป็นคนละเรื่อง (ทิศทางการหยิบ = GT-046)
- **ไม่ claim ว่าคลิปวิดีโอในหลักฐานที่มายืนยันช่องทาง transport ใด ๆ** — คลิปอยู่ชั้น client-observable ล้วน
- **การประกอบ element เป็นดีไซน์ของเรา** ไม่ใช่ของเซิร์ฟเวอร์เดิม · หน่วยพิกัดโลกแปลงเป็นหน่วยจริงไม่ได้
- **result:** (ผู้เทสกรอก: ภาพ G0/G1/G1b/G2 พร้อม sha256 · วิดีโอถ้ามี · คำตอบ "วาดไหม/กี่พิกัด/อยู่กี่วินาที" ·
  path raw GAME log · เวลา · sha canonical ก่อน-หลัง)


## 🆕🔬 GT-046 PICKUP-DIRECTION-001 [STATIC-ON-BRIDGE]: `PickupTerrainThing` เป็นข้อความที่ไคลเอนต์ "ส่งออก" หรือ "รับเข้าอย่างเดียว" — หาจุดสร้าง/จุดส่ง  [🟠 **PENDING — งาน static บนเครื่องสะพานล้วน · ไม่ต้องมี server/client/DB/`LOCK_GAME`/teardown**]

**ที่มา:** ร่างผู้ช่วย `notes_to_chief\20260823_0805_GT-TICKET-DRAFT-ground-drop-and-pickup-direction.md` (ท่อน GT-046)
ทำไมสำคัญกว่าที่เห็น: ถ้าไคลเอนต์ **ส่ง** เอง ⇒ มีตัวจุดชนวนฝั่งไคลเอนต์ (auto-loot/เพ็ต/ระยะ) เซิร์ฟเวอร์แค่ตอบ ·
ถ้าไคลเอนต์ **ไม่เคยส่ง** ⇒ การเก็บถูกตัดสินฝั่งเซิร์ฟเวอร์ทั้งหมด · **สองทางนี้ทำให้เราต้องเขียนเซิร์ฟเวอร์คนละแบบ**

**หมวด:** `STATIC-ON-BRIDGE` — ต้องเปิด `GameClient.local.bin` จึงทำบน cloud clone ไม่ได้ ·
ผู้รับงานคือคนที่นั่งหน้าสะพาน ไม่ใช่ผู้เทสหน้าจอเกม · **ใบนี้ไม่มีอะไรให้ดูบนจอเกมแม้แต่อย่างเดียว**

### objective (claim เดียว)
**`PickupTerrainThing` ถูกสร้างและเขียนลงสตรีมผ่าน `0x0089A600` (WRITE) ที่ VA ใดในอิมเมจ หรือไม่พบจุด WRITE เลย**
(ทิศทางตัดสินด้วยว่า object เข้าสตรีมผ่าน `0x0089A600` WRITE หรือ `0x0089A640` READ — สองตัวนี้พิสูจน์แล้วตั้งแต่ GT-040)

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — เปิดอ่านอิมเมจอย่างเดียว (กติกา stamp 420 นาที/teardown ไม่เกี่ยวกับใบนี้)

### สิ่งที่ต้องมี (precondition)
- **อิมเมจ:** `GameClient\GameClient.local.bin` · size `14759424` ·
  sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` · PE32 · ImageBase `0x00400000`
  🔴 **จด sha ก่อนเริ่มและหลังจบ ต้องตรงกันทั้งสองครั้ง เปิดอ่านอย่างเดียวเสมอ**
- **ท่าทำงาน:** ตามวินัย `pf-static-re` · 🔴 **ห้ามใช้ linear disassembler เป็นหลักฐานของ negative** (มันหยุดที่ไบต์แรกที่ decode
  ไม่ได้แล้วรายงาน negative อย่างมั่นใจ = ความผิดพลาดรอบ 83) · census ด้วย byte matching (`E8`/`E9 rel32` ทุกออฟเซ็ต) ·
  สวีป exec section ทั้งสอง: `.text` (`0x00401000`, Vsize `0x00838A2C`) และ `.code` (`0x00C3A000`, Vsize `0x2E1`)
- **span ฐานผ่านปฏิปักษ์แล้ว:** GT-042 **PASS 2026-08-23** — span ข้างล่างรอด re-derive และขอบเขต handler ถูกแก้แล้ว ·
  กติกาเดิมยังบังคับ: **verify sha ของทุก span ก่อนพึ่งด้วยตัวเอง** · sha ไม่ตรง = หยุด รายงาน

### ของที่มีอยู่แล้ว (จาก GT-040 ท่อน C · ผ่าน re-derive ปฏิปักษ์ใน GT-042 · verify sha ก่อนพึ่ง)
```
vtable                0x00F3005C
serializer  slot +0x18  [0x005E5E30,0x005E5E83)  len 83
                        sha 8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066
                        2 ฟิลด์: tag 0x14 @ +0x14 len 4  ·  tag 0x08 @ +0x18 len 1  (ไม่มีฟิลด์ที่สาม)
handler (ขอบเขตแก้แล้ว) [0x005EF640,0x005EF66F)  len 47
                        sha 5d17fc4fdeeafde0a4a34e900e76d0336e404f8d2f058ba085044ae8d88d602e
                        อ่าน +0x18 แยก FC/FD/FE -> message id 1F/03/22 แล้วคืน true
census                PickupTerrainThing 0xF3093C 1 จุด · 0x108202C 2 จุด · constructor 3 จุด
```
🔴 **erratum ที่ต้องพกไปด้วย (ปิดโดย GT-042):** span handler เก่า `[0x005EF640,0x005EF908)` len 712 (sha `22da3ff4...`)
**hash ตรงแต่ป้ายผิด** — ไม่ใช่ handler ฟังก์ชันเดียว (`0x005EF66F=CC` · `0x005EF670` เริ่ม prologue ฟังก์ชันถัดไป) ·
ขอบเขตที่ถูกคือ `[0x005EF640,0x005EF66F)` len 47 ข้างบน — ใบนี้อ้างขอบเขตที่แก้แล้วเท่านั้น

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3 -> 4)
1. ไล่ทั้ง 3 จุดที่อ้าง vtable literal `0x00F3005C` (constructor) → ใครเรียก constructor พวกนั้น (census `E8/E9 rel32` เอง)
2. ตามสายขึ้นไปจนถึงจุดที่ object ถูกป้อนเข้าสตรีม → ใช้ **`0x0089A600` (WRITE)** หรือ **`0x0089A640` (READ)** — ตัวตัดสินทิศทาง
3. ถ้าเจอฝั่ง WRITE: อะไรเป็นตัวเรียก (input handler / timer / entity update)? ค่าที่ใส่ `+0x14` มาจากไหน
4. ค่า `FC/FD/FE` ที่ `+0x18` — หาว่าฝั่งไหนเป็นคนเซ็ต · message id `0x1F/0x03/0x22` แปลเป็นข้อความอะไร
   (**เชื่อมกับคลิปได้ตรงนี้:** คลิปเห็นบรรทัด `ได้รับ [<ชื่อ>] * <จำนวน>` **สีเขียว** แยกจาก EXP/ค่าฝีมือที่**สีขาว** —
   ถ้า message id ใดใน 1F/03/22 ตรงกับ template ที่มี `* <จำนวน>` นั่นคือจุดเชื่อมสองชั้นแรก · จดว่าเชื่อมได้/ไม่ได้)

### pass criteria — **STATIC-ON-BRIDGE (span + sha256 + re-derive · ชั้นเดียว)**
**ชั้น static (ชั้นเดียวของใบนี้):**
- verify sha ของ **ทุก** span ที่พึ่งก่อน re-derive · 🔴 **sha ไม่ตรงแม้ตัวเดียว = หยุด รายงาน span ที่เพี้ยน ห้าม re-derive ทับ**
- ตอบ objective เป็นประโยคเดียวได้: `PickupTerrainThing ถูกสร้างและเขียนลงสตรีมที่ <VA> ผ่าน 0x0089A600`
  **หรือ** `ไม่พบจุด WRITE เลยในอิมเมจ (ไล่ census E8/E9 + indirect ครบแล้ว)`
- แนบ span `[start,end)` + file offset + len + sha256 ของ **ทุก** ฟังก์ชันที่อ้าง (รูปแบบเดียวกับ GT-040/GT-042/GT-044)
- sha256 อิมเมจก่อน-หลังตรงกัน · ถ้าเขียนสคริปต์ commit ลง `tools/` แบบรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา — ใบนี้ไม่ผลิตหลักฐานชั้นนี้ และห้ามใครอ้าง static เป็นหลักฐานว่าจอเห็นอะไร**
ไม่มีเกมให้บูต ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**

### 🔴 ผลลบมีค่าเท่าผลบวก
- **"ไม่พบจุด WRITE เลย"** = ผลที่มีค่าเท่าการเจอ ⇒ ชี้ว่าไคลเอนต์อาจรับเข้าอย่างเดียว (การเก็บตัดสินฝั่งเซิร์ฟเวอร์)
  **แต่ต้องเขียนกำกับว่าไล่ indirect ครบหรือยัง** — "ไม่พบ WRITE" ≠ "ไคลเอนต์ไม่ส่ง" ถ้าเป็นการเรียกผ่าน table/indirect
- **เจอจุด WRITE** = redirect ไปหาตัวจุดชนวนฝั่งไคลเอนต์ (input/timer/entity) — งานออกแบบเซิร์ฟเวอร์เปลี่ยนทิศทันที

### nonclaims (ติดไปกับผลทุกกรณี)
- **static ไม่พิสูจน์ว่ารันไทม์ส่งจริง** — พิสูจน์ได้แค่ว่ามี/ไม่มีเส้นทางในอิมเมจ
- **"ไม่พบจุด WRITE" ≠ "ไคลเอนต์ไม่ส่ง"** ถ้ายังไล่ indirect ไม่ครบ — ต้องระบุสถานะการไล่ indirect
- **ห้ามอ้างว่าคลิปวิดีโอยืนยันทิศทางของข้อความ** — คนละชั้นหลักฐาน
- **ไม่ claim ว่ารู้ชื่อคลาส** ของ record — vtable ไม่มี RTTI/name literal · **ห้ามเดาชื่อ = ห้ามประดิษฐ์ wire format**
- **ไม่ claim ว่า derived id ถูก** — id จริงมาจากรันไทม์ที่ `ds:0x0108202C` ซึ่ง `.data` เป็นศูนย์ในไฟล์
- **result:** (ผู้รับงาน static บนสะพานกรอก: ประโยคทิศทาง WRITE/READ + VA · span/file-offset/len/sha256 ทุกฟังก์ชัน ·
  สถานะการไล่ indirect · เวลา · sha อิมเมจก่อน-หลัง)


## 🆕🔬 GT-047 RUNTIMEPROTO-CAPTURE-VALIDATE-001 [STATIC-ON-BRIDGE]: parse เฟรม `GSCN_RunTimeProtocolReq`/`Res` จาก capture corpus ด้วย schema ของ Codex — ปิด F2 ของใบตรวจปฏิปักษ์  [🟠 **PENDING — งาน static บนเครื่องสะพานล้วน · ไม่ต้องมี server/client/DB/`LOCK_GAME`/teardown · ต้องรันบน Windows (ชั้น capture รันบน Linux mount ไม่ได้)**]

**ที่มา:** ใบตรวจปฏิปักษ์ `notes_to_chief\20260823_0705_ADVERSARY-VERDICT-on-codex-RE-handoff.md` (F2) +
`notes_to_chief\20260823_0730_ADVERSARY-FOLLOWUP-plus-GROUND-DROP-evidence.md` (ข้อ 2 · การ์ด mutation `field_offset`)
F2: สองใบที่สำคัญที่สุดในโปรเจกต์ (`GSCN_RunTimeProtocolReq` W 40,747 เฟรม · `GSCN_RunTimeProtocolRes` R 10,073 เฟรม =
รวม 50,820 เฟรม คลังหลักฐานที่รวยที่สุด) ยังเป็น `A2_STATIC_OPEN` **ไม่เคยถูก parse สักเฟรม** ·
และงานคอมแบต/ลูท/การเคลื่อนที่ทั้งหมดขี่อยู่บนใบนี้ (actor-entry collection · derived bit `0x02`/`0x04`/`0x08` ของ GT-040)

**หมวด:** `STATIC-ON-BRIDGE` — ใช้ capture corpus + ชุดส่งมอบ RE ที่อยู่บนเครื่องสะพานเท่านั้น ·
🔴 **ต้องรันบน Windows ของสะพาน** — ใบตรวจ 07:30 พิสูจน์แล้วว่าชั้น capture รันจาก Linux mount ไม่ได้
(`PF_INPUT_INVENTORY.tsv` ปักพาธ Windows · เจอ `ERROR: fresh capture path set differs from input inventory`)
**ไม่มีอะไรให้ดูบนจอเกม** ผู้เทสหน้าจอ **ไม่ต้องทำอะไรกับใบนี้เลย**

### objective (claim เดียว)
**สถานะของ `GSCN_RunTimeProtocolReq` (W) และ `GSCN_RunTimeProtocolRes` (R) ขยับจาก `A2_STATIC_OPEN` เป็น `VALIDATED`
ด้วยการ parse capture 50,820 เฟรมผ่าน schema จากชุดส่งมอบ RE ของ Codex หรือรายงาน mismatch เป็นตัวเลข**
🔴 **mismatch > 0 มีค่าเท่าหรือมากกว่า `VALIDATED`** — จดเป็นผล ไม่ใช่ fail (mismatch ที่วัดได้ = ที่ที่เราเดาผิด ชี้ตัวได้)

### db / server args
**ไม่ใช้ DB · ไม่บูตเซิร์ฟเวอร์ · ไม่บูต client** — parse capture + อ่าน schema TSV อย่างเดียว
(กติกา stamp 420 นาที/teardown/canonical ไม่เกี่ยวกับใบนี้ · แต่ **ห้ามแก้ capture และห้ามแก้ TSV ส่งมอบ** — เปิดอ่านอย่างเดียว)

### สิ่งที่ต้องมี (precondition · verify ก่อนเริ่ม)
- ชุดส่งมอบ RE ของ Codex ที่ `pf_bridge\external\` (บนเครื่องสะพาน — ยังไม่ได้ push เข้า repo) · verify จำนวนแถวตามที่ใบตรวจ 07:05 นับไว้:
  `PF_PROTOCOL_REGISTRY.tsv` 520 บรรทัด (519 + หัว) · `PF_SERIALIZER_FIELDS.tsv` 6,932 (6,931 + หัว) ·
  `PF_TAG_CENSUS.tsv` · `PF_FIELD_VALIDATION.tsv` · `PF_RUNTIME_CLASSMAP.tsv` 6,244 แถว (ทั้งหมด UNKNOWN — ห้ามพึ่งเป็นชื่อคลาส)
- เครื่องมือ: `pf_validate_capture_fields.py` (เรียก `validate_schema_mutation_regressions()` ทุกครั้ง) ·
  `pf_extract_protocol.py` (A4 · re-derive ผ่านแล้วใน 07:30 — sha256 TSV ตรงไบต์ต่อไบต์)
- capture corpus ที่อ้างใน `PF_INPUT_INVENTORY.tsv` (พาธ Windows ของสะพาน — อย่าแก้)
- 🔴 **ไม่ต้อง WAIT merge อะไร** — ชุดส่งมอบถูกรับเข้าใช้งานแล้ว (ใบตรวจ 07:05) และอยู่บนสะพานครบ ·
  แต่ **การ์ด mutation ตัวใหม่ (ดูจ็อบ 3) ต้องเพิ่ม/รันบน Windows** เพราะ Linux mount รันชั้น capture ไม่ได้

### จ็อบ (ทำตามลำดับ 1 -> 2 -> 3)
**จ็อบ 1 (แกน) — parse 50,820 เฟรมของสองข้อความ**
1. เอา schema ของ `GSCN_RunTimeProtocolReq` (W) และ `GSCN_RunTimeProtocolRes` (R) จาก `PF_SERIALIZER_FIELDS.tsv`
   (Res อ้าง serializer `0x005E3EE0` / handler `0x005E4060` ในใบตรวจ 07:05 — verify กับ TSV จริง อย่าฝังค่า)
2. รัน `pf_validate_capture_fields.py` บนคลัง 40,747 (W) + 10,073 (R) เฟรม · รายงานเป็นตัวเลข:
   parse ok / parse fail / **mismatch นับรายฟิลด์** · สถานะปลายทางของแต่ละข้อความ (`VALIDATED` หรือค้าง `A2_STATIC_OPEN` พร้อมเหตุ)

**จ็อบ 2 — re-derive ยืนยันว่า schema สกัดสดจากอิมเมจ ไม่ใช่ตารางจำ**
3. คัด `pf_extract_protocol.py` ไปรันในไดเรกทอรีเปล่านอกโฟลเดอร์ส่งมอบ ชี้อิมเมจเดิม → เทียบ sha256 ของ
   `PF_PROTOCOL_REGISTRY.tsv`/`PF_SERIALIZER_FIELDS.tsv`/`PF_TAG_CENSUS.tsv` ต้องตรงไบต์ต่อไบต์ (ใบตรวจ 07:30 ได้ตรงแล้ว — ยืนยันซ้ำ)

**จ็อบ 3 (ข้อบังคับจากใบตรวจ) — เพิ่ม mutation guard ที่ `field_offset`**
4. กลายพันธุ์ `field_offset` ของข้อความที่สถานะ `VALIDATED` (เช่น `TargetPosVital:W:1` จาก `+0x14` เป็น `+0x99`
   — เคสที่ใบตรวจ 07:30 พบว่า `build_schemas()` ยอมรับตารางผิดเงียบ ๆ) → **บังคับว่าผลตรวจ capture ต้องรายงาน `mismatch > 0`**
5. 🔴 **ถ้าไม่แดง (mismatch = 0) = การ์ดไม่ครอบคลุมการทุจริตชนิด `field_offset` — ต้องแก้การ์ดจนแดง**
   (บทเรียน D4/D5 รอบ 118: guard ที่ทำแดงไม่ได้ = หลักฐานปลอม) · เก็บ log การรัน mutation ทั้งก่อน (คาดเขียว) และหลังกลายพันธุ์ (ต้องแดง)

### pass criteria — **STATIC-ON-BRIDGE (span/schema + sha256 + re-derive · ชั้นเดียว)**
**ชั้น static (ชั้นเดียวของใบนี้):**
- ตัวเลขชี้ขาดของสองข้อความ: parse ok / fail / **mismatch รายฟิลด์** ต่อ `GSCN_RunTimeProtocolReq` (W) และ `GSCN_RunTimeProtocolRes` (R)
  พร้อมสถานะปลายทาง (`VALIDATED` หรือ `A2_STATIC_OPEN` + เหตุผล) · จำนวนเฟรมที่ประมวลจริงต้องเท่า 40,747 / 10,073 (หรืออธิบายส่วนต่าง)
- re-derive จ็อบ 2: sha256 ของ TSV ที่สกัดใหม่ = sha256 ของชุดส่งมอบ (ยืนยัน schema สดจากอิมเมจ)
- จ็อบ 3: log สองรอบ — ก่อนกลายพันธุ์ (เขียว) และหลังกลายพันธุ์ `field_offset` (**mismatch > 0 / แดง**) · ถ้าไม่แดง ต้องแนบ patch การ์ดที่ทำให้แดง
- sha256 ของอิมเมจ + ของ capture ก่อน-หลังตรงกัน (เปิดอ่านอย่างเดียว) · สคริปต์/การรันซ้ำได้พร้อม guard count + exit 0

**ชั้น client-observable:** 🔴 **ว่างเปล่าโดยเจตนา** — ไม่มีเกมให้บูต ไม่มีอะไรให้ถ่าย · ห้ามอ้าง static เป็นหลักฐานว่าจอเห็นอะไร

### 🔴 ผลลบมีค่าเท่าผลบวก
- **mismatch > 0** ⇒ ข่าวใหญ่: schema ของ Codex ไม่ตรง capture ที่ฟิลด์ไหน จำนวนเท่าไร ⇒ ชี้จุดที่ต้อง re-derive · หยุด จดตัวเลข
- **parse ok เต็ม 50,820 → `VALIDATED`** ⇒ ปิด F2 · แต่ **ยังห้ามอ้าง "0 mismatch" ลอย ๆ** (ดู nonclaims)
- **การ์ด mutation ไม่แดง** ⇒ พบช่องโหว่ของ validator เอง = ผลที่มีค่า ⇒ แนบ patch ที่ทำให้แดง แล้วรันซ้ำ

### nonclaims (ติดไปกับตัวเลขทุกครั้ง — 🔴 ห้ามอ้าง "0 mismatch" โดยไม่ติดสามข้อนี้)
- **F1** — ตัวเลข 11,904 instance ถูกแบกด้วย `CheckSecondPwdVital` (R) **9,166 = 77%** ใบเดียว + หางบาง 34 คู่ ·
  **ห้ามอ่านว่า "ตารางโปรโตคอลถูกยืนยันกว้าง ๆ"** — มันคือข้อความง่ายใบเดียวปริมาณมาก
- **F2** — ก่อนใบนี้ปิด สองข้อความนี้ยัง `A2_STATIC_OPEN` (static ล้วน) · ผลของใบนี้ยกได้เฉพาะสองข้อความนี้ ไม่ใช่ทั้งตาราง
- **F3** — 980 คู่ (95%) เป็น `NOT_OBSERVED` · 37 คู่ (3.6%) `VALIDATED` · "0 mismatch" ไม่พูดถึง 980 คู่นั้นเลย
- แถวที่ `status = VALIDATED` เท่านั้นนับเป็นหลักฐานสองชั้น · เวลาอ้างในเอกสารต้องเขียน `ยืนยันด้วย capture` หรือ `static ล้วน` เสมอ
  **ห้ามเขียนคำว่า "ยืนยันแล้ว" เฉย ๆ**
- **ไม่ claim ว่ารู้ความหมายของ tag** เกิน len (`0x2A`=float32/4 · `0x12`=uint16/2 · ที่เหลือ UNKNOWN ตามที่ Codex ประกาศ)
- **ไม่พึ่ง `PF_RUNTIME_CLASSMAP.tsv` เป็นชื่อคลาส** — 6,244 แถว UNKNOWN 100% (บันทึกผลลบ ไม่ใช่แหล่งชื่อ)
- **การประกอบ/ตีความของเราไม่ใช่ของเซิร์ฟเวอร์ต้นฉบับ** ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล
- **result:** (ผู้รับงาน static บนสะพานกรอก: ตัวเลข parse ok/fail/mismatch รายฟิลด์ของสองข้อความ + สถานะปลายทาง ·
  sha256 re-derive จ็อบ 2 · log การ์ด mutation ก่อน/หลัง (+patch ถ้าต้องแก้) · เวลา · sha อิมเมจ+capture ก่อน-หลัง)
