# PF Quest-Mark Lifecycle

Pair ID: `455c1aaca750b729dc24f10d67e702dbda62884219f1d87c03621a1f66558992`

## Result

`[MEASURED][IMAGE]` This source-separated static artifact closes the measured `QuestIconBoard` mechanics from pooled wrapper creation through CNetNPC ownership, typed update gating, global root-manager admission/withdrawal boundaries, owner and board destruction, and the inherited submission call. It contains **17 rows**, all `source=IMAGE`; no DUMP, CAPTURE, or DATA fact is mixed into any row.

The static render ceiling is exact but narrow: `QML-IMG-016` reaches the board's gated virtual submission, and `QML-IMG-017` reaches global manager call `0x00A9E6C0`. This does **not** prove final renderer/GPU execution or visible pixels.

## Lifecycle flow

1. `QML-IMG-001` seeds CNetNPC with no board and selector-cache byte 9.
2. `QML-IMG-002`/`003` acquire or allocate a 0x34-byte pool object and construct the typed board wrapper.
3. `QML-IMG-004` fixes the typed dispatch table. `QML-IMG-005` installs the refcounted board at CNetNPC +0x360 and invokes model init.
4. Selector cache/lookup, the 1000 ms QuestNPCModule refresh, and selector effects remain canonical in `PF_ATTR_QUEST_MARK_SELECTOR.tsv` and are cited below rather than copied.
5. `QML-IMG-006`/`007` carry the per-CNetNPC update through null gates, root bit-0 eligibility, spatial forwarding, and board update dispatch.
6. `QML-IMG-008`/`009` reach the measured manager-admission boundary. The engine name of the callback that triggers it remains OPEN.
7. `QML-IMG-010`/`011` reach the measured manager-withdrawal boundary; `QML-IMG-012` then transfers or releases/clears the owner reference according to an opaque global-mode branch.
8. `QML-IMG-013`/`014`/`015` establish owner, derived-board, and base-board destruction ordering.
9. `QML-IMG-016`/`017` establish a byte-gated submission call and the final static boundary reached in this artifact.

## Requested-surface coverage

| Surface | Status | Authority |
|---|---|---|
| creation | CLOSED for static pool/constructor mechanics | `QML-IMG-002..004` |
| attach/bind | CLOSED to refcounted owner install and model-init dispatch; runtime bind result OPEN | `QML-IMG-005`; `PF_QUEST_MARK_RESOURCE_RESOLVER.tsv` route key `79839063b5f2dad4f09c2c9022857ca6842763281547d762147f6939ccbb77cb` |
| cache/lookup | CLOSED by canonical reference, not duplicated | `PF_ATTR_QUEST_MARK_SELECTOR.tsv` SHA-256 `3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0` |
| refresh/timer | CLOSED for the canonical static 1000 ms path by reference; runtime cadence OPEN | selector support keys `QuestNPCModule_refresh` and `QuestNPCModule_timer` |
| per-object update | CLOSED to board dispatch | `QML-IMG-006..007`, `QML-IMG-016` |
| visibility gate | CLOSED only as measured root +0x18 bit-0 update eligibility; pixel visibility OPEN | `QML-IMG-007..009` plus selector reference |
| removal/unregister | CLOSED to manager-container withdrawal and owner clear/transfer | `QML-IMG-010..013` |
| scene/generation transition | measured root-manager effects CLOSED; scene/generation trigger identity OPEN | `QML-IMG-008..012` |
| destruction | CLOSED for measured derived/base release order | `QML-IMG-013..015` |
| render submission | CLOSED to `0x00A9E6C0`; final renderer/GPU/pixels OPEN | `QML-IMG-016..017` |

## Evidence rows

