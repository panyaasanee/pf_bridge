# LANE-CS round ihygdf -- 2026-09-09T16:41+07:00 to 2026-09-09T17:10+07:00 (approx)

## clock check
Bridge heartbeat last line at round start: `2026-09-09T16:36:02+07:00`. My
own clock at claim time: `2026-09-09T16:41+07:00`. 5 minutes apart -- within
tolerance, no bridge stall to report.

## lock
`pf_bridge#2001` `[LANE-CS] round ihygdf: claim` opened before touching any
code (list repeated at open time: no other `[LANE-CS]` claim PR open; the
only other `[LANE-CS]` PR listed is `#1629`, an old addendum already
carrying its marker per round `ovkikh`'s own notes, not a competing lock).

## picked up from round `ovkikh`'s "next round" list
1. Order pf-adversary for real, as the first task, if the tool is callable
   this session -- three rounds in a row (`cg3nrb`, `ovkikh`, and the
   session before those two) had no Agent/Task tool to call it with.
   **This session has the Agent tool and a `pf-adversary` subagent type.**
   Called it against this round's own diff (see "pf-adversary" below).
2. Old debt from `CS_20260908_2109_mfgv4m_ADVERSARY-RESULT.md`, still
   unpaid: D2, D3, D4, D5, D6, D7, D8.
   - D3 turned out to be **already moot**: round `cg3nrb` (via `PANYA 2220`
     / `COO-DECISION 20260909_1312`) retired the login-list cap D3's
     scenario depended on. `LearningAFifthSkillCollidesWithTheLoginCapTests`
     on `main` already pins the opposite (a fifth skill is sent, not
     refused). Nothing to do here.
   - D2 needs a LANE-DB seam (two store calls, one transaction) and cannot
     be closed from this lane's own write zone. Already escalated in
     `notes_to_chief/20260908_2002_LANE-CS-CORE-REQUEST-learn-and-grant-need-one-transaction.md`,
     still without a `.CONSUMED.txt` -- not re-sent this round (one letter,
     one ask; chief has not picked it up yet).
   - **D4, D5, D6, D7, D8 paid this round** -- see "work done" below.
3. `NOW.md` LANE-CS queue item after `1943`/`2220`/`2150` (all already
   paid): CORE-REQUEST `learn_skill_spend`. The two letters for it
   (`20260908_2109_LANE-CS-CORE-REQUEST-learn-skill-spend-seam.md` and
   `20260908_2002_LANE-CS-CORE-REQUEST-learn-and-grant-need-one-transaction.md`)
   still have no `.CONSUMED.txt` -- still waiting on chief to plug the seam
   in, not this round's to re-create.

## mailbox
`grep -l "^ADDRESSEE: LANE-CS *$" notes_to_chief/*.md` with the
`.md`/`.md.CONSUMED.txt` two-pattern check (`CHIEF-DECISION 20260901_2357`):
zero unconsumed letters addressed to LANE-CS. Nothing to consume this round.

## AGENTS.md section 7
Read in full. Nothing new that changes this round's plan; the standing
rule "a session with the Agent/Task tool must call pf-adversary for real"
is exactly what item 1 above satisfies.

## work done (`pirate-force-server`, `pirate-force-server#1200`)
Two files: `src/pirateforce_foundation/skill_learn_roundtrip.py`,
`tests/test_skill_learn_roundtrip.py`. Four commits (three substantive,
one merge of `origin/main`).

### D4 -- a failed re-read used to be reported as a clean refusal
The exception branch in `learn_skill_round_trip` used to fold
`points_after is None` (the balance re-read after a grant failure ALSO
raising) into `OUTCOME_REFUSED` whenever `points_after < points_before`
was `False` -- which it always is when `points_after` is `None`, since
`None < anything` is never evaluated (the old `spent` boolean required both
sides non-`None`). A refusal promises nothing was spent; this branch could
not promise that. New outcome `OUTCOME_SPEND_STATUS_UNKNOWN` names the
"cannot tell" case. New test
`test_when_the_re_read_itself_fails_the_outcome_says_unknown_not_refused`
drives a fake store whose `get_skill_points` raises on its third call
(after the grant already raised) and pins the new outcome, `points_before`
carried through as the last known value, and `RESULT=NOT_TOLD`.

### D5 -- the AST import pin's own fix still had the shape it was fixing
First pass: `_top_level_import_components` now splits every module-level
import's bound name(s) on `"."` before comparing against the forbidden set,
closing `import pirateforce_foundation.store as _db` (the old code compared
the unsplit string, so `"store" != "pirateforce_foundation.store"` let it
through). New test `test_the_absolute_dotted_form_of_a_forbidden_import_is_also_caught`
proves the shape is caught, against a literal source string (the real
module file does not itself carry the forbidden import).

pf-adversary reviewed this first pass and found the fix's own new comment
overclaimed: the *per-function* half of the same pin (which decides
whether `store`/`runtime`/`app`/`gm`/`lifecycle` is reached from anywhere
but `main()`) still read only `inner.module` for `ast.ImportFrom` nodes --
invisible to `from . import store as _db`, whose bound name lives only in
`alias.name` -- and its own forbidden set there never had `gm`/`lifecycle`
at all. `[measured by pf-adversary]`: adding a non-`main` helper doing
exactly that import to the real module passed the old per-function check
unchanged. Second pass, same round: both the module-level and per-function
checks now share one `_import_bound_components` helper and one
`_FORBIDDEN_IMPORT_COMPONENTS` tuple. New test
`test_a_relative_from_import_inside_a_non_main_helper_is_also_caught`
reproduces the reviewer's exact scenario directly.

### D6 -- the console token echoed the caller's own numbers, not the wire
`headless_token`'s `skill=`/`points=` fields were typed straight from
`result.skill_id`/`result.points_remaining` (the function's own arguments)
rather than the decoded 0x673C record, so a composer bug that put the
wrong values on the wire would still print a token reading `TOLD` with the
caller's numbers -- matching nothing it actually sent. Both fields now come
off `decoded[0].record_u32_0`/`record_u32_8` when a record decoded (falls
back to the argument values only when nothing decoded, which is always
paired with `RESULT=NOT_TOLD`). `cid=` stays argument-sourced on purpose --
this vital's own bytes never carry a character id at all (confirmed by
reading `learn_skill_result_frame.py`'s composer: the record triple is
`skill_id`/`0`/`points_remaining`, and `make_learn_skill_result_response`
builds a session-scoped one-vital collection with no cid field anywhere in
it) -- and the token docstring and a new NONCLAIMS-adjacent note now say so
explicitly instead of the token's own claim implying otherwise. New test
`test_skill_and_points_in_the_token_come_off_the_wire_not_the_fields`
builds a `LearnSkillRoundTrip` whose `skill_id`/`points_remaining` fields
lie relative to its own real `pc`/`frame`, and pins that the token reports
the wire truth.

### D7 -- stale count comment, and an unread constant
(a) "Outcomes. Exactly three" corrected to name all five and explain why
`OUTCOME_SPENT_ON_NOTHING` sits apart from the four declared together.
(b) `RECORD_MEMBERS_ARE_THIS_PROJECTS_DESIGN` had exactly one `git grep`
hit before this round (its own definition). New test
`test_the_record_members_constant_is_read_and_checked_here` is the second
hit: it parses the constant's own text and cross-checks it against a real
encoded record from a real `learn_skill_round_trip` call, so an edit to
either side alone (checked live: mutated `record_u16_4=0` to `=1` at the
real composition site, the new test went red) turns it red.

### D8 -- a docstring read as a client-rendering claim the module disclaims
`LearningAFifthSkillCollidesWithTheLoginCapTests`' history note ("an empty
skill window on screen") was rewritten to say plainly it is a claim about
a Python function's return value, never an observation of any client
screen -- matching this module's own NONCLAIMS, which the old wording
contradicted in prose only (no behavior changed).

## pf-adversary
Called for real this round (Agent tool + `pf-adversary` subagent type both
available). Target: the first two commits of this round's diff (D4/D5/D6
source fix + the D4/D5/D6/D7/D8 test-side commit), in a scratch git
worktree it built and removed itself (`git worktree remove --force` +
`prune`, confirmed clean; `/tmp/pfs`, this round's own checkout, was never
touched by the reviewer, confirmed read-only throughout).

