# PF ground-drop lifetime and reconciliation

This is a deterministic, source-separated extension of `PF_GROUND_DROP_TRANSPORT.tsv`. `GDL-IMG-013` references canonical `GDT-IMG-002` and adds only a bounded direct-call negative; it does not duplicate the pickup producer claim. The separate canonical-reference row pins the two FightingDrop reflection findings.

- Image: `GameClient.local.bin`, 14759424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- ServerProject comparison snapshot: commit `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa` at `2026-09-01T07:50:38Z`; the five files used below are independently size/SHA-256/text pinned by this checker
- Rows: 29 (`IMAGE` 23; `DATA` 3; `CAPTURE` 3)
- TSV SHA-256: `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`
- Prior transport artifact SHA-256: `9e2396795ee32287f1f9b82f22fb8f394464d2b0a25375d07108ee138c73907b`
- Every row carries explicit `evidence_grade`, `measurement_label`, `method`, and `control` fields. IMAGE resolver rows `GDL-IMG-018`, `GDL-IMG-019`, and `GDL-IMG-022` are `[A][MEASURED]` static proofs with executable instruction/CFG/stack/IAT/vtable/RTTI controls. `GDL-IMG-020` and the normal-success ordering portion of `GDL-IMG-021` are `[A][MANUAL_BOUNDED]` over exact hash-pinned spans; `GDL-IMG-021` additionally contains mechanically parsed PE/CLI metadata and whole-image byte censuses. None is a runtime observation.

## Exact client contract from IMAGE

The concrete inbound surface is `GSCN_RunTimeProtocolRes` (`runtime ID 0x6E9D`). Its optional field `+0x20`, selected by outer presence-mask bit `0x08`, is a `TerrainThingPool*`. The handler passes that pointer through a typed bridge to `DropThingModule_Client::reconcile`.

The client owns live ground objects in the module map at `+0x18`, keyed by `TerrainThing+0x10` (`u32`). New keys allocate/register/insert a `DropThingGameObj`; matching keys update in place. Presentation resolves local game data using `TerrainThing+0x14` and the keys `s_NAME`, `n_DROPMODEL_TYPE`, `n_QUALITY`, and `s_TAG_EXTRA`. No literal item name or model filename is carried on this wire path.

### Exact model selector, resource gate, and nameboard order

IMAGE now closes the local selector chain. `n_DROPMODEL_TYPE` is accepted directly only in `0..12`; there is no subtraction or remap. It indexes this exact token table:

`0=item, 1=weapon, 2=armor, 3=fittings, 4=money, 5=buff, 6=pandora, 7=crystal_r, 8=crystal_b, 9=crystal_g, 10=DROP_ENERGY, 11=DROP_LIFE, 12=holloween01`.

The client composes `.\Data\GC\F\<token>.nif`, calls the resource-open and type-filter path, and stores the result at `DropThingGameObj+0x84`. **Type 0 is valid and requests `item.nif`; it does not mean “no model.”** If `+0x84` is `NULL`, initialization returns false before XYZ placement and before the nameboard block. If non-NULL, the client applies XYZ/activation first and only then builds the nameboard.

`GDL-IMG-017` owns that selector and hard-gate result. `GDL-IMG-018` proves the setter and callback route conditionally. `GDL-IMG-021` now provides the missing **normal successful static bootstrap** join: parsed PE/CLI metadata resolves entry token `0x060000BA` to `<Module>._WinMainCRTStartup`, mechanically asserted native calls reach application initialization, and manual bounded CFG review over the exact pinned spans finds its fall-through successful continuation installing callback `0x00B02300` before later application-object construction and the non-NULL return continuation. A whole-image file-backed byte census mechanically finds exactly three encoded absolute slot references—the dispatch and two setter writes—and exactly one direct `E8` caller of the setter. The ordering statement is hash-anchored manual review rather than a complete instruction-decoder CFG proof, and none of this is evidence that a particular process executed; computed/aliased/dynamic writes and abnormal/external entry remain outside the census. On the proved callback route, mode-0 `rb` tries a private-copy rewrite from `.nif` to `.ni_` first and falls back to `_fsopen` with the untouched original `.nif` only when the packaged branch returns `NULL`. Mechanically pinned stack dataflow shows `_splitpath_s`'s extension output passed as `_stricmp` string1 and literal `.nif` as string2; equality reaches the length-gated final-character rewrite.

