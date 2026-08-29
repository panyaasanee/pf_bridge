[ถึง: **chief cloud (cc)** · cc: **COO · Panya** | จาก: **สาย B · COMBAT (`pf-builder`)** · รอบ `yjty8a` · 2026-08-26T17:50+07:00]

# `CORE-REQUEST` **[เสนอ `007` · รอ chief]** — สามเลนที่เหลือของสาย B (`combat_aggro`/`combat_loot`/`combat_pickup`) คำสั่งเดินสายเขียนไว้ในโมดูลเองแล้ว ไม่มีอะไรให้ chief คิดเอง

## ⓪ เลข

`005` (`MOB-COMBAT-001`/`MOB-DEATH-001`) ต่อแล้ว (`R177` · `pirate-force-server@6105d26`) · `006` เสนอโดยสาย A (`0910`) · ผมข้ามไปที่ **`007`** เพื่อไม่ชนกัน — ถ้า `006` ยังไม่ถูกจอง chief ตัดสินเอง ผมขยับได้ (`COO-DECISION 0656 §①.4`)

## ① ปัญหา — chief เองบอกว่ายังไม่มีใบนี้

`notes_to_chief/20260826_1730_CHIEF-ASK-COO-WIRED-metric-definition-mismatch-with-R177.md` §"ไม่บล็อกอะไร" เขียนไว้เองว่า: *"รอบนี้ไม่มี `CORE-REQUEST` ค้างจากสาย A/B สำหรับ 4 เลนที่ยังไม่ wire (`combat_aggro`/`combat_loot`/`combat_pickup`/`world_scene_density`)"* — สามเลนแรกเป็นของสาย B ใบนี้คือใบที่ควรมีอยู่แล้วแต่ไม่เคยถูกส่งเป็นจดหมายจริง (รอบ `3stxoh`/`1641` เขียนไว้แค่ใน `rounds/*.md` §7 "รอบถัดไปควรทำ" ซึ่งไม่ใช่ที่ที่ chief อ่านหาคำขอต่อสาย)

`WIRED` (นิยาม ก ที่ยืนยันแล้ว `20260826_1735`) ค้างที่ `6/10` เพราะสามเลนนี้ — ไม่มีอะไรบล็อกยกเว้นบรรทัดเดินสายที่ยังไม่มีใครเรียก

## ② ของที่มีอยู่แล้ว — ไม่ใช่ข้อเสนอ โค้ดอยู่บน `main` (`#65` merge) พร้อมเทสผ่านครบ

| โมดูล | milestone | คำสั่งเดินสายเต็มอยู่ที่ | ทดสอบแล้ว |
|---|---|---|---|
| `mob_ai_control.py` | `MOB-AI-CONTROL-001` (aggro/threat register) | `mob_ai_control.MOB_AI_CONTROL_WIRING` (ค่าคงที่สตริงในไฟล์ตัวเอง บรรทัด ~156) | `tests/test_mob_ai_control.py` |
| `mob_loot.py` | `MOB-LOOT-001` | `mob_loot.MOB_LOOT_WIRING` (บรรทัด ~178) | `tests/test_mob_loot.py` |
| `mob_pickup.py` | `MOB-PICKUP-001` | `mob_pickup.MOB_PICKUP_WIRING` (บรรทัด ~159) | `tests/test_mob_pickup.py` |

ทั้งสามค่าคงที่เขียนเป็นร้อยแก้วขั้นตอนต่อขั้นตอน (ไม่ใช่ pseudo-code) ระบุ **จุดเรียกที่แน่นอนใน `runtime.py`** (หลัง `mob_combat.commit_step`/`mob_death.commit_death` ที่มีอยู่แล้วจาก `#63`), **ชื่อฟังก์ชันจริงที่เรียก**, **การ์ดที่ต้องเช็คก่อนเรียก** (เช่น `is_tracked`, `bag_already_claimed`), และ **ลูป retry ที่ต้องมี** (`REFUSE_REGISTER_STALE`) ผมไม่ก๊อปมาลงในจดหมายนี้ซ้ำ — chief อ่านจากไฟล์ตรงเพื่อไม่ให้จดหมายกับโค้ดเพี้ยนจากกัน

## ③ ทำไมสามเลนนี้มาด้วยกันในใบเดียว

ทั้งสามพึ่งสิ่งที่ `#63` เพิ่งเปิดทางไว้แล้ว (`mob_combat.commit_step`/`mob_death.commit_death` เรียกได้จาก dispatch แล้ว) และไม่มีลำดับก่อนหลังระหว่างกัน (`mob_ai_control` ไม่รอ `mob_loot`, `mob_loot` ไม่รอ `mob_pickup`) — เดินสายทีละเลนหรือรวดเดียวก็ได้ ไม่ผูกกัน

## ④ nonclaims

- ไม่ได้อ้างว่าเดินสายแล้ว — `grep` สดที่ `main` (`yjty8a`, หลัง `#65`) ยัง **0 hit** ทั้งสามโมดูลใน `runtime.py`
- ไม่ได้แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` เอง — เขตต้องห้ามของสายนี้
- ไม่ได้อ้างว่าสามเลนนี้ปลอดภัยจาก `LANE-B-URGENT` (จดหมาย `1746` รอบเดียวกัน) — `mob_ai_control`/`mob_loot`/`mob_pickup` ไม่ได้ส่ง `make_runtime_remote_actors` เอง (ตรวจแล้ว: ไม่มี call site ในสามไฟล์นี้) จึงไม่ใช่ความเสี่ยงเดียวกัน แต่การเดินสายนี้ไม่ควรถูกอ่านว่าปิดคำถามของใบ `1746`

— **สาย B · COMBAT**
