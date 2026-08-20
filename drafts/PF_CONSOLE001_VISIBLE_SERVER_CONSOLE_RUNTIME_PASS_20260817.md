# PF-CONSOLE-001 — Visible Server Console Runtime Pass (2026-08-17)

> DRAFT เตรียมโดยเซสชันหลัก (มี context เต็ม) — ผู้ commit: ตรวจตัวเลขกับหลักฐานดิบ
> แล้วย้ายไฟล์นี้เข้า `reports/` ใน main worktree, เพิ่มบรรทัด `!/reports/...` ใน
> `.gitignore` ทั้งสอง worktree ถ้าจำเป็น, สร้าง `.manifest` คู่กัน แล้ว commit เป็น
> runtime-result commit แยก

## Primary claim (Grade B)

One controlled run proves the visible-console platform contract end to end:
a real visible console window for an actual server invocation, deterministic
UTF-8 mirrored summary logs, raw logs file-only, one bounded requested stop via
CTRL_C_EVENT, exactly one `[FOUNDATION] stopped` marker, and exit code 0 for
both the launcher shim and the server process.

## Evidence (controlled run 2026-08-17 03:14 ICT)

- Launcher `tools\run_foundation_visible.ps1` (console worktree, commit `0e922b6`)
  reported shim PID 11656; listeners 10188/10189 owned by server PID 4840.
- Shim window title:
  `Pirate Force Foundation Server | foundation | console_m1_20260817_031427.sqlite3`
- Bounded helper (AttachConsole + GenerateConsoleCtrlEvent, outside repo)
  returned `ctrl_c_sent=true` at 2026-08-16T20:14:43.551Z (UTC).
- Server exited 20:14:43.919Z, shim 20:14:43.933Z — **both exit code 0**
  (handles cached before exit; WaitForExit(30000) true for both).
- Mirror stdout 12,021 bytes: `[FOUNDATION] visible console` ×1,
  `[FOUNDATION] stopped` ×1. Mirror stderr 0 bytes.
- No listener and no python/py process remained.
- Disposable DB copy byte-identical before/after
  (`EA1C4459F9E88322EE4689B2C2A13C0465CF57BE35F2B47FEB1ED6D74EDD8F3B`);
  evidence source DB untouched (same hash).
- Full verifier T3 on the console worktree: PASS exit 0, 234 tests OK
  (job 001, 2026-08-17 02:51), after gitignored read-only copies of the required
  `backups/`/`evidence/` artifacts were placed in the worktree.
- Raw logs: `pf_bridge\outbox\004_runtime_exitcode_20260817_031427.utf8.txt`,
  capture root `GameClient\capture_console_m1_20260817_031427\`.

## Supplementary Grade B: first full gameplay loop on the canonical DB (04:17–04:24 ICT)

- Canonical play database established: `state\pirateforce.sqlite3` seeded from
  the newest baseline evidence DB (Arena01; backpack `[1@0,2@1,4@3]`); previous
  empty file backed up at `pf_bridge\backup\pirateforce.sqlite3.empty_pre_seed_20260817`.
- Old server (wrong post-move DB) stopped: exit 0. New server shim 3496 /
  server 6736 on the canonical DB, `--second-password-mode bypass`.
- Unchanged GameClient (`GameClient.local.bin`, SHA-256
  `9627...B623`) launched via CreateProcess: server select → PVP notice confirm
  → character select (Arena01 nameboard rendered) → **StartGame → Port Royal
  loaded in-map**: HP 100/100, LV.1, minimap, X:-9038 Y:-2866, system chat
  "Pirate Force local server online" (direct screenshot retained:
  `pf_bridge\backup\DEMO_INMAP_PortRoyal_Arena01_20260817_0422.jpg`).
- Clean client exit via in-game X + confirm dialog. Requested server stop:
  server exit 0, shim exit 0, stopped marker ×1, stderr 0 B, listeners 0.
- Post-run canonical DB: integrity ok; exactly one session
  (`08509a0d...`, lease_generation 1) opened 21:21:12.475Z closed 21:23:18.557Z;
  backpack unchanged.

## Defects found and fixed during this milestone (operational)

1. `GameClient\run_v142_client_only.bat` never launched the client on this
   machine: `start ""` uses ShellExecute and `.bin` has no association —
   **zero process was created, silently**. Fixed with
   ProcessStartInfo/`UseShellExecute=$false`; arguments unchanged; original
   kept as `run_v142_client_only.bat.orig.bak`. (`Start-Process -FilePath *.bin`
   fails the same way — do not use it.)
2. The WIP `session.py` guard rejects a non-baseline backpack silently (no log,
   empty stderr) — cost a full diagnostic round. M3 must add an explicit reject
   log line.

## Nonclaims

One requested-stop path through this exact helper/console host only. Not crash,
power-loss, every-signal-source, concurrent-client, remote-client or
authenticated multi-account proof. The gameplay loop adds no inventory, combat
or protocol claim beyond already-accepted ceilings; the in-map screenshot is
operator-grade visual evidence, not a new wire claim. Inventory remains
INCOMPLETE.
