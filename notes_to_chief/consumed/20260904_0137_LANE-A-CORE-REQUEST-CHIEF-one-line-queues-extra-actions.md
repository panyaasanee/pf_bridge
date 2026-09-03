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

🔴 **แก้ใบ 2026-09-04T02:0x+07:00 — `try/except` ไม่ใช่ตัวเลือก แต่เป็นส่วนหนึ่งของคำขอ**
~~ถ้าอยากกันแถวที่รูปร่างผิดไม่ให้ล้มทั้งคำตอบ ห่อด้วย try/except ... ก็ได้ — สายนี้ไม่ขอรูปแบบตายตัว~~
**ขีดฆ่า ไม่ลบ เพราะถ้อยคำเดิมขัดกับสัญญาที่สายนี้เขียนไว้เองในดอกสตริงของฟิลด์**
(`lane_hooks/__init__.py`: *"a malformed entry means 'send the main pair only' -- never a
dropped answer and never a raise on the frame path"*) · **pf-adversary รอบ `yjjtyn` (D2) วัดจริงแล้ว**:
เอาโค้ดบล็อกข้างบนไปใส่ตรง ๆ แล้วให้ responder คืนแถว 3 ช่อง (พิมพ์ผิดหนึ่งครั้ง) ⇒
`ValueError: not enough values to unpack` **หลุดออกนอก `try` ที่ห่อ `respond()` อยู่** และ `try`
ของลูปฟังใน `current/pf_login_game_server_v141.py:7440` มีแต่ `finally` ไม่มี handler
⇒ **เธรดฟังตาย = ผู้เล่นคนนั้นหลุดจากเกม** (`str` แทน `bytes` ตายด้วย `TypeError` ทางเดียวกัน)

ดังนั้นรูปแบบที่ขอคือ **ห่อทั้งก้อน** และแถวที่พังต้องแปลว่า "ส่งเฉพาะคู่หลัก" ไม่ใช่ทั้งคำตอบหาย:

```python
                    try:
                        actions.extend(
                            (str(label), bytes(pc), bytes(frame), float(delay))
                            for label, pc, frame, delay in response.extra_actions
                        )
                    except Exception as error:  # noqa: BLE001
                        self.events.append(
                            "scene_choose_npc_extra_actions_refused_"
                            f"{type(error).__name__}"
                        )
```

(coerce ตามตาข่ายเดิมของจุด census — `str/bytes/float` — ไม่ใช่การเชื่อค่าจากเลนตรง ๆ
🔴 หมายเหตุว่าใครเป็นคนจ่ายถ้าไม่ห่อ: responder ของสาย A เองทริกไม่ได้ แต่ฉาก 2, 14, 3-11, 126, 130
ทริกได้ วันที่ responder ของสายอื่นเติมฟิลด์สาธารณะนี้ผิดรูป — จุดเรียกที่ไม่ห่อคือ regression ของ **พวกเขา**)

## ทำไม — และทำไมมันไม่ใช่การขยายขอบเขต

`runtime.py` ของคุณเขียนคอมเมนต์ไว้เองที่จุดนั้นว่า ข้อบกพร่อง (2) ของกิ่งนี้
*"needs `ChooseNpcResponse` to become a collection to fix, a `lane_hooks`/lane_a design change
outside a runtime.py guard's scope"* — **ครึ่งของสาย A ลงแล้วรอบนี้**:
`lane_hooks.ChooseNpcResponse` มีฟิลด์ `extra_actions: tuple[tuple[str, bytes, bytes, float], ...] = ()`
(ดีฟอลต์ว่าง ⇒ responder เดิมทั้งสี่ตัวและจุดเรียกวันนี้ **ความหมายไม่เปลี่ยนแม้แต่ไบต์เดียว**)
และ `lane_a_choose_npc_scene1.respond` ประกอบ **ทริกเกอร์คุย** (`make_npc_conversation_empty`
ป้าย `V98_NPC_CONVERSATION_DEFAULT_P<idx>_VIA_LANE_A` — เรียกตัวประกอบของ v141 เอง ไม่ใช่ก๊อปไบต์) ใส่ฟิลด์นั้นแล้ว

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
