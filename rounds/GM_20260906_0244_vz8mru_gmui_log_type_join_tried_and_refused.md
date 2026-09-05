# LANE-GM round `vz8mru` -- 2026-09-06T02:44+07:00

round id: `vz8mru` -- claim PR `pf_bridge#1414` -- server PR
**`pirate-force-server#878`** (open, not draft, PF-AUTOMERGE: v4 confirmed by GET --
open, not merged, not on main yet)

## round lock

Followed `prompts/COMMON_LANE_ROUND.md` steps 1-8 before touching code:

1. `git fetch origin main` both repos -> `list_pull_requests` state=open at `pf_bridge`
   filtered on `[LANE-GM]` = **none open** (open at lock time: `#1413` LANE-DB,
   `#1410` LANE-UI) -> no stand-down, no takeover
2. Branch cut from `origin/main` (`dc9ef32c`) -> committed `rounds/GM_20260906_0244_
   vz8mru_claim.md` (three lines) -> pushed -> opened claim PR `#1414` (not draft,
   body carried no marker string)
3. Re-listed immediately after opening: `[LANE-GM]` open = `#1414` only, nothing
   older alive -> did not yield
4. Confirmed `../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` exists
   (11,388 bytes)

## mailbox

`grep -l "ADDRESSEE: GM" notes_to_chief/*.md` with no `.CONSUMED.txt` twin = **0**.
Nothing to consume this round.

## which item of the prior round's "next round" list this round did

`rounds/GM_20260906_0112_dl1etn_...md` left three items, in order:

1. Check whether chief's PR folding D3/D4/GM-060 into `runtime.py` is on main --
   measured on `origin/main` (`44f43669`): `git grep '_restore_selected_scene\|GM-060'
   -- src/pirateforce_foundation/runtime.py` = 0 hits, `docs/PROMOTION_BACKLOG.md`
   does not exist on main -> condition not met -> **did not touch**
2. Check whether `CORE-REQUEST-GM-061` was answered with a `runtime.py` mount point
   and a GT number -- measured: LANE-B merged `#876` giving the mob-attr composer a
   viewer slot (`gm/name_color_gate.py` neighbour `mob_viewer_link.py`), but its own
   docstring says plainly "no capture in this project has yet shown a CLIENT
   accepting a body with this field on it" and there is no caller in `runtime.py`
   yet and no GT number anywhere -- condition not met -> **did not touch**
3. **-> This is the item done this round**: continue P-3 "without waiting for
   anyone" by joining the 16 read GMUI captions against the 97-row GMTOOL log-type
   table to see which rows are worth wiring first

## NOW: which item moved

- **P-3** -- did not close any row (still `progress() == (0, 17)`), but ruled out
  a cheap next step and, more importantly, corrected a false claim `pf-adversary`
  found in this same round before it reached main. Recorded as a negative result,
  not a stall.
- **M2/M3/M4** -- not touched, not claimed.

## what was tried

`src/pirateforce_foundation/gm/gmui_log_type_join.py` (new) runs two searches
against the pinned `gmui_label_block.tsv` (37 rows, all captions/options/units/tab
titles, not only the 16 row labels) and `gm_tool_log_types.tsv` (97 GMTOOL log
messages):

1. **Whole-string join** (`CANDIDATES`): substring containment, both directions.
   3 hits, all tracing to one place: block row 1896 (page-3 row-5 caption, a
   two-word compound) whose two halves separately equal two different full log
   messages (ids 4 and 12), and one of those same words is also the page-3 tab
   title (block 1891) -- which covers all five rows under it and so cannot be
   evidence about any one of them. `NO_JOIN_SURVIVES_BECAUSE` records this.
2. **Rare-overlap join** (`NOTABLE_OVERLAPS` / `rare_overlaps()`): longest-common-
   substring, kept at length >= 6, then filtered to substrings recurring in at
   most 1 of the 97 log messages. 7 notable substrings on today's data, 4 rare
   ones. The one worth naming: the word this table spells for "monster" links
   the GMUI row captioned "monster that spawns" (block 1399, page 2 row 1) to the
   log message for "monster (loot) drop" (log id 1) -- same noun, different verb
   (spawn vs. drop) -- read by hand and rejected, not promoted.

`backed_matches()` returns `()` under both searches. Promotion requires an
attended observation (pressing a row's button and watching the log-type's
`n_LogType` appear in a server log), never name similarity alone -- stated in the
function's own docstring so the next round knows the actual bar.

### hardest part: not the search, the search's own false claim

