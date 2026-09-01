# PF 0x00661FA0 fixed-pool closure overlay

[MEASURED] This additive overlay was re-derived from the pinned IMAGE and frozen V1 rows. It contains no dump, capture, or data-layer fact.

## Outcome

- Removed **24** duplicated A2 analysis artifacts (six per target): the pool helper, old-object decrement, and new-object increment each appeared once under R and once under W in V1 even though they are read-branch lifecycle operations, not wire fields.
- Closed exactly **4** Priority-1 messages: `TradeCmdVital`, `GCGS_GuildStorageCmdVital`, `StorageCmdVital`, and `ItemMallBagItemTransfer`.
- Within the explicit overlay chain V1 (241) + the existing post-V1 static delta (3) + this delta (4), Priority 1 moves from **244/365** to **248/365**; open moves from **121** to **117**.
- That 248/365 number is this overlay chain's measured checkpoint, not a promise that a later independent Attr correction or later manifest will keep the same global headline.

## Base-before-delta / duplicate accounting

| table | added | changed | remove-nonwire directives | unchanged copied | duplicate rejected |
|---|---:|---:|---:|---:|---:|
| A2 pool delta | 0 | 0 | 24 | 0 | 0 |
| Priority pool delta | 0 | 4 | 0 | 0 | 0 |

Every directive names the exact frozen V1 line and canonical row SHA-256. The generator also verifies that none overlaps `PF_A2_POST_V1_STATIC_DELTA.tsv`; no unchanged V1 row is copied.

## Why 0x00661FA0 is not a serializer

- The helper's complete CFG is pinned below. Its successful direct-call set is critical-section entry/leave, `malloc`, a fixed constructor, recycled-pointer identity, and an allocation counter. Its allocation-failure path constructs and throws an exception. It has no stream formal and receives only `ECX=0x01030238`, metadata `0x00F0A90C`, and zero at both target call sites.
- Empty-pool and recycled-pool paths both call `0x005DF300`. That constructor hard-codes vtable `0x00F2FE14`; slot `+0x04` is exactly `0x005DFCA0`. The pool-head code-reference census pins all IMAGE code references to `0x01030238/3C/4C`; the only pool-return bodies are the same fixed object's deleting destructor and its size-0x20 exception cleanup.
- In `0x00699910`, `ESI` is the message, the read-path `EBX` is the stream, the helper result becomes `EDI`, old is loaded from `[ESI+0x1C]`, new is stored to `[ESI+0x1C]`, decrement receives old in `ECX`, and increment receives new in `ECX`. `0x006B9EA0` is identical with member `+0x18`. Neither atomic helper can alias the stream reaching definition.
- All four target constructors set the member to null. The only non-null member definition in the two pinned serializer bodies is the fixed helper result. At refcount zero, `0x0088D060` dispatches fixed vtable slot `+0x04` to `0x005DFCA0`; that body performs only base cleanup, pool return, or `free`. Its reachable base cleanup can show `MessageBoxW` on an invalid live-refcount condition but has no stream access.

This proves that the six V1 UNKNOWN rows per message are lifecycle/control artifacts. It does not change any numeric/tagged wire row already present in V1.

## Exact CFG branch pins

