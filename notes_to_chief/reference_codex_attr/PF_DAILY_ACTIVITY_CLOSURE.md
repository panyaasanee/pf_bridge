# PF IMAGE closure: DailyActivityState non-wire rows

[MEASURED] IMAGE-only additive correction built from the exact effective V3 A2.

## Outcome

- Removed 12 effective UNKNOWN analysis rows: 6 W + 6 R over exactly 6 physical sites.
- DailyActivityState Priority 3 changes OPEN -> CLOSED for serializer and structural status.
- Residual effective schema has 6 W + 6 R rows, zero UNKNOWN reasons, and non-empty fields in both directions.
- Closure is gated by one executable predicate over tag, offset, length, order, gate, and subcall flattening; built-in mutations of all six dimensions are rejected.
- source=IMAGE on every emitted TSV row; no capture, dump, data, runtime, or server claim is mixed in.
- Duplicate accounting: 0 repeated base targets, 0 prior provenance-key collisions, and 0 unchanged/copied rows.

## Exact proof boundary

| role | VA span | bytes | file offset | SHA-256 | executed CFG |
|---|---|---:|---:|---|---|
| DailyActivityState serializer | `0x0069CB20-0x0069CC63` | 323 | `0x0029BF20` | `28f27bb1158748030e9876e896e729d3b6fe1d18a988f7e90ed1d7b0745e31ca` | 117 nodes / 126 edges / 0 errors |
| stack-local link-state helper | `0x00B0BF70-0x00B0BFDC` | 108 | `0x0070B370` | `4e1374fd126457c82d11bf3e6efa0fda845bb85e2c2a985ed67c4eff3f4eb7e6` | 44 nodes / 49 edges / 0 errors |

The complete serializer stack fixed point has one entry-relative depth at every decoded node. All six reviewed sites have depth 0x28. The only semantic ESP-LEA override is exact bytes `8D642400` at `0x0069CB6C`, which is the identity `ESP := ESP+0`. The EBP proof carries an explicit entry-undefined sentinel and separately requires `0x0069CB90` to dominate all four register-indirect calls, so a bypass path cannot disappear at a set union.

| physical site | classification | entry-relative stack depth | rows removed |
|---:|---|---:|---:|
| `0x0069CB82` | direct PE import `MSVCR90.dll!_invalid_parameter_noinfo` | `0x28` | 2 |
| `0x0069CB9A` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |
| `0x0069CBA3` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |
| `0x0069CBB8` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |
| `0x0069CBBF` | EBP call; singleton IAT definition `0x0069CB90` | `0x28` | 2 |
| `0x0069CBD4` | stack-local receiver into helper `0x00B0BF70` | `0x28` | 2 |

At `0x0069CBD0`, `lea ecx,[esp+0x14]` at depth 0x28 proves receiver `entry_SP-0x14`. The helper copies entry ECX to ESI, and its exact three explicit writes (`0x00B0BFAB`, `0x00B0BFC8`, `0x00B0BFD7`) are all `[ESI+4]`, therefore target `entry_SP-0x10`. The helper receives no stack argument or stream formal; this local target is structurally distinct from the stream formal slot at `entry_SP+0x04` and the entry object receiver.

Both helper guard calls have the singleton reaching EDI definition from `[0x00C3B4C0]`, which PE metadata resolves to `_invalid_parameter_noinfo`. The helper graph has 0 direct wire-primitive intersections and 0 wire-address literal hits.

Whole-image raw E8 destination census remains `1350` calls to `0x0089A600` and `1350` calls to `0x0089A640`. This census is a negative-control boundary, not a reason to remove unrelated rows.

## Prior result not duplicated

The two DailyActivityState rows at physical call `0x0069CC4C -> 0x00652A30` (slot34 lines 1003/1004) were already removed by `PF_TARGET_652A30_A2_DELTA.tsv`. They are verified as prior effective removals and are not emitted again. This artifact covers only lines 986-999 listed in its TSV.

## Priority predecessor

The single Priority row chains from `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv:15`, canonical row key `c18d6d65a771b97b112ca8f1d7062c4d204bf8cb9bb87a6a22794737a8b6af13`, predecessor delta key `c4d24d899578ad584b3b13e3f81f4aa051f77f9380ea0c893929080434f8e017`. No base-V1 CLOSED row is reused as the predecessor.

## Nonclaims and stop rule

- No field meaning, gameplay behavior, runtime state, capture agreement, or server behavior is claimed.
- No other invalid-parameter or mutable-helper row is generalized from this serializer.
- Resume only if the pinned IMAGE/V3 effective inputs change or independent evidence identifies another exact still-effective DailyActivityState blocker.
