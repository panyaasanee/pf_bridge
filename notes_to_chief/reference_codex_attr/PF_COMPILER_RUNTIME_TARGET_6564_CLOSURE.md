# PF reviewed compiler-runtime and container-helper closure

[MEASURED] IMAGE-only additive correction. Frozen V1 and every earlier overlay remain unchanged.

## Outcome

- Removed **48 guarded compiler-runtime analysis rows**: 24 frozen-V1 plus 24 slot-0x34 rows, W 24/R 24.
- Removed **32 fixed container-helper rows**: 16 frozen-V1 plus 16 slot-0x34 rows.
- Removed **4 recursive node-delete helper rows** in a separate overlay. This target self-recurses and reaches only the exact `operator delete` import thunk.
- Emitted **7 changed Priority rows** and **0 unchanged copies**. The seven reviewed messages move from OPEN to CLOSED.
- The invalid-parameter removal is intentionally not global. Of 638 raw frozen-V1 rows, three were already removed by `PF_A2_POST_V1_STATIC_DELTA.tsv`; 635 remain effective before this overlay. Together with 296 slot-0x34 rows that is 931 effective rows, but only the 48 rows whose 18 exact call sites pass the pinned per-site guard/container proof are removed here.
- W/R rows are path-insensitive analysis rows. Their presence does not assert that each guard call executes in both modes.

## Publication and acceptance boundary

Normal publication holds the exclusive O_EXCL lock `.PF_V3_COMPILER_PUBLISH.lock`, stages and byte-verifies the complete five-file compiler set, journals each destination before replacement, rolls back on a caught failure, verifies every final byte, and writes this report last within that set. A hard kill intentionally leaves the lock stale so a later compiler publisher fails closed.

This five-file transaction is not the V3 acceptance marker. Root owns `PF_V3_MANIFEST.md` and must write it last only after all same-generation A2/Priority/status/validation artifacts pass their hash checks. Consumers must reject V3 whenever `PF_V3_MANIFEST.md` is absent or any manifest hash check fails.

## Duplicate accounting

| category | raw/source rows | already removed | emitted | unchanged copied | exact/key/semantic duplicate | source |
|---|---:|---:|---:|---:|---:|---|
| invalid import, frozen V1 | 638 | 3 | 24 | 0 | 0 | IMAGE |
| invalid import, slot-0x34 | 296 | 0 | 24 | 0 | 0 | IMAGE |
| three fixed targets, frozen V1 | 16 | 0 | 16 | 0 | 0 | IMAGE |
| three fixed targets, slot-0x34 | 16 | 0 | 16 | 0 | 0 | IMAGE |
| recursive node-delete target 0x00656690, frozen V1 | 4 | 0 | 4 | 0 | 0 | IMAGE |
| Priority effective changes | 7 | 0 | 7 | 0 | 0 | IMAGE |

The three excluded frozen-V1 rows are exactly `CTracePathVital` lines 5493-5495. Re-emitting them would be duplicated output; the generator requires their existing base-row-keyed removal and excludes them.

## Exact import and per-site guard proof

All 18 eligible sites are executed-decoder-confirmed exact direct `FF 15 C0 B4 C3 00` calls. PE import metadata resolves IAT `0x00C3B4C0` / file offset `0x008398C0` to `MSVCR90.dll!_invalid_parameter_noinfo` with descriptor `0x00C112DC`, lookup `0x00C118B4`, DLL name `0x00C1647C`, and symbol name `0x00C15C62`. Register-indirect and unknown targets are excluded.

The imported operation has no parameters. Each eligible call is additionally pinned behind a local null/identity/boundary guard in one of the five serializers below; no stream formal is passed to the call. The same pinned serializer reaches one or more of the fully closed container helpers. This per-site conjunction, not the import name alone, is the removal proof.

