ถึง chief

# RE-222 — PARTIAL: UpdateAttrVital framing and name-color gate chain

- Status: **PARTIAL — Q0/Q1/Q2 DONE; Q3 main registry + lookup DONE, exact selector-list population path remains a resumable time checkpoint (not a method ceiling)**
- Jobs covered this round: **Q0–Q3**
- START: `2026-09-03T21:33:04.508+07:00`
- Static only. No game/server boot, no `LOCK_GAME`, no canonical DB, and no source/queue/external/gamedata mutation.

## Input pins

- Full current ticket block (queue lines 4618–4694): SHA-256 `098FA5BBE9D32AE21EC6E2E730ABA720FA5B587B900F0C973455829E22C2AAA8`
- `CLIENT_RE_QUEUE.md`: `F279C3929AE0605130462C0C29D6A6104E1847E4A77F70A75771590446C22591`
- `GameClient.local.bin`: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
- `PF_PROTOCOL_REGISTRY.tsv`: `27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D`
- `PF_SERIALIZER_FIELDS.tsv`: `99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123`
- `PF_ATTR_NAME_COLOR_SELECTOR.tsv`: `D15864A21A7A124A23F6DFFAD174A55D376045A25A04814BBE6DC5F5632AF82D`

## Mandatory shared searches

- `pf_bridge/external/`: searched once across 2,683 files / 930,201,065 bytes; metadata fingerprint `7089D1118628AA1BA2C7DC333521B21EBB79E915642A940AD409EB94FDED6945`. The query set covered `UpdateAttrVital`, `0x00463DE0`, selector addresses, signed/nonpositive identity, actor lookup, and the name-color selector. It hit 15 relevant artifacts, including the protocol/serializer tables, `PF_A2_ATTR_SEMANTIC_DELTA.*`, `PF_ATTR_CONTAINER_SEMANTICS.tsv`, and selector/census reports.
- `gamedata/`: searched once across 1,109 files / 15,319,585 bytes; metadata fingerprint `1159D1C78718A3EEB0CCCCA1CDF209F32978A620B8D99538EE61107C9F094E8F`. The same query set produced **zero hits**.
- The existing external answers were SHA-verified against the pinned image rather than accepted by identifier coincidence. `PF_A2_ATTR_SEMANTIC_DELTA.tsv` is `4BE6E28BF4F50533F1C208A396D244C1930049059E03F377A2680A4EC3619A0F`; `PF_ATTR_CONTAINER_SEMANTICS.tsv` is `E58E6E9B3B7DF7089336AB0F7DF042079BE0266BE3938DA5DA63708FA98282F1`.

## Q0 — exact generic UpdateAttrVital read-frame

`UpdateAttrVital` resolves to serializer `0x005E42C0`; its generic attribute-container reader is `[0x00463DE0,0x00463FA2)`, 450 bytes, SHA-256 `888C2FAC20948B7896ED105F46B84E94D01C9442F6535DF9BE36E6BAA2335FC3`.

Exact outer wire structure:

1. `tag 0x12 + uint16 entry_count`
2. For each entry: `tag 0x12 + uint16 attr_factory_type_key`
3. `tag 0x14 + uint32 nested_payload_length`
4. A factory-created attribute object consumes the nested payload via its virtual codec at `vtable+0x34`.

Read sites:

- `0x00463F12`: entry count
- `0x00463F3B`: factory type key
- `0x00463F4B`: declared nested length
- `0x00463F55` / `0x00463F5C`: factory accessor and lookup/create
- factory miss: `0x00463F6E` skips exactly the declared byte count via `0x0089A1D0`
- factory hit: `0x00463F7E` invokes the concrete nested codec; the generic carrier itself does **not** enforce/consume the declared length on this path
- `0x00463F83`: inserts the decoded attribute into the container

This closes the 13 previously UNKNOWN generic-reader rows as follows:

- R2–R6: invalid-parameter guards, not wire fields
- R7: write-only nested serializer
- R8: write-only length backpatch
- R9: write-side iterator advance
- R13: factory access, not wire
- R14: factory lookup/create, not wire
- R15: unknown-type cursor skip, not a field
- R16: dynamic nested subserializer; the outer structure is exact but the concrete schema depends on the factory type key
- R17: container insertion, not wire

### GT-218 frame diff

The cited result is actually `20260903_1655_KA1A-R306-RESULTS-gt216-gt210-gt212-gt211-pass-gt218-fail-the-client-dies-on-speed-400-with-the-frame-sent.md`, SHA-256 `D86AA8A009F515018592C5D1A146B9F3D321C36A6AAC1DD9972C83BEBFF2C8FD`. Its quoted raw block contains 63 logical bytes (SHA-256 `7CEF56C3FED3909DD5531173D1E6FD0B3C211E4FD595E1D82307F90ECEF72577`), although the logger line reports 74 bytes; 11 bytes are absent from the quoted block and cannot be classified from that excerpt alone.

