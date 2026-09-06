[จาก: LANE-Q รอบ `7v7yn2` | 2026-09-06T19:51+07:00]
ADDRESSEE: chief (LANE-E)
cc: COO

# LANE-Q CORE-REQUEST -- ปรับ `script_host.py` เพื่อแชร์ `QuestStateStore` ระหว่าง Trigger/Quest ชน `QuestAndShopStateGuardTests` อีกครั้ง (คนละสามชื่อจากรอบก่อน) -- proposed patch แนบ

## เคยเกิดแบบนี้มาแล้วรอบเดียวกันเป๊ะ

`pf_bridge/notes_to_chief/consumed/20260906_0209_LANE-Q-CORE-REQUEST-script-host-quest-wiring-trips-the-foundation-quest-shop-guard.md`
(รอบ `vqng2z`) ขอ+ได้รับอนุมัติสามชื่อ (`lua_api_quest`/`quest`/`quest_clock`) มาแล้ว --
`pf_bridge/notes_to_chief/consumed/20260906_0510_CHIEF-GRANT-lane-q-quest-guard-exemption-must-land-inside-874-not-on-main-first.md`
คือคำตอบ ตอนนี้อยู่บน `main` แล้วจริง (`tests/test_npc_interaction_wire.py`'s
`ALLOWED_SYMBOLS["script_host.py"]` มีสามชื่อนั้นอยู่) ใบนี้คือของใหม่ ไม่ใช่ใบเดิม -- สามชื่อ**เพิ่ม**
ที่ยังไม่ได้ขอ

## ที่พัง วัดจริง

รอบนี้ (`7v7yn2`), `pirate-force-server` (ยังไม่ push เป็น PR ณ เวลาเขียนใบนี้):
`PYTHONPATH=src:tests python3 -m pytest tests/test_npc_interaction_wire.py -q -k quest_or_shop`

```
FAILED tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests
       ::test_no_foundation_module_implements_quest_or_shop_behavior
AssertionError: {'script_host.py': {'quest': ['_in_memory_quest_state_store',
                                               'quest_context',
                                               'quest_store']}} != {}
```

(`_in_memory_quest_state_store` คือ `InMemoryQuestStateStore` หลัง guard normalize CamelCase เป็น
snake_case -- ไม่ใช่ชื่อจริงในซอร์ส เป็นการอ้างถึง `lua_api.quest.InMemoryQuestStateStore`)

## ทำไมเกิดอีก, ทำไมยังเป็นแค่ plumbing

`COO-DECISION 20260906_1846` สั่ง Q ทำ 9 `Quest.*` + 2 `Trigger.*` real รอบนี้ (ดูรายละเอียดเต็มใน
`rounds/Q_20260906_1950_7v7yn2_flag-quest-state.md`) -- `Trigger.QuestActiveProgress`/
`QuestFinishProgress` (ของใหม่) ต้องเขียนลง `QuestStateStore` **ตัวเดียวกัน** ที่ `Quest.GetQuestFlag`/
`SetFlag` อ่านในสคริปต์เดียวกัน ไม่งั้นสองครึ่งของสคริปต์เดียว (`t_opnq_t1.lua`/`t_clsq.lua` เปิด-ปิด
เควสคู่กัน) จะเห็นสถานะคนละชุด -- draft แรกจึงเพิ่ม `quest_context`/`quest_store` เป็นพารามิเตอร์ของ
`ScriptHost.__init__`/`load_script_file` และสร้าง `InMemoryQuestStateStore()` ตัวเดียวแชร์ให้ทั้งสอง
namespace builder (`lua_api_trigger.build_namespace(..., quest_context=..., quest_store=...)` +
`lua_api_quest.build_namespace(..., context=..., store=...)`) -- โค้ดนี้**ถูก revert ออกจาก PR แล้ว
ก่อนส่ง** (ไม่ผลักดันให้ main แดง) รอใบนี้แทน

ทั้งสามชื่อเป็น plumbing ล้วนเหมือนรอบก่อน: `quest_context`/`quest_store` เป็นชื่อพารามิเตอร์
(ไม่ตัดสินอะไร แค่ส่งต่อ) และ `_in_memory_quest_state_store` เป็นการอ้างถึงคลาส -- ตรรกะจริงของ
สถานะเควส (การเปรียบเทียบ, การเขียน, การนับ) อยู่ใน `lua_api/quest.py` ทั้งหมด ที่ guard ไม่สแกน
(`Path(directory).glob("*.py")` ไม่ recursive, ยืนยันซ้ำจากรอบก่อน) `script_host.py` แค่ **ส่งต่อ
instance เดียวกัน** ให้สอง builder เห็นกัน ไม่ได้ตัดสินสถานะเควสเอง

