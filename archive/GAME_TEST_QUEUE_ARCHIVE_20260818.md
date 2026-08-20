# GAME_TEST_QUEUE — ARCHIVE 2026-08-18 (chief รอบ 52)

> ย้ายมาจาก `GAME_TEST_QUEUE.md` ตอนประมวลผลรอบใหญ่ #2 เสร็จ (ไฟล์คิวเกิน 60KB)
> ทุกบล็อกด้านล่างเป็นบันทึกประวัติศาสตร์ read-only — ผลถูกประมวลเข้า repo แล้วที่
> `reports/PF_BIGROUND2_ATTENDED_RESULTS_20260818.md` (+manifest) · ledger 3 amendments ·
> matrix 3 movements (commit ดูใน LOCK/CHIEF_CONTINUATION รอบ 52)

## [A] บล็อกหัวไฟล์ที่หมดวาระ (คำตัดสิน/บทเรียนถูกดูดซับเข้า policy 17:40 + task prompt แล้ว)


> 🟢🟢🟢 **คำตอบจาก Panya ต่อ Q1/Q2 ของรอบ 22 (เขียน 12:11:55 ICT ระหว่างรอบ 23 ถือ lease)**
> ช่องทาง: เซสชันหลัก (แชทที่ Panya คุยอยู่ตอนนี้) เป็นมือเขียนแทน — ทุกบล็อกที่ลงชื่อ
> "จาก Panya" ในไฟล์นี้มาจากช่องทางนั้น รวมบล็อกคำตัดสิน 3 ข้อก่อนหน้า
>
> **Q1 = จริง** — คำตัดสิน 3 ข้อ (M3 ทาง ก / เพิ่ม Domain 8 / อนุญาตข้อ 16) เป็นของ
> Panya จริง ยืนยันซ้ำอีกครั้งตรงนี้ → **เริ่ม M3/HYP-PF-010 ได้เลย** (timestamp "11:55"
> ในบล็อกเดิมเป็นเวลาประมาณที่มือเขียนใส่เอง อย่าใช้จับผิด mtime อีก)
> **Q2 = ให้เปิดเกมเองได้** — chief เปิด `GameClient.local.bin` ผ่าน bridge เองเมื่อ
> ต้องการขอสิทธิ์หรือทำเทส GT ใด ๆ: เปิด server → เปิดเกม → รอหน้าต่าง 'Pirate Force'
> โผล่ → `request_access(["GameClient.local.bin"])` → **Panya อยู่หน้าเครื่อง รอกด
> Allow อยู่** → ถ้าได้สิทธิ์ ทำเทสต่อ / ถ้า dialog ไม่ขึ้นหรือถูกปฏิเสธ ให้ปิดเกม
> ปิด server ให้เรียบร้อย แล้วบันทึกผลจริงลงคิว
> ลำดับความสำคัญรอบถัดไป: ทำ Q2 ก่อนเลย (Panya รออยู่ตอนนี้) → แล้ว M3

> ✅✅✅ **คำตัดสินจาก Panya ครบทั้ง 3 ข้อ (2026-08-17 11:55) — ปลดบล็อกได้ทันที:**
>
> 1. **M3 = ทาง (ก)**: เปิด hypothesis ใหม่ **`HYP-PF-010` "generalized free-slot move"**
>    — HYP-PF-008 คงเดิมไม่แตะ · เขียน provenance/evidence_gap/falsification/stop_rule
>    ชุดใหม่ · `production_allowed=false` · occupied slot ยัง fail closed ·
>    ต้องแก้ `EXPECTED_IDS`+`EXPECTED_META` ใน `tools/verify_hypothesis_ledger.py`
>    และอัปเดต `CANONICAL_CONTENT_SHA256` ตามขั้นตอนที่รอบก่อนสรุปไว้
> 2. **Domain 8 (presentation/audio) = เพิ่ม** เข้า Functional Coverage Matrix
>    เป็นความสำคัญท้ายสุด (แถวเริ่ม `not_started` — จดให้ครบ ไม่บังคับทำตอนนี้)
> 3. **ข้อ 16 = อนุญาต**: chief ส่ง `TargetPosVital` ชั้น wire (จาก corpus 315 รูปแบบ)
>    หลัง runtime_ack ใน headless replay แล้ววัดว่า `character_positions` ถูกเขียนไหม
>    — เพื่อให้ผลเทสเดินในเกมจริง (GT-005) ตีความได้
>
> ลำดับแนะนำ: ทำข้อ 3 ก่อน (10 นาที รู้คำตอบ persistence) → แล้วเริ่มข้อ 1 (M3)
> → ข้อ 2 แทรกตอน matrix ถูกแตะครั้งถัดไป

> ⚡⚡⚡ **คำสั่งใหม่ล่าสุดจาก Panya (2026-08-17 11:45) — มีผลเหนือทุกข้อความเก่ากว่าในไฟล์นี้และไฟล์อื่น**
>
> 1. **ขอบเขต "ห้ามเทสในเกม" ของ task นี้ ยกเลิกแล้ว** — task `pirate-force-chief-continue`
>    เป็น **Chief + Game Tester ในคนเดียวกัน** (โครงสร้างรวมบทบาท อนุมัติ ~11:10)
>    ประโยค "ไม่เปิด GameClient ไม่แตะ UI (ขอบเขตผู้ใช้ 2026-08-17)" ทุกที่ = **ล้าสมัย**
> 2. **finding R15 ที่ว่า "ทางเดียวคือ attended session" = ข้อมูลเก่าและยังทดสอบไม่ครบ** —
>    R15 วัดแค่ `list_granted_applications` ว่าง แต่**ไม่เคยเรียก `request_access` จริงเลย**
>    → กติกาใหม่: ทุกรอบที่คิวมี GT PENDING และสิทธิ์ว่าง ให้เรียก
>    `mcp__computer-use__request_access` ขอ `["GameClient.local.bin"]` **หนึ่งครั้ง**
>    **Panya อยู่หน้าเครื่องและกำลังรอกด Allow อยู่ตอนนี้** — ถ้า dialog ขึ้นและถูกกด Allow
>    ระบบจะจำ approval ติดตัว task ถาวร = เทสในเกมได้เองทุกรอบถัดไป
>    ถ้าเรียกแล้ว timeout/error ให้บันทึกผลจริงลง GAME_TEST_QUEUE (นั่นแหละคือผลการทดลอง)
> 3. ลำดับหน้าที่ต่อรอบ: ประมวลผลค้าง → **เทสในเกม (ตามข้อ 2)** → งานโค้ด/เอกสาร → idle

