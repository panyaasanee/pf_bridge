# ka1-A — R308 ผล GT-228: **PASS (กล่อง B)** — ตอนเรือแตะเกาะ ไคลเอนต์ยิง `TriggerVital 0x1FB2` ทุกครั้ง แต่ id = **2** ที่ Prison Exile และ **3** ที่ Spice Paradise (ไม่ใช่ 153/154)

**ADDRESSEE: LANE-A** (เจ้าของใบ · บริโภคผลเอง) · cc: chief · COO
**รอบ:** R308 2026-09-04 12:39-13:24 +07:00 · ผู้ขับ: Panya (เจ้าของ) · ผู้วัด/เขียน: ka1-A
**บูต:** `pirate-force-server` **`d8969729bcdf7f6880d1b18595ea8aea77e4a7f7`** (commit เขียวล่าสุดที่ resolver ให้ · ไม่ใช่หัว main — ดู deviation 1) · ไม่มีแฟล็ก scenario · ไม่มี PF_SPEED_TRIAL · ไม่มีวิดีโอ · DB = สำเนา `state\run_gt228_20260904_125449.sqlite3` · ตัวละคร Arena01 (Lv.1)
**jobs:** 1489 (abort เอง — รอ main เขียวไม่ทัน) → 1489b boot → 1490 relaunch client → 1491 teardown · log ทั้งหมดใน `outbox\`
**capture root:** `GameClient\capture_r308_20260904_125449\` (raw = `capture_v141\GAME_20260904_130510_526308_52808.txt` session ทะเล · `GAME_EVENTS_LIVE.txt` · `GAME_LIVE.txt` · `server_console_live.err.txt` · `boot_stderr.txt`) · ไฟล์สรุปหน้าต่าง hex: `capture_v141\GT228_hex_windows.txt` (เนื้อหาเต็มแนบท้ายใบนี้)

## คำตัดสิน
**PASS ตามกล่อง B ของใบ**: ได้ hex ดิบครบทุกจังหวะชน **ทั้งสองเกาะ** (เกาะ 2 ×3 ครั้ง · เกาะ 3 ×2 ครั้ง) · ทุกครั้งที่เรือแตะเกาะ ไคลเอนต์ยิง `0x1FB2` 69 ไบต์ (TriggerVital เป็น nested ตัวแรก + TargetPosVital ตัวที่สอง) · **id ที่เห็น: 2 (Prison Exile ทั้ง 3 ครั้ง) · 3 (Spice Paradise ทั้ง 2 ครั้ง)** · ไม่พบ `0F 99 00 0B 04` / `0F 9A 00 0B 04` เลย ⇒ คำทำนาย 153/154 **ผิด** (finding ไม่ใช่ FAIL) · redirect ตามกล่อง B: ใบ RE ต้องเลิกสมมุติ 153/154 แล้วไล่จาก id ที่จับได้จริง
`OBSERVER_CONFIRMED: 2026-09-04T13:22+07:00` (Panya นั่งหน้าจอทั้งใบ ยืนยันจังหวะชนทุกครั้งในแชทและถ่ายจอในเกม)

## ชั้น wire/DB
**(ก) หน้าต่าง ±5 วิ รอบเวลาถ่ายจอของทุกจังหวะชน** (เวลาเฟรม = timestamp ของ `GAME_LIVE.txt` STATE rx=N · ทุก opcode ไม่กรอง · เนื้อหาเต็มแนบท้าย):

| จังหวะ | เวลาถ่ายจอ | HUD X,Y ตอนแตะ | เฟรมในหน้าต่าง | เฟรม 0x1FB2 ในหน้าต่าง |
|---|---|---|---|---|
| เกาะ 2 ครั้ง 1 | 13:09:32 | -5,064 / 4,492 | 5 (rx130-134) | **rx130 13:09:28 id=2** (+ rx131 `COnLandVital` 0x1EB4 72 B) |
| เกาะ 2 ครั้ง 2 | 13:10:15 | -5,406 / 4,397 | 5 (rx151-155) | **rx152 13:10:13 id=2** |
| เกาะ 2 ครั้ง 3 (เกิน) | 13:13:35 (ภาพชี้เมาส์) | -6,167 / 5,130 | 5 (rx250-254) heartbeat ว่างทั้งหมด | ไม่มีในหน้าต่าง — แต่มี **rx248 13:13:26 id=2** 9 วิก่อนภาพ (ภาพนี้ถ่ายช้า) |
| เกาะ 3 ครั้ง 1 | 13:19:44 | -1,560 / -5,331 | 5 (rx433-437) | **rx433 13:19:39 id=3** |
| เกาะ 3 ครั้ง 2 | 13:21:39 | -1,877 / -5,370 | 5 (rx491-495) | **rx491 13:21:36 id=3** |

**(ข) เฟรม 0x1FB2 ทั้ง session ทะเล = 6 เฟรม** (นับจาก raw + EVENTS + hook ตรงกันทั้งสามที่):
`rx112 13:08:52 id=35` (ขณะแล่นเข้าหาเกาะ 2 ยังไม่แตะ) · `rx130 13:09:28 id=2` · `rx152 13:10:13 id=2` · `rx248 13:13:26 id=2` · `rx433 13:19:39 id=3` · `rx491 13:21:36 id=3`
ถอดค่าตามรูปเฟรมของใบ (`0F <u16 id> 00 0B 04 2A x 2A y 2A z`) — **ตัวเลขถอดตรง ๆ ไม่ตีความ**:
- rx130 id=2 trigger_xyz=(-4451.6, 4531.1, 186.0) · ship TargetPos ในเฟรมเดียวกัน=(-4800.0, 4632.2, 86.0)
- rx152 id=2 trigger_xyz=(-5613.8, 4162.5, 186.0) · ship=(-5613.8, 4162.5, 86.0) ← x,y เท่ากันเป๊ะ z ต่าง 100
- rx433 id=3 trigger_xyz=(-1563.5, -5275.1, 186.0) · ship=(-1560.1, -5331.6, 86.0)
- rx491 id=3 trigger_xyz=(-1720.4, -5251.6, 186.0) · ship=(-1877.2, -5370.0, 86.0)
- z ของ trigger = 186.0 ทุกเฟรม (ตรงกับที่ R307 จด) · z ของเรือ = 86.0 ทุกเฟรม

**(ค) ครึ่งคอนโซล (P1) ทำงานจริงในบิลด์นี้**: `boot_stderr.txt` มี `LANE_HOOK_REGISTERED pirateforce_foundation.lane_hooks.lane_a_island_trigger_log vital_inbound_trigger_vital` · `server_console_live.err.txt` มี `LANE_A_TRIGGER_VITAL` **6 บรรทัด = 6 เฟรม** ครบ ไม่มี `UNPARSED`:
```
LANE_A_TRIGGER_VITAL id=35 name=Thorn Flower PROP no_responder bytes_out=0
LANE_A_TRIGGER_VITAL id=2 name=Edmund Hidden Treasure PROP no_responder bytes_out=0   (x3)
LANE_A_TRIGGER_VITAL id=3 name=Seafood Cargo PROP no_responder bytes_out=0            (x2)
```
`LANE_A_ENTER_INSTANCE` = 0 บรรทัด (ถูกต้อง — ไม่มีใครกดยืนยัน ไม่มีหน้าต่างให้กด) · `NavigationEx`/`ENTER_INSTANCE` ใน out = 0 · Traceback 0 · ConnectionResetError 0
**(ง)** `integrity_check` ok ทั้งก่อน/หลัง · FK 0 · canonical sha256 ก่อน=หลัง=`4FF37060…A548454` (ไม่เปลี่ยน) · teardown: stopped ×1, traceback 0, listeners 0, client 0
sha256 ไฟล์: raw ทะเล `65692E9D…3CBE64FA` (1,084,786 B) · EVENTS `A5A9C664…ADCDC8CA6` · GAME_LIVE `BB37EFBB…B031FF68E` · err `26DA46C7…20D0FEA7` · boot_stderr `93235D69…31C86E2C` (ค่าเต็มใน `outbox\1491_r308_teardown.out.txt`)

## ชั้น client-observable (Panya เห็นเอง · ภาพในเกมเต็มความละเอียดที่ `GameClient\Data\ScreenShot\20260904_*.png`)
- **(จ) ตอนชนแต่ละครั้ง จอ = `ไม่มีอะไรเลย`** ทั้ง 5 ครั้ง — ไม่มีหน้าต่างรายงานกัปตัน ไม่มีข้อความปฏิเสธเลเวล (แม้ป้ายเกาะ 3 เขียน Lv.25 และตัวละคร Lv.1) ไม่มีข้อความอื่น
- **(ฉ)** จากภาพนิ่ง: เรืออยู่ชิดขอบเกาะ ไม่ทะลุเข้าไปในเกาะ · เจ้าของไม่ได้บรรยายว่าเด้งหรือหยุด — **ไม่อ้าง**
- **ป้ายชื่อเกาะขึ้นเมื่อ "ชี้เมาส์ค้าง" (ไม่คลิก)**: `Prison Exile Island` (ภาพ 13:14:18, 13:17:00 — มีข้อความบรรทัดสองตัวเล็ก อ่านไม่ออกจากภาพ) · `Spice Paradise Island [เข้าได้เมื่อ Lv.25]` (ภาพ 13:21:39) · ตอนชี้จะมี**วงแหวนแสงขาว-ฟ้ารอบเกาะ** (13:10:15, 13:17:00, 13:19:44, 13:21:39) — เอฟเฟกต์ของการชี้ ไม่ใช่ของเฟรม
- ขั้น 11ก: HUD ตอนเกิด **X:3,050 Y:232** (ภาพ 13:05:22) **ตรง `MARKER` แถว 17 (3050, 232)** ⇒ กรอบพิกัด HUD คงเดิม เลขขั้น 9-11 แปลงได้
- **(ช) สีป้ายชื่อ ต่อภาพ** (อ่านจากภาพเต็มเท่านั้น · จดสีอย่างเดียว):
  - 13:05:22 `S126-SPAWN`: Arena01 = ขาว · Intrepid (เรือ NPC) = เขียว · อื่น = none
  - 13:09:32 `ISL2-CONTACT-1`: Arena01 = ขาว · อื่น = none
  - 13:10:15 `ISL2-CONTACT-2`: Arena01 = ขาว · Tornado (เรือ NPC) = เขียว · อื่น = none
  - 13:13:35 `ISL2-CONTACT-3/hover`: Arena01 = ขาว · Tornado = เขียว (บังบางส่วน) · อื่น = none
  - 13:17:00 `ISL2-LABEL`: Arena01 = ขาว · tooltip "Prison Exile Island" = ขาวบนพื้นน้ำเงินเข้ม · Tornado = เขียว (บังบางส่วน)
  - 13:19:44 `ISL3-CONTACT-1`: Arena01 = ขาว · อื่น = none
  - 13:21:39 `ISL3-CONTACT-2/label`: Arena01 = ขาว · tooltip "Spice Paradise Island [เข้าได้เมื่อ Lv.25]" = ขาว/เหลืองอ่อนบนพื้นน้ำเงินเข้ม · อื่น = none
  - 13:09:17, 13:14:18 ยังไม่ได้อ่านสีป้าย (ภาพ approach/hover ของเจ้าของ — ไฟล์อยู่ครบ)
- แชท 13:09:17 มีบรรทัด `[ระบบ] : ฝ่ายตรงข้ามไม่มีอยู่ หรือ ฝ่ายนั้นไม่สามารถไปยังตำแหน่งนั้นได้!` — มาหลังเฟรม `0x4391` (trace-path req) 13:08:36 หนึ่งเฟรม = พฤติกรรม GT-120 (empty-vector reply) **ไม่เกี่ยวกับการชน**
- NO-CRASH: หมุนกล้องคลิกขวาลากตอนจบได้ ออกด้วย X ปกติ

## ข้อสังเกตให้ LANE-A (สมมุติฐาน — ผมไม่ตัดสิน)
1. **id ที่ยิงตอนแตะเกาะ = เลขฉากปลายทาง?** Prison Exile = ฉาก 2 → id 2 · Spice Paradise = ฉาก 3 → id 3 · ซ้ำได้ 100% (3/3 และ 2/2) · ส่วน R307 เห็น 40/51/**3**/57/36 ขณะแล่นผ่าน — 3 โผล่ตอนนั้นด้วย · ⇒ ตาราง `TEXTDATA_TH__Trigger_TIP` ที่ตั้งชื่อ id 2/3 ว่า "Edmund Hidden Treasure"/"Seafood Cargo" **อาจเป็นคนละ namespace** กับ id ในเฟรมนี้ — ควรเทียบกับตารางฉาก/`MARKER`/ตารางเกาะก่อนสรุปว่าเป็น prop
2. trigger_xyz ในเฟรมไม่เท่ากับตำแหน่งเรือใน 3 จาก 4 เฟรม (ต่างกันหลักร้อยหน่วย) แต่เท่ากันเป๊ะ 1 เฟรม (rx152) · z=186 คงที่ — ผมไม่รู้ว่าเป็นจุดของ trigger หรือของเรือ
3. `COnLandVital` 0x1EB4 (72 B) ยิง 2 ครั้ง (rx131 13:09:30, rx144 ~13:09:5x) เฉพาะช่วงแตะเกาะ 2 ครั้งแรก · ไม่ยิงเลยที่เกาะ 3 · ใน R307 ฉากบกยิง 221 ครั้ง (เป็น vital ธรรมดาของการเดิน?) — จดไว้เฉย ๆ
4. เกาะ 3 มีป้าย Lv.25 แต่ **ไม่มีข้อความปฏิเสธ** และไม่มีไบต์อื่นออกนอกจาก 0x1FB2 ⇒ ยังตอบไม่ได้ว่าเช็คเลเวลอยู่ฝั่งไหน (ไม่มี responder ก็ไม่มีอะไรให้ปฏิเสธ)

## deviations ของรอบนี้ (จดตรง ๆ)
1. **บูต d8969729 ไม่ใช่หัว main** — main ขยับทุก ~10 นาที (#729 12:30, #730 12:39, #731 12:49) การรอหัวเขียวรีเซ็ตเรื่อย ๆ · Panya เคาะ 12:52 ให้บูต commit เขียวล่าสุด · code delta 4 ไฟล์ (`damage_by_skill.py`, `mob_death.py`, `skill_catalog.py`, `world_m2_survey_plan.py` — ไม่เกี่ยวกับ hook ของใบ) · ใบผ่านทุก RECHECK บน d8969729 (P1-a 5efb55d ancestor=0, call site+hook, pytest 38 passed)
2. **ไม่ได้รีสตาร์ตเซิร์ฟเวอร์ระหว่างปิด X → เปิดใหม่ (P3/P4)** — ใช้ทางเดียวกับ R307 (relaunch client only, job 1490) เพราะ P3 มีไว้กันเคส "ไคลเอนต์ถูกฆ่า" ส่วน X = ปิดสะอาด (เซิร์ฟพิมพ์ `login client closed`/`closed game log`) · ผล: ล็อกอินครั้งสองลงฉาก 126 ปกติ (`GM_CHAT_STAGED_NEXT_LOGIN` → `WORLD_SCENE scene_id=126` ×1)
3. **บั๊กเครื่องมือของผมเอง**: job 1489b เพิ่ม `-RedirectStandardOutput/-RedirectStandardError` ให้ process เซิร์ฟเวอร์ (เพื่อเก็บบรรทัด `LANE_HOOK_REGISTERED` ตอนบูต — ได้ผลจริง) แต่ .NET เปิด handle inheritance ⇒ เซิร์ฟเวอร์ถือท่อ stdout ของ bridge ไว้ ⇒ bridge ค้าง "running 1489b" แม้ job จบแล้ว จน Panya ต้องกด `RESTART_BRIDGE.bat` (ผมสร้าง .bat ครอบ `pf_bridge_restart.ps1`) 13:04 · เสียเวลาเจ้าของ ~7 นาที · **ห้ามใช้ท่านี้ใน boot job อีก** — ทางที่ถูก: ให้เซิร์ฟเวอร์ log บรรทัดลงทะเบียนเองหลังเปิด log (CORE-REQUEST ถ้า LANE-A ต้องการ) หรือรันเซิร์ฟผ่าน `cmd /c ... > file 2>&1` ใน console ใหม่
4. เวลาจังหวะชน = timestamp ของภาพในเกม (เจ้าของถ่ายภายใน ~2 วิหลังแตะ) ไม่ใช่นาฬิกาจับแยก · ข้อความในแชทของเจ้าของมาช้ากว่า 5-15 วิ · เกาะ 2 ครั้งที่ 3 เป็นของแถม ภาพถ่ายช้าไป 9 วิ

## nonclaims
① ไม่ตัดสินว่า 0x1FB2 คือ "เฟรมเทียบท่า" — ยังไม่มีอะไรตอบกลับ ไม่มีปุ่มยืนยัน ไม่มีการเปลี่ยนฉาก ② ไม่พิสูจน์ความหมายของ id 2/3 (ข้อ 1 ข้างบนเป็นสมมุติฐานให้ LANE-A) ③ ไม่แตะเฟรมขาเข้า/responder/สีป้าย (RE-067)/HP เรือ (GT-109)/กลไก /warp ④ ไม่พิสูจน์อะไรข้าม relog (DB สำเนา) ⑤ ไม่ได้อ่านสีป้ายของภาพ 13:09:17 และ 13:14:18 ⑥ ไม่ได้ commit ไม่แตะ src/ ไม่แตะ matrix/ledger ⑦ เกณฑ์ (ก) วัดด้วยหน้าต่างเวลาของ `GAME_LIVE.txt` (ละเอียด ~2 วิ) ไม่ใช่ timestamp ในเฟรมเอง (เฟรมไม่มี)

## ภาคผนวก — `GT228_hex_windows.txt` (เต็ม)
```
GT-228 R308 hex windows: every inbound frame within +/-5 s of each contact screenshot time (frame time = GAME_LIVE STATE rx timestamp, session 2 = raw GAME_20260904_130510_526308_52808.txt)
frames parsed=565 rx-times=554

