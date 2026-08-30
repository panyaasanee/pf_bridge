# LANE-B round (scheduled, no live viewer) -- 2026-08-30T17:4x+07:00

## Player-visible difference from yesterday

**None.** No `runtime.py` call site was added this round (that file is chief's, per the hard limits), so
nothing built here can change what a player sees on its own. The one thing this round confirms is what
does NOT explain the missing loot labels: it is not the position of `loot_actions()` in `runtime.py`'s
action list -- that position was already the earliest one `CORE-REQUEST-007`'s own invariant allows.

## What this round consumed and decided

Read `notes_to_chief/20260830_1704_CHIEF-REPLY-force-pos-unlock-blast-radius-plus-loot-reorder-conflict-both-not-done.md`
(chief's answer to LANE-B round `qb1ytr`'s CORE-REQUEST asking to reorder `mob_drop_presence.loot_actions()`
ahead of the `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE(_DYING)` frames). Chief found the reorder conflicts with
`CORE-REQUEST-007`'s own standing comment ("AFTER the whole death schedule ... never between the dying and
dead frames") and asked COO/LANE-B to rule on whether that invariant should be relaxed.

**Decision (this lane's own, not COO's -- letter tagged `[สมมติของสาย B - รอ COO ยืนยัน]`):** do NOT relax
the invariant. Re-reading `runtime.py:4600-4824` directly (not the prior round's letter) found something
neither the original CORE-REQUEST nor chief's reply said plainly: **the reorder is not merely risky, it is
already impossible without breaking the invariant.** The 97-actor, ~17,910-byte census recompose is not a
separate queued wire action sitting between `MOB_DEATH_DEAD` and the loot frames -- it IS the frame content
of `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` themselves (`dying_frame`/`dead_frame` come straight from
`recompose_dying.frame`/`recompose_dead.frame`). And `actions.extend(mob_drop_presence.loot_actions(step))`
(`runtime.py:4821`) already sits immediately after `actions.append(("MOB_DEATH_DEAD", ...))` (`:4751-4754`)
with nothing in between except pure computation (`roll_drops`/`loot_a_kill`, which appends nothing to the
list). So loot is already queued at the earliest position the invariant permits today. There is nowhere
left to move it to that would both reduce `late_ms` and respect "never between dying and dead" -- moving it
earlier means moving it before `DYING`, which the invariant forbids just as directly.

**Consequence:** withdrew the reorder CORE-REQUEST outright (not "wait for COO" -- the code itself answers
the question). Wrote
`notes_to_chief/20260830_1743_LANE-B-DECISION-invariant-stands-membership-guard-built-instead.md`
recording this, consumed the CHIEF-REPLY letter (`.CONSUMED.txt` stub + copy to `notes_to_chief/consumed/`).

`label_life` itself remains a measured client fact
(`src/pirateforce_foundation/mob_drop_presence.py:166-167`, GT-045-derived), not a server-side lever --
confirmed again this round, nothing new to try there without touching `runtime.py` or the standing
`DROP_REFRESH_MS` production ban (COO-DECISION 2026-08-26T07:45), neither of which this lane will do on its
own authority. Left as a known NO-RESULT, same as round `qb1ytr` chose.

## RE-163 opened

If queue position doesn't explain `late_ms` (351-949ms measured `20260830_1554`), something else does:
either the real cost of serializing/writing two ~17,910-byte frames before the loot frame gets its turn, or
`runtime.py`'s own scheduler/`delay`-field semantics (the fourth tuple element: `0.0` for `MOB_DEATH_DYING`
and loot, `hold_ms/1000.0` for `MOB_DEATH_DEAD`) -- this lane does not know the scheduler internals well
enough to answer either question itself, so it does not guess. Opened
`CLIENT_RE_QUEUE.md` -> `RE-163 MOB-LOOT-DROP-LATE-MS-SOURCE-001` (static-on-bridge, no game boot, no new
capture -- reads the existing `capture_pexile_20260830_151429` console log) asking RE to identify the
scheduler mechanism and whether it explains the measured lateness, with an explicit bounded-negative exit
("outside runtime.py's own actions list, e.g. network/OS buffering") if it doesn't.

Numbering: `RE-162` is reserved by name/content in `notes_to_chief/20260830_1655_PANYA-ORDER-open-RE-162-*`
(in-session scene change) but not yet written into `CLIENT_RE_QUEUE.md` at the time this ticket opened --
skipped to `163` per the file's own collision rule (whoever writes later shifts their own number) rather
than racing that reservation. Verified via the file's own mandated search command before writing.

Annotated `GAME_TEST_QUEUE.md`'s `GT-146` P0 gate note (the section that already told the next attended
round the label_life wall blocks every boot) with the withdrawal, so nobody waits on the reorder path that
no longer exists.

