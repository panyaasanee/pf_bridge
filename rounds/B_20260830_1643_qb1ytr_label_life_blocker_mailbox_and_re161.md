# LANE-B round qb1ytr -- 2026-08-30T16:43+07:00

## Player-visible difference from yesterday

None from this round's own commits. This round found the single most important new fact of the
day -- the reason players see zero loot labels is not a bug in the drop pipeline (drops are real,
frames go out, the multi-drop shape works) but that the label's on-screen life (0.2s, a client fact
measured back at GT-045) is shorter than the time it now takes a drop frame to reach the client
(measured this round at 351-949ms). Fixing that requires either touching a standing COO ruling
(no re-announcement in production) or a runtime.py ordering change that is the chief's to make --
neither of which this lane can do unilaterally. So today's work is making sure the next round (of
any lane, or an attended session) does not waste a boot on a wall that is already understood, and
opening the two doors (COO question, RE ticket) that have to open before anyone can build the
actual fix.

## Section A (addendum v2) -- last round's PR fate

| repo | last [LANE-B] PR | result |
|---|---|---|
| `pirate-force-server` | #314 (`309h1a`) | merged (confirmed via `is:merged` search per orchestrator) |
| `pf_bridge` | #502 (`xt0g9c`) | merged (confirmed via `is:merged` search per orchestrator) |

No cherry-pick needed; both branches started from a clean `origin/main` tip in each repo.

## Section B (addendum v2) -- mailbox

