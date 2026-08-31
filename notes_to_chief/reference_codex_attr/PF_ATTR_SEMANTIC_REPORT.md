# PF Attr semantic report - active checkpoint

[MEASURED] Method: exact IMAGE codec/support-span hashes plus frozen-row selector partitions; control: fixed IMAGE SHA-256 and exact row/action censuses. TSV row status/evidence is authoritative over prose.

A published checkpoint is authoritative only through `PF_ATTR_GENERATION_MANIFEST.json`; consumers must resolve its content-addressed verified generation directory and parse the exact bytes whose hashes were verified. Top-level files are compatibility materializations, not a cross-file atomicity guarantee.

This is an additive read-only checkpoint, not the final version. The server/emulator is not evidence; all claims below originate from the original IMAGE or DATA layer named in the TSV rows.

`PF_ATTR_SEMANTIC_DELTA.tsv` is a true directional-field semantic/scope delta against pinned generation `1165903103511ed93a833ab3a0368f430fd1986f97ec543754f11ec139d13537` (manifest SHA-256 `c04c76619f69954b8491e8cf92385b2bbb1cf200c422167aea33befe8860cc6c`). It contains semantic-name/status changes, explicit `applies_to_class` corrections, and newly proved class-scoped rows; `PF_ATTR_FIELD_SEMANTICS.tsv` remains the cumulative active coverage table.

- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Field rows: 490
- Priority-0 gameplay fields: 28 structural; 30 class-scoped claims
- Priority-0 `PROVEN_EXACT`: 20
- Priority-0 `PROVEN_ROLE_ONLY`: 7
- Priority-0 `PARTIAL`: 0
- Priority-0 `UNKNOWN`: 3
- Semantic-delta rows: 300 (`IMAGE` 300; `DATA` 0)
- Delta by family (directional scoped rows): ActorAttr 42; ActorGatheringInfoAttr 2; ActorTreasureHuntExcavatingInfoAttr 2; AvatarAttr 40; BackpackAttr 2; BasicAttr 18; CAchievementsAttr.ListChild 8; CAchievementsAttr.TreeChild 6; CCooldownAttr 4; CGuildStorageAttr 2; CSkillAttr 6; CVehicleAttr 14; CollectionBagAttr 2; DailyQuestAttr.RecordNode 4; ExpressBagAttr 2; InstanceRefreshAttr 4; ItemAttr 34; ItemBagAttr 8; ItemBagAttr_Equiped 2; ItemMallBagAttr 2; ItemVaryAttr 6; MovementAttr 18; NPCAttr 16; NavigationExAttr 6; PetAttr 16; QuestMiscAttr.QuestMiscData 10; StallActorAttr 4; StorageAttr 2; SummonedPetAttr 10; SystemGiftAttr.SystemGift 6; UnlimitBagAttr 2
- Existing-row transitions: PARTIAL->PARTIAL 10; PARTIAL->EXACT 10; PARTIAL->ROLE 4; PARTIAL->UNKNOWN 6; EXACT->EXACT 110; ROLE->PARTIAL 2; ROLE->EXACT 16; ROLE->ROLE 80; UNKNOWN->ROLE 30; UNKNOWN->UNKNOWN 16; new rows 16 (BasicAttr exact 8; ActorAttr exact 2 and role-only 2; CVehicleAttr role-only scope-open 2; NPCAttr exact CNetNPC-scoped 2). The 24 added same-status transitions are fail-closed scope corrections for ItemAttr base, ItemBagAttr, and ItemVaryAttr count rows.
- Unified unresolved work ledger: 976 rows = 464 active claim rows + 512 standalone conflict work items; standalone conflict rows are work items, not UNKNOWN fields.
- Active field-direction claims withheld: 390 = 373 with semantic and/or scope open + 17 exact-semantic/exact-scope claims held only by OPEN conflict.
- Other active claim work: non-wire runtime rows 7; container concepts 32; class-link/codec/closure rows 27; combat-lifecycle semantic/order rows 8.
- OPEN conflicts represented exactly once in the unified ledger: 640 = rederived-IMAGE 616; measured-NOT_WIRE-needed 17; cross-source 2; runnable-server-code semantic 5.
- All conflict rows: 1285; OPEN 640; non-OPEN 645.
- Class-level open work: 0 paired codecs need first field decode; 0 already-enumerated codecs need deduplicated active IMAGE/semantic rederivation; 10 classes need getter/vtable recovery
- Selector evidence quarantined without suppressing field/server guidance: 0
- Open empty-codec/legacy-row closure conflicts needing measured NOT_WIRE corrections: 17
- Field status rows: exact 231; role-only 190; partial 27; unknown 42
- Field concrete-scope rows: exact 280; unknown 210
- Non-wire runtime/state rows: 13 (exact 6; role-only 6; unknown 1); Fight exact client-computed formulas: 29; 21 exact getter-to-widget-offset bindings; Activity adds 4 exact literal-control-to-object-slot bindings
- NPC/player primary-name selector paths: 14 valid IMAGE rows; 0 selector rows quarantined. Two local-CMyActor paths prove controller `0x00F2CD08`/child `+0x54`, three typed-CNetNPC paths prove `0x00F2CD48`/child `+0x50`, and nine untyped paths retain the exact dynamic union `+0x54_or_+0x50` without inferring class from identity sign.
- Combined UpdateAttr/Express-Get/Daily-Reward/CBuff/object-world/Pet/Activity container concepts: 68 (exact 39; role-only 16; partial 2; unknown 10; not-wire 1)
- Container concrete-scope rows: exact 44; unknown 24
- Source-separated binding rows: DATA 77 (exact 70; role-only 7); IMAGE loader mappings 1
- Combat lifecycle: 34 source-separated rows (`IMAGE` 26; `DATA` 8). Actor preexistence before lethal actor-entry dead-sync is exact; CHitResult-versus-HP arrival order, original-server cadence/death hold, exact equipment-dependent behavior selection, and original-server acknowledgement remain open. See `PF_COMBAT_LIFECYCLE.tsv`/`.md`.
- Frozen/re-derived conflict rows: 1285
- Approved attended probe requests: 0. `APPROVED_PROBE_REQUEST_SPECS` is empty, so no proposal has passed the fail-closed owner intake contract (linked unresolved key, exact commands, expected and falsifying observations, unlock, headless evidence, and prior-probe search). Zero probes does not mean zero unresolved work.

