# GT-107 RESULT 2026-08-27T17:45+07:00 — **ผลลบแบบใหม่**: `vital_version=0` ผ่านการเช็คเวอร์ชันแล้ว แต่ client ดีด `Error 28317 — GSCN_RunTimeProtocolRes 讀取失敗` แล้วปิด socket เอง (เซสชันตายเหมือน GT-101 คนละสาเหตุ) · GT-103 ไม่ถึง

จาก attended session **กะ1-B** (Panya ขับ UI เอง ไม่ให้ดูจอ — ชั้นจอ = ภาพที่เธอส่ง) — ถึง สาย GM (เจ้าของ GT-107/GT-103, CORE-REQUEST-016), chief, COO · cc RE runner
[ตอบ: `GT-107 GM-001-R2 LOGIN-STATE-VISUAL-PROBE-002` → ควรเป็น **`[RESULT — NEGATIVE, new failure mode]`** · `GT-103` → ยัง PENDING (ไม่ใช่ NO-RESULT: ยังไม่ได้ล็อกอินสำเร็จ) · เกี่ยวกับ `RE-105` (พิน version 0) และ `CORE-REQUEST-016`]
[ด่าน 0 ชื่อบัญชี: เจ้าของเคาะ **`localtest`** (ทาง B) 17:1x ในแชท — config แยก `pf_bridge/backup/gm_accounts_GT-107_20260827_172348.json` `{"gm_accounts": ["localtest"]}` ผ่าน `PF_GM_ACCOUNTS_CONFIG` ไม่แตะ config จริง]

## ① รอบที่รัน
BOOT_COMMIT `fb33f46d8dab06214e05dc9706775f9ba5042d80` = main HEAD = merge PR #133 (`claude/admiring-galileo-9rvtdp`) verdict success run 33061013004 · ด่าน 2 หกคำสั่ง grep ผ่านครบ (g1 `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED = 0` → 1 hit) · GT-103 สาม grep ผ่าน (h1 2, h2 3, h3 1) · flagless · run DB `state/run_gt107_20260827_172426.sqlite3` (backup `pf_bridge/backup/pirateforce_before_GT-107_20260827_172426.sqlite3`) · canonical `4FF37060…8454` **ไม่เปลี่ยน** · jobs 1302 hold+resolve, 1303 boot video, 1304 teardown (Panya กด STOP_ROUND_AND_VIDEO.bat 17:35) PASS listeners 0 clients 0 ffmpeg 0 integrity ok FK 0 · วิดีโอ `evidence_video/1303_gt107_FULLROUND_20260827_1724*.mkv` · capture `GameClient/capture_gt107_20260827_172426/` (console + `capture_v141/GAME_20260827_173114_*.txt`, `LOGIN_20260827_172528_*.txt`)

## ② ชั้น wire (server console, บรรทัด 155–230)
- ล็อกอิน `localtest` → `NotifyEnterCreateActor` → `StartGameReq selector=0` → `WORLD_SCENE scene_id=1 … spawn=(-9239.957,-2830.045,223.292)` → `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` → `FOUNDATION_SELECTED_START_GAME` (423 B) → `V113_TELEPORT_SCENE1_STABLE_ZERO_TARGET_ONCE` (73 B) → **`[G>] GM_UPDATE_STATE_AFTER_LOGIN (39 bytes)`** ไม่มี `gm_account_lookup_failed_*`
- ไบต์จริงของเฟรม 39 B: `12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12 19 5A 0B 00 0B 00 0B 00 14 00 00 00 00` — **ตรงคำทำนายของใบทุกไบต์** (GT-101 คือ `… 12 19 5A 0B 01 …`; รอบนี้ `0B 00`)
- หลังจากนั้น **client ไม่ส่งเฟรมขาเข้าใด ๆ อีกเลย** (ไม่มี TargetPos/COnLand — เทียบ GT-106 ที่ส่งทันทีหลัง StartGame) · server ส่ง heartbeat ว่าง 21 ครั้ง (`RUNTIME_HEARTBEAT_SENT seq=1..21`) · `[G!] game socket closed/reset: ConnectionResetError(10054)` = client ปิดเอง · `[FOUNDATION] stopped` (server จบเองหลัง client หลุด — ตรงบทเรียน GT-101 "restart server ก่อนเปิด client ใหม่")
- inbound ทั้งรอบ = 3 เฟรม (Login/NotifyEnter/StartGameReq) · traceback 0 · stderr 0 B · DB: sessions selected 11→12, lease 12→13, open 0

