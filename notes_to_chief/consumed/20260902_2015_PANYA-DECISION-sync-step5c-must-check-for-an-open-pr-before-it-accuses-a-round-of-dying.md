# PANYA DECISION - step [5c] must check for an OPEN pull request before it accuses a round of dying

- decided by: **Panya**, attended session, ~2026-09-02 20:05 (+07:00), approximate
- channel: chat. She was told the alarm was wrong, asked "whose is it", was shown the
  evidence, and answered "fix it".
- written by: ka1-A as her proxy writer
- patched: `pf_bridge\pf_git_sync.ps1` step [5c]
  (backup `agent_kit\pf_git_sync.ps1.pre_patch_5c_openpr_20260902`)
- verified: parser 0 errors, `-SelfCheck` exit 0, and **the live round at 20:12:16 did
  exactly the new thing** (below)

## The false alarm that caused this

At 19:48:10 step [5c] shouted:

```
round died holding the lock: 1 claude/* branch(es) whose tip is still a bare round
claim after 75 min - every scheduled run since then is backing out of a lock nobody
is using
  !! origin/claude/gracious-galileo-et2ux4  age=90min  tip="round claim: et2ux4"
a person must close that lock PR - this step will not touch it
```

The owner asked ka1-A to check before acting. **The branch was LANE-GM's and the round
had not died.** Its two pull requests were both already merged:

- `#590 [LANE-GM] The frame this lane sent locked a real client, so this door now holds
  every shape no client has been measured accepting` - merged 2026-09-02T12:05:33Z
- `#594 [LANE-GM] The clearance for the held /speed shape is a set, not a boolean, and
  the console stops claiming a cause` - merged 2026-09-02T12:40:04Z

The second merged **eight minutes before the alarm**, and the branch was already gone
from the server repo by the time anyone looked. Following the instruction would have
meant closing the work of a lane that had just finished - and #590 is the fix for the
GT-193 defect this same owner hit an hour earlier, when `/speed 300` locked her client.

## Why the age test alone could never work

A finished round and a dead one leave the identical artefact: a `claude/*` branch whose
tip is still the bare `round claim:` commit. The original comment in the step says as
much and picks age as the discriminator. Age does not discriminate: a round that
finishes in 40 minutes still leaves that tip lying there at 90 minutes, at 300 minutes,
forever.

What does discriminate is whether a pull request is still **open**.

## What changed

Before shouting, [5c] now asks GitHub whether any OPEN pull request has that branch as
its head, across both `panyaasanee/pf_bridge` and `panyaasanee/pirate-force-server`.
Three outcomes, three different lines:

- **open PR** -> shout as before, now saying "AND whose pull request is still OPEN"
- **no open PR** -> a quiet log line: "the round finished and left its claim commit
  behind, not an alert, nothing to close". Nobody is asked to do anything.
- **API unreachable** -> still shouts, but says the PR state is **UNVERIFIED** and that
  nobody should act on that line alone. Failing loud but honest beats failing silent.

Rate limit: the verdict is cached per branch for `$CLAIM_PR_RECHECK_MIN = 20` minutes in
`sync_state_claim_pr.log` (local, never committed), so a step that runs every two minutes
cannot burn the 60-per-hour unauthenticated budget. In dry-run and self-check modes no
call is made at all.

## Proof it works, from the live log

```
20:10:07  [5c]  SHOUT  round died holding the lock: 1 ... age=112min      <- old code
20:12:16  [5c]  1 bare round claim tip(s) with NO open pull request -
                the round finished and left its claim commit behind,
                not an alert, nothing to close
20:12:16  [5c]    -- origin/claude/gracious-galileo-et2ux4 age=114min openPR=no
20:14:07  [5c]  (same, served from cache - no second API call)
```

## NONCLAIMS

- This does NOT make [5c] able to tell a healthy round from a dead one in general. It
  removes one specific way of being wrong: accusing a round whose work already merged.
- A round that dies **before** opening its PR still looks like nothing at all to this
  step, exactly as before.
- The API is queried unauthenticated. A private repo, a rate-limit block or an outage all
  land in the `unknown` branch, which shouts rather than staying silent.
- No self-check test was added. The 14-test harness is still red on 5 of its own tests
  (`LOOSE_ENDS` item 2, still unowned).
- ka1-A also found **26** `claude/*` branches whose tips are bare `round claim:` or
  `wake gate:` commits going back to 26 Aug. They are outside [5c]'s 75-360 minute
  window so it never spoke about them, and this patch does not change that. Whether that
  backlog of branches should be pruned is somebody's decision, not this step's.
