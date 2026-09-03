# R307 attended round - results (eight tickets, one boot, one new character)

- who: ka1-A (attended in-game tester), owner Panya at the keyboard the whole round; she chose the eight-ticket set and said "thraab" to the full step list before the boot
- when: 2026-09-03 17:22 -> 18:58 (+07:00), from bridge job stamps and the GM command log
- head (worktree at boot): cbf1561ac8ed132527e152481ebfb473889735b3
- boot commit: 618215232fbb12e31c2f7d983fdc6329ef96110e (GREEN; the resolver measured its tree equal to the head of main in every path a booted server can execute)
- boot tree: pf_bridge\boot_trees\r307_1480_20260903_172258
- run db: state\run_r307_20260903_172258.sqlite3 (throwaway copy; the new character lives only here)
- capture: GameClient\capture_r307_20260903_172258 (server_console_live.out.txt 8,389,060 B sha256 299275DB... / .err.txt 10,898 B sha256 18D1362A...)
- canonical sha: 4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454 - UNCHANGED before and after (job 1482)
- flags: none; PF_SPEED_TRIAL empty (checked in the boot process); no video
- RECHECK: all eight tickets PASS headless on the boot commit (job 1480 log: strings + pytest 49 / 34 / 108 passed); nothing was cut
- jobs: 1479b (parse check), 1480 (hold + wait-for-green + RECHECK + boot, PASS first attempt), 1481 (client relaunch for GT-217), 1482 (teardown PASS: listeners 0, clients 0, stopped markers 1, traceback 0, integrity ok, fk 0 rows)
- GM command log (UTC): create 10:28 · warp 2 10:3x · warp 1 10:52:57 · warp 2 10:55:24 · warp 3..11 chain 11:0x-11:13 · warp 12 11:14:08 (refused, typo) · warp 14 11:14:12 · warp 130 11:14:58 · warp 1 11:20:04 · warp 126 11:2x · warp 278 100 200 x4 11:43-11:5x · warp 14 / warp 1 11:5x

Boot-time lane tokens are still not in the summary logs (R306 finding 5); every boot-line criterion was measured on the boot tree instead.

---

## GT-215  ->  [PASS on its own claim]  +  🔴 finding for chief (class and birth values)

