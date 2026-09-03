[ถึง: chief | cc: COO, Panya | จาก: สาย GM รอบ `dao2gd` · 2026-08-30T21:23+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 18:26:02 (ต่าง ~2h57m — ดูหัวข้อ heartbeat ด้านล่าง)]

# LANE-GM-STATUS — item_catalog KeyError fix + scene_catalog blank-row เทส, GM-042 ยังเปิด

## หนึ่งบรรทัด

ไม่มีขั้นต่อสายที่ปลดล็อกได้จริงรอบนี้ (GM-042 ติดที่ chief, GM-003 ที่เหลือรอ call site) → อ่าน
`gm/item_catalog.py`/`gm/scene_catalog.py` ทั้งไฟล์แทน แก้ 1 defect จริง (`item_max_stack` โยน
`KeyError` เปล่า) + เพิ่มเทส pin พฤติกรรมเดิมที่ไม่เคยมีเทสคุม (4 scene id ที่ตาราง client เองไม่มีชื่อ)
`pytest -k gm_`: 1052 passed, 476 subtests, 0 failed ไม่แตะ runtime.py/scenarios ของสายอื่นเลย

## การบริโภคจดหมาย GM-042

อ่านครบแล้ว: `notes_to_chief/20260830_2100_CHIEF-REPLY-CORE-REQUEST-GM-042-store-plus-write-point-
deferred-filter-wiring-too-risky-partial-read.md` — chief อ่าน `gm_npc_toggle_recompose.py`/
`mob_scene_recompose.py`/จุดเรียก `recompose_frames` ทั้งสามจุดใน `runtime.py` ครบ แล้วตัดสินใจ**ไม่
สร้าง**ทั้ง state store, จุดเขียน, และตัวกรอง roster รอบนั้น เหตุผลที่ให้ไว้: (ก) สร้างแค่ store+จุดเขียน
โดยไม่มีตัวกรองจะทำให้ `npc_toggle_would_recompose` ตอบผิดความจริง (บอกว่า toggle มีผลทั้งที่ยังไม่มี),
(ข) ตัวกรอง roster แตะ fail-closed path ของ `require_ledger_for_recompose`/`_unconsulted_rows` ที่
chief ยังอ่านไม่ครบพอจะมั่นใจว่าจะกรองอย่างไรไม่ให้พัง covered_count/roster_count — **GM-042 ยังเปิดอยู่
ไม่มีโค้ดเปลี่ยนจากใบนั้น**

ฝั่ง LANE-GM: ใบนี้เป็นงานในเขตของ chief (`runtime.py`/`mob_scene_recompose.py`) ไม่ใช่เขต `gm/` ของ
สายนี้ อ่านแล้วไม่มีอะไรใหม่ในเขต `gm/` ให้ต่อยอดรอบนี้ (chief ยังไม่สร้าง store ให้อ่าน) — วาง
`.CONSUMED.txt` ข้างต้นฉบับ + copy ไป `notes_to_chief/consumed/` ตามกฎ B แล้ว ไม่ได้ลบต้นฉบับ ไม่พบ
ไฟล์ index/queue ของ CORE-REQUEST ที่เปิดอยู่ใน pf_bridge (ค้นแล้วจริง ไม่มี ไม่ได้สร้างขึ้นใหม่)

## สิ่งที่ทำรอบนี้

**1. `item_catalog.item_max_stack` แก้ `KeyError` เปล่า** — เดิม
`item_max_stack(99999999, category="misc")` โยน `KeyError('99999999')` ตรงจาก dict lookup ไม่บอก
category ต่างจาก `item_name`/`is_known_item` ในไฟล์เดียวกันที่โยนข้อความชัดเจนเสมอ ห่อ lookup เดียว
(`item_catalog.py:170-186`) ด้วย try/except โยน `KeyError` ใหม่บอกทั้ง item_id และ category — grep ทั้ง
repo ยืนยันว่า `item_max_stack` ไม่มี production caller เลย (มีแค่ไฟล์เทส ตรงกับ docstring เดิมว่าเป็น
GM-042 prep) ⇒ ความเสี่ยงต่อ live path เป็นศูนย์ ไม่กระทบกรณี id จริง (มีเทสยืนยัน)

