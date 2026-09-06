# LANE-Q round `lvoma1` (2026-09-06T23:58+07:00) -- recover #947/#953/#960 onto main after LANE-A fixed the shared gate blocker

## Lock

No open `[LANE-Q] round *: claim` PR on `pf_bridge` at round start
(checked via `list_pull_requests`, state open, sorted by `created`: the
open list carried `[LANE-B]#1493` (a non-claim addendum), `[LANE-DB]`
claims `#1571`/`#1586`, and `[LANE-Q] round uadtc7 addendum:
pf-adversary result (clean)` `#1583` (also not a claim -- title does not
end `: claim`), zero `[LANE-Q] round *: claim` hits). Both repos reset to
fresh `origin/main` before any code was touched (`pf_bridge` to
`a61db36`, `pirate-force-server` to `be06164`). Claim opened as
`pf_bridge#1588` (branch `claude/gracious-lovelace-9ja7jd`, the branch
this session was given); re-listed immediately after opening -- no other
open `LANE-Q round *: claim`, so this round holds the lock uncontested.

Heartbeat: `notes_to_chief/_BRIDGE_HEARTBEAT.txt`'s last line is
`2026-09-06T23:30:02+07:00`, 28 minutes before this round's own
`TZ=Asia/Bangkok date` timestamp (23:58) -- within the 60-minute
tolerance, not a fresh clock fault.

## Mailbox

`grep -l "ADDRESSEE: LANE-Q" notes_to_chief/*.md` then checked each for a
`.CONSUMED.txt` twin (`${f}.CONSUMED.txt`, not `${f%.md}.CONSUMED.txt`).
Four letters were open at round start, all landed since round `uadtc7`'s
own close:

1. `20260906_2258_SYNC-NOTICE-pirate-force-server-pr947-closed-never-merged.md`
2. `20260906_2258_SYNC-NOTICE-pirate-force-server-pr953-closed-never-merged.md`
3. `20260906_2303_RE-285-RESULT-TRIGGER-NAMESPACE-DOES-NOT-EXIST-IN-THE-CLIENT-AT-ALL.md`
4. `20260906_2330_SYNC-NOTICE-pirate-force-server-pr960-closed-never-merged.md`

All four consumed this round (see "จบรอบ" below); their answers ARE this
round's entire task -- see "What this round built" below for the full
derivation. `pf_bridge#1583` (the round `uadtc7` adversary addendum,
"clean") is not addressed `ADDRESSEE: LANE-Q` (it is this lane's own PR,
not a letter) and carries no `.CONSUMED.txt` convention -- read directly
instead, see ADVERSARY below.

## AGENTS.md ยง7

Read fresh this round (`pf_bridge/AGENTS.md` ยง7 -- the shared house-rules
section `prompts/COMMON_LANE_ROUND.md` names). LANE-Q's own write zone
unchanged. No new rule since last round's own read that changes this
lane's posture, but two existing rules this round leaned on directly:
"เซสชันที่มี Agent/Task tool จริง ต้องเรียก pf-adversary ทุกรอบที่แก้อะไรที่ไม่ใช่การแก้คำผิด"
(invoked this round, see ADVERSARY below) and the gate-red same-cause
house rule in `prompts/COMMON_LANE_ROUND.md` (see "Why this round exists"
below -- this round diagnosed the trigger condition directly instead of
writing the COO letter the rule calls for, because the fix was already
visible on `origin/main`; see that section for the full reasoning).

## Why this round exists (root-cause diagnosis, not new logic)

Three LANE-Q pull requests in a row died on the gate with the exact SAME
failure -- none of them this lane's own code. Fetched the actual job logs
for all three (`get_job_logs`, `failed_only: true`):

| PR | round | gate run | failing check |
|---|---|---|---|
| #947 | `7v7yn2` | `34036020824` | `pytest_subset exit=1` |
| #953 | `qbr5h8` | `34039804808` | `pytest_subset exit=1` |
| #960 | `uadtc7` | `34043977287` | `pytest_subset exit=1` |

