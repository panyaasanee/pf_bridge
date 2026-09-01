# UpdateAttrVital A2 Attr-semantic delta - checkpoint 1

This delta does not edit the frozen `PF_SERIALIZER_FIELDS.tsv`. It uses that file only to name the 26 base rows, then re-derives every correction from IMAGE control flow.

- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Generic carrier span: `0x00463DE0..0x00463FA2`
- Span SHA-256 (end-exclusive): `888c2fac20948b7896ed105f46b84e94d01c9442f6535df9be36e6baa2335fc3`
- Base UNKNOWN rows reviewed: 26
- Wrong-direction duplicate rows removed from the effective view: 13
- `NOT_WIRE`: 9
- `PROVEN_EXACT`: 15
- `PARTIAL`: 2

## Re-derived envelope

Write mode emits an entry count (tag 0x12), then for each entry emits a type/key (tag 0x12), reserves a payload-length field (tag 0x14), dispatches the concrete Attr serializer through object vtable slot +0x34, and backpatches the measured payload length.

Read mode reads count, type/key, and payload length. It asks the type factory for a concrete Attr object. Unknown type IDs advance the stream cursor by the declared length; known types dispatch vtable slot +0x34 and insert the object into the container.

## Remaining real blocker

Two rows remain `PARTIAL`: the W and R nested payload dispatches. The carrier is intentionally polymorphic, so static analysis cannot select one serializer without the runtime type ID. The next step is a type-ID-to-class/vtable map followed by CAPTURE validation per payload type. This is not the same as the 24 resolved bookkeeping rows.

No raw DUMP or CAPTURE bytes are included.