## Exact Priority-0 semantics (scope shown; not all class-safe)

- `ActorAttr 0x104`: `age_text` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x120`: `constellation_text` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x13E`: `CGCPotionModule_thousand_quotient_positive_flag_and_mod1000_value_u16` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x148`: `second_password_account_md5_upper_hex` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x164`: `NameBoard_Player_LABEL_GUILD_text` (`applies_to_class=CNetActor`; scope `PROVEN_EXACT`)
- `ActorAttr 0x190`: `target_panel_friend_actor_id` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x198`: `target_panel_enemy_actor_id` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x1A0`: `Navy_Pirate_icon_selector` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x1A8`: `GetBoatHealth_current` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x1AC`: `GetBoatHealth_max` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x1B2`: `SELL_STALL_BASIC_addend_u8` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0x78`: `GetPpClass_value` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `ActorAttr 0xE8`: `residence_location_text` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_ActorAttr`; scope `UNKNOWN`)
- `BasicAttr 0x28`: `NameBoard_Player_LABEL_NAME_text` (`applies_to_class=CNetActor`; scope `PROVEN_EXACT`)
- `BasicAttr 0x28`: `NameBoard_Player_LABEL_NAME_text` (`applies_to_class=CNetNPC`; scope `PROVEN_EXACT`)
- `BasicAttr 0x54`: `FightAttr_run_speed_formula_input` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_BasicAttr__consumer_0x00467E60`; scope `UNKNOWN`)
- `BasicAttr 0x54`: `MOBS.n_SPEED_WALK_to_initial_visual_horizontal_locomotion_scalar` (`applies_to_class=CNetNPC`; scope `PROVEN_EXACT`)
- `BasicAttr 0x5C`: `scene_id__SCENE_NAME.n_ID` (`applies_to_class=UNKNOWN_CONCRETE_OWNER_OF_BasicAttr`; scope `UNKNOWN`)
- `BasicAttr 0x68`: `CNetNPC.template.n_FACTION` (`applies_to_class=CNetNPC`; scope `PROVEN_EXACT`)
- `BasicAttr 0x6C`: `CNetNPC.template.n_ENEMY` (`applies_to_class=CNetNPC`; scope `PROVEN_EXACT`)

## Priority-0 meanings still unknown

The following fields have exact wire structure/defaults but no unique gameplay-semantic binding:

`ActorAttr 0x13C` (UNKNOWN), `ActorAttr 0x1A4` (UNKNOWN), `ActorAttr 0x94` (UNKNOWN).

The scoped search result is not an absolute no-use claim; retained aliases, member-internal offsets, and generic virtual consumers remain possible.

ActorAttr +0x148 is the 32-character uppercase hexadecimal result of `MD5(second_password_narrow_bytes || login_account_narrow_bytes)`. IMAGE proves the local producer, request +0xFC codec, transfer into ActorAttr +0x148, and ActorAttr codec. It does not prove raw-password storage, password-only MD5, cryptographic security, original-server verification/storage policy, or that every inbound value was locally produced.

ActorAttr +0x190/+0x198 are exact FRIEND/ENEMY target-panel actor IDs. They are direct ActorAttr members on one typed branch; NPCAttr +0xA0/+0xA8 are the alternate typed branch. ActorAttr +0x198 drives the ENEMY target-panel resolver but is not a direct input to the separate `HP_ENEMY` evaluator, which reads NPCAttr +0xA8.

## Expanded character/world Attr families

- `MovementAttr`: 10 unique wire fields; exact 8, role-only 0, partial 2, unknown 0; scope-open directional rows 18.
- `AvatarAttr`: 22 unique wire fields; exact 18, role-only 3, partial 1, unknown 0; scope-open directional rows 40.
- `NPCAttr`: 8 unique wire fields; exact 6, role-only 1, partial 1, unknown 0; scope-open directional rows 14.

MovementAttr now has ten direct fields (20 directional rows) plus the canonical inherited DBAttribute prefix. World X/Y/Z, yaw, horizontal scalar, vertical velocity/launch value, and heading are exact. +0x38 is a uint8 movement-update mode carried into CActorTask_ActorMove +0x50: zero/nonzero select different bounded update branches, but both branches can converge on immediate application or task creation depending on later position/state gates. Enum labels and the complete domain remain open; it must not be implemented as a direct-versus-task switch. +0x3C remains a partial flag domain. Bounded consumers join bit 0x2 to an ActorMove constructor boolean, bit 0x8 to CActorTask_NetGlide, bit 0x200 to CActorTask_LearnSkill, bit 0x200000 to CActorTask_Fly, bit 0x01000000 to a six-node weapon presentation group, and bit 0x20000000 to the Sit transition; unnamed mirror/gate bits remain open.

