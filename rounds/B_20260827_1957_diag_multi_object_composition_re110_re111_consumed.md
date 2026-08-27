# LANE-B round B_20260827_1957 -- GT-DIAG-MULTI-OBJECT-001 composition built, RE-110/RE-111 consumed

IMPORTANT, read first: mid-round the owner issued ADDENDUM 20:18 to the
PANYA-ORDER, naming Mountain Deer (MOBS n_ID 27) as the body for all five
objects, superseding this round's pick (Jungle Big Tiger, template 60).
Mountain Deer is not in bg0001's mined roster and template 27 is not in
mob_death.WIDENING_RULINGS's covered set -- both are next round's work, not
done here. This round's code correctly answers ADDENDUM 19:05's original
two-criteria question for the body it names; it is simply superseded by the
owner's own later, more specific choice. See mob_diag_multi_object.py's
module docstring (top) for the full note.

- TZ=Asia/Bangkok date: 2026-08-27T19:57+07:00
- Heartbeat check: notes_to_chief/_BRIDGE_HEARTBEAT.txt last line
  2026-08-27T19:42:03+07:00 -> delta 15 min, within the 60-minute rule.
- Prior-round-fate check (addendum v2 section A): last [LANE-B] PR in each
  repo -- pf_bridge#226 and pirate-force-server#135 -- both merged=true on
  main (verified via pull_request_read). No recovery needed.
- Open [LANE-B] PR check (base lock rule): search_pull_requests
  `is:open in:title [LANE-B]` returned 0 results in both repos before this
  round started (only an unrelated open [LANE-E] draft in each repo).
- Mailbox scan (addendum v2 section B): three unconsumed items addressed to
  LANE-B -- RE-110-RESULT (18:32), RE-111-RESULT (18:39), and
  PANYA-ORDER-diag-multi-object-boot (18:55, ADDENDUM 19:05). All three
  read and acted on this round; see notes_to_chief/20260827_1957_LANE-B-
  STATUS-diag-multi-object-composition-built-re110-re111-consumed.md for
  the full account.

## Repo moved fast mid-round -- rebased twice

origin/main advanced three times while this round was in progress, including
a LANE-GM round (RE-113 opened) and what looks like chief's own CORE-REQUEST
wiring MOB-COMBAT-001/MOB-DEATH-001 into runtime.py's real dispatch
(`_dispatch_mob_combat` exists on main now; tests/test_field_mobs.py's own
tripwire test already expects runtime.py to mention field_mobs/mob_combat/
mob_death). A new module, player_hostile_pairing.py, also landed. Rebased
this round's branch onto fresh main twice (stash/reset/pop); the only
conflict was the field_mobs-importers tripwire list in test_field_mobs.py,
resolved by keeping main's real assertions (runtime.py IS wired now) and
adding mob_diag_multi_object.py to the importers list this round adds.

## This round's work

1. **RE-110 (auto-attack cadence/pose) consumed.** Closed in
   `CLIENT_RE_QUEUE.md` as CLOSED MIXED/BOUNDED-NEGATIVE. Pose selector is a
   positive field map (`ActionVital +0x30` -> `EQUIP_VALUE.n_ATTACK_SKILL` ->
   `BEHAVIOR.n_ID`); auto-repeat and real cadence hit static's method
   ceiling. `BUILD_IMPACT` says do not change production composition until
   an attended one-field A/B lands -- `mob_combat.py`'s
   `ATTACK_CADENCE_MS_PROVISIONAL=600` stays provisional. No code change
   owed.
2. **RE-111 (loot-drop render fields) consumed.** Closed in
   `CLIENT_RE_QUEUE.md` as CLOSED BOUNDED-NEGATIVE. Current 54B ground-list
   shape is complete for a generic announcement; no missing field has
   provenance. `mob_loot.py` checked for any guessed field -- none found,
   no code change owed.