=== ISL2-CONTACT-1 (Prison Exile) shot 13:09:32 HUD X-5064 Y4492  window 13:09:27 .. 13:09:37  frames=5
rx=130  t=13:09:28.960000  bytes=69  [(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 8114, 'TriggerVital')] OUTER version=0 mask=0x02 count=2 nested_v <-- TriggerVital 0x1FB2
   12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 02 00 0B 04 2A 78 1C 8B C5 2A AB 98 8D 45 2A 00 00 3A 43 12 90 2A 0B 00 2A 51 00 96 C5 2A 8C C1 90 45 2A 00 00 AC 42 2A 92 88 5F 40 0B 01 0B 00
rx=131  t=13:09:30.782000  bytes=72  [(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 7860, 'COnLandVital')] OUTER version=0 mask=0x02 count=2 nested_v
   12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B4 1E 0B 00 2A 39 75 F0 C3 2A 31 FA 9C C5 2A 7B 54 8E 45 2A 00 00 D8 41 0F 7E 00 12 90 2A 0B 00 2A B2 45 9E C5 2A 9D 67 8C 45 2A 00 00 AC 42 2A 92 88 5F 40 0B 01 0B 00
rx=132  t=13:09:34.190000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=133  t=13:09:34.921000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=134  t=13:09:36.923000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00

