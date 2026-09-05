ADDRESSEE: LANE-E

# panyaasanee/pirate-force-server #859 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-05 23:20:11 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-E] gate-windows: install lupa==2.8 so LANE-Q can drop its skip pins
    branch  : claude/upbeat-hamilton-supz66   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-05T16:13:30Z
    closed  : 2026-09-05T16:14:39Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/859

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **Gate RED (job `gate` = `failure`) - closing this pull request.**
    
    Run: https://github.com/panyaasanee/pirate-force-server/actions/runs/33977194920  --  Commit: `a19b90849fdd0b98f65a1fcdc9fb98fa783ad26b`
    
    Closed automatically by `.github/workflows/merge-claude-pr.yml`, and the reason is the lock rather than the work. An open `claude/*` pull request is what stops two cloud rounds running at once; a red one left open would stop **every** later round, forever, and no later round could repair it, because a session may only push its own branch.
    
    **The branch `claude/upbeat-hamilton-supz66` is kept and nothing on it is lost.** Start again from `main` in a later round; if these commits are worth recovering, recover them from that branch by hand.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
