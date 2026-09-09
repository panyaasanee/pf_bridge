# SYNC ALARM - 5 letter(s) nobody took and nobody answered

written by pf_git_sync.ps1 step [6b] at 2026-09-09 12:56:21 (machine local time)
Each letter is named ONCE, ever.  This alarm will not repeat for these.

## the test that was applied

    older than 12 h, newer than 7 days
    AND has no .CONSUMED.txt sibling
    AND is not present in notes_to_chief\consumed\
    AND no later letter quotes its yyyymmdd_hhmm stamp anywhere in its body

    The last clause is the important one.  Being unconsumed proves nothing:
    of 27 unconsumed letters older than a day on 2026-09-03, 20 had in fact
    been answered and only the source file was never marked.  A letter that
    nothing later quotes is one that demonstrably reached nobody.

## the letters

    20260908_2359_STANDING-A2-RESULT-GRAY-DEATH-REQUIRES-HP-ZERO-AND-THRESHOLD.md
    20260909_0009_STANDING-A3-RESULT-ERASE-ORDER-BEFORE-SAME-IDENTITY-RETURN.md
    20260909_0022_STANDING-A4-RESULT-MOB-ACTION-NUMBER-AND-PLAYER-HP-PATHS.md
    20260909_0034_STANDING-A5-RESULT-EA7D-SKIPS-WAIT-TASK-AND-LAND-CLOCK-CORRECTED.md
    20260909_0045_STANDING-A5-RESULT-CONTROLLER-FRAMES-AND-DISTANCE-TASKS.md

## what to do with this

    Read them, then either act or write one line saying why not.  Marking a
    letter consumed without reading it defeats the whole check.

## nonclaims

    - this does NOT say the letters are important, only that nothing has
      referred to them.  A routine notice nobody needed to quote lands here too.
    - the citation test is a substring match on the stamp.  A reply that
      answers a letter without quoting its stamp is a false positive.
    - this step has no idea WHY a letter was skipped, and never will: the
      mailbox records taking, not looking.