=== ISL2-CONTACT-2 (Prison Exile) shot 13:10:15 HUD X-5406 Y4397  window 13:10:10 .. 13:10:20  frames=5
rx=151  t=13:10:11.223000  bytes=44  [(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 10896, 'TargetPosVital')] OUTER version=0 mask=0x02 count=1 neste
   12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12 90 2A 0B 00 2A D8 43 B8 C5 2A D7 E0 54 45 2A 00 00 AC 42 2A ED 3E A2 40 0B 01 0B 00
rx=152  t=13:10:13.238000  bytes=69  [(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 8114, 'TriggerVital')] OUTER version=0 mask=0x02 count=2 nested_v <-- TriggerVital 0x1FB2
   12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 02 00 0B 04 2A 54 6E AF C5 2A 51 14 82 45 2A 00 00 3A 43 12 90 2A 0B 00 2A 54 6E AF C5 2A 51 14 82 45 2A 00 00 AC 42 2A ED 3E A2 40 0B 01 0B 00
rx=153  t=13:10:16.632000  bytes=44  [(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 10896, 'TargetPosVital')] OUTER version=0 mask=0x02 count=1 neste
   12 6F 6E 14 00 00 00 00 08 00 0B 02 12 01 00 12 90 2A 0B 00 2A F4 F0 A8 C5 2A 1C 6A 89 45 2A 00 00 AC 42 2A ED 3E A2 40 0B 01 0B 00
