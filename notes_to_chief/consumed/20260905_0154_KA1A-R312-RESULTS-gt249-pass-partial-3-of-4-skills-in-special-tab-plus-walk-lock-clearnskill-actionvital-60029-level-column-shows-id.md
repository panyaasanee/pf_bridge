# KA1A-R312-RESULTS — GT-249 = PASS-PARTIAL (3/4 รายการโผล่ในแท็บ "พิเศษ") + ของแถม 4 ข้อ (client ล็อกเดินหลังชุดเฟรม · CLearnSkillVital · ActionVital จาก hotbar = 60029/110/111 · คอลัมน์เลเวลโชว์ id)
ADDRESSEE: chief
cc: LANE-CS (เจ้าของใบ/ผู้บริโภคผล) · LANE-B (ท่าโจมตี/ActionVital) · COO · ka1-B
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 2026-09-05 01:54 +07:00 (ประมาณ)
รอบ: R312 · boot 01:17:39-01:50:39 · BOOT_COMMIT `f2a62bf0e08ac103fbad21633bfedc90b21e12ca` (= หัว main, code_delta 0) · ธงเดียว `--learn-skill-result-hypothesis-scenario scenarios\learn_skill_result_hypothesis_learn_sweep.json` · run DB `state\run_gt249_20260905_011739.sqlite3` (ทิ้ง) · **canonical sha ไม่เปลี่ยน** `4FF37060…8454` ก่อน/หลัง · jobs 1506 (boot) 1507/1507b (relaunch) 1508 (teardown) 1509 (release) · capture `GameClient\capture_r312_20260905_011739\`

## 1. GT-249 LEARN-SKILL-RESULT-REAL-KIT-CONTENT-001 → เสนอ **[PASS-PARTIAL / กล่อง P4]**

### wire/DB
- trigger `SKILLCONTENT` รับ 2 ครั้ง: frame #56 01:20:57.5 และ #87 01:21:51.9 (`0xAC52` 54 B) · แต่ละครั้งเซิร์ฟยิงครบ 6 เฟรม `[G>] HYP_PF_033_LEARN_SKILL_RESULT_*` ห่าง 3.0 s late ≤1.0 ms: COUNT0_TRAIL0 37 B · COUNT1_TRAIL0 50 B · COUNT1_TRAIL1 50 B · COUNT3_TRAIL0 77 B · COUNT3_TRAIL1 77 B · **COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 90 B**
- เฟรมที่ 6 (hex เต็มจาก console บรรทัด 483-488):
  `12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 3C 67 0B 00 12 04 00 14 6F 00 00 00 12 6F 00 14 6F 00 00 00 14 40 9C 00 00 12 40 9C 14 40 9C 00 00 14 63 00 00 00 12 63 00 14 63 00 00 00 14 6E 00 00 00 12 6E 00 14 6E 00 00 00 0B 00 0B 00`
  = vital `0x673C` · u16 count=4 · 4 records (u32/u16/u32 = 111,111,111 · 40000,40000,40000 · 99,99,99 · 110,110,110) · trailing u8 0 — ตรง scenario ที่ตรวจในบูตทรี (`SCN_HAS_COUNT4 True ids 111/40000/99/110`)
- ไม่มี Traceback · socket ไม่หลุด · sessions +2 (login 2 ครั้ง: 01:18 และ 01:49) · max lease 12→14 · integrity ok · FK 0 · ไม่มีตารางอื่นเปลี่ยน (database_write=none ตามใบ)
- pytest ในทรี: `tests/test_learn_skill_result*.py` 60 passed

### client-observable (Panya · OBSERVER_CONFIRMED 2026-09-05T01:26+07:00)
- S-BASE-K `ScreenShot\20260905_011957.png`: กด K ก่อน trigger → หน้าต่าง SKILL "รายการสกิล" แท็บ **Gladiator** ว่าง 0 รายการ (ตรง GT-116)
- หลัง trigger ทั้ง 2 รอบ แท็บ Gladiator **ยังว่าง** (`20260905_012212.png` · ตัวกรอง dropdown = "แสดงสกิลทั้งหมด")
- 🔴 **แท็บ "พิเศษ" มี 3 รายการ** (`20260905_012512.png`): `Normal Attack  99 / 1` · `Strive Jump  110 / 1` · `VIP Strive Jump  111 / 1` — ชื่อ+ไอคอนตรง 3 ใน 4 ของ kit · **40000 "Gladiator Basic Training" ไม่โผล่ทั้งสองแท็บ**
- **คอลัมน์ "เลเวล" แสดงเป็น `99 / 1`, `110 / 1`, `111 / 1`** (Panya สังเกตเอง `20260905_014629.png`) ⇒ ช่องหนึ่งใน record_u32_0/record_u16_4/record_u32_8 ถูก client อ่านเป็น **เลเวลสกิล** (จึงโชว์ค่า = id ที่เราใส่ซ้ำ) ส่วน "/ 1" = ค่าที่ client มีเอง (น่าจะ max level จากตาราง — ไม่ยืนยัน)
- ไอคอนสกิลโผล่ที่แถบขวาล่างเอง: `N` = VIP Strive Jump · `Ctrl+1` = Strive Jump (ไม่ได้ลาก) · ช่องขวาสุดของ hotbar หลักมีไอคอน Strive Jump
- ยิง trigger ซ้ำ (S-REPEAT-K): สถานะเหมือนเดิม 3 รายการ ไม่เพิ่ม/ไม่ซ้ำ
- หลัง relogin (01:49) **รายการหาย กลับเป็นว่าง** และช่อง hotbar ที่ลากไว้ว่าง ⇒ เนื้อหน้าต่างสกิลเป็นข้อมูลจากเซิร์ฟล้วน client ไม่จำ
- ไม่ crash · ไม่มี ErrorData · หมุนกล้องปกติ

### อ่านผล
PASS-PARTIAL ตามกล่อง P4: เฟรม 0x673C ที่ใส่ id จริงทำให้หน้าต่างมีรายการจริง 3/4 · ข้อสังเกตที่ LANE-CS ใช้ต่อได้ทันที: (ก) ช่อง "เลเวล" คือหนึ่งใน 3 ช่อง — รอบหน้าส่ง `<id>, <level=1>` แยกช่องจะรู้ทันทีว่าช่องไหน (ข) 40000 อาจไม่อยู่ในตาราง skill ฝั่ง client หรืออยู่แท็บ Gladiator ที่ต้องการฟิลด์เพิ่ม — ไม่ตัดสิน (ค) ต้องส่งรายการสกิลตอน login + เก็บ DB ถึงจะคงอยู่

## 2. ของแถม (สังเกตการณ์ ไม่ใช่ผลใบ)

### 2.1 🔴 client ล็อกการเดินหลังรับชุดเฟรม 6 เฟรม (หายเมื่อ relogin)
- ก่อน trigger: TargetPosVital ออกปกติ (#51-#53 01:20:54) · หลัง trigger แรกจนปิดเกม 01:48: **ไม่มี TargetPosVital แม้แต่เฟรมเดียว** ทั้งที่ Panya กดเดินหลายครั้ง (เธอยืนยัน "เดินไม่ได้" · UI อื่นตอบสนองปกติ เปิด K/ลาก/กดปุ่มได้) · ปิด K + Esc ไม่หาย
- หลัง relogin เซิร์ฟเดิม (job 1507b 01:48:5x): TargetPosVital 4 เฟรมใน 10 วิ = เดินได้
- ไม่รู้ว่าเฟรมไหนใน 6 เฟรมเป็นตัวล็อก (COUNT0…COUNT3 มีค่า FF/garbage) — เสนอ LANE-CS ยิงทีละเฟรมรอบหน้า · **ผลกระทบ**: ถ้าจะส่ง 0x673C ตอน login ต้องหาตัวล็อกก่อน ไม่งั้นผู้เล่นเดินไม่ได้

### 2.2 CLearnSkillVital (`0x36AA` 13994, registry: CLearnSkillVital) 150 B ×2 (frame #70 01:21:17.6 · #125 01:22:58.2)
- เป็นเฟรม **2 vital**: `0x36AA` body `14 00 00 00 00` (u32 0) ตามด้วย `0x0F01` UserSetting_UpdateServerSettingVital ทั้งก้อน · parser เราเห็นแค่ vital แรก (`DISPATCH_NESTED_VITALS vital_count=2 first_nested_id=0x36AA`)
- Panya จำไม่ได้ว่ากดอะไร (คลิก dropdown บ้าง) · ทดลองซ้ำทีละอย่าง (01:32-01:38): เปิด/ปิด K + dropdown → ไม่ส่ง · สลับแท็บ → ไม่ส่ง · คลิกรายการ → ไม่ส่ง · ลากลง hotbar → ไม่ส่ง ⇒ **ตัวส่งยังไม่รู้** (สงสัยดับเบิลคลิก/ปุ่ม "เพิ่มสกิล" ที่มีแต้ม 0) · เซิร์ฟไม่ตอบ ไม่มีผลข้างเคียงเห็นได้
- hex เต็ม #70: `12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 AA 36 0B 00 14 00 00 00 00 0B 02 12 01 0F 0B 00 0B 01 0B FF 32 00 00 00 00 00 00 00 00 26 FF FF FF FF 0B 19 0B 00 0B 00 05 01 32 00 00 00 00 00 00 00 00 26 01 00 00 00 0B 0C 0B 0C 0B 0C 0B 03 08 01 2A E3 64 30 3F 2A 5E AE 5E 3F 0B 02 0B 04 0B 00 32 6F 00 00 00 00 00 00 00 0B 04 0B 01 32 6E 00 00 00 00 00 00 00 08 02 2A E3 64 30 3F 2A FF 04 53 3F 0B 00 08 03 2A E3 64 30 3F 2A A0 5B 47 3F 0B 00 0B 00`

### 2.3 🔴 ActionVital จาก hotbar/ปุ่มสกิล = เฟรมเดียวกัน ต่างกันไบต์เดียว (+0x30 u32) — ให้ LANE-B/LANE-CS
- ลาก Normal Attack ลงช่อง 1 (ไม่มีเฟรมออกตอนลาก) · กดปุ่ม 1 → #619 UserSetting 145 B (ท้ายเฟรม `0B 01 08 00 14 63 00 00 00` = ช่อง 0 → u32 99 บันทึก hotbar) + **#620 ActionVital 84 B u32 = `7D EA 00 00` = 60029**
- กด N → #737 ActionVital 84 B u32 = 111 · กด Ctrl+1 → #739 u32 = 110
- hex #620: `12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12 EA 1A 0B 00 32 00×8 32 00×8 32 00×8 14 7D EA 00 00 19 00 00 00 00 2A E6 2F 47 40 2A 0F 19 0A C6 2A 23 EB 17 C5 2A 00 00 3A 43 0B 00 12 01 00 0B 00` (#737/#739 เหมือนกันทุกไบต์ยกเว้น `6F 00 00 00` / `6E 00 00 00`)
- ⇒ **"Normal Attack" (skill 99) ถูก client ส่งเป็นรหัส 60029 (0xEA7D)** = ค่าที่เซิร์ฟ echo ที่ +0x30 ตอน auto-attack (RE-110) · ดังนั้น 60029 ไม่ใช่ขยะ แต่คือ "รหัสสกิลโจมตีปกติ" ของ client · เซิร์ฟไม่ตอบทั้ง 3 เฟรม (ไม่มีเป้า) · client นิ่งทั้ง 3 (ไม่ออกท่า ไม่กระโดด) แต่ขอบช่อง hotbar มีเส้นไฟวิ่ง (สถานะกำลังใช้/คูลดาวน์)
- นัยต่อ GT-247: reply +0x30 ที่ทำให้ออกท่าอาจต้องเป็น BEHAVIOR id (280…) **หรือ** client ต้องการ reply ที่ "ยืนยันสกิล 60029" อีกรูปแบบ — ใบ A/B 7 ค่ายังคุ้มรัน แต่ LANE-B ควรเพิ่มสมมติฐาน "60029 = skill alias ของ Normal Attack; ท่ามาจากตาราง SKILL(99) ไม่ใช่ BEHAVIOR" ไว้อ่านผล
- นัยต่อ GT-243: ครึ่ง "hotbar สกิล 99 → เฟรมอะไร" ได้แล้ว = ActionVital 84 B u32 60029 (ภายใต้บูต scenario — ไม่นับเป็นผล GT-243 ตามกติกาใบ) · P0 ของ GT-243 ทำได้ในเซสชันเดียวกับ GT-249 (ลากได้) แต่ **ไม่คงอยู่หลัง relogin** ⇒ GT-243 ต้องรันในบูตที่มีสกิลตอน login หรือรันต่อเนื่องหลัง trigger ในบูตเดียวกับ scenario (ขัดกติกา flagless ของใบ — chief/CS ตัดสิน)

### 2.4 อื่น ๆ
- เปิดกระเป๋า 01:24:52 → CheckSecondPwdVital ตามเดิม (GT-242 ยัง BLOCKED)
- UserSetting_UpdateServerSettingVital 138 B ออกทุกครั้งที่เปิด/ปิดหน้าต่าง K (บันทึกสถานะ UI) · 145 B เมื่อ hotbar เปลี่ยน — ใช้เป็น differential ให้ RE-237 ได้ (ฟรี)

## nonclaims
- ไม่ตัดสินว่าช่องไหนใน 3 ช่องคือ level/id — เห็นแค่ว่า "ช่องที่ client โชว์เป็นเลเวล" ได้ค่า id · ไม่ตัดสินว่าทำไม 40000 หาย · ไม่ตัดสินความหมาย trailing u8
- ไม่ตัดสินว่าเฟรมไหนล็อกการเดิน · ไม่ตัดสินตัวส่ง CLearnSkillVital
- ActionVital ที่เห็นเป็นเฟรม client → server ไม่ขึ้นกับ scenario แต่รอบนี้บูตด้วยธง จึงเป็น "สังเกตการณ์" ไม่ใช่ผล GT-243
- ไม่ได้บันทึกวิดีโอ (กติกา Panya) — หลักฐานจอ = 6 ภาพใน `GameClient\Data\ScreenShot\20260905_01*.png`

## บทเรียนเครื่องมือ
- template DB query `characters.level` ไม่มีคอลัมน์นี้แล้ว (schema เปลี่ยน) → job 1506 พิมพ์ traceback แต่ไม่ abort · 1508 แก้แล้ว — ขอ chief แก้ template ที่ยังใช้ `level`
- job relaunch (1507) รันเร็วกว่า process client ปิดจริง → "[STOP] a client is still running" → ต้องวางซ้ำ (1507b) · เสนอ template relaunch รอ GameClient=0 สูงสุด 30 วิ ก่อน STOP

-- ka1-A
