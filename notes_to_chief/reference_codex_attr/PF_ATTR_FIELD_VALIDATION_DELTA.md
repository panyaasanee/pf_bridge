# PF Attr field validation delta

[MEASURED] Offline read-only A5 validation.  All result rows have
`source=CAPTURE`; IMAGE/A2 material is only the comparator and is not copied as
a CAPTURE fact.

## Result

| schema | dir | population | instances | mismatches | observed primitive orders |
|---|---:|---|---:|---:|---:|
| ActorAttr | R | BASELINE_PHYSICAL | 69 | 0 | 19/60 |
| ActorAttr | R | DELTA_PHYSICAL | 266 | 0 | 60/60 |
| ActorAttr | R | COMBINED_PHYSICAL | 335 | 0 | 60/60 |
| ActorAttr | R | DELTA_CLAIM_UNIQUE | 201 | 0 | 60/60 |
| CSkillAttr | R | BASELINE_PHYSICAL | 0 | 0 | 0/6 |
| CSkillAttr | R | DELTA_PHYSICAL | 10 | 0 | 6/6 |
| CSkillAttr | R | COMBINED_PHYSICAL | 10 | 0 | 6/6 |
| CSkillAttr | R | DELTA_CLAIM_UNIQUE | 2 | 0 | 6/6 |

- UpdateAttr wrapper mismatches: `0`.
- ActorAttr corrected Basic high-mask gates are applied at composed orders
  `14-17`.
- ActorAttr corrected nested `+0x1BC` gate is applied at composed orders
  `22-43`, `50`, `61`, and `62`.
- ActorAttr mask storage is treated as the paired object fields at `+0x1B4`
  and `+0x1B8`, never as the old stack-temporary claim.
- CSkillAttr is parsed as its inherited DBAttribute prefix, one record-count
  primitive, and repeated three-primitive records.

## Physical versus claim-unique

`BASELINE_PHYSICAL`, `DELTA_PHYSICAL`, and `COMBINED_PHYSICAL` retain repeated
frames.  `DELTA_CLAIM_UNIQUE` hashes the entire decompressed/PC block, rejects
anything already present in the baseline, then rejects later duplicates in the
delta.  The two populations are kept separate; claim-unique counts do not
replace physical validation counts.

Baseline text census: `918` files / `98590688` bytes; manifest `95f574e49b20957a025fd9d98dcfd888a51a76e2393ea169f99d147e3d69d447`.

Delta text census: `353` files / `68690435` bytes; manifest `7a2aa6b8b073e6b87d5949e53d8ff1aea790bc9da398e55e1beee9422ae4904c`.

## Current-inventory blocker

Exactly `24` files currently under `capture_*` are absent from
both pinned manifests.  They are excluded from every accepted validation count.
This run reads only their filesystem metadata and SHA-256; it does not open their
text through the packet parser.  Combined metadata manifest:
`46acdeebec044cdeee21a7f3d2c234b2d2f4038d1ac6788df5b52889ae97de4a`.

