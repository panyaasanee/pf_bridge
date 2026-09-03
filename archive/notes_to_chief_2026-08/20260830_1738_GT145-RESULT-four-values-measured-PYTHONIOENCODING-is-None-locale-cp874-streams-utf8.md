# GT-145 RESULT — 🟢 **วัดครบสี่ค่า** · `PYTHONIOENCODING=None` · `locale=cp874` · `chcp=874` · **สตรีมเป็น `utf-8` จริง** — ตรงคำทำนายของใบทั้งสี่ข้อ

ถึง: **chief (ผู้ตัดสินว่าไฟล์ไหนผิด · ADDRESSEE: chief)** · สาย GM (ผู้ขอ `CORE-REQUEST-GM-035` · ADDRESSEE: LANE-GM) · cc COO
จาก: attended session "กะ1-A" (Panya รันโพรบด้วยมือเอง) · **OBSERVER_CONFIRMED: 2026-08-30T17:3x+07:00**

## ค่าดิบที่คัดลอกมาจากคอนโซล (mark & copy ไม่ใช่ถ่ายรูป ไม่ใช่พิมพ์ตาม)

```
PS C:\WINDOWS\system32> cd "C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject"
PS C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject> py -3 -c "import sys,os,locale;print('PF_ENC stderr=%r stdout=%r PYTHONIOENCODING=%r locale=%r' % (sys.stderr.encoding, sys.stdout.encoding, os.environ.get('PYTHONIOENCODING'), locale.getpreferredencoding(False)))"
PF_ENC stderr='utf-8' stdout='utf-8' PYTHONIOENCODING=None locale='cp874'
PS C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject> echo $LASTEXITCODE
0
PS C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject> chcp
Active code page: 874
PS C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject> py -3 -V
Python 3.14.7
```

| คีย์ | ค่า |
|---|---|
| `sys.stderr.encoding` | `'utf-8'` |
| `sys.stdout.encoding` | `'utf-8'` |
| `os.environ.get("PYTHONIOENCODING")` | **`None`** |
| `locale.getpreferredencoding(False)` | `'cp874'` |
| `$LASTEXITCODE` | `0` |
| `chcp` | `Active code page: 874` |
| `py -3 -V` | `Python 3.14.7` |

**ข้อ 4 ของใบ (จดอย่างเดียว ไม่ตีความ): หน้าต่างใหม่** — เจ้าของเปิด Windows PowerShell ใหม่จากที่เปิดปกติ (prompt เริ่มที่ `C:\WINDOWS\system32`) **ไม่ใช่หน้าต่างเดียวกับที่บูตเซิร์ฟเวอร์** (รอบนี้เซิร์ฟเวอร์ถูกบูตโดย bridge แบบ hidden window)

## เกณฑ์ผ่านชั้น wire/DB — ครบทุกข้อ

- **(ก)** `netstat` ทั้งก่อนและหลังโพรบเห็น **LISTENING ทั้ง 10188 และ 10189** (pid 30696) ⇒ วัดตอนเซิร์ฟเวอร์รันจริง
  - ก่อน: `TCP 127.0.0.1:10188 ... LISTENING 30696` · `TCP 127.0.0.1:10189 ... LISTENING 30696`
  - หลัง: สองบรรทัดเดิม
- **(ข)** บรรทัด `PF_ENC` ออกครั้งเดียว · `$LASTEXITCODE = 0` ✅
- **(ค)** สี่คีย์ครบ ไม่มีคีย์ไหนเว้นว่าง · ค่าที่ไม่ได้ตั้งเขียนเต็มว่า `None` ✅
- **(ง)** `chcp` · `py -3 -V` · คำตอบข้อ 4 บันทึกครบ ✅
- **(จ)** canonical sha เท่าเดิมก่อน-หลัง (`4FF37060...`) · `MAX_LEASE 12` · `INTEGRITY ok` · `SESSIONS_SELECTED 11` (ค่าเดิมของสำเนา ไม่มีเซสชันใหม่เพราะไม่มีไคลเอนต์) ✅
- **client-observable: N/A ตามใบ** — ไม่มีไคลเอนต์ ไม่มีล็อกอิน ไม่มีตัวละคร

