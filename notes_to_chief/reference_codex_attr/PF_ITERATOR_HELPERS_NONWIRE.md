# PF IMAGE closure: stack-local link-state helpers

[MEASURED][IMAGE] Additive removal overlay only. Frozen V1 and every prior overlay remain untouched.

## Outcome

- Removed **40 unique effective V1 A2 analysis rows**: 26 for `0x00B0BF70` and 14 for `0x0046D2B0`.
- The selected cluster has **12 exact physical callsites** (7 + 5), **20 W / 20 R rows**, and **8 unique Priority-1 messages**.
- Duplicate accounting: unchanged/copied rows 0; duplicate base rows 0; duplicate delta keys 0; cross-overlay base/target/delta-key overlaps 0.
- No Priority TSV is emitted. A fresh effective-A2 reconstruction after all prior field overlays finds unresolved rows remaining for every affected message, so this overlay creates no closure transition.
- Scope is intentionally narrower than every row bearing the same tags. Selection requires current V2 Priority-1 OPEN status, primary object/mutable-alias blocker group, an exact pinned callsite, and immediate `lea ecx,[esp+disp8]` immediately before the helper call.

## Helper proof

| helper | span | bytes | file offset | SHA-256 | node flag | state writes | source |
|---|---|---:|---:|---|---:|---|---|
| `chain_plus_04_link_state` | `0x00B0BF70-0x00B0BFDC` | 108 | `0x0070B370` | `4e1374fd126457c82d11bf3e6efa0fda845bb85e2c2a985ed67c4eff3f4eb7e6` | `+0x15` | `0x00B0BFAB, 0x00B0BFC8, 0x00B0BFD7` | IMAGE |
| `pointer_slot_link_state` | `0x0046D2B0-0x0046D31C` | 108 | `0x0006C6B0` | `492e39afb9faf38f4f862abcdaa6278740417a4b1fc1e56d61a6b992421d5cf9` | `+0x21` | `0x0046D2EB, 0x0046D308, 0x0046D317` | IMAGE |

The generator recursively decodes the reachable CFG rather than relying on printed byte pins:

| helper | instruction nodes | basic blocks | covered bytes | decode errors | direct calls | indirect calls | EDI-dominated guards | singleton EDI definitions | mutable writes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `0x00B0BF70` | 44 | 13 | 108 | 0 | 0 | 2 | 2 | 2 | 3 |
| `0x0046D2B0` | 44 | 13 | 108 | 0 | 0 | 2 | 2 | 2 | 3 |

Each complete body has three returns, traverses node links, and writes only the stack-local link-state object's `+0x04` state. Executed dominator and reaching-definition analyses prove that the single EDI load from `[0x00C3B4C0]` dominates both indirect guard calls and is the singleton local EDI definition reaching each call. The pinned PE import table resolves that slot to `MSVCR90.dll!_invalid_parameter_noinfo`.

Those guard calls are used only as part of the helper proof. This overlay does **not** globally remove any invalid-parameter row.

## Exact affected callsites

| target | callsite | file offset | immediate ECX definition | V1 rows | messages | source |
|---:|---:|---:|---|---:|---|---|
| `0x00B0BF70` | `0x0049F83E` | `0x0009EC3E` | `lea ecx,[esp+0x1C]` | 6 | `GSSS_GuildEventVitalReq`, `GSSS_GuildEventVitalRes`, `GSSS_GuildUpdateEventVital` | IMAGE |
| `0x00B0BF70` | `0x0049F954` | `0x0009ED54` | `lea ecx,[esp+0x1C]` | 6 | `GSSS_GuildEventVitalReq`, `GSSS_GuildEventVitalRes`, `GSSS_GuildUpdateEventVital` | IMAGE |
| `0x00B0BF70` | `0x0049FA0E` | `0x0009EE0E` | `lea ecx,[esp+0x1C]` | 6 | `GSSS_GuildEventVitalReq`, `GSSS_GuildEventVitalRes`, `GSSS_GuildUpdateEventVital` | IMAGE |
| `0x00B0BF70` | `0x005EBD9E` | `0x001EB19E` | `lea ecx,[esp+0x10]` | 2 | `ServerAddedInfoVital` | IMAGE |
| `0x00B0BF70` | `0x006B0E40` | `0x002B0240` | `lea ecx,[esp+0x10]` | 2 | `ItemMallUpdatePersonalDataVital` | IMAGE |
| `0x00B0BF70` | `0x007157AC` | `0x00314BAC` | `lea ecx,[esp+0x20]` | 2 | `CHitParadeVital` | IMAGE |
| `0x00B0BF70` | `0x00716316` | `0x00315716` | `lea ecx,[esp+0x10]` | 2 | `CHitParadeVital` | IMAGE |
| `0x0046D2B0` | `0x0049F8C9` | `0x0009ECC9` | `lea ecx,[esp+0x1C]` | 6 | `GSSS_GuildEventVitalReq`, `GSSS_GuildEventVitalRes`, `GSSS_GuildUpdateEventVital` | IMAGE |
| `0x0046D2B0` | `0x006238CE` | `0x00222CCE` | `lea ecx,[esp+0x10]` | 2 | `CArenaGameDataVital` | IMAGE |
| `0x0046D2B0` | `0x006242F7` | `0x002236F7` | `lea ecx,[esp+0x18]` | 2 | `CArenaGameDataVital` | IMAGE |
| `0x0046D2B0` | `0x00625057` | `0x00224457` | `lea ecx,[esp+0x18]` | 2 | `CArenaGameDataVital` | IMAGE |
| `0x0046D2B0` | `0x006E83FC` | `0x002E77FC` | `lea ecx,[esp+0x14]` | 2 | `Express_ClientSendExpressVital` | IMAGE |

