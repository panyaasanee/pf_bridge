# LANE-GM round `owqad2` -- close pf-adversary D6: add O_BINARY to the two raw GM writers

Started 2026-09-06T20:46+07:00 - claim `pf_bridge#1559`

## Start (COMMON order)

1. `NOW.md` (fetched fresh, checked 19:55 by COO) -- nothing orders LANE-GM directly except the
   already-known state: "LANE-GM: `/lv` done -> P-3 GM buttons 3 pages = `GT-279`" -- that ticket
   waits on Panya's machine, not on code from this lane. `GM-063` withdrawn, `/speed` closed until
   the login mask lands, `/warp <n> <x> <y>` closed permanently, same-scene `/warp <n>` = spawn --
   none of these have new instructions this round.
2. Mailbox `ADDRESSEE: LANE-GM` without `.CONSUMED.txt` -- **0 letters** (checked every file the
   grep matches; the three that lack a stub are LANE-GM's own outgoing reports, where the string
   `ADDRESSEE: LANE-GM` appears only inside a quoted sentence describing this exact grep, not as
   the letter's own `ADDRESSEE:` line -- verified by reading each one's real `ADDRESSEE:` line).
3. `AGENTS.md` section 7 -- read, no new rule that changes this round's plan.
4. Latest round file `rounds/GM_20260906_1913_lkwmkp_...md` "next round" list:
   1. Check status of that round's server PR (`#944`) first -- **merged** (confirmed:
      `git merge-base --is-ancestor <944 head sha> origin/main` true, and `origin/main` HEAD
      is the merge commit of `#944`). Gate went green; no repeat of the same red signature.
   2. `GT-279` (P-3 GM buttons) -- still waits on Panya's machine, nothing to do here.
   3. **D6** (Windows CRLF risk from missing `os.O_BINARY`) -- this round's main work, below.
   4. D4 (COO decision `1940` on `_best_effort_unlink` retry) -- still no reply in the mailbox
      this round; left for whenever COO answers.

Clock check: system UTC `13:46:44` == Bangkok `20:46:44`, matching this round's own timestamp
command exactly; the most recent commit on `pf_bridge` main (`757a4d4d`, 20:39 Bangkok) is 7
minutes old at round start, corroborating the clock independently of the heartbeat file.
`notes_to_chief/_BRIDGE_HEARTBEAT.txt`'s last line is `19:00:02` (1h46m behind) -- NOT a clock
skew on this side (both independent checks above agree with the OS clock); `NOW.md`'s own
19:55 note already explains the gap ("Panya's machine off around 19:0x ... heartbeat normal") as
a known, already-reported state, not a new problem this round needs to escalate.

## Lock

`list_pull_requests`/`search_pull_requests` state=open, title starting `[LANE-GM] round`, in
`pf_bridge`: **empty** before this round opened its own. Branch cut from `origin/main` (`757a4d4d`),
claim file pushed, PR `#1559` opened (not draft, no marker in body). Listed again immediately
after: only `#1559`, nothing older -- did not lose to anyone.

## What was built (write zone: `gm/` only)

**Defect** (pf-adversary D6, round `lkwmkp`, left open there): `gm/command_capture.py`'s
`capture_raw_gm_command` and `gm/commands.py`'s `_append_audit_record` both write through a raw
`os.open()` + `os.write()` pair, and `os.O_BINARY` appears nowhere in `src/`, `tests/`, or
`tools/` in this project (grepped before writing anything). The trusted gate runs on
`windows-latest`; without the flag, Windows' C runtime opens the descriptor in its default
text-translation mode, and a raw `os.write()` against that descriptor can have an embedded `\n`
silently turned into `\r\n` -- corrupting the capture file's own "lossless copy" promise and the
ndjson audit log's one-line-per-record contract, and desyncing both functions' short-write retry
loops (which assume every byte handed to `os.write()` either lands unchanged or is reported back
as not written) from what actually lands on disk.

**Fix**: `getattr(os, "O_BINARY", 0)` OR'd into both `os.open()` flags arguments -- the real flag
on Windows, a no-op on POSIX where the attribute does not exist. One line changed per call site.

**Tests**: two per call site in `tests/test_gm_command_capture.py` and `tests/test_gm_commands.py`
-- one monkeypatches `os.O_BINARY` to a sentinel bit (absent on this Linux host) and spies on
`os.open` to assert the bit is threaded through; the other pins the flags value is byte-for-byte
unchanged when the attribute is absent, proving the fix is a true no-op on every platform this
suite runs on today.

**Mutant check**: reverted the `getattr(...)` addition on both call sites (temp copy, restored
after), re-ran the four new tests -- both "available" tests fail, both "absent" tests still pass.
Restored, full targeted run green again (83 passed).

## pf-adversary (ordered at round start, result returned before push)

Six findings reported; the one that mattered pre-push:

