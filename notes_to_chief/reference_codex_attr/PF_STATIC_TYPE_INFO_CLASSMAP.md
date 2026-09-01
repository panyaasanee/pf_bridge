# Static type_info class map (IMAGE)

## [MEASURED][IMAGE] Controls

Pinned image SHA-256: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`. Rows: **4**.

The complete aligned getter/marker census still has two candidates for `ItemAttr` and two for `VitalData`. Slot 0 descriptor getters plus the pinned MSVCR90 `type_info::_name_internal_method` import and exact static-initializer/RTTI edges identify the four static class identities shown in the TSV.

## [MEASURED][IMAGE] Descriptor backing

The descriptor-storage VAs are in the unbacked `.data` BSS tail (raw-backed end VA `0x0102BE00`), so every `descriptor_file_off` is `UNMAPPED_BSS`. No descriptor bytes were read or hashed. Backed MSVC TypeDescriptor names are separate IMAGE evidence.

## [MEASURED][IMAGE] Interpretation guard

`StallItem` shares the `ItemAttr` registry getter, and `Channel_MessageVtial` shares the `VitalData` registry getter. This establishes static class-hierarchy and registry-getter sharing only; it does **not** imply a runtime observation and does **not** justify collapsing or merging their serializer schemas. The base links are `StallItem -> ItemAttr` and `Channel_MessageVtial -> Channel_BasicVtial -> ClonableVital -> VitalData`.

## [MEASURED][IMAGE] Delta accounting

- Newly decoded A2 rows: **0**.
- Existing exact `ItemAttr` candidate references (`VTABLE_0x00F0EBB0`): **26**.
- Physical duplicate class-map rows: **0**.
- Priority-1 closures: **0**.
- Evidence source: **IMAGE** only. No DUMP, CAPTURE, or DATA evidence is mixed into these rows.

This is an identity artifact only; it does not select a canonical ItemAttr schema and does not change A2/status/manifest/index files.
