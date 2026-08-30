# Codex Attr P0 conflict checkpoint

Read-only IMAGE re-derivation found 544 row conflicts with the frozen A2 slot34 overlay:

- 16 BasicAttr rows omitted the high presence-mask gates for +0x5C/+0x60/+0x68/+0x6C in the frozen BasicAttr and composed ActorAttr contexts.
- 48 ActorAttr rows omitted the nested `+0x1BC != 0` group gate.
- 2 ActorAttr rows omitted both their mask gate and the nested group gate.
- 2 ActorAttr mask rows described temporary stack storage instead of the object mask pair at `+0x1B4/+0x1B8`.
- 20 CSkillAttr rows classified control-flow/import/container helpers as wire fields.
- 8 CSkillAttr rows need corrected persistent/node-relative offsets, composed order, or repeated-record gates. The R entry count is wire loop control and is not a direct object write.
- 306 ItemBag-family rows classified container/control-flow helpers as wire fields.
- 56 CollectionBag-family rows classified post-decode traversal as wire fields.
- 86 ItemBag-family rows need corrected object/node/dynamic-entry layout or composed order across nine classes.

The frozen artifact was not edited. Full paired provenance and evidence keys are in:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_CONFLICTS.tsv`

The additive structural corrections are:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_ACTOR_CODEC_CORRECTION.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_BASIC_CODEC_CORRECTION.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_CSKILL_CODEC_CORRECTION.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_ITEMBAG_CODEC_CORRECTION.tsv`

Related large outputs are in `pf_bridge\external\`. A human must decide whether any new external files should be committed. Codex did not commit or push.
