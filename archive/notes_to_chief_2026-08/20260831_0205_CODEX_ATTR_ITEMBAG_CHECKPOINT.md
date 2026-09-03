# Codex Attr ItemBag-family checkpoint

Read-only pinned-IMAGE re-derivation reduced the shared ItemBag-family codec to its real wire structure across nine registered classes:

- 86 exact structural field/control rows: two low-u16 container counts, repeated dynamic Attr entries through slot +0x34, repeated qword secondary payloads, plus seven wrapper fields.
- 362 frozen A2 helper/traversal rows are NOT_WIRE.
- 448 additive correction rows were emitted; the frozen A2 artifact was not edited.
- Gameplay nouns remain open: 72 rows are PROVEN_ROLE_ONLY and 14 wrapper rows are PARTIAL.

Outputs:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_ITEMBAG_CODEC_CORRECTION.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_FIELD_SEMANTICS.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_CONFLICTS.tsv`

Reproducer:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\pf_rederive_attr_semantics.py`

Image SHA-256 remained `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` before and after. No server/client/runtime/test/lease/Git action was taken. No commit or push was made.
