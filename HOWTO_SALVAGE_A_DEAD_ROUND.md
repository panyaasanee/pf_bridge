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

> ⚠️ การ์ดใบนี้เคยพังมาแล้วหนึ่งครั้ง อ่านข้อ 6 ก่อนพึ่งมันในรอบที่ไม่มีคนเฝ้า

## 6. 🔴 2026-08-21 — การ์ดกันรอบตาย ตายเสียเอง (และตอนนี้มี parse gate แล้ว)

`TEMPLATE_boot_writes_paired_teardown.ps1` ขึ้นชั้นตอน 08-20 21:59 และถูกใช้จริงครั้งแรกราวสามชั่วโมงต่อมา
ใน **รอบใหญ่ #11 ที่ไม่มีคนเฝ้า** (จ็อบ 949 · GT-039) — teardown ที่มันสร้างให้ (`950_gt039_teardown.ps1`)
**parse ไม่ผ่านตั้งแต่บรรทัดแรก ๆ**:

```
At ...\inbox\950_gt039_teardown.ps1:16 char:12
+ 2026-08-21 02:05:45
Unexpected token '02:05:45' in expression or statement.
=== exit 1 ===
```

**สาเหตุจริง ไม่ใช่ "ลืมใส่ `#`"** — ลืม `#` เป็นแค่อาการ ตัวต้นเหตุคือ **ลำดับความสำคัญของตัวดำเนินการ**:
ใน PowerShell เครื่องหมาย `,` **ผูกแน่นกว่า** `+` ดังนั้นบรรทัดในตัวสร้างที่เขียนว่า

```powershell
$lines = @(
    '# boot stamp : ' + $Stamp,     # <- ผิด
    '$tpl       = ' + (Esc $tpl),   # <- ผิดเหมือนกัน
)
```

ไม่ได้ถูกอ่านว่า `('# boot stamp : ' + $Stamp)` เป็นสมาชิกเดียว แต่ถูกอ่านว่า
`( ..., '# boot stamp : ' ) + ( $Stamp, '# scenario   : ' ) + ...` ซึ่งเป็น **การต่ออาร์เรย์** และการต่ออาร์เรย์จะ **แบนราบ**
⇒ คีย์กับค่ากลายเป็น **สมาชิกคนละตัว** ⇒ `WriteAllLines` (หนึ่งสมาชิก = หนึ่งบรรทัด) เขียนมันเป็น **คนละบรรทัด**
⇒ ค่าไปตกที่คอลัมน์ 0 โดยไม่มี `#` นำหน้า ⇒ PowerShell อ่าน timestamp เป็นโค้ด
`+` ทุกตัวในอาร์เรย์แตกหนึ่งบรรทัดเป็นสองบรรทัด (บรรทัด `# boot job` มี `+` สองตัว จึงแตกเป็นสาม)

**รอบนี้รอดเพราะผู้เทสเห็น `exit 1` แล้วปิดรอบเองด้วย `TEMPLATE_teardown_generic.ps1` (จ็อบ 951)**
ถ้าเชื่อการ์ดแล้วเดินจากไป รอบจะตายพร้อมเซิร์ฟเวอร์ที่ยังเปิดอยู่ — **ซึ่งคือสถานการณ์เดียวกับที่การ์ดใบนี้ถูกสร้างมาเพื่อกัน**

### แก้แล้วอย่างไร

1. **ทุกสมาชิกของอาร์เรย์ถูกครอบด้วย `( )`** — ห้ามมี `+` ระดับบนสุดใน `@( )` อีก (เขียนกฎไว้ในหัวไฟล์)
2. 🔴 **PARSE GATE** — ก่อนเขียนไฟล์ ข้อความทั้งก้อนถูกส่งเข้า `[scriptblock]::Create($text)` ใน try/catch
   **ถ้า parse ไม่ผ่าน = ไม่เขียนไฟล์เลย** แล้วแจ้งเลขบรรทัดกับข้อความ error ออกมาดัง ๆ
   งานที่ parse ไม่ผ่าน **ต้องไม่มีวันแตะดิสก์**