AvatarAttr now separates 22 direct wire fields (44 directional rows) plus the canonical inherited DBAttribute prefix. Eighteen have exact bounded client meanings, including the appearance/equipment identifiers and body presentation fields. +0x60 remains partial: bit 0x1 gates application of the +0x64 item/color pair map, bits 0x4/0x8 suppress equipment effects in bounded paths, and bit 0x10 selects a 1.3 scale multiplier. Bit 0x1 does not control +0x64 wire serialization, whose presence is independently gated by the AvatarAttr codec mask; the complete +0x60 flag domain is not proved. The remaining selector/pair/opaque fields are retained without invented job/class semantics.

ItemAttr preserves two codec variants without leaking StallItem-only consumers into the base inventory type. Base-vtable +0x28/+0x39 remain partial. Only the StallItem-vtable rows name +0x28 as the qword lookup-key pair forwarded to two item controls and +0x39 as the shared-0xFF-gated stall item-control population path. StallItem +0x48 is the exact per-unit-price u32: IMAGE copies it from the source record, accumulates it, dispatches it to MONEYPANEL_COST, and multiplies it by selected quantity.

NPCAttr is proved as BasicAttr-derived and uses slot +0x34, not the frozen slot +0x18 argument copier. +0x7C is the exact visual-preset resource basename. +0xA0 is the FRIEND target-panel actor ID dispatched with selector 2, while +0xA8 is the ENEMY target-panel actor ID dispatched with selector 1 and is also consumed directly by HP_ENEMY. The resolver preserves the selector result in BL to choose the FRIEND (+0x44/+0x48) versus ENEMY (+0x38/+0x3C) widget slots; the separately read global UI byte controls another visibility/instance path and does not choose the friend/enemy offsets. +0x7A remains partial because only bits 1/2 and the bit-2 CheckApproachTarget binding are proved, while +0xB0 remains role-only because actor resolution/local-player comparison does not uniquely prove an owner noun.

CVehicleAttr +0x18..+0x40 are an exact fixed six-qword structural slot array: constructor, typed copy, empty-test, target search, first-zero search, and codec all use base +0x18, stride 8, count 6. Entry 0 (+0x18) additionally feeds two linked-object lookup paths, but that consumer claim is separately scope-open and is not projected onto every CVehicleAttr instance. Entries 1..5 remain role-only slot identities; IMAGE does not prove passenger, occupant, component, or object-ID nouns for them.

NavigationExAttr +0x2A/+0x2C/+0x30 are three separately addressed change-tracked state components: typed copy, difference-mask construction, and bit-controlled merge are exact for each member. They are not a homogeneous array, and no bounded consumer identifies coordinates, heading, speed, path/node, flags, map/zone ID, or time; those gameplay nouns remain open.

## DBAttribute, progression, cooldown, and refresh Attrs

DBAttribute's own codec is not empty. It owns the canonical +0x20 qword-delta presence mask and the bit-0-gated +0x18 qword. The mask role is exact; the qword is proved only as a copied/compared/delta-tracked base value and must not be renamed DBID, character ID, GUID, or primary key. AvatarAttr and MovementAttr no longer duplicate these inherited fields, and the same primitives were removed from the container table.

CCooldownAttr now has six exact structural rows: a stored count, a signed selector, and a float value in each direction. The float is exact `cooldown_remaining_value_f32` because client code decrements it by tick delta and erases the record at <=0; its time unit remains unproved. The selector is role-only because its skill/action/item namespace is still open.

CSkillAttr now has eight exact semantic rows: stored/wire record count plus repeated `{skill_id_u16_wire, current_skill_level_u16, current_level_skill_point_progress_u32}`. The last value is tied to the original client's skill-point cost and cumulative-progress calculations; server-side level-up normalization and overflow policy remain outside this IMAGE proof.

InstanceRefreshAttr has six exact rows: count plus repeated `{instance_identifier_s16, instance_refresh_time_endpoint_u32}`. The UI resolves the signed identifier through `s_INSTANCE_NAME` and subtracts a runtime clock from the endpoint for `TIME_REFRESH`; the clock unit, epoch, and authority remain open.

ExpressCountAttr has an exact one-byte delta-presence mask and one gated count byte. The count role is exact to this Attr, but IMAGE does not yet distinguish sent/used/remaining meaning or reset window. DATA separately records `EXPRESS_TIMES=5`; no field-level IMAGE join is claimed.

Express_ClientGetExpressItemAttrsVital has ten effective directional wire rows at its exceptional vtable slot +0x18: an inherited opaque qword, an Express-item-attrs lookup/cache key qword, an operation-status byte, vector count, and nested entry. The +0x28 role and +0x30 bounded status role are proved but their exact ID/enum domains stay open. R allocates exact ItemAttr vtable 0x00F0EBB0 and calls codec 0x0046BD30; W dispatches through the current entry vtable and therefore remains partial. The vector has no outer per-entry type key or payload length.

