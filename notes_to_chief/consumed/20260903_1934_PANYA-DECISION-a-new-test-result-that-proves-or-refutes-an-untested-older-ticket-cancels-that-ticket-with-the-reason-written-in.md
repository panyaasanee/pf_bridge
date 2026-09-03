ADDRESSEE: chief (owner of GAME_TEST_QUEUE.md) - cc COO (NOW.md), every lane that opens GT tickets

# PANYA-DECISION: a new attended result that proves, refutes or covers an OLDER untested ticket cancels that ticket - with the reason written on it

- when: 2026-09-03 ~19:1x+07:00 (approximate; said in chat right after the R307 round closed)
- channel: chat with ka1-A (attended session), written down by ka1-A as proxy-writer
- author of this note: ka1-A (proxy); the order is Panya's, gist below in her words

## What Panya ordered (gist, Thai)

"ถ้าได้ผลเทสเกมแล้ว พบว่าพิสูจน์หรือหักล้างกับใบเก่าที่ยังไม่ได้เทส ให้ยกเลิกใบเก่าไปเลย แล้วให้เหตุผลว่า
ใบใหม่พิสูจน์หักล้าง / พิสูจน์ครอบคลุมไปแล้ว / หรือไม่จำเป็นต้องพิสูจน์แล้ว"

## The rule, as it should read in the queue header (chief writes it; this is the gist, not the wording)

1. When a result letter lands (attended or headless), the lane that consumes it must also scan the OPEN, not-yet-run
   tickets and ask, for each one that touches the same behaviour: does this result
   (a) REFUTE the ticket's premise, (b) already PROVE what the ticket set out to prove, or (c) make the proof unnecessary?
2. If yes, close the old ticket in the same round - do not leave it READY/PENDING/BLOCKED for a tester to burn a boot on.
3. The closing line on the old ticket must name the newer ticket/letter and say WHICH of the three it is:
   `CANCELLED - refuted by <GT-nnn / letter>` · `CANCELLED - covered by <GT-nnn / letter>` · `CANCELLED - no longer needs proving because <one sentence>`.
   No bare "cancelled".
4. The owner decides nothing per ticket here; she asked that this become routine so the attended queue only holds tickets
   that still need a human at the keyboard.

## Why (owner's reason, as ka1-A understood it)

Today's two rounds (R306 five tickets, R307 eight) produced 17 cross-lane findings; several older tickets in the queue are
now either answered by them or built on a premise they refuted, yet they still show READY/PENDING and would cost a boot each.
Attended time is the scarcest resource in the project (one person, one keyboard).

## Candidates from today - chief judges, ka1-A only points

(These are examples of what the rule is for, measured in R306/R307; the consuming lane writes the actual closing line.)
- GT-141 (warp to a pinned scene then relog): GT-217 did exactly this path (`/warp 126` staged -> X -> relaunch -> landed at the registry spawn). Likely "covered by GT-217".
- GT-128 (`/warp <current scene> <x> <y>` moves the character): R306 finding 3 - the same-scene coordinate form sent `LANE_GM_CHAT_WARP_TELEPORT_FORCE_POS` and the client closed itself (ErrorData=28317). Likely "refuted by R306 letter 1655, finding 3" until LANE-GM changes the frame.
- GT-204 (mob drop left-click pickup into backpack): R303 pickup burst + GT-216 (R306, 10 clicks / 9 inserted / 8 single-click) + GT-220 (R307, 1 click). Likely "covered by GT-216".
- GT-187 (census resync after `/warp <n> <x> <y>`): R307 measured the cross-scene coordinate form refused by `WarpExecutorError` on today's main - the ticket's entry path does not exist yet; either re-open when LANE-GM fixes the executor, or cancel as "premise not on main".
- GT-205 wire half: the same notice composer proved on the wire by GT-211 (`LANE_A_UIA_NOTICE_COMPOSED ... EXIT REFUSED`, 66 B); LANE-A decides whether subcode 3 still needs its own wire measurement.
- GT-178 (scene 14 hostile twelve aggro): NOT covered - R306/R307 measured `roster=0` on scene 14; it is blocked by the tick gate (GT-224), not answered. Do not cancel; chain it behind GT-224.

## nonclaims
- ka1-A did not edit any ticket, header or ledger (chief's authority).
- Whether this rule also lives in NOW.md is COO's call (NOW.md writers are Panya and COO only, decision 20260901_1155).
