# RED: A5 V4 retains static/capture mismatches

[MEASURED][CAPTURE] The canonical content-deduplicated replay retains 386 mismatch instances at 3 field locations and 4 field+reason points. IMAGE rows were not edited to fit CAPTURE observations.

| evidence | message | dir | declared field identity | reason | instances |
|---|---|:---:|---|---|---:|
| MEASURED/CAPTURE | `TeleportVital` | R | `BASE:0de634db4db1ff42639f6ded73ce9bfbab8b6a4b50e3ec32c36860dfeb0eb21e;DELTA:88ee2c5ddeac7aff9f0fc73b0eb32f2a77ad060215c59ae11b12d2d364e17563;ORDER:20` | `STRING_TAG` | 190 |
| MEASURED/CAPTURE | `TeleportVital` | W | `BASE:a9a17c82ae3d6f93644f407b6284ec736cead8f6652e010c5852e4900abed0fa;ORDER:4` | `TAG` | 188 |
| MEASURED/CAPTURE | `TradeCmdVital` | W | `BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5` | `TAG` | 6 |
| MEASURED/CAPTURE | `TradeCmdVital` | W | `BASE:08b5331568ca54ed10ef6b268a475d83c6ee33856efe4ff67110d6ba6a57e7fa;ORDER:5` | `TRUNCATED_TAG` | 2 |

## Replay result

- [MEASURED][CAPTURE] Full parser replay against the pinned corpus digest and exact logical-plan census measured parse success=22965; static-open=78532; schema-not-applied=0; mismatch=386; observed message/direction rows=66.
- [MEASURED][CAPTURE] Full-file SHA-256 inventory/canonical-path control measured 2154 paths; canonical unique contents=1509; exact-content duplicate paths rejected=645; canonical corpus digest=`c07c81161349de0ef68285cb8319a40b2aae660bbf8bf5dcf6844775f30877ee`.
- [MEASURED][CAPTURE] Fresh aggregate lookups after canonical plus duplicate-path replay measured zero observations for all 8 V4-touched message/direction keys.
- [MEASURED][CAPTURE] Exact mismatch-point equality against the frozen V3 control measured only TeleportVital R STRING_TAG, TeleportVital W TAG, and TradeCmdVital W TAG/TRUNCATED_TAG; no point was hidden or renumbered.

| evidence | message | dir | observed frames | observed instances | validator-derived zero-observation reason |
|---|---|:---:|---:|---:|---|
| MEASURED/CAPTURE | `ActorActivity_UpdateDailyActivityStateVital` | R | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `ActorActivity_UpdateDailyActivityStateVital` | W | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `CGuildStorageAttr` | R | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `CGuildStorageAttr` | W | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `DBSS_GuildStorageInitialVital` | R | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `DBSS_GuildStorageInitialVital` | W | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `DailyActivityState` | R | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |
| MEASURED/CAPTURE | `DailyActivityState` | W | 0 | 0 | `NO_REACHED_OUTER_OR_NESTED_REGISTRY_ID_DIRECTION_IN_CANONICAL_SHA256_CONTENT_DEDUP_REPLAY` |

[MEASURED][CAPTURE] Scope control: zero observation means the validator recorded no reached outer or nested registry ID for that message+direction in the canonical SHA-256 content-deduplicated replay. It does not prove absence from other runtime sessions or from bytes beyond an earlier unresolved parse boundary.

## IMAGE schema views

- [MEASURED][IMAGE] Strict base-key/action replay over the pinned V3 effective view measured stored/reference A2 rows=8657; UNKNOWN rows=3963; Daily removals=12; composition references changed=4; directionally impossible rows removed=2.
- [MEASURED][IMAGE] In-memory expansion with exact parent delta, child identity, serializer-target, and native-target-text controls measured validation rows=8721; UNKNOWN rows=3999. No expanded child row is written to A2.
- [MEASURED][IMAGE] The schema planner over that controlled in-memory view measured APPLICABLE=624; STATIC_OPEN=368; SCHEMA_NOT_APPLIED=46.
- [MEASURED][IMAGE] Numeric-tag full-match census measured stored physical A3 frequency=4081 and expanded validation-only frequency=4103; the expanded value is not written to A3.
- [MEASURED][IMAGE] Strict classmap source/schema/hash controls measured IMAGE identity only; exact per-variant field counts keep ItemAttr separate (VTABLE_0x00F0EBB0=26; VTABLE_0x00F4A188=30), and plan equality shows VitalData identity activates no A5 schema.

