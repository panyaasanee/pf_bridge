# FACTPACK R107 — กลไก sync ฝั่ง Windows (cloud chief ↔ ผู้เทส local)

**วัดจริงจากดิสก์ 2026-08-20 ~17:0x (เวลาบนไฟล์/สแตมป์ในไฟล์)** · ทุกบรรทัดมีที่มา
(ไฟล์:บรรทัด หรือคำสั่งที่รัน) · **รอบนี้ READ-ONLY** — ไฟล์นี้คือไฟล์เดียวที่ถูกเขียน

เครื่องมือ: `git --no-optional-locks` ทุกคำสั่ง · รันจาก Linux sandbox บน mount
`/sessions/funny-laughing-euler/mnt/Pirate Force/...` (= โฟลเดอร์เดียวกับ
`C:\Users\Panya\Desktop\Pirate Force\...`)

---

## 1. ของประสานงานอะไร tracked / untracked

### 1.1 bridge repo (`pf_bridge\`)

คำสั่ง: `git --no-optional-locks ls-files --error-unmatch <path>` และ
`git --no-optional-locks check-ignore -v <path>`

| ของ | tracked? | อยู่บนดิสก์? | rule ที่ทำให้ ignore |
|---|---|---|---|
| `CHIEF_CONTINUATION.md` | ✅ **TRACKED** | yes | ไม่ ignore (เปิดโดย `.gitignore:16:!/*.md`) |
| `GAME_TEST_QUEUE.md` | ✅ **TRACKED** | yes | ไม่ ignore (`.gitignore:16:!/*.md`) |
| `notes_to_chief/**` | ✅ **TRACKED 64 ไฟล์** (บนดิสก์ 77) | yes | ไม่ ignore (`.gitignore:34:!/notes_to_chief/` + `.gitignore:35:!/notes_to_chief/**`) |
| `LOCK.txt` | ❌ ignore | yes | `.gitignore:60:/LOCK.txt` |
| `LOCK_GAME.txt` | ❌ ignore | yes | `.gitignore:61:/LOCK_*.txt` |
| `LOCK_GIT.txt` | ❌ ignore | yes | `.gitignore:61:/LOCK_*.txt` |
| `PANYA_PRESENT.txt` | ❌ ignore | yes | `.gitignore:62:/PANYA_PRESENT.txt` |
| `bridge_loop_state.txt` | ❌ ignore | yes | `.gitignore:63:/bridge_loop_state.txt` |
| `watchdog_last_check.txt` | ❌ ignore | yes | `.gitignore:64:/watchdog_last_check.txt` |
| `inbox/` | ❌ ignore · tracked 0 | yes (0 ไฟล์) | `.gitignore:11:/*` (deny-all บรรทัดแรก ไม่มี `!` เปิดคืน) |
| `outbox/` | ❌ ignore · tracked 0 | yes (**782 ไฟล์ · 5,797,813 B**) | `.gitignore:11:/*` |
| `done/` | ❌ ignore · tracked 0 | yes (**225 ไฟล์ · 2,006,503 B**) | `.gitignore:11:/*` |
| `staged/` | ✅ tracked 17 (ดิสก์ 20) | yes | ไม่ ignore (`.gitignore:40:!/staged/` + `41:!/staged/**`) |
| `archive/` | ✅ tracked 46 (ดิสก์ 47) | yes | ไม่ ignore (`.gitignore:36:!/archive/` + `37:!/archive/**`) |
| `templates/` | ✅ tracked 1 (ดิสก์ 1) | yes | ไม่ ignore (`.gitignore:38–39`) |
| `_to_delete/` | ❌ ignore | yes (1 ไฟล์) | `.gitignore:11:/*` |

ข้อความของบรรทัดที่อ้าง (จาก `pf_bridge\.gitignore`):

```
 11  /*
 16  !/*.md
 34  !/notes_to_chief/
 35  !/notes_to_chief/**
 60  /LOCK.txt
 61  /LOCK_*.txt
 62  /PANYA_PRESENT.txt
 63  /bridge_loop_state.txt
 64  /watchdog_last_check.txt
```

