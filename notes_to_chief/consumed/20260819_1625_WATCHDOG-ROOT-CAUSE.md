# จากเซสชันหลัก ATTENDED (บัญชีใหม่) → chief · 2026-08-19 ~16:25

**provenance:** Panya สั่งในแชตให้ตรวจ watchdog · ผู้เทสรันจ็อบ 900/901 ผ่าน bridge · Panya เคาะ
"แก้เต็ม + ปลุกคอม" เมื่อ ~16:19 · **ไม่ได้ถือธงใดทั้งสิ้น** (แค่วางจ็อบลง inbox)

---

## 1) 🔴 แก้ข้อสรุปใน SHIFT_HANDOFF_20260819.md ข้อ 5.1 — "watchdog ไม่ทำงานจริง" **ผิด**

เอกสารส่งกะสรุปว่า watchdog พัง เพราะ `watchdog.log` ค้างที่ 2026-08-18 23:50
**แต่ watchdog เขียน log เฉพาะตอนที่ "ต้องปลุก bridge" เท่านั้น** — ถ้า bridge ยังอยู่ มันเงียบโดยตั้งใจ
⇒ log ที่ว่างคือหลักฐานว่า **bridge ยังมีชีวิตตลอด** ไม่ใช่หลักฐานว่า watchdog ตาย

**หลักฐานจริงจากจ็อบ 900 (16:17:27):**

```
State                : Ready          Enabled             : True
LastRunTime          : 2026-08-19 14:10:01      LastTaskResult : 0
NextRunTime          : 2026-08-19 16:20:00      NumberOfMissedRuns : 25
Repeat Every         : 5 Minutes      Repeat Until Duration : Disabled (ไม่มีเพดาน)
Logon Mode           : Interactive only
Power Management     : Stop On Battery Mode, No Start On Batteries
```

**สาเหตุจริง: คอมหลับ** — `NumberOfMissedRuns=25` x 5 นาที = **125 นาที** ตรงกับช่วง
`LastRunTime 14:10` → `จ็อบ 900 รัน 16:17` พอดี · Task Scheduler **ไม่รันตอนเครื่องหลับ และไม่ตามงาน
ที่พลาดย้อนหลัง** เพราะยังไม่ได้เปิด `StartWhenAvailable`
(ยืนยันซ้ำ: watchdog รันอีกครั้ง 16:17:59 หลัง Panya เปิด bridge ด้วยมือ 16:17:25 → เจอ bridge อยู่ → เงียบ ถูกต้องแล้ว)

## 2) สิ่งที่แก้ไปแล้ว

- ✅ **patch `pf_bridge_watchdog.ps1`** ให้เขียน heartbeat ทับใหม่ทุกรอบที่
  **`pf_bridge\watchdog_last_check.txt`** (`bridge-alive` / `bridge-missing-starting` + timestamp)
  ⇒ ต่อไปแยกออกว่า "watchdog รันแล้วเจอ bridge ปกติ" กับ "watchdog ไม่ได้รันเลย"
  · backup ของเดิม: `pf_bridge_watchdog.ps1.bak_20260819` (ห้ามลบ)
- ✅ เพิ่มไฟล์ `pf_bridge\FIX_WATCHDOG_ADMIN.bat` + `fix_watchdog_admin.ps1`

## 3) ⚠️ ที่ยังทำไม่ได้จาก bridge — ต้อง elevate

จ็อบ 901 ตอบ **`SETTINGS_FAILED: Access is denied`** และ **`LOGON_TRIGGER_FAILED: Access is denied`**
— `Set-ScheduledTask` แก้ task ใน root folder ไม่ได้ถ้า process ไม่ได้ยกสิทธิ์ (bridge รันแบบ Limited)
⇒ Panya ต้องคลิกขวา `FIX_WATCHDOG_ADMIN.bat` → **Run as administrator** · ผลจะลงที่
`outbox\902_fix_watchdog_admin.out.txt`
ค่าที่จะถูกเปิด: `StartWhenAvailable` · `AllowStartIfOnBatteries` · `DontStopIfGoingOnBatteries` ·
`WakeToRun` (Panya อนุมัติให้ปลุกคอมได้) · `ExecutionTimeLimit=0` · + trigger ตอน logon

**บทเรียนสำหรับ chief:** จ็อบใดที่ต้องแก้ Task Scheduler / registry / service **จะโดน Access is denied
เสมอผ่าน bridge** — ต้องออกแบบเป็นไฟล์ให้ Panya คลิกขวารันเอง อย่าวางลง inbox แล้วคิดว่าจะผ่าน

## 4) สถานะ ณ 16:25

- PF BRIDGE: **มีชีวิต** PID 13332 เริ่ม 16:17:25 (Panya เปิดด้วยมือ)
- LOCK_GAME / LOCK_GIT: **FREE ทั้งคู่**
- inbox ว่าง · จ็อบ 900/901 จบแล้ว exit 0 ทั้งคู่
- scheduled task chief `pirate-force-chief-continue` รอบแรก **17:02**

## 5) nonclaims

- **ไม่ได้** ตรวจว่าคอมหลับเพราะอะไร (ตั้งเวลา sleep / ปิดฝา / ผู้ใช้สั่ง) — สรุปแค่ว่า **มีช่วงที่ task ไม่ถูกรัน 125 นาที**
- **ไม่ได้** ตรวจว่า bridge ตายตอนกี่โมงแน่ ๆ — รู้แค่ outbox เขียนล่าสุด 11:36 และ 16:10–16:13 ไม่มีใครหยิบจ็อบ
- **ไม่ได้** ยืนยันว่า `WakeToRun` จะปลุกเครื่องได้จริง (ขึ้นกับ BIOS/ไดรเวอร์) — ต้องรอเห็น heartbeat ข้ามคืนก่อน
- **ยังไม่ได้** รัน `FIX_WATCHDOG_ADMIN.bat` — ค่าตอนนี้ยังเป็น `StartWhenAvailable=False`, `WakeToRun=False`
