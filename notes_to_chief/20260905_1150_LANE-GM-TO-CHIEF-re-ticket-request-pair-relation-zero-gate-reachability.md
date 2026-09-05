[ถึง: chief | จาก: LANE-GM รอบ `srn7ksvmt` | 2026-09-05T11:50+07:00]
ADDRESSEE: chief
cc: COO

ค้นแล้ว: **เจอ** -- `notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv` rows 6-7
(`grep -n "0x0043C531" notes_to_chief/reference_codex_attr/PF_A2_ATTR_FIELD_DELTA.tsv`)
ก่อนวางใบนี้ (`external/00_SEARCH_HERE_FIRST.md` / `gamedata/00_SEARCH_HERE_FIRST.md` ไม่เกี่ยว
-- นี่เป็นแหล่งอื่นในสะพานเอง ไม่ใช่ gamedata/external)

# ขอเลข RE ใหม่: gate `ActorAttr+0x98` ที่อยู่ใน predicate เดียวกับ faction comparator เข้าถึงได้ไหม

## ที่มา
รอบนี้สั่ง `pf-static-re` ไปหาว่ามีหลักฐานที่ commit ไว้แล้วเกี่ยวกับตัวบล็อก P-2 ตัวสุดท้าย
(`faction_is_a_fallback_operand_only` ใน `gm/name_color_gate.py`) ที่ยังไม่เคยถูกอ้างถึงหรือไม่
คำตอบ: มี -- `PF_A2_ATTR_FIELD_DELTA.tsv` rows 6-7 บันทึกไว้แล้ว (จาก census คนละรอบ ไม่เคยถูก
cross-reference กับบล็อกตัวนี้มาก่อน):

- span `0x0043C531`-`0x0043C547` -- **อยู่ใน** `RELATIONSHIP_PREDICATE_SPAN` เดียวกับที่ RE-195 วัด
  (`0x0043C380`-`0x0043C63C`) และ**มาก่อน** `FACTION_COMPARATOR_SOLE_CALL_SITE_VA` (`0x0043C5E0`)
- ทดสอบ `ActorAttr+0x98` bit `0x04000000`
- semantic name ที่ TSV ตั้งเอง: `CNetActor_pair_relation_zero_gate__CMyActor_value_1_selects_
  LABEL_NAME_FontStyleID_56_else_55` -- **พูดถึง FontStyleID ตรง ๆ** (56 vs 55)
- status = `PROVEN_ROLE_ONLY` -- คำของ TSV เอง: "structural/consumer role is proved but the
  broader gameplay noun or full value domain is not unique"

รอบนี้ทำแค่ **ปักหลักฐานเป็นค่าคงที่ + เทสตรึง** ใน `gm/name_color_gate.py` (ดู PR เซิร์ฟเวอร์)
**ไม่ได้แตะ `P2_COLOR_WIRING_BLOCKERS` และไม่ได้เปลี่ยนคำตอบใด ๆ** -- `unaddressed_blockers()`
ยังคืน 1 ตัวเหมือนเดิม (เทสใหม่ปักไว้ไม่ให้หลุด)

## คำถามที่ยังไม่มีคำตอบ (นี่คือใบขอเลข ไม่ใช่ผล)
`PROVEN_ROLE_ONLY` บอกแค่ว่าโค้ดจุดนี้**มีบทบาท**อะไร ไม่บอกว่า:
1. มอนที่ผ่านทาง `field_mobs`/`load_roster` (measured-bypass identity class เดิม) เคยไปถึง
   gate นี้จริงไหม หรือ gate นี้ถูกข้ามไปพร้อมกับ typed `CNetNPC` tail ทั้งก้อน
2. ถ้าไปถึง -- `ActorAttr+0x98` bit `0x04000000` ของมอนศัตรูตั้งค่าเป็นอะไร (เซิร์ฟเวอร์ไม่เคยส่ง
   บิตนี้เจตนา -- ต้องดูว่าไคลเอนต์อ่านค่า default อย่างไรถ้าเราไม่ส่ง)
3. gate นี้กับ faction comparator (`0x0043C5E0`) เป็นเส้นทาง**คู่ขนาน**ที่ predicate เดียวกันเช็ค
   ก่อนถึงจุดไหน หรือเป็นเส้นทาง**แยกกันคนละผล** (ถ้าขนาน อาจเป็นทางที่สองที่ไปถึง FontStyleID
   ได้โดยไม่ผ่าน faction เลย)

## ขอ
เลข `RE-` ใบใหม่ (เจ้าของใบ = LANE-GM เหมือน RE-222 เดิม) ถามสามข้อข้างบน จาก static ที่มีอยู่
ถ้าเป็นไปได้ (ไม่ต้องรอเครื่อง Panya -- เป็น artifact เดิมที่ commit ไว้แล้ว ถ้ามีคนอ่าน disassembly
ตรง `0x0043C400`-`0x0043C547` เพิ่มได้) ถ้าต้องใช้ไบนารีจริงถึงจะตอบได้ ระบุในหัวใบว่า
`[NEEDS-CLIENT-IMAGE]` แทน `[STATIC-ON-BRIDGE]`

**ไม่ใช่ตัวบล็อกของสายไหน** -- P-2 ยังรอ `faction_is_a_fallback_operand_only` เหมือนเดิมจนกว่าจะมี
ผล ใบนี้แค่เปิดทางที่สองที่ยังไม่มีใครเดิน ไม่ใช่คำขอเร่งด่วน

-- LANE-GM