> 🔴 **ข้อสรุปที่ตัดสินดีไซน์:** ธง `LOCK*.txt` / `PANYA_PRESENT.txt` /
> `bridge_loop_state.txt` / `watchdog_last_check.txt` **ถูก ignore โดยเจตนา**
> (`.gitignore:59` เขียนคอมเมนต์ไว้ตรง ๆ: *"runtime flags: whoever holds the
> machine owns these, never sync"*) ⇒ **git ไม่ใช่ช่องทางส่งธงระหว่างเครื่อง
> ในสภาพปัจจุบัน** และการเปิด allowlist ให้ธงเป็นการล้มเจตนาที่เขียนไว้ ไม่ใช่ bugfix
>
> เช่นกัน `inbox/ outbox/ done/` **ไม่อยู่ใน VCS เลย** ⇒ กล่องจดหมายฝั่ง "จ็อบ+ผลรัน"
> ไม่ sync (รวม 1,007 ไฟล์ · 7.8 MB) แต่ `notes_to_chief/` **sync ได้** เพราะ tracked

### 1.2 untracked ใน `notes_to_chief/` ตอนนี้

คำสั่ง: `git --no-optional-locks ls-files --others --exclude-standard notes_to_chief | wc -l`

- **13 ไฟล์** untracked · **ไม่มีไฟล์ไหนถูก ignore** (`ls-files --others` แบบมี/ไม่มี
  `--exclude-standard` ให้เลขเท่ากันคือ 13) ⇒ ทั้ง 13 พร้อม commit ได้ทันที
- รวมขนาด **75,508 bytes** (`du -cb` จากรายการเดียวกัน)
- รายการ:
  ```
  notes_to_chief/20260820_1410_ORDER-fix-actions-selfcheck-exitcode.md
  notes_to_chief/20260820_1440_ORDER-cp874-pin-stale-and-platform-dirty.md
  notes_to_chief/20260820_1520_GT027-RERUN-FINAL-video-npc-hp-does-not-move.CONSUMED.txt
  notes_to_chief/20260820_1545_ORDER-pytest-subset-fresh-clone-preconditions.CONSUMED.txt
  notes_to_chief/20260820_1650_PROVEN-cloud-routine-environment-facts.md
  notes_to_chief/20260820_1710_ORDER-cloud-prompt-and-sync-design.md
  notes_to_chief/FROM_CHIEF_R104_TO_ATTENDED_20260820_1430.md
  notes_to_chief/FROM_CHIEF_R105_TO_ATTENDED_20260820_1510.md
  notes_to_chief/FROM_CHIEF_R106_TO_ATTENDED_20260820_1640.md
  notes_to_chief/consumed/20260820_1410_ORDER-fix-actions-selfcheck-exitcode.md
  notes_to_chief/consumed/20260820_1440_ORDER-cp874-pin-stale-and-platform-dirty.md
  notes_to_chief/consumed/20260820_1520_GT027-RERUN-FINAL-video-npc-hp-does-not-move.md
  notes_to_chief/consumed/20260820_1545_ORDER-pytest-subset-fresh-clone-preconditions.md
  ```
  ⇒ **การเคลื่อนไหวของกล่องจดหมายในหนึ่งวัน = 13 ไฟล์ / 75 KB** นี่คือ throughput จริง
  ที่ตัว sync ต้องรับ ไม่ใช่ตัวเลขสมมติ

### 1.3 server repo (`Pirate Force ServerProject\`)

- **ไม่มีไฟล์ประสานงานสักไฟล์อยู่บนดิสก์ในรีโปนี้** — ตรวจแล้วทั้ง
  `CHIEF_CONTINUATION.md` `GAME_TEST_QUEUE.md` `LOCK.txt` `LOCK_GAME.txt`
  `LOCK_GIT.txt` `PANYA_PRESENT.txt` `bridge_loop_state.txt` = `ondisk=no tracked=no`
- โฟลเดอร์ `notes_to_chief/ inbox/ outbox/ done/ staged/ archive/ templates/` = **ไม่มีบนดิสก์** ทั้งหมด
- `check-ignore -v` ตอบทุก path ด้วย rule เดียวกัน: **`.gitignore:1:/*`** (deny-all บรรทัดแรก)
  รวมถึง `state/pirateforce.sqlite3` → `.gitignore:1:/*`
- ขนาด `.gitignore` ของ server = 29,205 B · 500 บรรทัด
  ⇒ **ไม่มี rule ที่พูดถึงธง/กล่องจดหมายโดยชื่อเลย** (grep `LOCK|PANYA|bridge_loop|notes_to_chief|inbox|outbox` เจอแค่บรรทัด 1 `/*`)

---

## 2. ประวัติ commit ของ bridge repo

คำสั่ง: `git --no-optional-locks rev-list --count HEAD` · `log -1` · `ls-files | wc -l` · `status --porcelain`

| รายการ | ค่า |
|---|---|
| จำนวน commit | **1** |
| commit ล่าสุด | `2accb96` · **2026-08-20 13:56:33 +0700** · author `Pirate Force Foundation` · subject `pf_bridge coordination repo: first commit` |
| tracked | **228 ไฟล์** |
| dirty — modified | **4** |
| dirty — untracked | **19** |
| ahead/behind `origin/main` | **0 / 0** (`rev-list --left-right --count origin/main...main` → `0 0`) |
| remote | `origin https://github.com/panyaasanee/pf_bridge.git` |
| `.git` บนดิสก์ | 9.6 MB |

ไฟล์ modified 4 ตัว (`git status --porcelain`):
```
 M CHIEF_CONTINUATION.md
 M GAME_TEST_QUEUE.md
 M PANYA_REPORT_20260820_cloud_readiness.md
 M READINESS_CHECKLIST_CLOUD_20260820.md
```
untracked 19 ตัว = 13 ใน `notes_to_chief/` (ข้อ 1.2) + `FACTPACK_R106_PYTEST_EXCLUSION_INVENTORY.md`
+ `FINDINGS_R106_R12_MEASURED_ON_A_SECOND_MACHINE.md` + `archive/CHIEF_CONTINUATION_ARCHIVE_20260820_R100_R101_R102.md`
+ `staged/` 3 ไฟล์

**เทียบกับ server repo:** 173 commit · HEAD `9045978` (2026-08-20 16:29:42 +0700) ·
tracked **523 ไฟล์ / 7,842,576 B** · **status สะอาด 0 บรรทัด** · ahead/behind `0 0` ·
`.git` 13 MB · branch: `main`, `codex/server-visible-console` (`0e922b6`), `remotes/origin/main`
+ refs พิเศษของ codex (`refs/codex/snapshots/...`, `refs/codex/turn-diffs/...`) + 13 tag

> 🔴 **bridge repo ยังเป็น repo อายุ 1 commit** — history ทั้งหมดของการประสานงาน
> อยู่ใน commit เดียวเมื่อ 13:56 วันนี้ ทุกอย่างที่เกิดหลังจากนั้น (รอบ 104/105/106
> ทั้งรอบ) ยัง **ไม่เคย commit** ⇒ ถ้า cloud chief clone ตอนนี้ จะไม่เห็นงาน 3 รอบล่าสุด

---

## 3. กลไก Windows ที่มีอยู่แล้ว ซึ่งเอาไปทำ git pull/push loop ได้

### 3.1 `pf_bridge.ps1` — worker loop (107 บรรทัด)

| หัวข้อ | ข้อเท็จจริง | ที่มา |
|---|---|---|
| รูปแบบ | `while ($true)` โพลโฟลเดอร์ `inbox\` หา `*.ps1` เรียงตามชื่อ เอาไฟล์แรก | `pf_bridge.ps1:52–56` |
| คาบโพล | **3 วินาที** เมื่อ idle (`Start-Sleep -Seconds 3`) | `pf_bridge.ps1:58` |
| หน่วงกันไฟล์เขียนไม่เสร็จ | **500 ms** ก่อนอ่านจ็อบ | `pf_bridge.ps1:61` |
| การรันจ็อบ | spawn `powershell -NoProfile -ExecutionPolicy Bypass -File <job>` แล้ว `*>&1 \| Tee-Object` ลง outbox | `pf_bridge.ps1:87–89` |
| state file | **`bridge_loop_state.txt`** เขียนทับทุกครั้ง เนื้อ 1 บรรทัด `"<what>  yyyy-MM-dd HH:mm:ss"` encoding **ascii** | `pf_bridge.ps1:34–39` |
| ค่าใน state | `idle` (ทุกโพล) / `running <job>` (ระหว่างจ็อบ) | `pf_bridge.ps1:58, 81, 102` |
| ค่าปัจจุบันบนดิสก์ | `idle  2026-08-20 17:01:21` | `cat bridge_loop_state.txt` |
| error handling | `$ErrorActionPreference = 'Continue'` (บรรทัด 15) · `try/catch` รอบการรัน จับ exception → `$code = 1` · เขียน `=== exit $code ===` ต่อท้าย outbox เสมอ · **ย้ายจ็อบไป `done\` ทุกกรณี** | `pf_bridge.ps1:85–101` |
| `Set-LoopState` เอง | ห่อด้วย `try {} catch {}` เปล่า — ล้มก็ไม่หยุด loop | `pf_bridge.ps1:36–37` |
| การหยุด | `Ctrl+C` เท่านั้น (ไม่มี exit condition อื่น) | `pf_bridge.ps1:48` |

**ท่าที่ยกไปใช้กับ git sync ได้ตรง ๆ:** `while(1) { งาน; เขียน state 1 บรรทัดพร้อม timestamp; sleep N }`
+ ทุกงานมี receipt เป็นไฟล์ + ย้ายไฟล์เข้าคลังเมื่อจบ

### 3.2 `pf_bridge_watchdog.ps1` — supervisor (131 บรรทัด)

| หัวข้อ | ข้อเท็จจริง | ที่มา |
|---|---|---|
| คาบ | **ทุก 5 นาที** ผ่าน Task Scheduler | `pf_bridge_watchdog.ps1:1` · `SETUP_BRIDGE_AUTOSTART.bat:6` |
| ชื่อ task | **`PF_Bridge_Watchdog`** | `SETUP_BRIDGE_AUTOSTART.bat:6` |
| คำสั่งลงทะเบียน | `schtasks /Create /F /TN "PF_Bridge_Watchdog" /SC MINUTE /MO 5 /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"...\pf_bridge_watchdog.ps1\""` | `SETUP_BRIDGE_AUTOSTART.bat:6` |
| ยิงทันทีหลังสร้าง | `schtasks /Run /TN "PF_Bridge_Watchdog"` | `SETUP_BRIDGE_AUTOSTART.bat:15` |
| ตรวจว่ามีชีวิตยังไง | `Get-CimInstance Win32_Process` filter `Name='powershell.exe' OR Name='pwsh.exe'` แล้ว `CommandLine -like '*pf_bridge.ps1*'` | `pf_bridge_watchdog.ps1:36–37` |
| **สัญญาณที่ 1 — loop นิ่ง** | อ่าน `bridge_loop_state.txt` แกะ timestamp ด้วย regex `(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*$` · `idle` เก่าเกิน **12 นาที** = frozen · `running` เก่าเกิน **25 นาที** = job wedged | `:27–28, 42–63` |
| **สัญญาณที่ 2 — inbox ไม่ระบาย** | จ็อบใน `inbox\` รอเกิน **25 นาที** โดยไม่มีใครประกาศ `running` = loop หยุด | `:75–92` |
| **heartbeat** | ✅ มี — `watchdog_last_check.txt` เขียนทับทุกรอบ 1 บรรทัด `"<ts>  <state>"` encoding **ascii** · state ∈ `bridge-alive` / `bridge-frozen-restarting` / `bridge-missing-starting` | `:99–104` |
| ค่าปัจจุบัน | `2026-08-20 16:57:01  bridge-alive` | `cat watchdog_last_check.txt` |
| การกู้ | `Stop-Process -Force` ทุก pid → `Start-Sleep 2` → **ตรวจซ้ำว่าตายจริง ถ้าไม่ตาย `exit 1` และไม่ยอมสตาร์ตตัวที่สอง** | `:110–120` |
| การสตาร์ต | `Start-Process powershell.exe -ArgumentList ... -WindowStyle Hidden` (ซ่อนจอ = กัน QuickEdit freeze) | `:2–3, 123–125` |
| log | `watchdog.log` (append, ascii) เขียนเฉพาะตอน (re)start จริง | `:25, 30–33` |
| error handling | `$ErrorActionPreference = 'SilentlyContinue'` ทั้งไฟล์ | `:22` |
| **หลักการที่เขียนไว้ตรง ๆ** | ถ้า state file **หายไป → ไม่ฆ่าอะไรเลย** ("absence of evidence is not evidence") | `:19–20` |

`watchdog.log` เป็นใบเสร็จว่ากลไกนี้ **เคยทำงานจริง** ไม่ใช่ทฤษฎี (4 เหตุการณ์):
```
2026-08-18 23:50:03  bridge not found - started hidden instance
2026-08-19 17:37:02  FROZEN BRIDGE: inbox\906_gt022_client_relaunch.ps1 has waited 46.2 min (> 25) ... loop stopped
2026-08-19 19:27:01  FROZEN BRIDGE: loop state 'running 909_gt022_boot.ps1  2026-08-19 18:57:51' is 29.2 min old (> 25) - job wedged
2026-08-19 21:36:56  bridge not found - started hidden instance
```

### 3.3 `fix_watchdog_admin.ps1` + `FIX_WATCHDOG_ADMIN.bat` — settings ที่ต้อง elevate

- `.bat` = 4 บรรทัด เรียก `.ps1` ด้วย `-NoProfile -ExecutionPolicy Bypass` · ผู้ใช้ต้อง **right-click → Run as administrator** (`FIX_WATCHDOG_ADMIN.bat:2–4`)
- `.ps1` ตรวจ elevation ด้วย `WindowsPrincipal.IsInRole(Administrator)` แล้ว **exit 1 ถ้าไม่ elevated** (`fix_watchdog_admin.ps1:15–23`)
- settings ที่ set (`:28–35`): `-StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero)`
- trigger ที่เพิ่ม (`:52`): `New-ScheduledTaskTrigger -AtLogOn -User 'Panya'` (เช็คซ้ำก่อนว่ามี `MSFT_TaskLogonTrigger` แล้วหรือยัง `:46–50`)
- **ใบเสร็จว่าถูก apply จริง** — `outbox\902_fix_watchdog_admin.out.txt` (2026-08-19 16:26:47):
  `ELEVATED=True` · `SETTINGS_OK` · `LOGON_TRIGGER_ADDED` ·
  `StartWhenAvailable: True` · `WakeToRun: True` · `DisallowStartIfOnBatteries: False` ·
  TRIGGERS: `MSFT_TaskTimeTrigger` + `MSFT_TaskLogonTrigger` · `LastTaskResult: 0`
- ทุก output ถูกห่อด้วย `Start-Transcript -Path <outbox\902...> -Force` (`:11`)

### 3.4 สรุปสูตรสำเร็จสำหรับ "git pull/push loop"

ท่ามาตรฐานของโปรเจกต์นี้ที่พิสูจน์แล้วบนเครื่องนี้ = **3 ชั้น**

1. **worker** — สคริปต์ PS1 `while(1)` โพลทุก 3 วินาที (`pf_bridge.ps1`)
2. **state file 1 บรรทัด + timestamp ต่อท้าย, encoding ascii** ที่ worker เขียนทับทุกโพล
   (`bridge_loop_state.txt`) — นี่คือสิ่งเดียวที่แยก "process มีชีวิต" ออกจาก "loop หมุน"
   (เหตุผลเขียนไว้ยาว `pf_bridge.ps1:24–33` และ `pf_bridge_watchdog.ps1:6–20`)
3. **watchdog ผ่าน Task Scheduler `/SC MINUTE /MO 5`** ตรวจอายุ state file (2 threshold: idle 12 นาที / running 25 นาที)
   + สัญญาณที่สองจาก backlog ที่ไม่ระบาย (25 นาที) + เขียน heartbeat ทุกรอบ + restart แบบ hidden + log เฉพาะตอนกู้

**สิ่งที่ต้องคัดลอกมาแน่ ๆ ถ้าทำ git sync loop:** ชื่อ task ใหม่ (เช่น `PF_Git_Sync`),
`/SC MINUTE /MO n`, settings ชุด elevate เดียวกัน (`StartWhenAvailable` = replay รอบที่พลาดตอนเครื่องหลับ,
`WakeToRun`, `MultipleInstances IgnoreNew` = **กัน pull/push สองตัวชนกัน**, `ExecutionTimeLimit 0`),
trigger `AtLogOn`, state file แยกใบของตัวเอง, และ `-WindowStyle Hidden`

---

## 4. ท่า commit ที่โปรเจกต์ใช้อยู่บน Windows

พบไฟล์ที่มี `read-tree` ทั้งหมด **88 ไฟล์** ใน `pf_bridge\` (`grep -rl "read-tree" .`)
— ส่วนใหญ่คือจ็อบ gate+commit ใน `done\` ตั้งแต่ `115_round69_...` ถึง `169_round106_...`
บวก `agent_kit/chief_task_prompt.md` และ archive ของ CONTINUATION 3 ใบ

**ตัวอย่างล่าสุดที่ใช้จริงและสำเร็จ:** `pf_bridge\done\169_round106_skip_census_gate_commit_RETRY.ps1`
(467 บรรทัด · commit `9045978`) — แก่นอยู่บรรทัด **333–367**:

```powershell
# ---------- 11. guarded commit: read-tree HEAD, stage ONLY the declared paths ----------
$committed = 0
if ($allGreen) {
    $rt = (git --no-optional-locks read-tree HEAD 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { W 'ABORT: read-tree failed'; exit 34 }
    $addFailed = 0
    foreach ($p in $paths1) {
        $o = (git --no-optional-locks add -- "$p" 2>&1 | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) { W "  RED add> $p :: $o"; $addFailed = 1 }
    }
    if ($addFailed -eq 1) { W 'ABORT: an add failed - refusing partial commit'; exit 35 }
    $stagedCount = @(git --no-optional-locks diff --cached --name-only 2>&1).Count
    W "staged path count = $stagedCount (expect 12)"
    $delLines = (git --no-optional-locks diff --cached --name-status 2>&1 |
                 Select-String -Pattern '^D' -CaseSensitive)
    if ($delLines) {
        W 'RED: staged set contains DELETIONS - aborting'
    } elseif ($stagedCount -ne 12) {
        W "RED: staged count is $stagedCount, expected 12 - aborting"
    } else {
        git --no-optional-locks commit -m "$msg" 2>&1 | Select-Object -First 3 | ...
        $headAfter = (git --no-optional-locks rev-parse HEAD 2>&1)
        if ($headAfter -cne $headBefore) { $committed = 1; W "COMMIT CONFIRMED: ..." }
        else { W "RED: commit returned but HEAD did not move (still $headBefore)" }
    }
} else {
    W 'NOT COMMITTING - a guard is red.  The edits stay as a dirty diff'
    W '(never reset/clean by iron rule)'
}
```

**คุณสมบัติของท่านี้ที่ sync ต้องรักษาไว้:**
1. `read-tree HEAD` **ล้าง index ให้เท่า HEAD ก่อน** แล้วค่อย `add` เฉพาะ path ที่ประกาศ
   ⇒ ไม่มีทางที่ของค้างใน index จาก session ก่อนจะติดไปด้วย
2. **นับ staged path เทียบเลขที่ประกาศไว้** (`expect 12`) — ไม่ตรง = abort
3. **ปฏิเสธ deletion ใน staged set** โดยไม่มีข้อยกเว้น
4. **ยืนยัน HEAD ขยับจริง** หลัง commit ไม่เชื่อ exit code ของ `git commit`
5. **ไม่เคยใช้ `git add -A`** (คำเตือนซ้ำใน `agent_kit\PUSH_TO_GITHUB_STEPS.md:54–55`)
6. **ไม่ reset / ไม่ clean เด็ดขาด** — ถ้าการ์ดแดง ปล่อยไว้เป็น dirty diff
7. `exit` code เฉพาะทาง: `34` = read-tree ล้ม · `35` = add ล้ม

**ท่า LOCK_GIT ที่มาคู่กัน** (`done\169_...ps1:76–99` และ `:400–455`):
```powershell
$lockGit = Join-Path $bridge 'LOCK_GIT.txt'
function Beat($phase) {                       # heartbeat ระหว่างทำงาน
    Add-Content -LiteralPath $lockGit -Value "HEARTBEAT: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')+07:00  $phase" -Encoding utf8
}
# 0. refuse to stomp another holder, then acquire
$firstLine = (Get-Content -LiteralPath $lockGit -TotalCount 1 -ErrorAction SilentlyContinue)
if ($firstLine -cmatch '^HELD:') { W "ABORT: LOCK_GIT.txt is HELD by someone else: $firstLine"; ... }
@( "HELD: $(Get-Date -Format 'yyyy-MM-ddTHH:mm')+07:00", ... ) | Out-File -FilePath $lockGit -Encoding utf8
# 13. release whatever happened
@( "RELEASED: ...", ... ) | Out-File -FilePath $lockGit -Encoding utf8
```

> 🔴 **บั๊กที่วัดเจอในรอบนี้ (ยังไม่มีใครรายงาน):** `LOCK_GIT.txt` บนดิสก์ขึ้นต้นด้วย
> **UTF-8 BOM `EF BB BF`** (`head -c 3 LOCK_GIT.txt | xxd -p` → `efbbbf`) เพราะ
> `Out-File -Encoding utf8` บน Windows PowerShell 5.1 ใส่ BOM เสมอ
> ⇒ การ์ด `$firstLine -cmatch '^HELD:'` (`done\169_...ps1:83`) **จะไม่แมตช์**
> ถ้าไฟล์อยู่ในสถานะ HELD จริง เพราะอักขระแรกคือ BOM ไม่ใช่ `H`
> ⇒ **ธง LOCK_GIT ที่ถูกถือค้างอยู่จะถูกทับเงียบ ๆ** · ไฟล์ธงอีกใบ `LOCK_GAME.txt`
> **ไม่มี BOM** (`52 45 4c` = `REL`) ⇒ ปัญหานี้เป็นของ `LOCK_GIT.txt` ใบเดียว
> **ตัว sync ห้ามคัดลอกท่าอ่าน `^HELD:` ไปดื้อ ๆ** ต้องกิน BOM ก่อน หรือใช้ `-Encoding ascii`
> อย่างที่ `bridge_loop_state.txt` / `watchdog_last_check.txt` ทำ (ทั้งคู่ไม่มี BOM: `69 64 6c`, `32 30 32`)

**ไม่มีจ็อบไหนใน `done\`/`staged\` ที่ `git push` หรือ `git pull` จริงเลย** — ไฟล์ที่ grep เจอคำว่า
`push|pull|fetch` (7 ไฟล์ + `agent_kit\PUSH_TO_GITHUB_STEPS.md`) พูดถึงมันในคอมเมนต์เท่านั้น
เช่น `done\169_...ps1:59`: *"NOT done here: git push / remote config - Panya pushes, always."*
⇒ **ท่า pull/push ยังไม่เคยมีบนเครื่องนี้ ต้องเขียนใหม่ทั้งหมด** (`agent_kit\PUSH_TO_GITHUB_STEPS.md:21`
ระบุว่า push เป็นขั้นตอนที่ Panya รันเอง — ผู้ช่วยไม่แตะ auth)

---

## 5. ความเสี่ยง merge จริง

### 5.1 ขนาดตอนนี้

| ไฟล์ | bytes | บรรทัด |
|---|---|---|
| `CHIEF_CONTINUATION.md` | **79,398** | 365 |
| `GAME_TEST_QUEUE.md` | **86,923** | 460 |

(`stat -c%s` · `wc -l` · ทั้งสองไฟล์ **tracked และ modified** อยู่ตอนนี้)

### 5.2 รอบใหม่ถูกแทรกตรงไหน — วัดจาก diff hunk จริง

คำสั่ง: `git --no-optional-locks diff -U0 -- <file> | grep '^@@'`

**`CHIEF_CONTINUATION.md`** — `+88 / −133` บรรทัด (`diff --numstat`)
```
@@ -2,0 +3,86 @@      <- แทรก 86 บรรทัดใหม่ ทันทีหลังบรรทัดที่ 2
@@ -12,133 +98,2 @@   <- ลบ 133 บรรทัด (รอบเก่าย้ายเข้า archive) เหลือ 2
```
- โครงสร้าง: **append-only ที่ "ด้านบน" (newest-first)** — บรรทัด 1 = ชื่อไฟล์,
  บรรทัด 3–14 = แบนเนอร์คำสั่ง Panya (ใช้ครั้งเดียว ลบได้รอบถัดไป — เขียนไว้เองบรรทัด 14),
  บรรทัด 16 = `> ## 🆕🆕 รอบ 106`, 62 = รอบ 105, 76 = รอบ 104, 89 = รอบ 103,
  101 = รอบ 99 … ไล่เก่าลงล่าง จนถึง stub `⤴ ย้ายไป archive แล้ว` บรรทัด 200+
- **รอบใหม่แทรกที่บรรทัด 3 เสมอ** และ **รอบเก่าถูกตัดออกกลางไฟล์พร้อมกัน**

> 🔴 **`git pull --rebase` จะชนแทบทุกครั้ง** ถ้าสองเครื่องเขียนไฟล์นี้ในรอบเดียวกัน:
> ทั้งคู่แก้ **บรรทัดที่ 3 ที่เดียวกัน** ⇒ conflict ทุกครั้ง ไม่ใช่บางครั้ง
> และการ archive ยังลบบล็อกกลางไฟล์ ⇒ conflict ชนิดที่ auto-merge ช่วยไม่ได้เลย

**`GAME_TEST_QUEUE.md`** — `+33 / −0` บรรทัด
```
@@ -166,0 +167,21 @@   <- แทรก 21 บรรทัด กลางหัวข้อ PLAYBOOK (บรรทัด 129 "PLAYBOOK เพิ่มเติม")
@@ -281,0 +303,12 @@   <- แทรก 12 บรรทัด ใต้ GT-028 (หัวข้อบรรทัด 298)
```
- โครงสร้าง: **แบ่งตามหัวข้อ `## GT-NNN <ชื่อ> [STATUS]`** ไม่เรียงเวลา —
  บรรทัด 202 GT-001, 226 GT-026, 273 GT-033, 290 GT-027, 298 GT-028, 317 GT-029,
  324 GT-034, 334 GT-035, 338 GT-036, 342 GT-037, 346 GT-038, 357 GT-030,
  385 GT-031, 414 GT-032 · หัวข้อ PLAYBOOK ที่ 79 และ 129 · lessons ที่ 436, 451
- **รอบใหม่แทรก "ใต้หัวข้อ GT ที่เกี่ยว" กระจายหลายจุดกลางไฟล์** ไม่ใช่บนสุดหรือล่างสุด
  (รอบนี้ 2 จุด: ใน PLAYBOOK และใต้ GT-028) · **ไม่มีการลบ** (`−0`)

> 🟡 **`git pull --rebase` ชนน้อยกว่า** ไฟล์แรก: ถ้าสองเครื่องแก้คนละ GT
> git จะ auto-merge ได้ เพราะ hunk ห่างกัน (167 vs 303) แต่ถ้าทั้งคู่แก้ GT เดียวกัน
> หรือแก้ PLAYBOOK พร้อมกัน = conflict · ความเสี่ยง = **ปานกลาง แบบมีเงื่อนไข**
> ไม่ใช่ **แน่นอน** อย่าง `CHIEF_CONTINUATION.md`

### 5.3 ตัวคูณความเสี่ยงเพิ่มเติมที่วัดได้

- `pf_bridge\.gitattributes:16` = `*.md   text eol=lf` ⇒ ทั้งสองไฟล์ normalize เป็น LF
  ในรีโป ⇒ **ไม่มีความเสี่ยง conflict จาก CRLF/LF** (ตรงกันข้ามกับ `.ps1`/`.bat` ที่
  `.gitattributes:19–20` บังคับ `eol=crlf`) · `.gitattributes:13` `* -text` = default ไม่แปลง
- ทั้งสองไฟล์ **เกินเพดานที่โปรเจกต์ตั้งเอง** — `LOCK_GIT.txt` (บันทึกของ job 169) เขียนว่า
  *"housekeeping (QUEUE ~82KB, CONTINUATION ~104KB both over their ceilings)"*
  ⇒ ยิ่งใหญ่ ยิ่ง conflict แพง
- `notes_to_chief/**` = ไฟล์ใหม่ล้วน ชื่อมี timestamp `YYYYMMDD_HHMM_` ⇒ **แทบไม่มีทางชนกัน**
  ⇒ **นี่คือช่องทางที่ปลอดภัยที่สุดสำหรับส่งข้อความข้ามเครื่องผ่าน git**
  (13 ไฟล์วันนี้ ไม่มีคู่ไหนชื่อซ้ำในโฟลเดอร์เดียวกัน)

---

## 6. `.git` ของ bridge + ไฟล์ lock ค้าง

### 6.1 bridge repo

- branch: **`main` เท่านั้น** (local) + `remotes/origin/main` · ทั้งคู่ชี้ `2accb96`
  (`git for-each-ref` → `refs/heads/main 2accb96` · `refs/remotes/origin/main 2accb96`)
- `HEAD` = `ref: refs/heads/main` (`cat .git/HEAD`)
- **ไม่มี tag เลย** · ไม่มี branch อื่น
- **`.git/*.lock` ค้าง: ไม่มีสักไฟล์** — `find .git -name "*.lock" -o -name "*lock*"` คืน **ว่างเปล่า**
- `.git/config`: `user.name = Pirate Force Foundation` · `user.email = local@pirate-force.invalid` ·
  `core.filemode = false` · `core.ignorecase = true` · `core.symlinks = false` ·
  `[branch "main"] remote = origin, merge = refs/heads/main` ⇒ **`git pull` ทำงานได้ทันทีไม่ต้องระบุ upstream**
- **ไม่มี `credential.helper` ใน `.git/config`** ⇒ auth มาจาก global/Windows Credential Manager
  (ไม่ได้ตรวจ — นอก scope)

### 6.2 ไฟล์ lock ที่รายงานว่ามี — **อยู่ใน server repo ไม่ใช่ bridge**

`find .git -name "*lock*"` ใน `Pirate Force ServerProject\` เจอ **3 ไฟล์ ขนาด 0 bytes ทั้งหมด**:

| path | bytes | mtime |
|---|---|---|
| `.git\STALE_index.lock_20260820_1210_delete_me` | 0 | 2026-08-20 13:09 |
| `.git\index_lock_stale_20260820` | 0 | 2026-08-20 02:41 |
| `.git\objects\maintenance.lock` | 0 | 2026-08-17 13:01 |

- **`.git\index.lock` ตัวจริงไม่มี** (`ls .git/index.lock` → No such file) ⇒ **git ใช้งานได้ปกติ ไม่ถูกบล็อก**
- ทั้งสามเป็นไฟล์ที่ถูก **rename ทิ้งไว้** ไม่ใช่ lock ที่ git ถืออยู่ (ชื่อไม่ใช่ `index.lock`)
- `done\169_...ps1:63` ระบุไว้ตรง ๆ ว่า **`.git\STALE_index.lock_20260820_1210_delete_me` เป็นของ Panya ที่จะลบเอง**
  (ซ้ำอีกครั้งในเนื้อ `LOCK_GIT.txt` บรรทัด `next:`) ⇒ รอบนี้ **ไม่แตะ**
- server repo: `HEAD = ref: refs/heads/main` → `9045978` · branch อีกใบ `codex/server-visible-console` (`0e922b6`)
  · มี `refs/codex/snapshots/*` และ `refs/codex/turn-diffs/captures/*` 4 อัน (ของเครื่องมือ codex) · 13 tag

---

## ภาคผนวก — ตัวเลขที่ chief ต้องใช้ตัดสินใจ (สรุปแถวเดียว)

| ตัวชี้วัด | bridge | server |
|---|---|---|
| commit | **1** | 173 |
| tracked ไฟล์ / bytes | 228 / — | 523 / 7,842,576 |
| dirty (M / ??) | **4 / 19** | 0 / 0 |
| ahead/behind origin | 0 / 0 | 0 / 0 |
| `.git` บนดิสก์ | 9.6 MB | 13 MB |
| lock ค้าง | **0** | **3 (0 B, ไม่บล็อก)** |
| ธง LOCK sync ผ่าน git ได้ไหม | ❌ ignore ทั้งหมด | ❌ ไม่มีไฟล์ธงในรีโป |
| กล่องจดหมาย `notes_to_chief` sync ได้ไหม | ✅ tracked · 13 ไฟล์ใหม่/วัน · 75 KB | ❌ ไม่มีโฟลเดอร์ |
| ของที่ไม่ sync (ตั้งใจ) | `inbox/ outbox/ done/` = 1,007 ไฟล์ · 7.8 MB | — |

---

## ไฟล์ที่แตะในรอบนี้

- **เขียนใหม่ 1 ไฟล์:** `pf_bridge\FACTPACK_R107_SYNC_MECHANICS.md` (ไฟล์นี้)
- **อ่านอย่างเดียว:** `pf_bridge\.gitignore` · `pf_bridge\.gitattributes` ·
  `pf_bridge\pf_bridge.ps1` · `pf_bridge\pf_bridge_watchdog.ps1` ·
  `pf_bridge\SETUP_BRIDGE_AUTOSTART.bat` · `pf_bridge\fix_watchdog_admin.ps1` ·
  `pf_bridge\FIX_WATCHDOG_ADMIN.bat` · `pf_bridge\CHIEF_CONTINUATION.md` ·
  `pf_bridge\GAME_TEST_QUEUE.md` · `pf_bridge\LOCK.txt` · `pf_bridge\LOCK_GAME.txt` ·
  `pf_bridge\LOCK_GIT.txt` · `pf_bridge\bridge_loop_state.txt` ·
  `pf_bridge\watchdog_last_check.txt` · `pf_bridge\PANYA_PRESENT.txt` ·
  `pf_bridge\CANON_SHA.txt` · `pf_bridge\watchdog.log` ·
  `pf_bridge\done\169_round106_skip_census_gate_commit_RETRY.ps1` ·
  `pf_bridge\done\900_watchdog_diag.ps1` · `pf_bridge\outbox\902_fix_watchdog_admin.out.txt` ·
  `pf_bridge\agent_kit\PUSH_TO_GITHUB_STEPS.md` ·
  `Pirate Force ServerProject\.gitignore` · metadata ของ `.git` ทั้งสองรีโป
- **ไม่ทำ:** ไม่ commit · ไม่ push · ไม่ pull · ไม่แตะ `state\pirateforce.sqlite3` ·
  ไม่เปิด UI/เกม/เซิร์ฟเวอร์ · ไม่แก้ `LOCK_*` / `GAME_TEST_QUEUE.md` / `CHIEF_CONTINUATION.md` ·
  ไม่รัน pytest · ไม่ลบไฟล์ lock ค้างของ server repo