3. **PANYA-ORDER diag-multi-object-boot: composition layer built (round 1
   of the order's own 2-round budget).** New module
   `pirate-force-server/src/pirateforce_foundation/mob_diag_multi_object.py`
   defines the five objects (D0 control, D1a dying-timer-hold, D1b
   dead-only-after-target, D2 repeat control, D3 no-faction-splice), all
   built by reusing existing production functions
   (`field_mobs.hostile_actor_entry`/`hostile_npc_attr`,
   `mob_death.kill`/`dying_frames`/`dead_frames`, and one direct call to the
   legacy bridge's `make_npc_attr` for D3) -- no new composer invented.
   `tests/test_mob_diag_multi_object.py` (18 tests) proves the byte-diff
   claim for every object by re-deriving the expected bytes independently
   from the same production functions, never by trusting the module's own
   claim about itself. `tests/test_field_mobs.py`'s field_mobs-importers
   tripwire updated to include the new module (one line, per that test's
   own stated convention).

   Body chosen: Jungle Big Tiger (`template_id=60`, `field_mobs.
   HOSTILE_PLACEMENTS` placement 58), not the order's own example (Mountain
   Deer), because bg0001's already-mined `field_mob_ai_tables.
   AI_WANDER_ROWS[11]` is the only nonzero-aggro row this scene has
   (n_AGGRO=1200), and `CONSTDATA_TH__MOBS.tsv` row 60 reads
   `f_RATIO_EXP=1.0`/`n_MOB_APPEAR=1` against `0.0`/large-arbitrary-id for
   the two story-NPC rows checked for contrast -- both criteria the
   addendum asks for, answered by data this scene already has committed,
   without opening new cross-scene RE. Tagged `[LANE-B ASSUMPTION -
   PROVISIONAL]` in the module where those two columns' semantics are read
   by contrast rather than RE-proven directly.

   `mob_death.kill()`'s `widened=` gate: used the already-registered exact
   string `"COO-RULING-20260827-1350 widen-death-scope-bg0001"` (not a new
   string) -- the gate checks `mob.template_id`, not identity, and template
   60 is in that ruling's covered set. Flagged in the round letter to COO
   that this is the first caller to reach that gate with template 60 on a
   mob that is not one of the ruling's 13 named real placements (a
   synthetic diagnostic one sharing the template); `mob_death.py`'s own
   design authorises this (template-keyed, not placement-keyed) but its own
   `[OPEN RISK]` comment already predicted exactly this shape of case, so
   it is surfaced rather than assumed silent.

   D2 read as an exact repeat of D0 (a second on-screen reference point),
   not as a probe of RE-109's still-open alternate-mask-value question --
   that question has no field value with provenance yet per RE-109 itself,
   and this lane does not invent one.

   Not done this round (order's own 2-round ceiling covers it): wiring into
   `runtime.py` (chief's file). The exact wiring is written into the module
   as `GT_DIAG_MULTI_OBJECT_WIRING` and repeated in this round's letter as a
   CORE-REQUEST, including an open question for chief: does anything in
   this lane's dispatch already track "has this identity been sent a
   TargetVital" (needed for D1b), or does that need building too.

4. **GAME_TEST_QUEUE.md GT-114 DIAG-MULTI-OBJECT-001 written** (this repo),
   marked BLOCKED-ON-WIRING (not runnable until chief's CORE-REQUEST above
   lands), cross-referencing RE-107/108/109 and this round's module.
   Numbering re-confirmed by grep at write time (highest prior: RE-113);
   no other lane opened 114 in the interval. Ticket body 6.6KB, under the
   8KB rule.
5. **pf-adversary review run before commit** on the new module/tests. Five
   findings, all fixed in this diff before push (none deferred):
   - [HIGH] `DIAG_CENTER_Z` was 0.0, borrowed from a DIFFERENT scene's
     precedent (PANYA-DECISION scene17). pf-adversary queried this scene's
     OWN already-committed `population.py` census and found every real
     placement within ~3000 units of the test point clusters at z~2200-2250
     (closest, placement 19, z=2231.17 at ~931 units). Fixed:
     `DIAG_CENTER_Z = 2231.17`, sourced and labeled as a nearest-neighbour
     estimate, not a terrain query. Left at Z=0 this would have passed every
     test and the headless "prove it before calling the owner" gate while
     spawning all five objects roughly 2200 units from anything her camera
     could see -- burning the attended round for nothing.
   - [HIGH] `GT_DIAG_MULTI_OBJECT_WIRING` (the CORE-REQUEST text) falsely
     claimed "all five" objects use `DIAG_WIDENED_RULING`. Verified against
     the actual code: only D0/D2/D1a do (via `kill_schedule`/
     `dying_timer_hold_schedule`); D1b's `dead_only_schedule` calls
     `mob_death.dead_frames()` directly, which carries no identity/template
     gate at all. Fixed the wiring text and added a test
     (`test_the_wiring_line_is_correct_about_which_objects_pass_the_widened_gate`)
     pinning `dead_frames`'s signature has no `widened` parameter, so this
     can't silently drift back.
   - [MEDIUM-HIGH] Docstring claimed only TWO bg0001 hostiles have nonzero
     aggro (Jungle Big Tiger, Ward Apes). A third exists: placement 132,
     Orc Chief (template 103), same `ai_wander=11`/`n_AGGRO=1200`, missed by
     a single unverified scan. Fixed the count to three, added the
     tie-breaker this module actually uses (lowest level of the three), and
     added `test_exactly_three_bg0001_hostiles_have_nonzero_aggro_and_
     control_is_lowest_level` so a future miscount fails loudly.
   - [MEDIUM] The `n_MOB_APPEAR`/"per-NPC ids 8700001/8700002" half of the
     template-60 justification was wrong on both counts: those numbers are
     `n_DROPS_QUEST` values, not any per-NPC id field, and `n_MOB_APPEAR=1`
     is the value on 92% of the whole table (the default, not a signal).
     Retracted from the docstring; the pick now stands on `f_RATIO_EXP`
     alone (1.0 vs 0.0 for the two comparison NPCs), which pf-adversary
     re-checked directly and confirmed.
   - [DISCLOSED] D1b's `target_vital_seen=True` attestation is unverifiable
     by this lane -- already disclosed in the module's own wiring text
     (says so plainly rather than hiding it); no code fix applies here
     beyond making sure the now-corrected wiring text is what chief
     actually reads.
   Full suite re-run after every fix: 110/110 on the three affected test
   files, 3663/3663 minus the same pre-existing 18 capstone-import errors on
   the whole suite (unrelated to this round, present on `main` before this
   diff too).

## Player-visible change this round

None yet from LANE-B's own commit -- the diagnostic composition is
unwired code + tests, same "no player-visible change" shape as a pure
consumption round. BUILD-004/005/006 status carried from prior rounds:
BUILD-004 re-verified live last round (13/13 mobs, 115/115 census);
BUILD-005 appears to be wired into production now (found mid-rebase, not
this round's own work -- needs chief/COO attended confirmation before
SERVER_VERSIONS.md says so); BUILD-006 has `dispatch_pickup_request()`
from a prior round.

## Write zone respected

`pirate-force-server`: `src/pirateforce_foundation/mob_diag_multi_object.py`
(new), `tests/test_mob_diag_multi_object.py` (new), `tests/test_field_mobs.py`
(tripwire line only). `pf_bridge`: `CLIENT_RE_QUEUE.md` (own RE-110/RE-111
headers only), `GAME_TEST_QUEUE.md` (new GT-114 appended, nothing existing
touched), `notes_to_chief/`, `rounds/`. No `runtime.py`/`app.py`/
`pf_login_game_server_v141.py`/`scenarios/world_*.json` touched.
