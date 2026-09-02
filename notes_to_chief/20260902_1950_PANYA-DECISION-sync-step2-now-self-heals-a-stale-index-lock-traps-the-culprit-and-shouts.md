# PANYA DECISION - sync step [2] self-heals a stale index.lock, traps whoever makes it, and shouts

- decided by: **Panya**, in the attended session, ~2026-09-02 19:30 (+07:00), approximate
- channel: chat, her exact answer was "take all 3"
- written by: ka1-A as her proxy writer
- patched file: `pf_bridge\pf_git_sync.ps1` step [2] (backup:
  `agent_kit\pf_git_sync.ps1.pre_patch_indexlock_20260902`)
- verified: PowerShell parser 0 errors, `-SelfCheck` exit 0, and a LIVE round at 19:48
  completed normally with `committed=1`

## Why she decided this

A 0-byte `.git\index.lock` blocked **every** sync round from 18:02:37 to 19:16 - **74
minutes** - during which nothing was committed, nothing pushed, and the whole GT-207
round's letters sat on the disk. The only trace was `SKIP_INDEX_LOCK git busy` repeated
in the log. Nobody would have noticed if the owner had not been at the keyboard.

Then the forensic hunt found this is the **sixth** occurrence, not the first:

```
2026-09-02 10:36  .git\STALE_index.lock.ka1B_1788320230
2026-09-02 10:30  .git\STALE_index.lock.ka1B_1788319856
2026-09-02 01:58  .git\STALE_index.lock.ka1B_1788289155
2026-08-31 16:57  .git\STALE_index.lock.ka1B_095807
2026-08-31 16:56  .git\STALE_index.lock.ka1B_20260831
2026-08-20 12:10  .git\STALE_index.lock_20260820_1210_delete_me   (staged jobs 168/169)
```

Five of them were renamed out of the way by the **ka1-B** session and never reported, so
the cause was never chased and the same outage kept recurring for thirteen days. That is
the failure this decision is aimed at as much as the lock itself.

## What changed, all three parts

**(1) self-heal, under three guards that must ALL hold**
`$INDEX_LOCK_STALE_MIN = 10`. The lock is deleted only when it is **0 bytes**, at least
**10 minutes old**, and **no git-family process is running**. Any one of those failing
means the block does not touch it. A non-empty lock is never deleted, on any age: a
non-empty lock means a git process wrote into it.

**(2) the trap** - `sync_state_index_lock_witness.log`, written beside the repo, appended
once per episode: the lock's size and mtime plus every running process (name / pid /
start time) matching git, powershell, pwsh, cmd, conhost, py, python, node, GameClient,
Code, ssh. **Next occurrence names the culprit.** Today nothing on the machine records
it - Windows process auditing is off - which is why the honest answer to "who did it"
is still *unknown*.

**(3) the alarm** - `$INDEX_LOCK_ROUNDS_BEFORE_LETTER = 5`. After five consecutive skips
(about ten minutes) step [2] writes ONE `SYNC-ALARM-index-lock-*` letter into
`notes_to_chief\`, then mutes until the lock clears, exactly like the step [5] alarm.

## What is deliberately NOT claimed

- Nobody knows which process creates these. The 0-byte size is consistent with a git
  process killed between creating the lock and writing into it, and no more than that.
- `PF_Git_Sync` is the most-exposed suspect only because it is the thing that runs git
  writes here every two minutes. That is exposure, not evidence.
- ka1-A does not exclude its own tooling, per the standing entry in `LOOSE_ENDS.md`.
- No self-check test was added for the new block. The 14-test harness is still red on 5
  of its own tests (`LOOSE_ENDS` item 2, still unowned), so a new test there would be
  landing in a harness nobody trusts yet.