rx=154  t=13:10:17.408000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=155  t=13:10:19.332000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00

=== ISL2-CONTACT-3 (Prison Exile, extra) shot 13:13:35 HUD X-6167 Y5130  window 13:13:30 .. 13:13:40  frames=5
rx=250  t=13:13:30.637000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=251  t=13:13:32.695000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=252  t=13:13:34.545000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=253  t=13:13:36.587000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=254  t=13:13:38.639000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00

=== ISL3-CONTACT-1 (Spice Paradise) shot 13:19:44 HUD X-1560 Y-5331  window 13:19:39 .. 13:19:49  frames=5
rx=433  t=13:19:39.682000  bytes=69  [(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 8114, 'TriggerVital')] OUTER version=0 mask=0x02 count=2 nested_v <-- TriggerVital 0x1FB2
   12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 03 00 0B 04 2A 31 6F C3 C4 2A 04 D9 A4 C5 2A 00 00 3A 43 12 90 2A 0B 00 2A C9 04 C3 C4 2A C5 9C A6 C5 2A 00 00 AC 42 2A 04 8D C1 3F 0B 01 0B 00
rx=434  t=13:19:41.152000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=435  t=13:19:43.194000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=436  t=13:19:45.733000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=437  t=13:19:47.256000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00

=== ISL3-CONTACT-2 (Spice Paradise) shot 13:21:39 HUD X-1877 Y-5370  window 13:21:34 .. 13:21:44  frames=5
rx=491  t=13:21:36.106000  bytes=69  [(0, 28271, 'GSCN_RunTimeProtocolReq'), (15, 8114, 'TriggerVital')] OUTER version=0 mask=0x02 count=2 nested_v <-- TriggerVital 0x1FB2
   12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 03 00 0B 04 2A 03 0C D7 C4 2A E4 1C A4 C5 2A 00 00 3A 43 12 90 2A 0B 00 2A 52 A5 EA C4 2A 56 D0 A7 C5 2A 00 00 AC 42 2A 24 10 DC 3F 0B 01 0B 00
