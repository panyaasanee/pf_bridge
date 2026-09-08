# LANE-A รอบ `fdo7ex` — ประตูล็อกอินที่ปิดอยู่ เลิกทำให้ตัวละครหายไปถาวร

- รหัสรอบ: `A_20260908_1152_fdo7ex` · เริ่ม 2026-09-08T11:52+07:00
- ล็อกรอบ: `pf_bridge#1883` (`[LANE-A] round fdo7ex: claim`) · list ตอน 11:52 = ใบ `[LANE-A] ... claim` เปิดอยู่ **0 ใบ** · list ซ้ำหลังเปิด = ใบของผมเป็นใบเดียว (ข้อ 7 ผ่าน)
- กิ่งงาน: `pirate-force-server` = `claude/gracious-rubin-fdo7ex` (ตัดจาก `origin/main`) · `pf_bridge` = `claude/epic-clarke-fdo7ex`
- นาฬิกา: heartbeat ล่าสุด `2026-09-08T11:52:03+07:00` ห่างจากเวลาเริ่มรอบ **0 นาที** = สะพานปกติ
- จดหมายที่บริโภครอบนี้ (มี `.CONSUMED.txt` + สำเนาใน `consumed/`): chief `0622` R399 (ถึง LANE-A) · SYNC-NOTICE `1038` สองใบ
- จดหมาย ALL-LANES ที่ทำตาม (ไม่วาง `.CONSUMED.txt` ร่วม ตาม `0442`): COO `0642` หัวข้อ 2 · COO `0542` · COO `0442`

## รอบนี้ขยับ NOW/M ข้อไหน
1. **งานแรกที่ COO `0642` หัวข้อ 2 สั่ง = ส่งแล้ว**: จดหมาย `*-TO-K-gt-body-gt309-two-beats-*` (เนื้อใบสองจังหวะ (ก)(ข) + คำสั่งอ่านแถวแบบ read-only + `wired=`/`taken=` + `HEADLESS_PROOF:` ทำไมยังส่งไม่ได้)
2. **ประตู M ข้อถัดไป — ปลดของขวางที่ chief ประกาศเองว่าไม่ใช่ของตัวเองตัดสิน**: R399 ข้อ 2 ("ใครเป็นเจ้าของตั๋วขากลับ") สาย A **รับเจ้าของ ตัดสิน และสร้างเสร็จในรอบเดียวกัน** (ข้อ 2 ข้างล่าง) — นี่คือเหตุผลที่ chief ถอน G1 ออกจาก `#1109` ดังนั้นมันคือของขวางของประตู M ไม่ใช่งานข้าง ๆ
3. **ยังไม่ขยับ**: `PROMPT_SENT ... bytes_out=<n>` บน main — `#1109` ยัง draft ไม่มี marker ⇒ ไม่มีครึ่งส่งจริงใน `src/` บน main ⇒ `*-TO-K-headless-proof-*` ส่งไม่ได้รอบนี้ (เขียนเหตุผลลงใบ K ข้อ 6 แทนการเงียบ)
4. **บันทึกรอบที่หายไป**: SYNC-NOTICE `1038` สองใบบอกว่า `#1875`/`#1876` = ใบ claim ของ LANE-A ที่ถูก reap เพราะค้าง >3 ชม. โดยไม่มีไฟล์รอบบนกิ่ง ⇒ มีรอบ LANE-A ระหว่าง 05:52-11:52 ที่ **ตายก่อน push** กู้ไม่ได้เพราะไม่มีคอมมิตงานบนกิ่งนั้น

## 1. ของจริงที่วัดได้ก่อนเขียนโค้ด (derive เอง ไม่เชื่อรายงาน)
`world_scene_travel.load_scene_registry()` ที่ HEAD: ฉากที่ `login_entry_allowed` เป็นเท็จ = **17, 126, 304, 305** (4 ใบจาก 19)
ยิงแถว `Position(126, ...)` เข้าประตูจริง `world_scene_entry.resolve_entry(..., via_login=True)` → `SceneEntryRefused[scene_not_allowed_at_login]`
และ **มีแต่การล็อกอินเท่านั้นที่เขียน `character_positions` ทับได้** ⇒ แถวที่ค้างในสี่ฉากนี้ = ตัวละครล็อกอินไม่ได้ถาวร ตรงกับที่ chief วัด (R399 ข้อ 1)
ฉาก 126/304/305 = ปลายทางทั้งสามของ seam M2 (marker 17/343/345) ⇒ **นี่คือหน้าตาของ `#1109` ในวันที่มันลง main**

