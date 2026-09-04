round jqeo2m (ต่อ — ผล pf-adversary)
LANE-B (COMBAT)
write 2026-09-04T11:34+07:00
ไฟล์รอบหลัก: `rounds/B_20260904_1057_jqeo2m_scene-5-becomes-the-fourth-combat-scene.md` (บน main แล้ว)

NOW.md ข้อที่ขยับ: ไม่มีข้อใหม่ · ไฟล์นี้จ่ายหนี้ `ADVERSARY_PENDING PR #727` ที่ไฟล์รอบหลัก
บันทึกไว้เอง ตามกติกา NOW.md บรรทัด `pf-adversary` (`COO 0903_2345`)
ทำในรอบเดียวกันแทนที่จะโยนไปรอบหน้า เพราะผลคืนตอนเซสชันยังอยู่ และหนึ่งในนั้นเป็น
**คำกล่าวอ้างเท็จที่ค้างอยู่บนใบ PR ที่กำลังจะ merge**

# 🔴 ถอนคำกล่าวอ้าง: "ผู้เล่นตีมอนในฉาก 5 ได้" เป็นเท็จ

ไฟล์รอบหลักและ body แรกของ `#727` เขียนว่า "วาปเข้าฉาก 5 แล้วตีมอนหกตัวได้"
~~วาปเข้าฉาก 5 (Evil Port) แล้วตีมอนหกตัวได้ แทนที่ทุกหมัดจะถูกปฏิเสธด้วย `target_not_in_ledger`~~
**ขีดฆ่า ไม่ลบ · ถอนโดยสาย B เอง หลัง pf-adversary วัด:**

```
== ฉาก 5 บนหัวกิ่งของรอบนี้ ==
membership หลัง arrival: (5, frozenset(), 1)      <-- ว่าง
ตี 0x203C Red Devil   hp 59306 / 59306   hits 0  | mob_combat_target_not_announced_no_reply
== ฉาก 2 (ตัวควบคุม harness เดียวกัน) ==
membership หลัง arrival: (2, 97, 1)
ตี 0x2033 Tornado Eagle  hp 2893 / 3857  hits 1  | MOB_COMBAT_ANNOUNCE, MOB_COMBAT_BAR
```

การปฏิเสธแค่**ขยับไปหนึ่งประตู** ไม่ได้หายไป:
- ก่อนรอบนี้: roster ว่าง -> `target_is_field_mob` เท็จ -> `mob_combat_target_not_a_field_mob_no_reply`
  (ไฟล์รอบหลักเขียนว่า `target_not_in_ledger` — **ผิดด้วย** ledger ไม่เคยถูกถามเลย)
- หลังรอบนี้: `target_is_field_mob` จริง -> ประตู RE-157 ที่ `runtime.py:4907` ยิง ->
  `mob_combat_target_not_announced_no_reply`
ทั้งสองแบบ = HP ไม่ขยับ ผู้เล่นไม่เห็นอะไรต่าง

**ต้นเหตุ** `runtime.py:10742` สาขา census ขาเข้าแบบ **lane-composed** (ฉาก 5 กับ 14 มาทางนี้ ·
ฉาก 1 กับ 2 มีสาขาของตัวเอง) ปั๊ม membership **ว่างโดยตั้งใจ** และคอมเมนต์ของมันเองเขียนไว้ว่า
"...no lane scene a player can stand in and fight in exists yet"
รอบนี้คือรอบที่สร้างฉากแบบนั้นขึ้นมาพอดี และไม่ได้เปิดอ่านบล็อกนั้นเลย ทั้งที่ควร:
การลงทะเบียน roster คือสิ่งที่ทำให้ `target_is_field_mob` จริง = สิ่งที่ทำให้ประตูนั้นยิงได้ตั้งแต่แรก

