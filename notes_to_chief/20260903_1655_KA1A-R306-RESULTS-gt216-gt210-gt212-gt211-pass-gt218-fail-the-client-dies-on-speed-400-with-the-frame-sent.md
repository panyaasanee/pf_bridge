# R306 attended round - results (five tickets, one boot)

- who: ka1-A (attended in-game tester), owner Panya at the keyboard the whole round
- when: 2026-09-03 14:17 -> 16:51 (+07:00), approximate, from bridge job stamps and the GM command log
- head (worktree at boot): c1660fd77494e3eefbbcacb68cee798c47728f05
- boot commit: 39a3a05faf6e8ece6533e5b9aaad21d712e22dbd (head of origin/main, GREEN, PR #649)
- boot tree: pf_bridge\boot_trees\r306_1476_20260903_141652
- run db: state\run_r306_20260903_141652.sqlite3 (throwaway copy)
- capture: GameClient\capture_r306_20260903_141652 (server_console_live.out.txt 13,619,595 B sha256 2DAB56DE... / .err.txt 12,011 B sha256 234EF25F...)
- canonical sha: 4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454 - UNCHANGED before and after (job 1479)
- PF_SPEED_TRIAL=400 set in the boot process (job 1476 line 26), no scenario flags
- jobs: 1472/1473 (boot aborted on CODE_DELTA while main moved), 1474 (wait-for-green, RECHECK 216 fail - see lessons), 1475 (why), 1476 (boot PASS), 1477 (client relaunch after warp crash), 1478 (client relaunch after GT-218 death), 1479 (teardown PASS)
- teardown: listeners 0, GameClient 0, stopped markers 1, traceback markers 0, integrity ok, foreign_key_check 0 rows
- run DB after: characters id=1 -> level 1, hp 100/100, speed_walk 400.0 · position scene 5 (13605.8, 23405.6, -760.0) · backpack 12 rows (baseline 3 + 9 picked)
- owner chose option (kho) = all five in one boot and said "ทราบ" before the boot; order 216 -> 210 -> 212 -> 218 -> 211

The GM command log (capture\gm_command_log.ndjson, UTC): warp 2 07:20:19 · warp 14 08:02:16 · warp 14 11665 -1500 08:06:55 (client crash) · warp 3 08:29:39 · warp 4 09:09:13 · warp 5 09:18:12 · speed 400 09:32:44.

🔴 Boot-time lane tokens (`LANE_HOOK_REGISTERED`, `LANE_HOOK_DISCOVERY ... SKIPPED_NOT_PRODUCTION_ALLOWED`, `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED`) are NOT in either summary log: they print to stderr at import time, before `server_console_live.err.txt` opens (the .err file starts at the first `LOGIN_SPEED`). Every ticket criterion that reads a boot line was therefore measured on the booted tree instead (static read of `pf_bridge\boot_trees\r306_1476_...\src`), and on the live `LANE_HOOK_FIRED` lines. Tooling gap for chief: the visible-console boot path loses the registration lines.

---

## GT-216  ->  [PASS]  (owner-measured, ka1-A proposes PASS; LANE-B/chief consumes)

client-observable (owner, scene 2 after `/warp 2`, first login had 4 kills on scene 2 before the round's warps):
- 10 pickup clicks on 10 ground items across the round, 9 landed in the backpack; 8 of 9 on the FIRST click. The one exception: the last item, clicked while walking toward it -> chat said "ระยะไกลเกินไป" (too far) repeatedly; it only entered the bag once the character stood completely still, then one click. Clicking while still walking never picks up.
- Backpack 3 -> 12 items. Blood Cubic Crystal and Energy Cubic Crystal entered the bag with NO icon and do nothing when clicked (owner: the real server applied them instantly on pickup). Recorded, not judged.
- Floor behaviour the owner could not pattern: after killing mob 1 (drop on the floor, not yet picked), the FIRST hit on mob 2 made mob 1's drop vanish from the floor; when mob 2 died the drop re-appeared at mob 1's spot and was picked with one click. Repeated on later mobs: sometimes vanished on the next first hit, sometimes not.

wire/DB (job 1479 tallies + manual grep):
- `MOB_PICKUP_REQUEST_DECODED` = 10 · `MOB_PICKUP_ROW_INSERTED` = 9 · `REFUSED reason=drop_already_taken` = 1 · `REFUSED reason=vital_count_not_one` = 0 · `REFUSED reason=claimant_out_of_range` = 0
- `VITAL_WALK_PROMOTED` = 7 lines, ALL on stderr (`vital=0x2A90 vital_count=4`, `0x4543 vc=8` first login; `0x2A90 vc=2`, `0x4543 vc=9`, `vc=3`, `vc=3`, `vc=2` during pickup). Five multi-vital pickup packets were walked and passed. `VITAL_WALK_REFUSED` = 7 (unknown_vital_id / not_a_vital_collection / not_a_runtime_protocol_req - the non-pickup packets, expected).
- `MOB_DEATH_DEAD` = 18 · `MOB_LOOT_DROP` = 31 · `MOB_COMBAT_BAR` = 120 for the whole round.
- Booted tree: `current/vital_walk.py` present, `isolate_vital` and `walk_nested_vitals` present, runtime import OK (job 1476 corrected RECHECK).
- Backpack row after: `[(0,2600001,2),(1,2400901,1),(2,2400046,1),(3,2200002,1),(4,2205001,1),(5,2400046,1),(6,2400046,1),(7,2204001,1),(8,2204001,1),(9,2400047,1),(10,2400046,1),(11,2205001,1)]`

nonclaims: does not prove the floor vanish/re-appear cause (observation only, see cross-lane note 1) · does not prove crystal use · does not prove anything about the real server's pickup animation · `claimant_out_of_range` = 0 means the walking-click case was refused by the CLIENT ("too far") before any packet, not by the server.

---

## GT-210  ->  [PASS]

client-observable (owner, scene 3 Spice Paradise, three full-res screenshots held by the owner: Columbus / Sand dragon / Reyna targeted):
- (จ) clicked NPC turns to face the character: YES for Columbus (owner stood next to him, compared before/after), Reyna and Sand dragon also turned when clicked.
- (ฉ) target panel opens: `Columbus HP 7980 LV 35` · `Sand dragon HP 5636 LV 31` · `Reyna HP 7980 LV 35` (copied from the panel).
- (ช) other actors unchanged: LV 31/35 labels all present, nobody changed appearance or name.
- Name-label colours (per frame, colour only, no cause): Columbus green · Reyna green · Sand dragon green · title lines "Marine Transport Station" / "Spice Merchant" blue · Arena01 white · targeted actor gets yellow arrows.
- NO dialogue/quest window at any click (this is what criterion (ง) requires at scene 3).
- Observation, not a criterion: at EVERY answered click, every M-model body in camera range (Columbus, all Sand dragons) does one short jerk "as if hit"; Reyna (P_FEMALE model) never does. The owner tested this many times.

wire/DB:
- 29 ChooseNPC clicks in scene 3: 1 `LANE_A_CHOOSE_NPC_SCENE3_DECLINED reason=no_player_position_walk_one_step` (the very first click, before the one step - the ticket's own predicted procedure fault) + 28 `LANE_A_CHOOSE_NPC_SCENE3_ANSWERED placement=<n> visible=62 omitted=0` (placements 0 = Columbus n_ID 36, 2 = Reyna n_ID 38, 48 = Sand dragon n_ID 55). `LANE_HOOK_FIRED ...roster_scenes scene_choose_npc_responder` before every one of the 29.
- Every answer is `LANE_A_CHOOSE_NPC_SCENE3_FACE_P<n>` 8,124 B, opcode `12 9D 6E 14`, `0x3E` = 62 entries: the clicked actor carries NPC_ATTR + MOVEMENT_ATTR (mask 3, heading to player); the other 61 carry NPC_ATTR only (arrival census was 11,684 B with MOVEMENT_ATTR on all 62).
- Client identity per click matched the label on screen (0x2001 Columbus, 0x2003 Reyna, 0x2031 dragon) and the player position in the 58-byte ChooseNPC variants matched the NPC the owner was standing next to.
- (ง) `CORE_REQUEST_014_COLUMBUS_Q3021` = 0 and `columbus_npc_conversation_sent_once` = 0 for the whole round.
- (ก)/(ง2) boot lines: not capturable (see red note at top). Booted tree: `lane_a_choose_npc_roster_scenes.py` line 329 `production_allowed = True`; `lane_a_choose_npc_scene1.py` line 227 `production_allowed = False`; `scenes_this_lane_answers_for()` = (3,4,5,6,7,8,9,10,11,126,130), `skipped_scenes()` = ().

nonclaims: per ticket 1-7 · the "jerk" observation is client-side rendering, cause NOT claimed (cross-lane note 1) · no label-colour meaning claimed (RE-067).

---

## GT-212  ->  [PASS]  (two islands: scene 4 and scene 5, as the ticket's steps 4-9 require)

client-observable (owner):
- scene 4 Slave Market Island after `/warp 4` + one step: islanders visible before any click. Clicked Salahuddin (P81) x3, Mori Hiroko (P3) x1, Mirage reel (P77) x2, Columbus (P1) x3 and more during the stare. Every clicked actor turned to face the character and the target panel opened (`Columbus HP 23976 LV 50` copied from the panel). After the Columbus click the owner stared 30 s: NO dialogue/quest window, still on Slave Market Island (same background, same islanders, camera not moved). LV labels all intact. Colours: Salahuddin green, Columbus green, "Liberate" / "Marine Transport Station" blue, Arena01 white. Owner: Salahuddin and Columbus jerk on every click; Mirage reel and the cat-shaped actor turn but never jerk.
- scene 5 Evil Port after `/warp 5` + one step: clicked Evil Port Bulletin Board 1 (P78), Old Tom (P2), Port Side Pirates (P3), Columbus (P1). All turned when clicked, none turned when not clicked; the jerk set is fixed per actor ("the ones that jerk always jerk, the ones that do not never do"). 30 s stare after Columbus: NO window, still Evil Port, LV labels intact. Panel `Columbus HP 71640 LV 70`. Colours: Columbus green, "Marine Transport Station" blue, Arena01 white.

wire/DB:
- scene 4: `LANE_A_CHOOSE_NPC_SCENE4_ANSWERED placement=<n> visible=109 omitted=0` x19 (placements 81, 1, 77, 3), `FACE_P<n>` labels x19, `COLUMBUS_CHOOSE_NPC_WRONG_SCENE scene=4 effect=columbus_lane_declined` printed ONCE at the first placement=1 click.
- scene 5: `..._SCENE5_ANSWERED ... visible=87 omitted=0` x5 (placements 78, 2, 3, 1), `COLUMBUS_CHOOSE_NPC_WRONG_SCENE scene=5 effect=columbus_lane_declined` once.
- (ค) placement=1 answered on both islands · (ง) zero Columbus q3021 tokens all round · (จ) integrity ok, canonical unchanged, traceback 0 · `LANE_A_CHOOSE_NPC_ROSTER_SKIPPED` = 0 in the logs (and unmeasurable at boot, see top).
- MOB_CENSUS_HOSTILITY scene_id=4 and 5: `roster=0` (same as scene 3 and 14 - combat ledger empty on every warped scene).

nonclaims: per ticket 1-5 · only scene 4 and 5 were visited, the other seven islands are NOT judged · the WRONG_SCENE token printing once per scene rather than once per click is recorded, not interpreted.

---

## GT-218  ->  [FAIL]  (the ticket's own "negative result is worth as much as a positive one" branch)

client-observable (owner, scene 5 Evil Port, X 13,515 Y 23,234, HP 100/100 and 1 gold on screen before):
- Typed `/speed 400` exactly, Enter. Within the 5-second no-touch window the character DIED: HP `0/1` (max HP became 1), gold `0`, the red death dialog "ท่านตายแล้ว กรุณาเลือกวิธีการคืนชีพ" with two buttons (return to spawn / revive here). Chat line, copied by the owner: `หักเงิน 1 ทอง 00 เงิน 00 ทองแดง`. Owner's reading, which I adopt: the cash attribute went 10000 -> 0 as a side effect of the frame and the client reported the difference; it is NOT a death penalty. Screenshot held by the owner.
- The owner pressed nothing in the death dialog (no ticket covers the revive path), closed the client with the X, job 1478 relaunched the client, she re-logged in: HP 100/100 and 1 gold back on screen, standing at Evil Port at the same coordinates.
- Camera / walk check after the frame: not performed (STOP condition hit first).
- Name-label colours on the death screenshot: Columbus green, "Marine Transport Station" blue.

wire/DB:
- stderr: `LANE_GM_CHAT_ACTION speed route=action` then `SPEED TRIAL OPEN account='localtest' command=speed env=PF_SPEED_TRIAL trial_opens_for=400.0 sending=400.0 character_id=1 identity=268500993:0`
- stdout: `[G>] LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL (74 bytes; late=0.2 ms)` exactly once · `SPEED DEFERRED` = 0 · `GM_CHAT_NO_BYTES_SENT` = 0 · the frame carries `00 00 C8 43` (400.0), not `00 00 96 43`.
- The 74 bytes, raw:
  ```
  12 9D 6E 14 00 00 00 00 08 04 0B 02 12 01 00 12
  9A 30 0B 00 12 01 00 12 AD 12 14 1E 00 00 00 0B
  01 32 01 00 01 10 00 00 00 00 12 40 00 2A 00 00
  C8 43 32 00 00 00 00 00 00 00 00 05 01 0B 00
  ```
- (ค) a non-heartbeat inbound frame followed: `[G< #2437] 31 bytes TargetVital` (GT-193 measured 0 of 426) - the client was still talking after the frame.
- (ง) run DB after: `characters` id=1 -> `speed_walk 400.0`, hp 100/100, level 1 (the row was never harmed; the value equals the login constant).
- Re-login: `LOGIN_SPEED wire_deferred value=400.0 ... withheld_row=400.0` and `LOGIN_VITALS from_row level=1 hp=100/100 apply=carried` - the login door held the row back exactly as COO-DECISION 0645 intends; that is why the recovery step was safe.
- (จ) integrity ok, canonical unchanged, traceback 0.

What this result says (ticket wording): the value is cleared as a suspect - 400 is the number login already sends and the character survives login every time. The suspect is now the FRAME SHAPE of `UpdateAttrVital 0x309A` as composed above. Evidence the frame touches more than speed: max HP became 1 and cash became 0 on the same frame. Suggest LANE-GM / an RE ticket compare this 74-byte shape against a real-server UpdateAttrVital capture (attr id `0x40`, the `12 AD 12 14 1E 00 00 00` header field, the trailing `05 01`).

nonclaims: does not prove which byte kills · does not prove `/speed` changes on-screen speed · does not judge GT-193's cause · the revive dialog path was not exercised.

---

## GT-211  ->  [PASS]

client-observable (owner, fresh login after GT-218, scene 5, no movement keys, no typing): HOME menu opened -> clicked "ออกจากเกม" once -> the menu window closed and the chat line `[ทั่วไป] : EXIT REFUSED` appeared IMMEDIATELY (same second as the click); no dialog, the client did not close, nothing else happened during the 30-s stare. Screenshot held by the owner (chat shows `Pirate Force local server online` then `EXIT REFUSED`). The owner then exited with the X.

wire/DB: `[G< #113] 34 bytes ... (15, 6976, '0x1B40')` (ONE vital, not the owner's 119-byte four-vital shape from the ticket background) -> `LANE_A_UIA_NOTICE_COMPOSED button=EXIT_GAME subcode=1 vitals=1 trailing=0 text=EXIT REFUSED pc=56 frame=66` -> `[G>] LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE (66 bytes)`. Note for LANE-A: the outgoing label still says BACK_REFUSED while the text is EXIT REFUSED - label naming only, bytes are the ticket's.

nonclaims: does not judge GT-205 · the 12-character wording is LANE-A's assumption per the ticket, recorded as seen.

---

## Cross-lane findings from this round (not tied to one ticket)

1. 🔴 For LANE-B and every combat ticket that ever recorded "the mob showed a hit animation": `MOB_COMBAT_BAR` (18,165 B), `MOB_DEATH_DYING` and `MOB_DEATH_DEAD` (18,112 B) all use opcode `12 9D 6E 14 ... 0x61` = the SAME whole-scene 97-actor roster frame as `WORLD_CENSUS_BG0002_INITIAL_97` (18,165 B). There is no separate "hurt" frame; the only other combat frame is `MOB_COMBAT_ANNOUNCE` (98 B, vital 0x16F7, carries the damage number). The owner's observation - the "hit jerk" on pink-named mobs looks identical to the jerk NPCs do when a ChooseNPC roster answer arrives - matches the wire: both are full-roster re-sends. Open question for RE: does the client have a real hurt animation at all, and what frame of the real server triggers it. Also consistent with RE-208: a roster re-send whose ground section is empty would REMOVE_ALL the floor and the death frame's ground section would ADD it back, which is the vanish/re-appear the owner saw in GT-216 - hypothesis, not proven.
2. Scene 14 (`/warp 14`): `MOB_CENSUS_HOSTILITY scene_id=14 scene=? roster=0` - the census ships 40+ mobs (Hell Volcanic Glaucoma etc.) but none is attackable: click walks the character to the mob, no damage, no HP bar. Same `roster=0` on scenes 3, 4, 5. LANE-B: the combat ledger is empty on every warped scene; only scene 2 (login scene) had a roster.
3. `/warp 14 11665 -1500` typed while already in scene 14 sent `LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS (45 bytes)` and the client closed itself with `GSCN_RunTimeProtocolRes ErrorData=28317`; server saw `ConnectionResetError` once, no traceback, survived. Cross-scene `/warp <n>` without coordinates worked five times.
4. Position persistence: after the crash-close the owner re-logged in at the scene-2 spot from BEFORE the earlier `/warp 14` (crash path does not checkpoint the warped scene); after the normal X exit in GT-218/211 she re-logged in at Evil Port scene 5 at the same coordinates (normal exit does persist). Run DB position row after the round: scene 5.
5. Boot-time lane tokens are not in the summary logs (see top). Ticket criteria (ก)/(ง2) of GT-210 and (ก) of GT-212 need either the visible console captured or the bridge to open the summary logs before import.
6. GT-216's RECHECK line in the ticket (grep lowercase `vital_walk` inside `vital_walk.py` itself, expecting 2 hits) is unsatisfiable - the module never contains its own name - and cost one boot attempt (job 1474 ABORT 40). Job 1476 used: file bytes > 0, `isolate_vital` present, `walk_nested_vitals` present, runtime import OK.
7. Two client bodies that never jerk on the roster re-send in scene 4 (Mirage reel, the cat) and one in scene 3 (Reyna) - and the jerk set is stable per actor. Raw observation for whoever owns client rendering; my first guess (P_ vs M_ model) was refuted by Mirage reel (M-model, no jerk).

## Lessons / tool notes

- `server_console_live.err.txt` carries the lane tokens (`VITAL_WALK_*`, `LANE_A_CHOOSE_NPC_*`, `SPEED TRIAL OPEN`, `LOGIN_*`); grepping only `.out.txt` gave me a false "VITAL_WALK_PROMOTED = 0" mid-round. Both files must be tallied.
- Bridge outbox files are UTF-8 BOM header + UTF-16 body; decode per line.
- main moved fast during this round (CODE_DELTA aborts x2, ten commits); "wait for the head of main to be green" (owner's choice) took 6 attempts.
- LOCK_GAME was held 13:45 -> 16:5x; a SYNC-NOTICE at 16:52 says released after 3h - that notice is about this hold, expected.

OBSERVER_CONFIRMED: 2026-09-03T16:51+07:00 (owner reported each ticket in chat as it was measured; screenshots are hers)
