# R294 (session `happy-dirac-69cabr` / `focused-turing-69cabr`)

2026-09-01T~21:2x+07:00

## NOW.md check

P-1/P-2/P-3 not lane-E blockers this round (server code+tests already done, only Panya's attended GT
test remains, per NOW.md's new rule at top). GM-A/census-latch/GM-B already have tracked owners/tickets.
Quest-mark icon work (raised in `notes_to_chief/20260901_2016_KA1B-TO-CHIEF-*.md`, unowned since
31 Aug) assigned to LANE-A this round
(`notes_to_chief/20260901_2050_CHIEF-TO-ALL-quest-mark-icon-work-assigned-lane-a.md`).

## What happened, in order

1. **store.py connect() PRAGMA-leak fix** (LANE-DB CORE-REQUEST, `notes_to_chief/20260901_1904_*.md`,
   option 1 -- chief fixes directly): wrapped `sqlite3.connect`+4 PRAGMA statements in try/except that
   closes and re-raises, ahead of the pre-existing try/finally around yield/commit/rollback. New
   regression test `tests/test_store_connect_pragma_leak.py` reproduces LANE-DB's exact repro
   (non-database file, `journal_mode=WAL` branch); confirmed it fails on pre-fix code, passes on the
   fix.

2. **CORE-REQUEST-GM-049** (`notes_to_chief/20260901_1728_*.md`), authorized by
   `COO-DECISION 20260901_1847` (scoped, temporary exception (ค) for the `/speed` sparse x=7 door only):
   - `attr_wire.UPDATE_ATTR_VITAL_VERSION_CONFIRMED`: `None` -> `0`, reasoning: convergence of two
     independently-proven vital_version bytes in the same GM-wire family (`state_wire`=0, `teleport_wire`
     `ForcePos`=0) -- NOT a copy of either alone (COO-DECISION forbade that).
   - `gm/chat_command_action.py`: new `_speed_action`, `_selected_speed_identity`, dispatched from
     `command.name == "speed"` right after `gmprobe`. Composes through `gm.speed_wire.
     compose_sparse_speed_update` (x=7 only, no merge, no other field touched). Label
     `LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL` (does not contain `TELEPORT`).
   - Delegated implementation to a general-purpose subagent (full context of `chat_command_action.py`'s
     conventions, mirrored `_say_action`'s shape exactly).

3. **Parallel static-RE on the vital_version byte itself**: opened `RE-198`
   (`CLIENT_RE_QUEUE.md`, numbered 198 not 197 to avoid colliding with `pf_bridge#750`'s in-flight
   `RE-197` claim -- confirmed no collision after #750 merged and this branch rebased). Result:
   **BOUNDED-NEGATIVE** -- no direct constructor proof for `0x309A` itself found, but a real finding that
   weakens the original "converges on 0" reasoning: `RE-129-RESULT` itself pins a THIRD vital in the same
   generic-reader mechanism, `TeleportVital`, at byte `4`, not `0` -- 2-of-3, not 3-of-3.
   `attr_wire.py`'s comment on the constant already (independently, before RE-198 finished) disclosed
   this same TeleportVital=4 fact -- the implementing subagent found it directly in RE-129's own result
   file while writing the reasoning comment, so no further edit was needed once RE-198 confirmed it.
   Recorded full result: `notes_to_chief/20260901_2119_RE-198-RESULT-*.md`. `0` remains the
   best-reasoned guess under COO's accepted bounded/reversible risk, not a measured value.

4. **Mandatory pf-adversary review** (before commit, per house rule) found a real, live defect: the
   CORE-REQUEST's run-copy-DB requirement ("never send against canonical") was documented as
   "no code-level mechanism exists" in `_speed_action`'s own docstring -- FALSE.
   `session.foundation.lifecycle.store.path` is a live, already-dereferenced-elsewhere attribute chain
   that reveals the exact DB file the process booted against. Since `lane_hooks/lane_gm_chat_command.py`
   sets `production_allowed = True` unconditionally and `runtime.py` unconditionally forwards the
   composed action to the real outbound frame list, this meant a GM typing `/speed` against a
   canonical-DB boot would send a real frame today -- exactly what the CORE-REQUEST asked to be refused.

5. **Fixed the adversary finding**: added `CANONICAL_DB_FILENAME = "pirateforce.sqlite3"` (cited from
   `app.py`'s own default `--db` fallback), `_speed_db_is_canonical`/`_speed_db_filename` helpers reading
   `session.foundation.lifecycle.store.path` defensively (unreadable chain = treated as canonical =
   refuse, never "assume safe"), new `EVENT_SPEED_WITHHELD_CANONICAL_DB`/
   `OUTCOME_SPEED_WITHHELD_CANONICAL_DB`, wired as the FIRST check in `_speed_action` (before identity,
   before version-gate). Docstring rewritten to state the real limitation plainly: this is a filename
   heuristic, not a cryptographic guarantee -- a mis-named copy in either direction would fool it.
   8 new tests (`SpeedRunCopyDbGateTests`) cover canonical-exact-match, non-canonical proceeds,
   backslash-path handling, and unreadable-chain withholding.

## An unexpected process event, flagged for the record

While this round's server-repo PR (`pirate-force-server#507`) was still marked `draft: true` (confirmed
by `pull_request_read get` immediately after opening it), the `merge-claude-pr.yml` automerge workflow
merged it anyway (`dc311fde`, `merged_by: github-actions[bot]`) partway through this round, before chief
had finished the round file, before CORE-REQUEST-GM-049's registry row was closed, and before the
run-copy-DB gate fix (item 5 above) had even started. This contradicts this house's own standing belief
("draft ถูกข้ามเสมอ" / reaper only acts on non-draft) recorded in multiple prior prompts. By luck, every
commit that had landed on that branch at the moment of the premature merge was already fully tested
(full suite green each time) -- nothing broken landed on `main` -- but the SEQUENCING contract (finish
work -> write real PR body -> take out of draft -> let automerge run) was bypassed entirely by the
workflow itself, not by chief. **Recommend COO/owner treat this as a live workflow-config question, not
closed**: either `merge-claude-pr.yml` does not actually gate on `draft` the way past prompts assumed, or
something else (a `ready_for_review`-adjacent trigger neither chief nor this round's tooling fired)
caused it to run. The `wake gate: <session>` empty-commit convention (repo section 3 step 4) was skipped
this round for `pirate-force-server` since the PR closed before chief reached that step -- if this
skip has downstream effects (gate not re-triggered on the merge commit), watch `ci/<merge-sha>.json` on
the NEXT round and report if it's missing.

## Verified

```
pirate-force-server: python3 -m pytest -q => 6434 passed, 323 skipped, 13750 subtests passed, 0 failed
                      (run independently twice -- once by the implementing subagent, once by chief)
                      python3 tools/verify_hypothesis_ledger.py => PASS entries=49
pf_bridge:            rebase onto post-#750 main clean after resolving 2 append-only conflicts in
                      CLIENT_RE_QUEUE.md (RE-197 vs RE-198 ordering, and RE-198's own status-line edit)
```

## GAME_TEST_QUEUE.md

`GT-193` updated: added RECHECK item 8 (reconnect-gate pass criterion, per COO-DECISION item 4) and
corrected the RECHECK section to reflect the actual architecture (dispatch lives in
`chat_command_action.py`, not a literal `/speed` string in `runtime.py`) and current status (wire-compose
half done+tested+adversary-reviewed; LANE-DB's DB-persistence half still not on `main` -- entry stays
`PENDING interface`, not promoted to `READY`).

## Mailbox triage

Stubbed 7 chief-addressed letters this round (2 CORE-REQUEST replies with real fixes, 2 status-only,
2 Codex checkpoints informational, 1 backlog-recovery postmortem with one actionable ask answered
-- quest-mark ownership). CORE-REQUEST registry row 030 (GM-049) closed this round -- see
`CHIEF_CONTINUATION.md`.

## WIRED

WIRED = 5/6 (lane_hooks modules with `production_allowed=True`, re-verified this round by direct grep of
`src/pirateforce_foundation/lane_hooks/lane_*.py`; unchanged -- `lane_a_choose_npc_scene1` intentionally
still `False`). No lane_hooks module touched this round.

## Not proven

`0` for `UPDATE_ATTR_VITAL_VERSION_CONFIRMED` is still a reasoned guess, not a measured value (RE-198,
BOUNDED-NEGATIVE). The run-copy-DB gate is a filename heuristic with a stated, real bypass in either
direction. LANE-DB's DB-persistence half of the `/speed` interface has not shipped, so `GT-193` cannot
be run attended yet even though the wire-compose half is on `main`.
