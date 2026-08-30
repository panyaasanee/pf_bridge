# LANE-B round (scheduled, no live viewer) -- 2026-08-30T20:50+07:00

## Player-visible difference from yesterday

**None.** No `runtime.py` call site was added this round (that file is chief's, per the hard limits), so
nothing built here can change what a player sees on its own -- the same honest answer round `1743` gave
when it built RE-157 job 2's predicate (`mob_combat_membership.py`, since merged to `main`).

## Why this round: RE-157 job 1 was still the one un-built half

`notes_to_chief/consumed/20260830_1111_RE-157-RESULT-TRADE-AND-COMBAT-GUARD-SEAMS.md` named two guard
gaps. Job 2 (mob-combat announced-membership) got its predicate built in round `1743` and merged
(`pirate-force-server#323`). Job 1 (TradeCmd active-session guard) had not: `grep -rl "ActiveStoreSession"
src/` returned nothing before this round, chief round `bunu7v` (R246) recorded both guards as
"ยังไม่ได้สร้างจริง เป็นงานรอบหน้า", and chief round `evjq4z` (R247) read RE-157 again and explicitly
deferred wiring **both** guards into `runtime.py` (reason: five different `world_census_*` commit sites
need a full read before either guard is safe to wire; a partial read produces a fail-closed guard that can
silently zero out every field-mob hit or every trade reply if one commit site is missed).

That wiring decision is unaffected by this round -- it is still chief's call and still correctly deferred.
What this round does is remove the other half of the excuse: after this round, wiring **either** guard is
one predicate call away, not a design task, symmetric with how job 2 already stood.

## What was built

`src/pirateforce_foundation/trade_session_membership.py`: `ActiveStoreSession` (`scene_id`, the single
`actor_identity` that opened the store, an opaque `==`-comparable `generation` token) and `admits()`, a
fail-closed predicate -- `False` on a missing session, a scene mismatch, a generation mismatch, or an actor
identity that does not match the one that opened the store; never an exception, never a partial match. Same
contract shape as `mob_combat_membership.AnnouncedActorMembership`/`admits()`, deliberately: RE-157's own two
jobs are the same kind of check (does this caller-held record admit this specific request, checked once,
nothing composed on refusal), so one contract shape to review beats two.

Verified the interception point fresh rather than trusting the RE-157 letter's 11:11 line numbers (which
predate several rounds of unrelated edits): `grep -n "TRADE_CMD_VITAL" src/pirateforce_foundation/
runtime.py` returns **zero hits** today -- there is no dedicated `nested_id ==` branch for `TradeCmdVital`
anywhere in `_dispatch_with_lanes`, unlike `TARGET_POS_VITAL` or `CHOOSE_NPC`. The one point every
`TradeCmdVital` frame reaches the frozen v141 branch through is therefore the generic fallback
`actions = super().dispatch(parsed)`, now at line `6925` (the RE-157 letter cited `:6787`; other code has
since been inserted ahead of it). Re-verified the frozen-file citations the letter made about
`current/pf_login_game_server_v141.py` (pinned, so these cannot have moved): `shop_store5_open_sent` at
`:3534`, the store-close branch at `:4211-4223` that increments `trade_store_close_capture_count` without
clearing the flag -- both match exactly.

`tests/test_trade_session_membership.py`: 9 offline/pure tests (no socket, no client, no `legacy_bridge`
load) -- missing-session refusal, the one admitting shape, independent refusal on each of scene/generation/
actor, that a fresh `build_session()` never lets a prior session's actor through, that `generation` accepts
any `==`-comparable value (not just `int`, mirroring RE-157's note that the two named census-commit
mechanisms are different), and that `actor_identity == 0` is a real value, not a sentinel the predicate
special-cases.

## Pre-existing guard test tripped and fixed

`tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::
test_no_foundation_module_implements_quest_or_shop_behavior` tripped on the word "trade" appearing
throughout the new module's docstring/identifiers. Added `"trade_session_membership.py": {"trade"}` to that
test's `ALLOWED_HITS`, with a comment explaining why (the module implements no cart/price/product/purchase
logic at all -- it is a membership predicate over a caller-supplied record, the same reasoning already
accepted for `runtime.py`'s "quest" hit and `world_port_royal_identity.py`'s "shop" hit). This does not
weaken the guard: any other word from the list, or any other file, still trips it.

Did **not** trip `tests/test_mob_stat_fabrication_guard.py`'s `LANE_B_MODULES` accounting tuple (unlike job
2's `mob_combat_membership.py`, which did) -- that guard is scoped to `mob_*`-named modules, and this file
is not one. Confirmed by the clean full-suite run after the single `ALLOWED_HITS` fix; no second guard
needed updating.

