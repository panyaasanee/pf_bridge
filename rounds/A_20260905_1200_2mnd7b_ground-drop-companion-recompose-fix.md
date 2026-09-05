# LANE-A round `2mnd7b` -- ground-drop companion frame for mid-combat recompose

start 2026-09-05T12:00+07:00 · this file written 2026-09-05T12:5x+07:00

## What NOW.md item moved this round · what did not

`COO-DECISION 20260905_1152` gave LANE-A the in-memory per-scene world registry and named two
pieces: (1) fix `MOB_COMBAT_BAR_CENSUS_RECOMPOSE` so it does not wipe another monster's ground
drops (PR due 12:21, falls due 13:51), and (2)/(3) the fuller per-scene registry API + NPC/object
coordinate accessor (PR due 13:51, falls due 15:21).

**Item (1): DONE, shipped this round** -- `pirate-force-server#818`, open, non-draft, marked.
**Item (2)/(3): NOT done this round** -- ran out of round budget after item (1)'s two required
`pf-adversary` passes plus the full-suite gate. Carried to the next LANE-A round as the first
item picked up (below). NOW.md's `13:51`/falls-due-`15:21` line for item (2)/(3) is not met by
this round; flagging that honestly rather than claiming partial credit.

Also this round: closed three RE ticket headers per item 4 of the same COO decision (RE-227,
RE-234) and the RE-138 client-observable caveat via `GT-250`'s NEGATIVE result (see below) --
`RE-248` was NOT touched: its own header names LANE-DB as owner/consumer, not LANE-A, and it
already carries a `.CONSUMED.txt` stub, so closing its header belongs to LANE-DB or to chief's
15:00 safety net, not to this lane.

## Item (1) -- the fix

R316/GT-242 (`notes_to_chief/20260905_1102_KA1A-R316-RESULTS-...md` finding "ค"): killing
monster A drops items (visible), then hitting a *different* monster B fires
`MOB_COMBAT_BAR_CENSUS_RECOMPOSE`, which carries no ground-drop information, so the client wipes
monster A's items off screen. PANYA-DECISION 1057 item 2 forbids exactly this shape (one action's
frame deleting world state that action never touched).

New function `mob_scene_recompose.ground_companion_actions(cell, legacy)` reuses the already
client-proven (`GT-242`) `mob_drop_presence.sustain_a_kill` rather than a new encoder. Does not
touch `recompose_frames`/`_compose`/`SceneRecompose` -- byte-pinned scene 1/scene 2 census tests
are untouched and green. `runtime.py` wiring (one line, inside `if recompose_record.composed:`)
is a CORE-REQUEST for chief, written out verbatim in `mob_scene_recompose.GROUND_COMPANION_WIRING`
and in the PR body -- nothing reaches production until that lands.

Delegated the implementation to the `pf-builder` subagent (full context: the COO letter, the R316
evidence, file-scope limits, house rules) since the actual work is a careful, deeply-invariant
edit inside a LANE-B-titled 1700-line module (`mob_scene_recompose.py`) -- this is a sanctioned
cross-lane edit per COO's own letter, same pattern this file already carries from earlier rounds
(`ACKNOWLEDGED_WITHOUT_COMPOSER` entries added by LANE-A rounds inside a LANE-B-titled file).

## pf-adversary (2 of 2 used this round)

Pass 1: **NOT APPROVED**, 2 confirmed defects:
- D1 (High): a literal Thai character copied verbatim from the R316 letter into a source comment
  broke `tests/test_mob_stat_fabrication_guard.py`'s ASCII-only sweep of `mob_*.py` files --
  measured full-suite failure (1 failed / 10743 passed / 418 skipped).
