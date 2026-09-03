ADDRESSEE: chief · cc: COO, กะ1-B, เจ้าของ
ประเภท: STATUS — สรุปรอบ `rawblk` (session `sched-20260831-lanegm`)

# สามบรรทัด

บริโภคใบ `COO-DECISION 2026-08-31T16:50+07:00` แล้ว: สร้าง `gm/attr_wire.py` (composer + `RawBlockCache`
+ 46 เทส) ครบทุกฟิลด์ที่มีชื่อ 55-แถวตาราง `FIELDS` — **ยังไม่ต่อคำสั่งแชท ยังไม่ขอ unlock** ตามที่ใบสั่งไว้
ตรง ๆ ว่าต้อง "ออกแบบและพิสูจน์กลไกก่อน" คำถามที่พิสูจน์กลไกนั้นค้างอยู่ที่ CORE-REQUEST-GM-044 (จดหมาย
แยก รอบเดียวกันนี้)

# ค้นแล้ว: เจอ/ไม่เจอ

ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`gamedata/00_SEARCH_HERE_FIRST.md` ก่อนเขียนโค้ด —
ไม่เจอเรื่อง ActorAttr/CreateActorDataEx sub-structure ในสองไฟล์นี้ (คาดว่าไม่เจออยู่แล้ว เป็นคำถามฝั่ง
server-side data model ไม่ใช่ client gamedata) รายละเอียดเต็มอยู่ใน CORE-REQUEST-GM-044

# สร้างอะไรบ้าง

`pirate-force-server`:
- `src/pirateforce_foundation/gm/attr_wire.py` — ใหม่ทั้งไฟล์
- `tests/test_gm_attr_wire.py` — ใหม่ทั้งไฟล์, 46 เทส, เขียวหมด
- `docs/GM_LANE.md` — รอบ `rawblk`

`pf_bridge`:
- `rounds/GM_20260831_1736_rawblk_attr_wire_composer_and_raw_block_cache.md`
- จดหมายนี้ + `CORE-REQUEST-GM-044`

# เขียว

`pirate-force-server`: `python3 -m pytest tests/test_gm_*.py -q` → **1150 passed, 511 subtests**
(จาก 1104/509) · `python3 -m pytest tests/ -q` → **5803 passed, 327 skipped, 10713 subtests** (จาก
5754/327/10709) เขียว(cloud sanity, รันในสภาพแวดล้อมนี้เอง — ไม่ใช่ Actions run)

# pf-adversary

Agent tool ไม่มีจริง (ตรวจด้วย ToolSearch) — self-adversarial แทน พบ+แก้ 1 ข้อ (field 37 transcription
error) รายละเอียดเต็มใน `docs/GM_LANE.md` รอบนี้

# ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ยังไม่มี — groundwork ล้วน ตามที่ COO สั่งเป๊ะ

# nonclaim

ไม่อ้างว่าปลดล็อกอะไร ไม่อ้างว่าตอบคำถาม "omission=zero" ได้ ไม่อ้างว่า `characters.actor_wire` ตรง/ไม่ตรง
กับ `FIELDS` (คำถามเปิด ส่งผ่าน CORE-REQUEST-GM-044) — รายละเอียดเต็มอยู่ในรอบนี้และ `docs/GM_LANE.md`

PF-AUTOMERGE: v4
