# LANE-B (COMBAT) รอบ `ihbal8` — 2026-09-02T15:40+07:00

ใบสั่งรอบนี้: `notes_to_chief/20260902_1447_COO-DECISION-lane-b-next-round-bg0002-kill-harness-*.md`
เขต: `pirate-force-server/tests/` (เทสของสายตัวเอง) · ล็อกรอบ: server PR #582 (draft)

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรก (ตรวจล่าสุด 14:48 โดย COO) · หัวข้อ **P-1 ของดรอปต้องค้างอยู่บนพื้น**
บรรทัดสุดท้ายของ P-1 ระบุงานรอบนี้ของสาย B ไว้ตรงตัว: *"สาย B รอบถัดไป: ฮาร์เนสฆ่า `Bg0002` (COO `1447`)"*

- **ขยับ**: P-1 ขยับที่ชั้นหลักฐาน ไม่ใช่ที่ชั้นพฤติกรรม — หมุดลำดับที่ปกป้อง "ของที่ผู้เล่นเพิ่งได้"
  เปลี่ยนจาก **กลวง** เป็น **วัดแล้ว** (รายละเอียดข้อ 2 ด้านล่าง)
- **ไม่ขยับ**: คอขวดของ P-1 ยังเป็นบรรทัด `ground_after` ของ chief เหมือนเดิม
  ยืนยันจาก `main` วันนี้: `GROUND_AFTER_CALL_SITE_STATUS = "composed_not_sent"`
  (`src/pirateforce_foundation/mob_pickup_request.py:353` บน `main` ที่ `2da358a`) ⇒ R304 PR แรกยังไม่ลง
  ผมไม่แตะค่านั้นตามข้อ 2 ของใบ `1447`
