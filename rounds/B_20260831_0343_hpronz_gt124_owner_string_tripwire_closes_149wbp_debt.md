# LANE-B round `hpronz` (scheduled, no live viewer) -- 2026-08-31T03:43+07:00

## Player-visible difference from yesterday

**None.** This round adds one test, touches no `runtime.py`/`app.py` call site (chief's files, per the
hard limits) and adds no scenario. Same honest answer round `n7vbxq` gave for RE-157 job 1's predicate:
a lane-B-zone build that does not change what a player sees on its own is still real work, reported as
such, not dressed up as a feature.

## Why this round: rule-F fallback (d), tech debt pf-adversary flagged and nobody closed

Round `n4vwrq` (01:47) and round `upf0xp` (02:41) were both pure reverify/no-drift rounds -- the
standing rule forbids a third one in a row. Mailbox pass (below) found nothing newly addressed to LANE-B
since `upf0xp`'s cutoff, and the named backlog (M5 pickup persist, BUILD-004 scene 14, RE-157 job 1/2
wiring, mob_aggro M6, drop label life) is still blocked with reasons a human already decided (`GT-146`
attended PENDING, `COO-DECISION 2026-08-26T12:46+07:00` not lifted, chief deferred RE-157 wiring twice).
None of it is this lane's to un-block by writing new code without overriding someone else's ruling.

