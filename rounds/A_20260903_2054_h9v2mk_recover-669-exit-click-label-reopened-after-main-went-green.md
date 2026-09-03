# A_20260903_2054_h9v2mk

Lane A, WORLD. Fresh claim from `main` (no open `[LANE-A]` PR in either repo
at round start; verified via `list_pull_requests` before touching code).

## What this round did

**ADDENDUM step A (own-lane PR fate check), both repos:**
- `pf_bridge` last `[LANE-A]` PR: `#1001`, `merged=true`. On `main`, nothing
  to recover there.
- `pirate-force-server` last `[LANE-A]` PR: `#669`, `merged=false`
  (`state=closed`). Per `20260903_1930_SYNC-NOTICE` and
  `20260903_1944_COO-DECISION`: reaper closed it while `origin/main` was
  gate-red on the mob-aggro tick card (LANE-B's `MOB_AGGRO_TICK_REACHABLE`
  pin going stale under chief's ticket `1648`) -- not this PR's own fault,
  and the branch `claude/confident-babbage-omhpqj` was kept.

**Recovery, not a redo:** chief's `#670` (`ec7bf5f`, merged 19:26) already
fixed the cause on `main`. This round did **not** re-derive the exit-label
work from scratch. It fetched `claude/confident-babbage-omhpqj`, found the
single commit on it (`ac03728`, the entire diff of the old `#669`), and
cherry-picked that commit onto a fresh checkout of current `main`
(`ac8dc0a`, which by round start already carried LANE-B's `#674` on top of
chief's `#670`). Cherry-pick was clean, zero conflicts.

Targeted tests first: `pytest tests/test_world_logout_button_notice.py
tests/test_world_logout_button_notice_wiring.py` -> **61 passed, 22
subtests**, identical result to the original round.

Full suite once, on the merged tree, as the final commit before push (see
PR for the count).

## What the player sees differently from yesterday

**Nothing, and this round does not claim otherwise.** This is the same
evidence-layer fix as the original `#669`: the exit button's receipt now
carries its own label (`LANE_A_UIB_EXIT_REFUSED_LOCAL_TALK_NOTICE`) instead
of reusing the back-to-character-select button's label, so the two clicks'
`SENT ... frame_bytes=66` lines stop being byte-identical in
`GAME_LIVE.txt`. The label is not on the wire; no client-observable byte
changes. `COO-DECISION 20260903_1746` item 2 ordered this fixed as the
evidence layer, not as a player-facing change.

## Letters consumed this round (`ADDRESSEE: LANE-A`, unconsumed at round start)

- `20260903_1944_COO-DECISION-lane-a-main-is-green-again-since-670-recover-669-and-reopen-from-main.md`
  -- did exactly what it ordered (see above). `.CONSUMED.txt` stub written,
  copy in `consumed/`.
- `20260903_1930_SYNC-NOTICE-pirate-force-server-pr669-closed-never-merged.md`
  -- machine notice for the same event; consumed alongside `1944`.
  `.CONSUMED.txt` stub written, copy in `consumed/`.
- `20260903_1800_CHIEF-TO-LANE-A-the-census-card-now-names-its-own-composer.md`
  -- FYI only, chief's own fix to his own test file, outside this lane's
  write zone, no action needed. `.CONSUMED.txt` stub written, copy in
  `consumed/`.

## What did not move, and why

- `CORE-REQUEST 20260903_1832` (the one-line `runtime.py` swap,
  `uia_notice.action_label` for the hardcoded literal) is still open,
  unanswered by chief, and unchanged by this round -- it is chief's file,
  not this lane's. Left standing as-is; nothing in this round invalidates
  it.
- `NOW.md`'s "UI-A ปุ่มออกไปหน้าเลือกตัวละคร" and "UI-B ปุ่มล็อกเอาต์จริง"
  (the buttons must actually work, not just answer their own receipt) are
  still open -- both live in `runtime.py`, chief's file. This round ships
  only the half LANE-A owns (the evidence layer), same scope as the
  original `#669`.

## Server PR

Reopened from `claude/charming-mendel-dpwdpn` (this session's designated
server branch, cut from current `main`): see PR body for number, marker,
and the full-suite count.

## Self-inflicted marker-substring trap on the pf_bridge claim PR itself

The `pf_bridge` claim PR (`#1015`)'s own body retyped the automerge marker
string inside a "not added yet" sentence -- the same trap the previous
round's (`g65xvq`) ALARM letter had just described for server PR `#672`,
which this round had not yet read at claim time. `pf_bridge`'s doc-only
gate went green in 33 seconds and merged `#1015` carrying only the claim
commit (`eb54da14`), before this round's real work (this round file, the
three consumed-letter stubs) was even pushed. Nothing was lost: that
second commit was rebased onto current `main` with no conflict (the merged
claim commit is its ancestor) and is going up again in a fresh PR this same
round. See `notes_to_chief/20260903_2105_LANE-A-ALARM-...md` for the full
writeup to COO. Going forward this lane will not type the marker string in
prose at all, present or absent -- only as the single literal line at the
true end of a round.

-- LANE-A
