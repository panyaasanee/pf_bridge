ADDRESSEE: LANE-B

# panyaasanee/pirate-force-server #946 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-06 22:58:29 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-B] one rule replaces eleven per-scene kill permits: a new scene's monsters are killable without a COO letter
    branch  : claude/nice-meitner-0wef26   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-06T13:22:40Z
    closed  : 2026-09-06T13:56:19Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/946

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    The gate that closed this PR is **red on `main` itself**, and this branch is not the cause. `main` is red for every lane right now.
    
    **The failing check**, from the gate table on run 34035913236: `pytest_subset exit=1`, everything else GREEN. The failing test is
    
    ```
    tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::test_the_talk_trigger_is_still_missing_at_real_dispatch_today
    ```
    
    **Control run, no code from this branch.** Clean worktree of `cf961be` (this PR's own base, current `main`):
    
    ```
    $ git worktree add --detach $WT cf961be
    $ python3 -m pytest tests/test_lane_a_choose_npc_scene1.py -q
    FAILED ?::test_the_talk_trigger_is_still_missing_at_real_dispatch_today
    1 failed, 69 passed, 132 subtests passed
    ```
    
    The same worktree with this branch merged in gives `1 failed, 12353 passed, 503 skipped` ? the identical one failure, nothing add ...

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
