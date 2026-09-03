# LANE-B (COMBAT) round `5pvte3` -- 2026-09-04T00:14+07:00

## 0. NOW.md -- what this round moves

Read `NOW.md` first, then `pf_bridge/notes_to_chief/` for `D7` (per this round's own brief,
which is the incoming-task letter, not a pf_bridge file).

- **Does NOT move**: M4 cause (1), "`apply_hp_damage`/`apply_hp_heal` has zero callers".
  Verified this round that it is **already fully built and merged**, by a round that ran
  before this session started (commits `c06ab6e6`, `d9353396`, both ancestors of `main` at
  `b6f74bc3`). This round did not need to write that module; it already exists as
  `src/pirateforce_foundation/mob_ai_player_damage.py`.
- **Does NOT move**: "D7" (the M4 combat-tick card). Also already paid, same pre-session
  window, round `nfrrqa`: `tests/test_mob_aggro.py::VocabularyTests::
  test_the_paid_debt_names_a_card_that_exists` requires two named functions to exist in
  `tests/test_mob_ai_control_dispatch.py`; both do (`test_a_target_pos_frame_really_runs_
  the_tick_not_only_the_gate`, `test_the_tick_does_not_run_on_a_frame_that_is_not_a_target_
  pos`), confirmed by grep and by running the file (below).
- **Does NOT move**: the live wiring of `apply_hp_damage` into `runtime.py`'s
  `maybe_tick` call. This is deliberately ON HOLD, and correctly so --
  `COO-DECISION 20260903_2050` (cc chief) already ruled that this write may not go live
  except together with a frame the player actually sees land. This round did not flip it,
  and did not ask chief to flip it either: doing so would contradict a live, reasoned,
  COO ruling this same lane received two rounds before this session started.
- **Narrowed this round**: what "prepare Door B" (the COO's own next-step wording in
  `2050`) is actually waiting on. Not an open RE question -- see section 3.
- **Not touched**: M4 cause (2)(i) (register/ledger de-sync at scene edges) -- explicitly
  the chief's per this round's own brief.
- **Deferred to next round**: M4 cause (2)(ii) (scenes 3/4/5 rosters). See section 5 --
  this is a bigger, real mining task than "open a ticket," and this round did not have a
  mandate to touch it as the primary job.

## 1. What this round actually investigated

Cloned both repos fresh, read `pirate-force-server/AGENTS.md`, then `pf_bridge/NOW.md`
(`git fetch` first, per house rule), which pointed at M4:

> "M4 hit-and-die still zero -- two causes, both LANE-B's: (1) `apply_hp_damage`/
> `apply_hp_heal` zero callers ... #668 on main => D7 + item (1)."

`git merge-base --is-ancestor` confirmed `server#668` (`eef0df7e`) IS an ancestor of
`main` (`b6f74bc3` at clone time). Per NOW.md's own sequencing rule, that made both D7 and
cause (1) due.

### 1.1 D7 -- found, not guessed

`grep -rl "D7" notes_to_chief/` turned up the definition in the letter that coined it,
`notes_to_chief/20260903_1801_LANE-B-REPORT-COO-two-bools-landed-and-a-false-green-in-my-
own-new-card.md`, section 3:

> "1. No card ties the wiring ORDER to the call site that COPIED it (D7) -- the card that
> would catch this exact bug directly. Cannot write it today because the two are
> deliberately different until chief lands 1648 => next round's debt.
> 2. The card measures what the gate ANSWERS, not whether `maybe_tick` RUNS. NONCLAIM in
> the card itself: going red the day 1648 lands is not a license to write True because a
> dict answered. The behavioral half must live beside
> `tests/test_mob_ai_control_dispatch.py`, which drives the real dispatcher headlessly."

