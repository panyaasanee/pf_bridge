# R322B RESULTS (ka1-A attended · Panya ที่คีย์บอร์ด 00:48–01:19 · ka1-A ขับ GMUI ด้วย computer use 01:11–01:17) — GT-281 ชั้นจอ PASS · GT-279 ได้เฟรม 0x51E9 จริง · ช่องว่างตาราง hostile ฉาก 2

ADDRESSEE: LANE-K (พับผล) · cc: COO · LANE-A · LANE-B · LANE-GM · LANE-DB · chief
ส่งทาง: สะพาน (เครื่องเจ้าของเปิด)
OBSERVER_CONFIRMED: 2026-09-07T01:05+07:00 (Panya: "ตีมอนตายได้ และทุกการคลิกตัวละครออกท่าฟันได้แล้ว" + ภาพ 3 ใบ · ชื่อมอนชมพู)

## บูต
- BOOT_COMMIT `c26ad70b` (= main ณ ตอนบูต · code_delta 0 · มี #927) · ไร้ธง ไร้ env · pytest ในต้นไม้ 46 passed · run DB `state/run_gt281_20260907_004747.sqlite3` (ใหม่จาก canonical) · canonical sha **ไม่เปลี่ยน** `4FF37060…A548454`
- capture `GameClient/capture_r322b_20260907_004747/` (2 client sessions · hex windows `R322B_GROUP1_hex_windows.txt` 38 hits) · jobs 1544/1545/1546/1547 · ปิดสะอาด stopped ×1 · traceback 0 · listeners 0 · clients 0 · `GameMaster.dll` อยู่ครบ

## GT-281 BASIC-FACTION-EVERY-LOGIN-SCENE-SEA-126 — **PASS ทั้งสองชั้น**
- ขั้น: login Arena01 ฉาก 1 → `/warp 126` (วาปสด) → X → relaunch (1545) → login **ลงทะเล 126 ผ่าน return ticket** (`WORLD_SCENE scene_id=126 … return_ticket=REQUIRED` บรรทัด 1245) → `/warp 2`
- wire: `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` **บน login ทะเล** (บรรทัด 1248) — สิ่งที่ R321 ไม่มี
- จอ (Panya + ภาพ): Fighting Fish soldier ชื่อ**ชมพู ไม่เขียว** · คลิกโจมตีติด · มอนตาย · wire: `damage announced -966, applied 966, hp 3138 -> 2172` (max HP ตรงตาราง 3138) · `POSE_PRODUCTION class=1 equip_type=1 base=2 behavior=280` = ท่าฟันดาบที่เจ้าของเห็นทุกคลิก (ผลข้างเคียงของ GT-274 บน main — ดาบยังไม่ชักออกจากหลังเพราะยังสวมอาวุธไม่ได้ RE-280)
- **หลอดฟ้าใต้ชื่อ + แผงตัวเอง HP -1**: ยังมีอยู่ **ทั้งที่ faction มาครบ** ⇒ **ไม่ใช่เรื่องฝ่าย** — ในทะเลแผงโชว์ HP **-1/1** (BoatHealth ไม่ถูกตั้ง) และหลังขึ้นบก คลิกตัวเองแผงยัง HP -1 LV1 (เจ้าของสังเกตเอง) = เซิร์ฟไม่สลับ HP เรือกลับเป็น HP ตัวละครตอนออกจาก 126 (= finding R307 3 ก.ย. "หลอด HP ใต้ชื่อค้างบนบก") · R321 โยงหลอดกับ faction **ผิด** — ขอให้ A แยกเกณฑ์ "ไม่มีหลอดฟ้า" ออกจากใบ 281 ไปเป็นใบสร้างของ A/DB: "ออกจาก 126 ต้องส่ง HP/หลอดตัวละครกลับ และ BoatHealth ห้ามเป็น -1"
- **ปลดล็อก**: GT-220 / GT-223 (BLOCKED จน GT-281 ผ่านจอ) เดินต่อได้

## GT-279 GM-PANEL-BUTTON-CAPTURE — **client PASS (ได้เฟรม) · server NEGATIVE (ไม่ตอบ ไม่ capture)**
- เจ้าของคลิกทุกปุ่ม/แถว 3 หน้าก่อน → **0 เฟรม** · ka1-A ขับต่อ (computer use): **แถวทั้ง 3 หน้าเป็น radio เลือกคำสั่ง ตัวส่งจริงคือปุ่ม "ปฏิบัติ" มุมล่างขวา** (ใบ 279/269 ไม่เคยระบุ)
- กดปฏิบัติ 5 ครั้ง → client ยิง **`GM_RunGMCommandVital` 0x51E9 3 เฟรม** (PC hexdump หลัง id `E9 51`):
  1. หน้า 1 แถว 1 "ตัวละครซ่อนตัว: ซ่อนตัว" 44 B: `0B 00 0B 01 14 01000000 14 00000000 0B 01 48 00000000 48 00000000`
  2. เดิม เลือก "ปรากฏตัว" 44 B: `0B 00 0B 01 14 01000000 14 00000000 0B 00 48 00000000 48 00000000` (ต่างไบต์เดียว: u8 หลัง u32 คู่ = 01→00)
  3. หน้า 1 แถว 2 "วาร์ป" ช่องว่าง X/Y/Z=0 46 B: `0B 00 0B 01 14 00100000 14 00000000 0B 00 48 02000000 3000 48 00000000` (u32 แรก = 0x1000 · `48 02000000 3000` = สตริง UTF-16 "0" ยาว 2 ไบต์)
  - หน้า 2 แถว 1 (มอนสเตอร์ที่เกิด ช่องว่าง) และหน้า 3 แถว 1 (ไอเทม 0) กดปฏิบัติแล้ว **client ไม่ส่ง** (คาดว่ากันช่องว่างฝั่ง client — nonclaim)
- server: ตอบ `exact empty RuntimeRes` ทุกครั้ง · **ไม่มีโฟลเดอร์ `capture/gm_command_capture` ใต้ต้นไม้บูต** ⇒ hook `gm/dispatch.py → capture_raw_gm_command` ที่ใบอ้าง **ไม่ได้เขียนไฟล์** (ต้องหาว่าเฟรมไปทางไหน — v141 path หรือ allowlist บัญชี) — นี่คือผลลบที่ใบบอกว่ามีค่า
- ป้ายหน้า GMUI (อ่านจาก zoom): หน้า 1 "ฟังก์ชั่นพื้นฐาน": ตัวละครซ่อนตัว(ซ่อน/ปรากฏ) · วาร์ป+X/Y/Z · NPC เพิ่ม · ผู้เล่นเพิ่ม · ตามผู้เล่น · ตามผู้เล่น(2) · ข้อมูลผู้เล่น(ช่องยาว) · หน้า 2 "ฟังก์ชั่นเสริม": มอนสเตอร์ที่เกิด · ลบมอน · ประกาศ(ประกาศ/ปิด)+ระยะเวลา+ข้อความ · ประกาศระบุผู้เล่น+ชื่อ+สาระ+ระยะเวลา · ไล่/ไอดี · หน้า 3 "ฟังก์ชั่นไอเทม": ไอเทม+จำนวน · BUFF · เปลี่ยนค่า · แสดง(เปิด/ปิด) · ติดตาม+จำนวน · ทุกหน้ามีปุ่ม "ปฏิบัติ" เดียว (ภาพ zoom อยู่ในแชท ka1-A; ป้ายบางคำอ่านไม่ชัด nonclaim)

## finding ข้ามสาย (วัดในบูตเดียวกัน)
1. **ตาราง hostile ฉาก 2 ตกมอนตามกฎ** — census บรรทัด 2335: `MOB_CENSUS_HOSTILITY scene_id=2 roster=12 backed=12 refused=8` · roster ฉาก 2 มี Mountain Deer(27) · Lion pirates(29 ×7) · Desert Eagle(30 ×4) · Rock turtle(32) · Sediment Wolf(33 ×3) ซึ่ง **ทุกตัว rank 1 + AI_COMBAT ≠ 0** (150/110/210/164/100) แต่ `field_mob_tables_bg0002.HOSTILE_PLACEMENTS` มีแค่ 17 แถว (Eagle 3 บนเขา · Fish 6 · Sergeant 3 · Orc Chief 5 ถูกกัน) ⇒ ตัวอื่นส่งเป็น civilian · **บนจอ Desert Eagle ชื่อเขียว ข้าง ๆ Fighting Fish ชมพู** (ka1-A เห็นเองตอนขับ) — คำอธิบายที่เจ้าของถามว่า "ทำไมมีแต่ปลาตีได้" · B: ต้อง regenerate ตารางจากกฎบน roster ที่ A ส่งจริง ไม่ใช่ crosswalk 17 แถว (คำอ้าง `2022` ว่า derive "จาก roster ที่ shipped = เอาต์พุตของกฎ" ยังไม่จริงสำหรับฉาก 2)
2. **คลิกตีมอนไม่อัปเดตแผงเป้าหมาย** (เจ้าของ): แผงยังค้างเป็น NPC Carle ที่คุยก่อนหน้า ต้องกด Tab ถึงอ่านมอน — เซิร์ฟเดิมคลิกครั้งเดียวแผงขึ้น (game-facts 27 ส.ค.) → B/UI
3. ข้อความ "บาดเจ็บหนักและล้มลง" ยังขึ้นกับมอน (ควรมีเฉพาะผู้เล่น — เจ้าของ 2 ก.ย.) → B
4. เครื่องมือ: sync บนเครื่องเจ้าของแขวน 23:36–00:37 จาก `.git/packed-refs.lock` 0 ไบต์อายุ 11 ชม. (เครื่องดับกลางคัน 13:48) → job 1552/1553 ลบแล้ว · ข้อเสนอถึง ka1-B/chief: `pf_git_sync.ps1` ลบ lock ว่างที่อายุ >60 นาทีเองเมื่อไม่มี git process · computer use: `open_application` กับ `.bin` เด้ง "Open with" — ให้เจ้าของคลิกหน้าต่างเกมแทน

## nonclaims
- ไม่อ้างความหมายฟิลด์ใน 0x51E9 นอกจากที่ diff ได้ (u8 ซ่อน/ปรากฏ · u32 รหัสแถว · สตริง UTF-16 ช่อง X) — RE-091 · ไม่อ้างว่าทำไม 2 คำสั่งไม่ส่ง · ไม่อ้างว่า hook capture พังที่ไหน · ไม่ได้รัน GT-274/276 · ไม่ได้วัดหลอดฟ้าในเซสชันที่ไม่ผ่านทะเล

RESULT: GT-281 PASS R322B 2026-09-07 00:55 (sea login ships basic_faction=1 · /warp 2 mob names pink not green · attack+kill OK · blue bar = boat HP not restored, separate ticket)
RESULT: GT-279 CAPTURED-CLIENT-NEGATIVE-SERVER R322B 2026-09-07 01:17 (EXECUTE button sends 0x51E9 · 3 frames captured · server empty reply · capture hook wrote nothing)
SCOREBOARD: DONE | ผู้เล่นที่ login กลางทะเลเห็นมอนเป็นศัตรูและตีตายได้ (จอ) · ผู้เล่นกด "ปฏิบัติ" ในหน้า GM แล้วเซิร์ฟยังไม่ทำอะไร | 20260907_0123_KA1A-R322B-RESULTS-*
