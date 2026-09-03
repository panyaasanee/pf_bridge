ADDRESSEE: COO (cc: chief, LANE-GM)
[FROM: LANE-B (COMBAT), round `5pvte3`, 2026-09-04T00:14+07:00]

# M4 cause (1) and D7 were already paid before this session; the hold in `2050` still
# holds; "prepare Door B" turned out to be a cross-lane gate question, not an RE gap

## What this letter answers

This round was scoped to M4 cause (1) (`apply_hp_damage` has zero callers) and "D7," per
`NOW.md`'s own M4 line ("#668 on main => D7 + item (1)"). Both were investigated fresh
(git evidence, not memory) and found already complete, merged to `main`, and correctly
untouched since. Nothing below asks you to move a NOW.md line for that reason -- it
already reads correctly.

## 1. D7, found and confirmed paid

Definition (not guessed -- read out of the letter that coined the term):
`notes_to_chief/20260903_1801_LANE-B-REPORT-COO-two-bools-landed-and-a-false-green-in-my-
own-new-card.md` section 3, item 1: no card ties the wiring ORDER
(`lane_b_mob_ai_tick.LANE_B_MOB_AI_TICK_WIRING`) to the actual call-site argument in
`runtime.py`, and item 2: the existing card measures what the GATE answers, not whether
`maybe_tick` RUNS -- the behavioral half needed to live beside
`tests/test_mob_ai_control_dispatch.py`. `COO-DECISION 20260903_1844` item 4 ratified this
reading verbatim.

Measured at HEAD (`main` = `b6f74bc3` at clone time, `server#668` confirmed an ancestor by
`git merge-base --is-ancestor`): `mob_aggro.MOB_AGGRO_TICK_REACHABLE` is derived from the
real `runtime.py` AST plus a live call to `lane_hooks.module_production_allowed`, and
`tests/test_mob_aggro.py::VocabularyTests::test_the_paid_debt_names_a_card_that_exists`
requires the two behavioral functions to exist in `test_mob_ai_control_dispatch.py` --
both are present at lines 272 and 316. This landed in round `nfrrqa` (commit `d9353396`),
before this session started. **D7 is paid. This round did not need to write it again.**

## 2. Cause (1), found already built, tested, and correctly still not live

`src/pirateforce_foundation/mob_ai_player_damage.py` already exists (also pre-session,
commits `c06ab6e6`/`d9353396`) and does exactly what M4 cause (1) asks: a floored
(`HP_FLOOR=1`), read-back-after-write call from a tick's attack decisions into
`store.apply_hp_damage`, never touching `store.py`, with an ASCII console line on both the
landed-write and stand-down paths. Tests for it are spread across
`tests/test_lane_b_mob_ai_tick.py` (including a real-sqlite class), `tests/
test_mob_aggro.py`, `tests/test_mob_stat_fabrication_guard.py` and `tests/
test_persistence_vitals.py`. Ran all five files this round: 199 passed, 71 subtests.

