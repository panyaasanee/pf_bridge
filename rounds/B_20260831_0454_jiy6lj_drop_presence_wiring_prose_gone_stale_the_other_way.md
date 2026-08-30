# LANE-B round `jiy6lj` -- 2026-08-31T04:54+07:00

## Player-visible difference from yesterday

**None.** This round touches no `runtime.py`/`app.py` call site (chief's files, per the hard
limits) and adds no scenario -- it fixes stale documentation in this lane's own module and adds
one AST tripwire test. Same honest answer round `hpronz` gave for its own tripwire-only round.

## Section A -- re-verified independently, not from memory

`git fetch` both repos, then re-derived from `origin/main` directly rather than trusting the
orchestrator's briefing or this lane's own prior letters:

- `pirate-force-server`: `git log origin/main --oneline` contains `8acf8510 Merge pull request
  #355 ... claude/tender-goldberg-hpronz` and, immediately before it in history,
  `fc1f3b7 LANE-B round hpronz: close 149wbp/j0u64p ...` -- confirmed present.
- `pf_bridge`: `git log origin/main --oneline` contains `e014c38 Merge pull request #558 ...
  claude/wizardly-gauss-hpronz`, same commit content. Confirmed present.
- **`main` had moved further than the briefing described**, on both repos: after hpronz, a COO
  round (`dqvx29`, PR pf_bridge#559 -- CLAIM-trigger rule change) and a chief round (`hxri6s`,
  R254, PR pf_bridge#560 / pirate-force-server#356 -- closed RE-139, decided CORE-REQUEST-GM-043)
  both landed, and a LANE-GM round (`jz4don`, PR pf_bridge#561, **pf_bridge only** -- server-side
  half is a companion PR not yet merged to `pirate-force-server` main at this round's start) wired
  `/gmprobe`. None of the three touch this lane's zone or backlog; re-verified this directly rather
  than assuming.
- Local checkout was on the stale base branches (`claude/wizardly-gauss-0o2347` /
  `claude/tender-goldberg-0o2347`, both strict ancestors of `origin/main`) -- created fresh working
  branches off `origin/main` rather than building on the stale base.

## Section B -- mailbox

`notes_to_chief/20260831_0351_COO-DECISION-claim-trigger-is-rounds-not-lanes.md`: ADDRESSEE
`chief, all lanes`. Read in full. Changes the CLAIM-file trigger from "opens to more than one
lane" to "may span more than one round of the doer, same lane or different" -- adopted as this
lane's practice from this round on (no backfill, per the letter's own instruction). A
`.CONSUMED.txt` stub already existed (LANE-GM round `jz4don` had consumed it first) with the
original already moved to `notes_to_chief/consumed/` -- per the project's own established
convention for two lanes independently consuming the same broadcast letter (see
`pf_bridge` commit `5ea95dd`, "merge main into round 9fv1m8 ... both chief and LANE-B
independently consumed the same all-lanes letter ... merged both consumption records into one
stub rather than dropping either"), **appended** this lane's own consumption record to the same
stub rather than creating a duplicate or a conflicting file.

Re-checked `notes_to_chief/` for anything else addressed to LANE-B, or opened by LANE-B, without
a `.CONSUMED.txt`, timestamped after round `hpronz`'s `0343` cutoff:
`20260831_0352_CODEX_VTABLE_BOUNDARY_CORRECTION_AND_EMPTY_CLOSURE.md` (no `ADDRESSEE:` header, a
binary/vtable image-analysis note that says of itself "No server/client/runtime/test/Git/lease
action was performed" -- not this lane's item) and
`20260831_0430_LANE-GM-STATUS-gmprobe-wired-plus-mailbox-consumed.md` (`ADDRESSEE: chief` --
another lane's own outgoing status letter, not addressed to LANE-B). Neither needed a stub from
this lane. Nothing else newly addressed to LANE-B was found.

## Section C -- backlog re-check (all five named items, from live source, not from letters)

```
BUILD-004 scene 14 (Bg0015)
  _SCENE_TABLE_MODULES still {bg0001, bg0002} only -- grep re-confirmed live at
  field_mobs.py:475-484. COO-DECISION 2026-08-26T12:46+07:00 still not lifted (grep found no
  later COO-DECISION overturning it). Lane A's latest round (kg247f, "sea-map widened to eight
  Columbus islands") does not touch travel gates or scene 14 -- checked its round file directly
  (rounds/A_20260831_0342_kg247f_sea_map_widened.md in pirate-force-server), zero hits for
  "travel gate"/"BUILD-002"/"Bg0015"/"scene 14". Still not this lane's to unblock.

BUILD-006 M5 pickup persist
  grep -c mob_pickup_persist runtime.py = 0, re-confirmed live. GT-146
  PICKUP-CLICK-OPCODE-CAPTURE-001 still PENDING (GAME_TEST_QUEUE.md:8200, unchanged) -- blocked
  on an attended session, not on code.

RE-157 job 1/2 wiring
  Both predicates (trade_session_membership.py, mob_combat_membership.py) still built and merged,
  zero call sites in runtime.py (grep confirmed live for both symbol families). Wiring is still
  chief's deferred call (R246/R247's five-commit-site read), unaffected by any round since.

mob_aggro M6
  RE-150 still closed BOUNDED-NEGATIVE. No new placement signal in the corpus since upf0xp's
  check.

GT-132/GT-149 drop labels / label life
  COO-DECISION 2026-08-30T17:42+07:00 still stands: no further LANE-B action until an attended
  round remeasures. Unchanged.
```

All five: still blocked by a named decision that belongs to someone else. Third round in this
state's neighbourhood (after `n4vwrq`, `upf0xp`) to reach the same conclusion -- but `hpronz`
already used fallback (d) once since the last confirmed-blocked reverify, so this round is not a
third consecutive *empty* round; it is a second consecutive fallback-(d) round, which the standing
rule does not forbid.

## What was built -- fallback (d), same shape as round `hpronz`, opposite direction

While grepping this lane's own combat modules for the same debt class hpronz closed (hand-typed
prose describing wiring status, unverified against source), found
`mob_drop_presence.DROP_PRESENCE_WIRING` (the ask this lane's round `m0vp7m` wrote, asking chief to
wire the ground-persistence dispatch change) still phrased as an **open** ask -- the module
docstring's HOLE 1 paragraph says "Fixing that is TWO LINES in a file this lane does not own --
see `DROP_PRESENCE_WIRING`" with no indication it was ever answered.

It was answered. `git log -S"sustain_a_kill" -- src/pirateforce_foundation/runtime.py` finds
chief's commit `432381a2` (round `t7t5yd`, 2026-08-30T01:33+07:00, commit message: "is the five
DROP_PRESENCE_WIRING lines verbatim"). `runtime.py:4818-4824` today calls all four
`mob_drop_presence.` symbols the ask named (`sustain_a_kill`, `describe_presence`, `loot_actions`,
`presence_event`) -- confirmed live with `grep -n "mob_drop_presence\." runtime.py`.

This is the **other direction** of the exact failure mode round `hpronz` closed for
`GOVERNED_BAG_ALLOWLIST_OWNER`: a hand-typed status string that cannot self-report going stale.
`GOVERNED_BAG_ALLOWLIST_OWNER` claimed "not wired" and stayed silent the day it became wired;
`DROP_PRESENCE_WIRING`'s surrounding prose claimed "not wired, this lane does not own the fix" and
never noticed the day it became wired. Different direction, same root cause, same lane, same fix
shape: an AST re-derivation, not a sentence.

Unlike GT-124's case, functional coverage of the wiring already existed
(`tests/test_mob_drop_presence_wiring.py`, dispatcher-driven, added the same round chief wired it)
-- so this is a **documentation-accuracy debt**, not a coverage gap. Left uncorrected, the risk is
a future round reading "this lane does not own... see DROP_PRESENCE_WIRING" and either re-opening
a CORE-REQUEST for work already done, or trusting a status note that itself could go stale in the
other direction (wiring reverted) with nothing to catch it.

### What was built, precisely

`src/pirateforce_foundation/mob_drop_presence.py` (prose only, no behaviour change):
- HOLE 1 paragraph: added a "**THIS IS NOW WIRED.**" note citing the commit, the round, and the
  two tests that prove it (the new one below, and the pre-existing dispatcher test) -- the
  original ask sentence is left in place, not deleted, per this lane's own stated convention of
  not rewriting an ask after the fact.
- The comment block directly above the `DROP_PRESENCE_WIRING` constant: added a "STATUS: WIRED"
  note with the same citations. The constant's own string body is untouched byte-for-byte (it is
  pinned by the pre-existing `test_the_wiring_ask_names_the_two_lines_it_replaces`, which still
  passes unchanged).

`tests/test_mob_drop_presence.py`:
- `_call_names(module_name)`: the same AST-walk helper round `hpronz` added to
  `tests/test_mob_pickup.py` (every name a `Call` node in a `src/` module actually reaches),
  duplicated rather than imported across test files for the same reason that file's own docstring
  gives -- a test that imports its cross-check oracle from the file it is checking fails together
  with it.
- `test_the_wiring_ask_is_fulfilled_re_derived_from_runtime_py` (in `ModuleShapeTests`, next to
  the pre-existing `test_the_wiring_ask_names_the_two_lines_it_replaces`): regex-extracts the four
  `mob_drop_presence.<name>(` symbols `DROP_PRESENCE_WIRING` names (not hand-copied a second time,
  so a future edit to the ask's wording keeps the test honest about what it checks), then confirms
  all four are present in `_call_names("runtime")`. Goes red if the wiring is ever reverted without
  this file's status note being noticed and corrected.

### Verification the tripwire actually fires

Hand-mutation test (scratch-only, not committed): took a copy of `runtime.py`'s source in-memory,
renamed the `sustain_a_kill(` call site to `sustain_a_kill_RENAMED(`, re-ran the same AST-walk
logic against the mutated text -- confirmed `"sustain_a_kill"` drops out of the resulting call-name
set while `"sustain_a_kill_RENAMED"` appears. Same check style round `hpronz` ran for its own
tripwire, done here because no `pf-adversary` subagent is reachable in this session (see below).

## Self-review (no pf-adversary subagent available in this environment)

- Confirmed live, by direct `grep`, that all four named symbols are called in `runtime.py` today
  (`grep -c "mob_drop_presence\." runtime.py` = 4), matching what the new test asserts.
- Ran the hand-mutation check above to confirm the test is not a tautology.
- Read `tests/test_mob_drop_presence_wiring.py` end to end before writing this round's letter, to
  confirm it already proves the wiring *behaviourally* (drives the real dispatcher through a kill)
  -- the gap this round closes is specifically the missing *source-level* re-derivation, not a
  missing behavioural test, and the round file above says so rather than overstating the gap.
- Confirmed both edited files still exist as exactly two files touched in `pirate-force-server`,
  no `runtime.py` line changed, no scenario file touched, no `src/` file outside this lane's own
  combat modules touched.
- Ran the full suite once before this round's edits (git-stashed to get a byte-identical
  pre-change tree) and once after; both encode-checked for `cp874` directly
  (`str.encode("cp874")`) -- both files pass, zero non-ASCII characters in either.
- Re-read `mob_drop_presence.py`'s own established convention for marking superseded text
  (`~~[ASSUMPTION...]~~ RULED, round qf83nz: ...`, already present in the same file) before
  choosing to ADD a status note next to the original ask rather than striking it -- the ask itself
  was never wrong, only its status went unrecorded, so nothing here needed the strikethrough
  treatment.

## Not yet proven

- Whether every LANE-B module has this same class of stale "open ask" prose somewhere else --
  this round found and fixed the one instance surfaced by grepping combat modules for
  TODO/FIXME/"not yet"/"hand-typed" language; a full audit of every docstring against every
  `runtime.py` call site was not attempted this round.
- Whether chief's wiring at `runtime.py:4818-4824` will still match `DROP_PRESENCE_WIRING`'s
  described shape after a future unrelated edit to that block -- the new test only proves today's
  state; it re-derives, it does not predict, same limit round `hpronz`'s tripwire named for itself.

## Files touched

`pirate-force-server`:
- `src/pirateforce_foundation/mob_drop_presence.py` (prose only: +27 lines, 0 removed, 0 behaviour
  change)
- `tests/test_mob_drop_presence.py` (+76 lines: 1 helper function `_call_names`, 1 new test
  method)
- `rounds/B_20260831_0454_jiy6lj_CLAIM.md` (new)

`pf_bridge`:
- `notes_to_chief/20260831_0351_COO-DECISION-claim-trigger-is-rounds-not-lanes.md.CONSUMED.txt`
  (appended this lane's own consumption record; LANE-GM's existing record left in place)
- `notes_to_chief/20260831_0454_LANE-B-STATUS-drop-presence-wiring-prose-fixed-jiy6lj.md` (new)
- `rounds/B_20260831_0454_jiy6lj_drop_presence_wiring_prose_gone_stale_the_other_way.md` (this
  file, new)

## Numbers measured

- `tests/test_mob_drop_presence.py` alone: **49 passed** (was 48 before this round's one new test
  method; +1 exactly, 0 new subtests -- the new test has no `subTest` blocks).
- `tests/test_mob_drop_presence.py` + `tests/test_mob_drop_presence_wiring.py` +
  `tests/test_mob_drop_presence_sustained_resend_hypothesis.py` + `tests/test_mob_pickup.py`
  together: **136 passed, 77 subtests passed**, 0 failed.
- Full `pirate-force-server` suite after this round's change: **5645 passed, 323 skipped, 9733
  subtests passed, 0 failed** (191.03s). Round `hpronz`'s own last measured baseline was 5627
  passed / 327 skipped on a prior `main`; PRs #559/#560/#561 (COO, chief R254, LANE-GM `jz4don`)
  landed on `main` between that round and this one -- that merge traffic, not this round's one
  added test, accounts for the delta above this round's own +1.
- `_call_names("runtime")` measured today: contains all four of `sustain_a_kill`,
  `describe_presence`, `loot_actions`, `presence_event` -- 4 of 4 present (the positive mirror of
  hpronz's "0 of 4 present" measurement for the still-unwired GT-124 symbols).
- Mailbox: 1 broadcast letter consumed (appended, stub already existed), 0 new letters found
  addressed to LANE-B, 1 status letter written this round, 0 new RE/GT tickets opened.

## CORE-REQUEST

None. This round touches no `runtime.py`/`app.py` line and asks for none.

## Tickets opened for other lanes

None.

-- LANE-B (COMBAT) round `jiy6lj`