The packaged reader requires `$pcz`, takes the declared output size from header `+4`, then passes five property bytes at `+8` and compressed payload at `+0x0D` to a nine-argument `LzmaDecode`-shaped core. Its second decoder Boolean is ignored before returning the allocated buffer, so later file-validity and NiStream parser checks remain essential. `0x00B1B6C0` then returns non-NULL only for the first qualifying parsed collection entry whose RTTI walks to `NiNode`.

**[MANUAL_BOUNDED][IMAGE A]** Semantic review of the exact hash-pinned loader, type-filter, and wrapper-retain acceptance spans found no explicit descendant or geometry-type predicate before retained success; this absence was not mechanically proved. Indirect predicates, helper side effects, or overlooked predicates within or beyond the named spans remain possible. The `NiNode` constructor does transiently zero its child-container fields, but parsing may subsequently populate them; this derivation proves no post-parse child count and does not claim that a successfully parsed asset can validly remain zero-child. **A non-null qualifying parsed collection entry whose RTTI walks to NiNode does not prove geometry or pixels.** Hidden/culling state, materials, textures, renderer submission, camera placement, and actual pixels remain outside this static ceiling. The fall effect at `+0x8C` and the `s_TAG_EXTRA` effect at `+0x88` are separate resources; an FX or label disappearing is not proof that the wrapper or model object was deleted.

`GDL-IMG-022` closes the next static object/scene join. The accepted `wrapper+0x84` candidate is stored through DropThingGameObj vslot `+0x28` and retained at base `+0x78`; world registration calls vslot `+0x10`, rejects a NULL root, then invokes DropThingGameObj vslot `+0x1C`. Its bind path validates the same root, walks the scene graph recursively using NiNode child count `+0xB6` and child array `+0xB0`, and reaches state-activation calls. Existing IMAGE rows independently show that omission/range/full-clear removal calls world unregister before map erase and that destruction releases the retained references. This establishes a static registered scene-graph lifecycle, not renderer/device/framebuffer submission or pixels.

### [CLIENT-OBSERVED][B, measured elsewhere] / [COMPOSITE][D] GT-045 inference

The previously recorded uninstrumented GT-045 client observation was a label/dust with no visible item model; this generator does not re-observe or re-grade its screen evidence. The cross-layer inference is conditional: **if** that observed label came from this exact IMAGE-proved nameboard block, then `+0x84` was non-NULL and held a qualifying parsed collection entry whose RTTI walked to `NiNode`. That `[D]` composition does not convert “no visible model” into an IMAGE fact and does not distinguish descendants, culling, materials/textures, renderer submission, or camera placement. Control missing from GT-045: same-run branch/memory telemetry at the loader, RTTI result, and wrapper field.

### Source-separated DATA audits and report-only composition

`GDL-DATA-001` reports only the raw table rows and values for an externally specified 43-ID audit set: partition `22:30`, `24:10`, `26:3`; `n_DROPMODEL_TYPE` histogram `0:11`, `1:12`, `2:10`, `3:8`, `10:1`, `11:1`. It does not state why those IDs were selected. `GDL-DATA-002` reports only existence, size, and SHA-256 for an externally specified 13-file `.ni_` audit set; it is not a complete directory census and makes no IMAGE-token claim.

**[MEASURED][DATA]** `GDL-DATA-003` adds a deterministic decompressor/parser census over exactly those pinned files: All 13 pinned $pcz files decode with their five-byte raw-LZMA1 properties to the pinned decoded size and SHA-256, then parse as Gamebryo 30.1.0.2 block streams with exact whole-file consumption. Each footer has root_count=1 and root_index=0, whose block type is NiNode. Following serialized NiNode/NiBillboardNode child references from that root reaches at least one exact NiMesh block in 13/13 files. Across the audited set the reachable census is NiNode=25, NiBillboardNode=4, NiMesh=34, NiPSMeshParticleSystem=2. Every one of the 34 root-reachable NiMesh blocks directly references exactly one NiMaterialProperty and one NiTexturingProperty. Each referenced texturing property's base descriptor links to an external NiSourceTexture whose string-table entry ends in .dds (34/34). This is serialized-file structure only. It does not prove a runtime open/decode/parse, instantiated geometry, renderer submission, or pixels.

