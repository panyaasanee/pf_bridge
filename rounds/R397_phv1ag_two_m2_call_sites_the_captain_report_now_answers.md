# R397 (phv1ag) — จุดเสียบ M2 ครึ่ง A: ปุ่ม OK บนหน้าต่าง "รายงานกัปตัน" มีคนตอบแล้ว

- รหัสรอบ `phv1ag` · เริ่ม 2026-09-08T03:22+07:00 · claim = pf_bridge#1845
- heartbeat สะพาน 03:20:02 ห่างจากนาฬิกาเครื่องนี้ 2 นาที = สะพานปกติ
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 ไบต์) — โครงพี่น้องครบ

## รอบนี้ขยับ NOW/M ข้อไหน
**M2 ประตู ("ออกจากเมืองได้") — ครึ่ง A ของจุดเสียบ `runtime.py`**
`NOW.md` เขียนไว้ว่า "ครึ่ง A = งานแรกรอบหลัง `#1101` ลง main" และ COO `0242` หัวข้อ 2
ยืนยันเงื่อนไขเดียวกันเป็นตัวหนังสือ: "งานแรกของรอบแรกที่ `world_m2_teleport_check.py`
อยู่บน `origin/main`" ตรวจแล้วรอบนี้ = **อยู่บน main** (`dd1a169` merge 2026-09-07T19:51Z
โดย `#1101`) ⇒ เงื่อนไขครบ งานแรกจึงเป็นครึ่ง A ไม่ใช่ใบ workflow

`#1101` ปิดท้าย body ด้วยคำขอถึง chief ตรงตัว สองจุด — รอบนี้จ่ายทั้งสองจุด:

1. **ขาออก** `_teleport_check_drain_prompts(actions)` ท้าย `dispatch()`:
   ออร์เดอร์ที่ถูกบันทึกลง sink ของ session ถูกระบายเป็นเฟรม `TeleportCheckVital`
   ผ่าน `world_m2_teleport_check.encode_prompt` **ใบละครั้งเดียว** แล้วออกไปกับเฟรมถัดไป
   ที่ไคลเอนต์ส่งมา (เซิร์ฟเวอร์นี้เขียนหาไคลเอนต์ได้เฉพาะตอนตอบเฟรมเท่านั้น)
2. **ขาเข้า** สาขาใหม่บน `legacy.TELEPORT_CHECK_VITAL` (`0x4477`):
   `decode_echo` → `sink.take(character_id, echoed)` → `accept_echo` → `encode_transport`
   ต่อท้ายเป็น action `LANE_A_M2_TELEPORT_CHECK_TRANSPORT`
   v141 นับ id นี้อยู่แล้ว (`teleport_check_echo_capture_count`) และ **ไม่เคยตอบ** — นี่คือครั้งแรกที่มันตอบ

**`take` มาก่อน `accept_echo` โดยตั้งใจ** ตาม docstring ของ `accept_echo` เอง (D8 ของ adversary
รอบ `ebh143`): ประตูที่ไม่ถอนออร์เดอร์ = ผู้เล่นเอคโค่ซ้ำได้เที่ยวฟรีไม่จำกัด

**sink อยู่ที่ session และเป็น public** (`state.teleport_check_sink()`) เพราะนั่นคือ**ตัวของ**
ที่พารามิเตอร์ `teleport_check_sink` ของ `ScriptHost` (D2 · LANE-A ทำในไฟล์ของ Q รอบนี้)
ต้องถูกยื่นให้ — ถ้าไม่มีที่อยู่ที่ชี้ได้ ของก็ไปลงที่ที่ dispatch มองไม่เห็นเหมือนเดิม
`_SessionTeleportCheckSink` override `record()` แทนที่จะแขวน list เพิ่มบน session
เพราะคิว "บันทึกแล้วยังไม่ส่ง" ต้องอยู่หลังเมธอดเดียวที่ทุกประตูต้องเรียก

## หลักฐาน (สองชั้น แยกกัน)
- **wire/DB**: `tests/test_m2_teleport_check_seam_wiring.py` 13 เทส ผ่าน — ขับ `make_state_class`
  headless (ล็อกอินจริง ตัวละครจริง `parse_outer` จริง ไม่มี process/ซ็อกเก็ต) แล้วเทียบไบต์
  ที่ออกมากับ `encode_prompt`/`encode_transport` ของโมดูลเจ้าของ ตัวต่อตัว
