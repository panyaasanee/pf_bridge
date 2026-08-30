# LANE-A round `n8fq3w`

Opened 2026-08-30T11:24+07:00 (TZ=Asia/Bangkok date), this account written
2026-08-30T11:36+07:00. HEAD at open: `pirate-force-server` branch
`claude/sleepy-ride-vapdhx` @ `1619aee` (PR #303 merged, matches
`origin/claude/sleepy-ride-vapdhx` exactly -- confirmed, no divergence);
`pf_bridge` branch `claude/quirky-planck-vapdhx` @ `7df691a` (PR #481
merged, matches `origin/claude/quirky-planck-vapdhx` exactly -- confirmed).

## Section A -- previous-round merge check

Both prior LANE-A rounds' PRs are confirmed merged onto their branch's own
history (not `main` -- this repo's `main` is a separate, unrelated lineage
at `645cca2`/PR #53 that does not contain this branch's PR #302/#303
history at all; that is a pre-existing repo-layout fact this round did not
create, flagged under "noticed outside scope" below, not investigated
further). No round "disappeared" -- nothing to recover.

## Section B -- mailbox

Checked `notes_to_chief/` for anything addressed to LANE-A (`ADDRESSEE:
LANE-A` and the `[ถึง: LANE-A ...]` header form) without a consumed copy.
Every literal `ADDRESSEE: LANE-A` letter already has a copy under
`consumed/`. The stale prompt's named tickets (`RE-095`, `096`, `097`,
`100`, `102`, `103`) were consumed on 2026-08-27
(`rounds/A_20260827_1448_mailbox_consumption_re095_re096_re097_re100_re102_re103_scene17_ground.md`)
-- re-confirmed here, not re-done.

One letter WAS outstanding under the `[ถึง: LANE-A ...]` header form (not
literal `ADDRESSEE:`, so a plain string grep missed it on the first pass):
`20260830_1022_CHIEF-REPLY-CORE-REQUEST-choosenpc-scene-guard-wired.md`
(chief, round `hd6tac`/R237). It named the one-line follow-up this round
does -- see Section F. Consumed this round: copied to `consumed/`, stub
written, both timestamped from `TZ=Asia/Bangkok date`.

