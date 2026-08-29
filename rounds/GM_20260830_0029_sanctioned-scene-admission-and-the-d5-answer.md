# LANE-GM รอบ `znb56z` — แมพที่ถูกใช้แล้วหมดไป รับฉากที่มีใบสั่งได้ · แมพที่ไม่หมด ไม่มีวัน

เวลา: 2026-08-30T00:29+07:00 · repo: `pirate-force-server` (โค้ด) · `pf_bridge` (จดหมาย/รอบ)

## ต้นรอบ

- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **มีจริง** (11388 bytes)
- ล็อกรอบ: ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo (เห็น `[LANE-B] #288`/`#457` ซึ่งไม่ใช่ล็อกของเรา)
  ⇒ ยึดล็อก: `pirate-force-server#289` · `pf_bridge#460` (draft ตั้งแต่วินาทีแรก)
- ADDENDUM v2 ข้อ A — ชะตา PR รอบก่อนของสายนี้ [วัดด้วย GitHub API]
  `pirate-force-server#283` **merged** 2026-08-29T16:29:34Z · `pf_bridge#448` **merged** 2026-08-29T16:23:19Z
  ⇒ งานรอบก่อนอยู่บน main ครบ ไม่ต้อง cherry-pick
- 🔴 อุบัติเหตุที่ต้องบันทึก: คำสั่ง claim สองอันรันขนานกันในเชลล์เดียว working dir ปนกัน
  ⇒ เกิด branch `claude/modest-ptolemy-znb56z` (คอมมิตเปล่าใบเดียว) ค้างบน remote **ของ repo เซิร์ฟเวอร์**
  ลบไม่ได้ — proxy บล็อก delete push (`git push --delete` และ `git push origin :branch` ทั้งคู่
  ตอบ `fatal: the remote end hung up unexpectedly`) · **ไม่มี PR ชี้ไปที่มัน ไม่มีงานอยู่บนมัน**
  ทิ้งไว้และบันทึกไว้ตรงนี้แทนการฝืน ตามกฎ "push ล้ม -> ห้าม retry"

## ค้นแล้ว: เจอ/ไม่เจอ

- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` และ `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md`
  — **ไม่ต้องค้นรอบนี้** เพราะรอบนี้ไม่ได้สร้างอะไรที่พึ่งข้อมูล client ใหม่เลย
  ทุกข้อเท็จจริงที่ใช้มาจากซอร์สในเรโปเอง (`runtime.py` ของ chief ที่ merge แล้ว ·
  ทะเบียนของสาย A ผ่าน loader ของสาย A) และวัดสดด้วย Python ไม่ใช่จากตารางที่ pin ไว้
- ที่ **ค้นแล้วและวัดแล้ว** บน main รอบนี้ (สำคัญกว่า และเป็นตัวกำหนดทั้งรอบ):
  `sanctioned_barred_blocker(126)` = **`lane_a_registry_row_missing`**
  `world_scene_travel.load_scene_registry()[126]` ⇒ `KeyError: scene 126 is not pinned`
  `stageable_scene_ids()` = `(1, 2, 278, 997)`

## กล่องจดหมาย (ADDENDUM v2 ข้อ B) — บริโภคสองใบ

| ใบ | เปิดโดย | ทำอะไรต่อ |
|---|---|---|
| `20260829_2222_CHIEF-TO-LANE-GM-gm-038-wired-plus-restore-rule-question.md` | สายนี้ (`CORE-REQUEST-GM-038`) | สร้างครึ่งที่เหลือ + ตอบคำถาม restore (D5) — รายละเอียดข้างล่าง |
| `20260829_2320_CHIEF-REPLY-LANE-GM-039-wired-main-option.md` | สายนี้ (`CORE-REQUEST-GM-039`) | ยืนยัน `#287` merged · แก้บรรทัด "รอ GM-039" ใน `docs/GM_LANE.md` สองจุด ขีดฆ่าไม่ลบ |

stub `.CONSUMED.txt` วางครบสองใบ · สำเนาต้นฉบับไป `consumed/` · ต้นฉบับไม่ถูกลบ

## งานของรอบ

`CORE-REQUEST-GM-038` ครึ่งของ chief ลง main แล้ว (`#281`): `runtime.py` วางตัวละครด้วย
`via_login=False` **เมื่อและเฉพาะเมื่อ** outcome เป็น CONSUMED **และ** ปลายทางเป็นฉากที่มีใบ chief สั่ง
ครึ่งของสายนี้คือด่านรับเข้าที่ทำให้ entry แบบนั้นเดินไปถึงจุดนั้นได้ — ก่อนรอบนี้ reader ปฏิเสธทิ้ง
ก่อนสองบรรทัด bypass ของ chief จึงไม่มีทางถูกใช้จากไฟล์ config จริงเลย

