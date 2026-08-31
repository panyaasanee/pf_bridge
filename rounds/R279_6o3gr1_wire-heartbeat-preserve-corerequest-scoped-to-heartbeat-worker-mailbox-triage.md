# R279 (session `6o3gr1`, chief / LANE-E) -- 2026-09-01T05:19+07:00

## What happened, in order

1. Round-overlap guard (prompt v6.4 หัวข้อ 2): no open `[LANE-E]` draft PR in either repo. Checked
   previous round's own `[LANE-E]` PRs via `pull_request_read(method=get)` -- both `pf_bridge#664`
   and `pirate-force-server#438` show `merged:true` (the `list_pull_requests` tool's `merged` field
   is unreliable, always came back `false` even for confirmed-merged PRs -- use `get`, not `list`,
   for merge status; noting this since it cost real time this round). Claimed lock: `pf_bridge#668`,
   `pirate-force-server#441`, both opened draft, `PF-AUTOMERGE: v4` in body, verified via `get`.
2. `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` present. Fetched + verified.
3. CORE-REQUEST backlog (hard priority per หัวข้อ 17.3): exactly one unconsumed CORE-REQUEST across
   both repos' mailboxes, `20260901_0420_LANE-B-CORE-REQUEST-heartbeat-preserve-ground-list-fixes-
   drop-clear.md` (LANE-B round `n8kq4r`, P-1: v141's frozen heartbeat clears every ground-drop on
   the client every ~2s because `make_runtime_res_empty_exact()` always emits both derived-mask
   bytes absent). Its dependency, `pirate-force-server#437` (adds `mob_loot.preserve_ground_
   heartbeat_frame`), was still open when checked but merged mid-round (CI went green at
   `2026-08-31T21:54:39Z`, merged by the automerge workflow at `21:54:53Z`) -- so wired it in the
   same round instead of deferring.

## The wiring, and what pf-adversary (this round) caught before commit

First draft did exactly what the CORE-REQUEST letter asked: blanket `legacy.make_runtime_res_
empty_exact = lambda: preserve_ground_heartbeat_frame(legacy)` before `adapt_game_listener(...)`.
Spawned `pf-adversary` (mandatory, per หัวข้อ 10) on that draft before commit. Findings:

1. `make_runtime_res_empty_exact` has THREE real call sites in v141, not one grepped by the
   letter: `heartbeat_worker` (the target), `run_self_test` (already neutralized separately), and
   `RUNTIME_RES_ACK_FIRST_REQ` in session dispatch (the first packet sent on every connect). A
   blanket attribute replacement changes all three; nobody reviewed or tested the connect-time ack
   under the new shape.
2. The letter's (and my first draft's comment's) claim that `adapt_game_listener()` copies
   `legacy`'s globals "once, when called" is wrong -- read `connection.py:226-239`: the copy
   happens *inside* the returned closure `adapted()`, at listener-thread invocation, not when
   `adapt_game_listener(original, ...)` is called to build the wrapper. The placement asked for
   (before the assignment line) is still safe, just for a weaker reason than claimed.

Fixed by extracting `install_ground_heartbeat_preserve(legacy)` (`app.py`), which now wraps rather
than replaces: substitutes the PRESERVE shape only when `sys._getframe(1).f_code.co_name ==
"heartbeat_worker"`, and falls through to v141's original implementation for every other caller.
Replaced the source-text-only test with a real behavioral one
(`test_ground_heartbeat_patch_only_changes_the_heartbeat_worker_caller`) that loads `legacy`
directly, calls through a locally-defined `heartbeat_worker` function and confirms the PRESERVE
bytes, then calls directly (a different frame name) and confirms v141's original CLEAR bytes are
unchanged. Second adversary pass (same session) found nothing further after the fix.

Also hit, twice, an unrelated pinned-count drift: adding test functions to
`test_foundation_legacy_seam.py` moved `package_a_pinned_test_functions` in
`reports/PF_MULTIPLAYER_READINESS_AUDIT001_SINGLE_PLAYER_ASSUMPTIONS_20260818.md`'s `AUDIT_COUNTS`
block (89 -> 90 -> 91, one bump per test added) -- re-pinned both times per that file's own
documented procedure, not a logic bug.

Wrote `PROCESS_GATES.md` rule #21: patches to a shared v141 global with more than one real caller
must be caller-frame-scoped, not blanket; verify a CORE-REQUEST's stated mechanism against source
before trusting it, even if the letter says a previous pf-adversary pass already corrected it.

## Tests / verifiers

Full suite: 6137 passed, 323 skipped, 0 failed (final state, after both re-pins).
`tools/verify_hypothesis_ledger.py` PASS (entries=47). `tools/verify_functional_coverage.py` PASS
(no drift; 8 domains still open, unrelated to this round).

## Mailbox triage

10 chief/everyone-addressed letters read + stubbed (self-close rule ack, my own prior CHIEF-ASK-COO
now answered/closed, a stale round-lock mirror, 6 Codex static-RE evidence letters for GM-plugin /
monster-color / ground-drop -- all design input for LANE-A/B/GM's own zones, no CORE-REQUEST
embedded, no chief write-zone action). CORE-REQUEST letter + its CHIEF-REPLY both stubbed after the
wiring above. See PROCESS_GATES rule #17 (grep ADDRESSEE, not date-range guessing) -- applied this
round too.

## Queue

Opened `GT-188` (attended, two-tier: wire/DB heartbeat-shape vs client-observable ground-drop
persistence past two heartbeats). `BLOCKED` until `pirate-force-server#441` merges. Explicitly NOT
gated to/from `GT-146` (pickup-opcode capture) per the CORE-REQUEST's own nonclaim -- both tickets
stand independently; GT-188 step 7 has an optional, non-blocking observation only.

## WIRED

WIRED = 5/5 lane_hooks modules (unchanged this round -- nothing here touches `lane_hooks/`).

## Not proven / nonclaims

- Codex's client-image read of the reconciler (`GSCN_RunTimeProtocolRes+0x20`) was not independently
  verified this round -- only the server-side byte behavior was.
- The fix's effect on-screen (does the ground drop actually persist longer for a real client) is
  exactly GT-188's job, unanswered as of this round.
- No full running-server boot test exists anywhere in this repo's test layout for `app.py`; the
  wiring is proven structurally + behaviorally at the unit level, not end-to-end.

## Status at round end

`pf_bridge#668` and `pirate-force-server#441`: pushed, PR bodies to be rewritten with round summary
+ marker (หัวข้อ 3 step 2), then draft removed via `update_pull_request`, then wait for
merge -- not "done" until a future round confirms `merged:true` via `pull_request_read(method=get)`.
