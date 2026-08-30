[LANE-B round record | 2026-08-30T14:48+07:00 | branch claude/admiring-galileo-309h1a / claude/friendly-ride-309h1a]

# Round 309h1a: ten fresh COO-DECISION letters consumed, and the wander-11 hunt one of them asked for actually run

## Player-visible difference from yesterday

None from this round's own commits. This round found that everything the ten COO-DECISION
letters ratified was already shipped by earlier LANE-B rounds -- the letters confirm work,
they do not ask for new behaviour. The one net-new thing built (four tests pinning a real,
data-backed finding about self-aggro monsters) has no player-facing effect by itself; it
records a fact for the next round that touches this area, and closes GT-159 as an open
question to a human tester rather than to guesswork.

## Section A (addendum v2) -- last round's PR fate

| repo | last [LANE-B] PR | result |
|---|---|---|
| `pirate-force-server` | #300 (`fxury2`) | merged 2026-08-30T06:37:23Z |
| `pf_bridge` | #491 (`8pliiv`-recovery) | merged 2026-08-30T06:38:42Z |

Both merged. `git pull --rebase origin main` before starting (pirate-force-server was 3
commits behind: PR #312 had landed since). No cherry-pick needed.

## Section B (addendum v2) -- mailbox

First pass with the literal string `ADDRESSEE: LANE-B` found nothing new (all consumed).
That grep is a FALSE NEGATIVE for this project's actual letter format, which uses
`[ถึง: LANE-B | ...]` on line 1, not the literal token `ADDRESSEE: LANE-B` -- worth flagging
for whichever lane owns the addendum wording next. Re-grepped on `^\[ถึง: LANE-B` and found
**ten** unconsumed letters, all `COO-DECISION`s dated `2026-08-30T13:51+07:00`, answering six
of this lane's own outstanding `ASK-COO` letters (one COO ruling batch touched more than one
ASK-COO each in places). Full triage:

| letter | what it ratifies | already shipped? | this round's action |
|---|---|---|---|
| `actor-identity-scene-scope-owner-assigned-chief` | scene-bound ledger = interim fix; structural fix is chief's, post-M5 | yes (round m0vp7m) | stub only |
| `banned-placements-filter-ratified` | filter must cover the WHOLE 8-placement owner ruling, not just the 5 that collide today | yes (round wmomy7) -- verified `OWNER_REFUSED_PLACEMENTS['Bg0002'] == (89,90,92,93,94,95,96,97)` | **wander-11 small ticket run this round** -- see below |
| `bg0002-cline-flip-declined-pending-gt143` | Bg0002 stays `setnum`; Bg0015 flip to `cline` approved | Bg0015 already `IDENTITY_RULE = 'cline'` | stub only |
| `declined-ledger-ceiling-refines-1842` | HP-ceiling + loud announce on ledger refusal is the standing rule | yes (round m0vp7m) | stub only |
| `drop-lifetime-120s-ratified` | `DROP_LIFETIME_SECONDS = 120.0` | yes (round fxury2) | stub only |
| `gate2-shape-check-interim-ratified` | interim gate-2 admission rule can wire into `session.py` | rule built; gate 2 itself still not live | stub only |
| `loot-ledger-full-reannounce-ratified` | full-ledger-per-kill announce is a shape change, not a cadence violation | yes, shipped | stub only |
| `multidrop-wire-shape-ship-ratified` | keep the 82/179/462-byte multi-drop wire shape | yes, shipped | stub only; `GT-132` still needs an attended run |
| `training-dummy-and-partial-roster-withdrawal` | 916 dummy ships; partial (4/9) withdrawal was fine for one round | **all 9/9 already withdrawn** (`LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION == []`), ahead of the letter's "within 2 rounds" deadline | opened `GT-159` (dummy name-colour, small, non-blocking, per the letter's own ask) |
| `widen-death-scope-bg0002-hostiles` | extend the 916 widening ruling to templates 31/34/35 | chief's call site (`runtime.py:4106`), not built | status-only, no LANE-B code |

Two more letters this batch (`scene2-ownership-standing-rule`, `third-insertion-point-tied-to-gt146`)
are `cc: LANE-B`, not primary addressee -- read for context, no stub required (this lane did
not open either). Both confirm decisions already reported to this lane in prior rounds; no
new information.

All ten stubbed as `notes_to_chief/<name>.md.CONSUMED.txt`, originals copied to
`notes_to_chief/consumed/`.

