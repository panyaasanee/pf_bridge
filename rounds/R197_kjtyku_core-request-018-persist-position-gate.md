# R197 (session kjtyku) — 2026-08-27 ~18:5x-19:2x (+07:00)

## Priority this round

Per duty order §17 item 3 (ต่อสาย CORE-REQUEST ก่อนงานอื่นทุกอย่างในรอบ), the highest-priority
unconsumed chief-owned letter at round start was
`notes_to_chief/20260827_1809_LANE-A-CORE-REQUEST-018-wire-persist-position-allowed-gt106-fix.md`,
itself answering `COO-DECISION 20260827_1746` ("M2 ยังไม่ปิดใบ ต้องแก้ persistence bug กับปลายทางฉากก่อนประกาศผ่าน").

## The bug (GT-106, attended, real)

A character who walked into scene 17 via the Columbus quest-3021 teleport came out of teardown with
a `character_positions` row reading `scene_id=1` but carrying scene 17's XYZ coordinates
(`x=-149.0, y=-1250.3, z=745.0`) — a row nobody chose, wrong on both columns, unsafe for the next
login. COO-DECISION 1746 mandated option (b): skip the position write entirely while in scene 17
(chosen scene 17 has `login_entry_allowed=False`, no measured return path, `n_MARKER=0`, `RE-077`
open) rather than write scene 17 explicitly (which would then lock the character out at next login).

Lane A already built and tested `world_scene_travel.is_position_persist_allowed(n_id, registry=None)`
(fail-open for any scene not in the registry, pinned `False` only for scene 17 today) but has no
write access to `runtime.py`/`app.py`. CORE-REQUEST-018 asked chief to wire it in.

## What I actually found and changed

Grepped for `character_positions`/`save_position` across the codebase. The actual write choke point
is not `runtime.py`/`app.py` directly (Lane A assumed this, correctly noting they didn't know the
line number) — it's `store.py`'s `save_position()`, called from exactly two places in the entire
codebase: `CharacterLifecycle.checkpoint()` and `CharacterLifecycle.exit()`, both in `lifecycle.py`.
Gating there is a single, DRY enforcement point instead of duplicating the check at N call sites in
`runtime.py`.

First draft: `checkpoint()`/`exit()` called `is_position_persist_allowed(position.scene_id)` and
skipped `store.save_position(...)` entirely when it returned `False`.

## pf-adversary — first pass (real subagent call)

