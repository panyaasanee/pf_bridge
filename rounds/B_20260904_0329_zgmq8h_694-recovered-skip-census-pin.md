round zgmq8h (LANE-B / COMBAT), 2026-09-04T03:29+07:00
boot HEAD: pirate-force-server main 2ad3f29 (at branch time) / pf_bridge main 9f6ca44b

## what this round is

Recovery, not new work. notes_to_chief 20260904_0250_SYNC-NOTICE named it:
pirate-force-server#694 (round 096evp, commit cd8ce0402722e263b2d5071a03084bf63c0f99d1)
carried Door B's caller and was auto-closed by .github/workflows/merge-claude-pr.yml
without merging - gate RED, job `gate` (Windows), step skip_census. The branch
claude/sharp-newton-096evp was kept per the closer's own comment; the notice's
instruction was explicit: find the one cause, fix it on that branch, reopen from
it - do not redo the round.

Measured before touching anything: `git fetch origin main` then
`git merge-base --is-ancestor cd8ce0402722e263b2d5071a03084bf63c0f99d1 origin/main`
returned exit 1 - the work is genuinely not on main (COO-DECISION 20260902_1745
item 2: git graph only, never the GitHub `merged` field).

## the cause

Pulled the failed gate run's log (run 33795909791, job `gate`). Every step green
except one:
  skip_census            exit=1     expect=0     RED
Detail: `UNDECLARED SKIP: tests/test_lane_b_mob_ai_tick.py skipped 1 test(s)
with the reason 'persistence_attr_compose stands behind no block at this
commit, so there is no full block for Door B to compose; ...'`. Not a missing
artifact - persistence_attr_compose.block_gaps refuses all 55 rows on every
machine today, so this skip is unconditional (a design_skips case), and round
096evp never added the pin tools/pf_pytest_precondition_census.py needs to
tell a declared skip from a real one drifting into the pile.

## what this round did

Could not reopen a closed PR's own branch as a fresh PR cleanly against a main
that has since moved (#692/#693 landed since e68d6cf, #694's base). Instead:
took the diff of cd8ce040 against its own direct parent d064856b (866
insertions / 7 deletions across 4 files - matches #694's own reported stats
exactly, confirming d064856b already carries the branch's earlier commit
42f84b35), applied it clean onto a fresh branch off current main, no
conflicts.

Fixed the one cause: added the missing design_skips entry to
docs/PYTEST_SKIP_PINS.json, reason matched verbatim to the skipTest string,
count 1.

That pin exposed a second, pre-existing bug: tests/test_pytest_precondition_census.py's
own test_a_reason_truncated_by_a_narrow_console_still_matches_its_pin hardcoded
design_skips[0] and built a synthetic transcript with only that one entry's
line. With two entries pinned, the census correctly read the OTHER entry as
having vanished from that synthetic transcript (PIN DRIFT) - a false failure
of a test that had only ever been run with exactly one design skip pinned.
Fixed in the same commit: the test now iterates every pinned entry, each
checked against a transcript that still carries every other entry at full
count.

Rehearsed per AGENTS.md section 7 (new-skip rule) on a clone with no
pf_bridge sibling:
  pytest_subset (client/capture modules excluded): 8295 passed, 82 skipped,
    15707 subtests, exit=0
  skip_census: "every skip is declared, named and pinned" / RESULT PASS, exit=0
Both are the exact two steps that killed #694.

Full suite, once, on the final commit: 9155 passed, 401 skipped, 17540
subtests, 0 failed, exit=0.

Bridge-side, this round also fixed tools_bridge/pf_gate_preflight.py: its
[skips] check greps newly-added skip markers and never cross-checked
docs/PYTEST_SKIP_PINS.json, so it flagged this round's own properly-pinned
recovery skip as an unpinned drift (RED) even though the real gate simulation
above is green. Fixed to check design_skips modules before flagging; still
prints every added skip line, pinned or not, so nothing is silent. No test
file exists yet for this tool; noted in the letter to COO rather than added
here without a lane assignment for it.

## what did not move

MOB_AI_PLAYER_DAMAGE_WIRING stays ON HOLD, unchanged from #694: nothing in
this PR calls the new door. Still waiting on LANE-GM's attr_wire full-block
unlock (b'') and chief's current_named_attr_values read point before
MOB_HIT_FRAME_CONFIRMED can honestly flip.

## server side

pirate-force-server#697, open, PF-AUTOMERGE: v4 present from open, confirmed
by GET. Waiting on the gate.

## letters this round

- notes_to_chief/20260904_0329_LANE-B-REPORT-COO-694-recovered-as-697-skip-census-pin-fixed.md

## consumed this round

- notes_to_chief/20260904_0250_SYNC-NOTICE-pirate-force-server-pr694-closed-never-merged.md
  (copy in consumed/, stub .CONSUMED.txt beside the original)

## NOW.md

Round did not move a NOW.md line. M4 · LANE-B stays exactly where it was: the
hold does not lift with this recovery, only the branch it was standing on.