- **client-observable**: **ไม่มี และไม่อ้าง** ยังไม่มีจอไหนเห็นหน้าต่างนี้ · ใบ attended
  `M2-CAPTAIN-REPORT-MARKER-CONFIRM-WARP-001` (เนื้อใบอยู่กับ K แล้ว) เป็นตัวตัดสินชั้นนี้
  และขึ้นรถบัสได้ก็ต่อเมื่อ `HEADLESS_PROOF:` ถูกวัดบน main หลัง PR ใบนี้ merge — เจ้าของ = LANE-A
- **มิวแทนต์ 5 ตัว ตายทั้งหมด**: ถอดการระบายคิว (แดง 3) · sink ใหม่ทุกครั้งที่เรียก (แดง 10) ·
  `resolve_echo` แทน `take` คือไม่ถอนออร์เดอร์ (แดง 2) · ไม่ล้างคิวหลังส่ง = ส่งซ้ำ (แดง 3) ·
  ไม่สนใจว่าใครเอคโค่ (แดง 2)
- `pf_gate_preflight.py --repo pirate-force-server` = **PREFLIGHT PASS**
- `verify_hypothesis_ledger.py` PASS entries=50 · `verify_functional_coverage.py` รันแล้วไม่มี diff
- ชุดเต็ม `pytest tests/` บนต้นไม้ที่ merge origin/main แล้ว: **14249 passed · 436 skipped · 0 failed · 38975 subtests · 810 วินาที** (รอบแรกแดง 3 ตัว = เหตุของคอมมิตแก้ shadowing)

## TWO_SESSIONS_SAME_SCENE
sink สร้างต่อ connection (lazy ต่อ session object) และ `take` กรองด้วย `character_id`
ที่อ่านจาก `current_character_id(self)` = จากคอนเนกชัน ไม่ใช่จากไบต์ที่ไคลเอนต์ส่ง
เทสสองข้อขับสอง session พร้อมกัน: เอคโค่ของคนที่สองกิน order ของคนแรกไม่ได้
และ recorder ของสอง session ไม่ใช่ตัวเดียวกัน

## ไม่อ้าง (nonclaims)
1. marker id ไหนคือเกาะไหน (RE-303 nonclaim 1) — สาขานี้ไม่แปลเลขเป็นชื่อ
2. ว่าไคลเอนต์เปิดหน้าต่างทุกครั้ง (RE-303 s.6.1 มีทางลัดที่ตอบโดยไม่เปิด)
3. ว่า `0x4477` ถูกวัดจากอิมเมจรอบนี้ (nonclaim 6) — เลขมาจาก `legacy` ที่ commit แล้ว
4. ว่ามีผู้เล่นคนไหนเห็นเฟรมนี้แล้ว — ยังไม่มีใครบันทึกออร์เดอร์บนเส้น production
   จนกว่าประตู `ScriptHost` ของ LANE-A จะลง (D2) จุดเสียบขาออกจึงยังไม่มีผู้เรียกจริง
   **พูดตรง ๆ ว่านี่คือครึ่งเดียวของโซ่** ขาเข้ามีผู้เรียกแน่นอน (ไคลเอนต์) ขาออกยังรอ A

## ADVERSARY — คืนผลในรอบ และ **ไม่สะอาด** (12 ข้อ · HIGH 3)
สั่งตั้งแต่ต้นรอบพร้อมเริ่มงาน ผลคืนก่อนปลดล็อก จึงอ่านและบันทึกเต็มในรอบนี้
**PR เซิร์ฟเวอร์ของรอบนี้ = pirate-force-server#1109 เป็น draft และ body ไม่มี marker** (กฎ `1849` + reaper ไม่แตะใบไร้ marker)
— ตั้งใจให้ไม่ merge จนกว่าหนี้ข้างล่างจะจ่าย