CrystalSlotAttr is structurally complete: +0x2C is the page*1000+slot key, +0x30 is a signed per-add nutrient cap (not an item ID), +0x32 is the crystal-presence flag, +0x33 the cultured level, +0x34 current cultivation EXP, and +0x36 luster. CrystalPlateAttr writes +0x48, signed max nutrient at +0x4C, a uint16 map count sourced from dword +0x44, then repeated CrystalSlotAttr children. Plate +0x48 remains the sole field-level semantic unknown; it is explicitly not the separately stored next-absorb time.

DailyRewardAttr serializes +0x28 countdown value, +0x2C item-definition ID, +0x30 item quantity, +0x32 slot code, and +0x33 UI-state code. DailyRewardBagAttr serializes the low uint8 of its stored dword size at +0x44 and repeated DailyRewardAttr children. Exact clock unit/basis, slot/state enum labels, and a direct DATA-row join remain open; no DATA vocabulary is promoted into the IMAGE rows.

CollectionPieceAttr serializes page ID, acquired mask, completion flag, and one opaque dword. CollectionObjPointAttr serializes its presence mask plus three gated uint16 values; the point widget value and finished-SUITS count are exact, while +0x2A remains unknown. CollectionBookAttr serializes a low-u8 count and repeated CollectionPieceAttr children. CollectableBookTypeAttr +0x28 is role-only; no DATA n_Type value is promoted into it without an exact join.

WinePotAttr serializes `{uint8 cellar_slot, uint8 unknown_29, uint32 formula_record_id, uint32 unknown_30, uint32 completion_deadline}`. The deadline role is exact but unit/epoch/authority are open. WineFormulaLearningAttr is an ordered unique uint16 formula-ID set: W emits sorted IDs, while R unions into the existing set without clearing. WineCellarAttr is an ordered uint8-slot to WinePotAttr map: R clears first, but its transferred uint16 count is used through a signed loop, so 0x8000..0xFFFF decode zero entries. These behaviors are preserved as measured quirks rather than normalized.

CAchievementsAttr serializes a mode byte followed by one of two counted containers. Mode zero clears the parent containers and transfers a keyed tree of `{lookup_key, action3_scalar, action4_scalar, counted_u32_components}` records. Nonzero transfers a sequence of `{opaque_u32, opaque_u32, opaque_u32, opaque_u8}` records; its R path appends without storing the incoming mode, while its W path frees the traversed list. Count transfers use low uint16 values while W traversal is container-bounded. DATA action names and tip references remain source-separated and are not promoted into IMAGE field names.

SystemGiftAttr inherits the canonical DBAttribute prefix, then transfers a low-u16 tree count and repeated `{qword key, u32 opaque, u16 opaque}` records. The key is copied into the exact `GSCN_RetieiveSystemGiftVital` request path and used by two lookup paths; the image spelling `Retieive` is preserved. Tree order is signed-qword ascending, duplicate keys do not insert, R does not clear an existing tree, and counts 0x8000..0xFFFF execute zero record iterations. UI shape does not justify naming the two opaque values as item ID or quantity.

QuestAttr transfers four ordered selector buckets for selectors 0, 1, 2, and 4. Each bucket is `{uint16 count, repeated uint16 quest_id}`; selector 1 is tied to active/client-local tracker behavior, while selector 4 is tied to ResetTodoTree, but the table deliberately keeps every selector name bounded rather than inventing offer/completed labels. DailyQuestAttr transfers an ordered unique `{uint16 key, uint32 value}` map with sequential duplicate handling and no pre-clear. QuestMiscAttr transfers an outer grouped map whose vectors contain `{uint16 group_key, uint8 kind, uint32 secondary_key, uint32 payload_a, uint32 payload_b}` records; kind 1 bounds payload_b to progress/value use and kind 2 bounds payload_a to a time-like endpoint, without assigning universal nouns.

UpdateAttrVital's paired codec at exceptional vtable slot +0x18 is now represented by four active container concepts: entry count, factory type key, declared payload length, and polymorphic nested Attr payload. The first three are exact. The nested payload remains partial by design because the entry/factory type key selects a concrete Attr +0x34 codec; on R, a null factory result skips the declared length, while a non-null decode does not consume or enforce that length. The existing 26-row A2 semantic delta remains the directional correction source.

## FightAttr and CBuffAttr

FightAttr's own slot +0x34 codec is empty. Its two runtime attachment pointers are non-wire fields. The 29 formulas in `PF_ATTR_COMPUTED_SEMANTICS.tsv` are exact original-client computations, but they do not prove which side was authoritative on the original server.

Pet/Activity adds ten non-wire runtime/state rows. Five attachment pointers are exact: DailyActivityState, CNetActor, PetsData, ActorLearnedPetsSkillData, and PetsMergingData. PetAttr +0x9C is a bounded mutation marker; PetsModule +0x20/+0x24 are selector-1/2 runtime references; +0x30 is tied to Pets_UpdateSummonPetsTimeOutVital and Pet_Sailor_CD but its time representation/units remain open. PetsModule +0x34 remains UNKNOWN because IMAGE proves only its constructor zero. The active-claim unresolved census is 464; the unified ledger is 976 after adding conflict-only work items. CAchievementsAttr replaces one coarse placeholder with thirteen precise open concepts (net +12); SystemGiftAttr replaces one coarse placeholder with six precise open field rows (net +5); the three Quest placeholders are replaced by fourteen field-role and six container-role concepts (net +17). These increases are finer resolution, not regressions.