client-observable (owner): character-select photo taken -> create -> the client capped the name field at 10 characters ("ห้ามเกิน 10 ตัวอักษร"), so the name on screen and in the DB is `GT215BORN0` (the ticket's `GT215BORN01` cannot be typed; `GT215BORN02` neither) -> enter game -> Port Royal, HUD `HP 100/100 LV 1`, MP `0/1`, CP `0/100`, 1 gold -> walked W/A/S/D, moved. No refuse, no crash.

wire/DB:
- BEFORE (job 1480 on the run-DB copy, before the server started): the ticket's own SELECT fails on a pre-migration copy - `no such column: level` (the copy of canonical has only the 14 base columns, user_version 0; the vitals columns arrive when the server applies migrations 006-009 at boot). Rows: id 1 Arena01 only.
- CREATE: `[CREATE] op=1 name='GT215BORN0' selector=1 identity=(0,0) wire=224` -> `FOUNDATION_CREATE_COMMITTED (260 bytes)`.
- first login of the new character: `LOGIN_VITALS from_row level=1 hp=100/100 apply=carried` (the row was READ, not a constant) and no refuse token.
- AFTER (job 1482): `(2, 1, 'GT215BORN0', 1, 100, 100, None)`; typed columns `level=1 hp=100/100 mp_current=None mp_max=None speed_walk=400.0 class_id=None cash=None stat_str=None`; position row scene 1; backpack 5 rows (4 present at birth: 2600001, 2400901, 2600001, 2200002 + the Blue Talisman picked in GT-220).

🔴 Finding (owner's, confirmed on the wire and in the DB): **the class she chose at creation (Sharpshooter) is discarded - the character plays as Gladiator - and MP/CP/cash on screen are constants, not birth values.**
- The class choice IS in the CreateActorVital the server keeps raw as `actor_wire` (224 B): the field `19 04 00 00 00` sits where Arena01's wire carries `19 01 00 00 00` (1 = Gladiator per CORE-REQUEST-022). Byte-diff of the two blobs: offsets 0x22-0x2a differ exactly there (plus the name and the avatar rows). Whether tag 0x19 u32 is the class id is for RE to confirm; the value 4 for a Sharpshooter pick is what was measured.
- The server never parses it: `characters.class_id` is NULL after creation; the login path hard-codes class 1 (CORE-REQUEST-022).
- migration 009 gives DEFAULTs only for level / hp_current / hp_max / speed_walk; mp, class_id, cash and the five stats stay NULL at birth; `player_wire.py` then sends constants (the ticket's own nonclaim 2).
- Owner's reference point: the 28 Aug ad-hoc ActorAttr probe base ("probe base") looked closer to a real freshly-created character than today's newborn.
- Proposal for chief (owner's request, in her words as gist): (1) parse the class from CreateActorVital into `class_id` at creation, (2) birth HP/MP/stats/cash from the class table in gamedata (CHARCREATE_CLASS s_SCORE / STANDARD_STATUS), not constants, (3) login reads class from the row instead of hard-coding 1.

nonclaims: the ticket's PASS is only "born with the three seeded vitals and not refused at login"; nothing about class or the other columns is claimed by the ticket - the finding above is extra.

---

## GT-220  ->  [PASS]  (sample smaller than the ticket asked: 2 items on the floor, 5 answered clicks on 2 townspeople)

client-observable (owner, scene 2 after `/warp 2`): killed mobs; a round where 2 drops stayed on the floor (Blood Cubic Crystal + Blue Talisman at one spot); she walked to two NPCs and clicked them (Kuck several times, Carle once); came back - both drops still on the floor; picked the Blue Talisman with ONE click; backpack 5/40 and chat `ได้รับ [ Blue Talisman ] * 1`.

wire/DB: at click time the ground frame in force was `MOB_LOOT_DROP (149 bytes)` = several rows; the 5 clicks were answered by `LANE_A_CHOOSE_NPC_SCENE2_ANSWERED placement=68 x4, placement=28 x1  visible=97 hostile=12 hp=ledger from_ledger=7 dead_as_corpse=5` through `GROUND_UNDER_PUBLICATION_REACHED lane_hooks.choose_npc_response.scene_2` (call site `wired_by_name_lookup`); FACE frames 12,602 B x5; then `MOB_PICKUP_REQUEST_DECODED object_ref=0x00100003` -> `MOB_PICKUP_ROW_INSERTED ... template_id=2205401 slot=4` -> `MOB_PICKUP_GROUND_REMOVAL_PUBLISHED key=0x100003 rows_left=1 frames=1` -> `MOB_PICKUP_DELTA_GROUND_KEPT`. `GROUND_UNDER_PUBLICATION_REACHED` = 6 for the round.

Observations repeated from R306 (owner): the first hit on the NEXT mob sometimes makes the previous mob's drop vanish from the floor, and it sometimes comes back when that mob dies; pattern not stable. `MOB_COMBAT_BAR` = 46 this round, all whole-roster frames.

nonclaims: does not prove the 3-item / 3-click numbers the ticket wrote; the claim itself (a click on a townsperson does not clear the floor) held on both layers.

---

## 🔴 Ground-drop lifetime finding (LANE-B) - measured while the owner waited between tickets

- The server declares `MOB_DROP_PRESENCE ... declared_lifetime=120.0s` for every drop and trims rows after 120 s (`live=4` -> `live=2 carried=0` across kills).
- After several minutes the owner clicked two old drops (Blood Cubic Crystal, Exile Sandal) 7 times: every click reached the server (`MOB_PICKUP_REQUEST_DECODED object_ref=0x00100004 / 0x00100005`) and every one was `MOB_PICKUP_REQUEST_REFUSED reason=drop_already_taken` (7 of 7).
- No ground frame is ever published on expiry (ground frames go out only on kill and on pickup), so the client keeps rendering expired drops as un-pickable ghosts until the next kill's pool frame happens to omit them. RE-208 (image) already measured that the client has no clock: removal is only ever the pool-shape frame.
- Owner on the real server: drops vanish on their own after roughly 1-2 minutes (not sure of the number). So 120 s is the right neighbourhood; what is missing is the second half - on expiry publish the pool without the row (REMOVE_OMITTED), or the NULL/empty pool when nothing is left.

---

## GT-214  ->  [PASS]

client-observable (owner, scene 2 re-entered via `/warp 1` then `/warp 2`): before-click photo; clicked Navy soldier (green name) - turned to face her, target panel `Navy soldier HP 1771 LV 20`, yellow arrows; other actors unchanged; hostile-safety half: a pink-named Fighting Fish Sergeant in frame before and after the click - no colour change, no charge, no attack. Label colours: Navy soldier green, Fighting Fish Sergeant pink, GT215BORN0 white.

wire/DB: after the fresh entry (`WORLD_CENSUS_BG0002_INITIAL_97` second time, 17,794 B - see finding below) 6 answered clicks: `LANE_A_CHOOSE_NPC_SCENE2_ANSWERED placement=4, 28, 99, 29, 29, 100  visible=97 hostile=12 hp=ledger from_ledger=5 dead_as_corpse=7`, `FACE_P<n>` x6. No `DECLINED` line for the pre-walk click (either it did not reach the responder or the step came first). 11 scene-2 answers for the round in total.

Procedure note for the ticket author: `/warp 2` typed while already in scene 2 does NOT re-enter the scene - the server answers `GM_CHAT_STAGED_NEXT_LOGIN scene_id=2 ... nothing was sent to the client now`. The owner re-entered via `/warp 1` + `/warp 2`. She has since decided that a same-scene `/warp <n>` must teleport to that scene's spawn (PANYA-DECISION 20260903_1800).

Finding (LANE-B): the re-entry census was 17,794 B against 18,165 B on first entry = 371 B less = 7 x 53 B = the seven mobs she had killed are dropped from the arrival frame (corpses gone on screen too) and nothing respawns them - there is no respawn timer yet. She found live mobs only because some were never hit.

---

## GT-192 + GT-200  ->  [PASS both]

client-observable (owner): walked the closed list `/warp 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 130` then `/warp 1`, photo before any click on every scene; her verdict: NPC counts, HP and LV labels look reasonable on every map, LV differs per actor; no map looked empty or abnormally thin. Her two standing gaps, not this ticket's: monsters are not hostile outside scene 2, and mob sets are not multiplied per group with the real count and `f_scale`. At scene 130 (Navy Training Camp) the chat printed six yellow system lines "เป้าหมายเป็นรูปแบบไม่มีอยู่ หรือ เป้าหมายไม่สามารถไปถึงตำแหน่งนั้นได้!" (target does not exist / unreachable) - recorded, cause not claimed.

wire/DB: every arrival census matched the ticket's predicted count exactly - 3=62 · 4=109 · 5=87 · 6=66 · 7=56 · 8=69 · 9=57 · 10=94 · 11=51 · 14=81 · 130=41 (`WORLD_POP_HANDOFF scene=<n> kind=census actors=<n> wire=<n>` + `WORLD_CENSUS_LANE_SCENE<n>_INITIAL_<n>`), scene 1 at the end `WORLD_CENSUS_INITIAL_108` (20,424 B) after her one step. `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` = 0. `MOB_CENSUS_HOSTILITY roster=0` on every warped scene (as in R306). Free negative control: her typo `/warp 12` -> `GM_CHAT_WARP_REFUSED scene_id=12 reason=scene_has_no_login_entry stageable=(1,2,3,4,5,6,7,8,9,10,11,14,126,130,278,997)`. Clicks along the way were answered (scene 5 placement 1 -> `COLUMBUS_CHOOSE_NPC_WRONG_SCENE scene=5`, scene 11, scene 130 x3); one `SCENE3_DECLINED no_player_position_walk_one_step` (click before the step, procedure).

nonclaims: photos are the owner's; per-actor LV numbers were not transcribed; label colours were recorded only where the owner called something out.

---

## GT-217  ->  [PASS]  (Atlantis / ocean panel reached and rendered for the first time)

client-observable (owner): `/warp 126` in Port Royal -> screen unchanged (correct: staged); closed the client with X; job 1481 relaunched it; logged in as GT215BORN0 -> **"Atlantic Ocean: Rising Sun Sea"**, the character is a ship, compass HUD instead of the minimap, HUD `X 3,050 Y 232`, NPC ships docked at a town, "Lonely Island" (green) and Port Royal visible next to the spawn. She sailed around: Blood Blade Island (`LV 1 HP 106`), a krathong object (`LV 60 HP 43275`), Tornado, Mad Sand Island, Pirate Ship, Pirate Lair, Jellyfish King (`LV 60 HP 43275`); every clicked one "turned to face her" - **islands and static objects included, which is nonsense** (owner). She found Spice Paradise Island and Prison Exile Island, the real entrances to scenes 3 and 2: on the real server sailing near them pops "รายงานกัปตัน เรือเทียบท่า [island]" and confirming enters the island - here nothing pops.
- 🔴 Player ship HUD showed **HP -1/1** and the ship model burns (sinking visual) the whole time.

wire/DB: `WORLD_SCENE scene_id=126 seq=0 model=Bg3001 name=Atlantis spawn=(3050.000,232.000,90.000) ... return_ticket=REQUIRED`, `WORLD_SCENE_RELOCATED ... reason=no_pinned_ground_for_scene used=(3050,232,90)`, `WORLD_CENSUS_BG3001 assembled=37/38 shippable=37 wire=37` (one placement unshipped: `placement=28 set=16 leader_n_id=0`), `WORLD_CENSUS_LANE_SCENE126_INITIAL_37 (6556 bytes)` + REAPPLY, `MOB_CENSUS_HOSTILITY scene_id=126 roster=0`. 8 clicks answered `LANE_A_CHOOSE_NPC_SCENE126_ANSWERED placement=26, 37, 17 x3, 29 x3 visible=37 omitted=0`. Login vitals were the human ones (`LOGIN_VITALS from_row level=1 hp=100/100`) - no vessel vitals are sent, hence -1/1 and the burning hull.
- 🔴 **Docking mechanism found on the wire:** while she sailed near islands the client sent `TriggerVital` (0x1FB2) five times, 69 B each, shape `12 B2 1F 0B 01 0F <u16 trigger> 00 0B 04 2A x 2A y 2A z(186.0)` + a position vital; trigger ids seen: 40, 51, 3, 57, 36. The server has no responder (5 sent, 0 answered). This is almost certainly the "captain report / dock" trigger the real server answers with the dock dialog. Raw frames (client -> server):
  ```
  #114  12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 B2 1F 0B 01 0F 28 00 0B 04 2A 83 EF BD 45 2A 9A 1A 7D 44 2A 00 00 3A 43 12 90 2A 0B 00 2A 7B FC C6 45 2A 29 87 96 44 2A 00 00 AC 42 2A 5C B1 C0 ..
  #203  ... 0F 33 00 0B 04 2A 62 B2 CE 45 2A B1 BE 96 C5 2A 00 00 3A 43 ...
  #217  ... 0F 03 00 0B 04 2A DE EB 86 C4 2A 79 6F BA C5 2A 00 00 3A 43 ...
  #229  ... 0F 39 00 0B 04 2A 31 10 8A C5 2A 8F A9 C3 C5 2A 00 00 3A 43 ...
  #247  ... 0F 24 00 0B 04 2A 7A C7 85 C5 2A 56 D1 91 C3 2A 00 00 3A 43 ...
  ```
  (full hex in the capture; GT-109 VEHICLE-BIND may want this too.)
- After the ocean scene: the player's own name label carries an HP bar under it on every land scene afterwards (scene 17 and Port Royal screenshots) - it was not there before 126. Client-side state left over from the vessel form; recorded, cause not claimed.

nonclaims: nothing about sailing physics, nothing about what the 37 actors' real identities should be, no claim that 0x1FB2 is the dock trigger beyond the correlation above.

---

## GT-187  ->  [NO-RESULT - the coordinate warp is refused on main today]

client-observable (owner): `/warp 278 100 200` typed twice in the ocean scene and twice in Port Royal - nothing happened on screen, no crash. `/warp 1` (no coordinates) left the ocean scene normally.

wire/DB: all four -> `LANE_GM_CHAT_ACTION warp route=action` then `GM_CHAT_NO_BYTES_SENT account='localtest' command=warp why=refused_warp_WarpExecutorError blocked_on='no blocker recorded' character_id=2`; GM log outcome `refused_warp_WarpExecutorError`. No teleport, no census resync to judge.

Two findings for LANE-GM: (1) the console line swallows the `WarpExecutorError` message, so nobody can tell which of the executor's raises fired (`scene_id not in scene_catalog`, `no marker`, arg shape ...) - print the message; (2) the cross-scene form with coordinates does not work on today's main even though GT-187's header says PR #438 merged the resync - the ticket needs a working entry path before it can be measured. (R306 finding 3 still stands: the same-scene coordinate form crashed the client.)

---

## GT-213  ->  [PASS on (A) and (B); (C) NO-RESULT as the ticket itself allows]

client-observable (owner):
- (A) `/warp 14` -> one step -> clicked the scene-14 `Columbus` (lv 110) twice: silent, no quest, no dialogue, stayed in scene 14.
- (B) `/warp 1` -> one step -> clicked the harbour Columbus (Marine Transport Station, `HP 100 LV 10` panel): the Story window opened with two options (`มุ่งหน้าไป Atlantic Ocean: Rising Sun Sea` / `ตั้งฐานทัพที่ Port Royal`); she pressed option 1 once -> scene changed to **"Ship in the Sea"** (ship deck interior, HUD X -102 Y 303) immediately.
- (C) `/warp 1` -> one step -> back in Port Royal at the harbour (X -8,323 Y -2,564), same NPCs (Loie, Columbus, Lisa, Drunkard Captain, Coulson...) as S00 at the dense area (X -6,320 Y -986); nothing taken away. Closed with X.

wire/DB: scene 14: `LANE_A_CHOOSE_NPC_SCENE14_ANSWERED placement=1 visible=81 omitted=0 hp=ceiling` x2 (with `LEDGER_NOT_ADMITTED reason=not_this_scenes_ledger`), `COLUMBUS_CHOOSE_NPC_WRONG_SCENE scene=14 effect=columbus_lane_declined` once; scene 1: `V98_NPC_CONVERSATION_DEFAULT_P1 (44 B)` -> `CORE_REQUEST_014_COLUMBUS_Q3021_NPC_CONVERSATION_ONCE (54 B)` -> `WORLD_SCENE scene_id=17 model=Bg1001 name=a_ship_at_sea ... return_ticket=REQUIRED`, `COLUMBUS_QUEST3021_NO_VEHICLE_DISPATCH`, `WORLD_M2_CROSSING_HANDOFF scene=17 kind=clear held=108`, `M2_SEA_DESTINATION offer=3021 target_scene=17 advertises_ocean=126`, `CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE (73 B)`; then `/warp 1` -> `LANE_GM_CHAT_WARP_CROSS_SCENE_NO_COORDS_TELEPORT_VITAL` + `WORLD_CENSUS_INITIAL_108`. `columbus_q3021_crossing_row_checkpointed` printed 0 times -> half (C) is NO-RESULT per the ticket's own rule; `COLUMBUS_Q3021_TELEPORT_REFUSED` printed 0 times (nothing was refused, nothing had to be).

🔴 Position persistence after the sea scenes (LANE-A / LANE-DB): the run DB after teardown holds character 2 at scene 1 (-6258.7, -879.2, 671) = the spot where she typed `/warp 126` at ~18:2x. Everything after that - Atlantis, scene 17, the `/warp 1` return, the walk to (-6320, -986), the X exit - was NOT persisted. Scenes 126 and 17 print `save=0`; after coming back to scene 1 the exit checkpoint did not write either. (R306 found the opposite for a plain land session: an X exit persisted Evil Port exactly.)

nonclaims: no claim about the scene-17 interior content (it is empty by decree, `held=108 composed=YES` is the clear frame); no claim about the quest text.

---

## Cross-lane findings from this round (in addition to R306's seven)

1. CreateActorVital carries the class pick (tag `19 <u32>`: 1 for Arena01/Gladiator, 4 for the newborn who picked Sharpshooter) and the server discards it; birth columns beyond level/hp/speed are NULL; login hard-codes class 1 (GT-215 block).
2. Drop lifetime 120 s expires the ledger with no removal frame -> ghost drops, `drop_already_taken` x7 (GT-220 block). Owner: real server ~1-2 min then gone.
3. `/warp <same scene>` = staged-next-login, useless mid-round; owner decision 20260903_1800 asks for a teleport to the spawn instead.
4. No mob respawn; killed mobs are omitted from the re-entry census (-53 B each).
5. Ocean panel 126 renders; the player ship has no vitals (HP -1/1, burning); islands/objects turn to face on click; client sends `TriggerVital` 0x1FB2 near islands with 5 distinct trigger ids and nothing answers - the dock path the owner described from the real server.
6. Cross-scene `/warp <n> <x> <y>` is refused by `WarpExecutorError` everywhere and the console hides the message.
7. Position persistence stops after visiting scenes 126/17 and does not resume on the way back to scene 1.
8. A self HP bar under the player's name label appears after the ocean scene and stays on land.
9. Client name field caps character names at 10 characters (`GT215BORN01` -> `GT215BORN0`); tickets that prescribe an 11-character name cannot be followed literally.
10. The ticket's GT-215 BEFORE SELECT cannot run on a pre-migration copy (`no such column: level`); it needs the migrated DB or a column-existence guard.

## Lessons / tool notes
- Job 1480 first attempt aborted at LOCK acquisition: `Write-Flag` rejects an empty string inside `-Lines` (Mandatory [string[]]), and my hand-written R306 release note had two empty lines. Fixed by mapping '' -> ' ' when re-reading the flag, and the flag file was sanitised. Any job that re-writes LOCK_GAME with `Read-Flag` output needs that mapping.
- RECHECK suites ran inside the extracted boot tree with `-p no:cacheprovider` (no repo pollution): 49 + 34 + 108 passed in ~15 s total.
- The relaunch-client-only job (1478/1481 pattern) is the practical "logout" while UI-A/UI-B are refused.

OBSERVER_CONFIRMED: 2026-09-03T18:58+07:00 (owner reported every ticket in chat as it was measured; screenshots are hers; she confirmed the class/birth-value finding and the drop-lifetime memory herself)
