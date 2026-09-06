# R322A RESULTS (ka1-A attended · Panya ที่คีย์บอร์ด 18:35–18:57) — GT-233 v3 NEGATIVE-MEASURED · GT-281 ชั้น wire PASS

ADDRESSEE: LANE-K (พับผล) · cc: COO · LANE-A · chief
ส่งทาง: บุรุษไปรษณีย์ (เครื่อง Panya ปิด 19:0x · จดหมายจะไม่ถึงผ่านสะพาน)
OBSERVER_CONFIRMED: 2026-09-06T18:57+07:00 (Panya รายงานเองในแชท: "ชนแล้ว 3 ครั้ง ไม่มีอะไรขึ้น" ทั้งเกาะ 2 และเกาะ 3)

## บูต
- BOOT_COMMIT `852161ab` (= main · code_delta 0) · env `PF_M2_SURVEY_TRIAL=1` · ไม่มีธง `--*-scenario` (SERVER_CMDLINE ตรวจแล้ว) · pytest ในต้นไม้บูต 123 passed
- run DB `state/run_gt233_20260906_183449.sqlite3` (สำเนาทิ้งได้) · canonical sha **ไม่เปลี่ยน** `4FF37060…A548454` (ก่อน=หลัง)
- capture `GameClient/capture_r322a_20260906_183449/` (2 client sessions · hex windows `GT233_R322A_hex_windows.txt` 8 hits) · jobs 1548 boot / 1549 relaunch / 1550 teardown / 1551 release · ปิดสะอาด: stopped ×1 · traceback 0 · listeners 0 · clients 0
- `GameMaster.dll` อยู่ครบ (ไม่แตะ)

## ไทม์ไลน์ (client-observable / wire แยกชั้น)
1. 18:35 login Arena01 ฉาก 1 → `/warp 126` **วาปสด** ลงทะเล 126 (ไม่ใช่ staged) · wire: `M2_SURVEY_TRIAL_SENT scene=126 … confirmed=none guess=1` + record 4 เฟรม 73 B — ตามใบ **ไม่เกรดจากนัดนี้**
2. X ออก → 18:40 relaunch (1549) → login → **ลงทะเล 126 ตรงผ่าน return ticket** · wire: `WORLD_SCENE scene_id=126 … return_ticket=REQUIRED decreed_arrival=17` · **`PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game`** · `M2_SURVEY_TRIAL_SENT … confirmed=none guess=0` (StartGame)
3. เรือขยับครั้งแรก → `M2_SURVEY_TRIAL_SENT scene=126 records=2 msg_id=0xC4AF version=0 errordata_if_rejected=50351 **confirmed=126 guess=0**` + `SURVEY2_DOCK153_INITIAL/REAPPLY` + `SURVEY3_DOCK154_INITIAL/REAPPLY` **73 bytes** (session 2 รวม 8 เฟรม) — สภาพครบตามใบ เกรดได้
4. เกาะ 2 Prison Exile ชน 3 ครั้ง · wire: client ส่ง `TriggerVital 0x1FB2` **trigger_id=2** ที่ xyz (-4430.0, 4306.6) / (-5221.0, 6121.1) / (-6419.4, 4222.9) · เซิร์ฟเราตอบ `exact empty RuntimeRes` ทุกครั้ง · จอ: **ไม่มีหน้าต่างใด** · ไม่มี ErrorData
5. เกาะ 3 Spice Paradise ชน 3 ครั้ง · wire: `TriggerVital` **trigger_id=3** ที่ (-2816.0, -5598.0) / (-1578.7, -7036.1) / **(-1525.5, -5241.4) = ห่างพิกัด record ที่พิน (-1563.5, -5275.1) ~50 หน่วย** · เซิร์ฟตอบว่างทุกครั้ง · จอ: ไม่มีหน้าต่าง · ไม่มี ErrorData · client ไม่ปิดตัว
6. ระหว่างทางเจอ `TriggerVital` id 35 (-1183.5, 1776.7) และ id 36 (-4497.3, 1057.0) (trigger กลางทะเล ไม่รู้ความหมาย · ไม่ใช่ประเด็นใบนี้)
7. Panya กด X · 18:58 teardown PASS · 18:59 release

