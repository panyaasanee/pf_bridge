[สาย GM รอบ `qgmm2s` · 2026-08-31T22:25+07:00 (`TZ=Asia/Bangkok date`)]

# รอบ `qgmm2s` — rule F เรียกจริง: ไล่ (ก)(ข)(ค)(ง) สดทั้งสี่ข้อ ไม่มีข้อใดให้หยิบ · ไม่มีโค้ดเปลี่ยน

## หนึ่งบรรทัด

รอบก่อน (`a10g3c`) เป็นรอบว่างรอบแรกและ flag ไว้ว่าถ้ารอบถัดไปว่างอีกต้องหยิบ (ก)-(ง) จริงจัง —
รอบนี้ไล่ทั้งสี่ข้อสดใหม่ (ลึกกว่ารอบก่อนหน้าทุกรอบ: ตรวจโค้ดจริงทีละบรรทัด ไม่ใช่แค่ grep TODO)
พบว่า **ทั้งสี่ข้อว่างจริง** ไม่ใช่การเชื่อบันทึกเก่า — รายละเอียดข้างล่าง

## 0. round-lock

- ต้นรอบ: `search_pull_requests(is:open, in:title [LANE-GM])` ทั้งสอง repo คืน 0 — ไม่มี PR ค้าง
- ตรวจชะตารอบก่อน (`a10g3c`) ด้วย `pull_request_read(method=get)`: `pf_bridge#632` `merged=true`,
  `pirate-force-server#414` `merged=true` — งานอยู่บน `main` แล้วทั้งคู่ ไม่มีอะไรต้อง cherry-pick
- `pf_bridge` อยู่หลัง `origin/main` 1 commit (sync ไฟล์ allowlist จาก Windows bridge) — fast-forward
  แล้วก่อนเริ่มงาน (`git merge --ff-only origin/main`, ไม่มี conflict)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีอยู่จริง
- heartbeat `_BRIDGE_HEARTBEAT.txt` ล่าสุด `22:08:01+07:00` เทียบต้นรอบ `22:17+07:00` ห่าง 9 นาที ผ่าน
- ยึดล็อกด้วย empty commit ("round claim: quirky-goodall-2seah3" / "round claim:
  magical-mendel-2seah3" — ชื่อสาขาต่างกันสองฝั่ง จึงใช้ session-id ที่ derive จากแต่ละสาขาเองสำหรับ
  commit message ทั้งสองฝั่ง แต่ใช้ tag รวม `qgmm2s` สำหรับไฟล์รอบนี้/จดหมาย) เปิด draft
  `pf_bridge#638` / `pirate-force-server#418`

## 1. กล่องจดหมาย (ข้อ 1-2 ของโปรโตคอล)

`for f in $(grep -rl "ADDRESSEE: LANE-GM" notes_to_chief/*.md); do [ -f "${f}.CONSUMED.txt" ] ||
echo UNCONSUMED: $f; done` → ว่างเปล่า ทุกใบที่จ่าหน้าถึงสายนี้บริโภคแล้วจากรอบก่อน

`ls notes_to_chief/*COO-DECISION*.md | sort | tail -5` → ใบล่าสุดยังเป็น `20260831_1843` เดิม
ไม่มี COO-DECISION ใหม่กว่านั้นเลย (ตรวจ `ls -t notes_to_chief/*.md | head` ด้วย — ใบล่าสุดสุดคือ
`20260831_2202_CODEX-CHECKPOINT-P05-COMBAT-LIFECYCLE.md` ไม่เกี่ยวกับสายนี้)

`CLIENT_RE_QUEUE.md`: `RE-172 ACTOR-BASIC-ATTR-LOGIN-OBSERVABLE-SOURCE-001` ยัง
`[OPEN — assigned สาย GM]` เหมือนเดิม — `COO-DECISION 1843` สั่งห้ามเปิดใบใหม่ถามซ้ำจนกว่าจะมีผล
ยังไม่ถึงเงื่อนไขนั้น ไม่เปิดใบใหม่

## 2. คิวของสายตัวเอง (ข้อ 3)

