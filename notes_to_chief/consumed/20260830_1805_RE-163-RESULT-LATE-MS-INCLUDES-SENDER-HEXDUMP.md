[ถึง: chief (ผู้รับผล RE) · cc: LANE-B, COO, Panya | จาก: Codex RE runner · 2026-08-30T18:05+07:00]

# RE-163 RESULT — `late_ms` เป็น sender-schedule overrun ที่รวม full-frame hexdump ก่อนหน้า ไม่ใช่เวลาถึง client

**สถานะที่เสนอ: DONE (static, jobs 1-3 ครบ)**

- ROUND START: `2026-08-30T18:00:25.384+07:00`
- TICKET START (minute precision): `2026-08-30T18:02+07:00`
- ticket block SHA-256: `f2370a39bd57ae2b54dfcedaff5776ebca0f05ba8e9011f12b1166d7edec6e0a`
- queue SHA-256: `be99f1c5a2529545d9db2a7cf1e22c4f6c5830d19033e591f2e327eb5ecc4465`

## คำตอบสั้น

ตัวส่งจริงคือ loop ใน `current/pf_login_game_server_v141.py:7746-7780` ไม่ใช่ `runtime.py` เอง:

1. `runtime.py:4748-4754,4821` สร้าง action ตามลำดับ `MOB_DEATH_DYING(delay=0)` →
   `MOB_DEATH_DEAD(delay=hold_ms/1000)` → `MOB_LOOT_DROP(delay=0)` และคืน list ที่ compose เสร็จแล้ว
2. v141 ตั้ง `send_deadline = time.monotonic()` ครั้งเดียว (`:7746`) แล้วเดิน list **อนุกรมใน thread เดียว** (`:7747`)
3. ค่า `delay` ถูก **บวกสะสมเข้า absolute monotonic deadline** (`:7748-7752`) แล้ว sleep เฉพาะเวลาที่ยังเหลือ
   ถ้างานก่อนหน้าเลย deadline ไปแล้วจะไม่ sleep ชดเชยอีก ดังนั้นมันเป็น cumulative relative schedule ไม่ใช่
   timestamp จาก client และไม่ใช่ metadata ที่ client อ่าน
4. แต่ละ frame ส่งด้วย synchronous `c.sendall(out_frame)` ใต้ `send_lock` (`:7753-7755`) ทีละใบ ไม่มี parallel send
5. `late_ms` คำนวณ **หลัง sendall ของใบนั้น** เทียบกับ deadline (`:7760`) แล้วก่อนขึ้น action ถัดไปยังทำ
   `live()` (เปิด/เขียน/ปิดไฟล์), console print, สร้าง full hexdump, เขียน full PC/frame ลง capture และ `flush()`
   (`:7761-7780`; `hexdump()` อยู่ `:482-489`; `live()` อยู่ `:7372-7381`)

ผลคือ `MOB_LOOT_DROP(delay=0)` ใช้ deadline เดียวกับ `MOB_DEATH_DEAD`: เวลาที่หมดไปหลังส่ง DEAD กับการพิมพ์/
เขียน hexdump ของ DEAD ทั้งก้อนจึงถูกนับเป็น `late_ms` ของ LOOT เต็ม ๆ ก่อน loop จะได้เรียก `sendall()` ของ LOOT

## หลักฐานจาก capture ที่มีอยู่แล้ว

`GameClient/capture_pexile_20260830_151429/server_console_live.out.txt`
SHA-256 `a2544e736dc7ba6f8ab132d30d270c13acca71e6f61a4c615643dc8c17fa17bb`:

- kill 1: DEAD 17,857 B `late=7.8ms` ที่ L8715 → full hexdump ยาวถึง L9831 → LOOT 54 B
  `late=948.6ms` ที่ L9833
- kill 3: DEAD 17,751 B `late=3.8ms` ที่ L23802 → full hexdump ถึง L24911 → LOOT 54 B
  `late=351.1ms` ที่ L24912
- kill 4: DEAD 17,698 B `late=0.9ms` ที่ L29662 → full hexdump ถึง L30768 → LOOT 82 B
  `late=897.7ms` ที่ L30769

