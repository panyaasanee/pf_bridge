# A2/A3 string wire-tag correction (additive overlay)

[MEASURED] Counts, addresses, offsets, and hashes below are re-derived from the pinned IMAGE and frozen V1 tables by this generator.

## Result

The 408 V1 A2 rows labelled `UNTAGGED_STRING8_LEN32LE` or
`UNTAGGED_WSTRING16LE_LEN32LE` stop at a helper payload boundary.  The exact
write/read helpers in the pinned IMAGE also emit or consume a one-byte wire tag:
`0x44` for string8 and `0x48` for wstring16le.  Therefore the full field shape is
`tag(1) + uint32le byte_count(4) + payload(N)`, or `5+N_bytes`.

This is an IMAGE-only representation correction.  No dump, capture, or data claim
is mixed into these rows, and no raw proprietary bytes are reproduced here.  The
frozen V1 tables remain unchanged.

## Non-duplicating outputs

| Output | Added rows | Logical changes | Unchanged rows copied | Duplicate rows rejected |
|---|---:|---:|---:|---:|
| `PF_A2_STRING_WIRE_TAG_DELTA.tsv` | 408 | 408 | 0 | 0 |
| `PF_A3_TAG_CENSUS_DELTA.tsv` | 2 | 0 | 0 (11 V1 tag rows remain by reference) | 0 |

Every A2 delta row has a stable SHA-256 `dedup_key` over its V1 row identity
(`message`, direction, order, call file offset, and original tag).  Apply each row
as a correction overlay; do not append it as an additional serializer field.  The
A3 delta contains only the two missing tags, not a copy of the 11-row V1 census.

## Affected census

- A2 delta: 408 unique rows across 101 unique messages.
- string8 / `0x44`: 60 rows (30 W, 30 R).
- wstring16le / `0x48`: 348 rows (174 W, 174 R).
- Priority 1: 384 rows across 92 messages.
- Priority 3: 24 rows across 9 messages.
- Priority 2: 0 rows.

## Exact IMAGE proof

| Kind/direction | Helper VA | Helper file offset | Helper end VA | Tag instruction VA | Tag instruction file offset | Span SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| string8 W (`0x44`) | 0x0089A6D0 | 0x00499AD0 | 0x0089A733 | 0x0089A6F1 | 0x00499AF1 | a0674fb3366720314e20ef5f5dbfa010330b12a73ed4e56e6c43e9d310dce9f1 |
| string8 R (`0x44`) | 0x0089A740 | 0x00499B40 | 0x0089A806 | 0x0089A75C | 0x00499B5C | 90c8c73b3b3c7158af57e374c694730763ab28292130b4f128a4754dec54e76a |
| wstring16le W (`0x48`) | 0x0089A810 | 0x00499C10 | 0x0089A875 | 0x0089A833 | 0x00499C33 | 08d6f27f030f3e0f1a32873d296c7f2c35a9d67f547607cf95c2900a60ffdad4 |
| wstring16le R (`0x48`) | 0x0089A880 | 0x00499C80 | 0x0089A95E | 0x0089A89C | 0x00499C9C | 2f564cb5d4f68d035d9e60fa1a4a5334b0875262420851f463f3f904e22ad978 |

The generator re-hashes every helper span, verifies each tag instruction at the
listed VA/file offset, and verifies that every selected A2 row pins the expected
helper target, span end, SHA-256, direction, string kind, and length-prefix form.

## Pinned inputs

| Input | SHA-256 |
|---|---|
| `GameClient.local.bin` | 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623 |
| `PF_SERIALIZER_FIELDS.tsv` | 99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123 |
| `PF_PROTOCOL_PRIORITY.tsv` | d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55 |
| `PF_TAG_CENSUS.tsv` | 63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a |

`source=IMAGE` applies to every TSV row in this overlay.
