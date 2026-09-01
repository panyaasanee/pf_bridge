# RED: A5 V5 retains static/capture mismatches

[MEASURED][CAPTURE] Full replay of the SHA-256 content-deduplicated corpus against the exact V5 logical plan measured 386 mismatch instances at 3 field locations and 4 field+reason points. IMAGE rows were not edited to fit CAPTURE observations.

| evidence | message | dir | declared field identity | reason | instances |
|---|---|:---:|---|---|---:|
| MEASURED/CAPTURE | `TeleportVital` | R | `BASE:0de634db4db1ff42639f6ded73ce9bfbab8b6a4b50e3ec32c36860dfeb0eb21e;DELTA:88ee2c5ddeac7aff9f0fc73b0eb32f2a77ad060215c59ae11b12d2d364e17563;ORDER:20` | `STRING_TAG` | 190 |
| MEASURED/CAPTURE | `TeleportVital` | W | `BASE:a9a17c82ae3d6f93644f407b6284ec736cead8f6652e010c5852e4900abed0fa;ORDER:4` | `TAG` | 188 |
| MEASURED/CAPTURE | `TradeCmdVital` | W | `BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5` | `TAG` | 6 |
| MEASURED/CAPTURE | `TradeCmdVital` | W | `BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5` | `TRUNCATED_TAG` | 2 |

## V5 replay result

- [MEASURED][CAPTURE] Parser replay measured pass=22965; static-open=78532; schema-not-applied=0; mismatch=386; observed message/direction rows=66.
- [MEASURED][CAPTURE] Full-file SHA-256 inventory control measured 2154 paths, 1509 canonical contents, and 645 rejected exact-content duplicate paths; corpus digest=`c07c81161349de0ef68285cb8319a40b2aae660bbf8bf5dcf6844775f30877ee`.
- [MEASURED][CAPTURE] Exact outcome and mismatch-point equality controls measured no aggregate change from V4.

## V5-touched zero observations

| evidence | message | dir | observed frames | observed instances | validator-derived reason |
|---|---|:---:|---:|---:|---|
| MEASURED/CAPTURE | `ItemMallUpdatePersonalDataVital` | R | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `ItemMallUpdatePersonalDataVital` | W | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `ServerAddedInfoVital` | R | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `ServerAddedInfoVital` | W | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |

[MEASURED][CAPTURE] Scope control: zero observation means no reached outer or nested registry ID for that message+direction in this canonical corpus replay. It is not proof of absence from other runtime sessions or from bytes beyond an earlier unresolved parse boundary. The eight historical V4 zero-observation rows are not copied here.

## IMAGE schema impact

- [MEASURED][IMAGE] Exact full-row-key replay consumed 20/20 unique still-effective V1 rows: five per direction for ServerAddedInfoVital and ItemMallUpdatePersonalDataVital; all rows are source=IMAGE REMOVE_NONWIRE_ROW actions.
- [MEASURED][IMAGE] Stored/reference A2 measured 8637 rows and 3943 UNKNOWN; validation-only logical view measured 8701 rows and 3979 UNKNOWN.
- [MEASURED][IMAGE] Numeric-tag census measured stored A3=4081 and validation-only logical=4103; no A3 row is written.
- [MEASURED][IMAGE] Exact schema planner measured APPLICABLE=628; STATIC_OPEN=364; SCHEMA_NOT_APPLIED=46.

| evidence | message | dir | V4 plan/fields | V5 plan/fields |
|---|---|:---:|---|---|
| MEASURED/IMAGE | `ItemMallUpdatePersonalDataVital` | R | STATIC_OPEN / 14 | APPLICABLE / 9 |
| MEASURED/IMAGE | `ItemMallUpdatePersonalDataVital` | W | STATIC_OPEN / 14 | APPLICABLE / 9 |
| MEASURED/IMAGE | `ServerAddedInfoVital` | R | STATIC_OPEN / 8 | APPLICABLE / 3 |
| MEASURED/IMAGE | `ServerAddedInfoVital` | W | STATIC_OPEN / 8 | APPLICABLE / 3 |