The two newest letters (`20260830_1109_RE-156-...`,
`20260830_1111_RE-157-...`) are addressed `ถึง chief`, not to LANE-A; read
for context (RE-157 flags TradeCmd/mob-combat guard gaps that belong to
`runtime.py`, the chief's file) but not consumed as LANE-A mail. `GT-148`
and `GT-134` remain `PENDING`/`[READY]`, both attended-only tickets this
cloud-only round cannot run (no `LOCK_GAME`, no GameClient access here).

## Section F -- real work, not an empty round

`e2q8c6` (previous round) was zero-diff. This round is not: it does the
one-line follow-up the chief's own reply letter named as still outstanding
and explicitly left to this lane's judgement.

### What changed and why it is safe

`src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene14.py`'s
`production_allowed` flips `False` -> `True`. Context, read fresh this
round rather than assumed from memory:

- The `runtime.py` guard this responder's own CORE-REQUEST asked for landed
  on `main` in round `hd6tac`/R237 and has sat there unflipped through one
  full round (`e2q8c6`, zero-diff).
- Scene 14 (Hell Volcano Island)'s login door is **already** open
  (`login_entry_allowed: true`, LANE-A round `vvy6q7`, COO-DECISION
  `20260829_2342`) and defect D3 (the dropped faction-1 byte) is
  **already** closed (`world_faction_admission.py`, same round). Neither
  of those depended on this flag.
- `SceneCensusResult.membership` -- the field this flag ultimately arms --
  only ever governs whether a `ChooseNPC`/`TARGET_VITAL` click on one of
  scene 14's 81 composed actors is ANSWERED. It never governed whether
  those 81 actors are drawn in the arrival frame; that frame already ships
  regardless of this flag (`lane_a_scene_census.py`'s own composer, wired
  since round `73fhoc`/chief and `02k3w5`/this lane).
- Before this flip: a scene-14 session's `population_indices` was never
  armed, so a click never reached the frozen per-actor loop at all (that
  loop only runs once `population_indices` is non-`None`) -- no crash
  risk, only a click that got no wire response.
- After this flip: the same click gets answered through the guard chief
  wired, using the same frozen wire shapes `world_face_frame.py` already
  uses for Port Royal, sourced from scene 14's own placement table
  (`world_bg0015_identity`). No new wire shape, no new scene, no touch to
  scene 278, M2 acceptance criteria, or the walk-in travel gate
  `COO-DECISION 20260826_1645` ordered off by default forever.
- Two gaps chief's reply letter named, both already pinned by tests before
  this round and left as-is (my own design judgement, matching the
  letter's own framing "not asking you to fix them before flipping"):
  claiming the scene skips v141's own `TARGET_VITAL` arming side effect
  (harmless today, scene 14's real actors don't have the arena-harness
  identity shape that arming's later consumer wants), and a multi-select
  click is answered with only one frame instead of one-per-identity.

### What I could NOT do: run pf-adversary as a subagent

The close-out protocol calls for a pf-adversary pass before any non-typo
commit. This session has no Task/subagent-launch tool -- only Read, Grep,
Glob, Bash, Edit, Write, directly. I read `.claude/agents/pf-adversary.md`
in both repos and applied its checklist to this diff myself rather than
skip the step silently. What that pass found and fixed **before** this
letter was written, not after:

- **Item 8, evidence layer laundering**: my first docstring draft claimed
  "a player standing on Hell Volcano Island already sees 81 named actors"
  as a flat fact. `GT-134` (the attended ticket for exactly this question)
  is still `[READY]`, not `PASS` -- nobody has looked. Rewrote that
  paragraph to say only what the wire/DB layer actually proves (the
  census frame ships 81 entries; whether a client renders them is
  `GT-134`'s unmeasured question) and to say plainly that this round's own
  claim about the click response is wire/DB-only, driven by this lane's
  own tests, not by any attended session.
- **Item 3/13**: re-read the chief's letter's own two pinned-gap paragraphs
  in full before citing them, rather than the convenient half.
- **Item 6/regression**: checked that `_PRODUCTION_ALLOWED` /
  `_SCENE_CHOOSE_NPC_RESPONDERS` are process-global dicts populated once by
  `_discover()` at import, so flipping the module attribute is picked up
  automatically with no second registration call needed, and grepped
  `tests/*.py` project-wide for any assertion counting "how many lane_hooks
  modules are production_allowed" that this flip could break -- none
  exists; every existing assertion is per-module.
- Ran the full existing test file (22/22 green baseline) before touching
  anything, then after each edit, then the whole file again (22/22), then
  the four related test modules (`test_lane_a_scene_census`,
  `test_lane_hooks`, `test_lane_scene_census_wiring`,
  `test_world_lane_static`: 69/69), then the full suite (5528 tests,
  errors=18, all pre-existing `ModuleNotFoundError: capstone`, same shape
  as `e2q8c6`'s 5508/18 baseline -- count grew from unrelated commits
  between rounds, not from this diff), then
  `tools/verify_hypothesis_ledger.py` (`PASS entries=47`) and
  `tools/verify_functional_coverage.py` (`PASS domains=8`), then a cp874
  encodability check on both touched `src/` files (both OK), then
  `git diff --check` (silent).
- I could not build the worktree-isolation step the agent file requires
  for its own mutation experiments (no separate worktree tooling exercised
  here beyond what `git worktree` itself would need, and this round makes
  no destructive/mutating experiment against the live checkout -- only the
  final, reviewed edits are present). Said here rather than silently
  assumed equivalent to the real subagent.

This is a substitution, not the real thing, and I am saying so rather than
writing "pf-adversary reviewed this" in the PR body.

### Files touched (pirate-force-server)

- `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene14.py` --
  flag flip + docstring rewrite (struck-not-deleted, per project
  convention) explaining what changed, why it is safe, and the evidence
  layer split above.
- `src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py` -- two
  docstring corrections: the ChooseNPC-gate paragraph (was describing the
  now-superseded closed state) and a separately-stale "scene 14 is not open
  to players / nothing today" opening claim that predated round `vvy6q7`
  and was never corrected there. Both struck-not-deleted.
- `tests/test_lane_a_choose_npc_scene14.py` -- renamed
  `TheResponderModuleGateIsClosedTests` ->
  `TheResponderModuleGateIsOpenTests` with both assertions flipped;
  removed now-redundant/now-harmful manual `production_allowed` forcing
  and `addCleanup` resets from `OnTheRealDispatcherBothWaysTests
  .test_responder_registered_and_allowed_membership_is_armed` and from
  `TheGuardAnsweredTheClickInsteadOfCrashingTests.setUp` (forcing True was
  a no-op once True is the default; the old `addCleanup` back to `False`
  would have actively broken every later test in the same process by
  resetting the real default); converted
  `test_no_responder_membership_withheld_stands` from "today's default,
  undriven" to an explicit forced-absent regression case (`mock.patch.dict`
  scoped to scene 14's own registry key only, restored automatically) so
  the withhold path this composer still has to support stays pinned even
  though scene 14 itself no longer takes it. 22/22 tests still pass; no
  test deleted, two renamed with history kept in their own docstrings per
  this project's convention (matching the `TheCrashThisModuleGuardsAgainst
  Tests` -> `TheGuardAnsweredTheClickInsteadOfCrashingTests` precedent from
  round `hd6tac`).

### Nonclaims

1. No client-observable claim. Nothing in this round opened a GameClient;
   `GT-134` remains the open attended ticket for whether scene 14's actors,
   or an answered click on one of them, render as intended. This round's
   evidence is wire/DB layer only: driven end-to-end through the real
   dispatcher by this lane's own offline tests.
2. Does not fix, or claim to fix, either gap pinned by
   `TheGuardAnsweredTheClickInsteadOfCrashingTests` (v141 arming skip,
   multi-select single-answer). Both remain exactly as chief's letter left
   them.
3. Does not touch, re-enable, or imply progress on scene 278's walk-in
   travel gate or M2 as a milestone. M2 stays formally paused
   (`PANYA-DECISION 2026-08-27 20:10`, twice reaffirmed).
4. Does not claim any change to who can REACH scene 14. Reachability is a
   separate mechanism (a character's own persisted `character_positions`
   row naming 14, or an account-scoped GM `/warp`) this round did not
   touch.
5. Does not touch `runtime.py`, `app.py`, or
   `current/pf_login_game_server_v141.py`. All three untouched, confirmed
   by `git diff --stat` before commit.

## Noticed adjacent to this diff, not fixed

`lane_a_scene_census.py`'s own "THE ONE THING STILL IN THE WAY (defect D3,
this lane's debt)" section, a few lines below the paragraph this round did
edit, is ALSO stale -- D3 was closed by `world_faction_admission.py` in an
earlier round (`vvy6q7`), before this round started, unrelated to this
round's own edit. It does not contradict anything this round wrote (it
never claimed to widen that guard, and still doesn't), so left alone to
keep this diff to the two paragraphs this round's own change actually
requires touching. Whoever next edits this file's docstring should expect
to find it and fix it then.

## Noticed outside scope, not fixed

`pirate-force-server`'s `main` branch (`645cca2`, PR #53 lineage) is a
completely separate history from this lane's working branch
`claude/sleepy-ride-vapdhx` (PR #302/#303 lineage) -- `git merge-base
--is-ancestor main HEAD` fails both directions. This round's own
instructions and this branch's own PR history make clear the working
branch, not `main`, is this lane's actual integration point, so this did
not block anything -- but a future round or a human skimming `git log
main` alone would see a different, unrelated set of LANE-A/LANE-B commits
(e.g. `LANE-B MOB-AGGRO-001`, a different `LANE-A BUILD-002 / M2` round)
and could mistake that for this lane's current state. Flagging for
whoever owns branch/main hygiene; not this round's to fix.
