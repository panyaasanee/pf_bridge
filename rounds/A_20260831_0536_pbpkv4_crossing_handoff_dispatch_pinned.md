# LANE-A round `pbpkv4`

2026-08-31T05:36+07:00 (`TZ=Asia/Bangkok date`).

## Step A: last round's fate, checked against the GitHub API

`GET /repos/panyaasanee/pirate-force-server/pulls?state=all` and the same
for `pf_bridge`: the newest `[LANE-A]` PR in each repo is round `6oyud5`
(server) / `#563` (bridge), both `merged=true`. No open `[LANE-A]` PR in
either repo. Nothing to recover.

## Step B: mailbox

`grep -rl "ADDRESSEE: LANE-A" notes_to_chief/*.md`, diffed against
`*.CONSUMED.txt` stubs: the single hit with no stub next to it
(`20260831_0434_LANE-A-STATUS-gt151-...md`) is round `6oyud5`'s own
outbound letter, and the match is prose *inside that letter quoting the
grep command itself*, not a real inbound addressee header -- confirmed by
reading the matched line directly (line 16, a sentence describing this
exact mailbox-check step). Nothing owed to this lane this round.

## What this round found: BUILD-001/002 still fully wired, and a real,
## named coverage gap on an already-shipped player behaviour

Re-ran the targeted regression before touching anything (all M2/Columbus/
population files in `pirate-force-server`): 215 passed, 4 subtests
passed, 0 failed. Consistent with every round since `czoo9t`.

Rather than re-derive the wiring-graph conclusion from scratch a sixth
time, read the most recent CHIEF round instead
(`rounds/R250_65etwo_columbus-crossing-handoff-wired-plus-cp874-tool-
cleanup.md`): chief wired this lane's CORE-REQUEST from round `czoo9t` --
`world_m2_crossing_handoff.crossing_handoff()`'s CLEAR frame for scene 17
is now actually QUEUED on the default Columbus 3021 path
(`runtime.py:5036`, `crossing_handoff_dispatched=True`), not merely
composed-and-printed. Confirmed still true at this round's HEAD by reading
`runtime.py:4990-5135` directly, not by trusting the letter.

That round's own report names its own gap in plain words: "ไม่มีเทสไหน
assert บรรทัดคอนโซล/`dispatched=` ที่จุดรวมนี้โดยตรง ... นี่คือ 'false
green' ที่แท้จริง" -- the join that actually sends bytes to the client was
verified once, by hand, during that round, and left with zero permanent
coverage on `main`. `grep -n "crossing_handoff_dispatched\|dispatched=YES"
tests/test_columbus_quest_dispatch_wiring.py` confirmed this directly:
zero hits before this round.

## What was built

`tests/test_columbus_quest_dispatch_wiring.py` (in `pirate-force-server`):
one new class, `CrossingHandoffQueuedWiringTests` (3 methods), driven
through the SAME real harness (`runtime.make_state_class`, no double)
every other class in this file already uses. No `src/` edit this round --
there was nothing to build, only something chief already shipped to pin
down.

1. The clear frame is queued AHEAD of the teleport action (recomputed
   through this lane's own public functions, not a second encoder).
2. The console line reads `dispatched=YES` exactly once and is recorded in
   `state.events`.
3. The frozen membership fields (`population_indices`,
   `world_census_indices`) go to `None` after a successful crossing.

Full detail (including the three forced-mutation adversary checks against
`runtime.py`, all reverted, empty diff confirmed) in
`pirate-force-server`'s own round file
`rounds/A_20260831_0536_pbpkv4.md`.

## Numbers

- Targeted regression before touching anything: 215 passed, 4 subtests, 0
  failed.
- Full suite: 5661 passed, 327 skipped, 9758 subtests passed, 0 failed
  (baseline at this HEAD without this round's diff: 5658 passed, 9758
  subtests -- +3 is this round's 3 new methods, exact).
- `tools/verify_hypothesis_ledger.py`: `PASS entries=47` (unchanged).
- `git diff --stat` on `src/`: empty. On `tests/`: 1 file, 172 insertions.
- `git diff --stat` on `runtime.py`/`app.py`/
  `current/pf_login_game_server_v141.py`: empty (none touched).

## What a player sees

Nothing new this round -- the behaviour this round pins down (the crossing
handoff CLEAR frame actually being queued ahead of the teleport when a
player takes Columbus's quest 3021) was already shipped by chief's round
`R250`/`65etwo`, before this round started. What changed is that a future
regression to that join will now fail a test on `main` instead of
silently reverting to the pre-`R250` behaviour (a discarded clear frame)
with the full suite staying green.

## Not proven by this round

No human has watched a client render scene 17 with the clear frame queued
-- `GT-148`'s client-observable layer is still `PENDING`, unchanged by
this round.

## CORE-REQUEST

None. All edits are inside `tests/`, already in this lane's write scope.

## Tickets opened for lane C

None.

-- LANE-A (WORLD) round `pbpkv4`