| ID | Lifecycle stage | Status | VA span | Span SHA-256 |
|---|---|---|---|---|
| QML-IMG-001 | OWNER_INITIAL_STATE | PROVEN_EXACT | 0x0045CC46..0x0045CCBC | d4ab65efec8b1ce51300eb86891c0c63b5bc3fa4ef3d83ae2d135959616493cf |
| QML-IMG-002 | CREATION_POOL_ACQUIRE | PROVEN_EXACT | 0x0045C740..0x0045C84B | 4fa5650c70976b02eaf327df857c7a002de2b1583c3905abf7f210112aadf8a9 |
| QML-IMG-003 | CREATION_CONSTRUCTOR | PROVEN_EXACT | 0x0045B9E0..0x0045BA29 | 14a7809766fbaa343ced9d11d7c3b3e24ad6133c64188094d43bb14d811c3703 |
| QML-IMG-004 | TYPE_AND_DISPATCH | PROVEN_EXACT | 0x00F0DEE4..0x00F0DF10 | 79a1fb8920895dc1003535e7de437efed33cd9b5fb60343087d28854e78628d6 |
| QML-IMG-005 | ATTACH_AND_BIND | PROVEN_EXACT | 0x0045D430..0x0045D471 | 298c8c31efc2fb052c5be6c35b57b4bb71fd04d8e2d663aca847bace92ea2f29 |
| QML-IMG-006 | PER_NPC_UPDATE_ENTRY | PROVEN_EXACT | 0x0045C500..0x0045C52C | 11d7f2a6cc9b38bcd175b7d5d4acaec1768c7148f85e4d9b38adcecbed331c62 |
| QML-IMG-007 | VISIBILITY_GATE_AND_SPATIAL_UPDATE | PROVEN_EXACT | 0x0045BB90..0x0045BC7A | 743790a6cee4f19b9dfaa9f484d4a5cca403b2674c0b6fdf4be6b55e3f84786e |
| QML-IMG-008 | ROOT_MANAGER_TRANSITION_CALLBACK | PROVEN_EFFECT_TRIGGER_OPEN | 0x0045CDB2..0x0045CDF2 | 2fcbd5cf8b7886228aa6bf36755789ba166f698c11b830a934480f7ea0a30c24 |
| QML-IMG-009 | ROOT_MANAGER_ADMISSION | PROVEN_TO_CONTAINER_BOUNDARY | 0x00B0E9A0..0x00B0EAA9 | c4592d7a252b213f0cb1d4f16813158327d1681fb418173c329fbe2940f9b455 |
| QML-IMG-010 | REMOVAL_FORWARDER | PROVEN_EXACT | 0x005BB150..0x005BB16C | b180fe92a5592b8b39a34908a42c5c7ef9b7e58dc494b3047d26d63520e34d8e |
| QML-IMG-011 | ROOT_MANAGER_WITHDRAWAL | PROVEN_TO_CONTAINER_BOUNDARY | 0x00B0F030..0x00B0F0B1 | d2799c04f86419c0c6e391ee71c7e30c1b8d11e4d444b134bd3356999dd692cc |
| QML-IMG-012 | OWNER_DETACH_OR_TRANSFER | PROVEN_EXACT_BRANCH_EFFECTS | 0x0045CEC0..0x0045CF57 | d0c5b310d9a5750cfc10f651caf46105a3d0da16456256032fc812f4024eae5d |
| QML-IMG-013 | OWNER_DESTRUCTION | PROVEN_EXACT | 0x0045CF60..0x0045CFF5 | 51485167a43478715b8b893fb7d711409300ea2d3eb93e95a96aa20b08cdbedc |
| QML-IMG-014 | BOARD_DERIVED_DESTRUCTION | PROVEN_EXACT | 0x0045BAD0..0x0045BB32 | 1e9e87d04bf0e662ae433d93f35a89b70d207c762fc690617fb42684840454a2 |
| QML-IMG-015 | BOARD_BASE_DESTRUCTION | PROVEN_EXACT | 0x005BAFE0..0x005BB146 | 0e4b9970c38d994640cdd8c113df5ed3017494eb330970e47b029e094a029493 |
| QML-IMG-016 | UPDATE_TO_SUBMISSION_DISPATCH | PROVEN_EXACT | 0x005BAC80..0x005BAC9D | 520f5eb44d9ee85e2f4c51061ec59130459e125e2ea7c5394eb292e3bca10eab |
| QML-IMG-017 | RENDER_SUBMISSION_CEILING | PROVEN_TO_SUBMISSION_BOUNDARY | 0x005BB170..0x005BB1C4 | ba3236aa8ec56e5a48896b70a1c6d5974ecad6224ed7832ca1aa02e8163f628b |

Evidence-key ordered-set SHA-256: `2ae0f8db37defcbfa15cf5be19aff7e7fbef477d6b399be0a7dcb26155951244`.

## Canonical selector references

The selector artifact is mandatory and pinned at SHA-256 `3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0`. Its 10 ordered `selector_key`/`evidence_key` pairs hash to `a1b636459217b7ff720be475e5dfb4a1d63b2e12816b4bd1c3a213fbc401cd48`. These keys are citations only; their selector conditions, event writer path, model-init body, and texture-routing claims are not republished as lifecycle evidence.

