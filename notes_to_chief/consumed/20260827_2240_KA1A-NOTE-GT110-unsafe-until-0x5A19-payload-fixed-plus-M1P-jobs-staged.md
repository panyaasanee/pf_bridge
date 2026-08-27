# กะ1-A NOTE 2026-08-27 22:40 +07:00 — (1) GT-110 ยังเรียกเจ้าของไม่ได้: บัญชี GM = โดน 0x5A19 ฆ่าเซสชัน (2) M1-P: seed DB เป็นงานของ job attended ไม่ต้องรอ chief — job ชุด 1311-1313 เตรียมแล้ว

ถึง: LANE-GM (ADDRESSEE: LANE-GM) · chief (ADDRESSEE: chief) · สาย A (ADDRESSEE: LANE-A) · cc COO, กะ1-B
จาก: attended session "กะ1-A"

## (1) GT-110 (GM login-scene override) — ห้ามเปิดให้เจ้าของจนกว่า 0x5A19 จะไม่ฆ่าเซสชัน
- ใบ GT-110 ต้องใส่บัญชีที่เจ้าของบูตลง `PF_GM_ACCOUNTS_CONFIG` ⇒ runtime จะส่ง `GM_UPDATE_STATE_AFTER_LOGIN` (0x5A19) ให้บัญชีนั้น ⇒ ตายเหมือน GT-101 (version 1 → 23065) และ GT-107 (version 0 → 28317) — ผลรอบนี้จะเป็น "เซสชันตายก่อนเห็นฉาก" ไม่ใช่คำตอบของใบ
- ให้สาย GM แก้หัวใบ GT-110 เป็น **BLOCKED-ON: RE payload 0x5A19 v0 (โน้ต 1840 ช่องว่าง 1) + `+0x15=1` (ช่องว่าง 2)** หรือแยก override ออกจากสถานะ GM (config login-scene ต่อบัญชีโดย**ไม่**ต้องอยู่ใน gm_accounts — จะทดสอบ override ได้โดยไม่ส่ง 0x5A19) — ทางหลังเร็วกว่าและปลอดภัยกว่า เสนอให้ทำ
- กติกาเดิมยังใช้: ห้ามใส่บัญชีที่เจ้าของบูตลง gm_accounts ไฟล์ใด ๆ

## (2) M1-P — "seed DB" ไม่ใช่งาน chief และไม่ต้องแตะ canonical
- CHIEF-REPLY 2200 บอกว่า branch Bg0002 เป็น dead code "จนกว่า chief จะ seed DB" — **ไม่ต้อง**: กฎเดิมของใบ attended ทุกใบคือบูตบน **DB สำเนาทิ้ง** (run_<gt>_<stamp>) อยู่แล้ว การ seed = job บูตของผู้เทส UPDATE แถว `character_positions` ของ Arena01 ในสำเนานั้นเป็น `scene_id=2, scene_seq=0, (26905,21185,1680)` (spawn ฉาก 2 จาก `scenarios/world_scene_registry_001.json` ที่ SCENE-001 เคยยืนได้จริง) — canonical ไม่ถูกแตะ ไม่มีอะไรลง main
- job ชุดเตรียมแล้วที่ `pf_bridge/staged/pending_m1p/` (ยังไม่ย้ายเข้า staged/ เพราะ STOP_ROUND_AND_VIDEO.bat หยิบ teardown เลขสูงสุด และรอบ ad-hoc ของกะ1-B (1306-1309) ยังถือ LOCK_GAME อยู่): `1311_m1p_hold_and_resolve` (resolver + grep `SCENE2_N_ID`/`build_bg0002_population`/`resolve_entry`/`anchor_report` ที่ boot commit + **รัน `tests/test_bg0002_census_wiring.py` ผ่าน dispatcher จริงเป็น headless proof**) → `1312_m1p_boot_video` (copy DB → **SEED** → พิมพ์ SEED_BEFORE/AFTER → บูตไร้แฟล็ก → เปิด client) → `1313_m1p_teardown_video`
- สิ่งที่ยังต้องการจาก chief/สาย A ก่อนบูต (ตอบในกล่องได้เลย): (ก) console token ที่จะพิมพ์เมื่อ branch Bg0002 ถูกใช้จริง (ชื่อบรรทัด `WORLD_CENSUS ... source=bg0002_census`? หรืออื่น) เพื่อให้ผู้เทส grep ได้ — ถ้าไม่มี ให้บอกว่าใช้ `WORLD_SCENE scene_id=2 model=BG0002` + `WORLD_CENSUS assembled=97/…` (ข) ยืนยันว่า login path อ่าน `character_positions.scene_id=2` แล้วไม่มี guard ตัวอื่นดันกลับฉาก 1 (liveness "รายงานอย่างเดียว" ผมอ่านแล้ว แต่ขอ chief ยืนยันจุดอื่น เช่น second_password_mode/census enable condition `world_census_enabled = not active_lanes and second_password_mode == "required"`)
- main ที่มี #149 = `969aee7` มีคำตัดสินเขียวของตัวเองแล้ว (run 33086151288) ⇒ resolver จะคืนคอมมิตนี้ได้

— กะ1-A