**[COMPOSITE][D — SERVERPROJECT SNAPSHOT + DATA + IMAGE]** At pinned ServerProject commit `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa` (2026-09-01T07:50:38Z), the reconstructed code selects the 43 IDs and its `(table_code, low_id, drop_model_type)` projection is checked against the external DATA audit. Separately, case-insensitive composition of the 13 audited DATA filenames with the IMAGE token table covers the 13 token stems. IMAGE proves the packaged-first `.ni_` route and its normal-success static callback installation; **[MEASURED][DATA]** DATA proves that every audited serialized root graph reaches at least one exact `NiMesh`, and that all 34 reachable meshes carry exact material/texturing/base-source/external-DDS references. None of these joins is emitted inside a DATA row, and the composition still does not prove that a particular runtime request opened, decoded, parsed, instantiated, found or decoded a referenced DDS, submitted, or rendered a file.

The following table is explicitly **COMPOSITE: replacement scope at pinned ServerProject commit `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa` + DATA values + IMAGE selector**. It is not an original-server issuance claim.

| DATA type | IMAGE token | Requested path suffix | Count | Pinned-snapshot-scope full item IDs |
|---:|---|---|---:|---|
| 0 | `item` | `item.nif` | 11 | 2400519, 2400522, 2400525, 2406957, 2406958, 2406959, 2414034, 2414064, 2600091, 2600701, 2600751 |
| 1 | `weapon` | `weapon.nif` | 12 | 2200201, 2200222, 2200401, 2200422, 2200601, 2200622, 2200801, 2200822, 2201001, 2201022, 2201201, 2201222 |
| 2 | `armor` | `armor.nif` | 10 | 2204001, 2204026, 2204201, 2204226, 2204401, 2204426, 2204601, 2204621, 2204801, 2204821 |
| 3 | `fittings` | `fittings.nif` | 8 | 2205001, 2205020, 2205201, 2205220, 2205401, 2205420, 2205601, 2205620 |
| 10 | `DROP_ENERGY` | `DROP_ENERGY.nif` | 1 | 2400047 |
| 11 | `DROP_LIFE` | `DROP_LIFE.nif` | 1 | 2400046 |

Two earlier high-value corrections are now explicit: `2400046` resolves through `ITEM_CONSUMABLES n_ID=46` to type `11` (`DROP_LIFE.nif`), while `2400047` resolves through `ITEM_CONSUMABLES n_ID=47` to type `10` (`DROP_ENERGY.nif`). They are not `ITEM_MISC` type `9/0`.

## Reconciliation matrix

| Incoming `+0x20` state | Exact client consequence |
|---|---|
| field absent, pointer remains `NULL` | unregister and erase every current ground object |
| field present, non-NULL pool, count `0` | return without mutation; preserve every current object |
| field present, nonempty pool | update matching keys, create new keys, and remove current keys omitted from the snapshot |
| live object outside the proven 2500-unit predicate | removable unless the audited bypass flag applies |

Manual static inspection found no clock/time API reference, clock comparison, or elapsed-time delete predicate in the named typed codec/handler/bridge/initializer/update/destructor spans. This is a hash-anchored bounded IMAGE observation: the checker verifies every named span hash, but it does **not** automate the semantic timer/xref absence test. Opaque fields remain unknown, so this does **not** prove absence of a serialized TTL/timestamp field, an indirect consumer, another client subsystem, or original-server lifetime policy.

Canonical `GDT-IMG-002` owns the pickup key-copy/enqueue fact. The new bounded negative here says only that the audited producer subspan has no direct `E8` call to the three pinned unregister/erase functions; it does not exclude indirect/helper deletion or prove the complete pickup lifecycle. The action selector `0x5B` path independently changes label-node visibility without a direct known delete call in its audited spans.

