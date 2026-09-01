# PF_RUNTIME_CLASSMAP.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_RUNTIME_CLASSMAP.tsv` ขนาด 1947472 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **6244** · คอลัมน์: **15**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`record_kind` · `vtable_va` · `class_name` · `type_descriptor_name` · `instance_count` · `type_descriptor_va` · `type_descriptor_count` · `type_info_vtable_va` · `object_offset` · `dump_name` · `dump_sha256` · `dump_file_offset` · `instance_file_offsets` · `rtti_status` · `source`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**record_kind**

| ค่า | จำนวน |
|---|---|
| `TYPE_DESCRIPTOR_UNBOUND` | 6242 |
| `SUMMARY` | 2 |

**type_descriptor_count**

| ค่า | จำนวน |
|---|---|
| `1` | 6242 |
| `3121` | 2 |

**dump_name**

| ค่า | จำนวน |
|---|---|
| `GameClient.local.bin_1.41.01_69151_20260816_0406` | 3122 |
| `GameClient.local.bin_1.41.01_69151_20260816_0428` | 3122 |

**dump_sha256**

| ค่า | จำนวน |
|---|---|
| `daf63c7d13dc7ca601776cc7e4abbf02aa2e367f91ea420b` | 3122 |
| `f982d47b6cec71171ccd2129ee9ce955a0cca05a9d5b606b` | 3122 |

**rtti_status**

| ค่า | จำนวน |
|---|---|
| `TYPE_DESCRIPTOR_PRESENT_COL_OR_HIERARCHY_NOT_CAP` | 6242 |
| `NO_COMPLETE_DUMP_NATIVE_VTABLE_RTTI_CHAIN` | 2 |

## ตัวอย่าง 4 แถวแรก

```
SUMMARY | UNKNOWN | UNKNOWN | UNKNOWN | 0 | UNKNOWN | 3121 | UNKNOWN | UNKNOWN | GameClient.local.bin_1.41.01_69151_20260816_040609.dmp
TYPE_DESCRIPTOR_UNBOUND | UNKNOWN | UNKNOWN | .?AVbad_alloc@std@@ | 0 | 0x018DA064 | 1 | 0x018557EC | UNKNOWN | GameClient.local.bin_1.41.01_69151_20260816_040609.dmp
TYPE_DESCRIPTOR_UNBOUND | UNKNOWN | UNKNOWN | .?AVexception@std@@ | 0 | 0x018DA080 | 1 | 0x018557EC | UNKNOWN | GameClient.local.bin_1.41.01_69151_20260816_040609.dmp
TYPE_DESCRIPTOR_UNBOUND | UNKNOWN | UNKNOWN | .?AVlength_error@std@@ | 0 | 0x018DABD0 | 1 | 0x018557EC | UNKNOWN | GameClient.local.bin_1.41.01_69151_20260816_040609.dmp
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
