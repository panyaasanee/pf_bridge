# R274 (session `gmcj4a`), 2026-08-31T~23:1x+07:00, LANE-E (PLATFORM)

## Round-lock guard (หัวข้อ 2)

`git fetch --all` both repos. No open `[LANE-E]` round-claim PR existed in either repo (only
`[LANE-A]`/`[LANE-B]` claims: `pf_bridge#637`, `server#411`, `server#415` — none touched, per rule).
Claimed lock: round-claim commits pushed on `claude/gracious-pasteur-gmcj4a` (pf_bridge) and
`claude/tender-wozniak-gmcj4a` (server), draft PRs opened immediately (`pf_bridge#640`, `server#419`),
confirmed `draft:true` via `pull_request_read get` on both before doing any other work.

**หัวข้อ 2 ข้อ 7 fate check**: previous round R273 (`httmc6`)'s PRs — `pf_bridge#635` and `server#416`
— both confirmed `merged:true` via `pull_request_read get` (the `list_pull_requests` `merged` field
read `false` for essentially every recently-closed PR across both repos again, same known artifact
noted every round since R265 — confirmed via `get`, not list, per the standing rule). Nothing missing
from main.

## CORE-REQUEST audit (หัวข้อ 17 ข้อ 3 — done before anything else)

Two CORE-REQUESTs were pending, both read in full before any other work:

1. **LANE-A+LANE-B joint (`20260831_2151_LANE-A-TO-CHIEF-scene14-hostile-splice-core-request-*.md`)**:
   wire a hostile-faction splice onto 12 of scene 14 (Bg0015)'s 81 monster placements. **WIRED THIS
   ROUND** — see below.
2. **LANE-B (`20260831_2156_LANE-B-STATUS-mob-ai-tick-hook-built-call-site-named-core-request.md`)**:
   wire `lane_b_mob_ai_tick.maybe_tick` into `runtime.py`'s `dispatch()`. **NOT WIRED THIS ROUND** —
   the letter's own pf-adversary note flags that `maybe_tick`/`tick_session` take a `player_alive`
   parameter defaulting to `True`, and there is currently no state anywhere in `dispatch()` that
   tracks whether the connected player is alive. Verified independently by grepping `runtime.py` for
   `player_death`/`respawn`/`is_player_dead`/`player_hp` — zero hits. Pasting the CORE-REQUEST's given
   block unchanged would make mob AI treat a dead player as permanently alive (aggro/threat computed
   against a corpse). Deferred until a real player-alive signal exists in `dispatch()`; this is not a
   silent drop — recorded here per the mandatory-reason rule.

## What was built and proven (server repo)

`src/pirateforce_foundation/world_population_handoff.py`, function `_roster_handoff` — the single
chokepoint both `handoff_for_arrival` (M1-P login) and `handoff_on_crossing` (M2 crossing) call for
scene 14 arrivals: added `if composer.source == "bg0015_roster":` splicing
`field_mob_hostile_bg0015.scene14_hostile_overrides(legacy)` onto the generation via
`mob_scene_recompose.splice_identity_override` (lane B's existing, already-tested reimplementation —
not a third copy of the algorithm). Both halves (LANE-A's `world_population_bg0015`, LANE-B's
`field_mob_hostile_bg0015` + `mob_scene_recompose.splice_identity_override`) were already built and
proven end-to-end by `field_mob_hostile_bg0015.scene14_civilian_then_hostile_splice_proof`; this round
is the three-line call site plus the ordering fix below.

**Two real defects found and fixed while wiring this, not left for later**:

1. `_require_pair` (the pc/frame consistency check) was originally placed only AFTER the splice.
   `splice_identity_override` unconditionally re-encodes a fresh frame from `pc` via the legacy
   encoder, ignoring whatever `frame` it was handed — so a composer bug that produced a
   foreign/mismatched frame for bg0015 would have been silently "healed" by the splice before the
   check ever ran, defeating `tests/test_world_population_handoff.py::
   test_a_roster_frame_is_checked_against_its_own_pc` (caught by running the targeted test file, not
   by inspection — it went red). Fixed by validating the composer's raw output BEFORE the splice, and
   keeping the existing post-splice validation as defense in depth for drift the splice itself might
   introduce.
