# PF Monster Role DATA Controls

Status: CHECKPOINT / PROVISIONAL

Source boundary: every TSV row is `source=DATA`. No IMAGE, DUMP, CAPTURE, server, or runtime fact is merged into a row.

## Result

- Published controls: 21 DATA rows.
- Metrics fingerprint: `d032c714a5eb9401744d6df02bccde34ad7705122e84b62f1115386413855435`.
- Bounded conclusion: no exact role law was identified or validated from the audited DATA candidates alone. These DATA controls cannot decide which proxy, if any, is authoritative.
- No explicit NPCAttr or offset/width/direction schema header is present among the 71 header cells of the five pinned tables. This header-only result does not exclude schemas encoded under neutral headers or in row values.
- DATA contains lexical training labels for ID 916, but no machine-readable role enum or original attackability result.
- The exact ASCII MOBS_TIP label for id 916 is `Training Iron Man`. This corrects only the prior blocker text; it does not prove dummy behavior or attackability.
- MOBS id 917 has no current MOBS_TIP row and remains an explicit missing-side control.

## Input pins

| Input | Size | SHA256 |
|---|---:|---|
| `PF_ROOT://GameClient/Data/B_CONSTDATA_TH.pc_` | 426944 | `496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8` |
| `PF_ROOT://GameClient/Data/B_TEXTDATA_TH.pc_` | 336985 | `56b4826ed437c3f30bd1937c580ca612c22655600b5fbeb781b64c767e74c467` |
| `PF_ROOT://pf_bridge/external/.pf_attr_generations/b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae/PF_ATTR_ROLE_DISCRIMINATOR.tsv` | 42626 | `3e8d99dd9fd9c8717e27d3ec8d43e2599a6037fc366e58637aff3a5cc8d5ec73` |
| `PF_ROOT://pf_bridge/gamedata/tables/CONSTDATA_TH__AI_COMBAT.tsv` | 79483 | `19cbc17fb124b5569dbe670fd793d22f00fec72645e6027348f09a6612d04a46` |
| `PF_ROOT://pf_bridge/gamedata/tables/CONSTDATA_TH__AI_TACTIC.tsv` | 2393 | `ddcdf163795217d717b5cf25d696ed60d93b51244a8f451541d7eed555efc42a` |
| `PF_ROOT://pf_bridge/gamedata/tables/CONSTDATA_TH__AI_WANDER.tsv` | 2313 | `0b3f1eb8e67915c4be5758c734cae17c575ac2aa76cb989e13242cfb6ad01a23` |
| `PF_ROOT://pf_bridge/gamedata/tables/CONSTDATA_TH__MOBS.tsv` | 749302 | `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b` |
| `PF_ROOT://pf_bridge/gamedata/tables/TEXTDATA_TH__MOBS_TIP.tsv` | 239200 | `e25ac667c9029e07752fbfd5d13b548d2e62ea439936884f30187c0c553ce38f` |

Packed DATA is decoded only in memory. Fixed decoded totals and the five exact table-span hashes are verified before any result is rendered.

## Complete-domain safeguards

- AI_WANDER: MOBS 3210; zero references 17; nonzero references 3193; all 3193 matched; duplicate definition IDs 0; unused definitions 12. The 17 zero-reference rows are never lost to an inner join.
- AI_COMBAT: zero references 1326; nonzero references 1884; all matched; duplicate definition IDs 0; unused definitions 92.
- AI_TACTIC: zero references 1326; nonzero references 1884; all matched; duplicate definition IDs 0; unused definitions 3.
- Combat/tactic nonzero state agrees on all 3210 MOBS rows. This is a coupled count, not proof that the two IDs have the same meaning.
- MOBS and MOBS_TIP are not a total join: overlap 2931, MOBS-only 279, MOBS_TIP-only 208.

## Mixed-trait controls

- U1 has 12 rows outside the empirical R+C comparator, while 139 R+C rows are outside U1.
- U2+K+Q has 670 rows, including 12 rank-positive, 10 combat-nonzero, and 8 offensive rows.
- U7 spans seven R/C/O cells and includes rank, combat, offensive, capability, quest, chat, and voice populations.
- `s_ROLE_GRAPHIC` is populated on 257 rows: combat 27, offensive 34, capability 204, quest 200. It is not one role flag.
- The case-insensitive ASCII token `monster` appears in 15 MOBS_TIP names, but only six have current MOBS rows; the joined six span U1/U2/U7/U8.
- O/Apos is asymmetric: O0/Apos has 15 rows, O1/Apos 1645, and O1/A0 zero. Neither axis is proved attack admission.
- The id 916 coarse tuple U7/R0/C0/T0/K0/Q0/drop0/O1 matches 21 IDs; lexical identity must not be generalized from that tuple.

## Prior-reference and correction policy

Existing `PF_ATTR_ROLE_DISCRIMINATOR.tsv` claims are not copied as new evidence. Applicable rows are referenced structurally by pinned artifact path, artifact SHA256, row id, row key, and claim digest.

The id 916 correction includes `supersedes_artifact`, `supersedes_row_key`, `supersedes_claim_digest`, and `corrected_field=blocker`. Its authority precedence is field-scoped: the canonical report and authority index must cite this pair; no other prior field is superseded.

