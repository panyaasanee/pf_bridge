# PF_MONSTER_PRESENTATION.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_MONSTER_PRESENTATION.tsv` ขนาด 20875512 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **8950** · คอลัมน์: **70**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`presentation_id` · `subject_id` · `presentation_key` · `row_kind` · `field_key` · `lexical_class` · `mobs_id` · `mobs_name` · `outfit_ordinal` · `outfit_token` · `n_boundary` · `n_height` · `ai_wander_id` · `asset_path` · `asset_sha256` · `decoded_content_sha256` · `nif_file` · `action_count` · `active_action_index` · `active_action_file` · `active_action_class` · `scene` · `scene_index_ordinal` · `placement_index` · `placement_name` · `placement_name_class` · `placement_x` · `placement_y` · `placement_z` · `placement_set_names` · `placement_template_ids` · `authored_group_count` · `extra_triple_count` · `scene_name_row_ids` · `cline_type` · `cline_projection` · `cline_candidate_mobs_ids` · `cline_count_fields` · `candidate_outfit_vectors` · `composition_join_status` · `claim` · `claim_sha256` · `semantic_status` · `evidence_mode` · `evidence_reuse` · `canonical_presentation_id` · `canonical_artifact` · `canonical_artifact_sha256` · `canonical_row_selector` · `canonical_row_digest` · `data_table_path` · `data_table_sha256` · `data_row_file_offset_start` · `data_row_file_offset_end` · `data_row_sha256` · `evidence_file` · `evidence_file_sha256` · `evidence_locator` · `evidence_span_start` · `evidence_span_end` · `evidence_span_start_file_offset` · `evidence_span_end_file_offset` · `evidence_span_sha256` · `support_spans` · `evidence_key` · `source` · `nonclaim` · `blocker` · `required_next_evidence` · `image_sha256`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**row_kind**

| ค่า | จำนวน |
|---|---|
| `AUTHORED_PLACEMENT_GROUP` | 6248 |
| `LEXICAL_M_PREFIX_OUTFIT_REFERENCE` | 2686 |
| `CANONICAL_MOBS_RUNTIME_REFERENCE` | 4 |
| `CLINE_MAP_LIST_PROJECTION_GUARD` | 4 |
| `EXPLICIT_PIKE_NON_M_TARGET` | 1 |
| `CANONICAL_AI_WANDER_REFERENCE` | 1 |
| `AVATAR_PART_NIF_PARSER` | 1 |
| `AVATAR_ACTION_KF_PIPELINE` | 1 |
| `AVATAR_ACTIONLIST_ORCHESTRATOR` | 1 |
| `SCENEFOG_ACTIVED_FALSE_LEAD` | 1 |
| `MONSTER_PRESENTATION_RUNTIME_SELECTION_OPEN` | 1 |
| `SCALE_MANAGER_IDENTITY_CENSUS` | 1 |

**lexical_class**

| ค่า | จำนวน |
|---|---|
| `LEXICAL_MOB_OR_MONSTER_NAME_OR_SET_NOT_CLASS_PRO` | 6230 |
| `LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS` | 2686 |
| `NONLEXICAL_NAME_AND_SET` | 18 |
| `N/A` | 11 |
| `DATA_NAMESPACE_AMBIGUITY_NOT_ACTOR_IDENTITY` | 4 |
| `EXPLICIT_NON_M_TARGET_NOT_MONSTER_CLASS_PROOF` | 1 |

**outfit_ordinal**

| ค่า | จำนวน |
|---|---|
| `N/A` | 6263 |
| `1` | 2187 |
| `2` | 499 |
| `3` | 1 |

**action_count**

| ค่า | จำนวน |
|---|---|
| `N/A` | 6263 |
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

**active_action_index**

| ค่า | จำนวน |
|---|---|
| `N/A` | 6263 |
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

**active_action_class**

| ค่า | จำนวน |
|---|---|
| `N/A` | 6263 |
| `READY` | 2167 |
| `SENTRY` | 286 |
| `ATTACK` | 74 |
| `WALK` | 55 |
| `TALK` | 43 |
| `HAPPY` | 23 |
| `NO_ACTIVE` | 18 |
| `DIE` | 13 |
| `FORWARD` | 8 |

## ตัวอย่าง 4 แถวแรก

```
MP-DATA-0001 | 0186168bfc18d806e56dccd909f125f1ce8cc33f054cd02c35b4e69416f2 | 9c5ad60d7c561db58b5f0b11f894ed6dadad41e2e50ab3544c01fc81c4d7 | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_2_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 2 | 賽巴斯汀 | 1 | M010_001_000_N
MP-DATA-0002 | d0b9f73f5877baca2ec7789b5e00f170893ccdf80fb9660855b08827df8e | c1acf060fb9820ba73ebe4df45842c2fc2158bd2a83b413206cc8c91bc4f | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_4_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 4 | 魔玉子 | 1 | M015_000_000_SP1
MP-DATA-0003 | 96e3a9b7451e29163427e70b4e3f9c34167b5ef6e722dcecfd925bb43bbe | fcfd71a0fe7c6b7b7d1669902a0ca59206e7421a983ee8816181d986a2ea | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_6_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 6 | 史杰客 | 1 | M001_000_000_SP3
MP-DATA-0004 | ac88d8ffa01e013b93d3ee9d9481202e918289964f7d1dc9eb32dfb4e551 | cb863349d285c0ab18b1a66d07e80c0ecbbfae3df2d37dee2e06a854568e | LEXICAL_M_PREFIX_OUTFIT_REFERENCE | MONSTER_PRESENTATION@MOBS_ID_7_OUTFIT_1#N | LEXICAL_M_PREFIX_NOT_PROVEN_MONSTER_CLASS | 7 | 史杰客的手下 | 1 | M001_000_000_SP1
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
