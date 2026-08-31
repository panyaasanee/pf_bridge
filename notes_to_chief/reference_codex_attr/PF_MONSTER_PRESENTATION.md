# PF monster presentation - source-separated P0-7 checkpoint

[MEASURED][LOCAL TOOLING] P0-7 status: **PARTIAL / CHECKPOINT_1**. This is the first P0-7 checkpoint. It publishes 2,697 deterministic rows (2,688 DATA; 9 IMAGE) and added three exact runtime rows: n_BOUNDARY +0x04, n_HEIGHT +0x08, and s_OUTFIT +0x108. At least one further P0-7 checkpoint is required before the two-consecutive-no-status-change stop rule can be evaluated.

[MEASURED][LOCAL TOOLING] Method/control: derive descriptor names only from the already guarded MOBS s_OUTFIT corpus; acquire read/share-read handles for all 615 lexical M descriptors plus Pike before parsing; verify packed and decoded hashes; decode XML only in memory; restrict IMAGE claims to exact pinned spans. No client, server, dump, capture, or runtime execution was used.

- [MEASURED][IMAGE] Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- [MEASURED][DATA] Lexical M### outfit references: 2,686 across 2,186 MOBS rows; 615 distinct descriptors. A lexical `M###` prefix is a corpus-selection rule, not proof of a concrete monster class.
- [MEASURED][DATA] Explicit non-M target: Pike MOBS ID 5 (`P_MALE_002_000_PAK`).
- [MEASURED][LOCAL TOOLING] Guarded descriptors: 616 total. `lexical_M_token_keyset_sha256=5418f7cbcba3105faf62d093eab8b0a5777b7f640bba00860c81cf6ec6a68be7` covers only the 615 lexical M descriptors; Pike is the additional guarded descriptor.
- [MEASURED][DATA] Weighted active classes: READY 2167, SENTRY 286, ATTACK 74, WALK 55, TALK 43, HAPPY 23, NO_ACTIVE 17, DIE 13, FORWARD 8.
- [MEASURED][DATA] Distinct-asset active classes: READY 489, SENTRY 77, ATTACK 14, WALK 14, TALK 4, HAPPY 4, NO_ACTIVE 5, DIE 2, FORWARD 6.
- [MEASURED][DATA] n_BOUNDARY: 3210 numeric rows, 33 distinct, min 1, max 1600.
- [MEASURED][DATA] n_HEIGHT: 3210 numeric rows, 71 distinct, min 1, max 2600.

## Exact targets

- [MEASURED][DATA] Pike ID 5 stores outfit `P_MALE_002_000_PAK`, boundary/height `75/75`, and AI_WANDER `2`; the shipped six-part composite descriptor has NifFile inventory `.\Data\GC\M\MAN_SKINBONE.nif;.\Data\GC\M\VM_CT_002.nif;.\Data\GC\M\DM_HD_000.nif;.\Data\GC\M\DM_HR_002.nif;.\Data\GC\M\VM_HT_002.nif;.\Data\GC\M\VM_LG_002.nif`, 0 Action entries, and no active action.
- [MEASURED][LOCAL TOOLING] The configured Pike comparison token matches original DATA; runtime selection and rendered equivalence are unproved.
- [MEASURED][DATA] Mountain Deer ID 27 lists `M005_000_000_SP1;M005_000_000_SP2`, boundary/height `110/160`, and AI_WANDER `16`. Both descriptors have 17 actions and the same active class/file metadata `SENTRY` / `.\Data\GC\A\M005_F_SENTRY_000.kf`; this metadata does not prove runtime selection or visual equivalence.

## Counterexamples

- [MEASURED][DATA] MOBS ID 30 pairs `M011_000_000_SP1` (READY) with `M011_000_000_SP2` (DIE).
- [MEASURED][DATA] MOBS ID 1365 pairs `M011_001_000_SP2` (SENTRY) with `M011_001_000_SP3` (DIE).
- [PROPOSED SAFETY RULE] Treat these only as DATA counterexamples; never rename `DIE` as sleep or idle.

## IMAGE boundary and open work

- [MEASURED][IMAGE] Exact named loads establish n_BOUNDARY +0x04, n_HEIGHT +0x08, and s_OUTFIT tokenization into +0x108; separate pinned spans establish the Avatar NifFile/KfFile/ActionList parser surfaces.
- [MEASURED][IMAGE] The f_SCALE key, 0.0 constructor default, and load into runtime +0x0C are exact. No typed effect consumer is currently proved within the recorded bounded review. Separate typed-census/alias-review digests are not incorporated or rederived by this generator, so neither census completeness nor global absence is claimed; 0.0 is not classified as a no-op.
- [MEASURED][IMAGE] The proposed `Actived` candidate at `0x009F939B -> 0x009F9040(1)` is refuted for Avatar use: it is the SceneFogCmp property family.
- [MEASURED][IMAGE] The exact Avatar action parser reads `KfFile` and `GetAllowActionPlus`; it does not read `Action/@Actived` on the bounded path.
- [MEASURED][IMAGE] After two bounded alias rounds, no type-preserving +0x108 token-vector to Avatar filename/parser/active-selection bridge is proved. `MONSTER_PRESENTATION@ACTIVE_SELECTION#N` remains one explicit active unresolved item; this bounded result does not satisfy the master two-checkpoint stop rule.
- [MEASURED][IMAGE] Exact ASCII/UTF-16 `IDLE` and `s_WANDER` literal checks find no direct named IMAGE action/task consumer. This does not exclude unnamed, indexed, virtual, offset-based, or runtime-only consumers.

## Nonclaims

[PROPOSED SAFETY RULE] Do not infer original-server selection from token order, call the first outfit a default, assign collision/physics semantics to n_BOUNDARY/n_HEIGHT, treat f_SCALE zero as a no-op, or use Action/@Actived as server policy without a new type-preserving proof.

[MEASURED][LOCAL TOOLING] The +1 unresolved row is coverage expansion, not regression: the earlier ledger did not represent this presentation-selection boundary. This remains CHECKPOINT_1; at least one further P0-7 checkpoint is required before the two-consecutive-no-status-change stop rule can be evaluated.
