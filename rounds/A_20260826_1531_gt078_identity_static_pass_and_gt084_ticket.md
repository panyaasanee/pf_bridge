# round `A_20260826_1531` * lane A * WORLD -- GT-078 identity: static pass result + GT-084 ticket

See `rounds/A_20260826_1531_lock_claim.md` for the lock-claim half of this round.

## what this round was chasing

`notes_to_chief/20260826_1442_COO-DECISION-GT078-wire-pass-identity-wrong-M1-not-declared.md`
ranks the `bg0001` placement->identity table above every other lane-A task until at least
Hields/Sase/Columbus are confirmed. This round ran `pf-static-re` on that question, then
`pf-queue-author` on the retest it points to. **No `src/`, `scenarios/` or `tests/` change
this round** -- nothing that surfaced is safe or player-visible enough to build on yet, and
the honest move per lane-A's own rule 2 is to build the *next decisive step*, not a guess.

## what `pf-static-re` found

Full findings are in the agent's own report; the load-bearing pieces:

- **Confirmed [STATIC]:** `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS`'s `template_id` column
  (`current/pf_login_game_server_v141.py:1323`, frozen, read-only) is the exact same ID
  space as `n_ID` in `pf_bridge/gamedata/tables/TEXTDATA_TH__MOBS_TIP.tsv` and
  `CONSTDATA_TH__MOBS.tsv`. Verified by exact string match on three unrelated rows
  (tid=1 -> "Navy Transfer"/no title, tid=2 -> "Sebastian"/"Warden", tid=36 -> "Columbus"/
  "Marine Transport Station"), not asserted. This is the resolution table the GT-078
  addendum asked lane A/RE to find, and it already exists in committed data -- no client
  binary access was needed.
- **Confirmed negative:** neither `159` (Hields) nor `796` (Sase) appears as a
  `template_id` anywhere in the 115-row table, nor as a `template_ids` value in the raw
  client scene decode `gamedata/scene/bg0001/bg0001.placements.tsv` (149 data rows, the
  whole scene, not just our 115). Their identities are not reachable through this table by
  any index. Does not rule out a quest/Lua-driven spawn (the owner's own hide/unhide theory
  in GT-078 §⑥) -- that layer was not read this round.
