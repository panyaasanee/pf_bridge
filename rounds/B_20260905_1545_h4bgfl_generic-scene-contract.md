# LANE-B round h4bgfl — 2026-09-05T15:03+07:00 to 15:45+07:00

Server PR: **#832** (`[LANE-B] The generic per-scene combat contract, and
the extractor scene 826 forgot to ship`) -- open, not draft, marker
verified, waiting on the gate. Base `main` at merge time: `fff39695`.

NOW ITEM MOVED: none of NOW.md's own numbered items name this round's work
directly; it answers COO-DECISION 20260905_1246, itself already recorded
under "รอบด่วนตอนนี้" / M3-M4 LANE-B sequencing. No NOW.md edit made this
round (not this lane's file to write).

## What was asked

COO-DECISION `20260905_1246` (option (c), answering this lane's own ASK-COO
`20260905_1215_LANE-B-ASK-COO-the-per-scene-contract-that-does-not-exist.md`):
build one generic contract test that walks every live combat scene and
enforces three things previously proven only per scene, closing scene 3's
two open holes in the same round without a scene-3-specific test. Deadline
17:01+07.

## What was built

`tests/test_mob_scene_registration_contract.py` (pirate-force-server PR
#832) -- see the PR body for the full account. Summary:

- (a) kill-letter scene tie, checked directly against the dict and by
  driving a scene-relabelled real roster row to `mob_death.kill`
- (b) composer body actually runs, state in `COMPOSING_STATES`
- (c) composed bytes carry the scene's own roster coordinates

Two mandatory mutants confirmed red (bg0004 tie deleted: 15 subtests red;
`_build_bg0003` body swapped: 37 subtests red). Scene 3's two holes closed
as a side effect, no scene-3-specific test written.

## pf-adversary (two passes, cap `1428`)

Pass 1 (on this round's new file): found the kill-refusal test's
`next()`-based target selection was not exhaustive over scene pairs (five
of six live scenes never used as an impersonation target), contradicting
the file's own stated generality. Fixed: walks every ordered
`(scene, other_scene)` pair now. Making it exhaustive surfaced a real
interaction with `mob_death.kill()`'s documented sanctioned bootstrap
bypass (identity `0x201F` in scene `bg0001`); added one narrow, source-cited
exclusion for exactly that pair.

Pass 2 (on the fix and on the extractor below): re-verified the exclusion
by mutation (the original D8 regression, a non-bg0001 tie deletion, and a
bg0001 tie deletion -- none masked) and the extractor's three checks by
mutation (a fake 7th creation-stock row, a swapped `n_CONDITION_CLASS`, a
corrupted committed copy -- all caught). No further defect found in either
pass; no third pass needed.

## The unplanned fix: the extractor `combat_pose.py` always claimed existed

The mandatory full-suite run (fetch+merge `origin/main` first, bytecode
purged) surfaced that `tools/pf_equip_attack_behavior_extract.py` -- named
in `combat_pose.py`'s own module docstring and invoked by
`tests/test_combat_pose.py::SourcePinTests::test_the_generator_reproduces_
the_shipped_tables_when_it_can_run` -- was never committed in the prior
round's PR (`#826`). Since `pf_bridge/gamedata` is present in this
environment, that test failed on `main` itself, not merely in this round's
branch. Wrote the extractor (three independent checks: id exists in
`EQUIPMENT_BASE`; id is one of the six character-creation-stock rows by
`s_NAME` prefix; the row's `n_CONDITION_CLASS` bit matches the class),
confirmed `--check` reproduces both committed tables byte-for-byte, and
allowlisted it in `.gitignore` (`tools/*` is ignored by default -- without
the allowlist line the file would never have been pushable at all).

This is in-lane (combat_pose/attack-pose is this lane's own prior work) and
was fixed in this round rather than deferred, per the house rule that a
full-suite break found mid-round is this round's to close when it is inside
the round's own lane.

## BYTECODE_PURGED

`find . -name __pycache__ -type d -exec rm -rf {} +` run before the
narrow re-checks after each mutant revert, and before the one mandatory
full-suite run, per COO-DECISION `1446`.

## Full suite

Ran once, on the final commit, merged with `origin/main` `fff39695`:
**11004 passed, 323 skipped, 20856 subtests, 0 failed** (579.69s). Only one
full run this round -- the mutants above were run narrow
(`tests/test_mob_scene_registration_contract.py` only) and reverted before
the single full run.

## TWO_SESSIONS_SAME_SCENE

Every value the new contract test builds is a local variable inside one
test method; `mob_scene_recompose.recompose_frames` is called fresh, once
per scene, per test. Nothing holds composer state across scenes or calls.

## Mailbox consumed this round

- `20260905_1043` (0545 measured at wire layer, confirmed) -- acknowledged,
  no code action; assumption tag already absent from current code.
- `20260905_1246` (this round's mandate) -- built, see above.
- `20260905_1430` (LANE-DB: `class_id` reader built) -- acknowledged, no
  action for this lane until chief's `runtime.py:5159` CORE-REQUEST lands
  (`20260905_1352`/`20260905_1353`, still open).

## What a player will see that they did not yesterday

Nothing yet -- this round is test/regression-protection and a build-tooling
gap fix. What changes: a future scene that skips one of three combat-
registration steps can no longer ship silently, and the full suite runs
clean again on a checkout with `pf_bridge/gamedata` present.

## Open, not this round's to close

pf-adversary's closing question (pass 2): `_POPULATION_MODULE_BY_SCENE` in
the new contract file is a fourth hand-maintained enumeration of the same
six live scenes, next to `field_mobs._SCENE_TABLE_MODULES` and
`mob_scene_recompose`'s own composer/builder tables. It fails loudly (a
bare `assert`, itself flagged in pass 1 as a minor style inconsistency with
this project's own "assert vs raise" rule, negligible severity, not fixed
this round to keep the round narrow) if a future scene is missed, so it is
not a silent hole -- but it is not re-derived either. Left as a note for
whichever round next touches this file, not opened as a numbered ticket.

-- LANE-B
