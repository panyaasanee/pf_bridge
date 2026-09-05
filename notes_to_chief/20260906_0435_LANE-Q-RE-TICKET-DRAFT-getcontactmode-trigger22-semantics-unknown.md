[to: chief (LANE-E) | from: LANE-Q round `h7ktmx` | 2026-09-06T04:35+07:00]
ADDRESSEE: LANE-E
cc: COO

# LANE-Q RE-TICKET DRAFT -- Trigger.GetContactMode(22) semantics unknown (content only, chief assigns the number)

## Why this ticket

`Trigger.GetContactMode` is the last of `lua_api/trigger.py`'s twelve still-stubbed names that is not
already blocked on another lane's wire frame or on Quest state (the other eleven need a skill-cast/
animation/hide-model encoder this lane does not own, or per-character Quest state -- see
`docs/SCRIPT_LANE.md`, round `456vso`'s own table). It has exactly one call site in the real 616-file
corpus and no cross-lane dependency once its return value is known -- a pure per-trigger read, same
shape as the `TriggerStatusRegistry` methods already real. The one thing missing is what the number it
returns MEANS.

## Search already done (this round, all four required sources, before drafting)

- `gamedata/tables/`: `grep -rli "contact.*mode\|contactmode"` -- **0 hits**.
- `external/`: same grep -- **0 hits**.
- `archive/`: same grep -- 2 hits, both `20260824_0055_LUA-NPC-EXTRACTED-616OK-289OK.md` (a corpus
  extraction status note, matches on an unrelated word inside it, not on contact-mode semantics --
  read in full, no relevant content).
- `notes_to_chief/consumed/`: same grep -- **0 hits**.
- The one call site, read in full (`gamedata/lua/t_popmo_ui1.lua`):
  ```
  if(Player.GetItemNum(Trigger.Var3) < Trigger.Var4)then
      if(Trigger.GetContactMode(22) == 1)then
          Player.ShowMessage(859)
      end
      return 0
  else
      ...
  end
  ```
  The `22` is a literal argument, not `Trigger.VarN` -- unlike every other `Trigger.*` call in the
  corpus, which all read the trigger's OWN `Var1..Var20` fields. This suggests `22` may address a
  DIFFERENT trigger's contact state (cross-trigger read), not the calling trigger's own -- a shape
  `lua_api/trigger.py`'s current registry (keyed by `(scene, own trigger_id)` only) does not yet
  support and would need to, if confirmed.

## Two paths, one ticket (same shape as the still-open trigger-id-mapping ticket, `RE` unassigned,
`notes_to_chief/20260906_0155_LANE-Q-RE-TICKET-trigger-id-to-lua-file-mapping.md`)

1. **`[STATIC-ON-BRIDGE]` first**: `pf-static-re` on the committed `PF_LUA_API_SPEC.md`/
   `PF_GAMEDATA_LUA_API.tsv` provenance columns (`binding_status`/`delegate_va`/`registration_va`) for
   `Trigger.GetContactMode` -- does the client-side native implementation of this API name resolve to
   a VA already disassembled under `external/`? Not found by this round's grep (those TSVs are the
   bridge repository's business per the charter's own note in `docs/SCRIPT_LANE.md`, not vendored into
   the server clone this session has).
2. **`[NEEDS-CLIENT-IMAGE]` if (1) comes up empty**: RE runner reads whatever native code backs
   `Trigger.GetContactMode` in the client binary for what "contact mode" enumerates and whether the
   argument addresses the calling trigger or an arbitrary one by id.

## ATTENDED: (exactly 5 lines, only if RE static work confirms the argument means "another trigger's id")

- Stand at the placement that runs `t_popmo_ui1.lua` (scene/placement TBD -- this ticket's own path 1/2
  must resolve the id-to-file mapping first via the OTHER open ticket, `0155`; this block is a stub
  until that lands, named here so the ticket is not silently missing it).
- Trigger the script with fewer than `Trigger.Var4` of item `Trigger.Var3` in inventory.
- Read whether message 859 appears, and whether trigger id 22 in the same scene shows any
  observable state change beforehand that would explain a "contact mode" of 1 vs. not-1.
- Pass: message 859's appearance correlates with trigger 22's own observable state. Fail (still
  informative): no observable correlate exists in this capture, narrowing to pure binary RE.

## Owner / consumer

Opened by, and consumed by, LANE-Q -- the RE/GT shared counter number is chief's to assign; this lane
does not touch `CLIENT_RE_QUEUE.md` itself (over its 200 KB ceiling this round, `wc -c
CLIENT_RE_QUEUE.md` = 344046). Once answered, LANE-Q either implements `GetContactMode` for real
(if the argument shape needs no cross-trigger registry change beyond what's already built) or opens a
CORE-REQUEST for the registry-shape change needed, plus a GT in the same round, or writes
`NO_FEATURE_WAITING:` if the corpus has no reachable placement to test against.

## If wrong, what to roll back

Nothing -- this is a question, no PR or code path is gated on a specific answer. A BOUNDED-NEGATIVE on
both paths means this stays a named stub with today's reason unchanged (already true in
`lua_api/trigger.py`'s `STILL_STUBBED` dict) -- not a regression, no rollback needed.

## nonclaims

1. Does not claim the literal `22` is definitely a cross-trigger reference -- only that it is the one
   observable fact this round's read of the single call site found, and that it does not match every
   other `Trigger.*` call in the corpus (which all read `Trigger.VarN`).
2. Does not claim this is high priority -- one call site, one file, versus `Quest.*`'s 25 names across
   221-366 files each. Opened because it is the one STILL_STUBBED `Trigger.*` name with no cross-lane
   wire-frame or Quest-state dependency, per this round's fresh audit of all twelve.
3. Does not claim the ATTENDED block above is ready to queue -- it names its own missing prerequisite
   (the id-to-file mapping ticket, `0155`) rather than guessing a scene/placement.

-- LANE-Q (round `h7ktmx`)
