# CODEX AUTHORITY CORRECTION — current critical artifacts

Time: 2026-09-01 15:19 +07:00  
Authority index: `pf_bridge/external/PF_CRITICAL_ARTIFACT_AUTHORITY.json`

This append-only note is the current metadata/supersession authority for the GM, monster-color and ground-drop artifacts. It exists so a reader does not have to infer authority from filenames or timestamps.

## Explicit supersession

- `20260901_1439_CODEX-CHECKPOINT-GM-COLOR-DROP-FIFTH.md`: its unqualified current-code PASS wording and color/drop metadata are superseded.
- `20260901_1439_CODEX-RE191-RESULT-FONTSTYLE63-RGBA.md`: only its color artifact metadata is superseded; the source-separated RE-191 evidence conclusions remain retained.
- `20260901_1440_CODEX-CORRECTION-GT188-ARTIFACT-HASHES.md`: only its color/drop artifact metadata is superseded; the GT-188 label-only false-green warning remains retained.
- `20260901_1504_CODEX-CORRECTION-IMMUTABLE-SERVERPROJECT-SNAPSHOT.md`: its immutable-snapshot design, artifact metadata and runtime ceilings remain retained; only the phrase “51 ServerProject snapshot files” is corrected below.

## Count correction

For the monster-color comparison at ServerProject commit `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`:

- 51 = explicitly pinned project-source anchors
- 157 = files in the exhaustive Foundation Python census

The two counts describe different sets and must not be interchanged.

## Current hashes

The machine-readable authority index contains every current file size, SHA-256, row count and source count. Its current summary is:

- GM: 19 rows = IMAGE 17 / DATA 2
- monster color: 66 rows = IMAGE 58 / DATA 8
- ground drop: 29 rows = IMAGE 23 / DATA 3 / CAPTURE 3
- color/drop replacement comparison: immutable ServerProject commit `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`, commit time `2026-09-01T07:50:38Z`

## Delivery wording correction

`pf_bridge/external` is local-only and **outside the canonical ServerProject Git worktree**. It is not accurate to call these files Git-ignored. They are not tracked and cannot be delivered to another clone by changing `.gitignore` or using `git add -f`; owner-approved packaging/ingest into the repository is required.

## Runtime ceiling

This correction changes document authority and reproducibility only. It does not claim a built GM DLL, a live GM panel, rendered monster pixels, or a rendered/persistent ground-drop model.
