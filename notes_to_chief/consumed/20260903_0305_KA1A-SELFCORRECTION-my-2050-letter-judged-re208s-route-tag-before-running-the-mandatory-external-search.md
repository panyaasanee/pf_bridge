# SELF-CORRECTION: my 2050 letter judged RE-208's route tag before running the search the queue makes mandatory

- who: ka1-A (attended)
- when: 2026-09-03 ~03:05 (+07:00), approximate
- corrects: `notes_to_chief/20260902_2050_KA1A-TO-CHIEF-re208-route-tag-contradicts-its-own-pass-criteria-and-half-the-open-re-queue-is-misrouted.md`
- prompted by: actually doing the ticket, an hour later, at the owner's instruction

## What I got wrong

The 2050 letter concluded that `RE-208`'s `STATIC-ON-CLOUD` tag was wrong because the
ticket asks for work "in the client image" and **"the cloud has no image."**

The first half stands. The second half led me to a conclusion I had not earned:
that a cloud round therefore **could not answer the ticket**.

It could have. `CLIENT_RE_QUEUE.md` rule 4 says, in bold, that before disassembling
anything a worker must search `pf_bridge\external\` first, and that a hit converts the
ticket from "go extract" into "verify sha -> adversarial re-derive -> use". I ran that
search only when I sat down to do the work. It hit immediately:
`PF_GROUND_DROP_LIFETIME.tsv` and `PF_GROUND_DROP_PICKUP_CLOSURE.md/.tsv` already carry
the reconcile matrix at VA level, and **both are committed to git**. A cloud round with
no image at all could have answered `RE-208` from them, exactly as I just did.

So I judged a routing tag while skipping the project's own mandatory first step for
judging what a ticket needs. Same failure family as my `20260902_0050` letter earlier
that day: a story that fit the evidence I had, published before I had looked at the
evidence I was required to look at.

## What still stands, and what does not

- **STANDS:** RE-208's header and its pass criteria contradict each other **as written**.
  The criteria say "ในภาพไคลเอนต์" and demand a VA; nothing in them mentions that the
  answer is already delivered in `external/`. A worker reading the ticket top to bottom is
  told to open the image.
- **STANDS:** `RE-169` carried no route tag at all when I looked, which is the `[B]`
  failure the lint tool exists to catch. (It has since been closed.)
- **STANDS:** `RE-138`'s tag is correct; I verified its body.
- **WITHDRAWN:** "a cloud worker cannot do RE-208, therefore the tag misroutes the work."
  Wrong. The tag may well have been right, and the ticket text is what is out of date.
- **CHANGED, and this is the useful part:** the defect is no longer "wrong tag". It is
  that **a ticket can demand image work in its pass criteria while its answer already sits
  committed in `external/`, and nothing reconciles the two.** RE-208's own checklist rows
  `ค้นใน pf_bridge\external\ แล้ว: (สาย RE กรอก)` sat empty from 09:5x yesterday until
  03:00 today -- the rule was in the ticket, unfilled, the whole time.

## The lint proposal from the 2050 letter should change with it

I asked for a `[C] ROUTE CONTRADICTS BODY` check that flags a `STATIC-ON-CLOUD` ticket
whose body mentions the image. **That check would have fired on RE-208 and it would have
been wrong.** Please do not build it as specified.

What would have actually helped, and what I would ask for instead:

**`[C] MANDATORY SEARCH FIELD UNFILLED`** -- flag any OPEN ticket whose
`ค้นใน pf_bridge\external\ แล้ว:` or `ค้น gamedata แล้ว:` row is still a
`(สาย RE กรอก)` placeholder. That is a rule the queue already imposes on every ticket,
it is purely textual, it has no judgement in it, and on RE-208 it would have pointed at
the real problem -- nobody had run the search -- instead of at a tag that may have been
fine.

## NONCLAIMS

- I still do not know whether RE-208's tag was typed deliberately or by habit. I am no
  longer claiming it was wrong; I am claiming I could not tell, and said so too firmly.
- I have not re-audited the other open tickets against this corrected reading.
- The RE-208 result letter filed at 0300 today is unaffected by this correction: it does
  not depend on the tag being right or wrong.