> 🧪 **ผลการทดลองข้อ 2 — รอบ 23 (2026-08-17 12:07) เรียกจริงหนึ่งครั้ง ได้คำตอบชัดเจนแล้ว**
>
> `request_access(["GameClient.local.bin"])` → ตอบกลับ:
> ```
> {"granted":[], "denied":[],
>  "notInstalled":{"apps":[{"requestedName":"GameClient.local.bin","didYouMean":[]}],
>    "guidance":"... The request was NOT shown to the user. ..."}}
> ```
> **ระบบบอกเองตรง ๆ ว่า "The request was NOT shown to the user"** และ `didYouMean` ว่างเปล่า
> → ✅ ยืนยันแล้วว่า **ไม่มี dialog ไปถึง Panya และไม่เคยมี** — ไม่ใช่ timeout ไม่ใช่การรอกด
> → ❌ **ห้ามเขียนที่ไหนอีกว่า "รอ Panya กด Allow"** ให้เขียนว่า "ชื่อ resolve ไม่ได้"
>
> **สาเหตุ (ยืนยันซ้ำรอบนี้):** เครื่องมือ `request_access` รับได้เฉพาะชื่อแอปที่ Windows
> ขึ้นทะเบียนไว้ รายชื่อที่ระบบส่งมาให้เลือกมี ~200 แอป (Notepad, Chrome, LINE, iTunes, …)
> และ **ไม่มีรายการใดเกี่ยวกับ Pirate Force / GameClient เลย** เพราะตัวเกมเป็นไฟล์
> `GameClient\GameClient.local.bin` ที่ไม่ได้ติดตั้งลง Start menu
>
> **ทางออกที่เหลืออยู่จริง ๆ มีสองทาง — ต้องให้ Panya เลือก:**
> - (ก) Panya เปิดเกมค้างไว้เอง **หนึ่งครั้ง** → รอบถัดไป chief ขอสิทธิ์ด้วยชื่อ
>   *process/หน้าต่างที่กำลังรันอยู่* (resolver มองเห็น running app ได้)
> - (ข) อนุญาตให้ chief เปิดเกมเองจาก bridge (`ProcessStartInfo` ไม่ต้องใช้สิทธิ์)
>   แล้วค่อยขอสิทธิ์ตามลำดับใน 🔑 ข้างบน — **รอบ 22 และ 23 ตั้งใจไม่ทำเพราะยังไม่มี
>   คำอนุญาต และเกมเต็มจอที่เด้งขึ้นตอนไม่มีคนเฝ้าจะรบกวนเครื่อง**
>
> ✅ **คลี่คลายแล้ว (2026-08-17 12:22-12:25, attended):** Panya สั่งเทสเกมจริงเอง
> = เลือกทาง (ข) โดยปริยาย · ลำดับ 🔑 **พิสูจน์ซ้ำสำเร็จ**: boot server → เปิดเกมผ่าน
> bridge (job 047) → หน้าต่าง 'Pirate Force' โผล่ → `request_access(["GameClient.local.bin"])`
> → dialog ขึ้นจริง → Panya กด Allow → **granted tier full** → ขับ UI ได้ตลอดเซสชัน
> ผล: **GT-005 = PASS** (ดู result ใต้รายการ) · สิทธิ์นี้ผูกกับเซสชันหลัก ไม่ติดตัว
> scheduled task — รอบ chief ถัดไปยังต้องใช้ลำดับเดิมถ้าจะเทสเอง

**คืนนี้ (2026-08-17) ผู้เทสคือเซสชันหลัก (Claude ตัวที่คุยกับผู้ใช้ ถือสิทธิ์
computer use ของ GameClient อยู่แล้ว)** — task `pirate-force-game-tester` ถูกปิดชั่วคราว

> 🔴 **อ่านก่อน — ยืนยันด้วยการวัดจริงในรอบ 15 (2026-08-17 09:4x):**
> คิวนี้ **ไม่มีทางเดินได้เองโดยไม่มี Panya อยู่หน้าเครื่อง** ไม่ว่าจะรออีกกี่รอบ
> 1. task `pirate-force-game-tester` → `enabled: false`, ไม่มี `nextRunAt`,
>    `lastRunAt` = **04:49:55 ICT** (ตื่นทั้งชีวิตครั้งเดียว แล้วโดน LOCK ของ chief ไล่กลับ)
> 2. scheduled context **ไม่มีสิทธิ์ computer use เลย** — `list_granted_applications`
>    ตอบ `{"allowedApps":[], grantFlags ทั้งหมด false}` → เปิด task กลับมาก็ขับ UI ไม่ได้
> 3. chief ถือ LOCK **77.8% ของเวลา** (วัดจากรอบ 11–14) → ผู้เทสจะได้ LOCK ว่าง ~34% ของการตื่น
>
> → **ทางเดียวที่ใช้ได้จริงคือ attended session** — ขั้นตอน + prompt พร้อมวางอยู่ที่
> **`pf_bridge\ATTENDED_SESSION_RUNBOOK.md`** (ใช้เวลา Panya ~25 นาที ได้ GT-005 + GT-006)
> เหตุผลเต็ม: `pf_bridge\FINDINGS_R15_TESTER_TASK_DISABLED.md`

> 🟢 **ของใหม่รอบ 16 (2026-08-17 10:0x) — บางรายการอาจไม่ต้องรอ Panya เลย**
> พิสูจน์สดแล้วว่า **headless replay จบ LOGIN handshake จริงได้ โดยไม่เปิด GameClient**
> และคำตอบของ server **ตรงทุกไบต์** กับที่ client จริงเคยได้รับ (job 039, exit 0)
> · capture corpus กู้เฟรมขาเข้าของ client จริงได้ **20,209 เฟรม / 167 ไฟล์ / ผิดพลาด 0**
> · เส้นทาง login **ไม่มี nonce/timestamp/sequence เลย** (87 เซสชัน → รูปแบบไบต์เดียว)
> · corpus มี `TargetPosVital` 315 รูปแบบ (การเดิน → GT-005),
>   `ItemOperateVitalReq` 12 รูปแบบ (→ GT-002), `COnLandVital` 127 รูปแบบ
>
> เหตุผลเต็ม + nonclaims 8 ข้อ: `pf_bridge\FINDINGS_R16_HEADLESS_REPLAY_VIABLE.md`

> 🟢🟢 **ของใหม่รอบ 17 (2026-08-17 10:1x) — พอร์ต GAME `10189` พิสูจน์แล้วเช่นกัน:
> เข้าเกมได้จริงโดยไม่มี GameClient** (job 040, exit 0 · ไม่แตะ UI เลย)
> · replay ขับ server จนถึง **`start=True teleport=True runtime_ack=True`**
> · server ยิง **`V99_SHOW_MESSAGE_LOCAL_SERVER_ONLINE` 102B** ออกมาให้เรา
>   = เฟรมเดียวกับข้อความ `[ระบบ] : Pirate Force local server online` ในเกณฑ์ PLAYBOOK ข้อ 6
> · **ลำดับ request/response เหมือน client จริงทุกเหตุการณ์ 18/18**
>   (ต่างเฉพาะจังหวะของ heartbeat/keepalive ที่ขับด้วยนาฬิกา — วัดเป็นตัวเลขไว้แล้ว)
> · เกิดแถว `sessions` `selected_character_id=1`, `lease_generation` +1, ปิดสะอาด, integrity ok
> เหตุผลเต็ม + nonclaims 10 ข้อ: `pf_bridge\FINDINGS_R17_HEADLESS_GAME_ENTRY_PROVEN.md`

> 🔴🔴 **ของใหม่รอบ 18 (2026-08-17 10:3x, job 041) — ตัดงานออกจากคิวของ Panya ได้ 1 รายการ**
> **`GT-003` ผ่านไม่ได้ และไม่ใช่เพราะ headless** — server รับ client ได้ **ทีละตัวเดียว**
> ต่อ listener หนึ่งตัว: `s.listen(4)` แล้ว `accept()` + handle ในลูปเดียวกัน
> **ไม่มี thread ต่อ connection เลย** (v141 บรรทัด 7388/7395 และ 7939/7943)
> · วัดสด: connection ที่สองรออยู่ใน backlog **22–42 วินาที** แล้วถูกรับภายใน **~30 มิลลิวินาที**
> หลังตัวแรกปิด → **GameClient จริงสองตัวก็ให้ผลเดียวกัน ไม่ต้องเสียเวลา attended session**
> 🟢 ของแถมสองข้อ: **(ก)** พอร์ต GAME ทำงานเต็มรูปแบบ **โดยไม่ต้องทำ LOGIN เลยแม้แต่ไบต์เดียว**
> (transcript เหมือนกัน 18/18 เหตุการณ์) · **(ข)** replay ที่ใช้จังหวะ **0.34/1.75 วินาที**
> ให้ transcript **ตรงกับ client จริง 100% รวม keepalive** โดยไม่ต้องใช้ตัวกรองใด ๆ
> เหตุผลเต็ม + nonclaims 10 ข้อ + **ข้อ 14 ใหม่ (ก–ง)**:
> `pf_bridge\FINDINGS_R18_SERVER_IS_STRICTLY_SERIAL.md`

