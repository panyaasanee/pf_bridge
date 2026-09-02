# CORE-REQUEST: the v141 parser reads only the FIRST nested vital

- who: ka1-A, from attended round R303, owner at the keyboard
- when: 2026-09-02 ~18:00 (+07:00), approximate
- evidence: `GameClient\capture_r303_20260902_161029\server_console_live.out.txt`
- boot tree: `pf_bridge\boot_trees\r303_1444_20260902_161029`
- owner has read this diagnosis in chat and agrees with it

## The one line that causes it

`current\pf_login_game_server_v141.py`, `parse_outer` (~2907-2921):

```
    if outer_mask & 0x02:
        vital_count = c.u16(0x12)
        if vital_count:
            # All client packets seen so far contain one nested vital. With more
            # than one, boundaries require each vital's serializer schema.
            nested_offset = c.p
            nested_id = c.u16(0x12)
            ...
```

The assumption in that comment is **false against the real client**. R303
observed inbound packets with `vital_count = 5`. Everything after the first
nested vital is invisible to every consumer downstream.

## What it costs, measured

### (a) picking things up - 42 of 46 clicks thrown away

`mob_pickup_request.py:548` refuses when `parsed.vital_count != 1`. The real
client batches the pickup click with whatever movement vitals are in flight, so
the request usually arrives as vital 2..5 of a packet and is refused
**before it is even decoded**.

| outcome | count |
|---|---|
| inbound `0x4543` pickup frames | 46 |
| `vital_count_not_one` | **42** |
| `claimant_out_of_range` | 2 |
| decoded | 4 |
| take completed | 2 |

Owner-visible effect: clicking an item on the ground does nothing, and then
after ten or twenty clicks it suddenly works once. She described exactly that
in chat before I had the tally, which is the strongest confirmation available:
the pattern was predicted by the defect, not fitted to it.

### (b) where the server thinks the player is standing

`runtime.py:6642` feeds the pickup range check from `self.last_target_pos`,
which is written **only** at `pf_login_game_server_v141.py:4259`, inside the
`nested_id == TARGET_POS_VITAL` branch - i.e. only when TargetPosVital is the
FIRST nested vital.

R303 carried **32** TargetPosVital blocks on the wire. The ones that arrived in
a multi-vital packet were dropped, so the stored position froze while the
player kept walking:

| console line | frame | TargetPosVital position | distance to the drop | packet |
|---|---|---|---|---|
| 5635 | #511 | 20500.2, 18381.9, 1940.0 | **9250.2** | vital_count=1, accepted |
| 5886 | #529 | 21355.7, 9430.0, 521.0 | 180.3 | multi-vital, DROPPED |
| 8630 | #671 | 21404.8, 9428.9, 509.0 | 173.1 | multi-vital, DROPPED |
| 8637 | #672 | 21490.0, 9426.9, 498.0 | 189.2 | multi-vital, DROPPED |
| 12231 | #714 | 21482.5, 9433.3, 498.0 | 191.8 | multi-vital (5 vitals), DROPPED |

The drop sat at (21421.0, 9277.1, 590.7). `PICKUP_RADIUS` is 450.0
(`mob_pickup.py:467` = `DROP_SCATTER_STEP 30.0 * (MAX_DROPS_PER_KILL 16 - 1)`).
The player was 173-192 units away - comfortably inside the gate - and the
server refused her at 9250 units because that is the last position it was
allowed to learn.

An example of the packet shape, frame #714, 156 bytes:
```
12 6F 6E 14 00000000 08 00 0B 02  12 05 00      <- vital_count = 5
   12 B4 1E 0B 00 <4 floats> 0F 01 00           <- COnLandVital   (read)
   12 B4 1E 0B 00 <4 floats> 0F 01 00           <- COnLandVital   (invisible)
   12 B4 1E 0B 00 <4 floats> 0F 01 00           <- COnLandVital   (invisible)
   12 B4 1E 0B 00 <4 floats> 0F 01 00           <- COnLandVital   (invisible)
   12 90 2A 0B 00 <4 floats> 0B 01 0B 00        <- TargetPosVital (invisible)
```

## What I am asking for

**One fix, and it closes both symptoms: make the outer parser walk every
nested vital instead of the first one.** Both `mob_pickup_request`'s
`vital_count_not_one` gate and `last_target_pos` become correct for free, and
so does anything else that has been silently losing the tail of a packet for
as long as this parser has existed.

I am NOT prescribing the implementation. The comment in the code is right that
per-vital boundaries need each serializer's schema; whoever owns this decides
whether that means a length table, a per-id fixed size, or a walk that stops at
the first unknown id. That is a lane decision, not a tester's.

If the full walk is too large for one round, the owner's clicks are being
thrown away today, so an interim that only makes the pickup gate and the
position update tolerant of a tail would still be worth having - but it is the
lane's call whether a partial fix is worse than none.

## NONCLAIMS

- I did NOT establish which client action produces a single-vital packet and
  which produces a batched one. The 4.3% success rate is what was observed; I
  have no model that predicts the timing.
- I did NOT check whether any other consumer besides pickup and
  `last_target_pos` is losing data to this. It is likely, and it is unmeasured.
- I did NOT run any test suite. Nothing in src was touched by me.
- The 2 successful takes prove the take path works; they do NOT prove the
  parser is the only thing standing between the client and a reliable pickup.
