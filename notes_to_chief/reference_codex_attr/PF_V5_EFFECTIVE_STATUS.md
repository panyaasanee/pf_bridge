# PF V5 effective IMAGE-static status checkpoint

[PROPOSED][DERIVED] Full V4 A2 and all 519 priority states were replayed before the accepted 20-row removal and two exact P1 transitions were applied.

## Priority result

| claim | priority | V4 | V5 |
|---|---|---:|---:|
| [PROPOSED][DERIVED] | P1 CLOSED / total | 255 / 365 | 257 / 365 |
| [PROPOSED][DERIVED] | P1 OPEN | 110 | 108 |
| [PROPOSED][DERIVED] | P2 CLOSED / total | 8 / 16 | 8 / 16 |
| [PROPOSED][DERIVED] | P3 CLOSED / total | 71 / 138 | 71 / 138 |
| [PROPOSED][DERIVED] | overall CLOSED / total | 334 / 519 | 336 / 519 |
| [PROPOSED][DERIVED] | overall OPEN | 185 | 183 |

## Independently replayed A2 and logical views

| claim | view | rows | UNKNOWN | direct invalid | generic CALL/JUMP | numeric |
|---|---|---:|---:|---:|---:|---:|
| [MEASURED][IMAGE] | stored/reference | 8637 | 3943 | 861 | 1312 | 4081 |
| [MEASURED][IMAGE] | logical validation | 8701 | 3979 | 869 | 1324 | 4103 |

- [MEASURED][IMAGE] Schema plans: APPLICABLE 628; STATIC_OPEN 364; SCHEMA_NOT_APPLIED 46.
- [MEASURED][IMAGE] Composition remains four references plus two removals; no child field is copied into stored A2.
- [MEASURED][IMAGE] ItemAttr variants remain 13R+13W and 15R+15W; VitalData remains withheld with no activated schema.

## Exact closure residuals

| claim | message | direction | effective rows | residual blockers | proven wire rows |
|---|---|:---:|---:|---:|---:|
| [MEASURED][IMAGE] | `ItemMallUpdatePersonalDataVital` | R | 9 | 0 | 8 |
| [MEASURED][IMAGE] | `ItemMallUpdatePersonalDataVital` | W | 9 | 0 | 8 |
| [MEASURED][IMAGE] | `ServerAddedInfoVital` | R | 3 | 0 | 3 |
| [MEASURED][IMAGE] | `ServerAddedInfoVital` | W | 3 | 0 | 3 |

## Priority-1 OPEN blocker groups

| claim | blocker group | rows |
|---|---|---:|
| [PROPOSED][DERIVED] | `CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED` | 12 |
| [PROPOSED][DERIVED] | `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED` | 79 |
| [PROPOSED][DERIVED] | `OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED` | 7 |
| [PROPOSED][DERIVED] | `REGISTRY_IDENTITY_UNRESOLVED` | 10 |

## Duplicate and historical-reference audit

- [MEASURED][OUTPUT-AUDIT] V5 component natural removals are 20/20 unique; physical IMAGE sites are 10 unique pairs with exact R+W legacy-row coverage; priority natural identities are 2/2 unique.
- [MEASURED][OUTPUT-AUDIT] Historical status-key repetition is 113 distinct / 423 occurrences / 310 extras, confined to labelled V2-V5 derived status snapshots.
- [MEASURED][OUTPUT-AUDIT] PF_V5_P1_OPEN.tsv contains 108 byte-identical retained V4 rows and no new evidence row.
- [MEASURED][OUTPUT-AUDIT] Canonical A5 remains PF_V2_FIELD_VALIDATION.tsv; this builder emits no A5 TSV and accepts no V3/V4/V5 duplicate A5 TSV.

## Boundaries

[NONCLAIM][LOCAL] This checkpoint does not claim capture agreement, gameplay behavior, field values, import-wide classification, or a VitalData serializer.

[PROPOSED][LOCAL] Treat PF_V5_P1_OPEN.tsv as a derived navigation snapshot. Evidence remains in the pinned component delta and IMAGE proof report.

[REPRODUCTION][LOCAL] Run `py -3 -B pf_build_v5_effective_status.py --self-test-publication`, then `--self-test-mutations`, `--audit-only`, normal publication, and `--check`.

[DECLARED-SCOPE] Local-only under pf_bridge/external; no client/server runtime, workflow, queue, lease, Git, capture, dump, index, manifest, A5 TSV, or GameClient mutation.
