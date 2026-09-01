# PF_MONSTER_PRESENTATION.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_MONSTER_PRESENTATION.tsv` ขนาด 4685803 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **2697** · คอลัมน์: **50**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`presentation_id` · `presentation_key` · `row_kind` · `field_key` · `lexical_class` · `mobs_id` · `mobs_name` · `outfit_ordinal` · `outfit_token` · `n_boundary` · `n_height` · `ai_wander_id` · `asset_path` · `asset_sha256` · `decoded_content_sha256` · `nif_file` · `action_count` · `active_action_index` · `active_action_file` · `active_action_class` · `claim` · `claim_sha256` · `semantic_status` · `evidence_mode` · `evidence_reuse` · `canonical_presentation_id` · `canonical_artifact` · `canonical_artifact_sha256` · `canonical_row_selector` · `canonical_row_digest` · `data_table_path` · `data_table_sha256` · `data_row_file_offset_start` · `data_row_file_offset_end` · `data_row_sha256` · `evidence_file` · `evidence_file_sha256` · `evidence_locator` · `evidence_span_start` · `evidence_span_end` · `evidence_span_start_file_offset` · `evidence_span_end_file_offset` · `evidence_span_sha256` · `support_spans` · `evidence_key` · `source` · `nonclaim` · `blocker` · `required_next_evidence` · `image_sha256`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**row_kind**

| ค่า | จำนวน |
|---|---|
| `LEXICAL_M_PREFIX_OUTFIT_REFERENCE` | 2686 |
| `CANONICAL_MOBS_RUNTIME_REFERENCE` | 4 |
| `EXPLICIT_PIKE_NON_M_TARGET` | 1 |
| `CANONICAL_AI_WANDER_REFERENCE` | 1 |
| `AVATAR_PART_NIF_PARSER` | 1 |
| `AVATAR_ACTION_KF_PIPELINE` | 1 |
| `AVATAR_ACTIONLIST_ORCHESTRATOR` | 1 |
| `SCENEFOG_ACTIVED_FALSE_LEAD` | 1 |
| `MONSTER_PRESENTATION_RUNTIME_SELECTION_OPEN` | 1 |

**lexical_class**

| ค่า | จำนวน |
|---|---|
| `LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS` | 2686 |
| `N/A` | 10 |
| `EXPLICIT_NON_M_TARGET_NOT_MONSTER_CLASS_PROOF` | 1 |

**outfit_ordinal**

| ค่า | จำนวน |
|---|---|
| `1` | 2187 |
| `2` | 499 |
| `N/A` | 10 |
| `3` | 1 |

**action_count**

| ค่า | จำนวน |
|---|---|
| `15` | 1177 |
| `16` | 413 |
| `17` | 346 |
| `5` | 137 |
| `14` | 101 |
| `21` | 99 |
| `11` | 86 |
| `10` | 83 |
| `6` | 56 |
| `18` | 54 |
| `13` | 45 |
| `12` | 38 |
| `19` | 26 |
| `N/A` | 10 |

**active_action_index**

| ค่า | จำนวน |
|---|---|
| `12_ZERO_BASED` | 1097 |
| `13_ZERO_BASED` | 333 |
| `11_ZERO_BASED` | 295 |
| `14_ZERO_BASED` | 205 |
| `2_ZERO_BASED` | 167 |
| `8_ZERO_BASED` | 86 |
| `16_ZERO_BASED` | 84 |
| `9_ZERO_BASED` | 71 |
| `3_ZERO_BASED` | 69 |
| `15_ZERO_BASED` | 54 |
| `17_ZERO_BASED` | 52 |
| `7_ZERO_BASED` | 52 |
| `10_ZERO_BASED` | 49 |
| `4_ZERO_BASED` | 23 |

**active_action_class**

| ค่า | จำนวน |
|---|---|
| `READY` | 2167 |
| `SENTRY` | 286 |
| `ATTACK` | 74 |
| `WALK` | 55 |
| `TALK` | 43 |
| `HAPPY` | 23 |
| `NO_ACTIVE` | 18 |
| `DIE` | 13 |
| `N/A` | 10 |
| `FORWARD` | 8 |

## ตัวอย่าง 4 แถวแรก

```
MP-DATA-0001 | 9c5ad60d7c561db58b5f0b11f894ed6dadad41e2e50ab3544c01fc81c4d7 | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_2_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 2 | 賽巴斯汀 | 1 | M010_001_000_N | 180
MP-DATA-0002 | c1acf060fb9820ba73ebe4df45842c2fc2158bd2a83b413206cc8c91bc4f | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_4_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 4 | 魔玉子 | 1 | M015_000_000_SP1 | 100
MP-DATA-0003 | fcfd71a0fe7c6b7b7d1669902a0ca59206e7421a983ee8816181d986a2ea | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_6_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 6 | 史杰客 | 1 | M001_000_000_SP3 | 170
MP-DATA-0004 | cb863349d285c0ab18b1a66d07e80c0ecbbfae3df2d37dee2e06a854568e | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_7_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 7 | 史杰客的手下 | 1 | M001_000_000_SP1 | 130
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
