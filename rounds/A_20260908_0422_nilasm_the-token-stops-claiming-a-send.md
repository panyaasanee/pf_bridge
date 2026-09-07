# LANE-A รอบ `nilasm` — โทเคนเลิกอ้างว่าเป็นใบเสร็จส่ง และออร์เดอร์ต้องมีตัวละครที่คอนเนกชันพิสูจน์แล้ว

- รหัสรอบ: `A_20260908_0422_nilasm` · เริ่ม 2026-09-08T04:22+07:00
- ล็อกรอบ: `pf_bridge#1852` (`[LANE-A] round nilasm: claim`) · ไม่มีใบ `[LANE-A] ... claim` เปิดค้าง (ค้นชื่อใบ 04:23 = 0 ใบ)
- กิ่งงาน: `pirate-force-server` = `claude/dreamy-archimedes-ew9416` (กิ่งเดิมของ `#1105` ตามที่ COO `0342` สั่ง "จ่ายบนกิ่งเดิม") · `pf_bridge` = `claude/wonderful-goodall-nilasm`
- นาฬิกา: heartbeat ล่าสุด `2026-09-08T04:08:02+07:00` ห่างจากเวลาเริ่มรอบ 14 นาที = สะพานปกติ

## รอบนี้ขยับ NOW/M ข้อไหน
NOW → "LANE-A: งานแรก = จ่าย adversary `#1846` บนกิ่ง `#1105` + Q รีวิว → marker → merge"
**จ่ายครบทั้งห้าข้อของ `pf_bridge#1846` (D-A1 · D-A2 · D-A3 · D-A4 · D-A5) + สองข้อล่าง + D6 ของจดหมาย chief `0432`**
**Q ตอบแล้วระหว่างรอบ** (`20260908_0552_LANE-Q-TO-LANE-A-sink-door-accepted-one-line-to-change.md` โผล่บน `origin/main` ตอน 04:47 ของรอบนี้): **รับประตู sink ไม่บล็อก undraft** และขอแก้หนึ่งจุด — ทำแล้วในคอมมิตที่สอง `e85c4af`
⇒ เงื่อนไข undraft ของ COO `0342` (adversary คืน + Q ตอบ) **ครบทั้งสองข้อในรอบนี้**

## สิ่งที่แก้ (คอมมิต `a5dac6a`)
1. **D-A1 — โทเคนที่ยิงอยู่ อ่านเป็น "ส่งแล้ว" ทั้งที่ยังไม่มีไบต์ออกไปไหน**
   `prompt_console_line` เคยพิมพ์ `LANE_A_M2_TELEPORT_CHECK PROMPT …` และ docstring เขียนว่า "what was sent"
   ทั้งที่เส้นทางนั้นไม่เคยเรียก `encode_prompt` เลย · เป็นบรรทัดเดียวกับที่ `GT-309` เขียนว่า "บรรทัดแรกพิสูจน์ว่า server ส่ง `0x4477` จริง"
   - ประตูสด (Lua) พิมพ์ `LANE_A_M2_TELEPORT_CHECK ORDER_RECORDED … sent=0` แทน
   - ครึ่ง "ส่งจริง" ได้บรรทัดของตัวเอง: `prompt_sent_console_line(pending, frame_bytes)` → `… PROMPT_SENT … bytes_out=<n>`
     ใช้ได้เฉพาะผู้เรียกที่ถือไบต์อยู่ในมือ (drain ท้าย `dispatch()` ของ chief) · **ยังไม่มีผู้เรียกใน `src/`** และมีเทสยืนยันด้วย AST ไม่ใช่ grep
2. **D-A2 — สามประโยคที่คอมมิตไว้เป็นเท็จ** วัดซ้ำเองบน `origin/main` ก่อนรับ: `_coerce_int` มีพื้นเป็น 0 ⇒ `TeleportCheck(0)` เคยถึงชื่อ refusal เสมอ (ชื่อผิดคือ `OUT_OF_FIELD`)
   - ชื่อใหม่ `CHECK_REFUSED_MARKER_ID_IS_ABSENT_SENTINEL` (0 = sentinel ของตาราง ไม่ใช่เลขที่ u16 แบกไม่ไหว) · `MARKER_ID_ABSENT_SENTINEL = 0`
   - แก้ประโยคเท็จให้เหลือประโยคแคบที่จริง: ที่เคยเรียกไม่ถึงคือ id **เกินเพดาน** และ id **ติดลบ**
   - ตารางปฏิเสธของประตูเพิ่ม `0` เข้าไป (ใบเดิมเลือก 70000/-1/0x10000/10**30 แล้วข้าม 0 พอดี)
   - ของจริงที่กระทบ: สคริปต์เดียวในคอร์ปัสที่เรียกชื่อนี้ (`t_telchk_lv.lua`) ส่ง `Trigger.Var1` ที่ยังไม่ผูก = ตกเคสนี้เป๊ะ