| serializer/messages | span | exact guard sites | fixed container calls | source |
|---|---|---|---|---|
| `ActorLearnedPetsSkillData` | `0x006FDF60-0x006FE058` / `357587a20115fd3ad22ff55a74dca38b4c6a3d96f69eed10ba79078b45502068` | `0x006FDFB6`, `0x006FDFCA`, `0x006FDFD9` | `0x006FDFF6->0x006564E0`, `0x006FE041->0x006FDB40` | IMAGE |
| `CBuffConditionState` | `0x00656D50-0x00656F78` / `61c60d54d3f48380c611981a0e8338c7ecb01c689499498a3d7d46c0c4aec917` | `0x00656DAE`, `0x00656DBC`, `0x00656DC7`, `0x00656E2E`, `0x00656E40`, `0x00656E4B` | `0x00656DE2->0x006564E0`, `0x00656E66->0x006564E0`, `0x00656E85->0x00656690`, `0x00656EAC->0x00656690`, `0x00656F0D->0x00656C50`, `0x00656F5C->0x00656C50` | IMAGE |
| `CollectionEffectData`, `WineFormulaLearningAttr` | `0x006A4DB0-0x006A4EA8` / `cc2032c193ffecffb950bc809b7106f78bdfa4d2824614cc58d86e380ef70fb5` | `0x006A4E06`, `0x006A4E1A`, `0x006A4E29` | `0x006A4E46->0x006564E0`, `0x006A4E91->0x00656C50` | IMAGE |
| `CollectionObj_UpdateCollectEffectVital`, `Winemaking_UpdateLearnedFormulaVital` | `0x006A75A0-0x006A7693` / `8b8ebeaa44a48eb1ca94ee43673e1549db2ee126f2ab537ed403a44c0fc9f525` | `0x006A75EE`, `0x006A7600`, `0x006A760B` | `0x006A7626->0x006564E0`, `0x006A767C->0x00656C50` | IMAGE |
| `NPCAppearAttr` | `0x00737FD0-0x007380CE` / `865dcf2144c2c8a86126bbae7e3ed3e1478a0d062194e4d1a6b5f52c2eaa2930` | `0x00738026`, `0x0073803A`, `0x00738049` | `0x00738066->0x006564E0`, `0x007380B7->0x006FDB40` | IMAGE |

## Fixed container graph

| role | span | bytes | file offset | executed CFG nodes | SHA-256 | source |
|---|---|---:|---:|---:|---|---|
| exception_copy | `0x00401030-0x0040108F` | 95 | `0x00000430` | 27 | `e8a0c69b0a0053ea46a9877c9e1dca61a8671b5c692b5b3d979026bc4a5d4bc6` | IMAGE |
| container_helper_6564E0 | `0x006564E0-0x0065654C` | 108 | `0x002558E0` | 44 | `94ba7836493b15264a81c5dc0024c1a3f3aee209e800a0b8fa3e0fcebf9fb1da` | IMAGE |
| link_assign_6565D0 | `0x006565D0-0x00656622` | 82 | `0x002559D0` | 30 | `0dcc90fdbe7788bf7bac5c3ca2050050ae5ac97f4fa1e74f8f088af6c25a1186` | IMAGE |
| recursive_node_delete_656690 | `0x00656690-0x006566C5` | 53 | `0x00255A90` | 23 | `0f6f28adcef1a035e5f1d8a955aebae23136ad1cb70a657eb30242c0e055a7f2` | IMAGE |
| node_allocate_6566D0 | `0x006566D0-0x0065670B` | 59 | `0x00255AD0` | 18 | `50408a0ab90885dac0d223000ec5d08d25b9cb67e86692058c31c15b4b26ccdb` | IMAGE |
| container_helper_656C50 | `0x00656C50-0x00656D43` | 243 | `0x00256050` | 97 | `efd14b2106dae6cf5c1f8261d0f010c05bbb8c62e65cef4eb509d17a93a9556a` | IMAGE |
| link_walk_6FD510 | `0x006FD510-0x006FD594` | 132 | `0x002FC910` | 52 | `bbe2c604df326e192c3b31e68f8fe502494d84d04d56184c633c30ec137e3f19` | IMAGE |
| link_assign_6FD600 | `0x006FD600-0x006FD64E` | 78 | `0x002FCA00` | 30 | `7ff8c78f5ad1120d6ecba4f07ca7b6add55fe62f91ab19f9e10e2d7ba9039306` | IMAGE |
| container_insert_6FD760 | `0x006FD760-0x006FD94F` | 495 | `0x002FCB60` | 168 | `0f1ee407d8acd21fc881daad2a7af48615d4574868d1b73116828a979bfc6e68` | IMAGE |
| container_helper_6FDB40 | `0x006FDB40-0x006FDC33` | 243 | `0x002FCF40` | 97 | `c10312a3c3ef4689c8488902d74f1bebaa8f7a81f7ca870e1b1a96bafbdc0f01` | IMAGE |
| operator_delete_thunk | `0x00B37952-0x00B37958` | 6 | `0x00736D52` | 1 | `dac5c7df4ee9addc4293b8459a55d2bc3eb5864debafc857fb97c01fbbb07cf8` | IMAGE |
| operator_new_thunk | `0x00B37980-0x00B37986` | 6 | `0x00736D80` | 1 | `026db59c9509fd5984356ee06312c76482b74741604ce391ee977c41473b76e4` | IMAGE |
| cxx_throw_thunk | `0x00B37998-0x00B3799E` | 6 | `0x00736D98` | 1 | `16bf8ff4ff7050398899b806680db04f97c42d1b2f69ba2f4eed563eae73ba16` | IMAGE |