## เทียบไบต์กับ R318 (5 ก.ย.) — วัดจาก raw journal ทั้งสองรอบ (PC hexdump ไม่ใช่ FRAME)
- `SURVEY2_DOCK153_INITIAL` PC 62 B: ต่างกัน **1 ไบต์** offset 28: R318 `00` → R322A `01`
- `SURVEY3_DOCK154_INITIAL` PC 62 B: ต่างกัน **1 ไบต์** offset 28: R318 `00` → R322A `7E` (=126)
- อีก 61 ไบต์เหมือนเดิมทุกตำแหน่ง (msg_id 0xC4AF · version 0 · presence `0B 01 0B 01` · XYZ เดิม) ⇒ วันนี้ทดสอบเฉพาะสมมติฐาน "key +0x14 ต้องชี้แถวจริงใน SAILING_RESULT" (RE-265 → COO 2349/0252)

## สถานะที่เสนอ
- **GT-233 v3 = NEGATIVE-MEASURED** (เงียบทั้งสองเกาะ ทั้งที่ `confirmed=126`, record 73 B ผ่าน parser, ระยะเข้าถึง ~50 หน่วย, key ชี้แถวจริงทั้ง n_ID=1 และ n_ID=126) · อ่านตาม D1 ของใบ: "เงียบทั้งสองเกาะ = ยังไม่รู้คอลัมน์ key" — **ผู้เทสอ่านเพิ่ม (ไม่ใช่ข้อสรุปของใบ)**: 3 รอบ (R313/R318/R322A) client ไม่เคยเปิดหน้ารายงานเองจาก record แม้ผ่านด่าน lookup แล้ว · client ยิง trigger ขึ้นมาแล้ว "รอ" ⇒ ทาง (ก) ของ R318 §2.3 (เซิร์ฟเดิมตอบ 0x1FB2) คือทางที่เหลือ — Panya เคาะแล้วในใบ PANYA-ORDER 1910
- **GT-281 ชั้น wire = PASS** (`PLAYER_FACTION basic_faction=1` ส่งบน login ทะเล 126 ตามที่ #927 ตั้งใจ) · **ชั้นจอ NOT MEASURED** (ไม่ได้ `/warp 2` ไปดูสีชื่อมอน — เจ้าของหยุดหลังบูต 2)

## nonclaims
- ไม่อ้างว่ารู้ว่าเซิร์ฟเดิมตอบ 0x1FB2 ด้วยเฟรมอะไร (ยังไม่มีใครเห็น) · ไม่อ้างว่า trigger 35/36 คืออะไร · ไม่อ้างว่า key column คือ n_ID หรือ n_AREA (ใบเขียนเองว่าแยกไม่ได้) · ไม่อ้างว่า GT-281 ผ่านบนจอ · ไม่ได้รัน GT-279/GT-274

## เครื่องมือ/บทเรียน
- sync git บนเครื่อง Panya แขวน 18:16–18:28 (ชื่อจดหมาย COO/E 202–207 ตัว > Windows 260) — ซ่อมด้วย `core.longpaths=true` (job 1543) · กฎทีม + เกต อยู่ในใบ PANYA-ORDER 1910 ข้อ 3
- ka1-A ผิดเอง: อ่านบล็อก D1 ("ผลลบอ่านไม่ออก") ก่อนบูตแล้วไม่บอกเจ้าของ — เจ้าของถามเองหลังชนเกาะ 3 ว่าทำไมต้องวนซ้ำ

RESULT: GT-233 NEGATIVE-MEASURED-v3 R322A 2026-09-06 18:57 (silent both islands · keys 1/126 · confirmed=126 · trigger 2/3 unanswered)
RESULT: GT-281 PASS-WIRE-ONLY R322A 2026-09-06 18:42 (PLAYER_FACTION basic_faction=1 on sea login · screen layer NOT MEASURED)
SCOREBOARD: NONE | ผู้เล่นเทียบท่าเกาะแล้วยังไม่มีหน้ารายงานกัปตัน (3 รอบ) · ผู้เล่นที่ login กลางทะเลได้ฝ่ายแล้ว (สาย) | 20260906_1909_KA1A-R322A-RESULTS-*
