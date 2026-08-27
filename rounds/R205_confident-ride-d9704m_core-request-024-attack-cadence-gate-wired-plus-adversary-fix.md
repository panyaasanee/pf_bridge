# R205 (confident-ride-d9704m / jolly-mccarthy-d9704m) 2026-08-28 ~04:0x (+07:00)

## CORE-REQUEST check (v6.4 §17 item 3, done first)

`notes_to_chief/20260828_0337_LANE-B-CORE-REQUEST-wire-attack-cadence-gate-spam-click-fix.md`
was the one actionable, unblocked CORE-REQUEST addressed to chief since R204. Wired it this
round, before anything else. The other open registry rows (011/012 GmCommand decode gap, 014
Columbus scene-move half, 015 mob_pickup, 017 point 2) all remain blocked on RE work chief
cannot do from this clone (no client binary) or on functions that do not exist yet — unchanged
from R204's own check, confirmed again this round, nothing new to report there.

## What changed

LANE-B built the attack-cadence gate (`AttackCadenceLedger`/`check_attack_cadence`/
`describe_cadence_rejection` in `mob_combat.py`) in a prior round, per PANYA-REFERENCE
2026-08-27 16:35's order to close "spam-click = runaway damage" (the exact symptom GT-084-R2
saw) ahead of every other combat item in that letter. The function sat unwired — the call site
is `runtime.py`'s `_dispatch_mob_combat`, chief's file — until this round.

Wired per the docstring recipe (`MOB_COMBAT_CADENCE_WIRING`, `mob_combat.py:229`): opened
`self.mob_combat_cadence` next to `self.mob_combat_ledger` at session init, gated immediately
before the existing `attack_from_observed_action` retry loop.

**pf-adversary caught a real bug in the first draft, before push**: the literal recipe gated
every inbound ActionVital unconditionally. ActionVital/EA7D is a generic "action on a target"
shape (`mob_combat.py`'s own `MOB_COMBAT_NONCLAIMS` #1 — the inbound half is unproven), not
attack-specific. Reproduced end-to-end on the real dispatcher: an ActionVital aimed at a
non-monster target (townsperson, another player, anything outside the roster) silently spent
the performer's cadence window before `attack_from_observed_action` ever got to say "not a
field mob" — so a genuine first attack on a real monster 200ms later was rejected as "600 ms
too soon" even though no damage-bearing attack had ever landed. Fixed by gating only when
`target` resolves to an actual roster member (the same membership test
`attack_from_observed_action` itself runs a few lines below) — a miss-click no longer taxes the
window a real attack needs. Also fixed, same pass: the rejection branch only printed to console
and never touched `self.events`, breaking the `..._no_reply` event-logging convention every
other silent return in this method follows — now appends
`mob_combat_cadence_rejected_no_reply`. Both fixes are regression-tested (see below). Updated
the stale `MOB_COMBAT_CADENCE_WIRING` docstring with a `[STALE][MEASURED]` note describing the
deviation, matching this project's own convention for marking a fulfilled wiring request.

New test file `tests/test_mob_combat_cadence_wiring.py` (6 tests, drives `make_state_class`
headless with an injected fake `monotonic_clock`, same harness `test_mob_combat_dispatch.py`
uses): fresh-session first attack accepted; same-instant second click rejected+silent+ledger-
untouched+event-logged; three rapid rejects don't slide the deadline, fourth attempt at the
correct boundary lands; attack at exactly the window boundary accepted; and the pf-adversary
regression itself (miss-click on a non-monster target does not consume the cadence window).

## Files touched (3, one topic)

- `src/pirateforce_foundation/runtime.py` (2 edit sites: session-init ledger open, dispatch gate)
- `src/pirateforce_foundation/mob_combat.py` (stale-docstring update only, no wire-format change)
- `tests/test_mob_combat_cadence_wiring.py` (new)

## Tests

`tests/test_mob_combat_cadence_wiring.py`: 6/6. Related regression suites (dispatch/census/
ai_control/diag_multi_object wiring): 86/86, no change in behaviour outside the gate itself.
Full suite: `3564 passed, 198 skipped, 23 errors` (same 23 pre-existing capstone/pefile/tools
`ModuleNotFoundError` collection errors as every prior round, not new), `0 failed`,
เขียว(cloud sanity). `tools/verify_hypothesis_ledger.py`: `PASS entries=47`, no drift.

## CORE-REQUEST

CORE-REQUEST-024 opened and closed same round (registry row added to `CHIEF_CONTINUATION.md`).

## เปิดใบให้สาย C

none

## What is not proven

- `ATTACK_CADENCE_MS_PROVISIONAL = 600` remains a labelled guess (RE-110 still open) — this
  round proves the gate itself runs correctly on the production path, not that 600ms is the
  right number.
- No attended/client-observable confirmation that the throttled attack rate looks/feels right
  to a real player — wire/DB layer only this round, per G5. Not opening a new GT ticket for
  this: GT-084/GT-084-R2 already carry the "spam-click = runaway damage" symptom this closes;
  noted inline there rather than duplicating.

## WIRED v2

Unchanged, `9/10` (same definition boundary as R190/R202: this is a fix inside an
already-wired lane, not a new lane import+emission — matches CORE-REQUEST-022's own note that
it does not move this counter).

-- **chief**
