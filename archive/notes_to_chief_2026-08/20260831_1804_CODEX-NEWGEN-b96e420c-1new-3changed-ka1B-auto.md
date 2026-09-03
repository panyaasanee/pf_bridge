# Codex ส่งงานรอบใหม่ - generation `b96e420c290201ce`

ใบนี้เขียนอัตโนมัติโดย `tools_bridge/pf_attr_conflict_digest.py` ไม่ใช่คนเขียน - มันบอกแค่ว่า**อะไรเปลี่ยน** ส่วน**แปลว่าอะไร** ต้องมีคนอ่านแล้วเขียนใบตีความตามมา

- generation ก่อนหน้า: `3578f2aa13fcf22e`
- generation นี้: `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`
- ยืนยัน sha256 ของ artifact ครบทุกไฟล์แล้วก่อนคัดลอก (ไฟล์ที่เขียนค้างจะไม่ถูกเผยแพร่)

## ไฟล์ใหม่ที่ไม่เคยมีมาก่อน (1)

- `PF_MONSTER_PRESENTATION.md` (5105 bytes)

## ไฟล์เดิมที่เนื้อหาเปลี่ยน (3)

- `PF_ATTR_FOR_SERVER.md` (126774 bytes)
- `PF_ATTR_RUNTIME_FIELDS.tsv` (20578 bytes)
- `PF_ATTR_SEMANTIC_REPORT.md` (45130 bytes)

## ไม่ได้มิเรอร์ (4) - อยู่บนดิสก์บริดจ์เท่านั้น

- `PF_A2_ITEMBAG_CODEC_CORRECTION.tsv` - 2149519 bytes, over the sync cap
- `PF_ATTR_CONFLICTS.tsv` - 3531496 bytes, over the sync cap
- `PF_ATTR_UNRESOLVED.tsv` - 2355364 bytes, over the sync cap
- `PF_MONSTER_PRESENTATION.tsv` - 4685803 bytes, over the sync cap

## conflict รอบนี้

- แถวทั้งหมด 1286 · Codex ปิดเอง 646 · **ยัง OPEN 640**
  - A_NON_WIRE_ROW: 426
  - D_LAYOUT: 120
  - B_MASK_GATE: 68
  - E_OTHER: 26
- แถว OPEN ที่แตะคลาสที่เซิร์ฟเวอร์ encode จริงวันนี้ (ActorAttr/BasicAttr): **71**
- unresolved 977 แถว

## อ่านที่ไหน

`pf_bridge/notes_to_chief/reference_codex_attr/` อ่าน `README_WHAT_THIS_IS.md` ก่อน · ตัวเลข conflict อยู่ใน `PF_ATTR_CONFLICTS_HEADLINE.txt` · แถวที่แตะโค้ดจริงอยู่ใน `PF_ATTR_CONFLICTS_OPEN_WIRED.tsv`

**กติกาที่ยังใช้เหมือนเดิม:** ทุกแถวของ Codex เป็นหลักฐานชั้น IMAGE (แกะไบนารีนิ่ง) ห้ามยกไปอ้างเป็นผลชั้น client-observable และคอลัมน์ `nonclaim` มีไว้ให้อ่าน - มันบอกว่าแถวนั้น**ไม่ได้**พิสูจน์อะไร

-- ka1-B (อัตโนมัติ)
