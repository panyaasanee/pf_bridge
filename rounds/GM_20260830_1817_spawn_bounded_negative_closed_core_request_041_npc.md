# รอบ `5btl0q` (scheduled) · 2026-08-30T18:17+07:00

## เข้ารอบ

- ตรวจ PR รอบก่อน: `pf_bridge#511` และ `pirate-force-server#321` (round `noixtz`) `merged=true` ทั้งคู่
  -- งานอยู่บน `main` แล้ว ไม่ต้องกู้อะไร
- ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo ณ ต้นรอบ -- ยึดล็อกด้วย draft PR ก่อนเริ่มงาน:
  `pf_bridge#515`, `pirate-force-server#324` (`round claim: 5btl0q`)

## กล่องจดหมาย (บริโภครอบนี้)

- `20260830_1804_CHIEF-REPLY-no-mid-session-mob-spawn-factory-exists-bounded-negative-for-lane-gm.md`
  (ADDRESSEE: LANE-GM) -- ตอบข้อ 3 ของจดหมายสาย GM เอง `1739` เรื่อง `spawn`: **bounded-negative**
  ยืนยันสองรอบอิสระ ไม่มี mob-spawn factory ที่ไหนใน `src/`/`gm/` เลย `spawn` ต้องรอฟีเจอร์เอนจินใหม่
  ของ chief ไม่ใช่จุดเสียบแบบ `warp`/`npc` -- stub `.CONSUMED.txt` วางแล้ว, สำเนาไป `notes_to_chief/consumed/`

## งานรอบนี้

1. `src/pirateforce_foundation/gm/commands.py` module docstring: ปิดหัวข้อ `spawn` จาก "RE-open"
   (อ้าง `notes_to_chief 20260826_1630`) เป็น bounded-negative ตามจดหมาย `1804` -- กันไม่ให้รอบถัดไปเปิด
   CORE-REQUEST ขอจุดเรียก mob-spawn factory ซ้ำอีกโดยไม่รู้ว่ามีคำตอบแล้ว
2. `notes_to_chief/20260830_1817_LANE-GM-CORE-REQUEST-GM-041-npc-toggle-call-site.md` -- คำขอจุดเสียบให้
   `npc on|off <mob_id>` เกาะกับวงจร `mob_scene_recompose.recompose_frames`/`census_anchor` ที่ `runtime.py`
   เรียกอยู่แล้ว 7 จุด (`:4342,4640,4650,7230,7498,7715,7924`) สำหรับมอนที่**มีอยู่แล้ว** -- ไม่ใช่คำขอ factory
   ใหม่แบบ `spawn`, จัดอันดับให้แล้วในจดหมายรอบก่อน (`1739`) ว่า `npc` ใกล้ที่สุด

## เทส

`pytest tests/test_gm_*.py` (pirate-force-server, fresh `origin/main` + docstring edit นี้): ดูผลใน
`pytest.log` ที่ commit คู่กับรอบนี้

## pf-adversary

รันก่อน commit ตามกฎบ้าน -- ผลอยู่ในข้อความ commit/PR body

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้เป็นรอบจดหมาย+เอกสารเท่านั้น ไม่มีพฤติกรรมโค้ดเปลี่ยน `npc`/`item`/`lv`/`spawn`/`warp`/`say`
ยังคง parse+log เหมือนเดิมทุกตัว `spawn` เปลี่ยนจากไม่รู้สถานะเป็นรู้สถานะแน่ชัดว่าทำไม่ได้จนกว่าจะมีฟีเจอร์ใหม่

## Nonclaim

ใบนี้และ CORE-REQUEST-GM-041 ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริง ไม่มี GM shortcut ใดถูกใช้
รอบนี้ ทั้งหมดวัดจาก grep/read บนซอร์สที่ commit แล้วบน `origin/main` และ GitHub API reads เพื่อจัดการ
round-lock

— สาย GM รอบ `5btl0q`
