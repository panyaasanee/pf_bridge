ADDRESSEE: LANE-B

# panyaasanee/pirate-force-server #936 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-06 18:28:27 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-B] give the sea a roster: ocean hostility reading, scene 126's two creatures, and a named "shipped but not killable" state
    branch  : claude/nice-meitner-mf71tm   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-06T10:18:18Z
    closed  : 2026-09-06T10:45:48Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/936

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **Gate RED (job `gate` = `failure`) - closing this pull request.**
    
    Run: https://github.com/panyaasanee/pirate-force-server/actions/runs/34027048384  --  Commit: `3c2f24c3c97cc2d3dc98a5916c2ae078e0f90c73`
    
    Closed automatically by `.github/workflows/merge-claude-pr.yml`, and the reason is the lock rather than the work. An open `claude/*` pull request is what stops two cloud rounds running at once; a red one left open would stop **every** later round, forever, and no later round could repair it, because a session may only push its own branch.
    
    **The branch `claude/nice-meitner-mf71tm` is kept and nothing on it is lost.** Start again from `main` in a later round; if these commits are worth recovering, recover them from that branch by hand.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
