# PF ground-drop transport - P0-6 static checkpoint

Overall P0-6 status: **PARTIAL**. The client-side pickup request path is closed by exact IMAGE control flow through buffer encoding; persistent server-to-client ground-object issuance/transport remains open.

- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Rows: 19 (`NEW_IMAGE_EVIDENCE` 10; `CANONICAL_REFERENCE` 9)
- All rows use `source=IMAGE`; no evidence layer is mixed within a row.

## Closed static pickup path

A click constructs `PickupTerrainThing`, copies the clicked runtime key into `+0x14`, and queues the nested object. The gameplay flush can wrap the shared list in `GSCN_RunTimeProtocolReq`; the login-phase alternative wraps it in `GSCN_LoginProtocol`. Each flush passes its outer object to `0x00A8D500`: only the ready branch enqueues it, while the refusal branch releases it. Both A8D500 branches return zero and the audited flush callers ignore EAX. A later conditional pump dequeues accepted objects and encodes them through the shared outer and nested writers.

The exact successful registration IDs are `0x4543` for nested `PickupTerrainThing`, `0x6E6F` for the gameplay outer, and `0x453A` for the login outer. These are runtime type IDs. This IMAGE artifact does not promote any of them to a top-level wire opcode.

## Persistent drop transport still open

The custom reflection chain proves `FightingDropModule_Client -> ClientModule` with metadata size `0x34` and `FightingDropNotify -> VitalData` with metadata size `0x50`. The shared descriptor vtable `0x00F36384` is reflection metadata, not a wire vtable. The exact A1 getter/vtable/slot census exposes no concrete canonical wire surface for either class; that bounded negative does not prove the transport is absent.

`TreasurePointAttr` at vtable `0x00F466BC` is an exact rejected false lead. Its getter, descriptor, and paired codec are distinct from the FightingDrop reflection descriptors.

## Evidence reuse

Nine rows authenticate existing `PF_PROTOCOL_REGISTRY.tsv` / `PF_SERIALIZER_FIELDS.tsv` rows by pinned artifact hash, stable selector, and canonical row digest. They do not copy those A1/A2 rows as new evidence. Ten rows carry genuinely new bounded IMAGE spans.

`PF_ATTR_CONFLICTS.tsv` corrects only the frozen RE-125 premise that `0x4543` was name-derived-only and that static evidence could not reach the assigned `PickupTerrainThing` ID. `GDT-IMG-002` through `GDT-IMG-007` separately evidence the click producer, nested queue, outer wrappers, conditional transport acceptance, and buffer encoder; those links are not claimed by the narrower conflict row. Any separate non-IMAGE live-observation conclusion in the frozen note remains outside this IMAGE artifact and is not overwritten.
