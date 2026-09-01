# PF V3 effective IMAGE-static priority status

[MEASURED][IMAGE] This is a chained effective index. It emits no copied field rows and treats a prior delta as the required base when that delta is the current state.

CAPTURE remains a separate evidence layer. V3 replay is documented in `PF_V3_FIELD_VALIDATION.md`; its aggregate TSV is byte-identical to canonical `PF_V2_FIELD_VALIDATION.tsv`, so no duplicate V3 TSV is emitted and IMAGE rows are never overwritten.

## Effective structural result

- Priority 1: **254/365 CLOSED** (69.59%); OPEN 111
- Priority 2: **8/16 CLOSED** (50.00%); OPEN 8
- Priority 3: **70/138 CLOSED** (50.72%); OPEN 68
- Overall: **332/519 CLOSED** (63.97%); OPEN 187

## Net-new correction

- Removed 48 guarded `_invalid_parameter_noinfo` analysis-artifact rows, 36 proven fixed container/helper rows, and 40 proven stack-local link-state-helper rows.
- The proposed global 931-row import cleanup was rejected: import identity alone did not satisfy the existing per-call wire-effect ceiling. The 883 unreviewed effective rows remain unresolved.
- The raw V1 import census also exposed three `CTracePathVital` rows already removed by `PF_A2_POST_V1_STATIC_DELTA.tsv`; the dedup audit rejects them as prior output rather than emitting them again.
- Net-new A2 removal targets: 124; duplicate `delta_key`: 0; duplicate/cross-file base-row target: 0; unchanged copies: 0.
- Seven messages close structurally: Priority-1 +4, Priority-2 +1, Priority-3 +2.
- Four of those seven status rows chain from `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv`; using V1 as their base is forbidden and would be duplicate/stale-state output.
- OPEN blocker metadata was rebuilt from final effective A2 for 8 touched messages; no stale removed blocker is copied forward.

## Priority overlay accounting

| overlay | changed rows |
|---|---:|
| `PF_POST_V1_PRIORITY_DELTA.tsv` | 3 |
| `PF_PRIORITY_POOL_638690_DELTA.tsv` | 4 |
| `PF_PRIORITY_POOL_661FA0_DELTA.tsv` | 4 |
| `PF_PRIORITY_POOL_46F4D0_DELTA.tsv` | 4 |
| `PF_PRIORITY_SERIALIZER_SLOT34_DELTA.tsv` | 37 |
| `PF_PRIORITY_COMPILER_TARGET_6564_DELTA.tsv` | 7 |

- Applied rows: 59; distinct messages: 55; legitimate chained messages: 4.
- Cross-file duplicate status base target: 0; duplicate priority `delta_key`: 0.

## Priority-1 OPEN primary blocker groups

| primary group | messages |
|---|---:|
| `CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED` | 14 |
| `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED` | 77 |
| `INDIRECT_JUMP_TARGET_UNRESOLVED` | 2 |
| `OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED` | 7 |
| `REGISTRY_IDENTITY_UNRESOLVED` | 11 |

Exact names and complete blocker strings are in `PF_V3_P1_OPEN.tsv`.

## Duplicate-control contract

- V1 messages: 519 unique; derived output contains only the 111 Priority-1 messages still OPEN.
- Every status change references the exact canonical row and line that was effective immediately before it.
- A chained row also binds the predecessor `delta_key`; no base row or previous result is copied as new evidence.
- Every row remains `source=IMAGE`; CAPTURE, DUMP, and DATA are not joined into this view.

## Reproduction

Run `py -3 -B pf_build_v3_effective_status.py --check` to hash every input, replay the complete status chain, and compare both outputs byte-for-byte.
