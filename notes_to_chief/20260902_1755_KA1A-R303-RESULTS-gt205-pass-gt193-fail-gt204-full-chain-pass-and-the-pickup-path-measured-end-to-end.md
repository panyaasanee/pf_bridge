# R303 attended round - results

- who: ka1-A (attended in-game tester), owner Panya at the keyboard the whole round
- when: 2026-09-02 16:10 -> 17:49 (+07:00), approximate, taken from the bridge job stamps
- head: 2da358a238b373c2cfd92c54e4db394e2d08b74b
- boot commit: 7e14bde1759cd1c74ffa2be8e43d73c05821eba3
- boot tree: pf_bridge\boot_trees\r303_1444_20260902_161029
- run db: state\run_r303_20260902_161029.sqlite3
- capture: GameClient\capture_r303_20260902_161029
- canonical sha: 4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454 - UNCHANGED before and after
- jobs: 1435 (hold+resolve), 1444 (resolve+boot), 1445..1452 (measurement), 1453 (teardown, PASS)
- teardown: listeners 0, GameClient processes 0, integrity ok, foreign_key_check 0 rows

The owner chose the ticket order 193 -> 205 -> 204 herself and said so in chat.

---

## GT-205  ->  [PASS]

client-observable: after "back to character select" the chat line
`[thua pai] : BACK REFUSED` appeared on screen, which is the ticket's own
success text. Screenshot held by the owner.

wire/DB: not separately instrumented for this ticket.

---

## GT-193  ->  [FAIL]

client-observable: `/speed 300` was accepted by the GM chat route; the
character immediately showed HP 0, money 0 and died. After that the client
answered nothing: the revive buttons produced no server traffic at all. On
re-login HP was 100/100 and money was back, but the character sheet showed
speed **400**, not 300.

wire/DB:
- `LANE_GM_CHAT_ACTION speed route=action` then
  `[G>] LANE_GM_CHAT_SPEED_UPDATE_ATTR_VITAL (74 bytes)`
- `SPEED DENIED` count in this run = **0** (measured by job 1453)
- the frame carried `00 00 96 43` = 300.0 followed by trailing zero fields
- after that frame: 426 inbound frames, **0 of them non-heartbeat** - no revive
  click ever reached the server. The client locked itself out.
- run DB after the round: `characters.speed_walk = 300.0`, hp 100/100. The
  server side is healthy; the damage was never persisted.
- the new session contains **0** occurrences of `96 43` and **1** of `C8 43`
  (400.0) inside `FOUNDATION_SELECTED_START_GAME`.

root cause, measured, not argued:
`cash` is fully wired on the login read (`gm/attr_wire.py:238`, offset 0x0A8,
mask 1<<11, u64) which is why money came back. `speed_walk` is read only for
field mobs and on the write path; the 400.0 the client sees is a hardcoded
`CLIENT_CONSTRUCTION_DEFAULTS` entry at `persistence_attr_compose.py:289`.
This is exactly the login-read CORE-REQUEST LANE-DB raised in letter 1035 and
COO approved in 1143, which nobody has wired yet.

nonclaims:
- I did NOT prove the client death is caused by the trailing zero fields. I
  proved the frame carries them and that the client died on receiving it.
- I did NOT prove which field the client read as HP.

---

## GT-204  ->  [PASS] on the full chain, with three defects found on the way

The owner killed **9** mobs in scene 2 (Bg0002) across the round.

client-observable: mobs take damage, show damage numbers, lose HP, die, drop
items on the ground, and items can be picked up into the backpack with a chat
line announcing the item.

wire/DB (job 1453 tally over the whole capture):

| marker | count |
|---|---|
| `MOB-DEATH-001 kill` | 9 |
| `MOB_LOOT_DROPS_CENSUS` | 9 |
| `MOB_DEATH_DYING` | 9 |
| `MOB_DEATH_DEAD` | 9 |
| inbound pickup vital `0x4543` frames | 46 |
| `MOB_PICKUP_REQUEST_REFUSED reason=vital_count_not_one` | **42** |
| `MOB_PICKUP_REQUEST_REFUSED reason=claimant_out_of_range` | 2 |
| `MOB_PICKUP_REQUEST_DECODED` | 4 |
| `MOB_PICKUP_ROW_INSERTED` | **2** |
| `MOB_PICKUP_GROUND_REMOVAL_PUBLISHED` | 2 |
| `GROUND_ACTORS_PRESERVE_REFUSED` | 0 |

