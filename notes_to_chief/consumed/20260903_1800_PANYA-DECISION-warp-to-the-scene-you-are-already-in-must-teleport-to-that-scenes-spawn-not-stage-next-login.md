ADDRESSEE: LANE-GM (owner of /warp) - cc chief, COO

# PANYA-DECISION: `/warp <scene>` with no coordinates, typed while ALREADY in that scene, must move the player to that scene's spawn point

- when: 2026-09-03 ~17:58+07:00 (approximate; said in chat during the R307 attended round)
- channel: chat with ka1-A (attended session), written down by ka1-A as proxy-writer
- author of this note: ka1-A (proxy); the decision is Panya's, verbatim gist below

## What Panya said (gist, her words in Thai)

"ตอนพิม /warp แมพเดิมแบบไม่ใส่พิกัด เท่ากับย้ายฉันไปตำแหน่งจุดเกิดของแมพเดิมนั้นแหละ"

= typing `/warp 2` while standing in scene 2 should teleport her to scene 2's spawn point (the same
spot a cross-scene `/warp 2` lands on), live, in-session.

## What the server does today (measured R307, boot 61821523, 2026-09-03 17:5x+07:00)

- `/warp 2` typed in scene 2 -> stderr `GM_CHAT_STAGED_NEXT_LOGIN account='localtest' command=warp scene_id=2
  coordinates=none next='log out and log back in to land there; nothing was sent to the client now'`
- nothing reaches the client; the owner reads it as "nothing happened".
- her workaround: `/warp 1` then `/warp 2` (two cross-scene teleports) to get a fresh entry into the same scene.

## Why she wants it

A same-scene warp that silently stages the NEXT login is useless mid-round: relogging costs the whole session
(UI-A/UI-B logout buttons are refused today, so "log out" means closing the client with X and relaunching).
The one thing a tester needs from `/warp <current scene>` is "put me back at the spawn", e.g. after walking far,
or to re-enter a clean scene. GT-214's own steps assume `/warp 2` gives a fresh entry.

## What is asked

1. LANE-GM: on `/warp <n>` with no coordinates where <n> == the current scene, send the same
   `LANE_GM_CHAT_WARP_CROSS_SCENE_NO_COORDS_TELEPORT_VITAL` (73 bytes) to the scene's pinned spawn that a
   cross-scene warp sends, and print a token that says so (not STAGED_NEXT_LOGIN).
2. Keep the coordinate form `/warp <n> <x> <y>` out of this decision - it is a different code path and it
   crashed the client when used in-scene on 2026-09-03 (R306 finding 3, ErrorData=28317).
3. Whether the same-scene teleport should also re-send the scene census (fresh roster) is LANE-A/LANE-B's
   call; Panya only asked for the position.

## nonclaims
- ka1-A did not read the warp_executor code for this note; the STAGED token line above is the measured behaviour.
- Not a claim about scene 1's "walk one step before census" rule.
