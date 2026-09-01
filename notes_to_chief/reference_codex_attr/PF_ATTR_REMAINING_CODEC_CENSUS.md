# PF Attr remaining codec census - active checkpoint

This is an IMAGE-only structural census of 128 registry classes. Rows already decoded in active field overlays remain present with an explicit detail status; this is not a gameplay-semantic completion claim.

- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Remaining registry classes: 128
- Paired codecs at their proved owning slot: 42
- Physical slot +0x34 paired codecs: 40; paired codecs at exceptional slot +0x18: 2
- Of the paired codecs, 42 classes are already decoded in active field overlays; 0 class codecs still need field-level decode.
- Empty/no-payload slot +0x34 routines: 50
- Concrete non-codec slot +0x34 routines: 26
- Attr-filter rows whose nominal +0x34 crosses into another registered class table: 2
- Getter/vtable recovery still open: 10
- Registry aggregate: `b025dc45edcdbd3957edea434c92b4b5a6375db0010ae441958752d84cf0e73d` (128 records / 6649 bytes)
- Bounded-vtable/audit-window aggregate: `1e5d7b1c3033dba0367f49f3948033d238ef95211e47c46b2cc7bef52ba31d50` (118 records / 9864 bytes; exact 0x24 for the two bounded Vital tables, 0x38 evidence windows for the other rows; the latter are not table-length claims)
- Getter aggregate: `f124f615463be43748fb0da96d27ed3d79180aa4cb1c6cacb3ade8e86ce4a1fd` (118 records / 4122 bytes)

## Interpretation

`P0_STATE_CODEC` means the proved owning slot is a paired read/write state codec and should be decoded next. `P1_BINDER_OR_ACCESSOR` must not be mistaken for a wire codec. `P2_NO_PAYLOAD` is structurally empty at +0x34, subject to the explicit cross-artifact closure conflicts. `P3_RECOVERY` still lacks a unique getter/vtable link.

`UpdateAttrVital` and `Express_ClientGetExpressItemAttrsVital` are boundary exceptions: their primary tables end before +0x34, their paired codecs are at +0x18, and the old nominal +0x34 values belong to `ReliveVital` and `Express_ClientSendExpressVital` respectively.

`FightingDropModule_Client` is no longer parent-UNKNOWN: its custom reflection descriptor proves immediate parent `ClientModule` and metadata size `0x34`. This does not close its codec. Descriptor vtable `0x00F36384` is reflection metadata, not a wire vtable, and the exact A1 getter/vtable/slot census still finds no concrete canonical wire surface; the remaining row therefore stays `P3_RECOVERY` with a concrete-wire-surface blocker.

Highest-yield undecoded groups are object/world adjuncts, collection/progression, and quest/reward. Bag/storage structure is already represented in the detailed ItemBag-family overlay.