| evidence | parent | dir | child | exact serializer target | measured child rows | measured child UNKNOWN | native target links |
|---|---|:---:|---|---:|---:|---:|---:|
| MEASURED/IMAGE | `ActorActivity_UpdateDailyActivityStateVital` | R | `DailyActivityState` | `0x0069CB20` | 6 | 0 | 5 |
| MEASURED/IMAGE | `ActorActivity_UpdateDailyActivityStateVital` | W | `DailyActivityState` | `0x0069CB20` | 6 | 0 | 5 |
| MEASURED/IMAGE | `DBSS_GuildStorageInitialVital` | R | `CGuildStorageAttr` | `0x00469FA0` | 26 | 18 | 23 |
| MEASURED/IMAGE | `DBSS_GuildStorageInitialVital` | W | `CGuildStorageAttr` | `0x00469FA0` | 26 | 18 | 23 |

## Duplicate and evidence controls

- [MEASURED][CAPTURE] UTF-8 byte-equality plus SHA-256 control measured the generated aggregate identical to `PF_V2_FIELD_VALIDATION.tsv` SHA-256 `10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806`; existence control measured no `PF_V4_FIELD_VALIDATION.tsv`, so V2 remains canonical.
- [MEASURED][IMAGE] Strict action/source/base-target checks measured only exact CHANGED/removal actions in Daily and composition inputs; row-count and key controls measured zero copied child rows.
- [MEASURED][IMAGE] Pinned component `--check` exit/marker controls passed for Daily, embedded-child composition, and static type-info classmap; before/after SHA-256 control measured the client image unchanged.
- [MEASURED][IMAGE+CAPTURE] Strict source-column and independent-plan/aggregate controls keep IMAGE structure separate from CAPTURE observations; source-census checks measured no DUMP or DATA identity in these rows.
- [MEASURED][CAPTURE] Raw-byte regex plus report-schema control permits counts, names, identities, addresses, and SHA-256 only; it measured no payload, field value, capture path, or hexdump in this output.

## Pinned V4 components

- [MEASURED][IMAGE] `PF_A2_DAILY_ACTIVITY_NONWIRE_DELTA.tsv` SHA-256 `10b54ee781ad0147d5bd18c0171b88132d9fd61dc39e0adf6fa4055bc7b7890d`.
- [MEASURED][IMAGE] `PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv` SHA-256 `b81c7a5590d60c44f10e4171a722feb680e0e83865e6c5c033121e9dccffbe00`.
- [MEASURED][IMAGE] `PF_DAILY_ACTIVITY_CLOSURE.md` SHA-256 `7a58caf4efb025c0703fa4a583785cb0d7d61269d4d92ddf18118da299bfc75e`.
- [MEASURED][IMAGE] `PF_EMBEDDED_CHILD_COMPOSITION.md` SHA-256 `4801b0412a164a53b524d96ddcb7800a56c59ad8447e83f4a3d11f88cfc0bd69`.
- [MEASURED][IMAGE] `PF_PRIORITY_DAILY_ACTIVITY_DELTA.tsv` SHA-256 `395b1776d3351304612ceb36eade9003b929fb8bb914986b4873f0737e60a5e3`.
- [MEASURED][IMAGE] `PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv` SHA-256 `048216205e1a99a1b4561bf643e1ad80bcf1a29283a4b526ee048654fac82d44`.
- [MEASURED][IMAGE] `PF_STATIC_TYPE_INFO_CLASSMAP.md` SHA-256 `b26f4060b6644c9653de37db0db0bf87afbcc8e8d7d9fc98f705723db221c8e2`.
- [MEASURED][IMAGE] `PF_STATIC_TYPE_INFO_CLASSMAP.tsv` SHA-256 `b5de29afb7c7af3c5b785130fdf368b4e1d089d0945441671201880f4429dea2`.
- [MEASURED][IMAGE] `pf_build_daily_activity_closure.py` SHA-256 `e58f4da41e6f82c9a3c182961019394ebab4b8034e1d39f2c8c92b272a35d09d`.
- [MEASURED][IMAGE] `pf_build_embedded_child_composition.py` SHA-256 `a8963458bc15fa13e7a60adf79fc75ae5183937af88ffa9a05602fbc9f8f7bba`.
- [MEASURED][IMAGE] `pf_build_static_type_info_classmap.py` SHA-256 `e25a45a13ad9b010ede4b155f219f791585e93a7637e27ae51348050f231c276`.
- [MEASURED][IMAGE] `GameClient.local.bin` size=14759424; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- [MEASURED][IMAGE] frozen V3 validator SHA-256 `3d145407c9a6e4236eefe829c9fb9eb0757bf53cce9ac9cb136f201f594a360b`.

## Reproduction

[PROPOSED][LOCAL] Run `py -3 -B pf_validate_v4_effective_capture.py --check` for integrity replay. Run the same command with `--fail-on-mismatch` for the deliberately red conformance gate.