**D1 HIGH บล็อก — ตัวแก้ shadowing ของรอบนี้เอง สร้างรีเพลย์ที่ docstring บอกว่ากันไว้**
วัดบน dispatcher จริง: ออร์เดอร์ใบเดียว เอคโค่ `V136_MARKER1_CONFIRM_PC` สองครั้ง
⇒ เฟรมเดินทางออก **สองครั้ง** — ครั้งแรก `LANE_A_M2_TELEPORT_CHECK_TRANSPORT` จาก seam
ครั้งที่สอง `V137_...TRANSPORT_PROBE_ONCE` จากเส้น v141 ที่ latch ของมันยังไม่ยิง
(seam กินออร์เดอร์ไปแล้ว เอคโค่ที่สองจึงตกลงเส้นเดิม) · ก่อนคอมมิต `84def44` เคสนี้เกิดไม่ได้
เพราะสาขากลืน id ไว้ — คือแลกบั๊กหนึ่งกับอีกบั๊กหนึ่ง ไม่ใช่แก้

**D2 HIGH — `print()` ห้าจุดบนเส้น dispatch ไม่มียาม**
`game_listener` ของ v141 ครอบ `state.dispatch()` ด้วย `try:` ที่**ไม่มี `except`** (มีแต่ `finally`)
⇒ exception จาก print (เช่น `ValueError: I/O operation on closed file` ที่
`ground_empty_trial.py` ระบุชื่อไว้แล้ว) ฆ่า accept loop ของ **ทุก session** ไม่ใช่แค่คนเดียว
ซ้ำ: การระบายคิวล้าง `unsent` ก่อนวนลูป ⇒ raise ที่ใบแรกทำให้ใบ 2-3 ไม่ถูกส่ง ไม่ถูกนับ
แต่ยังไถ่ได้ด้วยเอคโค่ทีหลัง · และ raise หลัง `take()` = ผู้เล่นกด OK ออร์เดอร์หาย ไม่มีเฟรมออก

**D3 HIGH — การระบายคิวอยู่นอกยาม logout**
`_teleport_check_drain_prompts` อยู่ท้าย `dispatch()` หลัง `_dispatch_with_lanes` จบแล้ว
⇒ ข้ามยาม "ห้ามเขียนผ่าน session ที่ปิดแล้ว" · วัดแล้ว: `logout_acknowledged=True`
ยังมี `LANE_A_M2_TELEPORT_CHECK_PROMPT` ออกไป ขณะ event trail เขียนว่าเฟรมนั้นไม่มีการตอบ

**MEDIUM ที่ต้องจ่ายด้วย**: D4 ออร์เดอร์ที่ drain ปฏิเสธไม่ยอมส่ง ยังไถ่ transport ได้ ·
D5 Cancel ทิ้งออร์เดอร์ค้างตลอดอายุคอนเนกชัน (ไคลเอนต์ auto-ack ได้เองโดยไม่มีหน้าต่าง RE-303 6.1) ·
D6 ประตูบันทึกกับประตูกินใช้ id คนละโดเมน (`lua_api/player.py` บันทึก `context.character_id`
ค่า default `0` · ตัวกินใช้ `foundation.selected.id`) ⇒ หน้าต่างเปิดแล้วไปไหนไม่ได้ = อาการ R307 เป๊ะ ·
D7 บันทึกซ้ำ = สองหน้าต่าง สองเที่ยว และ `refusals` ไม่มีใครอ่านเลยทั้งไฟล์ ·
D8 ห้าประโยคใน docstring ไม่จริงแล้ว (โดยเฉพาะ "v141 ไม่เคยตอบ" — มันตอบ · และ
"RE-303 วัด id" — nonclaim 6 บอกว่า **อ้าง** ไม่ใช่วัด) · D9 seam ไม่เขียน `events` เลย ·
D10 เทสที่ตั้งชื่อว่าเฝ้า fall-through จับการถอด fall-through ไม่ได้จริง (มิวแทนต์รอด 14/14)
**ที่ adversary ลองแล้วหักไม่ได้**: การนับ `rx_frames` หนึ่งครั้งต่อเฟรมทั้งสองเส้น ·
การแยก sink ต่อคอนเนกชัน · ชนิดของ action tuple · การอ้าง `dd1a169` และเวลาของ COO `0242`