| function | branch site | taken target | fallthrough |
|---|---:|---:|---:|
| pool_allocator | `0x00661FD6` | `0x00661FDD` | `0x00661FD8` |
| pool_allocator | `0x00661FE6` | `0x00662071` | `0x00661FEC` |
| pool_allocator | `0x00662000` | `0x0066200D` | `0x00662002` |
| pool_allocator | `0x0066200B` | `0x0066200F` | N/A |
| pool_allocator | `0x00662019` | `0x00662042` | `0x0066201B` |
| pool_allocator | `0x0066207E` | `0x00662089` | `0x00662080` |
| pool_allocator | `0x00662087` | `0x0066208B` | N/A |
| shared_serializer | `0x0069991D` | `0x00699972` | `0x0069991F` |
| shared_serializer | `0x0069995F` | `0x006999EA` | `0x00699965` |
| shared_serializer | `0x006999AC` | `0x006999EA` | `0x006999AE` |
| shared_serializer | `0x006999C6` | `0x006999DF` | `0x006999C8` |
| shared_serializer | `0x006999CA` | `0x006999D1` | `0x006999CC` |
| shared_serializer | `0x006999D6` | `0x006999DF` | `0x006999D8` |
| mall_serializer | `0x006B9EAD` | `0x006B9F02` | `0x006B9EAF` |
| mall_serializer | `0x006B9EEF` | `0x006B9F7A` | `0x006B9EF5` |
| mall_serializer | `0x006B9F3C` | `0x006B9F7A` | `0x006B9F3E` |
| mall_serializer | `0x006B9F56` | `0x006B9F6F` | `0x006B9F58` |
| mall_serializer | `0x006B9F5A` | `0x006B9F61` | `0x006B9F5C` |
| mall_serializer | `0x006B9F66` | `0x006B9F6F` | `0x006B9F68` |

The pool helper has return sites `0x0066206E` and `0x006620A8`, both `ret 8`. The shared serializer returns at `0x0069996F` and `0x006999ED`; the mall serializer returns at `0x006B9EFF` and `0x006B9F7D`.

## Exact direct-call pins

| function | call site | direct target |
|---|---:|---:|
| pool_allocator | `0x00661FCD` | `0x0088D5B0` |
| pool_allocator | `0x00661FDF` | `0x0049DA40` |
| pool_allocator | `0x00661FEE` | `0x0088D020` |
| pool_allocator | `0x00662004` | `0x005DF300` |
| pool_allocator | `0x0066202E` | `0x004160F0` |
| pool_allocator | `0x0066203D` | `0x00B37998` |
| pool_allocator | `0x0066204C` | `0x0088F350` |
| pool_allocator | `0x00662074` | `0x0088D030` |
| pool_allocator | `0x00662082` | `0x005DF300` |
| shared_serializer | `0x0069992B` | `0x0089A600` |
| shared_serializer | `0x0069993A` | `0x0089A600` |
| shared_serializer | `0x00699955` | `0x0089A600` |
| shared_serializer | `0x00699967` | `0x0074CF90` |
| shared_serializer | `0x0069997E` | `0x0089A640` |
| shared_serializer | `0x0069998D` | `0x0089A640` |
| shared_serializer | `0x006999A2` | `0x0089A640` |
| shared_serializer | `0x006999BA` | `0x00661FA0` |
| shared_serializer | `0x006999CC` | `0x0088D060` |
| shared_serializer | `0x006999DA` | `0x0088D050` |
| shared_serializer | `0x006999E5` | `0x0074CF90` |
| mall_serializer | `0x006B9EBB` | `0x0089A600` |
| mall_serializer | `0x006B9ECA` | `0x0089A600` |
| mall_serializer | `0x006B9EE5` | `0x0089A600` |
| mall_serializer | `0x006B9EF7` | `0x0074CF90` |
| mall_serializer | `0x006B9F0E` | `0x0089A640` |
| mall_serializer | `0x006B9F1D` | `0x0089A640` |
| mall_serializer | `0x006B9F32` | `0x0089A640` |
| mall_serializer | `0x006B9F4A` | `0x00661FA0` |
| mall_serializer | `0x006B9F5C` | `0x0088D060` |
| mall_serializer | `0x006B9F6A` | `0x0088D050` |
| mall_serializer | `0x006B9F75` | `0x0074CF90` |
| fixed_deleting_destructor | `0x005DFCA9` | `0x0088D280` |
| fixed_deleting_destructor | `0x005DFCC7` | `0x0088D5B0` |
| fixed_deleting_destructor | `0x005DFCE5` | `0x0049DA40` |

Indirect support calls are separately resolved through the named PE import pins below; the zero-refcount dynamic call is pinned as fixed vtable `0x00F2FE14` slot `+0x04` -> `0x005DFCA0`.

## IMAGE span pins