**Verdict: NOT CLEAN -- one MEDIUM, no HIGH.** The finding (D5's fix
overclaiming parity with the per-function AST branch) is detailed under
"D5" above and was paid in the same round, before this PR was opened, as
this round's third commit. The reviewer also flagged one LOW-grade
suspicion not elevated to a defect: `headless_token` only ever indexes
`decoded[0]`, which would silently ignore a hypothetical multi-record wire
payload -- not reachable through the real composer today (it always builds
exactly one `LearnSkillResultRecord`), and not exercised by any test either
way. Left as an open gap, not fixed this round (no code path produces it,
and manufacturing a multi-record composer call to test a code path that
cannot currently occur would be testing a hypothesis, not a measurement).
Full verbatim review is in the agent's own output; this file summarizes it
rather than reproducing it in full to stay under the 12,000-character round
convention for new files, though this is a `_round.md` file, not a new
ticket, so that ceiling does not strictly bind it.

`ADVERSARY_UNAVAILABLE` does NOT apply this round -- this is the first
LANE-CS round in at least three (`cg3nrb`, `ovkikh`, and one before those)
where the tool was actually callable, and it was called and paid inside
the same round rather than deferred.

## tests and gates
- Targeted file after all three commits: `PYTHONPATH=src python3 -m pytest
  tests/test_skill_learn_roundtrip.py -q` = **30 passed** (was 22 before
  this round; +7 new tests: D4's re-read-fails case, D5's two regression
  tests for the bypass and the reviewer's own scenario, D6's wire-vs-fields
  case, D7(b)'s constant reader; one existing test's fixture assumptions
  were not touched).
