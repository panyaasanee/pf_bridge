# PF_ATTR_CONFLICTS.tsv - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)

ไฟล์เต็ม `pf_bridge/external/PF_ATTR_CONFLICTS.tsv` ขนาด 3531500 ไบต์ **เกินเพดาน 2 MB ของ `pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**

- แถวข้อมูล: **1286** · คอลัมน์: **16**
- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่

## คอลัมน์

`conflict_key` · `field_key` · `conflict_kind` · `frozen_claim_ref` · `frozen_claim` · `frozen_claim_source` · `rederived_claim` · `rederived_evidence_key` · `rederived_evidence_artifact` · `rederived_source` · `resolution_status` · `source` · `image_sha256` · `conflict_group` · `claim_layer` · `counterpart_key`

## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)

**frozen_claim_source**

| ค่า | จำนวน |
|---|---|
| `IMAGE` | 1271 |
| `NON_EVIDENCE_REPORT` | 6 |
| `NON_EVIDENCE_SERVER_CODE` | 5 |
| `N/A` | 2 |
| `NON_EVIDENCE_ORDER_AND_AUDIT_REPORT` | 2 |

**rederived_evidence_artifact**

| ค่า | จำนวน |
|---|---|
| `PF_A2_ITEMBAG_CODEC_CORRECTION.tsv` | 448 |
| `PF_A2_QUEST_CODEC_CORRECTION.tsv` | 202 |
| `PF_A2_PET_ACTIVITY_CORRECTION.tsv` | 100 |
| `PF_A2_ACHIEVEMENTS_CODEC_CORRECTION.tsv` | 86 |
| `PF_A2_ACTOR_CODEC_CORRECTION.tsv` | 52 |
| `PF_A2_WINE_CODEC_CORRECTION.tsv` | 52 |
| `PF_A2_CRYSTAL_CODEC_CORRECTION.tsv` | 44 |
| `PF_A2_ITEMATTR_CODEC_CORRECTION.tsv` | 42 |
| `PF_A2_COLLECTION_CODEC_CORRECTION.tsv` | 30 |
| `PF_A2_ITEMVARY_CODEC_CORRECTION.tsv` | 30 |
| `PF_A2_CSKILL_CODEC_CORRECTION.tsv` | 28 |
| `PF_A2_DAILYREWARD_CODEC_CORRECTION.tsv` | 28 |
| `PF_A2_COOLDOWN_CODEC_CORRECTION.tsv` | 22 |
| `PF_A2_EXPRESS_GET_CODEC_CORRECTION.tsv` | 22 |

**rederived_source**

| ค่า | จำนวน |
|---|---|
| `IMAGE` | 1285 |
| `DATA` | 1 |

**resolution_status**

| ค่า | จำนวน |
|---|---|
| `CORRECTED_IN_ACTIVE_ATTR_OVERLAY_PRESERVE_FROZEN` | 628 |
| `OPEN_REDERIVED_IMAGE_CONFLICT` | 616 |
| `OPEN_NEEDS_MEASURED_NONWIRE_CORRECTION` | 17 |
| `CORRECTED_IN_ACTIVE_CHECKPOINT_PRESERVE_PRIOR_GE` | 12 |
| `OPEN_SERVER_CODE_SEMANTIC_CONFLICT` | 5 |
| `CORRECTED_IN_ACTIVE_ATTR_OVERLAY_PRESERVE_OLD_CH` | 3 |
| `OPEN_CROSS_SOURCE_MISMATCH` | 2 |
| `REFUTED_AND_CORRECTED_IN_ACTIVE_CHECKPOINT` | 2 |
| `STATIC_PREMISE_WITHDRAWN_NON_IMAGE_CONCLUSION_OU` | 1 |

**source**

| ค่า | จำนวน |
|---|---|
| `IMAGE` | 1285 |
| `DATA` | 1 |

**image_sha256**

| ค่า | จำนวน |
|---|---|
| `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d21` | 1285 |
| `N/A` | 1 |

## ตัวอย่าง 4 แถวแรก

```
b3fe2e2b565117184a3fc7e380b53de52bae73d44847cb914e2d25038df9 | ActorAttr@0x1B4.8#R | FROZEN_A2_MASK_STORAGE_LOCATION | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|195c56d69b36fb79e51e4474dc | field_offset=STACK@0x00466230+0x14 | IMAGE | mask storage is ActorAttr +0x1B4/+0x1B8 (8 bytes) | a67c074076011dbcef387e201cb62b10141e0eb7969b3eff013daec24e5f | PF_A2_ACTOR_CODEC_CORRECTION.tsv | IMAGE
c99f9c63771f4b6267d6abfee89516ff0e2a6454853bea3f7a1ed18d0802 | ActorAttr@0x78.4#R:b0x00000004 | FROZEN_A2_OMITTED_NESTED_GROUP_GATE | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|d37e89a3113cc826b7d811329c | gate=test@0x004667ED file_off=0x00065BED mask=0x4 set | IMAGE | gate=+0x1B4 & 0x00000004 AND +0x1BC != 0 | 09b0116843d9e1bc090af5f1157ad6bb6a1cc83b81783cb4e406c0ae3209 | PF_A2_ACTOR_CODEC_CORRECTION.tsv | IMAGE
113d3bb9bba22077d35b6b7656a9e92d52a73575d6c270fe65d72ba143fd | ActorAttr@0x7C.4#R:b0x00000008 | FROZEN_A2_OMITTED_NESTED_GROUP_GATE | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|c891d7cd355fce12db21eb5c56 | gate=test@0x00466805 file_off=0x00065C05 mask=0x8 set | IMAGE | gate=+0x1B4 & 0x00000008 AND +0x1BC != 0 | f6c3065e04fc91f8bae33ee2020bbf5d8d367470b44186cfd2b625a26982 | PF_A2_ACTOR_CODEC_CORRECTION.tsv | IMAGE
0121114a961832b67d0b3f0056403e2650e74404804f9d6cc8ce0ae8108b | ActorAttr@0x80.2#R:b0x00000010 | FROZEN_A2_OMITTED_NESTED_GROUP_GATE | PF_A2_SERIALIZER_SLOT34_DELTA.tsv|7098f65592ffde25998e38328c | gate=test@0x0046681D file_off=0x00065C1D mask=0x10 set | IMAGE | gate=+0x1B4 & 0x00000010 AND +0x1BC != 0 | 24e9685561158a6ab33b0fe84adbf8150f2c02d9511eba46bf90a5eb883d | PF_A2_ACTOR_CODEC_CORRECTION.tsv | IMAGE
```

อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ
