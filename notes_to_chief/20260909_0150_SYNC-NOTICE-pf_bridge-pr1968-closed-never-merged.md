ADDRESSEE: LANE-B

# panyaasanee/pf_bridge #1968 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-09 01:50:12 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-B] round 1iqdti: claim
    branch  : claude/compassionate-johnson-1iqdti   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-08T15:33:03Z
    closed  : 2026-09-08T18:38:36Z
    link    : https://github.com/panyaasanee/pf_bridge/pull/1968

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **REAPED: stale claim >3h, no round file**
    
    Nothing has happened on `claude/compassionate-johnson-1iqdti` for 3h and the only file under `rounds/` is this round's own `*_claim.md` placeholder, so the round that opened this lock died before it pushed any work. Closing it releases the lane lock.
    
    The branch is kept, so nothing on it is lost. Authorised by PANYA-ORDER 20260906_1315 (`notes_to_chief/20260906_1315_KA1A-PANYA-ORDER-CHIEF-reaper-autoclose-stale-claims-and-superseded-prs.md`): this reaper closes stale round claims and author-declared supersedes only, never a code pull request waiting on the gate or on review.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