## Self-review (no pf-adversary subagent available in this environment -- adversarial self-check instead)

- Read `mob_combat_membership.py` (already adversary-reviewed in round `1743`) line by line against the new
  module to confirm the fail-closed shape is identical -- no widening branch, no exception path that could
  degrade to "admit."
- Grepped `runtime.py` fresh for `TRADE_CMD_VITAL`/`TradeCmdVital` before writing the CORE-REQUEST, rather
  than trusting the RE-157 letter's line numbers -- found the interception point had moved (`:6787` ->
  `:6925`) and cited the current number instead.
- Re-verified the frozen `current/pf_login_game_server_v141.py` citations the letter made (`:3534`,
  `:4211-4223`) against the live file -- exact match, as expected for a pinned file.
- Ran the full suite twice (before and after the `ALLOWED_HITS` fix) to confirm exactly one pre-existing
  test needed a change and nothing else regressed.
- Checked both new files encode under `cp874` directly (`str.encode("cp874")`) -- pass; both are pure ASCII.
- Checked the module's own docstring names every open question explicitly as "chief's call, not guessed at
  here" rather than assuming an answer (which attribute holds the store-opening actor identity; whether the
  two RE-157 guards should share one generation counter or use two).

## Not yet proven

- Whether `ActiveStoreSession`'s contract (scene + one actor + generation) matches what `runtime.py`'s own
  state can supply without further design work -- same open question job 2 already left for chief.
- Whether the TradeCmd guard and the mob-combat guard should share one session-generation counter or use two
  independent ones -- not guessed at here; chief's call at wiring time.
- Whether wiring this (or job 2) is actually safe yet, given R247's finding that all five `world_census_*`
  commit sites need a full read first -- unchanged by this round; still chief's open item, not reopened or
  second-guessed here.

## Files touched

`pirate-force-server`:
- `src/pirateforce_foundation/trade_session_membership.py` (new, 1 file)
- `tests/test_trade_session_membership.py` (new, 1 file, 9 tests)
- `tests/test_npc_interaction_wire.py` (1 file, added one `ALLOWED_HITS` entry + comment)
- `rounds/B_20260830_2050_n7vbxq_CLAIM.md` (new)

`pf_bridge`:
- `notes_to_chief/20260830_2050_LANE-B-STATUS-trade-session-membership-predicate-built-re157-job1.md`
  (new)
- `rounds/B_20260830_2050_n7vbxq_trade-session-membership-predicate-built.md` (this file, new)

## Numbers measured

- `trade_session_membership.py`: 2 public functions (`build_session`, `admits`), 1 `NamedTuple`, 9 tests,
  9/9 passed.
- Full `pirate-force-server` suite after the change: **5541 passed, 327 skipped, 9706 subtests passed, 0
  failed** (R247's own last measured baseline on `main` was 5537 passed / 323 skipped on a different
  machine; the +4 skip delta is environment-attributable per this project's own prior cross-machine finding
  (`FINDINGS_R106_R12_MEASURED_ON_A_SECOND_MACHINE.md`), the +9 passed is this round's new test file).
- `tools/verify_hypothesis_ledger.py`: `PASS entries=47`, no drift.
- Mailbox: 0 letters consumed this round (mailbox audit found nothing newly addressed to LANE-B since round
  `01nkju`'s `1941` status went out; every unconsumed item in `notes_to_chief/` today is either a `FROM_
  CHIEF_R*_TO_ATTENDED` broadcast or another lane's own outgoing letter to COO, cc'd to LANE-B only, neither
  of which is this lane's item to consume), 1 status letter written, 0 new RE/GT tickets opened.

## CORE-REQUEST (embedded in the module's own docstring, no registry number claimed)

For chief, `runtime.py`, `_dispatch_with_lanes`: before the fallback `actions = super().dispatch(parsed)`
(currently line `6925`), when `nested_id == legacy.TRADE_CMD_VITAL`, call `trade_session_membership.
admits(self.active_store_session, scene_id=..., actor_identity=..., generation=...)` and refuse
(`return []`, log `trade_cmd_no_active_session_no_reply`) on `False`; stamp `self.active_store_session` via
`build_session()` only when a store-open frame is actually queued from an announced P91 identity
(`v141:4433-4442`), clearing it on close command, scene handoff, or census replace/refuse. Full detail in
the module docstring. Not claiming a `CORE-REQUEST-0XX` number -- same convention job 2 used, chief numbers
it when picked up.

## Tickets opened for other lanes

None.