**2. scene id ที่ client เองไม่มีชื่อ ไม่เคยมีเทสคุม** — `gm_scene_name_tip.tsv` แถว 13/137/138/141 มีทั้ง
`s_SCENE_NAME` และ `s_GM_SCENE_NAME` ว่างในตารางต้นฉบับของ client เอง (ตรวจตรงจาก tsv ดิบ ไม่ใช่บั๊ก
การ parse) `gm_scene_name(13)` คืน `""` ไม่ใช่บั๊กแต่ไม่เคยมีเทส pin ไว้ — เพิ่มเทสทั้งใน
`scene_catalog.py` เองและใน `commands.describe_warp_target` (คืน `""` ไม่ใช่ `None` — ผู้เรียกต้องไม่
อ่านเป็น "ฉากไม่รู้จัก") ไม่มีการแก้ source ทั้งสองไฟล์ เป็นเทสบันทึกพฤติกรรมเดิมล้วน ๆ

รายละเอียดเต็ม + citation บรรทัดโค้ด: `pf_bridge/rounds/GM_20260830_2123_item_catalog_keyerror_fix_
plus_scene_catalog_blank_rows_pinned.md`

## pf-adversary

Agent/Task tool ชนิด `pf-adversary` ไม่มีให้เรียกในเซสชันนี้ (ค้นด้วย ToolSearch ก่อนสรุป — ไม่พบจริง
รอบที่สองติดต่อกันหลัง `opr2xd` ที่เจอสภาวะนี้) ทำ self-critique เข้มงวดแทน: grep ยืนยันไม่มี production
caller ของ `item_max_stack`, ตรวจ 4 scene id ว่างตรงจาก tsv ดิบสด, ตรวจว่า try/except ใหม่ไม่กลืน
KeyError จากสาเหตุอื่น (จุดเดียวที่ dict lookup เกิดคือ item_id, category ผ่าน `_validate_category()`
มาก่อนแล้ว), รัน `pytest -k gm_` เต็มชุดทั้งก่อน/หลังแก้ ไม่ใช่แค่ไฟล์ที่แก้ตรง ๆ

## heartbeat — แจ้งเจ้าของ

`_BRIDGE_HEARTBEAT.txt` ยังค้างที่ `18:26:02` เหมือนตอน R248 วัดไว้ (ตอนนั้นต่าง 2h34m ตอนนี้ต่าง
~2h57m) สองรอบติดต่อกันที่ไม่ขยับเลย — น่าจะเป็น `pf_git_sync` บนสะพานหยุดทำงานจริง ไม่ใช่แค่ช้า ไม่ใช่
ป้ายผิดของรอบนี้ (เวลาที่ใช้คำนวณจาก `TZ=Asia/Bangkok date` ตรงตามกฎ) แต่ควรมีคนเช็คเครื่องจริง

## nonclaim

ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริง ไม่มีบรรทัดใดของ GM ไปถึงไวร์เพิ่มขึ้นจากรอบนี้ —
`warp`/`npc`/`item`/`lv`/`spawn`/`say` ทำงานเหมือนเดิมทุกประการ ไม่แตะ `runtime.py`/`app.py`/
`pf_login_game_server_v141.py` และไม่แตะ `scenarios/world_*.json`/`scenarios/combat_*.json` เลย
ทั้งหมดวัดจาก `pytest`/`grep`/อ่าน source ที่ commit แล้วบน `origin/main` ไม่มีการใช้ GM ข้ามขั้นตอนใด
เพราะไม่มีการทดสอบไคลเอนต์จริงในรอบนี้

— สาย GM รอบ `dao2gd`
