round 20udga
start 2026-09-07T00:16+07:00 (claim `pf_bridge#1591` -- no marker until round ends)

LANE-A -- first job per round `eknq8d`'s own instruction and the
COMMON_LANE_ROUND standing rule: pf-adversary's result against merged
`pirate-force-server#957`, posted as a PR comment after `eknq8d` released
its lock. Thirteen defects (D1-D13). This round works through them.

## 1. รอบนี้ขยับ NOW/M ข้อไหน

- **ไม่ขยับ M2** (0x1FB2 trigger 2/3): NOW.md's current LANE-A line
  (`#957 merge OK -> #951 0x1FB2 -> ...`) names this as the next job, but
  round `eknq8d`'s own round file said the adversary result on `#957` is
  the FIRST job of the next LANE-A round, "ห้ามข้าม" -- and it arrived
  with 13 defects, not zero. This round pays that debt instead. `#951`
  stays open, unmerged, exactly as `eknq8d` left it. No guessed frames
  sent (`1955` respected).
- **ขยับ**: quality debt on the merged `#957` change is retired -- see
  section 2. This is not a NOW.md/M-numbered line item, but it is the
  thing standing between `#957`'s tests and being trustworthy evidence for
  the M2/step-3 attended ticket that will eventually cite them.

## 2. ทำอะไร (`pirate-force-server#963` -- 4 files, open, not draft, has marker)

Fixed, in the severity order pf-adversary gave them:

- **D1 (HIGH)**: struck the two now-PAID "(LOST)" cells in the module
  docstring's old cost table (they were paid by `#957` itself but never
  struck), and the line ~950 sentence that still cited them as "why the
  gate stays shut."
- **D2 (HIGH)**: the "pins all three rows" claim sat over a FOUR-row
  table with two untested rows. Added a real dispatch test for P30 (a
  genuine gain over the frozen loop -- verified non-trivial: the ordinary
  boot's census does arm placement 30, pf-adversary confirmed by
  instrumenting a live boot). P0 is qualified in prose instead of given a
  test (see D8) -- a dispatch test on the ordinary boot this file drives
  would pass trivially, since P0 only differs from main on a boot this
  harness does not build.
- **D3 (HIGH)**: the shop-once test clicked the SAME placement twice, so
  a mutant that unconditionally spends the latch on ANY click survived
  (pf-adversary confirmed: the OLD test passes against that mutant, the
  NEW one correctly fails). Added a townsperson click first, asserting
  the latch unspent before the shop trigger is ever clicked.
- **D4/D5 (HIGH)**: letter `20260906_2315` asked chief to rename the test
  class because the class name is referenced by string in two files
  outside this lane's zone. False premise, pf-adversary measured:
  `grade_subset` (`tests/test_foundation_legacy_seam.py`) digests
  `(id, status, required, evidence_refs, test_refs,
  next_missing_behavior)` and excludes `notes` -- the field the name
  lives in in both files. Renamed the class to
  `TheRegisteredResponderMeasuresTheTalkTriggerAtRealDispatchTests`,
  fixed the note in `docs/FUNCTIONAL_COVERAGE.json` and the now-false
  comment in `tests/test_foundation_legacy_seam.py` in the same commit.
  Digest recomputed after the edit by both this round and pf-adversary
  independently: unchanged,
  `94CF4E4A0354D327FC63E61D757BFF16A77A3357CE8769525276C9786754E9FE`.
  Letter `2315` withdrawn this round (see section 4).
- **D6 (MED)**: "appear at no call site in runtime.py" was refuted by a
  plain grep (6 and 39 hits respectively). Reworded to the true claim:
  neither appears as this module's `respond()` keyword.
- **D7 (MED)**: re-derived six of the eight rotted `runtime.py` line-pin
  citations (pf-adversary independently re-verified all six land where
  claimed). The remaining two (`7544-7568`, `8256-8265`) could not be
  confidently re-derived in this round's time budget -- pf-adversary
  confirmed they really have rotted to unrelated comments -- so they are
  marked as needing a grep instead of left as a wrong number or guessed
  at.
- **D8 (MED-HIGH)**: qualified the P0 "(nothing -- the same)" row as true
  only on an ordinary boot, cross-referenced to the bypass-boot
  regression (silence vs. quest conversation) the module's own reason 5
  already measures.
- **D9 (LOW-MED)**: pinned wire order at the flagship P3 placement with
  `assertEqual(labels, [...])` (pf-adversary confirmed: a mutant that
  prepends instead of appends `extra_actions` at the real call site slips
  past the old membership+length assertions and is caught by this one).
