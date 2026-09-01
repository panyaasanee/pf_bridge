# LANE-GM round `p4cndg` -- 2026-09-01T11:19+07:00

## ล็อกรอบ

ต้นรอบ: `list_pull_requests(state=open)` ทั้งสอง repo = มีเฉพาะ `[LANE-E] WIP round claim 8zf80f`
(`pf_bridge#692`, `pirate-force-server#462`) -- ไม่ใช่ล็อกของสายนี้, ไม่นับ ยึดล็อกด้วย empty
commit "round claim: p4cndg" + draft PR `pf_bridge#695` / `pirate-force-server#464`
(หัวข้อ `[LANE-GM] WIP round claim p4cndg`)

หมายเหตุปฏิบัติการ: การ push สองรีโปพร้อมกันแบบ parallel tool call ทำให้ `cd` ของ Bash call หนึ่ง
ไม่ persist ข้าม parallel batch -- คอมมิต empty commit ซ้ำสามครั้งบน `pf_bridge` ก่อนจะแก้เป็น
sequential + explicit `cd` ทุกคำสั่ง ไม่กระทบผลลัพธ์ (empty commit ซ้ำไม่มีผลข้างเคียง) แต่บันทึกไว้
กันคนอ่านสงสัยทำไม `pf_bridge` มี "round claim: p4cndg" สามคอมมิตติดกัน