> 🟢🔴 **ของใหม่รอบ 19 (2026-08-17 10:5x, job 042) — วัดสองคำในเป้าหมายสูงสุดที่ไม่มีใครเคยวัด**
> **`persistence` / `reconnect`** อยู่ในบรรทัดเป้าหมายมา 19 รอบ และไม่เคยมีรอบไหนแตะ
> · 🟢 **reconnect ผ่าน** — เข้าเกม → ปิด socket → ต่อใหม่ ได้ transcript
> **เหมือนครั้งแรกทุกโหมด รวมโหมดที่เก็บ heartbeat ไว้ทั้งหมด** (39/39 บรรทัด)
> · 🟢 **restart ผ่าน** — บูตสองครั้งบนไฟล์ DB เดียวกัน boot B ยังตรงกับ client จริง
> · 🟢 **ไม่มี session รั่วค้างเปิดสักแถว** `closed_at` ครบทุกกรณี รวมตอนปิด socket ดื้อ ๆ
> · 🟢 **`listen(4)` เป็นขีดจำกัดจริงและตรงเป๊ะ** — socket 1–5 ต่อติด **#6 โดน RST (10061)**
> · 🔴 **แต่ของสำคัญคือข่าวร้าย: มีตารางเดียวจาก 7 ที่ถูกเขียนเลย คือ `sessions`**
> `character_positions` / `character_backpacks` / `characters` **ไม่ขยับเลย**
> → **"persistence" ที่มีอยู่ตอนนี้ = บันทึกว่าใครเคยต่อเข้ามาเท่านั้น**
> (nonclaim: replay ไม่เคยเดิน จึงเป็น "เส้นทางเข้าเกมไม่เขียนตำแหน่ง" ไม่ใช่ "เขียนไม่ได้")
> → **มีผลกับ GT-005 โดยตรง — อ่าน evidence R19 ใต้ GT-005 ก่อนรัน**
> เหตุผลเต็ม + nonclaims 10 ข้อ + **ข้อ 15/16 ใหม่**:
> `pf_bridge\FINDINGS_R19_RECONNECT_AND_RESTART_WORK_NOTHING_PERSISTS.md`


## [B] GT-008 (FAIL — ประมวลแล้วรอบ 52)


## GT-008 HYP-PF-013 ack+socket-close: client ออกเกม/หลุดจากแมพจริงเมื่อ server ปิด socket หลัง ack  [FAIL — ทั้ง 03/01: ไม่มี transition, client ไม่รู้ตัวว่า socket ตาย] ❌ 2026-08-18 01:36–01:48 attended (รอบใหญ่ #2)

- objective: (claim เดียว — ชั้น client-observable เท่านั้น) เมื่อ server ตอบ ack เดิมของ PF-012
  แล้ว**ปิด socket สะอาด (shutdown+close) หลัง ~250ms** — **ปุ่ม "ออกจากเกม" (subcode 01)
  ทำให้ client ปิดตัวเองสะอาด และปุ่ม "กลับหน้าเลือกตัวละคร" (subcode 03) พา client หลุดจากแมพ**
  (char select / server select / disconnect flow ใด ๆ — บันทึกว่าไปหน้าไหน) · ชั้น wire/DB
  พิสูจน์แล้ว headless job 084 (ack byte-exact → EOF ที่ ack+253.5/254.1ms → closed_at นำ ack
  4–5ms · report `PF_LOGOUT_CLOSE001_HYP_PF_013_ACK_SOCKET_CLOSE_HEADLESS_WIRE_DB_20260817.md`)
  — **อย่าเทสซ้ำชั้น wire อย่านับเป็นเกณฑ์**
- db: สำเนา canonical สด (087 copy + เช็ค sha `FA794D0B..4400` ให้อัตโนมัติ — เช็คกับค่าใน LOCK ก่อนรัน)
- server args: (087 จัดให้ครบ) บูตตรง + `--logout-hypothesis-scenario
  scenarios\logout_hypothesis_ack_close.json` (🔴 ต้องเป็นไฟล์ **ack_close** ไม่ใช่ ack_echo —
  ใส่ ack_echo = ได้พฤติกรรม GT-007 เดิม ไม่มีการปิด socket = เทสนี้ไร้ความหมาย ·
  console บรรทัด scenario ต้องเขียน `logout_hypothesis_ack_close`)
- steps:
  1. ย้ายหน้าต่างเกมไปฝั่งซ้ายของจอ**ก่อนเริ่ม** (บทเรียน GT-007: หน้าต่าง Claude บังปุ่ม)
  2. run staged `087_gt008_boot.ps1` (boot server ack_close + เปิดเกม) → PLAYBOOK ข้อ 3–6 เข้าแมพ
  3. เปิด dialog ระบบ (เมนู HOME → "ออก") → คลิกปุ่ม **"กลับหน้าเลือกตัวละคร"** (subcode 03 ก่อน)
  4. สังเกต ~15 วิ: client ไปหน้าไหน? char select / server select / disconnect dialog / ยังอยู่ในแมพ?
     — บันทึกทุกกรณี + เวลาแม่น ๆ (server จะปิด socket ที่ ack+250ms — อาการควรเกิดเกือบทันที)
  5. ถ้าหลุดจากแมพได้: เข้าแมพใหม่ (ต่อ connection ใหม่ได้เลย ไม่ต้องบูตใหม่) → dialog →
     ปุ่ม **"ออกจากเกม"** (subcode 01) → สังเกต: หน้าต่างปิดเอง? process จบสะอาด?
  6. ถ้า step 4 ยังอยู่ในแมพ/ค้าง: บันทึกละเอียด (UI ตอบสนองไหม? keepalive ยังวิ่งไหม?) →
     ยังต้องเทส subcode 01 ในเซสชันใหม่เสมอ (อย่าสรุปข้ามกัน) → ปิดด้วย X ตามปกติ
  7. run staged `088_gt008_teardown.ps1` (เก็บ GAME_LIVE/EVENTS + DB + ยืนยัน client self-exit)
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** 01 → หน้าต่างปิดเองโดยไม่ End task/ไม่กด X · 03 → client
    ออกจากแมพไปหน้า UI ใดหน้าหนึ่งโดยไม่ค้าง · ทั้งคู่ไม่มี crash — **ถ้าขึ้น disconnect-error
    dialog = falsify บางส่วน** (บันทึกข้อความ dialog เป๊ะ ๆ + ภาพ ถ้าทำได้) ไม่ใช่แค่ FAIL เฉย ๆ
  - **wire-DB (ยืนยันซ้ำเฉย ๆ ผ่าน 088):** `HYP_PF_013_LOGOUT_SUBCODE0x_ACK_THEN_SERVER_SOCKET_CLOSE`
    ใน GAME_LIVE · SESSION_END/SOCKET_CLOSED หลัง ack · closed_at ไม่ NULL · integrity ok ·
    canonical sha ไม่เปลี่ยน
