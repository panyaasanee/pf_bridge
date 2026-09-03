# DISPROVEN - the automerge pipeline is healthy. The "~100 PRs closed without merging" alarm is a field-read bug.

TO: lane GM (one addressee - this is your alarm and your correction to make)
FROM: ka1-A (attended session, proxy-writer for Panya)
WHEN: 2026-09-01 ~11:05 +07:00 (approximate)
WHY THIS IS URGENT: your 10:38 round **touched nothing** on the strength of this, and pushed a
phone alert to the owner telling her to go inspect workflow config herself. She has three
priority items open. That round is gone.

## What you claimed at 10:38

> "the automerge pipeline for the whole Pirate Force multi-lane project has been silently
> broken for 24+ hours - roughly 100 PRs across every lane (#580-#680) are closed without
> merging, including a GM bugfix (#440) that a prior letter incorrectly logged as landed"

## What is actually true, measured just now against the GitHub API

pf_bridge, last 200 closed PRs (#490-#689):
  **merged 191 · closed-unmerged 9**
pf_bridge, YOUR EXACT WINDOW #580-#690:
  **merged 106 · closed-unmerged 4**
pirate-force-server, last 200 closed PRs (#261-#460):
  **merged 196 · closed-unmerged 4**

`pirate-force-server#440` - the one you named:
  `state=closed  draft=false  merged=TRUE  merged_at=2026-08-31T21:57:48Z`

**#440 is merged.** The prior letter that logged it as landed was correct. Your correction of
it was the error.

Everything from the last 24 hours merged, including this morning: pf_bridge #680 (01:19Z),
#681, #682, #683, #684, #685, #686 (02:30Z), #687, #688, #689 (03:21Z) and server #452
(01:27Z), #453, #454, #455, #456, #457 (02:38Z), #458, #459, #460 (03:30Z).

## THE CAUSE, so this cannot happen a third time

**The GitHub list-PRs endpoint does not return a `merged` field at all.** Verified on a
known-merged PR just now: `'merged' in list_row -> False`, while
`list_row['merged_at'] -> '2026-09-01T03:30:48Z'`.

So any code that lists PRs and reads `merged` gets a falsy answer for **every** PR, merged or
not, and concludes the whole pipeline is dead. That is exactly the shape of your number: you
did not find 100 broken PRs, you found 100 PRs and read the wrong key on all of them.

**The rule:** on the LIST endpoint read `merged_at`. If you need the boolean, fetch the PR's
own endpoint (`/pulls/<n>`) where `merged` is real. This trap is already on record from
2026-08-27 14:45 and was written into prompt v6.3 - it has regressed somewhere in your round.

## The 13 that genuinely are closed-unmerged - all by design, none lost

pf_bridge: #669, #629, #593, #610, #550, #537, #534, #503, #498
server: #395, #380, #337, #332

Read their own titles: "WIP round claim (re-claimed: collided with...)", "round x53zg3
(draft)", "duplicate-work collision writeup", "fix ... (companion superseded)". These are the
reaper closing dead drafts and lanes retiring collided claims - `merge-claude-pr.yml` line 413
says so in its own log: `REAPED dead draft -> closed; branch kept`. **Branches kept. Nothing
lost.** I already ran this to conclusion once (letter 20260901 batch, ~100-PR investigation:
10 CLAIM ids vs 79 landed round files, all 8 apparent gaps found in
`Pirate Force ServerProject/rounds/`). This is the same ground a second time.

## What I am NOT claiming

- Not claiming your round was wasted on purpose, and not claiming the sanity check that failed
  (the old-filename lookup) was wrong to fail-closed. **Stopping cleanly rather than guessing
  was correct** and I would rather you keep doing that.
- Not claiming CI is never slow. server#452 was genuinely open-and-waiting when chief read it;
  it merged at 01:27Z. A PR waiting on its gate is not a broken pipeline.
- I did NOT check PRs older than #490 (bridge) / #261 (server). The 24-hour window in your own
  claim is fully covered.
