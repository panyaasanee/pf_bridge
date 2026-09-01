# PF Quest-Mark Event Census

Status: **OPEN overall; the bounded IMAGE census below is complete for the stated direct/static scope.**

## Outcome first

- On image SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, the return-value/query channel has **55** direct registration sites. Exactly **1** is kind `0x0A`: `0x00615BFC` in the QuestModule registration function referenced by `PF_ATTR_QUEST_MARK_SELECTOR.tsv` / evidence key `664c81eb05a59bb0661d3390d9f08a7c4f7401360e4bf3840678e4fa10a6f515`.
- Query dispatcher `0x005F9F60` uses owner map `+0xA0` and listener vtable slot `+0x44`. Its direct-target census has **126** calls: **123** pinned immediate-kind shapes plus **3** separately traced non-`0x0A` controls. The only immediate `0x0A` producer is `0x00449F30` / dispatch call `0x00449FAD`.
- Producer `0x00449F30` has **5** direct callers. The CNetNPC caller at `0x006167D1` seeds event `+0x18` from `NPCAttr+0x78` and `+0x20/+0x24` from actor `+0x78/+0x7C`.
- QuestModule handler `0x0061A8C0` receives the query callback through vtable `+0x44`; its `0x0A` branch calls the referenced selector computation, zero-extends AL, and overwrites the full dword at event `+0x18`. The query dispatcher continues after a true return, so an additional later listener could overwrite the result in principle. Within the pinned direct/static census there is only this one query-channel `0x0A` vtable owner.
- Numeric kind `0x0A` is **not globally a quest event**. The separate general-notification channel has **8** direct kind-`0x0A` registration sites bound through shared functions to **11** image vtables. General dispatcher `0x005F9C70` uses owner map `+0x80` and vtable slot `+0x40`. `GDL-IMG-015` / evidence key `b014e9c7797a1d24b5c13eef598b7374223af5b548fe3efda538a43cd65a7d09` independently establishes kind-`0x0A` clear behavior at handler `0x006B03F0`; this artifact adds only the channel/vtable binding and does not copy that row.

## Event object and lifetime

`0x00449F30` constructs a stack event, seeds `+0x18/+0x20/+0x24`, stores kind `0x0A` at `+0x10`, and synchronously calls the query dispatcher. If any handler returns true, it reads the low byte at `+0x18`; both true and false paths destroy the stack event before return.

The module add path rejects another module with an equal vtable `+0x10` identity in that manager. For a new module it calls general registration slot `+0x24` before query registration slot `+0x34`. The removal path unregisters the module from both owner `+0x80` and owner `+0xA0` maps. These are manager-local static boundaries, not process-wide or crash-time guarantees.

## Channel partition

| Property | Return-value/query channel | General-notification channel |
|---|---|---|
| registration API | `0x005FAE30` | `0x005FACE0` |
| manager lookup map | `+0xA0` | `+0x80` |
| listener virtual slot | `+0x44` | `+0x40` |
| dispatch API | `0x005F9F60` | `0x005F9C70` |
| kind-`0x0A` direct registration sites | 1 | 8 |
| kind-`0x0A` image vtable owners | 1 | 11 |
| CNetNPC query result writer | QuestModule `0x0061A8C0` writes `+0x18` | not in this registry/vector |

The general-channel vtable identities are retained as addresses unless an existing pinned reference supplies a class label:

- `vtable=0x00F33420;register_func=0x00615B40;handler=0x00619680`
- `vtable=0x00F3C2C8;register_func=0x006E4600;handler=0x0069AA00`
- `vtable=0x00F3DD38;register_func=0x006E4600;handler=0x006B03F0`
- `vtable=0x00F40D20;register_func=0x006E4600;handler=0x006E5AC0`
- `vtable=0x00F411A8;register_func=0x006ECC30;handler=0x006ED880`
- `vtable=0x00F420A8;register_func=0x006F9C30;handler=0x006FC2F0`
- `vtable=0x00F43268;register_func=0x0070F2D0;handler=0x0070F390`
- `vtable=0x00F46738;register_func=0x006E4600;handler=0x0073D360`
- `vtable=0x00F46EC8;register_func=0x00730470;handler=0x007318C0`
- `vtable=0x00F47958;register_func=0x0073E7B0;handler=0x0073E900`
- `vtable=0x00F47BF8;register_func=0x00742480;handler=0x00744620`

## Selector reference, without duplication

This artifact does not reproduce the selector table. It references exact selector evidence key `664c81eb05a59bb0661d3390d9f08a7c4f7401360e4bf3840678e4fa10a6f515` from `PF_ATTR_QUEST_MARK_SELECTOR.tsv` (SHA-256 `3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0`). In particular, selector `0` is **not called hidden** here: the referenced row says it sets board-root `+0x18` bit-mask `0x1` and does not select or bind a new texture. Client-observable visibility remains outside this IMAGE-only census.

## Measured rows