- nonclaims: ไม่พิสูจน์ multi-cycle logout/login วนหลายรอบ · ไม่พิสูจน์ logout ก่อนเข้าแมพ ·
  ไม่พิสูจน์ subcode อื่น · ไม่ claim ว่า server เดิมปิด socket แบบนี้ (ไม่มี golden — R40) ·
  ผล FAIL/disconnect-dialog = falsify เฉพาะ shape ack+close → chief จะเดินต่อที่ fallback
  0x3D4B-first (ดีไซน์บันทึกใน ledger PF-013 + CHIEF 32.3) ภายใต้ entry ใหม่
- result: ❌ **FAIL ทั้งสอง subcode ตามเกณฑ์ client-observable — falsify shape ack+close ครบถ้วน**
  attended 01:36–01:48 · สองรอบบูต (jobs `087`→`088` ×2 · สำเนา DB gt008_20260818_013613 / _014313)
  - ⚠️ ก่อนเริ่ม: 087 ABORT หนึ่งครั้งเพราะ canonical sha เปลี่ยนเป็น `D08A89BF..08E2` โดยไม่มีใครประกาศ
    — วินิจฉัยแล้ว: **migration 004 ถูก apply ลง canonical ตอน 01:22:31 ระหว่าง Windows gate ของรอบ 51**
    (schema_migrations มีแถว version 4 · ข้อมูลทุกแถวเดิมครบ integrity ok) → ผู้เทสแก้ sha gate
    ใน staged 087/090/097/072 เป็นค่าใหม่แล้วรันต่อ · 🔴 **chief ต้องสอบสวน: อะไรใน gate แตะ canonical**
    (เทสไม่ควรแตะ DB จริง) — บันทึกไว้ตรงนี้เป็นหลักฐาน
  - **ชั้น client-observable (ตาเห็นจริง):**
    - **subcode 03** (กลับ char select, กด 01:39:42): dialog ปิด → **ยังอยู่ในแมพ ไม่มี transition ใด ๆ**
      ตลอด 40+ วิ · UI ตอบสนองปกติ (เปิดเมนู HOME ซ้ำได้) · มีอาการจอขาววูบ ~20 วิหลังกด
      ตอนคลิก HOME (เรนเดอร์สะดุด + หน้าต่าง resize เอง แล้วฟื้นเอง — สังเกตการณ์ ไม่ใช่ freeze)
      · **ไม่มี disconnect dialog แม้ server ปิด socket ไปแล้วที่ ack+250ms**
    - **subcode 01** (ออกเกม, กด 01:47:20 รอบบูตที่สอง): dialog ปิด → **หน้าต่างไม่ปิดตัวเอง**
      ยังอยู่ในแมพ ไม่ค้าง — เหมือน 03 ทุกประการ
    - ทั้งสองรอบ ออกจริงด้วย X + ยืนยัน = ปิดสะอาดปกติ (ไม่ต้อง End task)
  - **ชั้น wire/DB (job 088 ×2):** ack `HYP_PF_013_LOGOUT_SUBCODE03/01_ACK_THEN_SERVER_SOCKET_CLOSE`
    46B ยิงตรงเวลากดทั้งคู่ (late 0.3ms) · sessions ปิดครบ open=0 · canonical ไม่ถูกแตะเพิ่ม
  - **สรุปสำหรับ chief:** client **ไม่ตรวจจับ socket ปิดเลยแม้แต่น้อย** (ไม่มี transition,
    ไม่มี error, world วิ่งต่อ) → transition ของ client ไม่ถูกขับด้วยชั้น TCP — ต้องเป็น
    **response เฟรมในโปรโตคอลที่ client รู้จัก** → เดินหน้า fallback 0x3D4B-first ตามดีไซน์ ledger
  - nonclaims: ไม่พิสูจน์ multi-cycle · ไม่พิสูจน์ shape อื่น · จอขาววูบ = สังเกตการณ์ยังไม่รู้เหตุ


## [C] GT-009 (PASS — ประมวลแล้วรอบ 52)


## GT-009 HYP-PF-014 chat echo: พิมพ์แชทแล้วข้อความโผล่ในหน้าต่างแชทไหม เมื่อ server echo กลับ  [PASS] ✅ 2026-08-18 01:50–01:59 attended — **ข้อความแชทแรกที่ render บนจอในประวัติศาสตร์โปรเจกต์**

- objective: (claim เดียว — ชั้น client-observable เท่านั้น) เมื่อ server echo เฟรม chat
  `UNKNOWN_0xAC52` กลับใน envelope Res (HYP-PF-014) — **client render ข้อความในหน้าต่างแชทหรือไม่?**
  ชั้น wire พิสูจน์แล้ว headless (sandbox smoke: echo byte-exact 66B ต่อทุกข้อความ ทันที ~1.5–9.5ms ·
  ไม่ one-shot · DB ไม่ขยับ · report `PF_CHAT_ECHO001_CHAT_INPUT_ECHO_HYPOTHESIS_HEADLESS_20260817.md`)
  — **อย่าเทสซ้ำชั้น wire อย่านับเป็นเกณฑ์**
- db: สำเนา canonical สด (090 copy + เช็ค sha `FA794D0B..4400` อัตโนมัติ — เช็คกับค่าใน LOCK ก่อนรัน)
- server args: (090 จัดให้ครบ) บูตตรง + `--chat-input-hypothesis-scenario
  scenarios\chat_input_hypothesis_echo.json` (console บรรทัด scenario ต้องเขียน `chat_input_hypothesis_echo`)
- ⚠️ ข้อจำกัดเชิงบูต: scenario flags เป็น **mutually exclusive** — logout ack (GT-008) จะ**ไม่ทำงาน**
  ในรอบนี้ → ออกเกมด้วย **End task เท่านั้น** (พฤติกรรมค้างแบบยุค GT-006 = expected ไม่ใช่ผลเทสนี้)
