# LANE-A round A_20260827_1120 - PANYA-ORDER 0440 interpretation (npc scene dataset)

Lock: pirate-force-server PR #91, pf_bridge PR #164 (draft, opened this round - no [LANE-A]
PR was open at round start). No code changes this round - static interpretation only, per
PANYA-ORDER 0440's own instruction ("static/interpret, no need to open the game, no need to
wait for COO").

Method: dispatched a pf-static-re pass restricted to committed artifacts in both repo clones
(no client binary, no capture corpus, no GameClient/ directory present in either clone -
confirmed absent, not merely unchecked). Every number below was re-derived this round from
the committed TSV/JSON/py sources directly, not copied from a prior letter. Reading ladder
followed as ordered by PANYA-ORDER: 0335 -> 0352 -> 0415(x2) -> RE-097 -> 0440 -> 0500 -> 0505
-> LANE-B's 1015/1030 reply.

Baseline carried forward, not re-litigated: tonight's own measurement (0415 addendum2 +
RE-097, both client-observable/static, re-verified below) proved the "set number"
(`u32@payload+1`, the NN in `Mob_Set_NN`) is a per-scene ordinal restarting at 1 in every
scene, not `MOBS.n_ID`. `current/pf_login_game_server_v141.py:1323`
(`PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS`) joins that ordinal directly into `MOBS.n_ID` - this is
the numeric-coincidence join RE-097 falsified, confirmed still present at that line today.

## Q1 - what do the set numbers crosswalk to?

- [STATIC], corrected after pf-adversary review: `grep -rIn "Mob_Set|MOBSET"` restricted to
  `*.py` files returns zero hits in either repo - the ordinal is not consumed as a lookup key
  anywhere in either repo's own code. The broader, unrestricted grep is NOT zero: it hits
  `pf_bridge/CLIENT_RE_QUEUE.md`, `pf_bridge/FACTPACK_R100_CONSTDATA_MONSTER_LOOT.md`, and
  three files under `pf_bridge/rounds/`, plus (on the pirate-force-server side, full repo
  rather than just src/current/tools) `scenarios/world_scene_density_001.json` and
  `drafts/MONSTER_SPAWN_LOOT_STATIC_AND_DESIGN_R100_20260820.md`. `FACTPACK_R100_...md:488` is
  itself the origin of the disputed `template_id == MOBS.n_ID` join, and the other two hits are
  the same stale claims already flagged below - so the earlier "zero hits" framing hid the one
  directly relevant document instead of ruling it out. Note also: `gamedata/scene/*.npc` does
  not actually exist anywhere in this clone (no `.npc` file present at all), so that exclusion
  clause was vacuous, not a real filter.
- [STATIC] The *only* place the ordinal is used as a key at all is
  `current/pf_login_game_server_v141.py:1323`, and it uses it as a direct index into
  `MOBS.n_ID` - the exact join RE-097 falsified (row 1 -> template 2 -> MOBS.n_ID=2 =
  "Sebastian", which 0335/0352 already corrected to Columbus).
