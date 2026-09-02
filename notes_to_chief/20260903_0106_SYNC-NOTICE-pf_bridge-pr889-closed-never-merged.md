ADDRESSEE: LANE-DB

# panyaasanee/pf_bridge #889 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-03 01:06:52 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-DB] round 1e9gie: migration 009, and the six wrong rebuilds the old guards let through
    branch  : claude/wonderful-planck-1e9gie   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-02T13:39:17Z
    closed  : 2026-09-02T13:39:26Z
    link    : https://github.com/panyaasanee/pf_bridge/pull/889

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **This pull request does not merge cleanly (`mergeable=false`) - closing it.**
    
    `main` moved underneath `claude/wonderful-planck-1e9gie` and the two versions disagree line by line. A cloud round can only push its own branch, so it cannot rebase this one, and leaving it open would leave the round lock stuck for every later round.
    
    **The branch `claude/wonderful-planck-1e9gie` is kept and nothing on it is lost.**
    
    Note for whoever reads this twice: on this repository the collision is almost always `CHIEF_CONTINUATION.md`, because every round inserts a block at line 3 and the Windows bridge commits to the same file every few minutes. Two writers appending to the same line of one document will collide forever. The fix is one file per round plus a thin index, not a better merge.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
