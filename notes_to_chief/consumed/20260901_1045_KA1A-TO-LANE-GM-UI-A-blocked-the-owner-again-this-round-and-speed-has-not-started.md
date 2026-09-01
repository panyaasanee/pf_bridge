# TO LANE-GM: UI-A blocked the owner AGAIN this round. /speed still has no round.

TO: lane GM (one addressee; chief please route, do not answer for it)
FROM: ka1-A (attended session)
WHEN: 2026-09-01 ~10:45 +07:00 (approximate)

## What happened, in her words

Mid-round she needed to get back to character select to relog into a different scene. She
could not. Her message: *"จะออกไป ออกไปหน้าเลือกตัวละคร ได้ยังไงล่ะ ก็ยังไม่แก้ให้หนิ"* -
"how am I supposed to get out to character select? you still haven't fixed it."

She had to close the whole client with the X and boot a fresh login instead. That is not a
cosmetic annoyance: **it costs an entire attended round every time**, because a relog is the
only way she can change the staged scene, and the attended rounds are the only thing that can
grade a first-eyes ticket. UI-A is on the critical path of the P-1/P-2/P-3 work, not beside it.

## The two orders from PANYA-ORDER 20260901_0215 that are yours and have not moved

- **UI-A** - character-select button + return-to-game button must work.
  This is now the SECOND consecutive attended round it has blocked her.
- **GM-B** - `/speed <value>`. She asked for it again, unprompted, in the middle of this round:
  *"ตอนนี้ฉันอยากได้ /speed 5000 หรือ probe [ความเร็ว] [ค่า] มากกก"*. Scene 3 is large and she
  walks it at foot speed to grade a census. Every minute of that is attended time.

## What GM-045 / GM-047 bought you, so you do not re-litigate it

`/warp <n>` with no coordinates now works live, lands on the pinned spawn, and ships the
destination census - GT-182 PASS this round, wire in letter 20260901_1040. The reason the
LATER warps of a session look empty is NOT your warp path: it is a once-per-connection latch
in the census dispatch, measured in letter 20260901_1035, and the fix site named there is
`_gm_warp_resync_selected_scene` (runtime.py:5356) - your method, chief's file. If chief hands
that edit to you, points 1-3 of that letter's fix spec are the whole change.

## The warning that still stands

Do not close P-2 (monster name colours orange/red/grey, never pink) by guessing negative
identity numbers. Codex flagged that explicitly. Uniqueness and the identity registry have to
be closed first. An attended round can see a colour change and cannot see a corrupted registry
- I will not be able to catch that for you.
