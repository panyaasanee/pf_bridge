# R100 Agent C -- in-repo fact pack for coverage row `monster_spawn_and_loot`

Date: 2026-08-20 . read-only research . repo root `$R` = `Pirate Force ServerProject`
Purpose: every proven fact the repo already holds about (A) item/backpack wire+DB
paths and (B) actor spawn/despawn transport, so a later round-98-style design can
rank the doors of a loot loop by how proven each is. Nothing here is a design.

Tag legend (same discipline as the sources): [PROVEN wire] = byte-exact capture or
runtime-accepted frame; [PROVEN db] = durable rows verified; [STATIC only] = client
disasm proof, never exercised; [NO PATH KNOWN] = nothing in repo; [NEGATIVE] =
searched and absent; [DERIVED] = computed here from a validated project algorithm.

---

## 1. ITEM/BACKPACK WIRE -- every proven message

### 1.1 Client -> server

| class | id | nested ver | body shape | proof |
|---|---|---|---|---|
| `ItemOperateVitalReq` | `0x4BED` | 0 | 3 fields: u8 tag `0x0B` operation (obj `+0x14`) + u32 tag `0x14` value32 (`+0x18`) + qword tag `0x32` item identity (`+0x20`). 36-byte framed request | V104 capture lane (`reports/PF_RE_V104_ItemOperate_Request_Capture_20260814.md`); exact merge PC pinned as `V111_MERGE_REQUEST_PC` in `src/pirateforce_foundation/inventory.py:77` (fields `(4,0,3)`); pf_bridge FINDINGS_R21 corpus audit: 24 ItemOperate-shaped inbound frames across 630 files / 20,209 inbound, ALL `operation=4`, 12 distinct PCs |
| `UseItemVital` | `0x1F4F` | - | ONE field: qword tag `0x32` identity (`+0x18`), serializer `0x6C0180` -- no operation byte, no value32. `use` does NOT ride ItemOperate | `reports/PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md` s.4.1 [STATIC only -- no capture, no server handler; v141 declares the constant only, 3 occurrences, no dispatch branch] |
| `TradeCmdVital` | `0x23B5` | 0 | see section 3 | V115/V120 runtime captures |

Operation byte space of `0x4BED` (all bounded, per SPLIT-OPERATE-001/002/003 + USE_DROP_SELL001):
- **op4** = move/merge family (value32 = destination slot or 0-for-merge). [PROVEN wire, runtime + corpus]
- **op5** = equip-from-bag (V123 capture; `V123_EQUIP_FROM_BAG_OPERATION = 5` in v141). [PROVEN wire, request direction]
- **op3** = single-target identity-only, produced ONLY by a modal-confirm dialog callback (`0x5B9CE0`, template `0x69`); destructive-shaped (no quantity, no destination, no counterparty). NOT claimed to equal "drop/destroy" -- caption is in packed `$pcz` text assets. [STATIC only]
- **op6** = quantity-op family behind numeric-input dialog helper `0x5A1630`; 4 call sites (A `0x57D1F4`, B `0x58294D`, C `0x5A3532`, D `0x5BA208`); verb `0x16` gates 3 of 4; sell-N ELIMINATED (zero vendor/price strings at any producer), remaining candidates split / drop-N / give-N. [STATIC only; live capture is the only remaining hop, queued GT-015]
- **sell does not ride ItemOperate at all**: `StallOperateVital` (priced wire: u8 op + qword identity + string + u32 price, serializer `0x76A630`) and the `GSCN_BlackMarket*` family are separate registered classes. [STATIC only]

### 1.2 Server -> client

