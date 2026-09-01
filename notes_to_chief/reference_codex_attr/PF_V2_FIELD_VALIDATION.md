# 🔴 A5 V2 พบ static/capture mismatch

[MEASURED][CAPTURE] ตัวเลขทั้งหมดด้านล่างมาจาก corpus และ effective schema ที่ pin hash ไว้; ข้อเท็จจริง CAPTURE ไม่ถูกเขียนทับเข้า IMAGE rows

พบ **3 field locations / 4 field+reason points / 386 instances** หลังใช้ effective V2 A2 กับ capture ที่ de-duplicate ตาม SHA-256 แล้ว ตาราง IMAGE ไม่ถูกแก้ให้เข้ากับข้อมูลสายจริง

| message | dir | declared field identity | reason | baseline | new | total |
|---|:---:|---|---|---:|---:|---:|
| `TeleportVital` | R | `BASE:0de634db4db1ff42639f6ded73ce9bfbab8b6a4b50e3ec32c36860dfeb0eb21e;DELTA:88ee2c5ddeac7aff9f0fc73b0eb32f2a77ad060215c59ae11b12d2d364e17563;ORDER:20` | `STRING_TAG` | 132 | 58 | 190 |
| `TeleportVital` | W | `BASE:a9a17c82ae3d6f93644f407b6284ec736cead8f6652e010c5852e4900abed0fa;ORDER:4` | `TAG` | 132 | 56 | 188 |
| `TradeCmdVital` | W | `BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5` | `TAG` | 5 | 1 | 6 |
| `TradeCmdVital` | W | `BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5` | `TRUNCATED_TAG` | 2 | 0 | 2 |

`V1:n->WIRE:m` รักษาทั้งหมายเลขแถว field เดิมและ wire-order ที่ overlay ประกาศ; ไม่มีการ renumber หรือสลับ field ให้เข้ากับ capture

ผลนี้เป็น aggregate `source=CAPTURE` เท่านั้น ไม่ส่งออก payload, field value, capture path หรือ hexdump

## Effective schema result

- parse success: 22965 instances
- IMAGE static-open: 78532 instances
- schema not safely applicable: 0 instances
- mismatch: 386 instances / 3 field locations / 4 field+reason points
- baseline canonical claims: pass=11903; static-open=52501; schema-not-applied=0; mismatch=271
- new canonical claims: pass=11062; static-open=26031; schema-not-applied=0; mismatch=115
- reconciliation invariant: V1-schema content-dedup total 101883 = effective 22965 pass + 78532 static-open + 0 schema-not-applied + 386 mismatch; exactly 388 formerly-open instances became 2 pass + 0 schema-not-applied + 386 mismatch, with no instance added or dropped.
- observed message/direction rows emitted: 66 (unobserved 519 x 2 rows are not copied)
- full effective plan census: APPLICABLE=606; STATIC_OPEN=386; SCHEMA_NOT_APPLIED=46

## Capture de-duplication

- inventoried paths: 2154 (671381597 bytes)
- unique full-file SHA-256 contents hashed and de-duplicated at one canonical path each: 1509
- canonical claims split without overlap: baseline=1189 unique contents; new=320 unique contents absent from baseline
- exact-content duplicate paths rejected before claim counting: 645
- duplicate-rejected message instances (audit only, never added to claims): 8 [pass=4; static-open=4; schema-not-applied=0; mismatch=0]
- canonical corpus inventory digest: `c07c81161349de0ef68285cb8319a40b2aae660bbf8bf5dcf6844775f30877ee`
- canonical non-text contents skipped by the packet-text parser: 561
- unique text contents inspected: 948; text contents with no recognized packet blocks and therefore no frames: 556; text contents contributing packet blocks: 392
- PC blocks: 15673; DECOMPRESSED blocks: 61611
- direction mapping is unchanged: `PC=R`, `DECOMPRESSED=W`.
- block/envelope errors: 0; unknown message IDs: 0

## Nested framing

- declared/reached nested instances: 25228/24599
- trailing instances deliberately unresolved after static-open / validator blocker / mismatch: 203 / 0 / 426
- complete collections with no tail / exact runtime zero-mask / other framing unresolved: 5542 / 13879 / 0

## Fail-closed compatibility boundary

