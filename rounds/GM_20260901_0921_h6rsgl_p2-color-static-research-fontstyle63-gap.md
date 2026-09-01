# LANE-GM round `h6rsgl` — 2026-09-01T09:21+07:00

## ล็อกรอบ

ต้นรอบ: ไม่มี PR `[LANE-GM]` เปิดค้างในสอง repo (`search_pull_requests is:open in:title [LANE-GM]` =
0 ทั้งคู่) ยึดล็อกด้วย draft PR `pf_bridge#685` / `pirate-force-server#456`

ตรวจชะตารอบก่อน (ADDENDUM v2 ข้อ A): PR `[LANE-GM]` ที่ปิดล่าสุดคือ `pf_bridge#677` / รอบ `bxkxfc` —
ตรวจด้วย `pull_request_read(method=get)` ตรง ๆ (ไม่เชื่อ `list_pull_requests`) ทั้งคู่ `merged:true`
งานรอบก่อนอยู่บน main แล้ว ไม่มีอะไรต้องกู้

## What (round `h6rsgl`)

### 1. บริโภคจดหมาย (ADDENDUM v2 ข้อ B)

จดหมายเดียวที่ยังไม่มี stub ที่แท้จริง (`ADDRESSEE:.*LANE-GM` ไม่จำกัดตำแหน่งคอมมา — ตรวจซ้ำเพราะรอบก่อน
ๆ grep แคบเกินไปพลาดใบที่มีผู้รับหลายคน): `20260901_0759_CHIEF-REPLY-gm047-fixed-pending-merge-plus-
queue-shrink-mandate-accepted.md` — อ่านแล้ว ยืนยันซ้ำอิสระว่า `GM-047` merge จริงผ่าน `git log` บน
`pirate-force-server` main (`01735df`/`3458277`, PR #452) วางสตับ + สำเนาไป `consumed/` แล้ว
ใบ `20260831_0720_LANE-GM-ASK-COO-two-empty-rounds...` เป็นใบที่สายนี้เปิดเอง (ไม่ใช่จดหมายเข้า)
ตอบแล้วโดย `COO-DECISION 20260831_0745` ไม่มีอะไรต้องทำเพิ่ม
CODEX-CHECKPOINT ทุกใบถึง `0443` บริโภคแล้วโดยรอบก่อน ไม่มีใบใหม่กว่านั้น

### 2. งานหลัก: P-2 (สีชื่อมอน) — static research

ตาม `PANYA-ORDER 20260901_0215` + `FROM_CHIEF_R278 20260901_0302` มอบ P-2 ให้ LANE-GM ชัดเจน ใช้
subagent `pf-static-re` ค้นข้อมูล static/headless ที่ commit แล้วทั้งหมด (ไม่มี client image ใน
สภาพแวดล้อมนี้) ตามกฎ "ค้นก่อนถอด" ผล:

- `PF_ATTR_NAME_COLOR_SELECTOR.tsv` มีแค่ 2 fontstyle ที่ยืนยันแล้วในเลน `typed_CNetNPC` (61/62 —
  สู้/ไม่สู้) ไม่มีแถวที่สาม ("ตาย") เลย
- ตัวเลือกใกล้เคียงที่สุด `fontstyle_id=63` มาจากเลน `untyped_dynamic_controller` เท่านั้น
  (`owner_class_unproved`) ตารางเองปฏิเสธตรง ๆ ว่า "FontStyleID 63 is not equivalent to dead"
- `RE-109` (ปิดแล้ว) มี `BUILD_IMPACT: NONE` ชัดเจน — ห้ามเดาสีจาก id ใด ๆ ในตารางนี้ สายนี้จึงไม่เขียน
  โค้ดสีรอบนี้ (จะขัด RE-109 ตรง ๆ)
- `RE-155` (เปิดอยู่) เป็นเรื่องสีตอนสู้ คนละสโคปกับตาย=เทา
- พบ predicate ตายที่พิสูจน์แล้วจริง (`0x0043BD70..0x0043BD9D`, สองตารางยืนยันตรงกัน) แต่ยังไม่พิสูจน์ว่า
  เรียกผ่าน vtable `CNetNPC` จริง — นี่คือช่องว่างที่แคบและตอบได้แบบ static ล้วน
- พบ data-hygiene gap: สองตารางที่ยืนยัน predicate ไม่อยู่ใน generation manifest + มีป้าย STALE ค้าง
  แจ้งให้ chief/RE ทราบเฉย ๆ ไม่ block

เขียนจดหมาย `20260901_0921_LANE-GM-STATUS-p2-color-static-research-fontstyle63-gap-re-followup-
proposed.md` เสนอใบ RE แคบ (static-only, ไม่ต้อง attended capture) ให้ chief มอบสาย RE ต่อ

### 3. pf-adversary — พบข้อขัดแย้งจริง แก้แล้ว

รันจริงเป็น subagent (ไม่ใช่ self-review) รีวิวจดหมายก่อน commit ครั้งสุดท้าย พบว่าฉบับร่างแรกเขียน
สับสน: ย่อหน้าหนึ่งบอกว่า `RE-155` "ไม่ใช่เรื่องตาย=เทา" แต่ย่อหน้าถัดมากลับอ้างว่า attended-capture
ของ `RE-155` เป็น "ทางเดียวที่เหลือจริง" ของ P-2 ทั้งที่ใบ RE ที่เสนอเองเป็น static ล้วนไม่ต้องรอ
attended capture เลย — ทำให้ escalate ปัญหาการตีความคำสั่งเจ้าของไปยัง chief/COO แบบไม่จำเป็น (false
dilemma) แก้จดหมายแล้ว: แยกให้ชัดว่าปัญหา freeze กระทบเฉพาะสโคปของ `RE-155` เอง ไม่กระทบใบ RE ที่เสนอ
สำหรับตาย=เทา เพิ่ม nonclaim ข้อใหม่ระบุตรง ๆ ด้วย

## เขียว

`cd pirate-force-server && python3 -m pytest tests/test_gm_*.py -q` = **1206 passed, 547 subtests
passed** เขียว(cloud sanity) — ไม่มีการแก้โค้ดรอบนี้ รันเพื่อยืนยัน baseline ก่อน/หลังไม่เปลี่ยน

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — รอบนี้เป็นรอบวิจัย/จดหมายล้วน ไม่มี wire ใหม่ ไม่มีโค้ดเปลี่ยน

## nonclaim (ระดับรอบ)

1. ไม่อ้างว่า fontstyle 63 คือสีเทาของมอนตาย — ยังไม่พิสูจน์
2. ไม่เขียนโค้ดสีใด ๆ — จะขัด `RE-109` `BUILD_IMPACT: NONE`
3. ไม่ตัดสินเองว่า attended-capture แบบสังเกตอย่างเดียวเข้าข่ายข้อยกเว้นคำสั่งเจ้าของหรือไม่ — ส่งต่อ COO
4. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`/`gm/attr_wire.py` (ยัง shelved เหมือนเดิม รอบนี้ไม่แตะ)
5. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone
6. GM-B (`/speed`, GT-183) ยังบล็อกจริงเหมือนรอบก่อน — ไม่มีความคืบหน้ารอบนี้ (path1/path2 ของ
   `attr_wire.py` ยังรอเจ้าของตอบใบ `2327`) ไม่ได้ตรวจซ้ำรอบนี้เพราะไม่มีจดหมายใหม่เข้าเรื่องนี้
7. ไม่ลบประวัติเดิม

## PR

`pf_bridge#685`, `pirate-force-server#456`

— สาย GM รอบ `h6rsgl`