ความติดกันนี้ตรงกับ source path คำต่อคำ: DEAD ถูกส่งตรง deadline ก่อน แล้ว diagnostic ของ DEAD กินเวลาใน loop
ก่อน LOOT ซึ่งมี delay เพิ่มศูนย์ ค่า 351-949ms จึงวัด sender-side instrumentation/scheduling overrun อย่างน้อย
หนึ่งส่วนที่ระบุชื่อได้แน่นอน ไม่ใช่หลักฐานว่า packet ใช้เวลา 351-949ms เดินทางถึง client

## แยกสิ่งที่รวม/ไม่รวมใน `late_ms`

- **ไม่รวม:** การ compose/serialize action ใน `runtime.py` เพราะทำเสร็จก่อน v141 ตั้ง `send_deadline` ที่ `:7746`
- **รวม:** synchronous `sendall()` ของ action ปัจจุบัน, overrun จาก action ก่อนหน้า, `live()` file open/write/close,
  console output, full PC/frame hexdump, capture-file write/flush ก่อน action ถัดไป
- **ยังแยกสัดส่วนไม่ได้จาก static:** กี่ ms เป็น console, filesystem, socket/OS buffering หรือการแย่ง `send_lock`

## job checkpoints

1. **DONE — external/gamedata first:**
   - `pf_bridge/external/`: 131 files / 37,176,794 B / manifest
     `b905e9b13f3c0c87fc4d4d457f637cbbcd31426e4e4ec76d4889fe15e680971c`; exact/raw-byte search
     `CActorTask_Dead|472810|MOB_LOOT_DROP|late_ms|hold_ms|MOB_DEATH|recompose|generation` = **ไม่พบ**
   - `pf_bridge/gamedata/`: 1,109 files / 15,319,585 B / manifest
     `9ba992357c2e6a7edbd366b996a801d3b354930babf695f35b615251bce3a3ab`; search ชุดเดียวกัน = **ไม่พบ**
   - ขอบเขตผลลบ: corpus สองโฟลเดอร์ ณ SHA/manifest ข้างบนเท่านั้น
2. **DONE — scheduler/delay walk:** `runtime.py:4748-4824` → v141 sender `:7746-7780`
3. **DONE — committed capture correlation:** สาม LOOT-positive kills ตรงกับ path เดียวกันทั้งหมด

## nonclaims

1. ไม่อ้างว่า network/OS/client ไม่มี latency — ไม่มี client-receipt timestamp ในหลักฐานชุดนี้
2. ไม่อ้างว่า hexdump กินครบทุก 351-949ms; พิสูจน์ได้ว่ามันถูกนับรวมแน่ แต่แยกสัดส่วนไม่ได้โดย static
3. ไม่อ้างว่า `late_ms` ทำให้ label หมดอายุก่อนถึงจอ หรือว่าการลดค่านี้จะทำให้ป้ายกลับมาเห็น
4. ไม่อ้างว่า frame order ผิด — order เป็น DYING → DEAD → LOOT ตาม invariant และ loop เดินตามนั้นจริง
5. ไม่แก้ `current/pf_login_game_server_v141.py`; ไฟล์ frozen SHA-256
   `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`

## BUILD_IMPACT

`BUILD_IMPACT_NONE (packet-order/runtime behavior)`: ห้าม reorder LOOT จากผลนี้ และห้ามใช้ `late_ms` ปัจจุบันเป็น
network/client-arrival metric. ถ้าต้องการ telemetry ใหม่ ให้ chief ออกแบบจุดวัดในชั้นที่ไม่แก้ v141 frozen โดยแยกอย่างน้อย
`queue_wait_ms`, `sendall_duration_ms`, และ diagnostic-after-send ออกจากกัน; client-observable label ยังต้องวัดแยกตามเดิม

## input SHA-256

- `src/pirateforce_foundation/runtime.py`:
  `7a3a958ca16b404a480bf04d43a5340f87c155bc79305385fdd6cf12a48185ca`
- `src/pirateforce_foundation/mob_death.py`:
  `3bc97f227a04dfb3f7f848dbc6a8bf2af36160c35b4bb233a8ff234eca7dcd6a`
- `current/pf_login_game_server_v141.py`:
  `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- capture console: `a2544e736dc7ba6f8ab132d30d270c13acca71e6f61a4c615643dc8c17fa17bb`

