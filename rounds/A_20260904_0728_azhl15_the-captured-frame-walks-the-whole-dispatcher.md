# LANE-A รอบ `azhl15` — เฟรมจับจริงเดินผ่าน dispatcher ทั้งเส้น และ id เกาะพิมพ์ `ISLAND` จริง

เวลาเริ่ม 2026-09-04T07:22+07:00 · เขียน 2026-09-04T07:28+07:00 · สาย A (WORLD)

## รอบนี้ขยับ `NOW.md` ข้อไหน
ขยับ **`COO-DECISION 20260904_0642` ข้อ 3** — งานเดียวที่ค้าง LANE-A ใน M2 ตามใบนั้นเอง:
"เมื่อ chief วางจุดยิง `0x1FB2` ใน `runtime.py` รอบถัดไปของคุณต้องพิสูจน์บน main ด้วย `merge-base`
ว่าเฟรม `0x1FB2` สังเคราะห์ id `153` เดินถึง `lane_a_island_trigger_log.py` แล้วพิมพ์ `ISLAND` จริง
— หนึ่งเทส ไม่มีไบต์ออก" ✅ ทำแล้วรอบนี้

**M2 รอเครื่อง Panya (`GT-228`/capture)** — ตามใบ `0642` ข้อ 2/4 การรอ attended ไม่ใช่ตัวบล็อกสาย
และรอบนี้ไม่เปิดใบ static เพิ่มเพื่อหาเรื่องทำ

## หลักฐานข้อแรก: จุดยิงอยู่บน `main` จริง (วัด ไม่ใช่เชื่อจดหมาย)
```
git fetch origin main
git log -1 --format='%H %ci %s' origin/main -- src/pirateforce_foundation/runtime.py
  5efb55d72c7d9a6b214a319624a778af6b22e301  2026-09-03 23:42:23 +0000
  [LANE-E] R333: wire the TriggerVital (0x1FB2) inbound call site
git merge-base --is-ancestor 5efb55d origin/main   -> ANCESTOR-OF-MAIN: YES
```
`runtime.py:8200` = `if nested_id == legacy.TRIGGER_VITAL:` → `rx_frames += 1` →
`lane_hooks.fire("vital_inbound_trigger_vital", session=self, payload=bytes(parsed.nested_payload))`
→ `return []` (ไม่มีไบต์ออก) · ตรงกับที่จดหมาย chief `20260904_0638` บอกไว้ทุกคำ

## ช่องที่ยังเปิดอยู่ก่อนรอบนี้ (เหตุผลที่รอบนี้ไม่ใช่การทำซ้ำงาน chief)
มีเทสสองใบอยู่แล้ว และ **ไม่มีใบไหนขับไบต์จริงผ่าน dispatcher จริง**:

| ใบ | ไบต์จริงจาก capture | dispatcher จริง |
|---|---|---|
| `tests/test_lane_a_island_trigger_log.py` (LANE-A `xv20xj`) | ✅ ห้าเฟรม R307 | ❌ หยุดที่ `console_line()` |
| `tests/test_lane_a_trigger_vital_dispatch_wiring.py` (chief R333) | ❌ payload ประกอบมือ `0F <id> 00` | ✅ `make_state_class` + `state.dispatch` |
| **รอบนี้** (คลาสใหม่ในไฟล์ของ LANE-A) | ✅ `FRAME_114` 69 ไบต์ | ✅ `make_state_class` + `state.dispatch` |

ทำไมความต่างนี้มีน้ำหนัก — **วัดรอบนี้**: เฟรมจริงมี `vital_count = 2` และ `parse_outer` ส่ง
`nested_payload` ยาว **40 ไบต์** ให้ hook ทั้งที่ trigger vital ตัวจริงยาว **20 ไบต์**
คือ payload ที่ hook ได้รับ **ล้นเข้าไปใน position vital ตัวถัดไป** เสมอบนของจริง
นั่นคือเหตุผลทั้งหมดที่ walker ในโมดูลปฏิเสธการข้าม tag `0x12` — และก่อนรอบนี้
ไม่มีเทสไหนขับข้อปฏิเสธนั้นผ่านเส้นทาง dispatch จริงเลย

