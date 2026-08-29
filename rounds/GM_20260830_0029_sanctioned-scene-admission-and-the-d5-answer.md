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

บรรทัดที่ operator เห็นจริงวันนี้ เดินผ่าน dispatcher จริง (`/warp 126`, บัญชีใน `gm_accounts`):

```
GM_CHAT_WARP_REFUSED account='GM_ONE' scene_id=126 reason=scene_sanctioned_but_route_incomplete
  stageable=(1, 2, 278, 997) blocker=lane_a_registry_row_missing
  sanction='CHIEF-DECISION 20260829_1603 item 2'
```

`blocker=` คือคำที่เปลี่ยนเจ้าของรอบนี้ — ก่อนรอบนี้เป็น `login_path_bars_it_needs_core_request_gm_038`
(รอ chief) ตอนนี้เป็น `lane_a_registry_row_missing` (รอสาย A) · `stageable=` ยังสี่ตัวเท่าเดิม
เพราะการกว้างยังไม่ให้อะไรเพิ่มจนกว่าแถวของสาย A จะลง


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

## pf-adversary — รอบนี้หักอะไรได้ และเปลี่ยนอะไร

ข้อโต้แย้งเรื่อง**ความปลอดภัย**ยืนได้: pf-adversary เดิน `runtime.py` เองไม่ได้เชื่อสรุปของสายนี้
แล้วพยายามหักสิบสองทาง **ล้มทั้งสิบสอง** (standalone map · แถวที่ตัวละครเก็บไว้เอง · การแข่งกันของสองแมพ ·
ลำดับใน `get_login_scene_override` · probe กับ real call ไม่ตรงกัน · restore เขียนผิดแมพ ·
บัญชีที่ไม่ใช่ GM · client ตั้งปลายทางเอง · `_refusal_cause` เปลี่ยน dispatch ·
`lane_a_row_on_disk` ปิดบังการปฏิเสธจริง · เลขบรรทัดที่อ้าง · โทเคน greppable)

🔴 แต่ **หลักฐาน**พัง: มิวแทนต์หกตัวของโค้ดใหม่รอบนี้เอง รอดทั้งชุด (957 passed)
สายนี้วัดเองได้สี่ตัวก่อน (M5 M6 M8 และ M14 หลังรายงานมาถึง) และ pf-adversary เจอเพิ่ม

| มิวแทนต์ | เดิม | หลังแก้ |
|---|---|---|
| M5 ลบตัวกรอง `is_known_scene_id` ใน way out | 957 passed | **1 failed** |
| M6 probe ใช้กฎแคบเสมอ | 957 passed | **2 failed** |
| M7 probe ใช้กฎกว้างเสมอ | 957 passed | **1 failed** |
| M8 `_refusal_cause` ตรึง `single_use=False` | 957 passed | **1 failed** |
| M14 way out ของ reader แคบเสมอ | 957 passed | **1 failed** |
| M16 สลับลำดับสองแขนของเพรดิเคต | 957 passed | **ไม่เพิ่มเทส ตั้งใจ** — ดู D4 |

🔴 **M5 คือมิวแทนต์เดียวกับที่บันทึกในไฟล์นั้นเองบอกว่าเคยหลุดขึ้น commit ที่ push แล้วครั้งหนึ่ง**
ฟังก์ชันใหม่ก๊อปตัวกรองมาและก๊อปคำอ้างอิงมา แต่ไม่ได้ก๊อปเทสมาด้วย

### สี่ข้อที่ไม่ใช่มิวแทนต์

- **D4** docstring อ้างเหตุผลที่ไม่มีอยู่จริง ("ลำดับไม่ใช่ความสวยงาม ... เพื่อให้ `TypeError` ออกมา")
  วัดแล้ว: สลับลำดับ ค่าผิดทั้งสี่ก็ยัง raise `TypeError` เหมือนเดิม **ขีดฆ่า**
  และสิ่งที่ load-bearing จริงอยู่คนละที่ — `sanctioned_barred_blocker` ตรวจ spawn **ก่อน** login bar
  ใครไป "ทำให้สอดคล้อง" กับลำดับของ `_target_is_admissible` = เปิดทางรับฉากที่ไม่มี spawn
- **D5** "สองแขนถามด้วย reading เดียวกัน" จริงครึ่งเดียว — เมื่อ caller ส่ง registry มาจริง
  แต่ค่า default `None` แต่ละแขนโหลดทะเบียนเอง (2 reads · way out 3 reads เทียบกับ 1 ของตัวข้าง ๆ)
  ขีดฆ่าครึ่ง พร้อมเหตุผลว่าทำไมเป็นราคา ไม่ใช่รูของความถูกต้อง
