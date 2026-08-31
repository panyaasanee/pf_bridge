# R255 (session `8skr91`) — mailbox stub bug found and backfilled at scale

2026-08-31T~04:5x+07:00, chief, audit round, no src change in either repo.

## Round-lock guard

`pull_request_read get` confirmed both R254 PRs merged=true before claiming this round's lock:
`pf_bridge#560` (merged 2026-08-30T21:03:09Z), `pirate-force-server#356` (merged 2026-08-30T21:09:57Z).
No stray `[LANE-E]` PR was open before that.

## What this round found and fixed

Audited `notes_to_chief/` against `notes_to_chief/consumed/`. A letter with a copy in `consumed/` was
read/processed at some point (that is what copying it there means); it should also carry a sibling
`<name>.CONSUMED.txt` stub in `notes_to_chief/` itself. Found **467 of 489** letters with a `consumed/`
copy but no stub — including letters R254 itself claimed to have stubbed a few hours earlier. This is
the same failure mode section 18 item 0 named for 6 specific RE-* letters, but at roughly 78x the
scope assumed: essentially every round since the v6.3 stub rule started has been dropping the stub
step after copying.

Backfilled all 467 with a generic, honest stub (states plainly this is a backfill, not a re-derived
per-letter judgment — the `consumed/` copy itself is the evidence the content was already acted on
when current).

Separately found and hand-read 7 more letters missing *both* stub and `consumed/` copy:
- `20260831_0430_LANE-GM-STATUS-gmprobe-wired-plus-mailbox-consumed.md` — genuinely new since R254,
  FYI: LANE-GM wired `/gmprobe <variant_id>` (CORE-REQUEST-GM-043 option A) entirely inside `gm/`,
  `runtime.py` untouched, GT-164 already unblocked by LANE-GM itself.
- `20260831_0352_CODEX_VTABLE_BOUNDARY_CORRECTION_AND_EMPTY_CLOSURE.md` — external read-only IMAGE
  checkpoint, no repo action possible.
- `20260828_0231_CHIEF-REPLY-CORE-REQUEST-022-*.md`, `20260828_0912_CHIEF-REPLY-CORE-REQUEST-027-*.md`,
  `20260829_0146_LANE-A-CORE-REQUEST-face-frame-*.md`, `20260829_0944_LANE-GM-CORE-REQUEST-GM-034-*.md`,
  `20260829_1105_LANE-GM-CORE-REQUEST-GM-035-*.md` — all five verified already answered/closed in
  earlier rounds (R203, R220, R225/`CHIEF-REPLY 1221`, GT-145 result) via grep cross-reference; the
  stub step was simply never done at the time. Backfilled with a one-line pointer to where each was
  actually resolved.

## CORE-REQUEST audit

No new CORE-REQUEST letter pending from LANE-A/B/GM this round. The only CORE-REQUEST-adjacent letter
since R254 (`LANE-GM-STATUS 0430`) reports GM-043 already wired in LANE-GM's own territory — nothing
for chief to wire in `runtime.py`/`app.py`.

## Escalated, not decided

Sent `CHIEF-ASK-COO 0457`: reports the 467-letter finding, and flags a separate, still-untouched
backlog of ~90 letters (39 `ASK-COO`, 22 `STATUS`, rest mixed) from 2026-08-28/29 that have neither a
stub nor a `consumed/` copy — meaning they may never have been read at all, not just missing their
stub. Most are COO's own `ASK-COO` letters or old lane `STATUS` FYIs, almost certainly superseded by
30+ rounds of decisions since, but chief has not verified that letter-by-letter. Asked COO whether to
triage individually or bulk-archive with a standing recall path.

## Not proven this round

No client opened, no DB measured, no server `src/` change — nothing new for `GAME_TEST_QUEUE.md` this
round (existing queue content untouched). `AGENTS.md` is still 39,103 B against its 25 KB v6.3 cap;
`COO-DECISION 20260830_1541` already authorizes cutting it on disclosed judgment without asking every
time, but the cut itself needs a full read of the file to do safely and was not attempted this round —
carried forward, not a new regression.

Ledger (`pirate-force-server`): `tools/verify_hypothesis_ledger.py` -> `HYPOTHESIS_LEDGER PASS entries=47`,
no drift.

PF-AUTOMERGE: v4
