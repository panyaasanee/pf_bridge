# R245 (session `nnlka4`) -- 2026-08-30T~17:5x-18:xx+07:00

## Round-lock recovery check (step B of the runbook, section 2 item 7)

Most recent prior `[LANE-E]` PRs (excluding this round's claim), confirmed via
`pull_request_read(method="get")` (list_pull_requests' own `merged` field is unreliable --
it reported `false` for PRs the git log on `main` proves were merged, e.g. `pf_bridge#507`;
only the per-PR `get` call's `merged`/`merged_at` fields were trusted):

- `pf_bridge#510` (R244, session `7ohcx5`): **merged=true** (`merged_at` 2026-08-30T10:09:36Z).
- `pirate-force-server#320` (R244, session `7ohcx5`): **merged=true** (`merged_at`
  2026-08-30T10:17:09Z).

Both repos' previous round landed on `main`. Nothing lost, no cherry-pick needed.

## Mailbox triage

Read the newest letters addressed to chief/LANE-E/everyone that arrived since R244 closed
(`~17:0x-17:5x`). Full list of what was consumed this round, with what was done for each, is
in the round-end letter to the attended tester. Highlights:

1. **KA1A-FINDING (`pf_bridge#507` drafts can starve a lane's own round-lock indefinitely)**
   -- real bug, fixed this round. See "What was done" below.
2. **Four COO-DECISION letters** answering R244's two escalations (force-pos unlock deadline
   moved to 2026-08-31 09:00, no code touched this round; loot-reorder invariant stands, no
   action; label-life rule stands, not chief's; RE-162 consumer-contract role accepted by
   COO, chief's obligation is future-conditional on RE-162 closing positive).
3. **GT-145 RESULT** (console encoding measured, four values match prediction) -- asked chief
   to fix a hardcoded canonical-sha value in its own `GAME_TEST_QUEUE.md` entry that would
   cause a false ABORT on the next boot. Fixed. Also flipped GT-145's status PENDING -> DONE
   (wire/DB layer only, N/A client-observable by the ticket's own design).
4. **LANE-GM's `spawn` wire-status question** (from the newer `LANE-GM-REPLY` at 17:39):
   is there ANY mid-session mob-creation factory anywhere in the engine, before LANE-GM
   writes a CORE-REQUEST for it? Delegated to `pf-static-re` for an independent second pass
   (LANE-GM had already grepped and found nothing, but the owner is specifically interested
   in `spawn`, so a second confirmation was worth the round). Answer: **bounded-negative,
   confirmed** -- no such factory exists in `src/` or `gm/` anywhere. One near-miss flagged
   (`mob_diag_multi_object.py`'s five-clone diagnostic scaffold, boot-census-time only, not a
   precedent for mid-session spawning) so LANE-GM doesn't accidentally cite it as one.
   Replied in `20260830_1804_CHIEF-REPLY-no-mid-session-mob-spawn-factory-*.md`.
5. Stubbed one now-superseded `LANE-GM-STATUS` letter (`1518`, "rule F invoked, all backlog
   blocked on chief") -- all three items it named (`GT-127`, `GT-128`, `GM-002`) were already
   resolved by R243/R244 before this round started; the letter itself just hadn't been
   marked consumed yet.

## What was done (this round's real work)

### 1. `pf_bridge/.github/workflows/merge-claude-pr.yml` -- fixed the stale-draft starvation bug

KA1A's finding, measured directly: `pf_bridge#507` ([LANE-A]'s own round-claim PR, real work
done, 3 files) sat in draft for roughly an hour. Every later LANE-A round saw its own open PR
at the start of the round and ended immediately -- **that check is correct behavior by
design** (an open PR of your own lane IS the round lock) -- but the old
`PF_STALE_HOURS='2'` reap threshold meant nothing would have force-closed that dead draft for
up to two full hourly cycles, well past LANE-A's own hourly cadence. The lane wasn't dead; it
was starving itself on schedule against a lock nobody was clearing in time.

Fix: renamed the env var `PF_STALE_HOURS` -> `PF_STALE_MINUTES`, value `'2'` (hours) ->
`'45'` (minutes) -- under the hourly lane cadence, comfortably above "a round lasts under an
hour" (the file's own stated normal case). Updated both `LIMIT`/`LIMIT2` computations
(`* 3600` -> `* 60`), all warning/comment strings that referenced the old name, and the
explanatory comment block at the env declaration to record the KA1A measurement as the
reason for the number. Ran the mandatory pre-commit checks for `.github/workflows/*.yml`
(section 7): the duplicate-key `yaml.safe_load` checker (no dup keys), `bash -n` on both
`run:` blocks (both OK), and an ASCII-only scan (clean). No `PF_STALE_HOURS` references
remain in the file.

Scope note: `pirate-force-server`'s own `merge-claude-pr.yml` was NOT touched this round --
it has a materially different architecture (`decide`/`reap` two-job split tied to the
Windows gate's verdict, `PF_STALE_HOURS='6'`, its own comment explaining it already keeps a
"hard reaper" on the server side per R219/#222) and deserves its own dedicated read rather
than a copy-paste of this fix. Flagged as a follow-up, not urgent (the KA1A finding was
specifically about the bridge-side symptom; no matching starvation measured on the server
side this round).

`#507` itself was already merged by the time this round's round-lock check ran (the owner
must have clicked "Ready for review" per KA1A's direct ask) -- no PR action needed for that
specific instance; this round only fixed the mechanism so it can't recur unbounded again.

### 2. `pf_bridge/GAME_TEST_QUEUE.md` -- GT-145 hardcoded canonical sha256 fixed, status closed

Per GT-145 RESULT's direct ask to chief. `db:` line's expected sha256 was a dead literal
(`673f4bfb1c35...`) instead of a `CANON_SHA.txt` reference -- every other queue entry in the
file uses the live-reference pattern; this was the one outlier the letter caught in the wild.
Replaced with a `CANON_SHA.txt` reference plus a one-line note explaining why (would have
caused a false `ABORT` on the DB-unchanged guard). Flipped the entry's status tag from
`[PENDING]` to `[DONE (wire/DB, N/A client-observable by design)]` with a pointer to the
result letter, since all five wire/DB pass criteria (a)-(e) were measured and the ticket's
own design declares the client-observable layer N/A.

Did not touch the two other judgment calls the same letter raised (`gate-windows.yml`
forcing `cp874:strict` as policy vs. the bridge's measured `cp874`-locale-but-utf8-stream
reality; `runtime_console.py:26`'s hardcoded `utf-8` constant vs. what happens when the
stream is piped/redirected instead of a real console) -- both are explicitly "chief decides"
per the letter's own nonclaim, and both need careful reasoning about behavior this cloud
environment cannot reproduce (no real Windows console, no cp874 locale here). Deferred to a
future round with room to think it through properly rather than a rushed edit to a file that
every unattended round depends on booting correctly.

## What was NOT done / deferred

- `FORCE_POS_VITAL_VERSION_CONFIRMED` unlock (COO's extended deadline: 2026-08-31 09:00) --
  needs a full round reading all 11 newly-discovered red tests one at a time before patching
  gates; this round's time went to the merge-workflow fix and mailbox triage instead.
- `pirate-force-server`'s own `merge-claude-pr.yml` reap-threshold review (see above).
- `gate-windows.yml` cp874 policy vs. measured reality, and `runtime_console.py`'s hardcoded
  encoding constant (see above).
- LANE-GM's `npc`/`item` wire-status notes are informational only this round; no
  CORE-REQUEST has been opened for either yet, so nothing to wire.

## Validation

- `.github/workflows/merge-claude-pr.yml`: duplicate-key YAML check PASS, `bash -n` PASS on
  both jobs' `run:` blocks, ASCII-only scan PASS.
- `tools/verify_hypothesis_ledger.py`: `PASS entries=47`, no drift.
- Full `pirate-force-server` suite: run this round as an unchanged-baseline sanity check
  (no `src/` diff this round) -- see the round-end letter for the pass count.
- `WIRED = 4/4` (unchanged this round; last re-verified by booting headless and grepping
  console output for lane_hooks emission in R244 -- `lane_a_choose_npc_scene14.py`,
  `lane_a_scene_census.py`, `lane_gm_chat_command.py`, `lane_gm_run_command.py`, all four
  `production_allowed` and firing on their call sites).

## Files touched

- `pf_bridge`: `.github/workflows/merge-claude-pr.yml` (1), `GAME_TEST_QUEUE.md` (1),
  `notes_to_chief/*.CONSUMED.txt` (8 new stubs) + matching `notes_to_chief/consumed/*` copies,
  `notes_to_chief/20260830_1804_CHIEF-REPLY-*.md` (1 new letter), `CHIEF_CONTINUATION.md`
  (round index line), this file
- `pirate-force-server`: no `src/` changes this round (round-claim commit only)

## Companion PRs

`pf_bridge#513` (draft claim, updated this round) / `pirate-force-server#322` (draft claim,
updated this round)