**Confirmed, fixed in this round's commit**: the sentinel-bit tests originally delegated to the
*real* `os.open()` with the untested sentinel bit still set in the flags forwarded to it --
harmless on this Linux host (an unrecognized `oflag` bit is silently ignored), but that exact bit
has never been asked of the real Windows CRT open call this fix targets, and Microsoft documents
an unrecognized `oflag` as unspecified behaviour, not guaranteed-ignored. A red Windows gate from
that would have read as "this fix broke Windows" when the real cause would have been the test
itself sending a syscall a value nothing asked it to accept. Fixed: the spy now clears the
sentinel bit before delegating to the real `os.open()`, recording the requested flags for the
assertion without ever letting the untested bit reach a real syscall. Re-verified: targeted tests
green, mutant check still kills the same two mutants after this change.

Other findings (diagnosis-confirms-correct, no-exact-flags-assertion-breaks-elsewhere,
no-signature-check-anywhere-in-suite) did not require a code change -- see the PR body
(`pirate-force-server#950`) for the full list.

A procedural note the adversary itself raised: it was told to review "before this fix is
written" but the fix had already landed on the branch by the time it read the tree, because this
round writes code and orders the adversary in parallel rather than serially (per
`COMMON_LANE_ROUND.md`'s own "ordered at the start of the round, not before commit" rule for
short work). Noted here rather than re-run, since its finding above still applied to the
byte-identical diff either way and was acted on before push.

## Evidence (two layers)

**Scanner/unit layer** -- `pytest tests/test_gm_command_capture.py tests/test_gm_commands.py`:
83 passed.

**Full suite** -- `pytest tests/` on a tree with `origin/main` (`cf961bef` on the server side)
already an ancestor (no merge needed): **12484 passed, 369 skipped, 26243 subtests passed, 1
failed** -- `tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::test_the_talk_trigger_is_still_missing_at_real_dispatch_today`.
Checked out `origin/main` HEAD detached (this round's commit not present) and re-ran that one
test in isolation: **same failure**. Pre-existing, outside `gm/`, not caused or touched by this
round. Reported separately: `notes_to_chief/20260906_2046_LANE-GM-REPORT-COO-lane-a-test-red-on-main-not-gm.md`.

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`: **PREFLIGHT PASS**
(cp874, skips, mainmerge, census, branch, bridgesize, queuegrowth, filenamelen,
scoreboard-manual all green).

PR: **`pirate-force-server#950`** -- open, not draft, `PF-AUTOMERGE: v4` present (confirmed by
GET after open), one commit, 164 additions / 2 deletions across 4 files (2 production lines
changed, the rest is comments and tests).

## nonclaims

- Not claiming the Windows gate will be green -- the O_BINARY fix is reasoned from CPython/CRT
  documented behaviour and mutant-verified on Linux only; no Windows machine exists in this
  cloud environment to measure the actual CRLF translation this fix targets.
- Not claiming `tests/test_lane_a_choose_npc_scene1.py`'s failure is understood, fixed, or even
  new as of this round -- only that no earlier LANE-GM round file names it and it is outside this
  lane's write zone. Reported, not touched.
- Not claiming `GT-279` or D4 (COO decision `1940`) moved this round -- both still wait on
  something outside this lane's control (Panya's machine; a COO decision not yet in the mailbox).
- Not claiming this closes every Windows-only byte-fidelity question in this module -- pf-adversary's
  other finding (D6's own sibling concern about CRT `_fmode` defaults elsewhere, if any) was not
  re-opened this round; only the two `gm/` call sites named in round `lkwmkp`'s D6 were touched.

TWO_SESSIONS_SAME_SCENE: not affected -- both writers are per-command file writes, no per-scene
world state shared between sessions, no frame sent to any client.

NO_FEATURE_WAITING: not affected -- this round did not consume an RE result.

QUEUE_TRIAGE: did not touch `GAME_TEST_QUEUE.md` this round -- not this lane's job per `NOW.md`
("LANE-K owns queue files").

## Letters this round

- Sent: `20260906_2046_LANE-GM-REPORT-COO-lane-a-test-red-on-main-not-gm.md` (new letter, not a
  reply to any pending mailbox item -- mailbox was empty at round start).
- Consumed: none (mailbox had 0 pending `ADDRESSEE: LANE-GM` letters at round start).

## Next round

1. Check status of `pirate-force-server#950` (this round's PR) first, same pattern as this round
   checked `#944` -- if gate red, read the actual failure before assuming it is D6-shaped.
2. `GT-279` (P-3 GM buttons) -- still waits on Panya's machine + bridge reachability.
3. D4 (COO decision `1940`, `_best_effort_unlink` retry) -- check mailbox for a reply.
4. Check whether COO/chief replied about the new `tests/test_lane_a_choose_npc_scene1.py` red-main
   report -- if it is already known to LANE-A, mark this lane's own copy of the finding
   understood and move on; if not, nothing further for this lane to do (LANE-A's write zone).

SCOREBOARD: COMING | No new on-screen player behaviour this round (Windows-only file-write byte
fidelity is an internal correctness fix, not a feature) -- but the capture file and GM-command
audit log are now protected against a silent Windows-only CRLF corruption that neither's own
short-write safety net could have caught, closing a defect flagged by a previous round's
adversary pass and left open for a full round | `pirate-force-server#950` (open, not draft,
PF-AUTOMERGE: v4 confirmed, pf-adversary finding addressed pre-push, mutant-verified) +
`pf_bridge#1559` (this claim) + full suite 12484 passed / 1 pre-existing unrelated failure
(confirmed present on origin/main without this round's changes)
