# ka1-A — R311 ผล: **GT-184 และ GT-186 ผลลบทั้งคู่** — ปุ่ม "กลับหน้าเลือกตัว" และ "ออกจากเกม" จอไม่เปลี่ยน ไม่มีข้อความ 90 วิ · **และ finding สำคัญ: "dialog-open push" (0x709E) ของสถานการณ์ทดสอบ ไม่เคยออกจากเซิร์ฟเวอร์เลย** — GetWorldInfo แบบเต็มได้ตอบกลับ 0 ไบต์ เซิร์ฟตอบแค่ ACK + ปิด socket แบบเดิม

**ADDRESSEE: LANE-UI** (เจ้าของ UI-A/UI-B ตาม 0330) · cc: chief · COO · LANE-A (เดิม)
**รอบ:** R311 2026-09-04 19:16-19:27 +07:00 · ผู้ขับ: Panya · ผู้วัด/เขียน: ka1-A
**บูต:** `pirate-force-server` **`55c9a05c30b9a5f6744b62b822d4b0ad2cdbb53f`** (newest green · main 3f41c103 ต่าง 11 ไฟล์) · **แฟล็กเดียว** `--logout-hypothesis-scenario scenarios\logout_hypothesis_dialog_open_push.json` (ตามหัวใบ GT-184: "Boot now with …") ยืนยันบน command line ของเซิร์ฟ (`SCENARIO_FLAG=present`) · DB สำเนา `run_gt184_20260904_191654` · Arena01
**jobs:** 1502 (abort เองที่ตัวเช็คแฟล็กของผม — นับ py.exe+python.exe เป็น 2) → 1502b boot · 1503 relaunch · 1504 teardown **PASS** (stopped ×1 traceback 0 listeners 0 client 0 · canonical sha ก่อน=หลัง `4FF37060…A548454` · integrity ok)
**capture:** `GameClient\capture_r311_20260904_191654\` · ภาพ `Data\ScreenShot\20260904_192129.png` (GT-184 +~110 วิ) · `192633.png` (GT-186 +~70 วิ)

## ลำดับบนสาย (เหมือนกันเป๊ะทั้งสองปุ่ม — คนละ subcode)
**GT-184 (session 1, 19:19):** client ส่ง `GetWorldInfoVital 0x3D4B` **แบบเต็ม 268 B** (`[G< #11]`) → **เซิร์ฟไม่ตอบอะไรเลย** → 1.8 วิต่อมา client ส่ง `0x1B40` 34 B payload `08 03 08 00 14 00 00 00 00 14 00 00 00 00` (= LogoutVital **subcode 03** กลับหน้าเลือกตัว) → เซิร์ฟ `[G>] HYP_PF_013_LOGOUT_SUBCODE03_ACK_THEN_SERVER_SOCKET_CLOSE` 46 B แล้วปิด socket
**GT-186 (session 2, 19:25):** `GetWorldInfoVital` เต็ม 268 B (`[G< #9]`) → ไม่ตอบ → `0x1B40` payload `08 01 08 00 …` (**subcode 01** ออกจากเกม) → `[G>] HYP_PF_013_LOGOUT_SUBCODE01_ACK_THEN_SERVER_SOCKET_CLOSE` 46 B แล้วปิด socket
**ไม่มี `[G>]` เฟรมใดระหว่าง GetWorldInfo กับ ACK** (รายชื่อ `[G>]` ทั้งรอบ: LOGIN_VERIFY_ACK_ONCE, FOUNDATION_CHARACTER_LIST_ONCE, FOUNDATION_SELECTED_START_GAME, RUNTIME_RES_ACK_FIRST_REQ, V99/V100/V113, GM_UPDATE_STATE_AFTER_LOGIN, HYP_PF_013 ×2 — **ไม่มี 0x709E / dialog-open push เลย**) · `LANE_A_UIA_NOTICE_NOT_THIS_BOOT reason=logout_scenario_owns_the_frame effect=no_bytes_composed` ×2
⇒ **สถานการณ์ `worldinfo_dialog_open_push` ไม่ได้ผลิตไบต์ push** บนบิลด์นี้ — ที่วิ่งจริงคือกิ่งเดิม HYP-PF-013 (ack + close) · ผมไม่วินิจฉัยว่าเพราะ `production_allowed=false` ของ scenario, เพราะ wiring ใน runtime ยังไม่ครบ หรือเพราะเงื่อนไข trigger ไม่ตรง — LANE-UI ดูจาก `logout_dialog_open_hypothesis.py` เอง (pytest ของมัน 12 ผ่านในต้นไม้ที่บูต)

## client-observable (Panya · 90 วิ ทั้งสองปุ่ม)
- GT-184: กด "กลับหน้าเลือกตัวละคร" → **ไม่มีอะไรเปลี่ยน ไม่มีข้อความ** จนครบ 90 วิ (ภาพ 192129) → ปิดด้วย X ได้ปกติ
- GT-186: กด "ออกจากเกม" → **ไม่มีอะไรเปลี่ยน ไม่มีข้อความ** (ไม่มีแม้ EXIT REFUSED — สถานการณ์นี้ยึดเฟรม UI-B ไปจาก LANE-A) → เกมไม่ปิดเอง → ปิดด้วย X ได้ปกติ (ไม่ค้าง ไม่ต้อง End task)
- `OBSERVER_CONFIRMED: 2026-09-04T19:26+07:00`

## คำตัดสินที่เสนอ
- GT-184: **NEGATIVE / hypothesis not exercised** — ปุ่มไม่พาไปหน้าเลือกตัว **แต่** push ที่ใบตั้งใจทดสอบไม่ได้ถูกส่ง ⇒ ยังตัดสิน HYP-PF-040 ไม่ได้ · ต้องแก้ให้ push ออกจริงก่อนแล้วรันใหม่ (ผมพร้อม ~6 นาที)
- GT-186: เช่นเดียวกัน (subcode 01)
- สิ่งที่ยืนยันได้จริงรอบนี้: (1) ปุ่มทั้งสองส่ง GetWorldInfo เต็ม 268 B ก่อน แล้ว 0x1B40 subcode 03/01 ตามลำดับ (2) ACK+ปิด socket ฝั่งเซิร์ฟ **ไม่ทำให้ client เปลี่ยนหน้า/ปิด** — ตรงกับ GT-033 เดิม (3) client ไม่ค้างหลัง socket ปิด — X ใช้ได้

## nonclaims
① ไม่พิสูจน์ว่า 0x709E push จะทำงานถ้าถูกส่ง ② ไม่ตัดสิน HYP-PF-040 ③ ไม่แตะโค้ด ไม่ commit ④ ไม่ได้อ่านสีป้ายในสองภาพ (จอเมืองปกติ ไม่ใช่เป้าของใบ) ⑤ ไม่ได้ทดสอบ subcode อื่น

— ka1-A, 2026-09-04 19:31 +07:00
