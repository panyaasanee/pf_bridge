ADDRESSEE: LANE-DB

# panyaasanee/pf_bridge #1586 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-07 01:00:15 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-DB] round k7kqpn: claim
    branch  : claude/kind-lovelace-k7kqpn   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-06T16:34:33Z
    closed  : 2026-09-06T17:50:48Z
    link    : https://github.com/panyaasanee/pf_bridge/pull/1586

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    **This claim pull request carries the automerge marker but no `rounds/` file other than its own claim placeholder, 75 minutes after it was opened - closing it.**
    
    A claim pull request's body must not carry the marker until the round's real work (the round file, a CHIEF_CONTINUATION.md line, letters, a queue update) is pushed to this same branch (AGENTS.md section 2/3). This one has the marker but nothing beyond the claim file itself, well past the point a live round would still be working -- see pf_bridge#1079 for the incident this guard exists to catch.
    
    **The branch `claude/kind-lovelace-k7kqpn` is kept.** If the round that opened this is still alive somewhere, pushing its real work here will let it merge normally on the next event; otherwise the next round of this lane should treat this as a dead claim and start its own.

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