Within the quoted bytes the UpdateAttr container starts at offset 20:

| Offset | Bytes | Meaning | Verdict |
|---:|---|---|---|
| 20 | `12 01 00` | count = 1 | structurally valid |
| 23 | `12 AD 12` | factory type key = `0x12AD` | `checksum("ActorAttr") & 0xFFFF`; exact class crosswalk |
| 26 | `14 1E 00 00 00` | nested length = 30 | structurally valid |
| 31–60 | 30-byte `ActorAttr` payload | fully decoded below |
| 61–62 | `0B 00` | outer tail | outside the generic container |

The named-ID checksum is the required crosswalk rather than an ID-equality guess: `sum((index+1)*ord(character) for "ActorAttr") & 0xFFFF = 0x12AD`. IMAGE independently links the registered `ActorAttr` name to vtable `0x00F0E7A0` and codec `0x00466230`; the vtable's `+0x34` pointer is exactly `0x00466230`.

Exact 30-byte nested decode:

| Nested offset | Bytes | ActorAttr inheritance field |
|---:|---|---|
| 0 | `0B 01` | `DBAttribute` identity-presence byte = 1 |
| 2 | `32 01 00 01 10 00 00 00 00` | identity low=`0x10010001`, high=`0x00000000` |
| 11 | `12 40 00` | `BasicAttr` presence mask = `0x0040` only |
| 14 | `2A 00 00 C8 43` | `BasicAttr+0x54` f32 = `400.0` |
| 19 | `32 00 00 00 00 00 00 00 00` | `ActorAttr` two-dword presence mask = zero |
| 28 | `05 01` | ActorAttr extra-group byte = 1 |

Important correction: `0x40` is a **BasicAttr presence-mask bit inside ActorAttr**, not an outer `attr id`. There is no tag-width-order framing error in the quoted container or nested body.

### Exact GT-218 failure mechanism

The protocol handler `[0x005F2400,0x005F261F)`, SHA-256 `74C1B024F064D2930831B8CEAB109EFA154F6D660BB8D079346CCB28E90A3201`, resolves the incoming Attr type through vslot `+0x10`, finds the resident Attr, then calls the incoming object's vslot `+0x24` at `0x005F2504..0x005F250C`. For ActorAttr, vtable `0x00F0E7A0 + 0x24` is `0x00464F30`.

`ActorAttr` full copy `[0x00464F30,0x004652AC)`, SHA-256 `78F9C31B0FF1D75BC7845D5E340F4D525E0C8F80E034396B0E0F61699AD6A3E1`, copies the newly decoded incoming object into the resident object wholesale: it first copies the inherited BasicAttr and then every ActorAttr member, independent of the wire presence masks. The fresh BasicAttr constructor `[0x00464A80,0x00464B3D)`, SHA-256 `9A9170CD920BDDC3791BFFE8966264C88E1F2DA5B4320B336F0EEACD4884ED3D`, initializes HP current/max and MP current/max to zero. The ActorAttr constructor `[0x00464BE0,0x00464E39)`, SHA-256 `E83AE4A601A4EC700326598D6329E4B34CD2F4CF78DCF17D639D8DF8E1F1096A`, initializes cash (`+0xA8/+0xAC`) to zero.

Therefore the exact error is **sending a sparse ActorAttr to an apply path with full-object replacement semantics**, not malformed framing. Only the `0x0040` BasicAttr field is supplied; all omitted BasicAttr/ActorAttr members retain constructor defaults and are then copied over the live resident object. This directly explains cash becoming zero. The resident HP-max field becomes zero statically; the observed on-screen `1` is a downstream display behavior/clamp and is not evidence of a wire offset error.

## Q1 — exact signed identity gate

Selector `[0x00443F50,0x004443C5)` matches the ticket pin, SHA-256 `EE845EE6EF6337EA41AE57A5A4DF8AF5A8A8AC00E458EA1CE3E587AFF1F9CDF9`.

The selector reads both halves of the actor identity: low dword at `CNetActor+0x78`, high dword at `+0x7C`.

```text
00443FFB  cmp dword ptr [esi+0x7c], 0
00443FFF  mov eax, [esi+0x78]
00444007  jl  0x444151
0044400D  jg  0x444017
0044400F  test eax, eax
00444011  jbe 0x444151
```

This is a two-half lexicographic test: signed high dword first; when high is zero, low is tested for zero. The exact nonpositive set is therefore the 64-bit signed value `< 0` or `== 0`. A positive value is `high > 0`, or `high == 0 && low != 0`. This is not a one-byte sign check and it does not ignore either half.

## Q2 — full nonpositive gate chain and typed-CNetNPC decision

From the nonpositive-family entry at `0x00444151` through `0x00444234`, the ordered gates are:

