round k1hsp0
start 2026-09-09T15:06+07:00
claim

# LANE-B round k1hsp0

HEAD ที่บูต: origin/main ba64381 (merge ตอนจบรอบ) · เลขจ็อบ: ไม่ได้ใช้ (ใบนี้ไม่ใช่ attended)
เวลาเทียบ heartbeat: `_BRIDGE_HEARTBEAT.txt` ล่าสุด 15:48:02 · เวลาผม 15:55 · ห่าง 7 นาที ไม่ค้าง

## ทำอะไร (pirate-force-server#1196 · claude/gifted-clarke-k1hsp0 · sha 3383187)

1. `src/pirateforce_foundation/mob_identity_sign.py` (docstring เท่านั้น) — งาน จ.1 ทาง 3
   ตรวจแล้วพบว่า `mob_wire_identity`/เพดานต่อฉาก/เทสยืนยันแถวศูนย์ของ `open_register`
   ตรงกับ ledger — ทั้งสามเงื่อนไขของ `COO-DECISION 20260908_1642` **มีอยู่แล้วบน main**
   ก่อนตัดกิ่งรอบนี้ด้วยซ้ำ (คอมมิตของรอบก่อนหน้า) ไม่ได้ทำซ้ำ
   เหลืออย่างเดียวที่ยังไม่ตรง: ใบสั่งขอ "สี่ผู้อ่าน" (เพิ่ม census) แต่โค้ด/เทสเดิมยืนที่
   "สามผู้อ่าน" พร้อมเหตุผลว่า census re-sort ตามระยะจากผู้เล่นทุกครั้งที่เรียก
   (`field_mobs.nearest_first` + `world_population_*.census_order` ทั้ง 17 ไฟล์) ไม่ใช้ลำดับ placement
   ตรวจซ้ำเองแล้วจริง จึงแก้ docstring ให้ฝัง "increasing order by placement is the contract,
   not a side effect" + บันทึกเหตุผลที่ปฏิเสธผู้อ่านคนที่สี่ ไม่ได้กุเพิ่มเพื่อให้ตรงใบสั่ง
   ไม่มีผลต่อพฤติกรรม

2. `src/pirateforce_foundation/lane_hooks/lane_b_mob_ai_tick.py` +
   `tests/test_lane_b_mob_ai_tick.py` — งานกฎ `1545` (R4 identity · 0 ห้าม)
   `LANE_B_MOB_AI_TICK_WIRING` (ข้อความ "วางลง runtime.py" ที่สายนี้ส่งให้ chief) ยังผูก
   player identity ด้วยสูตรมือ `((identity_hi & 0xFFFFFFFF) << 32) | (identity_lo & 0xFFFFFFFF)`
   ซึ่งเป็นรูปแบบเดียวกับที่ชุดกวาด "R4 beat 0" กำจัดไปแล้วทุกที่ (0 ต้องไม่ชนกับ actor id จริง)
   `runtime.py` เองใช้ `selected_actor_identity()` ที่ปลอดภัยแล้วทั้งสามจุดเรียกจริง (รอบ LANE-E
   ก่อนหน้าแก้ไปแล้ว diff รอบนี้กับ `runtime.py` ว่างเปล่า) แต่สตริงนี้เป็น "ต้นฉบับให้ก๊อป" —
   ถ้ามีการ re-paste/rebase บล็อกนั้นในอนาคตจากสตริงเดิม จะย้อนกลับไปชน identity=0 แบบไม่มี
   เทสจับ (`test_player_identity_one_dispenser.py` เป็น AST guard ที่อ่านแค่ `runtime.py` จริง
   ไม่เห็นสตริงนี้) แก้ให้เรียก `selected_actor_identity(...)` แทน + เพิ่มเทส
   `test_the_wiring_line_never_hand_composes_the_player_identity_again`
   (ยืนยันมือ: revert สูตรเดิมแล้วเทสแดง แก้กลับแล้วเทสเขียว)