## RE-157 job 2 -- built the predicate nobody had built yet

While re-reading `runtime.py` for the item above, confirmed
`notes_to_chief/20260830_1111_RE-157-RESULT-*.md` (Job 2, the mob-combat announced-actor guard) still had
no source built (its own nonclaim 3 says explicitly: "this lane's to build in `src/`, not this ticket's").
RE-157 named a real gap: `_dispatch_mob_combat`'s `target_is_field_mob` check (`runtime.py:4194-4196`)
validates a target against the STATIC scene roster only, never against what was actually announced to this
session's own client through a committed census -- so a forged/desynced `ActionVital` could spend
cadence/ledger mutation against a field mob that exists in the roster but was never shipped to this
session. RE-157 itself is explicit this is a forged/desync risk, not proven reachable by a normal client.

Built `src/pirateforce_foundation/mob_combat_membership.py`: `AnnouncedActorMembership` (scene_id, a frozen
actor-identity set, an opaque comparable generation token) and `admits()`, a fail-closed predicate (`False`
on a missing record, a scene mismatch, a generation mismatch, or an actor never in the announced set --
never an exception). No `runtime.py` call site -- that's chief's to wire, per the hard limits -- so this
module changes nothing live by itself; the module's own docstring carries the one-block CORE-REQUEST
(exact insertion point, current line numbers) for when a `runtime.py` round has time for it.

`tests/test_mob_combat_membership.py`: 9 tests, all offline/pure (no socket, no client, no `legacy_bridge`
load), covering the missing-record refusal, the one admitting shape, independent refusal on each of the
three fields, that a mutable source iterable cannot mutate a built record after the fact, duplicate-identity
collapse, and that "generation" only promises `==` (not `int`), matching RE-157's own note that the two
named commit points (home census vs. lane census) are different mechanisms.

Adding the new module tripped three pre-existing guard tests (by design -- they exist to catch exactly
this): `test_field_mobs.py`'s importer-set pin (my docstring's prose mentioned the literal string
`field_mobs`), `test_npc_interaction_wire.py`'s quest/shop/trade word sweep (my docstring quoted RE-157's
own filename, which contains the word "trade"), and `test_mob_stat_fabrication_guard.py`'s
`LANE_B_MODULES` tuple (a new `mob_*` file must be listed or the fabrication sweep silently skips it).
Reworded the docstring to avoid the two literal-string trips and added `mob_combat_membership.py` to
`LANE_B_MODULES` with the same per-module comment convention every other entry already carries. Full suite
re-run after the fix: **5514 passed, 327 skipped, 9554 subtests passed, 0 failed** (up from the prior
round's own last-known-green baseline plus this round's 9 new tests and the 3 that needed the guard-table
update).

## Not yet proven

- Whether the actual cause of `late_ms` (frame-write cost or scheduler semantics) is what `RE-163` will
  answer -- not measured this round, that ticket exists precisely because this lane could not answer it
  from `src/` alone.
- Whether `mob_combat_membership.admits()`'s contract (scene + exact actor identity + generation token) is
  the shape `runtime.py`'s actual census-commit state can supply without further design work -- RE-157
  named two commit points (`:7759-7799`, `:7548-7610`) with the same general shape but did not fully spell
  out how a single per-session record should track "the current generation" across both; flagged in the
  module's own CORE-REQUEST as chief's call, not guessed at here.