| class | id | nested ver | body shape | proof |
|---|---|---|---|---|
| `ItemOperateVitalRes` | `0x4C13` | **2** (v0 rejected at V105 with `ErrorData=0x4C13`; v2 accepted V106) | u8 tag `0x08` result (0 = processing path) + u8 tag `0x0B` ItemBagAttr-present + ItemBagAttr delta + u8 tag `0x08` affected-list count (0). ItemBagAttr delta = attr base (`0x0B 0xFF` + qword 0) + ItemAttr collection (u16 tag `0x0F` count + items) + removal-identity collection (u16 tag `0x0F` count + qwords) | V105/V106/V107 boundary reports; builders `make_item_operate_move_delta_success` / `make_item_operate_stack_merge_success` in `current/pf_login_game_server_v141.py:2653/2672`; client handler `0x5A8A00`: first collection -> update calls `0x59FB40`/`0x5A1240`, second -> removal `0x59FC50` [PROVEN wire, runtime-accepted V106-V111 and ITEM-LIFECYCLE-001] |
| `ItemOperateVital` | `0x36FE` | - | name/id registered in v141 `NAMES` only; never used as a carrier by any lane | v141:424 [NEGATIVE for usage] |
| Backpack initial projection | `BackpackAttr 0x1F81` subwire nested inside StartGame ActorAttr (marker `u16tag(0x12, 0x1F81)`, v141:2747) | - | attr base + ItemAttr collection + identity collection + trailing u8 tag `0x0B` operational-range mask from obj `+0x68` | V101/V102/V103 reports; ITEM-LIFECYCLE-001 byte-splice proof: replacing the 159-byte initial 4-item subwire with the 124-byte merged 3-item subwire reproduces the whole reconnect StartGame PC [PROVEN wire + runtime] |
| `UpdateAttrVital` `0x309A` carrying BackpackAttr | - | - | is a FULL REPLACEMENT of the visible primary item tree, not a delta -- a one-item "delta" would delete every other item | V121 static application audit (`reports/PF_RE_V121_to_V122_Final_Buy_Cash_Update_20260814.md`) [STATIC only, load-bearing constraint for any grant-item design] |

Per-item `ItemAttr 0x0ECD` wire (inside collections): qword `0x32` identity + u32 `0x14` template + u16 `0x0F` quantity + u16 `0x0F` slot + u8 `0x08` (+0x38 raw) + u8 `0x08` (+0x39 raw, 0xFF) + u8 `0x0B` detail-present. Identity qword at client obj `+0x28` is the Backpack tree key; canonical container order is by identity (high dword then unsigned low), proven Grade A in ITEM-MOVE-ORDER-001.

Client-side consumer with NO prestate gate: ITEM-MOVE-CONSUMER-001 (Grade A static) -- the `0x4C13` result handler clears the displayed payload by incoming identity, routes by incoming slot, and **clones the complete incoming identity/template/quantity/slot into the destination slot object with no destination-occupancy rejection and no old-quantity comparison**. This is the closest thing the repo has to a proven "client will display an item it did not previously have" path. [STATIC only]

Backpack gating facts that a pickup design will trip over:
- `BackpackAttr` trailing operational-range byte must be `0x01` or the free-slot counter `0x5A19E0` scans zero enabled segments (V120: fixed `not enough space` on the shop drag; base 40-slot segment = bit 0).
- Backpack UI is behind the second-password prompt (`CheckSecondPwdVital 0x4B98`; V110 OK response, and Foundation `--second-password-mode bypass`).

### 1.3 What "backpack write is one-shot and dispatch is unguarded" means operationally (FINDINGS_R21, pf_bridge)

