# PF static closure for target 0x00652A30

[MEASURED] IMAGE-only additive correction. Frozen V1 and the slot-0x34 correction remain untouched.

## Outcome

- Removed **16 effective A2 analysis artifacts**: 12 frozen-V1 rows plus 4 rows added by the slot-0x34 correction.
- The 16 directives contain **0 unchanged copies**, **0 duplicate base rows**, and **0 cross-overlay base-row overlaps**.
- No Priority delta is emitted. All six affected Priority-1 messages and both affected Priority-3 Attr messages retain other blockers and remain `OPEN`.
- `0x00652A30` is an ordered-tree lookup/insert helper reached only after the read branch has already consumed key/value bytes into caller stack locals. It is not a wire primitive.
- No semantic claim is made for any tree key or value. Their widths and nearby message names do not establish meaning.

## Duplicate and layer accounting

| input layer | removal action | rows | W | R | unchanged copied | duplicate/cross-overlap | source |
|---|---|---:|---:|---:|---:|---:|---|
| frozen V1 A2 | `REMOVE_NONWIRE_ROW` | 12 | 6 | 6 | 0 | 0 | IMAGE |
| slot-0x34 A2 overlay | `REMOVE_OVERLAY_NONWIRE_ROW` | 4 | 2 | 2 | 0 | 0 | IMAGE |

The W rows are path-insensitive duplicates of a call that exists only below the zero-mode/read branch. The R rows name a real call, but that call mutates an ordered-tree member after the stream primitives have returned; it does not itself read or write the stream.

## Exact helper boundary and call set

| role | start VA | end VA (exclusive) | bytes | file offset | SHA-256 |
|---|---:|---:|---:|---:|---|
| ordered_tree_lookup_insert | `0x00652A30` | `0x00652B1F` | 239 | `0x00251E30` | `fc953d5b6890f65b63eaa8c90dd5cf8afb97fbbcc787da643fd58d14482675f8` |
| ordered_tree_insert_rebalance | `0x00652550` | `0x0065292F` | 991 | `0x00251950` | `868ba1b4f464944d421e4f1f19e1893641874ce64a67221c247e2fba78c75a03` |
| ordered_tree_iterator_advance | `0x00767170` | `0x007671F4` | 132 | `0x00366570` | `cf948a67e84ac3e0a9d0db0909efebefb9a7364c7550adb552c9b23353e48de8` |

The complete 239-byte target decodes into the pinned 16-block CFG below and has three `ret 8` exits (`0x00652AC0`, `0x00652B05`, `0x00652B1C`). Its complete direct-call set is `0x00652AA0 -> 0x00652550`, `0x00652AC3 -> 0x00767170`, and `0x00652AE5 -> 0x00652550`; the only exact imported call in the body is `0x00652A8B -> [0x00C3B4C0]` (`_invalid_parameter_noinfo`). No call reaches wire primitive `0x0089A600` or `0x0089A640`.

Structurally, the helper walks children at node `+0x00/+0x08`, compares the caller-stack key with node `+0x0C`, checks the sentinel byte at `+0x15`, inserts/rebalances through fixed helper `0x00652550`, advances through `0x00767170`, and writes only the caller-provided result object at `+0/+4/+8` plus the ordered-tree state. This is structure, not a key/value semantic label.

## Exact CFG branches

| site | taken | fallthrough |
|---:|---:|---:|
| `0x00652A4D` | `0x00652A6E` | `0x00652A4F` |
| `0x00652A5F` | `0x00652A65` | `0x00652A61` |
| `0x00652A63` | `0x00652A68` | N/A |
| `0x00652A6C` | `0x00652A51` | `0x00652A6E` |
| `0x00652A7C` | `0x00652AD0` | `0x00652A7E` |
| `0x00652A85` | `0x00652A8B` | `0x00652A87` |
| `0x00652A89` | `0x00652A91` | `0x00652A8B` |
| `0x00652A97` | `0x00652AC3` | `0x00652A99` |
| `0x00652AD5` | `0x00652B08` | `0x00652AD7` |

Basic-block starts: `0x00652A30`, `0x00652A4F`, `0x00652A51`, `0x00652A61`, `0x00652A65`, `0x00652A68`, `0x00652A6E`, `0x00652A7E`, `0x00652A87`, `0x00652A8B`, `0x00652A91`, `0x00652A99`, `0x00652AC3`, `0x00652AD0`, `0x00652AD7`, `0x00652B08`.

## Caller provenance and stream separation

Every serializer uses stream formal `entry+0x4` and mode formal `entry+0x8`. The target receives neither formal: `ECX` is the member below, arg1 is a caller-stack result object, and arg2 is a caller-stack key/value object populated after primitive reads.

