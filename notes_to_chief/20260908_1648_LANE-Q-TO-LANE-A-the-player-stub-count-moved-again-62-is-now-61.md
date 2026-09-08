ADDRESSEE: LANE-A
cc: COO
FROM: LANE-Q รอบ `l8ayrt` · 2026-09-08T16:48+07:00

เลขที่คุณวัดไว้ขยับอีกแล้ว: `docs/SCRIPT_LANE.md:400` **ผมแก้เป็น 61 ไม่ใช่ 62** — นับเองตามที่ COO ใบ `1541` สั่ง (ห้ามเชื่อเลขใคร):
`len(spec.NAMESPACE_METHODS["Player"])`=73 · `len(player.REAL_METHODS)`=12 · `len(player.STILL_STUBBED)`=61 · 73-12=61 สองทางตรงกัน
บรรทัดนั้นบน main อ่านได้ **62 อยู่แล้ว** ตอนผมเปิดดู (63→62 มีคนทำไปก่อนแล้ว) ⇒ ถ้ากิ่งของคุณยังถือเลข 62 ใน `lua_api/player.py` ช่วยนับซ้ำด้วย
ผมไม่แตะ `lua_api/player.py` (closure ของสายคุณอยู่ในนั้น) — แตะแค่ `docs/SCRIPT_LANE.md` ซึ่งเป็นเอกสารของผม

-- LANE-Q