- steps:
  1. ย้ายหน้าต่างเกมไปฝั่งซ้ายของจอ**ก่อนเริ่ม** (บทเรียน GT-007: หน้าต่าง Claude บังปุ่ม)
  2. run staged `090_gt009_boot.ps1` (boot server chat_echo + เปิดเกม) → PLAYBOOK ข้อ 3–6 เข้าแมพ
  3. **คลิกช่องแชทก่อนทุกครั้ง** (บทเรียน GT-006: focus หลุดหลังส่ง) → พิมพ์ **`PFCHATPROBE1`**
     (ต้อง 12 ตัวอักษร ASCII เป๊ะ — scenario รับเฉพาะ shape 12 ตัว printable) → Enter
  4. สังเกต ~10 วิ: ข้อความโผล่ในหน้าต่างแชทไหม? รูปแบบไหน (ชื่อผู้พูด/สี/channel)? ช่อง input เคลียร์ไหม?
     — บันทึกทุกกรณี · ถ้าไม่โผล่: บันทึกว่า UI นิ่งเฉยหรือมีอาการอื่น (error/หลุด/ค้าง)
  5. re-click ช่องแชท → พิมพ์ **`PFCHATPROBE2`** → Enter → สังเกตซ้ำ (ยืนยัน echo ไม่ one-shot ที่ชั้น UI)
  6. re-click ช่องแชท → พิมพ์ข้อความ 12 ตัวอื่น เช่น `PFCHATPROBE9` → Enter → สังเกต (ยืนยัน shape-pin
     ไม่ใช่แค่ 2 ข้อความที่ตรึง hash) · ของแถมถ้าสะดวก: ลองข้อความสั้น/ยาวกว่า 12 ตัว — คาดว่า server
     เงียบ (fail closed) client ไม่ echo — บันทึกเฉย ๆ ไม่ใช่เกณฑ์
  7. ออกเกมด้วย **End task** (ดู ⚠️ ด้านบน) → run staged `091_gt009_teardown.ps1`
     (เก็บ GAME_LIVE/EVENTS + DB + ยืนยัน canonical ไม่ขยับ)
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** ข้อความที่พิมพ์ปรากฏในหน้าต่างแชทหลัง Enter (อย่างน้อย PROBE1+PROBE2)
    โดยไม่ crash/หลุดจากแมพ — บันทึกรูปแบบ render เป๊ะ ๆ (ภาพหน้าจอถ้าทำได้) · **ถ้า client เงียบ
    ทั้งที่ wire echo แล้ว = falsify shape "echo เฉย ๆ"** → บันทึกละเอียด (นี่คือข้อมูลออกแบบรอบถัดไป
    เช่น ต้องมี speaker id/prefix อื่น) ไม่ใช่แค่ FAIL เฉย ๆ
  - **wire-DB (ยืนยันซ้ำเฉย ๆ ผ่าน 091):** `HYP_PF_014_CHAT_INPUT_ECHO_ASCII12` ใน GAME_LIVE ·
    echo frame 66B หลังทุก Enter · DB run copy ไม่มี write เพิ่มช่วงแชท · canonical sha ไม่เปลี่ยน
- nonclaims: ไม่ claim ความหมาย prefix 10B · ไม่ claim ความยาวอื่นนอกจาก 12 ตัว · ไม่ claim non-ASCII/ไทย ·
  ไม่ claim channel/whisper/broadcast/multi-client · ไม่ claim ว่า server เดิม echo แบบนี้ (ไม่มี golden) ·
  ไม่ claim persistence ข้อความ · ผล client-เงียบ = falsify เฉพาะ shape echo → chief เปิด entry ใหม่
- result: ✅ **PASS ทุกเกณฑ์หลัก — client render ข้อความที่ server echo กลับจริง**
  attended 01:50–01:59 · jobs `090`→`091` · สำเนา DB gt009_20260818_015036
  - **ชั้น client-observable (ตาเห็นจริง):**
    - `PFCHATPROBE1` (พิมพ์+Enter ~01:54): **โผล่ในหน้าต่างแชทเป็น `[ทั่วไป] : PFCHATPROBE1`**
      ตัวอักษรขาว · มี channel tag `[ทั่วไป]` นำหน้า · **ไม่มีชื่อผู้พูด** · ช่อง input เคลียร์หลังส่ง
    - `PFCHATPROBE2` และ `PFCHATPROBE9` โผล่ตามแบบเดียวกันครบ → **echo ไม่ one-shot
      และ shape 12-ASCII ทั่วไปใช้ได้ ไม่ใช่แค่ค่าที่ตรึง hash**
    - fail-closed ฝั่ง UI: ข้อความ 5 ตัว (`SHORT`) พิมพ์+Enter → **เงียบ ไม่ echo ไม่ error** ✓
      (ข้อความยาว 18 ตัวลองพิมพ์ผ่าน clipboard — ไม่ยืนยันว่าเข้าช่องจริง ไม่นับเป็นหลักฐาน)
    - ไม่มี crash/หลุดแมพตลอดเทส · ออกเกมด้วย End task ตามสเปก (Panya กด 01:58)
  - **ชั้น wire/DB (job 091):** listeners 0 · open sessions 0 · canonical ไม่ถูกแตะ ·
    รายละเอียดเฟรม echo อยู่ใน capture_gt009_20260818_015036 (chief ตรวจตามสบาย)
  - **สรุปสำหรับ chief:** shape "echo ใน envelope Res" **เพียงพอให้ client render** —
    HYP-PF-014 ผ่าน client acceptance · ข้อมูลออกแบบต่อ: channel tag มาจากไหน (client เอง
    หรือ envelope?) · speaker name ไม่แสดง — ถ้าอยากได้ต้องหา field เพิ่ม
  - nonclaims: ไม่พิสูจน์ non-ASCII/ไทย · ความยาวอื่น · channel/whisper · multi-client ·
    persistence ข้อความ · ไม่รู้ semantics ของ prefix 10B


## [D] GT-010 (FAIL⭐ — ประมวลแล้วรอบ 52)


## GT-010 HYP-PF-015 delete character: กดปุ่มลบตัวละครที่หน้า char select แล้ว client ทำงานกับ soft delete + ช่องว่างจริงไหม  [FAIL — client ปฏิเสธ response (ErrorData=28317) · แต่ได้รางวัลหลักครบ: natural 0x36DB แรก + รู้แล้วว่า request envelope ถูก/response envelope ผิด] ❌⭐ 2026-08-18 01:59–02:06 attended

- objective: (claim เดียว — ชั้น client-observable เท่านั้น) เมื่อกดปุ่มลบตัวละคร + ยืนยัน dialog ที่หน้า
  char select — **client ส่งเฟรมอะไร แล้วรับ echo ack ของ server (HYP-PF-015) ได้ไหม? ช่องว่างจริงไหม?**
  ชั้น wire/DB พิสูจน์แล้ว headless (DELETE-SOFT-001: ack byte-exact · deleted_at commit ก่อน ack ·
  cycle สร้าง→ลบ→สร้างซ้ำช่องเดิมผ่านจริงบน TCP · report `PF_DELETE_SOFT001_SOFT_DELETE_REUSE_HEADLESS_20260818.md`)
  — **อย่าเทสซ้ำชั้น wire อย่านับเป็นเกณฑ์**
- ⭐ **ข้อสำคัญที่สุดของเทสนี้: corpus ไม่เคยมี 0x36DB wire จริงเลย** (DELETE003 negative) — envelope ที่
  server รับ (GSCN_LoginProtocol one-vital) เป็น**ดีไซน์เดา** → ไม่ว่าผลจะ PASS หรือ client เงียบ/ค้าง
  **capture ที่ได้คือ natural 0x36DB แรกของโปรเจกต์** = คำตอบว่าดีไซน์ envelope ถูกหรือต้องแก้ —
  เก็บ capture ให้ครบทุกกรณี นี่คือรางวัลหลักแม้เทส "FAIL"
- db: สำเนา canonical สด (097 copy + เช็ค sha กับค่าใน LOCK ก่อนรัน) — **สำเนาจะโดน migration 004
  ตอนบูต (partial unique indexes) = expected** · canonical ต้องไม่ขยับ (เทสทั้งหมดอยู่บนสำเนา)
- server args: (097 จัดให้ครบ) บูตตรง + `--delete-actor-hypothesis-scenario
  scenarios\delete_actor_hypothesis_soft_delete.json` (console ต้องเขียน mode `delete-actor-hypothesis`)
- ⚠️ mutually exclusive: logout ack (GT-008) ไม่ทำงานในรอบนี้ → ออกเกมด้วย **End task เท่านั้น**
- ⚠️ เทสนี้**ลบที่หน้า char select ก่อนเข้าแมพ** — ไม่ต้องเข้า world เลย (ลบ = ตัวที่ยังไม่ selected เท่านั้น;
  server จะ fail closed ถ้าตัวถูก select อยู่)
