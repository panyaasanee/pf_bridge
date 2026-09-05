# KA1A-R315-RESULTS — GT-247 = **PASS** (ท่าโจมตีออกจริงเมื่อ +0x30 = BEHAVIOR id · 5 ค่าให้ 5 ท่าต่างกัน · 286 กับ echo 60029 ไม่ออกท่า · 1 ท่าต่อ 1 คลิก) + GT-245 ครึ่งแรก PASS (หน้าเลือกตัวพิมพ์ "Prison Exile Island")
ADDRESSEE: chief
cc: LANE-B (เจ้าของใบ/ผู้บริโภคผล GT-247) · LANE-DB (GT-245) · LANE-CS (สกิล/ดาเมจ) · COO · ka1-B
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 2026-09-05 10:31 +07:00
รอบ: R315 · boot 10:11:45-10:2x · BOOT_COMMIT `987edc553d05a09c30b1a360063946d0d0a9ceaf` (= หัว main, code_delta 0) · **command line ไร้ธง** · สวิตช์ = env `PF_POSE_TRIAL=60029,280,284,288,282,290,286` ใน process เซิร์ฟ (ทางเดิน production `_dispatch_mob_combat` → `make_production_hit_pose_echo` server `#787`) · pytest ในทรี 53 passed (test_pose_trial, test_action_ack, test_pose_trial_production_hit_wiring) · run DB `state\run_gt247_20260905_101145.sqlite3` (ทิ้ง) · **canonical sha ไม่เปลี่ยน** `4FF37060…8454` · jobs 1517 boot / 1518 relaunch / 1519 teardown / 1520 release · capture `GameClient\capture_r315_20260905_101145\`
**ทางเบี่ยงที่ Panya เคาะเอง (10:05):** ใช้ลิสต์ 7 ค่าในบูตเดียว (ค่าหมุนต่อ hit) แทน 7 บูต ตามที่ chief `0451` เตือนเรื่อง banner — เหตุผล: banner พิมพ์ตอน import ก่อน tee จึงไม่เข้า log ของเราอยู่แล้ว หลักฐานจริงคือ token ต่อ hit (`POSE_TRIAL sent=<id> hit=<n>`) ซึ่งครบทุกคลิก · 1517 ยืนยันในทรีก่อนบูตว่า `selector_for_hit` หมุน 60029→280→284→288→282→290→286 (`POSE> POSE hit 1..8`)

## 1. wire (คอนโซล + capture_v141)
- ทุก hit ที่เซิร์ฟรับ: `POSE_TRIAL sent=<id> hit=<n>` → `[G>] MOB_COMBAT_POSE_TRIAL (100 bytes)` → `[G>] MOB_COMBAT_ANNOUNCE (98 B)` → `MOB_COMBAT_BAR` · รวม **41 hits** (10:16:37-10:2x) ค่าหมุนถูกลำดับตลอด (hit 1=60029, 2=280, 3=284, 4=288, 5=282, 6=290, 7=286, 8=60029 …) · เป้า 0x203D → 0x2057 → 0x203C → 0x2050 (มอน 4 ตัว ตายแล้วเปลี่ยนตัว)
- เฟรม echo 100 B ต่างกัน**เฉพาะ** u32 ที่ `+0x30`: hit 1 `7D EA 00 00` (60029) · hit 2 `18 01 00 00` (280) — hex hit 1:
  `12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 EA 1A 0B 00 32 01 00 01 10 00 00 00 00 32 3D 20 00 00 00 00 00 00 32 00 00 00 00 00 00 00 00 14 7D EA 00 00 19 00 00 00 00 2A 7B 0F 8F 3F 2A 73 FC A7 46 2A E2 FA 12 46 2A 00 00 F9 43 0B 00 12 02 00 0B 00 0B 08 12 00 00`
  (performer `0x1000100000001`-ish qword ตามที่ composer ใส่ · target 0x203D · +0x30 · u32 0 · heading/xyz f32 ×4 · `0B 00 12 02 00 0B 00` · change mask `0B 08 12 00 00`)
- ไม่มี Traceback · ไม่มี ErrorData · เฟรม ActionVital ขาเข้าจาก client 33 เฟรม (บางเฟรมพ่วง 2-3 ActionVital = คลิกรัว เซิร์ฟนับเฉพาะที่ผ่าน cadence) · hex ทุกเฟรม `capture_v141\GT247_hex_windows.txt` (จาก teardown 1519)

## 2. client-observable (Panya · OBSERVER_CONFIRMED 2026-09-05T10:24+07:00)
| hit (ค่า) | บนจอ |
|---|---|
| 1 · 8 · 15 (60029 = echo เดิม, control) | **ไม่ออกท่า** (ดาเมจขึ้นตามปกติ) |
| 2 · 9 · 16 (280 = equip type 1) | **ออกท่า: ฟันดาบ** |
| 3 · 10 · 17 (284 = type 2) | **ออกท่า: ฟาดกระบอง** |
| 4 · 11 (288 = type 8) | **ออกท่า: ยิงบอลไฟฟ้า** |
| 5 · 12 (282 = type 16) | **ออกท่า: ยิงกระสุน** |
| 6 · 13 (290 = type 32) | **ออกท่า: ยิงบอลเขียว** |
| 7 · 14 (286 = type 64) | **ไม่ออกท่า** |
- **1 ท่าต่อ 1 คลิก** ไม่ตีซ้ำเอง (auto-repeat ไม่เกิดจากเฟรมนี้ — objective 1 ของ RE-110 ยังเปิด) · ผลซ้ำได้ทุกรอบที่ค่าวนกลับมา (3 รอบ) · ไม่ crash
- ภาพ: `GameClient\Data\ScreenShot\20260905_101xxx.png` (หน้าเลือกตัว) — ท่าโจมตี Panya ไม่ได้ถ่าย (เกณฑ์ที่ผมให้: ถ่ายเมื่อออกท่า — เธอเลือกรายงานเป็นคำแทน ยอมรับได้เพราะ 5 ท่าต่างกันชัดและซ้ำได้ 3 รอบ)

## 3. อ่านผล → เสนอ **[PASS]** สองชั้นครบ
- **พิสูจน์แล้ว**: client เล่นอนิเมชันโจมตีตาม `+0x30` ของ ActionVital ที่เซิร์ฟตอบ และ**เลือกท่าตามค่า** (crosswalk RE-110 `EQUIP_VALUE.n_EQUIPTYPE → n_ATTACK_SKILL → BEHAVIOR.n_ID` ถูกทิศ) · echo 60029 = ไม่มีท่า (ต้นเหตุ "ยืนนิ่งแต่ดาเมจขึ้น" ที่ Panya ถามเมื่อ 4 ก.ย.)
- **ค่าที่ควรใช้จริงสำหรับ Arena01** ต้องมาจากอาวุธที่ถือ (ยังไม่มี provenance ของ equip type — ตามใบ) · Panya เห็นตัวละครถือดาบบนหน้าเลือกตัว ⇒ ถ้าอาวุธเป็น type 1 → **280** คือค่า production ที่ถูก (ต้องยืนยันจาก EQUIP_VALUE ของไอเทมที่ใส่ ไม่ใช่จากภาพ)
- **286 (type 64) ไม่ออกท่า**: nonclaim สาเหตุ — อาจเป็นท่าที่ต้องการ resource/อาวุธชนิดนั้นในตัวละคร หรือ BEHAVIOR 286 ไม่มีอนิเมชันสำหรับ model นี้ (LANE-B/RE ตัดสิน)
- งานต่อที่เห็นชัด: (ก) LANE-B: production ตอบ +0x30 = BEHAVIOR ตาม equip type จริงของ performer (แทน echo) — เกณฑ์ปลด BIND001 stop rule ตอนนี้มีหลักฐานจอแล้ว (ข) cadence/auto-repeat = ใบถัดไป (client ไม่ตีซ้ำเองแม้ออกท่า) (ค) ปิด RE-110 objective 2 ได้

## 4. GT-245 ครึ่งแรก (LANE-DB) → **PASS ครึ่งแรก**
- `/warp 2` ที่ Port Royal 10:13 → `GM_WARP_SCENE_PERSISTED scene=2` · X → relaunch 10:14 → **หน้าเลือกตัวละครพิมพ์ "Prison Exile Island"** ใต้ชื่อ Arena01 (ภาพในแชท 10:24 · Panya ยืนยัน) — ก่อน #778 พิมพ์ "Port Royal" เสมอ (R310)
- ครึ่งหลัง (`/warp 1` → relaunch → "Port Royal") จะได้ในบูต 3 ของนัดนี้ (R317) — ถ้าผ่านทั้งสองครึ่ง = PASS เต็ม

## nonclaims
- ไม่ตัดสิน equip type ของ Arena01 · ไม่ตัดสินสาเหตุ 286 · ไม่ตัดสิน cadence (600 ms คงเดิม) · ไม่ตัดสินดาเมจ/สูตร · ไม่ใช่ M4 (มอนไม่ตีกลับ)
- ทางเบี่ยง "ลิสต์ในบูตเดียว" เป็นคำเคาะของเจ้าของ ไม่ใช่ตัวอย่างให้รอบอื่นทำตามจนกว่า LANE-B แก้ banner (0756)

-- ka1-A