ตรวจชะตารอบก่อน (ADDENDUM v2 ข้อ A): PR `[LANE-GM]` ล่าสุดคือรอบ `gm-20260901_1013`
(`pf_bridge#689` / `pirate-force-server#460`) ตรวจด้วย `search_pull_requests` อ่าน `merged_at`
โดยตรง (ไม่ใช้ `list_pull_requests`'s `merged` boolean -- ดูเหตุผลในหัวข้อมอบจดหมายด้านล่าง):
`merged_at: 2026-09-01T03:21:18Z` (`pf_bridge#689`) / `2026-09-01T03:30:48Z`
(`pirate-force-server#460`) -- **merged จริง** งานรอบก่อนอยู่บน `main` แล้ว ไม่มีอะไรต้องกู้

## บริโภคจดหมาย (ADDENDUM v2 ข้อ B)

พบสามใบ `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt` คู่กัน:

1. `20260901_1045_KA1A-TO-LANE-GM-UI-A-blocked-...md` -- อ้างว่า UI-A เป็นของสาย GM **ผิด**
   ตรวจกับ `FROM_CHIEF_R278` (บรรทัด 49-50) แล้ว UI-A/UI-B เป็นของ **LANE-A** ตรงตัว และ LANE-A
   เปิด `RE-189` ไปแล้วตั้งแต่ 05:50 (ก่อนใบนี้ 5 ชม.) เขียนแก้กลับไปที่ chief แล้ว (ดูใบ STATUS
   ของรอบนี้) ตรวจซ้ำโดย pf-adversary subagent -- ไม่พบใบอื่นที่แย้งกับ R278
2. `20260901_1059_COO-DECISION-owner-rules-attr-wire-...md` -- GM-B (`/speed`) ย้ายเจ้าของงานไป
   สายใหม่ **LANE-DB** สาย GM ไม่ต้องทำอะไรเรื่อง `attr_wire.py`/`chat_command.py` ตอนนี้ ยกเว้น
   เตรียมรับคำขอจุดเสียบ -- ส่งใบข้อมูลล่วงหน้าให้ LANE-DB แล้ว (ดูหัวข้อถัดไป)
3. `20260901_1105_KA1A-DISPROVEN-the-automerge-pipeline-...md` -- แจ้งว่ารอบ 10:38 ก่อนหน้า (นอก
   ลำดับรอบที่มีไฟล์บันทึกของสายนี้) อ้างผิดว่า automerge pipeline พัง เพราะอ่าน `merged` field
   จาก `list_pull_requests` (คืนค่า `false` เสมอไม่ว่าจะ merge จริงหรือไม่) แทนที่จะอ่าน
   `merged_at` -- ไม่พบไฟล์รอบ/จดหมายของรอบ 10:38 ในเขตเขียนของสายนี้เลย (ตรงกับที่ใบบอกว่ารอบนั้น
   "touched nothing") ไม่มีอะไรต้องแก้ย้อนหลัง บทเรียนถูกใช้จริงในการตรวจชะตารอบก่อนของรอบนี้เอง
   (อ่าน `merged_at` ตรง ๆ ตลอด)

จดหมายที่สายนี้เปิดเองยังไม่มีคำตอบใหม่ (ไม่ใช่ของเข้าที่ต้องบริโภครอบนี้):
- ใบเสนอ RE follow-up สำหรับ P-2 (`h6rsgl`) -- chief ยังไม่มอบสาย RE (รอบที่ 2 ที่รอ) -- ขอย้ำใน
  จดหมาย STATUS รอบนี้

## ค้นตามกฎ (ก่อนอ้างข้อเท็จจริงจาก client)

- `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (sanity check ข้อ 0) --
  **ค้นแล้ว: เจอ** มีไฟล์อยู่จริงที่ root ของ `pf_bridge` (ต่างจากรอบก่อนที่หาไม่เจอใน `external/`)
- `pf_bridge/external/PF_MONSTER_COLOR_GATE.tsv`/`.md`/`.pair.json`/`pf_rederive_...py` (อ้างใน
  `CODEX_URGENT_1040`) -- **ค้นแล้ว: ไม่เจอ** ยังไม่ถูก sync เข้า clone นี้ (Windows-bridge-local
  เหมือนไฟล์ Codex ชุดก่อน ๆ)
- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` / `gamedata/00_SEARCH_HERE_FIRST.md` --
  **ค้นแล้ว: เจอ** ทั้งคู่

## งานหลักรอบนี้

ทั้งสามแนว (P-2/P-3/GM-B) ยังบล็อกจากภายนอกเหมือนรอบก่อน ไม่มีข้อมูลใหม่ให้เขียนโค้ด `gm/`:

- **P-2**: `CODEX_URGENT_1040` ถอนสถานะ exact ของ `MCG-IMG-025..033` ลงเป็น `PARTIAL` เพิ่มเติม
  (ไม่ใช่ปรับปรุง เป็นการถอน) แต่ยืนยันว่าข้อเสนอ RE follow-up ของสาย GM ยังไม่ถูกถอน เป้าที่ต้อง
  ปิดเหมือนเดิม (operand path `CNetNPC` -> caller `0x004446A7` -> selector -> controller `+0x50`
  instance เดียวกัน) ยังรอ chief มอบสาย RE
- **P-3**: `CODEX-CHECKPOINT-0934` ข้อ 2 (export/slot `+0x00`, calling convention, MSVCR90
  allocator) ถูกดูดเข้า stub ไปแล้วตั้งแต่รอบ `gm-20260901_1013` -- ไม่มีของใหม่
- **GM-B**: ย้ายเจ้าของงานไป LANE-DB ตาม COO -- สาย GM เขียนใบข้อมูล
  (`gm/attr_wire.py`'s field `x=7` ปัจจุบัน `known=False`, สองเงื่อนไขอิสระที่ต้องผ่าน) ให้ LANE-DB
  ไม่แตะโค้ด

รอบนี้จึงไม่มีการแก้โค้ดใน `gm/`/`scenarios/gm_*.json`/`tests/test_gm_*.py` -- งานที่ทำได้จริงคือ
แก้ที่มาข้อมูลผิด (UI-A), ยืนยัน/ปิดใบที่ตอบแล้ว (GM-B->LANE-DB), เตือน chief เรื่อง P-2 ค้างมอบสาย
2 รอบติด, และส่งข้อมูลล่วงหน้าให้ LANE-DB กันเสียรอบ

## เขียว

`cd pirate-force-server && python3 -m pytest tests/test_gm_*.py -q` = **1206 passed, 547 subtests
passed** เขียว(cloud sanity) เท่ากับ baseline (ไม่มีการแก้โค้ดรอบนี้)

## pf-adversary

รันจริงผ่าน `Agent(subagent_type: pf-adversary)` -- เครื่องมือนี้มีอยู่ใน session นี้ (ต่างจาก
รอบ `gm-20260901_1013` ที่ไม่มี) ตรวจสามข้อกล่าวอ้างหลักของจดหมายรอบนี้:

1. UI-A เป็นของ LANE-A ไม่ใช่ LANE-GM (ตรวจ R278 + `RE-189`) -- **ยืนยันถูกต้อง**
2. `attr_wire.py` field `x=7` (`offset 0x054`) `known=False` ตรงกับเป้าที่ COO-ORDER อ้าง แต่
   `known` gate เป็นเงื่อนไขอิสระจาก cache-seed gate -- **ยืนยันถูกต้อง** (พบเพิ่ม: COO-ORDER เอง
   พูดถึงแค่เงื่อนไข cache ไม่ได้พูดถึงเงื่อนไข `known` -- เพิ่มลงในจดหมายถึง LANE-DB แล้ว)
3. การไม่แตะโค้ด `gm/attr_wire.py`/`gm/chat_command.py` รอบนี้ถูกต้องตามคำสั่ง COO ("เหมือนเดิม
   ทุกไบต์") ไม่ใช่การตีความกว้างเกินไปของ "รอคำขอ" -- **ยืนยันถูกต้อง**

ไม่พบข้อบกพร่องในทั้งสามข้อ (รายละเอียดเต็มอยู่ใน subagent transcript ของรอบนี้ ไม่คัดลอกซ้ำที่นี่)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** -- รอบนี้เป็นรอบแก้ข้อมูลมอบหมาย/มอบจดหมายให้สายที่ถูกต้อง/เตือน chief ล้วน ไม่มี wire
ใหม่ ไม่มีคำสั่งแชทใหม่ ไม่มีอะไรให้ทดสอบเพิ่ม

## nonclaim (ระดับรอบ)

1. ไม่อ้างว่า P-2/P-3 ปิดได้แล้ว -- ทั้งคู่ยังบล็อกจากภายนอก
2. ไม่ flip `known` ของ `x=7` ใน `attr_wire.py` เอง -- COO สั่งตรงให้คงเดิมทุกไบต์
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `scenarios/world_*.json`/`scenarios/combat_*.json`/`gm/attr_wire.py`/`gm/chat_command.py`
4. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone
5. ไม่ใช้ GM เพื่อข้ามขั้นตอนใด ๆ รอบนี้ -- ไม่มีการ boot เกม/เซิร์ฟเวอร์เลย
6. ไม่ลบประวัติเดิมใด ๆ

## PR

`pf_bridge#695`, `pirate-force-server#464`

-- สาย GM รอบ `p4cndg`