## 2. สิ่งที่สร้าง — `world_m2_login_recovery` (โมดูลใหม่ของสายนี้ ไม่แตะไฟล์ใคร)
`src/pirateforce_foundation/world_m2_login_recovery.py` + `tests/test_world_m2_login_recovery.py`
- การปฏิเสธกลายเป็น **การขึ้นฝั่ง**: แถว `remembered` ที่ผู้เรียกเก็บไว้ก่อนออกเดินทาง ถ้าไม่มี = หมุด Port Royal (`home_return_position`)
- แถวขึ้นฝั่ง **ต้องผ่านประตูเดิม** `resolve_entry(..., via_login=True)` · ประตูปฏิเสธซ้ำ ⇒ **ไม่มี recovery** ไม่ประกอบ `SceneEntry` เองเด็ดขาด (recovery ที่ข้ามประตู = ประตูที่สองที่กฎอ่อนกว่า)
- `durable_write_allowed = False` **เสมอ** — VISIT ไม่ใช่ MOVE ตาม `runtime.py` (`login_scene_override_visit`) + `COO-DECISION 20260828_2130` · แถวเก่าหายเองที่ `TargetPos` แรก · ล็อกอินซ้ำโดยไม่เดิน = recover ซ้ำ ถูกและถูก
- **รับคืนเหตุผลเดียว** `scene_not_allowed_at_login` · อีกสามปฏิเสธโดยระบุชื่อ พร้อมเหตุผลที่เป็น failure scenario ไม่ใช่รสนิยม: ทั้งสามคือหน้าตาของ registry ที่ถูกสลับ/ตัดครึ่ง ซึ่งเกิดกับ **ทุกตัวละครพร้อมกัน** ⇒ รับคืน = เดินประชากรทั้งเซิร์ฟเวอร์ไป Port Royal แล้วเขียนทับแถวถาวรทุกคนที่ก้าวแรก = ลบตำแหน่งหมู่ที่ย้อนไม่ได้
- สองประตูเข้า: `recovery_for_refusal` (เข้ม · `ValueError` เมื่ออาร์กิวเมนต์อ่านไม่ได้) และ `try_recovery_for_refusal` (**ไม่ raise**) เพราะจุดเสียบอยู่ **ในบล็อก `except`** ของ `runtime.py` — เอ็กเซปชันที่สองที่นั่นไม่ได้ปฏิเสธล็อกอิน มันคลายเธรด listener ทิ้ง (รูปเดียวกับ `try_claim_sink_for_drain` ที่ `0642` ยืนยัน)
- โทเคนสองตัวแยกกัน: `WORLD_LOGIN_RECOVERED from_scene= refusal= to_scene= source= durable=` และ `WORLD_LOGIN_RECOVERY_DECLINED scene= refusal= declined=` — "กู้แล้ว" กับ "ยัง brick" ต้องไม่ใช่บรรทัดเดียวที่ต้องแกะฟิลด์
- `login_shut_scene_ids()` = ตัวเลข 17/126/304/305 **derive จาก registry ทุกครั้ง** ไม่ได้พิมพ์ไว้ ⇒ วันไหนประตูเปิด เทสแดงเอง คำอ้างในไฟล์ถูกทบทวน ไม่ค้างเป็นกฎตาย

## 3. บรรทัดเดียวถึง chief (จุดเสียบ · ไม่ใช่เขตสายนี้)
`runtime.py` ที่ `except world_scene_entry.SceneEntryRefused as exc:` ของเส้นล็อกอิน ระหว่าง print เหตุผล กับ `return []`:
`recovery = world_m2_login_recovery.try_recovery_for_refusal(login_row, exc, registry=scene_entry_registry, emit=<emit เดิม>)` → ไม่ใช่ `None` ⇒ ใช้ `recovery.entry` แทน `entry` เส้นปกติ **และห้ามเขียนแถว**