2. `tools/pf_runtimeres_actor_entry_static.py`'s `SRC_ACTOR_STREAM_SITES` pin (a naive full-text regex
   count of `make_runtime_remote_actors(` occurrences across `src/`, comments included — confirmed by
   reading `_count_src`) went from 34 to 35 because my own explanatory comment in
   `world_population_handoff.py` spelled out that literal call text. Caught by the full test suite
   (`tests/test_static_verifier_pins_cloud.py` failing), not by adversary review. Fixed by rewording
   the comment to describe the behavior without the literal regex-matching substring, verified the
   count returned to 2 (both pre-existing, unrelated) in that file and the guard test went green again.

`tests/test_world_population_handoff.py::HandoffTests::
test_a_composed_scene_gets_its_own_roster_and_never_the_dock_census` updated: it used to assert scene
14's handoff bytes are byte-identical to the RAW `build_bg0015_population` output; now asserts the
handoff equals `splice_identity_override` applied to that same raw build, and explicitly asserts it no
longer equals the raw (civilian) bytes.

**Numbers**: targeted files (`test_world_population_handoff.py`, `test_field_mob_hostile_bg0015.py`,
`test_mob_scene_recompose.py`): 137 passed, 110 subtests. Full suite before merge: 5972 passed, 323
skipped, 12389 subtests passed, 0 failed (ran twice — once caught the false-positive pin above, once
clean after the fix). `tools/verify_hypothesis_ledger.py`: PASS entries=47, no drift.

**pf-adversary reviewed this diff in an isolated worktree this round (mutation-tested, not just read)
and cleared everything about the diff itself** — the ordering fix and the composer-scoping guard both
hold under mutation, exception paths from `scene14_hostile_overrides` raising are caught on both the
login and crossing paths with no listener-thread escape, `placement_indices` survives the splice, no
non-ASCII was introduced. **It also found one CONFIRMED defect, not in this diff but activated by it**:
`lane_hooks/lane_a_choose_npc_scene14.py` (LANE-A's own file, out of chief's write territory) rebuilds
all 81 scene-14 actors via its own plain civilian `make_npc_attr` on every ChooseNPC click, never
consulting the hostile override — so clicking ANY NPC in the scene (not just one of the 12) silently
reverts all 12 hostile-spliced actors back to civilian (replace-by-omission, RE-092), verified by
running `respond()` against a real spliced generation and diffing the resulting pc. Reported to LANE-A:
`notes_to_chief/20260831_2318_CHIEF-TO-LANE-A-choosenpc-scene14-reverts-hostile-splice-to-civilian.md`.
`GT-177` was updated with a caution note before finalizing this round (do not click any scene-14 NPC
before observing aggro, or a real feature will read as a false negative). A secondary, lower-severity
finding — `lane_a_scene_census.py`'s `_hostility_lines` doesn't pass `override=`/`ledger=` to
`describe_census_hostility` for scene 14, so the one console line built for exactly this question
reports `not_reported` even though the splice is working — is noted in the same letter for chief/LANE-A
to pick up later; not fixed this round (not blocking, and touches a file this round did not open).

## GAME_TEST_QUEUE.md

