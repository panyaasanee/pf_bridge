# PF Attr class census - active checkpoint

This is a direct IMAGE re-derivation. Frozen A1-A6 outputs were not copied as evidence.

- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Whole registry census: 519 exact registration stubs
- Registry names containing Attr/Attribute/DataSet/Module: 140
- `REGISTRY_VTABLE_CODEC_LINKED`: 128
- `RTTI_NAME_ONLY`: 11
- `RTTI_VTABLE_CODEC_LINKED_NO_REGISTRY`: 1

## Current evidence ceiling

The census lists 139 relevant registered classes plus the RTTI-only nested PetAttr dependency. Thirty-three exact inheritance edges are currently proved in `PF_ATTR_INHERITANCE.tsv` (32 join rows in this class census; `CommunityActorAttr` is inheritance-only outside it); the separate 128-class remaining census is structurally classified in `PF_ATTR_REMAINING_CODEC_CENSUS.tsv`. Any row still carrying `parent_chain=UNKNOWN` is deliberate. A decorated TypeDescriptor name alone is never used to guess a parent, vtable, or serializer.

Codec ownership is table-bounded. Ordinary Attr rows use their proved `+0x34` role, while `UpdateAttrVital` and `Express_ClientGetExpressItemAttrsVital` have 0x24-byte primary tables and paired W/R codecs at `+0x18`; their nominal `+0x34` values belong to adjacent registered Vital classes. The 128-class remaining census records both the physical slot-34 role and the owning codec slot.

The census is structural coverage, not semantic completion. `NOT_WIRE` fields are reported separately in the A2 delta and do not count as semantic success.
