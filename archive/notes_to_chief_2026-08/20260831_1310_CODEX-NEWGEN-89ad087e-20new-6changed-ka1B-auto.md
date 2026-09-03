> **SUPERSEDED FOR ATTR ROLE GUIDANCE — 2026-08-31 20:35 +07:00.** generation `89ad087e…` และคำกล่าวว่าแถวทั้งหมดเป็น IMAGE ไม่ใช่สถานะปัจจุบัน ห้ามใช้ใบนี้ทำ role/trait policy หรือ implementation ให้ใช้เฉพาะ `20260831_2035_CODEX-CHECKPOINT-P04-ROLE-TRAITS.md` และ authoritative generation `5f18676004e95fa7466561871f3c25a2b6b217af81e9751cf3f446e4efa979f1`; travelling mirror ยัง stale และไม่ได้รับการ refresh ใน P0-4

# Codex ส่งงานรอบใหม่ - generation `89ad087edd0ea1ea`

ใบนี้เขียนอัตโนมัติโดย `tools_bridge/pf_attr_conflict_digest.py` ไม่ใช่คนเขียน - มันบอกแค่ว่า**อะไรเปลี่ยน** ส่วน**แปลว่าอะไร** ต้องมีคนอ่านแล้วเขียนใบตีความตามมา

- generation ก่อนหน้า: `(ยังไม่เคยมิเรอร์)`
- generation นี้: `89ad087edd0ea1ea0d707897ad580e6aa1a1b8b066868370d9c654b86073c462`
- ยืนยัน sha256 ของ artifact ครบทุกไฟล์แล้วก่อนคัดลอก (ไฟล์ที่เขียนค้างจะไม่ถูกเผยแพร่)

## ไฟล์ใหม่ที่ไม่เคยมีมาก่อน (20)

- `PF_A2_ACHIEVEMENTS_CODEC_CORRECTION.tsv` (430547 bytes)
- `PF_A2_ATTR_FIELD_DELTA.tsv` (488493 bytes)
- `PF_A2_ATTR_SEMANTIC_DELTA.tsv` (16186 bytes)
- `PF_A2_COLLECTION_CODEC_CORRECTION.tsv` (102444 bytes)
- `PF_A2_COOLDOWN_CODEC_CORRECTION.tsv` (34749 bytes)
- `PF_A2_CRYSTAL_CODEC_CORRECTION.tsv` (104939 bytes)
- `PF_A2_CSKILL_CODEC_CORRECTION.tsv` (53245 bytes)
- `PF_A2_DAILYREWARD_CODEC_CORRECTION.tsv` (62349 bytes)
- `PF_A2_EXPRESS_GET_CODEC_CORRECTION.tsv` (48963 bytes)
- `PF_A2_INSTANCE_REFRESH_CODEC_CORRECTION.tsv` (41372 bytes)
- `PF_A2_ITEMATTR_CODEC_CORRECTION.tsv` (131177 bytes)
- `PF_A2_ITEMVARY_CODEC_CORRECTION.tsv` (39754 bytes)
- `PF_A2_PET_ACTIVITY_CORRECTION.tsv` (116143 bytes)
- `PF_A2_QUEST_CODEC_CORRECTION.tsv` (1047985 bytes)
- `PF_A2_SYSTEM_GIFT_CODEC_CORRECTION.tsv` (49866 bytes)
- `PF_A2_WINE_CODEC_CORRECTION.tsv` (129907 bytes)
- `PF_ATTR_NAME_COLOR_SELECTOR.tsv` (37350 bytes)
- `PF_ATTR_QUEST_MARK_SELECTOR.tsv` (52137 bytes)
- `PF_ATTR_ROLE_DISCRIMINATOR.tsv` (41731 bytes)
- `PF_ATTR_SEMANTIC_DELTA.tsv` (856188 bytes)

## ไฟล์เดิมที่เนื้อหาเปลี่ยน (6)

- `PF_ATTR_DATA_BINDINGS.tsv` (53723 bytes)
- `PF_ATTR_FIELD_SEMANTICS.md` (8813 bytes)
- `PF_ATTR_FIELD_SEMANTICS.tsv` (1339980 bytes)
- `PF_ATTR_FOR_SERVER.md` (124266 bytes)
- `PF_ATTR_QUARANTINE.tsv` (359 bytes)
- `PF_ATTR_SEMANTIC_REPORT.md` (41440 bytes)

## ไม่ได้มิเรอร์ (3) - อยู่บนดิสก์บริดจ์เท่านั้น

- `PF_A2_ITEMBAG_CODEC_CORRECTION.tsv` - 2149519 bytes, over the sync cap
- `PF_ATTR_CONFLICTS.tsv` - 3528388 bytes, over the sync cap
- `PF_ATTR_UNRESOLVED.tsv` - 2346810 bytes, over the sync cap

## conflict รอบนี้

- แถวทั้งหมด 1283 · Codex ปิดเอง 645 · **ยัง OPEN 638**
  - A_NON_WIRE_ROW: 426
  - D_LAYOUT: 120
  - B_MASK_GATE: 68
  - E_OTHER: 24
- แถว OPEN ที่แตะคลาสที่เซิร์ฟเวอร์ encode จริงวันนี้ (ActorAttr/BasicAttr): **71**
- unresolved 966 แถว

## อ่านที่ไหน

`pf_bridge/notes_to_chief/reference_codex_attr/` อ่าน `README_WHAT_THIS_IS.md` ก่อน · ตัวเลข conflict อยู่ใน `PF_ATTR_CONFLICTS_HEADLINE.txt` · แถวที่แตะโค้ดจริงอยู่ใน `PF_ATTR_CONFLICTS_OPEN_WIRED.tsv`

**กติกาที่ยังใช้เหมือนเดิม:** ทุกแถวของ Codex เป็นหลักฐานชั้น IMAGE (แกะไบนารีนิ่ง) ห้ามยกไปอ้างเป็นผลชั้น client-observable และคอลัมน์ `nonclaim` มีไว้ให้อ่าน - มันบอกว่าแถวนั้น**ไม่ได้**พิสูจน์อะไร

-- ka1-B (อัตโนมัติ)
