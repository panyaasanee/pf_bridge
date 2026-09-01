# LANE-A round `of27sx` -- 2026-08-28T08:32+07:00

## Protocol A (previous-round PR lock check)
Pre-verified by the orchestrating session before this round started:
`pirate-force-server#183` and `pf_bridge#282` both `merged=true` (`pull_request_read`
direct). No recovery needed. Re-confirmed from this round's own fresh clone: both repos'
`main`/`origin/main` are clean, no ahead/behind surprise, HEAD on `pf_bridge` is `427f19c`
(sync commits only after the merge), HEAD on `pirate-force-server` is `496bd23` (merge of
PR #184, a source-less LANE-E mailbox round, `nwq79a`).

## Protocol B (mailbox sweep)
`grep -rl "ADDRESSEE: LANE-A" notes_to_chief/ --include=*.md` (excluding `consumed/`)
returns exactly 9 files. Two of those are LANE-A's OWN prior outbound STATUS letters
(`20260828_0427_LANE-A-STATUS-re119-*` and `20260828_0529_LANE-A-STATUS-mailbox-closeout-*`)
-- the string `ADDRESSEE: LANE-A` only appears in their own body text describing the
mailbox-check method, not in a header addressing them TO lane A -- so per the standing
rule these are not inbox items. The other 7 are genuinely addressed to LANE-A and every
one of them already has a `.CONSUMED.txt` stub next to it (checked with the CORRECT
naming rule from `20260828_0043_COO-DECISION-consumed-txt-naming-standard.md`:
`<full filename incl. .md>.CONSUMED.txt`, not the `.md`-stripped variant my first grep
pass used, which produced 130+ false "UNCONSUMED" hits before I re-read the standard and
redid the check correctly):
- `20260827_2305_KA1A-NUDGE-idle-lanes-*.md` -- STUBBED
- `20260827_1450_ATTENDED-REPLY-LANE-GM-1936-*.md` -- STUBBED
- `20260827_2010_PANYA-DECISION-pause-M2-*.md` -- STUBBED (the pause order itself)
- `20260827_2240_KA1A-NOTE-GT110-unsafe-*.md` -- STUBBED
- `20260828_0150_M1P-RESULT-PASS-*.md` -- STUBBED
- `20260827_1855_PANYA-ORDER-diag-multi-object-*.md` -- STUBBED
- `20260828_0235_KA1A-FOUND-GO-button-*.md` -- STUBBED

**Result: mailbox is genuinely clean. Nothing new to consume this round.**

## Backlog review (BUILD-001 done, BUILD-002 paused -- confirmed not lifted)
Re-checked `notes_to_chief/` for any note dated after `20260827_2010` that lifts the M2
pause: none exists. `PANYA-DECISION 0200` (2026-08-28) explicitly reorders priorities
without lifting the pause (#6 on its list: "M2 ยังพัก"). **BUILD-002/M2 not touched this
round, per standing owner order.**

With BUILD-001 shipped and reconfirmed (`qynsyw` round), I walked every M1-P2 gap the
owner named in her PASS letter (`20260828_0150_M1P-RESULT-PASS-*.md`, 6 numbered gaps +
1 addendum item) to find real, buildable backlog:

1. **Arrival census (gap 1):** already wired -- `CORE-REQUEST-026` landed R207
   (`pirate-force-server@13fe3aa`), `GT-121` open and ready for an attended session.
   Nothing to build.
2. **Heading (gap 2):** `RE-116` (RE runner, closed 05:16 this morning) is a clean
   bounded-negative -- exhaustive CFG trace of `CNetNPC`'s spawn path shows heading comes
   from `MovementAttr+0x34`, and BOTH the raw `.npc` placement floats and
   `MARKER.n_DIRTECTION` were checked as candidate crosswalk sources with **no** edge
   into that path. `BUILD_IMPACT: hard guard / no direct patch requested` -- explicitly
   forbids presenting the current four-way round-robin as authentic. Nothing to build
   until new data exists; `scene2_prison_exile_tables.py`'s own docstring already carries
   this caveat (I did not need to touch the module).
3. **Name color (gap 3):** `RE-109` closed bounded-negative, needs an attended
   `GT-114` (DIAG-001) field-diff run, wiring already landed R202. Not a static-build
   item, and not something lane A can force an attended session to happen.
4. **Density/scale (gap 4):** M1-P's own letter assigns this "สาย B/A" jointly and it
   depends on LANE-B's own placement-count measurement (`u16_1 ~= intended count 78%`,
   already LANE-B's finding, not re-derived here). No LANE-A-only action this round.
5. **Missing quest NPC "Mirage reel" (gap 5):** genuinely unticketed. See below --
   this is the one item this round turned into real backlog motion.
6. **Pose (gap 6):** owner said she will attach reference screenshots for comparison;
   nothing to build against yet (no source image, no field candidate beyond the
   `MOBS.n_AI_WANDER` hint already recorded in the owner's own letter).
7. **Attr completeness (addendum item 7 / `PANYA-DECISION 0200`):** RE runner's job
   (`RE-122`, closed 08:15 this morning as bounded-negative -- MP and 5-stat base values
   have no provenance anywhere in `external/`+`gamedata/`, hard guard against
   fabricating `MP=50` or similar). Nothing for lane A to build until that RE ticket (or
   a successor) finds real values.

## What I actually did: opened `RE-123` (CLIENT_RE_QUEUE.md)
Gap 5 (Mirage Reel) had never been ticketed anywhere (grepped both queue files and
`notes_to_chief/` for "Mirage" before opening -- zero hits besides the owner's own PASS
letter). Rather than guess an n_ID and inject a row into
`scene2_prison_exile_tables.py` without evidence (exactly what the module's own
docstring and CHARTER forbid), I did the cheap, bounded check that was actually in
lane A's own domain -- re-verified against the placements TSV lane A itself built
(`scene2_prison_exile_tables.py`'s 106-row join: 97 resolved + 9 unresolved) that
**none** of the 106 rows are named "Mirage reel" (cross-checked the 9 unresolved n_IDs'
real `MOBS_TIP` names: 37/101/102/103/104 = "Port transportation"/"Swamp
Tortoise"/"Orc"/"Orc Chief"/"Port transportation" -- none match). That rules out "it's
just an unresolved placement row" as the explanation and narrows the real question to
"quest-conditional spawn", which needs `QUESTDATA_TH__QUEST.tsv` /
`QUESTDATA_TH__QUESTTALK.tsv` / `gamedata/lua/Quest/` cross-referencing against 19
candidate `MOBS_TIP` n_IDs sharing the generic name "Mirage reel" -- RE-runner
methodology (T0-T4, provenance, nonclaims), not a lane-A code change. Opened
`RE-123 BG0002-MIRAGE-REEL-QUEST-SPAWN-CROSSWALK-001` in `CLIENT_RE_QUEUE.md` with that
narrowed scope and the negative check already done so RE runner does not have to redo it.

**Numbering:** shared RE/GT counter's highest before this round was `RE-122`/`GT-121`.
Grepped `RE-123`/`GT-123` = 0 hits across `CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`,
`notes_to_chief/`, `rounds/` at time of reservation (2026-08-28T08:3x+07:00) before
writing the entry.

## No code changes in `pirate-force-server` this round
Every avenue above either (a) is already wired and just needs an attended session
lane A cannot force, or (b) is a closed RE bounded-negative with an explicit
`BUILD_IMPACT: hard guard`, or (c) needs new RE work before there is anything true to
encode. Writing a src/ change against any of them right now would mean either
duplicating work already done, or fabricating a value/crosswalk the project's own rules
(and this round's own re-derivation of RE-116/RE-122's findings) explicitly forbid.
**Zero files touched in `pirate-force-server` this round** -- no placeholder commit made
there, per the standing rule against empty commits for their own sake.

## pf-adversary self-review (against `.claude/agents/pf-adversary.md`, this repo)
Applied to the one real change this round (the `RE-123` queue entry, since there is no
code to review):
- **Stale pins / re-derivable numbers:** the "19 candidate n_IDs" and "106
  rows/97+9" counts were re-grepped THIS round, not copied from the owner's letter or
  `scene2_prison_exile_tables.py`'s docstring from memory -- both counts independently
  reproduced (`grep -c "Mirage reel"` = 19; docstring's 97+9=106 arithmetic re-checked
  against the same TSV).
- **File exists on disk != file is in the repo:** confirmed with `git ls-files` that
  `QUESTDATA_TH__QUEST.tsv`, `QUESTDATA_TH__QUESTTALK.tsv`, `QUESTTEXT_TH__TEXT_QUEST.tsv`,
  `TEXTDATA_TH__MOBS_TIP.tsv`, and `gamedata/lua/Quest/` are all tracked, not just present
  locally -- RE runner can read them on the cloud clone.
- **Single-source claim:** "not in the placements TSV" is cross-checked two ways --
  the module docstring's own accounting (97+9=106, all rows classified) AND my own fresh
  grep of `TEXTDATA_TH__MOBS_TIP.tsv` at the specific 5 unresolved n_IDs, which agree.
- **Unlabeled proposal vs measurement:** the ticket text marks the "ruled out: not a
  static placement" line as something checked this round, not carried over as an
  assumption from the owner's addendum, which had left it as an open branch
  ("อาจเป็น static ที่ยัง unresolved หรือ spawn จากเควส").
- No defect found worth blocking on; nothing else to adversary-review this round (no
  code, no scenario, no workflow changed).

## CORE-REQUEST
none -- `CORE-REQUEST-026` (last one lane A opened) is already wired (R207); no new ask
for chief this round.

## เปิดใบให้สาย C (RE runner via CLIENT_RE_QUEUE.md)
`RE-123` -- see above.

## nonclaims
Did not touch `runtime.py`/`app.py`/`current/pf_login_game_server_v141.py`/canonical
DB/capture corpus/client image. Did not touch `GAME_TEST_QUEUE.md` (no GT ticket opened
or closed this round -- only `CLIENT_RE_QUEUE.md`). Did not resume BUILD-002/M2. Did not
edit any other lane's open ticket header. Made zero changes in `pirate-force-server`.

-- LANE-A (WORLD)
