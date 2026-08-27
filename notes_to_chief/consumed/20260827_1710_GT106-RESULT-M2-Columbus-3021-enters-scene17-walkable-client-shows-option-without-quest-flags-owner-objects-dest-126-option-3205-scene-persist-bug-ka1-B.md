# GT-106 RESULT + M2 Columbus probe 2026-08-27T17:10+07:00 — **ผู้เล่นออกจากเมืองผ่าน Columbus (3021) เข้าฉาก 17 ได้จริง ยืน/เดินบนดาดฟ้าได้** · client แสดงและกดตัวเลือก 3021 ได้โดยไม่มี flag เควส 110/739/111 (RE-106 ตอบเชิงจอ) · แต่เจ้าของแย้ง 3 ข้อ: ปลายทางต้องเป็นทะเล 126 ไม่ใช่ "Ship in the Sea" 17, ต้องมีออปชัน 2 (3205 bornagain), ตำแหน่งหลังวาร์ปถูกบันทึกเป็นฉาก 1 (บั๊ก)

จาก attended session **กะ1-B** (Panya ขับ UI เอง ผู้ช่วยเก็บหลักฐาน) — ถึง chief (เจ้าของ GT-106 / CORE-REQUEST-014), COO · cc สาย A (roster/scene), สาย B, สาย GM, RE runner
[ตอบ: `GT-106 SCENE17-PROVISIONAL-ARRIVAL-001` (PENDING → มีทางเข้าแล้ว) · `20260827_1545_CHIEF-STATUS-M2-quest-gate-skip-*` (คำถาม: client ยอมให้เลือก 3021 ไหม) · `20260827_1600_CHIEF-STATUS-M2-console-token-fix-plus-two-real-risks-*` · `RE-106`]
[อ่านกล่อง 30 นาทีล่าสุดแล้ว — ไม่มีใบใหม่หลัง 1600 นอกจากของกะ1-B]

## สถานะที่ควรเป็น
- **GT-106 → `[DONE]` ผลบวก**: เข้าฉาก 17 ด้วย (0,0,0) แล้ว client วางผู้เล่นบนดาดฟ้าเรือ ยืนได้ เดินได้ ไม่ตก ไม่ค้าง (claim เดียวของใบ)
- **CHIEF-STATUS 1545 ชิ้นที่ 4 (quest-gate skip)**: **ไม่ต้องทำ** — client แสดงตัวเลือก 3021 และส่ง `QuestOperateVital` ออกมาจริงทั้งที่ไม่มี flag 110/739/111 ⇒ ทาง "server-authoritative พอ" ตามที่ chief เขียนไว้ · RE-106 ปิดได้เชิงจอ (nonclaim ด้านล่าง)
- **M2 ตามสเปค 1525**: ผ่านชั้นจอ+wire ทุกข้อในตาราง (Columbus index 1 → 3021 → ฉาก 17 (0,0,0) → เล่นต่อได้) — **แต่เจ้าของดูแล้วแย้งว่าปลายทาง/ออปชัน/การบันทึกยังไม่ถูก** (ข้อ ④) ⇒ COO/chief เคาะว่า M2 "ผ่านแบบมี nonclaim" หรือรอแก้ ④ ก่อน

## ① รอบที่รัน
BOOT_COMMIT `0c8588845e63d70c3f08cfd6e808e1174858d8be` = main HEAD = merge PR #124 (`claude/awesome-darwin-e0daaa`) verdict success run 33057228498 · flagless (no scenario/export-events/second-password-mode) · run DB `state/run_gt106_20260827_163512.sqlite3` (backup `pf_bridge/backup/pirateforce_before_GT-106_20260827_163512.sqlite3`) · canonical `4FF37060…8454` **ไม่เปลี่ยน** ก่อน/หลัง · jobs 1298 hold+resolve (gate: dispatch+novehicle+provisional ผ่าน, code-delta 0) · 1299 boot video · 1300 teardown video (Panya กด STOP_ROUND_AND_VIDEO.bat 16:46) PASS listeners 0 clients 0 ffmpeg 0 integrity ok FK 0 · วิดีโอ `evidence_video/1299_gt106_FULLROUND_20260827_163516.mkv` (55 MB, 16:35–16:46) · เฟรม `evidence_screens/FRAME_1300_gt106_teardown_{5s,326p85s,650p7s}_*.jpg` · ตัวละคร Arena01 Lv1 เริ่มที่ Port Royal HUD X −8,174 Y −2,612 (ท่าเรือ)

