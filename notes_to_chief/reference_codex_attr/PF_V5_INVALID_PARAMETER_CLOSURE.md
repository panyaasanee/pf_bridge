# PF V5 invalid-parameter non-wire closure component

[MEASURED][IMAGE] Ten physical guard callsites in two pinned serializers pass exact per-site IMAGE proof. The import name is not used as a global classification rule.

[PROPOSED][LOCAL] This additive component removes exactly 20 still-effective V1 analysis rows and chains exactly two P1 closures from PF_V4_P1_OPEN.tsv. It does not replace the V4 checkpoint until a later integration layer applies it.

## Exact IMAGE and import identity

- [MEASURED][IMAGE] GameClient.local.bin: 14759424 bytes / SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- [MEASURED][IMAGE] IAT `0x00C3B4C0` / file offset `0x008398C0` resolves from descriptor `0x00C112DC`, lookup `0x00C118B4`, DLL-name `0x00C1647C`, symbol-name `0x00C15C62` to `MSVCR90.dll!_invalid_parameter_noinfo`.
- [MEASURED][IMAGE] Every selected instruction is exact `FF 15 C0 B4 C3 00`; instruction SHA-256 `00ce047cf99a16facf7d68cb5e783c88fa394c8355e8a315a275a4a815f051cf`.

## Executed CFG and non-alias proof

| claim | message | span | nodes | edges | covered bytes | direct calls | indirect calls | selected guards | stack depth | source |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| [MEASURED][IMAGE] | `ServerAddedInfoVital` | `0x005EBCF0-0x005EBE33` / `f3608dd2456f8577a585e35164b6990d465abb1ffd73697ff7f103e4cbd34960` | 109 | 118 | 323 | 8 | 5 | 5 | 44 | IMAGE |
| [MEASURED][IMAGE] | `ItemMallUpdatePersonalDataVital` | `0x006B0D20-0x006B0FBC` / `142b0ecac21efcf62367aec12d0dfab558c0bdd66428b8f2922a6b89367cd664` | 193 | 212 | 536 | 18 | 5 | 5 | 44 | IMAGE |

[MEASURED][IMAGE] Each selected guard is reachable only from the write-mode successor, is dominated by that successor, and is unreachable from the read-mode successor. Reaching-definition analysis pins the object root at every call. ItemMall also pins the live writer stream register to entry+4 at every call; Server passes entry+4 to its wire primitive before the guards, while each guard itself has only the absolute IAT operand. Every guard enters and exits at the stable local-frame depth 44, so no stream or stack argument is passed.

[MEASURED][IMAGE] The ItemMall V1 span is intentionally conservative: executed coverage excludes the six-byte alignment NOP gap `0x006B0DCA-0x006B0DD0` (no CFG edge or dword xref enters it) and stops at `ret 8` at `0x006B0F3B`; the `0x006B0F3E+` bytes are a separated next-function tail. Those bytes are not claimed as executed serializer CFG.

| claim | callsite | file offset | message | guard | window SHA-256 | result | source |
|---|---:|---:|---|---|---|---|---|
| [MEASURED][IMAGE] | `0x005EBD3E` | `0x001EB13E` | `ServerAddedInfoVital` | `NULL_OR_UNEXPECTED_NODE_GUARD` | `aecc6aa81e414c6522b5c37aa5e8364302902296d7baf4d7f8a7ed7f39e0f1c0` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x005EBD50` | `0x001EB150` | `ServerAddedInfoVital` | `NULL_NODE_GUARD` | `868bcb2426a7086b41810ac69269ab06c3cb0412bf2bbfff4031e364a04c4315` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x005EBD5D` | `0x001EB15D` | `ServerAddedInfoVital` | `NODE_BOUNDARY_EQUALITY_GUARD` | `bd10d03f2383a2e06e1b3f41df2c2422248ab4b53b9c65b8f0e9ac7f8f326c2b` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x005EBD7A` | `0x001EB17A` | `ServerAddedInfoVital` | `NULL_NODE_GUARD` | `527c476e67825fdcd959be795013af1b15ee5fa3b2334b1a63e34b159d6addc6` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x005EBD85` | `0x001EB185` | `ServerAddedInfoVital` | `NODE_BOUNDARY_EQUALITY_GUARD` | `9b8b78c956e485cb381f1c0848ed3da745b7c14f51a9eaaf72add6261874cd8f` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x006B0DE2` | `0x002B01E2` | `ItemMallUpdatePersonalDataVital` | `NULL_OR_UNEXPECTED_NODE_GUARD` | `aecc6aa81e414c6522b5c37aa5e8364302902296d7baf4d7f8a7ed7f39e0f1c0` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x006B0DF6` | `0x002B01F6` | `ItemMallUpdatePersonalDataVital` | `NULL_NODE_GUARD` | `7cc6dc1936d93920ddcd3ae44c737c6499908c332cb929486ad5b982df6704f7` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x006B0E03` | `0x002B0203` | `ItemMallUpdatePersonalDataVital` | `NODE_BOUNDARY_EQUALITY_GUARD` | `071ba0b21aae381f038fe119ea3ae707f0e6082a6fa9066e875c355b1a936694` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x006B0E1C` | `0x002B021C` | `ItemMallUpdatePersonalDataVital` | `NULL_NODE_GUARD` | `527c476e67825fdcd959be795013af1b15ee5fa3b2334b1a63e34b159d6addc6` | PROVEN_NONWIRE | IMAGE |
| [MEASURED][IMAGE] | `0x006B0E27` | `0x002B0227` | `ItemMallUpdatePersonalDataVital` | `NODE_BOUNDARY_EQUALITY_GUARD` | `b70f86eb14db6247191d77f9112da8b22f8edb4fe53ade005c423cb00335a829` | PROVEN_NONWIRE | IMAGE |