Because the LEA is the instruction immediately before each direct E8 call, there is no intervening ECX clobber. Executed helper dataflow copies entry ECX to ESI once; that definition dominates all three mutable writes, each write uses `[ESI+0x04]`, and ESI is restored by `pop` only on exit paths. The body reads no caller-stack formal and accepts no stack argument (plain `ret` at all exits). Therefore the mutable base is the pinned caller-stack link-state object; the stream formal is not received or used by either helper.

Callsite `0x0049FAD4` is deliberately excluded. Although it also has an immediate `lea ecx,[esp+0x1C]`, this artifact does not contain a complete entry-relative stack-depth/call-cleanup proof for that site. Its six V1 rows remain untouched.

## Whole-.text normalized family census

The 108-byte body was scanned across the complete pinned `.text` raw range (`0x00000400+0x00838C00`). Only six node-flag displacement bytes were masked (body offsets 22, 36, 44, 54, 69, 98). The exact normalized family contains **24** members:

`0x004493B0(+0x79)`, `0x00454530(+0x49)`, `0x0046D2B0(+0x21)`, `0x0050B3C0(+0x3D)`, `0x005247E0(+0x55)`, `0x00524850(+0x65)`, `0x005625B0(+0x61)`, `0x0057CEE0(+0x29)`, `0x005D2180(+0x19)`, `0x005DABB0(+0x4D)`, `0x006564E0(+0x0F)`, `0x0065E260(+0x45)`, `0x006835E0(+0x25)`, `0x006F7AE0(+0x31)`, `0x0073AEF0(+0x1D)`, `0x0073AF60(+0x35)`, `0x0073F160(+0x71)`, `0x007424F0(+0x41)`, `0x00745B20(+0x69)`, `0x00765540(+0x39)`, `0x0077ACD0(+0x51)`, `0x00B0BF70(+0x15)`, `0x00B0C5D0(+0x11)`, `0x00B1B8C0(+0x2D)`.

This family census is a structural identity check only. It does not authorize removals at the other 22 members or at unselected callers.

## Whole-image wire-reference census

A raw whole-image byte census (not a linear-disassembler negative) scanned every E8 byte as a mapped rel32 candidate and every little-endian absolute VA pattern:

| primitive | whole-image rel32 byte candidates | absolute-VA dword hits | hits inside either helper |
|---:|---:|---:|---:|
| `0x0089A600` | 1350 | 0 | 0 |
| `0x0089A640` | 1350 | 0 | 0 |

The primitives are abundant elsewhere in the same pinned image, but neither their rel32 byte patterns nor their absolute VAs occur in either helper. The only indirect-call target inside each helper is the fixed guard import proved above.

## Effective A2 residual check after prior overlays

The reconstruction applied these prior A2 overlays before applying the 40 removals in this file: `PF_A2_INVALID_PARAMETER_NONWIRE_DELTA.tsv`, `PF_A2_POOL_46BAA0_READER_DELTA.tsv`, `PF_A2_POOL_46F4D0_DELTA.tsv`, `PF_A2_POOL_638690_DELTA.tsv`, `PF_A2_POOL_661FA0_DELTA.tsv`, `PF_A2_POST_V1_STATIC_DELTA.tsv`, `PF_A2_SERIALIZER_SLOT34_DELTA.tsv`, `PF_A2_STRING_WIRE_TAG_DELTA.tsv`, `PF_A2_TARGETS_6564E0_656C50_6FDB40_NONWIRE_DELTA.tsv`, `PF_A2_TARGET_656690_NONWIRE_DELTA.tsv`, `PF_TARGETS_694790_6B3440_A2_DELTA.tsv`, `PF_TARGET_652A30_A2_DELTA.tsv`.

| message | unresolved W rows remaining | unresolved R rows remaining | closure transition from this overlay |
|---|---:|---:|---|
| `CArenaGameDataVital` | 35 | 35 | NO |
| `CHitParadeVital` | 40 | 40 | NO |
| `Express_ClientSendExpressVital` | 6 | 6 | NO |
| `GSSS_GuildEventVitalReq` | 73 | 73 | NO |
| `GSSS_GuildEventVitalRes` | 73 | 73 | NO |
| `GSSS_GuildUpdateEventVital` | 73 | 73 | NO |
| `ItemMallUpdatePersonalDataVital` | 5 | 5 | NO |
| `ServerAddedInfoVital` | 5 | 5 | NO |

Exact effective blocker strings and OPEN metadata are not duplicated here; `pf_build_v3_effective_status.py` recomputes them from the final effective A2 set. If a future rebuild finds zero unresolved rows for any affected message, this generator stops and requires a reviewed status transition instead of emitting one silently.

## Duplicate/layer accounting

| action | rows | W | R | unchanged copied | cross-overlay overlap | source |
|---|---:|---:|---:|---:|---:|---|
| remove `MUTATING_CHAIN_PLUS_04_HELPER` at selected `0x00B0BF70` callers | 26 | 13 | 13 | 0 | 0 | IMAGE |
| remove `MUTATING_POINTER_SLOT_TRAVERSAL_HELPER` at selected `0x0046D2B0` callers | 14 | 7 | 7 | 0 | 0 | IMAGE |

## Nonclaims and stop rule

- No node, field, gameplay, capture, runtime, or server semantic is assigned. An iterator interpretation is PROPOSED only and is not used as evidence or as a classification claim.
- No row outside the exact 40 V1 base identities is removed, including `0x0049FAD4`, rows with the same tag in other priority/blocker groups, and slot-0x34 additions.
- Resume this overlay only if an exact selected V1 base row changes or a later overlay targets one of the same base identities/callsites.
