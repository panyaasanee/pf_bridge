# PF_SERIALIZER_FIELDS.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_SERIALIZER_FIELDS.tsv` ขนาด 25195473 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **6931** · คอลัมน์: **12**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`message` · `direction(W/R)` · `order` · `tag` · `field_offset` · `len` · `gate_condition` · `span_start` · `span_end` · `span_sha256` · `file_off_claim` · `source`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**direction(W/R)**

| ค่า | จำนวน |
|---|---|
| `R` | 3467 |
| `W` | 3464 |

**len**

| ค่า | จำนวน |
|---|---|
| `N/A` | 3462 |
| `1` | 989 |
| `4` | 747 |
| `8` | 541 |
| `2` | 506 |
| `4+N_bytes` | 408 |
| `0` | 278 |

## ตัวอย่าง 4 แถวแรก

```
Attribute | R | 1 | EMPTY | N/A | 0 | ALWAYS | 0x00515EC0 | 0x00515EC3 | 1d10894625976bca9d8906f3ecf1e766b94e9219ec3bf1c30e02feea5e18
Attribute | W | 1 | EMPTY | N/A | 0 | ALWAYS | 0x00515EC0 | 0x00515EC3 | 1d10894625976bca9d8906f3ecf1e766b94e9219ec3bf1c30e02feea5e18
AvatarAttr | R | 1 | EMPTY | N/A | 0 | wire_empty_argument_value_copier@0x0043BB80 file_off=0x0003A | 0x0043BB80 | 0x0043BB91 | b625098be0bbf3e36927c8dce2ccf3cf171563fc8f1465a41039974b332c
AvatarAttr | W | 1 | EMPTY | N/A | 0 | wire_empty_argument_value_copier@0x0043BB80 file_off=0x0003A | 0x0043BB80 | 0x0043BB91 | b625098be0bbf3e36927c8dce2ccf3cf171563fc8f1465a41039974b332c
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
