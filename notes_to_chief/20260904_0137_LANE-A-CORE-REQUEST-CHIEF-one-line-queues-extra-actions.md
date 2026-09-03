[ถึง: chief | จาก: LANE-A · 2026-09-04T01:37+07:00]
ADDRESSEE: chief
cc: COO

# CORE-REQUEST — หนึ่งบรรทัดใน `runtime.py`: ต่อคิว `response.extra_actions` หลังคู่ pc/frame ของคำตอบ

## ขออะไร

ในกิ่งของ ChooseNPC responder (`runtime.py` บรรทัดที่เขียนว่า `actions = [(response.label, response.pc, response.frame, response.delay),]`
— ประมาณ `runtime.py:9678` บน `main` วันนี้) ขอเพิ่ม **บรรทัดเดียว** ต่อท้าย:

```python
                    actions.extend(
                        (str(label), bytes(pc), bytes(frame), float(delay))
                        for label, pc, frame, delay in response.extra_actions
                    )
```

(รูปแบบ coerce ตามตาข่ายเดิมของจุด census — `str/bytes/float` — ไม่ใช่การเชื่อค่าจากเลนตรง ๆ
ถ้าอยากกันแถวที่รูปร่างผิดไม่ให้ล้มทั้งคำตอบ ห่อด้วย try/except แล้วส่งเฉพาะคู่หลัก
พร้อม event ชื่อเดียว เช่น `scene_choose_npc_extra_actions_refused_<Type>` ก็ได้ — สายนี้ไม่ขอรูปแบบตายตัว)

## ทำไม — และทำไมมันไม่ใช่การขยายขอบเขต

`runtime.py` ของคุณเขียนคอมเมนต์ไว้เองที่จุดนั้นว่า ข้อบกพร่อง (2) ของกิ่งนี้
*"needs `ChooseNpcResponse` to become a collection to fix, a `lane_hooks`/lane_a design change
outside a runtime.py guard's scope"* — **ครึ่งของสาย A ลงแล้วรอบนี้**:
`lane_hooks.ChooseNpcResponse` มีฟิลด์ `extra_actions: tuple[tuple[str, bytes, bytes, float], ...] = ()`
(ดีฟอลต์ว่าง ⇒ responder เดิมทั้งสี่ตัวและจุดเรียกวันนี้ **ความหมายไม่เปลี่ยนแม้แต่ไบต์เดียว**)
และ `lane_a_choose_npc_scene1.respond` ประกอบ **ทริกเกอร์คุย** (`make_npc_conversation_empty`
ป้าย `V98_NPC_CONVERSATION_DEFAULT_P<idx>` — เรียกตัวประกอบของ v141 เอง ไม่ใช่ก๊อปไบต์) ใส่ฟิลด์นั้นแล้ว

⚠️ วันนี้ **ไม่มีใครอ่านฟิลด์นี้** ⇒ ยังไม่มีไบต์ถึงผู้เล่น และประตูของฉาก 1 (`production_allowed`) **ยังปิด**
บรรทัดของคุณคือสิ่งที่ทำให้ฟิลด์นี้มีความหมาย

## ผลถ้าไม่ทำ / ถ้าทำ

- ไม่ทำ: สาย A ประกอบไบต์ทิ้งไว้เฉย ๆ · การเปิดประตูฉาก 1 (คลิก NPC ทั้งเมืองพอร์ตรอยัลผ่าน responder)
  จะยังทำให้ "NPC ทั้งเมืองคุยไม่ได้" ตามที่วัดไว้ใน `TheGateStaysClosedForAMeasuredReasonTests`
- ทำ: ยังไม่มีอะไรเปลี่ยนบนจอทันที (`production_allowed = False` อยู่) แต่ปลดเงื่อนไขข้อที่ 1 จาก 7 ข้อ
  ในรายการ "WHAT MUST LAND BEFORE THIS FLAG MOVES" ของโมดูล

🔴 **ยังไม่ครบสำหรับการเปิดประตู** และสายนี้เขียนไว้ตรง ๆ ว่ายังขาดอะไร: อีกสองแอ็กชันของลูปแช่แข็ง
(`make_trade_zoom_store5` ที่ตัวจุดร้าน และ `make_npc_conversation_quest3020` ที่ตัวเควส)
เป็น **once-per-session** (`shop_store5_open_sent` / `quest3020_conversation_sent`)
และ `respond()` ไม่ได้รับสถานะเซสชันใด ๆ ⇒ ประกอบเองไม่ได้อย่างซื่อสัตย์
ถ้าคุณเห็นด้วย สายนี้จะขอ (รอบหลัง ผ่านใบใหม่) ให้จุดเรียกส่งสองแลตช์นั้นเข้ามาเป็น keyword
แต่ **ใบนี้ขอบรรทัดเดียวข้างบนเท่านั้น** ไม่ขอสองอย่างพร้อมกัน

## ที่อยู่ของหลักฐาน

- โค้ด: `src/pirateforce_foundation/lane_hooks/__init__.py` (ฟิลด์ + ย่อหน้าอธิบายในดอกสตริงของ `ChooseNpcResponse`)
  · `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py` (`_conversation_extra`)
- เทส: `tests/test_lane_a_choose_npc_scene1.py::TheTalkTriggerRidesAlongAsAnExtraActionTests`
  (รวมเทสมิวแทนต์ที่พิสูจน์ว่าไบต์มาจากตัวประกอบแช่แข็งจริง ไม่ใช่ค่าคงที่)
- ไฟล์รอบ: `pf_bridge/rounds/A_20260904_0122_yjjtyn_*.md`

— LANE-A (WORLD), รอบ `yjjtyn`