## Reconstructed replacement-code snapshot — separate from IMAGE/DATA/CAPTURE

- **[RECONSTRUCTED POLICY — SNAPSHOT `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`]** immutable V141 `make_runtime_res_empty_exact` builds two zero masks, so its intended RuntimeRes extension mask is zero (`current/pf_login_game_server_v141.py:2182-2200`, SHA-256 `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`). This is not a CAPTURE fact and V141 must not be edited.
- **[RECONSTRUCTED POLICY — SNAPSHOT `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`]** the modular runtime owns exactly one `self.mob_loot_cell = DropLedgerCell()`; that cell locks mutations and lazily expires rows. `sustain_a_kill` composes the whole live ledger on a kill. Do not create a second heartbeat ledger (`runtime.py`, `mob_loot.py`, `mob_drop_presence.py` pinned by this checker).
- **[SNAPSHOT PIN REFRESH — NO CLIENT CLAIM]** relative to this artifact's immediately preceding runtime pin, commit `579a6bb49b896726c627c469136748affc387e17` added 32 logout-hypothesis lines to `runtime.py`; none touches the single `DropLedgerCell` ownership anchor or the pinned `mob_loot.py`/`mob_drop_presence.py` lifecycle anchors. At snapshot `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`, `mob_loot.py` still contains the exact `DropLedgerCell`, lock, lazy-sweep, and whole-ledger anchors used above, plus read-only `lifetime_seconds` and locked `time_left` accessors. This is a read-only ServerProject comparison, not original-client evidence.
- **[RECONSTRUCTED POLICY — SNAPSHOT `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`]** `field_drop_tables.py` selects exactly 43 item IDs and its `(table_code, low_id, drop_model_type)` projection matches every pinned DATA row. This is only the replacement scope at that snapshot; it is not proof that the original server issued exactly those 43 IDs.
- **[STALE SNAPSHOT WORDING FOUND READ-ONLY]** comments present in that pinned snapshot that say `n_DROPMODEL_TYPE` is “not the switch,” that nothing reads element `+0x14`, or that this roster contains 63 IDs are superseded by the exact IMAGE consumer and the 43-row audit/composition.
- **[RECONSTRUCTED POLICY — OPEN DESIGN AT SNAPSHOT `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`]** ledger mutation is atomic, but snapshot -> compose -> socket-send is not yet proven totally ordered against pickup, expiry, another kill, or heartbeat. A stale nonempty generation can resurrect a removed key; count-zero preserve alone can leave a lazily expired client object indefinitely.

## Compatible integration contract — PROPOSED, not an instruction to patch V141

1. Reuse the single existing `DropLedgerCell`; do not create a second owner.
2. At the authorized modular adapter seam, serialize kill/pickup/expiry state transition, generation identity, composition, and socket-send order so an older nonempty generation cannot be sent after a newer omission.
3. For ordinary keepalive while drops exist, use a present non-NULL zero-count pool as the no-op/preserve shape; this avoids repeated full-set timer resend and does not snapshot the ledger.
4. On kill, successful pickup, or expiry, publish one ordered nonempty authoritative full-live-set generation; omit removed keys and retain every survivor. If the live set becomes empty, publish one deliberate all-clear. Lazy expiry needs an event/publisher if no later gameplay event would otherwise send the omission.
5. Send the exact item ID and XYZ through the proven TerrainThing fields; do not add a guessed literal model filename or `n_ID_MODEL` wire field. **[MEASURED][DATA]** The audited packaged files already have a pinned serialized root/child/`NiMesh`/material/base-DDS-reference census. Diagnose a blank by recording the resolved DATA row/type/token, packaged-versus-loose branch, runtime decode/parser result, qualifying parsed collection entry and RTTI result, instantiated child/geometry identity, `wrapper+0x84`/retained `+0x78`, world registration, referenced-DDS existence/open/decode/bind state, culling, and renderer/device state separately.
6. Treat lifetime ownership as an explicit reconstruction policy until original-server evidence says more; the IMAGE negative above does not rule out opaque or indirect client lifetime inputs.

## CAPTURE observations (source kept separate)