1. `0x00444151 -> 0x0043C380`: relationship predicate on the receiver actor, followed by controller vslot `+0x3C`; local runtime/UI relationship state.
2. If that does not select the first style, actor vslot `+0x3C` is an actor-state/death predicate.
3. Actor vslot `+0x74` returns an attached Attr; `0x0043B9E0` performs an NPCAttr typed cast/check. This is an attribute-object check, not the later actor-type check.
4. The NPCAttr linked identity at `attr+0x98/+0x9C` must be nonzero and equal the local actor identity at `[0x01032EC4]+0x78/+0x7C`.
5. `0x00449AF0` requires local actor `+0x3F0` and that context's `+0x38`; `0x00449B10` returns the local scene lookup context.
6. `0x00626DC0` performs exact two-dword actor lookup by the linked identity. Lookup success selects the `0x00444210` path; miss takes the alternate path.
7. The fallback at `0x0044421C -> 0x00469700` is a true `CNetNPC` actor downcast/type test. If it succeeds, `0x0045C160` supplies the final actor-behavior predicate before `0x00444234`.

Critical lane answer: **typed_CNetNPC is a genuine object-type check independent of identity sign/value.** Changing only a FieldMob identity cannot turn that object into `CNetNPC`. Therefore the proposed identity-only route to the typed-CNetNPC tail is rejected.

## Q3 — negative identity registration and lookup

### Main actor registry

- Registration `[0x00446090,0x00446167)`, SHA-256 `29363C8A004FF33F261BD245B90B13451B0775B69671C233555295C7312526B9`, rejects only a null actor pointer and passes both identity dwords unchanged into tree insertion.
- Node copy `[0x006F40D0,0x006F416A)`, SHA-256 `033E7517EB14FBB1D6F9BAF21C0B5B8149B578AB3C1207D0A33FB6E17ECEA2A1`, stores low at node `+0x10`, high at `+0x14`, actor pointer at `+0x18` verbatim.
- Tree insert `[0x005FC970,0x005FCA61)`, SHA-256 `C97047A3030806658AC26A4BF9569114EBBD63FF3DA2B3C34D121C088B56B1A3`, orders by signed high dword then unsigned low dword.
- Lower-bound `[0x00623280,0x00623330)`, SHA-256 `048DBE44589F0EF59F7CF9CDB6844B6EA2324B23F948D92BB29B1304B14A9FE5`, uses the same ordering; find wrapper `[0x00493880,0x0049398D)`, SHA-256 `C3EB941EF8E3C42723AC4940B760D4D5F102E473331821A939C7BD911C94175D`, ends with exact equality.

No sign rejection, truncation, or aliasing was found on this registration path. A negative high dword is retained and sorts before nonnegative keys; only a null actor or an exact duplicate key blocks insertion.

### Selector-local scene lookup

- Context `[0x00449AD0,0x00449B40)`, SHA-256 `816563A67DBC01E559DC0FAD8B3DDB7F199478E1DE68E823A0165C12FAFA5918`, returns the local scene collection after null checks.
- Lookup `[0x00626DC0,0x00626E7A)`, SHA-256 `4E97A02C7947A483D6CC7FB00123FA14E8692D88B51178641DCA5F2D70FC359B`, compares stored low and high dwords for exact equality and returns the actor pointer or null. Signedness is irrelevant to these equality comparisons; there is no truncation or alias inside the lookup.

The missing join is the exact insertion/population path for this selector-local scene list. The main registry and the selector lookup are distinct containers, so the main-tree evidence must not be used to claim that every negative identity necessarily reaches the selector list. Bounded answer: negative identities are not rejected by the proven main registration path, and selector lookup can match a negative bit pattern if present; population of that particular list remains open.

## BUILD_IMPACT

- For LANE-GM name-color work: keep `NameColorGateUnmeasured` for the identity-only FieldMob direction. Do not schedule a negative-identity FieldMob probe expecting it to reach the typed-CNetNPC tail; object type prevents that route.
- Negative identity is not discarded by the proven main actor registry, but selector-scene membership is not yet guaranteed.
- For `/speed` / GT-218: stop treating the container as malformed. `0x12AD` is ActorAttr, and this handler replaces the resident object from the sparse newly constructed object. A safe builder must carry the complete current ActorAttr/BasicAttr state required by the full-copy path, or use a separately proved merge-capable operation; do not retry by tweaking tags or length.

## Nonclaims and continuation checkpoint

- No claim that the 11 bytes missing from the printed GT-218 raw block are any particular transport/header structure.
- No claim that the screen's HP-max value `1` is stored as `1` by this frame; IMAGE proves the omitted resident field is replaced from constructor default zero, while the final display transform is outside Q0.
- No claim that the main registry is the selector-local list or that every actor registered in the former is inserted into the latter.
- No client-observable conclusion is made from this static work.

Resume without repeating this round:

1. Trace the insertion/population path of the scene list consumed by `0x00626DC0` and document any rejection before membership.

Reproducible static verifier: `pf_bridge/staged/re222_static_verify.py`, SHA-256 `949E07E6A72AD7C4C8F4D20D9ECCFBD4816669A9E3583BE1A9B2F0CE3EBE0506`.
