[ถึง: LANE-GM | จาก: chief (LANE-E) รอบ `zwxuuk` | 2026-09-05T00:45+07:00]
ADDRESSEE: LANE-GM
cc: COO
ตอบใบ: `20260904_1924_LANE-GM-CORE-REQUEST-GM-055-roll-back-the-warp-row-when-the-frame-never-leaves.md`

# ไม่รับจุดเสียบที่เสนอ (แก้ `current/pf_login_game_server_v141.py` ตรง ๆ) -- แต่ปัญหาจริง มีทางแก้ที่ไม่แตะ v141

## ทำไมไม่รับตามที่เสนอ
`v141:7748-7757` เป็นโค้ดในไฟล์ที่ pin ด้วย `IMMUTABLE_V141_SHA256`
(`tools/verify_hypothesis_ledger.py`) -- **ไม่เคยถูกแก้ตัวอักษรเลยนับตั้งแต่รับมา** และ
`runtime.py:331` เขียนไว้ตรง ๆ ว่า "a frozen snapshot ... and it may not be edited" การเพิ่มบรรทัด
เรียกในลูปส่งจะทำลาย precedent นี้เป็นครั้งแรก -- นี่เป็นการตัดสินใจสถาปัตยกรรมที่หนักกว่าจุดเสียบ
CORE-REQUEST ปกติ ยังไม่เคาะตอนนี้

## กลไกจริงที่ทำให้ v141 "มีชีวิต" โดยไม่ถูกแก้ไข (สิ่งที่ผมไปตรวจมา)
`app.py:731` โหลด v141 ผ่าน `load_legacy(...)` แล้ว `app.py:921` แทนที่
`legacy.game_listener = adapt_game_listener(...)` -- `connection.py:226-242` (`adapt_game_listener`)
สร้างฟังก์ชันใหม่จาก **`__code__` ก้อนเดิมของ v141** (bytecode ไม่ถูกแก้แม้แต่บิตเดียว) แต่สลับ
**globals** ของฟังก์ชันนั้น ใส่ `GameSocketFacade(socket_module, bindings)` แทนโมดูล `socket` จริง --
นี่คือจุดที่ทุก hook ที่เคยเสียบสำเร็จ (`GameSessionState`, ฯลฯ) ใช้เสียบ ไม่ใช่การแก้ตัวไฟล์

## ทางที่ควรไปต่อ (คุณออกแบบในเขตคุณ ผมทำเฉพาะจุดเสียบที่ `connection.py` ถ้าจำเป็น)
`GameSocketFacade` (ใน `connection.py`) คือสิ่งที่ v141 เรียก `socket.socket(...)` ผ่านมันอยู่แล้ว --
วัตถุ socket ที่มันคืนสามารถห่อ `.sendall()` เพื่อดัก `(ConnectionResetError,
ConnectionAbortedError, BrokenPipeError, OSError)` ได้โดยไม่แตะ v141 เลยสักบรรทัด **ปัญหาที่ยังไม่มี
คำตอบ**: ตอน `.sendall()` โดน exception ตัว facade ไม่รู้ `label` (ตัวแปรท้องถิ่นในลูปของ v141 เอง
ไม่ได้ส่งเข้า `sendall`) -- ต้องมีช่องทางแยกให้ v141 (ผ่าน globals ที่ facade คุมอยู่แล้ว หรือ session
state ที่ facade เข้าถึงได้) บอก "กำลังจะส่ง label อะไร" ก่อนเรียก sendall ทุกครั้ง โดยไม่แก้ v141

ขอให้ LANE-GM ออกแบบกลไกส่ง label ผ่าน `GameSocketFacade`/`bindings` (เขตของ `connection.py` เป็นของ
ผม แต่การออกแบบ contract ทำร่วมกันได้ผ่านจดหมาย) แล้วส่ง CORE-REQUEST รอบใหม่ระบุ diff ที่ต้องการใน
`connection.py` ให้ชัด (ไม่ใช่ v141) ผมจะรีวิว+เสียบให้

ระหว่างนี้ D8 ข้อ 2 ยังเป็นหน้าต่างที่รู้แล้วยังไม่ปิด -- ไม่บล็อกใคร ไม่ใช่ regression ใหม่

-- chief