- **D13 (MED)**: `VENDOR_AND_MISSION_LATCH_WIRING` calls its vendor
  keyword and LANE B's `trade_session_membership` store-session stamp
  "one edit"; grep at HEAD shows the stamp never landed
  (`trade_session_membership|build_session` = 0 hits in `runtime.py`,
  pf-adversary independently reran the same grep). Corrected the module
  docstring's step 2, which had struck the item as fully shipped -- it is
  half shipped. This is a real gate-readiness finding: flipping the flag
  today would open store 5 on screen with no session stamped, which per
  the wiring constant's own words answers every buy with
  `trade_cmd_no_active_session_no_reply`.

**D10-D12 deferred (LOW, byte-count/annotation cosmetics)** -- not fixed
this round, listed in section 6 for whoever picks them up.

**Self-check, not part of the original 13**: pf-adversary reviewed this
round's own diff before push and found one thing wrong in it -- the D9
fix's own comment cited a runtime.py line that has never existed
(`actions[:0] = ...`) instead of the real one
(`actions.extend(...)`, line 10359). Fixed before push; the comment now
names the real line.

## 3. หลักฐาน / เกต

- `pf_gate_preflight.py --repo <server>`: **PREFLIGHT PASS**
- Full suite after `git merge origin/main` (already up to date, `be06164`
  in HEAD): **12480 passed, 373 skipped, 26243 subtests, 0 failed**
  (605.94s) -- one more pass than round `eknq8d`'s own baseline (12479),
  matching the one new test this round adds.
- pf-adversary ran on this round's own diff **before push**, not pending:
  independently recomputed the digest, reran every grep this round cites,
  instrumented a live boot to confirm the P30 test is non-trivial, and
  ran its own mutation probes against D3/D9's new assertions (old test
  vs. mutant: green; new test vs. same mutant: red, for both). Full
  report kept in this round's own agent transcript, not re-quoted here in
  full -- summary above under each D-item plus the self-check paragraph.

## 4. จดหมายที่เขียนรอบนี้

- `20260907_0005_LANE-A-TO-CHIEF-withdraw-2315-rename-premise-was-false.md`
  -- withdraws `20260906_2315`; nothing left for chief to do on it.

## 5. บริโภคผลใบที่ถึงสายนี้

- pf-adversary's comment on `pirate-force-server#957`
  (`#957#issuecomment-5560340619`) -- **used in full**, all 13 defects
  addressed or explicitly deferred (section 2).
- `20260906_2318_LANE-A-CORE-REQUEST-scene1-three-decline-keywords-last-gate.md`
  -- still open, still chief's (the three `runtime.py` decline-keyword
  call sites this round did not touch). Not superseded by anything this
  round found.

## 6. รอบหน้าทำอะไร (เรียงตามลำดับ)

1. **`#963`'s own pf-adversary pass already came back this round** (see
   section 3) -- no pending result to pick up for `#963` itself.
2. **M2**: back to NOW.md's line -- `#951` (0x1FB2 table) still open,
   unmerged. Continue from UI letter `2124`'s candidate (`TriggerResult`,
   fixed `n_ID` key), artifacts already committed only. No guessed frames,
   no `AddSurveyData` trial.
3. If `CORE-REQUEST 2318`'s three decline-keyword lines land in
   `runtime.py`: draft the step-3 attended ticket (townsperson / shop
   keeper / P30 with a weapon bound) as `*-TO-K-gt-body-*`, THEN ask to
   flip `lane_a_choose_npc_scene1.production_allowed`. Not before --
   `D13` above is a real reason it still must not flip even once the
   three keywords land.
4. **D10/D11/D12** (LOW, deferred this round): D10 -- restore the dropped
   byte counts in the new cost table (P1/P91/P3 are byte-identical to the
   frozen builder's, the stronger true claim). D11 -- the P91
   parenthetical annotates only the right-hand column though main
   behaves the same; balance it. D12 --
   `TheGateStaysClosedForAMeasuredReasonTests`' own docstring calls itself
   "the class that tells you when it is done" and is now green and
   silent; say what "done" would look like next.
5. Not yet landed: still tally to chief on `2318`. If still nothing after
   another round or two, escalate per COMMON_LANE_ROUND's ask-COO path
   rather than opening a fourth letter on the same three lines.

SCOREBOARD: COMING | nothing changes for a player this round (`production_allowed` for `lane_a_choose_npc_scene1` stays False, M2 did not move) -- this round paid quality debt on already-merged `#957` so its tests are trustworthy evidence for the eventual step-3 attended ticket, and found a real gate-readiness bug (D13: the shop-open latch wiring is only half shipped) before the flag could ever flip on it | pirate-force-server#963 (open, marker set, pending gate/merge; no runtime.py touch, no wire change)
