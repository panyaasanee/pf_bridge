ADDRESSEE: LANE-GM

# panyaasanee/pirate-force-server #611 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-03 01:28:08 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-GM] The image checker names which rules it enforces, so install.bat can refuse an older copy of it
    branch  : claude/gracious-galileo-b8xrod   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-02T18:02:34Z
    closed  : 2026-09-02T18:19:40Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/611

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **Gate RED (job `gate` = `failure`) - closing this pull request.**
    
    Run: https://github.com/panyaasanee/pirate-force-server/actions/runs/33664875042  --  Commit: `32cbcdff063271eca6d2627b855612b269fbdf70`
    
    Closed automatically by `.github/workflows/merge-claude-pr.yml`, and the reason is the lock rather than the work. An open `claude/*` pull request is what stops two cloud rounds running at once; a red one left open would stop **every** later round, forever, and no later round could repair it, because a session may only push its own branch.
    
    **The branch `claude/gracious-galileo-b8xrod` is kept and nothing on it is lost.** Start again from `main` in a later round; if these commits are worth recovering, recover them from that branch by hand.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
