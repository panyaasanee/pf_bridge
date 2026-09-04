# LANE-A round 16uvmp -- 2026-09-04T19:43+07:00 to ~20:2x+07:00

claim #1194 (pf_bridge) · released #1156 on behalf (dead claim of round `tpuvll`,
4 h 48 m old, work already landed as server #753 -- COO-DECISION `20260904_1849`
item 2 ordered exactly this as the round's first task)

## NOW ข้อไหนที่รอบนี้ขยับ
M2. NOW.md 18:49 says the only blocker left is chief's (`msg_id` +
`runtime.py` call site) and that `GT-233` is "not your blocker, do not wait".
So this round took the backup queue -- and found that the M2 chain LANE-A owns
would have graded the attended `GT-233` trial as a false negative. The step
itself does not move (still no bytes out, still chief's call site); what moves
is that the trial can now answer its question instead of refusing itself.
A player will see nothing different from this PR alone; on the attended trial,
confirming the captain report now resolves to a real arrival for Prison Exile
(scene 2) and Spice Paradise (scene 3) where it resolved to
`ARRIVAL_REFUSED_HANDLE_NOT_ISSUED` before.

## ทำอะไร
1. **`#1156` ปลดล็อก** -- `PF-AUTOMERGE: v4` added to its body with the reason on
   the PR, GET-confirmed at 19:44+07. Not closed by hand (house rule on ghost
   claims).
2. **The defect.** `world_m2_provisioning_trial` writes the destination number
   (2/3) into the survey record's opaque u16 -- COO-DECISION `1345` item 1 --
   while `world_m2_survey_plan.confirm_resolution` recognised only its own
   allocated handle (`0xa099`/`0xa09a`). RE-227 item 3: the client copies the
   record's u16 back unchanged. So the `GT-233` confirm frame carries 2 or 3:
   not issued -> `arrival_order` refuses -> console prints `issued=no`, which the
   hook's own docstring reads as "the captain report popped WITHOUT a record from
   us" = a refutation of RE-227. A perfect attended run would have been graded as
   its own refutation, and the one attended slot spent.
   Both modules were fully tested and green; nothing crossed the two.
3. **The fix** (all inside LANE-A's write zone, `runtime.py`/`app.py` untouched):
   `plan.trial_survey_id()` is now the single decision about what the trial
   provisions and the trial module reads it; `confirm_resolution` resolves both
   values and reports `matched_as` (`handle`/`trial`) + `confidence`
   (`high`/`low`), handle first; the console appends `match=trial confidence=low`
   for the weak reading only (so every string other tests pin is unchanged, and
   no island/scene/trigger word is added -- RE-227 nonclaim 3).
4. **Tests that would have caught it**: every `survey_id` the trial sends resolves
   to its own destination; no two destinations can claim the same u16 (that one
   would teleport a confirming player to the wrong island); handle-over-trial
   precedence pinned against a synthetic collision; `arrival_order` composes the
   same order from either value; both still refuse when `MEASURED_XYZ` is empty.
5. **Stale docstrings struck through, not deleted** (house rule): `world_m2_arrival`
   said "refuses every handle today" (readiness is 2/2 since #753) and the
   enter-instance hook said `provisioned=0`.
6. **`GT-233` body**: added the console lines the attended grader must copy and
   how to read each (`match=trial confidence=low` = consistent, NOT proof), struck
   the `#753` half of its BLOCKED header (merged 18:42 `55c9a05`), and warned that
   a boot older than this round prints `issued=no` even when the mechanism works.
7. **Letters**: `1954` to chief (what the call site must correlate on, and that
   `world_m2_arrival.arrival_order(u16)` is ready to be called with the echo);
   `1955` to COO (this round's status + the one line `PANYA-DECISION 1857` needs:
   the scene-name half is already on main as `gm/scene_catalog.py`, no new RE
   ticket).

## measured, not claimed
`arrival_readiness()` = 2/2 · island 2 -> `wire_scene_id=2`,
`position=(2, 0, 26905.0, 21185.0, 1680.0)` · island 3 -> `wire_scene_id=3`,
`position=(3, 0, -21215.0, 16907.0, -830.0)` · `refusal=None` both.
Zero bytes leave the server: no send path exists yet, by design.

## pf-adversary (two passes, the ceiling -- no third call)
**Pass 1** (ordered with the work, on the finding + planned fix). It confirmed the
finding end to end and killed my headline: "a perfect run would be graded a
failure" is not what `GT-233` grades -- that ticket's criteria are the outbound
hex and the captain-report page, `issued=` appears in none of them, and COO
`1345` item 4 already says a failed trial is a measurement. Corrected in the
letters and in the queue rather than defended. It also swept for the collision I
was most afraid of (a u16 readable as two destinations -> wrong island) and found
none exists under either documented handle base or a fully widened plan, and it
built the wrong-island mutant: **it survives the pre-fix suite and dies on this
round's new test.** Three findings taken in commit two:
  - every fragment on the confirm line is CAPABILITY, not event -- five bytes from
    a client could make it read `issued=yes` on a build with no send path. Added
    `sent=`, tied to the composer's own no-importer guard by a test.
  - the `issued=no refutes RE-227` reading survived my own strike-through at the
    new number; corrected where it is written and in `GT-233`'s grading block.
  - `plan_is_for_scene()` had no caller: records provisioned to a player in scene
    17 with scene-126 coordinates could pop a report that -- because of THIS
    round's own fix -- now confirms into a real teleport. `encode_trial_records`
    takes `player_scene_id`, no default, `()` for any other scene.
**Pass 2** (on the repairs). Three parts closed in commit three: the same stale
refutation reading in two more places, and the new low-range test branched on
`SURVEY_HANDLE_BASE` so it stops forbidding the rollback its own comment cites.
🔴 **`ADVERSARY_PENDING` -- next LANE-A round takes these first, before claiming:**
  1. `sent=` is checked against this repository's source, not against a frame that
     left the process. Measured evasion: a call site that reaches the composer by
     `importlib.import_module` on a concatenated name sends 136 real bytes with
     every guard green. The honest fix is a counter incremented on the same path
     as the send, which cannot exist until chief's call site does -- so this is
     the first thing to do in the round after that lands, not now.
  2. `arrival_order` carries no confidence of its own: a `match=trial` echo
     composes a full deliverable teleport, with the caution living only on the
     console fragment. Whether the ORDER should refuse a low-confidence match (or
     require the caller to opt in) is a decision that can block M2's second island,
     so it goes to COO in the next round's letter rather than being taken here.
  3. the scene guard returns `()` silently where this codebase names its refusals
     (`ARRIVAL_REFUSED_*`, `BLOCKED_XYZ_UNMEASURED`), and accepts `126.0` while
     refusing `"126"`/`None` without a word.

## full suite
Ran **twice**, and the reason is the rule's own exception: the first run was on
commit two, and commit three (pass-2 repairs) changed a test and two docstrings,
so the pushed state had to be run again -- `git fetch origin main` first, merge
clean (main unchanged since 18:42), full run on the merged tree both times.
Result identical both times except the counts: **10,073 passed, 327 skipped,
19,410 subtests passed, 1 failed.**
🔴 **The one failure is not this round's and not this branch's**:
`tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_every_symbol_exemption_is_still_earned`
fails identically on **untouched `origin/main`** in a fresh worktree. It is the
documented interpreter divergence chief recorded in `f2d3df2`'s own commit
message: the exemption covers two f-string prefixes in `runtime.py`, which
tokenize as code on the gate's Python 3.14 (PEP 701) and as one STRING token on
this image's 3.11. Measured here on both interpreters:
`py3.13 -> ['columbus_quest3021_dispatch_refused_']` (exemption matches),
`py3.11 -> ['f"columbus_quest3021_dispatch_refused_{reason}"']` (nothing to match).
So the Windows gate should be green on it; nothing for this lane to fix, and
nothing to report as a main-is-red incident.

## push / PR status
- pirate-force-server: pushed to `claude/great-ride-16uvmp`, three commits. PR
  **#761** opened not-draft with `PF-AUTOMERGE: v4` in the body from the
  start, GET-confirmed.
- pf_bridge: this file + two letters + the `GT-233`/`1806` edits + the consumed
  stub land on `claude/eloquent-volta-16uvmp`, the same branch as claim PR
  **#1194**; the marker goes on #1194 only after that push, per the lock rule.
- `#1156` (the dead round's claim) released with a marker at 19:44+07 on COO's
  order, GET-confirmed. Not closed by hand.

## งานสำรอง (สาย A ถือไว้รอบถัดไป)
1. ISLAND responder id 2/3 edges not yet pinned: repeat contact inside one scene,
   and an id 2/3 frame arriving while `MEASURED_XYZ` is empty.
2. `world_m2_return_leg` -- capture the departed-from row before the crossing so
   the way back is not a new character's spawn (M2's second half, blocks on nobody).
3. `RE-234` -- narrow the id-3 / Seafood Cargo collision question further if
   `GT-233` results land first.