`COO-DECISION 20260903_1844` item 4 confirmed this reading verbatim ("D7 = your next
round's debt the moment #668 is an ancestor of main ... the behavioral half goes beside
`tests/test_mob_ai_control_dispatch.py` as you proposed. Do not write
`MOB_AGGRO_TICK_REACHABLE = True` from a dict's answer").

Checked at HEAD: `mob_aggro.MOB_AGGRO_TICK_REACHABLE` is derived (not pinned) from the
real AST of `runtime.py`'s call site plus a real call to
`lane_hooks.module_production_allowed`, and `tests/test_mob_aggro.py`'s own
`test_the_paid_debt_names_a_card_that_exists` requires the two named behavioral tests to
exist in `test_mob_ai_control_dispatch.py`. Both are present (`grep -n` confirmed line
272 and 316 of that file). This work landed in round `nfrrqa`
(`d9353396`), which is an ancestor of `main` and predates this session. **D7 is paid.
Nothing to build.**

### 1.2 Cause (1) -- built, tested, merged, correctly not live

`src/pirateforce_foundation/mob_ai_player_damage.py` (449 lines before this round) already
does exactly what this round's brief asked for: it turns `mob_ai_scheduler.tick_session`'s
per-tick attack decisions into a clamped-at-`HP_FLOOR=1`, read-back-after-write call to
`store.apply_hp_damage`, prints `MOB_AI_PLAYER_DAMAGE char=... hp=X->Y/Z floor_held=0|1`
on a landed write and `MOB_AI_PLAYER_DAMAGE_STAND_DOWN reason=...` on every refusal, never
touches `store.py`, and is covered by tests spread across `tests/test_lane_b_mob_ai_tick.py`
(most of the behavioral coverage, including a real-sqlite `RealDatabaseDamageTests` class),
`tests/test_mob_aggro.py`, `tests/test_mob_stat_fabrication_guard.py` and
`tests/test_persistence_vitals.py`.

What is genuinely NOT done, and is not a defect: the module is never called from
`runtime.py`. `lane_b_mob_ai_tick.maybe_tick` grew two optional keyword arguments
(`store`, `character_id`) for exactly this purpose, both still unpassed by `runtime.py`
(chief's file, out of reach for this lane per its own hard limits). This is not an
oversight -- `tests/test_lane_b_mob_ai_tick.py::
test_the_hold_is_a_state_of_runtime_py_and_not_a_comment` reads `runtime.py`'s AST and
requires the hold marker and the actual keyword arguments to disagree in exactly one
direction at all times, so a paste without an answer, or an answer with no paste, is red.
Confirmed still consistent (hold marker present, no keywords passed) by running the file
this round (section 4).

**Why it is still not wired, and why this round did not wire it**: this lane asked COO
three options in round `nfrrqa`'s letter
(`notes_to_chief/20260903_1952_LANE-B-ASK-COO-damage-door-built-rate-is-one-hp-per-frame.md`)
-- wire immediately, throttle unilaterally, or mine a cadence column. `COO-DECISION
20260903_2050` rejected the first two outright and answered the third "not minable today,"
then added a fourth condition nobody had asked for yet: **the write may go live only
together with a frame the player actually sees land** (`UpdateAttrVital`), because an
invisible, irreversible HP write is "silent grinding, not testable combat" (COO's own
words). That decision predates this session by roughly four hours and this round found
nothing that supersedes it. Overriding it -- either by wiring the call myself or by asking
chief to paste the line -- would mean ignoring a specific, reasoned, already-adjudicated
safety ruling this same lane received. This round did not do that.

## 2. So what did this round actually build

Given both assigned items (cause 1, D7) were already complete and correctly held, this
round's job narrowed to: verify the claims above independently (not just trust the
comments), and make real, safe progress on the one thing COO's `2050` ruling names as the
next concrete step -- "prepare Door B ... flip the moment RE-222 nails the frame shape."

`notes_to_chief/20260903_2149_RE-222-RESULT-PARTIAL-updateattr-and-name-color-gates.md`
(landed the same night, before this session) answered Q0 with the exact
`UpdateAttrVital`/`ActorAttr` wire container and proved the client's apply path
(`0x00464F30`) is a **full-object copy**: any `BasicAttr`/`ActorAttr` field a sent frame
omits reverts to the fresh-constructor default (zero), which is the exact mechanism that
zeroed `GT-218`'s cash and HP-max. That means a combat "hit" frame cannot be sparse (HP
bit only) without repeating `GT-218`'s failure on a different field the same round it
ships.

This round searched for the one fact that was still missing to build that frame: the
exact byte offset and presence-mask bit for `hp_current`/`hp_max`/`mp_current`/`mp_max`
inside `BasicAttr`. Grepped `notes_to_chief/reference_codex_attr/*` (the RE codex) and
`external/*` -- no hit for a player-owned HP/MP field anywhere in either (the only
`hp_current`/`hp_max` hits belong to `PetAttr`, a different class). A first draft of this
round drafted a new RE ticket for exactly that question (would have been `RE-225`, the
shared `GT`/`RE` counter's next number). **Before filing it**, `git fetch origin main` on
`pirate-force-server` pulled in `server#686` (LANE-GM, merged while this round was already
in progress), which touches `src/pirateforce_foundation/gm/attr_wire.py`. Reading that
file located the answer already sitting in this repo: `gm/attr_wire.FIELDS` rows 3-6 name
exactly those four fields --

```
(3, "basic", 0x0004, 0x044, 0x14, "u32", "hp_current", True, "HP bar")
(4, "basic", 0x0008, 0x048, 0x14, "u32", "hp_max",     True, "")
(5, "basic", 0x0010, 0x04C, 0x14, "u32", "mp_current", True, "")
(6, "basic", 0x0020, 0x050, 0x14, "u32", "mp_max",     True, "")
```

-- `known=True`, sourced from the owner's own `PF_ADHOC_ATTR_PROBE` live run (266 GM
commands in one connection, no crash), which this project already treats as a stronger
source than a fresh static RE ticket for named fields. **The RE ticket would have been a
duplicate of data that already exists.** The draft was discarded before it was ever
committed or pushed (no `CLIENT_RE_QUEUE.md` diff survives in this round's history --
checked with `git status`/`git diff` before every commit below).

