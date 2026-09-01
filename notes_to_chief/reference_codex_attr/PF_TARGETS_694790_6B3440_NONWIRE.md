# IMAGE closure: targets 0x00694790 and 0x006B3440

[MEASURED] Additive removal-only correction. Frozen V1 and slot-0x34 inputs are unchanged.

## Outcome

- Removed **30 effective A2 analysis artifacts**: 26 frozen-V1 rows and 4 slot-0x34 overlay rows.
- Effective census is **10 messages: 7 Priority-1 and 3 Priority-3**. The assignment's earlier 'six P1' count omitted slot-0x34 `ActorExpressData`, whose effective Priority overlay is OPEN.
- Counts are R=20, W=10. The ten W rows are path-insensitive duplicates: each of the five directional serializers has one physical call pair, located only in its pinned zero-mode/read branch.
- The 30 directives have 0 unchanged copies, 0 duplicate base rows, and 0 cross-overlay base-row overlaps. Every row has `source=IMAGE`.
- No Priority delta is emitted. All ten messages remain OPEN because independent blockers remain; the broad direct-call blocker category is not edited by this target-specific overlay.

## Proven non-wire structure

`0x006B3440` allocates one fixed 12-byte list node, stores its first two caller arguments at node +0/+4, and copies the third smart-reference argument into node +8 through `0x0069D040`. Its normal CFG has block starts 0x006B3440, 0x006B3485, 0x006B348A, 0x006B3491 and 0x006B3496; the separately pinned EH cleanup starts at 0x006B34BC. Calls are exactly operator-new, smart-reference copy, EH operator-delete, and C++ throw; normal return is `ret 12`.

`0x00694790` reads only container +0x18 and its one stack argument. Its three-block CFG starts at 0x00694790, 0x006947C6 and 0x00694802: success adds the argument (always 1 at these six callers) to container +0x18; overflow constructs and throws an exception. It returns `ret 4`.

The smart-reference support copies the payload pointer and calls the pinned InterlockedIncrement wrapper only when non-null. Each caller then links the node through the sentinel/tail and releases its temporary ownership through the pinned InterlockedDecrement wrapper. Neither target has a stream formal, neither target/support call set reaches wire primitives 0x0089A600 or 0x0089A640, and the PE imports/EH thunks are pinned by address, symbol and full IMAGE span hash.

No key/value, actor, party, item, or gameplay semantics are inferred from names or nearby strings.

## Caller and effective-row census

| caller/messages | span SHA-256 | node/size calls | container member | stream provenance | V1 rows | slot rows |
|---|---|---|---|---|---:|---:|
| `GSCN_RunTimeProtocolReq`, `GSCN_RunTimeProtocolRes`, `GSCN_LoginProtocol`, `LSCN_Protocol`, `VitalProtocol` | `bfdf1ada48068e9a3838b51241e164677e0142a6ce0f6d68d547299fe279e217` | `0x005F3F75` / `0x005F3F81` | owner+0x10; sentinel owner+0x24 | entry+0x4 -> EDI; target pair receives list/node args, not stream | 10 | 0 |
| `PartyUpdateVital` | `dae58227a8f755839eaa6343699a7782137ea5364f089b403cf02ae63d945935` | `0x006278D9` / `0x006278E4` | this+0x28; sentinel this+0x3C | entry+0x4 -> EDI; target pair receives list/node args, not stream | 4 | 0 |
| `PlayerSearchVitalRes` | `e26789d1ea041e2321860520737dcd564aa2b4eb82b6fac2bfa25837b54d54df` | `0x0069496A` / `0x00694975` | this+0x10; sentinel this+0x24 | entry+0x4 -> ECX on read branch; target pair receives list/node args, not stream | 4 | 0 |
| `ItemMallPersonalGiftVital` | `1d05f5d3dd6dbf2e6a86eaebefaba5313146d83ce7d678e29ca7c4fc0fcad6b3` | `0x006B2359` / `0x006B2364` | this+0x10; sentinel this+0x24 | entry+0x4 -> ECX on read branch; target pair receives list/node args, not stream | 4 | 0 |
| `ActorExpressData` | `9d533f91678a951228c059201bf22d160b6a685f2cb4a4aafddc89ed16ecab21` | `0x006E403A` / `0x006E4045` | this+0x30; sentinel this+0x44 | entry+0x4 -> EBP on read branch; target pair receives list/node args, not stream | 0 | 4 |
| `Express_InitalizeActorExpressVital` | `1954451838b7b206d97e228357393475609a4074d88411cf83410de43e8a033d` | `0x006E8291` / `0x006E829C` | this+0x28; sentinel this+0x3C | entry+0x4 -> EDI; target pair receives list/node args, not stream | 4 | 0 |

## Pinned spans

