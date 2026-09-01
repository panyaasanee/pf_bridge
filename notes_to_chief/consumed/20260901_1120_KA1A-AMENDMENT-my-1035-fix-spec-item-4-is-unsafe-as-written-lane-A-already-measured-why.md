# AMENDMENT to my own 20260901_1035 fix spec - item 4 is UNSAFE as I wrote it

TO: chief (one addressee)
FROM: ka1-A (attended session)
WHEN: 2026-09-01 ~11:20 +07:00 (approximate)
WHY NOW: before anybody implements 1035. This is a correction of my own letter, not of a lane's.

## What I wrote 45 minutes ago

> 4. **Drop the scene-1 walk requirement** (the disjunct above), so login ships the census
>    eagerly on the home scene too. That closes PANYA-ORDER 20260901_0955 in the same edit.

I wrote that as if it were a free one-clause deletion. **It is not, and lane A had already
measured why** - round `A_20260901_1037 (yv3k9x)`, written before I read it:

> ถ้าส่งก่อนเดิน `self.population_indices` จะถูกตั้งก่อนที่ dispatcher เดิม
> (`current/pf_login_game_server_v141.py:4395-4416`) จะมี `last_target_pos` ให้ unpack —
> คลิก NPC ก่อนเดินจะ `TypeError` กลาง listener thread (ไม่มี `except`) = หลุดการเชื่อมต่อ

In English, for the record: shipping the scene-1 census before the first `TargetPosVital`
sets `population_indices` while the frozen v141 click dispatcher still has no
`last_target_pos` to unpack. The first NPC click after that raises `TypeError` inside the
listener thread, which has **no `except`** (frozen file, md5
`7fcdf7d2b80326311a1edf8bc7b4803d`, and we do not edit it). The connection dies.

So the walk requirement is not an oversight. It is a brake, and the comment block at
`runtime.py:7560` says so in its own words: *"it needs either a deferred install of
population_indices at the first TargetPosVital, or a runtime.py ChooseNPC guard for scene 1
shaped like the one lane_hooks/lane_a_choose_npc_scene1.py already has for its own scene."*

## The corrected item 4

**Items 1, 2 and 3 of letter 1035 stand unchanged** - the latch, `last_target_pos`, and the
sibling scene fields. Those are the cross-scene warp path and carry none of this hazard,
because by the time a warp arrives the session has already been through login.

**Item 4 is now conditional.** Eager scene-1 login census may only land together with ONE of:
  (a) `lane_hooks/lane_a_choose_npc_scene1.py` flipped to `production_allowed = True` - lane A
      built it this round and deliberately left it OFF, for two reasons in its own docstring;
      or
  (b) a deferred install of `population_indices` at the first `TargetPosVital`.

Landing item 4 alone would hand the owner a disconnect on her first NPC click of every
session. She has already lost a round to a mid-play disconnect today. I will not have my own
letter cause the second one.

## A second thing I want on the record, because it is the same shape as my morning error

Lane A reached the correct answer on this from the comments already in the file, in a round
that also says - correctly - that its own prompt template is stale. I reached a wrong answer
faster by reading the same block and not following the comment it points at. **The lane was
right and I was quick.** Nobody should treat my measurements as outranking a lane's round file
just because they arrive from the attended session.

## One small real gap, low urgency, while I am here

PANYA-DECISION 20260901_0920 is implemented in `pf_bridge` (`PF_STALE_MINUTES: '55'` line 114,
`PF_STALE_CLOSE_HOURS: '6'` line 122, separate `LIMIT`/`CLOSE_LIMIT` at 356/357) and the
liveness reprieve is in BOTH repos (`br.yml:443-470`, `sv.yml:784-810`, `LIVENESS_WINDOW_SEC=1800`,
absolute bound 2x close). Good.

But `pirate-force-server` still has `PF_STALE_MINUTES: '45'` (line 156). The owner's reasoning
for 55 - *"รอจนใกล้ 60 นาทีใกล้รอบใหม่ก่อนค่อยปลด"* - applies to that repo's drafts identically.
Not urgent, not blocking anything, one value.

## NONCLAIM

I have not measured that a scene-1 eager census actually crashes anything - I am relaying lane
A's reading of the frozen dispatcher plus the runtime comment. Neither has anyone measured
that it does not. That is precisely why item 4 must not ship alone.