So: fallback (d). Round `149wbp`'s letter (`pf_bridge/rounds/B_20260829_0652_149wbp_recover-235-and-
close-chiefs-two-open-defects.md`, section 5.1) left one item open and said so explicitly rather than
closing it quietly:

> `GOVERNED_BAG_ALLOWLIST_OWNER` ยัง**เป็นข้อความที่พิมพ์มือ** (เทสตรวจได้แค่ว่ามันเอ่ยชื่อฟังก์ชันที่มีจริง)
> ⇒ เปิดเป็นงานรอบหน้าของสายนี้ ไม่ปิดเงียบ

Round `j0u64p`'s letter (item 4 of its "ค้าง" section) repeated the same open item three rounds later,
still unfixed. That is two separate pf-adversary-adjacent findings, in this lane's own zone
(`src/pirateforce_foundation/mob_pickup.py` + `tests/test_mob_pickup.py`), never closed. This round
closes it.

## What was wrong, precisely

`mob_pickup.GOVERNED_BAG_ALLOWLIST_OWNER` is prose naming GT-124 ("the remaining blocker is the absent
call site (GT-124)"). Its sibling constant, `GOVERNED_BAG_ALLOWLIST_BLOCKS_PERSISTENCE`, was fixed in
round `149wbp` to be re-derived from `store.py`'s actually-executed SQL (an AST walk,
`tests/test_mob_pickup.py::_executed_sql`) rather than trusted as a hand-set boolean. The OWNER string
never got the same treatment: the only assertions against it
(`test_the_governed_allowlist_is_the_wall_this_lane_stops_at`) check that it contains the substrings
`"GT-124"` and `"call site"`, and does NOT contain two retired phrases. None of that verifies the string
is still TRUE -- a stale string naming the wrong real function, or a string nobody updated the day the
chief actually wires GT-124, would keep passing that check forever. That is exactly the failure mode
`GOVERNED_BAG_ALLOWLIST_BLOCKS_PERSISTENCE` already had once (round 149wbp's own pf-adversary pass found
it silently untied from `store.py`) and exactly what fixing it there was supposed to prevent lane-wide.

## What was built

Nothing in `src/` needed to move -- the fix is a re-derivation, same shape as `_executed_sql`, added to
`tests/test_mob_pickup.py`:

- `_call_names(module_name)`: parses a `src/pirateforce_foundation/<name>.py` file's AST and returns
  every name actually reached by a `Call` node (`ast.Call.func.id` for a bare name, `.attr` for
  `module.name(...)`/`obj.name(...)`). Companion to the existing `_executed_sql`, which does the same
  thing for `execute`/`executemany`/`executescript` call arguments.
- `test_the_owner_strings_named_call_site_is_really_absent_from_runtime_py`: reads
  `mob_pickup_persist.MOB_PICKUP_PERSIST_HEADLINE_CALL` (the constant that already names, in one place,
  "the line the chief adds ... once GT-124's call site exists" -- built in round `uq2lxw`, after both
  the `149wbp` and `j0u64p` letters that flagged this debt), regex-extracts the symbol it names
  (`pickup_and_persist`, derived from the constant's text, not hand-copied a second time), confirms
  `mob_pickup_persist` actually defines that symbol, then asserts it does **not** appear in
  `_call_names("runtime")` -- i.e. `runtime.py` genuinely does not call it today. Also asserts the same
  for `dispatch_pickup_request` (the older, narrower name this lane's own docstring above still cites
  for the same absent call site; `pickup_and_persist` calls it internally, so a `runtime.py` that called
  the inner name directly, skipping the persist wrapper, would still be GT-124 wired and must still go
  red here).

The day the chief wires GT-124 (either form), this test goes red by construction -- an AST walk over the
file it describes, not a hand-typed string that cannot self-report going stale.

## Verification the tripwire actually fires (not just that it is green today)

Hand-mutation test (not committed, scratch-only): appended a synthetic function to a copy of
`runtime.py`'s source that calls `mob_pickup_persist.pickup_and_persist(...)`, re-ran the same AST-walk
logic against the copy, confirmed `"pickup_and_persist"` is found in the resulting call-name set. This is
the same "does the guard actually catch the thing it claims to catch" check pf-adversary has run against
this lane's other tripwires before (round `149wbp` section 4, item 3: "ตัวดักที่ผม 'แก้' แล้ว ยังดักไม่ได้
อยู่ดี"), done here in self-review since no `pf-adversary` subagent is reachable in this session (see
below).

## Self-review (no pf-adversary subagent available in this environment)

- Confirmed by direct `grep`/AST that `pickup_and_persist`, `dispatch_pickup_request`, `resolve_claim`,
  and `place_in_bag` all have zero call sites in `runtime.py` today, matching what the new test asserts
  and what the OWNER string claims.
- Ran the hand-mutation check above to confirm the new test is not a tautology that would stay green
  even if `runtime.py` were wired -- the specific failure mode round `149wbp` documented for its own
  first draft of this exact kind of tripwire ("A tripwire wired to a constant is not a tripwire").
- Re-read `mob_pickup_persist.py`'s docstring end-to-end to confirm `MOB_PICKUP_PERSIST_HEADLINE_CALL`
  is genuinely the authoritative, most-current statement of what GT-124's call site is (it postdates and
  narrows the older `dispatch_pickup_request`-only framing in `test_gate2_bag_admission_wiring.py`'s
  docstring and in this file's own older docstring) -- not asserting a symbol name invented for this
  round.
- Full suite run twice: once after the change alone (`tests/test_mob_pickup.py`, 79 passed / 77 subtests
  passed), once for the whole repo (see Numbers below) -- zero failures, zero new skips attributable to
  this change.
- Checked `tests/test_mob_pickup.py` encodes under `cp874` directly (`str.encode("cp874")`); the file
  carries only ASCII (the `-- ` em-dash convention this codebase's prose already uses throughout, not a
  Unicode dash).
- Confirmed `tests/` is in scope for non-ASCII test DATA per this lane's charter, but this diff adds
  none -- pure ASCII prose and code, so no exemption was needed either way.
- Diff is exactly one file (`tests/test_mob_pickup.py`); no `src/` file changed, so no risk of this
  round accidentally widening or narrowing a gate while "just" adding a test.

## Not yet proven

- Whether `mob_pickup_persist.pickup_and_persist` is in fact the call the chief will eventually wire, or
  whether a future design changes the shape again before GT-124 lands -- this test only proves today's
  named blocker is really absent today; it re-derives, it does not predict.
- Whether GT-124 itself is still blocked on the same grounds recorded in the last two LANE-B status
  letters (attended capture / owner priority) -- unaffected by and not re-litigated in this round.

## Files touched

`pirate-force-server`:
- `tests/test_mob_pickup.py` (1 file: +1 helper function `_call_names`, +1 test method, +1 import line
  (`re`), +1 import addition (`mob_pickup_persist`) -- 102 insertions, 1 deletion)
- `rounds/B_20260831_0343_hpronz_CLAIM.md` (new)

`pf_bridge`:
- `notes_to_chief/20260831_0343_LANE-B-STATUS-149wbp-owner-string-debt-closed-with-a-runtime-py-tripwire.md`
  (new)
- `rounds/B_20260831_0343_hpronz_gt124_owner_string_tripwire_closes_149wbp_debt.md` (this file, new)

## Numbers measured

- `tests/test_mob_pickup.py` alone: 79 passed, 77 subtests passed (was 78/76 before this round's one new
  test method; the new method contributes 1 test and 0 subtests -- it has no `subTest` blocks).
- Full `pirate-force-server` suite after the change: **5627 passed, 327 skipped, 9733 subtests passed, 0
  failed** (176.16s). Round `upf0xp`'s own last measured baseline was 5608 passed / 323 skipped, before
  the merge of PR #556 (LANE-GM round `b3fgm6`, unrelated lane) landed on `main` between that round and
  this one -- the +19 passed / +4 skipped delta is that merge, not this round's one added test; this
  round's own contribution is exactly +1 passed, +0 skipped, +0 failed.
- `_call_names("runtime")` measured today: does not contain `pickup_and_persist`, `dispatch_pickup_
  request`, `resolve_claim`, or `place_in_bag` -- 0 of the four GT-124-adjacent symbols are called.
- Mailbox: 0 letters newly addressed to LANE-B since round `upf0xp`'s 02:41 cutoff (checked
  `20260831_0245` through `20260831_0330`, all GM-lane or COO-to-GM correspondence, none `ADDRESSEE:
  LANE-B` and none answering a letter LANE-B opened); 1 status letter written this round, 0 new RE/GT
  tickets opened.

## CORE-REQUEST

None. This round touches no `runtime.py`/`app.py` line and asks for none.

## Tickets opened for other lanes

None.
