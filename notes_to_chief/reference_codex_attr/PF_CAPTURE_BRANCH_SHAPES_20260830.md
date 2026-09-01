# PF CAPTURE opaque-length delta — 2026-08-30

[MEASURED] Every path, count, offset, numeric ID, length, and hash below is re-derived from the pinned CAPTURE corpus by this generator.

## Result

This additive report publishes **67 pure-CAPTURE rows**. Every row is a numeric response-envelope/nested-ID/capture-kind/direction/opaque-region-length combination absent from the frozen CAPTURE baseline. **No baseline-existing length is repeated in the TSV.**

The rows are observed, exactly bounded opaque regions. They are not byte interpretations, full IMAGE serializer closures, A2 changes, or assertions about unobserved branches.

## Evidence-layer separation

### IMAGE selection context — Markdown context only

The following IMAGE mapping defines the bounded candidate set. These names are context only and are deliberately absent from every TSV row.

| IMAGE-resolved name | IMAGE protocol ID |
|---|---:|
| `CLearnSkillResultVital` | `0x673C` |
| `CTracePathVital` | `0x2F92` |
| `CreateActorVital` | `0x36CF` |
| `GSCN_LoginProtocol` | `0x453A` |
| `GetWorldInfoVital` | `0x3D4B` |
| `ItemOperateVitalRes` | `0x4C13` |
| `NPCConversation` | `0x31D8` |
| `SelectActorVital` | `0x36EF` |
| `TeleportVital` | `0x25A2` |
| `TradeCmdVital` | `0x23B5` |
| `TradeZoomVital` | `0x2A7A` |
| `UpdateAttrVital` | `0x309A` |
| `UserSetting_UpdateServerSettingVital` | `0x0F01` |

The pinned IMAGE/A2 selection audit observed all thirteen mapped candidates somewhere in the new capture text. Exact response-only numeric isolation succeeded for IDs `0x2A7A`, `0x2F92`, `0x309A`, `0x31D8`, `0x36EF`, `0x4C13`, `0x673C`. The IMAGE-resolved candidates not strictly isolated were `CreateActorVital`, `GSCN_LoginProtocol`, `GetWorldInfoVital`, `TeleportVital`, `TradeCmdVital`, `UserSetting_UpdateServerSettingVital`. This paragraph does not convert a CAPTURE observation into an IMAGE fact.

### CAPTURE-only observations and duplicate census

- New capture delta: 382 files / 76247171 bytes; 353 text files were parsed.
- Extracted blocks: 25394 total (`PC`=5211, `DECOMPRESSED`=20183); extraction errors=0.
- Full-block content dedup across the complete delta: claim-unique=3196; duplicate rejected against baseline=21261; duplicate rejected within delta=937.
- Strict selected response-branch instances=388; strict claim-unique instances=221.
- New opaque lengths published=67; published claim-unique instances=208.
- Baseline-existing opaque-length keys reobserved=6; their delta instances=103; their claim-unique instances=13. These reobservations are census-only and do not appear in the TSV.

| outer ID | nested ID | capture kind | direction | strict instances | claim-unique instances | new lengths published | existing lengths reobserved |
|---:|---:|---|---:|---:|---:|---:|---:|
| `0x6E9D` | `0x2A7A` | `PC` | R | 1 | 0 | 0 | 1 |
| `0x6E9D` | `0x2F92` | `PC` | R | 1 | 1 | 1 | 0 |
| `0x6E9D` | `0x309A` | `PC` | R | 276 | 203 | 62 | 1 |
| `0x6E9D` | `0x31D8` | `PC` | R | 34 | 10 | 1 | 2 |
| `0x6E9D` | `0x36EF` | `PC` | R | 57 | 0 | 0 | 1 |
| `0x6E9D` | `0x4C13` | `PC` | R | 9 | 2 | 0 | 1 |
| `0x6E9D` | `0x673C` | `PC` | R | 10 | 5 | 3 | 0 |

`capture_file_count` counts files contributing claim-unique instances to a newly published length. `dedup_key` hashes only the CAPTURE-observable numeric key. Block, opaque-region, file, and evidence-manifest SHA-256 columns support local audit without exporting proprietary values.

## Exact isolation rule

A row is eligible only when a captured block has numeric outer ID `0x6E9D`, declares exactly one nested numeric ID from the bounded selection set, exposes the fixed wrapper boundary, and ends at the response-only known runtime-zero tail. The bytes between wrapper and tail remain opaque; only their length, offsets, and SHA-256 are exported. Numeric request outer ID `0x6E6F` is excluded fail-closed because its tail boundary remains unresolved.

## Selection-audit limitation and nonclaims

The pinned `pf_validate_capture_fields.py` parser is reused for block extraction and the separate IMAGE selection audit. Its known GT-047 `field_offset` mutation limitation does not affect the pure-CAPTURE row key because no field, tag, width, sequence, name, or serializer interpretation is published. This delta does not repair A2 to fit observed traffic and does not close an IMAGE serializer path.

No dump/capture payload value, raw byte, or hexdump is emitted. Output is limited to numeric IDs, opaque lengths/offsets, counts, paths, and SHA-256 metadata.

## Frozen inputs and integrity

- Baseline CAPTURE text: 918 files / 98590688 bytes; manifest `95f574e49b20957a025fd9d98dcfd888a51a76e2393ea169f99d147e3d69d447`.
- New CAPTURE delta: 382 files / 76247171 bytes; manifest `e738fd72565a2dc4747dc31168091c98eabaf63acd87b522b3fd2b11a328f516`.
- New CAPTURE text: 353 files / 68690435 bytes; manifest `7a2aa6b8b073e6b87d5949e53d8ff1aea790bc9da398e55e1beee9422ae4904c`.
- Input files were hashed before parsing and hashed again before publication; both snapshots matched.

Pinned supporting inputs:

- `PF_INPUT_INVENTORY.tsv`: `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- `PF_PROTOCOL_REGISTRY.tsv`: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_TAG_CENSUS.tsv`: `63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a`
- `PF_DUMP_REQUEST.md`: `5fce70adf071120f8c7cd9739ac52b835d5e4ee9c0f70995dc295fca8199201d`
- `PF_FIELD_VALIDATION.tsv`: `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- `pf_validate_capture_fields.py`: `0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8`
