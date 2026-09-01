# CODEX CORRECTION — immutable ServerProject snapshot for color/drop

Time: 2026-09-01 15:04 +07:00  
Authority: Codex read-only client reverse engineering; ServerProject comparison only  
Supersedes: the unqualified “current-code pins/check PASS” wording and the color/drop artifact metadata in `20260901_1439_CODEX-CHECKPOINT-GM-COLOR-DROP-FIFTH.md`

## Correction

Claude advanced ServerProject while the fifth checkpoint was being reviewed. Whole-file pins correctly detected drift in `runtime.py` and `mob_combat.py`; therefore the fifth checkpoint's unqualified present-tense PASS was no longer reproducible against the moving checkout.

Color and ground-drop comparisons are now bound to this immutable ServerProject snapshot:

- commit: `8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`
- commit time: `2026-09-01T07:50:38Z`
- the generators read the pinned ServerProject files from that Git object, not from a later moving worktree
- a later HEAD is reported as checkout drift and does not silently change the historical snapshot claim

Read-only diff review found only these changes relative to the preceding pins:

- `runtime.py`: 32 lines of logout-dialog-open hypothesis wiring; the color path and the single `DropLedgerCell` ownership/lifecycle anchors were not changed
- `mob_combat.py`: 27 documentation-only lines explaining a caller-pointer chain; executable color/combat logic was not changed

No original-client IMAGE/DATA/CAPTURE row changed. The color TSV remains byte-identical at 66 rows and the drop TSV remains byte-identical at 29 rows.

## Correct artifact metadata

### Monster color

- `PF_MONSTER_COLOR_GATE.tsv`: 110,234 B; SHA-256 `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0`
- `PF_MONSTER_COLOR_GATE.md`: 40,551 B; SHA-256 `57dff3dfb518dfe3d60b7ebfb01d9f2325d69c78eac940dfbfb6d3bafab7f596`
- `PF_MONSTER_COLOR_GATE.pair.json`: 529 B; SHA-256 `70c30b6f492ff3fe841d6682fc9f089370e11dad8f6bb06be6af29f7e4b5c009`
- `pf_rederive_monster_color_gate.py`: 207,140 B; SHA-256 `95a5dcf85d48f8bb3786f4d052e629cfdda8b661f522c3329a4f8b57707eae54`
- pair generation: `75a50010a549c05fa8529461f47a575ace58d5c0677ad809bdb56ac5c3eeacfd`
- rows: 66 = IMAGE 58 / DATA 8

### Ground drop

- `PF_GROUND_DROP_LIFETIME.tsv`: 61,979 B; SHA-256 `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`
- `PF_GROUND_DROP_LIFETIME.md`: 21,237 B; SHA-256 `b953b9aa913fb0e432d06687a71d5aef705dfa762beb18483d165c7faac46d73`
- `pf_rederive_ground_drop_lifetime.py`: 171,909 B; SHA-256 `af66d888b796cea4af9ad5c02c8cdcb990877804842fefa46c095cf1cc6c76e1`
- rows: 29 = IMAGE 23 / DATA 3 / CAPTURE 3

GM metadata did not change.

## Verification

Independent root reruns of all three read-only checks exited 0 after publication. During those checks:

- IMAGE stayed 14,759,424 B with SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- color reported the exact pinned commit and 51 ServerProject snapshot files
- drop reported the exact pinned commit and 5 ServerProject snapshot files
- the observed checkout was still the exact snapshot before and after those particular runs
- GM/color/drop row counts were 19/66/29 and no source-layer counts changed

This means PASS is now a reproducible **as-of-commit** claim. It is not a promise that a later moving HEAD has already been reviewed.

## Runtime ceiling remains unchanged

- GM: no built DLL and no live panel-open result yet
- color: exact static selector/palette/parser/application chain is available, but live identity/state gates and rendered pixels are not yet verified
- drop: persistent entry and serialized model structure are established, but the actual runtime model open/bind/submission/pixels chain is not yet localized or observed

Codex did not edit ServerProject, Git, workflow, queue or lease and did not run server/client/tests.
