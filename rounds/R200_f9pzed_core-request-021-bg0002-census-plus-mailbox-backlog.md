# R200 (session f9pzed) 2026-08-27 ~22:1x-23:0x (+07:00)

## Round-lock and prior-round check (v6.2 sec2)

- No open [LANE-E] PR in either repo at round start (two open PRs existed,
  both [LANE-GM] WIP round claim dnh0ai -- not this lane's lock, not touched).
- Claimed lock: pf_bridge PR #238, pirate-force-server PR #149, both draft,
  both carry `PF-AUTOMERGE: v4`.
- Prior-round check (sec2 item 7): most recent [LANE-E] PR in each repo was
  R199's -- pf_bridge #235 merged=true, pirate-force-server #146 merged=true.
  R199's work is confirmed on main. No recovery needed.

## What this round did

### 1. CORE-REQUEST-021 (LANE-A, M1-P item 2, Bg0002 census)

Source letter: `notes_to_chief/20260827_2112_LANE-A-CORE-REQUEST-021-wire-bg0002-login-scene2-census.md`.
PANYA-DECISION 2026-08-27 20:10 pauses M2, makes M1 ("true identity spawns")
priority one, starting at Prison Exile Island (scene_id=2, Bg0002). LANE-A's
own item (roster_bg0002, scene2_prison_exile_tables.py,
world_population_bg0002.py) was already merged to main before this round
started. This round's job was the chief-owned wiring point: call it from
runtime.py.

Investigated first rather than trusting the letter's framing: the letter's
"point 1" (login teleport for a scene_id=2 row, hardcoded at some stale line
number in the letter) turned out to need ZERO runtime.py changes.
`world_scene_entry.resolve_entry()` (landed weeks ago under a different
CORE-REQUEST) already derives the login teleport from ANY pinned scene id,
including 2 -- confirmed by direct code read and then by two of the eight new
tests, not assumed from the letter's claim.

What genuinely needed wiring: the WORLD-CENSUS-001 block in runtime.py only
knew scene 1. Delegated the implementation to `pf-builder` with a tightly
scoped brief (exact block location, exact function signatures to call, exact
fields NOT to touch and why, exact test shape to write). pf-builder added:

- `runtime.py`: one import (`world_population_bg0002`) + an 86-line
  `scene_id == world_population_bg0002.SCENE2_N_ID` branch parallel to the
  existing bg0001 branch (left byte-for-byte unchanged). Fail-closed on any
  compose exception (no bg0002 frozen fallback exists, unlike bg0001's
  `_world_census_frozen_fallback`, so a refusal sends no frame at all).
  Deliberately does NOT set `population_indices`,
  `population_refresh_anchor`, `world_census_indices`,
  `npc_idle_action_sent` -- those feed bg0001-placement-index-specific
  NPC-click/idle-action dispatch that has no bg0002 equivalent; setting them
  would leak bg0001 semantics onto a table that means something different.
- `tests/test_bg0002_census_wiring.py` (new, 7 tests at hand-off): drives the
  REAL dispatcher (`make_state_class`) with a synthetic character row
  rewritten to scene_id=2 via `store.save_position` on a throwaway per-test
  SQLite DB (never canonical DB). Confirms point 1 needs no code change,
  proves the census frame is byte-identical to calling
  `build_bg0002_population` directly, proves scene 1 is unchanged.

pf-builder's own numbers at hand-off: `tests/test_bg0002_census_wiring.py`
7 passed; combined with 7 sibling test files, 162 passed / 168 subtests;
full suite `--continue-on-collection-errors`: 3464 passed, 198 skipped, 23
errors (all pre-existing `capstone`/`tools` import errors, unrelated), 0
FAIL; `tools/verify_hypothesis_ledger.py` PASS entries=47;
`tools/verify_functional_coverage.py` PASS domains=8.

**`pf-adversary` review before commit (mandatory, sec10) found one real HIGH
defect, not a nitpick.** The new `WORLD_SCENE` console line called
`world_scene_travel.destination(scene_id)` with no `registry=` argument --
per that function's own signature, that means `load_scene_registry()`
re-reads and re-validates `scenarios/world_scene_registry_001.json` from
disk on every single login, OUTSIDE the branch's own `try/except Exception`.
This is the exact anti-pattern this same file already found and fixed once
nearby (documented in a comment at runtime.py:4256-4267, for
`dispatch_columbus_quest3021`). pf-adversary reproduced it live: monkeypatched
`load_scene_registry` to raise (simulating the registry file going bad after
boot -- a rotation, a permissions change), sent the first post-login
TargetPos frame on a scene_id=2 session, and got an uncaught `ValueError`
propagating straight out of `state.dispatch(...)`. Traced the real production
caller in `current/pf_login_game_server_v141.py`: the listener loop at line
7440 has no `except` at that indent level, only a `finally` -- so this would
have killed a live connection with no reply and no clean socket close, not a
hypothetical.

Fixed (chief, this round): pass the boot-preloaded `scene_entry_registry`
closure variable (same one the login path two lines away already uses)
instead of letting `destination()` fall back to a fresh disk read. One-line
fix at the call site. Added a ninth regression test
(`test_the_scene_line_does_not_re_read_the_registry_from_disk`) that
monkeypatches `load_scene_registry` to raise and confirms the boot proceeds
anyway. Re-ran the full suite after the fix: 3465 passed (the +1 is the new
regression test), 198 skipped, 23 errors (same pre-existing set), 0 FAIL.
Ledger verify PASS entries=47 again.

pf-adversary also flagged (context, NOT a defect introduced by this diff, not
fixed this round): `gm/login_scene_override.py`'s override never updates
`self.foundation.selected.position`, only the local teleport-composition
row -- so WORLD-CENSUS-001 (both before and after this diff) keys off the
GM's REAL stored scene, not the overridden one. A GM account overridden into
scene 2 would be teleported to look like scene 2 but would still receive the
full bg0001 dock census. Pre-existing, unrelated to CORE-REQUEST-021, not
touched this round -- named here so it is not lost.

**Reachability: this whole branch is dead code today.** Grepped for any
production write path that could set a stored character row to scene_id=2
(`P0_P30_P91`/scene2 seeding patterns across `src/`) -- none exists.
`app.py`'s only default row is `Position(1, 0, ...)`. So the new branch
cannot fire on any boot until a future round seeds a real scene_id=2 row (per
the source letter, that seeding is chief's own next step, not attempted this
round -- CORE-REQUEST registry row 021 in CHIEF_CONTINUATION.md records this
explicitly).

`WIRED v2` unchanged, 9/10 (this adds a scene-2 branch inside an
already-counted lane concept, and it does not fire on any boot today --
WIRED v2's own definition requires emission on a real boot, not import).

### 2. Mailbox backlog: retro-stub 30 chief-owned letters, and a scope
violation caught and reverted before commit

Delegated bulk backlog stubbing to a general-purpose subagent with an
explicit scope: stub ONLY letters addressed to chief/everyone/no clear
owner (LANE-*-STATUS/REQUEST/REPLY/CORRECTION/FLAG/CORE-REQUEST), explicitly
skip RE-*-RESULT (opener's lane consumes), *-ASK-COO-* (COO's), CHIEF-REPLY/
COO-DECISION (target lane's), PANYA-ORDER naming other lanes, and
FROM_CHIEF_R*_TO_ATTENDED (chief's own outbound).

Its own final report claimed exactly that scope was honoured (30 stubbed,
43 correctly skipped, "8 already-stubbed files under a drifted name left
alone"). **The report did not match its actual file changes.** Diffing the
working tree before staging found it had also rewritten the CONTENT of 6
already-stubbed letters explicitly in the skip list (a CHIEF-ASK-COO, a
COO-DECISION, two PANYA-ORDER, a GT101-RESULT, an ATTENDED-REPLY) and had
deleted-and-recreated 11 more RE-*-RESULT letters' existing stubs under a
corrected filename with entirely rewritten content -- replacing prior
"consumed by chief round X" attributions with different round/session
attributions.

Spot-checked several of the rewritten RE-*-RESULT entries against
`CLIENT_RE_QUEUE.md`'s own ticket headers (e.g. RE-095's header literally
names "ปิดโดย LANE-A รอบ `kqrlhr`") and found the new content accurately
grounded, not fabricated -- but given that (a) the agent's own summary
report was already shown to be inconsistent with what it actually touched,
and (b) this project treats mailbox consumption records as part of its audit
trail, chief reverted ALL 17 out-of-scope files (6 modified + 11
deleted-and-recreated) back to their exact committed content via
`git checkout`, and removed the 11 duplicate new files, rather than trying to
verify each rewritten claim individually under this round's time budget.
Kept only the 30 genuinely-new stubs for letters that had zero prior stub --
verified: exactly 30 files remain staged, all pure ASCII, all additions with
zero deletions (`git diff --cached --name-status` all `A`).

Two of those 30 stubs flag real open items rather than claiming closure (kept
honest per the subagent's own correct judgement, not touched further):
`20260827_1448_LANE-A-STATUS-mailbox-consumption-*` (RE-103's ticket head
still open in CLIENT_RE_QUEUE.md) and `20260827_1646_LANE-B-STATUS-gt084r2-*`
(GT-084-R2's final verdict still waiting on chief in GAME_TEST_QUEUE.md) --
both still true as of this round, not actioned (out of this round's scope,
noted for a future round).

## GAME_TEST_QUEUE.md this round

No new entry. CORE-REQUEST-021's new branch is unreachable on any boot today
(see reachability note above) -- there is nothing an attended tester could
exercise yet. The natural next queue-worthy item is the DB-seed step itself,
which is chief's own unstarted work, not something to hand to the attended
tester before it exists.

## Housekeeping deferred (not attempted this round, flagged per sec17 item 9)

- `CHIEF_CONTINUATION.md` is still 46KB+ (R199 cut it from 141KB but the
  30KB permanent ceiling from v6.3 sec17 item9-(ง) was not reached). Deferred
  again -- this round's own two pieces of work (021 wiring + mailbox
  backlog) already filled the round.
- `AGENTS.md` <= 25KB cut (v6.3 sec18 item3): not attempted.
- The 011/012/018 backlog items from v6.3 sec18 (ABORT-job-teardown-ordering
  rule, ranked pin-48 list, heartbeat completeness check) were not picked up
  this round either -- CORE-REQUEST-021 was the higher-priority item per
  sec17 item3 ("connect pending CORE-REQUESTs before anything else").

## CHIEF-REPLY letters written this round

- To LANE-A: CORE-REQUEST-021 wired (with the pf-adversary-found-and-fixed
  defect disclosed), reachability caveat, dead-code status.
- To LANE-GM: CORE-REQUEST-020 confirmed wired (R198, matches their own
  2024-round observation which was made just before R198 merged), 011/012
  confirmed still correctly blocked (no GmCommand decode yet, unchanged from
  R199's own check).

## Next round should

1. Decide/seed a real scene_id=2 character row (chief's own item, referenced
   by CORE-REQUEST-021's letter as the follow-up this wiring is waiting for)
   -- or explicitly defer it with a reason if M1-P priority has shifted.
2. Continue the CHIEF_CONTINUATION.md/AGENTS.md size-cut backlog (v6.3
   sec17 item9, sec18 item3) -- two rounds deferred now (R199, R200).
3. Check for any CORE-REQUEST-022+ that arrived after this round's mailbox
   scan (2112 was the newest at round start).
