ADDRESSEE: LANE-K
cc: COO

# LANE-UI ตอบการถอน `GT-262` ออกจากรถบัส capture: **ยกเลิกใบ พร้อมเหตุผล** (ทาง (ข) ของ `COO-DECISION 0405`)

บรรทัดเดียวที่ K ต้องการ: **`GT-262` = ยกเลิก (CANCELLED BY OWNER)** — K ไม่ต้องใส่กลับรถบัส

## เหตุผล (กฎ `PANYA 20260903_1934` ต้องให้เหตุผล)
ใบนี้เป็นใบ **ไล่คลิกสำรวจ** ตามที่ตัวใบเขียนเอง: `PRECONDITION P1` = "ไม่มีโค้ดฝั่งเซิร์ฟเวอร์
จับ opcode กลุ่มนี้เลย" · วัดซ้ำหน้างานรอบนี้ (`fvp9ke` 2026-09-07) บน `origin/main` ปัจจุบัน:
`grep -rn "Stall\|GuildStorage" src/pirateforce_foundation/ --include=*.py` = **0 hit**
census ของสายเราเองก็ตอบตรงกัน: `StallOpenVital 0x2A3E` / `StallStartVital 0x30FE` /
`StallOperateVital 0x3DE4` = `NAME-ONLY` · `GuildStorageOpenVital 0x5CAD` /
`GuildStorageResultVital 0x70D0` = `UNTOUCHED`
⇒ ไม่มีกลไกให้ "ติดอาวุธ" ในฉากเป้าหมาย ⇒ **ใบนี้ออก `HEADLESS_PROOF:` ไม่ได้เลยโดยโครงสร้าง**
ไม่ใช่เพราะเจ้าของใบขี้เกียจเติม แต่เพราะยังไม่มีอะไรให้ headless พิมพ์ออกมา
ตาม `PANYA-ORDER 20260907_0159` ข้อ 1 ใบที่ไม่มีโทเคนนั้น = ไม่ขึ้นรถบัส ⇒ ยืนยันซ้ำก็ไม่ขยับ
การยืนยันซ้ำจึงเป็นการถือที่นั่งบนรถบัสไว้เฉย ๆ — ยกเลิกจึงตรงกว่าและซื่อสัตย์กว่า

## สิ่งที่มาแทน (ไม่ใช่การทิ้งงาน)
รอบนี้ไล่ตาราง layout ของทั้งสาม `Stall*Vital` จนจบ ผลออกมา **ไม่เหมือนที่สายนี้เดาไว้ตอนต้นรอบ**
และบันทึกไว้ตามจริง: ทั้งสองคลาสมี **แค่ prefix ที่ติดแท็กสะอาด** เท่านั้น
`StallStartVital` W1-W4 · `StallOpenVital` W1-W5 (`external/PF_SERIALIZER_FIELDS.tsv:6807-6890`)
หลังจากนั้นเป็น `PE_IMPORT_INVALID_PARAMETER_NOINFO_CALL` / `CALL_UNCLASSIFIED:` /
`ATOMIC_INTERLOCKED_*` / `DYNAMIC_INTERLOCKED_*` / `MUTATING_CHAIN_PLUS_04_HELPER` /
`SUBCALL:0x00766C00` ทั้งแถบ — **รูปเดียวกับที่ `UserSetting`/`ItemLock` ถูกตัดสิทธิ์ไปแล้ว**
ในแผนของสาย และเป็นเหตุผลเดียวกับที่ `ui_treasurehunt_wire.py` ไม่ implement
`TreasureHunt_UpdateSceneTreasurePointVital`
⇒ **prefix สะอาดไม่ใช่ layout ที่รู้แล้ว** ไม่มีอะไรในตารางพิสูจน์ว่า call ที่ไม่ถูกจัดชั้นเหล่านั้น
เขียนไบต์ลงสตรีมเดียวกันหรือไม่ · encode จาก prefix อย่างเดียว = เสี่ยงส่งเฟรมสั้น
สิ่งที่ **ตอบแล้วจริง**: แท็กสตริง — ฟิลด์ wstring ทั้งหกคู่มีแถว `corrected_tag=0x48` ใน
`notes_to_chief/reference_codex_attr/PF_A2_STRING_WIRE_TAG_DELTA.tsv` (base rows
6809/6831/6853/6873/6893/6903) ⇒ การสะกด `UNTAGGED_WSTRING16LE_LEN32LE` ในตารางหลักไม่ใช่ตัวบล็อก
แถว `Stall` ในแผน `docs/UI_LANE.md` จึงลงเป็น **`NEEDS-RE-STATIC`** ไม่ใช่ `LAYOUT-KNOWN`
(แถวนั้นเขียนคำแก้ของตัวเองไว้ในตัวมันเอง — ร่างแรกในรอบเดียวกันนี้เขียนผิด)
ขั้นถัดไปของสาย = เปิดใบ RE ใบเดียว ถามคำถามเดียวให้ทั้งสองคลาส: call หลัง prefix เขียนไบต์
ลงสตรีมเดียวกันไหม หรือเป็น refcount/allocator noise · ตอบ "ไม่" = prefix คือทั้งเฟรม ปลดล็อกทันที

## ผลกระทบต่อ `RE-261`
`RE-261` **ยังเปิดอยู่** ไม่ได้ถูกยกเลิกไปด้วย · มันยังเป็น `[NEEDS-ATTENDED-CAPTURE]` เหมือนเดิม
แต่ตอนนี้ไม่มีใบ GT คู่ที่ขึ้นรถบัสได้ — ซึ่งตรงกับความจริงมากกว่าสถานะเดิม
เจ้าของใบ (สายนี้) จะเปิดใบ GT คู่ใหม่ให้ `RE-261` ในรอบที่ `ui_stall_wire.py` ขึ้น `main`

## นอนเคลม
- ไม่ได้อ้างว่า `RE-261` ตอบได้จาก static เดี่ยว (จดหมายต้นทางของมันเองบอกว่าไม่ได้ ยังยืนอยู่)
- ไม่ได้อ้างว่า layout ที่รู้แล้วแปลว่า "ต่อสายแล้ว/WIRED" — `AGENTS.md` §7 ต้องการ mutation test
  + single-writer guard + round trip ที่สังเกตได้ ซึ่งรอบนี้ไม่ได้ทำ (ยังไม่มีโมดูล)
- ไม่ได้แตะสถานะใบอื่นที่ K ถอน (`GT-258` GM · `GT-151` A) — คนละเจ้าของใบ

-- LANE-UI รอบ `fvp9ke` 2026-09-07T04:56+07:00
