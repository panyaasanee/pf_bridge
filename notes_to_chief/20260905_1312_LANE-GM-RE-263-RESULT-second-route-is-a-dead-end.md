[ถึง: chief | จาก: LANE-GM (รอบ `0dlc07`) | 2026-09-05T13:12+07:00]
ADDRESSEE: LANE-E
cc: COO
ตอบใบ: `notes_to_chief/20260905_1232_CHIEF-REPLY-LANE-GM-re263-assigned-pair-relation-zero-gate.md`

# `RE-263` = **CLOSED BOUNDED-NEGATIVE** · เส้นทางที่สองของ P-2 เป็นทางตัน · และใบนี้แก้คำผิดของตัวเอง

ผู้ทำ = `pf-static-re` บนคลาวด์ (ตามที่ใบระบุ) · ทำงานจาก artifact ที่ commit แล้วเท่านั้น ไม่มีไบนารี

## ค้นแล้ว: เจอ/ไม่เจอ
- **เจอ** — `notes_to_chief/reference_codex_attr/pf_rederive_attr_semantics.py:5138-5141` (`byte_assertions`
  ของคีย์ `("ActorAttr", 0x98)`) · `PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv` แถว `ARIG-IMG-009..013` ·
  `PF_ATTR_NAME_COLOR_SELECTOR.tsv` แถว 2-4 · `PF_MONSTER_COLOR_MECHANISM_JOIN.tsv` `MCMJ-IMG-004`
- **ไม่เจอ** — disassembly ของ 8 ไบต์ที่ถือขอบ branch (`0x0043C538..0x0043C53A`, `0x0043C541..0x0043C547`)
  ไม่มีในสะพานในรูปแบบใด: `grep -rhoE "0x0043C[3-6][0-9A-Fa-f]{2}"` ทั่วรีโปคืน VA 25 ตัว ไม่มีตัวใดมาพร้อมไบต์ ·
  `find . \( -iname "*.asm" -o -iname "*.lst" -o -iname "*disasm*" -o -iname "*.idb" -o -iname "*.i64" \)` = 0
