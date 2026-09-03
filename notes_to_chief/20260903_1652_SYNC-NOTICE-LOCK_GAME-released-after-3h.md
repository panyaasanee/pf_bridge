ADDRESSEE: chief

# LOCK_GAME.txt was released automatically after 3 hours

written by pf_git_sync.ps1 step [5e] at 2026-09-03 16:52:06 (machine local time)

    flag  : LOCK_GAME.txt
    held  : about 3 hours, past the 3-hour bound
    check : no GameClient process and nothing listening on the server ports, so no live round was behind it.

## why this happened

    The holder of this flag never released it.  The usual cause is that this
    machine was switched off, slept, or had its console killed in the middle
    of the work.  A flag left HELD stops every later sync round, and nothing
    can clear it except the round that died, so it would have stayed stuck.

## what this step did NOT do

    It released the flag and nothing else.  Whatever the dead holder was in
    the middle of is still exactly where it was left - no commit, no merge,
    no cleanup, no judgement.  Someone should look at what that work was.
