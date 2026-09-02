# TO LANE-B: two things the owner saw with her own eyes in R303

- who: ka1-A, attended round R303, owner Panya at the keyboard
- when: 2026-09-02 ~18:05 (+07:00), approximate
- evidence: `GameClient\capture_r303_20260902_161029\server_console_live.out.txt`
- sample: 9 mob kills in scene 2 (Bg0002), one attended session

Neither of these is a refusal, an error or a traceback. Both are the server
doing exactly what it is written to do, and both are visible as a bug from the
player's chair. That is why they are worth a letter.

---

## 1. A mob that dies stands frozen until the player hits something else

What the owner saw, unprompted and repeated across the whole round:

> the mob I killed stayed standing, frozen. It only fell over when I hit the
> NEXT mob. Then it lay there as a stiff corpse.

What the console shows. Every kill sends two frames:

```
MOB-DEATH-001 kill: performer 0x10010001 -> target 0x2050 (ceiling 3857)
  dying frame 187 bytes, timer 20.0 (> 0, latches 0x44384C)
  dead  frame 187 bytes, timer  0.0 (<= 0, gates 0x443990)
  hold 700 ms between them
MOB_SCENE_RECOMPOSE ... actors=97 wire=97 ... frame=18006B ... dead_timer=20.0
MOB_SCENE_RECOMPOSE ... actors=97 wire=97 ... frame=18006B ... dead_timer=0.0
[G>] MOB_DEATH_DYING (18006 bytes)
[G>] MOB_DEATH_DEAD  (18006 bytes)
```

Both frames go out immediately, 700 ms apart, exactly as designed. The timing
is NOT the problem. The **shape** is: a death is published by rewriting the
entire 97-actor scene census, twice. The client appears to treat a census as
"here is the state of the world", not as "this actor just died", so it never
plays a death animation - the dead actor's pose only changes when the next
census arrives, which happens on the next hit or the next kill.

Counted over the round: 9 kills, 9 `MOB_DEATH_DYING`, 9 `MOB_DEATH_DEAD`,
17,688-18,112 bytes each. Roughly 320 KB of full-scene rewrites to announce
nine deaths.

### 1b. The 20-second timer is the wrong class of frame

The owner also reports, from the original server:

> when a mob died there was never a "knocked down" or "heavily injured" text
> and never a countdown. Those were for players only.

The dying frame carries `timer 20.0`, the client renders a 20-second countdown
that then vanishes when the dead frame (timer 0.0) lands. src already says of
that frame:

> same SHAPE as the frame GT-022/GT-025 watched drop an NPC, not the same body

So the player-death presentation is being reused for mobs. The owner's memory
of the original behaviour is first-hand and consistent; I am passing it on as
her testimony, not as something I measured.

---

## 2. Ground drops expire correctly and the client is never told

`DROP_LIFETIME_SECONDS = 120.0` (`mob_loot.py:819`) and the cell expires its own
rows lazily - "evaluated when you touch the cell". Nothing pushes an expiry to
the client, and the client's ground list is only corrected when a whole live
ledger is republished, which happens on the next kill or the next successful
take.

The countdown is real and visible in the log:

```
MOB_DROP_PRESENCE live=2 carried=1 oldest_left=19.2s newest_left=120.0s
MOB_DROP_PRESENCE live=2 carried=1 oldest_left=65.9s newest_left=120.0s
MOB_DROP_PRESENCE live=3 carried=2 oldest_left=19.6s newest_left=120.0s
MOB_DROP_PRESENCE live=3 carried=2 oldest_left=35.6s newest_left=120.0s
MOB_DROP_PRESENCE live=5 carried=3 oldest_left=11.4s newest_left=120.0s
MOB_DROP_PRESENCE live=5 carried=4 oldest_left=17.5s newest_left=120.0s
```

What the owner saw matches it exactly, including the exception:

> I hit the next mob and the earlier item disappeared. But one crystal did NOT
> disappear - and later I could still pick that one up.

The one that survived was inside its 120 s. The ones that "disappeared when she
hit the next mob" had already expired seconds or minutes earlier; the hit is
merely when the client was finally told. So the item she saw on the ground was
often an item that no longer existed.

This also explains the first drop of the round appearing to sit there forever:
no further kill happened for a long time, so no republish ever corrected it.

The timer is not broken. What is missing is telling the client when a row goes.

---

## NONCLAIMS

- I did NOT prove the client ignores census frames for death animation. I
  proved the server sends only census frames and that the corpse updates on the
  next one. The client-side reason is unmeasured.
- I did NOT measure the wall-clock gap between DYING and DEAD from the client's
  side; the 700 ms is the server's own stated hold, still marked
  "[COO-confirmed provisional, unmeasured]" in src.
- The "original server never showed a countdown for mobs" statement is the
  owner's recollection. It is not something this round measured.
- I did NOT look for a redraw or sweep tick anywhere outside `mob_loot`. If one
  exists elsewhere and simply never fired, that changes item 2 entirely.
- 9 kills is a small sample and all of them were in scene 2.
