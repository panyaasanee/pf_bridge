# round `B_20260827_1200` (`urlmag`) · lane B · COMBAT -- prove
`mob_ai_control.reconcile()` against a real `mob_death.DeathRegister`,
not just the hand-written `FakeDeaths` stub every prior test used

**opened:** 2026-08-27 11:37 (+07:00, PR `created_at` for
`pirate-force-server#112` / `pf_bridge#189`) · **closed:** 2026-08-27 12:0x
(+07:00)
**branches:** `claude/trusting-curie-2ezpxq` (pirate-force-server, PR #112) ·
`claude/lucid-hamilton-2ezpxq` (pf_bridge, PR #189)

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็นอะไรใหม่ในเกม -- รอบนี้แตะเฉพาะ
`tests/test_mob_ai_control.py` ไม่มีบรรทัดโปรดักชันเปลี่ยนแม้บรรทัดเดียว สถานะที่
ผู้เล่นเห็นได้จริงตอนนี้เหมือนรอบก่อน (`67jejl`): มอนสเตอร์แดงจากตาราง MOBS จริง 13 ตัว
ในสนาม, ตี/เลือดลด/ตายได้ที่ `0x201F` ตัวเดียว, ของหล่น/เก็บครึ่งแรก สิ่งที่รอบนี้ปิดคือ
ช่องว่างที่ผู้เล่นมองไม่เห็น: พิสูจน์ว่า `reconcile()` (ตัวซ่อมสถานะ AI ให้มอนที่ตายจริง
ไม่ค้างเป็น "ยังไม่ตาย") ใช้งานได้กับ `mob_death.DeathRegister` ตัวจริง ไม่ใช่แค่ตัวปลอม
ที่เทสเดิมทุกตัวในไฟล์นี้ใช้มาตลอด

## 1 ล็อกต้นรอบ (ตาม ADDENDUM v6.2 ข้อ A)

**0 ใบ** PR `[LANE-B]` เปิดค้างทั้งสองรีโปก่อนรอบนี้ ตรวจสดผ่าน `list_pull_requests` +
`search_pull_requests` ใบล่าสุดของสาย B คือ `pf_bridge#184` (`merged=true`,
`merged_at 2026-08-27T04:09:56Z`) และ `pirate-force-server#108` (`merged=true`,
`merged_at 2026-08-27T04:25:58Z`) -- งานอยู่บน `main` แล้วจริง ไม่ต้องกู้คืน

หมายเหตุ: `git fetch origin main` ตอนต้นรอบคืนค่า SHA เก่ากว่าที่ GitHub API บอกจริง
(proxy cache) ของทั้งสองรีโป -- ตรวจซ้ำด้วย `list_commits`/`list_branches` ตรง ๆ ก่อนเชื่อ
แล้วรีเซ็ต local branch ด้วย `git fetch origin <sha ที่ยืนยันจาก API>` +
`git reset --hard FETCH_HEAD` ปลอดภัยกว่า `git pull` ธรรมดา -- ไม่ใช่บั๊กใหม่ของ
โปรเจกต์ แค่บันทึกไว้เผื่อรอบถัดไปเจอ local ref ที่ค้างหลัง PR ถูก merge+ลบ branch

ยึดล็อกด้วย draft PR `pirate-force-server#112` + `pf_bridge#189` (empty commit
"round claim: urlmag" ทั้งสองฝั่ง) เวลาจริง `2026-08-27T04:37:42Z` = **11:37:42 +07:00**

## 2 อ่านก่อนเขียน (ไม่ขุดซ้ำ)

อ่าน `rounds/B_20260827_{1015,1215,1300,1545}` (4 ไฟล์ล่าสุด), จดหมายล่าสุดถึง chief,
และซอร์ส `mob_death.py`/`mob_loot.py`/`mob_pickup.py`/`mob_aggro.py`/
`mob_ai_control.py`/`field_mobs.py`/`field_mob_tables_bg0015.py`/
`player_hostile_pairing.py`/`world_population.py` ทั้งหมดก่อนเขียนบรรทัดแรก

**สรุปที่ยืนยันแล้ว (ไม่ใช่ของใหม่รอบนี้ แค่รีเช็ค):**
- `BUILD-004` เสร็จจริงและถูกสโคปแล้ว: มอน 13/13 ตัวจริงของ Port Royal มาจาก
  `field_mob_tables.HOSTILE_PLACEMENTS` ตรงกับเงื่อนไข `ai_combat ∧ rank ∧
  unambiguous` ของตัวสร้างตารางเอง `field_mob_tables_bg0015.py` เป็น roster ของ
  อีกฉาก (Prison Exile) ที่ยังไปไม่ถึงเพราะ world-travel gate ปิดตามคำเคาะ COO --
  ไม่ใช่ช่องว่างที่ยังเปิดอยู่
- `BUILD-005` -- `mob_aggro.py`/`mob_ai_control.py` เดินสายจริงใน `runtime.py`
  (บรรทัด ~3796-3825, ~3980-3999) ตาม CORE-REQUEST-007 และคำเคาะ COO
  `2026-08-26T04:02+07:00` แล้ว การตายยังล็อกที่ `SANCTIONED_FIRST_TARGET_IDENTITY
  = 0x201F` โดยตั้งใจ (`mob_death.py:196,1184`) -- การขยายไปทั้ง roster 13 ตัว COO
  อนุมัติล่วงหน้าไว้แล้วแต่มีเงื่อนไขต้องเห็นศพจริงในเกมก่อน (`GT-036`, ยัง `BLOCKED`
  ใน `GAME_TEST_QUEUE.md`) -- ล็อกนี้ถูกต้องตามดีไซน์ ไม่ใช่บั๊ก
- `BUILD-006` -- ฝั่ง "รับ pickup request จริง" ของ `mob_pickup.py` ติดที่ `RE-082`
  (ยังไม่รู้ client vital id) ซึ่งเป็นใบเปิดของสาย RE อยู่แล้ว ส่วน relog persistence
  ติดที่ session-gate ของ `inventory.py` ซึ่ง COO-DECISION `20260826_0950` มอบให้
  chief ไปแล้ว ไม่ใช่ของสายนี้

**ช่องว่างจริงที่พบ:** `mob_ai_control.reconcile()` (`mob_ai_control.py:826`) เอกสาร
ของฟังก์ชันเองบอกว่ารับได้ทุกอ็อบเจกต์ที่มี `is_dead`/`identities` (duck-type contract)
แต่เทสทุกตัวที่มีอยู่ทดสอบกับ `FakeDeaths` (stub มือเขียน) เท่านั้น ไม่มีเทสไหนพิสูจน์ว่า
`mob_death.DeathRegister` ตัวจริง (ที่คอมเมนต์ของ `reconcile()` เองระบุชื่อว่าเป็น caller
จริงใน production) ยังตรงตาม contract นั้นอยู่ -- รอยต่อระหว่างสองโมดูลที่ต่างคน
ดูแลกัน (แม้จะเป็นสาย B ทั้งคู่) แล้วไม่มีเทสจับ คือความเสี่ยงแบบที่โปรเจกต์นี้ถือว่าจริง

## 3 ของที่รอบนี้เขียน -- สองคอมมิต, พบข้อบกพร่องเทสเองจาก `pf-adversary`

### 3.1 คอมมิต `23ec64d` -- เทสใหม่ 3 ตัว, ขับ `strike -> kill -> commit_death` จริง

`tests/test_mob_ai_control.py::ReconcileAgainstARealDeathRegisterTests` ขับการตาย
จริงหนึ่งครั้งผ่าน `mob_combat.strike -> mob_death.kill -> mob_death.commit_death`
(ลำดับเดียวกับที่ `runtime.py` ใช้) กับมอน `0x201F` ตัวจริงจาก roster แล้วส่ง
`DeathRegister` ที่ได้ไปให้ `reconcile()` โดยไม่มี Fake เจือปนเลยในสายเรียก
ทำ mutation test เองด้วย (พังเช็ก `is_dead` ของ `reconcile()` ชั่วคราว) ยืนยันว่าเทส
happy-path จับได้จริง

### 3.2 คอมมิต `2119c11` -- `pf-adversary` เจอว่า 2 ใน 3 เทสใหม่ผ่านแบบว่างเปล่า

เรียก `pf-adversary` ตรวจก่อน push ตามกติกา พบจริง (ไม่ใช่แค่ทฤษฎี) ด้วย mutation
สองแบบที่รันจริงแล้วยืนยันซ้ำได้:

1. สลับเช็ก `is_dead` (`if not is_dead(...)` -> `if is_dead(...)`) -- `reconcile()`
   เดินย้อนศรทั้งกระดาน (ถอด mon ที่ยังไม่ตายทั้ง 12 ตัว ปล่อย mon ที่ตายจริงไว้เหมือนเดิม)
   -- `test_reconciling_twice_..._is_idempotent` **ยังผ่าน** เพราะเช็กแค่ว่าเรียกซ้ำแล้วได้
   อ็อบเจกต์เดิม ไม่เคยเช็กว่าอ็อบเจกต์นั้นถูกต้อง
2. ทำให้ `reconcile()` ไม่ถอดใครเลย (`if not is_dead(...)` -> `if not False:`) --
   `test_..._leaves_every_other_row_alone` **ยังผ่าน** เพราะ loop เช็กเฉพาะแถวที่ "ไม่ใช่"
   เป้าหมาย แต่ไม่เคยเช็กแถวเป้าหมายเองเลยในเทสนั้น

แก้โดยเพิ่ม assertion ว่าแถวเป้าหมายต้องอยู่ `PHASE_DEAD` จริงในทั้งสองเทส (ก่อนเช็ก
claim "untouched"/"idempotent" ของแต่ละเทส) รัน mutation ทั้งสองแบบซ้ำหลังแก้ -- คราวนี้
**ทั้งสามเทสพังทั้งคู่** ต่าง mutation ทั้งสองแบบ (จากเดิมที่ 2/3 ผ่านทั้งที่โค้ดพัง)

**สิ่งที่พิสูจน์จริง:** `reconcile()` ทำงานถูกต้องกับ `DeathRegister` ตัวจริง ไม่ใช่แค่กับ
stub ที่เขียนเอง และเทสสามตัวนี้จับการพังของฟังก์ชันได้จริงทั้งสาม ไม่ใช่แค่ตัวเดียว
**สิ่งที่ยังไม่พิสูจน์:** `commit_step`'s compare-and-swap เช็กแค่ generation/epoch/
identity-set แล้วคืน register ที่คำนวณไว้ล่วงหน้าตรง ๆ -- ไม่มีเทสไหน (เก่าหรือใหม่)
พิสูจน์ว่า `reconcile()` ที่ถอดมอนออก "ศูนย์ตัว" ทั้งที่ register มีศพจริงอยู่จะถูกจับได้
นอกจาก `test_reconcile_retires_the_row_a_real_death_register_calls_dead` ตัวเดียว --
ทิ้งไว้เป็นข้อสังเกต ไม่ใช่บั๊กที่ต้องแก้รอบนี้ (เทสตัวนั้นจับได้อยู่แล้ว)

## 4 เขตเขียน

`tests/test_mob_ai_control.py` เท่านั้น -- ไม่มีบรรทัดโปรดักชันถูกแตะเลยทั้งรอบ
(`git show --stat` ยืนยันทั้งสองคอมมิต) ไม่ได้แตะ `runtime.py`/`app.py`/
`pf_login_game_server_v141.py` และไม่ได้แตะ `scenarios/world_*.json`

## 5 หลักฐานสองชั้น

| ชั้น | รอบนี้มีอะไร |
|---|---|
| **wire / DB** | `tests/test_mob_ai_control.py` เดี่ยว 55/55 (52 เดิม + 3 ใหม่) · สวีตรวม `mob_death`+`mob_loot`+`mob_pickup`+`field_mobs`+`mob_combat`+`mob_ai_control`+`field_mob_tables_bg0015`: **332/332** · สวีตเต็ม `unittest discover`: 3479 เทส, error 18 ตัวเดิม (`capstone`, environment เท่านั้น, baseline เดียวกับทุกรอบก่อนหน้า), skip 212, **0 FAIL ใหม่** · mutation test สี่ครั้ง (สองแบบ ก่อน/หลังแก้) ยืนยันซ้ำได้ตรงกับที่ `pf-adversary` รายงาน |
| **client-observable** | ไม่มี -- รอบนี้แตะเฉพาะชั้นเทส ไม่มีบูตเกม ไม่ต้องมีผู้เทส |

## 6 ถ้าผิดต้องย้อนอะไรบ้าง

สองคอมมิต แตะไฟล์เดียว (`tests/test_mob_ai_control.py`) ย้อนได้ทันทีด้วย
`git revert 2119c11 23ec64d` -- ไม่กระทบ production path ใด ๆ เพราะไม่มีบรรทัด
โปรดักชันถูกแตะเลย

## 7 `pf-adversary` -- พบ 2 findings จริง ดูรายละเอียดที่ §3.2

## 8 ข้อสังเกตนอกเขตเขียน (ไม่แตะ แค่แจ้ง)

`runtime.py:4726-4733` (PANYA-CHASE, `basic_faction=1` บน flagless boot) เรียก
`self.foundation.projector.start_game(...)` ตรง ๆ แทนที่จะใช้
`player_hostile_pairing.compose_start_game_with_player_pairing`
(`player_hostile_pairing.py:98`) ที่รอบก่อนของสาย B สร้างไว้เฉพาะสำหรับจุดเรียกนี้
(CORE-REQUEST-009) วันนี้พฤติกรรมยังเหมือนกันทั้งสองทาง ไม่ใช่บั๊ก แค่ selector ซ้ำซ้อน
ในไฟล์ของ chief -- ฝากไว้ให้ chief ดูตอนแตะบล็อกนั้นครั้งหน้า ไม่ใช่คำขอด่วน

## 9 รอบถัดไปควรทำอะไร

1. `BUILD-004` (28 ส.ค. 12:00) -- พร้อมและเสร็จแล้วจริง (§2) ไม่มีความเสี่ยงใหม่
2. `BUILD-005` (29 ส.ค. 23:59) -- `0x201F` พร้อม การขยายไปทั้ง roster ยังรอ `GT-036`
   (เห็นศพจริงในเกม) ตามคำเคาะ COO เดิม ไม่ใช่ของที่สาย B เปิดเองได้
3. `BUILD-006` (31 ส.ค. 12:00) -- ไม่เปลี่ยนจากรอบก่อน ครึ่งแรกเสร็จ ครึ่ง relog รอ
   chief (`inventory.py` gate 2) ครึ่ง pickup-request รอสาย RE (`RE-082`)
4. ถ้ามีเวลาในรอบถัดไป: ไล่หา seam อื่นในสไตล์เดียวกัน (โมดูลที่ทดสอบกันแค่ผ่าน stub
   ไม่เคยทดสอบกับของจริงจากโมดูลพี่น้อง) -- `reconcile()`/`DeathRegister` เป็นตัวอย่าง
   แรกที่เจอ ไม่ได้แปลว่าเป็นตัวเดียว

-- **สาย B · COMBAT**
