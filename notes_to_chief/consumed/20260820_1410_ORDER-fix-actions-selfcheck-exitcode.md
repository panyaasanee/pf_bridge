# 🔴 คำสั่ง Panya 2026-08-20 ~14:10 — Actions run #1 แดง **เพราะบั๊กในตัว workflow เอง ไม่ใช่เพราะรีโป**

## เกิดอะไรขึ้น
Panya push `2de7d11` แล้ว `gate-windows` **run #1 = Failure ใน 24 วินาที**

ขั้นที่พัง: **`SELF-CHECK - prove both tripwires are armed before trusting them`** (0s)
log ของขั้นนั้นทั้งหมด:
```
self-check 1 PASS: native exit codes propagate
self-check 2 PASS: U+1F534 kills the process (exit 1) - cp874 is armed
Error: Process completed with exit code 1.
```

⇒ **self-check ทั้งสองข้อ PASS** แล้ว **ขั้นนั้นถึงค่อยแดง** — ไม่มี `throw` ไม่มีข้อความ error ของเราเลย

## Root cause (แน่นอน อ่านจากโค้ดของ workflow เอง บรรทัด 149-172)
คำสั่ง native ตัวสุดท้ายของขั้นนี้คือ **การจงใจทำให้ล้มเพื่อพิสูจน์ tripwire**:
```powershell
py -3 -c "print('\U0001F534')" 2>&1 | Out-Null   # <- ตั้งใจให้ exit 1
if ($LASTEXITCODE -eq 0) { throw '... tripwire is DISARMED' }
Write-Host "self-check 2 PASS: ..."
# <- ขั้นจบตรงนี้ โดยที่ $LASTEXITCODE ยังเป็น 1
```
ตัว wrapper ของ Actions สำหรับ `shell: pwsh` **จบ step ด้วย `$LASTEXITCODE`**
⇒ `Write-Host` ไม่ได้รีเซ็ตค่านั้น ⇒ **step แดงทั้งที่ตรรกะข้างในผ่านหมด**

**นี่คือ false red ที่เราสร้างเอง** — ตรงข้ามกับบทเรียน "false green" ของรอบ 142 พอดี

## แก้ (หนึ่งบรรทัด)
ปิดท้าย step `SELF-CHECK` ด้วยการรีเซ็ตรหัสจบให้ชัดเจน:
```powershell
          Write-Host "self-check 2 PASS: U+1F534 kills the process (exit $LASTEXITCODE) - cp874 is armed"

          # Both self-checks passed. The last native command exited 1 ON PURPOSE
          # (that is what proves the tripwire). The pwsh step wrapper exits with
          # $LASTEXITCODE, so without this line the step reports a failure that
          # its own log says did not happen. Reset explicitly.
          exit 0
```

🔴 **ตรวจทั้งไฟล์ด้วย ไม่ใช่แก้จุดเดียว** — ขั้นไหนก็ตามที่จบด้วยคำสั่ง native ที่ตั้งใจให้ล้ม
(หรือมี `| Out-Null` ปิดท้าย) มีบั๊กเดียวกัน · ขั้น `cp874 static tripwire` และ `THE GATE`
ยังไม่เคยได้รัน ⇒ **ยังไม่รู้ว่ามันมีปัญหาเดียวกันไหม**

## ที่ผมเดาผิด (บันทึกไว้กันคนอ่านผิดทีหลัง)
ผมทายว่าน่าจะพังที่ `chcp 874` เพราะ runner เป็นภาษาอังกฤษ — **ผิด**
ขั้น `Assert the environment is the one we think it is` **ผ่านใน 1 วินาที**
⇒ **`windows-latest` รองรับ cp874 ได้จริง และ `py -3` ชิมทำงานถูก** (3.14 series · stdout = cp874 strict)
เป็นข่าวดี: สมมติฐานหลักของ workflow นี้ยืนได้บนเครื่องของ GitHub

## ขั้นที่ผ่านแล้วจริง (run #1)
Set up job · Checkout (fetch-depth 0, 6s) · setup-python 3.14 · py-3 shim · pip install pytest/capstone/pefile (11s) · **Assert the environment (cp874 + 3.14 + stdout strict)**
⇒ โครงพื้นฐานของ workflow **ใช้ได้หมด** เหลือแค่บั๊กรหัสจบ

## 🔴 ข้อ 5 ของเช็คลิสต์ยัง **ไม่ผ่าน**
*"ต้องเห็น Actions แดงจริงหนึ่งครั้งแล้วเขียวกลับ"* หมายถึง **แดงเพราะข้อบกพร่องจริงในรีโป**
run #1 แดงเพราะท่อของตัวเอง ⇒ **ไม่นับ** · ยังต้องทำ deliberate red ตามแผนเดิมอยู่
ลำดับที่ Panya ต้องการ: **แก้ให้เขียวก่อน → แล้วค่อยจงใจทำให้แดง → แล้วเขียวกลับ**

## ขอบเขตของรอบนี้
- แก้ `.github/workflows/gate-windows.yml` (+ `README_GATE_CI.md` ถ้าต้องอธิบายเพิ่ม) เท่านั้น
- 🔴 **ห้าม push** เหมือนเดิม — Panya push เอง
- ถ้าเสร็จเร็ว **จบรอบเลย** อย่าหยิบงานอื่น (คำสั่ง 12:30 ยังมีผล)