What is genuinely still open, and belongs to nobody yet: `gm/attr_wire.py`'s own send
gate, `UPDATE_ATTR_VITAL_VERSION_CONFIRMED`, is locked for every caller except one scoped
exception (`/speed` sparse x=7 only, `COO-DECISION 2026-09-01T18:47+07:00`), and that
module's own docstring says its 3-point unlock condition (b) -- lossless preservation of
every field NOT named in `FIELDS` -- is still unproven. So "prepare Door B" for combat is
not an RE gap, it is a **cross-lane architecture question**: does a combat hit frame reuse
`gm/attr_wire.py`'s encoder (and inherit its still-open unlock condition, which this lane
did not create and cannot close alone), or does LANE-B build an independent, narrower
encoder against the same four named rows, with its own separate gate? This round did not
decide that -- it is not this lane's file, and the answer has stacking-order and
ownership consequences for LANE-GM's own open work. Routed to COO in this round's letter
(`notes_to_chief/20260904_0014_LANE-B-REPORT-COO-*`).

**What this round DID change**: `src/pirateforce_foundation/mob_ai_player_damage.py`'s own
`MOB_AI_PLAYER_DAMAGE_WIRING` comment block and the order string itself, updated
comment-only (the `store=`/`character_id=` keyword text a chief would paste is unchanged
byte-for-byte) to say the above precisely, so the next reader who lands on this hold does
not have to re-derive it: the COO answered `1952` already (`2050`), the field data is not
missing (cites `gm/attr_wire.FIELDS` rows 3-6 by name), and what remains is a COO
architecture call, not a research ticket. Verified no test checks the exact old wording
(`grep -rn "MOB_AI_PLAYER_DAMAGE_WIRING\b" tests/` -- both hits are `assertIn` substring
checks for `"store="` and `"MOB_AI_PLAYER_DAMAGE_WIRING_ON_HOLD"`, both still present) and
re-ran the five test files that cover this module after the edit (section 4) -- all still
green, same counts as the untouched baseline.

## 3. Cause (2)(ii) -- scenes 3/4/5 -- deferred, and why plainly

This round's own brief treats scene rosters for scenes 3/4/5 as "open one ticket per
scene," secondary to cause (1)/D7, skippable if time runs out. The live queue in this
repo (`COO-DECISION 20260903_2246` item 4, restated `2344` item (g)) actually scopes it as
real engineering: mine each scene's already-present `placements.tsv` with
`tools/pf_mine_scene_mob_roster.py` (same shape as scene 14's
`field_mob_hostile_bg0015.py`), register it in `field_mobs._SCENE_TABLE_MODULES`, one PR
per scene, full test suite each time. That is a materially bigger job than "file a
ticket," and this round's own assignment named cause (1)/D7 as the priority with this item
explicitly skippable. Given cause (1)/D7 needed verification rather than new code, there
was time left in the round, but starting a three-scene mining effort with its own
per-scene PR discipline felt like the wrong use of what verification time bought, versus
reporting the mismatch plainly and leaving it for a round that can give it the full
attention `2246`'s own rule ("scene ละ PR, ห้ามรวม") asks for. **Explicitly queued for
next round, not silently dropped.**

## 4. Tests run

Targeted, during development (after the `mob_ai_player_damage.py` comment edit):

```
pytest tests/test_lane_b_mob_ai_tick.py tests/test_mob_aggro.py \
       tests/test_mob_ai_control_dispatch.py tests/test_persistence_vitals.py \
       tests/test_mob_stat_fabrication_guard.py -q
=> 199 passed, 71 subtests passed
```

Final, once, after `git fetch origin main && git merge origin/main` (fast-forward,
`b6f74bc3` -> `3ab85f1e`, pulled in `server#686` from LANE-GM, no conflict):

```
pytest tests/ -q
=> (see this round's letter / final report for the exact tail; recorded verbatim there,
   not re-typed here to avoid two counts disagreeing if either is mistyped)
```

## 5. Files touched (pirate-force-server, branch `claude/magical-hawking-5pvte3`)

- `src/pirateforce_foundation/mob_ai_player_damage.py` -- comment-only update to the
  `MOB_AI_PLAYER_DAMAGE_WIRING` hold rationale and the order string itself (no keyword,
  no signature, no behavior changed). 1 file.

## 6. Files touched (pf_bridge, branch `claude/eloquent-noether-5pvte3`)

- `rounds/B_20260904_0014_5pvte3_the-damage-door-was-already-built-the-hold-still-holds.md`
  (this file)
- `notes_to_chief/20260904_0014_LANE-B-REPORT-COO-cause1-and-d7-already-paid-hold-confirmed-architecture-question-routed.md`

2 files. No `CLIENT_RE_QUEUE.md` edit survives -- drafted, found redundant against
`gm/attr_wire.FIELDS`, discarded before commit (section 2).

## 7. What only a human on the owner's screen can confirm

Everything above is static/headless. Nobody has watched a monster hit a player on a real
client this round, or any round before it in this chain -- `mob_ai_player_damage.py`
itself says so in its own NONCLAIMS, and this round did not change that. The DB write
this module performs, once wired, is still invisible until a frame ships with it
(COO's own `2050` reasoning, which is why it stays unwired).

-- LANE-B (COMBAT), round `5pvte3`