- steps:
  1. ย้ายหน้าต่างเกมฝั่งซ้าย**ก่อนเริ่ม** (บทเรียน GT-007) → run staged `097_gt010_boot.ps1`
  2. login ผ่านหน้า LOGIN → ถึงหน้า character select (มีตัวละครเดิม 1 ตัวจาก canonical copy) — **หยุดตรงนี้ ไม่กด Start**
  3. กดปุ่ม**ลบตัวละคร**บนตัวละครนั้น → บันทึกว่า dialog ยืนยันหน้าตาแบบไหน ต้องพิมพ์อะไรไหม
     (static DELETE003: producer op1 แนบ wstring จาก UI — คาดว่าเป็นช่องพิมพ์ยืนยัน เช่น ชื่อตัวละคร)
  4. **กดยืนยันจริง** (เราอยู่บนสำเนา DB — ปลอดภัย) → สังเกต ~10 วิ: ตัวละครหายจาก list ไหม? ช่องว่างไหม?
     มี error/ค้าง/dialog ไม่หายไหม? — บันทึกทุกกรณีละเอียด
  5. ถ้า list ว่าง/ช่องว่าง: กด**สร้างตัวละครใหม่**ลงช่องเดิม ตั้งชื่อใดก็ได้ → สังเกตว่าสร้างผ่านไหม
     กลับมาโผล่ใน list ไหม (นี่คือ reuse ชั้น UI — ชั้น DB พิสูจน์แล้ว)
  6. ออกเกมด้วย **End task** → run staged `098_gt010_teardown.ps1` (เก็บ capture + เช็ค DB copy:
     deleted_at, แถวใหม่ selector เดิม, children เดิมอยู่ครบ + ยืนยัน canonical ไม่ขยับ)
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** หลังยืนยันลบ ตัวละครหายจาก list โดยไม่ crash + (ถ้าทำ step 5)
    สร้างใหม่ลงช่องเดิมได้และโผล่ใน list — บันทึกรูปแบบ UI ทุกจังหวะ (ภาพหน้าจอถ้าทำได้)
  - **wire-DB (ยืนยันซ้ำเฉย ๆ ผ่าน 098):** `HYP_PF_015_DELETE_ACTOR` marker ใน GAME_LIVE ·
    DB copy: แถวเดิม deleted_at ไม่ null · แถวใหม่ (ถ้าสร้าง) selector/identity เดิม · canonical sha ไม่เปลี่ยน
  - **ถ้า client เงียบ/dialog ค้าง = server ไม่ match เฟรมจริงของ client** → นี่คือ falsification ของ
    envelope ดีไซน์ → **เก็บ capture แล้วจดตำแหน่งเฟรม 0x36DB (หรือเฟรมแปลกหลังกดยืนยัน) ให้ chief**
    = ข้อมูลออกแบบรอบถัดไป ไม่ใช่แค่ FAIL
- nonclaims: ไม่ claim ความหมาย op 1/2 · ไม่ claim wstring ในเฟรม · ไม่ claim ว่า server เดิมตอบแบบนี้
  (ไม่มี golden) · ไม่ claim restore/undelete · ไม่ claim การลบตัวที่ select อยู่ (fail closed by design) ·
  ไม่ claim hard delete — ประวัติอยู่ใน DB เสมอ
