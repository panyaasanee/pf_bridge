# PF Attr field semantics - Priority-0 structural checkpoint

[MEASURED] Method: exact IMAGE codec/support-span hashes plus frozen-row selector partitions; control: fixed IMAGE SHA-256 and exact row/action censuses. TSV row status/evidence is authoritative over prose.

A published checkpoint is authoritative only through `PF_ATTR_GENERATION_MANIFEST.json`; consumers must resolve its content-addressed verified generation directory and parse the exact bytes whose hashes were verified. Top-level files are compatibility materializations, not a cross-file atomicity guarantee.

- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Directional rows: 490
- Unique wire fields/controls: 256
- Priority-0 gameplay fields: 28 structural; 30 class-scoped claims (`PROVEN_EXACT` 20; `PROVEN_ROLE_ONLY` 7; `PARTIAL` 0; `UNKNOWN` 3)
- Recorded conflicts/claim corrections: 1286 rows; see `PF_ATTR_CONFLICTS.tsv` for source-separated details
- Concrete-class scope: `PROVEN_EXACT` 280; `UNKNOWN` 210
- `PARTIAL`: 27
- `PROVEN_EXACT`: 231
- `PROVEN_ROLE_ONLY`: 190
- `UNKNOWN`: 42

The 28 priority BasicAttr/ActorAttr gameplay fields now have exact W/R order, gate, offset, tag/sequence helper, length class, constructor default, VA, file offset, and codec-span hash. Eighteen have exact bounded semantics. BasicAttr +0x28 is split by `applies_to_class` and feeds `LABEL_NAME` in the separately proved CNetActor and CNetNPC nameboard controllers. ActorAttr +0x164 feeds the CNetActor `LABEL_GUILD` child +0x5C. ActorAttr +0x98 is role-only: it gates the CNetActor pair-relation predicate, while the local CMyActor path selects LABEL_NAME FontStyleID 56 for value 1 and 55 otherwise; the complete value domain/gameplay noun is not proved. BasicAttr +0x54 is split by `applies_to_class`: the dynamic FightAttr path consumes it in the exact run-speed formula but does not prove a concrete actor subtype; CNetNPC receives MOBS `n_SPEED_WALK` and passes it to the horizontal-locomotion scalar setter. The separate MOBS runtime +0x0C `f_SCALE` slot has no join to +0x54. Other exact bindings include BasicAttr +0x68 (`n_FACTION`), BasicAttr +0x6C (`n_ENEMY`), ActorAttr +0x78 (`GetPpClass`), +0x1A0 (Navy/Pirate icon), +0x1A8/+0x1AC (`GetBoatHealth` current/max), +0xE8 (residence location), +0x104 (age), +0x120 (constellation), +0x148 (uppercase MD5 of second-password bytes followed by login-account bytes), and +0x190/+0x198 (FRIEND/ENEMY target-panel actor IDs). Seven more have exact structural/consumer roles without a unique broader gameplay noun. Three remain semantically `UNKNOWN`: BasicAttr +0x5C, BasicAttr +0x60, and ActorAttr +0x1B2. Meaning certainty and concrete-class scope certainty are reported independently in the TSV.

The frozen A2 slot34 overlay is left unchanged. This checkpoint records its omitted BasicAttr high mask gates, omitted ActorAttr `+0x1BC != 0` nested gates, two omitted Actor mask gates, and its stack-only description of the `+0x1B4/+0x1B8` mask pair in `PF_ATTR_CONFLICTS.tsv`.

The three prefix fields are structural control fields: BasicAttr presence mask, ActorAttr's two presence masks, and the one-byte ActorAttr field-group gate. They are not counted as gameplay-semantic successes.

CSkillAttr is now structurally reduced to the inherited DBAttribute prefix, a stored object `_Mysize` whose low uint16 is written as the count, and three repeated record-node fields. The R count is deliberately keyed as wire control rather than a false direct object write. The node fields are now exact `skill_id_u16_wire`, `current_skill_level_u16`, and `current_level_skill_point_progress_u32`.

InstanceRefreshAttr is reduced to count plus repeated exact `{instance_identifier_s16, instance_refresh_time_endpoint_u32}` records. The identifier is consumed by the instance-name UI path and the endpoint is subtracted from a runtime clock; time unit and epoch remain open.

ExpressCountAttr has an exact one-byte delta-presence mask and one gated count byte. The count remains role-only because IMAGE does not distinguish sent, used, or remaining meaning or its reset window. DATA `EXPRESS_TIMES=5` is kept in a separate source row without a field-level join.