- **D6** ไฟล์เทสของรอบนี้ถือทั้งสองครึ่งของข้อขัดแย้งไว้ในเทสสองใบที่ผ่านทั้งคู่ —
  way out (reading เดียว) ตั้งชื่อฉากที่ `stage_login_scene` (สอง readings) ปฏิเสธ
  **ไม่ใช่ของใหม่จากการกว้าง** `stageable_scene_ids` มีทรงเดียวกันมาตลอด
  ตอนนี้ยืนยันไว้ตรง ๆ ที่เดียว พร้อมขอบเขต (ระหว่างสาย A merge กับการรีสตาร์ตครั้งถัดไป)
  และเหตุผลที่ปฏิเสธทางแก้ราคาถูก: way out ถูกสร้างอยู่ใน `raise` ของการปฏิเสธเอง
  การเพิ่ม read ที่ throw ได้ตรงนั้น = สลับ exception ที่ caller ต้องรับ เป็นตัวที่มันไม่รับ
- **D7** raise ที่เพรดิเคตเดิมไม่ทำ — วันนี้เอื้อมไม่ถึง (`spawn` เป็นฟิลด์ของ frozen dataclass)
  จะเอื้อมถึงวันที่มันกลายเป็น property · และทางแก้บรรทัดเดียวที่ชัดที่สุด **ผิด**
  (สลับลำดับ blocker = เปิดทางรับฉากไม่มี spawn) ⇒ **บันทึกเป็นข้อค้าง ไม่แก้ครึ่ง ๆ ใต้แรงกดดันเวลา**
- **D8** skip ตอน import ของโมดูลเทสใหม่ — **แก้ที่ต้นเหตุ ไม่ใช่ pin**
  ความพยายามแรกคือใส่ลง `docs/PYTEST_SKIP_PINS.json` แล้วเกตของเรโปเองปฏิเสธ:
  `test_every_pinned_count_is_a_positive_integer` — ไฟล์นั้นรับเฉพาะ skip ที่**เกิดจริง**
  และใบนี้ยังไม่เกิดวันนี้ ⇒ ถอน pin ออก แล้วเลิก raise ตอน import แทน:
  `the_only_sanctioned_scene()` คืน `None` และทุกคลาสติด `@requires_a_sanctioned_scene`
  วัดผลด้วยแมพว่าง [ใน worktree]: โมดูลนี้ **25 skipped ไม่มี failed**
  และ `test_gm_tests_collect_without_posix` **ไม่อยู่ในรายการที่แดงอีกต่อไป**
  (ที่ยังแดง 14 ใบ อยู่ในไฟล์ของรอบก่อน ๆ ซึ่งเป็นเทสตามหลักการ retirement ที่ตั้งใจให้แดง)
- **D9** แถวตัวแทนใช้จุดมาถึงที่ใบ chief ระบุ `(3050, 232, 90)` แทนของฉากบ้านแล้ว
  และเขียนไว้ตรง ๆ ว่าฟิลด์ไหนยังเป็นของฉากบ้าน และทำไมไม่มีฟิลด์ไหนถูกอ่าน

### 🔴 ข้อบกพร่องเชิงกระบวนการ ที่อันตรายกว่าทุกข้อข้างบน

การไล่มิวแทนต์รอบแรก **รันในเช็คเอาต์จริง** แล้วย้อนด้วย `git checkout -- .` ระหว่างตัว
pf-adversary จับได้กลางคันจาก `git diff` — และตัวที่มันเห็นคือ **M2 พอดี**
คือ standalone map บนกฎกว้าง = การถอยหลังแบบล็อกเอาต์ถาวรที่ทั้งใบนี้มีไว้เพื่อกัน
นั่งอยู่ในทรี ห่างจากการขึ้นเรือแค่ `git commit -a` ครั้งเดียว

**ไม่มีอะไรหลุดจริง** (ทุกมิวแทนต์ย้อนครบ · `git status` สะอาดที่คอมมิต · ตรวจซ้ำแล้ว)
แต่ความเสี่ยงเป็นของจริง และทางแก้ฟรี: การไล่รอบสองรันใน `git worktree add --detach`
**และนั่นคือกฎของสายนี้ตั้งแต่นี้ไป**
