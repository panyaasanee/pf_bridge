# รอบ LANE-GM `dao2gd` — 2026-08-30T21:23+07:00

## สรุปหนึ่งบรรทัด

ไม่มีขั้นต่อสายที่ปลดล็อกได้จริงรอบนี้ (GM-042 ยังติดที่ chief, `npc`/`item`/`lv` ยังรอ CORE-REQUEST call
site, `spawn` ปิดถาวรแล้ว) → อ่าน `gm/item_catalog.py` + `gm/scene_catalog.py` และเทสคู่กันทั้งไฟล์แทน
พบและแก้ 1 defect จริง (`item_max_stack` โยน `KeyError` เปล่าไม่บอกสาเหตุ) + เพิ่มเทส pin พฤติกรรมเดิมที่
ไม่เคยมีเทสคุม (4 scene id ที่ตารางของ client เองไม่มีชื่อ) รวม 6 เทสใหม่ ไม่มีการต่อสายรันไทม์ใด ๆ

## ล็อกรอบ

- ตรวจสอบมาก่อนแล้ว (โดยผู้สั่งงาน): ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo, รอบ GM ก่อนหน้า
  (`pirate-force-server#329`/`pf_bridge#524`, session `nbihci`) `merged=true` ทั้งคู่
- fetch `origin/main` สดทั้งสอง repo ก่อนแตกกิ่ง: พบว่า origin/main เดินหน้าไปแล้วตั้งแต่ผู้สั่งงานตรวจ
  (`pirate-force-server` `561cecd`→`aa5ba78` merge #330 LANE-E, `pf_bridge` `d78b1a2`→`f678957` merge
  #528) → `git reset --hard origin/main` ทับกิ่งเดิมก่อนแตกใหม่ (กิ่งยังไม่มี commit ของตัวเองตอนนั้น
  ปลอดภัย) แล้ว commit เปล่า "round claim: dao2gd" push สำเร็จทั้งคู่
