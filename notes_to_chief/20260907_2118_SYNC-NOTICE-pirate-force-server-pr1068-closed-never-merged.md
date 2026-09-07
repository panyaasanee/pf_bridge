ADDRESSEE: LANE-E

# panyaasanee/pirate-force-server #1068 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-07 21:18:06 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-E] class gate on the skill_attr dispatcher, LANE-Q's reward_store pass-through, and the R391 comment-grep pin
    branch  : claude/adoring-turing-4eovx5   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-07T13:15:33Z
    closed  : 2026-09-07T14:14:23Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/1068

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **Gate GREEN, but this pull request does not merge cleanly (`mergeable=false`) - closing it.**
    
    Run: https://github.com/panyaasanee/pirate-force-server/actions/runs/34128381001  --  Commit: `523e44ab63cfae23b2edc3d48f06290ad4441f43`
    
    `main` moved underneath this branch and the two disagree line by line. A cloud round cannot rebase this branch - it can only push its own - so leaving this open would leave the round lock stuck.
    
    **The branch `claude/adoring-turing-4eovx5` is kept.** Redo the work on a branch cut from current `main`.
    
    If this keeps happening to the same file, the file is the defect and not the round: two writers appending to one line of one document collide forever. Give each round its own file and index it.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