- [MEASURED][IMAGE] Exact plan-key comparison measured no other plan change. ItemAttr candidate schemas remain separate at 26 and 30 rows; VitalData identity activates no V5 A5 schema.

## Canonical singleton and controls

- [MEASURED][CAPTURE] UTF-8 byte equality and SHA-256 measured the generated aggregate identical to `PF_V2_FIELD_VALIDATION.tsv` (`10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806`); no V3, V4, or V5 duplicate A5 TSV exists.
- [MEASURED][OUTPUT-AUDIT] Mutation controls rejected duplicate-header and extra/missing/NUL-cell TSVs; detected restored-row plan/census drift; rejected canonical and duplicate-path instance-only/frame-only touched observations; and detected aggregate output drift. Current-state exactness controls separately enforce unique V5 targets/keys, still-effective base/old contracts, 20 complete removals, ItemAttr/VitalData boundaries, canonical aggregate equality, and exact mismatch-point carry-forward.
- [MEASURED][OUTPUT-AUDIT] Held-handle transaction controls denied a second lock acquisition and pathname unlink/replace while held, verified release did not affect a foreign inode, and injected an interrupt after destination replace that restored prior output or removed newly-created output with zero transaction residue.
- [MEASURED][OUTPUT-AUDIT] Casefold positive/negative controls detect the V5 lock plus temporary/rollback publication residue without treating the final Markdown or forbidden TSV name as transaction residue.
- [MEASURED][IMAGE+CAPTURE] Source-column, independent-plan, and aggregate controls keep IMAGE structure separate from CAPTURE observations; no DUMP or DATA fact is merged.
- [MEASURED][CAPTURE] Report schema and raw-byte regex controls export no capture payload, value, path, or hexdump.

## Pinned inputs

- [MEASURED][OUTPUT-AUDIT] `PF_A2_V5_INVALID_PARAMETER_NONWIRE_DELTA.tsv` SHA-256 `f3d877bbc2f3899d650286df6026d44df6691ef23b78ed3492a45da9c076d277`.
- [MEASURED][OUTPUT-AUDIT] `PF_PRIORITY_V5_INVALID_PARAMETER_DELTA.tsv` SHA-256 `0d02afcbbab22506ef74a3cf50d88dd1dd5e7a2c8b85f9333397275a4996114a`.
- [MEASURED][OUTPUT-AUDIT] `PF_V4_FIELD_VALIDATION.md` SHA-256 `4345387b12cbbe048ee3c3a78c43c15d22f680a5082a25bb8de30359aee75ef7`.
- [MEASURED][OUTPUT-AUDIT] `PF_V5_EFFECTIVE_STATUS.md` SHA-256 `b2606434c86cfb74cae1e96a0116b0091fe6a02fa0e07bbe669cdbb99296c021`.
- [MEASURED][OUTPUT-AUDIT] `PF_V5_INVALID_PARAMETER_CLOSURE.md` SHA-256 `12e5790c149324e971d47aae00dca36a7d369ae58ef45755a9422dc97b7f09ff`.
- [MEASURED][OUTPUT-AUDIT] `PF_V5_P1_OPEN.tsv` SHA-256 `9ce1310cce89b6f0c72381ffe684e5c6558b4ad7191d298c958bee4d28fd533e`.
- [MEASURED][OUTPUT-AUDIT] `pf_build_v5_effective_status.py` SHA-256 `6a465acafe4544bec4f3f00674bcabe8aeb51e76fcbe33b691e8effb8e70cc0e`.
- [MEASURED][OUTPUT-AUDIT] `pf_build_v5_invalid_parameter_closure.py` SHA-256 `3f7c6aa4993aa9fa5f1020c0b14fdc119ab568c7e92249003776111355869d73`.
- [MEASURED][OUTPUT-AUDIT] frozen V4 validator SHA-256 `d2e517b4457af2a0f7983d3b60ad88232fad69af392f8287adbe54bef0d2839a`.
- [MEASURED][IMAGE] GameClient.local.bin size=14759424; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

## Reproduction

[PROPOSED][LOCAL] Run `py -3 -B pf_validate_v5_effective_capture.py --check` for integrity replay. Add `--fail-on-mismatch` for the deliberately red conformance gate.