- `SUBCALL` is skipped only when later A2 primitives explicitly flatten the same target in the original/current IMAGE trace. A referenced-but-unflattened nested serializer is `SCHEMA_NOT_APPLIED`, never a synthetic PASS.
- `CTracePathVital` retains base trace sequence, declared gaps, `6_ALT`, and `kind==1/2` gates. Field identities are not normalized.
- CAPTURE observed `CTracePathVital R` once with a valid count field and zero records: message/container pass=1, record_instances_observed=0, record_branch_coverage=NONE. This does **not** validate any record-layout or kind branch.
- `ItemAttr` base/derived candidate schemas remain separate inputs. No canonical candidate is chosen or merged; an observed ItemAttr frame would be fail-closed.
- Static-open, validator compatibility blockers, and actual byte/tag mismatch are counted separately.

## Effective A2 overlay bookkeeping

- V1 rows: 6931; effective canonical rows: 8795
- string CHANGED: 408; other CHANGED: 35
- non-wire removals: 160; wrong-slot removals: 114
- slot34 canonical additions retained: 2130; later overlay removals: 8; ItemAttr candidate-only rows excluded from canonical: 56
- unchanged IMAGE rows are consumed in memory but are not copied to a new A2 output.

## Exact input bindings

- `PF_PROTOCOL_REGISTRY.tsv` SHA-256: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv` SHA-256: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_TAG_CENSUS.tsv` SHA-256: `63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a`
- `PF_INPUT_INVENTORY.tsv` SHA-256: `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- `PF_CAPTURE_DELTA_20260830.inventory.tsv` SHA-256: `8a85dd1fff3d608ef0f0777331f9235152d2353e67adc76f4ae6275f8bfe6a3e`
- `PF_A2_STRING_WIRE_TAG_DELTA.tsv` SHA-256: `e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2`
- `PF_A3_TAG_CENSUS_DELTA.tsv` SHA-256: `84f05381d34e81f117fa2c2e6a2bc82afe31932112c055c3ef8de1c8642fef53`
- `PF_A2_POST_V1_STATIC_DELTA.tsv` SHA-256: `96e5a476baad2b0ceda79b2ef47bc5a85189551f76003139e1be4cd034f5afc2`
- `PF_A2_SERIALIZER_SLOT34_DELTA.tsv` SHA-256: `1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334`
- `PF_A3_SERIALIZER_SLOT34_DELTA.tsv` SHA-256: `dd20d6dd263462259f4447357c3796604bce75d1bc9d8e5e200b9bb48b9bad87`
- `PF_A2_POOL_638690_DELTA.tsv` SHA-256: `da2a808073fe61ab962ff641d2597aa47d9177bfbe30eaeefa8e14d1a94b94df`
- `PF_A2_POOL_661FA0_DELTA.tsv` SHA-256: `689d37c6e670402b8e9bff7bac78eeda8093c7a8c3f39c340e145ee6d57bbb4f`
- `PF_A2_POOL_46F4D0_DELTA.tsv` SHA-256: `21c6ca53f12a1d4d299e971d0868aa871b1953eebabfed295af906c2b2c4315e`
- `PF_A2_POOL_46BAA0_READER_DELTA.tsv` SHA-256: `5099d8e6f09ac978c938f13d5059c2b735764ef7ed651ace28f9682880e317fa`
- `PF_TARGET_652A30_A2_DELTA.tsv` SHA-256: `217f7f9854df7412ca942d755c0ed858130954f93c8384185af9719415720592`
- `PF_TARGETS_694790_6B3440_A2_DELTA.tsv` SHA-256: `109c39dc16bf22edc97a607832c448f34aa0e0d7dc8f1dbef33f306e1be44dfe`
- `pf_validate_capture_fields.py` SHA-256: `0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8`
- `../notes_to_chief/20260828_0424_RE-119-RESULT-DISCRIMINATED-PATH-RECORDS-AND-UI-ACTIONS.md` SHA-256: `89986128551a0728fc74aa159d9792f508acee46edb1224d583a263e49b5ab22`
- `GameClient.local.bin` size/SHA-256: 14759424 / `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## Reproduction

Run `py -3 -B pf_validate_v2_effective_capture.py --check` to verify the frozen red report byte-for-byte. Exit 0 means artifact integrity/reproduction passed; it does **not** mean schema conformance because the frozen result contains mismatches. Use `--check --fail-on-mismatch` when a downstream gate must exit nonzero for any observed mismatch.
