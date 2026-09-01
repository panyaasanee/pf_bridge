# A6 broad-hit rejection audit delta

[MEASURED] This is a DUMP-only additive audit over the immutable V1 A6 outputs. It preserves every broad signature-zero hit as metadata but does not promote a rejected hit to a vtable.

## Result and duplicate control

- broad signature-zero + in-module-first-entry rows: 134
- strict accepted candidates: 0
- evidence-rejected broad hits: 134
- audit_added: 134
- strict_added: 0
- duplicate: 0
- immutable base A6 TSV SHA-256: c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985
- immutable base A6 extractor SHA-256: 54b7bcfecf598007ea468309481f8e41ff64e4139026a0ee200984b03ad82a2b
- this audit extractor SHA-256: f72ccc39a100836372a301a58c7283aea1513d7640d39e957c9a07bd9cedee99
- audit TSV SHA-256: 18a662070f53434d1230a41ef52ac130c46ee03d9fc14ab20e762bb5a3106a43

The 134 TSV rows are new rejection-audit records, not duplicate class-map rows. Every rejected row forces `strict_vtable_va=UNKNOWN`, `class_name=UNKNOWN`, and `instance_count=0`; its separate pointer-occurrence fields are a search census, not a live-object count. Unvalidated 32-bit words from rejected locator-shaped records are withheld rather than exported as if they were proven structure fields.

## Per dump

- GameClient.local.bin_1.41.01_69151_20260816_040609.dmp: sha256=daf63c7d13dc7ca601776cc7e4abbf02aa2e367f91ea420b3b05aaa8af7bffdc, broad=68, strict=0, rejected=68, type_descriptors=3121, distinct_aligned_values=1669258, mapped_table_slots=26231, mapped_locator_first_entry=944
- GameClient.local.bin_1.41.01_69151_20260816_042854.dmp: sha256=f982d47b6cec71171ccd2129ee9ce955a0cca05a9d5b606b0c97d5dd28169904, broad=66, strict=0, rejected=66, type_descriptors=3121, distinct_aligned_values=1669373, mapped_table_slots=26244, mapped_locator_first_entry=949

## Primary rejection partition

Primary reasons are ordered deterministically; their counts partition all 134 rejected rows.

- LOCATOR_VA_NOT_ALIGNED: 56
- TYPE_DESCRIPTOR_VA_NOT_ALIGNED: 20
- BROAD_POINTER_OUTSIDE_LOADED_MODULE: 20
- TYPE_DESCRIPTOR_OUTSIDE_LOADED_MODULE: 36
- HIERARCHY_OUTSIDE_LOADED_MODULE: 2
- partition total: 134

## All failed-predicate counts

A row may fail more than one predicate, so this section is not a partition.

- BROAD_POINTER_NOT_ALIGNED: 0
- LOCATOR_VA_NOT_ALIGNED: 56
- TYPE_DESCRIPTOR_VA_NOT_ALIGNED: 20
- HIERARCHY_VA_NOT_ALIGNED: 14
- BROAD_POINTER_OUTSIDE_LOADED_MODULE: 20
- LOCATOR_OUTSIDE_LOADED_MODULE: 19
- TYPE_DESCRIPTOR_OUTSIDE_LOADED_MODULE: 132
- HIERARCHY_OUTSIDE_LOADED_MODULE: 128
- RTTI_ADDRESSES_NOT_IN_SAME_LOADED_MODULE: 134
- FIRST_ENTRY_OUTSIDE_LOADED_MODULE: 0
- TYPE_DESCRIPTOR_NOT_EXACT_OR_NOT_CAPTURED: 134
- HIERARCHY_CHAIN_INVALID_OR_NOT_CAPTURED: 134

## Strict acceptance contract

A strict candidate must use aligned candidate/COL/TypeDescriptor/hierarchy addresses; all four addresses must lie inside the same loaded module; the first table entry must lie inside a loaded module; the TypeDescriptor must be exact; and the hierarchy/base-array/self-descriptor chain must validate inside the same dump snapshot. The class remains `UNKNOWN` in this candidate delta.

The refactored scan core has a synthetic full-chain positive control that must accept exactly one candidate. Signature, outside-module TypeDescriptor, and outside-module first-entry mutations must each accept zero. These controls prove that the zero strict count in the real dumps is not a vacuous acceptance path.

## Evidence boundary

The broad rows are locator-shaped search hits only. They cannot be used as vtable addresses, class identities, or object-instance counts. Candidate pointer addresses, dump offsets, module-membership labels, rejection reasons, counts, names, and SHA-256 values are retained; unvalidated locator scalar words are not exported. No IMAGE inference, nearby-string heuristic, raw dump byte, or hexdump is exported. Every TSV row has exactly one evidence layer: `source=DUMP`.
