[จาก: LANE-GM รอบ `yajien` | 2026-09-06T12:15+07:00]
ADDRESSEE: LANE-E (chief)
cc: COO
ตอบใบ: `20260906_1149_COO-DECISION-gm1119-option-b-...` (เลือก (ข) แล้ว แต่สั่งวัดข้อ 2 ก่อน)

# CORE-REQUEST-GM-063 -- นับ id ขาเข้าที่ไม่มีสาขาไหนรับ หนึ่งจุดในสายจ่ายงานของ `runtime.py`

## วัดข้อ 2 ก่อนตามที่สั่ง (COO item 2): บรรทัด capture ก่อน dispatch มีอยู่แล้วจริงหรือไม่บนเส้นที่ผู้เล่นจริงวิ่งผ่าน

**คำตอบ: ไม่มี บนเส้นที่ให้บริการจริงวันนี้** ไม่ใช่ศูนย์โค้ดใหม่

พบว่า `current/pf_login_game_server_v141.py` เอง (ไม่ใช่แค่เทส) มีบรรทัดแบบที่ COO พูดถึงจริง ในฟังก์ชัน
`main()` ของมันเอง (`~7481`): `print(f"[G< #{state.rx_frames + 1}] {len(pc)} bytes IDs={ids}")`
บวกบรรทัด `STRUCTURAL_IDS {ids!r}` ลงไฟล์ล็อกต่อคอนเนกชัน — ทั้งคู่อยู่**ก่อน** `state.dispatch(parsed)`
ที่บรรทัด `7558` พอดี นี่คือสิ่งที่คอมเมนต์ของ `runtime.py:~8159` ("v141 prints the capture line BEFORE
dispatch") หมายถึงเกือบแน่นอน

**แต่**: grep `app.py` / `connection.py` / `runtime.py` — ไฟล์ที่ถือ connection loop จริงของวันนี้ ตาม
`V141_FREEZE.md` เอง ("บั๊กในไฟล์นี้แก้ที่ปลายทางเสมอ" = v141.py ไม่ใช่ปลายทางที่รันจริง) — หาจุดเรียก
`pf_login_game_server_v141.main()` / `.GameState()` / `.dispatch(` / `.recv_frame(` หรือกลไกพิมพ์ id
ก่อน dispatch แบบเดียวกันของตัวเอง **ไม่เจอเลยสักจุด** `main()`/`GameState.dispatch()` ของ v141.py ถูกเรียก
จากฟังก์ชันเทส/self-test ของไฟล์ตัวเองเท่านั้น ไม่มีที่ไหนในแพ็กเกจเรียกมันจริงเพื่อให้บริการ connection

⇒ ทาง (ค) ตามที่ COO วางไว้: **ออก CORE-REQUEST-GM-063 พร้อมโมดูล hook ที่เขียนเสร็จแล้ว** (ไม่ใช่ทาง
"ศูนย์โค้ด แค่เขียนวิธีอ่านบรรทัดเดิมลงใบ P-3")

`grep แล้ว: เจอ` — บรรทัด print/log ใน v141.py (`current/pf_login_game_server_v141.py:7481` และบริเวณ
ใกล้เคียง) `grep แล้ว: ไม่เจอ` — จุดเรียกเข้า v141.py จาก `app.py`/`connection.py`/`runtime.py` และไม่เจอ
กลไกพิมพ์ id-ก่อน-dispatch แบบของตัวเองในสามไฟล์นั้น (ค้นด้วย `grep -n "\[G<\]\|structural_ids\|def recv_frame"`)

## สิ่งที่สร้างแล้ว (เขต `gm/`/`lane_hooks/` ของสายนี้ ตามรูปเดียวกับ `lane_gm_activity_cheat_code.py`)

`src/pirateforce_foundation/lane_hooks/lane_gm_unknown_vital_counter.py` — จุด hook ชื่อ
`vital_inbound_unknown_id` · ฟังก์ชัน `_on_unknown_vital(session, vital_id)`:
- บันทึกหนึ่งบรรทัดต่อ id ต่อ session ลง `session.events` (`unknown_vital_id_0xXXXX`) — ครั้งที่สองของ
  id เดิมบน session เดิม **ไม่เพิ่มอะไร** (set กันซ้ำต่อ session กันการยิงรัว ๆ ของ id เดิมไม่ให้โตไม่มีขอบเขต)
- ไม่รับ payload เลย (ดูลายเซ็นฟังก์ชัน — ไม่มีพารามิเตอร์ที่เป็น bytes ให้เก็บ) ไม่ส่งอะไรกลับ
- ไม่จัดสรรหน่วยความจำต่อเฟรมสำหรับ id ที่รู้จัก (ฟังก์ชันนี้ไม่ถูกเรียกเลยถ้า id ตรงสาขาไหนอยู่แล้ว —
  เป็นหน้าที่ของจุดเรียกที่ chief จะเสียบ ไม่ใช่ของฟังก์ชันนี้)
- `production_allowed = True` · `registered_but_not_fired = ("vital_inbound_unknown_id",)` จนกว่าจุดเรียก
  จะลง — ลบบรรทัดนี้พร้อมกับคอมมิตที่เสียบ `lane_hooks.fire(...)` (เหมือนที่ `GM-062` ทำกับใบพี่น้อง)

`tests/test_lane_gm_unknown_vital_counter.py` (10 เทส) — production_allowed · discovery/registration ·
กันซ้ำต่อ session ต่อ id · id ต่างกันไม่ถูกกัน · สอง session ไม่แชร์ set กัน · ไม่มีพารามิเตอร์ payload
ในลายเซ็น (ล็อกสัญญา "ไม่เก็บ payload" ไว้ที่ระดับ signature) · ผ่าน `lane_hooks.fire()` จริงหนึ่งจุด

## จุดเรียกที่ขอ (หนึ่งจุด ตำแหน่งเดียว)

ที่ **ท้ายสุด** ของสายจ่ายงานตาม `nested_id` ใน `runtime.py` (หลังทุกสาขาที่มีอยู่แล้ว **รวมของ GM เองทั้ง
สองจุด** `0x51E9`/`0x6CEC`) — เมื่อไม่มีสาขาไหนรับเฟรมนี้เลย ให้เรียก:
```python
lane_hooks.fire("vital_inbound_unknown_id", session=session, vital_id=nested_id)
```
ก่อน `return []` ที่จุดนั้น (ไม่ต้องมี test ปิดเทียบ per-opcode เพิ่มในเขตของ GM — เทสว่า "เส้นทาง opcode
ที่รู้จักไม่เปลี่ยน" ตามที่ COO ข้อ 3 สั่ง เป็นของ chief คู่กับจุดเรียก เพราะเขตนั้นคือ `runtime.py`)

## nonclaims

- ไม่อ้างว่าปุ่ม GMUI ใดส่ง opcode ที่ไม่รู้จัก — ยังไม่มีจุดเรียก ยังวัดไม่ได้
- ไม่อ้างว่า `current/pf_login_game_server_v141.py` เป็นตัวที่ให้บริการ attended session จริงวันนี้หรือไม่ —
  วัดแค่ว่าแพ็กเกจ `pirateforce_foundation` ไม่มีจุดเรียกเข้าไปจากซอร์สที่ grep ได้ ถ้าสะพาน Windows เรียก
  ไฟล์นั้นตรง ๆ นอกแพ็กเกจ (เช่นบูตแยกกระบวนการ) การวัดนี้จะไม่เห็น — เขียนไว้ตรง ๆ ว่าเป็นขอบของการวัดจากคลาวด์
- ไม่อ้างว่าเทสของโมดูลนี้พิสูจน์อะไรเกี่ยวกับ `runtime.py` เอง — พิสูจน์แค่ฟังก์ชัน hook เองก่อนมีจุดเรียก
  เหมือนที่ `test_gm_activity_cheat_code_dispatch.py` ทำกับ `gm/dispatch.py` ก่อน `GM-062`

SCOREBOARD: COMING | ยังไม่มีอะไรใหม่บนจอ -- โมดูลพร้อมให้ chief เสียบจุดเดียว เมื่อเสียบแล้วทุกปุ่ม GM
ที่ยังไม่มี sink จะทิ้ง id ไว้ให้เห็นแทนโฟลเดอร์ว่างที่อ่านไม่ออกว่า "ไม่ส่ง" หรือ "ส่งแต่เราไม่รู้จัก" |
`pirate-force-server#914` (โมดูล+เทสอยู่ในนั้น รวมกับรอบเดียวกัน) + `pf_bridge#1474`

-- LANE-GM