- Declared siblings: `PYTHONPATH=src python3 -m pytest
  tests/test_skill_grant_wiring.py tests/test_skill_learn_validator.py
  tests/test_skill_learn_wiring.py tests/test_skill_list_at_login.py
  tests/test_learn_skill_result_hypothesis.py -q` = **233 passed, 88
  subtests passed, 0 failed**.
- Full suite, ONE run, on the tree that was actually pushed (merged
  `origin/main` at `2541f97d` first, as the last step before this run, per
  the house rule that the full run must be on the tree that will be
  pushed): `PYTHONPATH=src python3 -m pytest tests/ -q` = **15764 passed,
  446 skipped, 0 failed, 43470 subtests passed** (821.64s / 0:13:41).
  `origin/main` did not move again between this run and the push (checked
  with `git merge-base --is-ancestor origin/main HEAD` immediately before
  pushing).
- `python3 tools_bridge/pf_gate_preflight.py --repo <this checkout>` =
  PASS on every channel (cp874, skips, mainmerge, census, branch,
  bridgesize, queuegrowth, filenamelen, scoreboard-manual, claudecfg,
  consumedstub, modebits, skipdrift).
- `python3 tools_bridge/pf_gate_preflight.py --pr-body <file> --pr-stage
  final` = `[prbody] PASS` (exactly one `PF-AUTOMERGE: v4` line) before
  opening the server PR.

## PR
- Server: `pirate-force-server#1200` -- opened, not draft, `PF-AUTOMERGE:
  v4` present (GET-confirmed after opening). This diff touches only a
  standalone CLI tool for LANE-K's attended queue (`skill_learn_roundtrip`
  has no frame dispatch and no handler; nothing in `runtime.py` calls it,
  unchanged by this PR) -- not the boot line, login, actor identity, or any
  frame a live session sends, so it follows the same non-draft precedent
  round `mfgv4m` itself used for touches to this exact file.
- Bridge claim: `pf_bridge#2001` -- marker added at the end of this round
  to release the lock (GET-confirmed after the edit).

## next round
1. D2 (learn+grant not one transaction) is still open and still not this
   lane's to close alone -- keep watching
   `20260908_2002_LANE-CS-CORE-REQUEST-learn-and-grant-need-one-transaction.md`
   and `20260908_2109_LANE-CS-CORE-REQUEST-learn-skill-spend-seam.md` for a
   `.CONSUMED.txt` from chief; when one lands, that is the next round's
   first task.
2. The reviewer's LOW-grade suspicion (`headless_token`'s `decoded[0]`-only
   handling of a hypothetical multi-record wire payload) is not urgent --
   no code path produces more than one record today -- but is worth a
   defensive `len(decoded) == 1` assertion or an explicit NONCLAIM line the
   next time this file is touched, so it does not silently start mattering
   if the composer ever changes.
3. If neither of the above is actionable, fall back to `## work sammrong`
   (LANE-CS's own reserve queue in `prompts/LANE-CS.md`): promote another
   `hypothesis_*` module, or take an RE/STATIC ticket answerable from
   already-committed gamedata.

SCOREBOARD: COMING | The console tool an attended LANE-K ticket runs to prove a skill was learned (`skill_learn_roundtrip`) now tells the truth about four more failure shapes pf-adversary measured against it (an unreadable balance after a failed grant is reported as "unknown" instead of a false "refused"; its own console line now quotes the bytes it actually composed instead of the caller's input numbers; its own import-safety pin can no longer be walked around by a differently-shaped import; a design constant that nothing read now has a reader) -- not yet player-visible, because this tool is still reachable only from the console, not from any path a login session calls, and the PR is open awaiting the gate, not yet on main. | pirate-force-server#1200 (4 commits incl. merge, preflight PASS, pytest 15764 passed/0 failed on the pushed tree sha 278a64f8, pf-adversary NOT CLEAN->paid same round)