`PF_ATTR_UI_BINDINGS.tsv` now contains 21 Fight getter-to-widget object-offset bindings plus four exact Activity literal-control bindings (`RADIOBUTTON_JEWEL`, `RADIOBUTTON_LINK`, `RADIOBUTTON_PUZZLE`, `BUTTON_OK`) to module object slots. Fight literal control names remain open where no exact model join exists.

UpdateAttrVital contributes its generic polymorphic Attr carrier, Express Get contributes an exact smart-pointer ItemAttr vector descriptor, DailyRewardBag and CollectionBook contribute bounded-count repeated child codecs, WineFormulaLearning contributes an additive ordered formula-ID set, WineCellar contributes a clearing slot-to-WinePot map, CAchievementsAttr contributes two mode-gated parent containers plus a counted TreeChild component vector, SystemGiftAttr contributes a signed-count ordered unique record tree, and the Quest family contributes four selector buckets, one Daily keyed-value map, and one nested grouped-record map. CBuffAttr has an exact filtered record count and three exact route buckets: +0x30 accepts a null primary lookup or selector 0, while +0x3C/+0x48 accept nonnull selectors 1/2 after a mask-overlap rejection. WRITE/count omit records whose +0x20 flags contain bit 0x2. Its record +0x30/+0x3C lookup roles and +0x40 tick-advanced threshold-clamped scalar are bounded; +0x28 is only one component of a compound coalescing match that also compares +0x30, +0x3C, and +0x80. Record +0x34/+0x38 remain wholly unnamed. The category gameplay labels are still deliberately open. Object/world and Pet/Activity containers remain separately enumerated. Every unresolved record noun remains explicit in `PF_ATTR_CONTAINER_SEMANTICS.tsv` and the unresolved queue.

Pet/Activity container offsets now carry an explicit outer-object basis. IMAGE constructor/factory proof adds exact PetAttr.CollectionRecord defaults (+0x10=0xFF, +0x12=0). The no-0x4000 finding is scoped only to the exact PetAttr codec; it is not a global claim about that bit.

PetAttr is an RTTI-only nested `PcRefObject` descendant outside the 139 relevant registered-class census. Its 18 direct fields are now structurally re-derived: +0x50 is exact `amity`, and +0x40 is the exact key passed to the IMAGE-loaded `PETDATA` record lookup. +0x18, +0x21, and +0x4C have bounded lookup/routing/property roles. +0x20 is UNKNOWN: the earlier 1/2 comparison belongs to +0x20 of a separately looked-up PETDATA record, not PetAttr +0x20. The apparent counterpath loads `SAILOR_SKILL_TIP` and tests its own payload byte without a proved PetAttr join. The other unconsumed meanings remain UNKNOWN.

## Source-separated DATA findings

`PF_ATTR_DATA_BINDINGS.tsv` publishes 77 DATA rows plus one separately labelled IMAGE loader-layout row. The DATA rows include name/quest/world/party/guild/activity/pet/crystal/Express/Daily Reward evidence, ActorAttr personal-data and second-password/login-account controls, hash-pinned and in-memory-decoded quest-mark assets, QUESTDATA, PETDATA, and STANDARD_MOB schema/value censuses, Collection storage widgets and six exact Collection table schemas, five exact Winemaking model/project definitions, five source-separated Achievement schema/component/action/tip-reference censuses, and two SystemGift UI-model definitions. The IMAGE row independently pins the 31-field STANDARD_MOB loader layout; it does not turn the DATA schema row into an IMAGE fact. DATA n_TYPE is explicitly not equated with QuestAttr selectors 0/1/2/4.

Important mismatch: IMAGE probes an optional MOBS runtime `f_SCALE` at VA 0x004A2FC3 and initializes the slot to 0.0 at VA 0x004A2020, while current original DATA MOBS has no `f_SCALE` column. The 0.0 meaning is not inferred, and the IMAGE and DATA claims must remain separate.

## Structural corrections

