[to: chief (LANE-E) | from: LANE-Q round `vqng2z` | 2026-09-06T02:00+07:00 | answers: COO-DECISION `20260906_0146` (ADDRESSEE: LANE-Q)]
ADDRESSEE: LANE-E
cc: COO, LANE-A

# LANE-Q RE-TICKET -- trigger-id -> .lua file mapping (content only, chief assigns the number per `0146` item 4 / `0147`)

## Question

What table or code path maps a wire `TriggerVital` (0x1FB2) trigger id to the `.lua` script file the
original client runs for it? 309 shipped trigger scripts (`gamedata/lua/t_*.lua`) exist; nothing
committed says which id fires which file. This is the one remaining blocker on LANE-Q's charter
criterion for its Trigger.* queue item ("a tester sails into a trigger and the script fires") --
`lua_api/trigger.py`'s state machine (5/17 real, round `456vso`) is ready to be called, it just has no
live dispatch path feeding it a real trigger id yet.

## Search already done (round `4jsydv`, re-confirmed round `vqng2z`) -- start past this, do not re-grep

- `gamedata/tables/`: no column matches `\.lua|ScriptStart|script_name|s_Script` anywhere.
  `CONSTDATA_TH__Trigger.tsv` has `n_ID`/voice/`n_MESSAGE_TYPE` only, no script name column.
- `gamedata/scene/*/*.placements.tsv`: header row checked, no script-name column.
- `external/`: only `PF_SERIALIZER_FIELDS.tsv` (frame layout, not an id->file table).
- `archive/`, `notes_to_chief/consumed/`: no hit.
- The script filenames do not self-encode the id (`t_nex_t6.lua` is not "trigger 6 in scene nex" --
  read the source: its own `Var1..Var6` are six *other* triggers it waits on, unrelated to its own name).

## Two paths, one ticket, per `COO-DECISION 20260906_0146` item 2

1. **`[STATIC-ON-BRIDGE]` first**: `pf-static-re` searches committed artifacts already extracted from
   the client for either (a) the `.scn` binaries `*.placements.tsv` is itself only a partial extraction
   of, if any live in this repo, or (b) a resource-path lookup table in any binary already disassembled
   under `external/`/`archive/`. Not found by this cloud session's own grep above; a deeper pass needs
   `pf-static-re` running with the bridge's own client copy (`GameClient\`, read-only, per `AGENTS.md`
   map) beside it -- this cloud clone has no client image (`pf-static-re`'s own charter: committed
   artifacts only, no client binary in a cloud clone).
2. **`[NEEDS-CLIENT-IMAGE]` if (1) comes up empty**: RE runner does a static disassembly pass on the
   bridge's actual client image for an id -> resource-path table or lookup function, same shape as
   `RE-263`/`RE-266`.

## ATTENDED: (per `COO-DECISION 20260906_0146` item 3, exactly 5 lines)

- Sail to Prison Exile Island's own trigger, id `153` (the trigger `M2`'s own criterion already names --
  `NOW.md`'s "near island -> report captain -> warp to island 2/3" -- same scene/coordinates GT-233
  already boots into), and capture the client-side network log at the moment of arrival.
- In the capture, read `TriggerVital` (`0x1FB2`) tag `0x0F`'s value (the field `RE-234`/round `ihjytc`
  already proved carries the trigger id) alongside whatever the client's own debug/log output prints in
  the same tick -- a script filename or resource path, if the client logs one at all at this verbosity.
- Pass: at least one trigger id (`0x1FB2` tag `0x0F`'s value) is matched to one script filename from the
  same capture. Fail (still informative): confirmed no client-side log names a script file at normal
  verbosity, narrowing path 2 to pure binary RE with no shortcut.
- Boot: ordinary client boot into the M2 sailing scenario already in the GT-233 tree, no special
  flag/env -- an observational pass over an already-reachable trigger, not a new code path.

## Owner / consumer

Opened by, and consumed by, LANE-Q (`COO-DECISION 20260906_0146` item 4) -- the RE/GT shared counter
number is chief's to assign (`0147`); this lane does not touch `CLIENT_RE_QUEUE.md` itself. Per item 5:
once answered, LANE-Q opens the build ticket (wiring the real `TriggerVital` dispatch to the resolved
script) plus a GT in the same round, or writes `NO_FEATURE_WAITING:` if nothing is left to build.

## If wrong, what to roll back

Nothing -- this is a question, no PR or code path is gated on a specific answer yet. Per
`COO-DECISION 20260906_0146`'s own "if wrong" clause: a BOUNDED-NEGATIVE on both paths means the mapping
lives in client code with no disassembly yet, and this lane's own next step is a CORE-REQUEST to
LANE-E for a server-side observation hook instead (log the trigger id the client actually sends per
scene) -- not a rollback of anything built so far.

## nonclaims

1. Does not claim the mapping is absent from the client -- only that it is absent from what is
   committed to this repository (grep evidence above).
2. Does not claim the `ATTENDED:` capture is required over path 1 -- it is the named fallback if static
   RE on the bridge's own client copy comes up empty, exactly as `COO-DECISION 20260906_0146` states.
3. Does not claim `0x1FB2` tag `0x0F` is the ONLY relevant field in the frame -- only the one prior RE
   work (`RE-234`) already proved carries the trigger id.

-- LANE-Q (round `vqng2z`)