CrystalSlotAttr now has six direct fields in each direction: an exact page*1000+slot key, a bounded per-add nutrient cap, a zero/nonzero crystal-presence flag, exact cultured level, current cultivation EXP, and luster level. CrystalPlateAttr adds max nutrient, map-size count, and repeated nested CrystalSlotAttr records; only Plate +0x48 remains semantically UNKNOWN. The old helper rows and wrong-direction nested-call duplicates live only as explicit corrections.

DailyRewardAttr now has five direct fields in each direction: countdown value, item-definition ID, item quantity, slot code, and UI-state code. DailyRewardBagAttr serializes the low uint8 of its stored size and repeated exact DailyRewardAttr children. The countdown unit/clock basis, exact slot/state enum labels, and any direct join to the DATA reward tables remain deliberately open.

The Collection overlay now separates four exact class codecs. CollectionPieceAttr carries page ID, acquired-piece mask, completion flag, and one still-unknown auxiliary dword. CollectionObjPointAttr carries its delta mask, one unknown uint16, the exact point widget value, and finished-SUITS count. CollectionBookAttr serializes a low-u8 count plus repeated CollectionPieceAttr records; CollectableBookTypeAttr remains role-only because its code domain has no unique typed consumer.

WinePotAttr serializes slot index, one unknown byte, formula-record ID, one unknown dword, and a completion deadline in each direction. WineFormulaLearningAttr is an ordered unique uint16 formula-ID set whose decoder adds/unions without clearing. WineCellarAttr is an ordered uint8-slot to WinePotAttr map whose decoder clears first; its uint16 transfer is consumed by a signed loop, so values 0x8000..0xFFFF execute zero entries. Clock unit/epoch and the two opaque WinePot fields remain open.

CAchievementsAttr now has a complete mode-gated grammar. Mode zero selects a keyed tree of TreeChild records; nonzero selects a ListChild sequence. TreeChild carries an exact lookup key, two action-specific scalar roles, and a counted vector of indexed progress components. ListChild carries three opaque dwords and one opaque byte. The active correction file removes 58 frozen non-wire helper rows instead of treating them as fields.

SystemGiftAttr now resolves to the inherited DBAttribute prefix, one uint16 record count, and repeated exact SystemGift records `{signed-qword retrieval key, opaque u32, opaque u16}`. The key is exact to lookup/retrieve behavior; the other two values are copied into UI-row state but remain unnamed because item-ID/quantity labels are not proved. The decoder uses a signed count loop, preserves a pre-existing tree, and collapses duplicate keys.

QuestAttr now resolves to four fixed selector buckets (0, 1, 2, 4), each carrying a uint16 count and repeated uint16 quest IDs. DailyQuestAttr is an ordered uint16-to-u32 map whose positive values insert/update and whose zero or signed-negative values remove. QuestMiscAttr is an ordered outer group map of record vectors; each record carries group key, kind byte, secondary key, and two kind-gated payloads. These are bounded IMAGE roles, not permission to rename selector states or equate them with DATA n_TYPE.

Express_ClientGetExpressItemAttrsVital is now decoded at its exceptional vtable codec slot +0x18 using the exact function end after `ret 8`. It serializes two qwords, a status byte, a uint16 vector count, and repeated ItemAttr payloads. The R child target is exact ItemAttr vtable 0x00F0EBB0 +0x34; the W runtime subtype remains partial. Existing ItemAttr subfields are referenced, not copied.

The ItemBag-family checkpoint covers nine classes sharing `0x0046F180`: two uint16-on-wire container counts, one dynamic nested Attr serializer, and one qword record payload per direction. Wrapper fields are attributed to their declaring class; specifically, CGuildStorageAttr inherits BackpackAttr +0x68 instead of creating a duplicate child-owned field. Gameplay nouns remain open, and the prior traversal/helper rows are retained only as explicit `NOT_WIRE` corrections.

ItemAttr now keeps its two vtable schemas separate. Both serialize six fixed fields plus an optional ItemVaryAttr presence bit and nested payload; the extended schema appends one dword. ItemVaryAttr is reduced to count, exact type byte, and a subtype payload selected as ItemVaryData_Value (<99), ItemVaryData_String (99..118), or ItemVaryData_Embeded (>=119).

No semantic name was copied from prior reports or owner-visible probes. Those artifacts are used only for priority and conflict checks.