## Helper boundary pins

[MEASURED][IMAGE] Both callers retain the earlier accepted stack-local `0x00B0BF70` helper and this-derived `0x00652A30` ordered-tree helper proofs. V5 re-hashes those bodies plus `0x00652550` and `0x00767170`, rechecks exact caller receiver origins, and re-derives the three fixed child calls. It does not copy or re-emit their already-closed rows.

## Full effective-A2 replay gate

- [MEASURED][IMAGE] Reconstructed frozen V4 effective A2 from the base plus the ordered V2/V3 replay and both V4 overlays: V3 component files/directives 4/124; V4 component files/directives 2/18; V4 targets accounted 18; effective rows 8657.
- [MEASURED][IMAGE] The 20 V5 directives were then applied by exact still-effective evidence key. Every declared target was consumed exactly once; no cardinality subtraction was used to obtain the post-V5 A2 census.

| claim | message | direction | removals applied | residual blocker rows | non-empty proven wire rows | effective rows after | source |
|---|---|---|---:|---:|---:|---:|---|
| [MEASURED][IMAGE] | `ItemMallUpdatePersonalDataVital` | W | 5 | 0 | 8 | 9 | IMAGE |
| [MEASURED][IMAGE] | `ItemMallUpdatePersonalDataVital` | R | 5 | 0 | 8 | 9 | IMAGE |
| [MEASURED][IMAGE] | `ServerAddedInfoVital` | W | 5 | 0 | 3 | 3 | IMAGE |
| [MEASURED][IMAGE] | `ServerAddedInfoVital` | R | 5 | 0 | 3 | 3 | IMAGE |

## Duplicate and layer audit

- [MEASURED][OUTPUT-AUDIT] Prior A2 overlays scanned from the exact V4 manifest: 15 files / 3053 directives = 451 full base targets + 2194 ADD semantic targets + 408 legacy string-correction targets; overlap with the 20 proposed targets and ten callsite semantics: 0.
- [MEASURED][OUTPUT-AUDIT] Existing provenance keys: 3404; existing full base targets: 576; ADD semantic targets: 2194; protected full+ADD target universe: 2770; new keys/targets: 22/22; overlap: 0.
- [MEASURED][OUTPUT-AUDIT] A2 actions: REMOVE_NONWIRE_ROW=20; Priority actions: CHANGED=2; ADD/COPY/UNCHANGED/A1/A3/A5 rows=0. Every TSV row has source=IMAGE.

## Effective projection if integrated after V4

[PROPOSED][DERIVED] A2 values below come from the full in-memory replay after exact removals. Priority values apply the two replay-gated transitions to the frozen V4 status but remain proposed until an integration checkpoint publishes them.

| claim | item | pinned V4 | projected after this component |
|---|---|---:|---:|
| [PROPOSED][DERIVED] | P1 CLOSED / total | 255/365 | 257/365 |
| [PROPOSED][DERIVED] | P1 OPEN | 110 | 108 |
| [PROPOSED][DERIVED] | overall CLOSED / total | 334/519 | 336/519 |
| [PROPOSED][DERIVED] | overall OPEN | 185 | 183 |
| [PROPOSED][DERIVED] | stored/reference A2 | 8657 | 8637 |
| [PROPOSED][DERIVED] | A2 UNKNOWN | 3963 | 3943 |
| [PROPOSED][DERIVED] | direct invalid-parameter UNKNOWN | 881 | 861 |
| [PROPOSED][DERIVED] | generic CALL/JUMP UNKNOWN | 1312 | 1312 |
| [PROPOSED][DERIVED] | A3 numeric-tag frequency | 4081 | 4081 |

## Nonclaims and stop rule

- [NONCLAIM][LOCAL] No gameplay meaning, server behavior, capture agreement, dump identity, runtime observation, field value, or import-wide classification is claimed.
- [NONCLAIM][LOCAL] No other `_invalid_parameter_noinfo` call is closed. A future site must repeat the same per-function CFG, reaching-definition, path, stack, and non-alias proof.
- [NONCLAIM][LOCAL] No raw DUMP or CAPTURE byte is read or emitted. No A5 TSV is copied. V1 and V4 remain immutable.

## Reproduction and scope

[REPRODUCTION][LOCAL] Run `py -3 -B pf_build_v5_invalid_parameter_closure.py --self-test-publication`, then `--self-test-replay-mutation`, `--audit-only`, normal publication, and `--check`.

[DECLARED-SCOPE] Local-only under pf_bridge/external. Read GameClient.local.bin and frozen external artifacts only. Do not run the client or server and do not write workflow, queue, lease, Git, V4, capture, dump, data, or GameClient files.
