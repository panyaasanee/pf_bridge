to chief -- RE-162 result IN-SESSION-SCENE-CHANGE-WIRE-001 (STATIC-ON-BRIDGE)

# RE-162 -- DONE / MIXED: WIRE MECHANISM FOR AN IN-SESSION CROSS-SCENE TELEPORT ALREADY EXISTS AND IS WIRED (client-image static evidence, RE-077/RE-090/RE-129, plus one already-merged server call site: Columbus quest-3021 scene-17 crossing). CLIENT-OBSERVABLE OUTCOME IS UNPROVEN -- the one attended ticket built to answer that (GT-106) is still PENDING. The GM `/warp <scene>` command specifically does NOT use this mechanism today; it is a separate, narrower, deliberately-shut path (same-scene ForcePos, COO-locked) plus a next-login-only config stage.

TICKET START: 2026-08-30T19:09:25+07:00
mode: static/read-only only. No client image in this clone (GameClient.local.bin absent -- confirmed by filesystem search, see "hard limit" note below). No canonical DB, no backups/, no capture corpus opened. No game booted, no source edited outside this one file.

NOTE ON LANGUAGE: house style in prior RE-156/RE-157 letters is Thai. This letter is written in ASCII-only English per this agent's own operating rule ("ASCII only in anything destined for a file -- the bridge console is cp874 and a character outside it kills the tool mid-report"). Structure, section order and citation rigor match RE-156/RE-157 exactly; only the language differs, and that is a deliberate safety choice, not a style deviation.

## Short answer

The five questions do NOT resolve to a clean bounded-negative ("login is the only way"). They resolve to a three-part split:

1. A real client-side, in-session scene-transition state machine exists and is pinned at the byte level in this clone's own committed archive (`RE-077`, PASS/DONE, 2026-08-26, all spans SHA-256-pinned against `GameClient.local.bin`). `TeleportVital`'s registered handler at VA `0x005F14B0` is a DEDICATED transition path, not a StartGame-only side effect: gate on client FSM state (`StateRunTime`/`StateNavigation` only, read from live state `[0x1093198]+0x34C`), reject `scene_id==0`, else build a `cStateSwitchScene` object and drive a normal `SCENE_NAME` table lookup/load, exactly the same machinery whichever caller (login or otherwise) supplies the target.
2. A server-side call site already exists that fires this mid-session, not at login: `runtime.py`'s `_dispatch_columbus_quest3021` (Columbus NPC conversation -> `QuestOperateVital` op1 -> `TeleportVital` to scene 17), wired at `runtime.py:8045`, composing the frame at `runtime.py:5035` via the SAME legacy encoder every login uses (`legacy.make_login_teleport`). This is a real, already-merged, in-session cross-scene teleport of an already-live character.
3. Whether the real client actually renders the new scene when this frame arrives OUTSIDE the guaranteed-post-`StartGameRes` moment has never been observed. The attended ticket built specifically to answer that, `GT-106`, is still `[PENDING]` in the committed `GAME_TEST_QUEUE.md` I can read (line 4840), and the risk that motivated it -- the client FSM-state gate from RE-077 T3 might silently swallow the frame if the client is not in `StateRunTime`/`StateNavigation` at the moment it arrives -- is recorded as unresolved in that same ticket and in `CHIEF-STATUS 20260827_1600`.

So: the reason a player cannot change maps mid-session via GM `/warp` today is NOT "the wire frame is impossible" and NOT "the client cannot do it". It is that (a) the GM `/warp` lane specifically chose not to compose `TeleportVital` (policy refusal in `gm/warp_executor.py`, unrelated to whether the bytes are buildable -- see Job 2/3), and (b) even the one code path that DOES send a real in-session `TeleportVital` (Columbus/quest 3021) has never been checked against a real client screen.

## Job 1 -- TeleportVital / ForcePos full layout, the field RE-090 left unproven, and the VA it is read at: DONE

Evidence layer: static image (client-image byte-level CFG, committed to this clone's `external/` and to the server repo's `gm/teleport_wire.py` docstring, which itself cites the same committed span/SHA-256 values).

### ForcePos (same-scene only)

`gm/teleport_wire.py:229-232` (`pirate-force-server`, sha256 of file `52019f9b0a193203de1cc9d4afda0b8aab7921401cffb5991e3373d947da9354`): vec3-only body, "carries no presence bit, scene id, sequence, string or control field". Serializer span `[0x005E4250,0x005E427C)`. RE-129 (`pf_bridge/notes_to_chief/20260828_2009_RE-129-RESULT-VERSION-ZERO-HANDLER-NOOP.md`) additionally pins: version byte written as literal 0 at `0x005E5186` inside constructor `[0x005E5170,0x005E51A2)`, generic reader does exact-equality compare at `0x005F3EFC`/`0x005F3F01`; and the REGISTERED HANDLER for ForcePos is the complete body `[0x00710440,0x00710445)` = `mov al,1; ret 4` -- it reads no payload and writes no position. ForcePos therefore has no scene id field by construction and its registered client handler is proven to be a no-op even when the frame is well-formed. This is why `gm/warp_executor.py` can only ever do same-scene moves with it, and why the whole ForcePos direction is separately COO-locked (see Job 3).

