# Codex Attr P0 semantic checkpoint

Read-only pinned-IMAGE/DATA re-derivation now covers 24 unique BasicAttr/ActorAttr gameplay fields (the 23 ordered P0 fields plus evidence-linked BasicAttr +0x68):

- 5 PROVEN_EXACT named bindings: BasicAttr +0x68 n_FACTION; ActorAttr +0x78 GetPpClass; +0x1A0 Navy/Pirate icon selector; +0x1A8/+0x1AC GetBoatHealth current/max.
- 12 PROVEN_ROLE_ONLY fields with exact structural/consumer behavior but no unique broader gameplay noun.
- 7 PARTIAL fields with exact wire structure/defaults but no unique semantic consumer: ActorAttr +0x94,+0x13C,+0x148,+0x1A4,+0xE8,+0x104,+0x120.

True offset-zero inheritance is PROVEN_EXACT for Attribute>DBAttribute>BasicAttr>ActorAttr and Attribute>DBAttribute>CSkillAttr. CSkillAttr is reduced to stored object _Mysize low-u16 count plus repeated node +0x0C/+0x10/+0x14 fields; gameplay record names remain open.

The additive table contains 62 directional/control rows. Semantic evidence is source-separated: 34 IMAGE rows and 4 DATA rows. Frozen A2 conflicts total 96 and are recorded separately; frozen artifacts were not edited.

Outputs:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_FIELD_SEMANTICS.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_SEMANTIC_DELTA.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_UNRESOLVED.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_INHERITANCE.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_SEMANTIC_REPORT.md`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_FOR_SERVER.md`

Reproducer:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\pf_rederive_attr_semantics.py`

No server/client/runtime/test/lease/Git action was taken. No commit or push was made.
