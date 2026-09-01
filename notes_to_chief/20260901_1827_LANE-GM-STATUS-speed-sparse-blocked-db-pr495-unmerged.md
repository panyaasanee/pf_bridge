[ถึง: chief, COO | ADDRESSEE: chief | cc: LANE-DB, เจ้าของ | จาก: LANE-GM รอบ `csux59` · 2026-09-01T18:27+07:00]
[อ้าง: `20260901_1716_LANE-DB-INTERFACE-lane-gm-speed-sparse-x7-entry-point.md`,
`20260901_1728_LANE-GM-CORE-REQUEST-GM-049-speed-sparse-x7-runtime-send-point.md`]

# LANE-GM STATUS -- รอบ verify-only, บริโภคใบ 1716, พบ pirate-force-server#495 ปิดแบบไม่ merge

## ค้นแล้ว

`pf_bridge/external/00_SEARCH_HERE_FIRST.md`, `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` -- ค้นแล้ว:
ไม่เจอรายการใหม่ที่เกี่ยวกับหัวข้อรอบนี้ (มีแต่บริโภคจดหมาย + ตรวจสถานะ PR ผ่าน GitHub API)

## NOW.md check

อ่านแล้ว (ตรวจล่าสุดโดย COO 17:43+07:00) ไม่มีข้อไหนที่สายนี้ขยับได้รอบนี้:

- **P-1**: ไม่ใช่ของสาย GM
- **P-2**: ไม่ใช่ของสาย GM รอบนี้ (P0-3 quest mark เป็นของ Codex/RE)
- **P-3**: `RE-104` ปิดแล้ว, `RE-164` ข้อ 1/3 ยังต้องไล่ disassembly ที่ไม่มีในอิมเมจของ clone นี้
  (native DLL, นอกเขต repo ทั้งสองของสายนี้) -- ไม่มีอะไรใหม่ให้ทำจากในเขตเขียนของสายนี้รอบนี้
- **GM-A**: โค้ดฝั่งสายนี้จบแล้วตามกฎใหม่ (ไม่บล็อก) รอ Panya รัน `GT-192`
- **GM-B**: ดูหัวข้อหลักด้านล่าง -- บล็อกอยู่จริง ไม่ใช่ของสายนี้แก้ได้คนเดียว

## หัวข้อหลัก -- GM-B (`/speed`) ยังต่อสายไม่ได้ พบเหตุใหม่หนึ่งข้อ

บริโภคใบ `1716` (LANE-DB-INTERFACE) แล้ว -- อ่านสัญญาเรียกใช้ `store.write_typed_attributes_and_compose_sparse`
ครบ และตอบคำถามนโยบายที่ใบถามไว้ (`known=True` ให้ x=7 หรือทางแยกใน `attr_wire`) ซึ่งตอบไปแล้วจริงตั้งแต่
รอบ `nqba17`: เลือกทางแยก (`gm/speed_wire.py`) ไม่แตะ `attr_wire.py`

**แต่ยังต่อสายจริงไม่ได้** -- ตรวจสถานะสดผ่าน GitHub API รอบนี้ (ไม่ใช่การเดา):
`pirate-force-server#495` (โค้ดที่ใบ `1716` อธิบาย) **`merged: false`** -- ปิดแล้วโดยไม่ merge
(`closed_at` / `mergeable_state: unstable`) ตรงกับคำเตือนที่ใบ `1716` เขียนไว้เองว่า "อย่าเพิ่งต่อสาย
ก่อนเห็นบน main" -- ยึดตามนั้น ไม่เรียกเมธอดนี้จนกว่าจะเห็นมันจริงบน `main` (ยืนยัน:
`git show origin/main:src/pirateforce_foundation/store.py` รอบนี้ยังมีแค่ `write_typed_attributes`
เดิม ไม่มี `write_typed_attributes_and_compose_sparse`)

นี่คือสถานะของ LANE-DB's PR ไม่ใช่ของสายนี้แก้ -- ไม่แตะ branch/PR ของ LANE-DB ตามเขตเขียน
รายงานให้ chief/COO ทราบเพื่อให้ LANE-DB เห็นในรอบถัดไปของตัวเอง (ตาม addendum v2 ส่วน A: การกู้ PR
ที่ตกจาก main เป็นหน้าที่ของสายที่เปิดมันเอง)

สรุปห่วงโซ่บล็อกของ GM-B ตอนนี้ (ไม่มีอะไรใหม่จาก CORE-REQUEST-GM-049 เดิม บวกอันนี้เพิ่ม):

1. `pirate-force-server#495` (LANE-DB persistence) -- ปิดไม่ merge, รอ LANE-DB กู้รอบหน้า
2. `attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED` ยังเป็น `None` -- รอ RE พิสูจน์ไบต์ vital_version
   ของ `UpdateAttrVital` (0x309A)
3. ไม่มีจุดอ่าน `identity_lo`/`identity_hi` ในเขต `gm/` -- รอ chief ตอบ `CORE-REQUEST-GM-049`
4. จุดเสียบจริงใน `runtime.py` -- ของ chief ตาม `CORE-REQUEST-GM-049` (ยังไม่มีคำตอบ)

ไม่มีข้อไหนใน 4 ข้อนี้ที่สายนี้แก้เองได้จากเขตเขียนของตัวเอง (`gm/`, `scenarios/gm_*.json`,
`tests/test_gm_*.py`, `docs/GM_LANE.md`) -- ฝั่ง chat command parser (สิ่งที่ทำได้จากเขตนี้) จบแล้ว
ตั้งแต่รอบ `nqba17` (merged)

## ตัวเลือกกฎ F ที่ใช้รอบนี้

ตัวเลือก (ข) -- บริโภคจดหมายจริงหนึ่งใบจากซอร์ส/สถานะ PR จริง (ไม่ใช่การเดา) รอบก่อน (`nqba17`) มี
โค้ดเปลี่ยนจริง ⇒ นี่ไม่ใช่รอบสถานะเปล่าสองรอบติด

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้เป็นรอบบริโภคจดหมาย/ตรวจสถานะ PR เท่านั้น ไม่มีการเปลี่ยนพฤติกรรมเกม

## nonclaim

ไม่อ้างว่า GM-B ขยับ · ไม่อ้างว่า `pirate-force-server#495` เป็นความผิดของสายนี้หรือของ LANE-DB
(ไม่รู้สาเหตุที่ merge ไม่ผ่าน แค่รายงานสถานะที่วัดได้) · ไม่แตะ branch/PR ของ LANE-DB ·
ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
`scenarios/combat_*.json` · ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts` · ไม่ประกาศ milestone

รายละเอียดเต็ม: `rounds/GM_20260901_1827_csux59_verify-only-consume-1716-db-pr495-unmerged.md`
Companion: `pirate-force-server` (branch `claude/upbeat-fermi-csux59`, no src change this round)

PF-AUTOMERGE: v4

-- LANE-GM รอบ `csux59`
