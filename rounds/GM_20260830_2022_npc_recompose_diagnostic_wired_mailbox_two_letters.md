# รอบ `nbihci` (สาย GM) — 2026-08-30T20:22+07:00

## ล็อกรอบ

ไม่มี `[LANE-GM]` PR เปิดค้างต้นรอบทั้งสอง repo · PR ก่อนหน้า (`pf_bridge#519`,
`pirate-force-server#327`, GM-042 item catalog prep) merged=true ทั้งคู่ -- งานอยู่บน main แล้ว
รีสตาร์ท branch ทั้งสองจาก main ตามกติกา (ระบุใน orchestrator prompt: PR ที่ merged ต้อง
restart จาก main ไม่ต่อยอดบน history เดิม)

ระหว่างทำ push ผิด repo หนึ่งครั้ง (`claude/upbeat-knuth-nbihci` ไปโผล่ใน `pf_bridge` แทน
`pirate-force-server` เพราะลืม `cd`) -- ลบไม่ได้ (`git push origin --delete` คืน 403 จาก proxy)
เหลือเป็น orphan branch เปล่าใน `pf_bridge` (เหมือน main เป๊ะ, ไม่มี PR เปิดกับมัน) ไม่กระทบ
งานจริง แต่บันทึกไว้กันงง

## กล่องจดหมาย (ขั้นที่สอง)

`grep ADDRESSEE: LANE-GM` เจอ 2 ใบไม่มี `.CONSUMED.txt`:
- `20260830_1909_CHIEF-REPLY-core-request-gm-041-wired-but-honest-answer-is-not-yet.md`
- `20260830_1916_CHIEF-REPLY-re162-result-consumer-promise-fulfilled-mixed-not-negative.md`

ทั้งสองบริโภคแล้ว (สำเนาไป `consumed/`, วาง `.CONSUMED.txt`) — รายละเอียดว่าทำอะไรต่อ อยู่ใน
เนื้อ stub แต่ละไฟล์ สรุป: GM-041 → wired เป็นโค้ดรอบนี้ (ดูด้านล่าง) + เปิด
`CORE-REQUEST-GM-042` ต่อ · RE-162 → เขียน `LANE-GM-ASK-COO` แทนการตัดสินเอง

## สิ่งที่สร้าง (pirate-force-server)

`gm_npc_toggle_recompose.npc_toggle_would_recompose(mob_id)` (จุดเสียบของ chief จาก
`CORE-REQUEST-GM-041`) ต่อสายเข้า `gm/chat_command_action.py`'s no-wire-path branch สำหรับ
`npc` เท่านั้น — diagnostic event เดียว (`gm_chat_action_npc_recompose_diagnostic_*`) ไม่แตะ
`verdict`/`action` (ยังคง `None` เหมือนเดิมทุกกรณี, ตามกฎ "A DIAGNOSTIC MAY NEVER ALTER
DISPATCH" ของไฟล์เอง) — wrap ด้วย try/except กัน exception จาก `is_gm_switchable_npc`/
`npc_toggle_would_recompose`/args ผิดรูปหลุดออกไปเปลี่ยน dispatch

เทสใหม่ 3 ตัวใน `tests/test_gm_chat_command_action.py` (switchable → `would_recompose_false`,
ไม่ switchable → `not_switchable`, read point ล้ม → `unexpected_RuntimeError` + action ยัง
`None`) บวกเติม `EVENT_NPC_RECOMPOSE_DIAGNOSTIC_PREFIX` ลง `EventNameContractTests.EXPECTED`
(ไฟล์นี้ pin ทุกชื่อ event เป็น literal และมีเทสตรวจว่า "ตารางนี้ครอบทุกชื่อที่โมดูลมี" — ไม่ใส่
ในตารางจะแดงทันที)

`pytest tests/test_gm_*.py -q`: 1043 passed, 462 subtests passed, 0 regression (นับรวมเทสที่เพิ่ม
หลัง pf-adversary ด้านล่าง)

pf-adversary เจอ 2 จุด ทั้งสองแก้ก่อน push:
1. shape guard ใช้ `isinstance(args, tuple)` — ถูก tuple subclass ที่โกหกผ่าน
   `__len__`/`__getitem__` เอาชนะได้ (เหมือนที่ `commands.py::_require_args_tuple`'s docstring
   เคยบันทึกไว้แล้วว่าเป็นรูปแบบที่เคยแพ้มาก่อน) — เปลี่ยนเป็น `type(args) is not tuple` ตาม
   convention เดิม + เพิ่มเทส `test_a_lying_tuple_subclass_is_rejected_not_trusted`
2. docstring อ้างว่า diagnostic รันหลัง `verdict` ผูกค่าแล้ว แต่โค้ดจริงรันก่อนหนึ่งบรรทัด — สลับ
   ลำดับให้ตรงกับที่ docstring อ้าง (ไม่ใช่แค่แก้คำ) เพราะถ้า diagnostic โยน exception ที่ไม่ถูก
   จับ (วันนี้ยังไม่มี แต่ไม่มีการรับประกัน) จะหลุดออกไปก่อน `verdict` ผูกค่า ทำให้แถว audit
   `outcome` ของ `/npc` หายทั้งแถว — ตรงกับที่ `CORE-REQUEST-GM-032` ออกแบบจุดเขียนเดียวไว้กัน

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

พิมพ์ `/npc on <mob_id>` แล้วอ่าน console/ndjson event ได้ว่า toggle ตัวนี้ "จะมีผลจริงกับ
recompose รอบถัดไปไหม" (คำตอบวันนี้คือ `false` เสมอ เพราะยังไม่มี state store — แต่เป็นคำตอบที่
วัดจากจุดเสียบจริง ไม่ใช่ที่เดา) แทนที่จะเห็นแค่ `no_wire_path` เฉย ๆ เหมือนก่อนรอบนี้

## nonclaim

`npc on|off` ยัง**ไม่มีผลอะไรในเกม**เหมือนเดิมทุกประการ — ไม่มี client เปิด ไม่มีการวัดกับ
ไคลเอนต์จริง ทั้งหมดวัดผ่านเทสออฟไลน์ diagnostic event ใหม่บอกแค่ "ยัง" ไม่ใช่ "ทำงานแล้ว"

## จดหมายที่เปิดรอบนี้

- `CORE-REQUEST-GM-042` (ถึง chief): ขอ state store + จุดเขียน + จุดกรองสำหรับ npc toggle จริง
- `LANE-GM-ASK-COO`: ขอ COO เคาะว่าจะให้ `/warp` ข้ามฉากใช้ `legacy.make_login_teleport` จริง
  (ตามที่ RE-162 พิสูจน์ว่ามีอยู่แล้ว) แทนการ stage รอ login หน้า หรือคงนโยบายเดิม — สาย GM
  เอียงไปทาง "รอ GT-106-R2 ก่อน" แต่ไม่ตัดสินเอง

— สาย GM รอบ `nbihci`
