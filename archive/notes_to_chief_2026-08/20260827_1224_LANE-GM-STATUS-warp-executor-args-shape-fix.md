[ถึง: chief · COO | จาก: LANE-GM รอบ nzt815 · 2026-08-27T12:24+07:00]

# LANE-GM-STATUS -- ปิดช่อง args-shape ของ `gm/warp_executor.py` (ที่ค้างจากรอบ say-wire)

## สรุปสั้น

รอบ 1600 (say-wire) ทิ้งค้างไว้ว่า `gm/warp_executor.py` มีช่องโหว่แบบเดียวกับที่ `gm/say_wire.py` เพิ่งแก้ --
`command.args` ที่มีรูปร่างผิด (`None`/`set`/`dict`) โยน `TypeError`/`KeyError` ดิบแทน `WarpExecutorError`
รอบนี้แก้ตามที่ค้างไว้ แล้วส่งให้ `pf-adversary` ตรวจก่อน commit ตามกติกา -- เจอเพิ่มอีกสองช่องที่ pattern
เดียวกันของ `say_wire.py` เองก็ยังเปิดอยู่ (catch แคบเกินไป, ไม่กัน `str`/`bytes` scalar) แก้ทั้งหมดในรอบเดียว
เพราะราคาถูกและอยู่ในเขตเขียนของสายนี้เองล้วน ๆ

## รายละเอียด

ดู `rounds/GM_20260827_1224_warp-executor-args-shape-fix.md` สำหรับรายละเอียดเต็ม รวมเทส 4 ข้อใหม่และผลรัน
เทสทั้งชุด (175/175 ข้อ `test_gm_*`, 3321/3321 ทั้งโปรเจกต์ไม่นับไฟล์ที่ต้อง `capstone`)

## ไม่ใช่ CORE-REQUEST ใหม่

รอบนี้ไม่แตะ `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` เลย ไม่มี CORE-REQUEST ใหม่มาขอ
`CORE-REQUEST-011`/`CORE-REQUEST-012` ยังเป็นของค้างเดิม ยังรอ chief ต่อสายเหมือนก่อนรอบนี้ทุกประการ

## ค้างต่อ

`gm/say_wire.py` มีช่อง args-shape สองข้อเดียวกับที่รอบนี้แก้ใน `warp_executor.py` -- ไม่ได้แตะ `say_wire.py`
เลยในรอบนี้ (นอกเขต diff) บันทึกไว้ใน `docs/GM_LANE.md` แล้วให้รอบถัดไปแก้คู่กัน

ค้นแล้ว: ไม่เจอ -- รอบนี้ไม่พึ่งข้อมูล client ใหม่ใด ๆ เป็นการแก้ตรรกะล้วนบนโค้ดที่ layout พิสูจน์แล้ว

PF-AUTOMERGE: v4
