# LANE-GM รอบ `dotoho` — 2026-09-03T07:39+07:00

## NOW.md ขยับข้อไหน
🔴 อ่าน `NOW.md` เป็นไฟล์แรกของรอบ (ตรวจล่าสุด 2026-09-03 06:49 โดย COO)

**รอบนี้ขยับ: หัวข้อ "ต่อคิวทันทีหลังสามข้อบน" ข้อ GM-B `/speed`**
บรรทัดที่ขยับคือบรรทัดของ COO เอง: *"รอบทดลองเปิดด้วยเกต runtime `PF_SPEED_TRIAL` เท่านั้น
ไม่เปิดบน `main` (`0646`)"* — เกตนั้นถูกสร้างจริงรอบนี้ ทั้งใบ

**ไม่ขยับ และเหตุผล**
- **P-0** ปิดแล้ว (COO วัดเอง 02:45) ไม่มีอะไรให้สายนี้ทำ
- **P-1** เจ้าของ = สาย E (ตัวเดิน multi-vital) และ สาย B — ไม่ใช่เขตของ LANE-GM ห้ามแตะ
- **P-2** สีชื่อมอนสเตอร์ — NOW.md สั่งห้ามเปิด RE ใหม่จนมีผลจากเครื่องจริงและ P0-2 ขยับ
- **P-3** ปุ่ม GM — NOW.md เขียนเองว่า *"ไม่บล็อก LANE-GM"* งานที่เหลือ (ใบเทสสอง DLL,
  คีย์ `BRIDGE_GM_INSTALL_BAT`) อยู่ที่ chief · chief ตอบวันแล้วในใบ `0545` ว่าเป็นงานแรกของรอบถัดไปของเขา
  รอบนี้จึงไม่แตะหมุดกับเดคอเรเตอร์ตามที่เขาสั่ง

## ล็อกรอบ
ต้นรอบ list ทั้งสองรีโป: `pf_bridge` เปิดค้าง #941 (LANE-DB) #940 (LANE-E) #938 (LANE-B) #937 (LANE-A)
— **ไม่มีใบไหนขึ้นต้น `[LANE-GM]`** · `pirate-force-server` ไม่มี PR เปิดค้างเลย
⇒ ยึดล็อกด้วย draft PR `pf_bridge#942` (`[LANE-GM] WIP round claim dotoho`) ก่อนแตะโค้ด

## ชะตา PR รอบก่อน (ADDENDUM ข้อ A / AGENTS.md 7)
- `pf_bridge#934` (รอบ `gj77z5`) — **merged=true** 2026-09-02T22:59:19Z
- `pirate-force-server#626` (รอบ `gj77z5`) — **merged=true** 2026-09-02T23:16:27Z
⇒ ไม่มีอะไรต้อง cherry-pick กลับ

## กล่องจดหมาย — บริโภคครบสี่ใบ
| ใบ | ทำอะไร |
|---|---|
| `20260903_0646_COO-DECISION-lane-gm-...` | **ข้อ 2 ทำครบทั้งข้อรอบนี้** (เกต `PF_SPEED_TRIAL`) · ข้อ 0 กับ 1 รับทราบ ไม่มีงานตามมา |
| `20260903_0635_LANE-DB-TO-LANE-GM-...built` | อ่านสัญญาครบ · **ยังไม่เสียบรอบนี้** (นอกขอบเขตที่ COO กำหนด) จะเปิดใบของมันเองรอบหน้า · รับข้อเบี่ยง `BEGIN IMMEDIATE` เปล่า ไม่ขอให้รอนานกว่านี้ |
| `20260903_0525_LANE-DB-TO-LANE-GM-...not built` | ถูกแทนที่โดยใบ `0635` ของ LANE-DB เอง |
| `20260903_0545_CHIEF-TO-LANE-GM-...` | รับทราบทั้งสี่ข้อ · **ไม่สลับหมุด/เดคอเรเตอร์รอบนี้** ตามที่ chief สั่ง |
สตับ `.CONSUMED.txt` ลงครบสี่ใบ ต้นฉบับสำเนาเข้า `consumed/` ไม่มีใบไหนถูกลบ

## สิ่งที่สร้าง (เขตตัวเองล้วน)
`pirate-force-server`
- `src/pirateforce_foundation/gm/speed_wire.py` — `SPEED_TRIAL_ENV` `TRIAL_UNSET/MALFORMED/ARMED`
  `_as_f32_or_none` `trial_opening` `trial_admits` `trial_console_field` (+165 บรรทัด ไม่ลบของเดิม)
- `src/pirateforce_foundation/gm/chat_command_action.py` — `SPEED_TRIAL_CONSOLE_TOKEN`
  `SPEED_TRIAL_UNAVAILABLE` `EVENT_SPEED_TRIAL_ADMITTED` `_trial_console_field` `_trial_admits`
  `_print_speed_trial_open` + ฟิลด์ `trial_opens_for=` บนบรรทัด `SPEED DEFERRED` เดิม
- `tests/test_gm_speed_trial_gate.py` (ใหม่ 43 tests) · `tests/test_gm_chat_command_action.py`
  (ลงทะเบียนอีเวนต์ใหม่ในตารางสัญญา) · `tests/test_gm_speed_deferred.py` +
  `tests/test_gm_speed_action.py` (ล้าง `PF_SPEED_TRIAL` ใน `setUp` ให้เทสไม่ขึ้นกับเชลล์)
- `docs/GM_LANE.md` — หัวข้อรอบ `dotoho`