`GT-172` (READY จากรอบ `2uud3t`) — อ่านซ้ำหัวใบเต็ม: เนื้อหายังตรงจริง ("เงื่อนไข PR merge เป็นจริง
แล้ว") ไม่มีอะไรล้าสมัยให้แก้ ไม่มีหัวใบ `GT-*` อื่นที่สายนี้เปิดค้างเงื่อนไข

## 3. ไล่ตัวเลือกกฎ F ทั้งสี่ข้อสดใหม่ (ลึกกว่ารอบก่อน — อ่านโค้ดจริง ไม่ใช่แค่เชื่อบันทึก)

### (ก) backlog pre-approved ในเขตตัวเอง
ค้น `notes_to_chief/` หา CORE-REQUEST-GM-0xx ที่ chief ตอบแล้วว่า "wired" แต่สายนี้ยังไม่ได้ทำส่วน
ตัวเอง — ไม่พบ (ใบล่าสุดที่เกี่ยวคือ `20260830_2100_CHIEF-REPLY-CORE-REQUEST-GM-042-*` และ
`20260831_0204_CHIEF-REPLY-*GM-042-deferred-roster-filter-structurally-inert*` — ทั้งคู่บอกว่า
"deferred, ไม่ทำ" ไม่ใช่ของค้างให้สายนี้ทำต่อ) **ไม่มี**

### (ข) ใบ RE/STATIC ที่ตอบได้จากซอร์ส/factpack ที่มีอยู่แล้ว
ตรวจ `docs/GM_LANE.md` หา follow-up ที่ทำได้แบบ static: พบข้อเดียวที่เข้าเกณฑ์ —
`TeleportVital`'s target field order "ไม่ได้ verify กับ 132 เฟรม `A2_STATIC_OPEN` จริง"
(`external/PF_FIELD_VALIDATION.tsv`: `TeleportVital W/R` แถวละ 132 candidate frames, 126 capture
files) ค้นหา raw capture corpus ที่จะใช้ re-derive: `find / -iname "*capture*" -type d`,
`find /home/user -iname "*.bin" -o -iname "*wire_capture*"` → **ค้นแล้ว: ไม่เจอ** ไฟล์ capture
ดิบ 126 ไฟล์ที่ตารางอ้างถึงอยู่นอกเครื่องนี้ (bridge/Windows-side เท่านั้น) — cloud session นี้ไม่มี
สิทธิ์เข้าถึง ทำต่อไม่ได้จริง เข้าเกณฑ์ capture-territory เดียวกับ item/npc/spawn **ไม่มีของที่ตอบ
ได้จาก static source ที่มีอยู่ในเครื่องนี้จริง ๆ**

### (ค) เขียน/ปรับใบเทสในคิว GAME_TEST_QUEUE.md เฉพาะหัวข้อที่สายนี้เป็นเจ้าของ
ไล่ทุกหัวใบ `GT-*` ที่สายนี้เปิด (`101/103/107/127/128/133/141/164/172` ตามที่รอบ `a10g3c` เคยไล่
ไว้ + ตรวจ `GT-106-R2` ที่เพิ่งปิดเป็น PASS): ทุกหัวใบตรงกับสถานะจริงแล้ว ไม่มีอะไรล้าสมัย
ไม่เปิดหัวใบใหม่เพราะไม่มีความสามารถใหม่ที่ built-แต่-ยัง-ไม่มีหัวใบ (cross-scene warp มีหัวใบ
`GT-172` ครอบอยู่แล้วตั้งแต่ก่อนหน้านี้) **ไม่มีอะไรให้แก้จริง**

### (ง) technical debt ที่ pf-adversary เคยชี้ในเขต gm/
ไม่มี agent `pf-adversary` แยกในอิมเมจนี้ (`ToolSearch` คำค้น "pf-adversary agent" ไม่พบ) — ทำ
self-review เข้มกว่ารอบก่อนแทนที่จะ grep TODO เฉย ๆ:
- `grep TODO/FIXME/XXX/HACK src/pirateforce_foundation/gm/*.py` = 2 hit เดิม ยืนยันซ้ำว่าเป็น false
  positive จริง (`\uXXXX` ใน docstring, "HARD LOCK, NOT A TODO" ใน `teleport_wire.py`)
- อ่าน `warp_executor.py`/`say_wire.py`/`commands.py` เต็มไฟล์ (ไม่ใช่แค่ grep) ตาม docstring ที่เล่า
  ประวัติ args-shape gap 4 รอบติด (blacklist → broad-except → str/bytes guard → dict-key gap →
  `type(args) is not tuple` แก้เด็ดขาด) — ยืนยันด้วย `grep -n "type(args) is not tuple"` ว่าทั้งสาม
  ไฟล์ใช้ guard เดียวกันจริงครบทุกจุดเรียก ไม่มีจุดหลุด
- ตรวจฟังก์ชันใหม่สุด `make_warp_teleport_frame_with_target` (เพิ่มจาก `COO-DECISION 1441`) มี
  `_require_args_tuple` + `is_known_scene_id` guard ครบ และมี unit test ปกคลุมแล้ว
  (`tests/test_gm_warp_executor.py` บรรทัด 301-380: happy path, scene 17 X=834/Y=-598 ตรงกับ
  GT-106-R2, refusal path, malformed-args path)
- `grep -n "\.args\["  gm/chat_command.py gm/chat_command_action.py` = 0 hit — ไม่มีจุด index
  `command.args` ตรง ๆ นอกเขตที่มี guard แล้ว (chat_command_action.py เรียกผ่าน
  `warp_executor`/`say_wire`'s hardened builders เท่านั้น)
**สรุป: ไม่มี technical debt ใหม่ ของเดิมทั้งหมดถูกปิดแล้วจริง ตรวจซ้ำเข้มกว่ารอบก่อนแล้วได้ผล
เดียวกัน ไม่ใช่การเชื่อบันทึกเก่า**

## สรุปกฎ F

ไล่ครบ (ก)(ข)(ค)(ง) สดทุกข้อ ลึกกว่ารอบก่อนหน้าทุกรอบ (อ่านซอร์สเต็มไฟล์ ไม่ใช่แค่ grep, ค้นหา
capture corpus จริงทั้งเครื่อง, ตรวจ test coverage ของฟังก์ชันใหม่ล่าสุด) — **ไม่มีข้อใดมีงานให้หยิบ
จริง** ทุกจุดบล็อกตรงตามเหตุที่ COO/RE ระบุไว้แล้วอย่างชัดเจน (ไม่ใช่การเดา):

- `attr_wire.py` (`/lv`): รอ `RE-172` (สาย RE, ยังเปิด) — `COO-DECISION 1843` ห้ามเปิดใบใหม่จนกว่า
  จะมีผล
- `say_wire.py` (`say`): ล็อกโดย `COO-DECISION 20260829_0041` ตรง ๆ — สายนี้เคาะเองไม่ได้
- `item`/`npc`/`spawn`: รอเฟรมจริงจาก attended session (capture territory จริง cloud ทำไม่ได้) —
  รวมถึง `TeleportVital` target field-order re-verify ที่ตอนแรกดูเหมือนทำได้แบบ static แต่ raw
  capture corpus ไม่ได้อยู่ในเครื่องนี้ (ค้นแล้ว: ไม่เจอ) จึงเป็น capture territory เหมือนกัน

## เขียว

`python3 -m pytest tests/test_gm_*.py -q` (HEAD ปัจจุบันหลัง fast-forward, ก่อนแก้อะไร — ไม่มีอะไร
ให้แก้จริงรอบนี้): ผลอยู่ในจดหมายสถานะ

## nonclaim

1. ไม่อ้างว่า `RE-172` ตอบแล้ว — ยังเปิดอยู่จริง ตรวจสดรอบนี้ด้วย grep ตรง ๆ
2. ไม่แก้ fail-closed gate ใด ๆ (`attr_wire`/`say_wire`) รอบนี้ — ทั้งสองยังปิดเหมือนเดิมทุกไบต์
3. ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts.json` ไม่มีการประกาศ milestone จากผลใด ๆ รอบนี้
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json` เลย
5. ไม่มีจุดเสียบใหม่ให้ผู้เทสลองรอบนี้ — `GT-172` (READY) ยังเป็นรายการเดียวที่พร้อมยิงจากคิว attended
6. การตรวจ (ก)-(ง) รอบนี้ลึกกว่ารอบก่อนจริง (อ่านซอร์สเต็มไฟล์ 3 ไฟล์, ค้นหา capture corpus ทั้ง
   filesystem, ตรวจ test coverage ของฟังก์ชันใหม่) แต่ผลลัพธ์ยังเป็น "ไม่มีงานให้หยิบ" เหมือนเดิม —
   ไม่ใช่การเลือกไม่ตรวจให้ลึกเพื่อประหยัดเวลา

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — ไม่มีการแก้โค้ดในเขตของสายนี้เลยรอบนี้ `GT-172` (READY จากรอบก่อน) ยังเป็นทางเดียวที่
ผู้เทส attended ทำได้ ไม่ต่างจากเมื่อวาน

## PR

- `pf_bridge#638` (draft ต้นรอบ → ready ท้ายรอบนี้)
- `pirate-force-server#418` (draft ต้นรอบ → ready ท้ายรอบนี้ + wake-gate commit ท้ายรอบ)

— สาย GM รอบ `qgmm2s`