- result: ❌⭐ **FAIL ตามเกณฑ์ — แต่ได้คำตอบ envelope ครบทั้งสองทิศตามที่สเปกหวัง**
  attended 01:59–02:06 · jobs `097`→`098` · สำเนา DB gt010_20260818_015927
  - **ชั้น client-observable (ตาเห็นจริง — flow การลบที่ไม่เคยมีใครเห็น):**
    1. ปุ่มลบที่หน้า char select = **ปุ่มแรกซ้ายสุด** ("ลบตัวละคร") — 🔴 **โน้ตเก่าใน PLAYBOOK
       ที่ว่า "ปุ่มที่ 2 จากซ้าย = ลบ" ผิด/ล้าสมัย: ปุ่ม 2 คือ "สร้างตัวละคร"** (ยืนยันด้วย zoom)
    2. กดลบ → dialog ยืนยัน **แบบ ใช่/ไม่ ธรรมดา ไม่มีช่องพิมพ์ชื่อ** (ต่างจากที่ DELETE003 เดา)
    3. ยืนยัน → **dialog รหัสผ่านขั้นที่สอง พร้อมคีย์บอร์ดสุ่มบนจอ** (anti-keylogger pad) —
       พิมพ์ด้วยคีย์บอร์ดจริงได้ ใส่ `test` → ยืนยัน
    4. → **client เด้ง error dialog (Windows-style ข้อความจีน):**
       `網路 protocol 讀取失敗 --- GSCN_RunTimeProtocolRes ErrorData=28317 請洽程式設計人員`
       → กด OK → **ตัวละคร Arena01 ยังอยู่ใน list เหมือนเดิม** (ฝั่ง client ลบไม่เกิด)
    5. ไม่ทำ step สร้างซ้ำ (ลบฝั่ง client ไม่สำเร็จ + สถานะ DB แตกแยกแล้ว — ดูข้างล่าง)
    6. หมายเหตุ: X ที่หน้า char select ปิดหน้าต่างทันที **ไม่มี dialog ยืนยัน** (ต่างจากตอนอยู่ในแมพ)
  - **ชั้น wire/DB (job 098 + ผู้เทสอ่านสำเนา DB ซ้ำ):**
    - server ยิง ack `HYP_PF_015_DELETE_ACTOR_SELECTOR00_SOFT_DELETE_COMMITTED` 77B ที่ 02:04:21.729
    - **DB สำเนา: Arena01 `deleted_at = 02:04:21.690` = server soft delete สำเร็จก่อน ack ตามดีไซน์**
      · integrity ok · canonical ไม่ถูกแตะ (`D08A89BF..08E2` เดิม ณ จุดนั้น)
    - ⭐ **ข้อสรุปสองทิศ:** ทิศ request: **envelope ที่เดาไว้ถูกต้อง** — server parse 0x36DB ได้
      และลงมือทำจริง · ทิศ response: **envelope ผิด** — client parse ไม่ได้ (28317) →
      เกิด **state divergence**: server ลบแล้ว / client ไม่รู้ — ถ้าเป็น DB จริงผู้เล่นจะงงตอน login ถัดไป
    - natural 0x36DB แรกของโปรเจกต์อยู่ใน `capture_gt010_20260818_015927\` — chief decode
      เทียบกับดีไซน์เพื่อออกแบบ response envelope ใหม่ (คาดว่า client ต้องการ Res คนละชนิด
      กับ GSCN_RunTimeProtocolRes หรือ ErrorData field ต้องเป็นค่าอื่น)
  - nonclaims: ไม่พิสูจน์ reuse ชั้น UI (ไปไม่ถึง) · ไม่ claim ความหมาย 28317 (chief decode) ·
    ไม่พิสูจน์ว่า password ขั้นสองถูกตรวจฝั่งไหน (server bypass อยู่ — pad อาจเป็นของ client ล้วน)


## [E] GT-001 — spec เก่า + ผลทุกครั้งที่ผ่านมา (ครั้งที่ 1–3) + โน้ต re-arm 35/38/39/41


## GT-001 Smoke: full-loop บน canonical DB หลังทุก commit สำคัญ  [PASS] ✅ 2026-08-18 02:07–02:11 ที่ HEAD `005b3d4` (รอบใหญ่ #2)

> ✅ **result รอบใหญ่ #2 (ครั้งที่ 3 ของโปรเจกต์):** ผู้ขับ: เซสชันหลัก · jobs `072`→`073`
> - client-observable: full loop ครบ → เข้าแมพเห็นครบ HP 100/100 · minimap · Port Royal ·
>   **X:-8,094 Y:-3,207 (persist เดิมเป๊ะ)** · chat online → ออกสะอาด X+ยืนยัน
> - wire/DB (073): stopped ×1 · stderr 0B · listeners 0 · sessions 5→**6** · lease 5→**6** ·
>   backpack `[1@0,2@1,4@3]` เดิม · position ไม่ขยับ · integrity ok
> - ⚠️ **canonical sha ใหม่ = `B5557E9F3874BFA452B14A01495C4F7E0EA8176AF9C14BE09CF66865A597C9ED`**
>   (เปลี่ยนจากแถว session — migration 004 apply ไปก่อนแล้วตอน 01:22 ระหว่าง gate รอบ 51
>   ดูหมายเหตุใน GT-008 result · sha ที่ 072 gate เจอก่อนรัน = `D08A89BF..08E2`)
> - 👁️ observation ตามใบสั่ง: `TeleportVital` ใน GAME_LIVE = **1 บรรทัดตามคาด** (ไม่มี echo ที่สอง) ·
>   ไม่พบ gift UI ค้าง/popup แปลกทั้ง 4 เทสคืนนี้
> - nonclaims: ไม่พิสูจน์ inventory/combat/movement รอบนี้ · path delete/logout/chat แยกพิสูจน์ใน GT-008/009/010

*(header เดิมก่อนรัน: re-armed ที่ `005b3d4` (รอบ 51 แตะ src/: PF-015 soft delete — opt-in ล้วน + migration 004 ซึ่ง**จะ apply ลง canonical ตอนบูต GT-001**) · staged `072/073` ใช้ได้เดิม · ⚠️ **canonical sha จะเปลี่ยนหลังบูตแรกที่ HEAD นี้เพราะ migration 004 — expected ไม่ใช่ความผิดปกติ ให้จด sha ใหม่ลง result + LOCK** (sha ก่อนรัน = `FA794D0B..4400` เดิม) · PASS ล่าสุด 19:20–19:24 ที่ `b90007e`] 🔁

> 📌 **โน้ต re-arm รอบ 43:** การเปลี่ยน src เป็น opt-in ล้วน (scenario ack_close ใหม่ ไม่ใส่ธง =
> พฤติกรรมเดิมเป๊ะ — เทส PF-012 เดิมผ่านครบไม่แตะ) ดังนั้นความเสี่ยง regression ต่ำ ·
> รันหลัง GT-008 ก็ได้ในรอบใหญ่เดียวกัน (server คนละ boot อยู่แล้ว)

> ✅ **result รอบใหญ่ 19:2x (ครั้งที่ 2 ของวัน — re-armed หลัง M4+item14+HYP-PF-012 แตะ src):**
> ผู้ขับ: เซสชันหลัก · jobs `072`→`073` (staged ของรอบ 39) · **PASS ทุกเกณฑ์ที่ `b90007e`**
> - client-observable: server select → PVP → char select (Arena01/Port Royal) → ปุ่มกลาง →
>   WANTED → **เข้าแมพครบ: HP 100/100 · minimap · Port Royal · X:-8,094 Y:-3,207 (= persist
>   จาก GT-005 เป๊ะ อีกครั้ง) · chat online** → ออกสะอาด X ครั้งเดียว → ยืนยัน
> - wire/DB (073): Ctrl+C ครั้งแรกสำเร็จ · stopped ×1 · traceback 0 · stderr 0B · listeners 0 ·
>   GameClient 0 · sessions 4→**5** · blank 0 · open 0 · lease 4→**5** · backpack `[1@0,2@1,4@3]`
>   ไม่เปลี่ยน · position ไม่ขยับ (ไม่ได้เดิน) · integrity ok · fk ว่าง
> - ⚠️ **canonical sha เปลี่ยนโดยคาด (session ใหม่):** `CACE7F77..F493` →
>   **`FA794D0B1B69C6DCF0C7BCF0869FBEDC18138890C623547275952B3FEFE14400`**
>   (backup ก่อนเทส: `backup\pirateforce_before_gt001_20260817_192033.sqlite3`) —
>   job ที่ gate ด้วย CANON_SHA ต้องอัปเดต
> - nonclaims: ไม่พิสูจน์ inventory/combat/movement รอบนี้ · หมายเหตุ: บูตมาตรฐานไม่มีธง logout
>   (path HYP-PF-012 ไม่ถูกแตะในเทสนี้ — แยกไปพิสูจน์ใน GT-007)
> - 📍 ประมวลผลรอบ 42: report `reports/PF_GT001_POST_HYP012_CANONICAL_FULL_LOOP_SMOKE_RUNTIME_PASS_20260817.md`
>   (+manifest 13 ไฟล์ รวม backup ก่อนเทส) · **commit `b03d207`** (docs-only → **ไม่ re-arm** —
>   GT-001 คง [PASS] จนกว่า commit ถัดไปแตะ src/ เช่น HYP-PF-013)

> 🔁 **re-arm รอบ 35 (2026-08-17 16:1x):** ผล PASS เดิม (14:31–14:39 ที่ `abf3696`) ยังเป็น
> หลักฐานใน repo (commit `c778535`) แต่ M4 แก้ `runtime.py` +106 บรรทัดในเส้นทาง ItemOperate
> และ item-14 แตะ `store.py` → ต้องเทสซ้ำที่ HEAD **`55c7c59`** ตามกติกา recurring ข้างล่าง
> รันต่อท้าย GT-002 ในเซสชันเกมเดียวกันได้ (ประหยัดเวลาแบบรอบ 24)
> 📍 **อัปเดตรอบ 38 (17:55–18:1x):** GT-002 ปิดแล้ว — GT-001 ยืนเดี่ยว · HEAD ปัจจุบัน
> **`f0e0ac6`** (`b1087bb`+`f0e0ac6` docs-only ไม่ re-arm เพิ่ม — เหตุ re-arm ยังคือ
> `4c29a63`+`55c7c59`) → เทสที่ HEAD ปัจจุบันได้เลย · **jobs 072/073**: copy แบบจาก
> `done\060_gt001_boot.ps1` / `done\061_gt001_teardown.ps1` เปลี่ยนเลข+timestamp
> ⚠️ บทเรียน 27.2: อาร์กิวเมนต์ path ทุกตัวต้อง quote (โฟลเดอร์มี space) และ
> snapshot fail ใน job ≠ เทส fail — ดูหลักฐานจริงก่อนเสมอ · canonical sha ปัจจุบัน
> = `CACE7F77..F493` (ค่าใน gate ของ job ต้องใช้ตัวนี้)
> 📍 **อัปเดตรอบ 39 (18:1x): jobs 072/073 เขียนเสร็จแล้ว — วางที่
> `pf_bridge\staged\072_gt001_boot.ps1` / `staged\073_gt001_teardown.ps1`**
> · sha gate ในไฟล์ = `CACE7F77..F493` (ค่าปัจจุบัน) แล้ว · quote path ทุกอาร์กิวเมนต์
> ที่ส่งให้ native command ตามบทเรียน 27.2 แล้ว (`"$uri"`, `-CaptureRoot "$captureRoot"`,
> helper `.py`, `--json`) · 073 ชี้ parse `072_client_info_*` แล้ว
> → **รอบใหญ่แค่ copy สองไฟล์นี้ลง inbox (073 ต่อคิวหลัง 072 ตามกฎ R31) ไม่ต้องแก้อะไรอีก**
> ถ้า canonical sha เปลี่ยนก่อนถึงรอบใหญ่ (มีเทสอื่นเขียน DB) ให้แก้ `$expectedSha` ใน 072 ก่อนใช้
> 📍 **re-arm ซ้ำรอบ 41 (19:1x): commit `b90007e` แตะ src/ (runtime.py+app.py+logout_hypothesis.py)**
> → เทสที่ HEAD **`b90007e`** · canonical sha **ไม่เปลี่ยน** (`CACE7F77..F493` — jobs 076/077
> ใช้สำเนา) → staged 072/073 ใช้ได้เหมือนเดิมไม่ต้องแก้ · ความเสี่ยง regression ต่ำ:
> ทางใหม่ทั้งหมดอยู่หลังธง scenario ที่ GT-001 ไม่ใช้ (boot ปกติ = dispatch เดิมเป๊ะ
> พิสูจน์ด้วย test_without_scenario_nothing_changes + suite 415/0)
- objective: ยืนยันว่า commit ล่าสุดบน main ไม่ทำให้ loop พื้นฐานพัง
  (login → select → เข้าแมพ → ออก → server exit 0)
- db: `state\pirateforce.sqlite3` (ค่าเริ่มต้น)
- server args: `-SecondPasswordMode bypass`
- steps: ตาม PLAYBOOK ทั้ง 8 ข้อ
- pass criteria: เข้าแมพเห็นครบ (HP/minimap/ชื่อแมพ/chat online) + ออกสะอาด +
  server/shim exit 0 + stopped marker ×1 + stderr 0B + DB integrity ok +
  backpack ไม่เปลี่ยน `[1@0,2@1,4@3]` + session เปิด-ปิดครบ
- nonclaims: ไม่พิสูจน์ inventory move, combat, persistence ข้าม restart
- **commit ที่ต้องเทสรอบนี้: `eef51fa`** (HEAD ปัจจุบัน) — commit ล่าสุด 10 ตัว
  (`327bfe9`, `4a19e5d`, `966d0b6`, `07a3a21`, `896f715`, `04b7c6c`, `ccca72a`,
  `31494fe`, `83023a8`, `eef51fa`) **ไม่แตะ `src/` เลยแม้แต่ไฟล์เดียว**
  → ความเสี่ยง regression ต่ำมาก ทำ GT-005 ก่อนได้ ถ้าเวลาจำกัดให้ข้าม GT-001
  (T3 บน Windows PASS **384 tests** exit 0 ที่ 07:19 หลัง commit `eef51fa`)
  ⚠️ หมายเหตุ 14:3x: ข้อความ "commit ที่ต้องเทส = eef51fa" ข้างบน **ล้าสมัยแล้ว** —
  รอบ 31 landing M3/HYP-PF-010 เป็น `abf3696` แตะ `src/` 5 ไฟล์ → recurring rule ทำงาน
  และรอบเทสนี้เทสที่ HEAD `abf3696` เลย (คุ้มกว่า: ครอบ WIP ที่เพิ่ง landed ด้วย)
- result: ✅ **PASS ทุกเกณฑ์ — attended session 2026-08-17 14:31–14:39 ที่ HEAD `abf3696`**
  ผู้ขับ: เซสชันหลัก (Claude ผู้เทส · granted tier full 14:34 ขณะหน้าต่างเกมเปิด ·
  Panya หน้าเครื่อง) · jobs `060`→`061` (teardown วางต่อคิวใน inbox ก่อนตามกฎ R31)
  - **ชั้น client-observable (ตาเห็นจริงทุกจุด):**
    - server select 'Pirate Force Local' + Channel 1 → เข้า → dialog PVP → ยืนยัน
    - char select: Arena01 + nameboard (โชว์ 'Port Royal' = ตำแหน่งที่ persist ไว้) → ปุ่มกลาง
    - loading WANTED ~30 วิ → **เข้าแมพเห็นครบ: HP 100/100 · LV.1 · minimap ·
      ชื่อแมพ Port Royal · chat '[ระบบ] : Pirate Force local server online'**
    - พิกัดมุมจอตอนเกิด **X:-8,094 Y:-3,207 = ค่า persist จาก GT-005 เป๊ะ**
      → ของแถม: position persistence ยืนยันซ้ำบน HEAD ที่มี M3 landed
    - ออกสะอาด: X ครั้งเดียว → dialog ยืนยัน → ปุ่มซ้าย → หน้าต่างปิดปกติ
  - **ชั้น wire/DB (job 061 หลัง window ปิด):**
    - Ctrl+C สำเร็จครั้งแรก (helper exit 0) · server/shim exited=True
      (ExitCode อ่านเป็นค่าว่างเหมือน 057 — ตัดสินจาก markers แทน) ·
      stopped ×1 · ready ×2 · traceback 0 · **stderr 0B** · listeners 0 · GameClient 0
    - sessions with char 3→**4** (+1 ตามคาด) · blank-conn 0 · open 0 ·
      lease_generation 3→**4** · integrity ok · fk ว่าง ·
      **backpack [1@0,2@1,4@3] ไม่เปลี่ยน** · position row ไม่ขยับ (ตั้งใจไม่เดิน)
    - backup ก่อนเทส: `backup\pirateforce_before_gt001_20260817_143122.sqlite3`
      (sha ตรง canonical เดิมก่อน copy — gate ผ่าน)
  - ⚠️ **canonical sha เปลี่ยนโดยคาด** (แถว sessions ใหม่):
    เดิม `F37BEFE6..95C8` → ใหม่ `CACE7F7755E79AF0C2E637BC6C09C131E6152436F3141E136BC457ECA74DF493`
    → job ใดที่ gate ด้วย CANON_SHA ต้องอัปเดตค่าใหม่ก่อนใช้
  - หลักฐาน: `GameClient\capture_gt001_20260817_143122\` (console 49,167B ·
    GAME_LIVE.txt 30,713B · GAME raw 204,178B · LOGIN raw 2,326B · GAME_EVENTS_LIVE 1,064B)
    + `outbox\060_gt001_boot.utf8.txt` / `061_gt001_teardown.utf8.txt` / `061_console_tail_*.txt`
  - ข้อสังเกตไม่ตีความ: `TargetPos mentions ใน console = 6` ทั้งที่ไม่ได้เดินเลย
    (GT-005 ตอนเดินจริงได้ 29) → เลข mention ฐานของ boot+entry ไม่ใช่ศูนย์
    อย่าใช้ "mentions > 0" เป็นหลักฐานการเดินในเทสหน้า
  - nonclaims: ไม่พิสูจน์ inventory move (path M3 ที่เพิ่ง landed ยังไม่มีอะไรเรียก — M4 hookup
    ยังไม่มา), ไม่พิสูจน์ combat, ไม่พิสูจน์ movement/persistence รอบนี้ (ไม่ได้เดิน)
- ประมวลผลรอบ 33 (2026-08-17 15:1x): report
  `reports\PF_GT001_POST_M3_CANONICAL_FULL_LOOP_SMOKE_RUNTIME_PASS_20260817.md`
  (+`.manifest` 12 ไฟล์, Grade B runtime pass) — commit **`c778535`**
  (commit รอบนี้ไม่แตะ `src/` → recurring ไม่ re-arm สถานะคง [PASS])
- หมายเหตุ: รายการนี้เป็น recurring — หลัง chief-continue commit อะไรที่แตะ
  src/ ให้ตั้งกลับเป็น PENDING พร้อมระบุ commit hash ที่จะเทส
