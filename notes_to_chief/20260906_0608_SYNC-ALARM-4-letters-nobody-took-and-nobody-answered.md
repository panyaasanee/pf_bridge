# SYNC ALARM - 4 letter(s) nobody took and nobody answered

written by pf_git_sync.ps1 step [6b] at 2026-09-06 06:08:07 (machine local time)
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

    20260905_1638_LANE-B-TO-CHIEF-RE-ticket-body-two-frames-one-burst-disagree-about-the-ground-list.md
    20260905_1751_COO-DECISION-chief1810-split-52-three-piles-wiring-pr-before-0x4543-827-comment-suffices-LANE-E.md
    20260905_1752_COO-DECISION-chief1830-three-frame-contract-owner-lane-b-reference-is-this-letter-chief-fixes-34-pins-d7-d9-ruled-LANE-E.md
    20260905_1810_CHIEF-R356-TO-COO-wired-v2-measured-15-of-67-plus-0249-item-2-is-17-sites-not-7.md

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
