# ka1-A — R310 ผล: **GT-219 ขั้น B PASS (GMUI เปิด)** · **auto-walk differential เก็บครบ 3 คลิก** · **วาปสดบันทึกฉาก — ยืนยันบนจอแล้ว (PANYA-DECISION 1430 ปิดได้)** · **P-2 พิกเซล: ชื่อมอนชมพูทั้ง 3 สถานะ** · + คำสั่งใหม่ 1857 (หน้าเลือกตัวแสดง Port Royal ตลอด)

**ADDRESSEE: chief** (GT-219 · เลขใบ auto-walk) · cc: COO · LANE-GM (P-3 · warp) · LANE-UI (auto-walk `1226` · หน้าเลือกตัว) · LANE-B (P-2 attr) · LANE-A
**รอบ:** R310 2026-09-04 18:45-19:07 +07:00 · ผู้ขับ: Panya · ผู้วัด/เขียน: ka1-A
**บูต:** `pirate-force-server` **`d01ae973124abcc3dfcfaff2b0eda679f872a8ae`** (newest green · main head 55c9a05c ต่างกัน 6 ไฟล์ — ไม่เกี่ยวกับใบ) · ไม่มีแฟล็ก · DB สำเนา `state\run_gt219_20260904_184529.sqlite3` · Arena01
**jobs:** 1498 boot (RECHECK + install.bat + DebugView) · 1499 relaunch · 1500 teardown+rollback · **teardown PASS**: stopped ×1 traceback 0 listeners 0 client 0 · canonical sha ก่อน=หลัง `4FF37060…A548454` · integrity ok
**capture root:** `GameClient\capture_r310_20260904_184529\` (รวม `dbgview_r310.log` sha `1B513C4F…C882D93`) · ภาพในเกม `GameClient\Data\ScreenShot\20260904_184909/185512/185526/185844/185906/185916/185937.png`

## 1. GT-219 ขั้น B — **PASS**
- ติดตั้งผ่าน `install.bat` (ไม่ copy เอง): `[ok] plugin_image_check: verdict=image_ok` → `[OK] installed` → sha `4a0ecb58…d743b` size 14848 · ไม่มี `[STOP]`/`[FAIL]`/`[FORCED]`
- DebugView (`dbgview64.exe /l`) จับ **`[GM_PLUGIN]` 10 บรรทัดต่อการเปิด client × 2 ครั้ง = 20 บรรทัด** (คำต่อคำใน `outbox\1500_r310_teardown.out.txt` `GMP>`) — build `Sep 2 2026 18:30:33`, `key=GMUI_1`, `alive, returning interface` ทุกครั้ง · **ตอนกดปุ่มไม่มีบรรทัดเพิ่ม** (เหมือน GT-207)
- **client-observable:** กดปุ่ม GM 1 ครั้ง → **หน้าต่างชื่อ `GMUI` เปิด** (ภาพ `184909.png`: 3 แท็บ ฟังก์ชันพื้นฐาน/ฟังก์ชันซ่อน/กิจกรรม · ช่อง X/Y/Z · NPC · ผู้เล่น · ปุ่ม "ปฏิบัติ") · NO-CRASH · ไม่มีข้อความระบบ
- สีป้ายในภาพ 184909: Arena01 = ขาว · อื่น = none (หน้าต่างบัง)
- rollback: `ROLLBACK removed GameMaster.dll` → เหลือ 0 ไฟล์ · (ก) ต้นฉบับครบ
- `OBSERVER_CONFIRMED: 2026-09-04T18:49+07:00`
⇒ ใบนี้ปิดได้ทั้งสองชั้น (ขั้น A ใบ 1508 + ขั้น B รอบนี้) · nonclaim ตามใบ: ไม่พิสูจน์ (ข), ไม่พิสูจน์เนื้อ manifest, หน้าต่างเปิด ≠ คำสั่ง GM ทำงาน

## 2. auto-walk differential (`1226` · ยังไม่มีเลขใบ — chief ตั้ง) — เก็บครบ 3 คลิก ฉาก 1 · session 1 (raw `GAME_20260904_184*`)
| คลิก | เวลา | เฟรมที่ client ส่ง |
|---|---|---|
| พื้น 1 ครั้ง | ~18:50-18:51 | **`TargetPosVital` เท่านั้น** (เดิน) — ไม่มี 0x4391 |
| NPC (Columbus P65 actor 0x2042) 1 ครั้ง | 18:51:52 / 18:51:54 | `TargetVital 0x1ADD` (40 B, kind=2) แล้ว `ChooseNPC 0x0FB6` (38 B) |
| มินิแมป 1 ครั้ง | 18:52:12 | **`CTracePathReqVital 0x4391`** 25 B payload `0F00000F000014000000000F01000F65010FB2000F007D0802` → server ตอบ `TRACE_PATH_EMPTY_VECTOR_REPLY` (35 B) · ตามด้วย `TargetVital target=clear` 18:52:16 |
⇒ **มีแค่คลิกมินิแมปที่เดิน 0x4391** · คลิกพื้น/NPC ไม่แตะ trace-path เลย · hex เต็มใน `GAME_EVENTS_LIVE.txt` seq 2-5

## 3. วาปสดบันทึกฉาก (server#745 · PANYA-DECISION 1430) — **CONFIRMED บนจอ**
`/warp 2` → `GM_WARP_SCENE_PERSISTED scene=2` ทันที · DB `character_positions` = **(2, 26905, 21185, 1680)** = spawn ของฉาก 2 **โดยผู้เล่นไม่ขยับ** → ปิด X ทันที → relaunch → ล็อกอินโผล่ **เกาะคุก** (ภาพ `185526.png`) ✓ · `GM_WARP_SCENE_PERSIST_FAILED` = 0
⇒ 1430 ปิดได้ · deviation ก่อนหน้า (R309 finding 3 "ต้องเดิน 1 ก้าว") หมดไป

## 4. P-2 พิกเซล (COO `1046`) — ฉาก 2 มอน `Fighting Fish soldier` Lv.25 เลือกด้วย Tab
| จังหวะ | ภาพ | สีชื่อมอน | อื่น |
|---|---|---|---|
| ก่อนตี | 185906 (18:59:06) | **ชมพู** | แผงเป้า HP 3138/3138 · ลูกศรแดงคู่ |
| โดนตี 1 ครั้ง | 185916 (18:59:16) | **ชมพู** | HP 2172/3138 · หลอด HP เล็กใต้ชื่อ |
| ตายแล้ว | 185937 (18:59:37) | **ชมพู** | ศพ**ยืนแข็ง** · ดรอป 2 ชิ้น `Blood Cubic Crystal` ป้ายซ้อนกัน (สีแดงเข้ม) · โมเดลคริสตัลเขียว |
สีอื่นในเฟรม: Arena01 = ขาว · NPC ในกรง `Nautilus Leader` ยศ = **ฟ้า**, ชื่อ `Carle` = **เขียว** (เซิร์ฟเดิม: ชื่อ NPC เหลือง) · มอนตัวอื่น = ชมพูหมด · จดสีอย่างเดียว (RE-067)
⇒ **สีตามสถานะยังไม่มีเลย** (ไม่ส้ม/แดง/เทา) = ค่าตั้งต้นของ P-2 สำหรับวัดหลังแก้

## 5. คำสั่งใหม่ของเจ้าของ (ใบ `20260904_1857_PANYA-DECISION-the-character-select-screen-*`)
หน้าเลือกตัวละครพิมพ์ **"Port Royal"** ใต้ชื่อเสมอ (ภาพ `185512.png`) ทั้งที่ DB = ฉาก 2 และเข้าเกมแล้วอยู่เกาะคุก ⇒ ฟิลด์ชื่อฉากในเฟรมหน้าเลือกตัวเป็นค่าคงที่ · ต้องอ่านจากแถวตำแหน่งจริง

## nonclaims
① ไม่ตัดสินความหมาย payload 0x4391 (LANE-UI) ② ไม่แตะ P-2 สาเหตุสี ③ ไม่พิสูจน์ปุ่มใน GMUI ทำงาน (P-3 ขั้นถัดไป) ④ ไม่ commit ไม่แตะ src/ ⑤ ภาพ 185844 ไม่ได้อ่าน (approach) ⑥ ไม่ได้ทำ GT-184/186 (ต้องแฟล็ก logout scenario — บูตแยก R311)

— ka1-A, 2026-09-04 19:11 +07:00
