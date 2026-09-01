# PF serializer slot +0x34 correction

[MEASURED] IMAGE-only additive correction. Frozen V1 remains untouched.

## Result

The V1 registry treated vtable `+0x18` as the serializer slot for every registration. The whole 502-row known-vtable census proves a second family: 56 rows have no W/R capability at `+0x18` and both W/R capabilities at `+0x34`.

- A1 slot-provenance corrections: 59 (56 changed targets, 2 same-target provenance corrections, 1 ambiguous ItemAttr).
- Exact bounded serializer roots: 58 (56 singleton rows plus 2 isolated ItemAttr candidates).
- A2 directives: 2308; ADD_AMBIGUOUS_CANDIDATE_ROW=56, ADD_ANALYSIS_BLOCKER_ROW=79, ADD_CORRECTED_SLOT34_ROW=2059, REMOVE_WRONG_SLOT_ROW=114
- A3 frequency rows: 23; ambiguous ItemAttr candidates are separate alternatives and are excluded from singleton frequencies.
- Priority rows changed: 37; P1 CLOSED->OPEN corrections: 6.
- Unchanged rows copied as new output: 0. Exact duplicate delta keys: 0. Old-slot/new-slot semantic-row overlap: 0.

## Whole-registry capability partition

- `DIFFERENT_NEITHER`: 101
- `DIFFERENT_SLOT18_NONE_SLOT34_RW`: 56
- `DIFFERENT_SLOT18_RW_SLOT34_NONE`: 343
- `SAME_NEITHER`: 2

The slot identity is anchored by the generic Attr carrier `[0x00463DE0,0x00463FA2)` (sha256 `888c2fac20948b7896ed105f46b84e94d01c9442f6535df9be36e6baa2335fc3`), which has exactly two vtable `+0x34` indirect call sites with one recovered two-argument path each and no vtable `+0x18` call. The factory initializer `[0x005F89F0,0x005F8BDF)` is pinned at sha256 `72d19d0a6395fcdcf9839982b9788453a5e2e1df223b72e7de722fae00dc5316`.

## Priority-1 truth corrections

| message | old serializer/structural | corrected serializer/structural | corrected blocker |
|---|---|---|---|
| `ActorExpressData` | `CLOSED/CLOSED` | `OPEN/OPEN` | `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved` |
| `ActorLearnedPetsSkillData` | `CLOSED/CLOSED` | `OPEN/OPEN` | `direct_call_not_proven_serializer | invalid_parameter_import_call_wire_effect_unproved` |
| `ActorMailData` | `CLOSED/CLOSED` | `OPEN/OPEN` | `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | invalid_parameter_import_call_wire_effect_unproved | mutable_pointer_slot_traversal_alias_unproved` |
| `ItemAttr` | `CLOSED/OPEN` | `OPEN/OPEN` | `registry vtable UNKNOWN | registry serializer UNKNOWN | atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | indirect_serializer_direction_unresolved | registry_serializer_slot34_ambiguous` |
| `ItemBagAttr` | `OPEN/OPEN` | `OPEN/OPEN` | `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | indirect_serializer_direction_unresolved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_pointer_slot_traversal_alias_unproved` |
| `ItemBagAttr_Equiped` | `OPEN/OPEN` | `OPEN/OPEN` | `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | indirect_serializer_direction_unresolved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_pointer_slot_traversal_alias_unproved` |
| `ItemMallBagAttr` | `OPEN/OPEN` | `OPEN/OPEN` | `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | indirect_serializer_direction_unresolved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_pointer_slot_traversal_alias_unproved` |
| `ItemMallGiftItem` | `CLOSED/CLOSED` | `OPEN/OPEN` | `direct_call_not_proven_serializer | invalid_parameter_import_call_wire_effect_unproved` |
| `ItemVaryAttr` | `CLOSED/CLOSED` | `OPEN/OPEN` | `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | mutable_dword_slot_nested_targets_and_alias_unproved` |
| `NPCAppearAttr` | `CLOSED/CLOSED` | `OPEN/OPEN` | `direct_call_not_proven_serializer | invalid_parameter_import_call_wire_effect_unproved` |

`ItemAttr` has two exact +0x34 candidates and therefore remains OPEN. Its candidate schemas are kept in separate `schema_variant` rows and are never merged into one asserted table.

## Fail-closed analysis boundary

- `CBuffAttr`: `direct_call_not_proven_serializer | primitive_tag_or_len_not_immediate`
- `VowLockData`: `atomic_target_object_alias_unproved | direct_call_not_proven_serializer | dynamic_vtable_plus_0x04_target_unresolved | indirect_call_not_proven_serializer_slot | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_dword_slot_nested_targets_and_alias_unproved | primitive_tag_or_len_not_immediate`

## Evidence boundary

- Every TSV row is `source=IMAGE`; no DUMP, CAPTURE, or DATA fact is mixed in.
- No raw dump/capture byte is emitted.
- A1 describes identity and slot provenance; A2 describes wire structure; candidate-only rows are not singleton facts and do not contribute to A3 or closure counts.
- The two same-target rows correct slot provenance only. They are not counted as newly discovered values.

## Reproduction

Run `py -3 pf_build_serializer_slot34_correction.py --check`. It pins every input, re-derives the full capability partition and bounded entry CFGs, verifies base-row keys, and compares every output byte-for-byte.
