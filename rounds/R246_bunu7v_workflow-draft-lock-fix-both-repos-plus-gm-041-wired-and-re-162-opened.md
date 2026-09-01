# R246 (session `bunu7v`) — 2026-08-30T~19:0x+07:00

## Round claim

`git fetch --all` both repos -> no open `[LANE-E]`/`WIP round claim` PR in either repo -> claimed lock:
empty commit + draft PR `pf_bridge#518` / `pirate-force-server#326`. Checked previous chief round's fate
(section 2 item 7): `[LANE-E] R245` PRs `pf_bridge#513` and `pirate-force-server#322` both `merged=true` --
nothing lost, proceeded normally.

## What this round did

1. **Structural fix, both repos: a finished round can no longer get stuck as an un-mergeable draft
   forever.** `notes_to_chief/20260830_1755_KA1A-REPAIR-*.md` measured (on `pf_bridge#507`) that the
   agent's own token gets HTTP 403 on both the REST `draft:false` PATCH and the GraphQL
   `markPullRequestReadyForReview` mutation, so a round that finishes clean and pushes real work can be
   stuck as an open draft with no agent-side way out. Patched `.github/workflows/merge-claude-pr.yml` in
   BOTH repos: the `reap` job now tries `gh pr ready "$PR"` with the *workflow's own* `GITHUB_TOKEN`
   (which already has `pull-requests: write` and already succeeds at `gh pr merge`/`gh pr close` a few
   lines below in the same job) before treating a stale draft as dead. Success -> the `ready_for_review`
   webhook re-runs `decide` normally on the next event; failure -> falls through unchanged to the existing
   close-and-keep-branch path. `pf_bridge`'s architecture had an explicit "close after `PF_STALE_MINUTES`"
   draft branch that now tries ready first; `pirate-force-server`'s reap job never special-cased `draft` at
   all (any stale PR just failed to merge and got closed via the generic "no gate verdict" path after
   `PF_STALE_HOURS`=6h) -- added the same try-ready-first step ahead of that generic path. Both patches
   passed the mandatory dup-key YAML check, `bash -n` on every `run:` block, and an ASCII-only scan, and
   both went through `pf-adversary` review before commit.
2. **`cloud_round_lock.json`**: per `COO-DECISION 20260830_1841` (round-lock-guarantee-doc-correction),
   corrected the `_who_releases_it` field's now-measured-false claim ("every path ends with the pull
   request not open, so the lock cannot get stuck") and added a `_correction_20260830` block describing
   the actual bound after the patch above.
3. **`PR_STATE.txt`** (pf_bridge root, newly un-ignored via `.gitignore`): per `COO-DECISION 20260830_1841`
   approving ka1-A's request, chief now writes a one-shot overwrite snapshot of open PR state (repo,
   number, draft, age_min, title, `OPEN_TOTAL`/`STUCK_DRAFT_OVER_45MIN`) every round that talks to the
   GitHub API, so the attended side can answer "what's stuck right now" from a real measurement instead of
   a stale browser tab or guessing from lane behavior.
4. **`CORE-REQUEST-GM-041` wired**: `notes_to_chief/20260830_1817_LANE-GM-*.md` asked for one read point
   `gm/` can call to learn whether toggling a GM-switchable NPC on/off would feed the existing census
   recompose cycle. Added `src/pirateforce_foundation/gm_npc_toggle_recompose.py`
   (`npc_toggle_would_recompose(mob_id) -> bool`) + `tests/test_gm_npc_toggle_recompose.py` (6 tests / 7
   subtests). Measured against `mob_scene_recompose.recompose_frames`'s roster source and `gm/`'s own
   `npc` dispatch path: the honest answer today is **False for every mob_id** -- no on/off state exists
   anywhere for a recompose call site to read. `pf-adversary` review (worktree-isolated, 3 mutation kills
   3/3) found and fixed one docstring overclaim (a "grep returns no hits" citation that was false against
   a pre-existing test file) before commit. Replied to LANE-GM (`CHIEF-REPLY 1909`) explaining the honest
   negative and that a real state-store + wiring is a separate, larger CORE-REQUEST if LANE-GM wants it
   pursued -- out of scope for what this letter actually asked (one read point).
5. **`RE-162` opened AND closed this same round** per direct owner order (`PANYA-ORDER 1655`): in-session
   scene-change wire question, full ticket text copied into `CLIENT_RE_QUEUE.md` without narrowing scope,
   investigation delegated to `pf-static-re` (finished within the round). **Result is MIXED, not the clean
   bounded-negative the owner's own framing assumed**: a real in-session cross-scene `TeleportVital`
   mechanism is already merged and firing (`_dispatch_columbus_quest3021`, `runtime.py:4826-5044`/`:8045`,
   composed via the same `legacy.make_login_teleport` encoder every login uses) -- but no one has ever
   confirmed the client actually renders it (`GT-106`, the attended ticket built for exactly this, is still
   `[PENDING]` since R198). `/warp`'s inability to cross scenes is a deliberate policy choice
   (`gm/warp_executor.py`, COO-locked), not an evidence gap. Fulfilled the consumer-promise table:
   `CHIEF-REPLY 1916` to LANE-GM/COO, `GT-106` updated in `GAME_TEST_QUEUE.md` pointing at the result and
   flagging it for COO's `GT-106-R2` decision, and the owner told directly in
   `FROM_CHIEF_R246_TO_ATTENDED`.