- D2 (Medium): the `GROUND_COMPANION_WIRING` CORE-REQUEST text made a false claim about
  `runtime.py`'s control flow -- the anchor line it named is a sibling statement after the whole
  if/else (runs on every arm, including the no-anchor fallback which "runs in ordinary play, not
  merely in theory" per the file's own comment), not nested inside the guard as claimed.

Both fixed (ASCII transliteration; `GROUND_COMPANION_WIRING` rewritten and re-anchored on
`recompose_record.composed`, with the actual `runtime.py` indentation independently re-verified
rather than trusted from prose).

Pass 2 (fix review): **PASS** -- independently re-derived `runtime.py`'s real indentation again
(did not trust the corrected prose either), confirmed the new anchor point correctly excludes
both the no-anchor fallback and the degraded one-entry-frame arm, confirmed `runtime.py` is still
byte-identical to `main` (no wiring performed), confirmed no other file in the tree repeats the
old false claim, full suite re-run clean.

## Evidence (final commit `4fe73bd` on `claude/charming-mendel-2mnd7b`)

- Targeted, throughout: `test_mob_scene_recompose.py` + new `test_mob_scene_recompose_ground_companion.py`
  (11 tests) + `test_mob_drop_presence*.py` + `test_mob_stat_fabrication_guard.py` -- all green
  at every checkpoint.
- **Full suite ran 3 times this round** (house rule requires an explanation whenever it runs more
  than once): pf-adversary ran it twice as part of its own two independent passes (not this
  round-holder's required run); this round's own one required full-suite gate ran once, as the
  actually-last step, on the tree merged with fresh `origin/main` (8 unrelated commits from other
  lanes, no conflicts): **10850 passed, 327 skipped, 20170 subtests passed, 0 failed** (420.82s).
- Stash-proof (pf-builder's own check, reproduced by pf-adversary independently): removing
  `ground_companion_actions` fails exactly the 7 tests that claim it as their subject, no others.

## TWO_SESSIONS_SAME_SCENE

Not applicable to this PR's own change: `ground_companion_actions` re-announces the scene's
*existing* live ground-drop ledger (`mob_ground_persistence`/`persistence_ground_drops`, already
world-scoped per `COO-DECISION 20260905_1152`, not session-scoped) -- it neither reads nor writes
anything about which session is present, so two sessions in the same scene see the identical
companion frame the first would. The bigger registry-API question (item (2)/(3), not done this
round) is where this answer will actually get exercised end to end.

## RE ticket closures (item 4 of `1152`)

- `RE-227` CAPTAIN-REPORT-ON-ISLAND-CONTACT-001: closed DONE/BOUNDED. Layer (1) STATIC stands
  and shipped to production (`#753`/`#760`/`#797`/`#810`, `RE-256`). Layer (2)'s original
  criterion (tie to wire via `TriggerVital`/id 153-154) is superseded, not satisfied on its own
  terms: `RE-234` (below) proved that hypothesis false and reconfirmed AddSurveyData as the real
  mechanism. Closed `covered by RE-234`, not force-fit to the stale bar.
- `RE-234` CLIENT-RESPONSE-PATH-FOR-TRIGGERVITAL-1FB2-ISLAND-001: closed DONE/MIXED PASS +
  BOUNDED-NEGATIVE from its own already-arrived result letter (`notes_to_chief/20260904_1953_...md`,
  never consumed until this round -- copied to `consumed/`, stub placed). TriggerVital response
  handler is a 5-byte no-op; AddSurveyData is the only proven window-opening route; id-only
  island classification is BOUNDED-NEGATIVE (unsafe to trust `M2_OBSERVED_ISLAND_TRIGGER_IDS` as
  island evidence without narrower scene/context scoping -- noted as backlog, no BUILD_IMPACT
  forced this round, log-only code).
- `RE-138`'s flagged-open client-observable gap: closed citing `GT-250` (R317, NEGATIVE -- the
  27-Aug name-label-vanish symptom did not reproduce on the current build after walking well out
  of sight and back).

## QUEUE_TRIAGE

Not this lane's queue to triage (chief owns `GAME_TEST_QUEUE.md`/`CLIENT_RE_QUEUE.md` triage
per `COO-DECISION 20260904_2159`) -- noting only the three closures above, which are this lane's
own tickets per their own headers.

## Backlog carried to next round (in order)

1. **Item (2)/(3) of `COO-DECISION 20260905_1152`**: the per-scene world registry API itself
   (ground drops + age, monster HP/death/respawn status, last-known monster position, with a
   write API for LANE-B) and the NPC/object-by-u16-id coordinate accessor UI's GO! CORE-REQUEST
   (`1151`) needs. Falls due 15:21 -- already past its 13:51 target when this round closes; will
   be the first thing picked up next round, not a fresh claim decision.
2. The GT ticket text for item (1)'s fix (drafted in `pirate-force-server#818`'s own body,
   ready to paste) still needs a number from chief.
3. R317 §4's Columbus-portrait-lingers finding (`GT-252`) needs a joint LANE-A/LANE-UI decision
   on which reply shape closes it -- not started this round, does not block anything.
4. `lane_hooks/lane_a_island_trigger_log.py`'s `M2_OBSERVED_ISLAND_TRIGGER_IDS` should be
   narrowed with scene/contact context before anyone treats an id-2/3 sighting as island
   evidence (from `RE-234`'s BOUNDED-NEGATIVE finding above) -- log-only, not blocking, no
   BUILD_IMPACT forced.

## Round-lock bookkeeping

Start-of-round check (both repos, both open-PR list and prior-round merge status): no live
`[LANE-A]` PR open in either repo; this lane's immediately prior closed rounds
(`pirate-force-server#810`/`#805`, `pf_bridge#1296`) all show `merged=true` -- prior round's work
is genuinely on `main`, nothing to recover.

Claim: `pf_bridge#1308` (opened 12:00, no marker until this file lands). Server PR:
`pirate-force-server#818` (opened as draft per the frame-touching rule since it adds a frame the
client receives, un-drafted + marked after `pf-adversary` pass 2 cleared it). Claim PR gets its
marker in the same push as this file, per the lock rule.

## Push state

Both repos pushed. `pirate-force-server#818`: **open, not draft, marked, mergeable_state has been
"unstable"** at last check (GitHub's own status, not yet re-verified against a fresh gate run on
this exact final commit -- not waiting on it to close this round, per the house rule that a round
hands off to the reaper/gate rather than babysitting it). `pf_bridge#1308`: about to get its
marker in this same push -- released after this file lands, not before.

## งานสำรอง (ทำเมื่องานหลักติด)

1. Start item (2)/(3) above (the per-scene registry API) -- `src/pirateforce_foundation/world_scene_registry.py`
   (new module) -- pass: a write API LANE-B's combat-state rounds can call without waiting on a
   second LANE-A round, tested against real scene-2 fixtures.
2. `RE-234`'s BOUNDED-NEGATIVE backlog item -- narrow `lane_hooks/lane_a_island_trigger_log.py`'s
   `M2_OBSERVED_ISLAND_TRIGGER_IDS` with scene/contact context -- pass: a mutation making the
   classifier accept a non-island id-3 sighting (ordinary sailing, per `GT-228`) turns red.
3. R317 §4 Columbus-portrait joint decision with LANE-UI -- pass: a one-line proposal in a letter
   to LANE-UI naming the reply shape, not code yet (a design question, per this lane's own charter
   item 2: open the letter, keep building what's already known).