- Everything about `label_life`/`REEMISSION_REDRAWS_THE_LABEL` remains exactly where round `qb1ytr` left
  it -- unmeasured, and unmeasurable headless.

## Files touched

`pirate-force-server`:
- `src/pirateforce_foundation/mob_combat_membership.py` (new, 1 file)
- `tests/test_mob_combat_membership.py` (new, 1 file, 9 tests)
- `tests/test_mob_stat_fabrication_guard.py` (1 file, added `mob_combat_membership.py` to `LANE_B_MODULES`)

`pf_bridge`:
- `notes_to_chief/20260830_1743_LANE-B-DECISION-invariant-stands-membership-guard-built-instead.md`
  (new)
- `notes_to_chief/20260830_1704_CHIEF-REPLY-force-pos-loot-reorder-both-not-done.CONSUMED.txt`
  (new)
- `notes_to_chief/consumed/20260830_1704_CHIEF-REPLY-force-pos-unlock-blast-radius-plus-loot-reorder-conflict-both-not-done.md`
  (new, copy of original)
- `CLIENT_RE_QUEUE.md` (new ticket `RE-163 MOB-LOOT-DROP-LATE-MS-SOURCE-001`)
- `GAME_TEST_QUEUE.md` (`GT-146` P0 gate note: reorder-withdrawn annotation)
- `rounds/B_20260830_1743_membership_guard_built_reorder_withdrawn_re163_opened.md` (this file)

## Filename-cap note (post-adversary fixup)

pf-adversary caught this round's mailbox filenames over the 100-char cap (AGENTS.md:142) on first
commit: the `.CONSUMED.txt` stub for `20260830_1704_CHIEF-REPLY-force-pos-unlock-blast-radius-plus-loot-
reorder-conflict-both-not-done.md` came out at 113 chars full-name form and 110 chars extension-stripped
form -- the original source name (100 chars, already at the cap) leaves no form under the cap, a gap
`notes_to_chief/README.md`'s existing near-cap guidance does not cover (it assumes the source name is a
few characters under 100, not already at it). Same problem hit this lane's own new `LANE-B-DECISION`
letter at 102 chars. Renamed both to shorter, still-unambiguous names (`git mv`, not a delete):
`20260830_1704_CHIEF-REPLY-force-pos-loot-reorder-both-not-done.CONSUMED.txt` (75 chars) and
`20260830_1743_LANE-B-DECISION-invariant-stands-membership-guard-built-instead.md` (80 chars). Updated
every cross-reference to the old names (`CLIENT_RE_QUEUE.md`, this file, the stub's own body text). The
original 1704 letter itself is untouched -- only the derived stub and this lane's own new letter were
renamed. Recording this here per the README's own instruction not to silently pick a form without a note.

## Numbers measured

- `mob_combat_membership.py`: 2 public functions (`build_membership`, `admits`), 1 `NamedTuple`, 9 tests,
  9/9 passed.
- Full `pirate-force-server` suite after the change: 5514 passed, 327 skipped, 9554 subtests passed, 0
  failed.
- Mailbox: 1 letter consumed (`20260830_1704_CHIEF-REPLY-*`), 1 decision letter written, 1 new RE ticket
  opened (`RE-163`).

## CORE-REQUEST

See `src/pirateforce_foundation/mob_combat_membership.py`'s own module docstring for the full block:
`runtime.py`'s `_dispatch_mob_combat`, after `target_is_field_mob = any(...)` (currently line 4194-4196)
and before the `if target_is_field_mob:` cadence branch (currently line 4197), call
`mob_combat_membership.admits(...)` and refuse (`return []`, log
`mob_combat_target_not_announced_no_reply`) on `False`. This lane does not know which existing `runtime.py`
attribute (if any) already holds "the session's current census generation counter" -- that is chief's call,
not guessed at here.

## Tickets opened for other lanes

`RE-163` (`CLIENT_RE_QUEUE.md`, addressed to RE) -- static-on-bridge, find the real source of the measured
`MOB_LOOT_DROP` `late_ms` now that queue position is ruled out.
