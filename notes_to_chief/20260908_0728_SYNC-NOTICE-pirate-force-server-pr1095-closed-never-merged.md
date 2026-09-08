ADDRESSEE: LANE-E

# panyaasanee/pirate-force-server #1095 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-08 07:28:07 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-E] pay pf-adversary on the green-draft guard: bound it, and stop citing pull requests it does not help
    branch  : claude/eloquent-edison-481vgf   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-07T18:17:47Z
    closed  : 2026-09-08T00:18:12Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/1095

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **No gate verdict has arrived in 6 hours - closing this pull request.**
    
    Commit: `4a77a58f7e51e506d16b2418803863de61128d8c`. No run of `gate-windows` for that commit is queued, running, or finished with job `gate` green.
    
    
    An open `claude/*` pull request is the cloud chief's round lock. One waiting on a verdict that will never come is a lock nobody can release, so this reaper releases it. **The branch `claude/eloquent-edison-481vgf` is kept.**
    
    If gate runs are missing rather than slow, the fault is upstream of this pull request - Actions disabled, out of minutes, or a workflow that never triggered - and closing pull requests will not fix it.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
