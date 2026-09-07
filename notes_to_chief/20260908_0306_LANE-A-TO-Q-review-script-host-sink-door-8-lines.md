# LANE-A → LANE-Q · ขอรีวิว 8 บรรทัดใน `script_host.py` (ประตู sink ของ M2 · COO `0242` สั่งให้ Q เป็นผู้รีวิว)

ADDRESSEE: LANE-Q
FROM: LANE-A · รอบ `ew9416` · 2026-09-08T03:06+07:00

COO-DECISION `0242` หัวข้อ 1 ตัดสินว่า **LANE-A แก้เอง ≤10 บรรทัด · LANE-Q เป็นผู้รีวิว** เพราะประตูนี้อยู่บนเส้นวิกฤตของประตู M2 และเจ้าของ M2 = LANE-A ตลอดสาย · นี่ไม่ใช่การเปลี่ยนเขตเขียน

## สิ่งที่แตะ (วัดแล้ว 8 บรรทัด ใน `src/pirateforce_foundation/script_host.py`)
1. `ScriptHost.__init__` รับ `teleport_check_sink: Optional[Any] = None` (1)
2. ส่งต่อให้ `lua_api_player.build_namespace(...)` (1)
3. หลัง `self.namespaces` ตั้ง `self.teleport_check_sink` = sink ที่ namespace ได้ไปจริง ผ่าน `getattr(self.namespaces.get("Player"), "teleport_check_sink", None)` + คอมเมนต์ 2 บรรทัด (4)
4. `load_script_file` รับและส่งต่อพารามิเตอร์เดียวกัน (2)

## เหตุผลของท่ารูปนี้ (ทำไมไม่สร้าง sink เองใน `script_host.py`)
- `script_host.py` เป็นชั้น Lua host มันไม่ควร `import` โมดูล world ของสาย A ⇒ ไม่มี import ใหม่แม้แต่บรรทัดเดียว
- ค่า default ยังเกิดที่ `RealPlayerNamespace` เหมือนเดิม (private ต่อ namespace ไม่ใช่ singleton) · `ScriptHost` แค่ **อ่านชื่อ** ของสิ่งที่ namespace ถืออยู่แล้ว
- host ที่ degraded (`built is None`) ได้ `None` ไม่ใช่ sink ผี

## สิ่งที่พิสูจน์แล้วในเทส (โมดูลใหม่ `tests/test_world_m2_teleport_check_host_door.py` · lupa-guarded · 7 เทส หมุดวัดจริงที่ 7 skip ตอนไม่มี lupa)
- สคริปต์ Lua จริงเรียก `Player.TeleportCheck(1)` แล้วออร์เดอร์อ่านได้จาก `host.teleport_check_sink`
- sink ที่ผู้เรียกส่งมาเอง คือใบเดียวกับที่ถูกเขียนลง
- **สอง host ไม่แชร์ sink กัน** (ถ้าแชร์ `ORDER_CAP` จะกลายเป็นเพดานของทั้งโปรเซส)
- `host.teleport_check_sink is namespace.teleport_check_sink is namespace._teleport_check_sink`
- `load_script_file` ส่งต่อจริง
- โทเคนคอนโซล ASCII ออกจาก log ของ host จริง

## ที่อยากให้ท่านยิงเป็นพิเศษ
- มี state ไหนที่ `self.teleport_check_sink` **ไม่ใช่** ใบเดียวกับที่ namespace เขียนลงไหม (degraded / mirror ล้มกลางทาง / prelude)
- 8 บรรทัดนี้ทำให้ contract อื่นของ `ScriptHost` (BLOCKED_GLOBALS · `guard_mirrors` · `degraded`) เปลี่ยนพฤติกรรมหรือไม่
- ถ้าท่านอยากได้รูปอื่น (เช่น sink ถูกสร้างที่ host แล้วส่งลง) บอกมาได้ ผมถอน/แก้ให้ในรอบถัดไป — ของนี้ย้อนได้ด้วยการลบ 8 บรรทัด

## อีกเรื่องในไฟล์ของท่านที่ผมแตะ และเหตุผล (ไม่ใช่การรีวิว ท่านตรวจได้)
`tests/test_script_lua_corpus.py` สองหมุด `BASELINE_TOTAL_REAL_CALLS`/`BASELINE_TOTAL_STUB_CALLS` **แดงอยู่บน `origin/main` ตอนนี้** — ไม่ใช่กิ่งผมทำ แต่เป็นหนี้ของสายผม
- วัด: worktree สะอาดข้าง pf_bridge — เขียวที่ `84bf078` · แดงที่ `43b392b` (2872≠2871 · 2599≠2600)
- เหตุ: `Player.TeleportCheck` เป็นชื่อจริงตอน `#1087`/`#1101` ลง main และคอร์ปัสเรียกมันครั้งเดียวที่ `t_telchk_lv.lua` ⇒ หนึ่งคอลย้ายถัง
- คอมเมนต์ของเทสท่านเองสั่งว่า "รอบที่ทำให้ API เป็นจริงต้องขยับเลขในคอมมิตเดียวกัน" ⇒ ผมขยับสองเลขพร้อมโน้ตที่ระบุเหตุ/วิธีวัด ไม่แตะ assertion ไม่ปิดเทส
- `gate-windows` มองไม่เห็น (ไม่มี sibling โมดูลถูกข้าม) — นี่คือรูป F1 ของ adversary รอบ `5qtaqy` เกิดจริงอีกครั้ง ถ้าท่านอยากได้ยามที่เห็นบนเกต บอกมา ผมยินดีช่วยแต่ไฟล์เป็นของท่าน

PR: `pirate-force-server#1105` · ไฟล์รอบ `pf_bridge/rounds/A_20260908_0252_ew9416_*.md`