The transitive fixed call graph contains only the executed nodes above and fixed imports/tail thunks for `basic_string<char>` construction/copy, `std::exception` construction, `operator new`, `operator delete`, `_CxxThrowException`, and the guarded `_invalid_parameter_noinfo` operation. Target `0x00656690` has a complete 23-node CFG, self-recurses at `0x006566A7`, and calls the exact `MSVCR90.dll!operator delete(void*)` thunk at `0x006566AF -> 0x00B37952 -> [0x00C3B82C]`. Its two CBuff callers are pinned at `0x00656E85` and `0x00656EAC`: arg1 comes from the two this-derived container node slots (`[EBP+0x38/+0x58]+0x04`) and ECX is the embedded container subobject (`EBP+0x20/+0x40`), not the stream formal. All register-indirect calls in the graph have singleton reaching definitions at exact IAT loads; no unresolved indirect target remains in this graph.

### Executed CFG and non-alias gates

The hash-pinned `pf_extract_protocol.py` source was executed against the pinned IMAGE. It decoded 13 graph spans / 589 CFG nodes and 5 serializer spans / 540 CFG nodes with zero decode errors. The exact graph census is 27 direct/indirect call or tail-jump sites; 4 register-indirect sites have singleton reaching IAT definitions.

For all 14 physical container/delete target callsites, the audit binds ECX and every pushed mutable argument to an exact singleton reaching definition. Stack-address arguments resolve to negative entry-relative locals or to the distinct entry `+0x08` non-stream slot. The one apparent exception is `NPCAppearAttr`: its read path reuses entry `+0x04`, but stream capture `0x00737FD9`, zero-kill store `0x007380A2`, and exact wire-read call `0x007380A6` all dominate target `0x007380B7`; EBP retains the singleton stream definition while the old stack-slot value is killed and replaced. Container and heap-node arguments trace to the entry `this` formal through exact MOV/LEA/ADD chains. Separately, all 7 stream loads resolve to entry stack `+0x04`. This executed kill/reaching-definition boundary, not primitive/literal absence alone, is the target-removal proof.

### Negative byte-pattern census

A whole raw-backed IMAGE byte-pattern census finds 1350 `E8 rel32` patterns targeting `0x0089A600` and 1350 targeting `0x0089A640`. These are raw patterns, not all instruction claims. Intersection with the 13 executed graph spans is **0**. A separate little-endian literal census for both primitive VAs inside those spans is **0**. The negative claim therefore comes from a whole-IMAGE pattern census plus exact span intersection, not from linear-disassembler failure.

## Priority changes

The generator executes hash-pinned `pf_validate_v2_effective_capture.py` (`7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9`) to replay all 8795 effective V2 A2 rows, applies exactly 84 proposed rows in memory by effective evidence key, and rechecks every pinned V2 input before and after. A Priority close is emitted only because all 7 reviewed messages have zero remaining UNKNOWN reasons and at least one non-EMPTY effective tag (measured minimum 4). Raw-table blocker strings are not the closure gate.

| message | priority | effective base | old | new | source |
|---|---:|---|---|---|---|
| `ActorLearnedPetsSkillData` | 1 | `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv:3` / delta `40f425f0e4b2a2bd69af2da289e2fc641bef341b917455b5857f02d11ef58eaa` | OPEN | CLOSED | IMAGE |
| `CollectionObj_UpdateCollectEffectVital` | 1 | `PF_PROTOCOL_PRIORITY.tsv:358` | OPEN | CLOSED | IMAGE |
| `NPCAppearAttr` | 1 | `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv:26` / delta `8f53b2c864649b9cace6ccc28f0e2791fdaefc262d53afd5b176e193823d4a05` | OPEN | CLOSED | IMAGE |
| `Winemaking_UpdateLearnedFormulaVital` | 1 | `PF_PROTOCOL_PRIORITY.tsv:297` | OPEN | CLOSED | IMAGE |
| `CBuffConditionState` | 2 | `PF_PROTOCOL_PRIORITY.tsv:170` | OPEN | CLOSED | IMAGE |
| `CollectionEffectData` | 3 | `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv:13` / delta `c3c30ae9f6d9fee4d2bc2059cc3e981e3a49b88c599df05b6cce41cf749b619c` | OPEN | CLOSED | IMAGE |
| `WineFormulaLearningAttr` | 3 | `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv:38` / delta `b1dea1b523569ffb72af6395c2af7244858d41b478fc243edf03ac40fcc39330` | OPEN | CLOSED | IMAGE |

## Nonclaims and stop rule

- No container key/value meaning, gameplay meaning, runtime behavior, capture agreement, or server behavior is claimed.
- The other 883 effective direct-IAT invalid-parameter rows remain unresolved. This report does not generalize from 18 reviewed sites to them.
- No register-indirect invalid-parameter row and no generic/unknown call target is removed.
- Resume only with a new per-site guard/path/non-alias proof or an independently reviewed proof that safely covers a wider exact set.