| # | selector_key | evidence_key |
|---:|---|---|
| 1 | `0d30ed3bfb692635a8367af8472e5f7309315766daca725460fc322dca5fcd3f` | `664c81eb05a59bb0661d3390d9f08a7c4f7401360e4bf3840678e4fa10a6f515` |
| 2 | `5464435ef50cdb99c6bdae1894455461970957c2294f7d1b23e7f12b1ab11439` | `43c0f31d521b1e3e8126f272bef7652b596f133bb50e7c070505860727e4f582` |
| 3 | `9eefcfa3f4c47b1c8aec68e788ec30b3e71cb7547953e905f602125738b74ea3` | `81df723f5fe9e1e5fd99b71092f13cc66e39e230e87b20c80e6ca24d1b670f61` |
| 4 | `8e0a307d7d14bbd2a66916938320d9e2b4ed96d57e81e538a723137268663ede` | `f956d7f3a3718008ee17893c5d1ce9a8fe4da065091d82da38ba9f75224f2635` |
| 5 | `ce7016e63d533dd7ac87809df14e1cc8aa2e727178b8c1f6180e970551d83b13` | `e708724848d2f8a19b73a460df044a75d4e80a3655b51ad4969f2c2d6fec211d` |
| 6 | `a23f05a8298f622f2942b57f14d26f8ed8c6e61af066157b0f6b538415edf43e` | `f1ac606313187059e89f403fbb3cc58018d26eb91d95d5e8e6d0d9eff691cbf9` |
| 7 | `68c906aabaca780c17e7d796e56d965ad34a2c09debbc5cd53d38a6bbf9cea05` | `cdd4087ccccaed21693b68865c37c9241b5320843fb20fc0e9d7ee33afd88aa4` |
| 8 | `719515671edf8347af6ced4ca86a7ec94c9aa29ef0f502fa4d8a609507023bd2` | `d84ad8e45794ecad59c855239a03f8954edfec285bc448c8c7c1f58dc6cc9872` |
| 9 | `2e2a66518ed5fab2335da6e58e8e98b361edbc21610d05336816c76e080e1e4a` | `503bae7ab8c6535a0fb6ba10efb245957f4d4ab1b87a1560b793953eab983fbe` |
| 10 | `8fd8a88db8a6dbe8dd412ec093faca965aaa240f4427b4096e071b6e9ad81807` | `69316df73e2d68e95c1edcf9163364c5df93950f20086deddef614c178623bd2` |

## Canonical resource-route reference

`PF_QUEST_MARK_RESOURCE_RESOLVER.tsv` is pinned at SHA-256 `de491977008f1b3a0ab75da4a45bbba9cd35504350ecfbff95cfbec69a8641ab`; its paired Markdown is pinned at SHA-256 `f39f41cc91a5f6a7f1748933853e7d7ef0db393008588abf6fa73927421b71cc`, pair `c9c9e96ee67762cdaab18bf12d6cf22c1a4cf82c83270f50562a849c90985304`. This lifecycle artifact cites only the canonical IMAGE route-bound `resolver_key` `79839063b5f2dad4f09c2c9022857ca6842763281547d762147f6939ccbb77cb`. Its status is preserved exactly as `BOUNDED_OPEN_RUNTIME`: runtime open, bind, and pixels all remain OPEN. No resource row, DATA control, decoded structure, or resolver claim is copied into this lifecycle table.

## Canonical event-lifetime references

`PF_QUEST_MARK_EVENT_CENSUS.tsv` is pinned at SHA-256 `40127e6410c1aa6405efada640c60b72663eb9e35537c8011cdeede47d0a0b35`, pair `6a513a67f9e349150933fccf2ea7468538332b3f2553d0a6e8b0206475376dd3`. The 12 lifecycle-relevant `event_key`/`evidence_key` citations hash to `81e85bd46d3fed51e914c49b62a28f5f11a591b356c41c9e22a0090df426922a`. They cover the module-local synchronous stack-event lifetime, CNetNPC binding, direct registration and vtable binding, result overwrite/order, manager uniqueness/unregister, and numeric-kind reuse controls. Their event spans and claims are not copied into this lifecycle table.

