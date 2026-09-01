# PF ground-drop / pickup closure

This standalone P0-6 artifact closes the exact typed identity and bounded client transport path while preserving the runtime/policy ceilings. `source=IMAGE` and `source=CAPTURE` facts remain separate in every TSV row. No ServerProject/code row appears; replacement-provenance capture observations remain CAPTURE, not original evidence.

## Outcome

- Rows: 15 (IMAGE 8, CAPTURE 7).
- IMAGE: `PF_ROOT://GameClient/GameClient.local.bin`, size `14759424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- Current CAPTURE corpus: `2227` files, `699015496` bytes, manifest `b8284a566d9993f52540dea52e82896b0d8eb499b9aa83ceb74084a0e671db3c`.
- Parsed CAPTURE text/block census: `1337` text files / `81954` PC+DECOMPRESSED blocks.
- TSV SHA-256: `0aa918f2c52d333d3d8bde32c28aac8315fdc6e7c5bff786573246de6195b49e`.
- Ordered claim-set SHA-256: `b04cb1f6e4d659d75f7a676dda950e5040ff844ca9b538cb7b437d311612c2b0`.

## Exact typed closure (IMAGE)

- The click path proves a DropThingGameObj is-a gate from the named MSVC TypeDescriptor through the custom descriptor parent chain. Derived classes are accepted.
- On the reached action/type/range/allocation-success path: `PickupTerrainThing+0x14 == [DropThingGameObj+0x7C]->TerrainThing+0x10 == DropThingModule_Client reconciliation/map key`.
- `0x4543` is the nested logical PickupTerrainThing runtime discriminator. `0x6E6F` is the gameplay outer logical discriminator. Login remains the distinct outer `0x453A`.
- These values are logical runtime discriminators, not established top-level semantic opcodes.
- The static path extends through serialize -> transform/repack -> chunks of at most `0x3FF8` -> the `WS2_32.dll` ordinal-19 `send` import.
- `0x5F253EAC` is transport framing. Because `0x00B743B0` rewrites the buffer, no final socket literal is claimed for the logical discriminators.
- The successful pickup-emission subpath has no direct edge to the three pinned known unregister/map-delete functions. Later authoritative S2C removal remains required/open.

## Canonical removal matrix (references only)

The matrix is composed only by content-addressing `GDL-IMG-007`, `GDL-IMG-008`, `GDL-IMG-009`, `GDL-IMG-010`, and `GDL-IMG-015` in pinned `PF_GROUND_DROP_LIFETIME.tsv`. Their IMAGE claims are not copied into new TSV evidence rows. The same rule is used for the FightingDrop false-lead classification (`GDT-IMG-008`, `GDT-IMG-009`, `GDL-CREF-001`).

## Current capture ceiling (CAPTURE)

- All four named target families (`PickupTerrainThing`, `DropThingModule_Client`, `FightingDropModule_Client`, `FightingDropNotify`) are W0/R0 in the broad current validator census.
- RuntimeRes R has 15,288 frames: 14,536 with derived TerrainThingPool bit 0x08 absent, zero present-count-zero, 23 present-nonempty, and 729 fail-closed unresolved. The 23 nonempty frames are 22 count-one plus one count-two; all are REPLACEMENT provenance in 11 files/19 unique complete-frame hashes.
- The nonempty-event metadata manifest is `fb771d2f6fbeffacac37b283bad676c998480d74e010b36f1ebd2bd37a0dc82e`. Its records contain path/hash/ordinal/provenance/count/keyset-hash only; runtime keys and payload bytes are not emitted.
- The all-729 unresolved-locator manifest is `23b8427bdf1ab56089dba2fa0a7c2f81d6a9f25b3a391ee03eecbebc665a7878` over UTF-8 lines `relative_path<TAB>file_sha256<TAB>block_ordinal<TAB>frame_sha256<TAB>reason`, sorted lexicographically and joined with LF plus final LF. It contains 726 stopped tails and the three exact truncated-derived-mask locators listed below.
- Combined gameplay/login C2S outer blocks total 65,610 (64,979 gameplay, 631 login); 58,412 have no nested collection. Of 15,350 declared nested instances, 14,615 wrappers/type IDs are reached; traversal advances only across PASS CLOSED schemas, leaving 735 later declarations behind the first fail-closed stop. PickupTerrainThing is 0/14,615 reached wrappers/type IDs, not globally absent.
- Exactly zero eligible ORIGINAL pickup-to-authoritative-removal exchanges are established. No exact CAPTURE omission/removal carrier is proved.
- Existing `PF_FIELD_VALIDATION.tsv` is frozen to 1,772 files / 595,134,426 bytes. It is not a current-2,227-file validation, and its generator has no `--check` option.
- No proprietary capture payload or raw byte is emitted. The current manifest records only path, size, and file SHA-256.

### Three truncated-derived-mask locators (CAPTURE metadata only)

- `capture_gt010_20260818_015927/capture_v141/GAME_20260818_020106_955833_62358.txt` | file SHA-256 `22afd705194e15b97dc1ed3605487e667f268d5ba8671bb01a99c9a05dd5e3bf` | block `6` | frame SHA-256 `6ddeeb879f8c7871a4655ed4f16a1955220e6e73136d4a8ad6087e49f48624e3`
- `capture_gt101_20260827_143419/capture_v141/GAME_20260827_143641_602267_55866.txt` | file SHA-256 `104abb1e6e9a793ecfa2cabfbdcccf73eaef39a6c75526264b94ef420227d7f5` | block `8` | frame SHA-256 `c6b19acb5786889cc2e18f03586b3b597b1a72301c7f873322f27bbb1e6f9e22`
- `capture_gt107_20260827_172426/capture_v141/GAME_20260827_173114_446035_53082.txt` | file SHA-256 `7bac8141e3d073100687c8bda9a34600981fc8e344f67c3dbbc2bbb58ee0a31e` | block `8` | frame SHA-256 `0ec871048ab41aa2131feddf6faf6c5f39f2bc90bb5b954c3b5c68897ac31ba8`

## IMAGE + CAPTURE analytical composition (not a TSV evidence row)

Applying the separately sourced canonical IMAGE reconciliation rules (`GDL-IMG-007`, `GDL-IMG-008`, `GDL-IMG-009`) as an explicit analytical convention to the ordered CAPTURE metadata—state scoped per file; unresolved invalidates state; bit-absent resets; count-zero preserves—classifies the 23 confirmed nonempty events as ADD=13, ADD+OMIT=10, same-set update=0, with 10 one-entry swaps. This composition is not presented as a CAPTURE-only state-transition fact and does not prove original-server policy.

## OPEN end-to-end gates

- Production caller/transaction ownership and server acceptance of a pickup are not proved by IMAGE or current CAPTURE.
- Last-item all-clear is OPEN. A non-NULL count-zero TerrainThingPool is canonically PRESERVE, so it cannot be renamed or guessed as clear.
- Original issuance carrier, co-order, expiry duration/policy, and post-pickup removal carrier are OPEN.
- Original-versus-replacement timing, shared-world ownership, scene ownership, retry policy, and final socket-byte literals are OPEN.
- Client-local direct deletion on the pickup-emission subpath is not proved; indirect/virtual/tail/callback/later lifecycle paths remain possible.

## RECONSTRUCTED current-server comparison (not TSV evidence)

The pinned urgent note `CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md` (SHA-256 `8b8904aed010ff49566b8af6bfb99898358e80b1f78f8fe2c014f58ea847aa8b`) reports that the current reconstructed implementation has scene-less drop-ledger ownership and no production pickup transaction/removal publisher. This comparison is labelled RECONSTRUCTED and is not used as IMAGE or CAPTURE evidence. The generator reads the pinned note, not ServerProject code.

## Source-separated rows

| closure_id | source | status | exact bounded result | blocker |
|---|---|---|---|---|
| GDP-IMG-001 | IMAGE | PROVEN_EXACT_CONDITIONAL | The static initializer binds MSVC TypeDescriptor .?AVDropThingGameObj@@ at 0x0101C218 to custom descriptor 0x010823E8. DropThingGameObj vtable slot +0x00 returns that descriptor. The click path obtains the clicked object's descriptor and 0x0088F2B0 walks descriptor +0x04 parents against 0x010823E8; only a successful is-a result retains the object pointer. | NONE_FOR_BOUNDED_STATIC_CLAIM |
| GDP-IMG-002 | IMAGE | PROVEN_EXACT_CONDITIONAL | On the reached action/type/range/allocation-success subpath, the retained typed object supplies [DropThingGameObj+0x7C]->TerrainThing+0x10 and the client stores that exact u32 into PickupTerrainThing+0x14. Canonical GDL rows independently bind TerrainThing+0x10 as the DropThingModule_Client reconciliation/map key. | LIVE_SERVER_ACCEPTANCE_AND_RESULTING_REMOVAL_NOT_ESTABLISHED |
| GDP-IMG-003 | IMAGE | PROVEN_EXACT_STATIC_SUCCESS_PATH | The nested-list writer calls each nested object's vtable +0x10 GetId and writes that u16 with tag 0x12 before invoking vtable +0x18 serializer. With the canonical successful PickupTerrainThing ID assignment and getter, 0x4543 is the nested logical runtime discriminator. | FINAL_SOCKET_LITERAL_AND_ORIGINAL_WIRE_OCCURRENCE_OPEN |
| GDP-IMG-004 | IMAGE | PROVEN_EXACT_STATIC_SUCCESS_PATH | The outer writer calls vtable +0x10 GetId, writes the returned u16 with tag 0x12, writes the remaining outer fields, then calls vtable +0x18 serializer. Canonical successful IDs therefore classify 0x6E6F as the gameplay GSCN_RunTimeProtocolReq logical outer discriminator; login uses the distinct GSCN_LoginProtocol logical outer discriminator 0x453A. | FINAL_SOCKET_LITERAL_AND_LIVE_PHASE_SELECTION_OPEN |
| GDP-IMG-005 | IMAGE | PROVEN_EXACT_STATIC_SOCKET_PATH | 0x00A8CC30 calls logical writer 0x00C3A0A0, transform/repack 0x00A8C8D0, then chunk/send 0x00A8CB30. The transform calls buffer-rewriter 0x00B743B0. The sender limits each payload chunk to at most 0x3FF8, and its flag-1 branch prepends eight transport bytes beginning with constant 0x5F253EAC before thunk 0x00B378E6 jumps through IAT 0x00C3BA74 to the WS2_32.dll ordinal-19 `send` import. | FINAL_SOCKET_BYTE_MAPPING_OPEN_AFTER_BUFFER_REWRITE |
| GDP-IMG-006 | IMAGE | PROVEN_EXACT_BOUNDED_NEGATIVE | The reached allocation-success subpath 0x006B062D..0x006B0658 has exactly three direct E8 calls: request factory, wrapper/ownership helper, and nested enqueue. None targets the three pinned known unregister/map-delete functions. Successful request emission therefore performs no proved direct local unregister or module-map erase; a later authoritative S2C removal remains required/open. | AUTHORITATIVE_POST_PICKUP_S2C_REMOVAL_CARRIER_OPEN |
| GDP-IMG-007 | IMAGE | CANONICAL_REFERENCE_SET_VERIFIED | This row content-addresses the existing GDL removal-matrix rows for NULL input, non-NULL empty input, nonempty omission, range pruning, and separate kind-0x0A clear/destruction. Their claims are not copied or reissued here. | ORIGINAL_SERVER_ISSUANCE_ORDER_EXPIRY_AND_POST_PICKUP_SELECTION_OPEN |
| GDP-IMG-008 | IMAGE | REFERENCE_ONLY_FALSE_LEAD_FOR_PROVED_TYPED_PATH | Content-addressed canonical rows classify FightingDropModule_Client and FightingDropNotify as custom-reflection surfaces that are not selected by the proved GSCN_RunTimeProtocolRes+0x20 TerrainThingPool typed path. No FightingDrop fact is reissued here. | NONE_FOR_BOUNDED_FALSE_LEAD_CLASSIFICATION |
| GDP-CAP-001 | CAPTURE | OBSERVED_EXACT_CURRENT_CORPUS_METADATA | The current read-only census contains 2,227 unique files totaling 699,015,496 bytes; 1,337 .txt files decoded as UTF-8 with replacement contain 81,954 validated PC/DECOMPRESSED blocks. | NONE_FOR_CURRENT_CORPUS_CENSUS |
| GDP-CAP-002 | CAPTURE | NOT_OBSERVED_IN_CURRENT_CORPUS | PickupTerrainThing, DropThingModule_Client, FightingDropModule_Client, and FightingDropNotify each have W=0 frames/instances/files and R=0 frames/instances/files in the current parsed corpus. | NO_ELIGIBLE_NAMED_PICKUP_OR_REMOVAL_INSTANCE |
| GDP-CAP-003 | CAPTURE | OBSERVED_OUTER_ONLY_A2_STATIC_OPEN | Current corpus observes GSCN_RunTimeProtocolReq W=64,979 frames/instances in 195 files and GSCN_RunTimeProtocolRes R=15,288 frames/instances in 206 files; opposite directions are zero. | NESTED_MEMBER_ATTRIBUTION_OPEN |
| GDP-CAP-004 | CAPTURE | OBSERVED_EXACT_WITH_FAIL_CLOSED_TAIL | Of 15,288 RuntimeRes R frames, the derived TerrainThingPool bit 0x08 is absent in 14,536, present with count zero in 0, present nonempty in 23 (22 count-one and one count-two), and unresolved in 729; 3 of the unresolved frames truncate before the derived mask. Outer mask 0x00 contains 602 absent and all 23 nonempty frames; outer mask 0x02 contains 13,934 absent and all 729 unresolved. | 729_TAILS_UNRESOLVED_AND_ORIGINAL_POLICY_OPEN |
| GDP-CAP-005 | CAPTURE | OBSERVED_EXACT_REPLACEMENT_SEQUENCE | All 23 confirmed nonempty frames are REPLACEMENT provenance, across 11 files and 19 unique complete-frame hashes; 22 carry one record and one carries two records. Their file/block order, record counts, and hashed keysets are content-addressed without emitting any runtime key. ORIGINAL=0 and UNKNOWN=0 among these confirmed nonempty frames. | NO_ORIGINAL_NONEMPTY_TERRAIN_POOL_FRAME |
| GDP-CAP-006 | CAPTURE | ZERO_IN_EXACT_REACHED_SUBSET_GLOBAL_ABSENCE_OPEN | The current REPLACEMENT corpus has 65,610 eligible C2S outer blocks: 64,979 gameplay 0x6E6F and 631 login 0x453A. 58,412 have outer bit 0x02 clear/no nested collection. Nested declared instances total 15,350; 14,615 wrappers/type IDs are exactly reached, traversal advances only across PASS CLOSED W schemas, and 735 later declared members remain unreached after the first fail-closed stop. PickupTerrainThing is 0 of 14,615 exactly reached wrappers/type IDs. | 735_C2S_NESTED_MEMBERS_FAIL_CLOSED_AND_ORIGINAL_TRAFFIC_ABSENT |
| GDP-CAP-007 | CAPTURE | ZERO_ESTABLISHED_EXCHANGES_CARRIER_OPEN | No eligible ORIGINAL C2S pickup plus S2C omission/removal exchange is established by the current corpus, and no exact omission/removal carrier is proved by CAPTURE. Existing PF_FIELD_VALIDATION.tsv is frozen to the older 1,772-file/595,134,426-byte inventory, not the current 2,227-file corpus. | ORIGINAL_PICKUP_ACCEPTANCE_REMOVAL_ORDER_AND_EXPIRY_UNOBSERVED |

## Pinned canonical inputs

- `PF_GROUND_DROP_TRANSPORT.tsv`: `9e2396795ee32287f1f9b82f22fb8f394464d2b0a25375d07108ee138c73907b`
- `PF_GROUND_DROP_LIFETIME.tsv`: `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`
- `PF_FIELD_VALIDATION.tsv` (frozen corpus only): `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- `pf_validate_capture_fields.py`: `0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8`

## Deterministic verification

```powershell
py -3 pf_rederive_ground_drop_pickup_closure.py --check
py -3 pf_rederive_ground_drop_pickup_closure.py --self-test
```