3. **HEADER GUARD** — ทุกบรรทัดในบล็อกหัวไฟล์ที่สร้างขึ้นต้องขึ้นต้นด้วย `#` (บั๊กคืนนี้ในรูปของ assertion)
4. **NEWLINE GUARD** — สมาชิกใดมี CR/LF ฝังอยู่ = ปฏิเสธ (หนึ่งสมาชิก = หนึ่งบรรทัด เสมอ)
5. **NAME GUARD** — `-TeardownName` ต้องเป็นชื่อไฟล์ธรรมดา `[A-Za-z0-9._-]` และ path ที่ resolve ได้ต้องอยู่ใน `staged\`
   ⇒ ไม่มีทางถูกบังคับให้เขียนลง `inbox\`
6. **ASCII GATE ขยายให้ครอบ `BootBase` / `Tpl` / `Now`** ซึ่งเมื่อก่อนไม่เคยถูกตรวจเลย
7. **การปฏิเสธเป็น terminating error + `$LASTEXITCODE = 41`** ไม่ใช่ warning แล้วไปต่อ
   (boot job ที่จำเป็นต้องรอดต้อง `try/catch` เองและประกาศออกมาว่ารอบนี้ต้องปิดด้วยมือ)

### และมีเทสที่ **รันตัวสร้างจริง** แล้ว

`staged\SELFTEST_boot_paired_teardown.ps1` — บรรทัดสุดท้ายคือ
`SELFTEST_BOOT_PAIRED_TEARDOWN_VERDICT=PASS` / `=FAIL` (exit 1 เมื่อ FAIL)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\SELFTEST_boot_paired_teardown.ps1"
```