- BasicAttr/ActorAttr gate-or-mask conflicts: 68.
- CSkillAttr non-wire rows removed by overlay: 20.
- CSkillAttr field-layout rows corrected by overlay: 8.
- CCooldownAttr non-wire control/iterator rows removed by overlay: 16; field-layout rows corrected: 6.
- InstanceRefreshAttr non-wire control/iterator rows removed by overlay: 14; field-layout rows corrected: 6.
- CrystalSlotAttr field rows corrected: 12; CrystalPlateAttr field rows corrected: 8, non-wire helpers removed: 22, wrong-direction nested duplicates removed: 2. The four old wrong-slot removals remain frozen and are not duplicated.
- DailyRewardAttr own field rows retained with active semantics: 10; DailyRewardBagAttr count rows corrected: 2; nested-child rows corrected: 2; non-wire factory/container rows removed: 22; wrong-direction nested duplicates removed: 2.
- Collection own directional field rows: 18; CollectionBook count/child rows corrected: 4; non-wire factory/container rows removed: 24; wrong-direction nested duplicates removed: 2.
- WinePotAttr directional field rows: 10; Wine formula/cellar container layout rows corrected: 8; frozen WinePot layout rows corrected: 10; non-wire factory/container rows removed: 32; wrong-direction cellar duplicates removed: 2.
- CAchievementsAttr directional field rows: 16; count metadata rows corrected: 6; child/element rows corrected: 6; non-wire control/helper rows removed: 58.
- SystemGiftAttr inherited base rows already correct and left unchanged: 6; count rows corrected: 2; child-subcodec rows corrected: 2; wrong-direction child duplicates removed: 2; non-wire control/helper rows removed: 16; nested SystemGift directional fields added: 6.
- Quest family: 202 active correction rows; 12 inherited rows already correct and left unchanged; 6 old wrong-slot removals not duplicated. QuestAttr resolves 2 base directions, 8 selector dispatches, 8 counts, and 8 ID-element layouts while removing 96 non-wire rows. DailyQuestAttr corrects 2 counts and 4 fields while removing 14 non-wire rows. QuestMiscAttr corrects 4 counts, 2 group keys, 2 child subcodecs, and 10 fields while removing 42 non-wire rows.
- Express Get effective wire rows corrected: 10; non-wire helpers removed: 5; wrong-direction duplicates removed: 7. The nested ItemAttr candidate set is referenced by its 26-row aggregate and is not re-emitted.
- UpdateAttrVital: the existing 26-row A2 semantic delta remains canonical (13 wrong-direction removals, 13 reclassifications); the active container summary adds no duplicate correction rows.
- DBAttribute canonical ownership: 4 base directional rows replace 8 duplicated Avatar/Movement projections; 2 DB primitives removed from the container table. Frozen A2 already contains the correct DB rows, so no duplicate correction file was emitted.
- ItemBag-family non-wire rows removed by overlay: 362.
- ItemBag-family field-layout rows corrected by overlay: 84; inherited ownership aliases corrected: 2.
- ItemAttr non-wire lifecycle rows removed: 20; field-layout rows corrected: 22.
- ItemVaryAttr non-wire factory/container rows removed: 24; field-layout rows corrected: 6.
- Pet/Activity state rows reclassified from wire to control/lifecycle: 68.
- Activity/Pets module attachment rows reclassified as non-wire: 32.
- Owning-vtable boundary corrections: 2; unsupported empty-closure conflicts: 17; module slot-role correction: 1.
- Total conflict rows: 1285.

CSkillAttr is a DBAttribute-derived object with stored `_Mysize` at object +0x48 (low uint16 on wire) and repeated node fields `{skill_id_u16_wire@+0x0C, current_skill_level_u16@+0x10, current_level_skill_point_progress_u32@+0x14}`.

CCooldownAttr is a DBAttribute-derived record map at outer object +0x28 with stored dword count at +0x48 (low uint16 on wire), signed selector at node +0x0C, and remaining float at node +0x10. Do not infer the selector namespace or the float's time unit.

InstanceRefreshAttr is a DBAttribute-derived record map with stored dword count at +0x44 (low uint16 on wire), signed instance identifier at node +0x0C, and refresh-time endpoint at node +0x10. Preserve the endpoint as u32 without inventing an epoch or unit.

ExpressCountAttr adds mask +0x28 and gated count byte +0x29 after the inherited DBAttribute prefix. Preserve the byte even though its sent/used/remaining interpretation and reset window remain open.

CrystalSlotAttr serializes six fixed fields after DBAttribute. CrystalPlateAttr serializes +0x48, signed max nutrient, map count, then repeated CrystalSlotAttr children. Use `PF_A2_CRYSTAL_CODEC_CORRECTION.tsv`; never treat removed iterator/reference-count helpers as wire operations, and preserve Plate +0x48 losslessly until a unique non-copy consumer is proved.

DailyRewardAttr serializes five fixed fields after DBAttribute. DailyRewardBagAttr serializes a one-byte count and repeated exact DailyRewardAttr children. Use `PF_A2_DAILYREWARD_CODEC_CORRECTION.tsv`; preserve countdown/byte-code domains losslessly and keep DATA reward-table vocabulary separate until an exact join is proved.

CollectionPiece/CollectionObjPoint fixed fields and CollectionBook count/child layout are in `PF_A2_COLLECTION_CODEC_CORRECTION.tsv`. Preserve the two remaining unknown fields and CollectableBookType code losslessly; do not equate the code with DATA `COLLECT.n_Type` without a join.

Wine uses `PF_A2_WINE_CODEC_CORRECTION.tsv`. Preserve both opaque WinePot fields and the deadline value unchanged. Reproduce FormulaLearning's additive set decode and Cellar's clearing signed-count decode exactly; do not silently normalize either behavior.

Achievements uses `PF_A2_ACHIEVEMENTS_CODEC_CORRECTION.tsv`. Preserve all four ListChild fields and the two TreeChild action scalars losslessly unless a separate exact join supplies a narrower noun. Reproduce the mode-dependent clear/append/free behavior and low-u16 count truncation exactly; do not infer IMAGE field names directly from DATA action-token text.

SystemGift uses `PF_A2_SYSTEM_GIFT_CODEC_CORRECTION.tsv`. Preserve record +0x18 and +0x1C losslessly; do not infer item ID or quantity from the UI controls. Reproduce signed-count, no-preclear, signed-qword ordering, duplicate-collapse, and inherited DBAttribute ownership exactly.

Quest uses `PF_A2_QUEST_CODEC_CORRECTION.tsv`. Preserve selector buckets as selector_0/1/2/4 unless a stronger producer proves complete state names; preserve Daily values and QuestMisc kind-gated payloads losslessly; do not equate DATA n_TYPE with runtime selectors. Reproduce additive/no-preclear, removal, duplicate, count-truncation, and vector-order behavior exactly as scoped in the container rows.

