# SYNC ALARM - 4 letter(s) nobody took and nobody answered

written by pf_git_sync.ps1 step [6b] at 2026-09-08 02:06:08 (machine local time)
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

    20260907_1332_LANE-K-NUMBERED-RE-298-GT-299.md
    20260907_1332_LANE-K-ROUND-du6wre.md
    20260907_1355_LANE-K-ADDENDUM-du6wre-my-do-not-look-line-was-false-re298-answer-is-in-the-repo.md
    20260907_1455_RE-289-CORRECTION-the-remaining-row-count-is-29-not-27.md

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