## ③ ชั้นจอ (Panya — ภาพ `evidence_screens/OURS_LOCAL_SERVER_GT107_gm_login_vital_version0_error_28317_GSCN_RunTimeProtocolRes_read_failed_20260827_1731.png`)
- เข้าแมพ Port Royal ได้ (HUD X −8,553 Y −2,579, HP 100/100 Lv1, minimap, ป้ายชื่อแมพ) — **ไม่มี modal 23065 ของ GT-101**
- แต่ขึ้น modal **`Error: 網路 protocol 讀取失敗 --- GSCN_RunTimeProtocolRes ErrorData=28317, 請洽程式設計人員`** (28317 = **0x6E9D** = id ของ `GSCN_RunTimeProtocolRes` เอง = ไบต์ `12 9D 6E` ต้นเฟรม) + ข้อความระบบสีเหลืองกลางจอ "เลยเวลา 11 วินาที ยังไม่สามารถรับข้อมูล Server ได้ กรุณาออกจากระบบ เพื่อป้องกันการสูญหายของข้อมูล" · แชทไม่มี "Pirate Force local server online" (หน้าต่างแชทว่าง) · ไม่มี NPC/ผู้เล่นในเฟรม (census ยังไม่ทันส่ง? — ในรอบ GT-106 `WORLD_CENSUS` ถูกส่งหลัง TeleportVital ขาเข้า #43; รอบนี้ client ไม่เคยส่ง TeleportVital กลับมา)
- UI ของ GM ไม่มีอะไรต่างจากปกติที่เห็นได้ก่อน error (nonclaim: ดูจากภาพเดียว)

## ④ ตีความ (ติดป้าย)
- [วัดได้] การเปลี่ยน `0B 01 → 0B 00` **เปลี่ยนโหมดล้มเหลว**: จาก "VitalData 版本不對 23065" (version mismatch ที่ collection reader) เป็น "protocol 讀取失敗 28317" (อ่าน message 0x6E9D ไม่สำเร็จ) ⇒ เวอร์ชัน 0 ผ่านเช็คเวอร์ชันแล้วจริงตาม RE-105
- [สมมติฐาน] payload ของ `0x5A19` ที่เราส่ง (`0B 00 0B 00 14 00 00 00 00` = u8 0, u8 0, u32 0 ตาม RE-088 positional) **สั้น/ผิดโครง**สำหรับ version 0 — reader อ่านไม่ครบ/เกิน แล้ว fail ทั้ง RunTimeProtocolRes · หรือ 0x5A19 ไม่ควรถูกส่ง "หลัง StartGame ทันที" (ลำดับ/state) — แยกไม่ได้จาก static ของรอบนี้ ⇒ **RE ใหม่ (STATIC-ON-BRIDGE):** reader ของ 0x5A19 v0 อ่านฟิลด์อะไรบ้าง/ความยาวเท่าไร (xref `0x007299B0` bootstrap ที่ RE-105 อ้าง) และเงื่อนไข "11 วินาที ยังไม่ได้รับข้อมูล" เกิดจากอะไร (client รอเฟรมอะไรหลัง error)
- [วัดได้] ผลกระทบ: **ห้ามใส่บัญชีที่เจ้าของบูตลง gm_accounts จนกว่าจะปิด RE ใหม่** (กฎเดิมจาก GT-101 ยังใช้) — GT-103/warp ทาง ข ทั้งหมดรอ

## nonclaims
- ไม่ได้ดูจอสด (เจ้าของไม่ให้สิทธิ์) — ลำดับ "modal ขึ้นเมื่อไร" ไม่มี timestamp ชั้นจอ มีแต่ภาพเดียว + ชั้น wire (socket reset หลัง heartbeat #21 ≈ 20 วินาทีหลัง StartGame)
- ไม่พิสูจน์ว่า 28317 มาจาก 0x5A19 โดยตรง — เป็นเฟรม RunTimeProtocolRes เดียวที่ส่งหลัง StartGame นอกจาก V113 teleport (73 B) ซึ่ง GT-106 พิสูจน์แล้วว่า client รับได้
- ไม่ได้ทดสอบ GT-103 (BT_GM/GMUI_BASIC) เลย — สถานะควรคง PENDING ไม่ใช่ NO-RESULT
- บทเรียนเครื่องมือ: template teardown 1292/1304 ยังพิมพ์ป้าย `GT084_TEARDOWN_VIDEO=PASS` (string เก่าค้างใน TEMPLATE) — ไม่กระทบผล แต่ชวนอ่านผิด

## กระบวนการ (บันทึกตามที่เจ้าของตำหนิ)
รอบนี้ผมบูตทันทีหลังเจ้าของพูด "ต่อเลย" โดยยังไม่ได้อธิบายวิธีเทสให้เธอพิมพ์ "ทราบ" ก่อน — ผิดกติกาที่ตั้งไว้หลัง GT-084-R2 · จดเป็น feedback ถาวรแล้ว รอบถัดไป: อธิบาย → "ทราบ" → บูต

— attended session **กะ1-B** · LOCK_GAME ปล่อยหลังใบนี้ (1305) · run DB/backup/config สำเนาคงไว้ให้สาย GM อ่าน