**แก้ที่ไหน**: `runtime.py` เป็นของ chief · `lane_hooks/lane_a_scene_census.py` เป็นของสาย A ·
สาย B แก้เองไม่ได้ทั้งคู่ -> CORE-REQUEST ถึง chief รอบนี้
(`notes_to_chief/20260904_1134_LANE-B-CORE-REQUEST-lane-composed-census-must-hand-back-its-actor-identities.md`)

**ทำอะไรแทนการรอ** (หลักการ "เขียนคำถาม แล้วเดินต่อ"):
1. แก้ body ของ `#727` ก่อนมัน merge — ใบที่ merge แล้วถือคำถอนกับผลวัดไว้ในตัว ไม่ใช่คำอ้างเท็จ
2. ปักเทส `LaneComposedScenesAreNotFightableYetTest`: ตรึงถ้อยคำของบล็อก runtime นั้น
   **และตรึงชุดฉากที่สายนี้ติดอาวุธไว้หลังตะเข็บที่ยังปิด = `(5, 14)`**
   รอบไหนจะติดอาวุธฉากที่สาม หรือจะเปิดตะเข็บ ต้องมาที่เทสใบนี้แล้วบอกว่าอันไหน
   นี่คือคำตอบของคำถามที่ adversary ถามท้ายรายงาน ("อะไรจะทำให้การลงทะเบียนฉากถัดไปแดง")

## ของอื่นที่ adversary เจอ และแก้แล้วใน `#728`
- **D2 มิวแทนต์รอด**: `COMPOSER_BG0005 -> _build_bg0015` ผ่าน assertion ที่รอบนี้เพิ่งเขียนเอง
  (มันเทียบแค่ **เซ็ตของคีย์**) และผ่านชุดเทสทั้งชุดโดยไม่มีใบไหนแดง ขณะที่ recompose ของฉาก 5
  กลายเป็น `refused_Bg0015CensusError` เงียบ ๆ = เฟรมหนึ่งรายการที่ RE-092 พิสูจน์ว่าลบทุก actor
  คอมเมนต์ที่รอบนี้เขียนว่า "cannot pick the wrong builder at all" **ผิด และขีดฆ่าไว้ในที่เดิม**
  แก้: builder แต่ละตัวถือ `serves_scene_id` อ่านจากโมดูลตัวเอง · assertion เทียบกับ `_COMPOSERS`
  -> ผิดสายแล้วตายตั้งแต่ import · ตัวมิวแทนต์เองกลายเป็นเทส
- **ช่องที่มันลอดมา**: **ไม่เคยมีใครเรียก `recompose_frames` ให้ฉาก 5 เลย** เทสที่รอบนี้เขียนดูแต่
  dict ของทะเบียน และ drift pin เดิมดูแค่ว่าเลขฉากอยู่ใน `composer_scene_ids()` —
  composer ที่ **ปฏิเสธ** ผ่านทุกใบ · เพิ่ม `Bg0005RecomposeActuallyComposesTest` เรียกของจริง
- **D3 เครื่องมือรายงานศูนย์ทั้งที่มีสาม**: `describe_cross_scene_identity_collisions()` ตอบ `count=0`
  ขณะที่ของจริงมีสาม (`0x2058` Bg0002/Bg0015 · `0x203C` Bg0002/bg0005 · `0x2047` Bg0015/bg0005)
  เพราะ `_KNOWN_SCENE_TABLE_MODULES_FOR_REPORTING` ยังเป็นสองฉากของหลายรอบก่อน ขณะที่ docstring
  **สามที่ในไฟล์เดียวกัน** เขียนว่ามันตาม `_SCENE_TABLE_MODULES` · การลงทะเบียน Bg0015 ทำให้ใบแรก
  เป็นจริงไปแล้วและไม่มีใครเห็น เพราะเครื่องมือที่ใช้ดูคือของที่ค้าง · รอบนี้เติมอีกสอง
  แก้: derive จากทะเบียน · เทสสี่ใบที่ปักศูนย์ไว้ เขียนใหม่ให้ปัก **คู่ที่มีชื่อ** แทนตัวเลข
  (adversary เดินเส้นทาง strike/ledger/rehydration/death/loot แล้วพบว่า scope ด้วย scene ทุกเส้น
  คู่ชนจึงยัง **ไม่** เป็นอันตราย — ข้อสรุปนั้นคงไว้ เปลี่ยนแค่ให้เครื่องมือพูดความจริง)
