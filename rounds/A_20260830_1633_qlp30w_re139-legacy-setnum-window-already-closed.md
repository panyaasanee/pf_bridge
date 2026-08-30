# LANE-A round `qlp30w`

Opened 2026-08-30T16:28+07:00 (Bangkok). Heartbeat at round start:
`_BRIDGE_HEARTBEAT.txt` last line 2026-08-30T14:58+07:00 (90 minutes old at
open, still well inside the correction the 60-minute rule is aimed at: no
hand-computed timestamp was used anywhere this round, every stamp below came
straight from `TZ=Asia/Bangkok date`).

## Section A -- last round's PR

Checked both repos via the GitHub REST API (no `gh`, per house rule):
`GET /repos/panyaasanee/pirate-force-server/pulls?state=closed&sort=updated`
finds the latest `[LANE-A]` PR as `#318` ("round 6p22bu: Bg0004 crosswalk and
census, not wired"), `merged_at: 2026-08-30T09:06:04Z` -- **merged: true**.
Nothing to salvage, nothing to cherry-pick. `pf_bridge`'s own open-PR list
(`GET /repos/panyaasanee/pf_bridge/pulls?state=open`) shows no `[LANE-A]` PR
open (only `#503 [LANE-E]`, not this lane's lock). `pirate-force-server`'s
open-PR list showed `#319 [LANE-GM]` (round-lock claim only) and `#317
[LANE-E]`, neither this lane's.

## Section B -- mailbox

No new `ADDRESSEE: LANE-A` letters since round `12lyda` (2026-08-30T14:35)
consumed the standing backlog. Confirmed by listing `notes_to_chief/`
modification order and re-reading the two most recent Lane-A status letters
(`20260830_1434_...` and `20260830_1435_...`) plus round `6p22bu`'s own
letter, none of which left an open mailbox item for this lane. Nothing to
consume this round.

## Section C -- the blocker this round actually ran into

This round's harness gives Lane A a git-writable worktree for `pf_bridge`
only. Every `git` command aimed at `/home/user/pirate-force-server` (`cd` +
git, `git -C`, or any bash line the sandbox could not statically prove stayed
inside the `pf_bridge` worktree) is refused outright: *"a worktree-isolated
agent's git operations must target its own worktree."* Plain filesystem
reads of `pirate-force-server` work fine (confirmed every file cited below is
byte-identical to `origin/main` via `raw.githubusercontent.com`, so nothing
read this round was somebody else's uncommitted work-in-progress in that
shared checkout) -- only `git status`/`add`/`commit`/`push` against that repo
are blocked. **No file under `pirate-force-server` was written or left
modified this round** (`echo test` was used once to probe write permission,
confirmed writable, and the probe file was deleted immediately -- not
committed, not left behind, because a shared checkout with no way to commit
from here is not a safe place for this lane to leave any diff, staged or
not).

This blocks the one concrete BUILD item queued from last round (`6p22bu`'s
Bg0004 identity+census wiring into `CENSUS_SOURCES`/`ROSTER_COMPOSERS`/
`lane_hooks`) -- that work needs `src/` writes in `pirate-force-server` and
could not be attempted this round for that reason, not for lack of a plan.

## What this round did instead (Rule F(b): an RE/STATIC ticket answerable
## from committed source, read-only)

`RE-139 P33-P58-IDENTITY-CONTRADICTION-001` (`CLIENT_RE_QUEUE.md:2391`,
addressed jointly to `LANE-A` + `LANE-B`, opened by chief round `wi1m62`)
asks which of two contradicting identity sources is correct for bg0001
placements 33/58 -- `world_population`'s CLINE-crosswalk census (Babu/Juliet)
or `mob_death.full_roster_override`'s roster (Fighting Fish soldier/Jungle
Big Tiger) -- and states plainly that `GT-104` cannot be graded until this is
answered.

Traced it end to end, read-only, across `field_mob_tables.py`,
`field_mobs.py`, `mob_death.py`, and the `runtime.py` call site (all
confirmed identical to `origin/main`): **the contradiction was real, for
exactly the one-round window `COO-DECISION 2026-08-29T00:41+07:00` ("nine
rows get one round only") authorized, and that window is already closed as
of the current `main` tip (`710700a`)**. `field_mob_tables.py`'s
`LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION` list -- the one that used to
carry P33/P58 under the old Mob-Set reading -- is empty, with a header
comment stating the migration is done; `SHIPPED_PLACEMENTS` (what
`field_mobs.load_roster()` actually reads) is 4 rows (the "Training Iron
Man" practice-dummy targets), not the 13 it was when `wi1m62` observed the
contradiction; `runtime.py`'s `full_roster_override` call site has no
hardcoded row count anywhere, so its output on current `main` is 4 identities
overridden, never P33/P58. Full citations, the reasoning for why `RE-139`'s
original observation was genuinely correct (not a misread) at the time it
was made, and the implication for `GT-104`'s own "do not grade identity
before reading RE-139" clause are in the result letter.

## What shipped in `src/`

**Nothing.** Zero diff in `pirate-force-server` this round (could not be
attempted regardless, per Section C; also not needed to answer `RE-139`,
whose own objective forbids fixing code under the ticket).

## Files touched this round (all in `pf_bridge`)

- `pf_bridge/rounds/A_20260830_1633_qlp30w_re139-legacy-setnum-window-already-closed.md` (this file, new)
- `pf_bridge/notes_to_chief/20260830_1633_RE-139-RESULT-legacy-setnum-window-closed-roster-is-4-not-13.md` (new)
- `pf_bridge/notes_to_chief/20260830_1633_LANE-A-STATUS-re139-answered-worktree-blocker-flagged.md` (new, paired status letter)

`CLIENT_RE_QUEUE.md`'s `RE-139` header is **not** edited this round -- opened
by chief, not by this lane; per the project's "opener closes" convention
(same handling `RE-156` got from round `re156-answer`), the result letter is
handed to chief to close.

## Player-visible claim

**None.** This round is a read-only RE answer plus round records. No code
changed, no scene's `login_entry_allowed` changed, nothing a player would see
differently today.

## What's blocked / waiting

- Bg0004 wiring (`CENSUS_SOURCES`/`ROSTER_COMPOSERS`/`lane_hooks`), queued by
  `6p22bu`, needs a Lane-A worktree that can write+commit
  `pirate-force-server` -- flagged as a process note (not a CORE-REQUEST,
  since `runtime.py`/`app.py` are not involved) in the paired status letter.
- `GT-104`'s own grading is not this lane's call (`G-OBS`) -- its remaining
  nonclaims (NPC-conversation lane blocking attack entry, double-click
  requirement) are untouched by this round's finding.

## Numbers measured this round

`field_mob_tables.py`: `HOSTILE_PLACEMENTS` = 0 rows, `TOWN_TARGET_PLACEMENTS`
= 4 rows, `LEGACY_SETNUM_PLACEMENTS_PENDING_MIGRATION` = 0 rows,
`SHIPPED_PLACEMENTS` = 4 rows total (roster `full_roster_override` actually
sees today), `WITHDRAWN_UNDER_THIS_RULE` = 9 rows (history only, not sent).
Three source files (`field_mob_tables.py`, `runtime.py`,
`world_port_royal_identity.py`) plus `mob_death.py` verified byte-identical
to `origin/main` before being cited.

## CORE-REQUEST

None from the `RE-139` finding itself (the one stale artifact it turned up,
a "13" in a `runtime.py` comment at line 7676, is prose-only and does not
affect behaviour -- noted for whichever round next touches that file, not
urgent enough for a dedicated request).

## ASK-COO

None opened this round -- the worktree/git-access gap in Section C is a
process note for COO's attention, not a decision this lane needs before it
can keep working (Rule F's own fallback list is exactly what this round
used).

## เปิดใบให้สายอื่น

None this round (RE-139 was already open; answered, not opened).