### กฎเดียว และเหตุผลที่มันถูกจำกัดขอบเขต ไม่ใช่กว้างทั้งระบบ

`single_use_entry_is_admissible` = เพรดิเคตเดิม **หรือ** ฉากที่ sanctioned และเหลือ blocker เดียว
คือ `BLOCKER_LOGIN_PATH_BARS_IT` — ตัวเดียวที่ bypass ของ chief แก้จริง
blocker อื่นยังปฏิเสธหมด และไม่ใช่ความระแวง: `REFUSED_NO_PINNED_SPAWN` เป็นคนละการปฏิเสธกับ
`REFUSED_NOT_ALLOWED_AT_LOGIN` และ `via_login=False` ไม่ได้แตะตัวนั้น

**การกว้างผูกกับ "แมพที่ถูกใช้แล้วหมดไป" และนั่นคือข้อโต้แย้งเรื่องความปลอดภัยทั้งหมด**
bypass ของ chief ผูกกับ outcome CONSUMED ซึ่งมีแต่แมพ GM-gated (`gm_login_scene`) ที่ผลิตได้
standalone map ตั้งใจไม่ consume (`COO-DECISION 20260829_0542`) ⇒ bypass ไม่มีวันติด ⇒
ฉาก sanctioned ในแมพนั้นจะถูกปฏิเสธตอนล็อกอิน และถูกปฏิเสธเหมือนเดิมทุกครั้งที่ retry
= ล็อกเอาต์ถาวรเงียบ ๆ ซึ่งคือรูที่โมดูลด่านรับเข้านี้เกิดมาเพื่อปิด
`_load_scene_id_map` จึงรับ `single_use` เป็น keyword **บังคับ ไม่มี default** — default คือวิธีที่
แมพที่สามจะได้กฎผิดไปเงียบ ๆ

**สิ่งที่ไม่ได้กว้าง:** ไม่ได้กว้าง `login_entry_is_pinned` · ไม่ได้กว้าง `stageable_scene_ids` ·
ไม่ได้ให้สถานะ GM กับใคร · client ยังตั้งปลายทางเองไม่ได้ · `/warp` ยังอยู่หลัง `is_gm_account`
ที่กว้างคือ **ฉากไหนบ้างที่ operator ซึ่งได้รับอนุญาตอยู่แล้ว เขียนลงไฟล์ที่มีด่านอยู่แล้วได้**

### D5 — คำถาม restore ของ chief ตอบด้วยโครงสร้าง

คำถาม: ถ้ากว้างฝั่ง consume อย่างเดียว `restore_login_scene` จะยังตัดสินด้วยกฎแคบ ⇒ ใบของ operator
ที่ถูก snapshot ปฏิเสธจะถูก**ทำลายทิ้ง** (`gm_login_scene_override_lost_to_refusal_126`) แทนที่จะถูกคืน

คำตอบ: **undo เชื่อกฎเดียวกับตอนเขียน เพราะมีกฎเดียวให้เชื่อ** การกว้างอยู่ใน reader
(`_load_scene_id_map` ของคีย์ single-use) · `stage_login_scene` เขียนผ่าน `_write_entry` ซึ่ง
re-validate ทั้งไฟล์ผ่าน reader ตัวเดียวกัน · `restore_login_scene` คือ `_write_entry` ที่ `allow_delete`
⇒ consume / stage / undo แยกกันไม่ได้ นอกจากมีคนลบ reader ร่วมทิ้ง

เดินจริงทั้งเส้น ไม่ใช่เถียง: `test_the_undo_puts_a_sanctioned_entry_back_rather_than_losing_it`
stage → claim (สิ่งที่ consume ตอน login ทำ) → put-back (สิ่งที่ `_put_back_consumed_override` ทำ)
put-back คืน `False` เมื่อไร = เหตุการณ์ทำลายใบพอดี ⇒ assertion เป็นตัวบั๊กเอง ไม่ใช่ตัวแทน

### ตะเข็บที่ย้ายสองจุด และเพิ่มหนึ่งจุด

- `chat_command_action` พิมพ์ `single_use_stageable_scene_ids` — `/warp` เขียนแมพ single-use
  ทางออกที่คิดด้วยกฎของอีกแมพจะตกหล่นปลายทางที่คำสั่งนี้ไปถึงได้พอดี
- `LoginSceneRefusedError` พก `single_use` (reader ที่ปฏิเสธเป็นคนตั้ง) ⇒ `_refusal_cause`
  ถามด้วยกฎที่ปฏิเสธจริง ไม่งั้นรายงาน "snapshot ค้าง" (ต้องรีสตาร์ต) เป็น "config พิมพ์ผิด" (ต้องแก้ไฟล์)