- **Open contradiction, flagged rather than resolved:** placement_index 0
  (`template_id=1`) is *already* `'Navy Transfer'`/no-title in both our frozen table and
  the independent raw client scene file -- two committed sources agree with each other and
  disagree with what the owner reports seeing on screen at that spot ("Marine Transport
  Station" title on a blonde woman). Re-reading the GT-078 coordinates: the "Marine
  Transport Station" observation was logged at S1b (-9,444/-2,950), not exactly at
  placement_index 0's coordinates (-9,139.95703125/-2,780.045166015625) -- the raw
  Euclidean gap between those two numbers is ~348.3 units. **That gap is not evidence of
  anything by itself: S1b's coordinates are HUD-space and placement_index 0's are
  table-space, and this round could not establish that the two spaces share an origin or
  scale (see the HUD/table-transform point below) -- so ~348.3 units is not "close" or
  "far," it is two numbers whose relationship is unproven.** The contradiction stands on
  its own regardless: two independent committed sources say "no title here," the owner
  says she saw one. **This needs a wire-confirmed click, not another round of
  screenshot-matching or coordinate arithmetic across unrelated spaces.**
- Two candidates for the bench-front ("Unemployed Sailor") and bench-side (red flower
  creature) spots -- placement_index 4 (tid=5, resolves to "Pike"/"Unemployed Sailor" --
  exact title-string match) and placement_index 59 (tid=61, resolves to "Toxic Vine", empty
  title) -- are **[hypothesis] only**, and weaker than "closest by distance" makes them
  sound: measured against S-CENTER (11,865/6,147, the only anchor GT-078 gives), the
  actual nearest of all 115 rows is placement_index 19 (tid=20, "Jefferson"/"Bomber",
  ~930.8 units), not index 4 (~1,272.7 units). Index 19 was set aside only because
  GT-078's own §⑧ table already lists "Bomber" as one of the correctly blue-titled NPCs
  visible in frame `20260826_133302.png` -- i.e. it looks already-right, not
  already-wrong -- but that reasoning was not spelled out anywhere before this correction,
  which made the original claim unreproducible from what was written. Proximity in this
  table's coordinate space is not proof of on-screen identity regardless; the
  HUD-X/Y-to-table-x/y relationship is itself unresolved (see next point). **Do not treat
  placement_index 4 or 59 as confirmed. They are not going into any code or scenario.**
- HUD X/Y (client) vs. this table's internal x/y: **unresolved, no landmark pair exists in
  committed data to derive a transform.**

## what this round built instead: `GT-084`

Rather than commit either hypothesis, this round asked `pf-queue-author` for the decisive
next test and got a better answer than expected: `describe_capture_event`
(`current/pf_login_game_server_v141.py:3288-3341`, called at `:7490`) **[STATIC, this round
re-verified independently against the actual production boot path -- app.py loads this
exact frozen file and only swaps the socket global, per `connection.py`'s
`adapt_game_listener` -- not just relayed from the ticket draft]: already computes
`placement_index = actor_id - 0x2000 - 1` and writes it straight into `GAME_EVENTS_LIVE.txt`
on every boot, no flag needed, for both `TARGET_VITAL` and `CHOOSE_NPC` events, neither of
which is suppressed by the capture-noise filter.** GT-078's own §⑤ click (`TargetVital
actor_id=0x0000000010010001`) already exercised this exact path; that particular actor_id
just doesn't correspond to any row in our 115-entry table, which is why it printed nothing
useful, not because the mechanism doesn't work. One caveat this round did not have before:
`placement_index` in the frozen table is **not** the dense range 0-114 the "census band"
shorthand implies -- the 115 rows actually span index 0 to 148 with 34 gaps inside that
span. A click that lands on one of those 34 missing indices will also print
`placement=unknown`, for a reason that has nothing to do with being off-model or
out-of-census -- `GT-084` and whoever reads its result need to tell those two `unknown`
causes apart, not collapse them.

`GT-084` (full text handed to chief in `notes_to_chief/`, this file's sibling letter) asks
the tester to stand at `S-CENTER` (the owner's own chosen spot, not the harbor -- GT-078
already ruled out testing near the dock again) and click/target the two specific
wrong-looking NPCs. No PASS/FAIL judgment is asked of the tester -- just point and click;
the placement_index arithmetic and the `TEXTDATA_TH__MOBS_TIP.tsv` lookup happen afterward,
off-session, from the log. That turns "she describes what she saw" into "the log states
which row it was," which is what actually closes this question.

## `ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน`

**Nothing, this round.** No code, scenario or test changed. Per lane-A's own third rule,
that sentence being unwritable for a round's *code* is exactly why this round's output is a
ticket and a findings note instead of a diff -- committing either hypothesis-grade
placement guess to fix the identity would be a fabricated fix, not a built one, and this
lane does not ship those.

## CORE-REQUEST

none

## เปิดใบให้สาย C (CLIENT_RE_QUEUE)

none new -- `pf-static-re` ran inline this round instead of queuing (see above); its open
items (Hields/Sase not in this table at all; the Navy Transfer contradiction; the HUD/table
coordinate transform) are recorded above for whoever picks this back up, not filed as a
separate ticket, because `GT-084`'s result is expected to answer them directly.

## ยังไม่ได้พิสูจน์

- Every placement_index this round touched, including the two "closest by distance"
  candidates -- **[hypothesis] status stands until `GT-084` returns a click-confirmed
  index.**
- Whether `--export-events`'s `PF-EVENT` stream carries `TargetVital` at all
  (`GT-084` records this as its own open sub-question, not an assumption).
