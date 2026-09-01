# R177 (session `mdj01v` / `session_01ScLLRQVDBfM3NXTwEWECqP`) — 2026-08-26 ~15:5x–16:2x (+07:00)

## สรุปหนึ่งบรรทัด
ต่อสาย `CORE-REQUEST-005` (`MOB-COMBAT-001`/`MOB-DEATH-001`) ที่ค้างเลยกำหนด COO มา ~8 ชั่วโมง — `runtime.py`
เรียก `mob_combat`/`mob_death` แบบไม่มีแฟล็กแล้ว ผ่าน `pf-adversary` บังคับก่อน commit สวีตเต็มเขียว(cloud sanity)

## บริบทต้นรอบ
- การ์ดกันรอบซ้อน: ไม่มี PR `[LANE-E]` เปิดค้างทั้งสอง repo (มี `pirate-force-server#61` เป็น `[LANE-A]` — ไม่ใช่ล็อกของฉัน ไม่แตะ) ⇒ จับล็อกด้วย `pf_bridge#118` + `pirate-force-server#63` (draft ทั้งคู่ ยืนยันด้วยการอ่านกลับ)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง · pull --rebase ทั้งสอง repo ผ่าน (ทั้งคู่ตรงกับ `origin/main` อยู่แล้ว)
- กล่องจดหมาย: มี 2 ใบค้างจริง (ใบอื่นทั้งหมดมี `.CONSUMED.txt` แล้ว) — `20260826_1500_ATTENDED-ORG-AUDIT` + `20260826_1543_COO-DECISION-WIRED-metric` — บริโภคทั้งคู่

## 🔴 v6.1 prompt §18 เป็นเนื้อหาเก่า — ไม่ทำตามข้อ 1, ข้อ 2/3/5 ทำไปแล้วก่อนรอบนี้
- **ข้อ 1 (`GT-001` samePos "แก้แล้ว"):** ไม่มีไฟล์ `staged/1166_gt001_teardown_verify_update_canon.ps1` อยู่จริงในทั้งสอง repo (`find` ว่างเปล่า) · `GAME_TEST_QUEUE.md:549` ยืนยัน `GT-001` ยัง **HOLD** ตามที่ `R175` ตรวจแล้วคืนสถานะ (ข้ออ้างเดิมสืบไม่ถึงจดหมายไหนเลย, `pf-adversary` จับได้) และ `R176` ปฏิเสธข้อความเดียวกันนี้ไปแล้วครั้งหนึ่ง ⇒ **ไม่แตะ `GT-001` ซ้ำเป็นรอบที่สาม** เสนอ COO/Panya ตัดข้อ 18.1 ออกจาก prompt จริง ๆ เสียที
- **ข้อ 2 (ABORT/state-file rule):** มีอยู่แล้วใน `AGENTS.md` + `staged/TEMPLATE_teardown_generic.ps1` (เขียนโดย R175) — ไม่ต้องทำซ้ำ
- **ข้อ 3 (พิน 48 + รายชื่อ):** ยืนยันแล้วโดย R175 ว่ามีรายชื่อเรียงอยู่ก่อนแล้ว — ไม่ต้องแก้
- **ข้อ 4 (`GT-033`/`RE-075`):** `GT-033` ปิดเป็น ANSWERED ไปแล้วตั้งแต่ R166 (คนละเส้นทางกับ `RE-075`) · `RE-075` เองก็ปิดไปแล้วโดย R175 (retire `HYP-PF-028` v1) — ข้อนี้อ้างถึงงานที่เสร็จไปแล้วก่อน v6 จะถูกเขียนด้วยซ้ำ
- **ข้อ 5 (heartbeat):** `notes_to_chief/_BRIDGE_HEARTBEAT.txt` ทำงานจริงอยู่แล้ว (พบไฟล์อัปเดตสด `15:46:02 +07:00` ตอนต้นรอบ) — ไม่ต้องแก้
⇒ **ทั้งหัวข้อ 18 ควรถูกลบออกจาก prompt เวอร์ชันถัดไป** ไม่ใช่แค่ข้อ 1 — เป็นการเสนอครั้งที่สองแล้ว (ครั้งแรกจาก R176)

## งานหลักของรอบ: `CORE-REQUEST-005`
`ORG-AUDIT 15:00` วัดว่าเลน production 10 ใบ แต่ `WIRED = 0` (module ของสาย A/B ที่ `runtime.py`/`app.py` import จริง)
— ตรวจสดพบว่า `CORE-REQUEST-003`/`004` ต่อแล้วจริงจาก R176 (`world_scene_entry`, `world_travel_gate` — grep ยืนยัน)
แต่ `MOB-COMBAT-001` (`COO-DECISION 20260826_0402`, กำหนดเดิม ≤ 08:00) ยังไม่ต่อ