## ② ชั้นจอ (client-observable — Panya เห็นเอง, ภาพใน evidence_screens/)
1. `OURS_LOCAL_SERVER_PortRoyal_harbor_Columbus_index1_still_labelled_Sebastian_dialog_3021_only_20260827_164x.png` (ภาพจาก Panya): NPC index 1 ที่ปืนใหญ่ **ยังชื่อ "Warden / Sebastian"** (roster ยังไม่แก้) · target panel บนซ้าย "Sebastian HP 100 LV 1" · คลิกคุย → หน้าต่าง QUEST หัว "Prison Exile Island …" (ข้อความของ NPC 2) มี**ตัวเลือกเดียว** "มุ่งหน้าไป Atlantic Ocean: Rising Sun Sea" · Panya กดครั้งเดียว
2. `OURS_LOCAL_SERVER_GT106_scene17_ShipInTheSea_arrival_X0_Y0_20260827_164301.png`: ฉากเปลี่ยนทันที ชื่อฉากมุมขวาบน **"Ship in the Sea"** ป้ายกลางจอ "Ship in the Sea" HUD **X:0 Y:0** ตัวละครยืนบนพื้นไม้ (ดาดฟ้า) ฟ้า/ทะเลรอบ ๆ ไม่มี NPC ไม่มีผู้เล่นอื่น minimap เป็นเข็มทิศเปล่า
3. `…scene17_walked_to_X-639_Y200_deck_cabin_20260827_164348.png`: เดินได้ HUD **X:−639 Y:200** เห็นห้องท้ายเรือ ประตู คบไฟ ถัง — พื้นเดินได้ปกติ ไม่ตก ไม่หลุดขอบ
4. `…scene17_third_shot_20260827_164516.png` (ภาพที่ 3 ของเจ้าของ)
[เห็นในภาพ] ไม่มีการแปลงร่างเป็นเรือ (ตามสเปค 1525 ไม่ต้อง) · ไม่มี message ระบบนอกจาก "รูปถูกบันทึกไว้ที่ …"

## ③ ชั้น wire/DB (`GameClient/capture_gt106_20260827_163512/server_console_live.out.txt` 4,031 บรรทัด)
- ล็อกอิน: `WORLD_CENSUS assembled=115/115` initial + reapply (ปกติ)
- คุย NPC: `[G>] V98_NPC_CONVERSATION_DEFAULT_P1` แล้ว `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE` (49 B; มี `12 CD 0B` = quest 0x0BCD = 3021)
- **client → server `[G< #86] QuestOperateVital` 43 B** payload `… 12 CD 0B 08 01 …` = quest 3021 op 1 (accept) — **เฟรมนี้ออกจาก client จริงทั้งที่ไม่มี flag 111** ⇒ ตอบคำถาม 1545/RE-106 เชิงพฤติกรรม
- server: `WORLD_SCENE scene_id=17 seq=0 model=Bg1001 name=a_ship_at_sea spawn=(0.000,0.000,0.000) sent_before=NO population=none save=0 marker=0 return_ticket=REQUIRED` → `SCENE_ENTRY scene=17 xyz=0.000,0.000,0.000 source=PROVISIONAL-OWNER-DECREE-20260827-1445` → `COLUMBUS_QUEST3021_NO_VEHICLE_DISPATCH scene=17 source=M2-NO-VEHICLE-OWNER-20260827-1525` → `[G>] CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE` (73 B) — **ยิงครั้งเดียว สำเร็จครั้งแรก** (ความเสี่ยง FSM/one-shot ของ 1600 ไม่เกิด)
- หลัง teleport client ส่ง `TargetVital` ×1, `TargetPosVital` ×10, `COnLandVital` ×8, `ActionVital` ×3 = client รับฉาก 17 แล้วเดิน/ลงพื้นจริง · ไม่มี traceback, stderr 0 B
- **DB หลังรอบ (run DB, ro): `character_positions` ของ Arena01 = `scene_id=1, x=−149.0, y=−1250.3, z=745.0` (updated 16:45:36)** — พิกัดเป็นของฉาก 17 (ตรงกับที่เดิน) แต่ **scene_id ยังเป็น 1** ⇒ ดูข้อ ④.3 · sessions selected 11→12, lease 12→13, open 0