- เปิด draft PR: `pirate-force-server#333`, `pf_bridge#529` ทั้งคู่มี `PF-AUTOMERGE: v4`
- `list_pull_requests state=open` ทั้งสอง repo ตอนเปิด PR คืนค่าว่างเปล่า (ไม่มี `[LANE-E]`/PR อื่นค้าง —
  #330 ที่ผู้สั่งงานเห็นว่าเปิดอยู่ merge ไปแล้วระหว่างนั้น) → ไม่ชนล็อกใคร

## กล่องจดหมาย

พบจดหมายที่ยังไม่บริโภค 1 ใบ ตรงกับที่ผู้สั่งงานสแกนไว้แล้ว:
`notes_to_chief/20260830_2100_CHIEF-REPLY-CORE-REQUEST-GM-042-store-plus-write-point-deferred-filter-
wiring-too-risky-partial-read.md` — chief อ่าน `gm_npc_toggle_recompose.py`/`mob_scene_recompose.py`/
จุดเรียก `recompose_frames` ทั้งสามใน `runtime.py` ครบแล้ว แต่**ตัดสินใจไม่สร้าง**ทั้ง state store,
จุดเขียน, และตัวกรอง roster รอบนั้น เพราะ (ก) สร้างแค่ store+เขียนโดยไม่มีตัวกรองจะทำให้
`npc_toggle_would_recompose` อ่านผิดความจริง และ (ข) ตัวกรอง roster แตะ fail-closed path ของ
`require_ledger_for_recompose`/`_unconsulted_rows` ที่ chief ยังอ่านไม่ครบพอจะมั่นใจ — **GM-042 ยังเปิด
ไม่มีโค้ดเปลี่ยนจากใบนี้เลย**

อ่านครบแล้ว (ตามที่ผู้สั่งงานทำไว้) แต่ใบนี้เป็นงานฝั่ง chief (`runtime.py`/`mob_scene_recompose.py`)
ไม่ใช่เขตเขียนของสาย GM (`gm/` เท่านั้น) — ไม่มีอะไรใหม่ในเขตของสาย GM ให้ต่อยอดจากใบนี้รอบนี้ วางบันทึก
สถานะไว้ในจดหมายรอบนี้ (`LANE-GM-STATUS`) + วาง `.CONSUMED.txt` + copy ไป `notes_to_chief/consumed/`
ตามกฎ B ไม่ลบต้นฉบับ

ไม่พบไฟล์ index/queue ของ CORE-REQUEST ที่ยังเปิดอยู่ใน pf_bridge (ค้นด้วย `ls`/`grep` คำว่า
index/queue/core-request-log — ไม่มีไฟล์แบบนั้นจริง) → ไม่ได้สร้างขึ้นใหม่ตามกฎห้ามเดา

## งานที่ทำ

อ่าน `gm/item_catalog.py`, `gm/scene_catalog.py`, `gm/npc_switch_catalog.py`, `gm/commands.py`,
`gm/chat_command_action.py` (ทั้งไฟล์ 1903 บรรทัด) และไฟล์เทสคู่กันทั้งหมด เพื่อยืนยันว่าไม่มีขั้นที่ยัง
ไม่เสร็จซึ่งไม่ต้องพึ่ง CORE-REQUEST ที่ยังไม่ตอบ — สรุปว่า GM-001/GM-004 พื้นฐานเสร็จแล้ว, GM-003 ทุก
คำสั่งเป็น parse+log อย่างเดียวเหมือนเดิมและรอ call site จาก chief, GM-002 (0x51E9 raw bytes) รอ RE พบ
2 ช่องว่างจริงในเขตของตัวเอง:

**1. `item_catalog.item_max_stack` โยน `KeyError` เปล่า** — `item_max_stack(99999999, category="misc")`
เดิมโยน `KeyError('99999999')` ตรงจาก dict lookup โดยไม่บอกว่า category ไหน ต่างจาก `item_name`/
`is_known_item` ในไฟล์เดียวกันที่โยนข้อความชัดเจนเสมอ (ตรวจสดด้วย python ก่อนแก้ ไม่ใช่เดา) แก้โดยห่อ
lookup เดียว (`item_catalog.py:170-186`) ด้วย try/except แล้วโยน `KeyError` ใหม่ที่บอกทั้ง item_id และ
category — ไม่กระทบพฤติกรรมกรณี id ที่มีจริง (มีเทสยืนยัน) `item_max_stack` **ไม่มี production caller**
เลยตอนนี้ (grep ทั้ง repo เจอแค่ในไฟล์เทส ตรงกับ docstring เดิมของโมดูลว่าเป็น "GM-042 prep") ⇒ ความเสี่ยง
ศูนย์ต่อ live path

**2. scene id ที่ตารางของ client เองไม่มีชื่อ ไม่เคยมีเทสคุม** — `gm_scene_name_tip.tsv` แถว 13/137/138/141
มีทั้ง `s_SCENE_NAME` และ `s_GM_SCENE_NAME` ว่างเปล่าในตารางต้นฉบับของ client เอง (ไม่ใช่บั๊กจากการ parse
ของโมดูลนี้ — ตรวจตรงจากไฟล์ tsv ดิบ) `is_known_scene_id(13)` เป็น `True` และ `gm_scene_name(13)` คืน
`""` ซึ่งไม่เคยมีเทสจับสภาวะนี้มาก่อน (เทสเดิมมีแค่ id จริง 1/2/3 กับ id ที่ไม่มีแถวเลย 123456 — ขาดสภาวะที่
สาม "มีแถวแต่ชื่อว่าง") เพิ่มเทส pin พฤติกรรมนี้ทั้งใน `scene_catalog.py` เองและใน
`commands.describe_warp_target` ชั้นบน (คืน `""` ไม่ใช่ `None` สำหรับ id เหล่านี้ — ผู้เรียกต้องไม่อ่าน `""`
ว่า "ฉากไม่รู้จัก" เพราะสิทธิ์ warp ตัดสินที่ `login_scene_admission`/`world_scene_travel` ไม่ใช่ที่ hint นี้)
ไม่มีการแก้ source ทั้งสองไฟล์ — เป็นเทสบันทึกพฤติกรรมเดิมล้วน ๆ

## ทดสอบ

`pytest tests/ -k "gm_" -q` บน `pirate-force-server`: **1052 passed, 476 subtests passed**, 0 failed —
รันทั้งก่อนและหลัง apply fix ผลตรงกัน ไม่มี regression (จาก 1046/473 ก่อนรอบนี้ เพิ่ม 6 เทสใหม่ของรอบนี้เอง)

## self-review (adversarial)

- ค้น ToolSearch หา Agent/Task tool ชนิด `pf-adversary` ก่อนสรุปว่าไม่มี — ไม่พบจริง (สถานการณ์เดียวกับที่
  รอบ `opr2xd` บันทึกไว้ใน `GM_20260830_1924_item_catalog_prep.md`) ⇒ ทำ self-critique เข้มงวดแทนการเรียก
  subagent จริง บันทึกไว้ตรงนี้แทนที่จะอ้างว่าได้เรียกแล้ว
- grep หา production caller ของ `item_max_stack` ทั้ง repo ก่อนสรุปว่า "ความเสี่ยงศูนย์" — พบเฉพาะไฟล์เทส
  จริง ไม่ได้เดา
- ตรวจ 4 scene id ว่างตรงจากไฟล์ tsv ดิบด้วย python สด (ไม่ใช่จำจากที่อื่น) ก่อนเขียนเทส
- ตรวจว่า try/except ใหม่ใน `item_max_stack` ไม่กลืน `KeyError` ที่มาจากสาเหตุอื่น: จุดเดียวที่ dict lookup
  เกิดขึ้นคือ `_BY_CATEGORY[category][item_id]` และ `category` ผ่าน `_validate_category()` มาก่อนแล้ว (ไม่
  โยน KeyError จากจุดนั้น) ⇒ except ที่เพิ่มดักเฉพาะกรณี item_id ไม่มีจริงเท่านั้น ไม่มีการกลืน error อื่น
- รัน `pytest tests/ -k "gm_"` เต็มชุดทั้งก่อนและหลังแก้ ไม่ใช่แค่ไฟล์ที่แก้ตรง ๆ เพื่อจับ regression ข้ามไฟล์

## ยังไม่ได้พิสูจน์ / ค้าง

- `CORE-REQUEST-GM-042` ยังเปิด — รอ chief มีเวลาต่อจาก `_unconsulted_rows`/`require_ledger_for_recompose`
  ให้ครบตามที่ระบุไว้ในจดหมายของ chief เอง (ไม่ใช่ของสาย GM ต่อได้เอง)
- `pf-adversary` subagent tool ไม่มีให้เรียกในเซสชันนี้ (รอบที่สองติดต่อกันที่พบสภาวะนี้ หลัง `opr2xd`) —
  ควรแจ้งเจ้าของว่าอาจเป็นปัญหาระดับ tooling ของ session ไม่ใช่เฉพาะรอบเดียว
- heartbeat `_BRIDGE_HEARTBEAT.txt` อ่านค่าล่าสุด `2026-08-30T18:26:02+07:00` ต่างจากเวลารอบนี้
  (`21:23`) ~2h57m — แย่ลงกว่า R248 ที่วัดไว้ 2h34m ต่อเนื่องมา 2 รอบแล้วว่าค้าง/ไม่ขยับ ควรแจ้งเจ้าของ
  ว่า pf_git_sync บนสะพานอาจหยุดทำงานจริง ไม่ใช่แค่ช้า (เวลาที่ใช้ในรอบนี้คำนวณจาก `TZ=Asia/Bangkok date`
  ตรงตามกฎ ไม่ได้คำนวณเอง)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี — รอบนี้ไม่มีอะไรใหม่ให้ผู้เทสหน้าจอเกมเห็น การเปลี่ยนแปลงทั้งหมดคือข้อความ error ของฟังก์ชันเตรียม
งานที่ยังไม่ถูกเรียกจาก production path ใด ๆ (`item_catalog.item_max_stack`) และเทสที่ pin พฤติกรรมเดิม
ของ `scene_catalog`/`commands.describe_warp_target` ที่มีอยู่แล้ว ไม่มีการเปลี่ยนพฤติกรรมโค้ดที่สังเกตได้
จากภายนอกเลยแม้แต่จุดเดียว

## nonclaim

ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริง ไม่มีบรรทัดใดของ GM ไปถึงไวร์เพิ่มขึ้นจากรอบนี้ —
`warp`/`npc`/`item`/`lv`/`spawn`/`say` ทั้งหมดยังทำงานเหมือนเดิมทุกประการ ไม่แตะ `runtime.py`/`app.py`/
`pf_login_game_server_v141.py` และไม่แตะ `scenarios/world_*.json`/`scenarios/combat_*.json` ของสายอื่น
เลยตลอดรอบ วัดผลจาก `pytest`/`grep`/การอ่าน source ที่ commit แล้วบน `origin/main` เท่านั้น ไม่มีการใช้ GM
ข้ามขั้นตอนใดเพราะไม่มีการทดสอบไคลเอนต์จริงในรอบนี้เลย

— สาย GM รอบ `dao2gd`
