# R277 (qux8c3) — 2026-09-01T~02:0x+07:00

Round claim: `pf_bridge#651` / `pirate-force-server#427`. Previous round's PR fate checked first
(section 2 item 7): `pf_bridge#647` and `pirate-force-server#424` (round `jjs9bi`, R276) both
`merged=true`, confirmed via `pull_request_read get` on both. No recovery needed, work is on
`main`.

## Mailbox triage

Grepped every `notes_to_chief/*.md` without a paired `.CONSUMED.txt` (189 files) per
`PROCESS_GATES.md` #17 (no date filtering, header read on every candidate, not filename
inference). Filtered by actual `ADDRESSEE:`/`ถึง:` header for chief/everyone-addressed letters
(most of the 189 are `LANE-A/B/GM-STATUS`/`ASK-COO` letters that lane consumes itself per the
"opener consumes" rule, or chief's own outgoing `CHIEF-ASK`/`CHIEF-REPLY`/`FROM_CHIEF_*_TO_ATTENDED`
letters, which do not need a chief-side consumed stub).

Found 21 genuinely chief/everyone-addressed letters with no stub, dating back to 2026-08-28
17:41 through 2026-09-01 01:48. Read every one; all but one were already actioned in
`PROCESS_GATES.md`/`AGENTS.md`/`UNATTENDED_RULES.md`/prior round work — stubbed each with a
one-line note naming where. The one not yet recorded (`COO-DECISION 20260901_0148`, lane-addressed
letters self-close) got a new `PROCESS_GATES.md` #19 this round, then stubbed. Also closed
`CHIEF-ASK-COO 20260831_0457` (the mailbox-stub-bug letter itself), answered by
`COO-DECISION 20260831_0548` and already executed at R256 — never got its own stub until now.

One partial-archive bug found and fixed along the way: `20260829_2255_COO-DECISION-snapshot-*`
had a `consumed/` copy from a prior round but no stub in `notes_to_chief/` itself (a stale partial
consume) — completed properly this round, copy refreshed to match the letter's current content.

## CORE-REQUEST audit (section 17 step 3)

Two live threads found:

1. **Scene14 (Bg0015) hostile-splice** (`20260831_2151_LANE-A-TO-CHIEF-scene14-*`, both lanes
   confirmed+built, asking chief to wire `runtime.py:7501`) — checked `world_population_handoff.py`
   directly: **already wired**, lines ~1019-1033, `if composer.source == "bg0015_roster":` calls
   `mob_scene_recompose.splice_identity_override(..., field_mob_hostile_bg0015
   .scene14_hostile_overrides(legacy))` exactly as asked. This was done by R274 (`gmcj4a`,
   ~23:2x that same night, after this letter was sent) — the letter just never got its own stub.
   Stubbed this round pointing at R274's work; confirmed still on `main` by reading the live file,
   not by trusting the old letter or the continuation log.

2. **`mob_pickup_persist.pickup_and_persist` + `lane_hooks.lane_b_mob_ai_tick.maybe_tick`** —
   `COO-DECISION 20260901_0145` (16 minutes before this round claimed its lock) tells LANE-B to
   wire both directly into `runtime.py` in LANE-B's own next round. This conflicts with the
   standing write-zone rule (prompt section 6): `runtime.py` is chief's alone, with exactly one
   named exception (LANE-B's world-wipe block) that does not cover these two call sites. Read
   both target modules (`mob_pickup.py` is 2000+ lines of heavily-nonclaimed contract, with two
   OPEN RISK notes — NONCLAIM 15/16 — about an unresolved bag-cell/claimant binding and a
   two-allocator desync on a failed commit) before deciding this is not something to either
   silently wire myself (no CORE-REQUEST names exact lines/handling for the open risks) or leave
   LANE-B to edit outside their zone without asking first. Wrote
   `20260901_0200_CHIEF-ASK-COO-mob-pickup-ai-tick-runtime-wiring-who-edits-runtime-py.md` — did
   not touch `runtime.py` for either point this round, to avoid racing LANE-B's own round if they
   already started under the COO's original instruction.

No other open CORE-REQUEST found (RE-170/171, GT-146 etc. are attended/RE-runner queue items,
not chief wiring asks).

## What did not change

No `src/` edit in either repo this round (`pirate-force-server` git status stays empty; server-side
PR carries only the round-claim commit). `PROCESS_GATES.md` (pf_bridge, docs) is the only
substantive file touched besides mailbox stubs. WIRED = 4/4, unchanged from R274-276 (no new
`runtime.py`/`app.py` import this round).

## Game test queue

Not updated this round — no server-code change means nothing new for the attended tester.
`GT-072`'s 102KB queue-shrink (flagged by R276 as next round's target) was **not** attempted this
round: it is an open (`PARTIAL`, not closed) entry, and safely trimming 100KB+ of accumulated
Thai technical timeline down to header+criteria+status+pointer without losing any of the
not-yet-tested content needs a dedicated read-through this round's budget did not have room for
after the mailbox/CORE-REQUEST work above. Left for a future round, flagged again here so it is
not silently dropped.

## Not proven / nonclaim

- The `mob_pickup_persist`/`mob_ai_tick` runtime.py wiring is unresolved pending COO's answer to
  the ownership-boundary question above — this is explicitly not "declined", just not started.
- `GT-072` queue-shrink still pending (see above).
- Ledger/coverage verifiers not re-run this round (no server-repo `src/` change to drift against).

PF-AUTOMERGE: v4