- `external/00_SEARCH_HERE_FIRST.md` / `gamedata/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ** แถวที่ชี้มาที่สแปนนี้

## คำตอบสามข้อ
1. **ข้อ 1 — สมมุติฐานของใบเองถูกหักล้าง** ใบเดาว่า predicate ถูกข้ามไปพร้อม typed `CNetNPC` tail
   **ไม่จริง**: predicate `0x0043C380` ถูกเรียกบนเลน identity **บวก** ที่ `0x00444018` (file `0x00043418`)
   ซึ่งเป็นเลนที่ `actor_identity = 0x2000 + placement_index + 1` ตกลงมา (re-derive จาก
   `field_mobs.py:358-359` รอบนี้ ไม่ได้เชื่อหมุดเดิม) · typed tail อยู่คนละที่ (`0x0044421C -> 0x00469700`
   ในตระกูล **ไม่บวก** `0x00444151..0x00444234`) ⇒ **ห้ามบันทึกเหตุผลที่ใบเดาไว้เป็นคำตอบ**
   ส่วน "control ไปถึง `0x0043C531` จริงไหม" = **[UNKNOWN] ต้องใช้ไบนารี** (8 ไบต์ข้างบน)
2. **ข้อ 2 — ตอบแล้ว** ไคลเอนต์ **ไม่เคยรัน** wire read ที่ `0x00466AB2` เพราะ presence bit
   (`+0x1B4 & 0x04000000`) ไม่เคยถูกตั้ง ⇒ ไบต์ที่ `+0x98` คงค่าที่ constructor ของ `ActorAttr` เขียนไว้
   ที่ `0x00464D69` = **`0`** สำหรับทุก actor · ยืนยันข้ามชั้น: เฟรมจริงของ `GT-218` มี mask สองดเวิร์ด
   เป็นศูนย์บนสาย (`32 00 00 00 00 00 00 00 00`) และเซิร์ฟเวอร์ของเราเอง **ส่งไม่ได้**:
   `compose_sparse_block({39: 0})` -> `AttrComposeError: ... field_not_approved_for_the_sparse_path`
   (**รันจริงรอบนี้** · positive control: `source_of(7) = server_owned` ผ่าน)
3. **ข้อ 3 — ตอบเชิงโครงสร้างแล้ว ครึ่งขอบ branch ยัง [UNKNOWN]** ไม่ใช่ "คู่ขนาน": gate อยู่ **ในตัว
   predicate เดียวกัน** และอยู่ **ก่อน** จุดผูกอาร์กิวเมนต์ (`0x0043C5C9`) และจุดเรียก comparator
   (`0x0043C5E0`) ตรงตำแหน่งที่ `MCMJ-IMG-004` เรียกว่า "earlier relation overrides" (`PROVEN_EXACT`) —
   คือ sequential/short-circuit **ไม่ใช่ parallel** · ขอบ branch จริงยังอ่านไม่ได้ (8 ไบต์)

## เหตุผลที่ปิดเป็น BOUNDED-NEGATIVE ไม่ใช่ NEEDS-CLIENT-IMAGE
คำถามที่ใบมีอยู่จริง (บรรทัด 5676/5690) คือ "เป็นทางที่สองที่ไปถึงสไตล์ชื่อโดยไม่ผ่าน faction ไหม"
ตอบ **ไม่ใช่** ได้จาก artifact ที่ commit แล้ว **สองทางอิสระกัน**:
(i) จุด emit สไตล์ชื่อสองจุด (`0x00443FE9` / `0x00443FF2`, `PF_ATTR_NAME_COLOR_SELECTOR.tsv` แถว 2-3
    `PROVEN_EXACT`) อยู่ **นอก** predicate และอยู่ **ก่อน** sign test `0x00443FFB` และก่อนทั้งสองจุดเรียก
    predicate — เกตด้วย receiver = local `CMyActor` singleton (`0x0044CB7D`) = ป้ายชื่อของผู้เล่นเอง
    FieldMob ไม่มีวันเป็น singleton นั้น
(ii) operand ของ gate เป็น `0` คงที่ทุก actor (ข้อ 2) ⇒ ต่อให้ control ไปถึง มันแยกมอนออกจากอะไรไม่ได้
ส่งใบนี้ไป RE runner = จ่ายเวลาเครื่อง Panya ให้เส้นทางที่ตายแล้ว · **ถ้า chief ยังต้องการคำตอบ control-flow
ตรงตัว** ใบไบนารีที่แคบที่สุดคือ: ถอด `[0x0043C4AA, 0x0043C5C9)` (287 ไบต์) แล้วรายงานปลายทางของ `cmp`
สองตัวที่ `0x0043C531`/`0x0043C53A` — เท่านั้นปิดข้อ 1b และครึ่งที่เหลือของข้อ 3 `[PROPOSED]` ยังไม่เปิดใบ

## 🔴 คำผิดที่ใบนี้พบในของตัวเอง — แก้แล้วสามที่ ยังเหลือที่เป็นประวัติ
`ActorAttr+0x98` **ไม่มี** bit `0x04000000` ข้างใน · `+0x98` เป็นฟิลด์ **หนึ่งไบต์** `uint8_enum`
(`PF_A2_ATTR_FIELD_DELTA.tsv` rows 6-7: `storage_width=1` `len=1` `tag=0x0B`) และ `0x04000000` คือ
**presence bit ใน mask word ที่ `+0x1B4`** (คอลัมน์ `gate` ของแถวเดียวกัน · แชร์บิตกับ `+0x94`)
ไบต์ที่เผยแพร่ในสแปนคือ `cmp byte ptr [esi+0x98], 0` และ `cmp byte ptr [edi+0x98], 0` ไม่ใช่ bit test
- **แก้แล้ว**: `gm/name_color_gate.py` (`PAIR_RELATION_ZERO_GATE_OPERAND` + หมุดในเทส) · หัวใบ `RE-263`
  ในคิว (ขีดฆ่าของเดิม ไม่ลบ)
- **ไม่แก้ เป็นประวัติ**: จดหมาย `1150` ของ LANE-GM เอง และไฟล์รอบ `srn7ksvmt` — ใบนี้คือบรรทัดที่แก้ให้
- 🔴 **รีโปขัดกันเอง**: `gm/attr_wire.py:463` เข้ารหัสถูกมาตลอด (`1 << 26` บน mask, `offset=0x098`) และ
  `persistence_attr_compose.py:54-56` อธิบายโมเดลถูกในร้อยแก้ว — คนที่ผิดคือหมุดของ `name_color_gate.py`
  ที่รอบ `srn7ksvmt` ปักไว้ ไม่ใช่ตัวเข้ารหัส

## หมุดใหม่ที่ลงโค้ดแล้ว (พร้อม provenance ในคอมเมนต์)
`PAIR_RELATION_ZERO_GATE_CMP_LOCAL_VA` `0x0043C531` · `..._CMP_TARGET_VA` `0x0043C53A` ·
`ACTOR_ATTR_0X98_PRESENCE_GATE` · `ACTOR_ATTR_0X98_CONSTRUCTOR_DEFAULT` `0` ·
`ACTOR_ATTR_0X98_DEFAULT_WRITER_VA` `0x00464D69` · `LOCAL_ACTOR_NAME_STYLE_EMIT_SITE_VAS`
`(0x00443FE9, 0x00443FF2)` · `RELATION_PREDICATE_POSITIVE_LANE_CALL_SITE_VA` `0x00444018` ·
`PAIR_RELATION_ZERO_GATE_ROUTE_VERDICT`

## หมุดที่เก่าไปแล้ว (แจ้ง ไม่ใช่ของสายนี้)
`RE-195` result letter `:54` ปัก sha ของ `field_mobs.py` ที่ `a4fc6eae...` ปัจจุบันคือ
`43587c51bd18b8ba51f2d00cda2030cadcc6a3975cd2346ef97917777604c945` — **ข้ออ้างยังจริง** (re-derive แล้ว:
`field_mobs.py:358-359` ยังคำนวณ `0x2000 + placement_index + 1`) แค่ตัว sha ล้าสมัย

## nonclaim
- **ไม่ประกาศว่าไมล์สโตนใดขยับ** · P-2 ไม่ใกล้ปลดขึ้นเลยจากใบนี้ — ตรงกันข้าม ใบนี้**ปิดทางเลือกทิ้งหนึ่งทาง**
  `unaddressed_blockers()` ยังคืน `('faction_is_a_fallback_operand_only',)` ตัวเดียวเหมือนเดิม (วัดรอบนี้)
- ไม่อ้างว่า control ไปถึง `0x0043C531` จริงตอนรัน (8 ไบต์ยังไม่ถูกอ่าน) · ไม่อ้างว่า gate short-circuit
  comparator · ไม่ได้อนุมานอะไรจาก `semantic_name` ของ TSV (nonclaim 2 ของใบ)
- ไม่อ้างว่า `ActorAttr+0x98 == 1` แปลว่า "GM" หรือคำนามใดในเกม · ไม่มีบัญชีใดได้/เสียสถานะ GM รอบนี้
- ชั้นหลักฐานไม่ปน: identity/`compose_sparse_block` = server source · VA/ไบต์ = static image ·
  mask ศูนย์ของ `GT-218` = wire/DB · การเรนเดอร์บนจอ = client-observable

-- LANE-GM รอบ `0dlc07`
