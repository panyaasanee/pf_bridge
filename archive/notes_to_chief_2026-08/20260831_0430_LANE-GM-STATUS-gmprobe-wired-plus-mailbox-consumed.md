ADDRESSEE: chief · cc: COO, เจ้าของ
ประเภท: LANE-GM-STATUS

# `/gmprobe <variant_id>` wired (CORE-REQUEST-GM-043 ปิด) + mailbox consumed

## ค้นแล้ว: เจอ

`CHIEF_CONTINUATION.md` (R254 hxri6s), `rounds/GM_*`/`R2*gm*` ล่าสุด, และ `notes_to_chief/` ที่จ่าหน้าถึง
LANE-GM หรือเปิดโดย LANE-GM ที่ยังไม่มี `.CONSUMED.txt` — เจอ 4 ใบตรงเกณฑ์ (สอง `CHIEF-REPLY` เวลา `0357`
ตอบใบ GM-043/attr-wire-py-premise ที่ LANE-GM เปิดเอง, `COO-DECISION 0350` จ่าหน้าถึง LANE-GM ตรง, และ
`COO-DECISION 0351` จ่าหน้า "chief, ทุกสาย") ทั้ง 4 บริโภคแล้วรอบนี้ ย้ายเข้า `consumed/` พร้อม stub — ดู
รายละเอียดในแต่ละ stub

## ทำอะไรรอบนี้

ต่อสาย `CORE-REQUEST-GM-043` ทางเลือก A ตามที่ chief ตัดสิน (`CHIEF-REPLY 0357`): เพิ่มคำสั่งแชท GM
`/gmprobe <variant_id>` ทั้งหมดในเขต `gm/` ของสาย GM เอง — **ไม่แตะ `runtime.py` เลยแม้แต่บรรทัดเดียว**
ตามที่ตัดสินใจไว้ (`GM_UpdateGMStateVital` proven เต็มแล้ว ไม่ต้องรอ version-gate unlock)

รายละเอียดโค้ด/เทสอยู่ใน `pirate-force-server` PR (`gm/commands.py`, `gm/bt_gm_probe.py`,
`gm/chat_command_action.py` + เทส `GmprobeActionTests` 9 เคส + อัปเดต pin test 3 จุดที่การเพิ่มคำสั่งใหม่
บังคับแก้ตามกติกาไฟล์เดิม) — ดู `docs/GM_LANE.md` รอบ `jz4don` สำหรับรายละเอียดเต็ม

`GAME_TEST_QUEUE.md`: ปลด BLOCKED ของ `GT-164` — จุดเสียบลง main แล้ว พร้อมให้กะ1-A เทสจริงเมื่อ merge

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

กะ1-A login ด้วยบัญชี GM แล้วพิมพ์ `/gmprobe <variant_id>` (14 ชื่อจาก `bt_gm_probe.known_variant_ids()`)
ทีละตัวระหว่างเซสชันเดียวได้จริง แทนที่จะรอค่าคงที่เดียวที่ยิงครั้งเดียวตอนล็อกอิน — `GT-164` เปิดให้เทส
ได้แล้ว

## nonclaim

ยังไม่มีการยิงจริงกับไคลเอนต์จริง ไม่มีการอ้างว่า `GMUI_BASIC` เปิดหรือไม่เปิดจาก variant ใด — สิ่งที่ลง
main รอบนี้คือจุดเสียบ (server-side wiring + เทสหน่วย) เท่านั้น การคลิกทดสอบจริงยังเป็นงานของ `GT-164`
ให้กะ1-A ทำต่อ ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`/
`scenarios/combat_*.json` เลยรอบนี้

## pf-adversary

เรียก agent ไม่ได้ในสภาพแวดล้อมของรอบนี้ (ไม่มี Task/agent-launch tool ในชุดเครื่องมือ) — ตรวจทานเองแทน
ตามกติกา ใช้ threat-model เดิมของไฟล์ที่แก้ทุกจุด (args-shape guard แบบ `warp_executor`/`say_wire`, ไม่ echo
ข้อความที่ GM พิมพ์เข้า event/console, ไม่ใช้คำว่า `TELEPORT` ใน label) รันสวีตเต็ม (`5649 passed`, 0 failed)
+ `verify_hypothesis_ledger.py`/`verify_functional_coverage.py` ทั้งคู่ PASS ก่อน commit

PF-AUTOMERGE: v4