Found one real **HIGH**: skipping `store.save_position` entirely also skips its
`EXISTS(SELECT 1 FROM sessions WHERE id=? AND selected_character_id=? AND closed_at IS NULL)`
ownership/staleness check — the project's only detection signal for a stale or hijacked session
(documented by name in `reports/PF_MULTIPLAYER_READINESS_AUDIT001_SINGLE_PLAYER_ASSUMPTIONS_20260818.md:126`,
and the matching half of `store.py`'s own single-session lease-takeover comment at `open_session()`).
Before this diff, a stale session's checkpoint/exit would raise `PermissionError`, loud. The adversary
reproduced directly: with a stale session id and a scene-17 target, `store.save_position` called
directly still raises correctly, but the first-draft `CharacterLifecycle.checkpoint()` returned
silently. This defeats the operator's only current collision signal specifically at the one scene
GT-106 already flagged riskiest.

Also flagged MEDIUM (uncached `load_scene_registry()` file read + full validation on every checkpoint
— measured ~19 calls in one short walk per `reports/PF_MOVE_CADENCE001_CHECKPOINT_CADENCE_PER_WALK_HEADLESS_20260818.md`)
and two lower-severity/nonclaim items (a bounds mismatch between the gate's `1..0xFFFF` scene-id
validation and `store.save_position`'s own `0..0xFFFF`, confirmed unreachable from any live call path
today; and two now-stale `runtime.py` comments claiming `selected.position` always mirrors the
persisted row, which is Lane A/GM code I don't own and is cosmetic, not a functional bug).

## Fix

- `store.py`: `save_position(sid, cid, pos, *, write_position: bool = True)`. When `True` (default,
  every pre-existing call site unaffected), behavior is byte-identical to before. When `False`, it
  runs the same ownership/staleness `SELECT` the `UPDATE...WHERE EXISTS` clause always implied,
  raises `PermissionError("stale or non-owning character session")` on no match, and returns without
  touching `character_positions` on a match.
- `lifecycle.py`: `checkpoint()`/`exit()` now always call `store.save_position(..., write_position=allowed)`
  — the ownership check always fires, only the column write is conditional. `CharacterLifecycle.__init__`
  now loads `self._scene_registry = load_scene_registry()` once (confirmed `CharacterLifecycle` is
  constructed exactly once at boot, `app.py:749` — no live-reload path exists anywhere in this
  codebase per grep, consistent with the project's own "not a live reload" comments elsewhere).
- `tests/test_lifecycle_persist_position_gate.py` (new, 7 tests): write-through for an unpinned
  scene, skip for scene 17, resume writing once back in an unpinned scene, `exit()` still closes the
  session either way, and two stale-session repros (open a second session for the same account,
  which closes the first via the single-session lease takeover, then assert `checkpoint()`/`exit()`
  on the now-stale first session id still raises `PermissionError` even for a scene-17 target — these
  fail against the pre-fix gate, confirmed by tracing).
- `repository.py`: cosmetic follow-up, `CharacterRepository` Protocol's `save_position` signature now
  matches (adversary's second-pass note).

## pf-adversary — second pass (real subagent call)

Re-reviewed both files fresh: confirmed no TOCTOU (the `write_position=False` branch is a single
atomic `SELECT`, nothing downstream depends on it staying valid), confirmed registry caching at
construction is safe and matches an existing precedent elsewhere in this codebase
(`tests/test_columbus_quest_dispatch_wiring.py:301-351` pins the same "reuse boot-loaded registry"
pattern for `resolve_entry`), grep-confirmed no other `save_position` caller is affected (keyword-only
arg with a default), and traced the new stale-session tests to confirm they're not vacuous. One
cosmetic-only note (the Protocol signature) — addressed above.

## Tests / evidence

- `python3 -m pytest -q` (repo root): `3520 passed, 327 skipped, 5025 subtests passed` — green(cloud sanity).
- `python3 tools/verify_hypothesis_ledger.py`: `HYPOTHESIS_LEDGER PASS entries=47` — no drift.
- No attended/client-observable evidence this round (server-side write-path fix only; the bug itself
  was already proven attended via `GT-106`).

## Pushed

- `pirate-force-server@9c920f4` (lifecycle.py + store.py + new test file)
- `pirate-force-server@fe89b55` (repository.py Protocol follow-up)
- Companion: `pf_bridge` (this round file + CHIEF_CONTINUATION.md registry row 018 + index line +
  mailbox replies/stubs)

## What is NOT proven / still open

- This closes only item 1 of 3 in `COO-DECISION 1746`. Item 2 (RE evidence for whether the client's
  own `Player.Teleport(17)` actually renders scene 126 "Atlantic Ocean: Rising Sun Sea" + a ship, per
  the owner's own objection to scene 17 as the real destination) is LANE-GM/RE runner work, not
  cloud-buildable. Item 3 (quest 3205 `Q_BORNAGAIN` dialog option) is LANE-A's own scene work.
  **M2 is still not closed. `GT-106-R2` should not be opened until all three land** (per the COO
  decision's own instruction to chief).
- No new `GAME_TEST_QUEUE.md` entry this round — added a status note under the existing `GT-106`
  entry instead, since a full re-test is premature until items 2/3 land too.
- Did not attempt `CHIEF_CONTINUATION.md`/`AGENTS.md` size housekeeping (both still far over their
  permanent caps, promised and deferred R193 through R196 for the same reason each time: too risky to
  combine with a round doing real code work). This is now five rounds deferred and should be the
  first thing a bookkeeping-only round does.
- Did not attempt a mailbox backlog sweep beyond the two letters this round's own work touches
  (backlog remains large — most of it is LANE-A/B/GM-owned per the v6.3 "whoever opened it consumes
  it" rule, not chief's to stub).