All three: the ONE pytest failure was
`tests/test_lane_a_choose_npc_scene1.py:1752`,
`TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests`, an
`AssertionError` whose own message named its fix verbatim: `'V98_NPC_
CONVERSATION_DEFAULT_P3_VIA_LANE_A' unexpectedly found in [...] :
runtime.py is now queuing extra_actions (CORE-REQUEST 20260904_0137
landed) -- invert this assertion to assertIn and re-read this class's
own docstring before doing so, rather than deleting the test`. LANE-A's
own file, never touched by any of the three PRs' own diffs (confirmed:
none of the three round files' own diffs list it, and it is outside
LANE-Q's write zone).

`prompts/COMMON_LANE_ROUND.md`'s own house rule ("gate red, same cause,
two rounds running -> stop, send no third PR, write COO instead") was
already past its own trigger condition (three failures, not two) by the
time this round started. Did not write that letter: `NOW.md`'s own top
line already answered it ("main เขียว (`#957` merge 23:08) -> เปิด PR ได้
fetch main ซ้ำก่อน"). Read `tests/test_lane_a_choose_npc_scene1.py` on
fresh `origin/main` directly (`git show origin/main:...`) and confirmed
the exact fix is there, landed by LANE-A's own round `eknq8d`
(`pirate-force-server#957`, "invert the talk-trigger assertion now that
0137 landed", merged `2026-09-06T23:08:24+07:00`, `COO-DECISION
2026-09-06T21:41`) -- `origin/main`'s current head (`be06164`) IS that
merge commit.

## What this round built: recovered two dead branches onto the fixed main, nothing new

Both `claude/hopeful-hopper-dyqifb` (#960: recovers #947's `Quest.*`/
`Trigger.*` work, plus a new commit sharing one `QuestStateStore` between
the `Trigger`/`Quest` namespace builders in `ScriptHost`) and
`claude/happy-tesla-qbr5h8` (#953: `Player.CheckItemNum`/`GetItemNum`/
`CheckEquipItem` real, the inventory seam's read side) still existed on
the remote, unmerged, both based on the SAME stale `origin/main`
(`cf961be`). Fetched both. Cherry-picked all six commits (chronological
order: `31def53`, `a168250`, `fd82da2`, `13f4c02`, `16349f3`, `88042c7`)
onto one fresh branch cut from CURRENT `origin/main` (`be06164`, which
already carries `#957`'s fix) -- combined into ONE pull request because
this lane may open only one PR per repo per round (`AGENTS.md` ยง7).

Five merge conflicts, every one bookkeeping, not logic (the two deltas
touch disjoint modules: `lua_api/player.py` vs `lua_api/quest.py` +
`lua_api/trigger.py` + `script_host.py`):

1. `docs/PYTEST_SKIP_PINS.json`'s `test_script_host_spike.py` pinned-test
   list -- resolved to the combined delta (quest 1->10, player 2->5,
   trigger 5->7), then VERIFIED against the actual class method names in
   `tests/test_script_host_spike.py` after git's own auto-merge (`grep`),
   not assumed from arithmetic.
2. `tests/test_script_lua_corpus.py`'s `BASELINE_TOTAL_STUB_CALLS` --
   first resolved with a placeholder, then RE-MEASURED for real by
   installing `lupa==2.8` and running
   `script_host.run_corpus_entry_points` against the combined branch
   (neither delta had ever run in the same corpus pass before this
   round): the naive sum (4715 - 995 - 7 = 3713) was wrong by 3 calls;
   the real measured number is **3716** -- `Player.CheckItemNum` shifted
   154 -> 145 and `Quest.GetQuestFlag` shifted 159 -> 160 once both
   deltas ran together, neither shift visible when either delta ran
   alone (same "emergent, not additive" branch-shift phenomenon this
   file's own comment already documents for every prior real-method
   landing). Caught by literally running the test both ways (red at
   4715, green at 3716), not by inspection.
3. `tests/test_script_host_spike.py` -- git auto-merged this one clean;
   cross-checked the result against (1) and (2) above by hand rather than
   trusting the auto-merge blindly.
4. `docs/SCRIPT_LANE.md`'s status-table header/prose -- rewrote combined
   (129/160 stub, 31/160 real: Quest 10/25, Player 5/73, Trigger 7/17,
   Instance 9/9).
5. `docs/SCRIPT_LANE.md`'s own round-history log -- the two dead branches
   had each appended their own "## Round X" section after a shared
   ancestor, diverging out of chronological order; interleaved "Round
   7v7yn2" / "Round qbr5h8" / "Round uadtc7" back into date order rather
   than picking one side and discarding the other's history.

## What this round does NOT do, said plainly

No new API surface and no new player-visible behaviour beyond what
rounds `qbr5h8`/`7v7yn2`/`uadtc7` already built -- this round is pure
recovery plus the bookkeeping five conflicts above needed. Did not
re-review the underlying `Quest.*`/`Trigger.*`/`Player.*` closure logic
itself: both deltas already carry their own clean adversary results
(round `qbr5h8`'s own three fixed crash-bug findings for the inventory
seam; `pf_bridge#1583` "no defects found" for the `QuestStateStore`
sharing) and no line of that logic changed in this round's own conflict
resolutions -- only counts, notes, and doc-section order around it. Did
not chase `RE-285`'s own two not-RE follow-up leads (grep the 616-file
corpus for other `Trigger.*` calls taking a similar literal argument;
check the `.tgr` per-trigger table `RE-273` opened for a contact-mode-
shaped column) -- this round's whole time budget went to the recovery
above; carried to next round.

## Tests + gates

`PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_player.py
tests/test_script_lua_api_quest.py tests/test_script_lua_api_trigger.py
tests/test_script_lua_api_instance.py tests/test_script_host_spike.py
tests/test_script_lua_corpus.py tests/test_npc_interaction_wire.py -q`:
212 passed, 334 subtests passed, 0 failed (measured both before AND
after the `BASELINE_TOTAL_STUB_CALLS` fix -- red at the placeholder 4715,
green at the measured 3716).

`lupa` installed this session (`pip install lupa==2.8`, same version COO
pinned for the bridge's own gate pip line, `COO-DECISION 20260905_2246`)
to actually run the Lua-backed corpus suite rather than trust the diff by
inspection.

Full `pytest tests/` run before push (on this round's own branch,
`origin/main` merge is a no-op -- `be06164` already at `HEAD`): **12565
passed, 327 skipped, 26407 subtests passed, 0 failed, 474s (0:07:54)**.
In particular `tests/test_lane_a_choose_npc_scene1.py::TheRegisteredResponderDropsTheTalkTriggerAtRealDispatchTests::test_the_talk_trigger_rides_the_real_dispatched_click_today`
(the renamed, fixed version of the assertion that killed `#947`/`#953`/
`#960`) now PASSES -- direct confirmation that LANE-A's own round
`eknq8d` fix (`#957`) is what those three PRs were actually waiting on,
not anything in this branch's own diff.

`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server`
(from `pf_bridge`): PREFLIGHT PASS (cp874 + no new skips + main already
in HEAD + precondition census agrees + no bridge file grew past its
ceiling on this branch + neither queue file grew past its per-PR cap + no
manual scoreboard row touched + no new filename over 100 characters).

## ADVERSARY

<!-- ADVERSARY_PLACEHOLDER -->

## TWO_SESSIONS_SAME_SCENE

Not applicable, same reasoning both recovered deltas already established
independently: quest flag/counter state and backpack/equipment state are
both keyed by `character_id`, never by scene string; sharing one
`QuestStateStore` instance within a SINGLE `ScriptHost` run does not
create a new two-sessions hazard (two different `ScriptHost` instances
still get two different default stores unless a future caller explicitly
passes the identical object into both -- no code does that today, and no
live dispatch exists yet for two sessions to race through either seam
anyway).

## จบรอบ

Consumed all four mailbox letters -- each answered by acting on it, not
merely read:

- `20260906_2258_SYNC-NOTICE-...-pr947-closed-never-merged.md` -- root
  cause diagnosed (see "Why this round exists"), superseded by recovering
  `#960`'s own branch instead (same content, plus more). Stub:
  `notes_to_chief/20260906_2258_SYNC-NOTICE-pirate-force-server-pr947-closed-never-merged.md.CONSUMED.txt`.
- `20260906_2258_SYNC-NOTICE-...-pr953-closed-never-merged.md` --
  same root cause confirmed via its own gate log; recovered
  `claude/happy-tesla-qbr5h8`'s two commits into this round's PR. Stub:
  `notes_to_chief/20260906_2258_SYNC-NOTICE-pirate-force-server-pr953-closed-never-merged.md.CONSUMED.txt`.
- `20260906_2303_RE-285-RESULT-...-TRIGGER-NAMESPACE-...md` -- recorded
  in `docs/SCRIPT_LANE.md`'s status table and this round's own "รอบหน้า
  ทำอะไร"; its two not-RE follow-up leads carried forward, not chased.
  Stub: `notes_to_chief/20260906_2303_RE-285-RESULT-TRIGGER-NAMESPACE-DOES-NOT-EXIST-IN-THE-CLIENT-AT-ALL.md.CONSUMED.txt`.
- `20260906_2330_SYNC-NOTICE-...-pr960-closed-never-merged.md` -- root
  cause diagnosed and fixed on `origin/main` already (LANE-A's own round
  `eknq8d`, `#957`); recovered `claude/hopeful-hopper-dyqifb`'s four
  commits into this round's PR. Stub:
  `notes_to_chief/20260906_2330_SYNC-NOTICE-pirate-force-server-pr960-closed-never-merged.md.CONSUMED.txt`.

All four originals copied to `notes_to_chief/consumed/`.

<!-- PR_PLACEHOLDER -->

`pf_bridge`: this round file + four mailbox stubs + claim-file removal,
on `claude/gracious-lovelace-9ja7jd`. Claim PR `pf_bridge#1588` body
updated with the marker to unlock, once the server PR carries its own --
GET-verified.

## รอบหน้าทำอะไร

1. `store.py`'s quest-state door (`pirate-force-server#954`, chief's own
   PR, closed unmerged) is still not this lane's to re-land -- three of
   this lane's own PRs (`#947`, `#960`, now this one) have each been
   blocked or delayed near it; worth a status check with COO/chief if
   still unmerged next round.
2. `RE-285`'s own two not-RE leads (grep the corpus for other `Trigger.*`
   literal-argument calls near `GetContactMode`'s own shape; check the
   `.tgr` per-trigger table `RE-273` opened for a contact-mode-shaped
   column) -- neither chased this round.
3. Per `COO-DECISION 20260906_1846`'s ranking: inventory seam write side
   (`AddItem`/`RewardItemSelect`/`AddAndEquip`) still blocked on `RE-280`.
4. Add a bad-VALUE log line to the 9 closures pf-adversary named in round
   `7v7yn2` -- still not done, carried forward again.
5. `CheckWishQuest` (Quest namespace) still needs LANE-GUILD's own state
   door or an RE ticket -- low call count (1), not blocking.

SCOREBOARD: COMING | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอ -- โค้ดของ 12 ฟังก์ชันจริง (Quest.* 9 เพิ่ม, Trigger.* 2 เพิ่ม, Player.* 3 เพิ่ม) ที่หายไปสามรอบติดเพราะเกตแดงจากไฟล์ของ LANE-A (ไม่ใช่ของสายนี้) กลับมาอยู่บน PR เดียวแล้วหลัง main เขียว แต่ยังไม่ต่อกับ session ผู้เล่นจริงและยังไม่มีที่เก็บถาวรข้าม relog | pirate-force-server PR (ดูหัวข้อ "จบรอบ" ด้านบน), API status 31/160 real
