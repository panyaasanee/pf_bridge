[ถึง: เจ้าของ (Panya), กะ1-A | ADDRESSEE: PANYA | cc: COO | จาก: chief รอบ `g3n3jp` (R264) · 2026-08-31T13:58+07:00]
[ตอบใบ: `20260831_1350_KA1A-FINDING-continue-does-not-recover-the-socket-v141-unfreeze-would-buy-nothing-measured.md`]

# CHIEF-REPLY -- รันการทดลอง loopback ที่กะ1-A ขอแล้ว: สมมติ "continue กู้อะไรไม่ได้" วัดจริงแล้ว ยืนยัน

## สิ่งที่ทำ (static/local, ไม่แตะ v141, ไม่แตะไฟล์ src ใด ๆ)

รันการทดลองตามที่ใบ `1350` ขอพอดี: เปิด TCP loopback pair, ฝั่ง server `sendall()` เฟรมแรกสำเร็จ
แล้วฝั่ง client ปิดกลางคันแบบ RST (`SO_LINGER` on/0 ก่อน `close()` -- จำลองไคลเอนต์ที่ตายกลางคันเหมือนที่
ผู้เทสเจอ `10053`) จากนั้นฝั่ง server เรียก `sendall()` ซ้ำอีก 3 ครั้งบน **socket object เดิม** (นี่คือสิ่งที่
`continue` แทน `break` จะทำที่ `pf_login_game_server_v141.py:7752-7758`)

## ผลวัดจริง

```
send1  -> ok (เฟรมแรกเข้า OS buffer ก่อน RST มาถึง)
send2.0 -> ConnectionResetError(104, 'Connection reset by peer')
send2.1 -> BrokenPipeError(32, 'Broken pipe')
send2.2 -> BrokenPipeError(32, 'Broken pipe')
```

ทุกครั้งหลังจากที่ socket เจอ RST แล้ว `sendall()` ซ้ำ **ไม่เคยส่งถึงฝั่ง client เลยสักครั้ง** -- โยน
exception รัวทุกครั้ง (ครั้งแรกเป็น `ConnectionResetError` ครั้งถัดไปกลายเป็น `BrokenPipeError` เพราะ OS
จำสถานะ socket ตายไว้แล้ว) ไม่มีครั้งไหน "ส่งถึง" ตามที่ใบ `1350` ตั้งคำถามไว้

## สรุปต่อคำถามที่ค้าง

สมมติของกะ1-A **"[สมมติของกะ1-A ยังไม่พิสูจน์ — ต้องวัด]: continue ไม่กู้เฟรมใด ๆ คืนมา" -- วัดแล้ว: จริง**
ทาง ก (แก้ `break`->`continue` แล้วปลดแช่แข็ง v141) ยืนยันอีกครั้งว่า **ซื้ออะไรไม่ได้** ตามที่กะ1-A คาดไว้
เปลี่ยนแค่ log ที่ยาวขึ้น (พิมพ์ `SEND_FAILED` ซ้ำต่อเฟรม) ไม่ใช่การส่งถึงไคลเอนต์เพิ่ม

## ข้อจำกัดของการทดลองนี้ (ตรงไปตรงมา)

1. เป็น loopback บน Linux container นี้ ไม่ใช่ทราฟฟิกจริงผ่านเน็ตที่ทำให้ผู้เทสเจอ `10053`
   (`WSAECONNABORTED`) บน Windows -- error class ต่างแพลตฟอร์ม แต่ **กลไกเดียวกัน**: OS ทำเครื่องหมาย
   socket file descriptor ว่าตายแล้วหลัง RST/abort ครั้งแรก และปฏิเสธ `send`/`sendall` ครั้งถัดไปทุกครั้ง
   ด้วย exception คลาส "connection ตายแล้ว" เสมอ (POSIX `ECONNRESET`/`EPIPE` คู่กับ Windows
   `WSAECONNRESET`/`WSAECONNABORTED` เป็นพฤติกรรมมาตรฐานเดียวกันของ TCP stack ทั้งสองฝั่ง ไม่ใช่ quirk
   ของ Linux)
2. ไม่ได้จำลอง partial-send/`EWOULDBLOCK` บน non-blocking socket เพราะ `v141` ใช้ blocking `sendall`
   (ยืนยันจาก source ที่กะ1-A อ้างเอง) -- ไม่เกี่ยวกับคำถามนี้
3. ไม่ได้แตะ `current/pf_login_game_server_v141.py` หรือรันมันจริง เป็นการทดลองแยกต่างหากล้วน ๆ

## ผลต่อคำถามที่ยื่นให้เจ้าของ (ใบ `1201`)

ทาง ก ปิดได้แล้วด้วยเหตุผล (ไม่ใช่แค่การคาดเดา): แก้ `break`->`continue` ไม่กู้ `WORLD_CENSUS_REAPPLY`
คืนมา เหลือทางเลือกจริงสำหรับบั๊ก data-loss นี้เท่าที่ chief เห็น: (ข) เปิด connection ใหม่/reconnect
เมื่อ `INITIAL` abort ก่อนพยายามส่ง `REAPPLY` (นอกเขตของ session เดียวที่ตายไปแล้ว ต้องมี retry loop ระดับ
บนสุด ไม่ใช่แค่ exception handler ของ loop เดิม) หรือ (ค) ยอมรับว่าเป็น known-loss เดิม บันทึกไว้ ไม่แก้
(ง) แก้ที่ต้นตอ -- หาสาเหตุว่าทำไม `INITIAL` abort บ่อยตั้งแต่แรก (คนละคำถามกับใบนี้) ทั้งหมดต้องแก้ไฟล์
แช่แข็ง จึงเป็นของเจ้าของเลือกเหมือนเดิม chief แค่ปิดข้อต่อที่ยังไม่ได้วัดให้แล้วตามที่กะ1-A ขอ

## nonclaims

1. ไม่ได้อ้างว่ารู้สาเหตุว่าทำไม `INITIAL` abort เกิดตั้งแต่แรก (คนละคำถาม, ยังเปิดอยู่)
2. ไม่ได้เสนอทางแก้ให้เจ้าของเลือก (ก/ข/ค/ง ข้างบนคือตัวเลือกที่เห็น ไม่ใช่คำแนะนำว่าทางไหนดีที่สุด)
3. ไม่ได้แตะ `src/`, `tests/`, หรือ `current/` ใด ๆ -- สคริปต์ทดลองอยู่ที่ scratchpad ของรอบนี้เท่านั้น ไม่ commit

-- chief รอบ `g3n3jp`
