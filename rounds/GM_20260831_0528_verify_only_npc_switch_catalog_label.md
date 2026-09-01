# รอบ `gm-20260831-0517` (2026-08-31T05:1x-05:3x+07:00) — verify-only, npc_switch_catalog.py 8180/8181 label เดียว

## ต้นรอบ

- `pf_bridge`/`pirate-force-server`: ไม่มี PR `[LANE-GM]` เปิดค้าง (open, รวม draft) ตอนต้นรอบ — orchestrator
  ยืนยันไว้ก่อนเรียกรอบนี้ (มีแค่ `[LANE-B] ... #360` เปิดอยู่ ไม่ใช่ของสาย GM ไม่แตะ) ยึดล็อกทันทีด้วย
  empty commit "round claim: gm-20260831-0517" แล้วเปิด draft PR: `pf_bridge#565`,
  `pirate-force-server#361`
- PR `[LANE-GM]` ล่าสุดของแต่ละ repo (`pf_bridge#561`, `pirate-force-server#357`, รอบ `jz4don`):
  `pull_request_read(method=get)` ยืนยัน `merged=true` ทั้งคู่ (ไม่ใช้ `list_pull_requests`'s `merged`
  field ที่รู้กันแล้วว่าไม่น่าเชื่อถือ) — งานรอบก่อนอยู่บน main จริง ไม่ต้อง cherry-pick กู้คืนอะไร

## กล่องจดหมาย

ไล่ `notes_to_chief/` หาใบที่จ่าหน้าถึง LANE-GM หรือเปิดโดย LANE-GM ที่ยังไม่มี `.CONSUMED.txt` (ตรวจทั้งสอง
รูปแบบชื่อไฟล์ consumed ที่ใช้จริงในโปรเจกต์นี้ — `<name>.md.CONSUMED.txt` และ `<name>.CONSUMED.txt`) —
**ไม่พบใบใหม่ที่ต้องบริโภครอบนี้** ใบล่าสุดที่แตะ LANE-GM ตรง (`0430_LANE-GM-STATUS-gmprobe-wired`,
`0245_COO-DECISION-gm042-owner-questions-npc-off-semantics-and-water-lantern-ids`) มี `.CONSUMED.txt`
ครบแล้วทั้งคู่ (backfill โดย chief รอบ `8skr91`/R255) heartbeat ล่าสุด `05:10:50` ต่างจากเวลารอบนี้
(`05:28`) ~17 นาที ปกติ

## สถานะ `RE-164`/`GT-164` (เรื่องหลักของ `PANYA-ORDER 0152`)

ตรวจ `CLIENT_RE_QUEUE.md#RE-164`/`GAME_TEST_QUEUE.md#GT-164` แล้ว **ไม่มีอะไรให้ต่อสายเพิ่มรอบนี้**:

- `GT-164` ปลด BLOCKED แล้วตั้งแต่รอบ `jz4don` (จุดเสียบ `/gmprobe <variant_id>` อยู่บน main แล้ว) เหลือแค่
  รอกะ1-A คลิกจริงในเซสชัน attended — ไม่ใช่งานที่ทำได้ในสภาพแวดล้อมรีโมตไม่มีจอของรอบนี้ (แม้จะเป็นสาย GM
  เอง ก็ไม่มี computer-use/attended session ให้เรียกในรอบนี้)
- `RE-164` suspect 1 (connection context) / 3 (current-UI object-key) / 4 (create path `0x007280D0`) ทั้งสาม
  ต้องใช้ disassembly ของไบนารีไคลเอนต์จริง (VA ที่อ้างเป็นของ client `.exe` ไม่ใช่ server source) — เป็นงาน
  RE lane ตามกฎ "ถ้าเป็นงานของ RE ไม่ใช่ของเรา เขียนใบขอแทนที่จะเดา" ใบ `RE-164` เปิดรออยู่แล้วจากรอบก่อน
  ไม่ต้องเปิดซ้ำ ไม่มีข้อมูลใหม่ให้เพิ่มในใบ

## สิ่งที่ทำรอบนี้ (เดียว เล็ก ปลอดภัย)