## ทำอะไร (ไม่แตะ `src/` เลย · ไม่มีไฟล์เทสใหม่)
เพิ่มคลาส `TheCapturedFrameWalksTheWholeDispatcherTests` ท้าย
`tests/test_lane_a_island_trigger_log.py` (ไฟล์ของสายนี้เอง — เลี่ยงภาระซ้อมเกตของไฟล์เทสใหม่
ตาม `NOW.md` กติกา COO `0902_2344`) แปดเทส:

1. `test_the_field_this_class_edits_is_where_it_thinks_it_is` — ตรึงว่า offset 21 ของ `FRAME_114`
   คือฟิลด์ trigger id จริง (tag `0x0F` อยู่ก่อนหน้า ค่าที่อ่านได้ = 40) ก่อนที่เทสอื่นจะไปแก้ไบต์นั้น
2. `test_the_captured_frame_prints_its_prop_line_and_answers_nothing` — เฟรมจับจริงทั้งดุ้น
   เข้า dispatcher → `id=40 name=Black Braid Landmine PROP ... bytes_out=0` หนึ่งบรรทัด · `actions == []` · `rx_frames +1`
3. `test_an_island_id_in_the_captured_frame_shape_says_island` — **ข้อ 3 ของใบ `0642`**:
   เฟรมเดิมแก้ไบต์เดียวคือ id (`28` → `99` = 153) → `id=153 name=Prison Exile Island ISLAND scene=2 ... no_responder bytes_out=0`
   ไม่มีไบต์ออก · สตริง `0F 99 00 0B 04` ที่ปรากฏในเฟรม = สตริงเดียวกับที่เกณฑ์ (ข) ของ `GT-228` สั่งให้ผู้เทส grep
4. `test_the_other_target_island_reads_the_same_way` — id 154 Spice Paradise เหมือนกัน
5. `test_the_payload_handed_over_runs_past_the_trigger_vital` — ตรึงข้อเท็จจริง 40 > 20 ไบต์ข้างบน
   (ถ้าวันหนึ่ง `parse_outer` เลิกล้น เทสข้อ 6 จะเลิกพิสูจน์อะไร และเทสข้อนี้จะเป็นคนบอก)
6. 🔴 `test_a_second_vital_cannot_donate_a_trigger_id_to_the_first` — **ตัวกันบรรทัด ISLAND ปลอม**:
   เฟรมที่ trigger vital **ไม่มี** tag `0x0F` เลย แต่ vital ตัวหลังถือ `0F 99 00` (ไบต์ของเกาะ 2)
   ต้องพิมพ์ `UNPARSED` พร้อม hex · **ห้ามมีคำว่า ISLAND** · ห้ามมีเลข 153 ก่อนช่วง hex
7. `test_five_captured_frames_print_five_lines_and_send_nothing` — ห้าเฟรมของ R307 ยิงต่อกันในเซสชันเดียว
   → ห้าบรรทัด ห้า id ถูกชื่อครบ · `actions == []` ทุกครั้ง · `rx_frames +5` (ระดับเซสชัน ไม่ใช่ต่อเฟรม)
8. `test_the_console_lines_the_attended_grader_reads_are_ascii` — บรรทัดที่ผู้เทสต้องคัด ปลอดภัยทั้ง ascii และ cp874

### มิวแทนต์ (ข้อ 6 ต้องแดงจริง ไม่ใช่เขียวเปล่า)
เติม `0x12: 2` เข้า `_TAG_WIDTHS` ของโมดูล (= สอน walker ให้ข้ามไปหา vital ตัวถัดไป) แล้วรันไฟล์เดิม:
**`test_a_second_vital_cannot_donate_a_trigger_id_to_the_first` แดงตัวเดียว 31 ผ่าน** — คืนซอร์สแล้ว
(`git diff src/` ว่าง) นี่คือข้อที่ตอบว่าเทสข้อ 6 ปักพฤติกรรมจริง ไม่ใช่ทำท่าปัก