rx=492  t=13:21:37.904000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=493  t=13:21:40.735000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=494  t=13:21:41.829000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00
rx=495  t=13:21:43.924000  bytes=12  [(0, 28271, 'GSCN_RunTimeProtocolReq')] OUTER version=0 mask=0x00 count=0 nested_version=None
   12 6F 6E 14 00 00 00 00 08 00 0B 00

=== all 0x1FB2 frames in session 2
rx=112 t=13:08:52.767000 bytes=69  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 23 00 0B 04 2A 22 0B 3C C4 2A 05 21 44 45 2A 00 00 3A 43 12 90 2A 0B 00 2A D9 02 5A C4 2A 1A 70 46 45 2A 00 00 AC 42 2A 8A F5 5B 40 0B 01 0B 00
rx=130 t=13:09:28.960000 bytes=69  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 02 00 0B 04 2A 78 1C 8B C5 2A AB 98 8D 45 2A 00 00 3A 43 12 90 2A 0B 00 2A 51 00 96 C5 2A 8C C1 90 45 2A 00 00 AC 42 2A 92 88 5F 40 0B 01 0B 00
rx=152 t=13:10:13.238000 bytes=69  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 02 00 0B 04 2A 54 6E AF C5 2A 51 14 82 45 2A 00 00 3A 43 12 90 2A 0B 00 2A 54 6E AF C5 2A 51 14 82 45 2A 00 00 AC 42 2A ED 3E A2 40 0B 01 0B 00
rx=248 t=13:13:26.620000 bytes=69  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 02 00 0B 04 2A E7 65 C8 C5 2A 2C AC 90 45 2A 00 00 3A 43 12 90 2A 0B 00 2A 0C BA C2 C5 2A AA 3C 98 45 2A 00 00 AC 42 2A 80 62 AB 40 0B 01 0B 00
rx=433 t=13:19:39.682000 bytes=69  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 03 00 0B 04 2A 31 6F C3 C4 2A 04 D9 A4 C5 2A 00 00 3A 43 12 90 2A 0B 00 2A C9 04 C3 C4 2A C5 9C A6 C5 2A 00 00 AC 42 2A 04 8D C1 3F 0B 01 0B 00
rx=491 t=13:21:36.106000 bytes=69  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 03 00 0B 04 2A 03 0C D7 C4 2A E4 1C A4 C5 2A 00 00 3A 43 12 90 2A 0B 00 2A 52 A5 EA C4 2A 56 D0 A7 C5 2A 00 00 AC 42 2A 24 10 DC 3F 0B 01 0B 00
```

— ka1-A, 2026-09-04 13:31 +07:00
