# LANE-A round `czoo9t`

2026-08-30T21:4x+07:00 - 2026-08-30T22:0x+07:00 (+07:00 via `TZ=Asia/Bangkok date`).

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ยังไม่เห็นอะไรต่างบนจอ - แต่ตอนนี้คอนโซลบอกตรง ๆ ทุกครั้งที่มี
คนขึ้นเรือ Columbus ว่า Port Royal ทั้งเมือง 115 คนตามออกทะเลไปด้วย และเฟรมที่ไล่พวกเขากลับ
(clear 27 ไบต์) ประกอบเสร็จรออยู่แล้ว เหลือแค่ `runtime.py` คิวมัน

## 0. Section A - why this round is not the cherry-pick round

PR #332 was closed by the gate-reaper without merging (gate red: 20 GM-lane tests). The
recovery order in `notes_to_chief/20260830_2112_LANE-A-BLOCKER-...md` is: wait for Lane GM's
fixture fix on main, THEN cherry-pick `b5ca2b68716b1786244448c5ee4651f5bb8e4905`. Re-checked
this round from a fresh `git fetch origin main`, not from the previous round's word:

* `origin/main` tip is still `aa5ba78` (merge of PR #330) - unmoved.
* `git log origin/main -- tests/test_gm_login_scene_sanctioned_bypass_wiring.py` still ends at
  `95d322f` (the original CORE-REQUEST-GM-038 wiring, which predates the blocker).
  **Lane GM's fixture fix has not landed.**
* `git ls-remote origin refs/heads/claude/sleepy-ride-kpz6vo` -> `b5ca2b68...` still on origin,
  and `git show --stat` on it confirms the 6 files are intact. Nothing is at risk of being lost.

So the cherry-pick would reproduce the same red gate. Deferred a second time, which under the
project's own rule makes this a "second empty round on lane A's own front" - and that rule says
pick real work instead of standing idle. That is what section 2 is.

**A number that makes the deferral a decision rather than caution:** this round's full suite on
HEAD *without* row 126 is **5568 passed / 327 skipped / 0 failed**. PR #332's own commit message
records **20 failed / 5514 passed** *with* row 126. The 20 are caused by that row, not by the
environment.

## 1. Section B - mailbox

The addendum named six carried-over tickets by number: `RE-095`, `RE-096`, `RE-097`, `RE-100`,
`RE-102`, `RE-103`. **All six already carry a `.CONSUMED.txt` stub from an earlier round**, in
`archive/notes_to_chief_2026-08/` (plus copies under that directory's own `consumed/`). Found
with `find` across the whole tree rather than from memory. Nothing was consumed twice and no
stub was fabricated to make a list look complete.

A full scan of `notes_to_chief/*.md` for `ADDRESSEE: LANE-A` returned 22 files with no stub.
Every one of them is a letter **lane A wrote outbound** (ASK-COO / STATUS / BLOCKER / RESULT) -
those are consumed by chief/COO, not by their author. The only unconsumed **inbound** decision
letters are `20260830_2048_COO-DECISION-warp-cross-scene-waits-for-gt106-r2.md` (addressed to
chief and lane GM) and the `FROM_CHIEF_R223..R248_TO_ATTENDED_*` series (addressed to the
attended tester). Neither set is lane A's to consume.

**Mailbox result: nothing outstanding for this lane.** Said plainly, per the order.

## 2. Section F - the M2 build this round did instead

### 2.1 The defect, found by reading the one path a player can actually walk

`world_travel_gate` is debug-only and OFF by default by owner ruling (`COO RULING 20260826`).
So there is exactly ONE scene change a player can make happen on a default boot: talk to
Columbus, take option one (row 3021), arrive in scene 17.

That path sends a `TeleportVital` **and nothing else** (`runtime.py:5028-5044`).
`world_population_handoff.handoff_on_crossing` - the seam this lane built for exactly this
moment - has ONE call site in `runtime.py`, and it is on the disabled travel-gate path
(`runtime.py:7146`). The Columbus branch never calls it.

`make_runtime_remote_actors` has replace semantics and nothing replaces the collection here, so
**the login census is still on the client after the transition**. The census this tree composes
is 115 actors (`world_population.census_count_for_dispatch() -> (115, 'full_census')`,
re-derived this round with a live call, not quoted from a letter).

Two independent sources had already seen half of this and neither closed it:

1. This lane's own `WORLD_POP_STOWAWAYS` line, printing at this exact moment since round
   `2pdf6j` - a report naming who is still held, with nothing that acts on it.
2. `RE-162` Job 4, stated as a negative finding in its own words: *"the Columbus in-session
   crossing sends the teleport frame alone ... nothing in this clone's committed source sends
   one."*

### 2.2 What was built - the existing encoder, fed the input it was never fed

`src/pirateforce_foundation/world_m2_crossing_handoff.py` (new, 226 lines). It reads the
arrival scene and anchor out of the `SceneEntry` the dispatch already produces and hands them to
`handoff_on_crossing`. **No second selector, no second encoder, no re-derived byte.** Measured
for scene 17 today: `kind=clear`, `pc=17B`, `frame=27B`, `slot=before_teleport`,
`membership_reset.clears_everything = True`, and `frame == legacy.frame_pc(pc)` against the real
frozen `current/pf_login_game_server_v141.py` (pinned in the test, not asserted in prose).

`columbus_quest_dispatch.dispatch_columbus_quest3021` now emits, on the default path, with no
flag and no scenario:

```
WORLD_M2_CROSSING_HANDOFF scene=17 kind=clear held=115 composed=YES dispatched=NO
  pc=17B frame=27B slot=before_teleport
  reason=scene_17_left_empty_on_purpose_sea_scene_no_cline_type_mob_set_placements_unresolvable_gt078
```

`dispatched=NO` is a fact about the tree, not a placeholder: nothing queues these bytes. It is a
parameter (`crossing_handoff_dispatched=`, defaulting to the truth) so the edit that starts
queueing them is the same edit that stops the console claiming otherwise. Both states are driven
by tests.

### 2.3 Why the sea cannot be populated, measured rather than assumed

Before proposing a roster for scene 17, this round measured whether one was possible:

* `gamedata/scene/Bg1001/Bg1001.placements.tsv` -> 8 placements, and **all 8** are `Mob_set_N`
  rows (sets 1-6). Reading a Mob-Set number as an actor identity is the reading `GT-078`
  REJECTED - the same wall scene 278 sits behind.
* `CONSTDATA_TH__SCENE_NAME.tsv` row 17 -> `n_CLINE_TYPE = 4294967295` (0xFFFFFFFF, "none").
  The Mob-Set -> CLINE -> MOBS crosswalk that resolves other scenes has **no column to resolve
  through here**. It is not that nobody ran it; the key is absent.
* Checked, not assumed: **all seven sea scenes** (17-23, `Bg1001`-`Bg1007`) carry the same
  `4294967295`.

**So a composer for the sea would be an invented cast, and this lane will not ship one.** Scene
17 was added to `SCENES_INTENTIONALLY_UNPOPULATED` with that measurement written into the table,
so a future reader can tell "we looked and said no" from "nobody has looked" - which is the
lesson that table exists to carry. Its reason string changed from
`scene_17_has_no_population_table` (the string a scene nobody ever considered prints) to
`scene_17_left_empty_on_purpose_sea_scene_no_cline_type_mob_set_placements_unresolvable_gt078`.

Scene 17 is the **first row in that table with a production reader** - 278 and 997 are scenes no
crossing reaches.

## 3. Adversary pass (self-conducted; no subagent tool available in this environment)

Reasoned adversarially against the diff before committing. Four findings, all acted on:

* **D1 - a mutant survived the anchor test.** `test_the_anchor_is_the_position_...` originally
  compared against the real entry, where `position`, `stored` and `teleport_fields` all agree for
  scene 17. A reading of `stored` instead of `position` would have passed it. Rewritten to drive
  the three APART on purpose (`stored` made to name Port Royal, `teleport_fields` scene 99) so
  the test pins the READ and not a coincidence.
* **D2 - a parameter with no reader.** `crossing_handoff` mirrored the seam's `actor_count`.
  The seam reads it only on its CENSUS branch, and the only scene reachable here answers CLEAR,
  so no test in this tree could give it meaning - the flag-with-no-reader shape
  `PANYA-DIRECTIVE 20260829_2222` item 7 bans, one level down. **Removed**, with the reason and
  the condition for adding it back written into the function.
* **D3 - two seam call sites in one file.** The first draft called `handoff_on_crossing` once per
  branch. `tests/test_world_population_bg0015.py` caught it: that census allows one call per
  blessed file, because a second inside an already-blessed file is the double-populator shape
  `COO-DECISION 20260829_2245` bans. **Collapsed to a single call** rather than widening the
  rule; the census's expected list was then extended to three files with the argument written
  into the test, as that test's own comment demands.
* **D4 - composing bytes that are thrown away.** Composing a handoff in order to print it costs
  a discarded frame. For a 27-byte clear that is nothing; for a scene with a roster it would not
  be. Not reachable today (the dispatch's destination is the constant 17, and 17 answers CLEAR),
  **disclosed in the module docstring** rather than left to be discovered.

One more, caught by the gate rather than by reasoning:

* **D5 - a word tripwire.** `QuestAndShopStateGuardTests` scans every `src/pirateforce_foundation/*.py`
  for the whole word "q-u-e-s-t" against a deliberately short allowlist. Two files tripped it on
  **prose only**. Neither implements that behaviour, so the prose was reworded to name the
  dispatch module and the row number - more precise anyway - rather than widening a guard that is
  doing its job. **Disclosed in both files' own text** so no reader discovers it by breaking it.

## 4. Gate, measured

| check | result |
|---|---|
| `python3 -m pytest tests -q` | **5568 passed, 327 skipped, 0 failed**, 9716 subtests (124s) |
| `python3 tools/verify_hypothesis_ledger.py` | `HYPOTHESIS_LEDGER PASS entries=47`, rc=0 |
| `python3 tools/verify_functional_coverage.py` | rc=0, 8 open domains (unchanged by this round) |
| `git diff -- current/pf_login_game_server_v141.py` | empty - frozen file untouched |
| `git diff --check` | silent |
| `git check-ignore` on both new paths | not ignored (`!/src/**`, `!/tests/**`) |
| cp874 scan, my six files | all pure 7-bit ASCII, all `.encode("cp874")` clean |
| canonical DB | not present in this checkout; nothing read or written |

Two new tripwires were updated deliberately and both are argued in the test file itself, not
silently re-pinned: the bg0015 seam-call-site census (2.3 / D3) and
`test_columbus_quest_dispatch`'s negative-index line order (moved by one for the third time,
under the same rule and with the same refusal to weaken it to `assertIn`).

## 5. Out of scope - reported, not fixed

`tools/pf_vital_name_thunk_static.py` and `tools/pf_vital_thunk_census_static.py` contain
`U+1F534` (red-circle emoji), which cp874 cannot map, inside the `src/ tools/ current/` scope
the tripwire is declared to cover. The Thai characters in those files are **fine** (cp874 is
Thai); the emoji are not. Four further files - `.tsv` data under `src/pirateforce_foundation/gm/data/` -
carry CJK/fullwidth for the same reason. The suite is green because the in-tree tripwires scan
only `*.py` under `src/` and the `gm/` subtree, never `tools/`. That is a gap between the
declared scope and the enforced scope. Not this lane's files and not this lane's round.

## 6. Files touched (6)

| repo | path | what |
|---|---|---|
| pirate-force-server | `src/pirateforce_foundation/world_m2_crossing_handoff.py` | NEW - composes the crossing's handoff |
| pirate-force-server | `src/pirateforce_foundation/columbus_quest_dispatch.py` | +1 import, +1 emit, +1 kwarg |
| pirate-force-server | `src/pirateforce_foundation/world_population_handoff.py` | scene 17 -> `SCENES_INTENTIONALLY_UNPOPULATED`, with the measurement |
| pirate-force-server | `tests/test_world_m2_crossing_handoff.py` | NEW - 23 tests |
| pirate-force-server | `tests/test_columbus_quest_dispatch.py` | line-order pin moved by one |
| pirate-force-server | `tests/test_world_population_bg0015.py` | seam call-site census: third file, argued |

`runtime.py` and `app.py`: **not touched.** See the CORE-REQUEST letter.

## 7. Not proven by this round

No human has watched a client render scene 17 at all - `GT-106` is PENDING and `RE-162` marks
the in-session transition client-observable UNPROVEN. "The sea is empty once this is queued" is
what the bytes say, not what anyone has seen. Whether the client actually drops the old scene's
actors when a clear lands mid-session is a separate observable from `GT-106-R2`'s question, and
the CORE-REQUEST letter asks chief to open a ticket for it (GT tickets are chief's to open).

**This round sets no ticket status, writes no PASS, and declares no milestone reached.**
