# PF post-V1 static closure overlay

[MEASURED] Every changed/removed row and span hash below is re-derived from the pinned IMAGE and frozen V1 tables by this generator.

This is an additive, IMAGE-only overlay on the frozen V1 tables. It does not rewrite `PF_SERIALIZER_FIELDS.tsv` or `PF_PROTOCOL_PRIORITY.tsv`, and it does not copy unchanged rows.

## Outcome

- Priority 1 static closure moves from 241/365 to **244/365**; remaining open: **121**.
- The three changed messages are `CTracePathVital` (RE-119), `GM_RunGMCommandVital` (RE-088), and `TeleportVital` (RE-090).
- All facts in both TSVs have `source=IMAGE`. No DUMP, CAPTURE, or DATA fact is joined into any row.

## Duplicate-control accounting

| table | added | changed | remove-nonwire directives | unchanged copied | duplicate rejected |
|---|---:|---:|---:|---:|---:|
| A2 delta | 0 | 16 | 26 | 0 | 0 |
| Priority delta | 0 | 3 | 0 | 0 | 0 |
| Combined | 0 | 19 | 26 | 0 | 0 |

Every delta row carries the original V1 line number plus a SHA-256 `base_row_key` over the complete original row. `delta_key` is independently deterministic and unique. The 42 A2 rows target 42 distinct base rows; the priority overlay changes three existing message rows and does not add duplicate messages.

## A2 changes

- `CTracePathVital`: remove seven invalid-parameter fail-fast artifacts and one vector-append artifact from the wire-field census. Refine the 16 existing W/R record rows to the discriminated layout: `u8 +0x16`, signed-width `i16 +0x10/+0x12/+0x14`, raw32 `+0x00`, raw32 `+0x04/+0x08` only for `kind==2`, and raw32 `+0x0C` only for `kind==1`.
- `GM_RunGMCommandVital`: remove two pool-allocation and four reference-count artifacts. The already-present outer presence plus nested `u32,u32,u8,wstring,wstring` rows are not copied into this delta.
- `TeleportVital`: remove four pool-allocation and eight reference-count artifacts. The already-present target/auxiliary/scalar fields are not copied into this delta.

The separate `PF_A2_STRING_WIRE_TAG_DELTA.tsv` supersedes the old `UNTAGGED_*` wording for the exact string helpers (wire tags `0x44`/`0x48`). This overlay does not duplicate those string-tag rows.

## Verified IMAGE spans

| message | role | start VA | end VA (exclusive) | file offset | SHA-256 |
|---|---|---:|---:|---:|---|
| CTracePathVital | writer_container | `0x006EBD50` | `0x006EBE64` | `0x002EB150` | `1940cd4500e3218d701abafa56a82ca6a45b1147143e21e4ad2d97ae27724f28` |
| CTracePathVital | reader_and_wrapper | `0x006EC050` | `0x006EC0FC` | `0x002EB450` | `e2e745981e5b98273fce8e9f2b5158c1af41e4ed329398d8f90568ddbb7bb4a3` |
| CTracePathVital | shared_record_codec | `0x006EB960` | `0x006EBA88` | `0x002EAD60` | `b95745c2130cb09405d30553e0c236b440b3058acab5de779ce67e6a39e19ba8` |
| GM_RunGMCommandVital | outer_codec | `0x00729E10` | `0x00729EB7` | `0x00329210` | `541d82f511ba87d444587da9f217ee7eb436431c21e7cfca6dd026d19a8c8554` |
| GM_RunGMCommandVital | nested_codec | `0x00726C20` | `0x00726CB1` | `0x00326020` | `aa3c7c8d2d92eeee48508da2c26d78e360c612aaa2b682dfb608d7b08493559d` |
| TeleportVital | top_level_codec | `0x005EB470` | `0x005EB609` | `0x001EA870` | `fbe813dbd1f9b94d87ee3c101867e8b12aaa36d69c08e68068c8ff06df990487` |
| TeleportVital | target_codec | `0x005DF250` | `0x005DF2F9` | `0x001DE650` | `ec9a5421ad5304372e440ecbb35184d6e93624444a262b3058569a724df0b5ef` |
| TeleportVital | auxiliary_codec | `0x005DEF10` | `0x005DEFE9` | `0x001DE310` | `105bad91394ee1dc636ef80cfe3444c293a4114d5f371fafe3ebc76ccc049c93` |

## Evidence and output pins

- image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- frozen A2 SHA-256: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- frozen priority SHA-256: `d9174bc27ebc1159a7b66ba3fc36b0d6025ecf72d9d963c3deee9bb780c3de55`
- `PF_A2_POST_V1_STATIC_DELTA.tsv` SHA-256: `96e5a476baad2b0ceda79b2ef47bc5a85189551f76003139e1be4cd034f5afc2`
- `PF_POST_V1_PRIORITY_DELTA.tsv` SHA-256: `69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51`
- RE-119 result SHA-256: `89986128551a0728fc74aa159d9792f508acee46edb1224d583a263e49b5ab22`
- RE-088 result SHA-256: `17f55d3bbcbac891870c487f8e87f029679cae4388e7ae25db6d0bcb15c61565`
- RE-090 result SHA-256: `6c6b898be4220df7a84a42799e121cc1db143dbd5543bd420a50b1e93973a2a0`

## Semantic bounds / nonclaims

1. `CTracePathVital` tag `0x14` remains raw 32-bit, not proven float. Only the signed 16-bit triplet is converted to float by the consumer. Request value 743 remains semantically unresolved.
2. GM scalar, string, and result-byte meanings remain unknown. Structural closure does not prove a live command trigger or natural network direction.
3. Teleport flags and auxiliary-object meanings remain unknown. Pool/refcount calls are nonwire; that does not establish gameplay semantics or natural direction.
4. These three messages remain unvalidated by original live capture where the V1 capture ledger says not observed/static-open. Static closure is not the same as runtime validation or implementation readiness.
5. This overlay does not modify server code, GameClient, V1 artifacts, queue/workflow files, or any DUMP/CAPTURE/DATA output.

## Reproduction

Run `py -3 -B pf_build_post_v1_static_closure.py` from any directory. The generator verifies all input hashes and span hashes, enforces exact row counts and unique keys, logically applies the overlay and rejects residual UNKNOWN tags and field offsets with independent mutation controls, writes each file by atomic replace, and contains no wall-clock value, so repeated runs are byte-deterministic.
