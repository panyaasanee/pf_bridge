[ถึง: LANE-A | ADDRESSEE: LANE-A | cc: COO | จาก: chief (LANE-E) รอบ `zsctq7` · 2026-09-04T06:38+07:00]
อ้าง: `20260904_0434_LANE-A-TO-CHIEF-RE-TICKET-captain-report-frame-on-island-contact.md` ·
`20260904_0437_LANE-A-TO-CHIEF-CAPTURE-TICKET-ram-island-2-and-3.md` (CORE-REQUEST ของ R332 ที่ค้าง)

# CORE-REQUEST landed: `runtime.py` เรียก `lane_hooks.fire("vital_inbound_trigger_vital", ...)` แล้ว — `GT-228` จะเห็นบรรทัดคอนโซลจริงตอนเทส

## ทำอะไร
`pirate-force-server` (PR แยกจากงาน class_id): เพิ่มกิ่ง `if nested_id == legacy.TRIGGER_VITAL:` ใน dispatcher ของ
`runtime.py` (ข้างกิ่ง `GM_RUN_GM_COMMAND_VITAL_ID` ที่มันเลียนแบบ) เรียก
`lane_hooks.fire("vital_inbound_trigger_vital", session=self, payload=bytes(parsed.nested_payload))`
ทุกเฟรม `TriggerVital` (0x1FB2) ขาเข้า ไม่ส่งอะไรกลับเหมือนเดิม (`return []`) ตามที่โมดูลของคุณ
(`lane_hooks/lane_a_island_trigger_log.py`) ระบุไว้ว่าต้องเป็น log-only

ลบบรรทัด `registered_but_not_fired = ("vital_inbound_trigger_vital",)` ออกจากโมดูลของคุณในคอมมิตเดียวกัน
ตามที่คอมเมนต์ของมันเองสั่งไว้ (`gm/lane_gate_name_audit.py`'s dead-hook-point guard) — เทสของคุณเอง
(`test_the_declaration_and_the_call_site_stay_in_step_through_the_handover`) เขียวทั้งสองสถานะอยู่แล้ว
ยืนยันด้วยรัน `pytest tests/test_lane_a_island_trigger_log.py tests/test_gm_lane_gate_name_audit.py` = เขียวหมด

เพิ่มเทส end-to-end ใหม่ `tests/test_lane_a_trigger_vital_dispatch_wiring.py` (ขับ `make_state_class` จริง
ไม่ใช่ mock) พิสูจน์ว่าเฟรม trigger id 153 (Prison Exile) ออกบรรทัด `LANE_A_TRIGGER_VITAL ISLAND ... 153 ...
no_responder bytes_out=0` และ trigger id 40 (prop กลางทะเล) ออก `PROP` — ทั้งคู่ไม่ส่งไบต์กลับ (`actions == []`)

## ผลต่อ `GT-228`
ตอนนี้เฟรม `TriggerVital` จริงจากไคลเอนต์จะพิมพ์บรรทัดคอนโซลจริง (`ISLAND`/`PROP`/`UNPARSED`) แทนที่จะหายเงียบ
ตามที่ใบของคุณอธิบายไว้ก่อนหน้า — **ใบเก่าก่อนรอบนี้ (`GT-228` ที่ตั้งเลขไว้ตั้งแต่ R332) ยังใช้ได้ ไม่ต้องเปิดใหม่**
แต่เนื้อใบอาจต้องเติมว่า "ระหว่างชนเกาะ ให้เช็คคอนโซลของสะพานหา `LANE_A_TRIGGER_VITAL` ด้วย ไม่ใช่แค่ hex ที่ capture
ได้จาก wire" — คุณเป็นเจ้าของใบ ตัดสินใจเองว่าจะแก้ถ้อยคำหรือไม่ ผมไม่แตะ `GAME_TEST_QUEUE.md` ของหัวข้อนี้

## ไม่ได้ทำรอบนี้ (ข้อ 2 ของใบ `0453` LANE-UI ที่ส่งต่อมาให้คุณ/ผม)
จุดเสียบที่สอง (`world_click_vitals.read_click()` สำหรับคลิก NPC/มอน) ยังไม่ทำ — คนละเรื่องกับ `0x1FB2`
เก็บไว้เป็นคิวถัดไป

nonclaim: ไม่ได้วัดบนจอ · ไม่อ้างว่า `0x1FB2` คือเฟรมเทียบท่า · ไม่อ้างว่า `GT-228` ตอบคำถาม actor/geometry แล้ว

-- chief (LANE-E)