| role | start VA | end VA (exclusive) | file offset | SHA-256 |
|---|---:|---:|---:|---|
| pool_allocator | `0x00661FA0` | `0x006620AB` | `0x002613A0` | `8e4b55f86fa64a27fe99ad80d60f308fe7889d4c69e767f3fbc94da5e2db91a8` |
| shared_serializer | `0x00699910` | `0x006999EE` | `0x00298D10` | `6f6d5832976137fa98b15ba81b512f64e30d2570f4d93f5311af9e25071540e8` |
| mall_serializer | `0x006B9EA0` | `0x006B9F80` | `0x002B92A0` | `22698df219264aa44bacdf383f50c4f91fa29067b0383f596df62bfecdc407e5` |
| fixed_object_constructor | `0x005DF300` | `0x005DF327` | `0x001DE700` | `df1047a07df1e04411943d6d6fdf7d5aac8fabb5d3fdd8efdddbaa6d7ecdbbff` |
| fixed_object_deleting_destructor | `0x005DFCA0` | `0x005DFCFE` | `0x001DF0A0` | `63a40c4a1594c32fd9e5f6a8787ed4a7750cf790e482f06c6ee64d00e18854f7` |
| refcount_increment | `0x0088D050` | `0x0088D05B` | `0x0048C450` | `6da78a1acc15d9fd5f7b2d620253debf8d8465136165dfb1eae35914b2442845` |
| refcount_decrement | `0x0088D060` | `0x0088D082` | `0x0048C460` | `d3b546ac50ded491a6c5a196138b9691f23d8499298e728925f1afb1f0e7734c` |
| enter_critical_section_wrapper | `0x0088D5B0` | `0x0088D5BA` | `0x0048C9B0` | `281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8` |
| leave_critical_section_wrapper | `0x0049DA40` | `0x0049DA4A` | `0x0009CE40` | `91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366` |
| malloc_thunk | `0x0088D020` | `0x0088D026` | `0x0048C420` | `162556d419434c255a68f63f36f37bea903e3adfe89623720318e28708160b58` |
| recycled_pointer_identity | `0x0088D030` | `0x0088D035` | `0x0048C430` | `99712f5745d56904d51e658eeac81bb39a7a2acb4c8834e9af91b4ef58557a0d` |
| allocation_counter | `0x0088F350` | `0x0088F361` | `0x0048E750` | `0a3399caca8eb23244cf6421ea6ab095933e6187b927739d140fefd8892aeebd` |
| refcount_base_destructor | `0x0088D280` | `0x0088D2F0` | `0x0048C680` | `d914c8eaef424f2988c6b76b6954acbb9247bd4309a2c8f0e09439cc64f1104a` |
| allocation_failure_exception_constructor | `0x004160F0` | `0x0041617F` | `0x000154F0` | `10d12b493a454e4e6cff25218d50705154cfc2e495cbfcab83c05bc6259bba21` |
| cxx_throw_thunk | `0x00B37998` | `0x00B3799E` | `0x00736D98` | `16bf8ff4ff7050398899b806680db04f97c42d1b2f69ba2f4eed563eae73ba16` |
| fixed_pool_sized_cleanup | `0x004FB6A0` | `0x004FB6F2` | `0x000FAAA0` | `42f841be59b2b3527c150aa5e47056f8e3c0fd113a5b08546d1979b359595325` |
| TradeCmdVital_constructor | `0x006645C0` | `0x0066463B` | `0x002639C0` | `7ab8e6d92d9ed20c72c5487aa0d607d1303972e9a7b6b23311e2fc543e1f9cd2` |
| GCGS_GuildStorageCmdVital_constructor | `0x006725F0` | `0x0067266B` | `0x002719F0` | `e9d89c09b1a676938c4dc23f7932425536d1dab1711c3fd72625379280d33980` |
| StorageCmdVital_constructor | `0x006990A0` | `0x0069911B` | `0x002984A0` | `fe18d9ce2eb4d707ec3923e0f96a9dbd0e165a062c16a2f37b95e7ab140c8c9e` |
| ItemMallBagItemTransfer_constructor | `0x006B8950` | `0x006B89CC` | `0x002B7D50` | `dff2e1747a3d586440dbc92100c3bdb564da2db6ec16129896b758f56c81c30b` |
| fixed_vtable_head | `0x00F2FE14` | `0x00F2FE1C` | `0x00B2E214` | `71e27f1ad8c483fcbf8af40c3246d8a1338ebf3cb24f44ccaaed2a91308d2a53` |

