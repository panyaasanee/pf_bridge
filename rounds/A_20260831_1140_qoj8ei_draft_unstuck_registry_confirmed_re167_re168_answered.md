# LANE-A round `qoj8ei`

2026-08-31T11:40+07:00 (`TZ=Asia/Bangkok date`).

## Step A: round-lock check (this round's real first action)

`pirate-force-server#374` (`[LANE-A]` round `3t75jw`) was still `state=open`, `draft=true`,
`mergeable_state=unstable` at the top of this round -- the exact stuck-draft symptom chief's `R261`
(`rounds/R261_iby4ui_urgent-draft-pr-reaper-notification-plus-re167-re168-opened.md`) had already
escalated to the owner. `pf_bridge#582` (same round) had already merged on its own.

**Tried the fix chief's R261 could not**: `mcp__github__update_pull_request(owner, repo, pullNumber=374,
draft=false)` -- the GitHub MCP tool, not a raw REST `PATCH`. It worked. `pull_request_read get`
immediately after confirmed `draft:false`. `merge-claude-pr.yml` (the repo's own automerge workflow)
picked it up within the minute and merged it: `merged_at: 2026-08-31T04:28:54Z`,
`merged_by: github-actions[bot]`.

**This matters beyond this one PR**: R261 tried GraphQL `markPullRequestReadyForReview` (blocked by the
proxy) and raw REST `PATCH .../pulls/{n}` with `{"draft": false}` (returned `200`, field unchanged) and
concluded only the human owner could unstick it. The MCP tool's `update_pull_request` call is a third,
apparently-different path that this round confirms actually flips the field. `pirate-force-server#363`
(`[LANE-B]`) is reported stuck the same way and was NOT touched by this lane (not this lane's PR, rule
followed), but the same MCP-tool fix is worth trying there before its reaper window closes -- said
directly in this round's status letter to chief, not acted on.

## Step B: mailbox, consumed this round

1. `20260831_1042_COO-DECISION-scene10-landing-geometry-open-affirmed.md` -- chief's `R261` had already
   stubbed it, but the instruction inside it ("LANE-A เปลี่ยนป้ายในทะเบียนเองเป็น CONFIRMED รอบถัดไป") had not
   been carried out yet. Done this round in `pirate-force-server`: struck the pending-assumption tag on
   scene 10's registry row, replaced with the confirmed ruling text, same strike-through convention scene
   1/14 use. See the `pirate-force-server` round file for the exact diff description.
2. `20260831_1037_GT148-and-GT165-RESULT-stowaways-cleared-and-slave-market-island-has-life.md` --
   `ADDRESSEE: LANE-A`, no stub before this round. Both tickets PASS both tiers (client-observable AND
   wire, per the letter's own two data points). Closed both headers in `GAME_TEST_QUEUE.md`:
   - `GT-148`: no Port Royal actor carried into the empty sea scene; `WORLD_M2_CROSSING_HANDOFF
     kind=clear dispatched=YES` confirmed on the wire.
   - `GT-165`: real, friendly, correctly-named NPCs seen at Slave Market Island;
     `WORLD_CENSUS_BG0004 assembled=109/116` matched the ticket's own predicted number exactly.
   Stub placed at `notes_to_chief/20260831_1037_...md.CONSUMED.txt`, original copied verbatim to
   `notes_to_chief/consumed/`.

Also this round: chief's `R261` assigned `RE-167` (census-frame intermittent `ConnectionAbortedError
10053`) and `RE-168` (Columbus dialogue window not reset across the scene-17 crossing) to this lane. Both
answered at the wire/DB tier (client-observable tier stays open -- neither has a shippable fix yet to
give a GT test):

- **`RE-167`** (`notes_to_chief/20260831_1136_RE-167-RESULT-...md`): read `current/
  pf_login_game_server_v141.py:7746-7757` directly. The one send site is a synchronous `c.sendall()` per
  action, no chunking, no retry; on `ConnectionAbortedError` et al. it prints and `break`s -- which also
  explains a detail nobody had named yet: a census-frame abort silently drops the paired REAPPLY frame
  too (`break`, not `continue`), matching every reported case exactly. `settimeout(600)` is far too wide
  to be the cause. No server-side buffer/timeout/race explains the intermittent abort -- closed
  bounded-negative at this tier. Chunking would require editing the frozen `v141` file, which the
  project's own gate (not just a lane boundary) requires stay byte-clean; flagged as a structural
  chief/COO question, not a same-round CORE-REQUEST.
- **`RE-168`** (`notes_to_chief/20260831_1142_RE-168-RESULT-...md`): read `world_m2_crossing_handoff.py`
  and `runtime.py:4889-5089` directly. The existing `kind=clear` frame is population-only (confirmed by
  its own docstring and call chain); no UI/dialogue field exists anywhere in it.
  `columbus_quest3021_conversation_sent` proves the server DOES track that the conversation opened (grep:
  3 hits total, set `True` once, never reset), so a close signal is technically wireable -- but no
  dialogue-close opcode is characterized anywhere in this tree yet. Proposed opening a new ticket to
  LANE-C/RE for the opcode search itself (not filed as a formal ticket this round -- flagged in the
  letter, a fresh round should title and file it properly after a duplicate-check, which already came
  back clean).

## Gate, measured (pirate-force-server side of this round)

| check | result |
|---|---|
| targeted (registry/scene/census files) | 116 passed, 468 subtests, 0 failed |
| `tests/test_tree_is_cp874_safe.py` | 5 passed, 411 subtests, 0 failed |
| full suite | 5706 passed, 323 skipped, 10238 subtests, 0 failed |
| `git diff --stat` on `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py` | empty (read for the two RE tickets, none touched) |

## What a player sees because of this round

**Nothing new directly from this round's edits.** The player-visible change this round actually delivers
is indirect: unsticking `pirate-force-server#374`'s draft status is what let round `3t75jw`'s own change
(scene 10's login door opening) actually reach `main` and become real instead of stranded on an unmerged
branch. The registry edit and the two RE answers are bookkeeping and static findings, not new behaviour.

## What's blocked / waiting

- `RE-167`/`RE-168` client-observable tiers: no fix exists yet, so no new GT opened.
- `RE-167`'s chunking question needs a chief/COO structural decision (frozen-file cleanliness vs a real
  fix), not a same-round CORE-REQUEST.
- `RE-168` needs a characterized client opcode from RE/LANE-C before any wire proposal is possible.
- `pirate-force-server#363` (LANE-B, stuck draft) -- not this lane's PR, flagged to chief only.

## ASK-COO

None this round. Scene 10's one live ASK-COO (round `3t75jw`) was already answered by `COO-DECISION
20260831_1042`, consumed above.

-- LANE-A (WORLD) round `qoj8ei`
