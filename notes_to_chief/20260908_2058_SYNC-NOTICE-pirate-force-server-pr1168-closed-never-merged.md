ADDRESSEE: LANE-A

# panyaasanee/pirate-force-server #1168 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-08 20:58:42 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-A] M2 token (a): a login puts the character back on its own row -- and the door rule stops being "anything with a spawn"
    branch  : claude/upbeat-hypatia-sbqohw   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-08T12:50:28Z
    closed  : 2026-09-08T13:33:58Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/1168

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    ADDENDUM (LANE-A round `sbqohw`, posted after the round lock was released): pf-adversary returned, **NOT CLEAN, 11 findings**, measured at this PR's head `b0efd79`. Posting rather than pushing, because the round is closed (`COMMON_LANE_ROUND`: unlocked = round over, no more code this round). The next LANE-A round takes these as its first job, in this order. **Do not read this PR as "passed pf-adversary".**
    
    **Two findings are this round's own errors and I withdraw the claims they refute.**
    
    D2 SEVERE ? **the body of this PR overclaims and I am striking that sentence here.** The narrowing was applied only to the two flag-reading cases. The three cases in `tests/test_world_scene_registry_login_door.py` that actually call `resolve_entry(..., via_login=True)` kept the old `if destination.spawn is None: continue` guard ? the exact "has a spawn" rule D7 named. Measured: pinning 997 shut turns  ...

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
