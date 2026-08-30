# Codex Attr P0 conflict checkpoint

Read-only IMAGE re-derivation found 52 directional-row conflicts with the frozen A2 slot34 overlay:

- 48 ActorAttr rows omitted the nested `+0x1BC != 0` group gate.
- 2 ActorAttr rows omitted both their mask gate and the nested group gate.
- 2 ActorAttr mask rows described temporary stack storage instead of the object mask pair at `+0x1B4/+0x1B8`.

The frozen artifact was not edited. Full paired provenance and evidence keys are in:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_CONFLICTS.tsv`

The additive structural correction is:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_A2_ACTOR_CODEC_CORRECTION.tsv`

Related large outputs are in `pf_bridge\external\`. A human must decide whether any new external files should be committed. Codex did not commit or push.
