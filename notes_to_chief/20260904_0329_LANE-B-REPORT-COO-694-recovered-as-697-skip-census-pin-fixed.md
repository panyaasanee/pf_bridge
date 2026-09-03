[ถึง: COO cc chief · จาก: LANE-B round zgmq8h]

เวลา 2026-09-04T03:29+07:00 · boot HEAD server main `2ad3f29` (ตอนแตกกิ่ง) · pf_bridge main `9f6ca44b`

## สรุปหนึ่งบรรทัด

`pirate-force-server#694` (รอบ 096evp) กู้กลับมาเป็น **`#697`** แล้ว สาเหตุที่ตายคือ `skip_census` หนึ่งข้อ ปิดแล้ว

## รายละเอียด

อ่าน `20260904_0250_SYNC-NOTICE` (บริโภคแล้ว รอบนี้) แล้วทำตามที่ระบุ: กู้จาก branch
`claude/sharp-newton-096evp` (commit `cd8ce0402722e263b2d5071a03084bf63c0f99d1`)
แทนที่จะเริ่มรอบใหม่ ตรวจด้วย `git merge-base --is-ancestor cd8ce040 origin/main`
ยืนยัน exit 1 (ไม่อยู่บน main จริง) ตามกติกา `COO-DECISION 20260902_1745` ข้อ 2

**สาเหตุที่เกตแดง**: gate log ระบุชัด `skip_census exit=1` (ทุกช่องอื่น GREEN รวม
`pytest_subset`) — `UNDECLARED SKIP: tests/test_lane_b_mob_ai_tick.py` หนึ่งใบ
(`persistence_attr_compose stands behind no block at this commit...`) ไม่เคย
ถูกลงทะเบียนใน `docs/PYTEST_SKIP_PINS.json` — ไม่ใช่ artifact หาย เป็น design
skip ที่ต้องปักหมุด ที่รอบ 096evp พลาดจุดเดียว

**สิ่งที่ทำในรอบนี้ (server, `pirate-force-server#697`)**:
1. Cherry-diff `cd8ce040` (diff กับ parent ตรงของมันเอง `d064856b` = 866/-7,
   4 ไฟล์ ตรงกับที่ PR #694 รายงานเป๊ะ) apply บน main ปัจจุบันสะอาด ไม่ชน
   `#692`/`#693`
2. เติม `design_skips` entry ให้ skip ที่ขาดใน `docs/PYTEST_SKIP_PINS.json`
3. การเติมนั้นไปโดนบั๊กเดิมใน `tests/test_pytest_precondition_census.py` เอง
   (`test_a_reason_truncated_by_a_narrow_console_still_matches_its_pin` ฮาร์ดโค้ด
   `design_skips[0]` แล้วสร้าง transcript มีแค่ entry เดียว พอมี entry ที่สอง
   census รายงาน `PIN DRIFT` ของ entry อื่นที่หายจาก transcript ปลอมนั้น) —
   แก้ในคอมมิตเดียวกัน ตามกติกา "แก้เครื่องมือ/เทสร่วมที่โดนสตริงของตัวเองกระทบ
   ในรอบเดียวกัน"
4. ซ้อมบน clone สะอาดไม่มี `pf_bridge` ข้าง ๆ ตามกฎ: `pytest_subset` exit 0
   (8295 passed, 82 skipped) · `skip_census` exit 0 ("every skip is declared,
   named and pinned") — สองช่องที่ฆ่า `#694` เขียวทั้งคู่แล้ว
5. ชุดเต็มครั้งเดียวบน commit สุดท้าย: `9155 passed, 401 skipped, 17540
   subtests, 0 failed`

**สิ่งที่ทำฝั่งสะพาน (pf_bridge, กิ่งนี้)**: `tools_bridge/pf_gate_preflight.py`
เช็ค `[skips]` เดิมเป็น grep หา skip marker ใหม่ล้วน ๆ ไม่รู้จัก
`docs/PYTEST_SKIP_PINS.json` เลย — เจอ skip ที่ปักหมุดถูกต้องแล้วก็ยังรายงาน
RED เหมือนกับ skip ที่ไม่ได้ปักหมุด ทำให้ preflight ของรอบนี้เองแดงทั้งที่เกตจริง
(จำลองแล้ว) เขียว แก้ให้ข้าม-ผ่านเมื่อไฟล์นั้นมีชื่ออยู่ใน `design_skips`
(ยังพิมพ์บรรทัดแจ้งอยู่ ไม่เงียบ) — ยัง**ไม่มีใบเทสของตัวเอง**สำหรับไฟล์นี้
เขียนไว้ให้ COO ทราบ ไม่ใช่การขออนุมัติย้อนหลัง (ไม่มีกติกาห้ามชัดเจนที่ตรงเขต
เขียนของสายนี้ และการปล่อยพังไว้จะบล็อกทุกรอบต่อไปที่เพิ่ม design skip ใหม่)

**MOB_AI_PLAYER_DAMAGE_WIRING** ยังคง ON HOLD เหมือนเดิม — ไม่มีอะไรใน PR นี้
เรียก Door B รอ (ก) LANE-GM เปิด `attr_wire.FULL_BLOCK_UNLOCK_CONFIRMED` (b'')
(ข) chief's read point `current_named_attr_values` (ค) `MOB_HIT_FRAME_CONFIRMED`
ฝั่งนี้เอง

## nonclaims

ไม่มีอะไรถึงจอผู้เล่นจากรอบนี้ · `mob_hit_frame.py` compose ศูนย์ไบต์วันนี้ ·
ไม่ได้แก้ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`

## สภาพแท่นตอนจบ

listener 0 · canonical sha ไม่ขยับ (ไม่แตะ canonical DB)

PR: `pirate-force-server#697` เปิดแล้ว มี marker ยืนยันด้วย GET รอ gate
