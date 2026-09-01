# PF_ATTR_UNRESOLVED.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_ATTR_UNRESOLVED.tsv` ขนาด 2355364 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **977** · คอลัมน์: **20**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`unresolved_key` · `field_key` · `wire_key` · `class` · `applies_to_class` · `scope_status` · `parent_chain` · `direction` · `offset` · `semantic_name` · `semantic_status` · `structural_status` · `unresolved_kind` · `conflict_keys` · `scoped_search_result` · `blocker` · `required_next_evidence` · `evidence_key` · `source` · `image_sha256`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**scope_status**

| ค่า | จำนวน |
|---|---|
| `N/A` | 512 |
| `UNKNOWN` | 243 |
| `PROVEN_EXACT` | 222 |

**direction**

| ค่า | จำนวน |
|---|---|
| `N` | 538 |
| `R` | 195 |
| `W` | 195 |
| `W/R` | 49 |

**semantic_status**

| ค่า | จำนวน |
|---|---|
| `N/A` | 512 |
| `PROVEN_ROLE_ONLY` | 217 |
| `PROVEN_EXACT` | 135 |
| `UNKNOWN` | 83 |
| `PARTIAL` | 29 |
| `NOT_WIRE` | 1 |

**structural_status**

| ค่า | จำนวน |
|---|---|
| `N/A` | 512 |
| `PROVEN_EXACT` | 432 |
| `PARTIAL` | 18 |
| `UNKNOWN` | 14 |
| `NOT_WIRE` | 1 |

**unresolved_kind**

| ค่า | จำนวน |
|---|---|
| `OPEN_CONFLICT_WORK_ITEM` | 512 |
| `ROLE_PROVED_BROADER_IDENTITY_OPEN` | 128 |
| `CONCRETE_CONSUMER_CLASS_UNKNOWN` | 114 |
| `CONCRETE_CONSUMER_AND_SEMANTIC_OPEN` | 96 |
| `CONCRETE_CONTAINER_RECORD_CLASS_AND_SEMANTIC_OPE` | 20 |
| `FIELD_GAMEPLAY_SEMANTIC_UNKNOWN` | 20 |
| `OPEN_NEEDS_MEASURED_NONWIRE_CORRECTION` | 17 |
| `OPEN_REDERIVED_IMAGE_CONFLICT` | 16 |
| `GAMEPLAY_SEMANTIC_UNKNOWN` | 15 |
| `CLASS_LINK_RECOVERY_OPEN` | 10 |
| `COMBAT_LIFECYCLE_SEMANTIC_OR_ORDER_OPEN` | 8 |
| `CONTAINER_GAMEPLAY_SEMANTIC_OPEN` | 8 |
| `NON_WIRE_RUNTIME_ROLE_OPEN` | 7 |
| `CONCRETE_CONTAINER_RECORD_CLASS_UNKNOWN` | 3 |

**scoped_search_result**

| ค่า | จำนวน |
|---|---|
| `(ว่าง)` | 962 |
| `no provenance-backed non-core semantic consumer ` | 6 |
| `The six mapped normal-attack BEHAVIOR rows all h` | 1 |
| `No direct repeat edge is present in the concrete` | 1 |
| `Bit 0 gates the CHitResult apply/display block.` | 1 |
| `Bit 3 is required on the known target-reaction l` | 1 |
| `Bit 4 selects the alternate knocked/exclusion pa` | 1 |
| `BasicAttr name +0x28 and current/max HP +0x44/+0` | 1 |
| `The relative order of CHitResult and the HP-bear` | 1 |
| `A valid behavior ID in ActionVital +0x30 is the ` | 1 |
| `After two bounded alias rounds, no type-preservi` | 1 |

## ตัวอย่าง 4 แถวแรก

```
930d9ea565f24483861ae3d7f3274147e2e7bf569e4f83f5c8126bc45d44 | ActorAttr@0x104.var#R:b0x00000010 | ActorAttr@0x104.var#R:b0x00000010 | ActorAttr | UNKNOWN_CONCRETE_OWNER_OF_ActorAttr | UNKNOWN | PcRefObject>Attribute>DBAttribute>BasicAttr>ActorAttr | R | 0x104 | age_text
89377de75d57b9731ea4425c45f253f886d4809c404f7d77474208e80a6b | ActorAttr@0x104.var#W:b0x00000010 | ActorAttr@0x104.var#W:b0x00000010 | ActorAttr | UNKNOWN_CONCRETE_OWNER_OF_ActorAttr | UNKNOWN | PcRefObject>Attribute>DBAttribute>BasicAttr>ActorAttr | W | 0x104 | age_text
28fc7b5475557e1c4a1e036ac1d4527baa3335f59bd7524cecc6aebc018b | ActorAttr@0x120.var#R:b0x00000020 | ActorAttr@0x120.var#R:b0x00000020 | ActorAttr | UNKNOWN_CONCRETE_OWNER_OF_ActorAttr | UNKNOWN | PcRefObject>Attribute>DBAttribute>BasicAttr>ActorAttr | R | 0x120 | constellation_text
f9a63e2946a8c6de6ec084e62340e55c8fe8b4584afdefcd61d7e1497fbc | ActorAttr@0x120.var#W:b0x00000020 | ActorAttr@0x120.var#W:b0x00000020 | ActorAttr | UNKNOWN_CONCRETE_OWNER_OF_ActorAttr | UNKNOWN | PcRefObject>Attribute>DBAttribute>BasicAttr>ActorAttr | W | 0x120 | constellation_text
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