## The wander-11 hunt (banned-placements-filter-ratified's own ask)

The letter's "who does what next" line: *"LANE-B opens a small ticket hunting for an
un-banned wander-11 (self-initiating aggro) placement, when convenient -- not urgent for
M4."* COO also ruled in the same letter that having zero self-initiating monsters today is
a known, tracked gap, not a block.

Ran the hunt with the tables already committed rather than leaving it as an open question:

```
field_mob_ai_tables.AI_WANDER_ROWS[11] = (..., n_OFFESIVE=1, n_AGGRO=1200)   -- self-aggro
field_mob_ai_tables.AI_WANDER_ROWS[16] = (..., n_OFFESIVE=0, n_AGGRO=0)     -- the everyday row
```

- `bg0001` (Port Royal): `HOSTILE_PLACEMENTS == []` -- zero hostile rows of any kind, so
  nothing to survey.
- `Bg0002`: wander-11 rows are placements 92-96 (`Orc Chief`, n_ID 103) -- **all five are
  inside `OWNER_REFUSED_PLACEMENTS['Bg0002']`** already. No un-banned candidate today.
- `Bg0015` (mined, committed, still COO-gated dormant per `COO-DECISION
  2026-08-26T12:46+07:00` pending lane A's second travel gate -- unrelated to the identity-
  collision question, which is already resolved at 12/12 agreement since round `ua236k`):
  placements 24, 27, 29, 31, 70 carry wander-11 and `OWNER_REFUSED_PLACEMENTS` has no
  `'Bg0015'` key at all. **Five real candidates exist for the day that gate opens.**

Pinned as four new tests in `tests/test_field_mobs.py`
(`SelfAggroPlacementSurveyTests`), hand-mutated (flipped the refusal set to empty --
caught; confirmed `AI_WANDER_ROWS[16]` is not mistaken for aggressive) rather than trusted
by eye. Opened `GAME_TEST_QUEUE.md` `GT-159` for the one client-observable follow-up this
surfaced (does the practice dummy's name render in enemy colour despite `rank=0`/
`ai_combat=0` -- a narrower instance of the still-open `RE-067`).

```
tests/test_field_mobs.py            : 47 -> 51 (new class SelfAggroPlacementSurveyTests, 4 tests)
tests/test_field_mob*.py (discover) : 103 -> 107, all green
full suite (unittest discover)      : 5568 tests, errors=18 (pre-existing capstone
                                       ModuleNotFoundError, same 3 files as every prior
                                       round), failures=0
```

ASCII/cp874 check on the one file touched (`tests/test_field_mobs.py`): 0 characters that
fail cp874 encoding (checked char-by-char, not just `ord(c) > 127`).

## pf-adversary by hand (no Task/Agent subagent available in this environment)

- Flipped the mutant `refused = set()` in the Bg0002 check by hand (outside the committed
  test, as a throwaway REPL check) to confirm the real `assertFalse(leftover)` line is not
  vacuous: it reports `{92,93,94,95,96}` as leftover when refusal is empty, so the check has
  a real subject.
- Confirmed `test_bg0001_ships_no_hostile_placement_at_all_so_none_can_self_aggro` is not
  redundant with the Bg0002 test: without it, the original (deleted) draft of
  `test_every_wired_scenes_self_aggro_row_is_owner_refused` iterated `(field_mob_tables,
  field_mob_tables_bg0002)` and failed immediately on bg0001's empty `HOSTILE_PLACEMENTS` --
  caught by running the suite, not assumed.
- Did not run `mutmut`; hand review only, same limitation every recent round has recorded.

## Debts carried, not fixed this round (already on record, re-checked, unchanged)

1. `mob_pickup_persist` still has zero call sites in `runtime.py` -- chief's, tied to
   `GT-124`/`GT-146` per `COO-DECISION third-insertion-point-tied-to-gt146`, not a LANE-B
   backlog item.
2. `docs/FUNCTIONAL_COVERAGE.json` still says Bg0002 has 17 monsters -- out of this lane's
   scope, not re-checked this round.
3. Bg0015 stays dormant -- blocked on lane A's second travel gate (`COO-DECISION
   2026-08-26T12:46+07:00`), not on identity, which is already resolved.

## ASK-COO / CORE-REQUEST this round

None. Nothing this round found needs either.

## Tickets opened for other lanes

`GT-159` (`GAME_TEST_QUEUE.md`, pirate-force-server via pf_bridge queue) -- attended,
in-game, not urgent, does not block M4/M5.