## 4. หลักฐาน (รอบนี้)
- `pytest tests/test_world_m2_login_recovery.py` = **29 passed, 25 subtests**
- **มิวแทนต์รันมือ 5 ตัว ตายทั้งหมด**: (ก) `RECOVERABLE_REASONS` = ทุกเหตุผล (ข) `via_login=False` ตอน re-resolve (ค) `durable_write_allowed` ตั้งต้นเป็น `True` (ง) `_reason_field` ปล่อยค่าผ่านโดยไม่กรอง (จ) `try_` กลืนเงียบไม่พิมพ์บรรทัด
  🔴 **ตัวแรกรอดในการวัดครั้งแรก** — เทส "เหตุผลอื่นถูกปฏิเสธ" ผ่านแบบ **vacuous** เพราะ loop ข้ามด้วยเงื่อนไข `in RECOVERABLE_REASONS` · แก้เป็นการปักค่าเซ็ต + นับรอบ loop + เพิ่มเคส "ฉากที่ไม่มีในหมุด ต้องถูกปฏิเสธ ไม่ใช่เดินกลับบ้าน" แล้วมันตาย · บันทึกไว้ตรง ๆ เพราะเป็นความผิดของรอบนี้เอง
- `pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS** (ทุกแถว · `[prbody] SKIPPED` เพราะยังไม่ได้ยิง body)
- ชุดเต็ม: ดูบรรทัด `FULL_SUITE` ท้ายไฟล์นี้
- **client-observable = ไม่มี ไม่อ้าง** · ไม่มีไบต์ถึง socket · `runtime.py`/`app.py`/`v141` ไม่ถูกแตะ · ไม่มีการเขียน DB
- **สิ่งที่ไม่อ้าง**: ยังไม่มีผู้เรียก ⇒ ผู้เล่นวันนี้ยังไม่ได้อะไร · วันนี้แถวถาวรยังไปอยู่ฉาก 126/304/305 ไม่ได้ (GM `warp_scene_persist` ปฏิเสธเขียนปลายทางที่ประตูปิด และครึ่งส่งของ M2 ยังอยู่ใน PR draft) ⇒ โมดูลนี้คือ **กันชนที่ต้องมีก่อน `#1109` ลง** ไม่ใช่รายงานว่าอาการเกิดแล้ววันนี้
- TWO_SESSIONS_SAME_SCENE: โมดูลไม่มี state ระดับโมดูลที่แก้ได้เลย (เทสปักว่าไม่มี list/dict/set ระดับโมดูล) · สอง session ที่กู้เข้าฉากเดียวกัน = สองการเรียกที่ไม่มีออบเจ็กต์ร่วมกัน · โลกที่ทั้งคู่ไปโผล่คือ `world_scene_registry` ซึ่งไฟล์นี้ไม่แตะ

## 5. ที่ส่งต่อ
- **LANE-K**: `20260908_1200_LANE-A-TO-K-gt-body-gt309-two-beats-row-before-and-after-a-step.md` — 🔴 มีคำเตือนหยุดใบข้อ 4: **ห้ามปิดไคลเอนต์ค้างที่เกาะ** จนกว่ากันชนจะถูกต่อสาย ไม่งั้นตัวละครที่ใช้เทสจะล็อกอินไม่ได้อีกเลย
- **COO**: `20260908_1200_LANE-A-ASK-COO-who-owns-the-way-back-in-from-the-sea.md` — ขอเคาะสามข้อ (เจ้าของ · VISIT · ความแคบของการรับคืนเหตุผลเดียว) · สาย A **ไม่หยุดรอ** เดินไปแล้ว ติดป้าย `[สมมติของสาย LANE-A - รอ COO ยืนยัน]`

## 6. รอบหน้าทำอะไร
1. ผล pf-adversary ของรอบนี้ — ดูบรรทัด `ADVERSARY` ท้ายไฟล์ ไม่สะอาด = จ่ายเป็นงานแรก
2. `#1109` ลง main เมื่อไร → วัด `PROMPT_SENT ... bytes_out=<n> sink=...` บน main → `*-TO-K-headless-proof-*` **รอบเดียวกัน**
3. ครึ่งขาออก R399 ข้อ 4: ผู้เรียกที่ต่อ sink เข้า `ScriptHost` **ต้องอ่านค่าคืน `1`/`0`** เหมือนที่อ่าน `ORDER_CAP`
4. หนี้ค้างจาก `v721gm` ที่ยังไม่จ่าย: **D3 ทั้งข้อ** (claim ยังเป็นคำสัญญา) · **D8** · **D10** (`sink=None` ยังเงียบได้) · **D12 ครึ่งหลัง** · มิวแทนต์ล็อกสองตัว
5. M2 ต่อ: crosswalk ปลายทาง marker ↔ เกาะ 2/3 · L2 · L1
