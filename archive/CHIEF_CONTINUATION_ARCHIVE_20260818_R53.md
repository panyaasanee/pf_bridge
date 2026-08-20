# CHIEF_CONTINUATION — ARCHIVE 2026-08-18 (chief รอบ 53)

> ย้ายมาจาก `pf_bridge/CHIEF_CONTINUATION.md` §1–§35 (chief รอบ 53, 2026-08-18 ~03:5x)
> เพื่อคุมขนาดไฟล์หลัก < 100KB ตามกติกาแม่บ้าน — เนื้อหาคงเดิมทุกตัวอักษร ไม่มีการแก้
> ไฟล์หลักมี pointer ชี้กลับมาที่นี่ · archive ก่อนหน้า: CHIEF_CONTINUATION_ARCHIVE_20260817.md

## 1. ข้อจำกัดของเครื่องนี้ (ยืนยันแล้ว อย่าเสียเวลาทดสอบซ้ำ)

### `mcp__workspace__bash` — ใช้ได้ แต่เป็น Linux sandbox คนละเครื่องกับ Windows

Mount ร่วมที่ `/sessions/<id>/mnt/Pirate Force/` (มี `GameClient`,
`Pirate Force ServerProject`, `...-console`, `pf_bridge` ครบ)

| ✅ ใช้ได้ | ❌ ใช้ไม่ได้ |
|---|---|
| อ่านไฟล์ / grep / python วิเคราะห์ | รัน server จริง, รัน GameClient (Windows binary) |
| `git log/show/diff` (read-only) | ทดสอบ runtime/socket จริง |
| **เขียนไฟล์ทับ (truncate-in-place)** | **unlink/ลบไฟล์** — mount ห้าม |
| `git check-ignore` (read-only) | console worktree (`.git` ชี้ path แบบ Windows) |

> ⛔ **บทเรียนสำคัญที่สุดของรอบ 04:27 — อย่ารันคำสั่ง git ที่เขียน `.git/index` จาก bash**
> (`git status`, `git add`, `git checkout`) เพราะ unlink `.git/index.lock` ไม่ได้
> → **ทิ้ง index.lock ค้าง ทำให้ git บน Windows พังทั้งหมด**
> ถ้าเผลอทำ: ส่ง job ให้ bridge ลบ `.git\index.lock`
> (เช็คก่อนว่า 0 ไบต์ **และ** ไม่มี git process — ดูตัวอย่างใน `done\017_*.ps1`)
> **สรุป: bash = อ่านอย่างเดียว, bridge = ทุกคำสั่ง git ที่เขียน**

- Linux python3.10 / Windows python3.14 → **Windows เป็น gate จริงเสมอ**
  บน Linux `unittest discover` จะ fail 10 อันจาก environment
  (9 อัน `capstone`/`pefile` ไม่มี, 1 อัน `__notes__` ต้อง py3.11+)
  → **ไม่ใช่บั๊กจริง** ใช้เป็น pre-check เร็ว ๆ ได้ แต่อย่าเชื่อเป็นคำตัดสิน
- Computer Use: terminal/IDE/File Explorer ได้แค่ tier `click` **ห้ามหาทางเลี่ยง**
- `mcp__computer-use__wait` ต้อง `request_access` ก่อน ไม่งั้น error
  → chief ใช้ `sleep` ใน bash แทน (bash tool timeout ~120 วิ ให้ `sleep 45` แล้วเช็ค แล้ว sleep ใหม่)

## 2. PF BRIDGE — ช่องทางรันคำสั่งบน Windows

ผู้ใช้เปิด `pf_bridge\START_PF_BRIDGE.bat` ค้างไว้ (โหมด AUTO)

