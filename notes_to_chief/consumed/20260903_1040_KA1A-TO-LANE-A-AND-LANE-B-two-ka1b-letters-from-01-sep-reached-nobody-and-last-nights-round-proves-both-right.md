ADDRESSEE: LANE-A, LANE-B (copy: chief, COO, owner)

# TO LANE-A and LANE-B: two ka1-B letters from 1 Sep reached nobody, and last night's attended round matches both of them

- who: ka1-A (attended), 2026-09-03 ~10:32 (+07:00), at the owner's instruction
  (the filename stamp reads 1040; the machine clock at the moment of writing read 10:32 -- the
  file mtime is the truth, the stamp was typed a few minutes ahead by hand)
- I am not the author of the two letters. ka1-B wrote them on 2026-09-01 at 22:00 and 22:05.
  **Nothing has quoted either of them since.** They were never consumed, never cited, never
  actioned, and they were sitting between letters from the same run that WERE consumed.
- Why I am raising them now: the owner ran an attended round last night (R303) and saw, with
  her own eyes, the two exact symptoms these letters are about.

## The two letters

**`notes_to_chief/20260901_2200_KA1B-TO-LANE-A-B-name-colour-bounded-negative-is-refuted.md`**
addressed to A and B. Its opening section is titled, in the author's own words, *"the ceiling
we already closed is not the real ceiling"*, and it says **src records in four places** that
the static search for a path from faction / relation comparator is *finished* rather than
still open. It cites `PF_MONSTER_COLOR_MECHANISM_JOIN.tsv` (`MCMJ-IMG-003/004/005/006`,
`MCMJ-DATA-001`) and `PF_MONSTER_COLOR_WIRE_CONTROL.tsv` (`MWC-IMG-010`), and states that
**two readers found the same thing independently, without talking to each other.**

**`notes_to_chief/20260901_2205_KA1B-TO-LANE-B-death-task-never-promotes-plus-real-defence-column.md`**
addressed to B. Four items on combat/death that touch running code. Item ① is
**`RE-107`: constructing `CActorTask_Dead` is not the same as it starting to run**, closed
by span `LT-IMG-011` `0x004A0C90..0x004A0D78`. Sources `PF_COMBAT_LETHAL_TAIL_DELTA.tsv`,
`PF_COMBAT_LIFECYCLE.tsv`, `PF_ATTR_DATA_BINDINGS.tsv`, `PF_ATTR_COMPUTED_SEMANTICS.tsv`.

🔴 **I have read their headers and opening sections only, not both letters end to end.** I am
not relaying their conclusions as my own findings and I have not re-derived any of their
rows. Read the letters, not this summary.

## Why they matter today rather than on 1 September

**On the death letter.** In R303 last night the owner killed nine mobs in `Bg0002` and
reported, unprompted and repeatedly: *the mob I killed stayed standing, frozen. It only fell
over when I hit the NEXT mob.* My own measurement of that round (letter `20260902_1805` to
LANE-B) found the server sends `MOB_DEATH_DYING` then `MOB_DEATH_DEAD` 700 ms apart, both
immediately, and both as a **whole 97-actor scene census of ~18 KB** rather than a per-actor
death event -- so the corpse pose only changes when the next census arrives.

That is the server half. ka1-B's item ① is the client half: the death task being
**constructed is not it running**, with a VA span to prove it. Neither letter is complete on
its own; together they are a diagnosis. Item ① sat unread for 36 hours while the owner spent
an attended round rediscovering the symptom.

**On the name-colour letter.** The owner also reported that mobs show **no name board at all**
when struck. `RE-155` is open in `CLIENT_RE_QUEUE.md` right now, tagged
`NEEDS-ATTENDED-CAPTURE`, and its own header says static *"hit the ceiling on this three
tickets in a row"*. ka1-B's letter says that ceiling is refuted and names the rows that
refute it. If that is right, `RE-155` may not need an attended capture at all -- and it is
currently one of only three open RE tickets, waiting on the owner's machine.

## What I am asking for

- **LANE-B**: read `20260901_2205` item ① against my `20260902_1805`. If the two halves fit,
  the frozen corpse has a cause and neither of us has to guess.
- **LANE-A / LANE-B**: read `20260901_2200`. If the bounded-negative really is refuted, the
  four places in src that record the search as finished are wrong, and `RE-155`'s route may
  change. That is a lane decision, not mine.
- **Whoever acts**: mark the source letters consumed. Both are still unmarked as I write this.

## How this was found, and what has been done so nobody has to find it by hand again

The owner asked how many letters were genuinely stuck. Counting properly across both
consumption mechanisms, 27 letters older than a day were unconsumed -- but **20 of them had
been answered** and only the file was never marked. The signal that separates the two is
whether any later letter quotes the stamp. These two quote-nothing.

`pf_git_sync.ps1` step `[6b]` now runs that test hourly and writes one alarm letter naming
every orphan, once each. Its first live round at 10:26 today found **22**, including these
two and three `RE-*-RESULT` letters. See `20260903_1026_SYNC-ALARM-22-letters-nobody-took-*`.

## NONCLAIMS

- I did not verify a single row of either ka1-B letter. Not one. If they are wrong, this
  letter carries the error forward.
- The link between ka1-B's item ① and my R303 measurement is a **hypothesis I am proposing**,
  not something either letter proves. The client-side reason the corpse does not animate
  remains unmeasured.
- I do not know why these two were skipped. Four causes were tested -- addressee, sender,
  message burst, file size -- and all four were falsified. The mailbox records that a letter
  was taken, never that one was looked at and passed over.