## Import pins

| import | IAT VA | IAT file offset | descriptor file offset | lookup file offset | DLL file offset | symbol file offset |
|---|---:|---:|---:|---:|---:|---:|
| `KERNEL32.dll!LeaveCriticalSection` | `0x00C3B168` | `0x00839568` | `0x00C11214` | `0x00C1155C` | `0x00C124EA` | `0x00C122CE` |
| `KERNEL32.dll!EnterCriticalSection` | `0x00C3B16C` | `0x0083956C` | `0x00C11214` | `0x00C11560` | `0x00C124EA` | `0x00C122B6` |
| `KERNEL32.dll!InterlockedExchangeAdd` | `0x00C3B19C` | `0x0083959C` | `0x00C11214` | `0x00C11590` | `0x00C124EA` | `0x00C121A4` |
| `KERNEL32.dll!InterlockedIncrement` | `0x00C3B1B0` | `0x008395B0` | `0x00C11214` | `0x00C115A4` | `0x00C124EA` | `0x00C11FC4` |
| `KERNEL32.dll!InterlockedDecrement` | `0x00C3B1B4` | `0x008395B4` | `0x00C11214` | `0x00C115A8` | `0x00C124EA` | `0x00C11FDC` |
| `USER32.dll!MessageBoxW` | `0x00C3B8F8` | `0x00839CF8` | `0x00C11228` | `0x00C11CEC` | `0x00C126EC` | `0x00C124FA` |
| `MSVCP90.dll!??4?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAEAAV01@PBD@Z` | `0x00C3B43C` | `0x0083983C` | `0x00C1128C` | `0x00C11830` | `0x00C15908` | `0x00C12F66` |
| `MSVCP90.dll!??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ` | `0x00C3B478` | `0x00839878` | `0x00C1128C` | `0x00C1186C` | `0x00C15908` | `0x00C12A86` |
| `MSVCP90.dll!??0?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@PBD@Z` | `0x00C3B480` | `0x00839880` | `0x00C1128C` | `0x00C11874` | `0x00C15908` | `0x00C129E4` |
| `MSVCR90.dll!free` | `0x00C3B4A4` | `0x008398A4` | `0x00C112DC` | `0x00C11898` | `0x00C1647C` | `0x00C15C08` |
| `MSVCR90.dll!_CxxThrowException` | `0x00C3B4C4` | `0x008398C4` | `0x00C112DC` | `0x00C118B8` | `0x00C1647C` | `0x00C15C7E` |
| `MSVCR90.dll!malloc` | `0x00C3B87C` | `0x00839C7C` | `0x00C112DC` | `0x00C11C70` | `0x00C1647C` | `0x00C15BFE` |

The TSV rows remain single-layer `source=IMAGE` facts.

## Guards and nonclaims

- `--check` re-derives all rows and compares all three outputs byte-for-byte.
- Independent mutation controls must reject: constructor-vtable drift, helper-call target drift, member-store displacement drift, vtable `+0x04` drift, import-name drift, a missing directive, a duplicate directive, and a synthetic residual blocker.
- Closure means static wire structure only. Runtime behavior, gameplay meaning, capture validation, and dump identity are not promoted.
- No raw proprietary byte sequence is emitted; outputs contain only addresses, structure, counts, and SHA-256 values.

## Output hashes

- `PF_A2_POOL_661FA0_DELTA.tsv`: `689d37c6e670402b8e9bff7bac78eeda8093c7a8c3f39c340e145ee6d57bbb4f`
- `PF_PRIORITY_POOL_661FA0_DELTA.tsv`: `3ba436e9b4876a1575a6d5544f49bb462896e2c6ae4191e085eacb56788ef880`

All TSV rows have `source=IMAGE`.
