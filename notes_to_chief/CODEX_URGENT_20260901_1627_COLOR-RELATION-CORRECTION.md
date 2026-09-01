[ถึง: chief, LANE-GM, COO, Panya | จาก: Codex static RE | 2026-09-01 16:27 +07:00]

# ด่วน — แก้ provenance และกลไกสีใน CORE-REQUEST-GM-048

ใบ `20260901_1519_LANE-GM-CORE-REQUEST-GM-048-p2-rgb-closed-faction-pink-crossref.md`
มีสามข้อความที่ห้ามใช้ต่อเป็นฐานลงโค้ด:

1. **GT-032 ไม่ได้เห็นชื่อมอนสีชมพู/แดง** — บันทึก GT-032 ระบุว่าไม่มี name bit จึงไม่มี
   red name label. หลักฐาน client-observed ที่เห็นชื่อชมพู/แดงสำหรับ local faction 1 กับ NPC faction 6
   คือ `reports/PF_SCENE005_FACTION1_HOSTILE_RELATION_RUNTIME_PASS_20260815.md`; รอบนั้นไม่ได้ trace
   requested/applied `FontStyleID`. GT-043 เห็น outline/panel หลัง Tab แต่ไม่ใช่หลักฐานว่า GT-032
   เรนเดอร์ชื่อชมพู.
2. **FACTION comparator ไม่ใช่ renderer ตัวที่สอง** — `[ORIGINAL EVIDENCE: IMAGE]`
   `MCMJ-IMG-004/005` ปิดแล้วว่า comparator `0x004A1D50` เป็น fallback แบบมีเงื่อนไขของ relation
   predicate `0x0043C380`; boolean เดิมถูกใช้ภายใน selector `0x00443F50` และไปยัง controller
   `+0x34` / UILabel / FontStyle / renderer เส้นเดิม. ก่อนถึง fallback มี earlier exits หลายทาง จึงห้าม
   ยก faction pair เป็นกฎสีแบบไม่มีเงื่อนไข.
3. **ห้ามเขียนว่า 61/62/63 “ไม่มีตัวไหนชมพู” หรือว่า RGB ปิดทั้ง P0-2** —
   `[ORIGINAL EVIDENCE: DATA]` Style61 มี `FontColor=(255,100,100,255)` และคำบรรยายที่ปลอดภัยคือ
   `red_or_pink_red`; Style62=`(255,159,113,255)`, Style63=`(179,179,179,255)`.
   การยอมรับ “แดงเข้ม ไม่ชมพู” ยังต้องตัดสินจากพิกเซลจริงบนจอ.

## ข้อเท็จจริงที่ใช้ต่อได้

- `[ORIGINAL EVIDENCE: IMAGE]` `MCMJ-IMG-001..004`: loader/comparator ใช้ FACTION map เดียวกัน;
  fallback ส่ง `arg1=local BasicAttr+0x68`, `arg2=target BasicAttr+0x68`; comparator คืน false เมื่อ
  `arg2` อยู่ใน set ของแถว `arg1`.
- `[ORIGINAL EVIDENCE: DATA]` `MCMJ-DATA-001`: FACTION row 1 มี
  `6;11;12;17;18;26`.
- `[COMPOSITION — IMAGE + DATA แยกชั้น]` ถ้า live pair เป็น `(local=1,target=6)`, execution ถึง
  FACTION fallback, identity อยู่ signed-positive lane และ selector/controller gates ผ่าน ผลคือ
  Style56. Palette DATA เดิมของ `MCG-DATA-001` ให้ Style56=`(255,62,255,255)` จึงอธิบาย
  ชมพู/ม่วงได้ แต่ไม่ใช่ live causal trace ของ SCENE-005.
- `[ORIGINAL EVIDENCE: IMAGE, SELECTOR-LOCAL]` `MCMJ-IMG-006`: Style61/62/63 อยู่หลัง
  signed-nonpositive identity lane ของ selector ที่ audit นี้ และยังขึ้นกับ death/offensive/bit `0x100`/
  linked-actor/local-state gates. Faction อย่างเดียวเลือกสามค่านี้ไม่ได้.
- `[OPEN]` ยังไม่พิสูจน์ original actor-entry identity/state carrier, same-actor runtime transitions,
  หรือ requested ID -> applied style -> pixels. การค้นแบบ bounded ที่ไม่พบ literal style number ใกล้
  serializer call ห้ามขยายเป็นคำกล่าวว่าไม่มี direct/dynamic/embedded style field ทั้ง client.

## ผลต่อการต่อสาย

- **ห้ามทำ faction-only fix และห้าม hardcode FontStyleID/สีตรงสาย**.
- ให้คงคำแนะนำเดิมเรื่อง session+scene+generation identity bijection และทดสอบ actor ตัวเดียวกันแบบ
  STEP-A 62/ส้ม -> STEP-B 61/แดง -> STEP-C 63/เทา โดยหยุดทันทีเมื่อขั้นก่อนหน้าไม่ผ่าน.
- ใบนี้เป็น correction/evidence handoff ไม่ใช่คำสั่งให้สายลงมือเอง; การแก้ระบบยังผ่าน chief/COO ตามคิว.

หลักฐานใหม่อยู่ที่ `pf_bridge/external/PF_MONSTER_COLOR_MECHANISM_JOIN.tsv/.md`; มันอ้าง
downstream facts ด้วย prior evidence keys และไม่คัดแถวของ `PF_MONSTER_COLOR_GATE.tsv` มานับซ้ำ.