### TeleportVital -- full field list, offsets, tags, VAs

Source of truth re-derived directly from `external/PF_SERIALIZER_FIELDS.tsv` rows 567-587 (W) and 588-620 (R) for message `TeleportVital` (file sha256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`, unchanged since RE-129 cited the same hash), cross-checked against `gm/teleport_wire.py`'s dataclasses (lines 342-407) and against RE-077's own span table.

Top-level body (serializer span `[0x005EB470,0x005EB609)`, sha256 `fbe813dbd1f9b94d87ee3c101867e8b12aaa36d69c08e68068c8ff06df990487`), stream order:

1. `field_0x18` (u8, tag `0x0B`) -- meaning NOT proven (positional only)
2. `target_presence` (u8, tag `0x0B`)
3. IF present: `target` sub-object, built via SUBCALL to `0x005DF250` (`PF_SERIALIZER_FIELDS.tsv:569`), span `[0x005DF250,0x005DF2F9)`, sha256 `ec9a5421ad5304372e440ecbb35184d6e93624444a262b3058569a724df0b5ef`
4. `aux_presence` (u8, tag `0x0B`)
5. IF present: `aux` sub-object, built via SUBCALL to `0x005DEF10`, span `[0x005DEF10,0x005DEFE9)`, sha256 `105bad91394ee1dc636ef80cfe3444c293a4114d5f371fafe3ebc76ccc049c93`
6. `field_0x20` (u8, tag `0x0B`) -- meaning NOT proven
7. `field_0x22` (u16, tag `0x0F`) -- meaning NOT proven

`target` sub-object (object-local offsets, NOT ascending -- `PF_SERIALIZER_FIELDS.tsv:570-573` / `597-600`, `gm/teleport_wire.py:349-364` documents the same out-of-offset-order write explicitly):

- `scene_id` -- u16, tag `0x12`, object offset `+0x12`. THIS IS THE SCENE ID FIELD the ticket asks for. Named/crosswalked (not positional-only) via RE-077 (`BasicAttr`/`ActorAttr +0x5C` -> bridge copy at `0x004B4C67` -> target `+0x12`, a byte-exact copy-site crosswalk, not an id-equality guess). READ instruction VA (client, R direction): `0x005DF2B5` (`target_stream_anchor_R`/`nonzero_anchor`, `PF_SERIALIZER_FIELDS.tsv:597` column 7/11, function `0x005DF250`). WRITE instruction VA: `0x005DF269` (`PF_SERIALIZER_FIELDS.tsv:570`).
- `scene_seq` -- u64, tag `0x32`, object offset `+0x18`. This is the "sequence" field the ticket asks for. Also RE-077/RE-090-named (crosswalked the same way as `player_wire.py`/`npc_wire.py`'s `scene_seq`), not positional-only.
- `field_0x10` -- u8, tag `0x0B`, object offset `+0x10`. Meaning NOT proven (`gm/teleport_wire.py:347`).
- `field_0x11` -- u8, tag `0x0B`, object offset `+0x11`. Meaning NOT proven.
- `x, y, z` -- three f32, tag `0x2A` each, via nested SUBCALL to the shared vec3 writer/reader (`0x005F3490` write / `0x005F34D0` read, `PF_SERIALIZER_FIELDS.tsv:574-577`/`601-604`). THIS IS THE XYZ FIELD. There is NO fourth float and NO separate heading field anywhere in `TeleportTarget` -- three components only. The ticket's premise that a "heading" field exists in `TeleportVital` is not supported by any committed artifact; treat that sub-question as answered NEGATIVE (see Nonclaims).

`aux` sub-object (also out-of-offset-order on the wire, confirmed real not a transcription artifact -- `PF_SERIALIZER_FIELDS.tsv:582-585`/`615-618`, `gm/teleport_wire.py:376-391`):

- `text` -- untagged UTF-16LE wstring, length-prefixed u32, object offset `+0x10`
- `field_0x2c` -- u16, tag `0x0F`, object offset `+0x14` (STACK-relative in the tsv row, not a top-level object offset)
- `field_0x30` -- u32, tag `0x14`, object offset `+0x30`
- `field_0x34` -- u32, tag `0x19`, object offset `+0x34`
- `field_0x40` -- u64, tag `0x32`, object offset `+0x40` -- written BEFORE `field_0x38` on the wire even though its object offset is higher
- `field_0x38` -- u32, tag `0x19`, object offset `+0x38`

Every `aux` field except `text` is positional-only, meaning NOT proven.

### The version byte (a separate axis from layout)

`TeleportVital` constructor `[0x005E53D0,0x005E5459)`: `mov byte ptr [esi+0x10],4` at `0x005E5425` -- version = 4, proven directly (RE-129, `pf_bridge/notes_to_chief/20260828_2009_RE-129-RESULT-VERSION-ZERO-HANDLER-NOOP.md`, T3). This is DIFFERENT from ForcePos's version=0 and is per-vital, not a project default (RE-105's own lesson, cited in `gm/teleport_wire.py:85-110`).

### What RE-090 left unproven, named explicitly

`field_0x10`, `field_0x11` (target sub-object), `field_0x18`, `field_0x20`, `field_0x22` (top-level body), and every `aux` field except `text`. `scene_id` and `scene_seq` are NOT in this unproven list -- they are named via the RE-077 copy-site crosswalk, which is a stronger evidence class than "positional name" (still `PF_FIELD_VALIDATION.tsv` status `A2_STATIC_OPEN`, 132 candidate frames per direction, candidate-matched not parse-confirmed against a live capture -- `external/PF_FIELD_VALIDATION.tsv:72-73`).

### Registry cross-check (gate 7: do not trust CLOSED alone)

`external/PF_PROTOCOL_PRIORITY.tsv:37`: `TeleportVital` `serializer_status=OPEN`, blockers `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved`. This is the EXTERNAL Codex-deliverable registry's own status column, and it disagrees in wording with the project's own `RE-090` result letter, which narrates those same three sub-calls as resolved ("object-pool allocation + refcount, not wire fields"). Both can be true at once (RE-090 explains WHY those specific calls are not stream fields; `PF_PROTOCOL_PRIORITY.tsv` has not been re-scored to reflect that explanation) but I am not merging them into one verdict -- flagging the mismatch rather than picking a side, per re-derive-don't-quote. Separately, and this is the part that matters for gate 4: `TeleportVital` unambiguously HAS real, non-EMPTY tagged fields (`0x0B`, `0x12`, `0x32`, `0x2A`, `0x0F`, `0x14`, `0x19` all appear with real offsets across 21 W-rows and 27 R-rows) -- this is not a `B0 01 C2 04 00` stub case. `ForcePos`/`CWarpResult` are `serializer_status=CLOSED` (`PF_PROTOCOL_PRIORITY.tsv:34-35`) and also have real fields (vec3; qword+vec3+u16) -- CLOSED-with-content in both cases, no landmine found here.

## Job 2 -- client-side unload/load function and its call paths: PARTIALLY DONE, from static image evidence already committed in this clone (not re-derived by me from raw disassembly -- I have no client image in this environment)

Evidence layer: static image (client-image CFG), inherited from an earlier ticket (`RE-077 SCENE-TRANSITION-SEQUENCE-001`, PASS/DONE, archived `2026-08-27`, full text at `pf_bridge/archive/notes_to_chief_2026-08-19_to_26/20260826_0120_RE-077-RESULT-SCENE-TRANSITION-SEQUENCE-PINNED.md`). I did not disassemble anything myself in this session -- the hard limit stands (`GameClient.local.bin` is not in this clone, confirmed: recursive filesystem search for `GameClient*.bin` under `/` returns nothing). What follows is RE-077's already-committed, SHA-256-pinned, byte-level result, re-read and re-cited by me, not re-verified against the image.

Chain (`RE-077`'s own span-pin table, reproduced with citations):

1. `TeleportVital apply` -- handler VA `0x005F14B0` (matches `external/PF_PROTOCOL_REGISTRY.tsv:37` column `handler_va`), span `[0x5F14B0,0x5F16F9)`, 163 instructions, sha256 `85723791e07493270b605313632013614d98a52c5c1ca9a4b0c809235ebd3694`. Rejects target `scene_id==0`. Reads live state `[0x1093198]+0x34C` and gates on RTTI token `StateRunTime` (`0x004C8740`) or `StateNavigation` (`0x004C7690`) ONLY.
2. On gate pass: constructs a `[0x24]`-byte object via ctor `0x004C6560` (span `[0x4C6560,0x4C65C5)`, 29 instr) carrying vtable `cStateSwitchScene`, copies the target into `[switch+0x14]`, calls `CState::RequestNext` (`0x004C7320`) at call site `0x5F16C9`.
3. `cStateSwitchScene` tick `0x004C6E80` (span `[0x4C6E80,0x4C7154)`, 199 instr) calls model-lookup helper `0x004C6660` (span `[0x4C6660,0x4C6769)`, 75 instr), which reads target `+0x12` (the same `scene_id` field from Job 1) and calls the `SCENE_NAME` table lookup chain `0x008923B0` -> `0x00890E70` (typed row + keyed row lookup) to resolve `s_MODLE_ID`.
4. Scene loader `0x00B02870` (span `[0xB02870,0xB02AAC)`, 194 instr) loads the resolved model id. On success, `cStateSwitchScene` reads `n_SCENE_TYPE` via `0x00430E10`: value `8` -> `StateNavigation` (`0x004C7600`), any other value -> `StateRunTime` (`0x004C8790`), then `RequestNext` at `0x4C70C7`.
5. On lookup MISS (unknown `scene_id`, or a row whose `s_MODLE_ID` is empty/wrong type): call site `0x4C6EED` sets `[cStateSwitchScene+0x0C] = 2` and returns. RE-077 T2 states explicitly: "no fallback/default path in this complete recursive CFG" -- an unrecognized scene_id does not degrade gracefully, it stalls the transition object with a status code and nothing else happens.
6. Old-scene cleanup: cleanup slot `0x004C7160` (span `[0x4C7160,0x4C7309)`, 98 instr) and helper `0x004C6920` clear world/app collections. RE-077 T5 closes this BOUNDED NEGATIVE: the CFG shows real cleanup calls but no identity-membership crosswalk proves "every remote actor is destroyed" or that "population census must be resent" -- do not upgrade this to either claim (see Nonclaims).

Call paths into this chain, as far as this clone's committed source shows:

- Login (`StartGameRes`): guaranteed to be in a known state before this fires (state is deterministic right after `StartGameRes`), via `legacy.make_login_teleport` at multiple `runtime.py` call sites (`5035`, `6552`, `6556`, `7132`) and `current/pf_login_game_server_v141.py:2431` (`make_login_teleport`) / `:2414` (`make_teleport_target`, whose own docstring already cites "Handler 0x5F14B0 rejects the packet unless SceneID > 0" -- this legacy encoder is written with RE-077/RE-090's findings already baked in).
- IN-SESSION, already-live character: `runtime.py:_dispatch_columbus_quest3021` (`runtime.py:4826-5044`), wired at the real dispatch call site `runtime.py:8045`. This fires on `QuestOperateVital` op1 matching Columbus's quest 3021 (see Job 3 for its gates), and composes the SAME `legacy.make_login_teleport` frame (`runtime.py:5035`) sending scene 17 with real registry-resolved coordinates, NOT at login. This is the one place in the committed corpus where the server sends a genuine cross-scene `TeleportVital` to a character that is already in an active session.

What I CANNOT answer from this clone: whether `0x005F14B0` and the chain above is the ONLY client entry point that can trigger an unload/load (e.g., whether some other UI-driven local path, like a ship dock or a menu "return to town" button, drives the same `cStateSwitchScene` machinery through a different call site). RE-077's own CFG was scoped to the `TeleportVital`-reachable path; it does not claim exhaustive coverage of every caller of `cStateSwitchScene`'s constructor. That would need fresh disassembly against the image, which needs the bridge machine.

## Job 3 -- gates on the in-session path: DONE, walked from the first gate, per the RE-118 lesson

Two SEPARATE gate stacks exist, because two separate things can happen "in session": (A) the GM `/warp` command as it is actually wired today, and (B) the Columbus quest-3021 in-session teleport that is already merged. They are not the same code and must not be conflated.

### (A) `/warp` today -- does NOT reach TeleportVital at all

`gm/chat_command_action.py` is the live route from an authorized GM chat line to an outbound action (confirmed live per its own docstring: `CORE-REQUEST-GM-029` replaced the dormant `lane_hooks.fire()` route with a direct call, merged as `pirate-force-server#214`). `runtime.py:37` imports it; `runtime.py:5523` calls `chat_command_action.make_gm_chat_command_action`. `chat_command_action.py:291-294` imports `make_warp_force_pos_frame_with_target`, `warp_command_has_coordinates`, `warp_command_scene_id` from `gm/warp_executor.py`. So the literal grep the owner-order cited (`grep -c warp_executor src/pirateforce_foundation/runtime.py` = 0) is TRUE but MISLEADING: `runtime.py` reaches `warp_executor.py` transitively through `chat_command_action.py`, which it does call directly. `warp_executor` is wired, just not by name in `runtime.py`.

Gate stack for the same-scene half (`ForcePos`):
1. `command.name == "warp"` and `args` is exactly a 3-tuple (`gm/warp_executor.py:175-192`)
2. `scene_id == current_scene_id` -- refuses (does not attempt) any cross-scene request (`gm/warp_executor.py:186-192`)
3. `x`, `y`, `z` finite-float validation (`gm/warp_executor.py:193-195`)
4. `FORCE_POS_VITAL_VERSION_CONFIRMED is not None` -- gate is permanently `None` today, HARD-LOCKED by `COO-DECISION 20260828_2130`, enforced mechanically by `tests/test_gm_force_pos_version_lock.py` (`gm/teleport_wire.py:77-151`). This is a POLICY gate (who owns a character's position after a warp), not an evidence gate -- RE-129 already answered the byte (`0`), but COO ruled the server must not write a position it did not observe from the client, and the confirmed-write point is not yet on `main`.

The cross-scene half never reaches `ForcePos` or `TeleportVital` at all -- it does not compose a frame. It writes a JSON config entry (`gm/login_scene_stage.py`) for the account's NEXT login:
1. `is_gm_account(account_name)` (`login_scene_stage.py:300`)
2. `is_known_scene_id(scene_id)` -- against `gm/scene_catalog.py`'s 330-row table (re-derived: `len(scene_catalog.SCENE_ID_TO_NAME) == 330`) (`login_scene_stage.py:302`)
3. `single_use_entry_is_admissible(scene_id)` -- against lane A's `scenarios/world_scene_registry_001.json` via `login_scene_admission.py`. Re-derived directly (not quoted from any letter): `stageable_scene_ids() == (1, 2, 14, 278, 997)` and `SANCTIONED_BARRED_SCENES == {126: 'CHIEF-DECISION 20260829_1603 item 2'}` as of this clone's committed `gm/login_scene_admission.py`.
4. Whole-file re-validate-before-write, read-back-after-write, restore-on-mismatch (`login_scene_stage.py:_write_entry_locked`)

Nothing crosses a scene while the GM is logged in via this path -- by design (`login_scene_stage.py:1-22`, explicit docstring: "Nothing is composed, nothing goes on the wire, and no character moves while it is logged in").

### (B) Columbus quest-3021 in-session teleport -- DOES reach TeleportVital, gates walked first-to-last

1. Census-membership gate (LOAD-BEARING per its own comment, `runtime.py:4873-4882`): `nested_id in (TARGET_VITAL, CHOOSE_NPC)`, `self.population_indices is not None`, and Columbus's placement index must be IN `population_indices` -- i.e. the arrival census must actually have armed Columbus for this connection before a click on him is honored at all.
2. One-shot latch: `not self.columbus_quest3021_conversation_sent` (`runtime.py:4886-4931`) -- the NPC conversation frame composes once per connection.
3. `QuestOperateVital` op1 gate: `nested_id == QUEST_OPERATE_VITAL`, `self.columbus_quest3021_conversation_sent`, one-shot latch `not self.columbus_quest3021_dispatch_attempted` (`runtime.py:4933-4955`), and `columbus_quest_dispatch.matches_columbus_dispatch(quest_fields)` -- the parsed quest fields must exactly match the Columbus/3021 shape.
4. `resolve_columbus_arrival` -> `world_scene_entry.resolve_entry(..., via_login=False)` -- must succeed against the registry (scene 17's provisional owner-decreed spawn pin, `scenarios/world_scene_registry_001.json`); raises `ColumbusDispatchRefused` otherwise (`columbus_quest_dispatch.py:514-586`).
5. ONLY THEN: `legacy.make_login_teleport(*entry.teleport_fields)` is composed and appended to the outbound action list (`runtime.py:5035-5044`).
6. `departed_from` (the character's own current scene) is passed through for a REPORT-ONLY console line -- it does NOT gate anything (`columbus_quest_dispatch.py:578-585`); the comment at `runtime.py:4996-5000` reads like a gate but the function it calls never refuses on it. Worth flagging: the code comment implies a scene guard that the implementation does not actually enforce as a refusal.
7. CLIENT-SIDE gate (Job 2, layer = static image, not this server's code): FSM state must already be `StateRunTime`/`StateNavigation` when the frame lands. Nothing in steps 1-6 measures or waits for that state -- the frame fires immediately after a dialogue-choice click, and nobody has measured what client state that click leaves the player in (`GAME_TEST_QUEUE.md:4874-4876`, `CHIEF-STATUS 20260827_1600` items (1)).

## Job 4 -- must census/actor data for the new scene follow, and in what order: DONE, evidenced from the one path that has ever composed a scene-crossing frame server-side (login/CORE-REQUEST-003 override path; the same ordering machinery the Columbus path reuses)

Evidence layer: server source (this is server-side ordering logic, not a client-observable fact and not a wire capture -- flagged as its own layer, do not read this as proof of what the CLIENT does with the order).

Re-read directly at `runtime.py:6108-6260` (login-scene-override branch, `CORE-REQUEST-GM-033`/`CHIEF-DECISION 20260829_0520`):

1. `world_scene_entry.resolve_entry(...)` resolves ONE destination (position + teleport fields) for the login.
2. The teleport frame (and the resynced `ActorAttr`/`MovementAttr` frames, when a login-scene override applies) are BUILT FROM `entry.position` -- composed BEFORE the in-memory character record is updated (`runtime.py:6182-6208`).
3. ONLY AFTER those frames are built: `self.foundation.selected.position` is updated in-memory to `entry.position` (`runtime.py:6229-6247`, comment states this explicitly: "Every later frame of this session reads `self.foundation.selected.position`... the census dispatch decides bg0001/bg0002/away-from-home from it").
4. Census composition (bg0001/bg0002/away-from-home dispatch) happens AFTER step 3, reading the UPDATED position -- so it necessarily follows the position update, which itself follows frame composition.

The measured failure mode when this order is wrong is on record, not hypothetical: `runtime.py:6236-6239` -- "an overridden login was measured asking for scene 1's checkpoint and scene 1's census while the player stood in another map -- a checkpoint that mislabels WHERE a coordinate is, which is worse than no checkpoint." This was a real, caught, since-fixed defect in this exact code, which is the strongest evidence available in this clone for "if census ordering is wrong, here is the observed symptom": the wrong scene's census gets composed/sent while the player's actual (teleported) position is a different scene.

Extending this to the in-session case (Columbus): `_dispatch_columbus_quest3021` composes and returns the `TeleportVital` action (`runtime.py:5035-5044`) but I found NO evidence in this call site, nor in `columbus_quest_dispatch.py`, that `self.foundation.selected.position` (or any census/actor dispatch for scene 17) is updated or resent as part of that same dispatch. This is a NEGATIVE finding worth stating plainly: the Columbus in-session crossing sends the teleport frame alone; if a scene-17 census/actor frame is required for the client to populate anything after the transition, nothing in this clone's committed source sends one. `columbus_quest_dispatch.py`'s own `_emit_arrival_stowaways` is a console REPORT line about who the client is still holding from the OLD scene's census -- it does not compose or send a new frame.

## Job 5 -- bounded-negative assessment: NOT a clean negative; see Short answer

The committed corpus does NOT support "there is no in-session scene-change path at all" (that would be the bounded-negative the ticket allows). There IS one, already merged, already exercising real `TeleportVital` bytes against an already-live character (Columbus/quest 3021/scene 17). What the corpus DOES support as a bounded statement is narrower and more useful: **no attended, client-observable confirmation exists that this in-session path actually moves the screen** (`GT-106` PENDING, `GAME_TEST_QUEUE.md:4840-4904`), and **the GM `/warp` command specifically does not use this mechanism** (it was deliberately scoped to same-scene-only-and-locked, plus a next-login-only stage, for policy reasons unrelated to whether the bytes can be built -- Job 3(A)). Both halves are real, permanent, citable facts; neither is "nothing exists here".

## Mandatory searches (per gate G1/G6, done before writing the source audit above)

### `pf_bridge/external/`

- scope: recursive, whole root, this clone's actual tree: 10 files, 27,925,214 bytes
- own reproducible manifest sha256 (method: sorted `relpath\tsize\tsha256\n` lines, hashed; NOT the same algorithm as whatever produced RE-156/RE-157's "manifest SHA-256" -- I do not have that tool in this clone, flagged rather than guessed at): `99691fb7b3f45f02f5edadc587a76ab981a4e9525f4460dcd406e35609ba7fe0`
- IMPORTANT DISCREPANCY, flagged not smoothed over: RE-156/RE-157 (same day, earlier rounds) both report `external/` as 130-131 files / ~37M bytes. THIS clone's `external/` has only 10 files / 27.9M bytes (`00_SEARCH_HERE_FIRST.md`, `PF_DATA_EVIDENCE.tsv`, `PF_FIELD_VALIDATION.tsv`, `PF_INPUT_INVENTORY.tsv`, `PF_PROTOCOL_PRIORITY.tsv`, `PF_PROTOCOL_REGISTRY.tsv`, `PF_RUNTIME_CLASSMAP.tsv`, `PF_SERIALIZER_FIELDS.tsv`, `PF_TAG_CENSUS.tsv`, `pf_validate_capture_fields.py`). The individual TSVs I did use (`PF_SERIALIZER_FIELDS.tsv`, `PF_PROTOCOL_REGISTRY.tsv`, `PF_FIELD_VALIDATION.tsv`) hash IDENTICAL to the ones RE-129 cited (`99282bdf...`, `27daac0c...`, `080a5f32...`), so the CONTENT I read is verified unchanged -- but this clone is missing ~120 other files (dump-derived registries, `pf_build_v5_manifest.py`, etc.) that other RE runners' environments had. Treat any claim in this letter of the form "not found in external/" as bounded to THIS reduced tree, not to the full bridge corpus.
- found: `TeleportVital`/`ForcePos`/`CWarpResult` registry rows (`PF_PROTOCOL_REGISTRY.tsv:37`, `:34-35`), full serializer field rows (`PF_SERIALIZER_FIELDS.tsv:560-620`), field-validation status rows (`PF_FIELD_VALIDATION.tsv:72-73`), priority/status rows (`PF_PROTOCOL_PRIORITY.tsv:34-37`)
- NOT found: any function named/labeled "scene unload" or "scene load" as such, any VA for a generic client scene-manager outside the `TeleportVital`-reachable chain RE-077 already walked, any capture-confirmed (not just candidate-matched) `TeleportVital` frame

### `pf_bridge/gamedata/`

- scope: recursive, whole root: 1,109 files, 15,319,585 bytes (matches the byte total RE-156/RE-157/RE-129 all independently report for this tree -- unlike `external/`, this tree is NOT reduced in this clone)
- own reproducible manifest sha256 (same method as above): `cac0c8338032589d5fbb6de1a1c9469dade80827f608947ad8498408b0faaa57`
- searched for: `scene load|unload|SceneManager|LoadScene|ChangeMap|ChangeScene` (case-insensitive, recursive) -- 0 relevant hits (one incidental hit, `CONSTDATA_TH__BUFF.tsv:9161`, a buff-effect keyword `CHANGESCENE(0)` unrelated to a client function)
- found (via RE-077, re-cited not re-derived by me): `CONSTDATA_TH__SCENE_NAME.tsv`, 271 data rows, key `n_ID`, fields `s_MODLE_ID`/`n_SCENE_TYPE`, sha256 `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b` (per RE-077; not re-hashed by me this round)
- NOT found: any table naming a client function VA for scene load/unload (this is native-code territory, not data-table territory -- consistent with RE-129's own nonclaim on the same tree)

### `pf_bridge/CLIENT_RE_QUEUE.md` / `GAME_TEST_QUEUE.md` / `notes_to_chief/`

- `RE-090` (TeleportVital/ForcePos/CWarpResult field pin): CLOSED PASS/DONE, archived `archive/CLIENT_RE_QUEUE_ARCHIVE_20260827_closed.md:2788`; full result letter is CONSUMED (`notes_to_chief/consumed/20260826_2346_RE-090-RESULT-TELEPORT-FORCEPOS-WARP-FIELDS-PINNED.md.CONSUMED.txt` -- summary only, body not recoverable in this clone); reconstructed the actual field layout from `gm/teleport_wire.py`'s docstrings (which cite RE-090 verdict + spans directly) plus `external/PF_SERIALIZER_FIELDS.tsv` rows, not from the original letter body.
- `RE-077` (SCENE-TRANSITION-SEQUENCE-001): CLOSED PASS/DONE, archived; full body IS recoverable at `archive/notes_to_chief_2026-08-19_to_26/20260826_0120_RE-077-RESULT-SCENE-TRANSITION-SEQUENCE-PINNED.md` -- this is the single most load-bearing prior result for this ticket and I read it in full.
- `RE-129` (FORCE-POS-VITAL-VERSION-001): DONE/PASS, full body at `notes_to_chief/20260828_2009_RE-129-RESULT-VERSION-ZERO-HANDLER-NOOP.md` (not consumed, still present).
- `GT-106` (`SCENE17-PROVISIONAL-ARRIVAL-001`): `[PENDING]` as of this clone's `GAME_TEST_QUEUE.md` line 4840 -- the attended ticket that would supply the client-observable half of Job 2/5 has never been run.
- `GT-141` (`GM-003 CHAT-WARP-STAGED-LOGIN-SCENE-001`): as of this clone's `GAME_TEST_QUEUE.md` (file mtime 2026-08-30 11:51+00:00, i.e. ~18:51+07:00), the ticket's own line still reads `[READY]` with its last embedded update literally stating "not yet measured against real client" (transliterated: "not yet ever measured against a real client"), and carries NO `PASS`/`OBSERVER_CONFIRMED` token anywhere in that line (checked programmatically, not by eye). The `PANYA-ORDER` letter that opened this ticket (`notes_to_chief/20260830_1655_PANYA-ORDER-...md`) asserts "GT-141 PASS today ~16:3x" -- that claim's timestamp postdates this file's last edit, so it is not a contradiction I can prove wrong, but it is also NOT verifiable from any committed artifact reachable in this session. I am not treating an order letter's own prose as provenance for a test result, per the provenance rule; this is `[UNKNOWN]`, not confirmed either way by me.
- `CHIEF-STATUS 20260827_1600` (`archive/notes_to_chief_2026-08/20260827_1600_CHIEF-STATUS-M2-console-token-fix-plus-two-real-risks-pf-adversary-found.md`): names the exact FSM-gate risk (risk (1)) that GT-106 was later opened to test, and confirms it is still unresolved as of that letter.

## Input SHA-256

- `pf_bridge/CLIENT_RE_QUEUE.md`: `d565a500fdc742c200b51f68328667625727889124c2729ef82720fc243ac444`
- `pf_bridge/GAME_TEST_QUEUE.md`: `33d8cd02007ea94e6a53fc28fb84b445d3db42a0f40ae7f035f17d3cbf4594d3`
- `pf_bridge/AGENTS.md`: `f4ecc8a3bec0780a4e09023e674a9aa643aa0e599616d18bed70865e4c90fd2b`
- `pf_bridge/EVIDENCE_GATES.md`: `b9b00ee9b848e76515613e349d3db01462123ec4adac3e75a713472cddbff21b`
- `pf_bridge/external/PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `pf_bridge/external/PF_PROTOCOL_REGISTRY.tsv`: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `pf_bridge/external/PF_FIELD_VALIDATION.tsv`: `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`: `b5880451300d28618d3cbd9d835c6f297d4fd0fc48316c1477502561256fce1f`
- `pirate-force-server/current/pf_login_game_server_v141.py`: `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`
- `pirate-force-server/src/pirateforce_foundation/runtime.py`: `7a3a958ca16b404a480bf04d43a5340f87c155bc79305385fdd6cf12a48185ca`
- `pirate-force-server/src/pirateforce_foundation/gm/teleport_wire.py`: `52019f9b0a193203de1cc9d4afda0b8aab7921401cffb5991e3373d947da9354`
- `pirate-force-server/src/pirateforce_foundation/gm/warp_executor.py`: `7a25b2f8d97cc4b22a694620f1703302c72e3a2b1045cf8df108ee164fd66081`
- `pirate-force-server/src/pirateforce_foundation/gm/login_scene_stage.py`: `ef8e115ea004946af66d79245166079ba5d90e35e31d633c3f284c1adb3da146`
- `pirate-force-server/src/pirateforce_foundation/gm/login_scene_admission.py`: `8c416eac6d2aac8381ee131df9357ad03e1cbe2b4818e4d4bde88217a12ca650`
- `pirate-force-server/src/pirateforce_foundation/gm/chat_command_action.py`: `4357f60a839613dd340787a020fd6551637020d52f3ab80451dc95056e2acdce`
- `pirate-force-server/src/pirateforce_foundation/world_scene_entry.py`: `31f60fc0972150b8cc79c8667208575d506c56b5629f5677ab5e47ae4eaacbcd`
- `pirate-force-server/src/pirateforce_foundation/columbus_quest_dispatch.py`: `1855ac2125b20c1577d81d9cedebf0a4e24ea7aa2fc4c7307b9b27cb957a4dc3`
- `pirate-force-server` git HEAD at time of this letter: `b5f1a70328397ff18da6c6bbf081825c4525a81c` (2026-08-30 11:53:07 +0000)

Confirmed absent from this environment (hard limit, not guessed): `GameClient/GameClient.local.bin` -- recursive search for `GameClient*.bin` under `/` returns zero results. No live client image was read to produce this letter; every VA cited above is re-read from already-committed, already-SHA-256-pinned prior RE results (`RE-077`, `RE-090` via `gm/teleport_wire.py`'s citations, `RE-129`) or from `external/*.tsv` rows, never from a fresh disassembly I performed.

## Nonclaims

1. Does NOT claim the in-session Columbus/scene-17 `TeleportVital` send has ever been observed to move a real client's screen. `GT-106` is `[PENDING]`. This is a `[STATIC]` mechanism claim only.
2. Does NOT claim `RE-077`'s client FSM-state gate (`StateRunTime`/`StateNavigation`) has been measured at the moment the Columbus dispatch fires (right after a dialogue click) -- nobody has instrumented that. It could pass or silently fail; both are open per `CHIEF-STATUS 20260827_1600`.
3. Does NOT claim `TeleportVital`'s `scene_id`/`scene_seq` naming is capture-confirmed -- it is a byte-exact copy-site crosswalk (RE-077) plus 132 candidate frames at `A2_STATIC_OPEN` (`PF_FIELD_VALIDATION.tsv:72-73`), not a parsed live capture.
4. Does NOT claim `TeleportTarget` has a heading field -- three vec3 floats only (x, y, z), confirmed from `PF_SERIALIZER_FIELDS.tsv` rows and `gm/teleport_wire.py`'s dataclass; if the ticket's premise assumed a heading field exists, that premise is not supported by anything committed and reachable here.
5. Does NOT claim census/actor data is or is not sent after the Columbus in-session crossing -- I found no evidence either way in the committed call site; this is a genuine gap in the shipped code, not a proven absence of intent.
6. Does NOT claim `RE-077` T5's cleanup-slot CFG proves remote actors ARE or ARE NOT destroyed on scene switch -- RE-077 itself closed that BOUNDED NEGATIVE and I am not upgrading it.
7. Does NOT resolve the `GT-141` PASS claim in the `PANYA-ORDER` letter one way or the other -- `[UNKNOWN]`, flagged, not assumed true or false.
8. Does NOT claim this clone's reduced `external/` tree (10 files vs the 130-131 other same-day letters report) means anything was deleted or hidden -- most likely a narrower checkout of this specific agent session; flagged as an environment fact, not investigated further (out of scope for a read-only RE ticket).
9. Does NOT open, modify, or recommend a specific byte value be sent to a real client. No VA in this letter was invented; every one is a citation to an already-committed, already-hashed prior result.
10. Does NOT change `CLIENT_RE_QUEUE.md`'s ticket status -- that is chief's to close after reading this letter, per the task instruction.

## BUILD_IMPACT

`BUILD_IMPACT: ANALYSIS-ONLY / TWO CONCRETE NEXT STEPS, NO SOURCE CHANGE IN THIS TICKET.` Both are `[PROPOSED]` (I did not run or observe either) and both stand entirely on the `[STATIC]`/`[PROVEN]`-cited facts above, not on new guesses:

1. **[PROPOSED]** The fastest path to an honest yes/no on "can the client change maps mid-session" is to RUN `GT-106` (already open, already scoped, already has its risk paragraph written) rather than open new server-side wiring. The mechanism (`TeleportVital` composed via `legacy.make_login_teleport`, the same encoder every login already uses successfully) is already merged and already fires in-session for Columbus/quest 3021 -- this ticket adds no new server code requirement to test that question, it only identifies that the test has not been run.
2. **[PROPOSED]** If GM-lane `/warp` is meant to eventually cross scenes live (not just stage a next login), `gm/warp_executor.py`'s refusal is a POLICY choice, not an evidence gap -- `RE-090`'s "unproven fields" concern is sidestepped entirely by the legacy `make_login_teleport`/`make_teleport_target` pair already in `current/pf_login_game_server_v141.py`, which sends `aux_presence=0` (no aux object at all) and fixed `field_0x10=field_0x11=0`/`field_0x18=2`/`field_0x20=0`/`field_0x22=0` -- values proven safe by every successful login this project has ever done, exactly the same "proven by practice" class of evidence `gm/teleport_wire.py` already accepts for `SELECT_ACTOR_VITAL`'s version=10. Reusing THAT encoder (not the newer `gm/teleport_wire.py` module, which still worries about aux-object fields nothing has to send) for a live cross-scene `/warp` would not require inventing any new unproven value. This is a design option for chief/COO to weigh against the same position-ownership policy question `COO-DECISION 20260828_2130` already ruled on for `ForcePos` -- I am not recommending it be built without that same sign-off, only naming that the "fields are unproven" objection specifically does not apply if the legacy encoder's already-battle-tested defaults are reused.