## ADVERSARY
สั่ง pf-adversary ก่อนเปิด PR (ไม่ pending): **CLEAN** ไม่มีข้อวิกฤต
ตรวจซ้ำอิสระ: census re-sort จริงทุกไฟล์ฉาก · อ่านโค้ดจริงของ `selected_actor_identity`
(เรียก `identity_is_drawn` ปฏิเสธ 0 จริง ไม่ใช่เชื่อชื่อฟังก์ชันเฉย ๆ) · reproduce เอง (revert สูตร
เดิม → เทสแดง → แก้กลับ → เขียว) · full suite ที่คอมมิตนี้ 15511 passed / 647 skipped / 0 failed
ข้อสังเกตไม่บล็อก: ประโยค "the four agreed" ในไฟล์เดิม (มีอยู่ก่อนรอบนี้ ไม่ได้แก้) ค้างไม่ตรงกับ
"THREE readers" ที่แก้ใหม่ — ทิ้งไว้ให้รอบหน้าเก็บ ไม่ใช่ของรอบนี้

## ขยับ NOW/M ข้อไหน
- จ.1 ทาง 3: ยืนยันว่าเข้าเงื่อนไขครบแล้วจริง (ไม่ใช่ของใหม่) + แก้ docstring ให้ตรงกับสภาพจริง
- กฎ `1545` (R4 identity · 0 ห้าม): ปิดช่องโหว่แฝงในสตริง wiring ที่ส่งให้ chief — โค้ดจริงปลอดภัย
  อยู่แล้ว แต่ต้นฉบับสำหรับ re-paste เคยไม่ปลอดภัย
- จ.2 (พลิกทีละฉาก): ยังค้างจนประตูทะเบียน A ลง main — ไม่ได้แตะรอบนี้ ตรวจแล้วยังไม่ลง
- GT-223 (ของพื้น/มอนตายไม่รอด reconnect): **ไม่ได้แตะ** ไม่ใช่ของกฎ 1545 ต้นตอจริงอยู่ที่
  `mob_death_persistence.py`/`mob_drop_presence.py` (ไม่ได้อ่านลึก) เป็นของรอบหน้า

## nonclaims
ไม่ได้พิสูจน์/แก้ root cause ของ GT-223 (ground-drop persistence) · ไม่ได้ยืนยันว่าประตูทะเบียน A
ลง main แล้วหรือยัง (ตรวจผิวเผินจาก NOW.md เท่านั้น) · ไม่ได้รัน `pytest tests/` เต็มรอบด้วยตัวเอง
ใช้ผลจาก pf-adversary (15511 passed/647 skipped/0 failed) แทน

## รอบหน้าทำอะไร
1. เช็คว่าประตูทะเบียน A ลง main หรือยัง — ลงแล้ว ⇒ จ.2 พลิกทีละฉาก + ใบ GT ตามลำดับเดิม
   ยังไม่ลง ⇒ งานสำรอง (`## งานสำรอง` ใน `prompts/LANE-B.md`) หรือ root cause ของ GT-223
2. เก็บประโยค "the four agreed" ที่ค้างใน `mob_identity_sign.py` (adversary ชี้ ไม่บล็อก)

SCOREBOARD: STUCK | ปิดช่องโหว่แฝงที่จะทำให้ identity=0 กลับมาชนกับ actor จริงถ้ามีคน re-paste บล็อก wiring ในอนาคต — ผู้เล่นยังไม่เห็นอะไรต่างวันนี้เพราะโค้ดจริงปลอดภัยอยู่แล้ว งานนี้ปิดความเสี่ยงแฝงในต้นฉบับที่ยังไม่เคยถูกใช้ผิด | pirate-force-server#1196 (adversary CLEAN, marker ติดแล้ว) - sha 3383187 - 731 passed/3 skipped (targeted) + 15511 passed/647 skipped/0 failed (full, adversary run)