- On a **standard boot** (`tools/run_foundation_visible.ps1`: only `--db --capture-root --second-password-mode`) exactly ONE backpack mutator is reachable: the exact V111 merge. It requires (a) the inbound bytes to equal `V111_MERGE_REQUEST_PC` whole (`inventory.py:277-287` `is_exact_merge_request`), and (b) DB pre-state exactly `INITIAL_BACKPACK` (`store.py:294`). Second attempt returns `None` = replay, no write. **So the backpack can be written once per character lifetime**; measured against the real client corpus, 1 of 24 ItemOperate frames would write; the other 23 fall through silently by design (no reply, no write).
- Move / swap / occupied-merge / generalized lanes exist but ONLY behind opt-in scenario flags (`--item-move-hypothesis-scenario` etc.); without the flag `session.py:78` raises `PermissionError` before any write.
- **Dispatch is unguarded**: `v141.py:7440` `try` pairs with `finally:7847` only -- no `except` around `state.dispatch(parsed)` (`:7558`). An exception escaping dispatch reaches `shutdown.py:267-269` `record_thread_failure` -> `request_stop` = the whole server dies. Inside dispatch, `_checkpoint_exact_target` (position save, `runtime.py:290/315/645`) is the one DB write with no try/except; `store.py:216` raises `PermissionError` when `rowcount != 1`. The merge lane (`runtime.py:164-174`) and hypothesis lane (`:264-274`) both catch `Exception` and answer "no reply". **Operational rule for any loot/pickup lane: every new DB write on the dispatch path must be wrapped like the merge lane, or a single failed write kills the server mid-play.** (Today the trigger is unreachable single-client because the accept-loop serializes sessions -- N2 -- but that interlock disappears the day multi-client lands.)
- FINDINGS_R21 N4: character delete has NO db path; `delete_actor.py` is a pure parser, `DELETE_ACTOR_VITAL` never dispatched. (Superseded in part by later DELETE-SOFT lanes -- `store.py` now has a guarded `deleted_at` soft-delete writer at ~:236 -- but the point stands that nothing about actors-in-scene ever touches the DB.)

---

## 2. ITEM/BACKPACK DB -- exact persistence

Tables (verbatim from `migrations/003_character_inventory.sql`):

```
character_backpacks(
  character_id INTEGER PRIMARY KEY REFERENCES characters(id) ON DELETE CASCADE,
  base_mask INTEGER NOT NULL CHECK(base_mask = 255),
  base_identity INTEGER NOT NULL CHECK(base_identity = 0),
  range_mask INTEGER NOT NULL CHECK(range_mask = 1),
  updated_at TEXT NOT NULL)

character_backpack_items(
  character_id INTEGER NOT NULL REFERENCES character_backpacks(character_id) ON DELETE CASCADE,
  item_identity INTEGER NOT NULL CHECK(item_identity BETWEEN 0 AND 9223372036854775807),
  template_id INTEGER NOT NULL CHECK(template_id BETWEEN 0 AND 4294967295),
  quantity INTEGER NOT NULL CHECK(quantity BETWEEN 0 AND 65535),
  slot INTEGER NOT NULL CHECK(slot BETWEEN 0 AND 65535),
  raw_u8_38 INTEGER NOT NULL CHECK(raw_u8_38 BETWEEN 0 AND 255),
  raw_u8_39 INTEGER NOT NULL CHECK(raw_u8_39 BETWEEN 0 AND 255),
  detail_present INTEGER NOT NULL CHECK(detail_present IN (0,1)),
  PRIMARY KEY(character_id, item_identity),
  UNIQUE(character_id, slot))
```

Writer module: `src/pirateforce_foundation/store.py` only.
- INSERT: `_insert_initial_backpack` (store.py:276-295; called at character creation, plus migration backfill of the exact 4 starter rows: identities 1..4, templates 2600001/2400901/2600001/2200002, slots 0..3).
- UPDATE/DELETE: `apply_v111_stack_merge` (store.py:340-377: UPDATE identity1 quantity->2 with full-row predicate, DELETE identity 3 with full-row predicate, touch `character_backpacks.updated_at`); `apply_hypothesized_v111_slot2_move` (:380+); later swap/merge hypothesis writers (FINDINGS_R21 A1 line map: backpacks 223/315/346/388; items 228/297/306/337/374).
- Read: `_load_backpack` `ORDER BY item_identity` then `require_known_backpack` (structural validation: unique identities, unique slots 0..39).

