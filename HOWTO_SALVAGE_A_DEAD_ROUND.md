# HOWTO: กู้หลักฐานจากรอบที่ตายไปแล้ว (salvage a dead round)

หน้านี้อ่านตอนที่ "รอบเทสจบไปแล้ว แต่ไม่มีใครปิดรอบ" เท่านั้น
ถ้ารอบยังเปิดอยู่และคุณกำลังจะปิดตามปกติ ให้ใช้ teardown ปกติ ไม่ต้องอ่านหน้านี้

## 1. รอบที่ตายแล้วหน้าตาเป็นยังไง

อย่างน้อยหนึ่งข้อ: เทสรันไปหลายชั่วโมงแล้วเงียบไปโดยไม่มีใครรัน teardown /
`pf_bridge\outbox\` ไม่มี `*_teardown*.utf8.txt` ของรอบนั้น / port 10188/10189 ยังค้าง /
รัน teardown แล้วมันปฏิเสธว่า:

```
ABORT(12): boot stamp is 605.2 min old (> 420) - stale round
```

**ยังอยู่บนดิสก์:** server console log, capture tree, run-copy DB, client stdout/stderr
**หายไปตลอดกาล:** ทุกอย่างที่ teardown ต้องวัด "ณ วินาทีที่รอบจบ"

## 2. คำสั่งที่ต้องรัน

เปิด PowerShell แล้วรัน (บรรทัดเดียว):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\TEMPLATE_teardown_generic.ps1" -Salvage
```

ถ้ารอบนั้นมี paired teardown ที่ boot job เขียนไว้ให้แล้ว (ไฟล์ `staged\<NNN>_<gtid>_teardown.ps1`)
ใช้อันนั้นแทนได้ และง่ายกว่า เพราะมันเติม scenario / boot stamp / run DB ให้แล้ว:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\127_gt016_teardown.ps1" -Salvage
```

**อย่าเอาไฟล์ที่ใส่ `-Salvage` ไปวางใน `inbox\`** — inbox รันด้วย `powershell -File <job>.ps1` เฉย ๆ ไม่มี argument
ดังนั้น `-Salvage` จะไม่ถูกส่ง แล้วมันจะกลายเป็น teardown ปกติที่ปฏิเสธด้วย exit 12

`-Salvage` **อ่านกับคัดลอกอย่างเดียว**: ไม่ kill process, ไม่แตะ DB, ไม่ปลด port, ไม่เขียนอะไรนอก `outbox\`
ถ้า port ยังค้างอยู่ มันจะบอก แล้วให้คุณรัน `staged\TOOL_stop_stale_server.ps1` เองทีหลัง

## 3. จะได้อะไรกลับมา

ไฟล์ `pf_bridge\outbox\SALVAGE_<jobtag>_<stamp>.txt` (+ `SALVAGE_..._console_tail_....txt` ถ้ามี console log)
บรรทัดแรกของไฟล์เขียนว่า `SALVAGE RECEIPT - DEGRADED EVIDENCE - THIS IS NOT A TEARDOWN RECEIPT`

**ได้ (เท่าที่ยังอยู่บนดิสก์):**

- server console log: ขนาด, mtime, จำนวน `Traceback`, จำนวน `listener ready` / `[FOUNDATION] stopped`, และ tail 400 บรรทัดสุดท้าย
- run-copy DB: path, ขนาด, mtime, sha256, และมี `-wal` / `-shm` ค้างไหม
- listener บน 10188/10189 **ณ เวลาที่กู้** พร้อม pid/parent
- capture tree: จำนวนไฟล์ + 12 ไฟล์ที่ใหญ่ที่สุด, GAME_LIVE.txt, GAME_EVENTS_LIVE.txt
- canonical DB sha เทียบกับ `CANON_SHA.txt`

**ไม่ได้ และจะไม่มีวันได้ (ทุกข้อขึ้นต้นด้วย `MISSING:` ในไฟล์):**

- DB snapshot ณ วินาทีที่รอบจบ (session counts / lease generation / integrity_check / fk_check)
- หลักฐานว่า server ปิดตัวเรียบร้อย (`*_ctrlc_*.json`) — ไม่เคยมีใครส่ง ctrl-c
- สถานะ process และ listener ตอนจบรอบ (มีแค่ ณ เวลาที่กู้)
- teardown receipt ของรอบนั้น

> รอบที่มีแค่ salvage receipt คือรอบ **degraded** — ใช้ประกอบ finding ได้ แต่ **ปิด hypothesis เดี่ยว ๆ ไม่ได้**
> `-Salvage` จบด้วย **exit 20** ไม่ใช่ 0 โดยตั้งใจ: มันต้องไม่ดูเขียว

## 4. ทำไม path ปกติถึงยังปฏิเสธอยู่

เพราะ teardown ที่รันช้าไปหลายชั่วโมงจะประทับหลักฐานที่ดู "สด" ลงบนรอบที่เย็นไปแล้ว
และ ctrl-c ที่ส่งช้าขนาดนั้นอาจไปโดน process ที่ไม่ใช่ของรอบนั้นอีกต่อไป — การปฏิเสธจึงถูกแล้ว
บั๊กคือมันปฏิเสธ *แล้วทิ้งหลักฐานที่ยังอยู่บนดิสก์* ซึ่ง `-Salvage` แก้ให้แล้ว

เพดานอายุถูกขยับจาก 180 เป็น **420 นาที** เพราะรอบ attended 2-3 ชั่วโมงคือเรื่องปกติของโปรเจกต์นี้
(รอบที่โดนปฏิเสธเมื่อ 2026-08-20 อายุ 185.7 นาที คือรอบที่จบปกติ แค่ยาว)
การขยับนี้ไม่ได้ทำให้กันของเก่าอ่อนลง เพราะตัวที่กันจริง ๆ คือ exit 15 (console pid ต้องเป็น parent ของ process ที่ถือ port อยู่ตอนนี้) ซึ่งไม่มีนาฬิกาเข้ามาเกี่ยวเลย

## 5. อย่าให้ต้องใช้หน้านี้อีก

ให้ boot job เขียน teardown ของตัวเองตอน boot สำเร็จ — `staged\TEMPLATE_boot_writes_paired_teardown.ps1`
เติม job number / boot stamp / scenario / run DB ให้เสร็จตั้งแต่ตอนนั้น
ปิดรอบเหลือแค่ **copy ไฟล์เดียวลง `inbox\`** ไม่มีอะไรให้กรอก ไม่มีอะไรให้จำ