Grepped `^\[ถึง: LANE-B` (the addendum's `ADDRESSEE: LANE-B` token is a false negative for this
project's actual letter header format, as a prior round already flagged) and cross-checked every
LANE-B-addressed letter against a `.CONSUMED.txt` stub. One new, substantive letter found:

`20260830_1554_GT143-GT132-GT149-RESULT-label-life-0.2s-is-the-real-blocker-drops-exist-set103-never-shipped.md`
(attended session "กะ1-A", `OBSERVER_CONFIRMED: 2026-08-30T15:4x+07:00`, boot commit `6961ecf`,
canonical DB unchanged, teardown PASS).

What it measured, and what this round did with each part:

1. **GT-149** (does the drop persist long enough to click) -- the owner never saw a single label in
   four kills, so the client-observable layer of the original question has no answer. But the wire
   layer answered a more useful question: `DROP_LIFETIME_SECONDS=120.0` (this lane's own interim
   number, COO-accepted 2026-08-29) is holding correctly -- the ledger really does survive 120s.
   The actual blocker is a different field entirely: `label_life=0.2s`. Header updated to
   `ANSWERED-DIFFERENTLY`.
2. **GT-132** (does a multi-drop kill draw N labels) -- wire layer proved a real 2-item multi-drop
   (template 34, 82-byte frame) exists and was sent correctly. Client layer: 0 labels, all four
   kills, not just the multi-drop one. Header updated to `NO-RESULT` on the claim itself (the
   coalesce mechanism was never given a chance to be seen, so it cannot be graded PASS or FAIL by
   this boot). Retracted this lane's own prior recommendation (round `xt0g9c`) to use template 103
   (Orc Chief) as the multi-drop example -- that template's five placements are all inside
   `OWNER_REFUSED_PLACEMENTS['Bg0002']` and have never once shipped to the field (confirmed by
   GT-143, same letter). Template 34 is the one proven this round.
3. **GT-143** (what is actually at the five Prison Exile coordinates) -- both of this lane's own
   competing predictions (`setnum` -> Orc Chief visible, `cline` -> invisible rank-0 row) were
   wrong. The census carries neither `n_ID 103` nor `917` at all; the five rows are simply absent
   from the pipe. Header updated to `ANSWERED`. Where in the pipe they were dropped is explicitly
   the letter's own item 4, addressed to lane A/chief, not re-opened here.
4. Corpse-pose-timing observation (item 3, the letter's "most valuable finding") -- a model stays
   frozen standing after its death frame and only visibly falls when the *next* kill's census
   recompose arrives, even though the current kill already sends its own dying+dead+recompose
   frames in the same batch. This is squarely an RE (client behaviour) question, so it was **not**
   guessed at in `src/` -- **opened as `RE-161`** in `CLIENT_RE_QUEUE.md` instead, per this lane's
   own rule 2 (build what is known, ticket what is not).

All consumed: stub written
(`notes_to_chief/20260830_1554_GT143-GT132-GT149-RESULT-*.md.CONSUMED.txt`), original copied to
`notes_to_chief/consumed/`.

## The governance question this round could not answer itself

`label_life` is a **measured client fact**, not a server-side field -- there is nothing in
`src/pirateforce_foundation/mob_loot.py` to tune. The only server-side lever that could plausibly
compensate (re-announcing a drop so its label gets redrawn) is `DROP_REFRESH_MS`, which the COO
explicitly forbade wiring into production on 2026-08-26T07:45 pending a measurement this letter
partially supplies. Flipping that switch myself would be hard-stop category (c) -- directly
contradicting a standing owner ruling -- so this lane did not do it. Instead:

- Wrote `notes_to_chief/20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md` laying
  out four options (do nothing / reorder frames / bounded re-announcement / leave as known
  NO-RESULT), stating which one this lane is proceeding with
  (`[สมมติของสาย B - รอ COO ยืนยัน]`: option 4, i.e. no code change, ticket the gap) and asking COO
  to rule on whether the 2026-08-26 ban should be revisited given the new `late_ms` evidence.
- Filed one `CORE-REQUEST` inside that same letter (chief-only, `runtime.py`): the 97-actor,
  17,910-byte `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE(_DYING)` frames are queued (`runtime.py:4634-4650`)
  *before* `mob_drop_presence.loot_actions()` (`runtime.py:4720`) in the same kill's action list --
  a structural (not measured) reason the shortest-lived frame in the system is consistently queued
  behind the most expensive one. This does not touch the "one announcement per drop" rule at all
  (it is about order, not repetition), so it does not conflict with the 2026-08-26 ban.
- Annotated `GT-146`'s P0 gate in `GAME_TEST_QUEUE.md` to say plainly it will abort every future
  boot until this is resolved, so nobody burns another attended session hitting the same wall
  before either the ASK-COO or the CORE-REQUEST lands.

## Files touched (pf_bridge)

- `GAME_TEST_QUEUE.md` -- GT-132 header (READY -> NO-RESULT + template correction), GT-143 header
  (OPEN -> ANSWERED), GT-149 header (PENDING -> ANSWERED-DIFFERENTLY), GT-146 P0 gate annotation.
- `CLIENT_RE_QUEUE.md` -- new ticket `RE-161 CORPSE-POSE-APPLIES-AT-NEXT-RECOMPOSE-NOT-AT-DEATH-FRAME-001`.
- `notes_to_chief/20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md` (new).
- `notes_to_chief/20260830_1554_GT143-GT132-GT149-RESULT-*.md.CONSUMED.txt` (new stub).
- `notes_to_chief/consumed/20260830_1554_GT143-GT132-GT149-RESULT-*.md` (copy of original).
- `rounds/B_20260830_1643_qb1ytr_label_life_blocker_mailbox_and_re161.md` (this file).

No files touched in `pirate-force-server` this round -- verified no safe, non-conflicting `src/`
change exists yet (the two candidate fixes both require either a chief-owned `runtime.py` edit or
overturning a standing COO ruling). Per rule F this is a real (non-empty) round: it changes ticket
state that three open tickets and one attended-session runbook step depend on, and it opens the two
tickets that have to exist before anyone can build the actual fix. Last round (`xt0g9c`) was also
non-empty, so this does not trigger the two-empty-rounds rule either way.

## Not yet proven

- Whether reordering `runtime.py`'s action list actually reduces `late_ms` enough to matter --
  structural inference from line numbers, not a measurement. Flagged as such in the CORE-REQUEST.
- Whether a bounded re-announcement (if COO approves reopening the question) would actually redraw
  the label at all (`REEMISSION_REDRAWS_THE_LABEL` stays `None` -- this round could not add data
  since no re-announcement was sent under current production cadence).
- Everything client-observable in this space needs an attended human in front of the screen; none
  of it is headless-measurable, which is exactly the split this round's letter itself criticised
  as under-designed in GT-143 ("เห็นว่างเปล่า" vs "cline ทำงานแล้ว" being visually indistinguishable).

## CORE-REQUEST

See body of `notes_to_chief/20260830_1643_LANE-B-ASK-COO-label-life-reopens-drop-refresh-ban.md`:
reorder `runtime.py` so `mob_drop_presence.loot_actions()` (`:4720`) queues before
`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE(_DYING)` (`:4634-4650`) in the same kill's action list.

## Tickets opened for other lanes

`RE-161` (`CLIENT_RE_QUEUE.md`, addressed to RE) -- corpse-pose-applies-at-next-recompose static
analysis question.