3. **D-A5 — recorder ที่เขียนแบบธรรมดาที่สุดทำประตูระเบิด** (`record` ไม่มี `return` → `None` → `TypeError` หลังบันทึกออร์เดอร์ไปแล้ว)
   `sink_stored_count()` ประกาศสัญญาไว้ที่เดียว · ประตู log `stored=unknown` และ **ยังพิมพ์บรรทัด ORDER_RECORDED** เพราะออร์เดอร์อยู่ใน sink จริง (ออร์เดอร์สดที่เงียบคือความเสียหายที่แย่กว่า)
4. **D-A3/D-A4 — มิวแทนต์ที่รอด** ตอนนี้ปักบรรทัดกับ literal ทั้งบรรทัด โดยใช้ marker 17 (ฉาก 126 ≠ id ตัวเอง จึงเห็นการสลับ marker/scene) + ปักค่าของ refusal ทุกชื่อกับ literal (รวม `CHECK_REFUSED_BAD_ARITY` ที่ D6 รอบก่อนตั้งไว้แล้วไม่มีอะไรกันการถอย)
5. **D6 ของ chief (`0432`) — id คนละโดเมนระหว่างประตูบันทึกกับประตูกิน**
   ตัดสินแล้ว: **id ที่บันทึกต้องเป็น id ที่คอนเนกชันพิสูจน์** · ออร์เดอร์ที่ลงด้วย context default `0` ไม่มีวันถูกเอคโค่กินได้ (dispatch กินด้วย `foundation.selected.id`) = "หน้าต่างที่ไปไหนไม่ได้" ของ R307
   ⇒ ประตูปฏิเสธด้วยชื่อ `CHECK_REFUSED_NO_CHARACTER_BOUND` และนับ แทนที่จะเปิดหน้าต่างเปล่า · เทสทั้งสองโมดูลผูก `player_context` เหมือนโปรดักชันแล้ว
6. ข้อล่างสองข้อ: log bad-value ใช้ `ascii()` แทน `%r` (อักขระนอก cp874 เคยฆ่าบรรทัดที่กำลังรายงานความผิดของสคริปต์เอง) · โมดูลเทส host door **collect เดี่ยวได้แล้ว** (คำสั่งที่โน้ตของ skip pin สั่งให้ซ้อมเอง เดิมตายที่ collection)

7. **คำขอของ Q (`0552`)** — `ScriptHost.teleport_check_sink` เคยเป็น attribute เขียนทับได้ ทั้งที่ฝั่ง namespace เป็น property อ่านอย่างเดียว
   `host.teleport_check_sink = other` สำเร็จเงียบ ๆ → namespace ยังเขียนใบเก่า → ผู้ dispatch อ่านใบใหม่ที่ว่างตลอดกาล = ออร์เดอร์หายทั้งเซสชันโดยไม่มี log
   ⇒ ทำเป็น **read-through property** ตามที่ Q เสนอ (4 บรรทัดแทน 4 บรรทัด ยังอยู่ในเพดาน 10 ของ COO `0242`) + เทสยืนยันว่า assign แล้วได้ `AttributeError`