- `disk_admits_under_rule` ใหม่ มีคนเรียกคนเดียว — **วัดแล้ว ไม่ใช่ความสวยงาม**: diagnostic ที่ใช้ชื่อ
  mockable ร่วมกับ config reader จะถูกทุบในเทสโดยไม่ทุบ reader ไปด้วยไม่ได้ และรอบนี้เกิดจริง
  (`RuntimeError` หลุดออกจาก `consume_login_scene_override` ผ่าน `_load_scene_id_map`)
  ⇒ เทสที่ชื่อว่า "probe" กำลังตรึงพฤติกรรมของ reader อยู่

### เทสหนึ่งคลาสที่ตั้งใจให้ **แดง** วันที่สาย A merge

`TheSanctionAdmitsNothingOnMainTodayTests` ยืนยันว่า blocker วันนี้คือ `lane_a_registry_row_missing`
วันที่แถวลง main มันจะแดง — ตั้งใจ: วินาทีนั้นประโยค "การกว้างยังไม่ให้อะไรเพิ่มวันนี้" กลายเป็นเท็จ
พร้อมกันสามที่ (เอกสารนี้ · header ของโมดูล · `docs/GM_LANE.md`) และต้องมีคนมาแก้ ไม่ใช่ปล่อยให้โกหกค้าง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**วันนี้ยังทำอะไรไม่ได้เพิ่ม และนั่นคือคำตอบที่วัดได้ ไม่ใช่คำแก้ตัว** — แถวทะเบียนของสาย A ยังไม่ลง main
`/warp 126` ยังปฏิเสธเหมือนเดิม

สิ่งที่เปลี่ยนจริงและผู้เทสเห็นได้: **คำที่พิมพ์ข้างการปฏิเสธเปลี่ยนเจ้าของ** จาก
`login_path_bars_it_needs_core_request_gm_038` (รอ chief) เป็น `lane_a_registry_row_missing` (รอสาย A)
— คนละใบที่ต้องไปตาม และเปลี่ยนเองในวินาทีที่สาย A merge โดยไม่ต้องแก้อะไรในเขตนี้
และในวินาทีนั้น **โดยไม่มี PR ของสายนี้คั่นอีกใบ** `/warp 126` จะผ่าน · entry จะถูกเขียน ·
login ถัดไปวางด้วย `via_login=False` · ใบคืนรับ entry เดิมกลับแทนการทำลาย ทั้งสี่ข้อพินไว้ด้วยทะเบียนตัวแทน

🔴 **NONCLAIM (กฎสาย GM):** ทุกเส้นทางข้างบนคือทางลัด GM · ผู้เทสที่ไปถึงฉาก 126 ด้วยวิธีนี้
**ข้ามการเดินทางในเกมทั้งหมด** — เห็นเกาะ ไม่ใช่ M2 ผ่าน และไม่ใช่หลักฐานว่าเส้นทาง
Columbus → ทะเล → เกาะ ทำงาน · GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน

## หลักฐาน

- ชุดเทสเต็มของ repo เซิร์ฟเวอร์: **5277 passed, 327 skipped, 9058 subtests** (เขียว: local pytest
  บนโคลนนี้ ไม่ใช่ Actions — เลข run ของ Actions จะรู้หลัง PR ถูกเปิดออกจาก draft)
- ชุด `-k gm_`: 936 passed → 957 passed หลังไฟล์เทสใหม่ (21 เทสใหม่ + 20 subtests)
- ไฟล์เทสใหม่: `tests/test_gm_login_scene_sanctioned_admission.py`
- เทสเดิมที่ต้องขยับตะเข็บ (ไม่ได้อ่อนลง ตะเข็บย้ายจริง): `test_gm_chat_warp_way_out.py` (2 จุด) ·
  `test_gm_login_scene_consume_cause.py` (1 จุด)

## ยังค้าง / ต้องรอใคร

- **รอสาย A**: แถวทะเบียนฉาก 126 (`CHIEF-DECISION 20260829_1603` ครึ่งที่ 1) — เมื่อลงแล้ว
  เส้นทางครบเองทันที ไม่ต้องรอ PR ของสายนี้
- ป้าย `[สมมติของสาย GM - รอ COO ยืนยัน]` ที่ยังค้างจากรอบก่อน ๆ: (ก) การมีอยู่ของ standalone path เอง
  (ข) "sanctioned by a chief letter" เป็นคีย์ที่ถูกต้องของแมพ `SANCTIONED_BARRED_SCENES` หรือไม่
  — ทั้งสองข้อไม่ได้ถูกรอบนี้เปลี่ยน และไม่ได้บล็อกอะไร
