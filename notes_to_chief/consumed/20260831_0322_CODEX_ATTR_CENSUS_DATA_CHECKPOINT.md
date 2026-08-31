# CODEX ATTR CENSUS/DATA CHECKPOINT - 2026-08-31 03:22 +07:00

Read-only static Attr re-derivation advanced without running or modifying the client, server, tests, captures, dumps, Git, or lease.

- Pinned IMAGE SHA-256 remains `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` before and after the deterministic run.
- `PF_ATTR_REMAINING_CODEC_CENSUS.tsv` now classifies all 124 registry classes remaining after the 11 detailed classes: 36 paired codecs, 51 empty/no-payload routines, 27 concrete non-codec routines, and 10 getter/vtable recovery cases.
- Three independently re-derived aggregate hashes are enforced: registry24 `1fa0dd2b4bd5443f99c40fb06cb4ab51a1f3bb54c8d810b27f687e4174e2fb72`, vtable38 `507645c80669bb1d7afed736a154916e0c7b90c6cc4ae348dee5feb2ab870306`, getter `1c5343299ad4dc0a9fc78a7415637eca663caab8d3ab94eb89b5aa8d165a1542`.
- `PF_ATTR_DATA_BINDINGS.tsv` adds 24 source-separated DATA rows. No DATA fact is merged into an IMAGE row.
- `PF_ATTR_UNRESOLVED.tsv` now contains 181 explicit open rows: 170 directional field rows, one non-wire runtime attachment row, and ten CBuff container/record concepts.
- The active semantic report now includes MovementAttr, AvatarAttr, NPCAttr, FightAttr, CBuffAttr, source-separated DATA, and the unresolved IMAGE/DATA f_SCALE mismatch.

Artifact SHA-256:

- script: `fdf646e71d7bdc1cdc02e8b4b0cc4b1080f9ca0ea7274efecffe7c7688824b39`
- remaining census: `a075a11a7f4c62178b0bf6a3bf7da0fbb03e191b77101085373c59c62d5c2f1f`
- DATA bindings: `9d2bd9f28fcfc8f1eed99a30042d6e328e22897d35bbba96a3aa159c2bb608df`
- unresolved queue: `7399f13c6bd22b2f4cc358d32fd7bc1fff95b47ae6a20821950a2107bed6fc65`
- semantic report: `b55cec7a7263bb53965e50b5bddf6bed4dcb130e2e87c5ed5ec6f8c801be6edd`

Work remains active. Object/world codec decoding and the remaining pet/activity/community/party/guild families are still in progress. Frozen A1-A6 artifacts were not edited.
