# PF_A2_SERIALIZER_SLOT34_DELTA.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_A2_SERIALIZER_SLOT34_DELTA.tsv` ขนาด 5335314 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **2308** · คอลัมน์: **23**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`delta_key` · `action` · `base_file` · `base_line` · `base_row_key` · `message` · `schema_variant` · `direction(W/R)` · `old_order` · `old_tag` · `old_field_offset` · `old_len` · `new_order` · `new_tag` · `new_field_offset` · `new_len` · `new_gate_condition` · `new_span_start` · `new_span_end` · `new_span_sha256` · `new_file_off_claim` · `resolution` · `source`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**action**

| ค่า | จำนวน |
|---|---|
| `ADD_CORRECTED_SLOT34_ROW` | 2059 |
| `REMOVE_WRONG_SLOT_ROW` | 114 |
| `ADD_ANALYSIS_BLOCKER_ROW` | 79 |
| `ADD_AMBIGUOUS_CANDIDATE_ROW` | 56 |

**base_file**

| ค่า | จำนวน |
|---|---|
| `N/A` | 2194 |
| `PF_SERIALIZER_FIELDS.tsv` | 114 |

**schema_variant**

| ค่า | จำนวน |
|---|---|
| `SINGLETON_SLOT34` | 2138 |
| `V1_SLOT18` | 114 |
| `VTABLE_0x00F4A188` | 30 |
| `VTABLE_0x00F0EBB0` | 26 |

**direction(W/R)**

| ค่า | จำนวน |
|---|---|
| `W` | 1162 |
| `R` | 1146 |

**old_order**

| ค่า | จำนวน |
|---|---|
| `N/A` | 2194 |
| `1` | 114 |

**old_tag**

| ค่า | จำนวน |
|---|---|
| `N/A` | 2194 |
| `EMPTY` | 96 |
| `CALL_UNCLASSIFIED:0x0046D7A0` | 18 |

## ตัวอย่าง 4 แถวแรก

```
c57f0e988fa41a6c48e49589476a1e1a4e1171e582d2941e22416b7b2c37 | REMOVE_WRONG_SLOT_ROW | PF_SERIALIZER_FIELDS.tsv | 4 | 6be0e1b9910642fc5245f7eac20a0b96996cf83095c579eccacea8675bb6 | AvatarAttr | V1_SLOT18 | R | 1 | EMPTY
a37a094d9f2cd68669e54dbf7c34cfc14f310060996e22b06269d490231e | REMOVE_WRONG_SLOT_ROW | PF_SERIALIZER_FIELDS.tsv | 5 | 27f61453900765693f27498bfce70fbe58983f2408e1e450d1d67fa8facb | AvatarAttr | V1_SLOT18 | W | 1 | EMPTY
e8d9619cf5ba2d3494f93cddb7143e5bb111c37fab3342fbcfbdfb20c3b4 | REMOVE_WRONG_SLOT_ROW | PF_SERIALIZER_FIELDS.tsv | 6 | d719ee4ecc800a7884e88d80b71a4392c1f8b08ee923e95830b21aaf0b23 | BasicAttr | V1_SLOT18 | R | 1 | EMPTY
bf67bd7ab793a77f35d16f86536c8f3857cc785e91cfc598b2f8586bb022 | REMOVE_WRONG_SLOT_ROW | PF_SERIALIZER_FIELDS.tsv | 7 | 46e37062a10ec99b8656fc49471184fa535aed93bad7e6043f71d2fcaa0b | BasicAttr | V1_SLOT18 | W | 1 | EMPTY
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
