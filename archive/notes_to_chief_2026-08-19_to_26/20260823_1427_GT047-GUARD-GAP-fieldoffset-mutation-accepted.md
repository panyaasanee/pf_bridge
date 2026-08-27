# GT-047 RUNTIMEPROTO-CAPTURE-VALIDATE-001 — GUARD GAP / keep PENDING

- Time: 2026-08-23 14:21-14:27 (+07:00)
- Code repo HEAD observed: `9e42cb7` (tester did not edit repo/source/tools/tests/queue)
- Suggested queue state: keep **PENDING / TOOL-GUARD-GAP**. Do not mark PASS or VALIDATED.
- LOCK_GAME/LOCK_GIT: not held; this ticket is STATIC-ON-BRIDGE and used no server, client, or DB.

## Result

### Baseline capture validation

- Job `1027_gt047_capture_validate_baseline.ps1` correctly refused the live capture tree because captures added after the frozen inventory made the fresh path set differ.
- Job `1028_gt047_inventory_mirror_validate.ps1` created a same-volume hard-link mirror containing only the 1,772 frozen inventory inputs; original captures and inventory were not edited.
- Validator exit 0 on that frozen view:
  `capture_files=1772 blocks=51894 nested_declared=13220 nested_reached=12785 pass=11904 static_open=52775 mismatch=0 unresolved_after_open=435`.
- Target rows in `PF_FIELD_VALIDATION.tsv`:
  - `GSCN_RunTimeProtocolReq` W: observed 40,747; A2_STATIC_OPEN 40,747; mismatch 0; status `A2_STATIC_OPEN`.
  - `GSCN_RunTimeProtocolRes` R: observed 10,073; A2_STATIC_OPEN 10,073; mismatch 0; status `A2_STATIC_OPEN`.
- Therefore the requested F2 transition to VALIDATED did **not** occur. Zero mismatch here does not promote either outer message while all target frames remain static-open.

### Re-derive

- Job `1031_gt047_rederive_protocol.ps1` copied the extractor into an empty directory and re-derived from `GameClient.local.bin`.
- Exact byte matches:
  - `PF_PROTOCOL_REGISTRY.tsv` `27DAAC0C...16CFB4D` (519 rows)
  - `PF_SERIALIZER_FIELDS.tsv` `99282BDF...B5C123` (6,931 rows)
  - `PF_TAG_CENSUS.tsv` `63BC9A03...AEA337A` (11 rows)
- Image SHA before/after unchanged: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623`.

### Required field_offset mutation guard — decisive negative result

- Job `1030_gt047_fieldoffset_mutation_retry.ps1` mutated only a temporary copy:
  `TargetPosVital:W:1 field_offset +0x14 -> +0x99`.
- Baseline field TSV SHA: `99282BDF...B5C123`; mutated temp SHA: `F13839C8...162A45`.
- Mutated validator still returned exit 0 with the exact same totals and `mismatch=0`.
- This is the ticket's mandated guard failure: the validator currently accepts the `field_offset` corruption and does not turn red. Job `1029` was an invalid first attempt caused by Start-Process path quoting and is superseded by clean job `1030`.
- Tester role did not patch `pf_validate_capture_fields.py`; chief/tooling owner must add a guard that demonstrably rejects this mutation, then rerun the ticket.

## Artifacts

- `outbox/1028_gt047_inventory_mirror_validate.out.txt`
- `outbox/GT047_inventory_mirror_validate.log.txt`
- `outbox/1030_gt047_fieldoffset_mutation_retry.out.txt`
- `outbox/GT047_fieldoffset_mutation_retry.stdout.txt`
- `outbox/1031_gt047_rederive_protocol.out.txt`
- hard-link frozen view: `pf_bridge/gt047_inventory_mirror_job1028/`
- temporary mutated handoff: `pf_bridge/gt047_fieldoffset_mutation_job1030/`

## Nonclaims

- This does not validate the whole protocol registry; 980 pairs remain NOT_OBSERVED and the reported corpus is highly skewed as documented by F1/F3.
- `mismatch=0` is not evidence that the two target messages are VALIDATED; their target rows explicitly remain A2_STATIC_OPEN.
- No tag meaning beyond the shipped length model is claimed.
- No client-observable, runtime game, server, wire-session, or DB claim is made by this static ticket.
- The reconstruction remains our design work; it is not proof of the original server, which is gone.