- `capture_gt127_20260830_170453/capture/gm_command_log.ndjson` size `2616` SHA-256 `2672873ff4246cb67de36a811686cb29098d2d44fb8b943a6b04de72a589678f`
- `capture_gt127_20260830_170453/capture_v141/GAME_20260830_170625_586379_49334.txt` size `169867` SHA-256 `39155a594d5dd880b89a0e0a37a3dcf93e0af5580b7e60735c8ae30da1c04098`
- `capture_gt127_20260830_170453/capture_v141/GAME_20260830_171140_163674_49674.txt` size `448031` SHA-256 `4f2e632b3b34e377df74ba2378da6725a0743788b22191eeb078c20dbfb682f9`
- `capture_gt127_20260830_170453/capture_v141/GAME_EVENTS_LIVE.txt` size `2811` SHA-256 `bdf8a1012ff851ae0b471c32713dfc541e45cb5ca0e9b36f32026c4e213b2d13`
- `capture_gt127_20260830_170453/capture_v141/GAME_LIVE.txt` size `42843` SHA-256 `5382a5ae6ad0af12b43eafee0b3a1c471a27798607859dbad8fd7a0dbc22ce37`
- `capture_gt127_20260830_170453/capture_v141/LOGIN_20260830_170547_649818_62065.txt` size `2326` SHA-256 `e69fcf13e19c5929f8c84213fc8f2218d68b908890f00f076905c9fec6ee7a5b`
- `capture_gt127_20260830_170453/capture_v141/LOGIN_20260830_171132_266083_55980.txt` size `2326` SHA-256 `a2637951e952f2d28b3f8bb1d3aa0b09c8f1bab01ef83a85c8f339e7185144c1`
- `capture_gt127_20260830_170453/server_console_live.err.txt` size `1195` SHA-256 `5656630a4c14649b47235061a34ee4e2705019a4e1cd23d8deee0ffcf16c828a`
- `capture_gt127_20260830_170453/server_console_live.out.txt` size `228708` SHA-256 `6638849c02d6101b08b2b85a8537bf586a441e96c0498dece8d490d66dfa081a`
- `capture_gt141_20260830_162539/capture/gm_command_log.ndjson` size `1954` SHA-256 `61bc924aaa2fca836e2292b85d8bdd456067ec807ff433fab57322e772c81059`
- `capture_gt141_20260830_162539/capture_v141/GAME_20260830_162734_953232_49795.txt` size `49700` SHA-256 `23462bfb670e07ce2ec15c7b9de650ee36d462bbda5767abd46d9de59d5b73d2`
- `capture_gt141_20260830_162539/capture_v141/GAME_20260830_163423_168128_62376.txt` size `414100` SHA-256 `426a20820a09e2e43368f908ac94eae2e64c15b14baa39c395015e3d8a61b1e1`
- `capture_gt141_20260830_162539/capture_v141/GAME_EVENTS_LIVE.txt` size `1361` SHA-256 `4ea743f4da00a6aeaf0ab50f61e3f368ea37352b0ed1aad7f6c1c885bcaa82db`
- `capture_gt141_20260830_162539/capture_v141/GAME_LIVE.txt` size `15117` SHA-256 `8db6424414314b81dd5a2bd6c23c4f71d1c42fa253c82e41c03c6df0762e9d58`
- `capture_gt141_20260830_162539/capture_v141/LOGIN_20260830_162606_886288_55879.txt` size `2326` SHA-256 `1738803604c3179040112b21f0328900d08a9bfa728e0430a2341d67c8d38fab`
- `capture_gt141_20260830_162539/capture_v141/LOGIN_20260830_163255_500117_54406.txt` size `2326` SHA-256 `b573f17fa4049599bab8cbe3283992fa6b607646d8aeb2aca0a3b0484d997604`
- `capture_gt141_20260830_162539/server_console_live.err.txt` size `506` SHA-256 `440c87599d122d3e6634dcd253fe2a99aa8a6186380f11200a46df46602f28ef`
- `capture_gt141_20260830_162539/server_console_live.out.txt` size `221394` SHA-256 `ec1a969a19d3840360bc1d587a194b38b8e98411e83c6fcba79356e8cf8284d9`
- `capture_pexile_20260830_151429/capture_v141/GAME_20260830_151554_328319_58456.txt` size `6005872` SHA-256 `20fa3074c9ed019e227456a1e36fa68ed392c5f3d80a57414098ae640e629f1b`
- `capture_pexile_20260830_151429/capture_v141/GAME_EVENTS_LIVE.txt` size `14189` SHA-256 `818872f1100b324447fa0e8c5d00e47d7cab604b87dd980f8cc18062f81f17ca`
- `capture_pexile_20260830_151429/capture_v141/GAME_LIVE.txt` size `247711` SHA-256 `ded232875f237e154b2c1ad9b3bab152b3aeb657728bd2da347cdd102cba110c`
- `capture_pexile_20260830_151429/capture_v141/LOGIN_20260830_151546_081084_58455.txt` size `2326` SHA-256 `7b91e8ce32ee1700de509bee6e78e7f8eece4574577204a43428d1a61fd0d626`
- `capture_pexile_20260830_151429/server_console_live.err.txt` size `0` SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `capture_pexile_20260830_151429/server_console_live.out.txt` size `2467886` SHA-256 `a2544e736dc7ba6f8ab132d30d270c13acca71e6f61a4c615643dc8c17fa17bb`

## Comparator boundary

- `GameClient.local.bin` SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `ActorAttr_codec` SHA-256 `f9ea39f3a6bc80e6d29d4aae3efa79c1d5ff855d70109319578cba86d5f9aabc`
- `BasicAttr_corrected_codec` SHA-256 `d0c15b74a36077df30a0e60dbeb8441e878c08b82587c1ea55365ab2ebd70020`
- `CSkillAttr_codec` SHA-256 `9227cc6009fff2f20c79a3b19c395f9623d87f68a4ee3462e541aed62aa7e906`

Comparator/supporting files pinned before and after the scan:

- `PF_A2_ACTOR_CODEC_CORRECTION.tsv` SHA-256 `db705474aeb4e66050d67f28f14acb85b6a0a5fa9def86baadfc9f02ba07ec29`
- `PF_A2_BASIC_CODEC_CORRECTION.tsv` SHA-256 `b0313135b57ff36637158361734ed4bd1f16d59bdda84384b92b02258ee8edec`
- `PF_A2_SERIALIZER_SLOT34_DELTA.tsv` SHA-256 `1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334`
- `PF_CAPTURE_DELTA_20260830.inventory.tsv` SHA-256 `8a85dd1fff3d608ef0f0777331f9235152d2353e67adc76f4ae6275f8bfe6a3e`
- `PF_INPUT_INVENTORY.tsv` SHA-256 `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- `pf_extract_capture_branch_shapes_20260830.py` SHA-256 `423bc4aa64f800dc53da729a0e4320198dc149d9d0837debaf8e5feb46b4e498`
- `pf_validate_capture_fields.py` SHA-256 `0166337cbc8e9e561d9d3cd5f02364f4ed43c49070644d5423387e87b793d8c8`

## Proprietary-data boundary

No raw CAPTURE byte, payload value, or hexdump is emitted.  The TSV contains
only structural counts, mismatch field ordinals/reasons, relative provenance
paths, and SHA-256 identifiers.  File and block hashes are provenance, not
payload publication.

## Reproduction

Run `py -3 pf_rederive_attr_capture_validation.py --check`.  The script refuses
to scan while `LOCK_GAME.txt` is HELD, pins the image and every comparator, takes
before/after snapshots of all baseline and delta inputs, and requires
byte-identical outputs.