| key | channel | row kind | status | primary VA span |
|---|---|---|---|---|
| QME-IMG-001 | SHARED_EVENT_OBJECT | EVENT_LAYOUT_INIT | PROVEN_EXACT | 0x005F8D43..0x005F8D84 |
| QME-IMG-002 | RETURN_VALUE_CHANNEL | QUERY_PRODUCER | PROVEN_EXACT | 0x00449F65..0x00449FB2 |
| QME-IMG-003 | RETURN_VALUE_CHANNEL | QUERY_RESULT_LIFETIME | PROVEN_EXACT | 0x00449FB2..0x00449FD9 |
| QME-IMG-004 | RETURN_VALUE_CHANNEL | QUERY_PRODUCER_CALLER_CENSUS | PROVEN_BOUNDED | 0x005250AC..0x005250BA |
| QME-IMG-005 | RETURN_VALUE_CHANNEL | CNETNPC_QUERY_BINDING | PROVEN_EXACT | 0x006167C1..0x006167D6 |
| QME-IMG-006 | RETURN_VALUE_CHANNEL | QUERY_REGISTRATION_CENSUS | PROVEN_BOUNDED | 0x00615BE0..0x00615C30 |
| QME-IMG-007 | RETURN_VALUE_CHANNEL | QUEST_QUERY_VTABLE_BINDING | PROVEN_EXACT | 0x00F33454..0x00F33468 |
| QME-IMG-008 | RETURN_VALUE_CHANNEL | QUERY_REGISTRY_INSERT | PROVEN_EXACT | 0x005FAE30..0x005FAF77 |
| QME-IMG-009 | RETURN_VALUE_CHANNEL | QUEST_QUERY_WRITER | PROVEN_EXACT | 0x0061A8D9..0x0061A8F9 |
| QME-IMG-010 | RETURN_VALUE_CHANNEL | QUERY_DISPATCH_ORDER | PROVEN_EXACT | 0x005F9F60..0x005FA011 |
| QME-IMG-011 | RETURN_VALUE_CHANNEL | QUERY_DISPATCH_TARGET_CENSUS | PROVEN_BOUNDED | 0x00449FA1..0x00449FB2 |
| QME-IMG-012 | RETURN_VALUE_CHANNEL | QUERY_NON0A_CONTROL | PROVEN_EXACT | 0x0050023F..0x00500313 |
| QME-IMG-013 | RETURN_VALUE_CHANNEL | QUERY_NON0A_CONTROL | PROVEN_EXACT | 0x006E2BF0..0x006E2D25 |
| QME-IMG-014 | RETURN_VALUE_CHANNEL | QUERY_NON0A_CONTROL | PROVEN_EXACT | 0x0075B003..0x0075B177 |
| QME-IMG-015 | BOTH_MODULE_CHANNELS | MODULE_ADD_BOUNDARY | PROVEN_EXACT | 0x005FB824..0x005FB8F1 |
| QME-IMG-016 | BOTH_MODULE_CHANNELS | MODULE_REMOVE_BOUNDARY | PROVEN_EXACT | 0x005FB607..0x005FB795 |
| QME-IMG-017 | GENERAL_NOTIFICATION_CHANNEL | GENERAL_REGISTRATION_CONTROL_CENSUS | PROVEN_BOUNDED | 0x00615B40..0x00615BDB |
| QME-IMG-018 | GENERAL_NOTIFICATION_CHANNEL | GENERAL_DISPATCH_CONTROL | PROVEN_EXACT | 0x005F9C70..0x005F9D05 |
| QME-IMG-019 | GENERAL_NOTIFICATION_CHANNEL | GENERAL_KIND0A_PRODUCER_CONTROL | PROVEN_EXACT | 0x005F6D08..0x005F6D5E |
| QME-IMG-020 | GENERAL_NOTIFICATION_CHANNEL | GROUND_DROP_CROSS_CONTROL_BINDING | PROVEN_EXACT | 0x00F3DD5C..0x00F3DD7C |

Every TSV row has exactly one source, `IMAGE`, and includes an exact primary VA range, file-offset range, and SHA-256. `reference_keys` joins prior rows without copying their evidence keys or converting their claims into new evidence.

## Open / proposed work (not measured facts)

- **OPEN:** computed control transfers with no static E8/E9/absolute target carrier, runtime-only listener injection, runtime registry order, reentrant mutation, and abnormal teardown are not closed by this bounded static census.
- **OPEN:** the four non-CNetNPC callers of `0x00449F30` and unlabelled general-channel vtables are intentionally not assigned gameplay/class names.
- **OPEN:** client-observable QuestIconBoard presentation is a different source layer and is not inferred here.
- **PROPOSED only if needed:** instrument registration/removal and one `0x0A` query dispatch to capture live vector identities/order. Do not merge that runtime evidence into these IMAGE rows.

## Re-derivation and publication

- Pinned image: `PF_ROOT://GameClient/GameClient.local.bin`, size `14759424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- Pinned selector reference: size `52137`, SHA-256 `3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0`, key `664c81eb05a59bb0661d3390d9f08a7c4f7401360e4bf3840678e4fa10a6f515`.
- Pinned cross-domain control: size `61979`, SHA-256 `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`, key `b014e9c7797a1d24b5c13eef598b7374223af5b548fe3efda538a43cd65a7d09` (`GDL-IMG-015`).
- Generation stages both files under an exclusive transient lock, fsyncs them, then replaces the pair. `--check` creates no lock, temporary file, or output and verifies a stable read plus exact regenerated bytes.
- Artifact pair SHA-256: `6a513a67f9e349150933fccf2ea7468538332b3f2553d0a6e8b0206475376dd3`. The same value appears in every TSV row, detecting mixed-generation publication.

Rows: 20. Sources: IMAGE=20. No DUMP/CAPTURE/DATA rows. No raw client/capture/dump bytes are published.
