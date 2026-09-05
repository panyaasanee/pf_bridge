# KA1A-R319-RESULTS — HYP-PF-040 = **FALSIFIED บนจอ**: บูตกิ่งทิ้ง e678a376 แล้ว push `0x709E` (ReturnSelectServerVital 48 B) **ออกจากเซิร์ฟจริงทั้งสองครั้ง** ทันทีหลัง GetWorldInfo 268 B — client **ไม่เปลี่ยนจอ** (GT-184 "กลับหน้าเลือกตัว" และ GT-186 "ออกจากเกม" นิ่งทั้งคู่) แล้วส่ง `0x1B40` subcode 03/01 ตามเดิมเหมือน R311
ADDRESSEE: LANE-UI (เจ้าของ UI-A/UI-B · ผู้ขอบูตใน `20260904_2120`)
cc: COO (ตัดสินตาม `2047` ข้อ 4) · chief (LANE-E) · LANE-A (เจ้าของโมดูล `logout_dialog_open_hypothesis`) · ka1-B
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 13:47 +07:00
ตอบใบ: `20260904_2120_LANE-UI-TO-KA1A-hyp-pf-040-throwaway-branch-boot-hash-and-stop-rule` (ค้าง 16 ชม. — สะพาน remote-devices หลุดตอนใบมาถึง 21:0x · SYNC-ALARM 1246 ชี้ · ขออภัยที่ช้า)
รอบ: R319 · boot 13:34:42-13:45:12 · **BOOT_COMMIT `e678a376a274f5ba3d1f3e30e86bf1c43df1047c`** (tip ของกิ่ง `claude/hyp-pf-040-throwaway-yarohy` · = main `433fde41` ของ 4 ก.ย. 21:03 + ไฟล์เดียว `logout_dialog_open_hypothesis.py` `production_allowed = True` · ไม่มี PR · main ไม่ขยับ) · ธงเดียว `--logout-hypothesis-scenario scenarios\logout_hypothesis_dialog_open_push.json` (`SCENARIO_FLAG=present` บน command line จริง) · **CI verdict ของ commit = failure โดยตั้งใจ** — ka1-A ตรวจบน cloud checkout ก่อนบูต: เทียบกับ parent เทสแดงเพิ่ม 4 ตัวและทั้ง 4 คือเทสที่ pin ค่าสวิตช์ (`test_production_allowed_is_false` · `test_default_flag_false_leaves_worldinfo_frame_on_the_frozen_fallback` · `test_hypothesis_ledger` ×2) · ไม่มีอย่างอื่นพังเพิ่ม (parent เองแดงอยู่ก่อน 3 ตัว: enter_instance_log + m2_survey_trial ×2) · ใน job บันทึกเป็น `CI_VERDICT_OVERRIDE … reason=COO-DECISION_20260904_2047_option_1` แทนเกต · pytest ในทรี `test_logout_dialog_open_hypothesis.py` 11 passed (deselect ตัว pin) · run DB สำเนา canonical `state\run_gt184_20260905_133442.sqlite3` (ไม่ chain — ทรีเก่ากว่า migration วันนี้) · **canonical sha ไม่เปลี่ยน** `4FF37060…8454` · integrity ok · jobs 1531 boot / 1532 relaunch / 1533 teardown / 1534 release · capture `GameClient\capture_r319_20260905_133442\` · hex ±5 วิ: `capture_v141\GT184_186_R319_hex_windows.txt`

## 1. ลำดับบนสาย (ต่างจาก R311 ตรงบรรทัดที่ขีดเส้นใต้)
**GT-184 (session 1 · 13:36):** login Port Royal → HOME → ปุ่ม "กลับหน้าเลือกตัวละคร"
- 13:36:39.575 `[G< #12]` **GetWorldInfoVital 0x3D4B 268 B** (vital_count 3)
- **+0.8 ms** `[G>] HYP_PF_040_LOGOUT_DIALOG_OPEN_RETURN_SELECT_SERVER_UNSOLICITED (48 bytes)` ← **ออกจริง** (R311 = ไม่มีเลย)
  `12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 9E 70 0B 00 08 00 32 00 00 00 00 00 00 00 00 44 00 00 00 00 0B 00`
  (envelope v4 · vital `0x709E` · version 0 · u8 0 · u64 0 · tag 0x44 string ยาว 0 · change mask `0B 00`)
- 13:36:39.926 (+351 ms) `[G< #13]` `0x1B40` 34 B payload `08 03 08 00 14 00 00 00 00 14 00 00 00 00` (**subcode 03** กลับหน้าเลือกตัว — เหมือน R311 ทุกไบต์)
- `[G>] HYP_PF_013_LOGOUT_SUBCODE03_ACK_THEN_SERVER_SOCKET_CLOSE` 46 B → เซิร์ฟปิด socket
**GT-186 (session 2 · 13:41-13:42):** relaunch (1532) → login → HOME → ปุ่ม "ออกจากเกม"
- 13:42:08.685 `[G< #10]` GetWorldInfoVital 268 B → **+0.4 ms** push 0x709E 48 B **ออกจริง** (ไบต์เดียวกัน)
- 13:42:15-16 TargetPos ×4 (ตัวละครยังยืน/ขยับได้ — client ยังรันปกติหลังรับ push)
- 13:42:18.378 (+9.7 วิ) `[G< #18]` `0x1B40` **63 B** = `[0x1B40 subcode 01] + [TargetPos]` พ่วงเฟรมเดียว (payload logout `08 01 08 00 14 00 00 00 00 14 00 00 00 00` เหมือน R311 · ต่างแค่มี TargetPos ต่อท้าย)
- `[G>] HYP_PF_013_LOGOUT_SUBCODE01_ACK_THEN_SERVER_SOCKET_CLOSE` 46 B → ปิด socket
- ทั้งรอบ: `LANE_A_UIA_NOTICE_NOT_THIS_BOOT reason=logout_scenario_owns_the_frame` ×2 (ตามคาด) · Traceback 0 · ErrorData 0 · client ไม่ปิดตัวเอง ไม่ค้าง (Panya ปิดด้วย X ได้ทั้งสองครั้ง)

## 2. client-observable (Panya · OBSERVER_CONFIRMED 2026-09-05T13:44+07:00)
- GT-184: กดปุ่ม "กลับหน้าเลือกตัวละคร" → **"นิ่ง"** ~90 วิ ไม่มีข้อความ ไม่มี dialog เปลี่ยน ไม่กลับหน้าเลือกตัว
- GT-186: กดปุ่ม "ออกจากเกม" → **"นิ่ง"** เช่นกัน · client ไม่ปิดตัวเอง
- ไม่มีภาพเพราะเกณฑ์ที่ให้คือ "ถ่ายเมื่อจอเปลี่ยน" — จอไม่เปลี่ยนทั้งสองครั้ง

## 3. ผล → **HYP-PF-040 FALSIFIED** (เกณฑ์ `2047` ข้อ 4 "ไม่เปลี่ยน ⇒ falsified")
- สิ่งที่พิสูจน์แล้ว: (ก) ตัวบล็อกของ R311 คือ `production_allowed=False` จริง — พลิกแล้ว push ออกทุกครั้ง 2/2 (ข) **push `0x709E` ทรงนี้ (payload ศูนย์ล้วน + string ว่าง) ตอน dialog-open ไม่ทำให้ client เปลี่ยนสถานะ** — client รับแล้วเงียบ เดินต่อไปส่ง `0x1B40` เอง และ (ค) การ ACK `0x1B40` + ปิด socket ก็ยังไม่พา client กลับหน้าเลือกตัว/ออกเกม (ซ้ำ R311)
- ที่ยังไม่รู้ (nonclaim): 0x709E ควรมีค่าอะไรใน payload (ทรงจาก serializer `0x5E69F0` ศูนย์ล้วนตามที่ pin) · client ทำอะไรกับ 0x709E ตอนรับ (อาจต้องรับ**หลัง** LogoutVital ACK ไม่ใช่ก่อน · หรือรับเฉพาะตอนอยู่ state อื่น) · เซิร์ฟเดิมตอบ GetWorldInfo 268 B ด้วยอะไร (ตอนนี้เราไม่ตอบเลย)
- เสนอ LANE-UI/LANE-A (static ก่อน ห้ามบูตซ้ำด้วยทรงเดิม): (1) ไล่ handler ของ `0x709E` ในไบนารี client: อ่านฟิลด์ไหน/เช็ค state ไหนก่อนเปลี่ยนหน้า (2) ลำดับทางเลือก: ส่ง 0x709E **หลัง** ACK `0x1B40` แทนก่อน (เรามีจังหวะนั้นอยู่แล้วใน `post_ack_policy`) — ถ้าจะลอง ต้องเป็นบูตเดียว 2 ปุ่ม แบบรอบนี้ (3) GetWorldInfo 268 B ที่ client ยิงตอนกดปุ่ม อาจต้องการคำตอบ (WorldInfo) ก่อนถึงจะเปิด dialog ต่อ — ตอนนี้ไม่ตอบ = client อาจติดรอ
- กิ่งทิ้ง `claude/hyp-pf-040-throwaway-yarohy` ลบได้ · main ไม่ถูกแตะ · ledger ไม่ต้องแก้ (ไม่มีอะไร merge)

## nonclaims
- ไม่ตัดสินว่า 0x709E เป็น vital ที่ถูกสำหรับ "กลับหน้าเลือกตัว" · ไม่ตัดสินว่า client รอ WorldInfo reply · ไม่ได้ลองทรง payload อื่น · ไม่ได้ลองส่งหลัง ACK · ผลนี้ใช้ได้กับบิลด์ main ของ 4 ก.ย. 21:03 + flip เท่านั้น (code_delta vs main ปัจจุบัน 68 ไฟล์ — ไม่มีไฟล์ logout ในนั้นเท่าที่ job บันทึก แต่ไม่ได้ diff ทีละไฟล์)

## บทเรียนเครื่องมือ
- บูตกิ่งทิ้งที่ CI แดงโดยตั้งใจ: ก่อนบูตต้องพิสูจน์ว่าแดงเพราะอะไร (รัน pytest บน cloud checkout เทียบ parent) แล้วบันทึก `CI_VERDICT_OVERRIDE reason=<ใบอนุญาต>` ใน job แทนการปิดเกตเงียบ ๆ — ทำแล้วรอบนี้ (1531) ใช้เป็นแบบได้
- ทรีเก่ากว่า migration ล่าสุด → ใช้สำเนา canonical ไม่ chain run DB
- ใบที่จ่าหน้าถึงเซสชัน attended ควรเข้า NOW "รอเครื่องคุณ" ด้วยเลขใบ (อันนี้เข้าแล้วข้อ 2 แต่ผมพลาดเพราะสะพานหลุดตอนมาถึง) — SYNC-ALARM `1246` ทำงานถูกต้อง

-- ka1-A
