# GT-046 PICKUP-DIRECTION-001 — STATIC PASS (outbound mouse-click path)

- Time: 2026-08-23 14:28-14:35 (+07:00)
- Code repo observed at `948e4c2` after R126 sync; tester did not edit repo/source/tools/tests/queue.
- Suggested queue state: **PASS / DONE (STATIC-ON-BRIDGE)** with the system-separation nonclaim below.
- No LOCK_GAME/LOCK_GIT, server, client, or DB was used.

## Objective — one sentence

`PickupTerrainThing` is created at the `0x006B0639` call, populated from the selected live drop object, handed to the outbound protocol queue at `0x006B0653`, and its serializer `0x005E5E30` writes the two fields through `0x0089A600` at `0x005E5E49` and `0x005E5E58`.

## Jobs 1-4

1. Three vtable-literal sites were re-censused: `0x005E8FE8`, `0x005E905D`, `0x005EE612`. The first two are allocation/initialization paths in the pickup-object factory entry `0x005E8F90`; the runtime producer calls that factory at `0x006B0639`.
2. The producer wraps the object at `0x006B064C` and passes it to generic outbound queue helper `0x005DD800` at call `0x006B0653`. The pickup serializer's write branch calls scalar WRITE `0x0089A600` twice; the read branch calls `0x0089A640` twice.
3. Trigger classification is static and exact: the `DropThingModule_Client` callback compares `0x200` (`WM_MOUSEMOVE`) at `0x006B0473` and `0x201` (`WM_LBUTTONDOWN`) at `0x006B0570`. Sending occurs only on the in-range `0x201` path. This is a mouse/input callback, not a timer or passive entity-update sender.
4. Response mapping: status `0xFC -> message 0x1F`, `0xFD -> 0x03`, `0xFE -> 0x22`. An independent local out-of-range branch also chooses message `0x1F`, so `0xFC/0x1F` is bounded to the too-far result. Meanings of `0x03` and `0x22` remain unbound. No static link from any of these three message IDs to the green `received [name] * quantity` chat template was found.

## R126 mandatory scope jobs 5-6

### Job 5 — what is field `+0x14`?

- At `0x006B0642..0x006B0649`, the producer reads pointer `[esi+0x7C]`, then dword `[pointer+0x10]`, and copies that dword to `PickupTerrainThing+0x14`.
- The containing callback `0x006B03F0` is pinned at vtable slot `+0x40` of `DropThingModule_Client`: base `0x00F3DD38`, slot address `0x00F3DD78`, value `0x006B03F0`.
- Therefore the field is the ID carried by a **live runtime drop-object instance selected by the module**, not a scene-table row read directly by this path. Static code here does not prove whether that runtime object was originally instantiated from scene data or from a network record; it only proves the source used by the outgoing request.

### Job 6 — other Drop/Loot/Item names

- Fresh registry census: 519 names total; 59 names match `Drop|Loot|Item`.
- Material independent candidates exist, so the result cannot be collapsed into one loot system:
  - `DropThingModule_Client` — name VA `0x00F0BAD0`, vtable `0x00F3DD38`.
  - `FightingDropModule_Client` — name VA `0x00F466A0`, static vtable/serializer/handler still UNKNOWN.
  - `FightingDropNotify` — name VA `0x00F0B504`, static vtable/serializer/handler still UNKNOWN.
  - `PickupTerrainThing` — name VA `0x00F3093C`, vtable `0x00F3005C`, serializer `0x005E5E30`, handler `0x005EF640`.
- The presence of the separate `FightingDrop*` family is a positive finding. It prevents claiming that `PickupTerrainThing` alone explains monster-drop production or all pickup behaviors.

## Exact spans

- pickup factory entry `[0x005E8F90,0x005E907E)`, file `[0x1E8390,0x1E847E)`, len 238, SHA `aa81d52564f61a2c4041e9d7a4ad3eee7d74fdef65bb74b0c58706ccd3f3261d`
- pickup factory wrapper `[0x005EB0D0,0x005EB0E2)`, file `[0x1EA4D0,0x1EA4E2)`, len 18, SHA `fa2b56400d8076cc1f6fb98a45d8559ec1b034d55bcd972265737b0ad62338cf`
- serializer `[0x005E5E30,0x005E5E83)`, file `[0x1E5230,0x1E5283)`, len 83, SHA `8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066`
- exact handler `[0x005EF640,0x005EF66F)`, file `[0x1EEA40,0x1EEA6F)`, len 47, SHA `5d17fc4fdeeafde0a4a34e900e76d0336e404f8d2f058ba085044ae8d88d602e`
- DropThing mouse callback `[0x006B03F0,0x006B069B)`, file `[0x2AF7F0,0x2AFA9B)`, len 683, SHA `a393f3d41b7f389fac31bc82a7cf4e78367d0413a5427d5dfe91d762b9685827`
- outbound queue helper `[0x005DD800,0x005DD887)`, file `[0x1DCC00,0x1DCC87)`, len 135, SHA `965efce3f8510ec9418168ae699df19851e822f59a1d58830750bedf2b7159af`
- registration `[0x00BEE5E0,0x00BEE5F8)`, file `[0x7ED9E0,0x7ED9F8)`, len 24, SHA `8fa9ec1ebc0b36405b847ff82adcfdbf31bb82ace52ea8efcf70bdeb1926dc81`
- module vtable window `[0x00F3DD38,0x00F3DD84)`, file `[0xB3C138,0xB3C184)`, len 76, SHA `e6540cd1d07c1df5de7850f7797f91f9627c80692ead030cd48891b3344954a6`
- image SHA before/after unchanged: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

## Artifacts

- `outbox/1032_gt046_constructor_contexts.out.txt`
- `outbox/1033_gt046_factory_callers.out.txt` (large exhaustive caller census)
- `outbox/1034_gt046_send_path.out.txt`
- `outbox/1035_gt046_trigger_vtable_and_name_census.out.txt`
- `outbox/1036_gt046_final_guards.out.txt`

## Nonclaims

- Static presence of the outbound path does not prove it ran in any captured session.
- The live runtime object used by this path is not proof of whether the object was originally created from scene data or wire.
- **Do not claim this result explains monster-drop pickup.** `FightingDropModule_Client` and `FightingDropNotify` are separate candidates and remain undecoded.
- The video/old player memory is not used to prove wire direction.
- No RTTI-backed class name is invented for the inner runtime record, no derived runtime ID is claimed, and no wire format beyond the proven two fields is added.
