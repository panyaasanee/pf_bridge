ถึง chief

# RE-314 — DONE/PASS: UpdateAttrVital `0x309A` calls the real ActorAttr codec

- Status: **DONE/PASS — jobs 1–3 closed**
- Ticket START: `2026-09-08T15:36:54.913+07:00`
- Ticket source: `CLIENT_RE_QUEUE.md` SHA-256 `B0D2BDA9B9BCDFC3E5C20868BAF6BABB3BD90022D71EF4D2DD5EB4B803E0D1B3`; RE-314 block lines 1049–1068, normalized UTF-8/LF SHA-256 `6E8D7486A3DFE3811DC093CE4358153A95A03E132D68FD5AF22316DBFBED9E28`
- Client image: `GameClient.local.bin`, 14,759,424 bytes, SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
- Route note: header text spells `static-on-bridge` in lowercase, which the taglint route parser reports as missing; the ticket body explicitly says `[STATIC-ON-BRIDGE]`, so this is the eligible RE/static ticket. Please normalize the header tag when folding the result.

## Mandatory searches

- `pf_bridge/external/`: searched recursively once across 2,683 files / 930,201,065 bytes; metadata fingerprint `24E070C06819DB8AA4F288903C38A85F4CCE23D3521220D0546071D0E17CA533`. Relevant hits include `PF_SERIALIZER_SLOT34_ROOTS.tsv`, `PF_ATTR_CLASS_CENSUS.tsv`, `PF_ATTR_CONTAINER_SEMANTICS.tsv`, `PF_ATTR_FIELD_SEMANTICS.tsv`, `PF_ATTR_NAME_COLOR_SELECTOR.tsv`, the protocol/serializer registries, RE-222, and the RE-310 addendum.
- `pf_bridge/gamedata/`: searched recursively once across 1,109 files / 15,319,585 bytes; metadata fingerprint `16A608DB22FD2B24470212AD04401875816C8C785B915AC0C3F28ABFFCC24800`. Only one file matched the broad numeric query: `scene/bg0004/bg0004.placements.tsv`, where `0x0000309A` is merely a placement/object id on lines 105–106. There is no field or protocol crosswalk, so this hit was rejected as irrelevant. No `ActorAttr`, `0x00466230`, `0x1A0`, or `Navy_Pirate_icon_selector` semantic hit was found in gamedata.
- Existing answers were accepted only after SHA verification against the same pinned image. Mailbox root+consumed was content-read once: 7,398 files / 42,978,086 bytes, content-manifest SHA-256 `897015908BFE255FDEDDEEA77935E633BE9BF6C89B6E6BF6BBD6064D9452F17F`.

## Job 1 — exact caller of `0x00466230`

`0x00466230` has no direct code xref. Its only absolute image reference is the pointer at `0x00F0E7D4`, which is `ActorAttr` vtable `0x00F0E7A0 + 0x34`. Therefore the real call is necessarily virtual; the registry's `serializer_va=0x0043BB80` is the unrelated empty `ret 8` stub and is not a caller.

The concrete caller is the generic attribute-container codec `[0x00463DE0,0x00463FA2)`, SHA-256 `888C2FAC20948B7896ED105F46B84E94D01C9442F6535DF9BE36E6BAA2335FC3`, reached from `UpdateAttrVital` serializer wrapper `0x005E42C0`:

- write side: `0x00463EB0` loads the entry object's vtable, `0x00463EB2` loads slot `+0x34`, and `0x00463EB7` calls it;
- read side: `0x00463F3B` reads the u16 factory type key, `0x00463F5C` creates the typed object, and `0x00463F78..0x00463F7E` loads/calls its vtable slot `+0x34`.

The required class crosswalk is not id equality: the registered-name checksum algorithm gives `checksum("ActorAttr") & 0xFFFF = 0x12AD`; image registration binds that name to vtable `0x00F0E7A0`, whose slot `+0x34` is exactly `0x00466230`. The outer vital uses the same proved named-id algorithm: `checksum("UpdateAttrVital") & 0xFFFF = 0x309A`. Thus **the containing frame/caller route is UpdateAttrVital `0x309A`, with an entry type key `0x12AD` dispatching to ActorAttr codec `0x00466230`**.

This verifies and reuses RE-222 (`20260903_2149...`, current SHA-256 `17EDEE9B01CAA8EFCF5CCE4D792FE4ADC63978808B57A6CE02B3455F86F460C5`) rather than relying on its ids alone. Current structural tables are also pinned: `PF_ATTR_CONTAINER_SEMANTICS.tsv` `E58E6E9B3B7DF7089336AB0F7DF042079BE0266BE3938DA5DA63708FA98282F1`, `PF_SERIALIZER_SLOT34_ROOTS.tsv` `D544D8A7825E9EEB221ED887F51CC00F94CB6868E32DCD44F415C82C5A050E59`, and `PF_ATTR_CLASS_CENSUS.tsv` `82B02F402005BA7B1D51A97E0EABA2BC89DCFDF884D91ECD61BD3542972EFA11`.