Opened `GT-177` (via `pf-queue-author`) for the client-observable half of this CORE-REQUEST: does one
of the 12 spliced placements in scene 14 actually behave hostile on screen, while the rest stay
civilian as `GT-134` already measured. Explicitly does not close, move, or overwrite `GT-134` — cross-
referenced as a distinct claim (GT-134 answered "does anything render", this asks "do the 12 spliced
ones read as hostile").

## Housekeeping: RE-132 archived + a stale measurement corrected

`kaa1-A`'s third chase letter (`20260831_2255_KA1A-CHASE3-*.md`) named `RE-132` as the largest queue
entry needing the PANYA-DECISION 1747 shrink (cited at "154 KB", repeating a figure from
`20260831_1747_PANYA-DECISION-*.md`). Checked before acting: `RE-132` is actually **CLOSED** (PASS,
closed 2026-08-29, so past the 24h housekeeping threshold in หัวข้อ 11) and its real heading-to-next-
heading span is **8,059 bytes**, matching what R269 had already measured and flagged as a discrepancy
against the same "154,463 B" figure — this round resolves that flagged discrepancy for good: the 154
KB number was a measurement error in the 1747 letter (not this entry's real size), not something to
inherit and repeat again. Moved the entry verbatim to
`archive/CLIENT_RE_QUEUE_ARCHIVE_20260831_R274_closed.md` per the closed-entry archive rule (not the
1747 shrink-in-place rule, which is for OPEN oversized entries) with a one-line stub, correcting the
byte-size record in the stub itself so the next reader doesn't repeat the same wrong number.
`CLIENT_RE_QUEUE.md`: 494,602 B -> 487,023 B.

This does not fully answer kaa1-A's ask (an OPEN oversized entry shrunk per PANYA-DECISION 1747) —
RE-132 turned out to be the wrong target (closed, not oversized). That is still open for a future
round: find the actual largest OPEN entry and shrink it per the 1747 rule, with the same
heading-to-next-heading measurement method used here (not whatever produced the 154 KB figure).

## Mailbox triage (หัวข้อ 5, grep ADDRESSEE/ถึง on every un-stubbed letter, per PROCESS_GATES #17)

Consumed and stubbed 7 letters addressed to chief or FYI-to-all with no clearer owner: the LANE-A/
LANE-B scene14 CORE-REQUEST (actioned above), the LANE-B mob_ai_tick CORE-REQUEST (deferred above, with
reason), LANE-GM verify-only round-9 status, two ka1-B IMAGE-tier findings (nameboard FontStyle
selector, quest-mark selector — both forwarded to the lanes they're cc'd to, no chief action item),
CODEX-CHECKPOINT-P05, and LANE-A's bg0007 build+wire+open status (ADDRESSEE: ALL). Everything else
un-stubbed in the mailbox has a clear non-chief owner (LANE-B-SELF, LANE-x-ASK-COO, KA1B-TO-COO,
KA1B-TO-LANE-B, CODEX-NEWGEN with no follow-up interpretation letter per หัวข้อ 14 ข้อ 13, or chief's own
outgoing CHIEF-REPLY/FROM_CHIEF letters) — consistent with what R270/R271/R273 already found reviewing
the same long tail.

## WIRED

WIRED = 4/4 (no new lane_hooks module added or wired to a production dispatch path this round; the
bg0015 splice is a change inside an existing chief-owned module, not a new lane_hooks entry, so it does
not move this counter under WIRED v2's definition).

## Not proven / nonclaim

No client screen has ever shown scene 14's hostile splice (`GT-177` opened for exactly that). The
mob_ai_tick CORE-REQUEST is deliberately not wired. RE-132's archive does not satisfy kaa1-A's actual
ask (shrinking an oversized OPEN entry) — still open. pf-adversary's verdict on this round's diff was
pending at the time this file was written; if it surfaced anything after this was committed, it will be
in the next round's file, not retroactively edited into this one.

## Files touched

**pirate-force-server**: `src/pirateforce_foundation/world_population_handoff.py`,
`tests/test_world_population_handoff.py`, `rounds/` (none — chief does not write per-repo round files,
per established convention, only this pf_bridge file).

**pf_bridge**: `CLIENT_RE_QUEUE.md`, `archive/CLIENT_RE_QUEUE_ARCHIVE_20260831_R274_closed.md`
(new), `GAME_TEST_QUEUE.md` (GT-177 opened, then amended with the ChooseNPC caution after pf-adversary's
finding), `CHIEF_CONTINUATION.md`, 7 `.CONSUMED.txt` stubs + 7 `consumed/` copies,
`notes_to_chief/20260831_2318_CHIEF-TO-LANE-A-choosenpc-scene14-reverts-hostile-splice-to-civilian.md`
(new), `notes_to_chief/FROM_CHIEF_R274_TO_ATTENDED_*.md`, this file.

push แล้ว รอ merge PR pf_bridge#640 / server#419