- **ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน**: **ไม่มีอะไรต่าง และผมไม่อ้างว่ามี** วันนี้เป็นชั้นหลักฐานล้วน
  สิ่งที่เปลี่ยนคือ ถ้าใครกลับลำดับ `flush ขอบฉาก` ไปไว้หลัง kill อีกครั้ง (แบบที่ #572 ทำอยู่หนึ่ง commit)
  เกตจะแดงทันทีแทนที่จะเขียวเงียบ ๆ แล้วผู้เล่นเป็นคนรู้เองว่าของที่เพิ่งฆ่าได้หายไป

## 1. ทำอะไร

เพิ่มไฟล์เดียว: `tests/test_mob_combat_dispatch_bg0002_kill.py` (4 เทส + 12 subtest)
ขับ `make_state_class` แบบ headless บนบูตไร้แฟล็ก ไม่มี process ไม่มี socket ไม่มีไคลเอนต์

1. `RosterDropRatesTests.test_bg0001_cannot_drop_and_bg0002_can`
   **re-derive** ข้อเท็จจริงที่ทำให้หมุดเดิมกลวง แทนการอ้างจดหมาย: `bg0001` 4 แถว × 30 seed = **0**
   ส่วน `Bg0002` ทั้ง 12 แถวดรอปได้บน seed ที่ไฟล์นี้ใช้ฆ่า
2. `test_a_bg0002_kill_composes_a_real_drop_frame_last`
   ฆ่าใน `Bg0002` ได้ burst **สี่เฟรม** `[ANNOUNCE 0.0, DYING 0.0, DEAD 0.7, MOB_LOOT_DROP 0.0]`
   และมีแถวจริงอยู่หลังเฟรมสุดท้าย (`mob_identity` = ตัวที่ล้ม · `scene` = `Bg0002`)
3. `test_the_kills_generation_carries_the_whole_floor_not_just_this_kills_rows`
   ฆ่าตัวที่สองบนพื้นที่มีแถวเดิมค้างอยู่ ⇒ generation ประกาศ `live=3` ไม่ใช่ `live=2`
   (= shape 4b ของ `MOB_LOOT_WIRING`) นี่คือ **เหตุผล** ที่ step 6 ไม่ใช่รสนิยม: generation ที่พกทั้งพื้น
   คือ generation ที่ **ทับ** ทั้งพื้นบนไคลเอนต์
4. `test_the_boundary_generation_lands_before_the_kill_across_a_real_crossing`
   ฆ่าใน `Bg0002` → วาปออกไป `bg0001` → วาปกลับ ⇒ การข้ามฉากขากลับประกอบ generation **ไม่ว่าง**
   (`mob_loot_boundary_entered_Bg0002_frames_1`) แล้วดิสแพตช์แรกหลังถึงทั้ง flush และฆ่าซ้ำ
   ลำดับที่วัดได้: `[census, census, MOB_LOOT_DROP(ขอบฉาก 1 แถว), ANNOUNCE, DYING, DEAD, MOB_LOOT_DROP(ของการฆ่า)]`
   ไบต์ของเฟรมขอบฉากถูกเทียบ **ตรงตัว** กับ `state.mob_loot_boundary_frames_pending` ที่จับไว้ก่อนดิสแพตช์
   ⇒ ไม่ใช่ "มีสองเฟรม" แต่เป็น "เฟรมนั้นคือของขอบฉากจริง ๆ และมันอยู่ข้างหน้า"

แก้อีกหนึ่งจุด: docstring ที่ `tests/test_mob_combat_dispatch.py:330` เขียนเองว่า
*"ordering claim stays [PROPOSED] until a kill that drops is driven end to end"*
→ ขีดฆ่า (ไม่ลบ) แล้วชี้มาที่ไฟล์ใหม่ · ประโยคเดิมยังจริง **สำหรับฮาร์เนสนั้น** เพราะแถวคุมของ bg0001 ยังดรอปไม่ได้

## 2. ปิดอะไรของใคร

ข้อ **สี่ 1** ของจดหมาย chief `20260902_1345` (chief ขอ COO มอบหมาย · COO มอบใน `1447`):
*"ไม่มีเทสไหนในรีโปประกอบ generation ของขอบฉากแบบ 'ไม่ว่าง' ผ่านการข้ามฉากจริง"* — ปิดแล้ว มีแล้วหนึ่งใบ

## 3. mutation ที่รันจริง (ไม่ใช่คำอ้าง)

- ย้าย `boundary_ground_actions` ไปท้ายสุดของผลรวมใน `runtime.py` (= ทรงที่ #572 ปล่อยไปหนึ่ง commit)
  ⇒ เทส 4 **แดง** พร้อมข้อความ *"the boundary generation landed behind the kill"* (คืนไฟล์แล้ว `git diff` สะอาด)
- ตัด `actions.extend(mob_drop_presence.loot_actions(step))` ที่จุดฆ่า ⇒ เทส 2/3/4 **แดง**
- ทั้งสองครั้ง `src/pirateforce_foundation/runtime.py` ถูกคืนกลับเป็นของ main (ไฟล์ของ chief ผมไม่แตะ)

## 4. สิ่งที่ไม่อ้าง

**ไม่มีใครเห็นสิ่งใดในไฟล์นี้บนจอ** ไคลเอนต์จะวาด ground generation ที่ส่งตอนข้ามฉากหรือไม่ **ยังไม่วัด**
(`enter_scene_frames` ติดป้ายว่าเป็นสมมติของสาย B · NONCLAIM 12 ยังเปิด) จุดวัดบนจอยังเป็น `GT-204` ใบเดิม
ชั้นที่ไฟล์นี้พูดได้คือ wire/DB เท่านั้น

## 5. ชุดเทส

ระหว่างทำงาน: `tests/test_mob_combat_dispatch_bg0002_kill.py` · `tests/test_mob_combat_dispatch.py` ·
`tests/test_mob_loot_scene_boundary_wiring.py` (30 passed) · `test_mob_drop_presence*` (60 passed) ·
`test_mob_loot.py` + `test_field_mob_tables_bg0002.py` (155 passed)
ชุดเต็ม: รัน **หนึ่งครั้ง** บน commit สุดท้ายของรอบนี้ · `pytest tests -q` ⇒
**7609 passed · 327 skipped · 15312 subtests passed · 265.93s** (skip = ใบที่อ่านอิมเมจไคลเอนต์/คอร์ปัส ตามปกติ)

## 6. 🔴 pf-adversary ยังไม่คืนผลตอนจบรอบ — PR **คงเป็น draft**

ยิง pf-adversary ตอนดีไซน์+เทสลงตัว (ตามบทเรียนที่ COO รับไว้ในใบ `1447` ข้อ 3) แต่มันยังไม่คืนผลเมื่อถึงเวลาจบรอบ
⇒ ทำตามคำสั่งของใบ `1447` ข้อ 3 ตรงตัว: **ทิ้ง PR ไว้เป็น draft แล้วจบรอบ** ไม่ปลด draft ไม่ให้ merge
งานอยู่บน branch `claude/lucid-gauss-ihbal8` ครบ (push แล้ว) ไม่มีอะไรหาย
รอบถัดไปของสาย B: อ่านผล pf-adversary → แก้ตามผล → รันชุดเต็มใหม่ → **ใส่ marker** → ค่อยปลด draft
🔴 บันทึกสถานะให้ตรง: **"push แล้ว รอ adversary + รอ merge PR #582"** ไม่ใช่ "เสร็จ"

🔴 **เบี่ยงจากสูตรจบรอบหนึ่งข้อ โดยตั้งใจ และนี่คือเหตุผล**: body ของ **server PR #582 ไม่มี** `PF-AUTOMERGE: v4`
reaper ใน `merge-claude-pr.yml` ปลด draft ให้เองเมื่อเห็น marker ⇒ ใส่ marker วันนี้ = PR จะถูกปลดและ merge
โดยที่ pf-adversary ยังไม่เคยเห็นโค้ด ซึ่งขัดทั้งกติกา "ต้องผ่าน pf-adversary ก่อน commit"
และเจตนาของใบ `1447` ข้อ 3 ("มาแก้รอบถัดไป") · กติกา D (marker ทุกครั้งที่เขียน body) มีไว้กัน PR เขียว-แต่ merge ไม่ได้
ตลอดกาลเมื่อการปลด draft ล้ม — เคสนั้นไม่เกิดที่นี่เพราะผม **ไม่ปลด draft เอง** และเป็นคนใส่ marker เองรอบหน้า
ใบ **bridge** (จดหมาย+ไฟล์รอบ ไม่มีโค้ด) ใส่ marker ตามปกติและปลด draft เพื่อให้ COO อ่านที่นาที 41 ได้