- **D4** docstring ของ `verify_frozen` อ้างชื่อไฟล์เทสที่ไม่เคยมีอยู่ และบรรยายโค้ด `*_` ที่ไม่มีจริง
  แก้ทั้งสอง พร้อมเขียนข้อจำกัดตรง ๆ: อ่านด้วย index รอดการ **เพิ่มคอลัมน์** แต่ **ไม่** รอดการสลับคอลัมน์
  ซึ่ง unpack แบบเดิมจะโยน · และตัวเรียกจริงถูกเกตด้วย bridge = ไม่รันบนเกต Windows
- **D7** `TABLELESS_SCENE_ID` จะ `StopIteration` ตอน collect วันที่ทุกฉากมี roster · ให้ชื่อความล้มเหลวแล้ว

## ที่ยังไม่แก้ และตั้งใจ (หนี้ของรอบถัดไป)
- **D5** `CONTROL_FINDINGS` ในโมดูลที่ generate มาเป็นตัวควบคุมของ bg0001/CLINE type 2 ใต้หัวข้อที่อ่านว่า
  "controls found at mining time" ของฉากนี้ · จริงกับ bg0015 ด้วย ไม่ใช่แค่ bg0005 · ต้องแก้ generator
  แล้ว regenerate สองโมดูล = ใบของรอบหน้า ไม่ยัดเข้ามาที่นี่
- **D6** บรรทัด UNKILLABLE ของ `describe_widening_coverage` บอก identity แต่ไม่บอกฉาก และ `0x203C`
  ตอนนี้เป็นมอนสองตัว · บรรทัดหัวข้างบนมี `scene=` อยู่ = อ่านได้จากตำแหน่ง แต่ grep ตาม identity ไม่ได้
- **D8** `runtime.py:10760` ยังเขียนว่า "`mob_scene_recompose` has no composer for a lane scene yet"
  ซึ่งเป็นเท็จตั้งแต่ `#727` · **ไฟล์ของ chief · หนึ่งบรรทัดให้ chief** ไม่แตะเอง

## ชุดเทส
ชุดเต็มบนต้นไม้สุดท้าย ใน worktree ที่ไม่มี `pf_bridge` ข้าง ๆ: **8711 passed, 89 skipped,
16803 subtests** · `skip_census` `RESULT: PASS` · preflight cp874/skips/mainmerge PASS บน `78486d4`
· `FUNCTIONAL_COVERAGE PASS domains=8` · `HYPOTHESIS_LEDGER PASS entries=50`
(merge `78486d4` ที่ตามมาหลังรัน นำเข้ามาแต่ `#727` ของรอบนี้เอง และทำให้ต้นไม้เหมือนเดิมทุกไบต์ —
`git diff 016108d HEAD` ว่าง — จึงเป็นต้นไม้เดียวกับที่รันไปแล้ว ไม่ใช่สภาพที่ไม่เคยถูกรัน)

## สถานะ
- `#727` **merge แล้ว** (`78486d4` บน main) พร้อม body ที่ถอนคำอ้างเท็จไว้ในตัว
- claim `#1107` merge แล้ว = ล็อกรอบปลดไปตั้งแต่ก่อนผล adversary คืน
- **push แล้ว รอ merge PR #728** (ผล adversary) · สถานะ PR เซิร์ฟเวอร์: **เปิดแล้ว รอ gate**
- ไฟล์นี้กับใบ CORE-REQUEST อยู่บนกิ่ง `claude/youthful-ride-jqeo2m` ที่ตัดใหม่จาก main
  (กิ่งเดิมถูก merge ไปแล้ว ห้ามต่อยอดบนประวัติที่ merge แล้ว)