Proof of durability: ITEM-LIFECYCLE-001 (Grade B runtime, `reports/PF_ITEM_LIFECYCLE001_V111_STACK_MERGE_PERSISTENCE_RUNTIME_PASS_20260816.md` + ledger row): Round A merge committed rows; Round B reconnect with zero CreateActor/ItemOperate received the exact 3-record merged Backpack; final SQLite adds migration 3 + merged rows only. Tests: `tests/test_item_lifecycle.py`, `test_item_move_*`, `test_item_swap_hypothesis.py`, `test_item_merge_hypothesis.py`.

**Fact a loot design must absorb: there is NO code path anywhere that inserts a NEW item row after character creation** (FINDINGS_R21 A1: items INSERT exists only at creation). Item creation = new `(character_id, item_identity)` row + server-owned identity allocation policy, and V121 explicitly lists "server-owned new item identity and slot policy" as unrecovered. The CHECK constraints do not block new rows (only header values are frozen), so the schema itself can hold a granted item today.

---

## 3. SHOP / OPERATE -- what V111-V115 (and the V116-V122 continuation) proved

- **V111** [PROVEN wire+runtime, later PROVEN db in ITEM-LIFECYCLE-001]: exact op4 `(dest=0, source id=3)` merge request answered by `0x4C13` v2 delta (identity 1 -> qty 2, remove identity 3); client showed `2/40` and kept the state across later moves.
- **V112-V114**: P30/template 31 `Tornado Eagle` (`0x201F`) = data-proven usage-1 monster at exact Port Royal placement; P91 `0x205C` usage-2 control. Both stream as **actor type 4** with only NPCAttr + initial MovementAttr -- no FightAttr/ActionVital/AI/unknown fields. P30 gets no conversation/facing service (usage-1 suppression proven).
- **V114 -> V115 TradeZoomVital `0x2A7A`**: nested version 2; member `+0x24` is UTF-16 (helper `0x89A810`, tag `0x48`); V114's ANSI tag `0x44` produced `ErrorData=10874` (= `0x2A7A`), V115 changed that ONE byte and the shop opened: second-password prompt (`CheckSecondPwdVital 0x4B98`, `1234` + OK response), then `Sword Soul Shop` with buy/sell grids.
- **V115 close**: `TradeCmdVital 0x23B5 v0` command 12 (`08 0C 19 00000000 08 00`), capture-only, no response invented.
- **V118/V120 corrections** (supersede V115's "icon inserted" impression): cart-add is **command 6** with dword 0 + ItemAttr detail (`identity 0, template 2200009, qty 1`), gated by the Backpack operational-range byte (V120 flipped trailing `0B 00 -> 0B 01`); ack = `TradeItemResultVital 0x557B v0 result 13` (`Store_ByItemOK`); final buy = **command 8**, dword 0, no detail. Exact bodies pinned in V120.
- **V122** [PROVEN wire+runtime, bounded]: after cmd6-ack + cmd8, ONE `UpdateAttrVital 0x309A` full ActorAttr with only cash `10000 -> 0` changed; HUD updated instantly and the store predicate re-read it (second Buy refused). Cash = ActorAttr qword `+0xA8`, mask bit `0x800` (V116).
- **Unresolved on purpose** (V121 audit): result 15 vs 17 (`ResetBuyItem`), UpdateAttr-vs-TradeItemResult ordering, full-Backpack-replacement semantics on purchase, server-owned identity/slot allocation, `ItemVaryAttr` body. No completed purchase exists anywhere in the corpus. Do not use `ItemOperateVitalRes` as a shop mutation carrier.
- **SPLIT-OPERATE-003** (`reports/PF_SPLIT_OPERATE003_VERB16_TWO_PANELS_STATIC_20260818.md`): inventory verb `0x16` -> op6 is reused across at least two panels (dispatcher `0x5A2A70` site `0x5A3532`; panel `0x5B9F70` site `0x5BA208`), both through the same numeric dialog helper `0x5A1630`; static caption route is evidence-closed (assets are `$pcz`-packed; and USE_DROP_SELL001 later showed the "dialog id 0x12" was an MSVC EH trylevel store, so there was never an id to map). Only remaining hop for a positive "split" label = live capture. `split_stack` stays `in_progress`.
- Server side today: v141 answers cmd6 with result 13 and journals cmd8 (no state change); buy-only, no sell branch; Foundation store implements none of it (coverage `shop_buy_sell` = `in_progress`, notes: "Nothing is implemented in the Foundation store").

---

## 4. SPAWN / DESPAWN TRANSPORT

### 4.1 Spawn -- proven end to end at the wire, and attended once

Carrier [PROVEN static Grade A + runtime-accepted]: `GSCN_RunTimeProtocolRes` id `0x6E9D` (=28317; name-hash re-derived AND observed live as the `ErrorData` code for malformed frames), v4, **derived change-mask bit `0x02` -> actor-entry collection at obj `+0x1C`** (`u16` count tag `0x12` + polymorphic entries; entry serializer `0x5E21D0`; emitters `v141.make_runtime_remote_actors` / `make_remote_actor_entry`). Inbound handler `0x5E4060` -> `0x446F30` (**one caller in the whole image, zero pointers**). Source: `reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md` (150-guard verifier).

Find-or-spawn semantics [PROVEN static]:
- unknown identity -> `0x446990` spawn via jump table on u8 `actor_type` at entry `+0x10`, **exactly cases 2..6, anything else silently dropped**:
  2 = `CNetActor` (remote player) . 3 = `CMyActor` (only if no local player) . 4 = `CNetNPC` . 5 = `CAvatarNPC` . 6 = `Pet`. Initial attrs applied through vtable `+0x10`, which can never reach the death chain (an actor cannot be born dead).
- known identity -> vtable `+0x20` = attr apply + dead-sync weld (`0x4446F0` -> `0x4437C0`).

HYP-PF-023 spawn-then-kill [PROVEN wire + dispatcher + attended render]: three `0x6E9D` frames for identity `0x2001` (actor_type 4, NPCAttr `0x0AD5` + MovementAttr `0x2067`; spawn HP 100 no bit `0x0080`; dying latch HP 0 timer 20.0f; death task HP 0 timer 0.0f; PCs 173/120/120 B, hash-pinned). GT-022 ran 3x on a real client 2026-08-19: wire held every time, NPC observed standing-then-flat, eyewitness photo retained (`pf_bridge/evidence_screens/biground7/gt022_r2_npc_corpse_panya_eyewitness_20260819_183537.png`). Caveats: which of the two kill frames produced the pose is UNATTRIBUTED (GT-025 latch-only queued); `_F_DIE_000` itself unobserved; and the "spawn" frame **updated an actor the client already draws from its own map data** -- the erratum withdrew "the NPC appears". Sources: `reports/PF_RUNTIMERES_ENCODER001_SPAWN_THEN_KILL_20260819.md` + ERRATUM 1; `docs/HYPOTHESIS_LEDGER.json` HYP-PF-023 (3 versions, budget full).

Whether a **novel identity at an arbitrary position visibly pops into existence** (what a loot drop needs) is therefore weaker than it looks: V89-V94 lanes and OBJECT-POP-002 rendered populations and membership changes at authentic placements, and remote-player probe HYP-PF-025 (actor_type 2 at offset positions, 5-frame sweep, headless-proven 162 guards) is **queued as GT-030, NOT RUN** -- "whether anything renders at all" is its open question. [PROVEN wire / render UNPROVEN for novel-position spawns]

Server-side spawn policy: none. Scene actors are static placements projected from the frozen hash-pinned `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` (115 rows) by `population.py` (nearest-20, identities `0x2000 + index + 1`); no spawn timer, no respawn cycle (coverage row verbatim). Only data lead in the decoded corpus: `INSTANCE` table (338 rows) carries "level, scene, lifetime, refresh and exit metadata" (V100 roadmap) -- unexplored. No decoded drop/loot table is named anywhere in the reports read. [NEGATIVE]

### 4.2 Despawn / actor-leaves -- the honest state

- **[PROVEN wire, runtime-observed once, emulator-era]** V91 (2026-08-14, `reports/PF_RE_V91_Runtime_and_V92_Authoritative_Membership_20260814.md`): after 20 actors appeared, a generation carrying only the 3 movers made **every omitted actor disappear from world view and radar**. Conclusion recorded: the RuntimeRes actor-entry list is **authoritative membership for that generation**, not a sparse delta. This is the ONLY observed actor-removal transport in the entire project.
- **[STATIC only, unexamined]** The client code that would do this is `0x446F30`'s second loop `0x446FE1..0x4470E5`, explicitly named "the reconcile/removal pass" and explicitly NOT examined (RUNTIMERES-ACTOR-ENTRY-001 "Explicitly not examined" list). Q2 of the chunk-2 findings adds that per-frame reconciliation happens against **the previous RuntimeRes frame's collection copy** (singleton `[0x01081A90]+0x154`), not against the actor registry.
- **[NEGATIVE]** No dedicated despawn/leave/exit vital has ever been decoded or captured. `DeleteActorVital 0x36DB` is a **character-select-stage delete, not a scene despawn** (DELETE-SOFT-002; readiness audit F7 says in as many words: "Do not reach for it as a 'player left' frame"). OBJECT-POP-002 logged zero `0x36DB` across 370 decoded structural lines and states it does not prove client-visible despawn for any particular omitted actor.
- **[TENSION, UNRESOLVED]** V91's authoritative-membership despawn vs the count-1 frames the HYP-PF-023/025 lanes send: if membership were strictly authoritative per frame, a count-1 death frame should wipe the rest of the visible population, and no such wipe was reported in GT-022 (nor asserted absent). Possible reconciliations (unproven): the removal pass diffs only against the previous frame's copy, or the 3-second population reapply masks any wipe. The remote-player report simply states "**No despawn exists on this lane** -- a probe stays until the client disconnects." A loot design that needs corpse removal or ground-object removal must first close this: (a) statically decode `0x446FE1..0x4470E5`, or (b) run a bounded membership-omission GT against a single known identity.
- Death does not remove: the HYP-PF-023 corpse stays flat indefinitely; no respawn/come-back-to-life encoder exists anywhere (HP-DEATH-001 negative, substring-guarded across the whole source tree).

---

## 5. THE GAP LIST -- "monster dies -> loot object appears -> pickup -> backpack row -> persists"

| # | hop | tag | source |
|---|---|---|---|
| 1 | Monster exists in scene (spawn transport) | **[PROVEN wire]** `0x6E9D` bit `0x02` actor_type 4; runtime-accepted V89-V94, OBJECT-POP-002, GT-022 | RUNTIMERES-ACTOR-ENTRY-001; OBJECT-POP-002 ledger row |
| 1b | Spawn timer / respawn cycle (server policy) | **[NO PATH KNOWN]** static placements only; only data lead = `INSTANCE` lifetime/refresh columns, unexplored | coverage row `monster_spawn_and_loot`; V100 roadmap |
| 2 | Monster dies visibly | **[PROVEN wire + attended render, bounded]** HYP-PF-023 3-frame sweep; corpse photographed; frame attribution + `_F_DIE_000` still open (GT-025) | RUNTIMERES-ENCODER-001 + ERRATUM 1 |
| 2b | Server decides the death (combat/damage/AI) | **[NO PATH KNOWN]** EA7D attack request direction only; zero authentic inbound combat-result frames in the whole corpus (SCENE-013 capability negative); scene actors never react (coverage `aggro` note) | SCENE-006..013 ledger rows |
| 3 | Corpse/actor removal after death | **[PROVEN wire once -- V91 membership omission]** + **[STATIC only]** removal pass `0x446FE1..0x4470E5` unexamined; no targeted single-actor despawn ever proven; membership-vs-count-1 tension open | V91 report; RUNTIMERES-ACTOR-ENTRY-001 s."not examined"; s.4.2 above |
| 4 | Loot object appears on the ground | **[NO PATH KNOWN]** actor-entry jump table is strictly 2..6 with no item/object case; client HAS registered classes `DropThingModule_Client` / `DropThingBoard` / `DropThingGameObj` but no transport, producer, or capture for any of them | RUNTIMERES-ACTOR-ENTRY-001 (jump table); USE_DROP_SELL001 s.7 nonclaim 3 |
| 5 | Player picks it up (request) | **[NO PATH KNOWN wire; name-grade lead]** `PickupTerrainThing` is a registered client class (registration `0xBEE5E5`); no serializer pinned, no capture, no server handler; derived id `0x4543` [DERIVED] | USE_DROP_SELL001 s.4.2; hash fn validated below |
| 6 | Client displays the new item (response consumer) | **[STATIC only, strong]** `0x4C13` v2 ItemBag delta handler clones incoming identity/template/quantity/slot into the slot widget with NO prestate/occupancy gate -- a never-before-seen identity is structurally displayable; UpdateAttr full-replacement is the other (riskier) carrier | ITEM-MOVE-CONSUMER-001 ledger row; V121 audit |
| 7 | Backpack row appears (item creation, server) | **[NO PATH KNOWN]** no INSERT of a new item row after creation anywhere in `src/`; identity/slot allocation policy explicitly unrecovered; schema itself would accept the row | FINDINGS_R21 A1; V121 audit; migration 003 |
| 8 | Persists across reconnect | **[PROVEN db, exact-state only]** V111 merged state survives reconnect byte-exact; every writer is exact-prestate-gated one-shot, so a generalized "grant item" persistence path must be new code following the merge lane's guarded pattern | ITEM-LIFECYCLE-001; FINDINGS_R21 A2 |

Cross-cutting constraint for hops 5-8: any new dispatch-path DB write must catch its own exceptions (merge-lane pattern, `runtime.py:164-174`) because dispatch is unguarded and an escaping exception stops the whole server (FINDINGS_R21 N1).

---

## 6. Identity/id space for a dropped-item actor

- **Actor-entry pipe has NO item/object actor_type.** The jump table at `0x4469BD` accepts exactly `2..6` (`add eax,-2; cmp eax,4; ja -> return NULL`, entry silently dropped): 2 = remote player `CNetActor` [PROVEN wire/dispatch, render pending GT-030], 3 = `CMyActor` (gated `[0x1032EC4]==0`), 4 = NPC `CNetNPC` [PROVEN runtime], 5 = `CAvatarNPC`, 6 = `Pet` (5 and 6 never exercised by any lane). A ground item cannot ride this pipe under any known type value. **[NEGATIVE for an item actor_type]**
- Ground items in the client are most plausibly the `DropThingGameObj` / `DropThingBoard` / `DropThingModule_Client` class family (names proven present in the 521-class registration table, USE_DROP_SELL001), i.e. a *different object family with its own unknown transport*, paired with `PickupTerrainThing` as the pickup request. Whether DropThing objects arrive via some undecoded `0x6E9D` sub-object (the unexamined derived bits `0x04`/`+0x24` and `0x08`/`+0x20`), via their own vital, or via scene data is **[UNKNOWN]**.
- Derived candidate ids, computed here with the project's proven name-hash `sum((i+1)*ord(c)) & 0xFFFF` (validated in the same run against four published ids: `ItemOperateVitalReq 0x4BED`, `ItemOperateVital 0x36FE`, `UseItemVital 0x1F4F`, `GSCN_RunTimeProtocolRes 0x6E9D` -- all matched): `PickupTerrainThing = 0x4543`, `DropThingModule_Client = 0x651A`, `DropThingBoard = 0x295E`, `DropThingGameObj = 0x3415`, `StallOperateVital = 0x3DE4`. [DERIVED -- ids only; registration proven for PickupTerrainThing and the Stall family; wire shapes NOT known.]
- Identity spaces already in use (for collision avoidance): local player `0x10010001`; scene NPCs `0x2000 + placement_index + 1` (`0x2001` probe, `0x201F` P30, `0x203D` P60, `0x205C` P91); remote-player probes `0x00A00001..3` (design choice, HYP-PF-025 refuses collisions with the other two bands by name). Backpack **item** identities are a separate per-character qword space (1,2,3,4 today; tree-keyed by identity). No identity convention for ground objects exists. **[UNKNOWN]**

---

## FILES TOUCHED

Read only (Windows paths under `C:\Users\Panya\Desktop\Pirate Force\`):
- `Pirate Force ServerProject\reports\PF_RE_V111_to_V115_Inventory_Monster_Shop_20260814.md`
- `Pirate Force ServerProject\reports\PF_RE_V100_Data_and_Attribute_Roadmap_20260814.md`
- `Pirate Force ServerProject\reports\PF_SPLIT_OPERATE003_VERB16_TWO_PANELS_STATIC_20260818.md`
- `pf_bridge\FINDINGS_R21_BACKPACK_WRITES_ARE_ONE_SHOT_AND_DISPATCH_IS_UNGUARDED.md`
- `Pirate Force ServerProject\docs\EXPERIMENT_LEDGER.md`
- `Pirate Force ServerProject\docs\FUNCTIONAL_COVERAGE.json` (inventory + world + shop + monster_spawn_and_loot rows)
- `Pirate Force ServerProject\docs\HYPOTHESIS_LEDGER.json` (HYP-PF-023 region)
- `Pirate Force ServerProject\reports\PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md`
- `Pirate Force ServerProject\reports\PF_RUNTIMERES_ENCODER001_SPAWN_THEN_KILL_20260819.md`
- `Pirate Force ServerProject\reports\PF_REMOTE_PLAYER_ENCODER001_ACTOR_TYPE_2_VISIBILITY_20260820.md`
- `Pirate Force ServerProject\reports\PF_USE_DROP_SELL001_ITEM_OPERATE_USE_DROP_SELL_STATIC_20260818.md`
- `Pirate Force ServerProject\reports\PF_RE_V116_to_V120_Cash_Monster_and_Shop_20260814.md`
- `Pirate Force ServerProject\reports\PF_RE_V121_to_V122_Final_Buy_Cash_Update_20260814.md`
- `Pirate Force ServerProject\reports\PF_OBJECT_POP002_AUTHORITATIVE_SCENE_ACTOR_RUNTIME_PASS_20260816.md`
- `Pirate Force ServerProject\reports\PF_RE_V91_Runtime_and_V92_Authoritative_Membership_20260814.md`
- `Pirate Force ServerProject\src\pirateforce_foundation\inventory.py`
- `Pirate Force ServerProject\src\pirateforce_foundation\store.py`
- `Pirate Force ServerProject\migrations\003_character_inventory.sql`
- `Pirate Force ServerProject\current\pf_login_game_server_v141.py` (constant table + ItemOperate builders, grep + bounded reads)
- greps across `reports/`, `docs/`, `drafts/`, `src/` for despawn/leave/0x6E9D/membership

Written (the single permitted output):
- `/sessions/friendly-dreamy-hopper/mnt/outputs/r100_agentC_inrepo_loot_spawn.md` (this file)

Not touched: `state/pirateforce.sqlite3` (never opened), no git mutation, no server boot, no UI, no LOCK_* files.