## ④ เจ้าของแย้ง (คำของ Panya หลังเทส) + สิ่งที่ผมเช็คในตารางแล้ว
1. **ออปชันของ Columbus Port Royal ต้องมี 2 ข้อ**: "มุ่งหน้าไป Atlantic Ocean: Rising Sun Sea" และ "**save Port Royal เป็นจุดเกิด**" — ค้น gamedata แล้ว **เจอ**: `MOBS 156 s_QUEST_BEGIN = 111;998;3021;3205;7062;7063` · **3205 = Q_BORNAGAIN "ตั้งฐานทัพที่ Port Royal"** (`n_VARI_2=1` → lua `Player.ResetMarker(1)`) = ออปชันที่ 2 · 998 Q_CON1 Lv1 "พี่สาว โปรดแนะนำด้วย" (n_VARI_1=111) · 7062/7063 Q_ENTER_INSTANCE6 Lv50/70 (Eagle/Bear Island) ⇒ dialog ที่เราสร้างมีแค่ 3021 ใบเดียว (chief ต่อสายเฉพาะ 3021)
2. **ปลายทางผิดฉาก**: เกมเดิม กด "มุ่งหน้าไป Atlantic Ocean" แล้ว**แปลงร่างเป็นเรือและโผล่ในแมพ "Atlantic Ocean: Rising Sun Sea"** ไม่ใช่ "Ship in the Sea" — ค้นแล้ว: `TEXTDATA_TH__SCENE_NAME_TIP` ฉาก **17 = "Ship in the Sea" (GM: เรือในทะเล 1)**, 18–23 = เรือในทะเล 2/3 รูปแบบ 1–3, 62–67 = แบบ_เปลี่ยนรูป · ฉาก **126 = "Atlantic Ocean：Rising Sun Sea" (GM: Atlantic Ocean1)** · `MAP_SCENE_LIST` แถว 1: n_NAME_ID 126 s_MAP_NAME `Bg3001_air_400` · ชื่อเควส 3021 = ชื่อฉาก 126 ตรงตัว แต่ `q_teleport1.lua` `Player.Teleport(Quest.Var2)` กับ n_VARI_2 = 17 ⇒ **[ไม่รู้]** เซิร์ฟเวอร์เดิมแปลง "17" เป็น "ฉาก 126 + เรือ" อย่างไร (Player.Teleport ฝั่ง client เป็น stub เซิร์ฟเวอร์ตัดสินเอง; เควสเดินทางไปเกาะ 3000–3020 ใช้ `Q_TELEPORT_WITH_VEHICLE1` → `Player.TeleportWithVehicle(scene เกาะ)`) — ต้องการหลักฐานเพิ่ม (RE ใหม่ หรือคลิปออกทะเลของเซิร์ฟเวอร์เดิม) · [สมมติฐาน] ฉาก 17–23 (เรือ 1/2/3 ลำ) = ฉาก "บนเรือ" ที่ใช้ตอนอยู่กลางทะเล ไม่ใช่ตัวแมพทะเล
3. **บั๊ก persistence**: ตำแหน่งหลังวาร์ปถูกบันทึกเป็น `scene_id=1` + XYZ ของฉาก 17 (−149, −1250, 745) ⇒ ล็อกอินครั้งหน้าจะเกิดที่ Port Royal พิกัดนั้น (อาจอยู่ในน้ำ/นอกพื้น) · `WORLD_SCENE … return_ticket=REQUIRED` บอกอยู่แล้วว่าเซิร์ฟเวอร์รู้ว่ายังไม่มีทางกลับ — chief/สาย A ควรตัดสินว่า (ก) บันทึก scene 17 ตามจริง หรือ (ข) ไม่บันทึกตำแหน่งขณะอยู่ฉาก 17 · **run DB นี้อย่าเอาไป promote เป็น canonical**
4. index 1 ยังชื่อ Sebastian/Warden — เรื่องเดิม (roster สาย A)

## nonclaims
- "client ไม่มีเกตฝั่งตัวเอง" พิสูจน์แค่ว่า **ด้วย dialog ที่เซิร์ฟเวอร์เราสร้าง** client แสดงและกด 3021 ได้ — ไม่พิสูจน์ว่า `Accept_Check`/`GetQuestFlag` ถูกเรียกหรือไม่ และไม่พิสูจน์ว่าไคลเอนต์เก็บ flag เควสอย่างไร (RE-106 ปิดได้แค่ "ไม่จำเป็นสำหรับ M2")
- ไม่ได้วัด client FSM state ตอนรับ TeleportVital — แค่ครั้งนี้รับ
- ไม่ได้ทดสอบซ้ำครั้งที่สองใน connection เดียว (one-shot lock) และไม่ได้ทดสอบกลับเมือง
- "เดินได้" = TargetPos/COnLand จาก client + ภาพ 2 ใบ ไม่ได้วัดขอบแมพ/น้ำ
- ฉาก 17 ไม่มี NPC/มอน (population=none) ตามที่ registry ตั้งไว้ — ไม่ใช่ผลลบของอะไร

## ที่ผมทำต่อ/ไม่ทำ
LOCK_GAME ปล่อยหลังใบนี้ (job 1301) · run DB/backup คงไว้ให้ chief อ่าน · ไม่แก้ GAME_TEST_QUEUE/CLIENT_RE_QUEUE (chief ยกไปแปะ) · บทเรียนเครื่องมือ: jobs 1298–1300 ถูก generate จาก 1294–1296 แค่เปลี่ยน gate (ใช้ซ้ำได้สำหรับรอบ Columbus ถัดไป)

— attended session **กะ1-B** · ภาพ: `evidence_screens/OURS_LOCAL_SERVER_GT106_*`, `OURS_LOCAL_SERVER_PortRoyal_harbor_Columbus_index1_still_labelled_Sebastian_dialog_3021_only_*` · วิดีโอ `evidence_video/1299_gt106_FULLROUND_20260827_163516.mkv`
