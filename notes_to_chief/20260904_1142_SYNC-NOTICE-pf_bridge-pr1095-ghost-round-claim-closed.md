ADDRESSEE: 
cc: COO, chief

# pf_bridge #1095 was a GHOST round claim and step [5c] closed it

written by pf_git_sync.ps1 step [5c] at 2026-09-04 11:42:17 (machine local time), on the owner rule of 2026-09-03 (ka1-A letter 20260903_20xx)

    branch   : claude/e-round-2vfbtf   <- kept, nothing was deleted
    round id : 2vfbtf
    age      : 139 min on a bare claim tip
    why      : age 139 min; branch holds only 1 claim stub(s); finished-round file already on main: rounds/R335_2vfbtf_push-run-merge-race-audit-six-confirmed-plus-claim-guard-agents-wording-re232-dispatch-visibility.md

## what a ghost claim is
    a round pushed its claim, did its server half (or was taken over), and died before
    it pushed the bridge half.  The open claim then reads as a live lock to every later
    round of that lane (round h4d51r lost an hour to #988 this way).  All three of the
    owner conditions held - age, stub-only branch, round finished or replaced - so this
    step closed it and wrote the same reason on the PR.

## if this is wrong
    reopen the PR, say so in notes_to_chief, and ka1-A tightens the rule.  Nothing on the
    branch was touched.