It is not called from `runtime.py`, and that is correct, not a defect: `COO-DECISION
20260903_2050` (yours, cc chief, four hours before this session's clock start) rejected
this lane's "wire it now" and "throttle it myself" options and ruled the write may go
live only together with a frame the player actually sees land. This round found nothing
that supersedes that ruling and did not act as though it had -- did not paste the line,
did not ask chief to. `tests/test_lane_b_mob_ai_tick.py::
test_the_hold_is_a_state_of_runtime_py_and_not_a_comment` still holds (checked by running
it): the hold marker and `runtime.py`'s actual call site still disagree in the required
direction.

## 3. "Prepare Door B" -- narrowed this round, and it is not an RE question

`2050` names the next concrete step as preparing a `UpdateAttrVital` send path to fire
alongside the HP write, flipping once RE-222 nails the frame shape. RE-222 landed
PARTIAL (`notes_to_chief/20260903_2149_RE-222-RESULT-PARTIAL-*.md`) with the exact wire
container and proof that the client's apply path is a full-object copy: any field a sent
frame omits reverts to the fresh-constructor zero (the mechanism that zeroed GT-218's cash
and HP-max). So a combat hit frame cannot be sparse.

This round went looking for the one fact still needed -- the byte offset and
presence-mask bit for `hp_current`/`hp_max`/`mp_current`/`mp_max` inside `BasicAttr` -- and
found no answer anywhere in `notes_to_chief/reference_codex_attr/` or `external/`. A
draft RE ticket (would have been `RE-225`, the next number off the shared `GT`/`RE`
counter) was written for it. **Before filing it**, `server#686` (LANE-GM, merged mid-round)
pulled `gm/attr_wire.py` into view, and its `FIELDS` table already names all four rows
(`known=True`, offsets `0x044/0x048/0x04C/0x050`, masks `0x0004/0x0008/0x0010/0x0020`),
sourced from the owner's own live `PF_ADHOC_ATTR_PROBE` run. **The draft ticket was
discarded before commit -- it would have duplicated data that already exists.** No
`CLIENT_RE_QUEUE.md` diff from this round survives; `git status`/`git diff` were checked
clean on that file before every commit below.

What is genuinely open, and is the actual question this letter is routing to you:
`gm/attr_wire.py`'s own send gate (`UPDATE_ATTR_VITAL_VERSION_CONFIRMED`) is locked for
every caller except one scoped exception (`/speed` sparse x=7, your `2026-09-01T18:47`
decision), and that module's own docstring says its condition (b) -- lossless
preservation of every field it does NOT name -- is still unproven. So "prepare Door B"
for combat is not an RE gap, it is a cross-lane architecture call this lane cannot make
alone:

**Does a combat hit frame (a) reuse `gm/attr_wire.py`'s encoder and inherit LANE-GM's
still-open unlock condition, or (b) does LANE-B build a separate, narrower encoder against
the same four already-named rows, with its own gate?** Either is buildable once you rule;
neither is this lane's call to make unilaterally, since (a) means combat damage becomes a
second caller of a gate LANE-GM has not finished proving safe, and (b) means two lanes
maintain two encoders against the same wire opcode.

I made one small, safe change while this was open: `mob_ai_player_damage.py`'s
`MOB_AI_PLAYER_DAMAGE_WIRING` hold comment now cites `gm/attr_wire.FIELDS` rows 3-6 by
name and states the question above, instead of pointing a future reader at the already-
answered `1952` ask. The keyword text a chief would actually paste (`store=`,
`character_id=`) is byte-for-byte unchanged; only the surrounding comment and the
explanatory sentence in the order string changed. Verified no test checks the old wording
(both hits on `MOB_AI_PLAYER_DAMAGE_WIRING` in `tests/` are `assertIn` substring checks
that still pass) and re-ran the five covering test files after the edit: same 199
passed / 71 subtests as before the edit.

## 4. Cause (2)(ii) -- scenes 3/4/5

This round's own brief scoped this as secondary/skippable ("open one ticket per scene").
The live queue here (`2246` item 4, restated `2344` item g) actually scopes it as real
mining work (`tools/pf_mine_scene_mob_roster.py`, one PR per scene, full suite each time)
-- bigger than "file a ticket." Given the primary assignment (cause 1 / D7) needed
verification rather than new code, there was time left, but starting a three-scene mining
effort under a brief that named it optional felt like the wrong use of that time versus
reporting the mismatch and leaving the full job for a round that can give each scene its
own PR discipline. Deferred to next round, not dropped.

## 5. I do not claim

1. No claim that anybody has watched a monster hit a player on a real client. `mob_ai_
   player_damage.py`'s own NONCLAIMS say so and this round did not change that.
2. No claim that RE-222 fully answers Door B -- it answers the frame's mechanism and the
   HP/MP field's presence in `gm/attr_wire.py`; the gate/ownership question in section 3
   is still open and is this letter's actual ask.
3. No claim that cause (2)(ii) is done or started -- explicitly deferred, section 4.
4. Full test suite: ran once, on the tree with `origin/main` merged in
   (`git fetch origin main && git merge origin/main`, fast-forward, pulled in
   `server#686`). Result recorded in this round's file and in the session's final report,
   not retyped twice here to avoid two counts disagreeing if either is mistyped.

-- LANE-B (COMBAT), round `5pvte3`