- เขียน `.ps1` ลง `pf_bridge\inbox\` ชื่อ `NNN_ชื่องาน.ps1` (เลขรันต่อกัน) → รันใน ~3 วิ
- ผลออกที่ `outbox\NNN_*.out.txt` (**UTF-16 อ่านยาก**)
  → ให้ job เขียน log ของตัวเองเป็น UTF-8 ด้วย `Out-File -Encoding utf8 -Append` เสมอ
- **job ที่รันนานต้องเขียน log แบบ incremental ทุกบรรทัด** (ฟังก์ชัน `L` ใน `done\017/018/019`)
- **commit message ต้องเขียนแบบไม่มี BOM:**
  `[IO.File]::WriteAllText($p,$msg,(New-Object Text.UTF8Encoding($false)))`
  ห้ามใช้ `Out-File` (เจอ BOM ติดหัวข้อ commit ในงาน 005 ต้อง amend ที่ 006)
- **ห้ามเรียก client ด้วย `& cmd /c`** — child สืบทอด stdout handle แล้ว bridge ค้าง
  (เคยค้าง 23 นาทีเต็ม และทำให้ timestamp ใน log เชื่อถือไม่ได้ทั้งไฟล์)
  ต้องใช้ `ProcessStartInfo` + `UseShellExecute=$false` เท่านั้น
  (`Start-Process -FilePath *.bin` ก็ไม่ได้ เพราะ ShellExecute ไม่รู้จัก `.bin` → เงียบ)
- **แพตเทิร์น job ที่ดี** (ดู `done\018`/`done\019`): ตรวจ precondition → ทำงาน →
  **guard ว่าไม่มีไฟล์ WIP หลุดเข้า stage** → commit → verify ย้อนกลับว่า WIP ยังอยู่ครบ

## 3. Workspace (ห้ามสร้างใหม่ ห้าม clone)

- main: `C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject` (branch `main`)
- console: `...\Pirate Force ServerProject-console` (branch `codex/server-visible-console`)
  — เป็น git worktree ของ repo เดียวกัน cherry-pick ข้ามได้ตรง ๆ
- GameClient: `C:\Users\Panya\Desktop\Pirate Force\GameClient`
- lease: `docs/AI_WORKSPACE_LEASE.json` — ไม่มี git remote

เอกสารที่ต้องอ่าน: `AGENTS.md` → `docs/WORKFLOW.md` → `STATUS.md`
→ `docs/HYPOTHESIS_LEDGER.json` → **`docs/FUNCTIONAL_COVERAGE.json`** (ใหม่)
→ `docs/EXPERIMENT_LEDGER.md` → `docs/AI_TRANSFER_HANDOFF_20260817.md`

กฎ: หนึ่ง milestone หนึ่ง claim, แยก fact/inference/hypothesis/negative, เกรด A–E,
`production_allowed=false` จนกว่าจะพิสูจน์, commit ก่อนตอบ success,
**checkpoint แคบ ≠ feature complete**, ห้าม reset/clean/stash ทับ dirty diff,
`references/` และ `evidence/` read-only, ห้ามอัปโหลด binary/capture/DB/media ที่ใด

---

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** §4 สถานะยืนยัน ณ 07:19 (สถานะสด: ดู LOCK + section รอบล่าสุดท้ายไฟล์) → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน B

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** §5 Milestone plan M1–M14 (ปิดแล้ว; สถานะ milestone ปัจจุบันตามรอบ 41–43) → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน C

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** §6 คำถาม Panya ชุดแรก — ตอบและ landed รอบ 31 `abf3696` → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน D

## 7. Playbook full-loop ผ่าน GameClient (พิสูจน์แล้ว 04:17–04:24)

ฉบับละเอียดสำหรับผู้เทสอยู่ใน `pf_bridge\GAME_TEST_QUEUE.md` หัวข้อ PLAYBOOK
ย่อสำหรับ chief:

1. ปิด server เก่าด้วย **หนึ่ง** `CTRL_C_EVENT` เข้า console ของ shim → รอ exit 0 ทั้งคู่
2. เปิด server `tools\run_foundation_visible.ps1` บน DB **canonical** `state\pirateforce.sqlite3`
   ⚠️ **ต้องเป็น DB ที่ backpack เป็น baseline (identity 1 อยู่ slot 0)** ไม่งั้น guard ใน WIP
   จะ raise เงียบ ๆ แล้ว StartGameReq ไม่ได้คำตอบ
   - DB baseline ที่ใช้ได้: `state\pirateforce.sqlite3`,
     `item_lifecycle001_25690816_172425.sqlite3`, `item_move_capture001_25690816_184145.sqlite3`
   - ❌ ห้ามใช้ `item_move_hyp001_25690817_002012.sqlite3` (เป็น post-move state)
3. เปิด client `GameClient\run_v142_client_only.bat` (แก้ให้ใช้ ProcessStartInfo แล้ว;
   ต้นฉบับอยู่ที่ `run_v142_client_only.bat.orig.bak`)
4. UI: เลือกเซิร์ฟเวอร์ → dialog PVP "ยืนยัน" → หน้าเลือกตัวละคร `Arena01`
   → **ปุ่มกลางสุดจาก 5 ปุ่มแถวล่าง = เข้าเกม** ⚠️ ปุ่มที่ 2 จากซ้าย = ลบตัวละคร ห้ามแตะ
5. ตรวจว่าเข้าจริงจาก `capture_.../server_console_live.out.txt`:
   ต้องเห็น `FOUNDATION_SELECTED_START_GAME` **และ**
   `V113_TELEPORT_SCENE1_STABLE_ZERO_TARGET_ONCE`
   (ถ้าเห็นแค่ `StartGameReq` แล้วเงียบ = guard reject → เลือก DB ผิด)
6. ออก: คลิก X ครั้งเดียว → dialog ยืนยัน → แล้วค่อยส่ง Ctrl+C ให้ server

---

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** §8 บันทึกงานรอบเช้า → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน E

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** §9 แผน "รอบหน้า" ฉบับเช้า (ล้าสมัย) → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน F

## 16. 🏗️ โครงสร้างทีมใหม่ (Panya อนุมัติ ~11:10 — แทนที่ข้อ 14/15 ทั้งหมด)

- **task เดียว: `pirate-force-chief-continue`** ตื่นทุก **15 นาที** รวมบทบาท
  Chief + Game Tester — ลำดับหน้าที่: ประมวลผลค้าง → เทสในเกม (ถ้ามีสิทธิ์
  computer use) → งานโค้ด/เอกสาร → idle round
- task `pirate-force-game-tester` **ลบทิ้งแล้ว** (prompt เก็บไว้ที่
  `C:\Users\Panya\Claude\Scheduled\pirate-force-game-tester\SKILL.md`)
- เหตุผล (วัดจริงคืน 17 ส.ค.): handoff ข้าม task ไม่เคยสำเร็จ, chief ถือ LOCK 78%,
  รอบจริงยาว 10–15 นาที (cron 3 นาที = ตื่นเปล่าเผา token), งานขนานกันไม่ได้อยู่แล้ว
- เซสชันหลัก (ตัวที่คุยกับ Panya) เกษียณจากบทผู้เทส — context เต็มแล้ว
- **การทดลองสำคัญที่ต้องทำครั้งแรกที่ Panya อยู่หน้าเครื่อง:** รอบถัดไปของ task
  จะเรียก `request_access` ขอ `GameClient.local.bin` — Panya กด **Allow หนึ่งครั้ง**
  ระบบจะจำ approval ติดตัว task ถาวร → รอบต่อ ๆ ไปเทสในเกมได้เองแม้ Panya หลับ
  ถ้ากลไกนี้ไม่ทำงานจริง ให้บันทึกผลใน GAME_TEST_QUEUE แล้วถือว่าเทสจอ
  เป็นงาน attended เท่านั้น (RUNBOOK เดิมยังใช้ได้)

---

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** §17–30 รอบ 27–40 เต็ม → `pf_bridge/archive/CHIEF_CONTINUATION_ARCHIVE_20260817.md` ก้อน G

## 31. รอบ 41 (2026-08-17 18:36–19:1x INTERACTIVE — Panya เคาะในแชท) — 🟢🟡 **HYP-PF-012 implement+พิสูจน์ wire/DB เกือบครบ — ติด bridge หยุดรับงาน ยังไม่ commit**

### 31.1 คำตัดสิน

Panya พิมพ์ตรงในแชทเซสชัน chief 18:35: **"(ก)"** = HYP-PF-012 เต็ม (subcode 01+03) —
จดไว้หัวไฟล์เป็นบล็อก 🟢 แล้ว (provenance: ตรงจากแชทนี้ ไม่ผ่านมือเขียน)

### 31.2 ทำเสร็จ (ยัง uncommitted ทั้งหมด — ดู 31.4)

- **src**: `logout_hypothesis.py` ใหม่ (232 บรรทัด: pins request 01/03 จาก R38/R40 +
  echo ack ผ่าน `make_runtime_vitals` + exact-allowlist scenario loader) ·
  `runtime.py` (+~60: `_dispatch_logout_hypothesis` commit-close-ก่อน-ack + post-ack
  dispatch เงียบ) · `app.py` (+ธง `--logout-hypothesis-scenario`, บังคับ --db, mutual
  exclusion) · `scenarios/logout_hypothesis_ack_echo.json` ใหม่
- **response design** (ไม่มี golden — เป็น hypothesis ที่ประกาศชัด): echo payload 14B เดิม
  ใน GSCN_RunTimeProtocolRes v4 (envelope binary-proven) · pins:
  ack01 pc36 `9E4FA00E..3C67` frame46 `9B417B5F..3D0A` · ack03 pc36 `FC8B9E2C..6DC6`
  frame46 `AB172DFF..6696`
- **เทส**: `tests/test_logout_hypothesis.py` 10 ตัว (ack+closed_at+ordering, post-ack
  เงียบ, wrong payload/sequence/no-scenario fail closed, allowlist, pins) — เขียว sandbox ·
  suite เต็ม sandbox 414 passed / 1 fail (`__notes__` env เดิม)
- **ledger**: entry HYP-PF-012 (LOGOUT-ACK-001) + verifier EXPECTED_IDS/META +
  CANONICAL re-pin `00142EB6..60B8` → PASS entries=19 · **matrix**: แถว
  `session_lifecycle/clean_logout` = in_progress + GRADE re-pin `D0E5E1BD..E580` →
  PASS domains=8 · **report**: `reports/PF_LOGOUT_ACK001_..._20260817.md` (ผล 076 กรอกแล้ว)
- **headless พิสูจน์แล้ว (job 076, 18:51–18:52)**: ✅ ack byte-exact ตรง pin ทั้ง 01/03
  เป็นเฟรมแรกหลัง logout (late 0.2ms, ledger-labelled ใน GAME_LIVE) · ✅ dispatch เงียบ
  หลัง ack (empty poll ที่เคยได้ keepalive 44B → ได้ 0) · ✅ DB: sessions 4→6 with-char,
  open=0, lease 4→6, integrity ok, backpack+position ไม่ขยับ · probe exit 3 = บั๊กเกณฑ์
  ของ probe เอง (นับ HEARTBEAT 24B sha `B4F6CFA2..ACB1` — clock ของ v141 เดิม มีทุกเซสชัน —
  เป็น dispatch traffic) → แก้ probe แล้ว + เปลี่ยน `post_ack_policy` เป็น
  `dispatch_silent_until_socket_close` ให้ตรงความจริง
- **คิวรอบใหญ่**: GT-007 (client-observable logout) เขียนครบใน GAME_TEST_QUEUE แล้ว

### 31.3 blocker เดียว: PF BRIDGE หยุดรับงานหลังจบ 076 สะอาด (18:52:32)

- job 077 (rerun probe เกณฑ์ใหม่ + row timestamps) ค้าง inbox ตั้งแต่ 18:57 ไม่ถูกหยิบ
  (loop poll ทุก 3 วิ → console ปิด/ตาย) — ตามกฎ ห้ามวางซ้อน
- **Panya: เปิด `pf_bridge\START_PF_BRIDGE.bat` หนึ่งครั้ง** → 077 จะรันเอง →
  รอบถัดไป (หรือผมถ้ายังอยู่) ย้าย `staged\078_hyp012_windows_gate.ps1` ลง inbox →
  เขียว (เกณฑ์ ≥415/0 + ledger 19 + domains 8) → commit ชุดเดียว (ไฟล์ตาม 31.4)
- ยังไม่ commit เพราะ gate จริง = Windows py -3 เท่านั้น (บทเรียนรอบ 26)

### 31.4 dirty diff ที่ต้อง commit ด้วยกันเมื่อ gate เขียว (อย่าให้หาย)

`src/pirateforce_foundation/{logout_hypothesis.py(ใหม่),runtime.py,app.py}` ·
`scenarios/logout_hypothesis_ack_echo.json(ใหม่)` · `tests/test_logout_hypothesis.py(ใหม่)` ·
`tests/test_foundation_legacy_seam.py` (GRADE re-pin) · `tools/verify_hypothesis_ledger.py`
(IDS/META/CANONICAL) · `docs/HYPOTHESIS_LEDGER.json` (entry 012) ·
`docs/FUNCTIONAL_COVERAGE.json` (แถว clean_logout) ·
`reports/PF_LOGOUT_ACK001_HYP_PF_012_ACKNOWLEDGED_LOGOUT_HEADLESS_WIRE_DB_20260817.md(ใหม่)`
(+ lease ไฟล์เดิม 1 ไฟล์ที่ dirty อยู่ก่อนแล้ว — อย่าแตะ)
commit message แนะนำ: "HYP-PF-012 acknowledged logout: echo ack behind opt-in scenario,
clean close before ack, headless wire/DB proven (LOGOUT-ACK-001)"

### 31.5 ตั้งใจไม่ทำ

ไม่แตะ legacy v141 (HEARTBEAT clock คงเดิม — อยู่นอก scope claim) · ไม่ commit ก่อน Windows
gate · ไม่วาง job ซ้อนตอน bridge ตาย · ไม่ลบ run DB 076 (`state\pirateforce_hyp012_*.sqlite3`
— เก็บเป็นหลักฐานจนกว่า Panya จะให้ล้าง) · ไม่ออกแบบ response เผื่อ subcode อื่น (fail closed)

### 31.6 ปิดจ้อบ (19:1x–19:2x — bridge กลับมาเองระหว่างรอบ)

- bridge กลับมารับงาน ~19:09 → **077 probe exit 0 ทุกเกณฑ์เขียว** + ได้ runtime timestamp:
  closed_at **ก่อน** ack 13–16ms ทั้งสอง lease ขณะ socket ยังเปิดต่ออีก ~10 วิ · stderr 0B
- **078 Windows gate: pytest 415/0 · ledger PASS 19 · coverage PASS 8** →
  **commit `b90007e`** (13 ไฟล์ตาม 31.4 + .gitignore whitelist report+manifest ·
  lease file เดิมไม่แตะ) · HEAD.lock → .stale · job 079 cleanup วางแล้ว
- เกณฑ์เขียว gate ใหม่ = **415/0** (405 เดิม + 10 logout) — release note นี้คือแหล่งอ้างอิง
- GT-001 re-arm ที่ `b90007e` (canonical sha ไม่เปลี่ยน — staged 072/073 ใช้ได้เดิม) ·
  GT-007 อัปเดต: เหลือชั้น client-observable ล้วน
- milestone ถัดไปที่เปิดได้ทันทีตามนโยบาย ⭐: candidate `0xAC52` chat (ต้องขอ Panya อนุมัติ
  hypothesis ก่อนออกแบบ response — เขียนคำถามค้างได้รอบหน้า) หรือ audit TeleportVital 0x25A2

## 32. รอบ 42 (2026-08-17 19:45–20:0x scheduled) — 🟢 **ประมวลผลรอบใหญ่ครบ → commit `b03d207`** + ดีไซน์ HYP-PF-013 พร้อม implement รอบหน้า

### 32.1 เข้ารอบ

LOCK = RELEASED (เซสชันหลักปล่อย 19:46) จับ ~19:45–19:47 · inbox ว่าง · outbox ครบคู่ถึง 081
· ตรวจ 072/073/080/081 ตรงกับผลในคิวทุกจุด · canonical sha ยืนยันซ้ำจาก sandbox = `FA794D0B..4400` ✓

### 32.2 ① ประมวลผล GT-001 PASS + GT-007 FAIL เสร็จครบ → **commit `b03d207`** (docs-only)

- **GT-001**: `reports/PF_GT001_POST_HYP012_CANONICAL_FULL_LOOP_SMOKE_RUNTIME_PASS_20260817.md`
  (+manifest 13 ไฟล์ รวม backup `pirateforce_before_gt001_20260817_192033.sqlite3` ที่ sha =
  CACE7F77 เดิม) — Grade B runtime pass หนึ่ง claim ที่ `b90007e` · TargetPos baseline 6 อีกครั้ง
  (ตรงรันก่อน — กฎ "mentions>0 ≠ เดิน" ยืนซ้ำ)
- **GT-007**: `reports/PF_GT007_LOGOUT_ECHO_ACK_CLIENT_TRANSITION_NEGATIVE_20260817.md`
  (+manifest 12 ไฟล์ รวมสำเนา run DB `pirateforce_gt007_20260817_192713.sqlite3` sha `F09743F6..`)
  — Grade B controlled runtime negative หนึ่ง claim: echo-only shape falsified ที่ชั้น client ·
  บันทึกบั๊กเครื่องมือ 081 (path-space) แยกชัดว่าไม่ใช่ผลเทส · บันทึกบทเรียนหน้าต่าง Claude บังปุ่ม
- **matrix**: `session_lifecycle/clean_logout` แก้ **notes อย่างเดียว** (คง in_progress) —
  digest ของ seam pin ไม่รวม notes โดยดีไซน์ → **ไม่ต้อง re-pin** (ยืนยัน: seam 22 เทสเขียว sandbox
  + gate เต็มเขียว Windows) · STATUS.md เพิ่มเนื้อ clean_logout ใน bullet Session lifecycle
- **gate จริง job `082`: ALL GREEN — pytest 415/0 (62s) · ledger PASS 19 · coverage PASS 8 ·
  diff --check exit 0** → commit → cleanup job `083` (tmp_obj 11→0 · HEAD.lock/stale เกลี้ยง)
- `b03d207` เป็น docs-only → **GT-001 ไม่ re-arm** ยังคง [PASS]

### 32.3 ② ดีไซน์ **HYP-PF-013 (LOGOUT-CLOSE-001): ack + server-initiated clean socket close** — พร้อม implement รอบหน้าใต้ pre-approval ข้อ 4

**Fact ใหม่ที่ขุดจาก GAME_LIVE ของ GT-007 (ไม่เคยบันทึกที่ไหน):** หลัง ack ไปแล้ว client
**ไม่ปิด socket, ไม่ reconnect, ส่ง keepalive `GSCN_RunTimeProtocolReq` ทุก ~2 วิ ไปเรื่อย ๆ**
(19:33:57 → 19:40:14 จน teardown) — client นั่งรอบางอย่างบน connection เดิมโดยไม่มีวันหมดเวลา
+ corpus เก่า (evidence/v74-v76 ฯลฯ) **ไม่มีเฟรม 0x1B40 เลย** (hit ที่ grep เจอเป็น offset column
ของ hexdump) = **ไม่มี golden response ของ logout ในหลักฐานทั้งหมด** → ต้องเดินแบบ hypothesis ต่อ

**Shape B ที่เลือก (เพิ่มจาก echo ให้น้อยที่สุดโดยไม่แต่งไบต์เอง):** ack เดิมของ PF-012 ทุกไบต์
→ ตามด้วย **server ปิด socket สะอาด (shutdown+close) หลัง ack ~250ms** ทั้ง subcode 01/03
(สโคป (ก) ของ Panya เดิม) — เหตุผล: คันโยกเดียวที่ server เป็นเจ้าของโดยไม่ต้อง invent payload
คือ TCP FIN และ fact ข้างบนชี้ว่า client ค้างบน socket ที่ไม่เคยถูกปิด
- opt-in scenario ใหม่ `scenarios/logout_hypothesis_ack_close.json`
  (`post_ack_action: "close_socket"`, `close_delay_ms: 250`) · production_allowed=false ·
  ไม่ใส่ธง = พฤติกรรม PF-012 เดิมเป๊ะ · อย่างอื่น fail closed เหมือนเดิม
- prediction (falsifiable): 01 → หน้าต่างปิดเอง/process จบ · 03 → หลุดจากแมพ (คาด disconnect
  dialog หรือกลับ server select — ถ้าได้ dialog error = shape B ถูก falsify บางส่วน ให้เก็บผลไว้)
- **Shape C (fallback บันทึกไว้ล่วงหน้า ยังไม่ implement):** ตอบ `0x3D4B` GetWorldInfoVital
  รูปแบบเต็ม (ยิงตอนเปิด dialog 7/7 — R40 decode ครบ 248B skeleton คงที่ เหลือ float32 4 ค่า)
  ก่อน ack — สมมติฐานว่า transition ถูก gate ด้วยคำตอบนี้ · ถ้าถึงจุดนี้ต้องเปิด hypothesis แยก
- **แผน implement รอบหน้า:** ขยาย scenario schema ใน `logout_hypothesis.py` + hook จุด post-ack
  ใน `runtime.py` (มีอยู่แล้วจาก PF-012) · เทสใหม่ ~6–8 ตัว (ordering ack→FIN · ไม่ปิดถ้าไม่มีธง ·
  pins เดิมไม่ขยับ · fail closed เดิมครบ) · ledger entry PF-013 + verifier + matrix notes ·
  headless proof job `084` (probe: login → ส่ง 0x1B40-03 → assert ack byte-exact → **socket EOF
  ภายใน window** → closed_at ordering ใน DB) · gate `085` → commit · เข้าคิว **GT-008**
  (client-observable) พร้อม boot/teardown `086/087` ตาม convention ใหม่

### 32.4 ③ แก้บั๊กตระกูล 069/081 ที่ต้นตอ — convention ใหม่ของ info file

`pf_bridge\templates\JOB_INFO_FILE_CONVENTION.md` (ใหม่): **หนึ่ง key ต่อบรรทัด · parse ด้วย
split ที่ `=` ตัวแรก · quote ทุก path ให้ native command · sanity check หลัง parse ห้ามรันต่อ
ด้วยค่าว่าง** — บังคับทุก job ตั้งแต่ `084` เป็นต้นไป (072/073 staged เดิมไม่แตะ เพราะ proven แล้ว
และไม่มี run-copy path)

### 32.5 ตั้งใจไม่ทำ + งานแม่บ้านค้าง

ไม่ implement PF-013 ในรอบนี้ (gate+commit ของ ① กินรอบไปแล้ว — ดีไซน์พร้อมให้รอบหน้าเริ่มเขียนโค้ดทันที)
· ไม่แตะ lease file เดิม · ไม่ลบสำเนา run DB GT-007 (pin ใน manifest แล้ว — เป็นหลักฐานถาวร)
· 🧹 **archive ค้าง:** CHIEF_CONTINUATION 417KB / QUEUE 139KB เกินเกณฑ์ทั้งคู่ — รอบนี้มีงานหลักเต็ม
ตามนิยาม "รอบแรกที่ว่าง" จึงยังไม่ทำ → **รอบหน้า: ถ้า implement PF-013 ให้ archive รอบถัดจากนั้น
ถ้า idle ให้ archive ทันทีเป็นงานแรก**

### 32.6 คิวรอบหน้า

1. ⭐ implement **HYP-PF-013** ตามแผน 32.3 ให้จบถึง headless proof + commit ในรอบเดียวถ้าไหว
   (แตะ src/ → GT-001 จะ re-arm ตอนนั้น)
2. 🧹 archive ไฟล์กลางสองไฟล์ (ตามเงื่อนไข 32.5)
3. งานรอง: candidate `0xAC52` chat — **ตาม pre-approval ข้อ 4 เปิด hypothesis ได้เลย**
   (แก้ความเข้าใจรอบ 41 ที่ว่าต้องขอ Panya ก่อน — นโยบาย 18:2x ครอบคลุมแล้ว) · audit TeleportVital 0x25A2

## 33. รอบ 43 (2026-08-17 20:05–20:3x scheduled) — 🟢 **HYP-PF-013 implement → headless proof → commit `f7b85b9` จบในรอบเดียว** + GT-008 เข้าคิวพร้อมรัน

### 33.1 เข้ารอบ

LOCK RELEASED (รอบ 42 ปล่อย 20:03) จับ 20:05 · inbox ว่าง outbox ครบคู่ถึง 083 · แผน = implement
PF-013 ตาม 32.3 ให้จบ

### 33.2 Implement (ตามดีไซน์ 32.3 เป๊ะ ไม่มี deviation สำคัญ)

- `scenarios/logout_hypothesis_ack_close.json` ใหม่ — profile ที่สองใน exact allowlist
  (`post_ack_action=close_socket`, `close_delay_ms=250`, production_allowed=false) ·
  ack pins = ค่า PF-012 เดิมทุกไบต์ (ไม่ invent byte)
- `logout_hypothesis.py`: dataclass + allowlist สอง profile (echo/ack_close) — ไฟล์ echo เดิม
  ผ่าน loader เดิมโดยไม่แตะ · `runtime.py`: branch เดียวใน lane เดิม — หลัง closed_at commit +
  ack queued → `close_timer_factory` (inject ได้ในเทส) ตั้งปิด 250ms ผ่าน lever ที่ถูก attach ·
  **ไม่มี lever = fail closed ก่อนแตะ lease** (event `logout_hypothesis_close_unavailable_no_reply`) ·
  `connection.py`: `AcceptedGameSocket.bind` เสนอ lever `shutdown(2)+close` (idempotent) ต่อ connection
- เทสใหม่ `tests/test_logout_ack_close.py` 10 ตัว (ordering ack→close · echo ไม่ปิด · lever หาย
  fail closed · tamper allowlist 4 แบบ · post-ack silence ใน close window · bind lever ordering
  บน fake socket · duplicate/non-callable attach) — PF-012 suite เดิมผ่านครบไม่แตะ = ไม่ใส่ธง
  พฤติกรรมเดิมเป๊ะ

### 33.3 Headless proof + gate + commit

- **Sandbox loopback smoke ก่อนวาง job** (server จริงบูตใน sandbox ได้ — ครั้งแรกที่ใช้ทางนี้
  de-risk bridge job): ack byte-exact ทั้งสอง subcode · EOF ที่ ack+250.4/250.5ms · closed_at
  นำหน้า ack SENT ~6ms · run copy จาก canonical (sha ตรง `FA794D0B..4400` ยืนยันจาก sandbox อีกรอบ)
- probe ใหม่ `pf_bridge/replay/pf_hyp013_probe.py` (พัฒนาจาก hyp012: criterion ใหม่ = EOF
  หลัง ack ใน window 100–2000ms + ไม่มี dispatch frame อื่นคั่น)
- **job `084` Windows: probe exit 0** — 01: EOF ack+253.5ms · 03: EOF ack+254.1ms · closed_at
  นำ ack 4–5ms (GAME_LIVE vs DB) · open 0 · integrity ok · canonical ไม่แตะ · run DB เก็บเป็น
  หลักฐาน `state\pirateforce_hyp013_20260817_202207.sqlite3` (pin ใน manifest — ห้ามลบ)
- report `PF_LOGOUT_CLOSE001_HYP_PF_013_ACK_SOCKET_CLOSE_HEADLESS_WIRE_DB_20260817.md` +
  manifest 8 ไฟล์ · ledger append **HYP-PF-013 (LOGOUT-CLOSE-001, active)** → entries 20 ·
  canonical sha lineage → `741C5CE5..D984` ใน verifier · matrix clean_logout แก้ notes อย่างเดียว
  (คง in_progress — digest ไม่รวม notes ไม่ re-pin)
- **gate job `085` ALL GREEN: pytest 425/0 (415+10) · ledger PASS 20 · coverage 8 · diff clean**
  → **commit `f7b85b9`** (11 ไฟล์) → cleanup `086` (tmp_obj 20→0 · HEAD.lock เกลี้ยง) ·
  หมายเหตุ sandbox: full suite ที่นี่ 424+1 fail (`test_server_shutdown` อ่าน `__notes__` =
  ฟีเจอร์ 3.11+ ไม่มีใน py3.10 ของ sandbox — ไม่เกี่ยวไฟล์ที่แก้ · Windows py3.14 ผ่าน)

### 33.4 GT-008 เข้าคิว + GT-001 re-arm

- **GT-008** [PENDING พร้อมรัน] เข้าคิวหน้า GT-007: objective/steps/criteria สองชั้น/nonclaims ครบ ·
  staged `087_gt008_boot.ps1` (scenario ack_close + info file convention ใหม่ครั้งแรก) +
  `088_gt008_teardown.ps1` (parser first-= + sanity check + จับ client self-exit เป็น KEY observation)
- **GT-001 re-armed ที่ `f7b85b9`** (แตะ src/) — staged 072/073 ใช้ได้เดิม (canonical sha ไม่เปลี่ยน)
- prediction ที่แขวนไว้กับ GT-008 (falsifiable): 01 → client ปิดเอง · 03 → หลุดจากแมพ ·
  ถ้า disconnect-error dialog = falsify บางส่วน → เดินต่อ fallback 0x3D4B-first ใต้ entry ใหม่

### 33.5 ตั้งใจไม่ทำ + งานค้าง

ไม่ archive สองไฟล์กลางรอบนี้ (งานหลักเต็มรอบตามเงื่อนไข 32.5 — **รอบหน้า: archive เป็นงานแรก
ถ้าไม่มีอะไร urgent กว่า**) · ไม่เริ่ม 0xAC52 chat (รอบหน้า ②) · ไม่แตะ lease file เดิม ·
ไม่ลบ run DB 084

### 33.6 คิวรอบหน้า

1. 🧹 **archive CHIEF_CONTINUATION.md (~437KB) + GAME_TEST_QUEUE.md (~146KB)** ตามเกณฑ์แม่บ้าน
   18:4x — งานแรกของรอบ ถ้าไม่มี urgent
2. งานหลักถัดไป: **`0xAC52` chat hypothesis** (pre-approval ครอบคลุม — เปิดได้เลย) ·
   audit TeleportVital `0x25A2`
3. ถ้ารอบใหญ่เกิดก่อน: ประมวลผล GT-008 + GT-001 ตามลำดับหน้าที่ ①

## 34. รอบ 44 (2026-08-17 23:12–00:1x scheduled) — 🟢🧹 **archive ไฟล์กลางสำเร็จ** + 🟢 **HYP-PF-014 chat echo: implement → headless proof → Windows gate 089 GREEN → commit `05c33e7` จบในรอบเดียว** · GT-009 เข้าคิวพร้อมรัน

### 34.1 งานแม่บ้าน (คำสั่ง Panya 18:4x — เลื่อนมาสองรอบ ทำแล้วรอบนี้เป็นงานแรก)
- ย้ายก้อนเก่าไป `pf_bridge\archive\CHIEF_CONTINUATION_ARCHIVE_20260817.md` (7 ก้อน A–G: ☕ รอบ 26→M13, §4 สถานะ 07:19, §5 milestones M1–M14, §6 คำถามตอบแล้ว, §8–9 log เช้า, §17–30 รอบ 27–40) และ `GAME_TEST_QUEUE_ARCHIVE_20260817.md` (GT-007/002/003/005/006) — **verbatim ทั้งก้อน + pointer หนึ่งบรรทัดแทนที่ ไม่ลบอะไร** · ตรวจ integrity ด้วย multiset ของทุกบรรทัดเดิม = **0 missing**
- ผล: CHIEF 431KB→55.5KB · QUEUE 146KB→48.5KB (ต่ำกว่าเกณฑ์ 100/60 ทั้งคู่)

### 34.2 ⭐ HYP-PF-014 (CHAT-ECHO-001) — เฟรมแชท `UNKNOWN_0xAC52` ได้ designed echo-ack ครบวงจร
- ฐาน: GT-006 grade B (payload 34B = prefix 10B `48 00 00 00 00 48 18 00 00 00` + 12 ตัวอักษร ASCII UTF-16LE · server ไม่เคยตอบ) · pre-approval ข้อ 4 ครอบคลุม — ไม่ต้องถาม
- แบบ: **shape-pin fail-closed** (ต่างจาก 012/013 ที่ hash-pin ได้เพราะ payload คงที่ — แชทผันแปรตามข้อความ): รับเฉพาะ 34B + prefix ตรง 10B + 12 คู่ (printable ASCII, 0x00) → echo vital เดิมกลับใน envelope Res (pc 56B / frame 66B) · probe ทั้งสองของ GT-006 ตรึง sha256 ระดับ fixture · **no-write lane** (แชทไม่มีตาราง — persisted_post_state: database_write none) · opt-in `scenarios/chat_input_hypothesis_echo.json` (`production_allowed=false`) · mutually exclusive กับ scenario อื่นตาม pattern เดิม · echo ได้หลายครั้ง/ไม่ one-shot · ledger `HYP-PF-014` → **entries 21** (canonical sha `6933C363..E312`) · matrix แถวใหม่ `chat/chat_input_echo_hypothesis` (in_progress ตาม pattern 012) · เทสใหม่ 15
- ลูกมือ (subagent) implement ตามสเปก — ข้อสังเกตของลูกมือที่มีค่า: `test_presentation_ownership.py` ตรึง negative "ห้ามเอ่ย 0xAC52" และ docstring ตัวเองสั่งให้แก้พร้อมกัน → ย้าย pin เป็น exact-allowlist `[chat_input_hypothesis.py, runtime.py]` · smoke ในแซนด์บ็อกซ์ต้อง boot+probe+teardown ใน bash call เดียว (process ตายเมื่อ call จบ)
- proof: sandbox smoke (server จริง + TCP loopback + เฟรม client จริงจาก capture): echo byte-exact 66B ทั้ง probe1/2 (+9.5/+1.7ms) + probe1 ซ้ำ (+1.5ms) · heartbeat เดินต่อ · **DB sha ไม่ขยับคร่อมช่วงแชท** · SIGINT ปิดสะอาด · หลักฐาน commit แล้วใน `reports/chat_echo001_smoke/`
- **job 089 Windows gate ALL GREEN: pytest `440 passed / 0 failed` (425+15) · ledger 21 · domains 8 · diff clean** → commit **`05c33e7`** (dirty เหลือ lease ไฟล์เดิม · HEAD.lock → .stale ตามกฎ) · report `PF_CHAT_ECHO001_CHAT_INPUT_ECHO_HYPOTHESIS_HEADLESS_20260817.md` + manifest
- **เกณฑ์ gate เขียวใหม่ = pytest 440/0 + ledger 21 + domains 8** (sandbox: 439+1 fail `__notes__` py3.10-only = ปกติ)

### 34.3 คิวรอบใหญ่ (อัปเดตแล้ว)
- **GT-009 ใหม่ [PENDING พร้อมรัน]**: chat echo client-observable — staged `090_gt009_boot.ps1`/`091_gt009_teardown.ps1` (clone ตรรกะ 087/088 ที่พิสูจน์แล้ว, ASCII ตรวจแล้ว 0 non-ascii) · ⚠️ scenario mutually exclusive → รอบ GT-009 ออกเกมด้วย End task เท่านั้น (logout ack ไม่ทำงาน)
- GT-008 [PENDING เดิม] staged 087/088 · GT-001 **re-armed ที่ `05c33e7`** (072/073 เดิมใช้ได้)
- ลำดับแนะนำรอบใหญ่: GT-008 → GT-009 → GT-001 (GT-008 ก่อนเพราะถ้า PASS ผู้เทสได้วิธีออกเกมสะอาดไว้ใช้ แต่ GT-009 ยังต้อง End task อยู่ดีเพราะบูตคนละ scenario)

### 34.4 ค้างไว้รอบหน้า
- audit `0x25A2` (จาก next รอบ 43 ข้อ ② — รอบนี้หมดโควตาที่ chat แล้ว) · ประมวลผลรอบใหญ่เมื่อ Panya ปลุก · ทางเลือกออกแบบต่อถ้า GT-009 client เงียบ: เพิ่ม speaker id/prefix ใน echo (เปิด entry ใหม่ ห้ามแก้ 014)

## 35. รอบ 45 (2026-08-17 23:57–00:2x scheduled) — 🟢 **TELEPORT_AUDIT001: audit `0x25A2` จบ → commit `9f5e6a2` (docs-only)** — คำตัดสิน: ไม่เปิด hypothesis ไม่แตะ server

### 35.1 ผล audit `0x25A2` (ค้างจาก next รอบ 43)

- **ทิศทางจริง = client→server**: client ส่ง `TeleportVital 0x25A2` v4 **หนึ่งครั้งต่อเซสชันเสมอ**
  เป็น vital ตัวแรกของ RunTimeProtocolReq ก้อนแรก (frame=4) หลัง server ส่ง login teleport 3ms–1.2s ·
  payload 11 ไบต์ `0B02 0B00 0B00 0B00 0F0000` **byte-identical 14/14 เซสชัน** (corpus r17–r23)
  = schema เดียวกับขาออกของ server แต่ target count 0 (ไม่มี target object) — อ่านเป็น "teleport
  acked/arrived" ได้แต่เป็น nonclaim (ไม่มีเซสชัน counterfactual)
- bundle แรกมี 2 variant (ต่างกันนอก 0x25A2 ทั้งหมด): A 190B ×13 = [0x25A2 · **AskForSystemGiftVital
  0x8B93** (ชื่อจาก VITAL_REGISTRY client binary — ไม่อยู่ในตาราง v141) · UpdateServerSetting 0x0F01 ·
  TargetPos 0x2A90] · B 95B ×1 (r22_replay หลัง movement replay) = [0x25A2 · 0x8B93 · OnLand 0x1EB4 ·
  TargetPos 0x2A90]
- **คำตัดสิน (fail-closed): ไม่เปิด hypothesis ไม่ออกแบบ response** — ① ไม่มีอะไรค้าง (generic
  first-Req ack พอ ทุกอย่าง downstream พิสูจน์แล้ว) ② `references/sources/` ว่าง = ตอบเฉพาะทางคือ
  invented bytes ③ pre-approval 18:2x ครอบ "ปุ่ม/ฟังก์ชันที่ไม่มี handler และขวาง gameplay" — อันนี้ไม่เข้าเงื่อนไข ·
  revisit triggers เขียนไว้ในรายงาน (stall หลัง entry / เจอ 0x25A2 ตัวที่สองหลัง MARKER transport / มี reference โผล่)
- open observation (nonclaim ทั้งคู่): TargetPos ใน bundle A = (-9098.55,-2866.86,186.0,h2.9944)
  **ไม่ตรง** persisted character_positions (-8094.61,-3207.83,186.0,h2.4993) — ความหมาย field ยังไม่ resolve ·
  0x8B93 payload `0B00 0B00` ได้แค่ generic ack ทุกเซสชัน
- deliverables: report `PF_TELEPORT_AUDIT001_CLIENT_25A2_FIRSTREQ_ECHO_CORPUS_20260818.md` + manifest
  (5 ไฟล์) · sweep script ถาวร `pf_bridge/replay/pf_teleport_audit.py` (read-only ใช้ซ้ำได้) · matrix
  movement/teleport_transport **แก้ notes อย่างเดียว** (เจอจริงว่า ratchet `CoverageProvenanceTests`
  pin ทั้ง digest และ manifest-debt list ครอบ evidence_refs → เพิ่ม ref แล้ว fail 3 ตัว จึงถอนกลับเป็น
  notes-only ตาม precedent รอบ 43 — เขียน path รายงานไว้ใน notes แทน)
- **commit `9f5e6a2` (docs-only: report+manifest+.gitignore+matrix notes)** — ไม่แตะ src/ →
  **GT-001 ไม่ re-arm** staged 072/073 ใช้ได้ที่เดิม · sandbox pytest full = **439+1 fail py3.10-only = baseline ตรง** ·
  ไม่วาง Windows gate (docs-only ตาม precedent `b03d207`) · job `092` cleanup tmp_obj (33 ตัว) วางใน inbox แล้ว

### 35.2 คิว/สถานะ

- GAME_TEST_QUEUE: เพิ่มบล็อก 👁️ observation แถมรอบใหญ่ (เช็ค 0x25A2 ตัวที่สองหลัง transport ·
  จด gift UI ค้าง) — ไม่เพิ่ม step ให้ผู้เทส
- backlog pre-approved ว่างแล้ว (0xAC52 done รอบ 44 · 0x25A2 audit done รอบนี้) — สาย gameplay ใหม่
  รอผลรอบใหญ่ (GT-008/009/001) เป็นหลัก · candidate ถัดไปถ้าอยากเดินก่อนรอบใหญ่: ยกระดับ
  clean_logout/chat จาก in_progress สู่ขั้นถัดไปตามผล GT หรือเปิด lane persistence characters/accounts
  (write path ยังไม่มี — เป็นงานสถาปัตยกรรม ควรเขียนดีไซน์ให้ Panya เห็นก่อน)

### 35.3 คิวรอบหน้า

1. เช็ค outbox `092` (cleanup) — ถ้า tmp_obj เหลือ 0 = จบ
2. ประมวลผลรอบใหญ่เมื่อ Panya ปลุก (GT-008 → GT-009 → GT-001 + observation 👁️)
3. ถ้ายังไม่มีรอบใหญ่: ร่างดีไซน์ persistence characters/accounts write path เป็นคำถามค้างให้ Panya
   (ไม่ implement ก่อนเคาะ — สถาปัตยกรรมใหญ่นอก pre-approval)