| caller/messages | span | target call | target ECX | stream reaching definition | source |
|---|---|---:|---|---|---|
| `ServerAddedInfoVital` | `0x005EBCF0-0x005EBE33` / `f3608dd2456f8577a585e35164b6990d465abb1ffd73697ff7f103e4cbd34960` | `0x005EBE1C` | `this+0x14` | stream `entry+0x4`, mode `entry+0x8` | IMAGE |
| `GSSS_GuildDataVitalRes`, `GSSS_GSInitialGuildDataVital` | `0x0066A320-0x0066A708` / `382d44de2e5bcdcfcba329d8a9a8a720f07276d1f49b819a7ce228fd99ca1abd` | `0x0066A6F1` | `this+0x40` | stream `entry+0x4`, mode `entry+0x8` | IMAGE |
| `ItemMallUpdatePersonalDataVital` | `0x006B0D20-0x006B0FBC` / `142b0ecac21efcf62367aec12d0dfab558c0bdd66428b8f2922a6b89367cd664` | `0x006B0F27` | `this+0x1C` | stream `entry+0x4`, mode `entry+0x8` | IMAGE |
| `ItemMallIMSDataRes` | `0x006BBFD0-0x006BC31C` / `50847a94f2ee128fac0e442bfaeea35688fd77c8d3b72ea5e80793a3c23475db` | `0x006BC27D` | `this+0x70` | stream `entry+0x4`, mode `entry+0x8` | IMAGE |
| `CHitParadeVital` | `0x00716220-0x007163F8` / `7cbbd7d8212c9102e8e026592559fb33c4322e8ff214b0f0a5ec906e39feac5c` | `0x007163E1` | `this+0x284` | stream `entry+0x4`, mode `entry+0x8` | IMAGE |
| `CCooldownAttr` | `0x006C9DC0-0x006C9F4A` / `4d40cadb26437db551ef308732c53a30eddc7429174ee53cb966cbf474a5bd0d` | `0x006C9F33` | `this+0x2C` | stream `entry+0x4`, mode `entry+0x8` | IMAGE |
| `DailyActivityState` | `0x0069CB20-0x0069CC63` / `28f27bb1158748030e9876e896e729d3b6fe1d18a988f7e90ed1d7b0745e31ca` | `0x0069CC4C` | `this+0x28` | stream `entry+0x4`, mode `entry+0x8` | IMAGE |

The two corrected Attr callers follow the same convention: `CCooldownAttr` parses `(i16,f32)` before inserting into `this+0x2C`; `DailyActivityState` parses `(u32,u8)` before inserting into `this+0x28`. Those are raw widths only, not meanings.

## Priority status after removing only this target

| message | priority | status | residual blockers (0x00652A30 removed) |
|---|---:|---|---|
| `ServerAddedInfoVital` | 1 | OPEN | `invalid_parameter_import_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved` |
| `GSSS_GuildDataVitalRes` | 1 | OPEN | `atomic_target_object_alias_unproved | atomic_target_pointer_alias_unproved | critical_section_pointer_alias_unproved | exact_direct_import_call_wire_effect_unproved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | locked_mutable_dword_slot_nested_target_and_alias_unproved | locked_mutable_pointer_slot_nested_target_and_alias_unproved | mutable_chain_target_object_alias_unproved | mutable_dword_range_nested_target_and_alias_unproved | mutable_pointer_slot_traversal_alias_unproved` |
| `GSSS_GSInitialGuildDataVital` | 1 | OPEN | `atomic_target_object_alias_unproved | atomic_target_pointer_alias_unproved | critical_section_pointer_alias_unproved | exact_direct_import_call_wire_effect_unproved | indirect_call_not_proven_serializer_slot | invalid_parameter_import_call_wire_effect_unproved | locked_mutable_dword_slot_nested_target_and_alias_unproved | locked_mutable_pointer_slot_nested_target_and_alias_unproved | mutable_chain_target_object_alias_unproved | mutable_dword_range_nested_target_and_alias_unproved | mutable_pointer_slot_traversal_alias_unproved` |
| `ItemMallUpdatePersonalDataVital` | 1 | OPEN | `invalid_parameter_import_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved` |
| `ItemMallIMSDataRes` | 1 | OPEN | `atomic_target_object_alias_unproved | dynamic_vtable_plus_0x04_target_unresolved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved | mutable_dword_slot_nested_targets_and_alias_unproved` |
| `CHitParadeVital` | 1 | OPEN | `atomic_target_pointer_alias_unproved | exact_direct_import_call_wire_effect_unproved | invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | locked_mutable_dword_slot_nested_target_and_alias_unproved | locked_mutable_pointer_slot_nested_target_and_alias_unproved | mutable_chain_target_object_alias_unproved` |
| `CCooldownAttr` | 3 | OPEN | `invalid_parameter_import_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved` |
| `DailyActivityState` | 3 | OPEN | `invalid_parameter_import_call_wire_effect_unproved | invalid_parameter_singleton_register_call_wire_effect_unproved | mutable_chain_target_object_alias_unproved` |

## Nonclaims and stop rule

- No tree key/value meaning, gameplay meaning, runtime behavior, capture agreement, or server behavior is claimed.
- No other blocker is removed merely because it appears in the same serializer.
- Stop at this exact helper and its seven proven callers. Resume only if another effective A2 layer adds a new `0x00652A30` row or if independent evidence resolves one of the listed residual blockers.
