ถึง chief

# RE-316 — DONE/PASS: CharCreate does not write a skill-point field

- Status: **DONE/PASS — bounded negative accepted by COO**
- Ticket START: `2026-09-08T20:59:15.122+07:00`
- Ticket source: `CLIENT_RE_QUEUE.md` SHA-256 `13D357BA12E8FA328A76349145312AA18906C441519E6F5CCC30062FF8DB341A`; RE-316 block lines 1080–1109, normalized UTF-8/LF SHA-256 `B1FC5F506B38DCB53C2D1DD11E973F8FB3306930D3906230542D8FBEAD94E37E`
- Client image: `GameClient.local.bin`, 14,759,424 bytes, SHA-256 `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`
- Route note: the ticket deliberately has no `[STATIC-ON-BRIDGE]` tag because cloud lacks the image. This runner is on the bridge, has the pinned image, and the ticket is explicitly non-attended, so it was eligible under the missing-route assessment rule. Please normalize the route metadata when folding the result so taglint and the prose do not disagree.

## Answer

**The CharCreate/CreateChar send path writes no skill-point field.** The exact skill-point field elsewhere in the character model is `ActorAttr` u32 `+0x7C`, mask bit `0x00000008`, but the create request does not carry `ActorAttr` at all. Consequently the original server's birth amount is **not measurable from this client request**.

`ActorAttr`'s constructor writes zero to `+0x7C` at `0x00464CDB`, but that is only the client-side default of a newly constructed attribute object. It does not prove the value the original server persisted or returned for a new character. Therefore the current server value `BIRTH_SKILL_POINTS = 0` remains an **ASSUMPTION**, exactly as COO's 2026-09-08 16:42 decision requires for this negative outcome; it must not be relabelled `MEASURED`.

## Mandatory searches

- `pf_bridge/external/`: searched recursively once across 2,683 files / 930,201,065 bytes; metadata fingerprint `24E070C06819DB8AA4F288903C38A85F4CCE23D3521220D0546071D0E17CA533`. Ten files matched the broad skill-point/create terms. Relevant evidence was the existing character-attribute semantics and serializer inventory. `PF_ATTR_FIELD_SEMANTICS.tsv` identifies the unrelated `CSkillAttr` per-skill progress field, not a global birth balance; no crosswalk from a CHARCREATE column to birth skill points exists.
- `pf_bridge/gamedata/`: searched recursively once across 1,109 files / 15,319,585 bytes; metadata fingerprint `16A608DB22FD2B24470212AD04401875816C8C785B915AC0C3F28ABFFCC24800`. The 248 matching files are Lua `AddSkillPoint`/criteria calls and SP tables for level, mob, quest, guild, or PVP. None declares a birth value. `s_SKILL_1..4` in CHARCREATE data are skill ids, not point counts.
- Mailbox root+consumed was content-read once: 7,657 files / 43,851,855 bytes; content-manifest SHA-256 `2B069E9AF0FA0F9A165BA7D0434E2CFF9D2D718F341AF5097FC39393724D4949`. The controlling COO decision explicitly says that if the client does not write the field, the negative answer is accepted and the `ASSUMPTION` label stays permanently.

## Static path proof

1. The creation-success branch is the function-anchored image span `[0x004B4621,0x004B4757)`, SHA-256 `C506375D3E8F9C67628375B6C6584B315A293F399B3E10DDBD2D1ACFFF750C4E`. At `0x004B4733` it allocates a `CreateActorVital`; `0x004B473E..0x004B4741` attaches the prepared `CreateActorDataEx` object; `0x004B4747` writes operation byte `1`; and `0x004B4752` enqueues the vital.
2. The registered-name crosswalk, not numeric-id coincidence, identifies the object: `PF_PROTOCOL_REGISTRY.tsv` binds `CreateActorVital` to named id `0x36CF`, vtable `0x00F3017C`, serializer `0x005EB3B0`, and handler `0x005EFD50`.
3. Serializer span `[0x005EB3B0,0x005EB47A)`, SHA-256 `038A2BF9EF058139576FA48BD4F29DCBE14D7E3D3215B29D536047AC8E7BB34B`, emits the operation byte and optional payload, then calls the `CreateActorDataEx` codec at `0x005DFF60`.
4. The complete function-anchored `CreateActorDataEx` codec `[0x005DFF60,0x005E01C6)`, SHA-256 `DE9DE2A04F4AC3EC8E6C07550336EEA2BE18954143C5C0DE1823A4A2171E3F8A`, serializes fixed scalars/strings, embedded `AvatarAttr` at `+0x60`, optional `ItemBagAttr` at `+0xF0`, and two trailing u32 fields. Its W-side inventory has 26 codec actions and no `ActorAttr` subcall or `+0x7C` field.
5. The required class crosswalk was already proved and reverified against the same image: the embedded `+0x60` object's vtable/slot resolves to `AvatarAttr`; the optional `+0xF0` object resolves to `ItemBagAttr`. Equal ids were not used to infer either class.
6. Independently, `ActorAttr` constructor span `[0x00464BE0,0x00464E40)`, SHA-256 `ED79407AE32BD3F75EAD5D828615D6168A5A941203F26E3106D2B01E7E48CC0C`, explicitly stores zero at `ActorAttr+0x7C` (`0x00464CDB`). The established UI consumer `0x0075C613 -> NUMBERLABEL_SPNOW` identifies that field as the current unspent skill-point balance. This establishes the field and its object default, not a server-issued birth award.

Pinned support files: `PF_PROTOCOL_REGISTRY.tsv` `27DAAC0C6FBBC45D88281C31B98E3A8B56F421BD1E8BC16F970FDFF5716CFB4D`; `PF_SERIALIZER_FIELDS.tsv` `99282BDF3F492EAEBDBAB4918AECC0E37BF8EFB42B904B18E1BA306767B5C123`; `PF_ATTR_FIELD_SEMANTICS.tsv` `1418B7559F5B05FEEF585490E76D33E8F72CD82C1FF854941D7FAF37878C7F2F`; `PF_ATTR_DATA_BINDINGS.tsv` `67E7550A09B00A5243F4C084FF486D29E420C6D0687704A092F157DBCE219CB2`.

## BUILD_IMPACT

- Keep `BIRTH_SKILL_POINTS = 0` and `BIRTH_SKILL_POINTS_PROVENANCE = "ASSUMPTION"`; do not name a shipped table and do not flip the label to `MEASURED`.
- Do not add a skill-point field to the client `CreateActorVital` request. The original request does not carry `ActorAttr`.
- If the reconstruction needs an authoritative birth value later, it must come from an original-server artifact or an independent observed post-create `ActorAttr` result, not from this client send path.
- No server/client source, queue, external, gamedata, DB, or git state was changed.

## Nonclaims

- No claim that the original server definitely gave zero skill points. Zero is the current owner-ordered assumption and the client object's constructor default only.
- No claim that absence of `SetSkillPoint` proves zero.
- No claim that `s_SKILL_1..4` are point balances; they are skill ids.
- No claim that a flat linear disassembly proves absence. The negative is bounded to the exact creation sender, named protocol object, complete serializer function, complete nested codec function, and typed subobject crosswalks.
- No client-observable behavior was tested and the game/server were not started.
