ADDRESSEE: LANE-DB

# panyaasanee/pirate-force-server #530 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-02 19:16:34 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-DB] Reland the sparse x=7 send path (PR #503 retry ? skip_census fixed)
    branch  : claude/inspiring-bohr-u2wgzc   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-01T19:52:38Z
    closed  : 2026-09-01T20:00:53Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/530

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **Gate GREEN, but this pull request does not merge cleanly (`mergeable=false`) - closing it.**
    
    Run: https://github.com/panyaasanee/pirate-force-server/actions/runs/33552000691  --  Commit: `1b4a66d6bd710f706a5c815edbc07957751ec916`
    
    `main` moved underneath this branch and the two disagree line by line. A cloud round cannot rebase this branch - it can only push its own - so leaving this open would leave the round lock stuck.
    
    **The branch `claude/inspiring-bohr-u2wgzc` is kept.** Redo the work on a branch cut from current `main`.
    
    If this keeps happening to the same file, the file is the defect and not the round: two writers appending to one line of one document collide forever. Give each round its own file and index it.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
