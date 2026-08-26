[ถึง: chief · cc: COO | จาก: LANE-GM · 2026-08-27T06:05+07:00]
ตอบเติม: `20260827_0524_LANE-GM-CORE-REQUEST-proposed-007-...md`

# LANE-GM ส่วนเติม — ผล `pf-adversary` รอบนี้ + คำถามเปิดสำหรับตอนต่อสาย 007

## สิ่งที่แก้แล้วในคอมมิตต่อ (ก่อน chief อ่านใบนี้)
1. **`docs/PYTEST_SKIP_PINS.json` ไม่มีแถวของ `tests/test_gm_scene_catalog.py`** — เกตจริง (เครื่อง Windows ไม่มี `pf_bridge` sibling) จะ skip เทสนั้นแบบไม่ pin ⇒ census แดง — เติมแถวแล้ว
2. **`gm/command_capture.capture_raw_command` เดิมรับ `is_gm: bool` จาก caller ตรง ๆ** — เสี่ยงต่อ wiring บั๊กในอนาคต (cache ค่าไว้ครั้งเดียวต่อ connection แล้วไม่เช็คซ้ำ) ⇒ เปลี่ยนให้ฟังก์ชันรับ allowlist แล้วเรียก `accounts.is_gm` เองทุกครั้ง ไม่มี caller ที่ต้องแก้เพราะยังไม่มี caller จริง (GM-003 ยังไม่เริ่ม)
3. **`is_gm()` ไม่มี guard เรื่อง `bool` ผสมกับ `int`** (Python `True == 1`) — เติม guard ให้เหมือนฝั่ง `load_gm_accounts` แล้ว
4. **`tools/pf_mine_gm_scene_catalog.py` พิมพ์ error ด้วย `%r` ตรง ๆ** — ถ้าตารางต้นทางเสียหายจนชื่อฉาก 1-4 มีอักขระนอก cp874 เครื่องมือจะ crash กลางทางแทนที่จะพิมพ์ `REFUSED:` ⇒ เปลี่ยนเป็น `ascii()` แล้ว
5. `.gitignore` ไม่มีบรรทัด allowlist ให้ `tools/pf_mine_gm_scene_catalog.py` ตอนเริ่มรอบ (พบก่อน commit แรก แก้แล้วในคอมมิตแรก)

## 🔴 คำถามเปิดที่ยังไม่แก้ ขอให้ chief ตัดสินตอนต่อสาย 007
`accounts.load_gm_accounts` คืน `frozenset` (โหลดครั้งเดียว ใช้ร่วม) — **แต่ไม่มีที่ไหนในเลนนี้บอกว่า runtime.py ควรเช็ค allowlist ใหม่บ่อยแค่ไหนหลัง login** ถ้า wiring โหลดครั้งเดียวตอนบูตแล้วผูกผลไว้กับ connection object ตลอดอายุ session การถอด account ออกจาก `gm_accounts` กลางคันจะไม่มีผลจนกว่าเซิร์ฟเวอร์ restart
`gm/command_capture.py` แก้ไม่ให้เป็นปัญหาฝั่งจับแพ็กเก็ตแล้ว (ข้อ 2 ข้างบน) แต่ฝั่ง **การส่ง `GM_UpdateGMStateVital` ตอน revoke** (`for_gm_revoke` มีอยู่แล้ว แต่ไม่มีใครเรียก) เป็นคนละคำถามที่ CORE-REQUEST-007 ยังไม่ได้ตอบ — ขอให้ chief ตัดสินใจตอนต่อสายว่า runtime.py เช็คซ้ำต่อแพ็กเก็ตหรือต่อ session-refresh อะไร

## สิ่งที่รับไว้เป็นความเสี่ยงต่ำ ไม่แก้รอบนี้
`tools/pf_mine_gm_scene_catalog.py` ตรวจแค่ 4 จาก 330 แถว (scene id 1-4) เป็น control — แถวอื่นไม่มีการ์ดเกินกว่า "3 คอลัมน์เป๊ะ" กับ "ไม่มี n_ID ซ้ำ" ความเสี่ยงคือชื่อฉากผิดหนึ่งแถวในเมนู GM ไม่ใช่ช่องโหว่ความปลอดภัย ⇒ ปล่อยไว้ บันทึกใน `docs/GM_LANE.md`

## ยืนยันจาก pf-adversary ว่าไม่มีปัญหา (ไม่ต้องขุดซ้ำ)
allowlist fail-closed จริง (env ว่าง/ไฟล์หาย/JSON เพี้ยน/ไม่ใช่ list/มี `true`/`false` ปนใน list ⇒ set ว่างเสมอ) · `state_wire.py` ตรงกับแถวจริงใน `PF_SERIALIZER_FIELDS.tsv` (เช็คแล้วบรรทัดต่อบรรทัด) · `scene_catalog.py` เป็น ASCII จริง (Thai เป็น `\uXXXX` escape) · sha/row-count re-derive ได้จริงจากสะพาน · ไม่มี shell/path injection · `command_capture` ไม่ตีความ payload จริง

— LANE-GM
