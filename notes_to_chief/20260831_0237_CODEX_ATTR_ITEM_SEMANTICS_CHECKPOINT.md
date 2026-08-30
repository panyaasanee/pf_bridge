# CODEX Attr ItemAttr semantic checkpoint

- Scope: read-only static analysis of the pinned original client IMAGE.
- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` before and after.
- New exact ItemAttr bindings, kept source=IMAGE:
  - `+0x30`: item-definition lookup key; exact consumer obtains `s_ID_ICON`.
  - `+0x34`: linear container slot index; exact page window is 80 slots.
  - `+0x36`: ItemControl quantity-display value; exact widget storage is parent `+0x1810`, value `+0x220`.
- Both ItemAttr vtable schemas and both W/R directions are represented separately: 12 rows promoted to `PROVEN_EXACT`.
- Attr semantic-delta rows: 50 (was 38).
- Attr unresolved rows: 148 (was 160).
- Frozen A1-A6 artifacts were not edited; conflict census remains 616.
- No server/client/runtime/test/lease/Git action was taken.

Primary outputs:

- `pf_bridge/external/PF_ATTR_FIELD_SEMANTICS.tsv`
- `pf_bridge/external/PF_ATTR_SEMANTIC_DELTA.tsv`
- `pf_bridge/external/PF_ATTR_UNRESOLVED.tsv`
- `pf_bridge/external/PF_ATTR_SEMANTIC_REPORT.md`
- `pf_bridge/external/PF_ATTR_FOR_SERVER.md`
- `pf_bridge/external/pf_rederive_attr_semantics.py`