`pirate-force-server`'s `gm/npc_switch_catalog.py`: เติม docstring ป้าย `8180`/`8181` (Water Lantern x2)
ตาม `COO-DECISION 20260831_0245` ("ครั้งต่อไปที่แตะไฟล์นี้ ให้ป้ายว่า catalog-only ยังไม่พบแถว server-side")
— ไม่มีการเปลี่ยน logic (`is_gm_switchable_npc`/`npc_gm_name` เหมือนเดิมทุกประการ)

🔴 **พลาดแล้วแก้เอง**: ร่างแรกใส่ตัวอักษรจริงของ `s_NAME` (อักษรจีนดั้งเดิม) ลงในไฟล์ `.py` ตรง ๆ —
`test_gm_source_is_cp874_safe.py` fail ทันที (ตัวอักษรนั้นไม่มี mapping ใน cp874) แก้เป็นข้อความ ASCII
ชี้ไปที่ไฟล์ TSV data แทน ก่อน commit — ไม่ปล่อยของที่ทำให้ gate แดงหลุดออกไป (ตัวอย่างสดของทำไมกฎ
"commit/code ต้อง ASCII English only" มีไว้)

รายละเอียดเต็มอยู่ใน `pirate-force-server` PR body และ `docs/GM_LANE.md` รอบ `gm-20260831-0517`

## pf-adversary

diff เดียวคือ docstring 12 บรรทัดใหม่ ไม่มีการเปลี่ยน logic/ฟังก์ชัน/ทางแยกใด ๆ — ไม่มี Task/agent-launch
tool ในชุดเครื่องมือของรอบนี้เหมือนรอบก่อน ๆ ตรวจทานเองแทน: ไม่มี threat model ใหม่ที่ต้องตรวจ (ไม่มีการ
parse/serialize/dispatch อะไรใหม่) รันสวีตเต็มก่อน/หลังยืนยันจำนวนเทสไม่เปลี่ยน

## เช็คสวีต

- `pytest tests/ -q` เต็ม: **5661 passed**, 323 skipped, 9758 subtests passed, 0 failed เขียว(cloud sanity)
- `python3 tools/verify_hypothesis_ledger.py`: PASS entries=47 ไม่มี drift
- `python3 tools/verify_functional_coverage.py`: PASS domains=8 ไม่มี drift (8 domain ยังเปิดเหมือนเดิม
  ทุกตัว รอบนี้ไม่แตะ)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — รอบนี้ไม่มีจุดเสียบใหม่ที่ยิงได้จริง `GT-164` ยังรอกะ1-A คลิกจริงเหมือนเดิมทุกประการ (ปลด BLOCKED
ไปแล้วตั้งแต่รอบ `jz4don`) การเปลี่ยนแปลงรอบนี้คือ docstring/label ไฟล์เดียว ไม่กระทบพฤติกรรมรันไทม์ใด ๆ

## nonclaim

1. ไม่ได้ยิงเฟรมใด ๆ ใส่ client จริงรอบนี้ ไม่ได้เปิด client ไม่มีจอในสภาพแวดล้อมนี้
2. ไม่ได้ตัดสินหรือเดาคำตอบของ `RE-164` suspect ใดเลย — ยังคงเป็นใบเปิดรอ RE lane เหมือนเดิม
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`/
   `scenarios/combat_*.json` เลยรอบนี้ ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts` ไม่มีการประกาศ
   milestone จากผลที่ได้ด้วย GM
4. ป้าย 8180/8181 เป็น docstring เท่านั้น ไม่ได้เพิ่ม/ลด behavior ใด ๆ ทั้งสอง id ยังถูกมองว่า "เป็นหนึ่งใน 7"
   เหมือนเดิมทุกประการ (แค่ไม่ให้ใครอ่านแล้วเข้าใจผิดว่ามีแถว server-side ยืนยันแล้ว)
5. ไม่มี ASK-COO ใหม่รอบนี้ — ไม่มีอะไรที่ต้องการการตัดสินใจระดับเจ้าของ/COO

## PR

- `pf_bridge#565` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready + retitle)
- `pirate-force-server#361` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready + retitle + wake-gate commit)

— สาย GM รอบ `gm-20260831-0517`
