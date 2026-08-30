# Codex Attr item-detail checkpoint

Read-only pinned-IMAGE re-derivation now separates both ItemAttr vtable schemas and the nested ItemVaryAttr codec:

- ItemAttr: 34 exact structural rows. The two schemas each carry six fixed fields plus an optional ItemVaryAttr presence flag/payload; the extended schema appends one dword.
- ItemVaryAttr: 6 PROVEN_EXACT rows for entry count, type code, and subtype payload.
- Exact type-code routing: below 99 -> ItemVaryData_Value; 99 through 118 -> ItemVaryData_String; 119 or above -> ItemVaryData_Embeded (client spelling).
- 72 additive A2 correction rows were emitted; 44 are NOT_WIRE helper/lifecycle rows. Frozen A2 was not edited.

Outputs:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_ITEMATTR_CODEC_CORRECTION.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_ITEMVARY_CODEC_CORRECTION.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_FIELD_SEMANTICS.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_CONFLICTS.tsv`

Reproducer:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\pf_rederive_attr_semantics.py`

Image SHA-256 remained `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` before and after. No server/client/runtime/test/lease/Git action was taken. No commit or push was made.