The first draft of this module's `LOG_TYPE_TABLE_IS_ITEM_ECONOMY_BOOKKEEPING`
constant claimed "none of the 97 messages contains a word for a player, a
monster, a ban, a kick, a warp, or a faction". `pf-adversary` (this round) showed
that half of that sentence was false by direct grep: log id 1 names a monster,
log ids 14/43/47 name a player. Ban, kick, warp and faction are genuinely absent
(re-verified this round with a direct grep of all four words against all 97
messages -- 0 hits each) but the claim as written overstated what search 1 (whole-
string containment) could actually see: it is structurally blind to a word shared
between two *different* multi-word compounds, which is exactly the monster case
(`gmui_catalog.GMUI_LABEL_BLOCK_ROLES[1399]` = "monster that spawns" as one
compound, the log message = "monster drop" as a different compound -- neither
nests inside the other, so search 1's containment check cannot find it). Fixed
by adding search 2 above, and by narrowing the false claim to a checkable list
(`ACTION_ROWS_WITH_NO_LOG_MATCH`, 12 GMUI rows naming a distinct
world/player-administration action, each independently confirmed at 0 whole-
string hits) instead of a blanket vocabulary denial.

## `pf-adversary`

Dispatched at the start of the work (not held until commit time). Returned
**before push** (this is not `ADVERSARY_PENDING`). Findings, all fixed in the
same commit as the main work (no second commit needed -- nothing wrong reached
main or was ever pushed):

- **D1 (worst -- false completeness claim)** -- see "hardest part" above.
  Fixed: `LOG_TYPE_TABLE_IS_ITEM_ECONOMY_BOOKKEEPING` narrowed to what search 1
  can actually prove; `ACTION_ROWS_WITH_NO_LOG_MATCH` added as the checkable
  list; search 2 (rare-overlap join) added so the vocabulary overlap is surfaced
  rather than denied.
- **D2 (tautological test)** -- the old `test_log_type_domain_note_names_the_
  absent_categories` asserted the note's own English words against itself, which
  would pass unchanged even with the false claim in it. Replaced with a test that
  checks the note *points at* `ACTION_ROWS_WITH_NO_LOG_MATCH`, which the
  `WholeStringSearchCoverageTests` class checks independently against real data.
- **D3 (wrong count)** -- docstring said "all 39 block rows"; the real count is
  37 (`len(GMUI_LABEL_BLOCK_ROLES) == len(LABEL_BLOCK) == 37`). 39 only comes
  from double-counting the two ids (1404, 1405) that carry two merged roles each
  -- the code does not iterate that way either. Fixed everywhere the number was
  written.
- **D4 (coverage test blind to a mid-loop skip)** -- the old test asserted hit
  ids were a subset of the full role dict, which a search that silently skips
  some ids still satisfies. `pf-adversary` inserted `if role == "undrawn":
  continue` mid-loop and the full suite stayed green. Fixed by having the search
  loop itself record, as its own last line, every block id it walked to
  completion (`_searched_block_ids()`), and comparing THAT set to the full role
  dict. Replayed the exact same mutation against the fixed test after the fix:
  now red, naming the two skipped ids (1396, 1403) directly in the assertion
  failure.
- **D5 (dead direction, untested)** -- `pf-adversary` deleted the
  `block_norm in log_norm or` half of the containment check and the full suite
  stayed green, because all three real hits fire through the other direction
  only on today's data. Fixed by extracting the predicate into
  `_is_mutual_substring` and pinning both directions directly with synthetic
  ASCII strings (`"cat" in "concatenate"` and the reverse), independent of
  whether real Thai data happens to exercise both today. Replayed the same
  mutation: now red.

Checked by `pf-adversary` and found NOT to be defects: the hit count (3,
reconfirmed in a fresh interpreter); the ASCII/cp874 claim (0 non-ASCII code
points added to either `.py` file, reverified after the fix); the
`backed_matches()` guard (seeding `_ATTENDED_CONFIRMED_JOINS` with the tab-title
id makes the two guard tests fail exactly as their docstrings say they should);
whether log ids 4/12 have a hidden structural kinship that would flip the
"coincidence" verdict (checked: `n_ID == n_LogType` for all 97 rows, i.e. there
is no separate category axis in this table to exploit either way).

## evidence

- Commit (pirate-force-server, one commit -- the adversary fixes landed before
  anything was ever pushed, so there is no separate "fix commit"): `f617e932`.
  Files touched (3, all inside this lane's write zone): `src/pirateforce_
  foundation/gm/gmui_log_type_join.py` (new), `tests/test_gm_gmui_log_type_join.py`
  (new), `docs/GM_LANE.md` (append only). **Not touched**: `runtime.py`, `app.py`,
  `v141`, DB, `scenarios/world_*`, `scenarios/combat_*`, `field_mobs.py`,
  `mob_viewer_link.py` (verified with `git diff --cached --name-only` before
  commit).
- `git diff --check` empty on both repos.
- Added lines in both `.py` files: **0 non-ASCII characters** (checked by direct
  codepoint scan, not just eyeballing) -- Thai text stays in the already-committed
  `.tsv` data files this module reads, same posture as `gmui_catalog.py`.
- `-k gm_` subset: **2695 passed**, 0 red (up from 2679 before this round's two
  new files; 1438 subtests passed).
- Full suite (`pytest tests/`), run once, after `git merge origin/main`
  (`44f43669` -- "Already up to date", branch was cut from that same commit and
  main did not move during the round): **11627 passed, 356 skipped (all
  pre-existing, 0 new), 22004 subtests passed**, 0 red. Took ~9.5 minutes.
- `tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` (run from
  `pf_bridge`): **PASS** (cp874, no new skips, main-is-ancestor, precondition
  census agrees, both branches mergeable, bridge file sizes under ceiling --
  `NOW.md` at 11,938 / 12,288 bytes, unchanged by this round).
- `tests/test_tree_is_cp874_safe.py`: 5 passed, 673 subtests (up from 663 before
  this round's files were added).
- Both of `pf-adversary`'s mutations replayed against the fixed test suite after
  the fix: both now fail red as intended (checked directly, not assumed from the
  fix alone).
- `BYTECODE_PURGED: PYTHONDONTWRITEBYTECODE=1 + python3 -B for every command this
  round.`
- No `rm -r`/`rm -rf`, any spelling, used this round.

## nonclaim (mandatory)

**GM skipped which steps: none.** No account received GM status this round. No
frame went out on the wire. The game was never booted. What this round produced
is a **ranking tool over two already-committed text tables**, not a feature --
no milestone is claimed from it.

- Does not claim any GMUI button is wired -- `gmui_catalog.progress()` is still
  `(0, 17)`, unchanged. `backed_matches()` on the new module is `()`.
- Does not claim the "monster" overlap (or any of the 4 rare overlaps) IS a real
  join -- read by hand, explicitly rejected, recorded in `docs/GM_LANE.md`. A row
  clearing the bar needs an attended pass watching a server log, not a table.
  This is the reason `backed_matches()` requires manual promotion via
  `_ATTENDED_CONFIRMED_JOINS` and does not auto-promote rare overlaps.
  Reason it is not automatic: a rarity filter distinguishes "uncommon" from
  "common" vocabulary, not "the same action" from "the same noun used for an
  unrelated action" -- the monster case is exactly that gap (spawn vs. drop).
- Does not claim the whole-string search is exhaustive proof that no GMUI action
  has ANY committed log-type counterpart -- it proves no WHOLE CAPTION matches;
  a word-level/tokenized join (splitting Thai compounds by vocabulary, which
  this round did not build) could in principle find something search 1 and 2
  both miss. Left as an open question for whoever picks this up next, not
  papered over.
- Does not claim `pirate-force-server#878` is merged -- open, PF-AUTOMERGE: v4
  present (confirmed by GET), waiting on gate. Will be on main only once a later
  round confirms with `git merge-base --is-ancestor <sha> origin/main`.
- Does not claim this round consumed any letter -- mailbox check found 0 pending
  `ADDRESSEE: GM` items; no letter was sent out this round either (nothing this
  round found needed COO's decision -- the negative result stands on its own
  evidence).

`TWO_SESSIONS_SAME_SCENE:` this round never touches shared per-scene world
state -- both new files are pure functions over already-committed, read-only
data tables (`gmui_label_block.tsv`, `gm_tool_log_types.tsv`), imported nowhere
in the boot/session path, with no caller and no per-session or per-scene state
of their own.

## next round

1. Check `pirate-force-server#878` merge state with `git merge-base
   --is-ancestor f617e932 origin/main` before writing "on main" anywhere.
2. Re-check items 1 and 2 from this round's own list above (chief's D3/D4/
   GM-060 fold into `runtime.py` + `docs/PROMOTION_BACKLOG.md`; whether
   CORE-REQUEST-GM-061 got a `runtime.py` mount point and a GT number) --
   neither was ready this round, may be by the next one.
3. If neither of the above is ready: the open question this round leaves is
   whether a tokenized/word-level join (not whole-string, not raw LCS) would
   find a real signal beyond the 4 rare overlaps already read and rejected --
   would need a real Thai word list or a hand-built stoplist of the generic
   words this round found noisy (player, item, change, character) to be worth
   attempting rather than repeating the same false-positive flood a naive
   n-gram search over Thai (no word spaces) produces at low thresholds.

SCOREBOARD: NONE | ยังไม่มีอะไรใหม่ที่ผู้เล่นทำได้วันนี้ที่ทำเมื่อวานไม่ได้ -- รอบนี้เป็นงานจัดลำดับภายใน (จับคู่ป้าย GMUI 16 แถวกับตาราง log type 97 แถวของไคลเอนต์ แล้วพิสูจน์ว่าไม่มีคู่ไหนแข็งแรงพอจะเดินสายก่อน) ไม่มีปุ่มไหนถูกกดแล้วทำงานเพิ่มจากเมื่อวาน | pirate-force-server#878 (เปิดแล้ว รอ gate, sha f617e932) + pf_bridge#1414