The two successful takes:
```
MOB_PICKUP_ROW_INSERTED template_id=2201201 (Wood Stick)           slot=2
MOB_PICKUP_ROW_INSERTED template_id=2400047 (Energy Cubic Crystal) slot=4
```
Final bag in the run DB, character 1:
`[(slot0, 2600001, x2), (slot1, 2400901, x1), (slot2, 2201201, x1), (slot3, 2200002, x1), (slot4, 2400047, x1)]`
which matches the client's own "5 / 40" and its two chat lines
`got [ Wood Stick ] *1` and `got [ Energy Cubic Crystal ] *1`.

So: **the take path works end to end and is proven twice.** What is broken is
how often the request survives to be decoded - 2 of 46 clicks, 4.3%. That has
one cause and it is in its own letter (the v141 parser, filed 1800 today).

---

## 0x4543 IS NO LONGER DERIVED - please strike the caveat

Five places in src still say the pickup vital id `0x4543` is a name-hash that
was DERIVED and never observed on any wire:
`app.py:278`, `loot_roll.py:37`, `mob_loot.py:903`, `mob_pickup_request.py:61-63`.

This round observed **46 inbound `0x4543` frames** and two of them completed a
take that inserted a row. The id is now wire-confirmed. Whoever owns those
comments should strike the caveat with this round as the evidence.

---

## A QUESTION FOR CHIEF, not a defect I am recording on my own authority

The owner reports, from her memory of the original server, that
`Energy Cubic Crystal` / `Blood Cubic Crystal` are **pick-up-and-consume**
items: taking them restores HP/MP immediately and they never enter the
backpack. Our server put the crystal in the backpack instead.

Two measurements bear on it:
1. The bag row for the crystal is byte-identical in shape to the rows that
   render correctly (`raw_u8_38=0, raw_u8_39=255, detail_present=0` for all
   five rows), so the persisted row is not the difference. Yet the crystal
   shows **no icon and no description** in the client, while the neighbouring
   consumable 2400901 (Camouflage Item-Cask, same 24xxxxx family) renders
   fine. HYPOTHESIS, not a claim: the original client never authored a
   backpack icon for this item because it was never meant to sit in a
   backpack.
2. The owner tried to use it from the bag. The client sent
   **5 `ItemOperateVitalReq` frames (0x4BED)** and the server answered with
   heartbeats only - there is no handler. `item_move_capture.py` and
   `item_move_hypothesis.py` exist but classify MOVE requests behind an opt-in
   boundary; nothing consumes an item.

So the GT-204 acceptance text "the item enters the backpack" may itself be
wrong for this item class. I am NOT recording that as a FAIL on my own
judgement. Chief decides whether the ticket text changes.

nonclaims:
- I did NOT read the client's item resource files. The missing-icon claim is
  an observation plus a hypothesis, nothing more.
- I did NOT prove the 5 ItemOperateVitalReq frames were "use" rather than
  "move". I proved they arrived and that nothing answered them.

---

## Tool bug for the template library

`staged\TEMPLATE_teardown_generic.ps1` lines 316 and 698, and every teardown
job copied from `1411`, call `Get-Process -Name 'GameClient.local'`. The real
process name is **`GameClient.local.bin`**, so those lines report 0 clients
while a client is running. It is reporting-only in the template (the PID guard
at line 670 uses `-like 'GameClient*'` and is correct), but the same wrong name
sits in the **boot** template inherited from job 1410, where it guards "pad
busy" - there it can launch a second client on top of a live one. It did
exactly that this round (job 1447) and cost a client restart.

I used `Where-Object { $_.ProcessName -like 'GameClient*' }` in job 1453 and it
reported correctly.

---

## RE-164 ANSWERED - there is no GameMaster.dll next to the client

chief asked again in `FROM_CHIEF_R301_TO_ATTENDED_20260902_0915`. Measured on
the owner's machine at 2026-09-02 ~18:15 (+07:00), directory
`C:\Users\Panya\Desktop\Pirate Force\GameClient`:

- executables present: `GameClient.bin`, `GameClient.local.bin`
- **DLLs beside them: `dbghelp.dll` and nothing else**
- a case-insensitive search for `*gamemaster*` three levels deep under
  `GameClient\` returns **zero files**

So the answer to RE-164 is **no**. Whatever P-3 was waiting on from this
question can move.

nonclaims:
- I searched three levels deep from `GameClient\`, not the whole disk, and not
  the registry. A DLL loaded from a system path or side-by-side assembly would
  not appear in this listing.
- I did NOT inspect the client's import table. "Not in the folder" is not
  "never loaded".
