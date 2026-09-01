# Codex Attr A5 checkpoint

Offline read-only CAPTURE validation completed against the two pinned manifests.

- ActorAttr R: 335/335 physical frames matched; 0 mismatches. The frozen delta contributes 201 claim-unique frames and observes all 60/60 primitive orders.
- CSkillAttr R: 10/10 physical frames matched; 0 mismatches. The delta contributes 2 claim-unique frames and observes all 6/6 positions.
- UpdateAttr wrapper mismatches: 0.
- Physical and claim-unique populations remain separate.
- 24 current capture files are absent from both pinned manifests. They are reported by path/count/SHA-256 only and excluded from every accepted count.
- No raw capture bytes, payload values, or hexdumps were emitted.

Outputs:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_FIELD_VALIDATION_DELTA.tsv`

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\PF_ATTR_FIELD_VALIDATION_DELTA.md`

Reproducer:

`C:\Users\Panya\Desktop\Pirate Force\pf_bridge\external\pf_rederive_attr_capture_validation.py`

Independent root `--check` passed with the image unchanged. Codex did not run the client/server/tests, edit the lease, commit, or push.