## หลักฐาน (รอบนี้)
- `pytest tests/test_world_m2_teleport_check.py tests/test_world_m2_teleport_check_host_door.py` = **66 passed, 5 subtests** (ติดตั้ง lupa 2.8 ในคลาวด์โคลนรอบนี้จึงรันครบ ไม่ใช่ skip)
- `PYTHONPATH=src:tests pytest tests/test_script_lua_corpus.py tests/test_pytest_precondition_census.py` = **94 passed, 1403 subtests** (หมุดคอร์ปัส 2872/2599 ที่ `#1105` ขยับไว้ยังเขียวหลังเพิ่ม refusal ใหม่)
- skip pin `tests/test_world_m2_teleport_check_host_door.py` 7 → **9** (เพิ่มเทส "host ที่ไม่ผูกตัวละคร" และ "ประตูของ host สลับใบไม่ได้") · **ซ้อมจริงโดยถอน lupa ออก: `9 skipped`** และโมดูล collect เดี่ยวได้ (คำสั่งเดียวกันโดยไม่ตั้ง PYTHONPATH ก็ได้ 9 skipped)
- `pf_gate_preflight.py` = แดงหนึ่งแถวคือ `[skips]` ซึ่ง **ไม่ใช่ของคอมมิตรอบนี้**: วัดแล้ว `git diff origin/main 66f8b2c -- tests/ | grep -c "^+.*skip_unless_present"` = 1 เท่ากับที่หัวกิ่งวันนี้ = บรรทัด decorator ที่รอบก่อนเพิ่ม · ตัวเครื่องมือเคลียร์เฉพาะโมดูลที่ปักใน `design_skips` ไม่อ่าน `preconditions` (ที่ census เกรดจริง) · และบนเกตวินโดวส์โมดูลนี้ **ไม่ skip เลย** เพราะ `gate-windows.yml` บรรทัด 155 ติดตั้ง `lupa==2.8` และโมดูลไม่อยู่ใน `windows_gate_excluded_modules` — เขียนเป็นบรรทัดเดียวถึง chief ใน body ของ `#1105`
- **client-observable = ไม่มี ไม่อ้าง** · ไม่มีไบต์ถึง socket ในรอบนี้ · `runtime.py` ไม่ถูกแตะ
- TWO_SESSIONS_SAME_SCENE: sink เป็นของ host/คอนเนกชัน ไม่ใช่ของ process (เทสสอง host ยังอยู่) · รอบนี้เพิ่มด้วยว่า **ออร์เดอร์ผูกกับ id ที่คอนเนกชันพิสูจน์** สอง session ในฉากเดียวกันจึงกินเอคโค่ของกันไม่ได้ · โมดูลนี้ไม่เขียนอะไรลง world registry ของ LANE-A

## ที่ส่งต่อ
- **จดหมายถึง K**: `20260908_0422_LANE-A-TO-K-gt-body-gt309-line-1-token-renamed.md` — เนื้อใบ `GT-309` หมวด `HEADLESS_PROOF:` ต้องเปลี่ยนบรรทัดแรกเป็น `PROMPT_SENT … bytes_out=<n>` (ใบยังห้ามขึ้นรถบัสจนกว่าจุดเสียบ drain ของ chief จะเรียกบรรทัดนั้น)
- **บรรทัดเดียวถึง chief** (เขียนใน body ของ `#1105`): drain ท้าย `dispatch()` เรียก `world_m2_teleport_check.prompt_sent_console_line(pending, len(frame))` หลังจ่ายไบต์เข้าคิวส่ง และสร้าง `ScriptHost` ด้วย `player_context=PlayerContext(character_id=<id ที่คอนเนกชันพิสูจน์>)` มิฉะนั้นทุกออร์เดอร์จะถูกปฏิเสธด้วยชื่อ (เห็นในทาลลี ไม่เงียบ)

## รอบหน้าทำอะไร
1. ถ้า Q ตอบแล้ว: undraft `#1105` + marker → merge → วัด `HEADLESS_PROOF:` บน main แล้วส่ง `*-TO-K-headless-proof-*`
2. ผล pf-adversary ของรอบนี้ (สั่งที่นาที ~18) ถ้าคืนหลังปลดล็อก = งานแรกของรอบหน้า
3. M2 ต่อ: ปลายทาง marker ↔ เกาะ 2/3 (crosswalk) ยังไม่มีใบตอบ

SCOREBOARD: COMING | ยังไม่มีอะไรที่ผู้เล่นเห็นเพิ่มวันนี้ แต่คำสั่งเดินทางที่ถูกบันทึกไว้จะไม่ถูกยื่นเป็นหลักฐานว่า "ส่งแล้ว" อีก และออร์เดอร์ที่ไม่มีตัวละครจริงผูกอยู่ถูกปฏิเสธโดยมีชื่อ แทนที่จะเปิดหน้าต่างที่เอคโค่กินไม่ได้ | pirate-force-server#1105 (draft, รอ Q) commit a5dac6a