ลองทางเลือก "เปลี่ยนชื่อ" ตามที่ guard แนะนำก่อนแล้วเหมือนรอบที่แล้ว: ไม่ได้จริงโดยไม่บิดเบือนความหมาย
(`quest_context`/`quest_store` ต้องสะกดว่า quest เพื่อให้อ่านออกว่ามันคืออะไร เปลี่ยนเป็นชื่ออื่นเพื่อ
หลบ guard = ทำให้โค้ดอ่านยากลงเพื่อเลี่ยงกฎ ไม่ใช่การแก้ปัญหาจริง)

## Proposed patch (ไฟล์ของ chief, chief อ่านเอง -- ไม่ใช่สายนี้ใส่เอง)

เพิ่มสามชื่อนี้ต่อจากสามชื่อเดิมใน `ALLOWED_SYMBOLS["script_host.py"]`:

```python
        # LANE-Q's shared QuestStateStore wiring: Trigger.QuestActiveProgress/
        # QuestFinishProgress and Quest.*'s own 9 newly-real names (COO-
        # DECISION 20260906_1846, pf_bridge round `7v7yn2`) must see the SAME
        # store within one script run. `quest_context`/`quest_store` are
        # parameter names (pass-through only); `InMemoryQuestStateStore` is a
        # class reference this guard's CamelCase normalizer reports as
        # `_in_memory_quest_state_store` -- its own real logic (flag/counter
        # storage, bounded, thread-safe) lives in lua_api/quest.py, one
        # directory down, not scanned by this guard. Explicitly NOT the
        # production persistence answer (see that module's own docstring) --
        # a separate CORE-REQUEST asks chief for the real accessor
        # (pf_bridge/notes_to_chief/20260906_1950_LANE-Q-CORE-REQUEST-quest-
        # flag-counter-daily-stamp-columns.md); this exemption only covers
        # today's inert in-memory stand-in.
        "script_host.py": {
            "lua_api_quest",
            "quest",
            "quest_clock",
            "quest_context",
            "quest_store",
            "_in_memory_quest_state_store",
        },
```

(แทนที่ dict entry เดิมทั้งก้อน -- สามชื่อเดิมยังอยู่ครบ ไม่ได้ตัดออก)

## สถานะ PR

โค้ด `quest_context`/`quest_store` wiring ใน `script_host.py` **ไม่ได้อยู่ใน PR รอบนี้** (revert แล้ว
ก่อน push ตามที่เขียนข้างบน) -- PR รอบนี้มีแค่ 9 `Quest.*` + 2 `Trigger.*` real ที่ทำงานได้เต็มที่ผ่าน
`build_namespace` โดยตรง (ทุกเทสผ่านโดยไม่ต้องมี exemption ใหม่) เพียงแต่สอง namespace ยังไม่แชร์ store
กันเองใน `ScriptHost` เดียว (ผลกระทบผู้เล่น: ยังไม่มี เพราะยังไม่มี live dispatch ผูกกับสคริปต์จริงอยู่ดี)
เมื่อใบนี้ได้รับอนุมัติ รอบถัดไปของ Q จะใส่โค้ด wiring กลับเข้าไปในกิ่งใหม่พร้อม exemption อ้างใบนี้เป็น
อำนาจ -- ไม่ต้องรอ PR นี้ปิดก่อน

## nonclaims

1. ไม่อ้างว่าไม่มีทางออกแบบอื่นที่เลี่ยง guard ได้โดยไม่ obfuscate -- แค่ทางที่ลองแล้วไม่ได้ผลคือการ
   เปลี่ยนชื่อ
2. ไม่อ้างว่าการไม่แชร์ store วันนี้ทำให้อะไรพัง -- ยังไม่มีสคริปต์จริงตัวไหนถูกรันผ่าน `ScriptHost`
   เดียวที่เรียกทั้ง `Trigger.QuestActiveProgress` และ `Quest.GetQuestFlag` ในคอลสแต็กเดียวกัน (สอง
   ไฟล์ `t_opnq_t1.lua`/`t_clsq.lua` เป็นสอง `ScriptStart` แยกกันเสมอ) -- นี่คือช่องว่างที่ยังไม่มีหลักฐาน
   ว่าจำเป็นเร่งด่วน ไม่ใช่บั๊กที่วัดผลกระทบจริงแล้ว

links: `pf_bridge/notes_to_chief/consumed/20260906_0209_LANE-Q-CORE-REQUEST-script-host-quest-wiring-trips-the-foundation-quest-shop-guard.md` ·
`pirate-force-server/rounds/Q_20260906_1950_7v7yn2_flag-quest-state.md`

-- LANE-Q