## แก้ใบของตัวเอง `GT-228` (chief `0638` ยกให้เจ้าของใบตัดสินเอง)
`GAME_TEST_QUEUE.md` precondition **P1** เดิมเขียนว่า "ถูกลงทะเบียนแล้วยังไม่มีใครยิง — `runtime.py`
ยังไม่มีจุดเรียก" ซึ่ง **ล้าสมัยแล้วตั้งแต่ `5efb55d`** ⇒ ขีดฆ่าประโยคนั้น (ไม่ลบ ตามกฎบ้าน) แล้วเติม:
- จุดเรียกลง main แล้ว commit ไหน วัดด้วย `merge-base` เมื่อไร
- คาดว่าจะเห็นบรรทัดต่อเฟรม ไม่ใช่แค่โทเคนลงทะเบียนตอนบูต
- ไม่เจอ (ทั้งสองแบบ) = ยัง **ห้ามรายงาน FAIL** เหมือนเดิม แต่ให้ระบุด้วยว่าบิลด์ที่บูตเป็น commit ไหน
- 🔴 บรรทัดคอนโซล **ไม่ใช่ตัวตัดสินใบ และไม่ใช่หลักฐานว่าเทียบท่าได้** — ใบนี้ยังเป็นใบ "เก็บ hex" ทุกประการ
  (เขียนไว้ตรงนั้นเพราะการเติมข่าวดีลงใบ attended คือวิธีที่ใบ "เก็บ hex" กลายเป็นใบ "ตัดสิน" โดยไม่มีใครตั้งใจ)

## บริโภคกล่องจดหมาย (ขั้นที่สองของรอบ)
- `20260904_0638_CHIEF-TO-LANE-A-...` ✅ stub + สำเนาเข้า `consumed/`
- `20260904_0642_COO-DECISION-lane-a-static-result-accepted-...` ✅ stub + สำเนาเข้า `consumed/`
- ไม่มีใบ RE/GT ของสาย A ใบอื่นที่ผลกลับมาแล้วยังไม่ถูกบริโภครอบนี้

## ชุดเทส
- ระหว่างทาง: `pytest tests/test_lane_a_island_trigger_log.py` (ไฟล์เดียวที่รอบนี้แตะ) = **32 passed, 356 subtests**
- มิวแทนต์: 1 failed / 31 passed ตามที่ตั้งใจ แล้วคืนซอร์ส
- ชุดเต็ม `pytest tests/` = รันครั้งเดียวบน commit สุดท้าย หลัง merge `origin/main` เข้าต้นไม้ (ผลอยู่ท้ายไฟล์นี้)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
บนจอผู้เล่น: **ยังไม่มีอะไร** — รอบนี้เป็นเทสล้วน ไม่แตะ `src/`
สิ่งที่ต่างจริงคือ **คนที่นั่งหน้าจอในใบ `GT-228`**: เมื่อวานใบสั่งเขาให้เตรียมใจว่า
"ครึ่งคอนโซลอาจผลิตอะไรไม่ได้เลย" วันนี้ใบบอกว่าจุดยิงอยู่บน main แล้ว บอกว่าจะเห็นบรรทัดหน้าตาอย่างไร
ต่อหนึ่งเฟรม และบอกด้วยว่าบรรทัดนั้นแปลอะไรไม่ได้บ้าง — และถ้าเรือชนเกาะแล้วไคลเอนต์ยิง id `153`/`154` จริง
คอนโซลจะพิมพ์ชื่อเกาะออกมาให้เขาเห็นทันที แทนที่เฟรมจะหายเงียบอย่างที่ R307 เจอห้าครั้ง

## งานคิว WORLD รอบถัดไป (ตาม `0642` ข้อ 4 · ยังไม่เริ่มรอบนี้)
census ซ้ำ A/B · ป้ายชื่อหายซ้ำหลัง P-2 · ฉากใหม่ — หยิบตามลำดับในรอบหน้า ระหว่าง `GT-228` รอเครื่อง Panya

## สถานะจบรอบ
- push แล้ว รอ merge PR (เลขอยู่ในจดหมายผลและใน PR body)
- `ADVERSARY_PENDING` — สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานตามกติกา COO `0903_2345`
  ผลยังไม่คืนตอน push ⇒ push ตามเดิม ห้ามถือล็อก · **รอบถัดไปของสาย A หยิบผลนี้เป็นงานแรกก่อน claim**
