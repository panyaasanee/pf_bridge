# PF V4 effective IMAGE-static priority status

[MEASURED][IMAGE] V4 replays all 519 priority states through V3, DailyActivityState, embedded-child composition, and the static type-identity delta. CAPTURE, DUMP, and DATA remain separate evidence layers.

## Effective result

- Priority 1: **255/365 CLOSED** (69.86%); OPEN 110
- Priority 2: **8/16 CLOSED** (50.00%); OPEN 8
- Priority 3: **71/138 CLOSED** (51.45%); OPEN 67
- Overall: **334/519 CLOSED** (64.35%); OPEN 185
- New structural closures: `DailyActivityState` (P3) and `ActorActivity_UpdateDailyActivityStateVital` (P1).

## Effective A2 and duplicate control

- Stored/reference A2 rows: **8657**; UNKNOWN 3963; generic CALL/JUMP UNKNOWN 1312; direct invalid-parameter UNKNOWN 881.
- A3 numeric-tag frequency remains **4081**.
- Daily removes 12 still-effective rows. Composition removes two directionally impossible rows and replaces four coarse rows with physical child-schema references.
- The reference overlay avoids materializing 76 V3 child rows (52 guild plus 24 daily). After the Daily removals, those references resolve to 64 current child rows; none is copied into parent A2.
- New A2 delta-key overlap: 0; new A2 base-target overlap: 0; unchanged/copied child rows: 0.

## Static registry identity

- ItemAttr base identity is exact at vtable `0x00F0EBB0`; the StallItem `0x00F4A188` polymorphic variant remains separate. Serializer family `{0x0046BD30,0x00766C90}` is known as a set, but neither the 26-row nor the 30-row schema is selected, merged, or copied.
- VitalData base identity is exact at vtable `0x00F0B930`; Channel_MessageVtial remains an exact retained derived class. Its serializer remains UNKNOWN.
- These two A1 identity rows produce zero structural closures. ItemAttr moves from registry blocker to dynamic blocker; VitalData remains a registry blocker narrowed to serializer only.

## Priority-1 OPEN primary blocker groups

| primary group | messages |
|---|---:|
| `CALL_EFFECT_OR_STREAM_PROVENANCE_UNRESOLVED` | 14 |
| `DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED` | 79 |
| `INDIRECT_JUMP_TARGET_UNRESOLVED` | 0 |
| `OBJECT_ALIAS_OR_MUTABLE_GRAPH_UNRESOLVED` | 7 |
| `REGISTRY_IDENTITY_UNRESOLVED` | 10 |

- The OPEN index has 110 rows. 107 rows are byte-identical derived references from V3 and are explicitly not new evidence; three OPEN rows changed and one V3 OPEN row closed.

## A5 boundary

- Schema plans: APPLICABLE 624 / STATIC_OPEN 368 / SCHEMA_NOT_APPLIED 46.
- A5 aggregate remains 22,965 parse-pass / 78,532 static-open / 0 schema-not-applied / 386 mismatch. The canonical TSV remains `PF_V2_FIELD_VALIDATION.tsv`; no duplicate V4 field-validation TSV is emitted.
- The existing 386 CAPTURE mismatches remain red and are not rewritten into IMAGE facts.

## Reproduction and scope

Run `py -3 -B pf_build_v4_effective_status.py --audit-only`, then normal publication, then `--check`. The normal mode uses an exclusive lock, staged transaction, journal-before-replace, rollback, input re-hash, and byte-exact readback.

No server/runtime/dump/capture/workflow/queue/Git file is written or run. All emitted TSV rows use `source=IMAGE`.