## สองล็อกยังปิดอยู่ วัดแล้ว
`SPEED_LOGIN_READ_LANDED` = `False` · `SHAPES_CLEARED_BY_A_REAL_CLIENT` = `frozenset()`
เทส `test_both_locks_are_still_shut_while_it_does` วัด **ในคอลเดียวกับที่เฟรมออก**
⇒ เกตนี้ **ข้าม** ล็อก ไม่ได้ **เปิด** ล็อก · รอบไหนทำด้วยการพลิกค่าคงตัวแทน เทสตัวนี้แดง

## บรรทัดคอนโซลที่ผู้คุมจอต้องอ่าน (COO `0646` ข้อ 2 บุลเล็ตสี่)
```
SPEED TRIAL OPEN account='GM_ONE' command=speed env=PF_SPEED_TRIAL trial_opens_for=450.0 sending=450.0 character_id=1 identity=1:0
```
และบรรทัดเดิมได้ฟิลด์ที่สี่: `SPEED DEFERRED ... trial_opens_for=450.0` (หรือ `unset` / `malformed`
/ `unavailable`) ⇒ คนที่พิมพ์เลขผิดรู้เลขที่ถูกจากคอนโซล ไม่ต้องกลับไปดูเชลล์

## หมุดของ pf-adversary ที่ดักดราฟต์แรกของรอบนี้ไว้เอง
ดราฟต์แรกเขียน `if speed_wire.send_deferred() and not trial_admitted:` ⇒
`test_gm_speed_denied_nine_paths.py::_assert_the_deferral_branch_holds_one_reason` **แดง ถูกแล้ว**
(หมุดของ pf-adversary รอบ `ha492g` D6: เขาเคยเขียนมิวแทนต์ `... or <อะไรก็ได้>` แล้ววัดว่า 276 เทสเขียว)
⇒ เปลี่ยนรูปเป็น **wrapper** `if not trial_admitted:` ครอบทั้งสองล็อก ล็อกทั้งคู่คงเงื่อนไข คำ audit
และบรรทัดคอนโซลเดิมทุกตัวอักษร · แล้วปักหมุดรูปของ wrapper เองเพิ่มจากฝั่งเทสของสายนี้

## มิวแทนต์ 11 ตัว ตาย 11
รวมตัวที่ **รอดในรอบแรก**: `_trial_admits(stored)` -> `_trial_admits(value)` เขียวทั้งไฟล์
เพราะสโตร์ดับเบิลสะท้อนเลขที่พิมพ์กลับมาทุกเทส ⇒ เพิ่มสโตร์ที่ read-back เบี่ยงจากที่พิมพ์
ปักสองทิศ: แถวถือค่าที่ arm ไว้ = ออกได้แม้พิมพ์เลขอื่น · แถวถือเลขอื่น = **กัก** แม้พิมพ์ตรง

## nonclaim (กฎข้อ 3 ของสายนี้)
- ใช้ GM ข้ามขั้นไหน: **ไม่มีเลย** รอบนี้ไม่ใช้สถานะ GM เป็นหลักฐานอะไรทั้งสิ้น
- **ไม่ใช่หลักฐานว่าค่า `/speed` ค่าไหนปลอดภัยกับไคลเอนต์** `GT-193` [FAIL] ยังเป็นผลวัดเดียวที่มี
  และมันจบด้วยตัวละครตาย ไคลเอนต์ล็อกตัวเอง และรอบ attended ที่เสียไปทั้งรอบ
- ไม่มีอะไรในรอบนี้ถูกรันบนไคลเอนต์จริง · ไม่มีไมล์สโตนไหนขยับ · P-1 ไม่ขยับ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
เมื่อวาน การลอง `/speed` ค่าเดียวบนไคลเอนต์จริงต้องแก้โค้ดบน `main` ซึ่งเปิดประตูให้ **ทุกค่า** พร้อมกัน
ถาวร และกับทุกคน — สิ่งที่ `COO 2147` ข้อ 3 ห้ามไว้ตรง ๆ
วันนี้เธอพิมพ์ `set PF_SPEED_TRIAL=450` ในหน้าต่างเซิร์ฟเวอร์ของเธอเอง แล้ว `/speed 450` ส่งได้
ส่วน `/speed 451` และทุกค่าที่เหลือยังถูกกักด้วยล็อกทั้งสองตัวเหมือนเดิม และประตูปิดเองเมื่อโปรเซสตาย

## backlog ของสาย (ติดที่ใคร)
1. **เสียบ `store.write_speed_by_identity` ของ LANE-DB** — ติดที่ **ตัวเอง** ใบของรอบถัดไป
   (นอกขอบเขตที่ COO ให้รอบนี้ กฎหนึ่งเรื่องต่อใบ)
2. **คีย์ `BRIDGE_GM_INSTALL_BAT`** — ติดที่ **chief** เขาระบุแล้วว่าเป็นงานแรกของรอบถัดไปของเขา (ใบ `0545`)
   สายนี้ห้ามสลับหมุดจนเขาส่งจดหมายพร้อมคำสั่ง `git grep`
3. **`GT-219` ใบวัดสอง DLL** — ติดที่ **ผู้เทส/เจ้าของ** หัวใบ `[BLOCKED]` โดยเจตนา (negative control
   13,824 ไบต์อาจถูกเขียนทับไปแล้ว) ห้าม build ใหม่เพื่อผลิตของชิ้นนั้น
4. **`GT-218` รอบทดลอง `/speed`** — ติดที่ **chief + เจ้าของ**: chief แก้ใบที่เขียนย้อนศร (`0649`)
   และเกตล็อกอินของใบ `0645` ต้องขึ้น `main` ก่อน ถึงจะเรียกรอบ attended ที่มีรีล็อกอินหลัง `/speed` ได้
5. **ตัว walker ที่รับ pytest-native precondition** — ติดที่ **ตัวเอง** (chief รับใบไว้แล้วถ้าเปิด) ยังไม่เปิด คิว COO อยู่เหนือ