| event_key | evidence_key |
|---|---|
| `QME-IMG-002` | `6f02802cc1a27963b05fa99bdd728d5aeb9d62123f4127f63b25595891aaf514` |
| `QME-IMG-003` | `c3b5362cd18c56d8f81aa2d55125cfdafccda82ac6d7750dbcf7865eb17da44b` |
| `QME-IMG-005` | `7ac26b8ad88f926cf2cf3d50d935edd61ac7e44cfeb75dd12601386ef3d7f6dd` |
| `QME-IMG-006` | `5bd7beeb2d75b7e2fe4cf70be660f0bdb37ce5eb6067456c7464de959e6723a1` |
| `QME-IMG-007` | `aeb9b33c61c0dfdb02c624271d203c41cae68ca87b75185609eafdce6b5088f2` |
| `QME-IMG-009` | `b09bdbbd6d4f3950289ddda24db1a0c614a2afc37ddc825395f64132b1ca4dc6` |
| `QME-IMG-010` | `e02f04f5c635f95d9949b13e5bd7041f6e28ff7c1712ac18fe302296d35abc9c` |
| `QME-IMG-015` | `567860bdeff1e1b557f947b0b0ef0dad873f2599a0137e3e386a19b5ba90ceef` |
| `QME-IMG-016` | `3bec0468cf60ef54ac95da9ca8679eed0eb99d9d4464cad28d69fd1e4d25fdb4` |
| `QME-IMG-017` | `8be3f62040f283114adc9cbffad880b30f7400e855ca2b2dce2e3df4b0b74da1` |
| `QME-IMG-018` | `f03ad0a59d548d4e314cc116a7d19b4b377b4dd9edb55484a639a76a06003838` |
| `QME-IMG-020` | `993dde804583a012fc0a24ba92dad7ccf51a4c9e4c95f80233d435fe49129a1f` |

The event artifact's exact ceiling is preserved: the stack event lives across the synchronous dispatch and is destroyed on both measured branches; listener lifetime is proven only through manager add/remove. Runtime reentrancy and abnormal teardown remain OPEN.

## Event-kind reuse safety

Numeric event kind `0x0A` is **not** named globally as quest here. `PF_QUEST_MARK_EVENT_CENSUS.tsv` keys `QME-IMG-017`, `QME-IMG-018`, and `QME-IMG-020` preserve the separate general-channel/reuse control. `PF_GROUND_DROP_LIFETIME.tsv` SHA-256 `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`, row `GDL-IMG-015`, evidence key `b014e9c7797a1d24b5c13eef598b7374223af5b548fe3efda538a43cd65a7d09`, independently proves a separate `DropThingModule_Client` callback using the same numeric kind and explicitly declines a gameplay-wide name. Numeric reuse therefore does not join the DropThing and typed CNetNPC/QuestIconBoard lifecycles.

## Method and ceiling

- Image guard: size `14759424` and SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- Every evidence span is mapped from VA through the PE section table and re-hashed.
- Typed dispatch is pinned by the 11 dwords at vtable `0x00F0DEE4`.
- Declared direct-call controls use a raw `E8 rel32` census over executable PE section file ranges. That census proves only exact direct-encoding hits for the named targets; it is not a whole-program absence proof and says nothing about indirect calls, tail jumps, imports, callbacks, or self-modifying/runtime code.
- No raw image, dump, or capture bytes are emitted.
- Publication takes an exclusive transient `O_EXCL` lock, stages and fsyncs both products, then replaces the pair while holding the lock. `--check` creates no lock, temporary file, output, or metadata sidecar; it rejects an active publisher, verifies stable size/mtime/content reads plus the shared pair ID, and compares exact regenerated bytes.

## Remaining blockers

- `[OPEN][IMAGE]` The original engine name and trigger semantics of the CNetNPC vtable +0x58 callback are not recovered.
- `[OPEN][IMAGE]` Root +0x18 bit 0 is proven as an update gate and written by measured paths, but this artifact does not rename it visible/hidden.
- `[OPEN][IMAGE]` The full producer census for setting base-board byte +0x28 true is outside this bounded lane.
- `[OPEN][IMAGE]` Resource open/decode/bind/pixel outcomes remain delegated to `PF_QUEST_MARK_RESOURCE_RESOLVER.tsv` key `79839063b5f2dad4f09c2c9022857ca6842763281547d762147f6939ccbb77cb` and remain OPEN there.
- `[OPEN][CAPTURE]` Actual quest-mark presentation, transition timing, and removal timing require source-separated client-observable evidence.
- `[OPEN][IMAGE]` The final renderer/GPU path after `0x00A9E6C0` is not traversed.
- `[OPEN][CAPTURE]` Event reentrancy and abnormal listener teardown are not measured by the static event census.

## Delivery boundary

`pf_bridge/external` is outside the canonical `Pirate Force ServerProject` Git worktree. These files are local-only and untracked there; another clone or executor needs owner-approved packaging or ingest. This is not described as a Git-ignore policy.