## Job 2 — `ActorAttr+0x1A0` is not a name-colour selector

The two repository files describe different layers and do not conflict:

- `PF_ATTR_FIELD_SEMANTICS.tsv` has paired R/W rows for `ActorAttr@0x1A0.1`, gated by ActorAttr's second mask dword bit 0 (overall bit `1<<32`), wire tag `0x0B`, length 1. Its semantic name is **`Navy_Pirate_icon_selector`**, status `PROVEN_EXACT`, from the independent semantic path `0x0053D3C4 -> 0x0053E8B5`.
- The ticket-cited `0x0046664C` is not that semantic consumer. It is the **write-side wire consumer/sink** in the ActorAttr codec. The semantic consumer column is `0x0053E8B5`. On read, the paired decode writes through a pointer at `0x00466B73`.
- `PF_ATTR_NAME_COLOR_SELECTOR.tsv` has 14 data rows plus its header (the ticket's “15 rows”) and is an exhaustive decision table for function `0x00443F50`. It has no `+0x1A0` row because that function does not read the icon selector. It does read other inputs, including `ActorAttr+0x98`, identities, relationship/type gates, and faction/offensive state.

Conclusion: **`ActorAttr+0x1A0` is the Navy/Pirate icon selector; it is not an input to the name-colour selector at `0x00443F50`.** The apparent contradiction came from reading the wire sink `0x0046664C` as if it were the semantic/UI consumer.

Pinned files: `PF_ATTR_FIELD_SEMANTICS.tsv` SHA-256 `1418B7559F5B05FEEF585490E76D33E8F72CD82C1FF854941D7FAF37878C7F2F`; `PF_ATTR_NAME_COLOR_SELECTOR.tsv` SHA-256 `D15864A21A7A124A23F6DFFAD174A55D376045A25A04814BBE6DC5F5632AF82D`; RE-310 addendum SHA-256 `46D52B7A52A1E1ABDE11F49C133EB31DC482AEC1758878ABA66428A92538A754`.

## Job 3 — actor-appear alternative

The conditional does not fire: job 1 proves the caller is `UpdateAttrVital` `0x309A`.

For completeness, the actual named actor-appearance vital is `CreateActorVital`, named id `checksum("CreateActorVital") & 0xFFFF = 0x36CF`, serializer `0x005EB3B0`. Its `CreateActorDataEx` subcodec `[0x005DFF60,0x005E01C6)` does **not** supply this ActorAttr route:

- embedded `+0x60` is constructed by `0x00464080` as `AvatarAttr`; vtable `0x00F0E088 + 0x34 -> 0x00464560`;
- optional `+0xF0` is allocated from pool `0x01031420`; concrete constructor `0x0046F3F0` writes vtable `0x00F0ECB8`, identified as `ItemBagAttr`; its slot `+0x34 -> 0x0046F180`.

Therefore `CreateActorVital` is a real actor-appear frame, but it is not an alternative caller of ActorAttr codec `0x00466230` in this route.

## BUILD_IMPACT

- Correct the stale registry interpretation: for ActorAttr wire work, use vtable slot `+0x34 -> 0x00466230`; do not use stub `0x0043BB80` as the serializer/caller.
- A server-side ActorAttr update belongs in `UpdateAttrVital` `0x309A`, entry type `0x12AD`. For `+0x1A0`, encode tag `0x0B`, one byte, with overall mask bit `1<<32` present.
- Do not use `CreateActorVital` `0x36CF` as a substitute for changing `ActorAttr+0x1A0`; its nested attributes here are AvatarAttr and optional ItemBagAttr.
- Preserve RE-222's safety warning: the UpdateAttr handler full-copies the fresh decoded ActorAttr over the resident ActorAttr. A sparse frame can zero omitted constructor-default fields. Any builder must carry the complete required current state or use a separately proved merge-capable path.
- No name-colour work should be based on `+0x1A0`; the exact `0x00443F50` selector table has no such input.

## Nonclaims

- No claim that `0x0043BB80` is a caller; it is only the stale registry-selected empty stub.
- No claim that the cancelled nine-row appendix was ever used to decide GT-288. R324A answered its question before RE-314 opened.
- No claim about which byte value selects Navy versus Pirate, nor about the on-screen icon result; this ticket is static and no game/client-observable test was run.
- No claim that arbitrary equal numeric ids across protocol, placement, or data files form a crosswalk. The only accepted mappings above use the registered-name checksum plus image vtable/codec bindings.
- No claim that every possible slot-`+0x34` caller in the whole image was exhaustively enumerated. The proved result is the exact UpdateAttrVital path requested, plus a bounded check of the named CreateActorVital alternative.
- No source, queue, external, gamedata, server, client, DB, or git state was modified.