## คำทำนายของใบ vs ของจริง — **ตรงทั้งสี่ข้อ**
ใบทำนาย: `PYTHONIOENCODING=None` · `locale=cp874` · `stdout=stderr=utf-8` เมื่อสตรีมต่อกับคอนโซลจริง ⇒ **ตรงหมด**

## 🔴 ใบล้าสมัย (ใบที่ 5 ในสัปดาห์นี้)
ใบฮาร์ดโค้ด canonical sha ไว้ว่าต้องได้ `673f4bfb1c35ec390d6ed3b0c1fe3f581b20c6895ace9183c86a5971bccc9708` ทั้งก่อนและหลัง — **ค่าจริงวันนี้คือ `4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454`** ตาม `CANON_SHA.txt` ซึ่งเป็นแหล่งอ้างอิงสด ⇒ ทำตามใบตรง ๆ = abort ทั้งที่ DB ไม่ได้ผิดอะไร · **ขอให้ chief แก้ใบให้อ้าง `CANON_SHA.txt` แทนการฮาร์ดโค้ด** (ใบอื่นที่ฮาร์ดโค้ด sha ควรถูกกวาดด้วย)

## nonclaims (ตามใบ — ผู้เทสไม่ตีความ chief ตัดสิน)
1. **ไม่อ้าง** ค่าของ `sys.stderr` **ภายในโปรเซสเซิร์ฟเวอร์หลัง `install_runtime_console` ทำงาน** — ตรงนั้นเป็น `_Mirror` คนละคำถาม ต้องเปิดใบใหม่
2. **ไม่อ้าง** อะไรกับ stdout ที่ถูก redirect/pipe — ใบนี้วัดกรณีคอนโซลล้วน · และไม่อ้างว่าค่านี้เท่ากับค่าบน CI
3. **ผู้เทสไม่ตีความและไม่แก้ไฟล์ใด ๆ** — สองบรรทัดล่างเป็น *ข้อสังเกตประกอบ* ไม่ใช่คำตัดสิน

## ข้อสังเกตประกอบ (chief ตัดสินเอง ไม่ใช่ข้อสรุปของผู้เทส)
- `PYTHONIOENCODING` **ไม่ได้ถูกตั้งบนสะพาน** ขณะที่ `gate-windows.yml:53` **บังคับ** `cp874:strict` บน runner ⇒ เข้าเงื่อนไข "ไม่ใช่ cp874" ของใบสำหรับตัวแปรนั้น: **CI ทดสอบสภาพที่ไม่มีอยู่บนเครื่องเจ้าของ**
- สตรีมคอนโซลเป็น `utf-8` จริงทั้งที่ code page = 874 (Python บน Windows ข้าม code page สำหรับคอนโซลจริง) ⇒ ค่าคงที่ `utf-8` ที่ `runtime_console.py:26` **บังเอิญตรงสำหรับกรณีคอนโซล** แต่มันเป็นค่าคงที่ ไม่ใช่การวัด ⇒ กรณีที่สตรีมถูก redirect/pipe (เช่น log ของ bridge job ทุกใบ) encoding จะไปตาม locale = **cp874** ซึ่งเป็น code page ไทย ⇒ อักษรไทยรอด แต่อักขระนอก cp874 จะโยน
- ทั้งสองบรรทัดข้างบนเป็นเขต chief ตัดสิน (`gate-windows.yml` และ `runtime_console.py`) ตาม nonclaim 3 ของใบ

## หลักฐาน
`outbox\1377_gt145_boot_server_only.utf8.txt` (canonical check, netstat before, SERVER UP) · `outbox\1378_gt145_stop_and_release.utf8.txt` (netstat after, FINAL listeners=0, canonical เท่าเดิม, integrity ok) · ข้อความคอนโซลคัดลอกดิบข้างบน · run DB `state\run_gt145_20260830_173326.sqlite3` (สำเนาทิ้ง canonical ไม่ถูกเปิด)

— กะ1-A · **ADDRESSEE: chief (ตัดสิน gate-windows.yml + runtime_console.py + แก้ใบที่ฮาร์ดโค้ด sha), LANE-GM (ปิด CORE-REQUEST-GM-035)**
