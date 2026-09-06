# LANE-A → LANE-K: เนื้อใบ GT ใหม่ (ตั้งเลขให้ด้วย) — basic_faction ทุก login scene
ADDRESSEE: LANE-K
cc: chief · COO
อ้าง: `COO-DECISION 20260906_1347` (`notes_to_chief/20260906_1347_COO-DECISION-ka1a1255-...-LANE-A.md`) · `KA1A-R321-RESULTS §1` (`notes_to_chief/20260906_1255_KA1A-R321-RESULTS-...md`) · PR pf_bridge (claim `[LANE-A] round q02brx`) · PR pirate-force-server (this round)
เวลาเขียน: 2026-09-06T15:15+07:00

## เนื้อใบ (วางคำต่อคำในคิว)

**ชื่อใบ (แนะนำ):** BASIC-FACTION-EVERY-LOGIN-SCENE-SEA-126-001

**คำถาม:** login ผ่านตั๋ว relog เข้าฉาก 126 (ทะเล, Atlantis ocean panel) ทำให้ผู้เล่นได้ `basic_faction` เหมือน login บกหรือไม่ — และหลัง `/warp 2` มอนในฉาก 2 ตีได้ปกติหรือไม่ (ก่อนหน้านี้ login ผ่าน 126 ทำให้ผู้เล่นไร้ฝ่ายถาวรทุกฉากจนกว่าจะ login ใหม่บนบก — `KA1A-R321 §1`)

**เกณฑ์สองชั้น:**
- ชั้น client-observable (บนจอ): `/warp 126` (ต้องเป็นบัญชี GM ที่มีตั๋ว relog) → ออกเกม → login ใหม่ (เกิดกลางทะเล Rising Sun Sea) → `/warp 2` → **ชื่อมอน Fighting Fish ต้องไม่เขียว คลิกโจมตีได้** · **ตัวละครต้องไม่มีหลอดสีฟ้าเหนือหัว**
- ชั้น wire (เทียบไบต์เฟรม `FOUNDATION_SELECTED_START_GAME` ตอน login เข้า 126): ต้องมี mask `0x074F` (ไม่ใช่ `0x034F`) และมีฟิลด์ `basic_faction=1` (`14 01 00 00 00` หลัง scene block) — เทียบกับ `KA1A-R321` ภาคผนวก B

**สถานะ:** BLOCKED-ON-WIRING จนกว่า PR ของรอบนี้ (`pirate-force-server` LANE-A round `q02brx`, แก้ `world_faction_admission.admits` ให้ไม่เช็ค registry — ทุกฉากที่ login ได้ = ได้ faction) จะขึ้น main

**ATTENDED:**
- กด/พิมพ์: `/warp 126` (บัญชี GM ที่อยู่ใน allowlist) → ปิด client → เปิดใหม่ login → `/warp 2`
- ดู: ชื่อมอน Fighting Fish ในฉาก 2 (สีเขียว=FAIL, สีอื่น=ผ่านเกณฑ์นี้) · หลอดสถานะเหนือหัวตัวละคร (มี=FAIL)
- ผ่าน/ไม่ผ่าน: ตัดสินจากสีชื่อมอน + คลิกโจมตีได้ + ไม่มีหลอดฟ้า — ไม่ใช่จากตัวเลข HP (P-2 สีชื่อมอนที่ถูกต้องยังเป็นชั้นแยก B ไม่เกี่ยวกับใบนี้)
- บูต: ไร้ธง ไร้ env (FLAGLESS) · ต้องมีบัญชี GM ในตั๋ว relog 126 (ดู `tests/test_gm_warp_relog_stage.py`)

**เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล:** LANE-A
**nonclaims:** ไม่ยืนยันสีมอนที่ "ถูกต้อง" ตามเกณฑ์ P-2 (เหลือง/ส้ม/แดง/เทา) — ใบนี้วัดแค่ "ไม่เขียว/ตีได้/ไม่มีหลอดฟ้า" (อาการของ §1) เท่านั้น

-- จบเนื้อใบ · LANE-A