1. spawn `pf-builder` (พื้นหลัง) ให้หา hook point เอง — ไม่มี dispatch ของ inbound `ActionVital`/EA7D ใน `runtime.py`
   มาก่อนเลย (มีแต่เลนที่มีแฟล็ก) ⇒ ต้องสร้าง `_dispatch_mob_combat` ใหม่ทั้งเมธอด ตาม `MOB_COMBAT_WIRING`/
   `MOB_DEATH_WIRING` ที่โมดูลสาย B เขียนไว้เอง (`mob_combat.py`/`mob_death.py`)
2. ผล: `runtime.py` (+256/-1), `tests/test_field_mobs.py` (tripwire เปลี่ยนจากลบเป็นบวก — ทำงานตามที่ออกแบบไว้),
   `tests/test_mob_combat_dispatch.py` ใหม่ 8 เทส · สวีตเต็ม `3097 passed, 327 skipped, 4986 subtests, 0 failed`
3. `pf-adversary` บังคับก่อน commit — พบ 2 Low + 1 Informational ทั้งหมด:
   - Low: retry loop ของ `REFUSE_LEDGER_STALE`/`REFUSE_REGISTER_STALE` เป็น `while True` ไม่มีเพดาน (พิสูจน์แล้วว่า
     unreachable วันนี้ แต่เป็นระเบิดเวลาถ้า invariant single-writer พังทีหลัง) → **แก้แล้ว**: ใส่เพดาน
     `MOB_COMBAT_STALE_RETRY_LIMIT = 8` ทั้งสองลูป พร้อม event ชื่อถ้าเกินเพดาน
   - Low: การรวมกับเลนที่มีแฟล็ก (`scene_load_scenario`) อาจกลืนเฟรมก่อนถึงมือ mob_combat — เปิดเผยในคอมเมนต์แล้ว
     ไม่บล็อก
   - Informational: `_apply_mob_death_census_override` โยน `RuntimeError` ที่ไม่ถูกจับเฉพาะจุด — pattern เดิมของไฟล์
     รับความเสี่ยงเท่าบั๊กอื่นในต้นไม้ ไม่ใช่ของใหม่จากรอบนี้
   - รันสวีตซ้ำหลังแก้: `3097 passed` เท่าเดิม (0 regression)
4. commit `pirate-force-server@6105d26` push แล้ว
5. อัปเดต `CORE-REQUEST` registry: 001-005 ต่อแล้วครบ · `WIRED = 7/10` (grep สดยืนยัน: `world_population`
   `world_scene_travel` `world_scene_entry` `world_travel_gate` `field_mobs` `mob_combat` `mob_death`)
6. `SERVER_VERSIONS.md`: เติมสถานะการสร้าง `BUILD-005`/`v4` ชั้นซอร์ส — **ยังไม่ประกาศ `v4`** (กฎสะสม: `v1`/`v2`/`v3`
   ยังไม่มีตัวไหนประกาศเลย)
7. คำถามค้างที่ไม่ตัดสินเอง (เข้าเกณฑ์นโยบาย 5 — multiplayer): ledger/register เป็น per-session ไม่ใช่
   server-wide ⇒ ผู้เล่นสองคนตีมอนสเตอร์เดียวกันเห็น HP คนละค่า — เขียน `CHIEF-ASK-COO 20260826_1600` พร้อม
   คำแนะนำของฉัน (ยอมรับสำหรับ `v4` ผู้เล่นเดียว, เลื่อนแก้ไปพร้อม persistence)
8. คิว: เปิด `GT-084` (blocked-on-merge) ผ่าน `pf-queue-author` — สองชั้นหลักฐานแยกกัน + ท่าบูตจำลอง (ไม่แตะ
   `state\play.sqlite3`) ครบตามฟอร์แมต

## สวีตเต็ม
`3097 passed, 327 skipped, 4986 subtests, 0 failed` — เขียว(cloud sanity) — รันสองครั้ง (ก่อน/หลังใส่ retry cap)

## ค้างสำหรับรอบถัดไป
- `CHIEF-ASK-COO 1600` รอคำตอบ (ไม่บล็อก)
- `RE-082` ยัง "ค้างสำหรับรอบถัดไป" มาสามรอบติด (amend `RE-077` T5 + แก้ span pin `GT-046`) — ไม่ได้แตะรอบนี้
  เพราะความเสี่ยงจากการรีบทำโดยไม่มีเวลาตรวจลึกสูงกว่าประโยชน์ของการรีบ
- เสนอ COO/Panya ตัด v6 prompt §18 ทั้งหัวข้อออก (เนื้อหาทำไปหมดแล้วก่อนรอบนี้ หรือเป็นข้อความเท็จที่ตรวจแล้ว)
- `GT-078` (placement→identity), `session.py` position-injection, `CHIEF_CONTINUATION.md` ใกล้ ~110KB (รอ archive
  รอบถัดไปถ้ายังไม่มีใครทำ)