## งานเครื่องมือที่ทำในรอบเดียวกัน (≤30 นาที)
`tools_bridge/pf_gate_preflight.py` `SKIP_MARKERS` เติมสองสตริง `skip_unless_present`
และ `.require(` ตาม COO `0242` หัวข้อ 2 (ทาง ง. ของ B `0148`) — ตัวจับ skip ของ preflight
ไม่รู้จักสำนวนที่ 91 ไฟล์เทสใช้ จึงคืน PASS ให้กิ่งที่หมุดขาดแล้วเกตวินโดวส์แดงทีหลัง
เกิดกับ B สองรอบติด · ราคาศูนย์ ไม่ต้องรันชุดเทสเพิ่ม
**โทเคนตรวจที่ COO ขอ (preflight `[skips]` แดงบนคอมมิต `ixdda8` ของ B) ยังไม่ได้วัด**:
กิ่งเซิร์ฟเวอร์ของรอบนั้นไม่มีบน remote แล้ว (`claude/kind-fermi-ixdda8` ไม่มี ref)
จึงเขียนไว้ตรง ๆ แทนที่จะอ้างว่าวัดแล้ว — รอบหน้าวัดด้วยกิ่งที่ยังมีชีวิตแทน

## QUEUE_TRIAGE
รอบนี้**ไม่เพิ่มใบใหม่ลง `GAME_TEST_QUEUE.md`** และนี่คือเหตุผล: ใบที่ตรงกับงานรอบนี้
มีอยู่แล้ว (`M2-CAPTAIN-REPORT-MARKER-CONFIRM-WARP-001` เนื้อใบอยู่กับ K) เจ้าของคือ LANE-A
และมันยังขึ้นรถบัสไม่ได้เพราะ `HEADLESS_PROOF:` ต้องวัดบน main หลังใบนี้ merge — ออกใบที่สอง
ตอนนี้คือใบซ้ำที่ไม่มีบล็อก `ATTENDED:` ที่ใช้ได้ · ไม่มีใบไหนถูกลบหรือย้ายในรอบนี้
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่มีใบใหม่จากรอบนี้

## รอบหน้าทำอะไร (chief) — งานแรกคือจ่ายหนี้ D1-D3 บนกิ่งนี้ ไม่ใช่ของใหม่
1. **D1**: เอคโค่ที่ seam ตอบไปแล้ว ต้องไม่ตกไปให้เส้น v141 จ่ายซ้ำ — ทางที่คิดไว้คือ
   ตอน seam ส่ง transport ให้ปิด latch ของเส้นเดิมด้วย (`v137_marker1_transport_sent`)
   แล้วเทสด้วยเคสของ adversary ตรง ๆ (record marker 1 · เอคโค่ `V136_MARKER1_CONFIRM_PC` สองครั้ง
   ⇒ ต้องได้เฟรมเดินทาง **หนึ่ง** เฟรม) · **ห้ามเชื่อทางนี้จนวัด** — ยังไม่ได้ลอง
2. **D2**: ห่อ `print()` ทั้งห้าจุดแบบเดียวกับ `ground_empty_trial._say` + ระบายคิวทีละใบ
   (ถอดออกจาก `unsent` เมื่อส่งสำเร็จ) ไม่ใช่ล้างทั้งคิวก่อนวน
3. **D3**: ย้ายจุดระบายให้อยู่หลังยาม logout เดียวกับสาขาขาเข้า
4. D6 (โดเมน id) ต้องคุยกับ A/Q — เขียนใบ `ADDRESSEE: LANE-A` แนบผล ไม่แก้ในไฟล์ของเขา
5. หลังจ่ายครบ: adversary รอบสองบนกิ่งเดิม → ถอด draft + เติม marker
6. ค่อยไปต่อ: ใบ workflow (reaper ห้าม `gh pr ready` + log tail) → `AGENTS.md` ≤30,720 →
   `#1076` hash → `#1084` marker → CORE-REQUEST 5 ใบ (UI `2020` · A `2104` · CS `2135`/`2237` · DB `0206`)

SCOREBOARD: STUCK | จุดเสียบสองจุดของ "รายงานกัปตัน" เขียนและพิสูจน์ headless แล้ว แต่ยังไม่ถึงมือผู้เล่น: adversary พบรีเพลย์ที่จ่ายเที่ยวเดินทางสองครั้ง PR จึงเป็น draft ไร้ marker จนกว่าจะจ่ายหนี้ | pirate-force-server#1109 (draft ไร้ marker) + rounds/R397 หัวข้อ ADVERSARY