Express Get uses `PF_A2_EXPRESS_GET_CODEC_CORRECTION.tsv`. Its exact codec is 0x006E8920..0x006E8A8F; the older 0x006E8920..0x006E8A8D window cuts the `ret 8` instruction, and the frozen 0x006E8920..0x006E8AED span extends into the next handler. Preserve +0x18 and the open +0x28/+0x30 domains without invented account/mail/package semantics.

The nine-class ItemBag family uses two stored dword container sizes whose low uint16 values are serialized, a dynamic nested Attr entry through vtable slot +0x34, and a qword secondary-node payload. The byte/u16 wrapper fields are structurally exact but still gameplay-unknown.

ItemAttr has two separately keyed vtable schemas. Its optional +0x3C payload is proven to be ItemVaryAttr. ItemVaryAttr type codes select exact IMAGE-named subtypes: Value for values below 99, String for 99 through 118, and Embeded for 119 or above.
ItemAttr +0x30 is the item-definition lookup key used to obtain s_ID_ICON, +0x34 is the linear container slot index resolved in pages of 80, +0x36 is the quantity value written to the exact ItemControl quantity-widget slot (+0x1810/+0x220), and +0x38 is the XML `quai` quality tier that maps values 1..5 to Label_ItemName FontStyle IDs 15..19. IMAGE and BigFontStyle DATA claims remain separate rows.

## P0-2 primary name FontStyle selector

[MEASURED][IMAGE] Method/control: the pinned selector hash is paired with an independent bounded `PUSH imm8` signature census for FontStyleID 55..63 and an executable-section `E8 rel32` census whose sole direct caller is `0x004446A7`. `PF_ATTR_NAME_COLOR_SELECTOR.tsv` publishes 14 valid paths and quarantines 0 paths. Only two local-CMyActor paths prove controller `0x00F2CD08`/child `+0x54`, and only three post-cast CNetNPC paths prove `0x00F2CD48`/child `+0x50`; nine paths remain the exact dynamic controller union. Both proved controller families load `NameBoard_Player`; no IMAGE runtime path to `NameBoard_NPC.model` is claimed.

[MEASURED][IMAGE] Signed-nonpositive control paths emit 60 when the relationship predicate succeeds, 63 when receiver vslot `+0x3C` succeeds, and 61/63 from linked `NPCAttr+0x98` actor resolution, but those paths do not independently prove owner class. After an exact CNetNPC cast, 61 is emitted for `AI_WANDER.n_OFFESIVE != 0`, 61 for UNNAMED runtime bit `+0x70 & 0x100` when two local-state predicates are false, and 62 when that bit is clear. `0x00444267` clears bit `0x100` and emits no style.

[MEASURED][DATA] `BigFontStyle.fsl` independently defines 60 as yellow, 61 as light red with dark-red outline, 62 as orange, and 63 as gray. IMAGE separately proves the pushed value reaches UILabel `FontStyleID`; the palette remains a DATA row. `FONT_COLOR`, `MOBS.n_SKIN_COLOR`, and unrelated UI property IDs are not joined.

[MEASURED][IMAGE] No selector path proves a separate monster C++ class. Style 61 is not equivalent to `n_AGGRO`: its emission conditions include linked-actor success, `n_OFFESIVE`, and UNNAMED bit `0x100`; two HitResult writer causes are observed but are not a complete writer census. Style 63 is not equivalent to dead: the ordered CNetNPC dead predicate is one cause, while linked-actor failure is another. Style 62 is a bounded fallback, not proof of a monster class. ActorAttr +0x180 separately selects `LABEL_GUILD` FontStyleID 64..67 and is the negative control for the independent quest-mark board.

## P0-3 CNetNPC quest-mark selector

[MEASURED][IMAGE] `PF_ATTR_QUEST_MARK_SELECTOR.tsv` publishes nine valid selectors 0..8 plus one explicit out-of-range guard row. CNetNPC construction stores NPCAttr at +0x358, the QuestIconBoard pointer at +0x360, and a selector cache at +0x364. The audited QuestNPCModule refresh reads NPCAttr +0x78, submits a client-local event kind 0x0A, and the proved QuestModule handler calls 0x00619E00 before CNetNPC reaches the selector at 0x006078D0. This proves one local computation path, not that 0x00619E00 is the sole/final writer: the remaining event-subscriber overwrite census is open.

[MEASURED][IMAGE] Selectors 1..8 map exactly to eight resource literals. Selector 0 sets board-root bit 0 and loads no new resource; it is not labelled hidden or absent. Input greater than 8 selects no new resource and reaches the common bit-clear tail, but the audited compute span emits only 0..8. The setter can skip its board call when the CNetNPC gate is clear, the board pointer is null, or the cached selector is unchanged. The refresh can also skip on missing typed-object/template/actor/singleton prerequisites.

