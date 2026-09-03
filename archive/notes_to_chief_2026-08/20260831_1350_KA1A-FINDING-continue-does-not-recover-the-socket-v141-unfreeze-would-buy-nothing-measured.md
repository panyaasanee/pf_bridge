[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: เจ้าของ, COO | จาก: กะ1-A (attended) · 2026-08-31T13:50+07:00]
[ตอบใบ: `20260831_1201_CHIEF-ASK-PANYA-v141-sendall-break-drops-census-reapply-on-abort.md`]

# FINDING — ข้อสรุปเชิงสาเหตุของใบ 1201 มีข้อต่อที่ยังไม่ได้วัด: `continue` ไม่กู้ socket ที่ตายแล้ว

## สิ่งที่วัดจริง (static, อ่านไฟล์สด ไม่ใช่สำเนา)

`Pirate Force ServerProject/current/pf_login_game_server_v141.py:7752-7758` — md5
`7fcdf7d2b80326311a1edf8bc7b4803d` ตรงกับสำเนาใน `adhoc_actorattr_probe/tree/` ทุกไบต์ (ไฟล์เดียวกัน)

```
try:
    with send_lock:
        c.sendall(out_frame)
except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError) as e:
    print(f"[G!] send failed: {e!r}")
    f.write(f"SEND_FAILED {label} {e!r}\n")
    break
```

## ข้อต่อที่ยังไม่ได้พิสูจน์

ใบ 1201 อ้างว่า "ถ้า `INITIAL` abort แล้ว `REAPPLY` ในคิวเดียวกันก็ไม่ถูกส่งด้วย เพราะ `break`" —
ข้อเท็จจริงส่วนนี้ถูก แต่ **ข้อสรุปว่าแก้เป็น `continue` แล้ว `REAPPLY` จะถึงไคลเอนต์ ยังไม่มีการวัด**

ทั้งสี่คลาสที่ดักไว้ (`ConnectionResetError`, `ConnectionAbortedError`, `BrokenPipeError`, `OSError`
บน blocking `sendall`) คือ **การตายของ connection ทั้งสิ้น** ไม่ใช่ transient/partial-send —
`sendall` บน blocking socket ไม่โยน `EWOULDBLOCK` `WSAECONNABORTED (10053)` ที่ผู้เทสเจอ แปลว่า
สแตกฝั่งโฮสต์ทิ้ง connection นั้นไปแล้ว การวนต่อด้วย `continue` จะยิงลง socket เดิมที่ตายแล้ว
คาดว่าได้ `SEND_FAILED` ซ้ำทุก action ที่เหลือ **ไคลเอนต์ยังไม่ได้รับอะไรเพิ่ม** — เปลี่ยนความละเอียด
ของ log ไม่ใช่เปลี่ยนการส่งถึง

[สมมติของกะ1-A ยังไม่พิสูจน์ — ต้องวัด]: `continue` ไม่กู้เฟรมใด ๆ คืนมา

## ผลต่อคำถามที่ยื่นให้เจ้าของ

ถ้าสมมตินี้จริง **ทาง ก (แก้ `break`→`continue` แล้วปลดแช่แข็ง v141 เป็นครั้งแรก) ซื้ออะไรไม่ได้เลย** —
จ่ายด้วยการเปิดข้อยกเว้นถาวรให้ไฟล์ที่ไม่เคยมีข้อยกเว้น แลกกับ log ที่ยาวขึ้น จึงไม่ควรให้เจ้าของ
เคาะเลือกระหว่าง ก/ข จนกว่าจะปิดข้อต่อนี้ก่อน

## ที่ขอ (ราคาถูก ไม่ต้องปลดแช่แข็ง ไม่ต้องใช้เครื่องเจ้าของ)

หนึ่งการทดลอง static/local: จำลอง socket ที่ถูก abort แล้วเรียก `sendall` ซ้ำ (loopback + ปิดฝั่ง
ไคลเอนต์กลางคัน) ดูว่าการเรียกครั้งที่ 2..n ส่งถึงหรือโยนซ้ำ — ตอบได้ในรอบเดียวโดยไม่แตะ v141
ผลออกมาแล้วค่อยเสนอเจ้าของว่าเหลือทางเลือกจริงกี่ทาง

## nonclaims

1. ไม่ได้อ้างว่าใบ 1201 ผิดทั้งใบ — ข้อเท็จจริงเรื่อง `break` ถูกต้อง ที่ค้านคือข้อสรุปเชิงกู้คืน
2. ไม่ได้อ้างว่า `RE-167` ทำงานพลาด — เป็น static read ที่ถูกต้องในขอบเขตของมัน
3. ไม่ได้เสนอให้ปิดคำถามเรื่องเฟรมสำมะโน ~20 KB — นั่นเป็นคนละตั๋วและยังเปิดอยู่
4. ไม่ได้แตะไฟล์ใด ๆ ทั้ง `src/` และ `current/` — อ่านอย่างเดียว

— กะ1-A (ผู้เทส attended)
