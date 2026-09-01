# PF_A2_ITEMBAG_CODEC_CORRECTION.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_A2_ITEMBAG_CODEC_CORRECTION.tsv` ขนาด 2149519 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **448** · คอลัมน์: **37**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`correction_key` · `conflict_key` · `class` · `base_row_ref` · `direction` · `delta_action` · `prior_order` · `prior_tag` · `prior_field_offset` · `prior_gate` · `field_key` · `wire_key` · `offset_basis` · `object_offset` · `storage_width` · `wire_len` · `corrected_order` · `tag` · `corrected_gate` · `semantic_name` · `structural_status` · `semantic_status` · `field_source_va` · `field_source_file_offset` · `wire_call_va` · `wire_call_file_offset` · `persistent_write_va` · `consumer_va` · `codec_span_start` · `codec_span_end` · `codec_span_sha256` · `support_span_sha256` · `evidence_key` · `source` · `blocker` · `required_next_evidence` · `image_sha256`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**class**

| ค่า | จำนวน |
|---|---|
| `CollectionBagAttr` | 58 |
| `ExpressBagAttr` | 58 |
| `ItemMallBagAttr` | 58 |
| `UnlimitBagAttr` | 58 |
| `BackpackAttr` | 44 |
| `CGuildStorageAttr` | 44 |
| `StorageAttr` | 44 |
| `ItemBagAttr` | 42 |
| `ItemBagAttr_Equiped` | 42 |

**direction**

| ค่า | จำนวน |
|---|---|
| `R` | 224 |
| `W` | 224 |

**delta_action**

| ค่า | จำนวน |
|---|---|
| `REMOVE_NON_WIRE_CONTROL_FLOW_ROW` | 306 |
| `CORRECT_FIELD_LAYOUT` | 84 |
| `REMOVE_NON_WIRE_POST_DECODE_TRAVERSAL_ROW` | 56 |
| `ANNOTATE_INHERITED_FIELD_ALIAS` | 2 |

**prior_order**

| ค่า | จำนวน |
|---|---|
| `19` | 18 |
| `21` | 18 |
| `23` | 18 |
| `8` | 18 |
| `6` | 18 |
| `10` | 18 |
| `12` | 18 |
| `14` | 18 |
| `11` | 18 |
| `18` | 18 |
| `16` | 18 |
| `24` | 18 |
| `9` | 18 |
| `22` | 18 |

**prior_tag**

| ค่า | จำนวน |
|---|---|
| `PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL` | 112 |
| `PE_IMPORT_INVALID_PARAMETER_NOINFO_SINGLETON_REG` | 72 |
| `0x0F` | 44 |
| `MUTATING_POINTER_SLOT_TRAVERSAL_HELPER` | 26 |
| `CALL_UNCLASSIFIED:INDIRECT(DEREF(DEREF(RET(0x004` | 18 |
| `CALL_UNCLASSIFIED:0x0046EC20` | 18 |
| `CALL_UNCLASSIFIED:0x005D2180` | 18 |
| `DYNAMIC_INTERLOCKED_DECREMENT_ECX_PLUS_0C_VTABLE` | 18 |
| `CALL_UNCLASSIFIED:0x0046E2D0` | 18 |
| `0x32` | 18 |
| `CALL_UNCLASSIFIED:0x0046BAA0` | 18 |
| `CALL_UNCLASSIFIED:INDIRECT(DEREF(DEREF(DEREF(DER` | 18 |
| `UNKNOWN` | 18 |
| `ATOMIC_INTERLOCKED_INCREMENT_ECX_PLUS_0C` | 18 |

**prior_field_offset**

| ค่า | จำนวน |
|---|---|
| `UNKNOWN(invalid_parameter_import_call_wire_effec` | 112 |
| `UNKNOWN(direct_call_not_proven_serializer)` | 80 |
| `UNKNOWN(invalid_parameter_singleton_register_cal` | 72 |
| `UNKNOWN(indirect_call_not_proven_serializer_slot` | 36 |
| `UNKNOWN(mutable_pointer_slot_traversal_alias_unp` | 26 |
| `STACK@0x0046F180+0x40` | 18 |
| `UNKNOWN(dynamic_vtable_plus_0x04_target_unresolv` | 18 |
| `STACK@0x0046F180+0x3C` | 18 |
| `UNKNOWN(indirect_serializer_direction_unresolved` | 18 |
| `UNKNOWN(atomic_target_object_alias_unproved)` | 18 |
| `STACK@0x0046F180+0x18` | 9 |
| `DEREF(STACK@0x0046F180+0x18)+0x10` | 9 |
| `+0x8A` | 8 |
| `+0x68` | 6 |

## ตัวอย่าง 4 แถวแรก

```
1b2535407263c810b64709c845aae59b9a581bb884e57220f2207e2affe3 | 79446615149e8ace6d9a5614dc59d89d9d136f7e6b8266b376b26d5c1e73 | BackpackAttr | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|063a4f136895fa8c75fe40a9ad | R | CORRECT_FIELD_LAYOUT | 26 | 0x0B | +0x68 | ALWAYS
1d992f6d734e75145f90073e824203526c1ec3dd0edee1bc660dfdf13ab1 | 1117ffa7ece9ee9cd1a356bc107a10a43bfb12aa8d2a2fe72795354e13bf | BackpackAttr | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|0dd9ca2a740143e64fa9ca7e3f | R | CORRECT_FIELD_LAYOUT | 19 | CALL_UNCLASSIFIED:INDIRECT(DEREF(DEREF(RET(0x0046BAA0))+0x34 | UNKNOWN(indirect_call_not_proven_serializer_slot) | direction_call@0x00469FAF file_off=0x000693AF target_test@0x
87c7a08e0769da0349ca34c119833bb339ec585fbf95635ae8d930040597 | a53666d8f5819ebc848ac724e8080639f23622ceeed4b635083077173851 | BackpackAttr | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|178be8560a6e162cc5101a059f | R | REMOVE_NON_WIRE_CONTROL_FLOW_ROW | 21 | CALL_UNCLASSIFIED:0x0046EC20 | UNKNOWN(direct_call_not_proven_serializer) | direction_call@0x00469FAF file_off=0x000693AF target_test@0x
01f8150ca04e8e91b9b18bba0831662bda50d5f837d1289bf8dd4ad4300e | d4f0b419bd6377f97e0ee24472d82c8ae952be60cfaf58291507a0b2d527 | BackpackAttr | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|1bb2a4760623d6727bbaa0283a | R | CORRECT_FIELD_LAYOUT | 23 | 0x0F | STACK@0x0046F180+0x40 | direction_call@0x00469FAF file_off=0x000693AF target_test@0x
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
