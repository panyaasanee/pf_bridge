# GT-103 (steps 2a/2b) RESULT 2026-08-28 11:40 +07:00 — **ผลลบเข้ม: คลิก `BT_GM` เงียบสนิททั้ง 4 สถานะ UI** ⇒ สมมติฐาน "เปิด panel ให้ current-UI key ไม่ว่างแล้วจะเปิดได้" ของ RE-118 **ถูกหักล้างในระดับปฏิบัติ**

ถึง: **สาย GM (เจ้าของใบ · ADDRESSEE: LANE-GM)** · **RE runner (ADDRESSEE: RE)** · chief · cc COO, สาย A/B, กะ1-B
จาก: attended session "กะ1-A" (Panya ขับ UI เอง; brief -> "ทราบ" -> บูต) · OBSERVER_CONFIRMED: 2026-08-28T11:36-11:37+07:00 (คำเจ้าของ + คอนโซล) · **รอบนี้ไม่มีวิดีโอตามคำสั่งเจ้าของ** — หลักฐาน = คำเจ้าของ + คอนโซลเซิร์ฟเวอร์

## สถานะที่ควรเป็น
- **GT-103 = NO-RESULT ต่อ claim ของตัวเอง** (ไม่เคยถึงข้อ 3 ⇒ ไม่มีไฟล์ capture `0x51E9` ให้ตรวจ — `capture\gm_command_capture\` ABSENT ตามคาด ไม่ใช่ teardown fail)
- **RE-118 A/B (ข้อ 2b) = ทำครบและได้ผลลบที่มีค่าสูง** — ต้องเปิดใบ RE ใหม่ ทิศทางเปลี่ยน (ล่าง)

## บูต (jobs 1323 hold+resolve · 1324 boot · 1325 teardown กดโดยเจ้าของ 11:38 · 1326 release)
- BOOT_COMMIT **336857cd** = main HEAD (เขียวของตัวเอง run 33140147157) ไร้แฟล็ก
- ด่าน: **grep 9/9** (ชุด GM frame 5 + ชุด 0x51E9 path 4) + **pytest 2 ชุดผ่าน dispatcher จริง** — `test_gm_login_state_guard.py` 4 passed (ไบต์ตรงตัว) และ `test_gm_run_command_dispatch_wiring.py` 4 passed · code delta vs main = 0
- `PF_GM_ACCOUNTS_CONFIG=backup\gm_accounts_GT-103AB_20260828_112313.json` = `{"gm_accounts": ["localtest"]}` (ไฟล์แยก config จริงไม่แตะ) · DB สำเนา `run_gt103ab_20260828_113546` · **canonical UNCHANGED ก่อน/หลัง** · teardown PASS (listeners 0, clients 0, integrity ok, fk 0)
- คอนโซล `GameClient\capture_gt103ab_20260828_113546\server_console_live.out.txt` (3001 บรรทัด)

## 🔴 ของเสียที่พบในใบ GT-103 เอง (chief แก้ด้วย)
ด่าน 2 ของใบสั่ง `git grep "handle_gm_run_command_vital" -- src/pirateforce_foundation/runtime.py` — **ล้าสมัย** โค้ดย้ายออกจาก runtime.py ไป `lane_hooks/lane_gm_run_command.py` + `gm/dispatch.py` แล้วตั้งแต่ v6.3 lane_hooks move-out ⇒ ทำตามใบตรง ๆ จะได้ 0 hit และขึ้น **BLOCKED ทั้งที่ของอยู่ครบ** · กะ1-A เปลี่ยนเป็นด่านรูปแบบจริงหลังย้าย 4 ข้อ (ผ่านทั้งหมด): `GM_RUN_GM_COMMAND_VITAL_ID` ใน runtime.py (2 hit) · `def handle_gm_run_command_vital` ใน gm/dispatch.py:336 · `def capture_raw_gm_command` ใน gm/command_capture.py:116 · `production_allowed = True` ใน lane_hooks/lane_gm_run_command.py:34 — **ขอให้ chief แก้ด่าน 2 ในใบเป็นชุดนี้** ไม่งั้นรอบหน้าติดซ้ำ

## ชั้น client-observable (คำเจ้าของ คำต่อคำ)
> "เข้าไปยังไม่ทำอะไร กด gm > เงียบ , เปิด map ค้างไว้ กด gm > เงียบ , ปิด map กดเดินหนึ่งครั้ง เปิด กระเป๋าค้าง กด gm > เงียบ , ปิดกระเป๋า กด gm > เงียบ"

**เจ้าของทำมากกว่าที่ใบขอ — 4 สถานะ UI แทนที่จะเป็น 2:**

| # | สถานะ UI ตอนคลิก | ผล |
|---|---|---|
| A | HUD เปล่า ยังไม่ได้ทำอะไรเลยตั้งแต่เข้าแมพ | เงียบ |
| B | **หน้าต่างแผนที่ (M) เปิดค้าง** | เงียบ |
| B2 | **กระเป๋าเปิดค้าง** (หลังกดเดิน 1 ครั้ง) | เงียบ |
| A2 | ปิดกระเป๋าแล้วคลิกซ้ำ | เงียบ |

ไม่มีหน้าต่าง ไม่มีข้อความ ไม่มี error ในทุกกรณี

## ชั้น wire (คอนโซล)
- L199 `[G>] GM_UPDATE_STATE_AFTER_LOGIN (41 bytes; late=5.2 ms)` = `12 9D 6E 14 00000000 08 04 0B 02 12 01 00 12 19 5A 0B 00 | 0B 00 0B 01 14 00 00 00 00 | 0B 00` — **ไบต์ตรงกับรูปแบบที่พิสูจน์แล้วของ GT-101-R3 ทุกตัว**
- **ชนิดเฟรมขาเข้าตลอดรอบ:** `GSCN_RunTimeProtocolReq` 31 · `TargetPosVital` 3 · `GSCN_LoginProtocol` 3 · `UserSetting_UpdateServerSettingVital` 2 · `TeleportVital` 1 · `StartGameReq` 1 · `NotifyEnterCreateActor` 1 · `LoginVerifyVital` 1 · `CheckSecondPwdVital` 1 — **`0x51E9` = 0 · ไม่มีเฟรมชนิดใหม่ใด ๆ ในช่วงคลิกทั้งสี่ครั้ง**
- **ตัวควบคุมสำคัญ:** `TargetPosVital` ×3 ตรงกับ "กดเดินหนึ่งครั้ง" ของเจ้าของ ⇒ **client มีชีวิต รับอินพุตและส่งแพ็กเก็ตได้ตามปกติในช่วงเดียวกัน** — ไม่ใช่ client ค้าง ไม่ใช่ socket ตาย · เซสชันอยู่จนเจ้าของปิดเกมเอง (`[*] game client closed`)
- `capture\gm_command_capture\` **ABSENT** (ถูกต้อง: ไม่เคยมี 0x51E9 เข้ามา)

## 🔬 สิ่งที่ผลนี้แปลว่า (ข้อสำคัญที่สุดของใบ)
**สมมติฐานปฏิบัติของ RE-118 ("เปิด panel ที่ให้ current-UI key ไม่ว่างก่อน แล้วคลิกจะเปิดได้") ถูกหักล้างแล้ว** — เปิด panel สองชนิดต่างกัน (แผนที่, กระเป๋า) แล้วยังเงียบเหมือนกันทุกประการ

เหลือความเป็นไปได้สองทาง แยกให้ชัด:
1. **แผนที่/กระเป๋าไม่ได้ตั้ง "current UI" ในความหมายที่ handler อ่าน** (คือ key ยังว่างอยู่ดี) ⇒ สมมติฐานเดิมยังอาจถูก แต่วิธีทำให้ key ไม่ว่างยังไม่รู้
2. **จุดที่หยุดอยู่ก่อนหน้านั้น** — ไม่ใช่ current-UI key เลย

⇒ **ข้อเสนอของกะ1-A: ให้ RE ไล่ "ประตูบานแรก" ก่อน ไม่ใช่บานสุดท้าย** RE-118 T1 ระบุลำดับใน handler `0x0053B9B0` ไว้เอง 5 ขั้น และขั้นที่ **1** คือ `cmp source,[this+0x48]` — "ถ้าคอนโทรลที่ถูกคลิกไม่ใช่ตัวนี้ ออกเงียบ" · **RE-104 พิสูจน์ว่าปุ่ม `BT_GM` ถูก render/enable เมื่อ gate ผ่าน แต่ไม่เคยพิสูจน์ว่าปุ่มที่ render นั้นคือ control object เดียวกับที่ handler ตัวนี้จดทะเบียนไว้** — "ปุ่มที่วาดออกมา" กับ "แหล่งคลิกที่ handler ยอมรับ" อาจเป็นคนละ object และอาการจะเหมือนกันเป๊ะ (เงียบ ไม่มี log ไม่มี packet) นี่เป็นคำถาม **static ตอบได้** และถูกกว่าการ instrument runtime มาก

**ใบ RE ที่ขอเปิด (STATIC-ON-BRIDGE, ต่อจาก RE-118):** ① control object ที่ `[0x0053B9B0]` ใช้เป็น `this` คือใคร และ `this+0x48` ถูกตั้งค่าเมื่อไร/จากที่ไหน ② ปุ่ม `BT_GM` ที่ RE-104 พิน ถูกผูกกับ handler ตัวนี้จริงหรือกับ dispatcher ตัวอื่น ③ ถ้าไม่ใช่ตัวเดียวกัน — handler ที่ผูกกับ `BT_GM` จริงอยู่ที่ VA ไหน ④ (ถ้าข้อ 1-3 เคลียร์แล้วยังไม่พบ) จึงค่อยไปที่ `[0x01032EC4]` connection context และค่อยกลับมาที่ current-UI key ⑤ มีทางเข้าอื่นสู่ `GMUI_BASIC` ไหม (hotkey / double-click / คำสั่งแชท) — ถ้าเจอทางเข้าที่ถูกกว่า ข้ามเรื่องปุ่มไปเลยได้

## nonclaims
1. [ไม่อ้าง] ว่า current-UI key ว่างจริงหรือไม่ว่างจริงในรอบนี้ — เราวัด**พร็อกซี** ("มี panel เปิดค้าง") ไม่ได้วัดค่า key · RE-118 nonclaim ① ยังยืนอยู่
2. [ไม่อ้าง] ว่า panel ทุกชนิดในเกมให้ผลเหมือนแผนที่/กระเป๋า — ทดสอบสองชนิด ไม่ใช่ทั้งหมด
3. [ไม่อ้าง] ว่าเฟรม `0x5A19` มีอะไรผิด — ไบต์ตรงกับรูปแบบที่พิสูจน์แล้ว และปุ่มโผล่บนจอตามเดิม (gate `+0x19` ยังผ่าน)
4. [ไม่อ้าง] อะไรเกี่ยวกับ capture path ของ `0x51E9` — path นี้ยังไม่เคยถูกทดสอบ live เลย (GT-103 claim จริงยังค้าง รอทางเข้า GMUI)
5. [ไม่อ้าง] ว่า `this+0x48` คือสาเหตุ — เป็น**ลำดับการค้นที่เสนอ** ตามลำดับ gate ที่ RE-118 พินไว้เอง ไม่ใช่ข้อสรุป

## ต่อไป (เสนอ)
1. **สาย GM เปิดใบ RE ตามข้อ ①-⑤ ข้างบนในรอบถัดไปทันที** — และรายงานกลับในกล่องเมื่อปิดใบ **อย่าให้ค้าง 7 ชั่วโมงเหมือนรอบ RE-118** (ดูจดหมาย 1105)
2. **chief แก้ด่าน 2 ของใบ GT-103** เป็นชุด grep 4 ข้อหลัง lane_hooks move-out (ข้างบน) + ปรับหัวใบ GT-103 เป็น `[NO-RESULT ... A/B ทั้งสี่สถานะเงียบ, blocked on RE follow-up]`
3. **chief แก้หัวใบ RE-118** เพิ่มบรรทัดว่า BUILD_IMPACT A/B ถูกทำแล้วและให้ผลลบ (ใบยัง PASS/DONE ในส่วน static ของมัน — ที่ล้มคือ*คำแนะนำเชิงปฏิบัติ* ไม่ใช่ผล disasm)
4. คิว attended ที่พร้อมถัดไป: **GT-114 DIAG (Mountain Deer)** — wiring landed R202 แล้ว เจ้าของบูตได้ทันทีเมื่อพร้อม

## หลักฐาน
คอนโซล L199-201 (เฟรม GM 41B), ตารางชนิดเฟรมขาเข้าทั้งรอบ (0x51E9 = 0), L279/2929/2962 (TargetPosVital = client มีชีวิต), tail (`[*] game client closed` เจ้าของปิดเอง) · outbox\1323 (9 greps + pytest 4+4 passed) · outbox\1324 (ENV + GM_COMMAND_CAPTURE_EXPECTED_AT) · outbox\1325 (TEARDOWN PASS, GM_CAPTURE_DIR ABSENT, canonical unchanged)

— กะ1-A · **ADDRESSEE: RE (ใบใหม่ ①-⑤), LANE-GM (ข้อ 1), chief (ข้อ 2, 3)**
