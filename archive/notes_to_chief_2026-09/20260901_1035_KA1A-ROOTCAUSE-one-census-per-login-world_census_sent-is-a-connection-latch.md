# ROOTCAUSE - "no NPC on any map after the first warp" is ONE latch, measured

TO: chief (one addressee)
FROM: ka1-A (attended session, proxy-writer for Panya)
WHEN: 2026-09-01 ~10:35 +07:00 (approximate, wall clock)
ROUND: GT-182 boot 1404, BOOT_COMMIT 3ce8ab1682f82b783be0ba9b9fa596fc032e9ab8,
capture `GameClient\capture_gt182_20260901_094056`, run DB run_gt182_20260901_094056.sqlite3

## The owner's report

Session 2 of the GT-182 round. She warped to 5, 6, 7, 8, 9, 10, 11, 14 and back to 1.
Every warp DID change the map (screenshots: Evil Port X:9,280 Y:11,350 / Ocean Walled City
X:-9,652 Y:23,860 / Voodoo Island X:-21,191 Y:8,574 / Silver Harbour X:19,440 Y:23,997 /
Hell Volcanic Island X:-10,384 Y:5,234). **Not one of them had a single creature, even after
she walked. Port Royal on the way back was empty too.**

## THE CAUSE - one line, `runtime.py:7572`

    if (
        world_census_enabled
        and not self.world_census_sent        # <<< THIS
        and not self.world_census_refused     # <<< AND THIS
        and parsed.outer_id == legacy.GSCN_RUNTIME_PROTOCOL_REQ
        ...

`self.world_census_sent` is initialised **once per connection** (runtime.py:1155, in the
connection state constructor) and set True the moment a census ships (7785 / 7996 / 8016 /
8122 / 8250 / 1384). **Nothing anywhere resets it.** `_gm_warp_resync_selected_scene`
(CORE-REQUEST-GM-045/047) relabels `selected.position.scene_id` and stops there - I read the
whole method, it never touches the latch.

So the census dispatch is a **once-per-login** dispatch. Not once per scene. Once per TCP
session. Every warp after the first one is silent by construction.

## The wire proves it, exactly

Whole-session counts from `server_console_live.out.txt` (8,228 lines) and `.err.txt`:

| token | count |
|---|---|
| inbound chat vitals `0xAC52` | **20** |
| `LANE_GM_CHAT_ACTION warp route=action` | 16 |
| `LANE_GM_CHAT_WARP_CROSS_SCENE_NO_COORDS_TELEPORT_VITAL` (73 B) sent | **10** |
| `GM_CHAT_WARP_REFUSED ... scene_has_no_login_entry` (12, 13, 15, 17) | 4 |
| `GM_CHAT_STAGED_NEXT_LOGIN` (3, 126) | 2 |
| `LANE_HOOK_FIRED ... scene_census_composer:3` | **2** |
| `WORLD_POP_HANDOFF` | **2** |
| `WORLD_CENSUS_BG*` assembled lines | **2** |

Two censuses in a whole round. Both scene 3. Both are the FIRST census of their login:
- session 1: login at scene 1 (no census - see the second bug below), then `/warp 3` -> census.
- session 2: login **into** scene 3 (persisted position), census at once, latch set -> the
  next nine warps got a teleport frame and nothing else.

Ten warp frames went out. Two censuses came back. That is the whole bug.

## SECOND BUG, same block, same round: scene 1 still needs her to walk

Same `if`, last disjunct:

    and (
        self.last_target_pos is not None
        or self.foundation.selected.position.scene_id != world_population.SCENE_ID
    )

For scene 1 the census cannot ship until a `TargetPosVital` has arrived - i.e. **until she
walks**. That is exactly the thing PANYA-ORDER 20260901_0955 forbids, and exactly what she
saw at both logins into Port Royal. It is one clause, not a redesign.

## FIX SPEC - what has to change (src/ is your authority, I did not touch it)

1. **Clear the latch on a cross-scene arrival.** The natural site is
   `_gm_warp_resync_selected_scene` (runtime.py:5356), inside the branch that has already
   proven `target.scene_id != selected.position.scene_id`, i.e. right beside
   `gm_warp_selected_scene_resynced_<n>`. Reset `world_census_sent`, `world_census_refused`.
2. **Clear the stale anchor with it: `last_target_pos = None`.** Otherwise the newly-unlatched
   census composes the destination roster around the DEPARTURE scene's coordinates. This is
   not hypothetical - it is F-1 from GT-172 arriving through a different door. The reason
   `/warp 3` looked right in session 1 is that she had not walked in Port Royal, so
   `last_target_pos` was None and the block fell through to the destination's pinned spawn.
   Had she walked first, GT-182 would have "passed" with 62 actors planted in Port Royal's
   coordinate space.
3. **Clear the siblings that describe the old scene**, or click-dispatch will point at the
   previous map's placement indices: `population_indices`, `world_census_indices`,
   `population_refresh_anchor`, `census_anchor_record`, `npc_idle_action_sent`,
   `world_census_identity_resolved`, `world_census_actor_count`.
4. **Drop the scene-1 walk requirement** (the disjunct above), so login ships the census
   eagerly on the home scene too. That closes PANYA-ORDER 20260901_0955 in the same edit.
5. Registry check I already did so nobody re-does it: `ROSTER_COMPOSERS` currently holds
   bg0015, bg0004, bg0010, bg0005, bg0006, bg0008, bg0003, bg0007, bg0009, bg0011, bg4001 -
   **every scene she tried has a composer**. Nothing is missing from the table. The rosters
   were ready and the latch never let them out.

## NONCLAIMS

- I did NOT measure that the fix works. This is a read of the code plus a count of the wire.
- I did NOT prove the client would render a second census in the same session. Replace
  semantics on `make_runtime_remote_actors` says it should; nobody has measured it. **The
  round that lands this must be attended-tested before any first-eyes ticket is graded.**
- I did NOT check whether `world_census_refused` had latched instead of `world_census_sent`
  in session 2. Both are in the same `if`; either one explains it identically.
- `gm_warp_selected_scene_resynced_*` does not appear in the console. Events are not printed
  live, so this is NOT evidence the resync failed - it is simply unmeasurable from this capture.

## SELF-CORRECTION - my previous message to the owner was wrong

One message before this I told her the client had **stopped transmitting chat** (I said "1
chat frame in the whole session") and advised a one-warp-per-login loop. **That was wrong.**
The count is 20 inbound chat vitals, and the hex decodes to `/warp 3, 5, 3, 5, 5, 6, 7, 8, 9,
10, 11, 12, 13, 15, 14, 17, 126, 997, 1`. Every command she typed reached the server. My
measurement was filtered too narrowly and I published it as a fact. Same class of error as
the 8 KB head-truncation and the "RE lane does not exist" call. The correction is in her hands
already; this is the file copy.