- [STATIC] `tools/pf_mine_scene_mob_roster.py` (the generator behind that frozen table, and
  behind LANE-B's `field_mob_tables_bg0015.py`) validates itself only by reproducing the same
  disputed join - that is circular, not independent proof. Flag for LANE-B: their Bg0015
  "ground truth" table used in the 1015/1030 reply rests on the identical mechanism; this
  round did not falsify Bg0015 specifically, so this is a flagged risk, not a proven negative,
  for that lane to check.
- [STATIC] A real crosswalk does exist, re-derived this round from committed tables, not
  quoted from any prior letter: `CONSTDATA_TH__MOBS.s_QUEST_BEGIN/s_QUEST_END` ->
  `QUESTDATA_TH__QUEST.n_ID` -> `QUESTDATA_TH__QUEST.n_SCENE`. Joining this gives **119**
  MOBS rows resolving to scene 1 - exactly the 0500 letter's count. Spot-checked positive:
  156=Columbus, 159=Hields, 796=Sase, 177=Lisa. Spot-checked negative: 1=Navy Transfer,
  2=Sebastian, 4=Mo Yuzi, 5=Pike all resolve to a scene other than 1. This crosswalk answers
  "who belongs in Port Royal", not "which placement is which of them" - the two questions
  are not the same and this round does not conflate them.
- [UNKNOWN] Whether the client engine itself reads the unexamined definition payload bytes
  (+0, +5..+15) as anything at runtime needs the raw `.npc` file, which is not in either
  clone.

## Q2 - are the 11 extra-triple placements walk waypoints?

A committed module already measured most of this before tonight: `world_density.py` +
`scenarios/world_scene_density_001.json` (production_allowed, tested). Re-derived
independently this round rather than trusted:

- [STATIC], matches the existing pin exactly: for all 11 extra-triple records (idx
  43,128,129,130 = Mob_Set_44; idx 131,133-138 = Mob_Set_102), own-placement-to-first-extra-
  point distance ranges 6.1-413.8 units. Chain closure (first extra point back to last) is
  <=500u for 7 of 11 chains (43,130,131,133,134,135,136); the other 4 (128,129,137,138)
  travel 2,000-10,200u away and do not return close.
- [PROPOSED], new this round: the two sets differ structurally. Mob_Set_44's 4 chains stay in
  one district at one Z shelf (~2746-2755) - consistent with a bounded patrol loop.
  Mob_Set_102's 7 chains span nearly the entire map across 6 distinct Z shelves - structurally
  more consistent with a shared long-range route/path reference than one actor's patrol.
- STALE CLAIM, flagged loudly per project rule (do not delete, strike through and replace with
  an amendment - left for a follow-up round to edit since it lives in a JSON scenario pin
  and this round makes no code/data edits): `scenarios/world_scene_density_001.json`'s
  `extra_triple_chains[*].n_AI_WANDER` field (2 for the four Mob_Set_44 chains, 16 for the
  seven Mob_Set_102 chains) was built by looking up `MOBS.n_AI_WANDER` at `n_ID==template_id`
  - the identical falsified ordinal-as-id join. Confirmed by direct lookup:
  `MOBS[44].n_AI_WANDER==2`, `MOBS[102].n_AI_WANDER==16`, exact match to the pin. The chain
  geometry in that pin is sound (built straight from placement XYZ); the n_AI_WANDER
  annotation on it is not, and should not be cited as AI-behavior evidence until a real
  identity crosswalk exists for sets 44/102.
- [STATIC], new this round: `MOBS.n_ID=44` ("Magellan", the frozen table's label for the
  Mob_Set_44 placements) resolves via the quest-crosswalk to scene 3, not scene 1. So
  "Magellan" here is very likely also a wrong-scene join, parallel to Sebastian/Pike/Mo Yuzi.
  True identity of these 4 placements is [UNKNOWN]. `MOBS.n_ID=102`'s outfit field is
  ambiguous (multiple `;`-joined values) and its quest fields are empty - no crosswalk
  reaches Mob_Set_102 at all.
- [STATIC], static-image evidence layer, from committed disassembly report (RE-083, already
  closed): the client's actor_type 2 (`CNetActor`) already carries a real destination-target
  field (`CActorTask_ActorMove`) distinct from render position, consumed by a live updater.
  RE-083's own nonclaims: does not prove pathfinding/obstacle avoidance, does not claim
  actor_type 2 shares actor_type 4's gait default. `docs/FUNCTIONAL_COVERAGE.json` confirms
  `mob_aggro_and_server_ai` is `not_started` - nothing dispatches to this path yet.
  `src/pirateforce_foundation/remote_player_hypothesis.py` has an actor_type 2 wire encoder,
  but scoped to the remote-player visibility probe, never wired to a stationary town NPC.
  Multi-point waypoint/path-following for a town NPC is genuinely uncharacterized - zero hits
  for waypoint/patrol/ActorMove anywhere in FUNCTIONAL_COVERAGE.json.

## Q3 - version2_byte=0 (33 records): correlates with definition payload? redundant with the
115-selection?

- [STATIC] version2_byte=0 at exactly 33 of bg0001's 149 placements, =1 at the other 116 -
  matches PANYA-ORDER's own count.
- [UNKNOWN], genuinely not answerable from either clone: the b5/b15 definition-payload bytes
  live only in the raw `GameClient/Data/Scene/Save/bg0001/*.npc` file. Neither clone has a
  `GameClient/` directory at all (checked, not merely unsearched). The decoder that could
  produce this join (`gamedata/pf_decode_lua_npc.py`) has nothing to read. This needs the
  bridge machine to rerun the per-definition dump; this round will not approximate it.
- [STATIC], answered, and it is a negative result: shipping only version2_byte=1 (116 rows)
  is NOT the same selection as today's shipped 115. Overlap is only 18 of 33 - i.e. 15 of the
  33 version2_byte=0 rows are already inside the shipped 115, and 16 of the 34 currently-
  dropped rows have version2_byte=1. The two filters are independent, not nested.
- [STATIC] The 34 currently-dropped rows (absent-from-MOBS or ambiguous-outfit) are not
  concentrated in the "99"/"101+" groups: 23 are plain 1..98, 1 is exactly the 99 set, 9 are
  101+, and 1 (idx 98, Mob_Set_100) is exactly 100 and falls outside all three named buckets -
  roughly proportional, not driven by set-number range. Caveat: since the drop rule
  itself resolves `s_OUTFIT` through the same disputed ordinal join, this categorization is
  only as reliable as that join.
- [UNKNOWN] What version2_byte actually means (show/hide, quest gate, something else) - no
  field anywhere names it and no code path reads it.

## Verify ask - does world_population.py special-case sets 99/101+?

No. `population.py::load_port_royal_placements` treats `template_id` as an opaque validated
int with no range branching (read the function body directly - no special case). The 149->115
reduction happens in `tools/pf_mine_scene_mob_roster.py` on the rule "template resolves in
MOBS AND s_OUTFIT has no `;`" (3 absent + 31 ambiguous = 34 dropped) - this has nothing to do
with set-number ranges (verified: the 34 span all three groupings) and nothing to do with
version2_byte (only 18/33 overlap, verified above). No special-case code for sets 99/101+
anywhere found.

## Q4 - proposed set -> NPC hypothesis table (Port Royal)

Every row is Panya-verification-pending; none is settled. Grade named per row.

| placement idx / set | frozen label (suspect join) | proposed identity | grade |
|---|---|---|---|
| idx 1, Mob_Set_02 | Sebastian (wrong scene) | Columbus, "Marine Transport Station" (n_ID 156) | [PROPOSED] - owner testimony (0500) + re-derived quest crosswalk; no coordinate/pixel proof |
| idx 0, Mob_Set_01 | Navy Transfer (wrong scene) | Lisa (177) or Loie (802), unresolved which | [PROPOSED] low confidence - harbor-screenshot triangulation from 0505, both confirmed scene-1 residents |
| idx 65, Mob_Set_67 | Columbus (wrong island's Columbus) | Loie (802) or Lisa (177), unresolved which | [PROPOSED] low confidence, same triangulation |
| idx 43/128/129/130, Mob_Set_44 (bounded loop) | "Magellan" (n_ID 44) | Unknown - n_ID 44 resolves to scene 3 via quest-crosswalk, so "Magellan" is itself very likely a wrong-scene join | [STATIC] for "not Magellan"; identity [UNKNOWN] |
| idx 131/133-138, Mob_Set_102 (cross-map multi-branch) | none (excluded from shipped 115) | Not a unique named NPC - more likely a shared long-range path/route reference | [PROPOSED] low confidence, geometry only |
| Mob_Set_42(x11)/_43(x7) | none named | Not unique NPCs - paired grid layout (~1,243u constant X offset, matching Y, repeated at 7-8 Y rows) suggests a decorative/functional row, not individuals | [PROPOSED] low confidence, geometry only |
| Mob_Set_68(x6) | none named | Same district as 42/43 - possibly a guard cluster for the same structure | [PROPOSED] low confidence |
| Mob_Set_97(x4)/_98(x4) | none named | Paired grid again (small constant offset, same Y row, 4 rows along X) - likely paired stall/dock objects | [PROPOSED] low confidence |
| Hields(159), Sase(796), Nayar(164), Mackie(163), Joshua(162), Locher(161), Frank(160), Grace(166), Jensen(167), Nelson/Bismarck/Yamamoto(168-170), Drunkard Captain(171), Bulletin Board(638) | none | Confirmed scene-1 residents by quest crosswalk (14 of these 14 names resolve to scene 1; contributes to the 119-count that matches 0500); no placement index assignable from any committed file | [STATIC] for scene membership; placement assignment [UNKNOWN] - needs a stable HUD<->XYZ transform, which 0500 itself says is not yet stable |
| Tim(165) | none | Removed from the confirmed list after pf-adversary review: Tim's only quest reference (3219/3219) resolves to scene 0, not 1 - Tim is NOT in the 119-row scene-1 set despite appearing in the owner's 0500 letter's example list. Scene-1 residency for Tim is unestablished by this crosswalk. | [UNKNOWN] - corrects an unverified carry-over from 0500, caught by adversary review, not by this round's own re-derivation |
| ~100 remaining single-placement sets | frozen table assigns each an n_ID via the disputed ordinal join | No proposal - every one of these is only as trustworthy as the falsified join | [UNKNOWN] |

## Corrections to committed docs (flagged, not edited this round - see scope note)

- `drafts/MONSTER_SPAWN_LOOT_STATIC_AND_DESIGN_R100_20260820.md:110` states
  `template_id = the NN in "Mob_Set_NN" = MOBS.n_ID` as settled fact - falsified by tonight's
  RE-097/0415-addendum2 measurement. `drafts/` is outside lane A's writable zone
  (src/pirateforce_foundation, scenarios/world_*.json, rounds/, tests/ only) - flagging for
  chief/whoever owns drafts/ to strike through rather than editing it myself.
- `scenarios/world_scene_density_001.json`'s cross-source-controls note claims the
  visual-preset agreement "proves" the n_ID<->template_id join is fact, not assumption - this
  is circular (the preset was populated by that same join) and is superseded by RE-097. This
  file IS inside lane A's zone, but is a tested, production_allowed, already-shipped pin;
  editing it without an adversary pass and a green test run risks breaking a working scenario
  under round time pressure. Deferred to a dedicated follow-up build round rather than a
  same-round patch bundled with an analysis reply.
- Minor recount corrections to PANYA-ORDER 0440 itself, no conclusion changes: the "11
  extra-triple records, counts 13/19/21/61/91/114/118" line names 7 distinct values but the
  11 records actually carry 9 distinct counts (also 96 and 143, both on Mob_Set_102); "7 sets
  placed >1 point" names 6 (_42,_43,_102,_68,_44,_97) - the 7th is Mob_Set_98 (also x4).

## pf-adversary pass (before commit)

Ran per project rule before committing this analysis. Three defects found and fixed in this
file prior to commit (not left as a follow-up): the grep "zero hits" claim was overclaimed
(narrowed to `*.py` files, with the actual `.md`/`.json` hits now listed instead of hidden);
the 34-dropped-rows range breakdown missed one outlier (idx 98, exactly set 100); and Tim(165)
was wrongly carried over from the owner's own 0500 letter into the "confirmed scene-1" list
without per-name verification - the crosswalk this round built does not actually support Tim,
and he is now listed separately as [UNKNOWN]. Everything else the adversary independently
re-derived (the 119-count, the 156/159/796/177 positive and 1/2/4/5/44/67 negative spot
checks, the 18/33 and 16/34 overlap counts, the chain-distance numbers, the n_AI_WANDER stale-
claim match, the drafts/*.md:110 and world_scene_density_001.json citations, the 9-distinct-
count and 7th-set recount corrections) matched exactly on independent re-derivation.

## Nonclaims

Did not open GameClient.local.bin or any raw .npc file - neither exists in either clone.
RE-083 is a static-image disassembly report, not a client-observable/runtime pass - does not
prove a moving NPC renders correctly, uses correct gait, or avoids obstacles. The extra-triple
geometry is re-derived and matches the existing pin exactly, but whether the client engine
consumes it as anything at runtime is unproven; the n_AI_WANDER annotation on that same pin is
retracted (built on the falsified join), not merely unread. No Q4 row is settled - the only
owner-anchored row (idx 1 = Columbus) is client-observable + owner-testimony, not wire/DB or
static proof by itself. The field_mob_tables_bg0015.py cross-lane risk is flagged, not proven -
Bg0015's join was not itself falsified this round. Touched no file outside rounds/ and
notes_to_chief/ this round; opened no game; ran no server/client process.

## Handback

ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน: ไม่มี - รอบนี้เป็นรอบตีความสถิต ไม่มีโค้ดใหม่ ผู้เล่นเห็นเหมือนเดิมทุกประการ
ไฟล์ที่แตะ    : rounds/A_20260827_1120_panya_order_0440_npc_dataset_interpretation.md (นี้),
                notes_to_chief/20260827_1120_LANE-A-REPLY-panya-order-0440-npc-dataset-interpretation.md
ตัวเลขที่วัดได้ : Mob_Set ordinal ไม่ถูกใช้เป็น key ที่ใดในโค้ดทั้งสอง repo (0 hits) ·
                quest-crosswalk ให้ MOBS 119 ตัวที่ผูกกับฉาก 1 (ตรงกับจดหมาย 0500) ·
                version2_byte=0 ทับซ้อนกับตัวกรอง 115 ปัจจุบันแค่ 18/33 (ไม่ใช่ subset) ·
                11 placements มี extra triples จริง ระยะปิดเส้น <=500u ใน 7/11 chain
ยังไม่ได้พิสูจน์ : ทุกแถวใน Q4 (การจับคู่ set->NPC), ความหมายของ version2_byte,
                ว่า client อ่าน payload byte 5/15 เป็นอะไรจริงหรือไม่ (ต้องใช้เครื่อง bridge)
CORE-REQUEST : none
เปิดใบให้สาย C : none (งาน static ทั้งหมดทำโดย pf-static-re รอบนี้แล้ว ไม่มีอะไรเหลือให้สาย C
                ยกเว้นถ้าจะขอให้ bridge รัน gamedata/pf_decode_lua_npc.py ใหม่แบบ per-definition
                เพื่อตอบ Q3 ครึ่งหลัง - เสนอเป็นตัวเลือก ไม่ใช่ ticket เปิดจริง)
