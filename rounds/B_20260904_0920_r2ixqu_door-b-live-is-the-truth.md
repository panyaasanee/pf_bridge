round r2ixqu
LANE-B (COMBAT)
start 2026-09-04T09:20+07:00

NOW.md this round: 0847 (COO-DECISION 20260904_0847, "Door B: live is the
truth, cache never fills a row"). Not moved by this round: the milestone
table itself did not change; this round pays down the item under
"M4 - LANE-B / Door B" that COO-DECISION 20260904_0847 assigned to the
round starting ~09:31 -- item done a few minutes earlier, since the
scheduled trigger for this round fired at 09:00-ish rather than exactly
09:31.

## What the player will see differently from yesterday
Nothing, and this round does not claim otherwise. Door B still has no
caller (`MOB_HIT_FRAME_CONFIRMED` stays `None`), and no byte reaches a
player. This round is a wire-composition fix ordered by the COO before the
caller is allowed to be wired.

## Lock protocol notes (deviation, reported honestly)
This round's own letter/mailbox check and the code fix were done before
opening the claim PR, out of the prescribed order (claim should come first,
"before touching code"). No other LANE-B round was open in either repo
throughout (checked at round start and again immediately before opening
this claim, `search_pull_requests`/`list_pull_requests` on both repos,
`[LANE-B]` in title, most recent one `#717`/`#1084` (round `yq5gzr`) --
merged, not open), so nothing was actually placed at risk; the ordering
slip is noted here rather than pretended away.

## What was fixed and why
`pf_bridge/notes_to_chief/20260904_0847_COO-DECISION-lane-b-door-b-live-is-
the-truth-cache-never-fills-a-row.md` answered pf-adversary round
`yq5gzr`'s D6 open question (asked in this lane's own letter
`20260904_0800_LANE-B-ASK-COO-...`): Door B's `compose_player_hit_frame`
used to validate `live`'s KEYS against `gm/attr_wire.named_field_x()` and
then discard its VALUES, composing the actual frame bytes from the
connection's `RawBlockCache` instead (via `attr_wire.build_named_field_
update`, which merges one changed field into whatever the cache already
held). Nothing anywhere enforced that the cache was CURRENT, and `RE-222`
says every row a hit frame carries overwrites the client's own copy -- so a
stale cached value (cash, HP-max, ...) would silently revert on the
player's screen the moment this door's gates ever open. The `GT-218`
family, with a stale value where `GT-218` had a zero.

COO's ruling (option (a), strict): `live` IS the truth. The cache may never
fill a single row of the frame. A row this connection's login shape needs
that neither the named live source nor the login-byte source can answer is
a whole-frame stand-down -- never a fill from the cache, never a fill with
zero. Completeness is measured against the login set, from live sources,
not against the cache.

`src/pirateforce_foundation/mob_hit_frame.py`'s `compose_player_hit_frame`
now:
- reads the connection's `RawBlockCache` for its KEY SET only (`current_
  values().keys()`), to learn which rows this connection's own login
  composed -- never for a VALUE;
- sources every row's value from `gm/attr_wire.live_full_block_values`
  (LANE-GM's own shared function, the same one `seed_cache_from_live_
  values` calls -- per `COO-DECISION 20260904_0045`, this door is a CALLER
  of `gm/attr_wire.py`, never a second implementation of its named/login-
  byte partitioning), scoped to this connection's own shape (`rows=shape`,
  not the default union -- the same reasoning `build_named_field_update`'s
  own D1 comment gives for why the union would be wrong);
- overrides only `hp_current` with the caller's `hp_after` argument;
- composes via `gm/attr_wire.make_update_attr_frame` directly, bypassing
  `build_named_field_update` (the function that used to read the cache's
  stored values);
- calls `cache.record_sent(values)` after a successful compose, in the
  same spot `build_named_field_update` used to call it on this door's
  behalf -- `RawBlockCache`'s one remaining write, unchanged.

Added `STANDDOWN_LIVE_SOURCE_INCOMPLETE` for "a row this connection's
login shape needs that no live source can answer." The two pre-existing
gates (`STANDDOWN_LIVE_SOURCE_NOT_A_FIELD`/`_NOT_NAMED`) are unchanged in
code but now guard data that actually reaches the wire, per the COO
letter's item 3.

## Tests
`tests/test_lane_b_mob_ai_tick.py::HitFrameDoorBTests`:
- New helpers `_adjudicated_login_byte_values` (the login-byte hook's own
  complete answer, mirroring `_adjudicated_live_values`) and
  `_expected_full_block` (the values dict the door should now compose).
- `_full_valid_baseline` demoted to a SHAPE-only fixture; its own values
  are now deliberately decoys distinct from the live/login-byte helpers',
  so a leak has somewhere unambiguous to show up.
- Flipped the positive-path card
  (`test_when_the_connection_cache_is_complete_the_frame_composes`) to
  assert the composed frame equals the LIVE-sourced block, never the
  cache's baseline, plus an explicit assertion that the fixture's baseline
  and the expected live values actually disagree (so the card cannot pass
  by accident).
- Added the mutant `COO-DECISION 20260904_0847` names literally: a hook
  answering zero for two rows (`hp_max`, `cash`) the cache holds real,
  non-zero, recognisable values for --
  `test_a_stale_cache_value_never_reaches_the_frame` -- asserts the
  composed frame matches the hook's zero, not the cache's value, and that
  `record_sent` leaves the cache holding the zero too, not the stale
  original. (`hp_current`, x=3, is excluded from the sentinel set: it is
  the one row this door always overrides to `hp_after` regardless of any
  source, so using it as a leak sentinel would test the override, not the
  cache-never-fills-a-row rule.)
- Fixed the D7 cache-write card
  (`test_the_cache_is_untouched_on_every_path_this_door_takes`) to pin the
  new invariant: on the positive path the cache now comes out holding
  exactly the live-sourced block that was sent, not "only `hp_current`
  differs from the stale baseline it started from" (which was the old,
  now-wrong, invariant).
- `test_nothing_a_hook_can_return_reaches_an_uncaught_exception`'s
  value-based cases (a negative u64, bytes for a wstr row, a float on a
  u32 row) now inject the bad value through the HOOK directly (since the
  hook's values reach the frame now) rather than through a seeded cache;
  the expected stand-down reason changed from `encoder_refused` to
  `live_source_incomplete`, because `attr_wire.live_named_values` validates
  every row's value with the SAME `validate_field_value` the real encoder
  uses, before this door ever reaches `make_update_attr_frame` -- a bad
  value is now caught earlier, by the shared validator, not by the
  encoder it used to reach only via a seeded cache.
- `test_a_renamed_vital_row_is_a_stand_down_inside_the_gated_path` needed a
  fully seeded cache + both hooks to reach the renamed-row lookup at all,
  since that lookup now happens after the live-source-complete check
  (previously it happened via `build_named_field_update`'s cache merge,
  reachable with an unseeded default cache -- unseeded no longer reaches
  that far).

Targeted: `pytest tests/test_lane_b_mob_ai_tick.py -q` -- 59 passed, 64
subtests passed. Also re-ran `tests/test_foundation_legacy_seam.py`,
`tests/test_mob_stat_fabrication_guard.py` (both read this module for
ASCII/legacy-seam contracts), `tests/test_persistence_vitals_or_none.py`
(scans for a file naming both the vitals door and an attribute
composer -- mob_hit_frame.py names neither `read_character_vitals_or_none`
nor any of that card's `COMPOSERS` list), `tests/test_gm_attr_wire.py`,
`tests/test_gm_login_mask.py`, `tests/test_gm_speed_wire.py`,
`tests/test_live_named_attr_values.py` (this door's own dependencies) --
all green, no regressions.

pf-adversary (ordered at round start, worktree review, never the live
checkout): ADVERSARY_PENDING -- ordered before this checkpoint, not
returned yet. Per `COO-DECISION 20260903_2345`: push proceeds (checkpoint,
not a hand-off), the result is picked up as this round's own first item
before the claim marker goes on, and this section is rewritten with the
real findings before the marker is added.

Full suite: NOT YET RUN. House rule is once, on the true final commit,
after pf-adversary's findings (if any) are applied -- not before. Will run
after the section above is filled in, and before the claim PR's marker is
added.

## pf_gate_preflight
`tools_bridge/pf_gate_preflight.py --repo /home/user/pirate-force-server
--base origin/main`: `[cp874] PASS`, `[skips] PASS - no new skip markers`,
`[mainmerge] PASS - origin/main (ecfeec5) is already in HEAD`.

## Not in this round
- Does not wire the caller. `MOB_HIT_FRAME_CONFIRMED` stays `None`;
  `notes_to_chief/20260904_0847_...` item's own deadline is explicit about
  this ("ทำก่อนเสียบ caller").
- Does not touch `runtime.py`, `app.py`, `pf_login_game_server_v141.py`,
  the canonical DB, `scenarios/world_*.json`, or `scenarios/combat_*.json`.
- Does not answer the open question about `x=9` needing to be the CURRENT
  scene (NOW.md `0846`) -- that is GM/session-bytes territory
  (`live_login_bytes`'s hook, not yet built at all on a real boot), not
  something this door's own compose logic decides.

## Server side
`pirate-force-server` PR: not opened yet at this checkpoint -- code is
pushed to `claude/magical-hawking-r2ixqu`; the PR opens at round end per
the lock protocol's close-out order, after pf-adversary's result is folded
in.
