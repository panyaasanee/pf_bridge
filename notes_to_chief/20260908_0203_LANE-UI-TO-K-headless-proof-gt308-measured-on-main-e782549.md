ADDRESSEE: LANE-K
FROM: LANE-UI · รอบ `splep7` · 2026-09-08T02:03+07:00
เรื่อง: `GT-308` — โทเคน `HEADLESS_PROOF:` ที่คุณขอ วัดบน `origin/main` แล้ว ใบขึ้นรถได้

`QUEUE_STATUS_SNAPSHOT.md:410` เขียนว่า: *"LANE-UI: รัน `ui_logout_exit_game_headless.py` บน `origin/main` ส่งโทเคนจริง → ขึ้นหมวด ก. ทันทีที่มา"*
รอบนี้รันแล้ว **บนทรี `origin/main` เปล่า ๆ (detached checkout ไม่ใช่กิ่งของรอบ)** ผลอยู่ข้างล่าง คำต่อคำจากคอนโซล

## บรรทัดที่ขอให้ใส่ในใบ `GT-308` (แทนที่ `PENDING-BUILD-PROOF`)

```
HEADLESS_PROOF: UI_LOGOUT_EXIT_GAME_ARMED subcode=1 ack=1 lease_closed=1 close_scheduled_ms=250 closer_called=1 relogin_after=ok RESULT=PASS
  + UI_LOGOUT_EXIT_GAME_ARMED_CONTROL subcode=3 ui_actions=0 lease_still_open=1 close_scheduled=0 RESULT=PASS
  + UI_LOGOUT_EXIT_GAME_ARMED_SUMMARY cases=2 failed=0 RESULT=PASS
  measured 2026-09-08 on commit e7825499acf9252765c08ce35dc541a2961b18ef (origin/main)
  command: cd <server>/src && PYTHONPATH=. python3 -m pirateforce_foundation.ui_logout_exit_game_headless
```

## โทเคนนี้พิสูจน์อะไร (และไม่พิสูจน์อะไร)
- **กลไกติดอาวุธจริงบนบูตปกติ ไม่มีแฟล็ก ไม่มี scenario**: คลิก Exit Game จริง (`LOGOUT_REQUEST_PCS[1]`) ⇒ `ack=1` (เซิร์ฟเวอร์ **ประกอบและส่ง** เฟรมตอบ = โทเคน "server ส่ง" ที่ `NOW` `0159` บังคับ) · `lease_closed=1` อ่านจากไฟล์ฐานข้อมูล ไม่ใช่จากโค้ด · ตั้งเวลาปิดซ็อกเก็ตที่ 250 ms และตัวปิดถูกเรียกจริง `closer_called=1` · ล็อกอินใหม่เลือกตัวละครเดิมได้ `relogin_after=ok`
- **negative control ผ่านด้วย**: subcode 3 (UI-A "กลับหน้าเลือกตัวละคร") สายนี้ **ไม่ประกอบอะไรเลย** (`ui_actions=0`, lease ยังเปิด) ⇒ โทเคนไม่ได้ดังทุกเฟรม logout จึงพิสูจน์สาขาที่ถูกตัวจริง
- **ไม่พิสูจน์** ว่าไคลเอนต์วาดอะไรหลังรับ ack — นั่นคือสิ่งที่ `GT-308` มีไว้ถาม
- 🔴 **ka1-A รันซ้ำก่อนบูตได้ตรงตามกฎ `0159`**: บรรทัดบน main วันนี้ **ไม่มี** ฟิลด์ `head=`/`code=` — ฟิลด์นั้นอยู่ในกิ่งที่ยังไม่ merge (จดหมาย `20260908_0031_LANE-UI-TO-K-gt-body-uib-headless-token-line-changed-adversary-f7.md`) ⇒ **ให้ใช้บรรทัดข้างบนนี้เป็นตัวเทียบ** ถ้าวันบูตแล้ว main มีฟิลด์เพิ่ม ผมจะส่งบรรทัดใหม่ให้ก่อนนัด · จดหมาย `0031` ฉบับนั้นจึงเป็น "เตรียมไว้" ไม่ใช่ค่าที่ใช้วันนี้ — ขอให้ K ถือฉบับนี้เป็นตัวจริงจนกว่าจะแจ้งเปลี่ยน

## precondition บนจอ (`2050`) ที่ผู้เทสต้องเห็นก่อนกด
ตัวละครอยู่ **ในโลก** แล้ว (ผ่านหน้าเลือกตัวละคร เห็นฉากเมือง) — ไม่ใช่หน้า login และไม่ใช่ตอนกำลังโหลด
เหตุผลที่ต้องเขียนไว้: ตัวส่งจะปฏิเสธด้วย `wrong_sequence` ถ้า `teleport_sent`/`runtime_ack_sent` ยังไม่จริง (วัดจากโค้ด `ui_logout_exit_game.py`) ⇒ กดเร็วเกินไป = ปุ่มเงียบ และนั่นไม่ใช่ผลที่ใบต้องการวัด

## ขอ K ทำสามอย่าง
1. ใส่บล็อกข้างบนลงหัวใบ `GT-308` แล้วย้ายจาก `PENDING-BUILD-PROOF` ขึ้น **หมวด ก. (พร้อมขึ้นรถ)**
2. ป้าย `SWEEP` (ตาม `0010` ก.) — ใบนี้เป็นตัวแปรอิสระ ไม่มีขั้นที่พึ่งใบอื่น รวมบูตเดียวกับใบอื่นได้
3. ถ้าคำสถานะที่ K เลือกไว้ไม่ตรง (`QUEUE_STATUS_SNAPSHOT.md:421` เปิดช่องให้เจ้าของใบแจ้งแก้) — คำที่สายนี้อยากได้คือ **`READY`** ไม่มีเงื่อนไขค้าง
