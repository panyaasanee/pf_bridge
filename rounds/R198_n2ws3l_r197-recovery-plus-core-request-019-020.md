# R198 (session n2ws3l) — 2026-08-27 ~19:5x-20:1x (+07:00)

## §2 item 7 check: previous round's own PR

`pf_bridge#227` (R197): `merged=true`. `pirate-force-server#140` (R197): `merged=false` --
gate RED, closed automatically by `merge-claude-pr.yml`. Root cause found below. Branch
`claude/awesome-darwin-kjtyku` was kept (workflow promise honored); recovered by cherry-pick.

## Part 1: recovering R197's lost server-side work

`pirate-force-server#140`'s gate died on `pytest_subset` / `tools/pf_multiplayer_readiness_audit.py`:
its `X03` guard asserts exactly 2 occurrences of
`raise PermissionError("stale or non-owning character session")` in `store.py`. R197's own
`CORE-REQUEST-018` fix (the `write_position=False` branch, added on pf-adversary's own advice to
keep the ownership check even when skipping the write) legitimately added a third, independent
occurrence of that raise -- the guard was correct to flag it as drift, R197 just never ran the
audit tool locally before pushing.

Cherry-picked `9c920f4`/`fe89b55` from `claude/awesome-darwin-kjtyku` cleanly onto this round's
branch (rebased onto current `main`, which had advanced past R197 via LANE-GM's PR#141 merge).
Bumped `X03`'s expected count 2 -> 3 in the audit tool, with a one-line comment naming the cause.
Added a matching "Re-pin, chief round n2ws3l" paragraph to
`reports/PF_MULTIPLAYER_READINESS_AUDIT001_SINGLE_PLAYER_ASSUMPTIONS_20260818.md` (same convention
as round 176's precedent) -- the frozen HEAD-`5cc0eda` table itself is untouched by design.

`pf-adversary` (real subagent call) confirmed the fix is correct, not a paper-over: verified by
reverting only the pin edit and reproducing the exact drift message, confirmed the new occurrence
is a genuinely independent crash chain (not a text duplicate of the existing write-path check),
and confirmed no TOCTOU in the new SELECT-based ownership check. It also caught that I had not
added the report re-pin paragraph before its review pass -- added afterward, in the same commit.

`python3 tools/pf_multiplayer_readiness_audit.py` no longer lists `X03` as drifted.
`tests/test_multiplayer_readiness_audit.py`: 26 passed, 4 skipped (all declared preconditions).
Full non-GameClient/non-capture_v141 pytest subset: 2673 passed, 8 skipped, all skips declared.

## Part 2: CORE-REQUEST-019 (LANE-A, Columbus quest 3205 / option 2)

Per duty order Section 17 item 3, this was flagged by R197 as next round's top priority (item 3/3
of `COO-DECISION 1746`). Letter:
`notes_to_chief/20260827_1848_LANE-A-CORE-REQUEST-019-wire-columbus-quest3205-option2.md`.

Lane A built `columbus_quest_dispatch.make_columbus_conversation_two_options()`,
`matches_columbus_bornagain_dispatch()`, `dispatch_columbus_quest3205()` (always refuses today,
named reason `BORNAGAIN_MARKER_RESET_REFUSED_NO_PERSISTENCE_ROW` -- no persisted home-marker
column exists yet). Wired into `runtime.py`'s `_dispatch_columbus_quest3021`:

1. The `ChooseNPC` branch now composes the two-option conversation instead of the single-option one.
2. The `QuestOperateVital` branch gained a parallel `elif` for op1/quest 3205, with its own
   independent per-session latch (`columbus_quest3205_dispatch_attempted`) -- NOT shared with
   3021's latch, so a player can attempt either option regardless of order or of the other's
   outcome. The outer gate widened from `not attempted3021` to
   `not attempted3021 or not attempted3205` to allow this.

Added 4 new tests to `tests/test_columbus_quest_dispatch_wiring.py`: the two-option conversation
carries both quest tags; op1/3205 refuses with the named reason and does not touch 3021's latch;
op1/3021 still works unchanged (regression guard); both options dispatch independently in either
order. All 40 tests in that file plus `test_columbus_quest_dispatch.py` pass.

`pf-adversary` (real subagent call) found no correctness defect, confirmed the census-membership
gate and the "both options visible, one always refusing" design are unaffected/intentional, and
mentally mutated each new test to confirm none are vacuous. It did flag one real, non-blocking
side effect: widening the outer gate to an OR means a session that completes 3021 but never
deliberately triggers 3205 keeps parsing and checking every later `QuestOperateVital` frame (any
quest) for the rest of that session, instead of the early exit the pre-widening gate gave 3021
alone. No wrong output, not client-visible (a parse + two dict-key checks per frame). Accepted for
now, documented in `_dispatch_columbus_quest3021`'s own docstring rather than fixed this round --
decoupling the two latches from one shared outer gate is a real design question, not an emergency.
It also flagged the function's docstring hadn't been updated for the new quest -- fixed in a
follow-up commit.

Item 3/3 of `COO-DECISION 1746` is now wired (items 1 (`CORE-REQUEST-018`) and 2
(`RE-096`/`RE-103`, both closed bounded-negative earlier) were already done). **This does not mean
M2 can be announced passed** -- that still needs an attended `GT-106` confirmation, per the
decision's own text.

## Part 3: CORE-REQUEST-020 (LANE-GM, `field_0x0b_second=1`)

Letter: `notes_to_chief/20260827_1933_LANE-GM-CORE-REQUEST-020-set-plus0x15-field-to-1.md`.
RE-089 (reconfirmed by RE-104) proved the client's update path gates the `BT_GM` button's
visibility on wire byte `+0x15 == 1`; `runtime.py`'s GM-state-after-login call site was sending
that field as a literal `0` always, so the gate the client checks was always false. Changed the
literal argument tuple from `0, 0, 0` to `0, 1, 0` at the exact call site the letter named
(`runtime.py` ~4979-4986, inside the `CORE-REQUEST-016` block).

The letter's own author (LANE-GM) identified that `tests/test_gm_login_state_guard.py`'s
`test_a_gm_account_gets_the_re105_pinned_state_frame` hardcodes the expected frame bytes with the
old `(0, 0, 0, 0)` tuple and would go red the instant this landed, and proposed fixing it
themselves "in the same round chief pushes" -- but LANE-GM's own round runs on a separate cadence
from this one, and shipping this change with a known-red test in the same PR would have been
exactly the kind of self-inflicted gate failure Part 1 of this round just recovered from. Fixed
`tests/test_gm_login_state_guard.py`'s hardcode myself in the same commit instead (`(0, 0, 1, 0)`)
so the PR the gate actually sees is green, and will tell LANE-GM in the reply letter that this is
already done rather than theirs to do next round.

`tests/test_gm_login_state_guard.py`, `tests/test_gm_state_wire.py`, `tests/test_gm_dispatch.py`:
16 passed.

**This does not close the GM login block by itself** -- `RE-113` (GT-107's `28317
GSCN_RunTimeProtocolRes` error, `pirate-force-server#141`, not yet merged) still has to land too
before the owner's `gm_accounts` login is safe to retry (per the letter's own note, same rule as
GT-101/GT-107).

## Verification before push

`python3 tools/verify_hypothesis_ledger.py`: `PASS entries=47`, no drift.
`python3 tools/pf_multiplayer_readiness_audit.py`: no drift besides the pre-existing, declared
shallow-clone historical-pin gap (documented in `.github/workflows/README_GATE_CI.md` as a known
sandbox limitation, not something this round introduced).
Full non-GameClient/non-capture_v141 pytest subset re-run after all changes: 2677 passed, 8
skipped, all skips declared preconditions, 0 failed. green(cloud sanity).

Pushed to `pirate-force-server@claude/awesome-darwin-n2ws3l`. One process note: pushed the
round-claim commit first (per §2), then ran `git pull --rebase origin main` out of habit --
exactly the mistake R189's own recorded lesson warns against ("push WIP แล้วห้าม rebase อีก").
Recovered per that same lesson: `git merge origin/<branch>` (not a second rebase, not a force
push -- force push is banned unconditionally by this project's own rules) reconciled the two
histories with no conflicts, since the diverged commit was itself an empty round-claim commit.

## WIRED v2

Unchanged, 9/10 -- neither Columbus quest dispatch nor the GM state-frame field is one of the 10
counted lanes (same precedent as R192/R196 for this same dispatch tree).

## GAME_TEST_QUEUE.md

No new entry this round. Both changes are either a refusal path with a named reason (3205, no
client-visible success state to test yet) or feed into the existing `GT-107`/RE-113-gated GM login
block (`field_0x0b_second`), which already has an open queue item. Noted in the reply letters
instead.

## Outstanding

- `RE-112` closed BOUNDED-NEGATIVE mid-round by Lane A's own RE runner (letter `1947`, consumed
  below): no client ack found after `Player.ResetMarker`/`Q_BORNAGAIN` -- confirms
  `dispatch_columbus_quest3205`'s always-refuse design is correct, not provisional.
- `pirate-force-server#141` (`RE-113`, GT-107's 28317 fix) not yet merged -- blocks GM account
  re-entry alongside CORE-REQUEST-020.
- The outer-gate early-exit regression pf-adversary flagged (Part 2) -- documented, not fixed.
- CHIEF_CONTINUATION.md/AGENTS.md size housekeeping -- deferred again (R193-R197's same reasoning:
  too risky to combine with code-heavy rounds). Attempted separately this round if time remains
  (see the housekeeping PR, if one exists for this round).
- Mailbox backlog: chief-owned slice still large; this round only consumed the two letters tied to
  the code work (CORE-REQUEST-019/020) plus their own replies -- no bulk pass attempted.