| role | VA span (end exclusive) | bytes | file offset | SHA-256 |
|---|---|---:|---:|---|
| size_increment | `0x00694790-0x0069481A` | 138 | `0x00293B90` | `62b074c5ba49c9d91c06f56ffb509eb6e609170b0c49bbc9c69c629e621d9f98` |
| node_allocate | `0x006B3440-0x006B34D2` | 146 | `0x002B2840` | `e03507a26af6b8954d07e08b7d34b82925324f114c95943fa79297352af3e4b3` |
| exception_copy | `0x00401030-0x0040108F` | 95 | `0x00000430` | `e8a0c69b0a0053ea46a9877c9e1dca61a8671b5c692b5b3d979026bc4a5d4bc6` |
| smart_ref_copy | `0x0069D040-0x0069D09A` | 90 | `0x0029C440` | `b79870afe41d0111715a239fd6137b54216374300befa0ee0b4e9601e280b2f8` |
| ref_increment | `0x0088D050-0x0088D05B` | 11 | `0x0048C450` | `6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845` |
| ref_decrement | `0x0088D060-0x0088D082` | 34 | `0x0048C460` | `d3b546ac50ded491a6c5a196138b9691f23d8499298e728925f1afb1f0e7734c` |
| operator_new_thunk | `0x00B37980-0x00B37986` | 6 | `0x00736D80` | `026db59c9509fd5984356ee06312c76482b74741604ce391ee977c41473b76e4` |
| operator_delete_thunk | `0x00B37952-0x00B37958` | 6 | `0x00736D52` | `dac5c7df4ee9addc4293b8459a55d2bc3eb5864debafc857fb97c01fbbb07cf8` |
| cxx_throw_thunk | `0x00B37998-0x00B3799E` | 6 | `0x00736D98` | `16bf8ff4ff7050398899b806680db04f97c42d1b2f69ba2f4eed563eae73ba16` |
| shared_serializer | `0x005F3E20-0x005F406D` | 589 | `0x001F3220` | `bfdf1ada48068e9a3838b51241e164677e0142a6ce0f6d68d547299fe279e217` |
| party_serializer | `0x00627730-0x00627942` | 530 | `0x00226B30` | `dae58227a8f755839eaa6343699a7782137ea5364f089b403cf02ae63d945935` |
| player_search_serializer | `0x00694820-0x006949C3` | 419 | `0x00293C20` | `e26789d1ea041e2321860520737dcd564aa2b4eb82b6fac2bfa25837b54d54df` |
| personal_gift_serializer | `0x006B2230-0x006B23A6` | 374 | `0x002B1630` | `1d05f5d3dd6dbf2e6a86eaebefaba5313146d83ce7d678e29ca7c4fc0fcad6b3` |
| actor_express_serializer | `0x006E3EF0-0x006E4142` | 594 | `0x002E32F0` | `9d533f91678a951228c059201bf22d160b6a685f2cb4a4aafddc89ed16ecab21` |
| express_initialize_serializer | `0x006E8150-0x006E82E4` | 404 | `0x002E7550` | `1954451838b7b206d97e228357393475609a4074d88411cf83410de43e8a033d` |

## Residual Priority blockers

The table lists blockers other than the broad direct-call category. That category is also left untouched because other direct targets may still contribute to it.

| message | priority | effective status | other blockers proving OPEN |
|---|---:|---|---|
| `ActorExpressData` | 1 | OPEN | `atomic_target_object_alias_unproved | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved` |
| `Express_InitalizeActorExpressVital` | 1 | OPEN | `atomic_target_object_alias_unproved | dynamic_vtable_plus_0x04_target_unresolved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved` |
| `GSCN_LoginProtocol` | 1 | OPEN | `atomic_target_object_alias_unproved | call_clobber@0x005F3F34:ecx | dynamic_vtable_plus_0x04_target_unresolved | exact_import_thunk_call_wire_effect_unproved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | pe_security_cookie_failure_path_wire_effect_unproved | primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE` |
| `ItemMallPersonalGiftVital` | 1 | OPEN | `atomic_target_object_alias_unproved | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved` |
| `PartyUpdateVital` | 1 | OPEN | `atomic_target_object_alias_unproved | dynamic_vtable_plus_0x04_target_unresolved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_dword_slot_nested_targets_and_alias_unproved` |
| `PlayerSearchVitalRes` | 1 | OPEN | `atomic_target_object_alias_unproved | dynamic_vtable_plus_0x04_target_unresolved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved` |
| `VitalProtocol` | 1 | OPEN | `atomic_target_object_alias_unproved | call_clobber@0x005F3F34:ecx | dynamic_vtable_plus_0x04_target_unresolved | exact_import_thunk_call_wire_effect_unproved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | pe_security_cookie_failure_path_wire_effect_unproved | primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE` |
| `GSCN_RunTimeProtocolReq` | 3 | OPEN | `atomic_target_object_alias_unproved | call_clobber@0x005F3F34:ecx | dynamic_vtable_plus_0x04_target_unresolved | exact_import_thunk_call_wire_effect_unproved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | pe_security_cookie_failure_path_wire_effect_unproved | primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE` |
| `GSCN_RunTimeProtocolRes` | 3 | OPEN | `atomic_target_object_alias_unproved | call_clobber@0x005F3F34:ecx | dynamic_vtable_plus_0x04_target_unresolved | exact_import_thunk_call_wire_effect_unproved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved | mutable_pointer_slot_traversal_alias_unproved | pe_security_cookie_failure_path_wire_effect_unproved | primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE` |
| `LSCN_Protocol` | 3 | OPEN | `atomic_target_object_alias_unproved | call_clobber@0x005F3F34:ecx | dynamic_vtable_plus_0x04_target_unresolved | exact_import_thunk_call_wire_effect_unproved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | pe_security_cookie_failure_path_wire_effect_unproved | primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE` |

## Stop rule

Stop at these two helpers, their fixed support/EH/import paths, and the six proven caller spans. Resume only if a later effective A2 layer adds one of these exact target tags or independent evidence resolves a remaining blocker.
