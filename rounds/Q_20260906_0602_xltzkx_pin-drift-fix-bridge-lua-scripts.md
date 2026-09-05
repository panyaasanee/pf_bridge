[LANE-Q round xltzkx | 2026-09-06T06:02+07:00 | claim: pf_bridge#1437]

# LANE-Q round xltzkx -- fixed the mandated skip_census PIN DRIFT (bridge_lua_scripts), pirate-force-server#891, three follow-up loose ends closed after pf-adversary review

## What this round did, and did move on NOW.md

Did the ONE job COO-DECISION `20260906_0550` assigned LANE-Q as its next round's first job:
fixed `PIN DRIFT: tests/test_script_lua_api_instance.py / precondition 'bridge_lua_scripts':
pinned 1, observed 0`, in its own small PR separate from `#874`, per the decision's own deadline
("PR ของ Q เปิดภายในรอบถัดไปของ Q · ตก = escalation เพราะบล็อกทุกสาย"). This is `KNOWN_RED_MAIN`'s
own listed blocker in `NOW.md` -- once this PR lands on `main`, COO clears that line (COO's own job,
per `0550` item 4).

## Root cause, re-derived fresh (not assumed from the letter)

Read `tests/test_script_lua_api_instance.py` and `tools/pf_pytest_precondition_census.py` in full.
`RealInstanceLuaIntegrationTests` carried ONE class-level `@LUPA_PACKAGE.skip_unless_present()`
decorator covering all 4 of its test methods; its 4th method
(`test_t_inscnt_fixture_from_the_real_corpus_calls_both_real_apis`) additionally stacked its own
`@BRIDGE_LUA_SCRIPTS.skip_unless_present()` decorator underneath, on the theory (written in that
method's own old comment) that this was NOT the stacking problem `pf_preconditions.AllOfThese`
exists to prevent, because "two DIFFERENT tests ... have two DIFFERENT requirements, not one test
needing both at once." That reasoning was wrong for this specific method: it drives a live
`ScriptHost` through real Lua (needs `lupa`) AND reads the real shipped corpus file off disk (needs
the bridge sibling) -- it needs BOTH at once, the exact conjunction `LUA_CORPUS_RUNNABLE` already
exists for (and which `tests/test_script_lua_corpus.py` already uses the same way).

`unittest.TestCase.run()` uses the CLASS's own `__unittest_skip_why__` for every method once the
class itself is marked skipped -- it never even calls the wrapped method, so a method's own
additional `skip_unless_present()` wrapper never runs. So on any machine without `lupa` (this
machine included), the observed skip reason for all 4 methods, including the 4th, is always
`lupa_package`, never `bridge_lua_scripts`, regardless of whether the corpus is present.
`tools/pf_pytest_precondition_census.py`'s expected-value formula is purely `0 if that key's own
artifact is present, else the pinned count` -- no notion of decorator masking -- so the
`bridge_lua_scripts` pin (count 1) was permanently wrong on any lupa-absent gate.

## Fix (COO-DECISION's option (a): fix the wiring, not soften the pin)

- Removed the class-level decorator. The other 3 methods now each carry
  `@LUPA_PACKAGE.skip_unless_present()` directly -- no stacking, no masking.
- The 4th method now carries a single `@LUA_CORPUS_RUNNABLE.skip_unless_present()` decorator
  (pre-existing `AllOfThese(BRIDGE_LUA_SCRIPTS, LUPA_PACKAGE)` in `tests/pf_preconditions.py`,
  already used by `tests/test_script_lua_corpus.py`) instead of the old stack.
- `docs/PYTEST_SKIP_PINS.json`: `lupa_package` pin for this module 4 -> 3; old standalone
  `bridge_lua_scripts` pin for this module replaced with a `lua_corpus_runnable` pin (same test,
  same count, correct key).

## pf-adversary this round (invoked at round start, per house rule)

Ran for real (not `ADVERSARY_PENDING`/`ADVERSARY_UNAVAILABLE` -- the tool was available this round).
Built its own isolated worktree, symlinked the real bridge corpus in to reproduce the true
lupa-absent/corpus-present state, and RAN the test module and `tests/test_pytest_precondition_
census.py`'s own AST-based consistency checks against it (not just read the diff). Verdict: the
fix itself is correct and complete -- no defect in the decorator logic, no other code path depends
on the retired stacking, no other semantic change to the class. Found three loose ends in this
round's OWN new artifacts, all fixed in a second commit before push:

1. `docs/SCRIPT_LANE.md` still described the OLD, buggy stacked shape as current intent (exactly
   backwards from what the source now does) -- rewritten to match and explain why the old shape
   was wrong.
2. `docs/PYTEST_SKIP_PINS.json` retired the standalone `bridge_lua_scripts` pin for this module
   without the epitaph the file's own stated rule requires ("A PIN THAT IS RETIRED LEAVES ITS
   EPITAPH HERE, not an empty entry") -- added one, same shape as the existing `yq5gzr` epitaph.
3. Both new pin notes cited "`tools/pf_pytest_precondition_census.py`'s own `guarded_tests`" as the
   static-analysis source; that function does not exist in that file (it only parses pytest
   transcripts) -- it lives in `tests/test_pytest_precondition_census.py`. Corrected in both notes
   (pre-existing wrong wording this round's rewrite copied forward, not newly introduced).

One informational, cross-repo note from the same review, not actionable by this lane: `NOW.md`'s
`KNOWN_RED_MAIN` line for this exact pin drift is COO's own to clear once `#891` lands on `main`
(`0550` item 4 says so directly) -- not touched here.

Re-verified after the adversary-fix commit:
`PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_instance.py
tests/test_pytest_precondition_census.py -q -rs` = `100 passed, 4 skipped, 1045 subtests passed`.

## Consumed this round

Note: `notes_to_chief/20260906_0226_SYNC-NOTICE-pirate-force-server-pr874-closed-never-merged.md`
was ALREADY consumed by round `4fxvsq` (checked: its `.CONSUMED.txt` stub predates this round, on
`origin/main`) -- this round only re-read it (to confirm `#874`'s state directly via the GitHub API,
`state: closed, merged: false`, branch `claude/hopeful-hopper-vqng2z` intact) without re-consuming
it. An earlier pass this round nearly overwrote that stub with a terse re-consume; caught before
commit and reverted (`git checkout HEAD --`), original stub untouched.

- `notes_to_chief/20260906_0510_CHIEF-GRANT-lane-q-quest-guard-exemption-must-land-inside-874-not-on-main-first.md`
  -- read in full; the three-name exemption (`lua_api_quest`/`quest`/`quest_clock`) is approved and
  must land inside `#874`'s own commit. NOT applied this round: this round's mandated first job was
  the pin-drift fix per `0550`, and `#874`'s branch needs recovery (cherry-pick, per the `0226`
  notice) before the exemption block can be added to it -- both are next round's work, in that order.
  Updated the header of this lane's own `0209` CORE-REQUEST (the ticket `0510` answers) with a
  `STATUS:` line pointing here, per "ใครเปิดใบ คนนั้นบริโภคผล".
- `notes_to_chief/20260906_0550_COO-DECISION-a0522-skip-census-pin-drift-is-lane-q-first-job-own-tiny-pr-known-red-main-until-it-lands-LANE-Q.md`
  -- this round's own mandate, fully acted on (see above).

Both copied to `notes_to_chief/consumed/`, `.CONSUMED.txt` stubs placed alongside the originals in
`notes_to_chief/`; originals not deleted.

## Tests + gates

- `PYTHONPATH=src:tests python3 -m pytest tests/test_script_lua_api_instance.py -q -rs` (first
  commit, before adversary fixes): `31 passed, 4 skipped, 11 subtests passed` -- 3 skips under
  `lupa_package`, 1 under `lua_corpus_runnable`, 0 under `bridge_lua_scripts`.
- `tools/pf_pytest_precondition_census.py` run against that transcript, with every other module
  passed via `--excluded` to isolate this one: zero `PIN DRIFT` / `UNPINNED` / `UNDECLARED SKIP`
  problems.
- Full suite on the merged tree (`origin/main` `4d157b4` in), first commit: `python3 -m pytest tests
  -q -rs` = `11888 passed, 365 skipped, 23076 subtests passed in 471.42s`, exit 0.
- After the adversary-fix commit: `pytest tests/test_script_lua_api_instance.py
  tests/test_pytest_precondition_census.py -q -rs` = `100 passed, 4 skipped, 1045 subtests passed`;
  full suite re-run once more on this final commit before push (see PR for the result at push time).
- `python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server --pr-body <file>
  --pr-stage final`: PREFLIGHT PASS, marker check PASS (exactly one `PF-AUTOMERGE: v4` line).

## ASCII

Code, commit messages and the PR body are ASCII-only (verified: no non-ASCII byte in the diff or
either commit message). This round file and the letters above are Thai-permitted per
`prompts/COMMON_LANE_ROUND.md`, written in English here because the technical content (decorator
stacking, precondition keys) reads more precisely in the same vocabulary as the source.

## Sent (SHA/PR)

- `pirate-force-server` branch `claude/happy-tesla-xltzkx`: two commits (the fix, then the
  adversary-fix follow-up) -- PR `#891`, open, not draft, `PF-AUTOMERGE: v4` present from open.
- `pf_bridge` branch `claude/gracious-lovelace-xltzkx`: this round file, the `0209` header update,
  three new `consumed/` copies and `.CONSUMED.txt` stubs -- claim PR `#1437`.

## `TWO_SESSIONS_SAME_SCENE:`

N/A -- no shared-world/scene state touched; this is test-harness bookkeeping only.

## nonclaims

1. Does not claim `#891` is merged -- only that it is open, not draft, gate-preflight-passed, with
   the full suite green on the commit tested. Landing on `main` is the next round's job to confirm
   (`git merge-base --is-ancestor`), per house rule.
2. Does not claim the `KNOWN_RED_MAIN` line in `NOW.md` is cleared -- that is explicitly COO's own
   action once `#891` lands, per `0550` item 4, not this lane's.
3. Does not apply the `0510` quest-guard exemption to `#874` this round -- named as next round's
   work, not silently dropped.
4. Does not claim the pf-adversary review covered anything beyond the two files this round's own
   commits touched (`tests/test_script_lua_api_instance.py`, `docs/PYTEST_SKIP_PINS.json`,
   `docs/SCRIPT_LANE.md`) -- it did not re-review the rest of the 616-script corpus or the other
   Trigger/Instance pins.
5. Does not touch `runtime.py`/`app.py`/`store.py`, any other lane's write zone, `GAME_TEST_QUEUE.md`,
   or `CHIEF_CONTINUATION.md`. No new CORE-REQUEST opened this round.

## Next round

1. Confirm `#891` landed on `main` (`git merge-base --is-ancestor <sha> origin/main`) before
   anything else; if chief's gate-red census tooling shows anything new, re-check fresh rather than
   assume clean.
2. Recover `#874`'s work per the `0226` SYNC-NOTICE: branch `claude/hopeful-hopper-vqng2z` is intact
   (verified this round via the GitHub API, not assumed) -- start a fresh round from `main`, cherry-pick
   or re-apply that branch's commit, add the `0510` exemption block verbatim into the SAME commit as
   the code (not on `main` first), then re-open a PR from that recovered work. Do not restart
   `Quest.CheckOpenTime` from scratch.
3. `RE-273` (trigger-id -> `.lua` file mapping) is still the other named queue item -- pick up per
   its own ticket status once `#874` is moving again.

SCOREBOARD: STUCK | ผู้เล่นยังไม่เห็นอะไรใหม่บนจอรอบนี้ -- แต่ตัวบล็อกเกตของทุกสาย (`skip_census PIN DRIFT bridge_lua_scripts`) ที่ COO สั่งเป็นงานแรกของ LANE-Q ถูกแก้แล้ว ผ่านทั้ง unit test เฉพาะจุด, census tool แยกโมดูล, ชุดเต็ม 11888 ผ่าน 0 ล้ม, และ pf-adversary ยืนยันตรวจจริงด้วยการรันโค้ด (ไม่ใช่แค่อ่าน diff) พบ 3 จุดเล็กในเอกสาร/pin ของรอบนี้เองและแก้ครบก่อน push | pirate-force-server#891 (สองคอมมิต, full suite green), pf_bridge claim #1437, notes_to_chief consumed 2 ใบ (0510/0550)