[MEASURED][IMAGE] Canonical selector conditions (verbatim from `PF_ATTR_QUEST_MARK_SELECTOR.tsv` claim-bound rows): selector 0: audited compute precondition fails, no eligible s_QUEST_END/s_QUEST_BEGIN MOBS candidate remains, or the pinned zero/5 fallback selects zero | selector 1: s_QUEST_BEGIN candidate; QuestAttr +0x28 lookup returns 0; opaque IMAGE predicate, local-singleton BasicAttr+0x5E opaque u16 threshold, and Accept_Check pass; n_TYPE(+0x14) not in {20,30}; no later 2/6/7/8 override | selector 2: selector-1 conditions plus n_TYPE(+0x14) in {5,6,7,10,40}, unless later 6/7/8 override wins | selector 3: s_QUEST_END candidate; QuestAttr +0x28 lookup returns 1 and Report_Check passes; n_TYPE(+0x14) not in {5,6,7,10,40}; returns before s_QUEST_BEGIN scan | selector 4: selector-3 conditions plus n_TYPE(+0x14) in {5,6,7,10,40}; returns before s_QUEST_BEGIN scan | selector 5: s_QUEST_END candidate has QuestAttr +0x28 lookup value 1 but Report_Check fails, and no later s_QUEST_BEGIN candidate wins | selector 6: accepted s_QUEST_BEGIN candidate whose n_LEVEL_QUEST(+0x18) plus global[0x010223E4] is below local-singleton BasicAttr+0x5E opaque u16 threshold; overrides 1/2 unless n_TYPE(+0x14) 25/41 later selects 7/8 | selector 7: accepted s_QUEST_BEGIN candidate with n_TYPE(+0x14) 25; overrides earlier 1/2/6 choice | selector 8: accepted s_QUEST_BEGIN candidate with n_TYPE(+0x14) 41; overrides earlier 1/2/6 choice | selector >8: accepted by the selector input guard path; not emitted by the audited compute span. Callback names and opaque thresholds do not prove original-server gameplay semantics.

[MEASURED][DATA] Eight shipped packed textures are decoded only in memory and pinned by packed hash, decoded TGA hash, 64x64x32 header, alpha-plane geometry class, and alpha-weighted RGB palette class. The DATA rows are explicitly UNJOINED and make no IMAGE ownership or runtime-resolution claim. No decoded bytes are written to an artifact.

[INFERENCE][CROSS-SOURCE] The case-insensitive filename stems of the IMAGE `.tga` literals resemble the shipped DATA `.tg_` names. This is only a review lead: the exact live resolver, runtime selection, placement, alpha/blend appearance, and display remain unproved.

[MEASURED][IMAGE] The shared function at 0x00616740 is a typed module-attachment filter that accepts CNetNPC and stores the object at module +0x18; the older `serializer` label is superseded for this function. NPCAttr +0x78 now has two exact CNetNPC-scoped directional rows while its generic UNKNOWN rows remain an unresolved owner remainder excluding the proved CNetNPC owner—not evidence that another class was observed. QuestAttr wire claims continue to cite `PF_A2_QUEST_CODEC_CORRECTION.tsv` and container rows, not the EMPTY base serializer census.

## P0-4 CNetNPC role and trait discriminator

[MEASURED][IMAGE] PF_ATTR_ROLE_DISCRIMINATOR.tsv publishes 15 IMAGE rows. The audited actor factory dispatch contains cases 2/3/4/5/6, each still subject to state/allocation null paths, and CNetNPC carries NPCAttr plus a parsed MOBS row; no distinct actor_type case named monster is present in that bounded dispatch. One audited interaction route requires a CNetNPC cast, relation true, and the exact condition NPCAttr +0x7A bit1 clear or bit2 set before later state/distance gates can reach ChooseNPC. A separate generic interaction path requires CNetNPC plus distance. In two audited target-selection branches, relation false leads to local enemy-target +0xC8/+0xCC; generic actor-state/range logic then reaches the EA7D ActionVital producer. No access in that core has a proven CNetNPC, NPCAttr, or parsed-MOBS base for n_RANK, n_AI_COMBAT, n_OFFESIVE, n_CAPABILITY, or n_MOB_USAGE; matching numeric offsets on other bases are unrelated.

[MEASURED][IMAGE] Presentation remains independent: n_RANK bits 6..10 have exactly two boss-UI callers; n_OFFESIVE has one direct nameboard predicate caller; n_CAPABILITY==1 drives duplicated raw-table UI/data gates. The unique named n_AI_COMBAT query is its loader and unnamed offset-based consumers remain open; n_ENEMY is loaded/copied without a proved admission consumer; n_MOB_USAGE has zero exact ASCII/UTF-16 literals. The shared death predicate and loaded drop configuration do not produce a proved death-to-loot edge.

[MEASURED][DATA] The 13 DATA rows retain the independent MOBS/AI_WANDER census. n_MOB_USAGE=1 overlaps the empirical rank+combat cluster in 1533/1545 rows but has 12 exceptions and misses 139 other rank+combat rows. usage=2 + capability=1 + quest vectors has 670 rows but includes 12 rank-positive, 10 combat, and 8 offensive counterexamples. MOBS ids 916 and 917 are exact, distinct record fingerprints; neither proves a generalized dummy bit. Same-name control groups 27/1732/8621 and 31/1635/2127 vary across rank, combat, usage, and offensive traits.

[MEASURED][CROSS-SOURCE NONCLAIM] No single is_monster, talk_only, or attackable field is proved. IMAGE and DATA remain separate rows; the empirical DATA clusters are not original role policy.

[PROPOSED] For reconstruction review, model the role as additive, independently testable traits. This is design guidance, not evidence that the original server stored those traits or one role enum.

## A5

Capture validation is published separately in `PF_ATTR_FIELD_VALIDATION_DELTA.tsv/.md`; it keeps CAPTURE facts separate from IMAGE/DATA rows and reports any current-inventory exclusions explicitly.

## Deduplication

No duplicate A1/A3 Attr overlay was emitted; the prior slot34 deltas remain the canonical A1/A3 structural destination. Frozen A1-A6 artifacts were not edited.