ครอบ: T1 ไฟล์ที่สร้างต้อง **parse ผ่าน** (เช็คด้วย `[scriptblock]::Create` — คือเช็คตัวเดียวที่จะจับบั๊กคืนนี้ได้) ·
T2 ค่า metadata ถูกต้องและอยู่บรรทัดเดียวกับคีย์ + boot stamp ที่ฝังไว้ **ปฏิเสธ stamp ของรอบอื่นจริง (exit 12)** ·
T3 metadata ที่เป็นพิษ (ช่องว่าง, `:`, `'`, `"`, `$( )`, backtick, ขึ้นบรรทัดใหม่) ต้อง **ไม่มีวันรันโค้ดที่แทรกมา** ·
T4 ไม่มีอะไรลง `inbox\` เด็ดขาด · T5 buffer ที่จงใจทำให้พังต้อง **ถูกปฏิเสธ** ไม่ใช่ถูกเขียน
(T5 ใช้วิธี mutation — เอาบั๊ก 08-21 ใส่กลับเข้าไปในสำเนาของตัวสร้างใน `%TEMP%` แล้วดูว่าการ์ดยิงจริงไหม)

> 🟡 **บทเรียนรอบ 109 ที่จ่ายซ้ำเป็นครั้งที่สาม:** เทสที่ขึ้นชั้นโดยไม่เคยถูกรัน จะระเบิดในวันที่มันสำคัญที่สุด
> **ไฟล์เทสข้างบนนี้ยังไม่เคยถูกรันบนเครื่อง Windows จริง** ณ ตอนที่เขียนหน้านี้ — ต้องรันหนึ่งครั้งแล้วบันทึกผล
> ก่อนจะถือว่าการ์ดชุดนี้ "พิสูจน์แล้ว"

## 7. 🔴 รอบที่ไม่มีคนเฝ้า: รัน preflight ก่อนเสมอ

คืนเดียวกัน (รอบใหญ่ #11 · GT-031) เสียไปราว **20 นาที** กับสาเหตุที่ผู้เทส **แก้เองไม่ได้เลย**:
หน้าต่าง **`Administrator: Windows PowerShell`** ที่ยกระดับสิทธิ์ (elevated) และอยู่บนสุด วางทับกลางจอที่ `L234 T234 R1227 B753`
Windows (UIPI) ห้าม process ธรรมดาแตะหน้าต่าง elevated **ทุกช่องทาง** และผู้เทสวัดมาครบสามทาง ไม่ใช่เดา:

| วิธี | ผลที่วัดได้ |
|---|---|
| คลิกปุ่ม minimize ด้วย computer use | ไม่มีอะไรเกิดขึ้น |
| `ShowWindow(SW_MINIMIZE)` (จ็อบ 953) | เรียกได้ แต่ **ไม่มีผล** |
| `SetWindowPos` ย้ายออก (จ็อบ 954) | **`False` · `lastError=5` = ACCESS DENIED** |

ย้าย**หน้าต่างเกม**แทนได้สำเร็จ (เกมเป็น process ธรรมดา) แต่ **เกมก็ยังไม่รับคลิกอยู่ดี**

⇒ ให้ลำดับ boot ของรอบใหญ่เพิ่ม **สองบรรทัดนี้เป็นอย่างแรก** ก่อนจะเปิดเซิร์ฟเวอร์หรือ client:

```powershell
& 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\TEMPLATE_preflight_unattended.ps1'
if ($LASTEXITCODE -ne 0) { Write-Host 'PREFLIGHT FAILED - not booting this round'; exit $LASTEXITCODE }
```

`staged\TEMPLATE_preflight_unattended.ps1` **อ่านอย่างเดียว** — ลิสต์หน้าต่าง top-level ที่มองเห็นทุกบาน
พร้อม title / process / rect / TOPMOST / MINIMIZED / ทับจุดกึ่งกลางจอหรือไม่ แล้ว**ยกเลิกรอบพร้อมรายชื่อ**
ถ้าเจอหน้าต่าง elevated · มันไม่ย้าย ไม่ย่อ ไม่ปิด ไม่ kill อะไรทั้งนั้น (คลาส interop ของมันประกาศเฉพาะฟังก์ชันอ่าน)

**exit code:** `0` ปกติ · `61` เจอหน้าต่าง elevated · `62` มีหน้าต่างที่ **ตัดสินไม่ได้** ว่า elevated หรือไม่ · `63` enumerate ไม่สำเร็จ

> 🔴 **"ตัดสินไม่ได้" ถือเป็น finding ไม่ใช่ "ผ่าน"** — การที่อ่าน token ของ process ไม่ได้ **คืออาการปกติของ elevated เอง**
> (`OpenProcess`/`OpenProcessToken` โดนปฏิเสธ) ไม่ใช่หลักฐานว่าปลอดภัย · ถ้าจะยอมรับความเสี่ยงต้องพิมพ์
> `-UndeterminedIsWarning` ออกมาเอง เพื่อให้มันถูกบันทึกว่ามีคนตัดสินใจ ไม่ใช่ระบบเดาให้
> การปัดค่าที่ไม่รู้ให้เป็น "ปลอดภัย" คือรูปแบบความผิดพลาดที่โปรเจกต์นี้จ่ายค่ามันซ้ำ ๆ (BOM ในไฟล์ flag รอบ 109,
> info file เก่าในจ็อบ 145, การ์ด teardown ที่ไม่เคยถูกรันก่อนขึ้นชั้นในจ็อบ 950)

**และเรื่องที่ preflight แก้ให้ไม่ได้:** ถ้าเจอ elevated window ต้องให้ **คนจริง ๆ** ปิดหรือย่อมันก่อนไปนอน
ผู้เทสไม่มีทางแก้เองได้เลย — นี่คือข้อเสนอที่ผู้เทสส่งถึง Panya โดยตรงในใบ 20260821_0250