## Rows

| ID | Measurement | Status | Count |
|---|---|---|---|
| `CONSTDATA_INPUT_CHAIN` | `PACKED_DECODED_DERIVED_PIN` | `PROVEN_EXACT` | packed_files=1;decoded_spans=4;derived_tables=4 |
| `TEXTDATA_INPUT_CHAIN` | `PACKED_DECODED_DERIVED_PIN` | `PROVEN_EXACT` | packed_files=1;decoded_spans=1;derived_tables=1 |
| `AI_WANDER_LINK_INTEGRITY` | `FULL_LEFT_DOMAIN_REFERENCE_JOIN` | `PROVEN_EXACT` | population=3210;matched_nonzero=3193;missing_nonzero=0;orphan_definitions=12 |
| `AI_COMBAT_LINK_INTEGRITY` | `FULL_LEFT_DOMAIN_REFERENCE_JOIN` | `PROVEN_EXACT` | population=3210;matched_nonzero=1884;missing_nonzero=0;orphan_definitions=92 |
| `AI_TACTIC_LINK_INTEGRITY` | `FULL_LEFT_DOMAIN_REFERENCE_JOIN` | `PROVEN_EXACT` | population=3210;matched_nonzero=1884;missing_nonzero=0;orphan_definitions=3 |
| `AI_COMBAT_TACTIC_COUPLING` | `FULL_3210_BINARY_MATRIX` | `PROVEN_EXACT` | population=3210;observed_cells=3;mismatches=0 |
| `USAGE_RCO_FULL_MATRIX` | `FULL_USAGE_RCO_MATRIX` | `PROVEN_EXACT` | population=3210;usage_values=9;total_cells=72;nonzero_cells=33 |
| `USAGE_U1_COUNTEREXAMPLES` | `EXACT_FALSE_POSITIVE_AND_FALSE_NEGATIVE_IDS` | `PROVEN_EXACT` | counterexample_ids=12;missed_RC=139 |
| `USAGE_U2_KQ_MIXED_TRAITS` | `EXACT_MIXED_TRAIT_IDS` | `PROVEN_EXACT` | U2KQ=670;R=12;C=10;O=8 |
| `USAGE_U7_MIXED_TRAITS` | `COMPLETE_U7_TRAIT_COUNTS` | `PROVEN_EXACT` | population=346;RCO_observed_cells=7 |
| `MOBS_TIP_NON_TOTAL_JOIN` | `FULL_OUTER_ID_CENSUS` | `PROVEN_EXACT` | overlap=2931;left_only=279;right_only=208 |
| `NPC_CHAT_MIXED_TRAITS` | `NONEMPTY_CHAT_LEFT_JOIN_CENSUS` | `PROVEN_EXACT` | population=1844;usage_values=9 |
| `NPC_VOICE_MIXED_TRAITS` | `NONEMPTY_VOICE_CENSUS` | `PROVEN_EXACT` | population=666;usage_values=5 |
| `ROLE_GRAPHIC_MIXED_TRAITS` | `NONEMPTY_ROLE_GRAPHIC_CENSUS` | `PROVEN_EXACT` | population=257;usage_values=6 |
| `LEXICAL_MONSTER_COUNTEREXAMPLES` | `FULL_TIP_NAME_SUBSTRING_CENSUS` | `PROVEN_LEXICAL_ONLY` | TIP_hits=15;joined=6;orphan=9;joined_usage_values=4 |
| `OFFENSIVE_AGGRO_POSITIVE_MATRIX` | `FULL_3210_O_APOS_MATRIX` | `PROVEN_EXACT` | population=3210;observed_cells=3;exception_ids=15 |
| `ID916_LEXICAL_TRAINING_CORRECTION` | `EXACT_ID916_LEXICAL_JOIN` | `PROVEN_LEXICAL_ONLY` | MOBS_records=1;MOBS_TIP_records=1;AI_WANDER_records=1 |
| `ID916_COARSE_TRAIT_COHORT` | `EXACT_COARSE_TRAIT_COHORT` | `PROVEN_EXACT` | cohort=21;tip_present=11;tip_missing=10 |
| `ID917_MISSING_TIP_CONTROL` | `EXACT_ID917_LEFT_ONLY_CONTROL` | `PROVEN_EXACT` | MOBS_records=1;MOBS_TIP_records=0;AI_WANDER_records=1 |
| `NO_DATA_SIDE_NPCATTR_SCHEMA` | `EXACT_HEADER_SCHEMA_CENSUS` | `BOUNDED_NEGATIVE` | tables=5;header_cells=71;negative_hits=0 |
| `NO_VALIDATED_DATA_ROLE_LAW` | `AUDITED_ROLE_LAW_VALIDATION_STATUS` | `NOT_VALIDATED` | audited_candidate_families=7;independent_role_oracles=0;validated_exact_role_laws=0 |

## Nonclaims and next evidence

These DATA controls do not decide talk versus attack, interaction admission, damage handling, death, loot issuance, or original-server policy. Those decisions require separately sourced client consumer or runtime evidence.

Re-derive with `py -3 pf_rederive_monster_role_data_controls.py`; verify without writing with `--check`; run in-memory mutation guards with `--self-test`.
