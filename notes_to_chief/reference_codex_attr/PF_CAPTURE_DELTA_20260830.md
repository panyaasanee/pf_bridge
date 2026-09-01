# PF capture delta 20260830

[MEASURED] Path, hash, disposition, frame, and validation counts below are re-derived from the pinned CAPTURE corpus by this generator.

This is an incremental `source=CAPTURE` batch. It contains no payload values, capture bytes, or hexdumps and does not repeat the 1,772-row v1 inventory or the 1,038-row v1 A5 table.

## Input and de-duplication

- v1 paths verified twice against frozen size/SHA-256: 1772
- current paths: 2154; new paths inventoried: 382; missing v1 paths: 0
- new bytes: 76247171
- unique new content (claim-eligible canonical paths): 320
- exact-content duplicates rejected: 62 path(s) (61 already in v1; 1 aliases within this batch)
- raw new text paths inspected: 353; claim-eligible text paths inspected: 291; non-text new paths: 29
- raw path dispositions: recognized blocks=117; no recognized blocks=236; marker/envelope error=0; non-text=29
- claim-eligible dispositions: recognized blocks=116; no recognized blocks=175; marker/envelope error=0; non-text=29
- Canonical selection is the lexicographically first relative path for each full-file SHA-256. If the SHA-256 already exists in v1, every new alias is excluded from claim counts.

## A5 delta: de-duplicated claim counts

- files containing parseable blocks: 116
- PC blocks: 5211; DECOMPRESSED blocks: 20181
- matched pinned schema: 11061 message instance(s)
- schema not applied: 26147 message instance(s); these are not promoted to matched
- nested declared/reached/unresolved-after-schema-not-applied: 12010/11816/194
- unresolved nested reason: UNRESOLVED_AFTER_SCHEMA_NOT_APPLIED; these trailing instances were not checked for later field mismatches or IDs
- mismatch: 0 instance(s), 0 distinct message/direction/field/reason point(s)
- block/envelope errors: 0; unknown message IDs: 0

## Raw-path comparison (duplicates included only for audit)

- files containing parseable blocks: 117
- PC blocks: 5211; DECOMPRESSED blocks: 20183
- matched pinned schema: 11063 message instance(s)
- schema not applied: 26149 message instance(s)
- nested declared/reached/unresolved-after-schema-not-applied: 12012/11818/194
- mismatch: 0 message instance(s)
- duplicate-rejected message instances: 4

## Delta bookkeeping against v1 A5

- ADDED message/direction rows (not observed in v1, claim-observed here): 8
- CHANGED message/direction rows (already observed in v1, more claim evidence here): 42
- UNCHANGED message/direction rows in the 1,038-key universe: 988
- observed duplicate-only rows rejected from claim evidence: 0

## Message/direction observations first seen in this CAPTURE delta

| message | direction | claim instances | raw instances | CAPTURE outcome |
|---|:---:|---:|---:|---|
| `AbilityDepolyAll` | W | 3 | 3 | MATCHED_PINNED_SCHEMA |
| `CLearnSkillResultVital` | R | 10 | 10 | SCHEMA_NOT_APPLIED |
| `Community_ChangeActorCommentVital` | W | 2 | 2 | MATCHED_PINNED_SCHEMA |
| `CPotionVital` | W | 13 | 13 | MATCHED_PINNED_SCHEMA |
| `CTracePathVital` | R | 1 | 1 | SCHEMA_NOT_APPLIED |
| `DailyRewardVitalReq` | W | 7 | 7 | MATCHED_PINNED_SCHEMA |
| `GM_UpdateGMStateVital` | R | 4 | 4 | MATCHED_PINNED_SCHEMA |
| `ReturnSelectServerVital` | R | 2 | 2 | MATCHED_PINNED_SCHEMA |

This table reports CAPTURE observations only. Priority and serializer closure remain in separate IMAGE-source tables and are not embedded in these rows.

## Guards and bindings

- GT-047 validator SHA-256: `cafa5f69401eaf152f7ae4e646ce76eb3016c3d6b71e76c494819a029877011b`
- GameClient.local.bin SHA-256 before/after: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- v1 input inventory SHA-256: `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- v1 field validation SHA-256: `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- GT-047 parser regression, schema mutation, A2/A3 census, static-open membership, and W/R field-offset mirror guards all passed before parsing.
- Every v1 and new capture path was size/hash checked once before parsing and once again before publication.
- Every frozen external file and the local image were re-hashed after parsing; no frozen artifact changed.