6. **`RE-157` closed (analysis) / guards not yet built**: read the result letter in full (`TradeCmd` needs
   an active-store-session stamp gated before `runtime.py:6787`'s `super().dispatch`; mob-combat needs an
   announced-actor-identity membership check at `:4093-4096` before cadence/ledger mutation). Marked the
   ticket DONE (analysis) in `CLIENT_RE_QUEUE.md`, explicitly NOT claiming the guards exist -- building
   them is real feature work (new per-session state, wiring into two call sites) too large to fit in this
   round alongside everything else above. Chief's own task for a coming round, not a new RE ticket.
7. **`CORE-REQUEST-007` / LANE-B's proposed loot-reorder**: consumed `COO-DECISION 20260830_1841` --
   invariant stands, LANE-B's competing request (round `qb1ytr`) is withdrawn, not pending. No code change.
8. Consumed 11 mailbox items addressed to chief/everyone (`PANYA-ORDER`, `CORE-REQUEST-GM-041`, 4x
   `COO-DECISION` from 1841, `RE-156-RESULT`, `RE-157-RESULT`, `RE-162-RESULT`, `KA1A-REPAIR`,
   `KA1A-SELFCORRECTION`) with stubs + `consumed/` copies.
9. `pf-adversary` review of the `pirate-force-server` workflow patch (item 1) found the fix's core claim
   overstated: pf_bridge#507's draft was undrafted by the OWNER clicking the button, not by any workflow
   token call, so it is evidence the AGENT's token was refused, NOT evidence the WORKFLOW's own token
   would succeed at the same `markPullRequestReadyForReview` mutation. Reworded both repos' code comments
   from an implied-confident `MEASURED` framing to explicit `[MEASURED: symptom]` / `[PROPOSED, UNTESTED:
   fix]`, and added the missing "we tried `gh pr ready` first, that failed too" context to
   `pirate-force-server`'s two close-comment paths (pf_bridge's already had it). Both re-validated
   (dup-key/`bash -n`/ASCII) after the fix.
10. Housekeeping: archived `CHIEF_CONTINUATION.md` rounds R231-R238 to
   `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R231_R238.md` (29.8KB -> ~19.5KB before adding this round's
   line, well under the 30KB cap).

## CORE-REQUEST audit

Only pending item found this round was `CORE-REQUEST-GM-041` (wired, see above). No other lane letter in
the unconsumed mailbox carried an open `CORE-REQUEST`/`CORE-REQUEST-GM-*` this round.

## What was NOT done / deferred

- `RE-157`'s two source guards (TradeCmd active-session stamp, mob-combat announced-membership check) --
  scoped, not built. Next chief round's priority alongside whatever else is pending then.
- `FORCE_POS_VITAL_VERSION_CONFIRMED` unlock (COO's extended deadline 2026-08-31 09:00) -- not touched
  this round, still needs the full "read all 11 red tests one at a time" pass R244 flagged.
- `GAME_TEST_QUEUE.md` physical archiving of closed-24h+ entries (section 17 item 9-b) -- file is large
  (1.6MB) but this round's time went to the items above; not attempted.

## Validation

- Both repos' `.github/workflows/merge-claude-pr.yml`: dup-key YAML check PASS, `bash -n` PASS on every
  `run:` block, ASCII-only scan PASS. `pf-adversary` review run on both: pf_bridge's `gm_npc_toggle_recompose`
  Python code got a separate, clean pass (see below); both workflow patches got a dedicated review, findings
  applied (honesty-framing fix on both, plus a close-comment fix on `pirate-force-server` only, since
  `pf_bridge`'s close-comment already had the needed context).
- `pirate-force-server`: `tools/verify_hypothesis_ledger.py` -> `PASS entries=47`, no drift.
- `gm_npc_toggle_recompose.py` + tests: `pf-adversary` (worktree-isolated) found and I fixed one docstring
  overclaim before commit; ran 3 mutation kills, 3/3 killed. Full suite re-run after all fixes:
  **5524 passed, 0 failed, 323 skipped, 9565 subtests passed** in 161s -- clean.
- `WIRED = 4/4` (unchanged this round; last re-verified booting headless in R244).

## Files touched

- `pf_bridge`: `.github/workflows/merge-claude-pr.yml` (1), `cloud_round_lock.json` (1), `PR_STATE.txt`
  (1, newly un-ignored), `.gitignore` (1), `CLIENT_RE_QUEUE.md` (1, RE-162 opened+closed + RE-157 status),
  `GAME_TEST_QUEUE.md` (1, GT-106 update pointing at RE-162), `CHIEF_CONTINUATION.md` (1),
  `archive/CHIEF_CONTINUATION_ARCHIVE_20260830_R231_R238.md` (1 new), `notes_to_chief/*.CONSUMED.txt`
  (11 new stubs) + matching `consumed/*` copies, 3 new letters (`CHIEF-REPLY-core-request-gm-041-*`,
  `CHIEF-REPLY-re162-result-*`, this round's `FROM_CHIEF_R246_TO_ATTENDED`), this file
- `pirate-force-server`: `.github/workflows/merge-claude-pr.yml` (1), `src/pirateforce_foundation/`
  `gm_npc_toggle_recompose.py` (1 new), `tests/test_gm_npc_toggle_recompose.py` (1 new)

## Companion PRs

`pf_bridge#518` (draft claim, updated this round) / `pirate-force-server#326` (draft claim, updated this
round)
