# CODEX CHECKPOINT — P0-7 PRESENTATION CHECKPOINT_2

checkpoint_at: 2026-09-02 01:26 +07:00  
status: CHECKPOINT / PROVISIONAL  
decision: P0-7_PARTIAL_CHECKPOINT_2 / EVIDENCE_COVERAGE_DELTA / PAUSED_BY_OWNER_AFTER_CHECKPOINT

## Result

- Main generation: `4b02f45a71046e1b13761f4d9e10472d6c653a4f10f2a328f87bf47080ad97ae`.
- `PF_MONSTER_PRESENTATION.tsv`: 8,950 rows = DATA 8,940 / IMAGE 10.
- CHECKPOINT_1 rows preserved: 2,697/2,697 with zero mismatch across all 50 old columns.
- Added coverage: 6,248 authored placement groups, four CLINE map-list ambiguity guards, one manager-sensitive `f_SCALE` row.
- Semantic status closures: **0**. Main field semantic UNKNOWN remains 42/490; field scope UNKNOWN remains 210; unified unresolved remains 977.
- P0-7 remains `PARTIAL / CHECKPOINT_2`.

## Evidence boundaries and open claims

- Authored placement groups are file-authored records, not live actor/spawn density.
- Extra triples are not actor/spawn counts. Per-file template tokens are not generally MOBS IDs.
- CLINE guards are map-list projections only, not runtime actor identity. Ordinary placement rows use `NOT_APPLIED_MAP_LIST_CONTEXT`.
- `f_SCALE` is still role-only/open for typed effect, unit and zero policy. The bounded initializer did not read MOBS+0x0C; this is not a whole-program absence claim.
- `s_OUTFIT +0x108 -> Avatar` active outfit/action/idle selection remains UNKNOWN. DIE is not sleep.
- `pf_decode_lua_npc.py` is not yet pinned as the permanent decoder authority; raw `.npc` and derived placement inputs are individually pinned. This is a provenance blocker, not a semantic closure.

## Integrity and comparator

- Final generator SHA-256: `c7d6c560f0848b3eb0edc34bb147a66d5c3fc1661ed0d88fb9c4065ca0a7528c`, size 1,530,912 B.
- Manifest SHA-256: `8ffa1ec8b5ce8fe9dc774cbc3b01997a7ff3ee516120d536bee5875898b338da`, size 8,204 B.
- Presentation TSV SHA-256: `658ae9352da2e45c1cd5306851dd7bbe8271dabe5cef3728ce223df31193722c`, size 20,875,512 B.
- Presentation MD SHA-256: `2a2a6990bb28cdff5c3a2c1791852f992ec020db15c70f9ab6f929c42a8be282`, size 16,783 B.
- Full publication ran twice from the same frozen source and produced the same generation. Manifest/internal manifest, snapshot, reader, hashes, sizes and 48 top-level compatibility mirrors passed; mirror warnings 0; stage debris 0.
- `--check`, `--self-test` and junk arguments now fail before snapshot/stage/manifest/mirror mutation. This generator has one authoritative mode: complete staged re-derivation.
- The old `d5eeb931...` context-leak counterexample is rejected by the final validator.
- Presentation V2: `c942fd4ef6d6347b13977a6d503d9fb8886497a13bfd4f6095628068aa8452e7`.
- V3 subject-set: `9e05ee4153eb9ccb703a467e879fa3b51264b93dda812862942d5f5a7e0b4a37`.
- V3 subject+status: `17d691d8de7b6f096f8cabd22a9a6355802e1be2f3726de620821202126c3222`.
- Evidence/coverage changed and V3 is a new baseline, therefore `no_change_streak=0`.
- Input IMAGE remained 14,759,424 B, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, with pinned mtime unchanged.

## GT-192 level correction

The prior diagnosis that ordinary census actors carried level and the client partially decoded the record is withdrawn. The ordinary frozen builder sends name, HP, speed, scene and sequence but omits BasicAttr level bit `0x0002`/u16. HP was present; therefore LV 1 does not prove partial decode. RE-117 separately proves the inherited NPCAttr level field at bit `0x0002`, object `+0x5E`, u16 tag `0x12`. See `CODEX_URGENT_20260901_2340_LEVEL-OMITTED-NOT-PARTIAL-DECODE.md`. Monster color and NPC-like nameplate remain separate open presentation problems.

## Delivery pins

- Canonical cumulative report: `Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md`, 188,872 B, SHA-256 `98e3c59ae85bef72c0e9fe7dab2f612b712d7f93f04b7708ee80a21228200a97`.
- Permanent pre-overwrite snapshot: `audit_history/Pirate_Force_Codex_Audit_Recommendations.4b02f45a7104_20260902_0126.byka1B.md`, 186,075 B, SHA-256 `79526d748fb7c0ee894a87c7ff0df0f2bfbfac0a40105575059989c354f00119`.
- Machine authority: `PF_CRITICAL_ARTIFACT_AUTHORITY.json`, 33,430 B, SHA-256 `4faae5f0dc3bc86b4e71ef5069dda43c3ea86cec2ea3fa3c156307f22fd24fbf`.
- P0-7 CHECKPOINT_2 has no complete tracked mirror/commit. Consume it through the external generation manifest on this machine; do not claim clone delivery.

## Pause and next ordered lane

Owner instruction is to stop after this checkpoint. Codex has not started P0-8 or P1. By simple P0 heading count, 7 of 8 P0 topics have reached their current checkpoint/decision (about 87%); the whole GOAL_MASTER including broad, unstarted P1 is only a workload estimate of about 55–65%, not a measured completion ratio. When the owner explicitly resumes, P0-8 is next.