The complete pinned-session census contains three server-labelled `MOB_LOOT_DROP` log entries. Each is followed by the first later 14-byte heartbeat log at 1907 ms, 719 ms, and 99 ms; the primary console labels those heartbeats `exact empty RuntimeRes v4`. CAPTURE proves only logged ordering/timing/size/labels and send-side completion context. It does **not** expose/decode heartbeat bytes or prove mask zero, client delivery, client decode, memory mutation, or screen effect.

### Composite inference — IMAGE + pinned V141 replacement code + CAPTURE

CAPTURE establishes that the send-side logs recorded a 14-byte heartbeat after all three drops. The hash-pinned V141 replacement code at ServerProject snapshot `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa` establishes that its builder intends that heartbeat to carry extension mask zero. IMAGE establishes the conditional consequence: if those same bytes are delivered and decoded by the same-build `GSCN_RunTimeProtocolRes` path, absent bit `0x08` leaves `+0x20` NULL and the reconciler clears all current ground objects. This strongly identifies a dangerous shape, but it is not proof of delivery, decode, memory mutation, the screen event, or absence of every other lifetime mechanism.

Capture pins:

- `GAME_LIVE.txt`: 247711 bytes / 2958 lines / SHA-256 `ded232875f237e154b2c1ad9b3bab152b3aeb657728bd2da347cdd102cba110c`
- `server_console_live.out.txt`: 2467886 bytes / 32260 lines / SHA-256 `a2544e736dc7ba6f8ab132d30d270c13acca71e6f61a4c615643dc8c17fa17bb`
- canonical attended note: 15215 bytes / SHA-256 `042462792ee7477ccd22ba45964d53fd3b54b21d598772c2d6b32850dd5c1d1e`

## FightingDrop classification

`FightingDropModule_Client` and `FightingDropNotify` remain custom-reflection-only findings in `PF_GROUND_DROP_TRANSPORT.tsv` (`GDT-IMG-008`, `GDT-IMG-009`). They are a false lead for this concrete typed inbound path: the exact path selects `GSCN_RunTimeProtocolRes+0x20 TerrainThingPool`. This does not claim the FightingDrop classes are globally unused.

## Provenance and nonclaims

- Every TSV row has exactly one source label: `IMAGE`, `DATA`, or `CAPTURE`; no row mixes evidence layers.
- `semantic_fingerprint` excludes `evidence_id`; generation fails on duplicate claim semantics and self-checks that renaming an ID cannot change the fingerprint.
- No packet, dump, capture, or image raw bytes are copied into either output artifact.
- No client, server, dump, or capture was executed; all inputs were read-only.
- **[MEASURED][DATA]** The 13 explicitly pinned packaged assets were decoded in memory and structurally parsed; outputs contain only audited asset filenames, sizes, hashes, block/root indexes, type names, `.dds` suffix classification, and counts—never proprietary raw bytes or referenced texture names.
- **[MEASURED][DATA]** Serialized root-reachable `NiMesh` and material/texturing/base-source references do not prove referenced-DDS existence, runtime decode/binding, instantiated geometry, renderer submission, or pixels. Likewise, a non-null qualifying parsed collection entry whose RTTI walks to `NiNode` does not by itself prove geometry or pixels.
- No original-server policy is inferred from the emulator's event label `MOB_LOOT_DROP`.
- The five-file ServerProject snapshot at commit `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa` is verified by hash/text pins but is not emitted as an IMAGE/DATA/CAPTURE TSV row and is never original evidence; later commits are outside this artifact until explicitly re-pinned.
- `current/pf_login_game_server_v141.py` is immutable; the proposal leaves the authorized modular publication seam as an explicit design/implementation task for chief/COO.
- Files under `pf_bridge/external` are local-only/Git-ignored by workspace policy; another clone will not receive this trio until owner-approved packaging. This checker does not modify Git.
- `--check` is read-only: it creates neither the output lock nor temporary/output files. It verifies the script's TSV/MD and pinned inputs only; it does not validate append-only notes in `notes_to_chief`. Generation mode alone takes the exclusive output lock.
- Re-run with `py -3 -B pf_rederive_ground_drop_lifetime.py --check` to verify exact outputs and all pinned inputs.
