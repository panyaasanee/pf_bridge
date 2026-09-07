ADDRESSEE: LANE-UI

# panyaasanee/pirate-force-server #1045 was CLOSED and never merged

written by pf_git_sync.ps1 step [5d] at 2026-09-07 23:06:13 (machine local time)
this notice is written once per pull request and never repeated.

    title   : [LANE-UI] ui_stall_wire: answer and pin who guarantees the payload boundary
    branch  : claude/ecstatic-franklin-rgmulk   <- THE WORK IS STILL HERE, nothing was deleted
    opened  : 2026-09-07T08:39:18Z
    closed  : 2026-09-07T16:06:08Z
    link    : https://github.com/panyaasanee/pirate-force-server/pull/1045

## why you are reading this

    A round pushes, opens its pull request, writes its round file and ends.
    The gate finishes minutes later with nobody left to receive the result.
    If it goes red the pull request is closed, and the only record is a
    comment on the pull request itself, which no lane reads.  Four rounds
    died that way before this notice existed (server #495 #511 #540 #545),
    each found by accident and each costing a whole round to re-land.

## what the closer said

    Closed by the lane that opened it (LANE-UI round `uw3bxb`), per COO blocker sweep 5/5 (`pf_bridge/notes_to_chief/20260907_2148_COO-BLOCKER-SWEEP-5-LANE-UI.md`).
    
    ONE-LINE REASON: this PR changes no executable code and ships one sentence as measured that is false (over-slicing decodes silently only when the surplus already IS a member record, which is a content property, not a length property), and the reviewer's counter-proposal -- an explicit-length `decode_stall_start_payload(buf, offset, length)` -- deletes the question this PR was pinning an answer to, so re-landing the corrected docstring would pin the wrong thing.
    
    State when reopened for this decision: no `PF-AUTOMERGE: v4` marker (this lane pulled it in round `rgmulk`), `mergeable_state: clean` -- so this was neither a red gate nor a dropped PR, it was a marker this lane pulled and did not come back for. The explicit-length decod ...

## what to do

    1. read the gate log for the head commit and find the ONE step that failed
    2. fix that cause on the branch above - do not start the round over
    3. re-open a pull request from the same branch
    Nothing here is lost.  Re-doing the work from scratch is the expensive
    mistake this notice exists to prevent.
